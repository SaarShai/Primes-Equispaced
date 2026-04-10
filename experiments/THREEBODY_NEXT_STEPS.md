# Three-Body Paper: Next Steps Assessment
**Date:** 2026-03-29

## Current State
- Figure-eight = 1/phi (exact, Fibonacci matrix) -- confirmed
- AUC=0.98 nobility predicts braid entropy -- confirmed (with circularity caveat)
- Periodic table: 9x8 grid, 51 cells -- confirmed
- Paper drafted in LaTeX -- ready

---

## Q1: Can we get unequal-mass orbit data?

**YES.** The Li-Liao GitHub repo (sjtu-liao/three-body) has:
- `unequal-mass-data/` directory with orbits at mass ratios 0.5, 0.75, 2, 4, 5, 8, 10
- `non-hierarchical-3b-supplementary_data.txt` -- 135,445 orbits with unequal masses (13,315 stable)
- Free group words in `three-body-unequal-mass-free-group-word.md`

**Action:** Download and run nobility analysis on the 1,349 families. This is straightforward.

---

## Q2: Does the Li-Liao catalog include Floquet/Lyapunov exponents?

**NO -- only binary S/U classification.** The data files contain:
- Initial conditions (positions, velocities)
- Period T
- Free group word (topological classification)
- Stability: "S" (stable) or "U" (unstable) -- binary only

The actual Floquet multiplier VALUES are not published by Li-Liao.

**HOWEVER:** Hristov et al. (2025) computed monodromy eigenvalues to 30 correct digits for:
- 4,860 free-fall orbits (arXiv:2503.00432) -- all unstable, but eigenvalues available
- 971 stable orbits with 160-digit monodromy matrices (arXiv:2510.22802)
- 462 trivial choreographies with 180-digit initial conditions (arXiv:2210.00594)

These are DIFFERENT orbit catalogs from Li-Liao's, but they overlap in some families.

---

## Q3: Can we compute nobility vs Floquet correlation?

**PARTIALLY.** Two paths:

### Path A: Use Hristov's eigenvalue data (easier)
- The 4,860 free-fall orbits have 30-digit eigenvalues available
- We can extract the free group words from these orbits, compute nobility, and correlate against the actual maximal Lyapunov exponent (mu_max)
- This would be an INDEPENDENT test -- Lyapunov exponent is a dynamical quantity, not derived from the braid word
- **Problem:** These are all unstable (no stable orbits), so we'd be testing whether nobility predicts DEGREE of instability, not stability vs instability

### Path B: Compute Floquet multipliers ourselves (harder but better)
- We have initial conditions for the Li-Liao equal-mass orbits
- Integrating the variational equations + computing the monodromy matrix is standard (but needs careful numerics)
- This would give us Floquet multiplier values for the exact orbits we already analyzed
- **Effort:** Medium -- a few hundred lines of Python with scipy, but numerical precision matters

### Path C: Use the S/U classification as a proxy (weakest but immediate)
- Binary logistic regression: does nobility predict S vs U?
- Already partially done but weak statistically with equal-mass data alone
- Gets much stronger with the 135,445 unequal-mass orbits (13,315 stable / 122,130 unstable)

---

## Q4: The circularity objection -- is honesty enough?

**Assessment: Honesty helps but reviewers will likely demand more.**

The circularity: braid entropy is computed from the braid word, and CF properties (nobility) are ALSO derived from the braid word. So a correlation between them is partly tautological -- both are functions of the same symbolic string.

### What would satisfy reviewers:

1. **An independent dynamical measure** (Floquet multiplier, Lyapunov exponent, or KAM stability) that is computed from the DIFFERENTIAL EQUATIONS, not the topology. This breaks the circularity completely.

2. **A prediction task:** Use nobility to PREDICT which topological class an orbit falls into, or predict the period T (which IS dynamical). If nobility predicts period better than word length alone, that's non-trivial.

3. **Cross-catalog validation:** Show the pattern holds on orbits discovered by DIFFERENT groups using different search methods (Hristov vs Li-Liao vs Suvakov-Dmitrasinovic).

### Our honest framing is necessary but insufficient. The paper should:
- Keep the honesty about circularity (essential for credibility)
- ADD at least one independent test from the list above
- Frame nobility as providing STRUCTURE within the space of braid words that braid entropy alone doesn't capture

---

## CRITICAL: Competitor/Complementary Work

A Research Square preprint (rs-8283973/v1, Dec 2025) does something VERY similar:

**"A Stability-Symmetry Approach to Periodic-Orbit Classification"**
- Combines Floquet stability + discrete symmetry + braid complexity into Q(o) = S(o) * tau(o) * C(o)
- Their C(o) is braid-theoretic word length -- similar to our approach but cruder (length, not CF structure)
- They show high-Q orbits are dynamically preferred (chaotic trajectories linger near them)

**Implications:**
- We MUST cite this paper
- Our approach is more refined (CF structure > word length), but we need to show this clearly
- Their Q(o) includes Floquet data -- they've already partially solved our circularity problem
- Potential collaboration or comparison opportunity

---

## Recommended Priority Actions

### HIGH PRIORITY (do before submission)
1. **Download unequal-mass data + run nobility analysis** -- 1-2 days work, would expand from ~700 to ~135K orbits
2. **Get Hristov eigenvalue data** -- contact authors or find supplementary, correlate nobility vs mu_max on their 4,860 orbits. This BREAKS THE CIRCULARITY.
3. **Cite the Research Square preprint** -- position our work as complementary (finer structure via CF vs their coarse word-length)

### MEDIUM PRIORITY (strengthens paper)
4. **Compute Floquet multipliers ourselves** for the ~700 equal-mass orbits we already analyzed -- 3-5 days of coding + computation
5. **Nobility predicts period T** -- test whether CF nobility correlates with the dynamical period (independent of braid word)

### LOWER PRIORITY (nice to have)
6. **3BP-4 full unequal-mass extension** -- systematic scan across mass ratios with nobility analysis
7. **Cross-catalog validation** -- test on Suvakov-Dmitrasinovic's 13 families + Hristov's orbits

---

## Bottom Line

The paper is submittable as-is IF we are honest about circularity. But it will likely get a "revise and resubmit" asking for an independent stability measure. **The single most impactful thing we can do is obtain Hristov's 30-digit Lyapunov exponents and correlate against nobility.** This would convert the paper from "interesting observation with a circularity caveat" to "predictive framework validated against dynamical stability."
