"""Main training loop for 3D Gaussian Splatting.

Handles:
  - Scene loading from COLMAP
  - Gaussian initialization from SfM
  - Adam optimizer with per-parameter LR + exponential decay for positions
  - Random view sampling per iteration
  - Pluggable densification strategy (ADC, Farey, Midpoint)
  - Checkpointing at configurable iterations
  - Periodic evaluation on test views
"""

import json
import math
import os
import random
import sys
import time
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import torch
from torch import Tensor

from .colmap_loader import load_scene, SceneData, image_meta_to_world2cam
from .config import Config
from .gaussian_model import GaussianModel
from .losses import combined_loss, psnr
from .renderer import Renderer, numpy_w2c_to_tensor
from .strategy_adc import ADCStrategy
from .strategy_farey import FareyStrategy
from .strategy_midpoint import MidpointStrategy


def get_strategy(config: Config):
    """Factory function for densification strategy."""
    if config.strategy == "adc":
        return ADCStrategy(config)
    elif config.strategy == "farey":
        return FareyStrategy(config)
    elif config.strategy == "midpoint":
        return MidpointStrategy(config)
    else:
        raise ValueError(f"Unknown strategy: {config.strategy}")


def exponential_decay_lr(
    optimizer: torch.optim.Adam,
    lr_init: float,
    lr_final: float,
    step: int,
    max_steps: int,
):
    """Apply exponential learning rate decay to an optimizer."""
    if max_steps <= 0:
        return
    t = min(step / max_steps, 1.0)
    lr = lr_init * (lr_final / lr_init) ** t if lr_init > 0 else 0
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


class Trainer:
    """Main 3DGS trainer."""

    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device(config.device)

        # Ensure gsplat-mps is importable
        if config.gsplat_dir not in sys.path:
            sys.path.insert(0, config.gsplat_dir)

        # Load scene
        print(f"Loading scene from {config.data_dir}...")
        self.scene = load_scene(
            config.data_dir,
            images_subdir=config.images_subdir,
            test_every=config.test_every,
        )

        # Initialize Gaussian model
        self.model = GaussianModel(config)
        self.model.init_from_sfm(self.scene.points_xyz, self.scene.points_rgb)

        # Renderer
        self.renderer = Renderer(config)

        # Strategy
        self.strategy = get_strategy(config)

        # Output directories
        run_name = f"{config.scene_name}_{config.strategy}_seed{config.seed}"
        self.output_dir = Path(config.output_dir) / run_name
        self.checkpoint_dir = self.output_dir / "checkpoints"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Preload training images and cameras
        print("Preloading training images...")
        self.train_images = []
        self.train_cameras = []
        for meta in self.scene.train_metas:
            img = self.scene.load_image(meta, downscale=config.data_factor)
            img_tensor = torch.tensor(img, dtype=torch.float32, device=self.device)
            self.train_images.append(img_tensor)

            cam = self.scene.get_intrinsics(meta)
            w2c = image_meta_to_world2cam(meta)
            self.train_cameras.append({
                "w2c": numpy_w2c_to_tensor(w2c, self.device),
                "fx": cam.fx,
                "fy": cam.fy,
                "cx": cam.cx,
                "cy": cam.cy,
                "height": img_tensor.shape[0],
                "width": img_tensor.shape[1],
            })
        print(f"Loaded {len(self.train_images)} training views")

        # Preload test images
        print("Preloading test images...")
        self.test_images = []
        self.test_cameras = []
        for meta in self.scene.test_metas:
            img = self.scene.load_image(meta, downscale=config.data_factor)
            img_tensor = torch.tensor(img, dtype=torch.float32, device=self.device)
            self.test_images.append(img_tensor)

            cam = self.scene.get_intrinsics(meta)
            w2c = image_meta_to_world2cam(meta)
            self.test_cameras.append({
                "w2c": numpy_w2c_to_tensor(w2c, self.device),
                "fx": cam.fx,
                "fy": cam.fy,
                "cx": cam.cx,
                "cy": cam.cy,
                "height": img_tensor.shape[0],
                "width": img_tensor.shape[1],
            })
        print(f"Loaded {len(self.test_images)} test views")

    def train(self):
        """Run the full training loop."""
        cfg = self.config
        model = self.model

        # Set seed
        random.seed(cfg.seed)
        np.random.seed(cfg.seed)
        torch.manual_seed(cfg.seed)

        # Setup optimizers
        params = model.get_params_dict()
        optimizers = model.setup_optimizers()

        # Initialize strategy state
        state = self.strategy.initialize_state(model.num_gaussians)

        # Training metrics
        metrics_log = []
        total_time = 0.0

        print(f"\n{'='*60}")
        print(f"Training: {cfg.scene_name} | strategy={cfg.strategy} | "
              f"seed={cfg.seed} | iters={cfg.iterations}")
        print(f"Initial Gaussians: {model.num_gaussians}")
        print(f"{'='*60}\n")

        for step in range(1, cfg.iterations + 1):
            t0 = time.time()

            # Update SH degree
            model.update_sh_degree(step)

            # Update position learning rate (exponential decay)
            exponential_decay_lr(
                optimizers["means"],
                cfg.lr_means, cfg.lr_means_final,
                step, cfg.iterations,
            )

            # Random training view
            idx = random.randint(0, len(self.train_images) - 1)
            gt_image = self.train_images[idx]
            cam = self.train_cameras[idx]

            # Render
            output = self.renderer.render(
                means=params["means"],
                scales=params["scales"],
                quats=params["quats"],
                opacities=params["opacities"],
                sh_coeffs=params["sh_coeffs"],
                viewmat=cam["w2c"],
                fx=cam["fx"],
                fy=cam["fy"],
                cx=cam["cx"],
                cy=cam["cy"],
                img_height=cam["height"],
                img_width=cam["width"],
                sh_degree=model.active_sh_degree,
            )

            # Compute loss
            loss = combined_loss(
                output.image, gt_image,
                lambda_l1=cfg.lambda_l1,
                lambda_dssim=cfg.lambda_dssim,
            )

            # Strategy pre-backward
            self.strategy.step_pre_backward(
                params, state, step, output.xys, output.radii,
            )

            # Backward
            for opt in optimizers.values():
                opt.zero_grad()
            loss.backward()

            # Strategy post-backward (densification)
            params, optimizers, state = self.strategy.step_post_backward(
                params, optimizers, state, step, output.xys, output.radii,
            )

            # Update model params reference (in case densification changed them)
            model.means = params["means"]
            model.scales = params["scales"]
            model.quats = params["quats"]
            model.opacities = params["opacities"]
            model.sh_coeffs = params["sh_coeffs"]

            # Optimizer step
            for opt in optimizers.values():
                opt.step()

            # Normalize quaternions
            with torch.no_grad():
                params["quats"].data = torch.nn.functional.normalize(
                    params["quats"].data, dim=-1
                )

            iter_time = time.time() - t0
            total_time += iter_time

            # Logging
            if step % 100 == 0 or step == 1:
                train_psnr = psnr(output.image.detach(), gt_image)
                print(f"Step {step:>6d}/{cfg.iterations} | "
                      f"loss={loss.item():.5f} | "
                      f"PSNR={train_psnr:.2f} | "
                      f"#G={model.num_gaussians:,} | "
                      f"SH={model.active_sh_degree} | "
                      f"t={iter_time:.3f}s")

                metrics_log.append({
                    "step": step,
                    "loss": loss.item(),
                    "train_psnr": train_psnr,
                    "num_gaussians": model.num_gaussians,
                    "sh_degree": model.active_sh_degree,
                    "iter_time": iter_time,
                })

            # Evaluation on test views
            if step % cfg.eval_every == 0 or step == cfg.iterations:
                test_psnr = self._evaluate_test(params)
                print(f"  >> Test PSNR: {test_psnr:.2f} dB")
                if metrics_log:
                    metrics_log[-1]["test_psnr"] = test_psnr

            # Checkpointing
            if step in cfg.checkpoint_iters:
                self._save_checkpoint(params, optimizers, state, step, metrics_log)

        # Final summary
        print(f"\n{'='*60}")
        print(f"Training complete: {total_time:.1f}s total "
              f"({total_time/cfg.iterations:.3f}s/iter)")
        print(f"Final Gaussians: {model.num_gaussians:,}")
        print(f"{'='*60}\n")

        # Save final metrics
        metrics_path = self.output_dir / "metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics_log, f, indent=2)
        print(f"Metrics saved to {metrics_path}")

        return metrics_log

    @torch.no_grad()
    def _evaluate_test(self, params: Dict[str, Tensor]) -> float:
        """Evaluate PSNR on test views."""
        psnr_values = []
        for i in range(len(self.test_images)):
            gt_image = self.test_images[i]
            cam = self.test_cameras[i]

            output = self.renderer.render(
                means=params["means"],
                scales=params["scales"],
                quats=params["quats"],
                opacities=params["opacities"],
                sh_coeffs=params["sh_coeffs"],
                viewmat=cam["w2c"],
                fx=cam["fx"],
                fy=cam["fy"],
                cx=cam["cx"],
                cy=cam["cy"],
                img_height=cam["height"],
                img_width=cam["width"],
                sh_degree=self.model.active_sh_degree,
            )

            val = psnr(output.image, gt_image)
            psnr_values.append(val)

        return sum(psnr_values) / len(psnr_values) if psnr_values else 0.0

    def _save_checkpoint(
        self,
        params: Dict[str, Tensor],
        optimizers: Dict[str, torch.optim.Adam],
        state: Dict[str, Tensor],
        step: int,
        metrics_log: list,
    ):
        """Save a training checkpoint."""
        ckpt_path = self.checkpoint_dir / f"ckpt_{step:06d}.pt"
        checkpoint = {
            "step": step,
            "params": {k: v.detach().cpu() for k, v in params.items()},
            "state": {k: v.detach().cpu() if isinstance(v, Tensor) else v
                      for k, v in state.items()},
            "config": vars(self.config),
            "num_gaussians": params["means"].shape[0],
            "active_sh_degree": self.model.active_sh_degree,
        }
        torch.save(checkpoint, ckpt_path)
        print(f"  >> Checkpoint saved: {ckpt_path}")

        # Also save metrics so far
        metrics_path = self.checkpoint_dir / f"metrics_{step:06d}.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics_log, f, indent=2)
