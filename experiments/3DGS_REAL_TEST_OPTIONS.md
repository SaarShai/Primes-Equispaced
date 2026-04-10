# 3DGS Real Test Options: Honest Assessment

**Date:** 2026-03-29
**Hardware:** Apple M5 Max, MPS/Metal, no CUDA GPU
**Python:** 3.9.6 (system), no conda

---

## 1. Can We Run REAL 3DGS on Apple Silicon RIGHT NOW?

### Option A: splat-apple (MOST PROMISING)
- **Location:** `~/Desktop/3dgs-experiment/splat-apple/`
- **Status:** Cloned, has both MLX and PyTorch(MPS) backends
- **COLMAP support:** YES -- loads bicycle directly via `load_colmap_dataset()`
- **Scene normalization:** YES -- has `--normalize` flag for 360 scenes
- **Densification:** NO. Fixed Gaussian count from SfM initialization only. No split/clone/prune.
- **MLX backend:** BLOCKED -- requires Python 3.12+, we have 3.9.6
- **PyTorch backend:** AVAILABLE -- MPS works with PyTorch 2.8.0
- **Speed estimate:** ~0.84 it/s (pure Python rasterizer), ~10.6 it/s (C++ GCD mode, needs build)
- **Critical limitation:** Without densification, this is NOT real 3DGS. It just optimizes the ~54K SfM points as Gaussians. No adaptive refinement = no valid comparison to ADC.

### Option B: gsplat-mps (PARTIALLY VIABLE)
- **Location:** `~/Desktop/gsplat-mps/`
- **Status:** Installed (gsplat 1.5.3 pip, fork cloned)
- **What it does:** MPS-ported rasterizer from gsplat 0.1.3
- **Training script:** `examples/simple_trainer.py` -- fits random Gaussians to a single image
- **Multi-view training:** NO built-in multi-view pipeline
- **Densification:** NO. Fixed point count.
- **COLMAP support:** NO. The simple_trainer fits to one image.
- **Usefulness:** Could be used as a rasterizer backend if we write our own training loop with densification. Significant engineering effort.

### Option C: OpenSplat (BEST FULL PIPELINE, BUT BLOCKED)
- **Status:** Not installed
- **What it offers:** Full 3DGS pipeline with ADC densification, COLMAP input, Metal GPU backend
- **Build requirement:** CMake + `-DGPU_RUNTIME=MPS` + Xcode.app (not just CommandLineTools)
- **BLOCKER:** Xcode.app is NOT installed. Only CommandLineTools present. Metal shader compilation requires full Xcode.
- **Fix:** Install Xcode.app from App Store (~12 GB download), then `sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer`
- **If Xcode installed:** Could build and run bicycle scene. Has real ADC densification. ~12 min for 2K steps on M2 (M5 Max would be faster).
- **This is the only path to a real ADC comparison on local hardware.**

### Option D: Mainline gsplat 1.5.3
- **Status:** Installed via pip
- **MPS support:** NO. All rasterization calls go through CUDA kernels. Hardcoded `device="cuda"`.
- **Verdict:** Cannot use on Apple Silicon for training.

### Option E: Pure-PyTorch 3DGS (No custom kernels)
- **Not found.** All serious implementations use custom CUDA or Metal kernels for the rasterizer. A pure-Python/PyTorch rasterizer would be ~100x slower and impractical for multi-view scenes.

---

## 2. Dataset Status

**Mip-NeRF 360 bicycle scene: READY**

| Item | Status |
|------|--------|
| `~/Desktop/nerf_data/bicycle/sparse/0/cameras.bin` | Present |
| `~/Desktop/nerf_data/bicycle/sparse/0/images.bin` | Present |
| `~/Desktop/nerf_data/bicycle/sparse/0/points3D.bin` | Present (54,275 sparse points) |
| `images/` (full res) | 194 images |
| `images_4/` (1237x822) | 194 images |
| `images_8/` (618x411) | 194 images |

Other scenes available: bonsai, counter, garden, kitchen, room, stump.

---

## 3. Cloud GPU Options

### Google Colab (Free T4)
- Free tier: T4 GPU (16GB VRAM), 12-hour session limit
- Can run original 3DGS or gsplat natively
- **Bicycle at images_8 (618x411), 7K iterations:** ~15-20 minutes
- **Bicycle at images_4 (1237x822), 30K iterations:** ~2-3 hours
- **Cost:** Free
- **Limitation:** Need to upload dataset (~2 GB for bicycle) or mount from Drive

### Lambda Labs / RunPod / Vast.ai
- A100 40GB: ~$1.10/hr
- **Bicycle full pipeline (30K iters, images_4):** ~30 min on A100
- **Total cost:** ~$1-2
- Easiest: use nerfstudio or gsplat's example trainer

### Recommendation: Colab is sufficient and free.

---

## 4. Is It Even Worth It?

### What our 2D tests actually showed:

**Kodak benchmark (real images, 5K steps, ~1000 Gaussians):**
- ADC: 24.52 dB PSNR
- Farey: 24.89 dB PSNR
- Delta: **+0.37 dB** (modest, within noise for a single image)
- Gaussian count: roughly equal (~985 vs ~1014)
- **No compactness advantage on real images**

**Budget-matched test (100 Gaussians, same image):**
- ADC: 21.04 dB
- Farey: (similar range)
- At low budgets on real images, both methods are comparable

**Synthetic density fields (our strongest results):**
- 1D: 33x efficiency (but this is fitting a 1D signal, not rendering)
- 2D: 2.4-3.6x efficiency (synthetic patterns with known frequency structure)
- 3D: 11.5x test MSE improvement (synthetic sphere+bumps, not images)

### The pattern is clear:
Farey's advantage **decreases** as the task gets more realistic:
- Synthetic 1D: 33x
- Synthetic 2D: 2.4-3.6x
- Synthetic 3D: 11.5x (density field)
- Real 2D images: +0.37 dB (~1.09x)

### Why 3D rendering is unlikely to be different:

1. **Real images lack the clean frequency structure** that Farey exploits. The mediant-based placement works well when there are sharp boundaries between smooth and complex regions. Real scenes have gradual, overlapping complexity.

2. **Error-guided placement already adapts.** ADC uses gradient magnitudes -- essentially error signals -- to decide where to split. This is already adaptive to the actual rendering loss landscape.

3. **Densification is not the bottleneck in modern 3DGS.** Recent work (Mini-Splatting, CompGS, HAC) shows that the bigger wins come from compression, better initialization, and anti-aliasing -- not densification strategy.

4. **The 54K SfM initialization already covers the scene well.** Unlike our synthetic tests starting from 25-64 points, real 3DGS starts with thousands of points from COLMAP. The initialization advantage of Farey placement is diluted.

### Honest prediction for bicycle scene:
- Farey densification vs ADC: likely within +/- 0.5 dB PSNR
- Possible slight advantage in compactness (fewer Gaussians for same quality) but not dramatic
- Will NOT show the 2x-30x improvements seen on synthetic data

---

## 5. Minimum Viable Test

### If we proceed anyway (and we should, for honest reporting):

**Setup:** Google Colab (free T4)

**Scene:** bicycle (standard benchmark, 194 images, most-cited)

**Resolution:** images_8 (618x411) for quick test, images_4 for publication

**Protocol:**
1. Run original 3DGS (Kerbl et al.) with default ADC -- this is baseline
2. Modify densification to use Farey-guided insertion:
   - Replace gradient threshold with gap-weighted criterion
   - Use mediant positions instead of clone/split positions
   - Keep everything else identical (learning rates, loss, pruning schedule)
3. Run both for 7K iterations (quick validation) then 30K (publication)
4. Compare: PSNR, SSIM, LPIPS, Gaussian count, training time

**Expected timeline:**
- 7K quick test: ~20 min on Colab T4
- 30K publication run: ~2-3 hours on Colab T4
- Modifying the densification code: ~2-4 hours of engineering

**What comparison to include:**
- ADC (original) vs Farey densification (ours) -- this is our claim
- Do NOT compare against SOTA methods (3DGS-MCMC, Mini-Splatting, etc.) -- that would set us up for embarrassment since those methods address fundamentally different bottlenecks

---

## 6. The Honest Bottom Line

### What we can claim (defensible):
- Farey sequences provide a **mathematically principled** densification framework with provable properties (bounded insertion, no cascading, monotonic information gain)
- On **synthetic density fields**, this gives measurable efficiency gains (2-10x)
- The framework is **theoretically elegant** and connects to deep number theory

### What we CANNOT claim (yet):
- That Farey densification improves real 3DGS rendering quality
- That it beats ADC on standard benchmarks
- That it saves significant compute on real scenes

### Should we run the test?
**YES, but with correct framing.** The value is:
1. If it works (+0.5 dB or more): genuine contribution, publish
2. If it ties (within 0.3 dB): still publishable as "principled alternative with theoretical guarantees"
3. If it loses: honest negative result, still valuable for the community, pivots our paper framing

**The worst outcome is NOT running the test and claiming things we haven't verified.**

### Recommended next step:
Install Xcode.app (enables OpenSplat local build) OR set up a Colab notebook with gsplat + modified densification. Either path gets us to a real answer in one afternoon.

---

## Appendix: Local Path Without Cloud GPU

If we want to avoid cloud entirely:

1. **Install Xcode.app** (~12 GB, from App Store)
2. **Build OpenSplat** with Metal: `cmake -B build -DGPU_RUNTIME=MPS && cmake --build build`
3. **Run bicycle:** `./build/opensplat ~/Desktop/nerf_data/bicycle/ --val-render`
4. **Modify densification** in OpenSplat's C++ code (harder than Python, but possible)
5. **Expected time:** ~30-60 min training on M5 Max at images_8 resolution

This path gives us a real local test but requires C++ modification of the densification logic, which is significantly harder than modifying Python code in Colab.
