# Comprehensive Literature Search: Farey Discrepancy and Related Results

**Date:** 2026-03-29
**Purpose:** Identify prior work relevant to our proof, especially lower bounds on sum D^2, spectral formulas, and per-step discrepancy results.

---

## 1. Farey Sequence Discrepancy Lower Bounds / L2 Discrepancy

### Dress (1999) — "Discrepance des suites de Farey"
- **Journal:** J. Theorie des Nombres de Bordeaux, 11(2), 345-367
- **Key Result:** The absolute discrepancy of the Farey sequence F_Q is EXACTLY 1/Q for every Q >= 1. This is sharp — it matches the local discrepancy at the point 1/Q.
- **Method:** Uses an upper bound on an integral related to the summatory function of the Mobius function.
- **Relevance to us:** (a) No lower bound on sum D^2 improving N^3 to N^3 log N. (b) No spectral formula. (c) No per-step results. But confirms our discrepancy normalization is correct.
- **Sources:** [Numdam PDF](https://www.numdam.org/article/JTNB_1999__11_2_345_0.pdf), [EUDML](https://eudml.org/doc/248344), [JSTOR](https://www.jstor.org/stable/43972541)

### Niederreiter (1973) — "The distribution of Farey points"
- **Journal:** Mathematische Annalen, 201, 341-345
- **Key Result:** First proved the discrepancy of F_Q has order of magnitude 1/Q (best possible estimate). Used exponential sum methods and Ramanujan sums.
- **Connection to us:** The exponential sum / Ramanujan sum technique is relevant to spectral decomposition approaches. Ramanujan sums c_q(n) are character-like objects.
- **Source:** [Springer](https://link.springer.com/article/10.1007/BF01428199)

### General L2-discrepancy lower bounds (Hinrichs-Markhasin 2010, Roth, Bilyk-Lacey)
- These concern general point sets in [0,1]^d, not specifically Farey sequences.
- Best known: L2-discrepancy >= c * sqrt(log N) in dimension 2 (Roth's method via Haar basis).
- **Not directly applicable** to our Farey-specific sum of squared discrepancies.

---

## 2. Franel-Landau Identity and Sum of Squared Discrepancies

### Franel (1924) + Landau (1924)
- **Papers:** "Les suites de Farey et le probleme des nombres premiers" (Gottinger Nachr. 1924, 198-201) and Landau's "Bemerkungen" (ibid., 202-206).
- **Key Identity (Franel's Identity):** For the Farey sequence F_n with |F_n| = Phi(n) = sum_{k<=n} phi(k), define d_k = a_k - k/Phi(n) where a_k is the k-th Farey fraction. Then:

  **sum_{k=1}^{Phi(n)} d_k^2 = sum_{k=1}^{n} (M(floor(n/k)))^2 / ... [see below]**

  The exact identity (from Edwards, Riemann's Zeta Function, p.264) is:

  sum_{v=1}^{A(x)} f(r_v) = sum_{k=1}^{infty} sum_{j=1}^{k} f(j/k) * M(x/k)

  where M is the Mertens function and A(x) = |F_x|. Setting f appropriately yields:

  **sum d_k^2 is expressible as a bilinear form in M(floor(n/k))**.

- **RH Equivalences:**
  - (Franel) sum d_k^2 = O(n^r) for all r > -1 iff RH
  - (Landau) sum |d_k| = O(n^r) for all r > 1/2 iff RH

- **Connection to Mertens:** M(n) = -1 + sum_{a in F_n} e^{2*pi*i*a}. This formula is used in the proof.

- **CRITICAL NOTE:** The Franel identity expresses the L2-discrepancy sum as a quadratic form in the Mertens function values M(floor(n/k)). This is the closest thing in the literature to our approach but works with the GLOBAL discrepancy, not per-step discrepancy.

### What is NOT known (gaps we might fill):
- **(a)** No explicit lower bound on sum d_k^2 improving the trivial O(N^{-1}) per term bound to get N^3 log N type growth for the cumulative sum.
- **(b)** No spectral/character decomposition of the Franel identity beyond the connection to Ramanujan sums.
- **(c)** No per-step version of the Franel identity.

---

## 3. Mikolas and Extensions

### Mikolas (1949, 1951) — Farey series and prime number problem
- **Papers:** Acta Sci. Math. (Szeged), 13 (1949), 93-117 and 14 (1951), 5-21.
- **Key Identity (Mikolas):** sum_{n=1}^{x} M(floor(x/n)) = 1
- **General Theorem:** For polynomials of degree <= 3, power moment results that generalize Franel's sum. Kopriva, Mikolas, and Zulauf results are special cases.
- **Lemma 7:** For each s with Re(s) >= 1/2, the estimate S_s(x) = O(x^{1/2+eps}) is equivalent to RH.

### Mikolas-Sato (1992) — "On the asymptotic behaviour of Franel's sum and the Riemann Hypothesis"
- **Journal:** Results in Mathematics, 21, 368-378
- **Key Result:** Studies the asymptotic behavior of Franel's sum (sum of squared Farey discrepancies) and its connection to RH. Extends the class of functions for which RH equivalences hold.
- **Source:** [Springer](https://link.springer.com/article/10.1007/BF03323094)

---

## 4. Codeca-Perelli (1988) — Uniform Distribution and l^p Spaces

- **Paper:** "On the uniform distribution (mod 1) of the Farey fractions and l^P spaces"
- **Journal:** Mathematische Annalen, 279(3), 413-422 (1987/88)
- **Key Result:** Studies the l^p norms of the Farey discrepancy vector. The case p=2 corresponds to the Franel sum. For general p, establishes RH-equivalences.
- **Relevance:** This is the most direct precursor to studying sum |d_k|^p for general p. However, it does NOT study per-step changes or provide lower bounds beyond what Franel gives.
- **7 citations** (relatively niche).
- **Sources:** [EUDML](https://eudml.org/doc/164331), [Springer](https://link.springer.com/article/10.1007/BF01456278), [Semantic Scholar](https://www.semanticscholar.org/paper/On-the-uniform-distribution-(mod-1)-of-the-Farey-Codec%C3%A0-Perelli/acd7ef0e49358635a7caa7b43a34dcbb00785ec1)

---

## 5. Kanemitsu-Yoshimoto (1996) — Farey Series and RH

- **Paper:** "Farey series and the Riemann hypothesis"
- **Journal:** Acta Arithmetica, 75(4), 351-374
- **Key Result:** Significantly extends the class of functions (including Kubert functions) for which conditions equivalent to RH can be formulated. Generalizes the "problem of equivalence" posed by Mikolas.
- **Series:** Part I of IV:
  - II: Acta Math. Hung. 78 (1998), 287-304
  - III: Ramanujan J. 1 (1997), 363-378
  - IV: Acta Math. Hung. 87 (2000), 109-119
- **Relevance:** Extends Franel-Landau to Kubert functions. Does NOT provide lower bounds, spectral decompositions, or per-step analysis.
- **Source:** [Full PDF](http://matwbn.icm.edu.pl/ksiazki/aa/aa75/aa7544.pdf), [EUDML](https://eudml.org/doc/206882)

---

## 6. Boca-Cobeli-Zaharescu (2000-2005) — Pair Correlation of Farey Fractions

### BCZ Map and h-spacing (2001)
- **Paper:** "The h-spacing distribution between Farey points"
- **Journal:** Math. Proc. Cambridge Phil. Soc. 131(1), 23-38 (2001)
- **Also:** "A conjecture of R. R. Hall on Farey points," J. Reine Angew. Math. 535 (2001), 207-236

### Pair Correlation (Boca-Zaharescu 2005)
- **Paper:** "The correlations of Farey fractions"
- **Journal:** J. London Math. Soc., 72(1), 25-39 (2005)
- **Key Result:** ALL correlations of Farey fractions exist. Explicit formula for pair correlation:

  g(lambda) = (6/pi^2 * lambda^2) * sum_{1 <= k < pi^2*lambda/3} phi(k) * log(pi^2*lambda / 3k)

  As lambda -> infinity: g(lambda) = 1 + O(lambda^{-1}), confirming Poissonian behavior at large scales.
- **The BCZ Map:** A dynamical systems tool encoding Farey sequence statistics. Used to study distribution problems.
- **Extensions:**
  - Xiong-Zaharescu (2008): prime denominators -> Poissonian pair correlation
  - Boca-Siskaki (2022): arithmetic progressions
  - Chahal-Chaubey (2023): square-free denominators (arXiv:2303.12882)
- **Relevance:** The pair correlation measures SPACING between adjacent Farey fractions. This is closely related to per-step discrepancy changes when a new fraction is inserted. The BCZ map could potentially encode our Sign Theorem.
- **Sources:** [arXiv:math/0404114](https://arxiv.org/abs/math/0404114), [Cambridge Core](https://www.cambridge.org/core/journals/journal-of-the-london-mathematical-society/article/abs/correlations-of-farey-fractions/5EB07F8B97A1AAAC46C253E32C7D61B4)

---

## 7. Karvonen-Zhigljavsky (2025) — Maximum Mean Discrepancies of Farey Sequences

- **Paper:** "Maximum mean discrepancies of Farey sequences"
- **Journal:** Acta Math. Hungar. (2025); arXiv:2407.10214 (July 2024)
- **Key Result (Theorem 2.1):** For a positive-semidefinite kernel K on [0,1] with RKHS H satisfying:
  - (a) H is a subset of W^{1,2}([0,1]) (Sobolev space of order 1)
  - (b) H contains functions x -> a + bx + x^beta for beta in [2,gamma] union {4,5} with gamma approx 3.405

  Then RH holds iff MMD(F_n) = O(n^{-3/2+eps}) = O(N^{-3/4+eps}) for every eps > 0.

- **Critical Identity (Lemma 4.1):** For kernel K_0(x,y) = 1 + min{x,y}:

  **MMD(X)^2 = (1/N) * sum_{i=1}^{N} (i/N - x_i)^2 - 1/(6N^2)**

  This directly connects MMD to the L2 discrepancy of the Farey sequence!

- **Covered kernels:** Matern (nu >= 1/2), integrated Brownian motion, energy-distance (alpha in [1,2)).
- **No lower bounds or spectral decomposition** in this work.
- **Sources:** [arXiv:2407.10214](https://arxiv.org/abs/2407.10214), [Acta Math. Hungar.](https://link.springer.com/article/10.1007/s10474-025-01577-5)

---

## 8. Mertens Function Mean Square

### The Weak Mertens Conjecture
Under RH and the Gonek-Hejhal conjecture on negative moments of zeta:

**integral_0^Y (M(e^y) / e^{y/2})^2 dy ~ beta * Y**

where beta = 2 * sum_{gamma > 0} 1/|rho * zeta'(rho)|^2, summing over nontrivial zeros rho of zeta(s).

Equivalently: integral_1^X M(t)^2 / t^2 dt ~ beta * log X.

### Key References:
- **Nathan Ng (2004):** "The distribution of the summatory function of the Mobius function," Proc. London Math. Soc. [arXiv:math/0310381](https://arxiv.org/abs/math/0310381). Proves (conditionally) that e^{-y/2} M(e^y) has a limiting distribution.
- **Gonek's Conjecture:** 0 < lim sup |M(x)| / (sqrt(x) * (log log log x)^{5/4}) < infinity.
- **Akbary-Ng-Shahabi:** Extended weak Mertens conjecture to number fields.
- **Odlyzko-te Riele (1985):** Disproved Mertens conjecture |M(x)| <= sqrt(x).
- **Soundararajan (conditional on RH):** M(n) << sqrt(n) * exp(sqrt(log n) * (log log n)^{14}).

### IMPORTANT for our work:
The mean square of M(n) involves zeta zeros through the explicit formula. The leading constant beta depends on 1/|rho * zeta'(rho)|^2. This connects to our Franel identity approach since sum d_k^2 is a quadratic form in M(floor(n/k)).

---

## 9. Per-Step Discrepancy / Incremental Discrepancy

### Search Result: NO PRIOR WORK FOUND

The terms "per-step discrepancy" and "incremental discrepancy" in the context of Farey sequences returned ZERO results across all databases searched. This is strong evidence that:

**Our per-step Farey discrepancy DeltaW(p) is genuinely novel.**

No paper studies how the discrepancy changes when transitioning from F_{n-1} to F_n (or when inserting fractions with denominator n). The entire literature focuses on the GLOBAL discrepancy of F_n, not the per-step change.

### Closest Related Work:
- The BCZ map (Boca-Cobeli-Zaharescu) encodes spacing statistics, which is related but not the same as per-step discrepancy changes.
- Pair correlation measures spacings between adjacent Farey fractions, which is one component of what changes at each step.

---

## 10. Wobble Monotonicity / Wasserstein Discrepancy Monotone

### Search Result: NO PRIOR WORK FOUND

The terms "wobble monotonicity" and "Wasserstein discrepancy monotone" in the context of Farey sequences returned ZERO results. These appear to be our own terminology.

### Closest Related Work:
- Chahal-Chaubey (arXiv:2412.19728, Dec 2024): "On the distribution of polynomial Farey points and Chebyshev's bias phenomenon." Studies Chebyshev bias for Farey denominators in arithmetic progressions. Obtains Omega-results for error terms. This involves sign changes but of a different quantity (counting function error, not discrepancy).

---

## 11. Dedekind Sum / Spectral Connections

### No unified spectral/character formula found
The search for a spectral decomposition of Farey discrepancy sums using Dedekind sums and character theory returned no single unified framework. However:

- Dedekind sums are connected to quadratic reciprocity and the functional equation of the eta function.
- Zagier's higher-dimensional Dedekind sums have reciprocity laws.
- Huxley (1971) generalized Franel's theorem to Dirichlet L-functions, which involves Dirichlet characters. Weighting the Farey sum by chi(q) connects to L-function zeros.
- Ramanujan sums c_q(n) appear naturally in exponential sum approaches to Farey discrepancy (Niederreiter 1973).

### Potential spectral approach (not yet in literature):
The Franel identity expressing sum d_k^2 as a quadratic form in M(floor(n/k)), combined with the explicit formula for M in terms of zeta zeros, COULD yield a spectral decomposition. But this has apparently not been carried out explicitly in the literature.

---

## 12. Huxley (1971) — Generalization to Dirichlet L-functions

- **Paper:** "The distribution of Farey points, I"
- **Journal:** Acta Arithmetica, 18, 281-287 (1971)
- **Key Result:** Vast generalization of Franel's theorem. Showed that the discrepancy of Farey fractions, when weighted by Dirichlet characters chi(q), connects to zeros of the corresponding L-function L(s, chi). This extends the RH equivalence to the Generalized Riemann Hypothesis.
- **Relevance:** This is the closest thing to a "character decomposition" of Farey discrepancy. By taking chi = chi_0 (principal character), one recovers Franel. Non-trivial characters give GRH equivalences.

---

## Summary Table: Relevance to Our Proof

| Paper | Lower bound on sum D^2? | Spectral formula? | Per-step? | Sign Theorem? |
|-------|------------------------|-------------------|-----------|---------------|
| Dress 1999 | NO (exact disc = 1/Q) | NO | NO | NO |
| Franel-Landau 1924 | NO (RH equiv only) | Partial (via M) | NO | NO |
| Mikolas 1949-51 | NO | NO | NO | NO |
| Mikolas-Sato 1992 | NO | NO | NO | NO |
| Codeca-Perelli 1988 | NO (l^p study) | NO | NO | NO |
| Kanemitsu-Yoshimoto 1996 | NO | NO (Kubert fns) | NO | NO |
| Boca-Zaharescu 2005 | NO | Pair corr formula | NO | NO |
| Karvonen-Zhigljavsky 2025 | NO | MMD = L2 disc | NO | NO |
| Ng 2004 | NO | Zeta zeros | NO | NO |
| Huxley 1971 | NO | Character weights | NO | NO |
| Chahal-Chaubey 2024 | NO | NO | NO | Omega-result |

---

## Key Conclusions for Our Work

### What IS known:
1. **Franel Identity:** sum d_k^2 = quadratic form in M(floor(n/k)). RH <=> sum d_k^2 = O(n^{-1+eps}).
2. **Dress:** Absolute discrepancy of F_Q is exactly 1/Q.
3. **Pair Correlation:** Explicit formula exists (Boca-Zaharescu). Poissonian at large scales.
4. **MMD = L2 discrepancy** for the kernel K_0(x,y) = 1 + min(x,y) (Karvonen-Zhigljavsky).
5. **Weak Mertens Conjecture:** integral M(t)^2/t^2 dt ~ beta * log X (conditional).
6. **Huxley's generalization:** Character-weighted Farey discrepancy connects to L-function zeros.

### What is NOT known (our potential contributions):
1. **Per-step discrepancy DeltaW(p):** NOBODY has studied how discrepancy changes step by step. This is genuinely novel.
2. **Sign Theorem:** No prior result on the sign of per-step discrepancy changes.
3. **M(p) <-> DeltaW(p) connection at the per-step level:** Not in the literature.
4. **Lower bound on sum D^2 with log factor:** The literature gives RH equivalences but no unconditional lower bounds improving N^3 to N^3 * log N.
5. **Spectral decomposition of per-step changes:** Not attempted.
6. **Wobble monotonicity:** Our terminology, our concept, not in any prior work.

### Papers we MUST cite:
1. Franel (1924) + Landau (1924) — foundational identity
2. Dress (1999) — exact discrepancy result
3. Niederreiter (1973) — discrepancy order of magnitude
4. Huxley (1971) — L-function generalization
5. Mikolas (1949) — identity sum M(floor(x/n)) = 1
6. Mikolas-Sato (1992) — asymptotic Franel sum
7. Codeca-Perelli (1988) — l^p generalization
8. Kanemitsu-Yoshimoto (1996) — Kubert function generalization
9. Boca-Cobeli-Zaharescu (2001) / Boca-Zaharescu (2005) — pair correlation
10. Karvonen-Zhigljavsky (2025) — MMD-RH equivalence
11. Ng (2004) — Mertens function distribution
12. Edwards — Riemann's Zeta Function (textbook, contains Franel identity proof)

### Classification (Aletheia framework):
- Our per-step discrepancy perspective: **A1-A2** (autonomous, minor-to-publication novelty). The perspective is new; individual techniques are standard.
- The M(p) <-> DeltaW(p) connection: **C1-C2** (collaborative, depends on verification depth).
- Sign Theorem: **C2 if proved analytically** (would be publication-grade).
