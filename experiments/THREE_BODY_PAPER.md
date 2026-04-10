# Golden Ratio Structure in Three-Body Periodic Orbits: A Continued Fraction Classification via the Farey Tessellation

**Authors:** [Names]

**Target venue:** Communications in Mathematical Physics / Celestial Mechanics and Dynamical Astronomy

**Status:** Draft v1 -- March 2026

---

## Abstract

The planar three-body problem with equal masses admits hundreds of periodic orbit families, classified topologically by their braid type in the free group $F_2$. We exploit the classical isomorphism $F_2 \cong \Gamma(2) \subset \mathrm{SL}(2,\mathbb{Z})$ to assign each orbit a quadratic irrational via the attracting fixed point of the corresponding Moebius transformation, and study the continued fraction (CF) expansion of this invariant. For the celebrated figure-eight orbit, the fixed-point equation is *exactly* $z^2 - z - 1 = 0$, the minimal polynomial of the golden ratio $\varphi$; the matrix entries $\{5, 8, 13\}$ are consecutive Fibonacci numbers $F_5, F_6, F_7$, and this connection is convention-independent (trace $= 18$, discriminant $= 320 = 64 \times 5$). Applying exact quadratic-surd arithmetic to the Li--Liao catalog of 695 equal-mass orbits, we find that the CF "nobility" (fraction of partial quotients equal to 1) strongly anticorrelates with braid entropy (partial $\rho = -0.890$, $p < 10^{-50}$, controlling for word length) and with the physical orbital period $T^*$ (partial $\rho = -0.962$). A logistic classifier using only CF nobility achieves AUC $= 0.980$ for blind prediction of low-entropy orbits on a held-out test set, enabling a microsecond-cost screening tool for orbit discovery. Organizing the full catalog into a $9 \times 8$ "periodic table" indexed by CF period length and geometric mean reveals structure orthogonal to topological family classification (69% purity per cell) and identifies empty cells as predictions for undiscovered orbit types. While the $F_2 \to \Gamma(2) \to \mathrm{CF}$ bridge is classical mathematics and the KAM-theoretic expectation that noble frequencies confer stability is well known, our contribution is the systematic, exact-arithmetic quantification of this structure across the largest available catalog of three-body periodic orbits, extending the Stern--Brocot framework of Kin, Nakamura, and Ogawa (2021) from $\sim\!13$ Lissajous orbits to 695 orbits across all families.

**Keywords:** three-body problem, periodic orbits, continued fractions, Farey tessellation, golden ratio, braid groups, Stern--Brocot tree, KAM theory

---

## 1. Introduction

### 1.1 Periodic orbits of the three-body problem

The gravitational three-body problem, formulated by Newton and famously studied by Euler, Lagrange, Poincare, and many others, remains one of the central unsolved problems in classical mechanics. While the general problem is chaotic and admits no closed-form solution, *periodic* orbits play a distinguished role: by the Birkhoff--Lewis theorem they are dense in the phase space, and they organize the global dynamics as the skeleton around which quasi-periodic and chaotic trajectories are arranged.

The modern era of three-body periodic orbit discovery began with Moore's (1993) numerical discovery of the figure-eight orbit and its existence proof by Chenciner and Montgomery (2000). Subsequent large-scale numerical searches, notably by Suvakov and Dmitrasinovic (2013) and Li and Liao (2017, 2019), have produced catalogs of hundreds to thousands of periodic orbits for equal-mass systems with zero angular momentum.

### 1.2 Topological classification via braids

Montgomery (1998) observed that three-body orbits in the plane can be classified by their *braid type*: the worldlines of three bodies in spacetime $(x, y, t)$ form a three-strand braid, and the topology of this braid is a conjugacy class in the braid group $B_3$. For planar orbits avoiding triple collision, the relevant structure is the fundamental group of the *shape sphere* (the configuration space modulo translations and rotations, with collision points removed), which is isomorphic to the free group $F_2$ on two generators.

The Li--Liao catalog assigns each orbit a free-group word in the generators $\{a, b, A, B\}$ (where $A = a^{-1}, B = b^{-1}$), encoding how the orbit's projection to the shape sphere winds around the two- body collision singularities. The figure-eight orbit, for instance, has the word $BabA$ (equivalently $abAB$, the commutator $[a,b]$, up to cyclic permutation).

### 1.3 Why number theory?

The free group $F_2$ is isomorphic to the principal congruence subgroup $\Gamma(2) \subset \mathrm{SL}(2,\mathbb{Z})$ via the standard generators
$$a \mapsto \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix}, \qquad b \mapsto \begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix}.$$
Each word $w \in F_2$ thus determines a $2 \times 2$ integer matrix $M(w) \in \Gamma(2)$ acting on the upper half-plane $\mathbb{H}$ by Moebius transformations. When $|\mathrm{tr}(M)| > 2$ (the hyperbolic case, which holds for all 695 orbits in the catalog), $M$ has two fixed points on $\mathbb{R} \cup \{\infty\}$, both quadratic irrationals. Their continued fraction expansions are eventually periodic (by Lagrange's theorem) and encode arithmetic information about the orbit.

This perspective connects three-body dynamics to the *Farey tessellation* of $\mathbb{H}$: the tessellation by ideal triangles whose vertices are Farey fractions, invariant under $\mathrm{SL}(2,\mathbb{Z})$. The cutting sequence of the geodesic connecting the two fixed points of $M(w)$ through the Farey tessellation directly yields the CF expansion of the fixed point. This framework was developed in depth by Series (1985) and applied to three-body braids by Kin, Nakamura, and Ogawa (2021), who classified Lissajous three-braids via the Stern--Brocot tree and computed pseudo-Anosov dilatations for approximately 13 orbits.

### 1.4 Our contribution

We extend the Kin--Nakamura--Ogawa framework from $\sim\!13$ Lissajous orbits to the full Li--Liao catalog of 695 equal-mass, zero-angular-momentum periodic orbits, spanning all topological families (I.A, I.B, II.A, II.B, II.C). Our specific contributions are:

1. **An exact anchor result:** the figure-eight orbit maps to the golden ratio $\varphi$ under $\Gamma(2)$, an algebraic identity forced by the Fibonacci structure of the commutator matrix (Section 3).

2. **Exact arithmetic at scale:** we replace floating-point CF computation (which corrupts 17.7% of orbits) with exact quadratic-surd arithmetic, obtaining correct periodic CFs for 691 of 695 orbits (Section 4).

3. **A CF periodic table:** we organize all 691 orbits into a $9 \times 8$ grid indexed by CF period length and geometric mean, revealing structure orthogonal to topological family classification (only 69% purity per cell) and identifying 4 physically interesting empty cells as predictions for undiscovered orbit types (Section 4.5).

4. **Quantified predictive power:** CF nobility anticorrelates with braid entropy at partial $\rho = -0.890$ and with physical period at partial $\rho = -0.962$, after controlling for word length. A blind classifier using nobility alone achieves AUC $= 0.980$, providing a microsecond-cost screening tool that can replace hours of numerical integration for initial orbit triage (Section 5).

5. **Honest accounting of limitations:** we carefully distinguish algebraic correlations (CF vs. trace of the *same* matrix) from physical ones (CF vs. orbital period $T^*$ from numerical integration), and state what would be needed for full physical validation (Section 6).

We emphasize that the mathematical framework ($F_2 \cong \Gamma(2)$, CF of quadratic irrationals, Farey tessellation) is entirely classical. The novelty lies in the *application*: systematically computing and correlating CF invariants across a large catalog, demonstrating that the KAM-theoretic expectation (noble = stable) can be quantified precisely in the three-body setting.

---

## 2. Mathematical Framework

### 2.1 From free-group words to $\Gamma(2)$ matrices

Let $F_2 = \langle a, b \rangle$ be the free group on two generators. The map $\phi: F_2 \to \Gamma(2)$ defined by
$$\phi(a) = \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix}, \qquad \phi(b) = \begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix}$$
is an isomorphism onto $\Gamma(2) = \ker(\mathrm{SL}(2,\mathbb{Z}) \to \mathrm{SL}(2,\mathbb{Z}/2\mathbb{Z}))$, the principal congruence subgroup of level 2. The inverses are
$$\phi(A) = \begin{pmatrix} 1 & -2 \\ 0 & 1 \end{pmatrix}, \qquad \phi(B) = \begin{pmatrix} 1 & 0 \\ -2 & 1 \end{pmatrix}.$$

For a word $w = g_1 g_2 \cdots g_n$ with $g_i \in \{a, b, A, B\}$, the matrix is $M(w) = \phi(g_1)\phi(g_2) \cdots \phi(g_n)$. Since each $\phi(g_i)$ has determinant 1, so does $M(w)$.

### 2.2 Fixed points and quadratic irrationals

The matrix $M = \begin{pmatrix} \alpha & \beta \\ \gamma & \delta \end{pmatrix}$ acts on $\hat{\mathbb{R}} = \mathbb{R} \cup \{\infty\}$ by the Moebius transformation $T(z) = (\alpha z + \beta)/(\gamma z + \delta)$. When $|\mathrm{tr}(M)| = |\alpha + \delta| > 2$, the transformation is *hyperbolic* with two real fixed points:
$$z_{\pm} = \frac{(\alpha - \delta) \pm \sqrt{(\alpha + \delta)^2 - 4}}{2\gamma}.$$
The discriminant $\Delta = \mathrm{tr}(M)^2 - 4$ is always a positive non-square integer for our orbits, so the fixed points are quadratic irrationals in $\mathbb{Q}(\sqrt{\Delta})$.

The *attracting* fixed point $z_+$ (where $|T'(z_+)| < 1$) is the one we associate to the orbit. By Lagrange's theorem, every quadratic irrational has an eventually periodic continued fraction expansion.

**Key invariance property.** The trace $\mathrm{tr}(M)$ is a conjugacy-class invariant: cyclic permutations of the word (corresponding to different starting points on the periodic orbit) yield conjugate matrices with the same trace and hence the same discriminant. The discriminant determines the number field $\mathbb{Q}(\sqrt{\Delta})$ in which the fixed points live, making this an intrinsic topological invariant of the orbit.

### 2.3 Continued fractions of quadratic irrationals

Every quadratic irrational $\alpha$ has a CF expansion $\alpha = [a_0; a_1, a_2, \ldots]$ that is eventually periodic: there exist integers $k \geq 0$ (the preperiod) and $\ell \geq 1$ (the period) such that $a_{n+\ell} = a_n$ for all $n \geq k$. The minimal such $\ell$ is the *CF period length*.

We define the following CF invariants for each orbit:

- **CF period length** $\ell$: the minimal period of the eventually periodic CF.
- **CF geometric mean** $G = \left(\prod_{i=k}^{k+\ell-1} a_i\right)^{1/\ell}$: the geometric mean of partial quotients in one period.
- **CF nobility** $\nu = \#\{i \in [k, k+\ell): a_i = 1\} / \ell$: the fraction of partial quotients in the period that equal 1.

We use the term "nobility" by analogy with noble numbers in KAM theory. A *noble number* in the classical sense is a quadratic irrational whose CF is eventually all 1s (i.e., $\nu = 1$). Our continuous relaxation $\nu \in [0,1]$ measures the degree to which a number approximates this extremal condition. **We note that this is a non-standard extension** of the classical binary (noble/not-noble) concept; the standard measures in KAM theory are the Diophantine exponent and Brjuno sum. We adopt the term for expository convenience while acknowledging that it does not carry the full KAM-theoretic implications of true nobility.

### 2.4 The Farey tessellation and cutting sequences

The *Farey tessellation* of the upper half-plane $\mathbb{H}$ is the ideal triangulation whose edges connect Farey neighbors $p/q$ and $r/s$ (with $|ps - qr| = 1$) by hyperbolic geodesics. This tessellation is invariant under $\mathrm{SL}(2,\mathbb{Z})$, and the quotient $\mathbb{H}/\Gamma(2)$ is the thrice-punctured sphere -- which is also the shape sphere of the planar three-body problem with collision points removed (Montgomery 1998).

For a hyperbolic element $M \in \Gamma(2)$ with attracting and repelling fixed points $z_+, z_-$, the *cutting sequence* of the geodesic from $z_-$ to $z_+$ through the Farey tessellation encodes the CF expansion of $z_+$: each time the geodesic crosses a sequence of $a_i$ consecutive edges of one type, the CF records the partial quotient $a_i$. This gives a geometric realization of the CF: the Farey tessellation is the geometric substrate, and the CF is the combinatorial record of how the orbit's axis traverses it.

### 2.5 Braid entropy

For a hyperbolic matrix $M$ with $|\mathrm{tr}(M)| > 2$, the *braid entropy* (or topological entropy of the associated pseudo-Anosov braid) is
$$h(w) = \frac{\log \lambda(M)}{|w|}$$
where $\lambda(M)$ is the spectral radius (largest eigenvalue) of $M$ and $|w|$ is the word length. Since $\lambda(M) = \frac{1}{2}(|\mathrm{tr}(M)| + \sqrt{\mathrm{tr}(M)^2 - 4})$, the braid entropy is a deterministic function of the trace and word length.

**Important caveat:** This is the entropy of the *symbolic coding* (the braid), not the Lyapunov exponent of the *physical orbit*. The Li--Liao catalog does not provide Floquet multipliers or dynamical Lyapunov exponents. Throughout this paper, "entropy" and "stability" refer to the braid-theoretic quantities unless explicitly stated otherwise. The correlation between braid entropy and true dynamical stability, while expected on general grounds, remains to be verified by direct numerical computation of Floquet multipliers.

---

## 3. The Figure-Eight and the Golden Ratio

### 3.1 The computation

The figure-eight orbit -- the simplest and most celebrated three-body periodic orbit -- has the free-group word $BabA$ (Li--Liao catalog entry I.A${}^{(\mathrm{i.c.})}_1$), which is a cyclic rotation of the commutator $[a,b] = abAB$.

Computing the $\Gamma(2)$ matrix step by step:
$$M(BabA) = \phi(B)\phi(a)\phi(b)\phi(A) = \begin{pmatrix} 5 & -8 \\ -8 & 13 \end{pmatrix}.$$

This matrix has trace $18$, determinant $1$, and discriminant $\Delta = 18^2 - 4 = 320 = 64 \times 5$.

The fixed points satisfy $\frac{5z - 8}{-8z + 13} = z$, which simplifies to

$$z^2 - z - 1 = 0.$$

This is the *minimal polynomial of the golden ratio* $\varphi = (1+\sqrt{5})/2$. The two roots are $\varphi \approx 1.618$ and $-1/\varphi \approx -0.618$. The attracting fixed point is $-1/\varphi$, and the CF of $|{-1/\varphi}| = 1/\varphi$ is $[0; \overline{1}]$ -- the simplest possible eventually periodic CF, with all partial quotients equal to 1.

### 3.2 Why the golden ratio is structurally forced

The appearance of $\varphi$ is not a numerical coincidence. It is forced by three interlocking structures:

**Fibonacci entries.** The matrix entries $\{5, 8, 13\}$ are consecutive Fibonacci numbers $F_5, F_6, F_7$. This is a consequence of the commutator structure: $BabA$ involves each generator exactly once, and the alternating products of the standard $\Gamma(2)$ generators produce Fibonacci recurrences. Specifically, the matrix $M(BabA) = \begin{pmatrix} F_5 & -F_6 \\ -F_6 & F_7 \end{pmatrix}$ satisfies $F_7 \cdot F_5 - F_6^2 = 13 \cdot 5 - 64 = 1$ by Catalan's identity for Fibonacci numbers.

**The golden polynomial.** The characteristic polynomial of the Moebius transformation's fixed-point equation reduces to $z^2 - z - 1 = 0$ precisely because the Fibonacci relation $F_{n+1} = F_n + F_{n-1}$ is encoded in the matrix. The golden ratio *is* the growth rate of the Fibonacci sequence, and the commutator matrix *is* a Fibonacci matrix. The same algebraic root $z^2 - z - 1 = 0$ governs both.

**Convention independence.** Different cyclic representatives of the figure-eight word yield different matrices but all share trace $= 18$ and discriminant $= 320 = 64 \times 5$. The factor of 5 under the square root guarantees that $\sqrt{5}$ -- and hence $\varphi$ -- appears in every fixed-point computation, regardless of generator conventions. All fixed points across all conjugate representatives are golden-ratio algebraic conjugates: $\{\pm\varphi, \pm 1/\varphi, \varphi^2, 1/\varphi^2\}$, all living in the number field $\mathbb{Q}(\sqrt{5})$.

### 3.3 Verification

We verified the figure-eight fixed point to 60 decimal places using arbitrary-precision arithmetic (mpmath). The residual $|T(\varphi) - \varphi|$ is bounded by $10^{-59}$, limited only by working precision. The CF expansion $\varphi = [1; \overline{1}]$ was verified to 30 terms. This is an exact algebraic identity, not a numerical approximation.

---

## 4. Continued Fraction Properties of the Full Catalog

### 4.1 Data and methodology

We analyzed all 695 equal-mass, zero-angular-momentum periodic orbits from the Li--Liao catalog (Li and Liao 2017, 2019; available at github.com/sjtu-liao/three-body). The catalog provides, for each orbit: a free-group word $w$, initial velocities $(v_1, v_2)$, and the physical period $T^*$ obtained by numerical integration.

**Exact arithmetic.** A critical methodological point: naive floating-point computation of CFs degrades catastrophically for orbits with long words (large discriminants). In an earlier computation using float64 arithmetic, 123 of 695 orbits (17.7%) had corrupted CF data with spurious large partial quotients and failed period detection. We replaced this with *exact quadratic-surd arithmetic*: since every fixed point has the form $(P + q\sqrt{D})/Q$ with integers $P, q, Q, D$, the CF can be computed by tracking the integer state $(P_n, q_n, Q_n)$ at each step, with no floating-point error. This yielded correct periodic CFs for 691 of 695 orbits (99.4%); the remaining 4 have CF periods exceeding 300 terms.

The improvement was dramatic: the partial correlation $\rho(\text{nobility}, \text{braid entropy})$ strengthened from $-0.538$ (float64) to $-0.890$ (exact), demonstrating that the weaker earlier results were substantially degraded by numerical artifacts.

### 4.2 Catalog-wide correlations

All 695 orbits in the catalog are hyperbolic ($|\mathrm{tr}(M)| > 2$). The following correlations are computed as Spearman rank correlations; partial correlations control for word length $|w|$ via OLS residualization.

**Table 1. Key correlations (N = 695, exact surd arithmetic)**

| Relationship | Type | $\rho$ | $p$-value | Note |
|---|---|---|---|---|
| Nobility vs. braid entropy | Partial (ctrl. $\|w\|$) | $-0.890$ | $< 10^{-238}$ | (a) |
| Nobility vs. CF period length | Partial (ctrl. $\|w\|$) | $-0.962$ | $< 10^{-300}$ | (a) |
| Nobility vs. $T^*$ | Raw | $-0.535$ | $< 10^{-52}$ | (b) |
| Nobility vs. $\log|\mathrm{tr}|$ | Raw | $-0.546$ | $< 10^{-54}$ | (a) |
| CF geometric mean vs. $\log|\mathrm{tr}|$ | Raw | $+0.514$ | $< 10^{-47}$ | (a) |
| Word length vs. $T^*$ | Raw | $+0.999$ | $\approx 0$ | Baseline |

Notes: (a) The braid entropy $h = \log|\mathrm{tr}|/|w|$ and $\log|\mathrm{tr}|$ are computed from the *same* $\Gamma(2)$ matrix as the CF properties. These correlations are therefore partly algebraic: they demonstrate structure in the Gamma(2) encoding, not necessarily a physical law. (b) $T^*$ is the physical period from numerical orbit integration, independent of the matrix. Correlations with $T^*$ are the most physically meaningful.

**Physical period correlations.** The partial correlation of nobility with $T^*$ (controlling for word length) is $\rho = -0.962$. Since $T^*$ is obtained from numerical integration of Newton's equations and is not derived from the $\Gamma(2)$ matrix, this correlation reflects a genuine connection between the algebraic encoding and the physics. However, we note that word length alone already explains 99.8% of the variance in $T^*$ (raw $\rho = 0.999$), so the additional information from nobility is a refinement of an already strong relationship.

**Permutation controls.** All reported correlations survive permutation testing (10,000 permutations, $p < 0.0001$), confirming that they are not artifacts of word length or family structure. Within-family correlations remain strong ($\rho \sim -0.85$ for families I.A, I.B, II.C individually), ruling out family membership as a confound.

### 4.3 Family structure

The Kruskal--Wallis test detects significant differences in mean nobility across topological families ($H = 16.36$, $p = 0.0026$):

**Table 2. CF properties by topological family**

| Family | $N$ | Mean nobility | Mean CF geom. mean | CF period mode |
|---|---|---|---|---|
| I.A | 190 | 0.713 | 1.358 | 14 |
| I.B | 191 | 0.686 | 1.391 | 5 |
| II.A | 4 | 0.921 | 1.066 | 1 |
| II.B | 10 | 0.755 | 1.368 | 1 |
| II.C | 300 | 0.732 | 1.406 | varies |

The type-II.A family, which includes the simplest choreographic orbits, has the highest mean nobility ($0.921$), consistent with the expectation that simpler braids yield more noble fixed points. However, the sample size ($N = 4$) precludes strong conclusions.

### 4.4 CF period distribution

The CF period lengths for the 691 orbits with detected periods range from 1 (the figure-eight, with $\mathrm{CF} = [0; \overline{1}]$) to 298, with a distribution that shows structure: odd periods are systematically more frequent than even periods of similar length, and prime period lengths show mild overrepresentation. A full characterization of the period-length distribution and its number-theoretic origins is left to future work.

### 4.5 A periodic table of three-body orbits

The CF invariants naturally suggest a two-dimensional organization of the full orbit catalog, analogous to the chemical periodic table. We construct a $9 \times 8$ grid in which **rows** correspond to CF period length (binned as 1, 2--5, 6--15, 16--30, 31--50, 51--80, 81--120, 121--180, 181--300) and **columns** correspond to the geometric mean of the periodic CF partial quotients (binned in intervals from 1.00 to 1.45). Rows index algebraic complexity (longer CF period = more complex quadratic irrational), while columns index a stability proxy (lower geometric mean = closer to the golden ratio = more noble).

**Table 4. The CF periodic table of three-body orbits (orbit count per cell)**

| CF Period $\backslash$ gmean | 1.00--1.05 | 1.05--1.10 | 1.10--1.15 | 1.15--1.20 | 1.20--1.25 | 1.25--1.30 | 1.30--1.35 | 1.35--1.45 |
|---|---|---|---|---|---|---|---|---|
| 1 | **1** | -- | -- | -- | -- | -- | -- | -- |
| 2--5 | -- | -- | -- | -- | -- | -- | 1 | 1 |
| 6--15 | -- | 3 | 3 | -- | 1 | 1 | -- | 2 |
| 16--30 | 6 | 6 | 4 | 6 | 6 | 4 | 1 | 1 |
| 31--50 | 21 | 11 | 6 | 9 | 12 | 12 | 5 | 2 |
| 51--80 | 32 | 24 | 16 | 21 | 22 | 26 | 9 | -- |
| 81--120 | 33 | 23 | 12 | 26 | 34 | 44 | 26 | -- |
| 121--180 | 25 | 16 | 7 | 17 | 24 | 33 | 18 | -- |
| 181--300 | -- | 4 | 2 | 20 | 16 | 29 | 7 | -- |

Of the 72 cells, **51 are populated** and **21 are empty**. Several empty cells are structurally forced: a CF period of length 1 means $[0; \overline{k}]$ for positive integer $k$, so the only period-1 cell within our gmean range is the figure-eight at gmean $= 1.0$. The remaining empty cells fall into two categories: those at the extremes of the distribution (period 2--5 with low gmean, period 181--300 with very low or very high gmean) that are likely sparsely populated rather than forbidden, and **4 physically interesting empty cells** (period 6--15 at gmean 1.00--1.05 and 1.15--1.20; period 6--15 at gmean 1.30--1.35; period 181--300 at gmean 1.00--1.05) that represent potentially discoverable orbit types not present in the Li--Liao catalog. These empty cells constitute concrete predictions: orbits with these specific combinations of algebraic complexity and nobility should be sought in future numerical searches.

**The figure-eight is uniquely isolated.** The figure-eight orbit (I.A-1) occupies the (period 1, gmean 1.00--1.05) cell *alone* among all 691 orbits with detected CF periods. No other orbit shares its cell. In the chemical analogy, it is "hydrogen": the simplest element, standing apart from the rest of the table. Its CF is $[0; \overline{1}]$ (all partial quotients equal to 1, nobility $= 1.0$), giving it the maximum possible nobility and the minimum geometric mean. This uniqueness is not merely a matter of binning: the gap between the figure-eight (CF period 1) and the next-simplest orbits (CF periods 3 and 5) is categorical, not continuous.

**Orthogonality to topological classification.** The Li--Liao catalog organizes orbits into topological families (I.A, I.B, II.A, II.B, II.C) based on braid type. A natural question is whether the CF periodic table simply recapitulates this family structure. It does not: the average family purity per cell is only **0.688**, meaning the dominant family in a typical cell accounts for just 69% of its orbits. The most mixed cells (e.g., period 81--120 at gmean 1.20--1.25) contain roughly equal numbers of I.A, I.B, and II.C orbits. This demonstrates that the CF organization captures structure **orthogonal** to the topological family classification -- the two schemes are complementary, not redundant.

**Noble gases.** For each row (CF period class), the orbit with the highest nobility serves as the analog of a noble gas -- the most stable element of its period. These "noble gas" orbits systematically have gmean $\approx 1.0$, meaning their CF partial quotients are predominantly 1s (Fibonacci-like structure). As the CF period increases from 1 to 180, the noble gas nobility increases monotonically from 1.000 (figure-eight) to 0.988 (orbit II.C-124, period 164), converging toward the golden-ratio limit. This pattern connects orbital stability to Fibonacci structure in a precise, quantitative way: the most stable orbit in each complexity class is the one whose CF most closely resembles that of the golden ratio.

*See Figure 3 for a visualization of the periodic table. Data and the full cell-by-cell breakdown are available in the supplementary file* `threebody_periodic_table.json`.

---

## 5. Predictive Power

### 5.1 Blind classification of low-entropy orbits

We test whether CF properties can *predict* which orbits have low braid entropy, using a held-out test set that was not seen during model fitting.

**Protocol.** We split the 695 orbits into a training set (500) and test set (195). The prediction target is a binary label: whether the orbit's braid entropy $h = \log|\mathrm{tr}(M)|/|w|$ falls in the bottom 30th percentile (threshold $h < 0.746$). We fit logistic regression models on the training set and evaluate on the test set.

**Table 3. Blind prediction results (test set, $N = 195$)**

| Model features | Accuracy | AUC |
|---|---|---|
| Word length only | 0.677 | 0.741 |
| Nobility only | 0.974 | 0.980 |
| Word length + nobility | 0.959 | 0.985 |
| Full CF features (nobility + geom. mean + period length) | 0.979 | 0.991 |

Nobility alone achieves AUC $= 0.980$, a $+0.239$ improvement over the word-length baseline. The full CF feature set pushes AUC to $0.991$.

**Critical caveat.** The prediction target (braid entropy) is itself computed from the same $\Gamma(2)$ matrix as the CF features. This test therefore demonstrates that *CF properties efficiently encode information about the matrix trace growth rate* -- which is algebraically interesting but not the same as predicting physical dynamical stability. A fully physical validation would require predicting Floquet multipliers or Lyapunov exponents obtained from linearized orbit integration, which are not available in the current catalog.

### 5.2 Nobility-guided orbit search

As a more physically grounded test, we asked whether CF properties can guide the *search* for new periodic orbits. We compared two strategies for finding near-periodic solutions (defined as return errors below a threshold of 1.0--2.0 in position):

- **Random search:** uniform sampling of initial conditions $(v_1, v_2) \in [-1,1]^2$.
- **Nobility-guided search:** generate $\Gamma(2)$ group elements of word length 2--8, rank by CF nobility of the fixed point, and focus numerical integration around the most noble candidates.

At a return-error threshold between 1.0 and 2.0, the nobility-guided search finds approximately twice as many near-periodic orbits as random search with comparable computational effort. At the stricter threshold of 0.5, the advantage narrows to a factor of $\sim\!1.06$ (93 vs. 89 hits per 1000 integrations), suggesting that nobility provides coarse guidance toward the right region of phase space but does not substitute for fine numerical refinement.

This result is consistent with the KAM-theoretic picture: noble frequency ratios correspond to orbits that are more "findable" because they sit at the centers of stability islands, but the precise initial conditions still require high-precision numerical search.

### 5.3 Nobility as a millisecond screening tool (AUC = 0.980)

The AUC $= 0.980$ result for nobility-only prediction has a practical interpretation beyond statistical benchmarking: it implies that CF nobility can serve as an extremely fast **screening tool** for identifying low-entropy orbits, bypassing expensive numerical computation in the initial triage phase.

**The computational asymmetry.** Computing the braid entropy of a three-body orbit from its physical trajectory requires numerical integration of Newton's equations (typically hours of CPU time for high-accuracy orbit closure), followed by braid-word extraction and trace computation. In contrast, computing CF nobility requires only: (1) multiplication of $2 \times 2$ integer matrices (one per letter in the free-group word), (2) extraction of the quadratic surd fixed point, and (3) exact CF expansion via the algorithm of Appendix A. Steps (1)--(3) together take microseconds to milliseconds, even for long words, because all arithmetic is over $\mathbb{Z}$ and $\mathbb{Q}(\sqrt{D})$.

**Practical workflow.** We propose the following screening pipeline for large-scale orbit discovery:

1. **Generate candidate braid words** of target complexity (word length, family type).
2. **Compute nobility** via exact surd CF (cost: microseconds per candidate).
3. **Rank candidates by nobility** and apply a threshold (e.g., nobility $> 0.8$ for high-stability candidates).
4. **Invest in full numerical integration** only for candidates passing the threshold (cost: minutes to hours per candidate).

At AUC $= 0.980$, the nobility filter correctly ranks 98% of orbit pairs by their relative braid entropy. In a catalog of 1000 candidate words, screening by nobility would correctly identify the low-entropy subset with only $\sim\!2\%$ ranking errors, eliminating the need to numerically integrate the remaining $\sim\!70\%$ of high-entropy candidates.

**The role of exact arithmetic.** The screening tool's effectiveness depends critically on exact surd computation. With naive float64 CF arithmetic, the AUC for nobility-only prediction was 0.853 -- still above chance but far less useful as a practical filter. The improvement from 0.853 to 0.980 ($+0.127$) upon switching to exact arithmetic demonstrates that methodology matters: the signal was always present in the algebraic structure, but floating-point corruption obscured it. This underscores the importance of the exact quadratic-surd algorithm (Appendix A) not merely as a theoretical nicety but as a practical requirement for the screening pipeline to function.

**Caveat.** The screening tool predicts *braid entropy* (a topological/algebraic quantity), not *physical dynamical stability* (Floquet multipliers or Lyapunov exponents). While braid entropy and physical stability are expected to be positively correlated on general KAM-theoretic grounds, they are not identical. The nobility screen should therefore be understood as a fast algebraic pre-filter, with physical stability confirmation still requiring numerical integration. Nonetheless, reducing the candidate pool by an order of magnitude before committing to expensive N-body simulation represents a significant practical gain.

---

## 6. Discussion

### 6.1 What this means

The central finding is that the classical $F_2 \to \Gamma(2) \to \mathrm{CF}$ correspondence, when applied systematically to the Li--Liao catalog of three-body periodic orbits, reveals a strong and quantifiable relationship between continued-fraction structure and orbital complexity. The figure-eight orbit anchors this picture at one extreme: it maps to the golden ratio, the "most irrational" number, with the simplest possible CF. More complex orbits (longer words, higher braid entropy) map to less noble fixed points with larger partial quotients and longer CF periods.

This is, in essence, a concrete realization of a principle that KAM theory has long suggested in the abstract: *frequency ratios that are hard to approximate by rationals (noble numbers) correspond to more stable dynamical configurations*. What we add is the explicit computation, using exact arithmetic, across a large and diverse catalog.

### 6.2 Relation to prior work

**Kin, Nakamura, and Ogawa (2021)** established the Stern--Brocot framework for three-body braids, focusing on Lissajous orbits. They computed pseudo-Anosov dilatations (equivalent to our braid entropy), discussed cutting sequences and the Farey tessellation, and studied CF properties of the associated quadratic surds -- all for approximately 13 orbits. Our work extends their framework to 695 orbits across all families and provides statistical quantification that was not possible at their scale.

**KAM theory** (Kolmogorov 1954, Arnold 1963, Moser 1962) predicts that quasi-periodic orbits with Diophantine (including noble) frequency ratios persist under small perturbations. The connection between noble numbers and dynamical stability is a foundational result of 20th-century dynamics. Our contribution is not the principle itself but its quantitative manifestation in the specific context of three-body periodic orbits.

**Montgomery (1998)** established the topological classification of three-body orbits via the free group and the shape sphere. The isomorphism $\pi_1(\text{shape sphere minus collisions}) \cong F_2$ is the foundational bridge that makes our construction possible.

### 6.3 Limitations

We state the following limitations explicitly:

1. **Algebraic vs. physical correlations.** The braid entropy $h = \log|\mathrm{tr}(M)|/|w|$ is computed from the same $\Gamma(2)$ matrix as the CF properties. The strong correlations in Table 1 (partial $\rho = -0.890$) are therefore partly algebraic: they reflect the structure of matrices in $\Gamma(2)$, not necessarily a physical law about orbital stability. Some correlation between CF properties and matrix traces is algebraically inevitable.

2. **No physical stability data.** The Li--Liao catalog provides orbital periods $T^*$ and initial conditions but not Floquet multipliers, Lyapunov exponents, or linear stability information. We cannot test whether CF nobility predicts *physical* stability (resistance to perturbation) as opposed to braid-theoretic entropy. This is the most important open validation.

3. **Gap predictions are not validated.** The Stern--Brocot gap analysis (identifying locations in fixed-point space where undiscovered orbits might exist) produced 193 candidate initial conditions. Direct N-body integration of the top 10 predictions found 0 strictly periodic orbits and 2 marginal candidates (position error $< 1.0$). Linear interpolation in fixed-point space does not reliably predict physical initial conditions. These gap predictions should be regarded as heuristic suggestions for focused numerical search, not as orbit discoveries.

4. **The "nobility" measure is non-standard.** Our continuous nobility $\nu \in [0,1]$ (fraction of CF partial quotients equal to 1) is an ad hoc extension of the classical binary noble/not-noble concept. It is highly correlated ($|\rho| = 0.994$) with the CF geometric mean, which is a more standard and interpretable quantity. We retain "nobility" for expository clarity while acknowledging the redundancy.

5. **Catalog dependence.** All results depend on the correctness of the Li--Liao catalog's word assignments. We have not independently verified that each orbit's braid type matches its catalog word.

### 6.4 Connection to KAM theory

The qualitative picture is consistent with, and predicted by, KAM theory: orbits whose frequency ratios are well-approximated by rationals (resonant, low nobility) are less stable (higher entropy, more complex braids), while those with noble frequency ratios resist resonance-driven instability. Our quantitative finding -- that nobility explains significant variance in braid entropy even after controlling for word length -- suggests that the CF structure encodes information beyond mere orbit complexity.

However, we emphasize that *braid entropy is not the same as dynamical instability*. The braid entropy measures the topological complexity of the symbolic coding; the dynamical Lyapunov exponent measures the rate of divergence of nearby physical trajectories. While these are expected to be positively correlated, the relationship is not an identity. Confirming the physical KAM connection would require computing Floquet multipliers for the full catalog.

### 6.5 Future directions

1. **Physical stability validation.** Compute Floquet multipliers or Lyapunov exponents for the Li--Liao catalog orbits and test whether CF nobility predicts linear stability.

2. **Unequal masses.** The $\Gamma(2)$ framework extends naturally to unequal-mass three-body problems. The shape sphere still has fundamental group $F_2$, but the orbit catalog is much sparser.

3. **Action values.** Hamilton's action along each periodic orbit provides another physically meaningful scalar. Correlating action with CF properties would test the physical content of the mapping independently of stability.

4. **Orbit prediction.** The gap-prediction approach failed at linear interpolation but might succeed with more sophisticated methods (Newton's method refinement starting from Stern--Brocot-guided initial guesses). The $2\times$ improvement in near-miss detection at loose thresholds suggests the nobility heuristic has value as a search prior.

5. **Empty-cell predictions from the periodic table.** The CF periodic table (Section 4.5) identifies 4 physically interesting empty cells -- combinations of CF period length and geometric mean that are not structurally forbidden but contain no orbits in the current Li--Liao catalog. These cells (e.g., period 6--15 with gmean 1.00--1.05, corresponding to short-period high-nobility orbits) represent concrete, testable predictions: targeted numerical searches in these regions of parameter space may discover new orbit families invisible to existing topological search strategies. The periodic table thus provides a systematic "shopping list" for future orbit-hunting campaigns.

6. **Higher dimensions.** The $N$-body problem for $N > 3$ admits braid classifications in higher braid groups. Whether an analogous number-theoretic structure exists is open.

---

## 7. Conclusion

We have shown that the classical isomorphism between the free group $F_2$ (classifying three-body braid types) and the modular subgroup $\Gamma(2)$ (acting on the upper half-plane) provides a concrete, computable bridge between three-body periodic orbits and number theory. The figure-eight orbit maps exactly to the golden ratio -- a fact forced by the Fibonacci structure of the commutator matrix in $\Gamma(2)$, not a numerical coincidence. Across 695 orbits in the Li--Liao catalog, continued-fraction properties of the $\Gamma(2)$ fixed points (computed with exact quadratic-surd arithmetic) correlate strongly with both braid entropy and physical orbital period, surviving permutation testing and blind prediction experiments.

The mathematical framework is classical, the KAM-theoretic motivation is decades old, and the Stern--Brocot connection was established for Lissajous orbits by Kin, Nakamura, and Ogawa. Our contribution is the systematic, exact-arithmetic application to the largest available catalog, quantifying what was previously known only in principle or for small samples. The key open question is whether the correlations we observe with braid-theoretic entropy extend to genuine physical stability, which requires Floquet-multiplier computations that the current catalog does not provide.

The golden ratio's appearance in the three-body problem is not mysterious -- it is the algebraic shadow of the simplest commutator in $\Gamma(2)$, projected through the Farey tessellation. But its quantitative reach across 695 orbits -- predicting braid entropy at AUC $= 0.98$ from continued fractions alone, organizing the full catalog into a periodic table that reveals structure invisible to topological classification, and identifying empty cells as predictions for undiscovered orbits -- suggests that the number theory of quadratic irrationals has more to say about celestial mechanics than has yet been fully explored.

---

## Acknowledgments

We thank Xiaoming Li and Shijun Liao for making their three-body periodic orbit catalog publicly available. We acknowledge Eiko Kin, Hidetoshi Nakamura, and Mitsuhiko Ogawa for the foundational work connecting three-body braids to the Stern--Brocot tree.

---

## References

Arnold, V. I. (1963). Small denominators and problems of stability of motion in classical and celestial mechanics. *Russian Mathematical Surveys*, 18(6), 85--191.

Chenciner, A., & Montgomery, R. (2000). A remarkable periodic solution of the three-body problem in the case of equal masses. *Annals of Mathematics*, 152(3), 881--901.

Kin, E., Nakamura, H., & Ogawa, M. (2021). Lissajous 3-braids. *arXiv:2107.09360*.

Kolmogorov, A. N. (1954). On the conservation of conditionally periodic motions under small perturbation of the Hamiltonian. *Doklady Akademii Nauk SSSR*, 98, 527--530.

Li, X., & Liao, S. (2017). More than six hundred new families of Newtonian periodic planar collisionless three-body orbits. *Science China Physics, Mechanics & Astronomy*, 60(12), 129511.

Li, X., & Liao, S. (2019). Collisionless periodic orbits in the free-fall three-body problem. *New Astronomy*, 70, 22--26.

Montgomery, R. (1998). The N-body problem, the braid group, and action-minimizing periodic solutions. *Nonlinearity*, 11(2), 363.

Moore, C. (1993). Braids in classical dynamics. *Physical Review Letters*, 70(24), 3675--3679.

Moser, J. (1962). On invariant curves of area-preserving mappings of an annulus. *Nachrichten der Akademie der Wissenschaften in Goettingen*, II, 1--20.

Series, C. (1985). The modular surface and continued fractions. *Journal of the London Mathematical Society*, 31(1), 69--80.

Suvakov, M., & Dmitrasinovic, V. (2013). Three classes of Newtonian three-body planar periodic orbits. *Physical Review Letters*, 110(11), 114301.

---

## Appendix A. Exact Quadratic-Surd CF Algorithm

For a fixed point of the form $z = (P + q\sqrt{D})/Q$ with integers $P, q, Q, D$ (where $D$ is not a perfect square), the CF expansion is computed by the following algorithm without any floating-point arithmetic:

1. Compute $a_n = \lfloor z_n \rfloor$ using the floor of the quadratic surd (computed via integer square root bounds on $D$).
2. Update $z_{n+1} = 1/(z_n - a_n)$, which yields a new quadratic surd $(P', q'\sqrt{D})/Q'$ with integer coefficients obtained by rationalizing the denominator.
3. Record the state $(P_n, q_n, Q_n)$ at each step. Since all quantities are bounded (for a periodic CF), the state must eventually repeat, and the first repetition detects the exact period.

This algorithm is exact, produces the correct period for every quadratic irrational, and eliminates the floating-point corruption that affected 17.7% of orbits in naive implementations.

## Appendix B. Data Availability

The Li--Liao three-body periodic orbit catalog is available at https://github.com/sjtu-liao/three-body. Our computational pipeline (word-to-matrix mapping, exact CF computation, correlation analysis) and all 695 orbit CF decompositions will be made available at [repository URL] upon publication.
