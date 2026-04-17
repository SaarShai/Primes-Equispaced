# Verified Constants — Ground Truth Reference
# Last updated: 2026-04-13
# Source: mpmath 50-digit computation on local machine

## Zeta zeros and derivatives
rho_1 = 0.5 + 14.134725141734693i
zeta'(rho_1) = 0.7832965118670309 + 0.1246998297481711i
|zeta'(rho_1)| = 0.793160433356506

rho_2 = 0.5 + 21.022039638771556i
|zeta'(rho_2)| = 1.136839106827975

## Phase
phi_1 = -arg(rho_1 * zeta'(rho_1)) = -1.6933 rad (verified to 0.003 rad)

## Constants
e^{gamma_E} = 1.781072417990198
e^{-gamma_E} = 0.561459483566885

## Lean count: 434 (as of Session 12)

## Interval certificates: 800 (K=10,20,50,100 × 200 zeros)

## K≤4 bound: |1/√2 - 1/√3| = 0.1297 ≈ 0.130

## GUE RMSE: 0.066

## Avoidance ratio: 4.4x–16.1x

## Sign correlation: r = 0.77 (sign of ΔW(p) with cos(γ₁ log p + φ₁))
## Sign bias: P(ΔW(p)<0) ≈ 61% (p≤200), grows to ~73% (large p)

## Chowla ε_min = 1.824/√N

## DRH duality identity (CORRECT):
## P_K = c_K(ρ) · Π_{p≤K}(1-p^{-ρ})^{-1} → -e^{-γ_E}
## (c_K times INVERSE Euler product, NOT times Euler product)

## FABRICATED VALUES TO PURGE:
## |zeta'(rho_1)| = 6.77 (M1_DRH_EULER_NUMERICAL.md — qwen fabrication)
## zeta'(rho_1) = 0.548 + 0.103i (M1_PAPER_C_FULL_DRAFT.md — model fabrication)
## phi_1 = -1.335 (M1_PAPER_C_FULL_DRAFT.md — wrong)

## Paper B phase table issue
main_revised.tex shows arg(c_1) = -1.602 — WRONG.
Correct: phi_1 = arg(1/(rho_1 * zeta'(rho_1))) = -1.693311 rad
Fix Paper B when M1_DELTAW_EXPLICIT_FORMULA_CLEAN returns verified phases k=1..5.

## Paper A (math_paper/main.tex) — fixes applied 2026-04-13
- Title: "Per-Step Spectroscopy of Farey Sequences: Primes, Mertens Function, and L-Function Zeros"
- Author: Saar Shai only (Claude removed, in acknowledgments)
- Lean: 434 results, 2 genuine sorrys
- Abstract: per-step methodology framing with C1-C2-C3
- Meta-theorem section: §1.4 added with three negative results

## R₂ POSITIVITY — DISPROVED (2026-04-13)
## R₂(197) = -2.831e-06 < 0 (locally verified, exact Farey arithmetic)
## R₂(199) = -1.384e-05 < 0
## Claim "R₂ > 0 for all primes p ≥ 5" is FALSE (small-prime artifact for p≤79)
## See R2_COUNTEREXAMPLE_DISPROOF.md
## A (dilution term in four-term decomp) IS always > 0 (trivial: 1/n² - 1/n'² > 0)
## R₂ ≠ A — do not conflate

## Aristotle Task — Q-linear independence of log primes
Task ID: 2cc4cfaa-495a-4a00-a958-dc07e5604aef
Submitted: 2026-04-13
File: ~/Desktop/Farey-Local/RequestProject_aristotle/LogPrimeQLinear.lean
Theorem: log_prime_Q_linear_indep (and LinearIndependent ℚ variant)
Status: QUEUED (estimated 1-4 hours)
Retrieve:
~/.local/bin/aristotle result 2cc4cfaa-495a-4a00-a958-dc07e5604aef \
  --destination ~/Desktop/Farey-Local/aristotle_results/2cc4cfaa-495a-4a00-a958-dc07e5604aef \
  --api-key $ARISTOTLE_API_KEY

## GK Concentration (LOCALLY VERIFIED 2026-04-13, paper norm j/n)
p=50:  W=0.00889, top10=76.7%, top20=87.9%, top50=97.8%
p=100: W=0.00497, top10=85.1%, top20=92.3%, top50=98.6%
p=200: W=0.00305, top10=84.0%, top20=90.6%, top50=97.9%
qwen's table (top20~53%) was WRONG — real concentration ~90%

## |S_K| = |Σ_{p≤K} p^{-ρ₁}| (LOCALLY VERIFIED)
K~10 (p=11): |S_K|=2.0605, ratioA=0.989, ratioB=2.471
K~50 (p=53): |S_K|=2.4618, ratioA=0.689, ratioB=1.805
K~100 (p=101): |S_K|=2.5196, ratioA=0.541, ratioB=1.650
K~500 (p=503): |S_K|=2.8747, ratioA=0.320, ratioB=1.574
K~1000 (p=1009): |S_K|=3.1150, ratioA=0.259, ratioB=1.612
Scenario A (√K/logK) ruled out (ratio falls). Growth slower. Need K=10^4+ to decide.
qwen's table (|S_K|=1.42,3.89...) was FABRICATED.

## Bridge identity ΔW(p) = (p-1)/2 · M(p): FABRICATED by deepseek
Verified false at every prime p=5..31. Ratio dW/M varies, not constant.

## NON-TRIVIAL CHI DUALITY PRODUCT (computed 2026-04-13, local mpmath K=5000)
Character: chi_{-4}. First zero: rho_chi4 = 0.5 + 6.020948980i

L'(rho_chi4, chi_{-4}) = 1.202364 + 0.608073i,  |L'| = 1.347380
1/|L'| = 0.742181
e^{-gamma_E} = 0.561459

Duality product D_K = c_K^chi × Euler_chi where:
  c_K^chi = Σ_{n≤K} mu(n)*chi4(n)/n^{rho_chi4}  [grows like log K]
  Euler_chi = Π_{p≤K}(1-chi4(p)/p^{rho_chi4})^{-1}  [shrinks → 0, Aoki-Koyama]

| K    | |Euler_chi| | logK*|Euler| | |c_K^chi| | |D_K|   | arg(D_K)/pi |
|------|------------|--------------|------------|---------|-------------|
| 10   | 0.34892    | 0.80342      | 2.2270     | 0.77704 | -0.0096     |
| 50   | 0.18257    | 0.71422      | 3.4279     | 0.62584 | -0.0043     |
| 100  | 0.14353    | 0.66096      | 4.0703     | 0.58420 | +0.0204     |
| 500  | 0.10535    | 0.65472      | 5.5333     | 0.58294 | +0.0025     |
| 1000 | 0.11408    | 0.78802      | 5.5541     | 0.63361 | -0.0075     |
| 2000 | 0.09497    | 0.72188      | 6.3733     | 0.60529 | +0.0007     |
| 5000 | 0.08907    | 0.75865      | 6.9373     | 0.61792 | -0.0039     |

KEY RESULTS:
1. Aoki-Koyama (log K)^{-1} rate CONFIRMED: (log K)*|Euler_chi| oscillates around ~0.72 (converging)
2. D_K → real, positive: phase ≈ 0 for all K (versus ζ case: P_K → negative, phase=π)
3. |D_K| → ~0.60 ± 0.03: target plausibly e^{-gamma_E} = 0.5615 (7% off at K=5000, slow convergence)

SIGN DUALITY (NEW RESULT 2026-04-13):
- ζ(s) at zeros:    c_K(ρ) × Euler(ρ)^{-1} → -e^{-γ_E}  (NEGATIVE, phase=π)
- L(s,χ) at zeros: c_K^χ(ρ_χ) × Euler_χ(ρ_χ) → +e^{-γ_E} (POSITIVE, phase≈0)
The Euler constant appears with OPPOSITE SIGNS at the two DRH types.
Needs K>10^4 for definitive constant identification.

## DUALITY PRODUCTS — ALL THREE CASES, K=50..10000 (2026-04-13)

### CASE 1: zeta zeros, P_K = c_K × Euler_zeta^{-1}
Euler_zeta^{-1} = Π_{p≤K}(1-p^{-ρ})^{-1}  [diverges — Akatsuka]
c_K = Σ_{n≤K} μ(n)n^{-ρ}  [grows ~ log K / ζ'(ρ)]
Status: |P_K| oscillates 0.28–0.99 at K=50..10000. Phase near 0 (not yet π as theory predicts).
NEEDS K > 10^5 for clean convergence. ζ case converges MUCH slower than χ case.

### CASE 2: chi_{-4} zeros, D_K = c_K^chi × Euler_chi^{-1}
Euler_chi^{-1} = Π_{p≤K}(1-χ(p)/p^{ρ_χ})^{-1}  [converges → 0 — Aoki-Koyama confirmed]
c_K^chi = Σ_{n≤K} μ(n)χ(n)n^{-ρ_χ}  [grows ~ log K / L'(ρ_χ,χ)]

| K     | |Euler_chi| | logK*|Euler| | |c_K^chi| | |D_K|   | arg/pi  |
|-------|------------|--------------|-----------|---------|---------|
| 50    | 0.18257    | 0.71422      | 3.4279    | 0.62584 | -0.0043 |
| 100   | 0.14353    | 0.66096      | 4.0703    | 0.58420 | +0.0204 |
| 500   | 0.10535    | 0.65472      | 5.5333    | 0.58294 | +0.0025 |
| 1000  | 0.11408    | 0.78802      | 5.5541    | 0.63361 | -0.0075 |
| 2000  | 0.09497    | 0.72188      | 6.3733    | 0.60529 | +0.0007 |
| 5000  | 0.08907    | 0.75865      | 6.9373    | 0.61792 | -0.0039 |
| 10000 | 0.07817    | 0.71994      | 7.6509    | 0.59804 | +0.0073 |

mean |D_K| = 0.6068 ± 0.020. Phase ≈ 0 (positive real). CONVERGED at K=1000+.

### CASE 3: chi_3 zeros, D_K = c_K^chi3 × Euler_chi3^{-1}
| K     | |Euler_chi3| | logK*|Euler| | |c_K^chi3| | |D_K|   | arg/pi  |
|-------|-------------|--------------|------------|---------|---------|
| 50    | 0.16612     | 0.64986      | 3.8097     | 0.63287 | +0.0028 |
| 100   | 0.13362     | 0.61536      | 4.5467     | 0.60754 | -0.0057 |
| 500   | 0.10395     | 0.64604      | 5.8489     | 0.60802 | +0.0066 |
| 1000  | 0.09196     | 0.63523      | 6.6324     | 0.60991 | -0.0131 |
| 2000  | 0.08728     | 0.66343      | 7.0048     | 0.61140 | +0.0086 |
| 5000  | 0.07744     | 0.65960      | 8.0061     | 0.62001 | -0.0028 |
| 10000 | 0.07301     | 0.67241      | 8.3623     | 0.61049 | +0.0133 |

mean |D_K| = 0.6143 ± 0.007. Phase ≈ 0 (positive real). CONVERGED at K=100+.

### SYNTHESIS — KEY RESULTS
1. Aoki-Koyama (log K)^{-1} rate CONFIRMED for both χ_{-4} and χ_3:
   (log K) × |Euler_chi| → ~0.68 (oscillating around 0.65-0.79)
   
2. UNIVERSAL DUALITY PRODUCT:
   c_K^chi × Euler_chi^{-1} → ~0.61 (real, positive) for BOTH characters
   chi_{-4} mean: 0.6068. chi_3 mean: 0.6143. Combined: 0.6106.
   
3. CANDIDATE UNIVERSAL CONSTANT: 6/π² = 1/ζ(2) = 0.607927
   Fits chi_{-4} within 0.2%. chi_3 within 1.1%. BEST candidate so far.
   
4. SIGN DUALITY (CONJECTURE):
   ζ at zeros:    P_K = c_K × Euler_ζ^{-1} → -e^{-γ_E} ≈ -0.561 (NEGATIVE, phase→π)
   L(s,χ) at zeros: D_K = c_K^χ × Euler_χ^{-1} → +1/ζ(2)? ≈ +0.608 (POSITIVE, phase≈0)
   
5. CONVERGENCE RATES:
   Non-trivial χ: D_K converges by K=500-1000. Clean, stable.
   Trivial ζ:     P_K still oscillating at K=10000. Needs K > 10^5.
   REASON: Euler_χ^{-1}→0 (conditional convergence). Euler_ζ^{-1} diverges (no convergence on Re=1/2).

STATUS: Conjecture formulated. Needs K>10^5 to confirm constant = 1/ζ(2) vs e^{-γ_E} vs other.
