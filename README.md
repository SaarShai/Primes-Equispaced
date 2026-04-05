# The Geometric Signature of Primes in Farey Sequences

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The nontrivial zeros of the Riemann zeta function influence the step-by-step regularity of rational numbers.**

**[Read the paper (PDF)](paper/main.pdf)**

---

## Key Discoveries

### 1. The Farey Spectroscope — A New Way to "See" the Riemann Zeta Zeros
**What it is:** We built a mathematical instrument that detects the locations of the Riemann zeta function's zeros — some of the most important numbers in mathematics — using nothing but data about how fractions are distributed.

**What was known before:** For over 150 years, finding zeta zeros required evaluating the zeta function directly — a complex analytic computation involving infinite sums. Nobody had used Farey discrepancy data as a computational tool to actually LOCATE zeros.

**What we did differently:** We showed you can find the zeros by studying something completely different: how the regularity of simple fractions (like 1/3, 2/5, 3/7) changes when you add more fractions to the list. It's like discovering you can figure out the shape of a bell by listening to its echo off a wall, instead of looking at the bell itself. The key ingredient is a geometric weight R(p) extracted from the Farey step-by-step discrepancy — a quantity that nobody had computed before.

### 2. The Damage/Response Mechanism — Why Primes Improve Order
**What it is:** When a prime number p enters the sequence of fractions, it disrupts the existing order — like a new student joining a perfectly arranged classroom. But the existing fractions shift their positions to MORE than compensate for the disruption. The net effect: things get MORE regular, not less. Nobody had decomposed the process into "damage" and "response" at each individual prime step. The question "why does adding a prime improve regularity?" had no mechanistic answer.

**What we discovered:** The improvement is not automatic — it's a tug-of-war. The new fractions actively DAMAGE the order (we quantify this as R₁ < 0), but the existing fractions collectively shift to overcompensate (R > 0 for all 5,000+ tested primes). This is a structural insight, not just an observation: it reveals that rational numbers have a built-in self-correcting mechanism triggered by primes.

### 3. The 1/p Formula — One Fraction Causes Almost All the Damage
**What it is:** We proved an exact formula: when prime p arrives, the single fraction 1/p (the smallest newcomer) is responsible for about 65% of ALL the disruption. Its displacement is exactly D(1/p) = 1 - |F_p|/p, which approaches -3p/π². Nobody had asked "which individual fraction contributes the most to the discrepancy change?" The idea of tracking damage at the single-fraction level is new.

**The breakthrough:** The product D(1/p) · (1/p) approaches -3/π² ≈ -0.304 — a universal constant, independent of p. This means the damage from each prime is controlled by a single number related to π² and the density of coprime pairs. It's elementary, exact, requires no assumptions, and connects the local geometry of one fraction to a global constant of number theory.

### 4. Per-Step Farey Discrepancy — A New Object Nobody Studied Before
**What it is:** Instead of asking "how regular are all fractions up to N?" (which mathematicians have studied for a century), we ask "what changes when you go from N-1 to N?" — measuring the regularity change ONE STEP AT A TIME. The PER-STEP change ΔW(p) = W(F_{p-1}) - W(F_p) appears not to have been investigated. All prior work looked at the sum; we looked at the summands.

**What this reveals:** The per-step view exposes structure that the cumulative view completely hides. Each prime's contribution correlates strongly with the first zeta zero (R = 0.77 across 4,617 primes). When the correlation breaks at p=243,799, it's not random — the controlling oscillation cos(γ₁·log(p) + φ) crosses through zero at exactly that prime (cos = -0.033), which we can predict. This connects Farey geometry to the Chebyshev bias framework of Rubinstein and Sarnak — a bridge between two areas that had no known connection at this level of detail.

---

## Repository Structure

```
paper/                  LaTeX source, PDF, and supplementary material
RequestProject/         Lean 4 formal proofs (30 files, 258 verified results)
experiments/            Computational scripts and data
  dataset_qualifying_primes.csv  R(p) data for ~5,000 qualifying primes
  R_bound_1M.c                  C program for R(p) computation
  farey_spectroscope.py         Farey spectroscope — detect zeta zeros
  unified_depth_tests.py        Zeta detection + sign prediction tests
  gaussian_farey.py             Gaussian Farey fraction enumeration
  ford_circles_clean.py         Ford circle / hyperbolic verification
figures/                All paper figures (PNG + PDF vectors)
```

## Tools for Researchers

**Farey Spectroscope** — detect zeta zeros from Farey data:
```python
python3 experiments/farey_spectroscope.py
python3 experiments/unified_depth_tests.py
```

**R(p) Computation** — extend the correlation ratio dataset:
```bash
gcc -O2 -o R_bound experiments/R_bound_1M.c -lm
./R_bound 200000
```

**Lean 4 Proofs** — verify all formal results:
```bash
cd RequestProject && lake build
```

## Citation

```bibtex
@article{shai2026geometric,
  title={The Geometric Signature of Primes in Farey Sequences},
  author={Shai, Saar},
  year={2026},
  note={Preprint}
}
```

## AI Disclosure

Research conducted collaboratively with AI systems:
- **Anthropic Claude** (Opus 4.6, Sonnet 4.6, Haiku) — mathematical analysis, computation, formal verification, manuscript
- **Google Gemma 4** (26B) — literature search, brainstorming
- **Alibaba Qwen 3.6 Plus** — analytical reasoning, strategy
- **OpenAI Codex** — adversarial code review
- **Google Gemini** (2.5 Flash, 3, 3.1 Pro) — independent paper review
- **Aristotle** (harmonic.fun) — Lean 4 proof automation

The human author takes full responsibility for the correctness of all mathematical claims.

## License

MIT License
