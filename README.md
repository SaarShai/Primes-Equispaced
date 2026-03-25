# The Geometric Signature of Primes in Farey Sequences

**Primes and composites play fundamentally different geometric roles in the distribution of fractions.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Summary

We study the per-step uniformity of Farey sequences and discover that composites account for ~96% of uniformity improvement while primes are responsible for ~99% of uniformity damage. The direction of each prime's geometric effect is controlled by the Mertens function M(p).

**Sign Theorem** (Theorem 9.1): For all primes 11 ≤ p ≤ 100,000 with M(p) ≤ -3: ΔW(p) < 0. Proved by hybrid computation + analysis, with zero counterexamples among 4,617 primes. Certified counterexample at p = 92,173 (M = -2) by 256-bit MPFR interval arithmetic.

## Formal Verification (Lean 4)

**9 files, 139 results, ZERO sorry.** Bridge identity proof chain constructed autonomously by [Aristotle](https://aristotle.harmonic.fun).

| File | Results | Contents |
|------|---------|----------|
| PrimeCircle.lean | 19 | Farey cardinality, Ramanujan sums, wobble decomposition |
| BridgeIdentity.lean | 34 | Bridge identity, coprime permutation, Möbius properties |
| CharacterBridge.lean | 11 | Character-weighted bridge for all Dirichlet characters |
| InjectionPrinciple.lean | 11 | Each Farey gap gets ≤1 new fraction k/p |
| DisplacementShift.lean | 17 | D_new = D_old + δ displacement-shift identity |
| DenominatorSum.lean | 16 | Σ D(a/b) = -φ(b)/2 per denominator |
| StrictPositivity.lean | 16 | Σ δ² > 0 via rearrangement inequality |
| DeltaCosine.lean | 10 | δ-cosine framework |
| MertensGrowth.lean | 5 | Computational witnesses for |M(N)| > √N/2 |

## The Paper

**"The Geometric Signature of Primes in Farey Sequences"**
Saar Shai and Anthropic's Claude Opus 4.6
23 pages, available in `paper/main.pdf`.

## How to Reproduce

```bash
# Lean 4 proofs (requires Lean 4.28.0 + Mathlib 4.28.0)
lake build

# Computational experiments
cd experiments
cc -O3 -o wobble_primes_only wobble_primes_only.c -lm
./wobble_primes_only 100000
```

## Authors

- **Saar Shai** — Independent Researcher
- **Claude** (Anthropic) — AI research assistant

## License

Code: MIT License | Paper and proofs: CC-BY 4.0
