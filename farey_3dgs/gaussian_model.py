"""3D Gaussian model with all standard parameters.

Parameters per Gaussian:
  - means:     (N, 3)  3D position
  - scales:    (N, 3)  log-space scales (exp applied before use)
  - quats:     (N, 4)  rotation quaternions [w, x, y, z]
  - opacities: (N, 1)  logit-space opacity (sigmoid applied before use)
  - sh_coeffs: (N, K, 3)  spherical harmonic coefficients, K = (max_degree+1)^2

Initialize from SfM point cloud.
"""

import math
from typing import Dict, Optional

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor

from .config import Config


def inverse_sigmoid(x: float) -> float:
    """Inverse of sigmoid function."""
    return math.log(x / (1.0 - x))


def random_quats(n: int) -> Tensor:
    """Generate N random unit quaternions [w, x, y, z]."""
    u = torch.rand(n, 1)
    v = torch.rand(n, 1)
    w = torch.rand(n, 1)
    quats = torch.cat([
        torch.sqrt(1.0 - u) * torch.sin(2.0 * math.pi * v),
        torch.sqrt(1.0 - u) * torch.cos(2.0 * math.pi * v),
        torch.sqrt(u) * torch.sin(2.0 * math.pi * w),
        torch.sqrt(u) * torch.cos(2.0 * math.pi * w),
    ], dim=-1)
    return quats


def rgb_to_sh0(rgb: np.ndarray) -> np.ndarray:
    """Convert RGB [0,1] to degree-0 SH coefficient.

    SH basis Y_00 = 0.28209479...
    color = sh_coeff * Y_00 => sh_coeff = color / Y_00
    """
    C0 = 0.28209479177387814
    return (rgb - 0.5) / C0


class GaussianModel:
    """Container for all Gaussian parameters with optimizer setup."""

    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device(config.device)
        self.active_sh_degree = 0
        self.max_sh_degree = config.sh_degree_max
        self.num_sh_coeffs = (config.sh_degree_max + 1) ** 2  # 16 for degree 3

        # Parameters (initialized in init_from_sfm or init_random)
        self.means: Optional[Tensor] = None
        self.scales: Optional[Tensor] = None
        self.quats: Optional[Tensor] = None
        self.opacities: Optional[Tensor] = None
        self.sh_coeffs: Optional[Tensor] = None  # (N, K, 3)

    @property
    def num_gaussians(self) -> int:
        if self.means is None:
            return 0
        return self.means.shape[0]

    def init_from_sfm(self, points_xyz: np.ndarray, points_rgb: np.ndarray):
        """Initialize Gaussians from SfM point cloud.

        Args:
            points_xyz: (N, 3) float64 point positions
            points_rgb: (N, 3) float64 colors in [0, 1]
        """
        n = points_xyz.shape[0]
        print(f"[GaussianModel] Initializing {n} Gaussians from SfM points")

        # Means: directly from SfM
        self.means = torch.tensor(points_xyz, dtype=torch.float32, device=self.device)

        # Scales: initialize from local point density
        # Compute average distance to 3 nearest neighbors for each point
        # Use a simple heuristic: log of avg nn distance
        dists = self._compute_nn_dists(points_xyz, k=3)
        avg_dist = np.mean(dists, axis=1)  # (N,)
        avg_dist = np.clip(avg_dist, 1e-7, None)
        log_scales = np.log(avg_dist)[:, None].repeat(3, axis=1)  # (N, 3)
        self.scales = torch.tensor(log_scales, dtype=torch.float32, device=self.device)

        # Rotations: identity quaternion [1, 0, 0, 0]
        self.quats = torch.zeros(n, 4, dtype=torch.float32, device=self.device)
        self.quats[:, 0] = 1.0

        # Opacities: logit(0.1) ~ -2.197
        init_opacity = inverse_sigmoid(0.1)
        self.opacities = torch.full(
            (n, 1), init_opacity, dtype=torch.float32, device=self.device
        )

        # SH coefficients: degree-0 from RGB, rest zero
        sh_coeffs = torch.zeros(n, self.num_sh_coeffs, 3, dtype=torch.float32, device=self.device)
        sh0 = rgb_to_sh0(points_rgb)  # (N, 3)
        sh_coeffs[:, 0, :] = torch.tensor(sh0, dtype=torch.float32, device=self.device)
        self.sh_coeffs = sh_coeffs

        # Enable gradients
        self._enable_grad()

    def init_random(self, n: int = 100_000, extent: float = 5.0):
        """Initialize N random Gaussians (for testing)."""
        self.means = extent * (torch.rand(n, 3, device=self.device) - 0.5)
        self.scales = torch.rand(n, 3, device=self.device) - 2.0  # log-space, small
        self.quats = random_quats(n).to(self.device)
        self.opacities = torch.full((n, 1), inverse_sigmoid(0.1),
                                     dtype=torch.float32, device=self.device)
        self.sh_coeffs = torch.zeros(n, self.num_sh_coeffs, 3,
                                      dtype=torch.float32, device=self.device)
        self._enable_grad()

    def _enable_grad(self):
        """Enable gradient tracking for all parameters."""
        self.means.requires_grad_(True)
        self.scales.requires_grad_(True)
        self.quats.requires_grad_(True)
        self.opacities.requires_grad_(True)
        self.sh_coeffs.requires_grad_(True)

    def _compute_nn_dists(self, points: np.ndarray, k: int = 3) -> np.ndarray:
        """Compute distances to k nearest neighbors for each point.

        Uses a simple chunked approach to avoid OOM on large point clouds.
        Returns (N, k) array of distances.
        """
        n = points.shape[0]
        if n <= 50_000:
            # Direct computation
            dists_sq = np.sum((points[:, None, :] - points[None, :, :]) ** 2, axis=-1)
            # Set self-distance to inf
            np.fill_diagonal(dists_sq, np.inf)
            # Get k smallest
            indices = np.argpartition(dists_sq, k, axis=1)[:, :k]
            nn_dists = np.sqrt(np.take_along_axis(dists_sq, indices, axis=1))
            return nn_dists
        else:
            # Chunked computation for large point clouds
            chunk_size = 10_000
            nn_dists_list = []
            for i in range(0, n, chunk_size):
                end = min(i + chunk_size, n)
                chunk = points[i:end]  # (C, 3)
                dists_sq = np.sum((chunk[:, None, :] - points[None, :, :]) ** 2, axis=-1)
                # Zero out self-distances
                for j in range(end - i):
                    dists_sq[j, i + j] = np.inf
                indices = np.argpartition(dists_sq, k, axis=1)[:, :k]
                nn_dists_list.append(np.sqrt(np.take_along_axis(dists_sq, indices, axis=1)))
            return np.concatenate(nn_dists_list, axis=0)

    def get_params_dict(self) -> Dict[str, Tensor]:
        """Return parameter dict for optimizer and strategy."""
        return {
            "means": self.means,
            "scales": self.scales,
            "quats": self.quats,
            "opacities": self.opacities,
            "sh_coeffs": self.sh_coeffs,
        }

    def get_activated_scales(self) -> Tensor:
        """Return scales in real space (exp of log-scales)."""
        return torch.exp(self.scales)

    def get_activated_opacities(self) -> Tensor:
        """Return opacities in [0, 1] (sigmoid of logit-opacities)."""
        return torch.sigmoid(self.opacities)

    def get_colors(self, viewdirs: Tensor, sh_degree: int) -> Tensor:
        """Evaluate SH to get view-dependent RGB colors.

        Args:
            viewdirs: (N, 3) normalized view directions
            sh_degree: active SH degree to use

        Returns:
            (N, 3) RGB colors clamped to [0, 1]
        """
        import sys
        sys.path.insert(0, self.config.gsplat_dir)
        from gsplat.sh import spherical_harmonics, num_sh_bases

        n_bases = num_sh_bases(sh_degree)
        # sh_coeffs is (N, K, 3), we need (N, K, 3) with K >= n_bases
        colors = spherical_harmonics(sh_degree, viewdirs, self.sh_coeffs)
        # spherical_harmonics returns (N, K, 3), take first component (N, 3) for DC
        # Actually it returns the summed result (N, 3)
        colors = colors + 0.5  # SH DC offset
        return torch.clamp(colors, 0.0, 1.0)

    def setup_optimizers(self) -> Dict[str, torch.optim.Adam]:
        """Create per-parameter Adam optimizers with 3DGS learning rates."""
        cfg = self.config
        optimizers = {}

        optimizers["means"] = torch.optim.Adam(
            [self.means], lr=cfg.lr_means, eps=1e-15
        )
        optimizers["scales"] = torch.optim.Adam(
            [self.scales], lr=cfg.lr_scales, eps=1e-15
        )
        optimizers["quats"] = torch.optim.Adam(
            [self.quats], lr=cfg.lr_quats, eps=1e-15
        )
        optimizers["opacities"] = torch.optim.Adam(
            [self.opacities], lr=cfg.lr_opacities, eps=1e-15
        )
        optimizers["sh_coeffs"] = torch.optim.Adam(
            [self.sh_coeffs], lr=cfg.lr_sh_dc, eps=1e-15
        )

        return optimizers

    def update_sh_degree(self, step: int):
        """Update active SH degree based on training step."""
        new_degree = min(
            step // self.config.sh_degree_interval,
            self.max_sh_degree,
        )
        if new_degree > self.active_sh_degree:
            print(f"[GaussianModel] SH degree: {self.active_sh_degree} -> {new_degree}")
            self.active_sh_degree = new_degree

    def state_dict(self) -> Dict[str, Tensor]:
        """Return state dict for checkpointing."""
        return {
            "means": self.means.detach().cpu(),
            "scales": self.scales.detach().cpu(),
            "quats": self.quats.detach().cpu(),
            "opacities": self.opacities.detach().cpu(),
            "sh_coeffs": self.sh_coeffs.detach().cpu(),
            "active_sh_degree": torch.tensor(self.active_sh_degree),
        }

    def load_state_dict(self, state: Dict[str, Tensor]):
        """Load from checkpoint."""
        self.means = state["means"].to(self.device).requires_grad_(True)
        self.scales = state["scales"].to(self.device).requires_grad_(True)
        self.quats = state["quats"].to(self.device).requires_grad_(True)
        self.opacities = state["opacities"].to(self.device).requires_grad_(True)
        self.sh_coeffs = state["sh_coeffs"].to(self.device).requires_grad_(True)
        self.active_sh_degree = int(state["active_sh_degree"].item())
