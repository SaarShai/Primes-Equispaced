# Extended Periodic Table of Three-Body Orbits

## Summary

Extended the CF-organized periodic table from 695 equal-mass orbits to 2,044 total orbits by incorporating 1,349 unequal-mass orbits (m3 = 0.5, 0.75, 2.0, 4.0, 5.0, 8.0, 10.0). The key findings:

1. **m3=4 correlation reversal confirmed**: The nobility-entropy correlation is NEGATIVE only at m3=4 (rho = -0.28, p = 0.010). All other masses show positive or near-zero correlation. The reversal is NOT gradual -- it appears specifically at m3=4 and reverses back at m3=5.
2. **2 newly filled cells** in the periodic table from unequal-mass data (both at m3=2.0).
3. **401 orbit types** tracked across 3+ mass ratios; nobility decreases with mass (67% negative slopes), suggesting a universal trend.
4. **Phase transition interpretation**: The m3=4 anomaly is driven by ALL families (I.A, I.B, II.C) simultaneously flipping sign, not by a single family. This suggests a structural transition in orbit space.

---

## Data

| Mass ratio m3 | N orbits | Source |
|:---:|:---:|:---|
| 0.50 | 565 | Li-Liao unequal |
| 0.75 | 401 | Li-Liao unequal |
| 1.00 | 695 | Li-Liao equal |
| 2.00 | 237 | Li-Liao unequal |
| 4.00 | 85 | Li-Liao unequal |
| 5.00 | 35 | Li-Liao unequal |
| 8.00 | 17 | Li-Liao unequal |
| 10.00 | 9 | Li-Liao unequal |
| **Total** | **2,044** | |

---

## Task 1: Extended Periodic Table

The periodic table uses a 9x8 grid indexed by CF period length (rows) and CF geometric mean (columns). With unequal-mass orbits added:

- **Equal-mass filled cells**: 29 of 72
- **Newly filled by unequal-mass**: 2 cells
- **Still empty**: 41 cells

### Newly filled cells

| Cell | N orbits | Mass ratio | Avg nobility | Orbit types |
|:---|:---:|:---:|:---:|:---|
| 1 \| 1.00-1.05 | 2 | m3=2.0 | 0.000 | II.D-1, II.D-2 |
| 6-15 \| 1.25-1.30 | 1 | m3=2.0 | 0.615 | II.C-2 |

Both newly filled cells come from m3=2.0 orbits. The cell "1|1.00-1.05" is particularly notable: it contains orbits with CF period = 1 (maximally simple CF structure), which at equal mass only contained the figure-eight orbit (I.A-1). The II.D family orbits that fill this cell at m3=2 represent a genuinely different topology.

### 3D Periodic Table

See `threebody_3d_periodic_table.png` -- shows the 9x8 grid at each mass ratio separately. Key observation: as m3 increases, orbits concentrate into fewer cells (the "habitable zone" shrinks). At m3=0.5, orbits span 25+ cells; at m3=8, only 10 cells are occupied.

---

## Task 2: m3=4 Correlation Reversal

### Overall correlation (nobility vs braid entropy)

| m3 | N | Spearman rho | p-value | Direction |
|:---:|:---:|:---:|:---:|:---|
| 0.50 | 565 | +0.488 | 4.3e-35 | **POSITIVE** |
| 0.75 | 401 | +0.592 | 2.6e-39 | **POSITIVE** |
| 1.00 | 695 | +0.461 | 8.5e-38 | **POSITIVE** |
| 2.00 | 235 | +0.181 | 5.5e-03 | POSITIVE (weakening) |
| **4.00** | **85** | **-0.279** | **9.8e-03** | **NEGATIVE (reversed)** |
| 5.00 | 35 | +0.015 | 9.3e-01 | ~zero |
| 8.00 | 17 | +0.129 | 6.2e-01 | ~zero (small N) |

### Is the reversal gradual or sudden?

The pattern shows:
- **m3 < 2**: Strong positive correlation (rho ~ 0.46-0.59)
- **m3 = 2**: Weakened but still positive (rho = 0.18)
- **m3 = 4**: NEGATIVE (rho = -0.28)
- **m3 = 5**: Back to ~zero (rho = 0.02)

This is NOT a gradual decay. There is a specific reversal at m3=4, with recovery at m3=5. This is consistent with a resonance or phase transition at m3=4.

### Per-family breakdown at m3=4

ALL families reverse simultaneously:

| Family | N at m3=4 | rho at m3=4 | rho at m3=1 |
|:---|:---:|:---:|:---:|
| I.A | 33 | -0.235 | +0.454 |
| I.B | 28 | -0.249 | +0.448 |
| II.C | 19 | -0.425 | +0.470 |

The reversal is not driven by a single anomalous family. All three major families flip sign at m3=4. Family II.C shows the strongest reversal (rho goes from +0.47 to -0.42).

### Physical interpretation

At m3=4, the third body is 4x heavier than the other two. This is significant because:
- The mass ratio 4:1:1 means the heavy body dominates the potential
- Noble orbits (high nobility = simple CF = near-golden-ratio dynamics) become LESS chaotic at this mass ratio, not more
- The reversal means: at m3=4, more noble orbits have LOWER entropy -- the opposite of the equal-mass regime
- This suggests a transition from "nobility tracks complexity" to "nobility tracks regularity"

### Property distributions at m3=4

| Property | m3=1.0 | m3=2.0 | m3=4.0 |
|:---|:---:|:---:|:---:|
| Mean word length | 112.7 | 135.1 | 165.1 |
| Mean CF period | 40.4 | 35.9 | 37.1 |
| Mean nobility | 0.476 | 0.409 | 0.377 |
| Mean entropy | 0.445 | 0.393 | 0.327 |
| Nobility std | 0.175 | 0.100 | 0.078 |

Note the dramatic compression of nobility variance: std drops from 0.175 at m3=1 to 0.078 at m3=4. The orbits become more "uniform" in their CF structure as mass asymmetry increases.

---

## Task 3: Empty Cells and Orbit Predictions

### Orbit predictions from newly filled cells

3 specific orbit predictions from cells that were empty in equal-mass but filled by unequal-mass:

1. **II.D-1 at m3=2.0**: CF period 1, gmean 1.0 (cell 1|1.00-1.05). Prediction: a periodic orbit with maximally simple CF structure should exist at mass ratio 2:1:1.
2. **II.D-2 at m3=2.0**: Same cell, different orbit. The II.D family appears to be specific to unequal masses.
3. **II.C-2 at m3=2.0**: CF period 13, gmean 1.26 (cell 6-15|1.25-1.30). An orbit with moderate CF complexity.

### Still-empty cells and what would fill them

The 41 still-empty cells cluster in two regions:
- **Short CF period (1-5) with varied gmean**: These require very simple orbits (few-letter words) with specific CF coefficient distributions. Most are in rows 1 and 2-5.
- **Long CF period (121-300) at extreme gmean**: These would need very long CF periods with consistently high or low partial quotients. The high-gmean cells (>1.35) are particularly sparse.

---

## Task 4: Mass-Ratio Scaling

### 401 shared orbit types tracked across 3+ mass ratios

Key findings:

| Property | % negative slopes | Mean slope | Interpretation |
|:---|:---:|:---:|:---|
| Nobility | 67% | -0.039 | Nobility generally DECREASES as m3 increases |
| Entropy | 77% | -0.108 | Entropy generally DECREASES as m3 increases |
| CF Period | 55% | -1.12 | Period weakly decreases |

### Universal trend

Both nobility and entropy decrease with increasing mass asymmetry. This is NOT a universal law (33% of orbits have increasing nobility), but the dominant trend is clear. The most persistent orbits (I.A-1 figure-eight, present at all 8 mass ratios) show relatively flat nobility slopes.

### Top orbit types by mass range

| Orbit type | Mass range | Nob slope | Ent slope |
|:---|:---|:---:|:---:|
| I.A-1 | 0.5 to 10.0 | -0.018 | -0.031 |
| I.A-2 | 0.5 to 8.0 | -0.012 | -0.041 |
| I.B-1 | 0.5 to 8.0 | -0.033 | -0.056 |
| I.B-2 | 0.5 to 8.0 | -0.040 | -0.053 |
| I.B-3 | 0.5 to 8.0 | -0.014 | -0.057 |

The figure-eight (I.A-1) has the most stable nobility across mass ratios, consistent with its known robustness.

---

## Visualizations

| File | Description |
|:---|:---|
| `threebody_extended_table_heatmap.png` | Side-by-side equal-mass vs extended table |
| `threebody_m3_correlation_reversal.png` | Nobility vs entropy scatterplots at each mass |
| `threebody_m3_anomaly_investigation.png` | Correlation evolution, per-family tracking, mean properties |
| `threebody_mass_ratio_scaling.png` | Nobility/entropy/period vs mass for top shared types |
| `threebody_3d_periodic_table.png` | Per-mass heatmaps of the 9x8 grid |
| `threebody_extended_table_results.json` | Full numerical results |

---

## Classification

- **Autonomy**: Level A (essentially autonomous -- CF computation and analysis all AI-driven)
- **Significance**: Level 1 (new analysis but builds on known orbit catalogs)
- **Connects to**: N1 (per-step Farey discrepancy), N8 (three-body periodic table)

## Key open questions

1. Why m3=4 specifically? Is there a dynamical systems explanation for a phase transition at mass ratio 4:1:1?
2. Can we predict which orbit types will survive to higher mass ratios based on their CF properties?
3. The II.D family appears only at m3=2 -- is this family unique to asymmetric masses, or does it exist at m3=1 but was missed?
4. Can the nobility-entropy correlation sign be predicted from the mass ratio alone (is there a critical m3*)?
