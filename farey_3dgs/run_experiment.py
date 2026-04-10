"""CLI interface for running a single 3DGS training experiment.

Usage:
    python -m farey_3dgs.run_experiment --scene bicycle --strategy adc --seed 42 --iterations 30000
    python -m farey_3dgs.run_experiment --scene bicycle --strategy farey --seed 42 --iterations 30000
    python -m farey_3dgs.run_experiment --data_dir /path/to/garden --strategy midpoint

Or from the parent directory:
    python farey_3dgs/run_experiment.py --scene garden --strategy adc
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Ensure package is importable when run as script
script_dir = Path(__file__).resolve().parent.parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from farey_3dgs.config import Config
from farey_3dgs.trainer import Trainer
from farey_3dgs.evaluator import Evaluator
from farey_3dgs.colmap_loader import load_scene, image_meta_to_world2cam
from farey_3dgs.renderer import numpy_w2c_to_tensor


# Default dataset root
DEFAULT_DATA_ROOT = os.path.expanduser("~/Desktop/Farey-Local/data/mipnerf360")

# Known scenes
SCENES = [
    "garden", "bicycle", "kitchen", "room", "counter",
    "bonsai", "stump", "flowers", "treehill",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Run a single 3DGS experiment")

    # Scene
    parser.add_argument("--scene", type=str, default="garden",
                        choices=SCENES, help="Scene name")
    parser.add_argument("--data_dir", type=str, default=None,
                        help="Full path to scene dir (overrides --scene)")
    parser.add_argument("--data_root", type=str, default=DEFAULT_DATA_ROOT,
                        help="Root directory containing scene folders")
    parser.add_argument("--images", type=str, default="images_4",
                        help="Image subdirectory")

    # Strategy
    parser.add_argument("--strategy", type=str, default="adc",
                        choices=["adc", "farey", "midpoint"],
                        help="Densification strategy")

    # Training
    parser.add_argument("--iterations", type=int, default=30_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--eval_every", type=int, default=1000)

    # Output
    parser.add_argument("--output_dir", type=str,
                        default=os.path.expanduser("~/Desktop/Farey-Local/output"))

    # Evaluation
    parser.add_argument("--eval_lpips", action="store_true", default=False,
                        help="Compute LPIPS (requires lpips package)")
    parser.add_argument("--save_renders", action="store_true", default=False,
                        help="Save rendered test images")

    return parser.parse_args()


def main():
    args = parse_args()

    # Resolve data directory
    if args.data_dir:
        data_dir = args.data_dir
    else:
        data_dir = os.path.join(args.data_root, args.scene)

    if not os.path.exists(data_dir):
        print(f"ERROR: Data directory not found: {data_dir}")
        print(f"Expected Mip-NeRF 360 scene at this path.")
        print(f"Available scenes in {args.data_root}:")
        if os.path.exists(args.data_root):
            for d in sorted(os.listdir(args.data_root)):
                if os.path.isdir(os.path.join(args.data_root, d)):
                    print(f"  {d}")
        sys.exit(1)

    # Build config
    config = Config(
        data_dir=data_dir,
        images_subdir=args.images,
        strategy=args.strategy,
        iterations=args.iterations,
        seed=args.seed,
        eval_every=args.eval_every,
        output_dir=args.output_dir,
    )

    print(f"\n{'='*60}")
    print(f"3DGS Experiment")
    print(f"  Scene:     {config.scene_name}")
    print(f"  Strategy:  {config.strategy}")
    print(f"  Seed:      {config.seed}")
    print(f"  Iters:     {config.iterations}")
    print(f"  Images:    {config.images_subdir}")
    print(f"  Output:    {config.output_dir}")
    print(f"{'='*60}\n")

    # Train
    t0 = time.time()
    trainer = Trainer(config)
    metrics_log = trainer.train()
    train_time = time.time() - t0

    # Final evaluation
    print("\nRunning final evaluation...")
    evaluator = Evaluator(config)

    params = trainer.model.get_params_dict()
    scene = trainer.scene

    save_dir = None
    if args.save_renders:
        save_dir = str(Path(config.output_dir) /
                       f"{config.scene_name}_{config.strategy}_seed{config.seed}" /
                       "renders")

    results = evaluator.evaluate(
        params=params,
        scene_data=scene,
        active_sh_degree=trainer.model.active_sh_degree,
        compute_lpips=args.eval_lpips,
        save_dir=save_dir,
    )

    # Print final summary
    print(f"\n{'='*60}")
    print(f"FINAL RESULTS")
    print(f"  Scene:      {config.scene_name}")
    print(f"  Strategy:   {config.strategy}")
    print(f"  Seed:       {config.seed}")
    print(f"  PSNR:       {results['mean_psnr']:.2f} dB")
    print(f"  SSIM:       {results['mean_ssim']:.4f}")
    if results.get('mean_lpips', 0) > 0:
        print(f"  LPIPS:      {results['mean_lpips']:.4f}")
    print(f"  Gaussians:  {results['num_gaussians']:,}")
    print(f"  Train time: {train_time:.1f}s ({train_time/60:.1f}min)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
