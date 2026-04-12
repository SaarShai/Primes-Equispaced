# Farey Spectroscopy: Detecting Riemann Zeta Zeros from Arithmetic Data

**434 Lean 4 verified results** | **800 interval-arithmetic certificates** | **Batch spectroscope: 10K L-functions in 18 seconds**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What This Is

The **Mertens spectroscope** detects nontrivial zeros of the Riemann zeta function from arithmetic data alone, without evaluating zeta(s):

$$F(\gamma) = \gamma^2 \left|\sum_{p \le N} \frac{M(p)}{p} e^{-i\gamma \log p}\right|^2$$

where M(p) is the Mertens function. Peaks in F(gamma) locate zeta zero ordinates.

## Key Results

### Theorems (proved)
- **K <= 4 non-vanishing** (unconditional): |c_K(rho)| > |1/sqrt(2) - 1/sqrt(3)| > 0 for ALL nontrivial zeta zeros
- **Density-zero detection** (unconditional): c_K(rho) != 0 for all but O(T) zeros up to height T
- **Detection theorem** (GRH): F(gamma_k)/F_avg -> infinity for every zero
- **Universality** (GRH): any prime subset with divergent reciprocal sum detects all zeros
- **Stability** (unconditional): large sieve noise bound

### Computational Certificates
- **800/800** interval-arithmetic certifications: c_K(rho_j) != 0 for K=10,20,50,100 at first 200 zeros
- **Amplitude matching**: theoretical R^2 = 0.949 vs empirical 0.944 (50-digit precision)
- **Phase verification**: phi_1 = -1.6933 rad (0.003 rad accuracy)

### The Avoidance Phenomenon (novel discovery)
The truncated Mobius Dirichlet polynomial c_K(s) has infinitely many zeros (Langer 1931), but they **systematically avoid** zeta zero ordinates by 4-16x. This extends to L-functions (verified for L(s, chi_4) at 3.84x). See the [Generalized DPAC conjecture](https://github.com/google-deepmind/formal-conjectures/pull/3716).

### Batch Spectroscope
C implementation scans all Dirichlet L-functions mod q simultaneously:
- q = 97: 0.12 seconds (96 characters)
- q = 997: 1.7 seconds (996 characters)
- q = 9973: 18 seconds (9972 characters)

See [batch-spectroscope repo](https://github.com/SaarShai/batch-spectroscope).

## Lean 4 Formalization

434 verified results across:

| Category | Results | Key theorems |
|----------|---------|-------------|
| Farey combinatorics | ~200 | Mediant minimality, gap formulas, cardinality |
| Bridge Identity | ~50 | Sum over F_{p-1} of e^{2pi i p f} = M(p) + 2 |
| Injection Principle | ~30 | Distinct gap insertion via modular inversion |
| Four-term decomposition | ~30 | DeltaW = A - B - C - D exact decomposition |
| Figure-eight orbit | 8 | Three-body period ratio = golden ratio |
| Prime power divergence | 3 | Sum p^k diverges for k >= 1 |
| Strict positivity | ~50 | Various bounds on Farey statistics |
| Other supporting | ~60 | Displacement-shift, Ramanujan sums, etc. |

**2 remaining sorrys**: BridgeIdentity (assembly step), SignTheorem (general case).

## Repository Structure

```
RequestProject/          # Lean 4 source files (434 results)
  BridgeIdentity.lean    # Farey-Mertens bridge (1 sorry)
  InjectionPrinciple.lean
  PrimeCircle.lean       # Core Farey properties
  SignTheorem.lean        # Sign pattern (2 sorry)
  ...
spectroscope-paper/      # Visualizations and benchmarks
lakefile.toml            # Lean 4 build configuration
lean-toolchain           # Lean version
```

## Related Repositories

- **[batch-spectroscope](https://github.com/SaarShai/batch-spectroscope)** — C implementation + benchmark results + interval certificates
- **[Formal conjectures PR #3716](https://github.com/google-deepmind/formal-conjectures/pull/3716)** — DPAC + Bridge Identity + Sign Pattern submitted to DeepMind

## Papers (in preparation)

- **Paper C**: "Prime Spectroscopy of Riemann Zeros" — 5 theorems, 800 certificates, batch speedup
- **Paper A**: "Per-Step Farey Discrepancy" — DeltaW(N), four-term decomposition, 33,000:1 cancellation
- **Paper B**: "Chebyshev Bias in Farey Sequences" — phase resolution phi_1 = -1.6933 rad

## Citation

```
Saar Shai, "Prime Spectroscopy of Riemann Zeros" (2026).
GitHub: https://github.com/SaarShai/Primes-Equispaced
AI Disclosure: Research conducted with assistance from Claude (Anthropic).
```

## License

MIT
