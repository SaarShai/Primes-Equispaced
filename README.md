# Prime Farey Wobble: A New Connection Between Primes and Farey Uniformity

## Overview

This repository contains the code, data, formal proofs, and computational experiments for a research project investigating how individual primes affect the uniformity of Farey sequences.

**Main discovery:** When a prime p is added to the Farey sequence F_{p-1}, the change in the L² discrepancy (which we call the "wobble change" ΔW) is controlled by the Mertens function M(p) = Σ_{k≤p} μ(k).

**Conjecture (computationally verified for 5,129 primes, zero counterexamples):**
> For all primes p ≥ 11: ΔW(p) > 0 implies M(p) ≥ 0

This conjecture connects the **geometry** of fraction distribution on a circle to the **arithmetic** of the Möbius function, with implications for the Riemann Hypothesis through the Franel-Landau theorem.

## Why This Matters

The value of this work is not in any single identity — each one follows from known number theory. The value is in **looking where nobody looked before**: decomposing Farey discrepancy one prime at a time, and discovering that the sign of each prime's geometric contribution is controlled by the Mertens function.

This creates a **bridge between two research communities** that have had limited overlap: researchers studying Farey sequence geometry/discrepancy, and researchers studying the Mertens function and Möbius arithmetic. Our bridge identity (Σ cos(2πpf) = M(p) + 2) says their objects are literally equal — a result about M(p) immediately implies something about Farey geometry, and vice versa. The master involution principle, the per-step wobble decomposition, the violation-Mertens correlation, and the exact formula chain form an interconnected framework where the bridge identity is the keystone that makes the whole arch stand.

## Interactive Demo

Open [`demo/index.html`](demo/index.html) in a browser to see an interactive visualization of the Farey circle. Slide through values of N and watch how primes (100% grid fill) vs composites (partial fill) affect the distribution, and how the Mertens bias (red = top-heavy, teal = bottom-heavy) controls whether primes heal or disrupt uniformity.

## Key Results

### Novel Discoveries
- **Per-step wobble decomposition**: First analysis of how Farey discrepancy changes one integer at a time
- **Prime/composite sign flip**: Primes increase wobble ~85% of the time; composites decrease it ~69%
- **Violation-Mertens correlation**: The sign of ΔW(p) tracks the sign of M(p) with zero counterexamples across 2,986 M<0 primes
- **Prime-specific mechanism**: The conjecture fails for composites (97 counterexamples), confirming it relies on the equispaced insertion geometry unique to primes
- **Burst-quiet pattern**: Violation clusters grow with N and track positive excursions of M(N)/√N

### New Exact Identities
1. **Master involution principle**: For any symmetric function g on the Farey sequence, Σ D(f)·g(f) = -(1/2)·Σ g(f)
2. **Bridge identity**: Σ cos(2πpf) over F_{p-1} = M(p) + 2
3. **Displacement-cosine identity**: Σ D(f)·cos(2πpf) = -1 - M(p)/2
4. **Fractional parts sum**: Σ {pf} over F_{p-1} = (n-2)/2
5. **δ² identity**: Σ D·δ² = -(1/2)·Σ δ² - 1/2
6. **Reversed Dedekind sum**: Σ_{b=2}^{p-1} s(b,p) = -(p-1)(p-2)/(12p)

### Formal Proofs (Lean 4)
24+ theorems formally verified using the [Aristotle](https://aristotle.harmonic.fun) automated theorem prover, including the master involution principle, bridge identity, wobble decomposition, and Ramanujan sum identities.

## Repository Structure

```
├── RequestProject/
│   └── PrimeCircle.lean       # Formal Lean 4 proofs
├── experiments/
│   ├── wobble_primes_only.c    # Fast C implementation for large-N computation
│   ├── wobble_primes_50000.csv # Computational data through N=50,000
│   ├── visualizations.py       # Publication-quality figure generation
│   ├── mertens_farey_analysis.py
│   ├── cross_term_violations.py
│   └── ...                     # Various experimental scripts
├── figures/                    # 9 publication-quality visualizations
├── research_tracker.json       # Comprehensive project tracking
├── PROOF_STATUS.md             # Current status of proof attempts
└── README.md
```

## Computational Evidence

| Range | Primes tested | Violations (ΔW>0) | With M<0 | Counterexamples |
|-------|--------------|-------------------|----------|-----------------|
| p ≤ 50,000 | 5,129 | 1,109 (21.6%) | 0 | **0** |
| M < 0 only | 2,986 | — | 0 violations | **0** |

## How to Reproduce

### Lean 4 Proofs
```bash
# Requires Lean 4 and Mathlib
lake build
```

### Computational Experiments
```bash
cd experiments

# Compile the fast C implementation
cc -O3 -o wobble_primes_only wobble_primes_only.c -lm

# Run for N up to 100,000
./wobble_primes_only 100000

# Generate visualizations
python3 visualizations.py
```

### Requirements
- Lean 4 + Mathlib v4.28.0+ (for formal proofs)
- Python 3.8+ with numpy, matplotlib (for experiments)
- C compiler with -lm (for fast computation)

## Status

**Proof status:** The conjecture is supported by:
- 24+ formally verified theorems in Lean 4
- 8 exact identities connecting Farey discrepancy to the Mertens function
- Computational verification through N=50,000 with zero counterexamples
- The analytical bound for the complete proof is an active area of investigation

**Open problem:** Bound |Σ D·({pf} - 1/2)| (the antisymmetric part of the rank-weighted tooth position sum) to close the analytical proof.

## Author

**Saar Shai** — [GitHub](https://github.com/SaarShai)

## Citation

If you use this work, please cite:
```
@misc{shai-primes-equispaced-2026,
  author={Shai, Saar},
  title={Per-Prime Farey Wobble and the Mertens Function:
         A New Connection via Equispaced Insertion},
  year={2026},
  url={https://github.com/SaarShai/Primes-Equispaced},
  note={Preprint in preparation}
}
```

## Acknowledgments

- [Aristotle](https://aristotle.harmonic.fun) (Harmonic) — automated theorem proving for Lean 4
- Formal proofs co-authored by Aristotle
- Research conducted with Claude (Anthropic)

## License

Code: MIT License
Paper and proofs: CC-BY 4.0
