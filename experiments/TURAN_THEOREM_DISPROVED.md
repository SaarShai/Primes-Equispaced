# CRITICAL: Theorem A2 (Turán Non-Vanishing) is UNPROVED
# Date: 2026-04-10 ~00:30
# Source: Opus adversarial reviewer O1, confirmed by literature check

## THE FINDING

The "Turán theorem" as quoted in TURAN_BAKER_PROOF.md (lines 84-92) — claiming that a non-zero
Dirichlet polynomial has only FINITELY MANY zeros in a strip — **does not exist**.

The actual classical results say the OPPOSITE:

- **Langer (1931)**: An exponential polynomial Σ a_k e^{λ_k s} with ≥2 terms has
  INFINITELY many zeros, with count N(T) ~ (λ_max - λ_min)T/π up to height T.
  [Bull AMS 37(4):213-239]

- **Moreno (1973)**: When exponents are Q-linearly independent, zeros are DENSE in
  each critical strip — there are zeros arbitrarily close to any vertical line.
  [Compositio Math 26(1):69-78]

For c₁₀(s) = -2^{-s} - 3^{-s} - 5^{-s} + 6^{-s} - 7^{-s} + 10^{-s}:
- Exponents: log 2, log 3, log 5, log 6, log 7, log 10
- Zero count: ~ (log 10 - log 2)T/π ≈ 0.51T up to height T
- **c₁₀ has ~51 zeros up to height 100, ~510 up to height 1000**

## WHAT THIS MEANS

1. **Theorem A2 is UNPROVED** — the "all but finitely many" claim has no valid proof
2. **The first adversarial reviewer was WRONG** to validate it
3. **Turán's actual theorem** gives LOWER BOUNDS for the maximum of power sums — 
   NOT finiteness of zeros. Montgomery (1994) Lecture 8 discusses this correctly.
4. **The claim might still be TRUE** — c_K has infinitely many zeros, ζ has infinitely
   many zeros, but they might not coincide. Computational evidence supports non-vanishing
   at zeta zeros (min|c₁₀(ρ)| ≈ 0.024 across 100+ tested zeros).

## WHAT SURVIVES

| Result | Status |
|--------|--------|
| Theorem A2 (unconditional non-vanishing) | **UNPROVED** — proof uses non-existent theorem |
| Theorem A3 (quantitative lower bound) | **UNPROVED** — depends on A2 framework |
| Theorem B (GRH detection, all zeros) | **VALID** — uses explicit formula, not Turán |
| Theorem C (GRH universality) | **VALID** — independent of Turán |
| Theorem D (large sieve noise bound) | **VALID** — unconditional, independent |
| Theorem E (Schmidt-Łojasiewicz) | **UNPROVED** — the proof sketch has multiple gaps |
| Computational: c_K(ρ) ≠ 0 for tested zeros | **VALID** — empirical observation |
| Computational: |c_K(ρ)| grows with K | **VALID** — consistent with 1/ζ pole (under RH) |
| Batch L-function speedup | **VALID** — algorithmic, not dependent on Turán |
| Amplitude matching R²=0.949 | **VALID** — numerical verification |

## PATHS FORWARD (from O1)

(a) **Prove c_K zeros avoid zeta zeros**: Show the infinitely many zeros of c_K(s) in the
    critical strip are "generically distributed" and don't cluster at zeta zero ordinates.
    Uses: random-like distribution of ζ zeros + algebraic structure of c_K zeros.

(b) **Work directly with full spectroscope F(γ)**: Instead of approximating by c_K, prove
    detection for F(γ) = Σ_k μ(k)·T(k,γ). Requires handling non-Dirichlet-polynomial weights.

(c) **Accept GRH-conditional**: The detection theorem is proved under GRH via explicit formula
    (OPUS_CLEAN_PROOF_FINAL.md). State honestly and drop unconditional claim.

(d) **Numerical certificate**: For specific K and T, verify computationally that c_K has no
    zeros within ε of any zeta zero γ_j with j ≤ J. This gives a verified unconditional
    result for those specific zeros (not a general theorem).

## IMPACT ON PAPER C

The paper outline (OPUS_PAPER_C_OUTLINE.md) must be revised:
- Section 3 (Turán) should present the non-vanishing as a **conjecture** supported by
  computational evidence, not as a proved theorem
- OR Section 3 should present the Langer zero count as context, with the observation that
  c_K zeros and zeta zeros appear disjoint (computationally)
- The GRH-conditional results (Sections 4-5) become the strongest proved theorems
- The batch computation results and numerical verification remain fully valid

## LESSON

This is EXACTLY why adversarial verification exists. The first reviewer VALIDATED the
claim (incorrectly). The second reviewer with deeper literature knowledge BROKE it.
The rule: **never trust a single verification pass on a novel theorem**.

## REFERENCES

- Langer, R.E. (1931). On the zeros of exponential sums and integrals. Bull AMS 37(4):213-239.
- Moreno, C.J. (1973). The zeros of exponential polynomials (I). Compositio Math 26:69-78.
- Roy, D. & Vatwani, A. (2019). Zeros of Dirichlet polynomials. arXiv:1912.03711.
- Asymptotic number of zeros in critical strips (2020). Monatshefte für Mathematik.
