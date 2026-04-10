# Google Colab Batch Run Instructions

## Overview

Four notebooks ready for Colab execution. Each is self-contained with Quick and Full modes.

| # | Notebook | GPU? | Quick | Full | Key Test |
|---|----------|------|-------|------|----------|
| 1 | `3dgs_colab_definitive_test.ipynb` | T4 required | ~15 min | ~2 hr | 3DGS Farey vs ADC densification |
| 2 | `colab_3bp_unequal_mass.ipynb` | No | ~1 min | ~30 min | Nobility predicts 3-body stability? |
| 3 | `colab_r_bound_extension.ipynb` | No | ~2 min | ~15 min | R > -1/2 for all M(p)<=-3 primes |
| 4 | `colab_ramanujan_filter.ipynb` | No | ~1 min | ~5 min | M(q)-ordered filter bank savings |

## Step-by-Step Instructions

### 1. Upload notebooks to Colab

Option A (recommended): Upload to Google Drive, then open from Drive.
Option B: Go to https://colab.research.google.com -> File -> Upload notebook.

### 2. Set runtime type

For **Notebook 1 only** (3DGS):
- Runtime -> Change runtime type -> T4 GPU

For Notebooks 2-4: default CPU runtime is fine.

### 3. Set execution mode

In the **Configuration** cell of each notebook, change:
```python
MODE = 'quick'   # for fast test (~1 min)
MODE = 'full'    # for complete analysis
```

Recommendation: Run Quick first to verify everything works, then Full.

### 4. Run all cells

Runtime -> Run all (Ctrl+F9)

### 5. Collect results

Each notebook saves:
- A JSON file with all numerical results
- A PNG plot with visualizations

If Google Drive is mounted, results auto-save to `/content/drive/MyDrive/Farey_Results/`.

Otherwise, download manually from the Colab file browser (left sidebar).

## Results to Copy Back

### Notebook 1 (3DGS)
- `3dgs_definitive_results.json` -- PSNR, SSIM, LPIPS for Farey vs ADC
- Training curve plots
- **Key number:** PSNR difference (Farey minus ADC)
- **Kill criterion:** If PSNR difference < 0.5 dB on real scene, it is a NO-GO

### Notebook 2 (3BP)
- `3bp_unequal_mass_results.json` -- Nobility and stability for each orbit
- `3bp_nobility_analysis.png` -- Distributions and scatter plots
- **Key number:** Logistic regression AUC for nobility vs word-length
- **Kill criterion:** If nobility AUC < word-length AUC, nobility adds no value

### Notebook 3 (R-bound)
- `r_bound_verification_results.json` -- R(p) for every prime
- `r_bound_verification.png` -- R vs p scatter
- **Key number:** min(R) across all tested primes
- **Kill criterion:** If any R <= -1/2, the bound fails

### Notebook 4 (Ramanujan Filter)
- `ramanujan_filter_results.json` -- Detection counts per ordering
- `ramanujan_filter_results.png` -- Bar chart comparison
- **Key number:** Mean M(q)/Sequential ratio
- **Kill criterion:** If ratio >= 0.90, it is NO-GO

## Troubleshooting

- **OOM on 3DGS:** Reduce `N_POINTS_INIT` in the config cell, or use a smaller scene
- **Download fails for Li-Liao data:** Check GitHub rate limits; wait and retry
- **Slow Fraction arithmetic:** Expected for R-bound at large primes; the exact arithmetic is intentional
- **Import errors:** The first cell in each notebook installs dependencies; re-run if needed
