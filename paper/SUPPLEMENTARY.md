# Supplementary Material
# "The Geometric Signature of Primes in Farey Sequences"

The following material was removed from the main paper for brevity.
It is available here and in the GitHub repository for interested readers.

## 1. Why Primes Are Special (former Section 5)
Classical Farey sequence properties including:
- Injection Principle (Theorem, with proof)
- Generalized Injection Principle
- Universal Mediant Property (cf. Hardy-Wright)
- Fisher Information Monotonicity
- Mediant Minimality (cf. Hardy-Wright)
- Farey Gap Formula (classical)
- Convergence Rate (Corollary)

These are well-known results included for completeness in earlier drafts.
See Hardy & Wright, "An Introduction to the Theory of Numbers."

## 2. Composite Healing Characterization
- Observation: ~90% of composites heal (ΔW > 0) for n ≤ 800
- Rate decreases from 96% (n≤200) to 90% (n≤800)
- φ(n)/n controls healing but no clean threshold exists
- 5 counterexamples to φ/n < 1/3 at n = 438, 546, 570, 654, 678
- All 7 composites with φ/n < 0.25 heal (n ≤ 800)

## 3. Gauss-Kuzmin Concentration
- Top 20% of fractions (by CF depth) contribute 93% of |Σ D·δ|
- Stable across p = 31 to 199
- Reflects infinite-mean property of Gauss-Kuzmin distribution
- Figure: gk_concentration_curve.png

## 4. Applications and Connections
- Farey quadrature errors
- Geometric computation of the Mertens function
- Franel-Landau per-step refinement

## 5. Extended Open Questions (6-10)
- Erdős discrepancy multiplicative case
- Wobble-entropy duality deeper analysis
- Higher-dimensional Farey (S², torus)
- Quantum ergodicity / horocycle connection
- Montgomery pair correlation extension

## 6. Lean 4 File Inventory
258 results across 15 files. Full listing available at:
https://github.com/SaarShai/Primes-Equispaced/tree/main/RequestProject
