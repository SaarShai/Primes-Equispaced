# Sign Theorem Proof Gap Analysis
Date: 2026-04-13
Source: Codex deep thinking (task a40aaec0255b3fe5a)

## The Theorem
**Sign Theorem**: For every prime 11 ≤ p ≤ 100,000 with M(p) ≤ -3: ΔW(p) < 0.

## Current Proof Strategy
Uses four-term decomposition: ΔW(p) = A - B - C + 1 - D_term - 1/n'²
Claim: C + D_term + 1/n'² > A (so ΔW < 0 even ignoring B ≥ 0)

## Codex Analysis: 5 Questions

### Q1: D_term/A ≥ 0.97 provable analytically?
**Status: OPEN. Not provable from current tools.**
- Equidistribution (Franel-Landau) works for fixed test functions, not p-varying discrepancy field
- Needed: asymptotic for Σ D_{F_p}(k/p)² and Σ D_{F_{p-1}}(f)² with same main term
- Strictly stronger than any standard discrepancy bound
- Would require Garcia 2025 local discrepancy + new second-moment theorem

### Q2: C/A ≥ π²/(432 log²N) provable?
**Status: UNVERIFIED CLAIM IN PAPER. Plausible but no proof.**
- For each denominator b: Σ_{(a,b)=1} δ(a/b) = 0 exactly (permutation preserves residues)
- No first-moment gain from Cauchy-Schwarz
- C is a VARIANCE problem for permutations a → pa mod b
- If b | (p-1), permutation is identity, δ = 0 on entire denominator → C can be very small
- The claim requires uniform control on modular correlation structure across all b ≤ p-1: NEW information

### Q3: Telescoping identity exists?
**Algebraic identity exists but does NOT bypass four-term analysis.**
S_p = Σ_{f∈F_{p-1}} (D_{F_{p-1}}(f) + δ(f))² + Σ_{k=1}^{p-1} D_{F_p}(k/p)²
Subtracting S_{p-1} gives the usual decomposition. No sign-manifest simplification.

### Q4: What lemma closes the Lean sorry?
**Precise lemma:**
> **Lemma (DiscrepancyStep)**: For all primes p ≥ 11 with M(p) ≤ -3:
>   C(p) + D_term(p) + |F_p|⁻² > A(p)

More Lean-friendly form: -ΔW(p) ≥ c/p² for explicit c > 0.

Lean footprint needs: formal F_n, D_{F_n}, M(n), exact algebraic decomposition.
No Mathlib theorem covers Farey-discrepancy or Mertens-function inequalities.

### Q5: RH-conditional proof?
**Status: RH insufficient by itself.**
- RH gives W(N) = O(log⁴N / N) → 0. But this is an UPPER BOUND.
- Need C + D_term > A: comparison of two positive quantities. RH gives sizes, not ratios.
- RH doesn't imply M(p) ≤ -3 occurs infinitely often on primes (sign-pattern is separate)

## What IS Proved
- Explicit discrepancy recursions via Möbius/Mertens sums
- Franel-Landau equivalences (RH ↔ Farey equidistribution)
- Unconditional order bounds for local discrepancy
- RH-conditional size bounds on W(N)
- Sign Theorem COMPUTATIONALLY for p ≤ 100,000

## What Needs New Ideas
- Sharp second-moment asymptotic for step F_{p-1} → F_p
- OR uniform theorem controlling modular permutation variance Σ δ(f)² across denominators:
  Σ_{b≤p-1} Σ_{(a,b)=1} ((pa mod b) - a)² / b² vs Σ D_{F_{p-1}}(f)²

## Impact on Paper A
1. Sign Theorem STAYS as Theorem — computationally verified for p ≤ 100,000
2. The "proof" section must be rewritten: current proof has UNVERIFIED CLAIM C/A ≥ π²/(432 log²N)
3. Correct status: computational verification + open proof with precisely stated gap (DiscrepancyStep lemma)
4. Lean sorry: remains until DiscrepancyStep proved

## References (Codex citations)
- Garcia 2025 (CERN:2923145) — local discrepancy formulas
- Dress 1999 (EUDML:248344) — Farey structure
- Niederreiter 1973 (EUDML:162396) — discrepancy bounds
- Tomas 2022 (CERN:2851291)
- Ledoan 2018 (DOI:10.1007/s10474-018-0868-x)
