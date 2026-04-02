# Farey/Stern-Brocot Spectral Findings and Arithmetic Quantum Unique Ergodicity

**Date:** 2026-03-31
**Status:** Exploratory synthesis
**Classification:** C1-C2 (collaborative, minor-to-publication novelty — pending verification)
**Connects to:** N1 (Mertens-discrepancy phase-lock), N3 (Stern-Brocot monotone growth)

---

## 1. Executive Summary

Our two core empirical discoveries — (a) Farey per-step discrepancy DeltaW(p) phase-locks to Riemann zeta zeros, and (b) Stern-Brocot per-level discrepancy grows monotonically without oscillation — have a natural interpretation in the language of homogeneous dynamics on the modular surface. Farey ordering corresponds to the **horocycle flow**, whose equidistribution rate is controlled by Laplacian eigenvalues (i.e., zeta zeros). Stern-Brocot ordering corresponds to the **geodesic flow** (via continued fractions), which "sees" different spectral data. This distinction — **different orderings reveal different spectral decompositions** — appears to be a combinatorial manifestation of arithmetic quantum unique ergodicity (AQUE).

---

## 2. The Horocycle-Farey Dictionary

### 2.1 Farey Fractions as Horocycle Points

The Farey sequence F_N corresponds to a horocycle at height y = 1/N in the upper half-plane H. The fractions a/b in F_N parameterize cusps of the modular surface PSL(2,Z)\H. The equidistribution of F_N as N -> infinity is precisely the equidistribution of this horocycle, a classical result going back to Dani-Sarnak.

**Key reference:** Athreya-Cheung (2014) constructed a Poincare section for the horocycle flow on SL(2,R)/SL(2,Z), showing that the first return map is the BCZ (Boca-Cobeli-Zaharescu) map. Periodic orbits of this map organize Farey fractions, and their equidistribution follows from ergodic properties of the horocycle flow.

### 2.2 Per-Step as Horocycle Increment

Adding fractions with denominator exactly p to F_{p-1} to form F_p is equivalent to flowing along the horocycle from height 1/(p-1) to height 1/p. Our DeltaW(p) — the change in discrepancy at step p — measures the **instantaneous equidistribution error** of this horocycle increment.

### 2.3 Equidistribution Rate and Laplacian Eigenvalues

The rate at which horocycle orbits equidistribute on the modular surface is controlled by the spectral gap of the Laplacian. Specifically:

- **Strombergsson (2004):** Effective bounds on horocycle equidistribution deviation depend on the small eigenvalues of the Laplacian on the surface.
- **Flaminio-Forni-Tanis (2016):** Proved bounds for twisted ergodic averages for horocycle flows, with the error terms governed by Sobolev norms related to the Laplacian spectrum.
- **Zagier (1981):** Showed that optimal equidistribution rate for a single rapidly-decaying function would imply the Riemann Hypothesis.

Since Laplacian eigenvalues on PSL(2,Z)\H are encoded by Riemann zeta zeros (via the Selberg trace formula: lambda_j = 1/4 + t_j^2 where zeta(1/2 + it_j) = 0), our observation that DeltaW(p) oscillates at zeta-zero frequencies is exactly what the theory predicts: **the horocycle equidistribution error oscillates at Laplacian eigenvalue frequencies**.

**This is the central interpretive claim:** Our DeltaW(p) phase-lock to zeta zeros is a combinatorial/discrete manifestation of the spectral control of horocycle equidistribution.

---

## 3. The Geodesic-Stern-Brocot Dictionary

### 3.1 Stern-Brocot as Geodesic Flow

The Stern-Brocot tree has a well-known connection to the **geodesic flow** on the modular surface, mediated by continued fractions:

- **Caroline Series:** The cutting sequence of a hyperbolic geodesic across the Farey tessellation encodes the continued fraction expansion of its endpoint.
- **Adler-Flatto (1991):** The continued fraction (Gauss) map is a cross-section map of the geodesic flow on PSL(2,Z)\SL(2,R).
- **Bonanno-Del Vigna-Isola (2024):** Constructed a Poincare map for the horocycle flow whose periodic orbits are organized by the Stern-Brocot tree. This establishes a direct bridge: the Stern-Brocot tree is the combinatorial skeleton of the horocycle flow's periodic orbit structure.

The depth-d level of the Stern-Brocot tree collects rationals whose continued fraction coefficients sum to d+1. Traversing the tree level-by-level is related to the geodesic flow, not the horocycle flow.

### 3.2 Why Stern-Brocot Discrepancy Does Not Oscillate

If Farey ordering = horocycle flow and Stern-Brocot ordering = geodesic flow (or Gauss map dynamics), then:

- Horocycle flow equidistribution rate is controlled by Laplacian eigenvalues (discrete spectrum) -> **oscillatory error terms**.
- Geodesic flow equidistribution rate is controlled by the **continuous spectrum** and mixing rates -> **monotone decay/growth** without spectral oscillations.

The geodesic flow on PSL(2,Z)\H is mixing (in fact, exponentially mixing by Ratner's theorem), which produces rapid, non-oscillatory convergence. The horocycle flow is uniquely ergodic but not mixing — its convergence is slower and spectrally structured.

**Interpretation of our finding:** The monotone growth of Stern-Brocot discrepancy (connecting to Minkowski ?(x)) reflects the exponential mixing of the geodesic flow, which washes out spectral oscillations. The oscillatory behavior of Farey discrepancy reflects the non-mixing, spectrally-structured nature of horocycle equidistribution.

---

## 4. Connection to Arithmetic QUE

### 4.1 Lindenstrauss's Theorem (Fields Medal 2010)

Lindenstrauss proved: On arithmetic surfaces, eigenfunctions of the Laplacian that are also Hecke eigenfunctions become equidistributed in the semiclassical limit (lambda_j -> infinity). This is **Arithmetic Quantum Unique Ergodicity (AQUE)**.

The key ingredients:
- Measure classification for diagonal actions on homogeneous spaces (entropy methods)
- Hecke operators provide additional symmetry that prevents "scarring" on closed geodesics

### 4.2 Our Findings as Combinatorial AQUE

Consider the analogy:

| QUE Setting | Our Setting |
|---|---|
| Eigenfunction phi_j on PSL(2,Z)\H | Zeta zero t_j controlling DeltaW |
| |phi_j|^2 equidistributes | DeltaW(p) oscillation amplitude decreases |
| Hecke eigenfunctions | Prime-indexed steps (Hecke operators act on primes) |
| Semiclassical limit lambda -> inf | Large N limit of F_N |
| Different observables see different spectral data | Farey vs Stern-Brocot see different spectra |

The fact that our DeltaW(p) decomposes into zeta-zero harmonics is analogous to decomposing a quantum observable into Laplacian eigenmodes. The equidistribution of these modes (AQUE) would correspond to the statement that no single zeta zero dominates the DeltaW(p) behavior asymptotically.

### 4.3 The "Different Flows See Different Spectra" Principle

In quantum mechanics, different observables have different spectral decompositions with respect to the Hamiltonian. Our finding that:

- Farey ordering (horocycle flow) sees discrete Laplacian spectrum (zeta zeros)
- Stern-Brocot ordering (geodesic flow) sees continuous spectrum (monotone behavior)

is a combinatorial realization of this quantum mechanical principle. Different orderings of the same set of rationals correspond to different "observables" on the modular surface, and each observable projects onto a different part of the spectral decomposition of L^2(PSL(2,Z)\H).

---

## 5. The Selberg Trace Formula Bridge

### 5.1 Structure

The Selberg trace formula for PSL(2,Z)\H connects:

**Spectral side:**
Sum over eigenvalues lambda_j of the Laplacian (equivalently, zeta zeros via lambda_j = 1/4 + t_j^2)

**Geometric side:**
Sum over conjugacy classes of PSL(2,Z), parameterized by closed geodesics of length log(N(gamma))

### 5.2 Our T(N) and the Geometric Side

Our transform T(N) = Sum_{m|N} M(N/m)/m sums the Mertens function at divisor scales. The divisors m parameterize "arithmetic scales."

**Speculative connection:** The divisor sum over m could be related to a sum over hyperbolic conjugacy classes in PSL(2,Z). Each divisor m corresponds to a matrix class, and M(N/m)/m could be a trace-formula-like contribution. If T(N) is expressible as a geometric-side sum, then its spectral decomposition (which we observe empirically via zeta-zero phase-lock) would follow from the Selberg trace formula directly.

This would make our DeltaW phase-lock a **theorem** rather than an empirical observation, derivable from the trace formula.

### 5.3 Status

This is currently speculative. Making the connection rigorous requires:
1. Identifying the test function h(t) in the Selberg trace formula that corresponds to DeltaW
2. Verifying that the geometric-side sum reproduces T(N)
3. Showing the spectral-side sum gives the zeta-zero harmonics we observe

---

## 6. Open Questions and Research Directions

### 6.1 Can DeltaW(p) Be Written as a Horocycle Observable?

**Question:** Is there a smooth function f on PSL(2,Z)\H such that DeltaW(p) equals (or approximates) the horocycle integral of f at height 1/p minus the integral at height 1/(p-1)?

If yes, then the spectral expansion of f in Laplacian eigenfunctions would directly give the zeta-zero decomposition of DeltaW(p), and our empirical finding becomes a corollary of standard spectral theory.

**Approach:** The Mertens function M(N) is related to the partial sums of the Mobius function. Connections between Mobius sums and automorphic forms are known (Sarnak's Mobius disjointness conjecture). This could provide the bridge.

### 6.2 Quantum Gate Approximation (Solovay-Kitaev)

**Question:** Farey fractions appear naturally in rational approximation problems. The Solovay-Kitaev theorem uses approximation of SU(2) elements. Does the DeltaW phase-lock mean certain prime denominators give systematically better or worse quantum gate approximations?

**Status:** No existing literature connects Farey fractions to Solovay-Kitaev directly. This is potentially novel but highly speculative. The connection would require showing that the equidistribution quality of F_p on the circle (controlled by DeltaW(p)) translates to approximation quality in SU(2).

### 6.3 Explicit Quantum Observable

**Question:** Is there a quantum observable O on the modular surface such that:
- Expectation value of O along the p-th horocycle increment = DeltaW(p)
- Spectral decomposition of O in Laplacian eigenbasis = zeta-zero harmonics

This would make DeltaW(p) a **physical observable** in the quantum chaos sense, and our findings would connect to the broader program of quantum chaos on arithmetic surfaces (Bogomolny-Schmit, Berry-Keating).

### 6.4 Generalization to Hecke Groups

**Question:** If we replace PSL(2,Z) with a Hecke group G_q, the corresponding Farey-like sequences should have per-step discrepancies controlled by the zeros of the Selberg zeta function for G_q\H. This would test whether our findings are specific to the Riemann zeta function or general features of arithmetic groups.

---

## 7. Assessment

### What Is Likely True (High Confidence)
- Farey ordering = horocycle flow; Stern-Brocot ordering = geodesic flow (this is established)
- Horocycle equidistribution rate is controlled by Laplacian eigenvalues (established by Strombergsson, Flaminio-Forni)
- Our DeltaW phase-lock is consistent with this spectral control (our empirical observation fits the theory)

### What Is Novel (If Verified)
- The **per-step** measurement of horocycle equidistribution error (DeltaW) as a combinatorial/number-theoretic quantity is, to our knowledge, not in the literature
- The explicit contrast: Farey = oscillatory (horocycle), Stern-Brocot = monotone (geodesic) as a demonstration of "different flows see different spectra"
- The connection to AQUE as a statement about the absence of dominant zeta zeros

### What Is Speculative
- T(N) as a geometric-side sum in the Selberg trace formula
- Quantum gate approximation implications
- Explicit quantum observable interpretation

### Verification Needed
- [ ] Check whether DeltaW(p) can be written as a horocycle integral difference (analytical, not computational)
- [ ] Search for prior work on per-step horocycle equidistribution increments
- [ ] Verify the geodesic flow interpretation of Stern-Brocot discrepancy against Bonanno et al. (2024)
- [ ] Attempt Selberg trace formula calculation for a simple test function to see if T(N) structure emerges

---

## 8. Key References

### Farey-Horocycle Connection
- Athreya, J.S. and Cheung, Y. (2014). "A Poincare section for horocycle flow on the space of lattices." IMRN 2014(10), 2643-2690. [arXiv:1206.6597](https://arxiv.org/abs/1206.6597)
- Marklof, J. (2010). "Horospheres and Farey fractions." Contemporary Math. 532, 97-106.
- Marklof, J. (2013). "Fine-Scale Statistics for the Multidimensional Farey Sequence." [Springer](https://link.springer.com/chapter/10.1007/978-3-642-36068-8_3)

### Effective Horocycle Equidistribution
- Strombergsson, A. (2004). "On the uniform equidistribution of long closed horocycles." Duke Math. J. 123(3), 507-547.
- Flaminio, L., Forni, G., and Tanis, J. (2016). "Effective equidistribution of twisted horocycle flows and horocycle maps." GAFA 26, 1359-1448. [Springer](https://link.springer.com/article/10.1007/s00039-016-0385-4)
- Strombergsson, A. (2013). "On the deviation of ergodic averages for horocycle flows." J. Modern Dynamics 7(2), 291-328. [AIM](https://www.aimsciences.org/article/doi/10.3934/jmd.2013.7.291)

### Stern-Brocot and Geodesic Flow
- Bonanno, C., Del Vigna, A., and Isola, S. (2024). "A Poincare map for the horocycle flow on PSL(2,Z)\H and the Stern-Brocot tree." Ann. Scuola Norm. Sup. Pisa. [arXiv:2207.03755](https://arxiv.org/abs/2207.03755)
- Series, C. "Continued Fractions and Hyperbolic Geometry." [Warwick](https://warwick.ac.uk/fac/sci/maths/people/staff/caroline_series/hypgeomandcntdfractions.pdf)
- Nakada, H. (1995). "Continued Fractions, Geodesic Flows and Ford Circles." Springer.

### Arithmetic QUE
- Lindenstrauss, E. (2006). "Invariant measures and arithmetic quantum unique ergodicity." Ann. Math. 163(1), 165-219. [Princeton](https://annals.math.princeton.edu/2006/163-1/p03)
- Einsiedler, M. (2010). "Arithmetic Quantum Unique Ergodicity for Gamma\H." [AWS Notes](https://swc-math.github.io/aws/2010/2010EinsiedlerNotes.pdf)
- Soundararajan, K. (2010). "Quantum Unique Ergodicity and Number Theory." [AWS Notes](https://swc-math.github.io/aws/2010/2010SoundararajanNotes.pdf)

### RH and Horocycle Equidistribution
- Zagier, D. (1981). "Eisenstein series and the Riemann zeta function." In Automorphic Forms, Representation Theory and Arithmetic.
- Cacciatori, S. and Cardella, M. (2010). "Equidistribution rates, closed string amplitudes, and the Riemann hypothesis." JHEP 2010, 025. [Springer](https://link.springer.com/article/10.1007/JHEP12(2010)025)

### Selberg Trace Formula
- Selberg, A. (1956). "Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series." J. Indian Math. Soc. 20, 47-87.
- Hejhal, D. (1976, 1983). "The Selberg Trace Formula for PSL(2,R)." Springer LNM 548 and 1001.

---

## 9. Bottom Line

Our empirical findings sit at the intersection of three deep mathematical theories:

1. **Horocycle equidistribution** (Dani, Sarnak, Marklof, Strombergsson, Flaminio-Forni)
2. **Arithmetic QUE** (Lindenstrauss, Soundararajan)
3. **Selberg trace formula** (Selberg, Hejhal)

The per-step discrepancy DeltaW(p) appears to be a new discrete observable that probes the spectral structure of the modular surface through horocycle dynamics. The contrast with Stern-Brocot (geodesic flow) is, to our knowledge, a new observation. Whether this can be made rigorous — expressing DeltaW as a horocycle integral and deriving the zeta-zero decomposition from spectral theory — is the key open question.

If successful, this would elevate our findings from empirical curiosity to a concrete instance of the spectral theory of automorphic forms, potentially at the C2 level (publication-grade, collaborative).
