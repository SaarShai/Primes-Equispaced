# Codex Feedback: Paper A — Quick Wins + Subject Matter
**Date:** 2026-04-13

## CRITICAL fixes (must address)
1. **Novelty statement**: First page must say exactly what ΔW is NOT (not Franel-Landau, not local discrepancy, not δD). Benchmark against prior art explicitly.
2. **One central theorem**: Four-term decomposition + R₂ > 0 positivity. Everything else supports this.
3. **Reproducibility**: State prime cutoff, precision model, cancellation handling for every numerical claim.
4. **"65% damage"**: Must show stability across ranges of p, not just one number. Otherwise: numerology.
5. **"93.6% concentration"**: Present as empirical + methodology. Not a theorem. Show convergence with p.
6. **ΔW ~ M(p)/p² scaling**: Shakiest claim. Needs derivation from bridge identity, not curve-fitting.
7. **Sign bias**: Error bars, robustness across cutoffs.

## EASY wins
- Base cases N=1,2,3,4 exact (sanity check for reader)
- Calibration lemma: ΔW ≠ Franel-Landau (make distinction explicit)
- D(1/p) as clean corollary/proposition
- Sign stats split by ranges [1K, 10K, 100K]

## Literature to cite
Franel 1924, Landau 1924, Huxley 1971, Niederreiter 1973, Codecà-Perelli 1988, Dress 1999
Kanemitsu-Yoshimoto 1996, Mikolás 1950/1952, Tomás 2022, Ledoan 2018, García 2025

## Recommended structure
1. §1: Main theorem (four-term decomp + R₂ > 0, unconditional)
2. §2: Calibration (symmetry, D(1/p), base cases N=1..4)
3. §3: Prime-composite asymmetry (damage/response, examples)
4. §4: Computational evidence (sign bias, concentration — labeled empirical)
5. §5: Conditional theory (explicit formula, Mertens bridge — under RH+LI)
6. §6: Open problems (CLT, wobble, asymptotics)

## Red flags
- Sign flip at p=243,799: interesting data point but don't overweight
- "Top 20% → 93.6%": Pareto stat, not theorem. Show robustness.
- ΔW ~ M(p)/p²: derive or label heuristic. Don't present as proved.
