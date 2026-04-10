"""Standard ADC (Adaptive Density Control) densification strategy.

Implements the densification logic from Kerbl et al. (3D Gaussian Splatting, 2023):
  1. Track 2D position gradients accumulated over iterations
  2. Clone small Gaussians with high gradient (size < threshold)
  3. Split large Gaussians with high gradient (size >= threshold)
  4. Prune low-opacity Gaussians (< 0.005)
  5. Reset opacity every 3000 iterations
  6. Active from iter 500 to iter 15000, every 100 iterations
"""

import math
from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from .config import Config


class ADCStrategy:
    """Adaptive Density Control densification strategy."""

    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device(config.device)

    def initialize_state(self, num_gaussians: int) -> Dict[str, Tensor]:
        """Initialize gradient accumulation state."""
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

        if new_size > old_size:
            # Extend with zeros
            extra = new_size - old_size
            state["grad_accum"] = torch.cat([
                state["grad_accum"],
                torch.zeros(extra, 2, device=self.device),
            ], dim=0)
            state["grad_count"] = torch.cat([
                state["grad_count"],
                torch.zeros(extra, 1, device=self.device, dtype=torch.int32),
            ], dim=0)
            state["max_radii"] = torch.cat([
                state["max_radii"],
                torch.zeros(extra, device=self.device),
            ], dim=0)
        else:
            # Truncate
            state["grad_accum"] = state["grad_accum"][:new_size]
            state["grad_count"] = state["grad_count"][:new_size]
            state["max_radii"] = state["max_radii"][:new_size]

        return state

    def step_pre_backward(
        self,
        params: Dict[str, Tensor],
        state: Dict[str, Tensor],
        step: int,
        xys: Tensor,
        radii: Tensor,
    ):
        """Called before loss.backward(). Retain grad on xys for tracking."""
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
        """Called after loss.backward().

        Accumulate gradients, then periodically densify and prune.
        """
        if step < self.config.densify_start or step >= self.config.densify_stop:
            return params, optimizers, state

        N = params["means"].shape[0]

        # Ensure state matches current size
        state = self._update_state_size(state, N)

        # Accumulate 2D position gradients
        if xys.grad is not None:
            grad_norms = xys.grad.detach().norm(dim=-1, keepdim=False)  # (N,)
            # Update max radii
            visible = (radii.squeeze(-1) if radii.dim() > 1 else radii) > 0
            state["max_radii"][visible] = torch.max(
                state["max_radii"][visible],
                (radii.squeeze(-1) if radii.dim() > 1 else radii)[visible].float(),
            )
            # Accumulate gradients
            state["grad_accum"][visible] += xys.grad.detach()[visible]
            state["grad_count"][visible] += 1

        # Densification step
        if step > 0 and step % self.config.densify_every == 0:
            params, optimizers, state = self._densify_and_prune(
                params, optimizers, state, step
            )

        # Opacity reset
        if step > 0 and step % self.config.opacity_reset_every == 0:
            params = self._reset_opacity(params, optimizers)

        return params, optimizers, state

    def _densify_and_prune(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
        state: Dict[str, Tensor],
        step: int,
    ) -> Tuple[Dict[str, Tensor], Dict[str, torch.optim.Adam], Dict[str, Tensor]]:
        """Perform one round of densification (clone/split) and pruning."""
        N = params["means"].shape[0]

        # Compute average gradient magnitude
        count = state["grad_count"].squeeze(-1).float().clamp(min=1)
        avg_grad = state["grad_accum"].norm(dim=-1) / count  # (N,)

        # High gradient mask
        high_grad = avg_grad >= self.config.grad_threshold

        # Scale magnitude (max across 3 axes)
        scales = torch.exp(params["scales"])  # activated scales
        scale_max = scales.max(dim=-1).values

        # Determine split threshold from scene extent
        # Use percentile of current scales as threshold
        scale_threshold = torch.quantile(scale_max, 0.75).item() * self.config.split_scale_threshold / 0.01

        # Actually: standard 3DGS uses a fixed percent_dense parameter
        # We use a simpler heuristic: split if scale > median, clone otherwise
        is_large = scale_max > torch.quantile(scale_max, 0.5)

        # Clone candidates: high grad AND small
        clone_mask = high_grad & ~is_large
        # Split candidates: high grad AND large
        split_mask = high_grad & is_large

        n_clone = clone_mask.sum().item()
        n_split = split_mask.sum().item()

        # --- Clone: duplicate the Gaussian ---
        if n_clone > 0:
            clone_params = {k: v[clone_mask].clone() for k, v in params.items()}
            params = self._concat_params(params, clone_params)
            optimizers = self._extend_optimizers(optimizers, clone_mask, params)

        # --- Split: replace large Gaussian with two smaller ones ---
        if n_split > 0:
            params, optimizers = self._split_gaussians(
                params, optimizers, split_mask, scales
            )

        # --- Prune low-opacity Gaussians ---
        opacities = torch.sigmoid(params["opacities"].squeeze(-1))
        prune_mask = opacities < self.config.opacity_prune_threshold

        if prune_mask.any():
            keep_mask = ~prune_mask
            params = {k: v[keep_mask] for k, v in params.items()}
            optimizers = self._prune_optimizers(optimizers, keep_mask)

        # Reset gradient accumulation state
        new_N = params["means"].shape[0]
        state = self.initialize_state(new_N)

        n_prune = prune_mask.sum().item() if prune_mask.any() else 0
        print(f"  [ADC] step={step}: clone={n_clone}, split={n_split}, "
              f"prune={n_prune}, total={new_N}")

        return params, optimizers, state

    def _split_gaussians(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
        split_mask: Tensor,
        scales: Tensor,
    ) -> Tuple[Dict[str, Tensor], Dict[str, torch.optim.Adam]]:
        """Split large Gaussians into two smaller ones."""
        n_split = split_mask.sum().item()

        # Get parameters of Gaussians to split
        split_means = params["means"][split_mask]           # (M, 3)
        split_scales = params["scales"][split_mask]         # (M, 3) log-space
        split_quats = params["quats"][split_mask]           # (M, 4)
        split_opacities = params["opacities"][split_mask]   # (M, 1)
        split_sh = params["sh_coeffs"][split_mask]          # (M, K, 3)

        # Activated scales for sampling offset
        act_scales = torch.exp(split_scales)  # (M, 3)

        # Sample offset along principal axis
        # Use scales as standard deviation for the offset
        samples = torch.randn(n_split, 3, device=self.device)
        offsets = samples * act_scales  # (M, 3)

        # New Gaussian 1: original position + offset, reduced scale
        new_means_1 = split_means + offsets
        new_scales_1 = split_scales - math.log(1.6)  # Reduce by factor 1.6

        # New Gaussian 2: original position - offset, reduced scale
        new_means_2 = split_means - offsets
        new_scales_2 = split_scales - math.log(1.6)

        # Stack new Gaussians
        new_params = {
            "means": torch.cat([new_means_1, new_means_2], dim=0),
            "scales": torch.cat([new_scales_1, new_scales_2], dim=0),
            "quats": torch.cat([split_quats, split_quats], dim=0),
            "opacities": torch.cat([split_opacities, split_opacities], dim=0),
            "sh_coeffs": torch.cat([split_sh, split_sh], dim=0),
        }

        # Remove originals, add new
        keep_mask = ~split_mask
        params = {k: v[keep_mask] for k, v in params.items()}
        params = self._concat_params(params, new_params)

        # Rebuild optimizers for new parameter set
        optimizers = self._rebuild_optimizers(optimizers, params)

        return params, optimizers

    def _reset_opacity(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
    ) -> Dict[str, Tensor]:
        """Reset all opacities to a low value."""
        # inverse_sigmoid(0.01) ~ -4.595
        new_opacity = torch.full_like(params["opacities"], -4.595)
        params["opacities"] = new_opacity.requires_grad_(True)

        # Reset optimizer state for opacities
        optimizers["opacities"] = torch.optim.Adam(
            [params["opacities"]], lr=self.config.lr_opacities, eps=1e-15
        )

        print(f"  [ADC] Opacity reset")
        return params

    # -----------------------------------------------------------------------
    # Optimizer management helpers
    # -----------------------------------------------------------------------

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

    def _extend_optimizers(
        self,
        optimizers: Dict[str, torch.optim.Adam],
        clone_mask: Tensor,
        params: Dict[str, Tensor],
    ) -> Dict[str, torch.optim.Adam]:
        """Rebuild optimizers after cloning (simple approach)."""
        return self._rebuild_optimizers(optimizers, params)

    def _prune_optimizers(
        self,
        optimizers: Dict[str, torch.optim.Adam],
        keep_mask: Tensor,
    ) -> Dict[str, torch.optim.Adam]:
        """Prune optimizer state to match kept Gaussians.

        For simplicity, we rebuild optimizers. The Adam momentum is lost,
        which is acceptable since pruning happens infrequently.
        """
        # We cannot easily keep per-param optimizer state with masking,
        # so we rebuild. This is what many 3DGS implementations do.
        return optimizers  # Will be rebuilt in trainer

    def _rebuild_optimizers(
        self,
        optimizers: Dict[str, torch.optim.Adam],
        params: Dict[str, Tensor],
    ) -> Dict[str, torch.optim.Adam]:
        """Rebuild all optimizers for the current parameter tensors."""
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
