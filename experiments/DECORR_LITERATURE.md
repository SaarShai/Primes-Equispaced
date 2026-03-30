# Decorrelation Between Farey Rank Fluctuations and Multiplicative Shifts: Literature Review

**Date:** 2026-03-30
**Problem:** Show |Sigma D_err(f) * delta(f)| = o(Sigma delta^2) where D_err is the nonlinear part of Farey displacement and delta is the multiplication-by-p shift.

---

## Executive Summary

No paper in the literature proves exactly our claim. However, the ingredients exist across several deep results in analytic number theory. The most promising paths are:

1. **Daboussi's theorem** (orthogonality of multiplicative functions to additive characters) — closest philosophical match
2. **Boca-Zaharescu correlation theory** — establishes that Farey fraction correlations exist and are computable
3. **Klurman-Mangerel pretentious framework** — gives precise conditions under which multiplicative functions decorrelate from structured sequences
4. **Bombieri-Friedlander-Iwaniec bilinear form estimates** — the technical machinery for controlling bilinear sums
5. **Matomaki-Radziwill short interval theory** — controls multiplicative functions in short windows

The key insight: our D_err is an "additive/order-statistic" object (depending on the rank ordering of Farey fractions), while delta is a "multiplicative" object (multiplication by p modulo 1). The general principle that additive and multiplicative structures decorrelate is well-established but proving it in our specific setting requires assembling tools from multiple sources.

---

## 1. Farey Fraction Correlations

### 1.1 Boca-Zaharescu (2005): "The Correlations of Farey Fractions"
- **Journal:** J. London Math. Soc. 72(1), 25-39
- **arXiv:** math/0404114
- **Result:** ALL correlations of Farey fractions exist and explicit formulas are provided for the correlation measures.
- **Relevance:** HIGH. This is the foundation for understanding any correlation structure among Farey fractions. Their methods use the connection between Farey fractions and lattice points in domains bounded by hyperbolas.
- **Gap:** They study correlations between Farey fractions themselves (spacing statistics), not correlations between Farey rank errors and multiplicative shifts. But their framework could potentially be extended.

### 1.2 Boca-Siskaki (2021): "A Note on the Pair Correlation of Farey Fractions"
- **arXiv:** 2109.12744
- **Result:** Pair correlations of Farey fractions with denominators q satisfying (q,m)=1 or q = b (mod m) exist and are explicitly computed.
- **Relevance:** MEDIUM. Shows the theory extends to restricted denominator sets, which is closer to our multiplication-by-p setting.

### 1.3 Chahal et al. (2023): Pair Correlation with Square-Free Denominators
- **arXiv:** 2303.12882
- **Result:** Limiting pair correlation function exists for Farey fractions with square-free denominators.
- **Relevance:** MEDIUM. Demonstrates robustness of correlation theory under arithmetic restrictions.

### 1.4 Karvonen-Zhigljavsky (2024): "Maximum Mean Discrepancies of Farey Sequences"
- **arXiv:** 2407.10214, published in Acta Math. Hungar. (2025)
- **Result:** Identifies a large class of positive-semidefinite kernels (including all Matern kernels of order >= 1/2) for which polynomial convergence rate of MMD of Farey sequences is equivalent to RH.
- **Relevance:** HIGH for conceptual framework. Connects Farey discrepancy to kernel methods, providing a modern statistical language for our problem.

### 1.5 New Analytical Formulas for Farey Rank (2024)
- **Journal:** Mathematics 13(1), 140
- **Result:** New rank formula for Farey fractions with improved error estimates for local discrepancy.
- **Relevance:** DIRECT. The D_err in our problem IS the local discrepancy/rank error. Any improved formula for D_err feeds directly into our decorrelation bound.

---

## 2. Multiplicative Function Correlations and Decorrelation

### 2.1 Daboussi's Theorem (1975) — THE KEY ANALOGY
- **Result:** For any bounded multiplicative function f and irrational alpha: (1/x)|Sigma_{n<=x} f(n) e(alpha n)| -> 0.
- **Interpretation:** Bounded multiplicative functions are ORTHOGONAL to additive characters.
- **Relevance:** CRITICAL. This is the closest known result to what we need. Our D_err(f) plays the role of an "additive" or "order-statistic" quantity, and the multiplication-by-p shift delta(f) has multiplicative structure. Daboussi says these should decorrelate.
- **Gap:** D_err is not exactly an additive character — it depends on the rank structure of Farey fractions, which is more complex. We need a "Daboussi for Farey rank errors."
- **Extensions:** Katai gave a simpler proof and extended to e(theta n^2). Frantzikinakis-Host extended to nilsequences.

### 2.2 Klurman (2017): "Correlations of Multiplicative Functions and Applications"
- **Journal:** Compositio Math. 153(8), 1622-1657
- **arXiv:** 1603.08453
- **Result:** Asymptotic formula for correlations Sigma f_1(P_1(n)) ... f_m(P_m(n)) for bounded pretentious multiplicative functions at polynomial arguments.
- **Consequences:** Characterizes all f: N -> {-1,+1} with bounded partial sums (answering Erdos 1957); settles Katai conjecture.
- **Relevance:** HIGH. The pretentious/non-pretentious dichotomy is key: NON-PRETENTIOUS functions decorrelate from everything. The Mobius function mu(n) is non-pretentious, and our delta shift inherits multiplicative structure from the denominator arithmetic.

### 2.3 Klurman-Mangerel-Teravaiinen: Pretentious Framework Extensions
- **Papers:** Multiple, 2018-2023, published in Math. Annalen, Mathematika, PLMS
- **Key result:** Non-pretentious multiplicative functions satisfy Elliott's conjecture at almost all scales — this is a DECORRELATION result.
- **Relevance:** HIGH. Gives conditions under which we can guarantee decorrelation.

### 2.4 Matomaki-Radziwill (2016): "Multiplicative Functions in Short Intervals"
- **Journal:** Annals of Mathematics 183(3)
- **arXiv:** 1501.04585
- **Result:** Relates short averages of multiplicative functions to long averages. Proves cancellation of mu(n) in almost all short intervals [x, x+psi(x)] with psi(x) -> infinity arbitrarily slowly.
- **Relevance:** HIGH. If we can express our bilinear sum as an average over short intervals, this machinery applies.
- **Key technique:** Combines Halasz's theorem with a novel "short to long" transfer principle.

### 2.5 Correlation Sequences of Multiplicative Functions
- **Related to Daboussi, formalized by Frantzikinakis-Host**
- **Result:** Correlation sequences f(a) = lim (1/log omega_m) Sigma g_0(n+ah_0)...g_k(n+ah_k)/n are uniform limits of periodic sequences. If the product g_0...g_k does NOT pretend to be a Dirichlet character, then f vanishes identically.
- **Relevance:** MEDIUM-HIGH. Provides structural results about when correlations vanish.

---

## 3. Bilinear Form Estimates (Technical Machinery)

### 3.1 Duke-Friedlander-Iwaniec (1997): "Bilinear Forms with Kloosterman Fractions"
- **Journal:** Inventiones Math. 128, 23-43
- **Result:** First non-trivial bounds for bilinear sums involving Kloosterman fractions overline{m}/n.
- **Relevance:** HIGH. Kloosterman fractions are intimately connected to Farey sequence structures. The bilinear form Sigma_{m,n} a_m b_n e(overline{m}/n) is exactly the type of sum that appears when analyzing Farey displacement under multiplication.
- **This is the technical engine** we need: bounding Sigma a_m b_n (nonlinear Farey term) reduces to controlling bilinear forms with Kloosterman-type phases.

### 3.2 Bettin-Chandee (2019): Trilinear Forms
- **arXiv:** 1502.00769
- **Result:** Improved bounds for trilinear forms in Kloosterman fractions.
- **Relevance:** MEDIUM. Provides stronger estimates that feed into the dispersion method.

### 3.3 Kowalski-Michel-Sawin: Bilinear Forms with Hyper-Kloosterman Sums
- **Result:** Non-trivial bounds for general bilinear forms in hyper-Kloosterman sums below the Polya-Vinogradov range.
- **Relevance:** MEDIUM. Extends the toolkit to more general settings.

### 3.4 Recent improvements (2025): arXiv 2601.00292
- **Result:** Improves DFI bounds; in the balanced case, improvement by 1/12.
- **Relevance:** LOW-MEDIUM. Incremental but shows the field is active.

---

## 4. The Dispersion Method and Type I/II Decomposition

### 4.1 Linnik's Dispersion Method (1958-1961)
- **Book:** "The Dispersion Method in Binary Additive Problems" (AMS)
- **Result:** Controls bilinear correlations by bounding the "dispersion" (variance) of arithmetic sums.
- **Relevance:** HIGH. The dispersion method is specifically designed for the type of bilinear correlation we need to control. It reduces the problem to bounding a variance.

### 4.2 Fouvry-Radziwill (2018): "Another Application of Linnik's Dispersion Method"
- **arXiv:** 1812.00562
- **Result:** General dispersion estimate for "narrow" type-II sums. Shows multiplicative convolutions have exponent of distribution beyond 1/2. Uses Bettin-Chandee trilinear Kloosterman bounds and DFI bilinear bounds.
- **Relevance:** VERY HIGH. This is the closest modern work to what we need technically. They control bilinear sums where one variable has multiplicative structure and the other has additive structure.

### 4.3 Vaughan's Identity and Type I/II Decomposition
- **Original:** Vaughan (1977)
- **Result:** Decomposes sums over primes into Type I (convolution structure, tractable) and Type II (bilinear, requires Cauchy-Schwarz).
- **Relevance:** HIGH for methodology. If we can decompose our D_err * delta sum using a Vaughan-type identity, we reduce to standard Type I and Type II estimates.
- **Connection to Farey:** In the circle method, Farey fractions organize the major/minor arcs. Vaughan's identity is applied to the exponential sums that arise on minor arcs.

---

## 5. Shifted Convolution Sums

### 5.1 Classical Theory
- **Key authors:** Ingham, Estermann, Good, Jutila, Motohashi
- **Result:** Asymptotic formulas for Sigma d(n)d(n+h), where d is the divisor function.
- **Relevance:** MEDIUM. Our sum Sigma D_err(f) delta(f) has the flavor of a shifted convolution where one factor is arithmetic (delta) and the other is order-statistic (D_err).

### 5.2 Shifted Convolutions with Multiplicative Functions (2022)
- **arXiv:** 2204.08221
- **Result:** Asymptotic formulas for Sigma tau(n) f(n+h) for multiplicative f, using Bettin-Chandee trilinear Kloosterman bounds AND Linnik's dispersion method AND the Bourgain-Katai-Sarnak-Ziegler criterion.
- **Relevance:** HIGH. Demonstrates exactly the kind of hybrid estimate (arithmetic shift + multiplicative function) that we need.

### 5.3 Decorrelation for Convolutions (Canadian J. Math, 2024)
- **Result:** For periodic multiplicative functions f_1, f_2 from Klurman's classification, there is a nontrivial correlation between Delta(x) and Delta(theta*x) when theta is RATIONAL, and DECORRELATION when theta is IRRATIONAL. Quantitative if theta has finite irrationality measure.
- **Relevance:** VERY HIGH. This is a concrete decorrelation theorem for an arithmetic error term under multiplicative scaling. Our setting (multiplication by prime p) makes theta = p, which is rational — but our D_err is different from the divisor-sum error Delta.

---

## 6. Additive vs. Multiplicative Structure: The Grand Theme

### 6.1 Sum-Product Phenomenon (Erdos-Szemeredi, Bourgain, Tao-Vu)
- **Principle:** A set cannot simultaneously have large additive AND multiplicative structure. |A+A| + |A*A| >> |A|^{1+epsilon}.
- **Relevance:** CONCEPTUAL. Our decorrelation claim is a continuous analogue: the additive (rank-ordering) structure of D_err and the multiplicative structure of delta cannot correlate strongly.

### 6.2 Sarnak's Mobius Disjointness Conjecture
- **Conjecture (2010):** For any deterministic (zero-entropy) sequence xi(n), Sigma mu(n) xi(n) = o(N).
- **Relevance:** VERY HIGH. If D_err(f) is "deterministic" (low complexity), then the Mobius function — and by extension multiplicative shifts — should be disjoint from it. The question is whether D_err has sufficiently low dynamical complexity.
- **Status:** Proved for many classes of deterministic sequences (Bourgain-Sarnak-Ziegler, Green-Tao, Matomaki-Radziwill-Tao).

### 6.3 Bourgain-Sarnak-Ziegler Criterion
- **Result:** If xi(n) has sufficiently slowly growing complexity, then Sigma mu(n) xi(n) = o(N).
- **Relevance:** HIGH. Could potentially be applied to D_err if we can bound its "complexity."

---

## 7. Barban-Davenport-Halberstam for Farey

### 7.1 Classical BDH Theorem
- **Result:** Sigma_{q<=Q} Sigma_{a: (a,q)=1} |E(x;a,q)|^2 << xQ log x for Q <= x, where E(x;a,q) is the error in the prime counting function in arithmetic progressions.
- **Relevance:** MEDIUM. The BDH gives mean-square control of errors in arithmetic progressions. An analogous result for Farey rank errors would directly give our decorrelation bound.

### 7.2 Hooley's Extensions
- **Papers:** Series "On the Barban-Davenport-Halberstam theorem I-XVIII"
- **Relevance:** MEDIUM. Extensive refinements that may contain applicable lemmas.

---

## 8. Equidistribution of Coprime Residues

### 8.1 Pollack-Singha Roy (2023): Distribution of Multiplicative Functions in Coprime Residue Classes
- **arXiv:** 2303.14600, published in Math. Zeitschrift
- **Result:** Polynomially-defined multiplicative functions (like phi(n)) are equidistributed in coprime residue classes mod q, uniformly for q << (log x)^K.
- **Relevance:** MEDIUM. Shows that multiplicative functions spread out uniformly, which is a form of decorrelation from the additive structure of residue classes.

---

## 9. Recommended Proof Strategy

Based on this literature review, here is the most promising attack plan:

### Strategy A: Daboussi + Farey Rank Analysis
1. Express D_err(f) in terms of an explicit formula involving Euler/totient sums (using the rank formula literature, Section 1.5)
2. Express delta(f) = {pf} - {f} in terms involving e(pf) type exponentials
3. Apply Daboussi-type orthogonality (Section 2.1) to show the cross-terms cancel
4. **Difficulty:** D_err is not a pure additive character; it has a nonlinear dependence on the rank ordering

### Strategy B: Dispersion Method (Fouvry-Radziwill style)
1. Write Sigma D_err * delta as a bilinear form
2. Apply Cauchy-Schwarz to reduce to bounding Sigma |Sigma_f D_err(f) e(alpha f)|^2
3. Open the square and use the Farey correlation theory (Boca-Zaharescu) to evaluate the diagonal
4. Use DFI bilinear Kloosterman bounds for the off-diagonal
5. **Advantage:** Closest to existing technology. Fouvry-Radziwill (2018) did exactly this for a related problem.

### Strategy C: Sarnak Disjointness
1. Show D_err has "deterministic" or "low complexity" behavior (it is determined by the Farey ordering, which is a geometric/lattice construction)
2. Apply Bourgain-Sarnak-Ziegler or Matomaki-Radziwill-Tao to get Sigma mu(n) D_err(n) = o(N)
3. Transfer from Mobius to multiplication-by-p via partial summation
4. **Advantage:** Conceptually cleanest. **Disadvantage:** Hardest to make quantitative.

### Strategy D: Direct BDH Analogue
1. Prove a BDH-type mean-square bound for Farey rank errors averaged over shifts
2. Sigma_{p<=P} |Sigma_f D_err(f) delta_p(f)|^2 << (something manageable)
3. This gives decorrelation for MOST primes p, which may suffice
4. **Advantage:** Only need a mean-square bound, not pointwise. **Disadvantage:** Need to develop the BDH machinery for Farey ranks from scratch.

---

## 10. Key Open Questions

1. **Is D_err "deterministic" in the sense of Sarnak?** If yes, Strategy C applies immediately.
2. **Can we write D_err explicitly as a sum of Kloosterman-type terms?** If yes, Strategy B applies via DFI bounds.
3. **Does BDH extend naturally to Farey rank errors?** No one seems to have tried this.
4. **What is the "pretentious distance" of our delta shift from structured functions?** If delta is non-pretentious, Klurman-Mangerel gives decorrelation for free.

---

## 11. References (Full List)

### Farey Correlations
- Boca, F.P. and Zaharescu, A. "The correlations of Farey fractions." J. London Math. Soc. 72(1), 25-39 (2005). arXiv:math/0404114
- Boca, F.P. and Siskaki, M. "A note on the pair correlation of Farey fractions." arXiv:2109.12744 (2021)
- Chahal, J. et al. "Pair correlation of Farey fractions with square-free denominators." arXiv:2303.12882 (2023)
- Karvonen, T. and Zhigljavsky, A. "Maximum mean discrepancies of Farey sequences." Acta Math. Hungar. (2025). arXiv:2407.10214

### Multiplicative Correlations and Decorrelation
- Daboussi, H. "Fonctions multiplicatives presque periodiques B." Asterisque 24-25, 321-324 (1975)
- Klurman, O. "Correlations of multiplicative functions and applications." Compositio Math. 153(8), 1622-1657 (2017). arXiv:1603.08453
- Klurman, O. and Mangerel, A. "Rigidity theorems for multiplicative functions." Math. Annalen 372(1), 651-697 (2018)
- Klurman, O., Mangerel, A. and Teravaiinen, J. "Correlations of multiplicative functions in function fields." Mathematika 69(1), 155-231 (2023)
- Matomaki, K. and Radziwill, M. "Multiplicative functions in short intervals." Ann. Math. 183(3) (2016). arXiv:1501.04585
- Matomaki, K. and Radziwill, M. "Multiplicative functions in short intervals II." arXiv:2007.04290 (2020)

### Bilinear Forms and Kloosterman Sums
- Duke, W., Friedlander, J. and Iwaniec, H. "Bilinear forms with Kloosterman fractions." Invent. Math. 128, 23-43 (1997)
- Deshouillers, J.M. and Iwaniec, H. "Kloosterman sums and Fourier coefficients of cusp forms." Invent. Math. 70, 219-288 (1982)
- Bettin, S. and Chandee, V. "Trilinear forms with Kloosterman fractions." arXiv:1502.00769 (2019)
- Kerr, B. et al. "Bounds on bilinear forms with Kloosterman sums." J. London Math. Soc. (2023)

### Dispersion Method
- Linnik, Yu.V. "The Dispersion Method in Binary Additive Problems." AMS Translations of Mathematical Monographs 4 (1963)
- Fouvry, E. and Radziwill, M. "Another application of Linnik's dispersion method." arXiv:1812.00562 (2018)

### Shifted Convolution Sums
- arXiv:2204.08221 — Shifted convolutions with multiplicative functions (2022)
- arXiv:2502.08305 — On additive convolution sum of arithmetic functions (2025)
- Canadian J. Math (2024) — Decorrelation of divisor-sum error under irrational scaling

### Sarnak Disjointness and Orthogonality
- Sarnak, P. "Three lectures on the Mobius function, randomness and dynamics." (2010)
- Bourgain, J., Sarnak, P. and Ziegler, T. "Disjointness of Moebius from horocycle flows." (2013)

### Barban-Davenport-Halberstam
- Hooley, C. "On the Barban-Davenport-Halberstam theorem I-XVIII." Various journals (1975-2005)

### Equidistribution
- Pollack, P. and Singha Roy, A. "Distribution in coprime residue classes of polynomially-defined multiplicative functions." Math. Zeitschrift (2023). arXiv:2303.14600

### Farey-Mertens Connection
- Cox, D. et al. "The Farey Sequence and the Mertens Function." arXiv:2105.12352 (2021)
- Franel, J. and Landau, E. (1924) — Original equivalence of Farey discrepancy sum and RH

---

## 12. Verdict

**Nobody has proved our exact decorrelation claim.** The closest results are:

| Result | How close | Gap |
|--------|-----------|-----|
| Daboussi orthogonality | Very close philosophically | D_err is not an additive character |
| Boca-Zaharescu correlations | Close technically | Studies Farey-Farey correlation, not Farey-multiplicative |
| Fouvry-Radziwill dispersion | Close in machinery | Their sums have different structure |
| Sarnak disjointness | Close if D_err is deterministic | Need to verify complexity condition |
| Shifted convolutions (2022) | Close in flavor | Their arithmetic function is different |

**Bottom line:** This appears to be a genuinely novel problem requiring assembly of known tools in a new configuration. The most promising approach is Strategy B (dispersion method + Kloosterman bilinear bounds), with Strategy C (Sarnak disjointness) as a cleaner but harder alternative.

**Classification:** If proved, this would be a C1-C2 result (collaborative, minor to publication grade) — the individual tools are known, but the specific combination and application to Farey rank errors appears new.
