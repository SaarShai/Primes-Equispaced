"""Farey-guided densification strategy.

Key differences from ADC:
  - Uses kNN (k=6) spatial neighbors instead of gradient-threshold clone/split
  - Computes adaptive gap threshold (75th percentile of gap ratios)
  - Inserts at mediant positions where gap > threshold AND error is high
  - New Gaussians inherit properties from neighbors (not fixed values)
  - Same opacity reset and pruning schedule as ADC
  - Max insertions per step bounded

The Farey mediant placement:
  For neighboring Gaussians i, j with "denominators" d_i = round(1/scale_i):
    pos_new = (d_j * pos_i + d_i * pos_j) / (d_i + d_j)
  This is the Farey mediant in the fraction lattice.

Level schedule: N = farey_level_start + (step / densify_every)
  A gap is admissible at level N if: d_i + d_j <= N
"""

import math
from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from .config import Config


class FareyStrategy:
    """Farey-guided densification strategy."""

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
        """Resize state tensors to match new Gaussian count."""
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
        """Called before loss.backward(). Retain grad on xys."""
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
        """Called after loss.backward(). Accumulate grads, then Farey densify."""
        if step < self.config.densify_start or step >= self.config.densify_stop:
            return params, optimizers, state

        N = params["means"].shape[0]
        state = self._update_state_size(state, N)

        # Accumulate 2D position gradients (same as ADC, for error gating)
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
            params, optimizers, state = self._farey_densify_and_prune(
                params, optimizers, state, step
            )

        # Opacity reset
        if step > 0 and step % self.config.opacity_reset_every == 0:
            params = self._reset_opacity(params, optimizers)

        return params, optimizers, state

    def _farey_densify_and_prune(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
        state: Dict[str, Tensor],
        step: int,
    ) -> Tuple[Dict[str, Tensor], Dict[str, torch.optim.Adam], Dict[str, Tensor]]:
        """Farey-guided densification + pruning."""
        N = params["means"].shape[0]
        means = params["means"].detach()        # (N, 3)
        scales = torch.exp(params["scales"].detach())  # (N, 3) activated

        # Farey level schedule
        farey_level = self.config.farey_level_start + (step // self.config.densify_every)

        # Average gradient for error gating
        count = state["grad_count"].squeeze(-1).float().clamp(min=1)
        avg_grad = state["grad_accum"].norm(dim=-1) / count  # (N,)

        # ---- Step 1: kNN spatial neighbors ----
        k = self.config.farey_knn_k
        nn_indices, nn_dists = self._knn(means, k)  # (N, k), (N, k)

        # ---- Step 2: Compute denominators (reciprocal of spatial extent) ----
        # Use max scale as the "size" of each Gaussian
        scale_max = scales.max(dim=-1).values  # (N,)
        denominators = torch.round(1.0 / scale_max.clamp(min=1e-6))  # (N,)
        denominators = denominators.clamp(min=1, max=1000)

        # ---- Step 3: Compute gap ratios for each neighbor pair ----
        # gap_ratio = distance / (scale_i + scale_j)
        # This measures how "spread out" the pair is relative to their sizes
        scale_i = scale_max.unsqueeze(1).expand(-1, k)          # (N, k)
        scale_j = scale_max[nn_indices]                         # (N, k)
        gap_ratio = nn_dists / (scale_i + scale_j + 1e-8)      # (N, k)

        # ---- Step 4: Adaptive gap threshold ----
        gap_threshold = torch.quantile(
            gap_ratio[gap_ratio > 0].flatten(),
            self.config.farey_gap_percentile / 100.0,
        ).item()

        # ---- Step 5: Farey admission criterion ----
        denom_i = denominators.unsqueeze(1).expand(-1, k)       # (N, k)
        denom_j = denominators[nn_indices]                       # (N, k)
        denom_sum = denom_i + denom_j

        admissible = denom_sum <= farey_level                    # (N, k) bool
        large_gap = gap_ratio > gap_threshold                    # (N, k) bool

        # ---- Step 6: Error gating ----
        # Only densify where gradient indicates high error
        high_error = avg_grad > self.config.farey_error_threshold  # (N,)
        # At least one of the pair should have high error
        error_i = high_error.unsqueeze(1).expand(-1, k)          # (N, k)
        error_j = high_error[nn_indices]                          # (N, k)
        error_gate = error_i | error_j                            # (N, k)

        # ---- Step 7: Select gaps to fill ----
        insert_mask = admissible & large_gap & error_gate         # (N, k)

        # Avoid duplicate insertions: only insert for i < j
        idx_i = torch.arange(N, device=self.device).unsqueeze(1).expand(-1, k)
        insert_mask = insert_mask & (idx_i < nn_indices)

        # Flatten and limit insertions
        insert_pairs = insert_mask.nonzero()  # (M, 2) where col0=gaussian_idx, col1=neighbor_slot
        max_insert = self.config.farey_max_insertions_per_step
        if insert_pairs.shape[0] > max_insert:
            # Prioritize by gap ratio (largest gaps first)
            gap_vals = gap_ratio[insert_mask]
            _, top_indices = gap_vals.topk(min(max_insert, gap_vals.shape[0]))
            all_insert_flat = insert_mask.nonzero()
            insert_pairs = all_insert_flat[top_indices]

        n_insert = insert_pairs.shape[0]

        if n_insert > 0:
            # ---- Step 8: Compute mediant positions ----
            i_indices = insert_pairs[:, 0]                        # (M,)
            k_slots = insert_pairs[:, 1]                          # (M,)
            j_indices = nn_indices[i_indices, k_slots]            # (M,)

            pos_i = means[i_indices]                              # (M, 3)
            pos_j = means[j_indices]                              # (M, 3)
            d_i = denominators[i_indices].unsqueeze(1)            # (M, 1)
            d_j = denominators[j_indices].unsqueeze(1)            # (M, 1)

            # Farey mediant position
            new_means = (d_j * pos_i + d_i * pos_j) / (d_i + d_j)  # (M, 3)

            # ---- Step 9: Inherit properties from neighbors ----
            # Scale: average of neighbors, slightly smaller
            scale_i_full = params["scales"].detach()[i_indices]   # (M, 3) log
            scale_j_full = params["scales"].detach()[j_indices]   # (M, 3) log
            new_scales = (scale_i_full + scale_j_full) / 2.0 - math.log(1.2)

            # Rotation: copy from nearest neighbor (i)
            new_quats = params["quats"].detach()[i_indices]       # (M, 4)

            # Opacity: average of neighbors (in logit space)
            new_opacities = (
                params["opacities"].detach()[i_indices] +
                params["opacities"].detach()[j_indices]
            ) / 2.0                                               # (M, 1)

            # SH: average of neighbors
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

        # ---- Prune low-opacity Gaussians ----
        opacities = torch.sigmoid(params["opacities"].squeeze(-1))
        prune_mask = opacities < self.config.opacity_prune_threshold

        n_prune = 0
        if prune_mask.any():
            n_prune = prune_mask.sum().item()
            keep_mask = ~prune_mask
            params = {k: v[keep_mask] for k, v in params.items()}
            optimizers = self._rebuild_optimizers(optimizers, params)

        # Reset state
        new_N = params["means"].shape[0]
        state = self.initialize_state(new_N)

        print(f"  [Farey] step={step}: level={farey_level}, insert={n_insert}, "
              f"prune={n_prune}, total={new_N}")

        return params, optimizers, state

    def _knn(self, points: Tensor, k: int) -> Tuple[Tensor, Tensor]:
        """Compute k-nearest neighbors using chunked distance computation.

        Args:
            points: (N, 3) positions
            k: number of neighbors

        Returns:
            indices: (N, k) neighbor indices
            dists: (N, k) distances
        """
        N = points.shape[0]
        k = min(k, N - 1)

        if N <= 50_000:
            # Direct computation
            dists_sq = torch.cdist(points, points, p=2.0) ** 2  # Would be cleaner with p=2
            # Actually, torch.cdist returns distances, not squared
            dists = torch.cdist(points, points, p=2.0)  # (N, N)
            dists.fill_diagonal_(float("inf"))
            nn_dists, nn_indices = dists.topk(k, dim=-1, largest=False)
            return nn_indices, nn_dists
        else:
            # Chunked for memory efficiency
            chunk_size = 10_000
            all_indices = []
            all_dists = []
            for i in range(0, N, chunk_size):
                end = min(i + chunk_size, N)
                chunk = points[i:end]  # (C, 3)
                dists = torch.cdist(chunk, points, p=2.0)  # (C, N)
                # Zero out self-distances
                for j in range(end - i):
                    dists[j, i + j] = float("inf")
                nn_dists, nn_idx = dists.topk(k, dim=-1, largest=False)
                all_indices.append(nn_idx)
                all_dists.append(nn_dists)
            return torch.cat(all_indices, dim=0), torch.cat(all_dists, dim=0)

    def _reset_opacity(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
    ) -> Dict[str, Tensor]:
        """Reset all opacities to a low value."""
        new_opacity = torch.full_like(params["opacities"], -4.595)
        params["opacities"] = new_opacity.requires_grad_(True)
        optimizers["opacities"] = torch.optim.Adam(
            [params["opacities"]], lr=self.config.lr_opacities, eps=1e-15
        )
        print(f"  [Farey] Opacity reset")
        return params

    def _concat_params(
        self,
        params: Dict[str, Tensor],
        new_params: Dict[str, Tensor],
    ) -> Dict[str, Tensor]:
        """Concatenate new parameters to existing ones."""
        result = {}
        for k in params:
            result[k] = torch.cat([
                params[k].detach(),
                new_params[k].detach(),
            ], dim=0).requires_grad_(True)
        return result

    def _rebuild_optimizers(
        self,
        optimizers: Dict[str, torch.optim.Adam],
        params: Dict[str, Tensor],
    ) -> Dict[str, torch.optim.Adam]:
        """Rebuild all optimizers for current parameters."""
        cfg = self.config
        lr_map = {
            "means": cfg.lr_means,
            "scales": cfg.lr_scales,
            "quats": cfg.lr_quats,
            "opacities": cfg.lr_opacities,
            "sh_coeffs": cfg.lr_sh_dc,
        }
        new_optimizers = {}
        for name, param in params.items():
            new_optimizers[name] = torch.optim.Adam(
                [param], lr=lr_map[name], eps=1e-15
            )
        return new_optimizers
