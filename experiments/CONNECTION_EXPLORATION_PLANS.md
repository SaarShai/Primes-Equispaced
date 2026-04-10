# Connection Exploration Plans — Next Steps, Verification, Proof Targets, Applications
Created: 2026-04-04
Practical applications research delegated: tasks 073, 074 in Ollama queue

## DEEP CONNECTION 1: Ford Circles / Geodesics in H²

**What we know:**
- Farey tessellation tiles H² with ideal hyperbolic triangles
- Geodesics between Farey neighbors = shortest paths in hyperbolic metric
- Ford circle at a/b: radius 1/(2b²), tangent to x-axis. Two tangent iff |ad-bc|=1
- Series-Adler-Flatto: continued fractions CODE geodesics on PSL(2,Z)\H

**Verification steps:**
1. Compute: for each pair of Farey neighbors (a/b, c/d) in F_p, compute the hyperbolic geodesic length = 2·arcsinh(|c/d - a/b|/(2·sqrt(1/(2b²)·1/(2d²)))). Verify these equal the Ford circle tangency distances.
2. Verify: the coding map (geodesic on modular surface → sequence of L/R moves → continued fraction) reproduces the Stern-Brocot path for specific examples (p=13, 19, 31).
3. Check: does the total hyperbolic length of all Farey geodesics at level p have an asymptotic formula involving ζ(2)?

**Proof targets:**
- PROVE: The total hyperbolic area added at step p (from F_{p-1} to F_p) equals φ(p)·π (each new ideal triangle has area π). This should be elementary from the tessellation.
- PROVE: Our four-term decomposition ΔW = (A-B-C-D)/n'² has a geometric interpretation: A = "new triangle area contribution", B+C = "overlap with existing triangles", D = "dilution from rescaling". Can we formalize this on the modular surface?
- DERIVE: Express R(p) = 2ΣD·δ/Σδ² in terms of hyperbolic quantities (e.g., geodesic curvatures, horoball volumes).

**Computational tests (delegate):**
- Plot Ford circles for F_31 colored by ΔW contribution (positive=blue, negative=red)
- Compute hyperbolic Voronoi tessellation of Farey points at level p
- Check if the "hyperbolic ΔW" (discrepancy in hyperbolic metric) has cleaner behavior than Euclidean ΔW

---

## DEEP CONNECTION 2: Horocycle Equidistribution → ΔW

**What we know:**
- Marklof: F_N parameterizes horocycle at height 1/N on PSL(2,Z)\H
- ΔW(p) = change in discrepancy as horocycle descends 1/(p-1) → 1/p
- Rate of equidistribution controlled by spectral gap of Laplacian on PSL(2,Z)\H
- λ₁ = 1/4 + γ₁² gives the dominant oscillation frequency

**Verification steps:**
1. Compute: the Marklof parameterization explicitly for F_13, F_17, F_19. Map each Farey fraction to a point on the horocycle {z ∈ H : Im(z) = 1/N} and verify the correspondence.
2. Verify: the discrepancy of the horocycle points in the fundamental domain matches our W(F_N) up to known constants.
3. Compute: the spectral expansion of the horocycle integral h_N(f) = Σ_{a/b ∈ F_N} f(a/b + i/N) for specific Maass forms f. Check that the γ₁ term dominates.

**Proof targets:**
- PROVE: ΔW(p) = d/dN [horocycle discrepancy] evaluated at N=p, up to lower-order terms. This would formally connect ΔW to the derivative of horocycle equidistribution.
- PROVE (GRH-conditional): The spectral expansion of ΔW(p) has leading term proportional to cos(γ₁·log(p) + φ)/√p, with explicit constants from |c₁| = 1/(ρ₁·ζ'(ρ₁)).
- DERIVE: The four-term decomposition A, B, C, D in spectral language. What spectral modes contribute to each term?

**Key references to check:**
- Marklof, "The n-point correlations between values of a linear form" (2000)
- Boca-Cobeli-Zaharescu, "Distribution of lattice points visible from the origin" (2000)
- Sarnak, "Asymptotic behavior of periodic orbits of the horocycle flow" (1981)

---

## DEEP CONNECTION 3: Selberg Trace Formula / Spectral Dominance

**What we know:**
- Selberg trace formula: Σ_j h(r_j) = Σ_{γ} [geometric terms involving closed geodesic lengths]
- Spectral parameters r_j relate to Laplacian eigenvalues: λ_j = 1/4 + r_j²
- For PSL(2,Z)\H: Eisenstein series (continuous spectrum) involve ζ(s); Maass cusp forms (discrete spectrum)
- Our observation: γ₁ dominance in sgn(ΔW) = lowest spectral mode dominance

**Verification steps:**
1. Compute: Express ΔW(p) as a sum over spectral data. Using the explicit formula approach: ΔW(p) should decompose as Σ_k c_k · p^{iγ_k}/p + error terms. Verify the coefficients c_k match c_k = 1/(ρ_k · ζ'(ρ_k)).
2. Verify: The truncated spectral expansion (using only γ₁) predicts sgn(ΔW(p)) correctly for p ≤ 100K. What's the error rate? How many γ_k do we need for 99% accuracy?
3. Compute: The first 10 spectral coefficients |c_k| and check that |c₁| >> |c₂| >> ... (spectral dominance).

**Proof targets:**
- PROVE: The spectral expansion ΔW(p) = Σ_k c_k · p^{iγ_k - 1/2} + O(1/p) with explicit c_k = 1/(ρ_k · ζ'(ρ_k)). This is the GRH-conditional Perron integral result.
- PROVE: |c₁| = 0.089 dominates: |c₁| > Σ_{k≥2} |c_k| for the purposes of sign determination (i.e., the γ₁ phase prediction has accuracy > 50%). This would be a statement about the distribution of |ζ'(ρ_k)|.
- DERIVE: From the Selberg trace formula perspective, what does "ΔW(p)" correspond to on the geometric side? Are there specific closed geodesics whose lengths relate to log(p)?

**The quantum chaos angle:**
- "Temperature" = 1/log(p). As p grows, lower modes dominate (like cooling a quantum system).
- Predict: for very large p, sgn(ΔW(p)) should be almost perfectly predicted by γ₁ alone. For small p (p < 100), multiple modes contribute and prediction is noisier.
- Test: plot prediction accuracy of γ₁-only vs number of modes, as function of p-range.

---

## MODERATE CONNECTION 1: Mediant as Denominator-Minimizer

**What we know:**
- Mediant (a+c)/(b+d) of Farey neighbors uniquely minimizes denominator in the interval (a/b, c/d)
- This is a discrete extremal principle (not variational calculus)
- Well-known from Stern-Brocot tree theory

**Verification:** Already proven — this is a theorem.

**Proof target — something NEW:**
- PROVE: When a new fraction a/p enters F_p, its "insertion cost" (contribution to ΔW) is related to its Stern-Brocot depth. Specifically: fractions deeper in the tree (more continued fraction steps) contribute less to |ΔW|.
- COMPUTE: For each new fraction in F_p, compute its Stern-Brocot depth and its ΔW-contribution. Is there a monotone relationship?
- DERIVE: If depth correlates with ΔW contribution, this gives a "variational" interpretation: the mediant principle (minimize denominator) also minimizes discrepancy cost.

---

## MODERATE CONNECTION 2: Stern-Brocot Path = Best Rational Approximation

**What we know:**
- Convergents p_k/q_k of CF(α) minimize |α - p/q| subject to q ≤ q_k (Lagrange, Hurwitz)
- Stern-Brocot path from root to a/b = continued fraction expansion
- Gauss-Kuzmin distribution governs statistics of CF partial quotients

**Verification:** Classical theorem — nothing to verify.

**Proof target — something NEW:**
- PROVE: The statistics of Stern-Brocot depths of fractions in F_p follow the Gauss-Kuzmin distribution. This should be provable from the connection between the Gauss map and the geodesic flow on PSL(2,Z)\H.
- DERIVE: Does the average Stern-Brocot depth of new fractions entering at level p relate to our ΔW(p)? If deeper fractions contribute less to ΔW, the average depth × φ(p) should predict |ΔW(p)|.
- COMPUTE: Stern-Brocot depths of all φ(p) new fractions entering F_p for p ≤ 1000. Check correlation with |ΔW(p)|.

---

## PRACTICAL APPLICATIONS (all connections)

### Quantum Mechanics / Modular Surface

**Quantum chaos on PSL(2,Z)\H (DEEP 2+3):**
- The modular surface is a canonical example in quantum chaos. Maass forms ARE the quantum eigenstates; our ΔW(p) detects their spectral contributions.
- APPLICATION: Our spectral expansion (c_k coefficients) could provide a new numerical method for computing Maass form eigenvalues — if the coefficients can be extracted from ΔW data alone. Test: invert the spectral expansion to recover γ_k from ΔW(p) data.
- APPLICATION: Quantum unique ergodicity (QUE) on the modular surface was proved by Lindenstrauss (2006 Fields Medal). Our horocycle interpretation of ΔW may give quantitative refinements of QUE — controlling not just equidistribution but the RATE at each prime step.

**Quantum computing:**
- PSL(2,Z) gate sets: some quantum computing proposals use modular group elements as gates. Farey structure provides a canonical decomposition of these gates (via continued fractions).
- SPECULATIVE: Could Farey mediants provide a gate synthesis algorithm (approximating arbitrary unitaries from a finite gate set)? The Stern-Brocot tree already solves the analogous problem for rational approximation. Solovay-Kitaev theorem is the existing solution.

### Cryptography

**Lattice-based crypto (DEEP 1):**
- Modern lattice crypto (NTRU, Kyber) works in polynomial rings. Ford circles / Farey geometry live in a simpler 2D lattice (Z²). Connection is structural (both use lattice geometry) but not directly applicable to current schemes.
- MODERATE: The Farey tessellation provides a geometric framework for studying lattice reduction (LLL algorithm). Each LLL reduction step can be viewed as a move in the Farey tessellation. Could our ΔW analysis improve lattice reduction bounds? SPECULATIVE but worth checking.

### Engineering / Signal Processing

**Spectral dominance as filter design (DEEP 3):**
- Our finding that γ₁ controls sgn(ΔW) is structurally a band-pass filter centered at frequency γ₁/(2π) in log-space.
- APPLICATION: For signals with number-theoretic structure (e.g., prime-indexed data), a filter at the γ₁ frequency would extract the dominant oscillation. Niche but real for number-theoretic data analysis.

**Rational approximation (MODERATE 2):**
- Stern-Brocot tree for clock synthesis (approximating irrational frequency ratios with rational ones) is already used in PLL design. Our contribution: the ΔW analysis tells you the "cost" of each approximation step.
- APPLICATION: In FPGA clock generation, choosing which rational approximation to use could be informed by minimizing the Farey discrepancy contribution. Very niche.

### AMR / Mesh (already HIGH priority — see AMR-8, task_074)
- Crack-free LOD hierarchy is the strongest practical application.
- 7-15x cell reduction for shock-capturing CFD.
- Full industry exploration delegated to task_074.

---
## PAPER SECTION: "A Different Computational Path to the Zeta Zeros"

The Farey spectral function F(γ) = |Σ R(p)·p^{-1/2-iγ}|² detects zeta zero locations
from Farey discrepancy data alone. Key figures: farey_spectroscope.png, farey_vs_classical_zeros.png.

Significance:
1. Alternative computational path to zeros (normally via Riemann-Siegel formula)
2. Confirms Chebyshev bias mechanism: same γ₁ controls prime races AND Farey regularity
3. Concrete manifestation of Franel-Landau equivalence at individual zero level
4. "Farey spectroscope" = visually compelling, pedagogically powerful
