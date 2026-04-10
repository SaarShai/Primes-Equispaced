"""All hyperparameters for the 3DGS training pipeline."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    # ---- Scene / Data ----
    data_dir: str = ""                          # Path to scene directory (e.g., data/mipnerf360/garden)
    images_subdir: str = "images_4"             # Which resolution images to use
    test_every: int = 8                         # Every Nth image is held out for testing
    data_factor: int = 1                        # Additional downscale factor applied at load time

    # ---- gsplat-mps path ----
    gsplat_dir: str = "/Users/saar/Desktop/gsplat-mps"

    # ---- Training ----
    iterations: int = 30_000
    batch_size: int = 1                         # Views per iteration (always 1 for 3DGS)
    seed: int = 42

    # ---- Learning Rates ----
    lr_means: float = 1.6e-4
    lr_means_final: float = 1.6e-6
    lr_opacities: float = 0.05
    lr_scales: float = 0.005
    lr_quats: float = 0.001
    lr_sh_dc: float = 0.0025
    lr_sh_rest: float = 1.25e-4

    # ---- Loss ----
    lambda_l1: float = 0.8
    lambda_dssim: float = 0.2

    # ---- SH Degree Schedule ----
    sh_degree_max: int = 3
    sh_degree_interval: int = 1000              # Upgrade SH degree every N iterations
    # SH degrees: 0 at start, 1 at 1000, 2 at 2000, 3 at 3000

    # ---- Densification (shared) ----
    densify_start: int = 500
    densify_stop: int = 15_000
    densify_every: int = 100
    opacity_prune_threshold: float = 0.005
    opacity_reset_every: int = 3000

    # ---- ADC Strategy ----
    grad_threshold: float = 0.0002
    split_scale_threshold: float = 0.01         # Percentile scale above which we split (not clone)

    # ---- Farey Strategy ----
    farey_knn_k: int = 6
    farey_gap_percentile: float = 75.0          # Gap threshold = Nth percentile of gap ratios
    farey_level_start: int = 4
    farey_error_threshold: float = 0.01         # Local reconstruction error gate
    farey_max_insertions_per_step: int = 50_000

    # ---- Midpoint Strategy ----
    midpoint_knn_k: int = 6
    midpoint_gap_percentile: float = 75.0
    midpoint_error_threshold: float = 0.01
    midpoint_max_insertions_per_step: int = 50_000

    # ---- Strategy Selection ----
    strategy: str = "adc"                       # "adc", "farey", "midpoint"

    # ---- Checkpointing ----
    checkpoint_dir: str = "checkpoints"
    checkpoint_iters: list = field(default_factory=lambda: [7_000, 30_000])
    eval_every: int = 1000                      # Evaluate on test views every N iterations

    # ---- Output ----
    output_dir: str = "output"
    scene_name: str = ""                        # Auto-derived from data_dir if empty

    # ---- Device ----
    device: str = "mps"

    # ---- Rasterizer ----
    glob_scale: float = 1.0
    clip_thresh: float = 0.01
    block_x: int = 16
    block_y: int = 16

    def __post_init__(self):
        if self.scene_name == "" and self.data_dir:
            self.scene_name = self.data_dir.rstrip("/").split("/")[-1]

    @property
    def sh_degree_at(self):
        """Return a function: iteration -> active SH degree."""
        def _sh_deg(step: int) -> int:
            deg = step // self.sh_degree_interval
            return min(deg, self.sh_degree_max)
        return _sh_deg

    @property
    def num_sh_coeffs(self) -> int:
        """Total SH coefficients per color channel at max degree."""
        return (self.sh_degree_max + 1) ** 2    # 16 for degree 3

    @property
    def lr_means_schedule(self):
        """Return exponential decay schedule parameters for position LR."""
        return {
            "lr_init": self.lr_means,
            "lr_final": self.lr_means_final,
            "max_steps": self.iterations,
        }
