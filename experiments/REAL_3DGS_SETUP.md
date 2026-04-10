# Real 3DGS Pipeline Setup: Farey Densification Experiment

**Target hardware**: Apple M5 Max MacBook Pro, PyTorch MPS
**Date**: 2026-03-27
**Status**: Planning phase (nothing installed yet)

---

## 1. CODEBASE DECISION

### Options Evaluated

| Codebase | MPS? | Full Pipeline? | Densification? | Modifiable? | Verdict |
|----------|------|----------------|----------------|-------------|---------|
| gsplat v0.1.3 (local) | YES (Metal shaders) | NO (single-image only) | NO | Low-level only | Rasterizer only |
| gsplat v1.5+ (main) | NO (CUDA only) | YES (COLMAP, SH, SSIM, ADC/MCMC) | YES (pluggable Strategy API) | Best API | No MPS backend |
| splat-apple (ghif) | YES (MPS + MLX) | PARTIAL (COLMAP, SSIM loss, SH) | NO (no ADC at all) | Medium | Missing densification |
| OpenSplat | YES (Metal, C++) | YES (COLMAP, full pipeline) | Probably yes (C++) | Hard (C++) | C++ makes Farey integration painful |
| nerfstudio splatfacto | NO (needs CUDA gsplat) | YES (everything) | YES | Good | MPS blocked by gsplat |

### Recommended Path: HYBRID APPROACH

**Primary: splat-apple (PyTorch MPS backend) + custom densification**

Rationale:
1. splat-apple already has the hard parts working on MPS: differentiable rasterization via the local gsplat-mps Metal shaders, COLMAP loading, SSIM+L1 loss (0.8*L1 + 0.2*D-SSIM), spherical harmonics, and Adam optimizer with per-parameter LRs.
2. What it lacks (densification/ADC) is exactly what we want to replace anyway. We need to write custom densification regardless -- using Farey logic instead of standard ADC.
3. The gsplat v1.5 Strategy API provides the reference implementation to port from. We copy the DefaultStrategy logic (gradient accumulation, split/clone thresholds, opacity pruning, opacity reset) into a Python module that works with splat-apple's Gaussian parameter format, then swap in Farey admission.

**Fallback: Build a full trainer on top of gsplat-mps v0.1.3 directly**

If splat-apple proves too difficult to extend, we write a trainer from scratch using the local gsplat-mps rasterizer. The rasterizer (project_gaussians + rasterize_gaussians) is the only part that needs Metal acceleration. Everything else (COLMAP loading, loss computation, densification, evaluation) is pure Python/PyTorch that runs on any device.

### Why NOT the other options

- **gsplat v1.5 main**: The ideal codebase, but its rasterization kernels are CUDA-only. The entire `_C` backend is compiled CUDA. There is no MPS backend in any version after v0.1.3.
- **OpenSplat**: Full pipeline with Metal, but it is C++. Implementing Farey densification in C++ and rebuilding for every change is impractical for rapid experimentation.
- **nerfstudio**: Depends on gsplat for splatfacto, which has no MPS support. Confirmed broken on Apple Silicon (GitHub issue #3290).

---

## 2. DATASET: Mip-NeRF 360

### Download Method

The standard dataset with COLMAP reconstructions is hosted by Google Research:

```bash
# Full dataset (~6 GB compressed, ~12 GB uncompressed)
wget http://storage.googleapis.com/gresearch/refraw360/360_v2.zip
unzip -d ~/Desktop/Farey-Local/data/mipnerf360 360_v2.zip

# OR download just one scene via nerfbaselines:
pip install nerfbaselines
nerfbaselines download-dataset external://mipnerf360/garden -o ~/Desktop/Farey-Local/data/garden
nerfbaselines download-dataset external://mipnerf360/bicycle -o ~/Desktop/Farey-Local/data/bicycle
```

### Dataset Structure (per scene)

```
garden/
  images/           # Full-resolution photos (~4000x3000)
  images_2/         # 2x downsampled (used by default in papers)
  images_4/         # 4x downsampled (faster training)
  images_8/         # 8x downsampled (debugging)
  sparse/
    0/
      cameras.bin   # Camera intrinsics (focal length, distortion)
      images.bin    # Camera extrinsics (pose per image)
      points3D.bin  # SfM point cloud (initialization)
```

### Scene Selection for Phased Experiments

| Scene | Type | Difficulty | Images | Notes |
|-------|------|------------|--------|-------|
| garden | Outdoor | Medium | ~200 | Good first test, varied geometry |
| bicycle | Outdoor | Hard | ~200 | Thin structures, challenging |
| kitchen | Indoor | Easy | ~300 | Well-textured, bounded |
| room | Indoor | Easy | ~300 | Simple geometry |
| counter | Indoor | Easy | ~300 | Tabletop scene |
| bonsai | Indoor | Medium | ~200 | Fine detail |
| stump | Outdoor | Hard | ~200 | Complex natural geometry |
| flowers | Outdoor | Hard | ~200 | High-frequency detail |
| treehill | Outdoor | Hard | ~200 | Distant background |

**Phase 1**: garden (good baseline, medium difficulty)
**Phase 2**: garden + kitchen + bicycle (indoor/outdoor/hard)
**Phase 3+**: All 9 scenes

### Train/Test Split Convention

Standard 3DGS convention: every 8th image is held out for testing. This is deterministic and reproducible. The COLMAP loader should sort images by filename and select indices where `i % 8 == 0` as test.

---

## 3. ARCHITECTURE: WHAT TO BUILD

### 3.1 Files to Create

```
~/Desktop/Farey-Local/farey_3dgs/
  __init__.py
  colmap_loader.py          # Parse cameras.bin, images.bin, points3D.bin
  dataset.py                # PyTorch dataset: load images, return (image, camera)
  gaussian_model.py         # Gaussian parameters: means, scales, quats, opacities, SH
  rasterize.py              # Wrapper around gsplat-mps project+rasterize
  losses.py                 # L1, D-SSIM, combined loss
  metrics.py                # PSNR, SSIM, LPIPS evaluation
  strategy_base.py          # Base densification strategy interface
  strategy_adc.py           # Standard ADC (gradient threshold, clone/split/prune)
  strategy_farey.py         # Farey densification (our contribution)
  lr_schedule.py            # Exponential decay for means LR, step schedule for SH
  train.py                  # Main training loop (30K iterations)
  eval.py                   # Held-out test evaluation
  config.py                 # All hyperparameters
```

### 3.2 Files to Reuse

From splat-apple (if usable):
- `torch_gs/io/` -- COLMAP binary parser
- `torch_gs/renderer/` -- rasterization wrapper
- `torch_gs/training/trainer.py` -- train_step skeleton (has SSIM+L1 loss)
- `torch_gs/core/` -- Gaussian parameter classes

From gsplat-mps (already installed):
- `gsplat/project_gaussians.py` -- Metal-accelerated projection
- `gsplat/rasterize.py` -- Metal-accelerated rasterization
- `gsplat/sh.py` -- Spherical harmonics evaluation

From gsplat v1.5 main (reference only, not runnable):
- `gsplat/strategy/default.py` -- DefaultStrategy (ADC) to port
- `gsplat/strategy/mcmc.py` -- MCMCStrategy (reference)
- `examples/simple_trainer.py` -- Full training pipeline logic to adapt
- `examples/datasets/colmap.py` -- COLMAP parser to adapt

### 3.3 Densification Strategy Interface

```python
class DensificationStrategy:
    """Base class for Gaussian densification strategies."""

    def initialize_state(self, params: dict) -> dict:
        """Set up tracking state (gradient accumulators, etc.)."""
        ...

    def step_pre_backward(self, params, optimizers, state, step, info):
        """Called before loss.backward(). Record 2D positions for grad tracking."""
        ...

    def step_post_backward(self, params, optimizers, state, step, info):
        """Called after loss.backward().
        Accumulate gradients, then periodically:
        - Grow (split/clone) Gaussians exceeding gradient threshold
        - Prune low-opacity Gaussians
        - Reset opacity periodically
        Returns updated params, optimizers, state.
        """
        ...
```

### 3.4 Key Hyperparameters (matching original 3DGS paper)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Total iterations | 30,000 | Standard |
| Position LR | 0.00016 -> 0.0000016 | Exponential decay |
| Opacity LR | 0.05 | Fixed |
| Scaling LR | 0.005 | Fixed |
| Rotation LR | 0.001 | Fixed |
| SH (DC) LR | 0.0025 | Fixed |
| SH (rest) LR | 0.000125 | Fixed |
| Loss | 0.8*L1 + 0.2*D-SSIM | Standard |
| Densify start | 500 | iterations |
| Densify stop | 15,000 | iterations |
| Densify every | 100 | iterations |
| Gradient threshold | 0.0002 | For ADC baseline |
| Opacity prune threshold | 0.005 | Standard |
| Opacity reset every | 3,000 | iterations |
| SH degree schedule | 0->1->2->3 at 1K, 2K, 3K | Progressive |
| Image resolution | 4x downsample | For speed on MPS |

---

## 4. WHAT TO MODIFY FOR FAREY DENSIFICATION

The Farey strategy replaces the gradient-threshold criterion in `strategy_adc.py` with:

### 4.1 Core Changes (in strategy_farey.py)

1. **Gap detection**: Instead of checking gradient magnitude > threshold, compute spatial gaps between neighboring Gaussians. Use kNN (k=16) with a spatial hash for O(N log N) neighbor finding instead of full Delaunay (which is O(N^2) in 3D at scale).

2. **Admission criterion**: A gap between Gaussians i and j is "admissible" at Farey level N if:
   ```
   d_i + d_j <= N
   ```
   where d_i = round(1 / scale_i) is the "denominator" (reciprocal of spatial extent).

3. **Mediant placement**: New Gaussians are placed at the weighted midpoint:
   ```
   pos_new = (d_j * pos_i + d_i * pos_j) / (d_i + d_j)
   ```
   instead of random offset from the parent (ADC) or voxel center.

4. **Rate control**: At most 1 new Gaussian per gap per refinement step (the injection principle).

5. **Error gating**: Only densify in gaps where the local reconstruction error exceeds a threshold. This is critical for fairness -- ADC has this implicitly via gradient accumulation.

6. **Level schedule**: N starts low (e.g., N=4) and increases over training, providing coarse-to-fine refinement. Schedule: N = 4 + (step / densify_every).

### 4.2 Files That Change Between ADC and Farey

Only ONE file differs: `strategy_farey.py` vs `strategy_adc.py`. The training loop, loss function, rasterizer, COLMAP loader, and evaluation are identical. This is the clean experimental design.

### 4.3 Ablation Variant

A third strategy, `strategy_midpoint.py`, that does error-guided midpoint placement WITHOUT Farey math (no denominator mapping, no admission criterion, no level schedule). This isolates whether Farey adds value over simple gap-filling.

---

## 5. INSTALLATION COMMANDS (DO NOT RUN YET)

### Step 1: Clone splat-apple and inspect

```bash
cd ~/Desktop
git clone https://github.com/ghif/splat-apple.git
cd splat-apple
# Inspect: does torch_gs/io/ have COLMAP binary parser?
# Inspect: does torch_gs/renderer/ wrap gsplat-mps properly?
# Inspect: what Gaussian parameter format does it use?
```

### Step 2: Set up project environment

```bash
mkdir -p ~/Desktop/Farey-Local/farey_3dgs
cd ~/Desktop/Farey-Local

# Option A: Reuse gsplat-mps venv (already has PyTorch 2.8 + MPS)
source ~/Desktop/gsplat-mps/venv/bin/activate

# Option B: Fresh venv
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision  # PyTorch 2.8+ with MPS
pip install numpy pillow tqdm tensorboard
pip install lpips              # For LPIPS evaluation
pip install pytorch-msssim     # For D-SSIM loss
pip install plyfile            # For reading/writing PLY point clouds
pip install tyro               # CLI argument parsing
```

### Step 3: Install gsplat-mps as editable package

```bash
# Already built at ~/Desktop/gsplat-mps with Metal shaders compiled
cd ~/Desktop/gsplat-mps
pip install -e .
# Verify:
python -c "from gsplat import project_gaussians; print('gsplat-mps OK')"
```

### Step 4: Download dataset

```bash
cd ~/Desktop/Farey-Local/data
wget http://storage.googleapis.com/gresearch/refraw360/360_v2.zip
unzip -d mipnerf360 360_v2.zip
# ~6 GB download, ~12 GB uncompressed
```

### Step 5: Verify rasterizer on MPS

```bash
cd ~/Desktop/gsplat-mps
source venv/bin/activate
python examples/simple_trainer.py --num_points 10000 --iterations 100
# Should run on MPS without errors
```

---

## 6. ESTIMATED RUNTIMES ON M5 MAX

### Baseline Estimates

The gsplat-mps rasterizer on M-series has been benchmarked at roughly 3-5x slower than an RTX 3090. On an RTX 3090, 30K iterations on a Mip-NeRF 360 scene at 4x resolution takes approximately 15-25 minutes with gsplat v1.5.

| Configuration | Est. Time (M5 Max) | Notes |
|--------------|---------------------|-------|
| 7K iter, 1 scene, 4x res | 20-40 min | Verification run |
| 30K iter, 1 scene, 4x res | 1.5-3 hours | Full training |
| 30K iter, 1 scene, 2x res | 4-8 hours | Higher resolution |
| 30K iter, 3 scenes, 2 seeds | 9-18 hours | Phase 3-4 |
| 30K iter, 9 scenes, 5 seeds | 67-135 hours | Full benchmark |

### Memory Estimates

M5 Max has 128GB unified memory. At 4x resolution:
- Gaussians (3M): ~1.5 GB
- Images (~200 at 1000x750): ~0.5 GB
- Gradients + optimizer state: ~6 GB
- Rasterizer buffers: ~2 GB
- Total: ~10 GB (well within budget)

At 2x resolution, image memory increases to ~2 GB. Still fine.

### Key Bottleneck

The Metal rasterizer in gsplat v0.1.3 may not have backward pass optimizations that v1.5 has. If backward pass is slow, the main options are:
1. Use 4x resolution throughout (good enough for comparing densification strategies)
2. Port selected v1.5 kernel improvements to the Metal backend
3. Use OpenSplat's Metal rasterizer if it has faster backward

---

## 7. BLOCKERS AND RISKS

### Critical Blockers

1. **gsplat-mps backward pass completeness**: The v0.1.3 Metal port must support gradients for means, scales, quats, opacities, and colors. The simple_trainer.py works (so backward through rasterize exists), but we need to verify it supports all the gradient types needed for densification (specifically, the 2D position gradients that ADC accumulates).

2. **Spherical harmonics on MPS**: The gsplat-mps `sh.py` module exists but needs verification that SH evaluation and its backward pass work on MPS tensors. If not, we fall back to SH degree 0 (direct RGB) for initial experiments.

3. **splat-apple compatibility**: If splat-apple uses a different gsplat fork or API than gsplat-mps v0.1.3, the COLMAP loader and renderer may not be directly reusable. Need to inspect before committing.

### Medium Risks

4. **kNN at scale**: Computing 16-nearest-neighbors for 1M+ Gaussians every 100 iterations. PyTorch has `torch.cdist` but it is O(N^2) memory. Need spatial hashing or a library like `faiss` or `pynndescent`. Estimated overhead: 0.5-2 seconds per densification step, acceptable.

5. **D-SSIM loss on MPS**: The `pytorch-msssim` package should work on MPS, but some older versions have CUDA-specific code paths. May need the `kornia` implementation instead.

6. **LPIPS on MPS**: The `lpips` package uses a pretrained VGG/Alex network. Should work on MPS but needs verification.

### Low Risks

7. **Numerical precision**: MPS uses float32 by default (no float16 TF32 like CUDA). This is actually an advantage for reproducibility.

8. **Image loading**: Standard PIL/torchvision, no issues expected.

---

## 8. NIGHTLY TASK PLAN

### Night 1: Setup + Vanilla Verification (7K iter)

**Goal**: Confirm the full pipeline runs end-to-end on MPS.

```
Tasks:
1. Download garden scene from Mip-NeRF 360
2. Clone splat-apple, inspect compatibility with gsplat-mps
3. Assemble the training pipeline (COLMAP -> Gaussians -> Train -> Eval)
4. Run vanilla ADC training for 7K iterations on garden at 4x resolution
5. Report PSNR on held-out test views

Success criterion: Pipeline completes without errors. PSNR > 20 dB at 7K.
Expected time: 20-40 min training + setup time.
```

### Night 2: Add Farey Strategy + Test (7K iter)

**Goal**: Farey densification runs and produces comparable quality.

```
Tasks:
1. Implement strategy_adc.py (port from gsplat v1.5 DefaultStrategy)
2. Implement strategy_farey.py (Farey admission + mediant placement)
3. Implement strategy_midpoint.py (ablation: midpoint without Farey math)
4. Run all 3 strategies on garden for 7K iterations
5. Compare PSNR, Gaussian count, training time

Success criterion: All 3 strategies complete. Farey PSNR within 1 dB of ADC.
Expected time: 3 x 30 min = 1.5 hours training.
```

### Night 3-4: Full Training, 3 Scenes, 2 Seeds (30K iter)

**Goal**: Statistically meaningful comparison across scenes.

```
Tasks:
1. Run 3 strategies x 3 scenes (garden, kitchen, bicycle) x 2 seeds
   = 18 training runs
2. Evaluate PSNR, SSIM, LPIPS on held-out test views
3. Generate comparison table
4. Identify any scenes where Farey particularly helps or hurts

Success criterion: Complete all 18 runs. Generate per-scene metrics table.
Expected time: 18 x 2 hours = 36 hours (parallelize 2 at a time = 18 hours).
```

### Night 5-7: Full Benchmark (30K iter, 9 scenes, 5 seeds)

**Goal**: Publication-quality results.

```
Tasks:
1. Run 3 strategies x 9 scenes x 5 seeds = 135 training runs
2. Full evaluation suite
3. Compute means and standard deviations
4. Generate paper-ready tables and figures
5. Compare against published numbers (3DGS, Mini-Splatting, SteepGS)

Success criterion: Complete benchmark with confidence intervals.
Expected time: 135 x 2 hours = 270 hours / 2 parallel = 135 hours = ~5.5 days.
Note: May need to reduce to 3 seeds (81 runs, ~3.4 days) if time-constrained.
```

---

## 9. REFERENCE NUMBERS TO BEAT

From published papers on Mip-NeRF 360 (averaged over 9 scenes):

| Method | Gaussians | PSNR | SSIM | LPIPS | Source |
|--------|-----------|------|------|-------|--------|
| 3DGS (Kerbl 2023) | 3.34M | 27.47 | 0.815 | 0.214 | Original paper |
| Mini-Splatting (2024) | 0.49M | 27.30 | 0.813 | 0.218 | ECCV 2024 |
| Scaffold-GS (2024) | 0.76M | 28.84 | -- | -- | CVPR 2024 |
| SteepGS (2025) | 1.61M | 28.73 | -- | -- | CVPR 2025 |

**Our target**: Match 3DGS PSNR (27.5 dB) with 2x fewer Gaussians, OR match Gaussian count with +0.3 dB improvement. Either would be publishable.

**Realistic expectation**: If Farey adds value beyond error-gating, we might see +0.1-0.3 dB improvement over the midpoint ablation. The mathematical novelty (provable bounds on densification) is the primary contribution regardless.

---

## 10. DECISION CHECKLIST BEFORE STARTING

Before Night 1, verify these manually:

- [ ] gsplat-mps venv activates and simple_trainer runs
- [ ] PyTorch version >= 2.0 with MPS support
- [ ] `torch.backends.mps.is_available()` returns True
- [ ] Enough disk space for dataset (~12 GB) + checkpoints (~2 GB per run)
- [ ] splat-apple cloned and its torch_gs/ code inspected for compatibility
- [ ] COLMAP binary parser handles cameras.bin format (PINHOLE vs SIMPLE_PINHOLE vs OPENCV)
- [ ] pytorch-msssim or kornia SSIM works on MPS tensors
- [ ] lpips package loads pretrained network on MPS

---

## 11. SOURCES

- gsplat-mps (local): ~/Desktop/gsplat-mps/ (v0.1.3 with Metal shaders)
- gsplat main: https://github.com/nerfstudio-project/gsplat
- gsplat densification API: https://docs.gsplat.studio/main/apis/strategy.html
- gsplat COLMAP example: https://docs.gsplat.studio/main/examples/colmap.html
- splat-apple: https://github.com/ghif/splat-apple
- OpenSplat: https://github.com/pierotofy/OpenSplat
- gsplat-mps fork: https://github.com/iffyloop/gsplat-mps
- Mip-NeRF 360 dataset: http://storage.googleapis.com/gresearch/refraw360/360_v2.zip
- nerfbaselines (dataset download): https://nerfbaselines.github.io/
- SteepGS: https://github.com/facebookresearch/SteepGS
- 3DGS original: https://github.com/graphdeco-inria/gaussian-splatting
