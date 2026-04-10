"""Loss functions: L1, D-SSIM (differentiable), and combined 3DGS loss.

The SSIM implementation is a simple differentiable version using
torch.nn.functional, not requiring torchmetrics or external packages.
"""

import torch
import torch.nn.functional as F
from torch import Tensor


# ---------------------------------------------------------------------------
# SSIM (Structural Similarity Index)
# ---------------------------------------------------------------------------

def _fspecial_gauss(size: int, sigma: float, device: torch.device) -> Tensor:
    """Create a Gaussian kernel for SSIM computation."""
    coords = torch.arange(size, dtype=torch.float32, device=device) - (size - 1) / 2.0
    g = torch.exp(-(coords ** 2) / (2 * sigma ** 2))
    g = torch.outer(g, g)
    return g / g.sum()


def ssim(
    img1: Tensor,
    img2: Tensor,
    window_size: int = 11,
    sigma: float = 1.5,
    size_average: bool = True,
    data_range: float = 1.0,
) -> Tensor:
    """Compute SSIM between two images.

    Args:
        img1, img2: (H, W, C) images in [0, 1]
        window_size: Size of Gaussian window
        sigma: Gaussian window sigma
        size_average: If True, return mean SSIM; else per-pixel
        data_range: Range of pixel values

    Returns:
        SSIM value (scalar if size_average=True)
    """
    C = img1.shape[-1]

    # Reshape to (1, C, H, W) for conv2d
    img1 = img1.permute(2, 0, 1).unsqueeze(0)  # (1, C, H, W)
    img2 = img2.permute(2, 0, 1).unsqueeze(0)

    # Create Gaussian window
    window = _fspecial_gauss(window_size, sigma, img1.device)  # (K, K)
    window = window.unsqueeze(0).unsqueeze(0)  # (1, 1, K, K)
    window = window.expand(C, 1, window_size, window_size)  # (C, 1, K, K)

    pad = window_size // 2

    # Constants
    C1 = (0.01 * data_range) ** 2
    C2 = (0.03 * data_range) ** 2

    mu1 = F.conv2d(img1, window, padding=pad, groups=C)
    mu2 = F.conv2d(img2, window, padding=pad, groups=C)

    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = F.conv2d(img1 * img1, window, padding=pad, groups=C) - mu1_sq
    sigma2_sq = F.conv2d(img2 * img2, window, padding=pad, groups=C) - mu2_sq
    sigma12 = F.conv2d(img1 * img2, window, padding=pad, groups=C) - mu1_mu2

    ssim_map = ((2.0 * mu1_mu2 + C1) * (2.0 * sigma12 + C2)) / \
               ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    if size_average:
        return ssim_map.mean()
    else:
        return ssim_map


# ---------------------------------------------------------------------------
# Loss functions
# ---------------------------------------------------------------------------

def l1_loss(pred: Tensor, target: Tensor) -> Tensor:
    """L1 (mean absolute error) loss.

    Args:
        pred, target: (H, W, 3) images

    Returns:
        Scalar L1 loss
    """
    return torch.abs(pred - target).mean()


def dssim_loss(pred: Tensor, target: Tensor) -> Tensor:
    """D-SSIM loss = (1 - SSIM) / 2.

    Args:
        pred, target: (H, W, 3) images in [0, 1]

    Returns:
        Scalar D-SSIM loss in [0, 1]
    """
    return (1.0 - ssim(pred, target)) / 2.0


def combined_loss(
    pred: Tensor,
    target: Tensor,
    lambda_l1: float = 0.8,
    lambda_dssim: float = 0.2,
) -> Tensor:
    """Standard 3DGS combined loss: lambda_l1 * L1 + lambda_dssim * D-SSIM.

    Args:
        pred, target: (H, W, 3) images in [0, 1]
        lambda_l1: Weight for L1 loss
        lambda_dssim: Weight for D-SSIM loss

    Returns:
        Scalar combined loss
    """
    loss_l1 = l1_loss(pred, target)
    loss_dssim = dssim_loss(pred, target)
    return lambda_l1 * loss_l1 + lambda_dssim * loss_dssim


# ---------------------------------------------------------------------------
# Evaluation metrics (non-differentiable, used in evaluator.py)
# ---------------------------------------------------------------------------

@torch.no_grad()
def psnr(pred: Tensor, target: Tensor) -> float:
    """Compute PSNR (Peak Signal-to-Noise Ratio).

    Args:
        pred, target: (H, W, 3) images in [0, 1]

    Returns:
        PSNR in dB
    """
    mse = ((pred - target) ** 2).mean().item()
    if mse == 0:
        return float("inf")
    return 10.0 * torch.log10(torch.tensor(1.0 / mse)).item()


@torch.no_grad()
def ssim_metric(pred: Tensor, target: Tensor) -> float:
    """Compute SSIM metric (same as loss but returns float).

    Args:
        pred, target: (H, W, 3) images in [0, 1]

    Returns:
        SSIM value in [0, 1]
    """
    return ssim(pred, target).item()
