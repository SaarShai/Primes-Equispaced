# Session 8 — Honest Final Assessment
## Date: 2026-03-29

## The Sign Theorem: For primes p ≥ 11 with M(p) ≤ -3, ΔW(p) < 0.

### Status: COMPUTATIONALLY PROVED to p = 100,000. ANALYTICAL TAIL REMAINS OPEN.

---

## What IS proved (unconditional, rigorous)

### New Identities
1. **Permutation Square-Sum**: Σ x·δ = C/2 (elementary, independently verified)
2. **Deficit formula**: D_q(2) = q(q²-1)/24 (pure algebra)
3. **Deficit minimality**: D_q(r) ≥ D_q(2) (Dedekind reciprocity + permutation inequality)
4. **Spectral positivity**: K̂_p(χ) = (p/π²)|L(1,χ)|² for odd χ (Codex, proved)
5. **Farey symmetry**: Σ D = -n/2, E(k) = -E(p-k)
6. **Σ D_new = -(p-1)/2** exactly (non-circular first moment)

### Bounds
7. **C_W ≥ 1/4** (Cauchy-Schwarz from Σ D = -n/2)
8. **C_W ≥ N/28** (large-b fractions, elementary)
9. **Σ E(k)² ≥ p²/28** (endpoints + antisymmetry)
10. **Σ D² ≥ N³/12200** (from C_W bound)
11. **Odd energy ≥ (3/4)(p-1)²** (elementary Möbius identity)

### Computational
12. **ΔW < 0** for all 4,617 M(p) ≤ -3 primes to p = 100,000
13. **B+C > 0** for all 210 M(p) ≤ -3 primes to p ≈ 3,000 (R always positive)
14. **B+C < 0** at p = 1399 (M = +8) — Sign Theorem fails for positive-M primes

### Lean Formalization
15. **PermutationIdentity.lean**: 8 lemmas proved (5 direct + 3 Aristotle), 3 sorry (Finset plumbing)
16. **Four-term decomposition** verified in Lean

---

## What is NOT proved (the remaining gap)

### The logp Factor
The bypass condition C' + D' > A' + 1 requires D' ≈ A' (both ~ p²·logp).
Our proved bound Σ E² ≥ p²/28 gives D' ≥ p²/28, but A' ~ 0.065·p²·logp.
For large p: D' < A', and the bypass fails.

The logp factor in the empirical Σ E² ~ 0.06·p²·logp comes from the
**correlation between L-function eigenvalues and Mertens character sums**
in the spectral formula:

  Σ E² = (p/(π²(p-1))) Σ_{χ odd} |L(1,χ)|² · |Λ_p(χ)|²

This correlation is a genuine number-theoretic phenomenon. Proving it
requires understanding why characters that "detect" Mertens structure
also have large L-function values — an open problem.

### Wrong Heuristics Corrected
- Σ M(t)² ~ (6/π²)t was WRONG (confused μ² with M²). Actual: Σ M(t)² ~ 0.016·t²
- Σ D² ~ n²·logN was WRONG. Actual: Σ D² ~ N³·(const + 0.24·log(logN))
- C_W grows as ~log(logN), NOT logN

---

## What the paper CAN claim

1. **Theorem** (computational): ΔW(p) < 0 for all primes 11 ≤ p ≤ 100,000 with M(p) ≤ -3.
2. **Theorem** (Lean-verified small primes): ΔW(p) < 0 for primes 11 ≤ p ≤ 113.
3. **Theorem** (conditional on RH): ΔW(p) < 0 for all sufficiently large p with M(p) ≤ -3.
4. **Theorem** (new): Permutation Square-Sum Identity.
5. **Theorem** (new): Deficit minimality D_q(2) = q(q²-1)/24.
6. **Theorem** (new, Codex): Spectral positivity K̂_p(χ) = (p/π²)|L(1,χ)|².
7. **Conjecture**: The spectral correlation gives Σ E² ≥ c·p²·logp, which would close the unconditional proof.

---

## Session Achievements (genuine progress)

| # | Discovery | Status | Novel? |
|---|-----------|--------|--------|
| 1 | Permutation identity Σxδ = C/2 | Proved + verified | Yes |
| 2 | B+C = -2ΣRδ reformulation | Proved | Yes |
| 3 | Deficit-Dedekind connection | Proved | Likely new |
| 4 | D_q(2) = q(q²-1)/24 formula | Proved | Elementary |
| 5 | D_q(2) minimality | Proved | Via Dedekind reciprocity |
| 6 | K̂_p(χ) = (p/π²)|L(1,χ)|² | Proved (Codex) | Structural |
| 7 | C_W ≥ 1/4 (Cauchy-Schwarz) | Proved | Elementary |
| 8 | C_W ≥ N/28 (large-b) | Proved | Elementary |
| 9 | Σ E² ≥ p²/28 | Proved | Elementary |
| 10 | B+C < 0 at p=1399 | Discovered | Important correction |
| 11 | Σ D_new = -(p-1)/2 | Proved | Clean identity |
| 12 | Odd energy ≥ (3/4)(p-1)² | Proved | From Möbius identity |
| 13 | El Marraki effective Mertens | Found in literature | Key reference |
| 14 | Σ M(t)² confusion corrected | Corrected | Prevented false claim |
| 15 | Spectral correlation = logp source | Identified | Key insight for future |

---

## Recommended Next Steps

1. **For the paper**: Add the new theorems (permutation identity, spectral positivity, deficit minimality). Frame the unconditional analytical tail as an open conjecture with the spectral correlation as the key target.

2. **For the proof**: Attack the spectral correlation. The exact formula Σ E² = (p/(π²(p-1))) Σ |L(1,χ)|²|Λ_p(χ)|² with K̂ ≥ 0 is the right framework. The open step is proving that the weighted sum grows as p²·logp, not just p².

3. **For computation**: Extend verification to p = 10⁶ or 10⁷ (trivial with C code, hours of runtime) to strengthen the computational base.
