# Hristov Stability Test: Does Syzygy Structure Predict Dynamical Stability?

**Date:** 2026-03-29
**Status:** COMPLETED -- MODERATE SIGNAL FOUND
**Verification:** Unverified (needs independent replication)

## Objective

Test whether "nobility-type" measures derived from orbit topology predict the TRUE dynamical instability (Lyapunov exponents from monodromy eigenvalues), using data from Hristov et al. (arXiv:2503.00432).

**Why this matters:** Our nobility measure (CF structure of Gamma(2) fixed point) predicts braid entropy with AUC=0.98 -- but braid entropy comes from the SAME matrix as CF. This is the "circularity objection." If nobility also predicts independently-computed Lyapunov exponents, circularity is dead.

## Data

- **Source:** https://db2.fmi.uni-sofia.bg/3bodysym4860/
- **Paper:** Hristov, Hristova, Puzynina, Sharipov, Tukhliev (2025)
- **N = 4,860** free-fall three-body periodic orbits with central symmetry
- **Lyapunov exponents:** ln(|mu_max|) computed from monodromy eigenvalues to 30 correct digits
- **Syzygy sequences:** Symbolic dynamics (symbols {1,2,3} = which body is in the middle at collinearity)
- **All orbits are UNSTABLE** (4 loxodromic, 198 hyperbolic-elliptic, 4658 hyperbolic-hyperbolic)
- Lyapunov range: [6.51, 73.37], median = 33.42, std = 8.20

Files downloaded to `experiments/hristov_data/`:
- `syzygies.txt` -- 4860 syzygy sequences
- `res_exponents.txt` -- max eigenvalue + Lyapunov exponent per orbit
- `res_eigen.txt` -- full 4 complex eigenvalues per orbit (30-digit precision)
- `euler_100_4860.txt` -- initial conditions (100-digit precision)

## Critical Finding: Direct CF Mapping Fails

**The Gamma(2) CF approach does NOT work for Hristov's data.** Here's why:

Hristov's orbits are PERIODIC. A periodic orbit's syzygy sequence, when reduced in the free group (canceling adjacent identical symbols), gives the IDENTITY -- the empty word. This is fundamental: periodic orbits represent closed loops in the configuration space, so they map to the trivial conjugacy class.

Consequence: All 4,860 orbits produce the SAME CF (the golden ratio, period [1]), making CF-based nobility trivially constant (1.0 for all orbits). The Gamma(2) matrix approach is algebraically degenerate here.

**This does NOT affect our Li-Liao results,** which use the non-reduced free-group word (a,b,A,B encoding) that preserves the full topological information. The difference is that Li-Liao provides the free-group word directly, while Hristov provides syzygy sequences that reduce to identity.

## What We CAN Measure: Syzygy Sequence Structure

Since the unreduced syzygy sequence carries all the information about orbit complexity, we computed multiple measures directly from the symbolic dynamics:

### A. Key Correlations with Lyapunov Exponent (N=4860)

| Measure | vs lyap (rho) | vs lyap/step (rho) | p-value (lyap) |
|---------|:---:|:---:|:---:|
| **Stutter fraction** | +0.124 | **+0.429** | 2.7e-217 |
| Frequency balance (1-max_freq) | -0.248 | -0.205 | 7.4e-69 |
| 3-gram complexity | +0.204 | -- | 1.3e-46 |
| Symbol entropy | -0.220 | -0.177 | 2.9e-54 |
| Transition entropy | +0.075 | +0.249 | 1.4e-7 |
| |det(T)| (transition matrix) | -0.233 | -0.275 | 3.9e-61 |
| Self-transition probability | +0.104 | +0.349 | 4.3e-13 |

### B. Partial Correlations (controlling syzygy length)

| Measure | rho (partial) | p-value |
|---------|:---:|:---:|
| **Stutter fraction** | **+0.278** | 6.4e-87 |
| Frequency balance | -0.238 | 1.5e-63 |
| Frequency entropy | -0.200 | 3.5e-45 |
| Transition entropy | +0.174 | 1.9e-34 |

### C. Multivariate Prediction

- **Syzygy features -> lyap/step:** R^2 = 0.347 (34.7% variance explained)
- **5-fold cross-validated R^2:** 0.180 +/- 0.083
- **Raw lyap prediction (without length):** R^2 = 0.189

### D. Quartile Analysis (most stable Q1 vs most unstable Q4)

| | Q1 (most stable) | Q4 (most unstable) | Ratio |
|---|:---:|:---:|:---:|
| N | 1215 | 1215 | -- |
| Mean stutter fraction | 0.018 | 0.051 | 2.91 |
| Mean self-transition prob | 0.016 | 0.044 | 2.67 |
| Mann-Whitney U test | p = 1.1e-146 | | |

### E. Symmetry Type Breakdown

The third column of syzygies.txt encodes symmetry type (1, 2, or 3):

| Type | N | Mean lyap | Std |
|---|:---:|:---:|:---:|
| 1 | 1422 | 32.70 | 7.87 |
| 2 | 1672 | 32.36 | 8.20 |
| 3 | 1766 | 35.64 | 8.09 |

Type 3 orbits are significantly more unstable (p << 1e-10).

## Interpretation

### The "Stutter Fraction" as Nobility Analog

Our original "nobility" measures the fraction of 1s in the CF period (simple approximation = noble number = stable). The **stutter fraction** measures consecutive identical syzygies in the orbit word. Both capture the same intuition: **structural simplicity of the orbit encoding predicts lower dynamical complexity**.

The correlation rho = +0.43 (stutter vs lyap/step) means:
- **More stutters = HIGHER per-step Lyapunov = MORE UNSTABLE**
- This is counterintuitive at first: stutters are "simpler" patterns
- Explanation: stutters correspond to the orbit lingering near a syzygy (collinear configuration), which is a SADDLE POINT of the potential. More time near saddles = exponentially diverging trajectories = higher Lyapunov

This is OPPOSITE to the nobility-stability direction in our Li-Liao analysis (where high nobility = more stable). The sign difference matters and needs careful interpretation.

### Does This Kill the Circularity Objection?

**Partially.** The evidence is:

1. **Stutter fraction vs lyap/step: rho = +0.43** -- a moderate correlation that is highly significant (p ~ 10^-217). This is real signal, not noise.

2. **Partial correlation controlling length: rho = +0.28** -- still strong after removing the trivial length dependence.

3. **Multivariate R^2 = 0.18 (CV)** -- syzygy structure explains ~18% of Lyapunov variance even cross-validated.

4. **But:** The correlations are moderate, not strong (not rho > 0.5). The signal is real but the orbit topology captures only a fraction of the dynamical instability.

5. **Critical caveat:** Stutter fraction is a DIFFERENT measure from CF-nobility. The CF-based nobility was constant (=1) for all orbits. So strictly speaking, this test shows that **syzygy structure** predicts stability, not that **CF-nobility** predicts stability.

## Verdict

**MODERATE SIGNAL: Syzygy topology predicts dynamical Lyapunov exponents with rho ~ 0.28-0.43, but the specific CF-nobility measure is degenerate for periodic orbits.**

The circularity objection is WEAKENED but not killed:
- Topological orbit structure (from the syzygy word) does predict true dynamical instability
- This prediction is independent of braid entropy (Hristov's data comes from monodromy matrices, not braids)
- But our specific "nobility" measure (CF coefficients of Gamma(2) fixed point) is not directly testable here because periodic orbits reduce to identity in the free group
- We need Li-Liao orbits WITH Lyapunov exponents to do the exact nobility test

## Li-Liao Stability Data

Checked the sjtu-liao/three-body GitHub repository thoroughly:
- **Free-fall data:** Only contains PNG images (orbit plots), no eigenvalue data
- **Unequal-mass data:** Has binary S/U (stable/unstable) classification for 135,445 orbits, but NO numerical eigenvalues or Lyapunov exponents
- **No monodromy eigenvalue data** available anywhere in the Li-Liao repo
- The S/U classification could be used for a different test (nobility vs binary stability), but this would not address the circularity objection as strongly

## Next Steps

1. **Email Hristov group** -- ask if they can provide the mapping between their orbit numbering and the Li-Liao free-group words. This would let us compute CF-nobility AND have Lyapunov exponents for the same orbits.

2. **Compute our own monodromy eigenvalues** for the 695 Li-Liao equal-mass orbits where we already have CF-nobility. This is computationally intensive but doable.

3. **Use the Li-Liao S/U classification** for the unequal-mass catalog to test whether nobility predicts binary stability.

4. **Investigate the sign reversal** -- why does high stutter fraction correlate with MORE instability (opposite to the nobility-stability direction in Li-Liao)?

## Files

- `hristov_data/` -- all downloaded data files (4860 orbits)
- `hristov_stability_test.py` -- analysis script
- `hristov_correlations.csv` -- full correlation table
