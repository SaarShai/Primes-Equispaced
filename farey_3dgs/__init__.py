"""Farey 3DGS: 3D Gaussian Splatting with Farey-guided densification.

A training pipeline for 3D Gaussian Splatting on Apple Silicon (MPS),
comparing standard ADC densification against Farey-guided mediant placement.

Modules:
    config          - All hyperparameters
    colmap_loader   - Parse COLMAP binary format
    gaussian_model  - 3D Gaussian parameters
    renderer        - gsplat-mps rasterization wrapper
    losses          - L1, D-SSIM, PSNR, SSIM
    strategy_adc    - Standard ADC densification
    strategy_farey  - Farey-guided densification
    strategy_midpoint - Midpoint ablation baseline
    trainer         - Main training loop
    evaluator       - Test evaluation (PSNR, SSIM, LPIPS)
    run_experiment  - Single experiment CLI
    run_benchmark   - Full benchmark CLI
"""

from .config import Config
from .gaussian_model import GaussianModel
from .renderer import Renderer
from .trainer import Trainer
from .evaluator import Evaluator

__version__ = "0.1.0"
