"""Midpoint ablation strategy: gap-filling WITHOUT Farey math.

Same as Farey strategy but:
  - No denominator mapping (no d_i = round(1/scale_i))
  - No admission criterion (no d_i + d_j <= N level schedule)
  - Simple midpoint instead of weighted mediant
  - Still uses gap threshold + error gating

This isolates whether the Farey mediant math adds value
over simple error-guided gap-filling.
"""

import math
from typing import Dict, Tuple

import torch
from torch import Tensor

from .config import Config


class MidpointStrategy:
    """Midpoint gap-filling densification (Farey ablation baseline)."""

    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device(config.device)

    def initialize_state(self, num_gaussians: int) -> Dict[str, Tensor]:
        """Initialize state tracking."""
        return {
            "grad_accum": torch.zeros(num_gaussians, 2, device=self.device),
            "grad_count": torch.zeros(num_gaussians, 1, device=self.device, dtype=torch.int32),
            "max_radii": torch.zeros(num_gaussians, device=self.device),
        }

    def _update_state_size(self, state: Dict[str, Tensor], new_size: int):
        """Resize state tensors."""
        old_size = state["grad_accum"].shape[0]
        if new_size == old_size:
            return state

        for key in ["grad_accum"]:
            old = state[key]
            if new_size > old_size:
                state[key] = torch.cat([old, torch.zeros(new_size - old_size, old.shape[1], device=self.device)], dim=0)
            else:
                state[key] = old[:new_size]

        for key in ["grad_count"]:
            old = state[key]
            if new_size > old_size:
                state[key] = torch.cat([old, torch.zeros(new_size - old_size, 1, device=self.device, dtype=torch.int32)], dim=0)
            else:
                state[key] = old[:new_size]

        for key in ["max_radii"]:
            old = state[key]
            if new_size > old_size:
                state[key] = torch.cat([old, torch.zeros(new_size - old_size, device=self.device)], dim=0)
            else:
                state[key] = old[:new_size]

        return state

    def step_pre_backward(
        self,
        params: Dict[str, Tensor],
        state: Dict[str, Tensor],
        step: int,
        xys: Tensor,
        radii: Tensor,
    ):
        """Called before loss.backward()."""
        if step >= self.config.densify_start and step < self.config.densify_stop:
            xys.retain_grad()

    def step_post_backward(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
        state: Dict[str, Tensor],
        step: int,
        xys: Tensor,
        radii: Tensor,
    ) -> Tuple[Dict[str, Tensor], Dict[str, torch.optim.Adam], Dict[str, Tensor]]:
        """Called after loss.backward()."""
        if step < self.config.densify_start or step >= self.config.densify_stop:
            return params, optimizers, state

        N = params["means"].shape[0]
        state = self._update_state_size(state, N)

        # Accumulate gradients
        if xys.grad is not None:
            visible = (radii.squeeze(-1) if radii.dim() > 1 else radii) > 0
            state["max_radii"][visible] = torch.max(
                state["max_radii"][visible],
                (radii.squeeze(-1) if radii.dim() > 1 else radii)[visible].float(),
            )
            state["grad_accum"][visible] += xys.grad.detach()[visible]
            state["grad_count"][visible] += 1

        # Densification step
        if step > 0 and step % self.config.densify_every == 0:
            params, optimizers, state = self._midpoint_densify_and_prune(
                params, optimizers, state, step
            )

        # Opacity reset
        if step > 0 and step % self.config.opacity_reset_every == 0:
            params = self._reset_opacity(params, optimizers)

        return params, optimizers, state

    def _midpoint_densify_and_prune(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
        state: Dict[str, Tensor],
        step: int,
    ) -> Tuple[Dict[str, Tensor], Dict[str, torch.optim.Adam], Dict[str, Tensor]]:
        """Midpoint gap-filling + pruning."""
        N = params["means"].shape[0]
        means = params["means"].detach()
        scales = torch.exp(params["scales"].detach())

        # Average gradient for error gating
        count = state["grad_count"].squeeze(-1).float().clamp(min=1)
        avg_grad = state["grad_accum"].norm(dim=-1) / count

        # ---- kNN neighbors ----
        k = self.config.midpoint_knn_k
        nn_indices, nn_dists = self._knn(means, k)

        # ---- Gap ratios ----
        scale_max = scales.max(dim=-1).values
        scale_i = scale_max.unsqueeze(1).expand(-1, k)
        scale_j = scale_max[nn_indices]
        gap_ratio = nn_dists / (scale_i + scale_j + 1e-8)

        # ---- Gap threshold ----
        gap_threshold = torch.quantile(
            gap_ratio[gap_ratio > 0].flatten(),
            self.config.midpoint_gap_percentile / 100.0,
        ).item()

        large_gap = gap_ratio > gap_threshold

        # ---- Error gating (same as Farey) ----
        high_error = avg_grad > self.config.midpoint_error_threshold
        error_i = high_error.unsqueeze(1).expand(-1, k)
        error_j = high_error[nn_indices]
        error_gate = error_i | error_j

        # ---- NO Farey admission criterion (this is the ablation) ----
        insert_mask = large_gap & error_gate

        # Avoid duplicates
        idx_i = torch.arange(N, device=self.device).unsqueeze(1).expand(-1, k)
        insert_mask = insert_mask & (idx_i < nn_indices)

        # Limit insertions
        insert_pairs = insert_mask.nonzero()
        max_insert = self.config.midpoint_max_insertions_per_step
        if insert_pairs.shape[0] > max_insert:
            gap_vals = gap_ratio[insert_mask]
            _, top_indices = gap_vals.topk(min(max_insert, gap_vals.shape[0]))
            all_insert_flat = insert_mask.nonzero()
            insert_pairs = all_insert_flat[top_indices]

        n_insert = insert_pairs.shape[0]

        if n_insert > 0:
            i_indices = insert_pairs[:, 0]
            k_slots = insert_pairs[:, 1]
            j_indices = nn_indices[i_indices, k_slots]

            pos_i = means[i_indices]
            pos_j = means[j_indices]

            # ---- SIMPLE MIDPOINT (not Farey mediant) ----
            new_means = (pos_i + pos_j) / 2.0

            # Inherit properties (same as Farey)
            scale_i_full = params["scales"].detach()[i_indices]
            scale_j_full = params["scales"].detach()[j_indices]
            new_scales = (scale_i_full + scale_j_full) / 2.0 - math.log(1.2)

            new_quats = params["quats"].detach()[i_indices]

            new_opacities = (
                params["opacities"].detach()[i_indices] +
                params["opacities"].detach()[j_indices]
            ) / 2.0

            new_sh = (
                params["sh_coeffs"].detach()[i_indices] +
                params["sh_coeffs"].detach()[j_indices]
            ) / 2.0

            new_params = {
                "means": new_means,
                "scales": new_scales,
                "quats": new_quats,
                "opacities": new_opacities,
                "sh_coeffs": new_sh,
            }

            params = self._concat_params(params, new_params)
            optimizers = self._rebuild_optimizers(optimizers, params)

        # Prune
        opacities = torch.sigmoid(params["opacities"].squeeze(-1))
        prune_mask = opacities < self.config.opacity_prune_threshold

        n_prune = 0
        if prune_mask.any():
            n_prune = prune_mask.sum().item()
            keep_mask = ~prune_mask
            params = {k: v[keep_mask] for k, v in params.items()}
            optimizers = self._rebuild_optimizers(optimizers, params)

        new_N = params["means"].shape[0]
        state = self.initialize_state(new_N)

        print(f"  [Midpoint] step={step}: insert={n_insert}, "
              f"prune={n_prune}, total={new_N}")

        return params, optimizers, state

    def _knn(self, points: Tensor, k: int) -> Tuple[Tensor, Tensor]:
        """Compute k-nearest neighbors."""
        N = points.shape[0]
        k = min(k, N - 1)

        if N <= 50_000:
            dists = torch.cdist(points, points, p=2.0)
            dists.fill_diagonal_(float("inf"))
            nn_dists, nn_indices = dists.topk(k, dim=-1, largest=False)
            return nn_indices, nn_dists
        else:
            chunk_size = 10_000
            all_indices = []
            all_dists = []
            for i in range(0, N, chunk_size):
                end = min(i + chunk_size, N)
                chunk = points[i:end]
                dists = torch.cdist(chunk, points, p=2.0)
                for j in range(end - i):
                    dists[j, i + j] = float("inf")
                nn_dists, nn_idx = dists.topk(k, dim=-1, largest=False)
                all_indices.append(nn_idx)
                all_dists.append(nn_dists)
            return torch.cat(all_indices, dim=0), torch.cat(all_dists, dim=0)

    def _reset_opacity(self, params, optimizers):
        new_opacity = torch.full_like(params["opacities"], -4.595)
        params["opacities"] = new_opacity.requires_grad_(True)
        optimizers["opacities"] = torch.optim.Adam(
            [params["opacities"]], lr=self.config.lr_opacities, eps=1e-15
        )
        print(f"  [Midpoint] Opacity reset")
        return params

    def _concat_params(self, params, new_params):
        result = {}
        for k in params:
            result[k] = torch.cat([
                params[k].detach(), new_params[k].detach(),
            ], dim=0).requires_grad_(True)
        return result

    def _rebuild_optimizers(self, optimizers, params):
        cfg = self.config
        lr_map = {
            "means": cfg.lr_means, "scales": cfg.lr_scales,
            "quats": cfg.lr_quats, "opacities": cfg.lr_opacities,
            "sh_coeffs": cfg.lr_sh_dc,
        }
        return {
            name: torch.optim.Adam([param], lr=lr_map[name], eps=1e-15)
            for name, param in params.items()
        }
