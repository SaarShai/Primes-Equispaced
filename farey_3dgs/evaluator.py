"""Evaluation module: compute PSNR, SSIM, LPIPS on test views.

Saves per-view metrics and summary statistics.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import torch
from torch import Tensor

from .colmap_loader import load_scene, image_meta_to_world2cam
from .config import Config
from .gaussian_model import GaussianModel
from .losses import psnr, ssim_metric
from .renderer import Renderer, numpy_w2c_to_tensor


class Evaluator:
    """Evaluate a trained 3DGS model on test views."""

    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device(config.device)

        # Import gsplat-mps
        if config.gsplat_dir not in sys.path:
            sys.path.insert(0, config.gsplat_dir)

        self.renderer = Renderer(config)
        self._lpips_net = None  # Lazy-loaded

    def _get_lpips(self):
        """Lazy-load LPIPS network."""
        if self._lpips_net is None:
            import lpips
            self._lpips_net = lpips.LPIPS(net="alex").to(self.device)
            self._lpips_net.eval()
        return self._lpips_net

    @torch.no_grad()
    def evaluate(
        self,
        params: Dict[str, Tensor],
        scene_data,
        active_sh_degree: int,
        compute_lpips: bool = True,
        save_dir: Optional[str] = None,
    ) -> Dict:
        """Evaluate on all test views.

        Args:
            params: Gaussian parameters dict
            scene_data: SceneData from colmap_loader
            active_sh_degree: Current SH degree
            compute_lpips: Whether to compute LPIPS (slower)
            save_dir: If given, save rendered images here

        Returns:
            Dict with per-view and aggregate metrics.
        """
        cfg = self.config
        results = {
            "per_view": [],
            "num_gaussians": params["means"].shape[0],
            "active_sh_degree": active_sh_degree,
        }

        if save_dir:
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)

        psnr_vals = []
        ssim_vals = []
        lpips_vals = []

        for i, meta in enumerate(scene_data.test_metas):
            # Load ground truth
            gt_img = scene_data.load_image(meta, downscale=cfg.data_factor)
            gt_tensor = torch.tensor(gt_img, dtype=torch.float32, device=self.device)

            # Camera
            cam = scene_data.get_intrinsics(meta)
            w2c = image_meta_to_world2cam(meta)
            viewmat = numpy_w2c_to_tensor(w2c, self.device)

            # Adjust intrinsics if images were loaded at different resolution
            scale_x = gt_tensor.shape[1] / cam.width if cam.width != gt_tensor.shape[1] else 1.0
            scale_y = gt_tensor.shape[0] / cam.height if cam.height != gt_tensor.shape[0] else 1.0
            fx = cam.fx * scale_x
            fy = cam.fy * scale_y
            cx = cam.cx * scale_x
            cy = cam.cy * scale_y

            # Render
            output = self.renderer.render(
                means=params["means"],
                scales=params["scales"],
                quats=params["quats"],
                opacities=params["opacities"],
                sh_coeffs=params["sh_coeffs"],
                viewmat=viewmat,
                fx=fx,
                fy=fy,
                cx=cx,
                cy=cy,
                img_height=gt_tensor.shape[0],
                img_width=gt_tensor.shape[1],
                sh_degree=active_sh_degree,
            )

            rendered = output.image  # (H, W, 3)

            # PSNR
            p = psnr(rendered, gt_tensor)
            psnr_vals.append(p)

            # SSIM
            s = ssim_metric(rendered, gt_tensor)
            ssim_vals.append(s)

            # LPIPS
            l = 0.0
            if compute_lpips:
                try:
                    lpips_net = self._get_lpips()
                    # LPIPS expects (B, C, H, W) in [-1, 1]
                    pred_lpips = rendered.permute(2, 0, 1).unsqueeze(0) * 2.0 - 1.0
                    gt_lpips = gt_tensor.permute(2, 0, 1).unsqueeze(0) * 2.0 - 1.0
                    l = lpips_net(pred_lpips, gt_lpips).item()
                    lpips_vals.append(l)
                except Exception as e:
                    print(f"  LPIPS failed for view {i}: {e}")

            view_result = {
                "view_index": i,
                "image_name": meta.name,
                "psnr": p,
                "ssim": s,
                "lpips": l,
            }
            results["per_view"].append(view_result)

            # Save rendered image
            if save_dir:
                from PIL import Image
                img_np = (rendered.cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
                Image.fromarray(img_np).save(save_path / f"render_{i:04d}.png")

        # Aggregate metrics
        results["mean_psnr"] = float(np.mean(psnr_vals))
        results["mean_ssim"] = float(np.mean(ssim_vals))
        results["mean_lpips"] = float(np.mean(lpips_vals)) if lpips_vals else 0.0
        results["std_psnr"] = float(np.std(psnr_vals))
        results["std_ssim"] = float(np.std(ssim_vals))
        results["std_lpips"] = float(np.std(lpips_vals)) if lpips_vals else 0.0

        print(f"\n{'='*50}")
        print(f"Evaluation Results ({len(scene_data.test_metas)} test views)")
        print(f"  PSNR:  {results['mean_psnr']:.2f} +/- {results['std_psnr']:.2f}")
        print(f"  SSIM:  {results['mean_ssim']:.4f} +/- {results['std_ssim']:.4f}")
        if lpips_vals:
            print(f"  LPIPS: {results['mean_lpips']:.4f} +/- {results['std_lpips']:.4f}")
        print(f"  Gaussians: {results['num_gaussians']:,}")
        print(f"{'='*50}\n")

        # Save results
        if save_dir:
            with open(save_path / "metrics.json", "w") as f:
                json.dump(results, f, indent=2)

        return results
