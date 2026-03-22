# Proof Status: ΔW(p) > 0 ⟹ M(p) ≥ 0

## The Conjecture
For all primes p ≥ 11: if the per-step Farey wobble change ΔW(p) is positive
(wobble decreased), then the Mertens function M(p) ≥ 0.

## Computational Evidence
- 5,129 primes tested through p = 49,999
- 1,109 violations (ΔW > 0), ALL have M ≥ 0
- 2,986 primes with M < 0, NONE have ΔW > 0
- 3 edge cases at M = 0 with ΔW ≈ 10⁻¹⁰ (numerical precision boundary)
- Conjecture FAILS for composites (97 counterexamples) — prime-specific

## Formally Proved Theorems (Lean 4, via Aristotle)
1. Farey involution: σ(a,b) = (b-a,b) is bijection on F_N
2. D(f) + D(σ(f)) = -1 for all Farey fractions
3. **Master identity**: Σ D·g = -(1/2)·Σ g for ANY symmetric g
4. Bridge identity: Σ cos(2πpf) = M(p) + 2
5. Displacement-cosine: Σ D·cos(2πpf) = -1 - M(p)/2
6. Fractional parts sum: Σ {pf} = (n-2)/2
7. Insertion orthogonality: Σ D(k/p)·cos(2πk/p) = 0
8. {pf} involution: {pf} + {p(1-f)} = 1
9. Wobble decomposition: W = S2 - 2R/n + J(n)
10. New fractions sum: Σ(k/p)² = (p-1)(2p-1)/(6p)
11. L² decomposition: ∫(D+g)² = ∫D² + 2∫Dg + ∫g²
12. δ² identity: Σ D·δ² = -(1/2)·Σ δ² - 1/2
13-24+. Various supporting lemmas (Ramanujan sums, coprime permutation, etc.)

## Exact Identities Discovered (verified computationally)
- Σ D·{pf}² = Σ D·{pf} + n/4 - Σ{pf}²/2 - 1/2
- Σ δ = -1 for primes (from Σ{pf}=(n-2)/2 and Σf=n/2)

## Key Structural Findings
- **Prime-specific**: Primes add EQUISPACED fractions (φ(p)=p-1, all coprime).
  Composites add NON-equispaced fractions, breaking the mechanism.
- **Σ D·{pf} cancels from δ²**: The hard quantity enters ΔW only linearly.
- **M-independent background deeply negative**: ~-0.7n, overwhelms M-dependent part.
- **Ratio test**: max ratio 2Σ D·δ/(-rest) = 0.736 at p=11, improves for larger p.
- **Rademacher bound approach**: Dedekind sum bounds give 0.18 < 0.35 needed.

## THE GAP (what remains for complete proof)
Bound |Σ D·({pf} - 1/2)| (the antisymmetric part of Σ D·{pf}).

### What doesn't work:
- Cauchy-Schwarz: 1.5-2.3x too loose
- Involution principle: blind to antisymmetric functions
- Fourier/sawtooth series: slowly convergent, higher modes grow
- Per-denominator Weil bounds: 4.5x too loose
- Individual tools all too loose by factors of 1.5-5x

### What might work:
- Rademacher bound on Dedekind sums (asymptotic bound 0.18 < 0.35 needed)
- Pólya-Vinogradov inequality (formalized in Isabelle/HOL)
- Large sieve inequality for the SUM (not per-denominator)
- A completely new identity for the antisymmetric part
- The equispacing geometry of prime insertions
- Goedel-Prover-V2 (AI prover, outperforms DeepSeek on PutnamBench)

## Available Tools
- Aristotle (Lean 4 prover): 24+ theorems proved
- SageMath: Dedekind/Kloosterman sum computation
- PARI/GP: fast number theory
- Goedel-Prover-V2: open-source AI prover
- Lean Copilot: LLM-assisted proof search
- Isabelle/HOL: has Farey sequences + Pólya-Vinogradov formalized
