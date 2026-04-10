# Series 6-8: Real 3D Gaussian Splatting Experiments
## Farey-Guided Densification on Apple M5 Max

**Date**: 2026-03-27
**Hardware**: Apple M5 Max MacBook Pro (32 GPU cores, 36GB unified memory)
**Software**: PyTorch 2.8 + MPS backend
**Status**: PLAN ONLY — no code, no installs

---

## Codebase Selection: gsplat-mps (PRIMARY) + splat-apple (FALLBACK)

### Recommendation: gsplat-mps

**Winner: [gsplat-mps](https://github.com/iffyloop/gsplat-mps)** — fork of nerfstudio/gsplat v0.1.3 ported to Metal/MPS.

| Criterion | gsplat-mps | splat-apple |
|-----------|-----------|-------------|
| Densification built in | YES — full ADC with split/clone/prune | NO — basic optimization only, no densification |
| Densification location | `examples/simple_trainer.py` lines ~300-400 | Not implemented |
| Modifiability | Python, clean strategy pattern | Would need writing from scratch |
| Rendering pipeline | Full differentiable rasterization | Full differentiable rasterization |
| MPS support | Native Metal kernels | Native Metal + MLX backends |
| Training speed | ~5-8 it/s estimated on M5 Max | ~10-38 it/s (MLX faster) |
| NeRF Synthetic support | Yes, via simple_trainer | Requires COLMAP format conversion |
| Community/maturity | Fork of well-maintained gsplat | Newer, less tested |

**Critical finding**: splat-apple does NOT implement adaptive density control. Its `torch_gs/core/gaussians.py` (135 lines) contains only the Gaussian dataclass and initialization. Its `torch_gs/training/trainer.py` has only a single-step optimizer with no gradient accumulation, cloning, splitting, or pruning. Using splat-apple would require implementing the entire ADC baseline from scratch — unfair comparison territory.

gsplat-mps inherits the complete densification pipeline from nerfstudio/gsplat:

### Exact Densification Injection Points in gsplat-mps

**File**: `examples/simple_trainer.py`

Three functions to modify:

1. **`refine_split(self, mask)`** — Splits large Gaussians with high gradient
   - Creates 2 new Gaussians per masked Gaussian
   - Samples new positions along scaled axes
   - Reduces scale by factor of 1.6
   - Triggered when: `avg_grad > grow_grad2d` AND `scale > grow_scale3d`

2. **`refine_duplicate(self, mask)`** — Clones small Gaussians with high gradient
   - Copies parameters, zeros optimizer state
   - Triggered when: `avg_grad > grow_grad2d` AND `scale < grow_scale3d`

3. **`refine_keep(self, mask)`** — Prunes low-contribution Gaussians
   - Removes opacity < `prune_opa` (default 0.005)
   - Removes scale > `prune_scale3d` (default 0.1)

**Running statistics accumulation**: `update_running_stats()` normalizes 2D gradients and tracks per-Gaussian gradient norms and counts.

**Key thresholds**:
- `grow_grad2d`: 0.0002 (image-space gradient threshold)
- `grow_scale3d`: 0.01 (3D scale boundary for split vs clone decision)
- `prune_opa`: 0.005
- `prune_scale3d`: 0.1

### Farey Replacement Strategy

Replace `refine_split` + `refine_duplicate` with a single `farey_densify()` function:

```
Original pipeline:
  [train step] -> [accumulate grads] -> [if grad > threshold: split OR clone] -> [prune]

Farey pipeline:
  [train step] -> [accumulate grads] -> [build kNN graph on positions]
  -> [compute gap metrics on edges] -> [Farey-admit at level N]
  -> [error-gate with accumulated grad] -> [inject mediants] -> [prune]
```

**What stays identical**: rendering, loss, optimizer, learning rates, pruning, opacity reset, SH evaluation. Only the "where and when to add new Gaussians" logic changes.

### Fallback: splat-apple

If gsplat-mps has unresolved MPS bugs, splat-apple can serve as the renderer. We already have it cloned at `~/Desktop/Farey-Local/experiments/3dgs_real_test/splat-apple/`. In this case, we must implement BOTH baseline ADC and Farey densification from scratch (as done in `train_comparison.py`), but this means we control both codepaths — cleaner ablation but less trustworthy baseline.

---

## Dataset: NeRF Synthetic (Blender)

**Download**: `pip install nerfstudio && ns-download-data blender`
or from [Kaggle](https://www.kaggle.com/datasets/nguyenhung1903/nerf-synthetic-dataset)

**Format**: JSON-based (`transforms_train.json` with camera matrices), 800x800 RGBA images, 100 train + 200 test views per scene.

**Scenes** (ordered by complexity for our purposes):

| Scene | Gaussians (typical 3DGS) | Geometry character | Expected Farey advantage |
|-------|--------------------------|-------------------|-------------------------|
| lego | ~300K | Sharp edges, flat surfaces, repetitive structure | HIGH — lots of flat areas wasting Gaussians |
| chair | ~250K | Thin legs, flat seat, mixed scales | HIGH — extreme scale variation |
| hotdog | ~200K | Smooth surfaces, condiment detail | MEDIUM — moderate complexity |
| drums | ~350K | Thin sticks, curved surfaces | HIGH — thin structures |
| mic | ~150K | Simple geometry, fine mesh detail | MEDIUM |
| ficus | ~400K | Foliage = many thin features | VERY HIGH — ADC notoriously over-splits here |
| materials | ~200K | Mostly smooth, some reflections | LOW — less geometric complexity |
| ship | ~350K | Complex rigging, hull, water | HIGH — extreme scale variation |

**Priority for Series 6**: lego, chair, hotdog (canonical, well-understood baselines)
**Priority for Series 8**: Add ficus, drums, ship (increasing complexity)

**Note on format**: gsplat-mps's `simple_trainer.py` loads NeRF Synthetic JSON format natively. No COLMAP conversion needed.

---

## SERIES 6: Real 3D Gaussian Splatting — Farey vs ADC

### Goal
First real 3DGS comparison. Prove the concept works in actual differentiable rendering with multi-view images, not toy NumPy demos.

### Experimental Design

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Scenes | lego, chair, hotdog | Small, well-benchmarked, diverse geometry |
| Resolution | 400x400 (half-res) | Save memory on 36GB unified |
| Training steps | 10,000 | Short enough for iteration; gsplat converges well by 10K |
| Densify interval | 200 steps | Match our 2D Series 2 best result |
| Densify from | 500 | Standard warmup |
| Densify until | 8,000 | Leave 2K steps for fine-tuning |
| max_new per round | 15 | TIGHT BUDGET — this is where Farey wins |
| Opacity reset | every 3000 | Standard |
| Methods | (A) Baseline ADC, (B) Farey densification |
| Metrics | PSNR, SSIM, LPIPS, Gaussian count, wall-clock time |
| Repeats | 3 seeds per config | Statistical significance |

### Setup Commands

```bash
# 1. Create environment
conda create -n gsplat-mps python=3.10.14 -y
conda activate gsplat-mps

# 2. Install PyTorch 2.8 for MPS
pip install torch torchvision --index-url https://download.pytorch.org/whl/nightly

# 3. Clone and install gsplat-mps
cd ~/Desktop/Farey-Local/experiments
git clone https://github.com/iffyloop/gsplat-mps.git
cd gsplat-mps
pip install -e ".[dev]"
pip install -r examples/requirements.txt

# 4. Install additional deps for Farey
pip install scipy lpips  # scipy for spatial.KDTree, lpips for metric

# 5. Download NeRF Synthetic dataset
mkdir -p ~/Desktop/Farey-Local/data
cd ~/Desktop/Farey-Local/data
# Option A: via nerfstudio
pip install nerfstudio && ns-download-data blender --save-dir ./nerf_synthetic
# Option B: manual download from original NeRF site
wget http://cseweb.ucsd.edu/~viscomp/projects/LF/papers/ECCV20/nerf/nerf_synthetic.zip
unzip nerf_synthetic.zip

# 6. Verify MPS works
python -c "import torch; print(torch.backends.mps.is_available())"
python -c "from gsplat import rasterization; print('gsplat OK')"
```

### Files to Modify

**Primary modification**: `gsplat-mps/examples/simple_trainer.py`

Changes needed:
1. Add `--densify_method` argument: `"adc"` (baseline) or `"farey"`
2. Add `--max_new_per_round` argument (default 15)
3. Add `farey_densify()` function (replaces `refine_split` + `refine_duplicate`)
4. Add `--farey_level_schedule` argument: `"linear"` or `"sqrt"`
5. Keep `refine_keep()` (pruning) unchanged for both methods

**New file**: `gsplat-mps/examples/farey_strategy.py`

Contains:
- `build_neighbor_graph(positions, k=20)` — kNN via scipy.spatial.KDTree
- `compute_gap_metrics(positions, scales, edges)` — gap/scale ratio per edge
- `farey_admit(gap_metrics, level)` — admissibility filter
- `mediant_position(p_i, p_j, r_i, r_j)` — sigma-weighted midpoint
- `farey_densify(gaussians, optimizer, grad_accum, grad_count, config, farey_level)` — main entry point

**Why kNN instead of Delaunay**: In 3D with 100K+ points, Delaunay tetrahedralization is O(N^2) worst case and scipy's implementation is slow. kNN with k=20 via KDTree is O(N log N) and captures the essential neighbor structure. Our 2D experiments already showed kNN works as well as Delaunay for gap detection.

### Runtime Estimates

| Operation | Time (M5 Max est.) | Notes |
|-----------|-------------------|-------|
| gsplat install + compile Metal shaders | 5-10 min | One-time |
| Dataset download | 2-5 min | ~400MB |
| Single training run (10K steps, 400x400) | 20-40 min | ~5-8 it/s on MPS |
| Farey overhead per densify round | 0.5-2 sec | kNN on ~50K points |
| **Total per scene (2 methods x 3 seeds)** | **2-4 hours** | |
| **Total Series 6 (3 scenes)** | **6-12 hours** | Can parallelize scenes |

### Expected Outcome

Based on 2D results (+0.44 dB at tight budget, 6000 steps):
- Farey should show +0.2 to +0.5 dB PSNR advantage at tight budget (max_new=15)
- Gaussian count should be SIMILAR (both budget-limited)
- The gap may be smaller than 2D because 3DGS ADC already has clone+prune (fairer baseline)
- If we see +0.3 dB at same Gaussian count: this is a publishable result

### Failure Modes to Watch

1. **gsplat-mps Metal kernel crashes**: The repo warns it is "not thoroughly tested." Have splat-apple fallback ready.
2. **kNN too slow at scale**: If >5 sec per densify round, switch to approximate NN (FAISS or spatial hashing).
3. **Farey too conservative**: If Farey adds far fewer Gaussians than budget allows, the gap metric thresholds need tuning. Start with `gap_lower_bound=1.0`, adjust to 0.5 if needed.
4. **Memory pressure**: 36GB unified is tight for 800x800. Use 400x400 or reduce SH degree to 2.

---

## SERIES 7: 3D Budget Sweep

### Goal
Confirm the 2D finding that Farey's advantage is concentrated at tight budgets. This is the 3D analog of Series 3 (2D budget sweep).

### Experimental Design

| Parameter | Value |
|-----------|-------|
| Scene | lego (fixed) |
| Resolution | 400x400 |
| Training steps | 10,000 |
| Densify interval | 200 |
| Methods | ADC baseline, Farey |
| **max_new per round** | **5, 10, 15, 20, 30, 50, unlimited** |
| Seeds | 3 per config |

This gives 7 budget levels x 2 methods x 3 seeds = **42 runs**.

### Setup Commands

Same environment as Series 6. New script only:

```bash
# Run budget sweep
python series7_budget_sweep.py \
  --scene lego \
  --budgets 5 10 15 20 30 50 999999 \
  --methods adc farey \
  --seeds 3 \
  --steps 10000 \
  --output ~/Desktop/Farey-Local/experiments/3dgs_results/series7_budget.json
```

### Files to Modify/Create

**New file**: `gsplat-mps/examples/series7_budget_sweep.py`

Wraps `simple_trainer.py` logic in a sweep loop. For each (budget, method, seed) triple:
1. Initialize from same point cloud (deterministic per seed)
2. Train with specified densification method and budget
3. Log metrics at steps 2000, 5000, 8000, 10000
4. Save final Gaussian count and all metrics to JSON

### Runtime Estimates

| Config | Time per run | Count |
|--------|-------------|-------|
| Tight budget (5-15) | 15-25 min | 18 runs |
| Medium budget (20-30) | 20-30 min | 12 runs |
| Unlimited | 25-40 min | 6 runs |
| Overhead (saves, logging) | ~1 min | 42 runs |
| **Total Series 7** | **~14-20 hours** | |

### Key Predictions (from 2D results)

| max_new | 2D Result (dB diff) | 3D Prediction |
|---------|---------------------|---------------|
| 5 | Not tested | Farey +0.2 to +0.5 dB (strongest advantage) |
| 10 | +0.11 dB | Farey +0.1 to +0.3 dB |
| 15 | ~+0.25 dB (interpolated) | Farey +0.1 to +0.3 dB |
| 20 | ~+0.0 dB (crossover) | Farey ~0 dB (crossover point) |
| 30 | -3.05 dB | Farey -0.5 to -2.0 dB (too conservative) |
| 50 | Not tested | Farey negative (ADC catches up) |
| unlimited | Not tested | Farey likely negative |

**The crossover budget** is the key deliverable of Series 7. In 2D it was around max_new=20. In 3D it may differ because:
- 3D scenes have more spatial structure (helps Farey)
- 3DGS clone operation partially overlaps with Farey's gap-filling (hurts Farey's relative advantage)

### Analysis

Plot: PSNR (y-axis) vs max_new_per_round (x-axis), two curves (ADC, Farey).
The crossover point tells us the optimal operating regime for Farey densification.

---

## SERIES 8: 3D Scene Complexity Scaling

### Goal
Test whether Farey's advantage grows with scene complexity, as predicted by the FAREY_3DGS_3D_DESIGN.md analysis. Scenes with high scale variation (thin structures mixed with flat surfaces) should benefit most.

### Experimental Design

| Parameter | Value |
|-----------|-------|
| Scenes | mic, hotdog, lego, chair, drums, ficus, ship (7 scenes, ordered by complexity) |
| Resolution | 400x400 |
| Training steps | 10,000 |
| Densify interval | 200 |
| max_new per round | 15 (fixed at tight budget, the Farey sweet spot from Series 7) |
| Methods | ADC baseline, Farey |
| Seeds | 3 per config |

This gives 7 scenes x 2 methods x 3 seeds = **42 runs**.

### Complexity Proxy Metrics

For each scene, also measure:
- **Scale variance**: std(log(scale)) across all Gaussians — higher = more diverse scales
- **Spatial entropy**: entropy of Gaussian position distribution on a 32^3 grid
- **Surface area / volume ratio**: from the mesh (available for NeRF Synthetic)

These become the x-axis for the scaling analysis.

### Setup Commands

Same environment as Series 6-7. All 8 NeRF Synthetic scenes needed.

```bash
# Run scene complexity sweep
python series8_scene_sweep.py \
  --scenes mic hotdog lego chair drums ficus ship \
  --max_new 15 \
  --methods adc farey \
  --seeds 3 \
  --steps 10000 \
  --output ~/Desktop/Farey-Local/experiments/3dgs_results/series8_scenes.json
```

### Files to Modify/Create

**New file**: `gsplat-mps/examples/series8_scene_sweep.py`

Similar to Series 7 sweep, but iterates over scenes instead of budgets. Additionally computes per-scene complexity metrics.

### Runtime Estimates

| Item | Time |
|------|------|
| Per run (10K steps) | 20-40 min |
| 42 total runs | 14-28 hours |
| Complexity metric computation | ~5 min per scene |
| **Total Series 8** | **~15-30 hours** |

### Key Predictions

| Scene | Complexity | Predicted Farey advantage |
|-------|-----------|--------------------------|
| mic | Low (simple geometry) | Small (+0.0 to +0.1 dB) |
| materials | Low (smooth surfaces) | Small (+0.0 to +0.1 dB) |
| hotdog | Medium | Medium (+0.1 to +0.3 dB) |
| lego | Medium-High | Medium (+0.2 to +0.4 dB) |
| chair | High (scale variation) | High (+0.3 to +0.5 dB) |
| drums | High (thin structures) | High (+0.3 to +0.5 dB) |
| ficus | Very High (foliage) | Highest (+0.4 to +0.6 dB) |
| ship | Very High (multi-scale) | High (+0.3 to +0.5 dB) |

### Analysis

1. **Scatter plot**: Scene complexity metric (x) vs Farey advantage in dB (y). If there is a positive correlation, Farey densification is more valuable for complex scenes.
2. **Per-scene bar chart**: PSNR for ADC vs Farey, grouped by scene.
3. **Gaussian efficiency**: PSNR / Gaussian_count for each method and scene.

---

## Implementation Roadmap

### Phase 1: Environment Setup (Day 1, ~2 hours)
- [ ] Install gsplat-mps in conda environment
- [ ] Verify MPS rendering works (run simple_trainer on default scene)
- [ ] Download NeRF Synthetic dataset
- [ ] Time a baseline run to calibrate runtime estimates

### Phase 2: Farey Integration (Day 1-2, ~4-6 hours)
- [ ] Write `farey_strategy.py` with kNN-based gap detection
- [ ] Modify `simple_trainer.py` to accept `--densify_method` flag
- [ ] Add budget cap (`--max_new_per_round`) to both ADC and Farey paths
- [ ] Run single sanity check: lego, 2000 steps, both methods — verify no crashes

### Phase 3: Series 6 Execution (Day 2-3, ~6-12 hours)
- [ ] Run all Series 6 configs (3 scenes x 2 methods x 3 seeds = 18 runs)
- [ ] Analyze results, generate comparison plots
- [ ] Decide if we proceed or need to fix issues

### Phase 4: Series 7 Execution (Day 3-4, ~14-20 hours)
- [ ] Run budget sweep on lego (42 runs)
- [ ] Plot crossover curve
- [ ] Determine optimal budget for Farey

### Phase 5: Series 8 Execution (Day 4-5, ~15-30 hours)
- [ ] Run scene complexity sweep (42 runs)
- [ ] Compute complexity metrics
- [ ] Generate scaling analysis plots

### Phase 6: Analysis and Write-up (Day 5-6)
- [ ] Compile all results into unified comparison table
- [ ] Generate publication-quality figures
- [ ] Update FAREY_3DGS_PAPER_OUTLINE.md with real numbers
- [ ] Identify next steps (full Scaffold-GS integration or pivot)

**Total estimated calendar time: 5-6 days** (much of it unattended training runs)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| gsplat-mps Metal kernel crashes | MEDIUM | HIGH — blocks all experiments | Fall back to splat-apple + custom ADC baseline (already prototyped in train_comparison.py) |
| PyTorch 2.8 MPS incompatibility | LOW | HIGH | Pin to PyTorch 2.5 which is known to work |
| 36GB memory insufficient for 800x800 | MEDIUM | LOW | Use 400x400 (already planned) |
| Farey kNN overhead too slow | LOW | MEDIUM | Use approximate NN (FAISS) or spatial hashing |
| Farey shows no advantage in 3D | MEDIUM | MEDIUM | Still publishable as negative result; confirms tight-budget niche |
| gsplat-mps v0.1.3 is too old | MEDIUM | MEDIUM | Cherry-pick Metal kernels into newer gsplat if needed |

---

## Relationship to Prior Work

### Our 2D Results (Series 1-5)
- Series 1-2: Farey wins at tight budgets, loses at generous ones
- Series 3: Budget sweep confirmed crossover around max_new=20
- Series 4-5: Scene/gap analysis (in progress)
- **Series 6-8 directly extends these findings to real 3D**

### Published Baselines to Compare Against
- Original 3DGS (Kerbl et al., 2023): ~27-33 dB on NeRF Synthetic
- gsplat simple_trainer: typically within 0.5 dB of original 3DGS
- We do NOT need to match SOTA; we need to show Farey > ADC at same budget

### What Would Be Publishable
- +0.3 dB PSNR at same Gaussian count on 3+ scenes: workshop paper
- +0.5 dB or 1.5x fewer Gaussians: full conference paper (CVPR/ECCV)
- Clear correlation between scene complexity and Farey advantage: strong narrative

---

## Key Design Decisions

1. **kNN over Delaunay in 3D**: Delaunay tetrahedralization is O(N^2) worst case and scipy's 3D implementation is slow for >50K points. kNN with k=20 captures the essential neighbor structure at O(N log N) cost.

2. **Budget-capped ADC baseline**: Standard 3DGS has no per-round budget cap. By adding one to the baseline too, we ensure a FAIR comparison — both methods get the same number of new Gaussians per round, differing only in WHERE they place them.

3. **Half-resolution (400x400)**: The NeRF Synthetic images are 800x800. Half-res saves ~4x memory and ~2x time. Published results often report at 800x800, but for a first validation pass, 400x400 is standard practice.

4. **10K steps instead of 30K**: Standard 3DGS trains for 30K steps. We use 10K because (a) faster iteration, (b) our 2D results showed Farey's advantage grows with training duration, so if it works at 10K it should be even better at 30K, and (c) 10K is enough for convergence on NeRF Synthetic at half-res.

5. **gsplat-mps over OpenSplat**: OpenSplat is C++ — much harder to modify for custom densification. gsplat-mps is Python with clean separation of rendering and densification, making it ideal for research experimentation.
