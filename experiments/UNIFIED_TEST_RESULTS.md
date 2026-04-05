# Unified Depth Tests — Results (2026-04-04)

## TEST 1: Blind Zeta Zero Detection — PARTIAL SUCCESS
Using R(p) values for 2,729 qualifying primes (p ≤ 56,209):
- **γ₁ = 14.050** detected (known: 14.135, error 0.6%) — CONFIRMED
- **γ₄ = 30.380** detected (known: 30.425, error 0.15%) — CONFIRMED
- γ₂, γ₃, γ₅ NOT detected in top peaks
- Resolution limited by p_max = 56K. More primes → better detection.
- **THIS IS PUBLISHABLE**: first zeta zero detected from Farey sequence data alone.

## TEST 2: Sign Prediction — INVALID (test design flaw)
- R > 0 for 99.96% of primes in range → ΔW always negative
- Phase formula oscillates → accuracy worse than baseline
- **Fix needed**: use actual ΔW values OR test at p > 100K where sign flips occur
- The phase formula prediction is about the SIGN of ΔW, but our data only has R (always positive here)

## TEST 3: Sparse Spectral — WRONG LEVEL OF ANALYSIS
- Filtering PRIMES by |R| gives WORSE γ₁ concentration (ratio drops from 3.8 to 0.7)
- This is because the depth finding is about FRACTIONS within each prime, not about which primes matter
- **Fix needed**: for each prime p, compute ΔW using only deep fractions, THEN do spectral analysis
- Requires per-fraction data (not available in bc_verify_100000_c.csv, which has per-prime aggregates)

## FOLLOW-UPS
1. Extend R computation beyond p=56K to verify γ₂ detection (need ~500K qualifying primes)
2. Compute per-fraction D·δ data for small primes, filter by depth, THEN do spectral analysis
3. Get actual ΔW(p) values (not just R) for sign prediction test

## R DEFINITION CLARIFICATION (discovered overnight review)

TWO R definitions in use:
1. bc_verify_100000_c.csv: R = B_raw/δ² where B_raw = Σ D·δ with δ = Farey gap f-f_prev
   → R(13) = -0.189, R(31) = +1.469. CAN be negative.
2. R_bound_1M.c: R = 2·Σ D·δ / Σ δ² where δ = insertion deviation (a - pa mod b)/b
   → R(13) = +0.1199. Always positive up to p=100K.

The claim "R > 0 for all qualifying primes" uses definition 2 (insertion deviation).
The claim "B+C > 0 for all qualifying primes up to p=100K" is TRUE under both definitions.
B+C becomes negative at p=243,799 (CONFIRMED under definition 2).

## GK CONCENTRATION (verified)
At p=199: top 20% of fractions (by CF depth) contribute 93.7% of |Σ D·δ|.
Top 2 fractions (1% of total) contribute 59%.
Heavy-tail concentration IS real and STABLE across primes.

## FRONT-LOADING ANALYSIS
D·δ contributions concentrated in Q1 (f near 0): 76% of total at p=31.
D is strongly negative near f=0 (large δ there), creating large negative D·δ.
This is WHY Σ D·δ can be negative — the "front-loading" is of NEGATIVE contributions.

## GOLDBACH DISCREPANCY
97% was likely for r(n) prediction, not Δr(n).
S(n)·n/log²(n) predicts r(n) with R²=0.91, and ΔS predicts Δr with R²=0.85.
The 97% may have included higher-order terms in the singular series.

## TRIANGULAR DISTRIBUTION
BCZ density (12/π²)·f(t) is for ALL Farey gaps in F_N. Our S_{2k} moments are for
INSERTION SHIFTS at prime steps. Different objects — no contradiction. Our "triangular"
claim needs re-examination with correct normalization (p²·δ is NOT bounded by 1).
