# Reviewer Handoff: Three-Body Periodic Orbits Paper

**Date:** 2026-03-29
**Authors:** Saar Shai & Anthropic's Claude Opus 4.6
**Paper:** `papers/threebody/main.tex`
**Title:** "Continued Fraction Invariants of Three-Body Periodic Orbits: The Golden Ratio Structure of the Figure-Eight and a Periodic Table of 695 Orbits"

---

## 1. Paper Summary: What It Claims

The paper applies the classical isomorphism F_2 = Gamma(2) < SL(2,Z) to map three-body periodic orbit braid words to 2x2 integer matrices, then extracts continued fraction (CF) invariants from the attracting fixed points of these matrices. It analyzes all 695 equal-mass, zero-angular-momentum orbits from the Li-Liao catalog.

### Core claims:

1. **Figure-eight = golden ratio (exact):** The figure-eight orbit (word BabA) maps to the matrix [[5,-8],[-8,13]] with Fibonacci entries. The fixed-point equation is z^2 - z - 1 = 0, the minimal polynomial of phi. This is an algebraic identity forced by the commutator structure, not a numerical coincidence. (Section 3)

2. **Exact surd arithmetic fixes CF corruption:** Naive float64 computation corrupts 17.7% of orbit CFs (123/695). Replacing with exact integer quadratic-surd tracking (using mpmath only for floor evaluation) yields correct periodic CFs for 691/695 orbits. (Section 4)

3. **Nobility anticorrelates with braid entropy:** CF nobility (fraction of partial quotients = 1) has partial rho = -0.890 with braid entropy controlling for word length, p < 10^-50. (Section 4, Table 1)

4. **Blind prediction:** Nobility alone achieves AUC = 0.980 predicting low-entropy orbits on a held-out test set of 195 orbits (from a 500/195 train/test split). (Section 5, Table 3)

5. **Periodic table:** A 9x8 grid indexed by CF period length and geometric mean organizes 691 orbits into 51 populated cells. Family purity per cell is 69%, meaning the CF organization is substantially orthogonal to topological family classification. 21 cells are empty (potential predictions). (Section 4)

### What the paper explicitly does NOT claim:
- It does NOT claim braid entropy = physical stability (stated as a caveat in the abstract and multiple times in the text)
- It does NOT claim the CF framework is new mathematics (the F_2 = Gamma(2) bridge and Farey tessellation are classical)
- It does NOT claim the empty-cell predictions are validated (direct N-body integration found 0 strictly periodic orbits in 4,199 attempts)
- It does NOT claim novelty in individual components, only in the systematic exact-arithmetic application at scale (extending Kin-Nakamura-Ogawa from ~13 to 695 orbits)

---

## 2. Known Weaknesses and Caveats (Brutally Honest)

### WEAKNESS 1: The Circularity Problem (FUNDAMENTAL)

**Braid entropy and CF properties are computed from the SAME Gamma(2) matrix.** The correlation between nobility and braid entropy is therefore at least partly algebraic/tautological -- both are functions of the same symbolic string (the free-group word). The paper states this in Table 1 note (a) and in Section 6, but this is the single biggest vulnerability.

What this means concretely: a reviewer could argue that finding a correlation between two functions of the same matrix is unsurprising, and that the AUC = 0.98 result is an algebraic identity masquerading as a prediction. The paper's honest labeling helps, but the lack of an independent physical validation is a real gap.

The only truly independent quantity in the correlation table is T* (the physical period from numerical orbit integration), and the correlation with that is only rho = -0.535 (raw, not partial). This is much weaker than the headline numbers.

### WEAKNESS 2: CF-Nobility Is DEGENERATE for Periodic Orbits

**The Hristov test (2026-03-29) showed that CF-nobility cannot distinguish periodic orbits at all.** When Hristov et al.'s 4,860 free-fall periodic orbits are processed, their syzygy sequences reduce to the identity in the free group (because periodic orbits are closed loops). This means ALL 4,860 orbits produce the same CF (the golden ratio, period [1]), making CF-nobility trivially constant = 1.0 for every orbit.

This is NOT a bug in the Li-Liao analysis (which uses the unreduced free-group word that preserves topological information), but it means:
- The CF-nobility measure is not a universal stability predictor
- It works only because the Li-Liao catalog provides non-reduced topological braid words
- A different encoding of the same orbits could make the measure trivial
- The paper does not discuss this degeneracy at all; it should

A follow-up test using syzygy-derived "stutter fraction" as a proxy achieved rho = +0.43 with actual Lyapunov exponents (from Hristov's monodromy eigenvalues), which is real signal but moderate -- and crucially, the SIGN is OPPOSITE to the nobility-stability direction predicted by KAM analogy.

### WEAKNESS 3: Blind Test Size

The paper says "held-out test set of 195 orbits" -- this is correct (500/195 train/test split from 695 total). However, the title says "695 orbits" and the abstract says "695 equal-mass orbits." A reviewer might note that 195 is modest for a prediction claim, though the AUC = 0.980 is strong enough that sample size is not the main issue.

### WEAKNESS 4: "Exact Arithmetic" Is Mislabeled

The paper calls its computation "exact quadratic-surd arithmetic" and "exact integer arithmetic." This is mostly accurate for the surd state tracking (P, q, Q are exact integers), but the floor evaluation step uses mpmath at 100 digits -- which is HIGH-PRECISION floating point, not exact. The paper acknowledges this in Appendix A but the main text uses "exact" loosely.

More precisely: the method is "exact integer surd tracking with high-precision floor evaluation." The floor step could in principle fail for surds very close to an integer, though 100 digits of precision makes this astronomically unlikely. A rigorous version would use interval arithmetic to certify the floor; the paper does not do this.

The 4 orbits with CF periods > 300 that the method could not resolve further highlight that this is not truly exact.

### WEAKNESS 5: Several Empty Cells in the Periodic Table

Of 72 total cells in the 9x8 grid, 21 are empty. The paper frames these as "predictions for undiscovered orbit types," but:
- Direct N-body integration of the top 10 predictions found 0 strictly periodic orbits (0/10, with 4,199 integration attempts)
- 2/10 were "marginal" (near-periodic but not converging)
- The empty cells could simply be forbidden by number-theoretic constraints on CF structure, not indicators of missing orbits

The predictive power of the periodic table is therefore currently zero for orbit discovery.

### WEAKNESS 6: Non-Standard "Nobility" Measure

The paper uses "nobility" as a continuous measure nu in [0,1] (fraction of partial quotients = 1). In classical KAM theory, "noble" is a binary property (noble number = CF of all 1s = golden ratio and its equivalents). The paper acknowledges this (Section 2.3: "This is a non-standard extension"), but:
- Nobility has rho = 0.994 correlation with CF geometric mean, making them essentially redundant
- The standard KAM measures are the Diophantine exponent and Brjuno sum, which are not computed
- The term "nobility" could mislead readers into thinking this connects to standard KAM theory more strongly than it does

### WEAKNESS 7: Missing Competitor Citation

A Research Square preprint (rs-8283973/v1, Dec 2025) on "A Stability-Symmetry Approach to Periodic-Orbit Classification" does something similar: combining Floquet stability + braid complexity. Their approach is cruder (word length, not CF structure) but includes actual Floquet data. This should be cited.

---

## 3. What a Reviewer Should Check

### Mathematical correctness:
- [ ] Verify the figure-eight matrix computation: B*a*b*A = [[5,-8],[-8,13]], trace 18, det 1 (this is straightforward and has been independently verified)
- [ ] Check that the fixed-point equation z^2 - z - 1 = 0 follows from the matrix (it does: (5z-8)/(-8z+13) = z simplifies correctly)
- [ ] Verify the claim that all 695 orbits are hyperbolic (|tr(M)| > 2). This is stated but could be checked computationally
- [ ] Confirm the partial correlation methodology: OLS residualization to control for word length is standard but should be spelled out

### Statistical claims:
- [ ] The AUC = 0.980 on 195 test orbits -- is this a logistic regression? What model? The paper is vague about the classifier
- [ ] Permutation testing (10,000 permutations, p < 0.0001) -- for which statistics specifically?
- [ ] Kruskal-Wallis H = 16.36, p = 0.0026 for family differences -- check df and whether this is meaningful given unequal group sizes (II.A has only 4 orbits)

### The circularity question:
- [ ] Push the authors on whether there is ANY test against a quantity not derived from the braid word
- [ ] The T* correlation (rho = -0.535) is the only independent test -- is this statistically meaningful after controlling for word length?
- [ ] Ask whether Floquet multiplier data exists for any subset of these orbits

### Novelty assessment:
- [ ] Kin-Nakamura-Ogawa (2023) did the Stern-Brocot / Farey connection for ~13 Lissajous orbits. Is going from 13 to 695 orbits a sufficient contribution for a standalone paper?
- [ ] The figure-eight = golden ratio result: is this already known? The Fibonacci matrix structure of the commutator in Gamma(2) is classical. Is the connection to the figure-eight orbit stated anywhere?
- [ ] Series (1985) established cutting sequences through the Farey tessellation give CFs. How much of this paper is just applying Series' framework to a specific dataset?

### Reproducibility:
- [ ] Code availability: the paper promises a GitHub release but it is not yet public
- [ ] The Li-Liao catalog is public (GitHub sjtu-liao/three-body) -- can the results be independently reproduced from the raw free-group words?

---

## 4. Open Questions and Future Directions

### The big open question: Does CF structure predict PHYSICAL stability?

This is the paper's Achilles heel and its most promising future direction. Three paths exist:

1. **Hristov data (best available):** 4,860 orbits with 30-digit Lyapunov exponents. But CF-nobility is degenerate for these orbits (see Weakness 2). A different measure (e.g., stutter fraction from the unreduced syzygy word) achieves rho ~ 0.28-0.43 with Lyapunov, but this is a different measure from what the paper proposes.

2. **Compute Floquet multipliers for Li-Liao orbits:** Medium effort (variational equation integration), would give the definitive test. No one has published these values.

3. **Li-Liao binary S/U classification:** Available for 135,445 unequal-mass orbits. Weaker test (binary, not continuous) but immediately available.

### Other open directions:

- **Unequal mass extension:** Preliminary results show AUC = 0.79 (cross-validated), weaker than equal-mass but still above chance. The m3 = 4 mass ratio shows anomalous correlation reversal -- interesting but unexplained.
- **Nobility-guided orbit search at scale:** Current test (200 trials) is too small. Need Newton refinement of near-periodic solutions.
- **The sign reversal puzzle:** In Hristov's data, higher "stutter fraction" (the analog of simplicity) correlates with MORE instability, opposite to the KAM intuition. Why?
- **Brjuno sum comparison:** Compute the actual Brjuno sum for each orbit's fixed point and compare with the ad-hoc nobility measure.

---

## 5. Status of Fixes Applied to the Paper

The current draft (main.tex) incorporates the following corrections relative to earlier versions:

### Corrections present in the current draft:

| Fix | Description | Status |
|-----|-------------|--------|
| Circularity caveat in abstract | Abstract explicitly states braid entropy != physical stability | DONE |
| Circularity caveat in Section 5 | "Critical caveat" box stating prediction target comes from same matrix | DONE |
| Circularity caveat in Section 6 | Full discussion of algebraic vs physical correlations | DONE |
| Honest limitation #1 | Algebraic vs physical correlations noted | DONE |
| Honest limitation #2 | No physical stability data (no Floquet multipliers) | DONE |
| Honest limitation #3 | Gap predictions not validated (0/10 periodic) | DONE |
| Honest limitation #4 | Non-standard nobility measure, rho=0.994 with geometric mean | DONE |
| Honest limitation #5 | Catalog dependence | DONE |
| "Exact" arithmetic clarification | Appendix A describes mpmath floor evaluation | DONE |
| Braid entropy != Lyapunov | Stated in Section 2.5 and Section 6.2 | DONE |
| Non-standard nobility | Flagged in Section 2.3 with bold text | DONE |
| KAM connection qualified | Section 6.2 says "qualitative" consistency, not proved | DONE |
| Test set size stated | Abstract says 195 orbits explicitly | DONE |
| 691 vs 695 distinction | Paper says 691 with detected CF periods out of 695 total | DONE |

### Corrections NOT yet in the draft:

| Missing Fix | Description | Impact |
|-------------|-------------|--------|
| CF-nobility degeneracy for periodic orbits | The Hristov test showed CF-nobility is constant for periodic orbits. This fundamental limitation is not mentioned anywhere in the paper. | HIGH -- a reviewer aware of this would question the measure's universality |
| Hristov stutter fraction results | The moderate signal (rho ~ 0.28-0.43) from syzygy structure predicting Lyapunov is not mentioned | MEDIUM -- would strengthen the paper by showing some link to physical stability exists |
| Sign reversal between nobility and stutter fraction | High stutter = more unstable, opposite to KAM prediction | MEDIUM -- honest reporting would increase credibility |
| Research Square competitor citation | rs-8283973/v1 does Floquet + braid classification | MEDIUM -- must cite for completeness |
| mpmath != exact arithmetic | Main text says "exact" but the floor step is 100-digit floating point, not certified | LOW -- pedantic but a careful reviewer would notice |
| Unequal mass results (AUC = 0.79) | Available but not in paper | LOW -- would expand scope |

---

## 6. Bottom-Line Assessment

### What is solid:
- The figure-eight = golden ratio identity is an exact algebraic result. It is correct, verifiable, and aesthetically compelling.
- The exact surd arithmetic pipeline is a genuine improvement over float64 (fixing 17.7% of corrupted CFs). This is useful infrastructure.
- The periodic table organization is a novel visualization that may inspire future work.
- The paper's honesty about limitations is above average for this type of work.

### What is vulnerable:
- The headline AUC = 0.98 result is undermined by the circularity problem. A hostile reviewer could dismiss it as algebraic tautology.
- The KAM analogy (nobility ~ stability) is not validated by any physical data. The Hristov test suggests the relationship may be more complicated (or even reversed in sign) compared to what the paper implies.
- The "nobility" measure is non-standard and nearly redundant with the geometric mean (rho = 0.994).
- The paper is fundamentally a computational survey applying classical mathematics to a specific dataset. Whether this constitutes a sufficient contribution depends on the target journal.

### Recommended target journals:
- **Celestial Mechanics and Dynamical Astronomy** -- best fit (computational + dynamical systems audience)
- **Communications in Mathematical Physics** -- ambitious, would need stronger theoretical content
- **Journal of Nonlinear Science** -- possible if framed as computational discovery
- **Physica D** -- good fit for the periodic table / classification aspect

### Pre-submission must-do:
1. Add a section or remark about the CF-nobility degeneracy for periodic orbits (Hristov test result)
2. Either obtain Floquet data or clearly frame the paper as "Part 1: algebraic structure" with physical validation as explicit future work
3. Cite the Research Square preprint
4. Clarify "exact" vs "high-precision" in the main text
