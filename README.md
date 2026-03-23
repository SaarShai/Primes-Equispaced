# Primes-Equispaced: Per-Step Farey Discrepancy and the Mertens Function

**New identities connecting the geometry of Farey sequences to multiplicative number theory.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What We Discovered

The Farey sequence $F_N$ — all fractions $a/b$ with $0 \leq a/b \leq 1$, $b \leq N$, $\gcd(a,b)=1$ — has been studied for two centuries. We asked a question that, to our knowledge, had not been systematically investigated: **what happens to its uniformity when we add one more integer?**

The answer reveals a striking asymmetry:

- **Composites** improve uniformity ~96% of the time (in computations up to $N = 200{,}000$)
- **Primes** contribute ~99% of all uniformity *degradation*
- The sign of the wobble change $\Delta W(p)$ at each prime is governed by the **Mertens function** $M(p) = \sum_{k \leq p} \mu(k)$

This creates a direct bridge between the geometry of Farey fractions and the arithmetic of the Möbius function — two areas with no previously known connection at this level of granularity.

## Eight Exact Identities

| # | Identity | Formula | What it says |
|---|----------|---------|-------------|
| 1 | **Bridge** | $\sum_{f \in F_{p-1}} e^{2\pi i p f} = M(p) + 2$ | Farey exponential sum = Mertens function |
| 2 | **Generalized Bridge** | $\sum_{f \in F_N} e^{2\pi i m f} = M(N) + 1$ (prime $m > N$) | ALL primes above $N$ give the same sum |
| 3 | **Universal Formula** | $\sum_{f \in F_N} e^{2\pi i m f} = M(N) + 1 + \sum_{d \mid m, d \geq 2} d \cdot M(\lfloor N/d \rfloor)$ | Complete evaluation at EVERY frequency |
| 4 | **Master Involution** | $\sum D(f) \cdot g(f) = -\frac{1}{2}\sum g(f)$ for symmetric $g$ | General tool for Farey weighted sums |
| 5 | **Displacement-Cosine** | $\sum D(f) \cdot \cos(2\pi p f) = -1 - M(p)/2$ | Fourier coefficient of rank discrepancy |
| 6 | **Fractional Parts** | $\sum \{pf\} = (n-2)/2$ | From coprime residue permutation |
| 7 | **δ-Symmetric** | $\sum \delta(f) \cdot g(f) = g(1)$ for symmetric $g$ | Shift function identity |
| 8 | **Cross-Term** | $\sum D(f) \cdot \delta(f)^2 = -\frac{1}{2}\sum \delta^2 - \frac{1}{2}$ | Boundary correction formula |

The bridge identity (Theorem 1) uses a classical Ramanujan-sum decomposition; the m=1 case is implicit in Edwards (1974). The per-frequency generalization (Theorems 2–3) and the per-step application to $\Delta W$ (Theorems 4–8) appear to be new.

## Key Empirical Findings

| Finding | Data |
|---------|------|
| Primes tested (p ≥ 11) | 9,588 up to $p = 100{,}000$ |
| $\Delta W > 0$ (uniformity improved) | 2,295 (23.9%) |
| $M(p) < 0$ with $\Delta W > 0$ (counterexamples) | **1** (at $p = 92{,}173$, numerically observed) |
| $M \leq -3$ class counterexamples | **0** among 4,617 primes |
| Sigmoid transition | 0% violations for $M/\sqrt{p} < -0.1$; 100% for $M/\sqrt{p} \geq 0.3$ |

The counterexample at $p = 92{,}173$ has $\Delta W \approx 3.56 \times 10^{-11}$, confirmed by three floating-point methods but not yet certified by exact rational arithmetic.

## Formal Verification (Lean 4)

**44 results, zero `sorry`** across three core files, verified by the [Aristotle](https://aristotle.harmonic.fun) automated theorem prover:

| File | Results | sorry | Contents |
|------|---------|-------|----------|
| `PrimeCircle.lean` | 13 | 0 | Farey cardinality, Ramanujan sums, wobble decomposition |
| `BridgeIdentity.lean` | 26 | 0 | Bridge identity, coprime permutation, Möbius properties |
| `DeltaCosine.lean` | 5 | 0 | δ-cosine framework |
| `MertensGrowth.lean` | 5 | 1 | Growth witnesses (proved); general $\|M(N)\| = \Omega(\sqrt{N})$ (stated) |

The bridge identity proof chain — coprime residue permutation → Ramanujan sum at coprime argument → bridge identity — was constructed **autonomously** by Aristotle.

## Repository Structure

```
paper/                  LaTeX source and PDF (18 pages, 10 figures)
RequestProject/
  PrimeCircle.lean      Core Lean 4 proofs
  BridgeIdentity.lean   Bridge identity chain (zero sorry)
  DeltaCosine.lean      δ-cosine framework
  MertensGrowth.lean    Mertens growth witnesses
experiments/
  wobble_primes_only.c  Fast C implementation
  wobble_primes_*.csv   Computational data (up to 200K)
  visualizations.py     Figure generation
figures/                10 publication-quality visualizations
```

## How to Reproduce

```bash
# Lean 4 proofs (requires Lean 4.28.0 + Mathlib)
lake build

# Computational experiments
cd experiments
cc -O3 -o wobble_primes_only wobble_primes_only.c -lm
./wobble_primes_only 100000
python3 visualizations.py
```

## The Paper

**"New Identities Connecting Farey Sequences to the Mertens Function via Per-Step Discrepancy"**

Saar Shai and Anthropic's Claude Opus 4.6

18 pages, 10 figures, 8 theorems, 13 references. Available in `paper/main.pdf`.

## Citation

```bibtex
@article{shai2026fareymertens,
  title={New Identities Connecting Farey Sequences to the Mertens Function
         via Per-Step Discrepancy},
  author={Shai, Saar and Claude (Anthropic)},
  year={2026},
  url={https://github.com/SaarShai/Primes-Equispaced}
}
```

## Acknowledgments

- [Aristotle](https://aristotle.harmonic.fun) (Harmonic) — automated theorem proving for Lean 4
- Research conducted with [Claude](https://claude.ai) (Anthropic)

## License

Code: MIT License | Paper and proofs: CC-BY 4.0
