# 3DGS Experiment Best Practice Setup
## (Based on survey of 7 published papers 2023-2025)

### Standard Training
- **30,000 iterations** (universal standard)
- Adam optimizer
- Loss: 0.8 * L1 + 0.2 * D-SSIM
- LR: position 0.00016→0.0000016 (exp decay), opacity 0.05, SH 0.0025, scaling 0.005, rotation 0.001

### Standard Densification (baseline)
- Start: iteration 500
- Stop: iteration 15,000
- Interval: every 100 iterations
- Gradient threshold (tau_grad): 0.0002
- Opacity pruning: 0.005
- Opacity reset: every 3,000 iterations

### Benchmarks (mandatory)
- **Mip-NeRF 360** (9 scenes: bicycle, bonsai, counter, flowers, garden, kitchen, room, stump, treehill)
- **Tanks and Temples** (2 scenes: Truck, Train)
- **Deep Blending** (2 scenes: DrJohnson, Playroom)
- Test split: every 8th image held out

### Metrics (all mandatory)
- PSNR, SSIM, LPIPS, Gaussian count, training time

### Statistical Rigor (our differentiator)
- **5 random seeds** per config, report mean ± std
- Only 1 of 7 papers does this — we stand out

### Initialization
- SfM point clouds from COLMAP (universal, non-negotiable)

### Baselines to compare against
- Vanilla 3DGS ADC (Kerbl et al.)
- 3DGS-MCMC (budget-matched)
- Revising Densification (ECCV 2024)
- SteepGS (CVPR 2025)

### Notes
- Our current experiments use 2K-6K iterations, 200-3000 Gaussians, synthetic scenes
- Published papers use 30K iterations, 1-5M Gaussians, real scenes
- We are off by 1-2 orders of magnitude — results so far are indicative only
