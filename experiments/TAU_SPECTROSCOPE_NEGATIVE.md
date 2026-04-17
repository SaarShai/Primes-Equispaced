# Ramanujan Tau Spectroscope: NEGATIVE
# Date: 2026-04-12

## Raw Σ τ(n)/n^6 spectroscope does NOT detect Δ(s) zeros.
- All z-scores at known Δ zeros: -0.55
- Peaks at γ≈47, 39 (spurious edge artifacts)
- Also does NOT detect ζ zeros (correct — τ is for Δ, not ζ)

## Why: same failure mode as Gauss circle, Goldbach, partitions
The spectroscope works ONLY with cumulative arithmetic sums at insertion points.
Raw f(n)/n over all n doesn't isolate oscillatory zero contributions.

## What might work:
- Cumulative: S_τ(x) = Σ_{n≤x} τ(n)/n^{11/2} evaluated at PRIMES
- Hecke eigenvalues: a_p = τ(p)/p^{11/2} as weights (primes only)
- Mertens-style: M_Δ(p) = Σ_{k≤p} τ(k)/k^{11/2} then spectroscope on M_Δ(p)/p

## Lesson reinforced:
The per-step / cumulative-at-primes structure is NOT optional.
Raw arithmetic function spectroscopy fails universally.
