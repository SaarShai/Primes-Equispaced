"""Full benchmark runner: all scenes x all strategies x multiple seeds.

Saves results to JSON and prints a summary table.

Usage:
    python -m farey_3dgs.run_benchmark
    python -m farey_3dgs.run_benchmark --scenes garden kitchen bicycle --seeds 42 43 44
    python -m farey_3dgs.run_benchmark --strategies adc farey --iterations 7000
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Ensure package is importable
script_dir = Path(__file__).resolve().parent.parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from farey_3dgs.config import Config
from farey_3dgs.trainer import Trainer
from farey_3dgs.evaluator import Evaluator


DEFAULT_DATA_ROOT = os.path.expanduser("~/Desktop/Farey-Local/data/mipnerf360")
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/output")

ALL_SCENES = [
    "garden", "bicycle", "kitchen", "room", "counter",
    "bonsai", "stump", "flowers", "treehill",
]
ALL_STRATEGIES = ["adc", "farey", "midpoint"]
DEFAULT_SEEDS = [42, 43, 44, 45, 46]


def parse_args():
    parser = argparse.ArgumentParser(description="Run full 3DGS benchmark")

    parser.add_argument("--scenes", type=str, nargs="+", default=["garden"],
                        help="Scenes to benchmark")
    parser.add_argument("--strategies", type=str, nargs="+", default=ALL_STRATEGIES,
                        help="Strategies to compare")
    parser.add_argument("--seeds", type=int, nargs="+", default=[42],
                        help="Random seeds")
    parser.add_argument("--iterations", type=int, default=30_000)
    parser.add_argument("--data_root", type=str, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--output_dir", type=str, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--images", type=str, default="images_4")
    parser.add_argument("--eval_lpips", action="store_true", default=False)
    parser.add_argument("--resume", action="store_true", default=False,
                        help="Skip runs that already have results")

    return parser.parse_args()


def run_single(data_dir, strategy, seed, iterations, images, output_dir, eval_lpips):
    """Run a single experiment and return results."""
    config = Config(
        data_dir=data_dir,
        images_subdir=images,
        strategy=strategy,
        iterations=iterations,
        seed=seed,
        output_dir=output_dir,
    )

    t0 = time.time()
    trainer = Trainer(config)
    trainer.train()
    train_time = time.time() - t0

    evaluator = Evaluator(config)
    params = trainer.model.get_params_dict()

    results = evaluator.evaluate(
        params=params,
        scene_data=trainer.scene,
        active_sh_degree=trainer.model.active_sh_degree,
        compute_lpips=eval_lpips,
    )

    results["train_time_seconds"] = train_time
    results["scene"] = config.scene_name
    results["strategy"] = strategy
    results["seed"] = seed
    results["iterations"] = iterations

    return results


def print_summary_table(all_results):
    """Print a formatted summary table."""
    if not all_results:
        print("No results to display.")
        return

    # Group by (scene, strategy)
    from collections import defaultdict
    grouped = defaultdict(list)
    for r in all_results:
        key = (r["scene"], r["strategy"])
        grouped[key].append(r)

    # Get unique scenes and strategies
    scenes = sorted(set(r["scene"] for r in all_results))
    strategies = sorted(set(r["strategy"] for r in all_results))

    # Header
    print(f"\n{'='*100}")
    print(f"BENCHMARK RESULTS SUMMARY")
    print(f"{'='*100}")
    print(f"{'Scene':<12} {'Strategy':<10} {'Seeds':>5} "
          f"{'PSNR':>8} {'SSIM':>8} {'LPIPS':>8} "
          f"{'#Gauss':>10} {'Time(min)':>10}")
    print(f"{'-'*100}")

    for scene in scenes:
        for strategy in strategies:
            key = (scene, strategy)
            runs = grouped.get(key, [])
            if not runs:
                continue

            n_seeds = len(runs)
            psnr_vals = [r["mean_psnr"] for r in runs]
            ssim_vals = [r["mean_ssim"] for r in runs]
            lpips_vals = [r.get("mean_lpips", 0) for r in runs]
            gauss_vals = [r["num_gaussians"] for r in runs]
            time_vals = [r.get("train_time_seconds", 0) / 60.0 for r in runs]

            import numpy as np
            psnr_mean = np.mean(psnr_vals)
            ssim_mean = np.mean(ssim_vals)
            lpips_mean = np.mean(lpips_vals)
            gauss_mean = np.mean(gauss_vals)
            time_mean = np.mean(time_vals)

            psnr_str = f"{psnr_mean:.2f}"
            ssim_str = f"{ssim_mean:.4f}"
            lpips_str = f"{lpips_mean:.4f}" if lpips_mean > 0 else "N/A"
            gauss_str = f"{int(gauss_mean):,}"
            time_str = f"{time_mean:.1f}"

            if n_seeds > 1:
                psnr_str += f"+-{np.std(psnr_vals):.2f}"
                ssim_str += f"+-{np.std(ssim_vals):.4f}"

            print(f"{scene:<12} {strategy:<10} {n_seeds:>5} "
                  f"{psnr_str:>8} {ssim_str:>8} {lpips_str:>8} "
                  f"{gauss_str:>10} {time_str:>10}")

        if scene != scenes[-1]:
            print(f"{'-'*100}")

    print(f"{'='*100}\n")


def main():
    args = parse_args()

    total_runs = len(args.scenes) * len(args.strategies) * len(args.seeds)
    print(f"\n{'='*60}")
    print(f"3DGS Benchmark")
    print(f"  Scenes:     {args.scenes}")
    print(f"  Strategies: {args.strategies}")
    print(f"  Seeds:      {args.seeds}")
    print(f"  Iterations: {args.iterations}")
    print(f"  Total runs: {total_runs}")
    print(f"{'='*60}\n")

    # Results file
    results_dir = Path(args.output_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    results_path = results_dir / "benchmark_results.json"

    # Load existing results if resuming
    all_results = []
    if args.resume and results_path.exists():
        with open(results_path) as f:
            all_results = json.load(f)
        print(f"Loaded {len(all_results)} existing results from {results_path}")

    completed_keys = set()
    for r in all_results:
        completed_keys.add((r["scene"], r["strategy"], r["seed"]))

    run_count = 0
    t_total = time.time()

    for scene in args.scenes:
        for strategy in args.strategies:
            for seed in args.seeds:
                run_count += 1
                run_key = (scene, strategy, seed)

                if args.resume and run_key in completed_keys:
                    print(f"[{run_count}/{total_runs}] SKIP (already done): "
                          f"{scene} / {strategy} / seed={seed}")
                    continue

                data_dir = os.path.join(args.data_root, scene)
                if not os.path.exists(data_dir):
                    print(f"[{run_count}/{total_runs}] SKIP (not found): {data_dir}")
                    continue

                print(f"\n[{run_count}/{total_runs}] "
                      f"Running: {scene} / {strategy} / seed={seed}")
                print(f"{'-'*50}")

                try:
                    results = run_single(
                        data_dir=data_dir,
                        strategy=strategy,
                        seed=seed,
                        iterations=args.iterations,
                        images=args.images,
                        output_dir=args.output_dir,
                        eval_lpips=args.eval_lpips,
                    )
                    all_results.append(results)

                    # Save incrementally
                    with open(results_path, "w") as f:
                        json.dump(all_results, f, indent=2)

                except Exception as e:
                    print(f"  ERROR: {e}")
                    import traceback
                    traceback.print_exc()
                    all_results.append({
                        "scene": scene,
                        "strategy": strategy,
                        "seed": seed,
                        "error": str(e),
                    })

    total_time = time.time() - t_total
    print(f"\nBenchmark completed in {total_time/60:.1f} minutes")

    # Print summary
    valid_results = [r for r in all_results if "error" not in r]
    print_summary_table(valid_results)

    # Save final results
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    main()
