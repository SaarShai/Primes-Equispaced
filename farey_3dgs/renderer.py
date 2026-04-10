"""Renderer wrapping gsplat-mps project_gaussians and rasterize_gaussians.

Handles:
  - Building viewmat/projmat from COLMAP camera extrinsics
  - Computing tile bounds
  - SH evaluation for view-dependent color
  - Returning rendered image + alpha + projection info for densification
"""

import math
import sys
from typing import Dict, NamedTuple, Optional, Tuple

import numpy as np
import torch
from torch import Tensor

from .config import Config


class RenderOutput(NamedTuple):
    """Output from rendering a single view."""
    image: Tensor               # (H, W, 3) rendered image in [0, 1]
    alpha: Tensor               # (H, W) alpha channel
    xys: Tensor                 # (N, 2) 2D projected positions (for grad tracking)
    radii: Tensor               # (N,) radii of 2D projections
    depths: Tensor              # (N,) depths
    num_tiles_hit: Tensor       # (N,) tiles hit per Gaussian


class Renderer:
    """Wrapper around gsplat-mps rasterization."""

    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device(config.device)

        # Import gsplat-mps
        if config.gsplat_dir not in sys.path:
            sys.path.insert(0, config.gsplat_dir)

        from gsplat.project_gaussians import project_gaussians
        from gsplat.rasterize import rasterize_gaussians
        from gsplat.sh import spherical_harmonics, num_sh_bases

        self._project_gaussians = project_gaussians
        self._rasterize_gaussians = rasterize_gaussians
        self._spherical_harmonics = spherical_harmonics
        self._num_sh_bases = num_sh_bases

        self.background = torch.zeros(3, device=self.device)

    def render(
        self,
        means: Tensor,          # (N, 3)
        scales: Tensor,         # (N, 3) log-space
        quats: Tensor,          # (N, 4)
        opacities: Tensor,      # (N, 1) logit-space
        sh_coeffs: Tensor,      # (N, K, 3)
        viewmat: Tensor,        # (4, 4) world-to-camera
        fx: float,
        fy: float,
        cx: float,
        cy: float,
        img_height: int,
        img_width: int,
        sh_degree: int,
        background: Optional[Tensor] = None,
    ) -> RenderOutput:
        """Render a single view.

        Args:
            means: 3D Gaussian centers
            scales: Log-space scales (exp applied internally)
            quats: Rotation quaternions [w, x, y, z]
            opacities: Logit-space opacities (sigmoid applied internally)
            sh_coeffs: SH coefficients (N, K, 3)
            viewmat: 4x4 world-to-camera matrix
            fx, fy, cx, cy: Camera intrinsics
            img_height, img_width: Output image dimensions
            sh_degree: Active SH degree
            background: Background color (default: black)

        Returns:
            RenderOutput with rendered image, alpha, and projection info.
        """
        if background is None:
            background = self.background

        N = means.shape[0]

        # Tile bounds
        BLOCK_X = self.config.block_x
        BLOCK_Y = self.config.block_y
        tile_bounds = (
            (img_width + BLOCK_X - 1) // BLOCK_X,
            (img_height + BLOCK_Y - 1) // BLOCK_Y,
            1,
        )

        # Build projection matrix from intrinsics
        # gsplat-mps uses viewmat as both view and projection in simple_trainer
        # For proper perspective: we need a projmat
        # Looking at simple_trainer.py, it passes viewmat as both viewmat and projmat
        # This works because project_gaussians uses focal length params directly
        projmat = viewmat  # gsplat v0.1.3 uses focal params, projmat is just for clipping

        # Activate scales and opacities
        activated_scales = torch.exp(scales)
        activated_opacities = torch.sigmoid(opacities)

        # Project Gaussians to 2D
        # Returns: xys, depths, radii, conics, num_tiles_hit, cov3d
        xys, depths, radii, conics, num_tiles_hit, cov3d = self._project_gaussians(
            means3d=means,
            scales=activated_scales,
            glob_scale=self.config.glob_scale,
            quats=quats,
            viewmat=viewmat,
            projmat=projmat,
            fx=fx,
            fy=fy,
            cx=cx,
            cy=cy,
            img_height=img_height,
            img_width=img_width,
            tile_bounds=tile_bounds,
            clip_thresh=self.config.clip_thresh,
        )

        # Compute view-dependent colors via SH
        # viewdirs = normalize(cam_center - means)
        # cam_center = -R^T @ t (from viewmat)
        R = viewmat[:3, :3]  # (3, 3)
        t = viewmat[:3, 3]   # (3,)
        cam_center = -R.T @ t  # (3,)

        viewdirs = cam_center[None, :] - means  # (N, 3)
        viewdirs = viewdirs / (viewdirs.norm(dim=-1, keepdim=True) + 1e-8)

        # Evaluate SH
        if sh_degree > 0:
            colors = self._spherical_harmonics(sh_degree, viewdirs, sh_coeffs)
            colors = colors + 0.5  # DC offset
            colors = torch.clamp(colors, 0.0, 1.0)
        else:
            # Degree 0: just use DC component directly
            # sh_coeffs[:, 0, :] is the DC coefficient
            C0 = 0.28209479177387814
            colors = sh_coeffs[:, 0, :] * C0 + 0.5
            colors = torch.clamp(colors, 0.0, 1.0)

        # Rasterize
        # Filter to visible Gaussians (radii > 0)
        visible_mask = radii.squeeze(-1) > 0 if radii.dim() > 1 else radii > 0

        out = self._rasterize_gaussians(
            xys=xys,
            depths=depths,
            radii=radii,
            conics=conics,
            num_tiles_hit=num_tiles_hit,
            colors=colors,
            opacity=activated_opacities,
            img_height=img_height,
            img_width=img_width,
            background=background,
            return_alpha=True,
        )

        # rasterize_gaussians with return_alpha=True returns (out_img, out_alpha)
        out_img, out_alpha = out

        return RenderOutput(
            image=out_img,          # (H, W, 3)
            alpha=out_alpha,        # (H, W)
            xys=xys,               # (N, 2)
            radii=radii,           # (N,)
            depths=depths,          # (N,)
            num_tiles_hit=num_tiles_hit,
        )


def numpy_w2c_to_tensor(w2c: np.ndarray, device: torch.device) -> Tensor:
    """Convert a numpy 4x4 world-to-camera matrix to a float32 tensor."""
    return torch.tensor(w2c, dtype=torch.float32, device=device)
