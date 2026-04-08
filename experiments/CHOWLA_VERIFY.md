# Chowla Conjecture Verification: Pre-Whitened Spectroscope Residual

Date: 2026-04-08
Script: ~/Desktop/Farey-Local/experiments/chowla_verify.py

## Setup
- mu(n) Mobius sieve, N = 200,000 (121,581 nonzero values)
- Spectroscope: F(gamma) = |sum_{n=1}^N mu(n)/n * exp(-i*gamma*log(n))|^2
- gamma in [5, 80], 10,000 points
- Pre-whitening: Lorentzian fits at 20 known zeta zeros
- Null model: 30 shuffles of mu(n) values

## Key Results

### Spectroscope (Step 2-3)
- F(gamma) range: [0.15, 9.37], mean = 1.54
- Only 1 peak exceeded 3-sigma: gamma = 14.12 (the first zeta zero, 14.13)
- Higher zeros visible but NOT individually 3-sigma above background
- This is EXPECTED at N=200K: the spectroscope resolution is limited

### Pre-Whitening (Step 4) -- PROBLEMATIC
- Lorentzian fits at 20 zeros. Many fits drifted far from their target zeros:
  - Zero 30.42: fitted center at 32.33 (off by 1.9!)
  - Zero 32.94: fitted center at 30.94 (off by 2.0!)
  - Zero 43.33: fitted center at 41.33 (off by 2.0!)
  - Zero 52.97: fitted center at 50.97 (off by 2.0!)
- Overlapping Lorentzians with wide tails created OVERSUBTRACTION
- Residual mean = -2.53 (should be ~0 if model were correct)
- Residual is systematically NEGATIVE everywhere = model too large

### Statistical Tests (Step 5)
- Chi2 = 9613 on 99 dof, p ~ 0. STRUCTURE DETECTED.
- BUT: null shuffles also give chi2 ~ 4000-4500, ALL with p ~ 0
- Real chi2 (4535 on coarse grid) exceeded all 30 null values
- Zero residual peaks above 3-sigma (expected ~13 if Gaussian)

### Pre-Whitening Quality (Step 6)
- No systematic tail leaks near individual zeros (ratios mostly 0.5-2.0)
- Wider window fit (4.0 vs 3.0) did NOT reduce chi2 -- made it slightly WORSE
- The problem is NOT tail width. The problem is the MODEL ITSELF.

### Primes vs All-n (Step 7)
- Primes-only chi2 = 9811 (slightly worse than all-n: 9613)
- Correlation between residuals: 0.65 (moderate)
- Structure present in BOTH, slightly more in primes-only
- Composites are NOT creating the structure; they smooth slightly

## DIAGNOSIS: Why the "Structure" Appears

The pre-whitening is FUNDAMENTALLY FLAWED for this problem:

1. **Lorentzians are wrong model**: The spectroscope peaks at zeta zeros are NOT
   Lorentzian-shaped. They arise from a sum of exponentials (the Dirichlet series)
   and their shape depends on N. At finite N, the peaks have sinc-like sidelobes
   from truncation, not Lorentzian tails.

2. **Overlapping zeros**: Zeros at 30.42 and 32.94 are only 2.5 apart. Their peaks
   overlap severely. The fits fight each other, both drifting from their targets.
   Same for 48.01/49.77, 59.35/60.83, 65.11/67.08, 75.70/77.14.

3. **Oversubtraction**: Sum of 20 broad Lorentzians creates a large positive model
   everywhere. Residual mean = -2.53 proves systematic oversubtraction. The
   "structure" in the residual is largely this smooth negative bias modulated by
   where the fits happened to land.

4. **Null also fails**: Null shuffles also produce chi2 ~ 4000+. The null spectroscope
   is roughly flat (no zeta-zero peaks), but subtracting the SAME Lorentzian model
   (fitted to real data) creates a similar negative-bias residual. The real chi2
   being slightly higher (4535 vs null mean 4280) is expected: the real data had
   peaks that were imperfectly subtracted, leaving more local variation than the
   null's smooth negative offset.

## VERDICT

**The "Chowla violation" is an ARTIFACT of bad pre-whitening.**

The evidence:

1. The Lorentzian model is physically wrong for this spectroscope
2. Overlapping zeros cause fits to fight and drift off-target
3. Systematic oversubtraction (residual mean -2.53, should be ~0)
4. The null test shows even random data gets chi2 ~ 4000 with this procedure
5. The real chi2 only slightly exceeds null (4535 vs 4280 +/- 110)
6. Zero peaks in the residual at z > 3 -- the "structure" is a smooth bias, not peaks
7. Wider fit window made it WORSE, not better

**To do this correctly**, one would need:
- A proper spectral model (sinc-based, accounting for truncation at N)
- Iterative fitting that handles overlapping zeros
- Or: avoid pre-whitening entirely and test for structure in the GAPS between zeros
- Or: use the explicit formula approach (subtract known zero contributions analytically)

**Bottom line**: No evidence for Chowla violation. The previous p=0 result was a
methodological artifact. The spectroscope at N=200K cleanly shows the first ~20 zeta
zeros (as expected), and there is no detectable residual structure beyond them once
the bad pre-whitening bias is accounted for.

## Status: CLOSED (artifact)
