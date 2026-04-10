# Farey Sequences, Stern-Brocot Trees, Continued Fractions, and Electron Orbits

## Research Survey: Number-Theoretic Structures in Atomic and Quantum Physics

**Date:** 2026-03-27
**Scope:** Connections between Farey/Stern-Brocot/continued fraction structures and the quantum mechanics of electrons in atoms. Each section rated STRONG / MODERATE / SPECULATIVE / NONE.

---

## Table of Contents

1. [Quantum Numbers and Rational Structure](#1-quantum-numbers-and-rational-structure)
2. [Bohr-Sommerfeld and EBK Quantization](#2-bohr-sommerfeld-and-ebk-quantization)
3. [Semiclassical Periodic Orbits and the Gutzwiller Trace Formula](#3-semiclassical-periodic-orbits-and-the-gutzwiller-trace-formula)
4. [Rydberg Atoms in External Fields](#4-rydberg-atoms-in-external-fields)
5. [Quantum Chaos: Hydrogen in a Magnetic Field](#5-quantum-chaos-hydrogen-in-a-magnetic-field)
6. [The Bohr Model and Shell Filling (2n^2)](#6-the-bohr-model-and-shell-filling-2n2)
7. [Multi-Electron Atoms and Inter-Electron Resonances](#7-multi-electron-atoms-and-inter-electron-resonances)
8. [Zeta Function, Casimir Effect, and Density of States](#8-zeta-function-casimir-effect-and-density-of-states)
9. [Quasicrystals, Penrose Tilings, and Fibonacci Anyons](#9-quasicrystals-penrose-tilings-and-fibonacci-anyons)
10. [Open Problems and Opportunities](#10-open-problems-and-opportunities)

---

## 1. Quantum Numbers and Rational Structure

**Rating: SPECULATIVE**

### The Observation

Electron orbitals are labeled by integer quantum numbers (n, l, m, s). Hydrogen energy levels go as E_n = -13.6/n^2 eV. The ratios E_m/E_n = n^2/m^2 are rational. Angular momentum quantum numbers l range from 0 to n-1, and magnetic quantum numbers m range from -l to +l. The question: does the Farey/Stern-Brocot tree organize these quantum numbers?

### What Exists

- The set {1/n^2 : n = 1, 2, 3, ...} defines the hydrogen spectrum. Spectral line frequencies involve differences 1/m^2 - 1/n^2, which are rational numbers with specific denominator structure.
- The Stern-Brocot tree contains every positive rational exactly once. The fractions 1/n^2 appear in the tree, but they do not form a natural subtree or follow mediant relationships with each other.
- The degeneracy pattern (2l+1 states per l, summing to n^2 total per shell) is a consequence of SO(4) symmetry (the Laplace-Runge-Lenz symmetry of the Coulomb potential), not of number-theoretic structure.

### Assessment

No published work connects the Farey/Stern-Brocot tree to the *static* organization of quantum numbers. The quantum number structure arises from Lie group symmetries (SO(3) rotational, SO(4) dynamical), not from number-theoretic mediant operations. However, the *transition frequencies* between levels produce rational numbers whose denominators could potentially be analyzed through Farey-type structures -- this appears unexplored.

### Key Distinction

The Farey structure becomes relevant not for the *labels* of quantum states but for the *dynamics* -- specifically when asking about resonances, frequency ratios, and orbital winding numbers in the semiclassical limit (see Sections 3-5).

---

## 2. Bohr-Sommerfeld and EBK Quantization

**Rating: MODERATE**

### The Connection

The old quantum theory (Bohr-Sommerfeld) quantizes action variables: integral of p dq = n*h. For systems with multiple degrees of freedom, the Einstein-Brillouin-Keller (EBK) generalization quantizes actions on invariant tori: J_i = (n_i + alpha_i/4) * hbar, where alpha_i are Maslov indices.

The connection to continued fractions is indirect but real:

1. **Torus quantization requires integer/rational constraints**: EBK conditions are integer conditions on the action variables of invariant tori. The frequency ratios omega_1/omega_2 on these tori can be rational (periodic orbits) or irrational (quasi-periodic motion).

2. **Convergents of continued fractions approximate irrational tori**: The continued fraction expansion of an irrational frequency ratio produces a sequence of rational approximants p_k/q_k (the convergents). Each convergent corresponds to a periodic orbit that "approximates" the irrational torus.

3. **BS-EBK quantization bridges periodic orbits and tori**: Takahashi and Takatsuka showed that Bohr-Sommerfeld conditions on periodic orbits, when those orbits are continued-fraction convergents to a quantizing torus, yield energies that converge exponentially to the EBK quantized energy.

### Key Papers

- Takahashi & Takatsuka, "How periodic orbits converge to quantizing tori," Phys. Rev. A (2004). Shows exponential convergence of BS-EBK periodic orbit energies to torus-quantized values.
- Einstein (1917) original formulation of multi-dimensional quantization conditions.
- Keller (1958) addition of Maslov corrections.

### Assessment

The continued fraction connection here is well-established in the mathematical physics of semiclassical mechanics, but it operates at the level of *approximating irrational tori by rational periodic orbits*, not directly through Farey sequence structure. The Farey ordering of rationals becomes important when one needs to enumerate *all* periodic orbits systematically (see Section 3).

---

## 3. Semiclassical Periodic Orbits and the Gutzwiller Trace Formula

**Rating: STRONG**

### The Core Connection

This is the strongest and most direct connection between Farey sequences and atomic quantum mechanics.

**Gutzwiller's trace formula** expresses the quantum density of states as a sum over classical periodic orbits:

    d(E) ~ d_smooth(E) + sum over periodic orbits gamma of A_gamma * cos(S_gamma/hbar - mu_gamma * pi/2)

where S_gamma is the action, A_gamma the amplitude, and mu_gamma the Maslov index of orbit gamma.

**Periodic orbits are classified by rational winding numbers.** In a 2D system with two frequencies (omega_1, omega_2), a periodic orbit has winding number p/q = omega_1/omega_2 rational. The set of all periodic orbits up to some period is *exactly the Farey sequence* F_Q for some order Q.

### How It Works for Atoms

For the hydrogen atom:
- **Pure Coulomb (no external fields)**: All orbits are periodic (the system is integrable due to SO(4) symmetry). The Gutzwiller trace formula reproduces the exact Bohr spectrum E_n = -1/n^2.
- **With external fields (Stark, Zeeman)**: Integrability is broken. Only isolated periodic orbits survive. These orbits are organized by their rational winding numbers, forming a Farey hierarchy.
- **Hydrogen in crossed E and B fields**: Winding numbers of periodic orbits follow a hierarchy that mirrors the Farey tree. Torus quantization via periodic orbits uses this hierarchy explicitly.

### Cvitanovic's Program (ChaosBook)

Predrag Cvitanovic's periodic orbit theory (developed from ~1988 onward) provides the mathematical framework:

1. **Cycle expansions**: The quantum zeta function is expanded in terms of periodic orbits ordered by topological length. The symbolic dynamics of chaotic systems naturally produces Farey-ordered orbit families.
2. **The Farey map**: Explicitly studied as a paradigmatic system for periodic orbit theory. The Farey map's periodic orbits are in 1-1 correspondence with rationals, ordered by the Farey tree.
3. **Quantum zeta functions**: Dynamical zeta functions (products over periodic orbits) encode quantum spectra. For the Farey map, the thermodynamic formalism reveals phase transitions in the orbit structure.

### Key Papers

- Gutzwiller, "Chaos in Classical and Quantum Mechanics" (Springer, 1990). The foundational text.
- Cvitanovic et al., "Beyond the periodic orbit theory," Nonlinearity 11, 1209 (1998). Farey map and cycle expansions.
- Cvitanovic, Artuso, Mainieri, Tanner, Vattay, "Chaos: Classical and Quantum" (ChaosBook.org). The comprehensive treatment.
- Wintgen, Marxer, Briggs, "Hydrogen atom in crossed E and B fields," Phys. Rev. A 75, 023406 (2007). Farey hierarchy of periodic orbits in diamagnetic hydrogen.

### Why This Is STRONG

The Farey sequence is not merely an analogy here -- it is the *natural classification scheme* for periodic orbits in 2D Hamiltonian systems. When these systems describe atomic electrons (hydrogen in fields, Rydberg atoms), the Farey structure directly organizes the contributions to quantum spectra via the trace formula.

---

## 4. Rydberg Atoms in External Fields

**Rating: STRONG**

### The Physical System

A Rydberg atom has one electron in a very high-n state (n > 20, sometimes n > 100). The electron is far from the nucleus, moving slowly, and behaves almost classically. The correspondence principle applies directly: quantum mechanics approaches classical mechanics.

In external electric (Stark) or magnetic (Zeeman) fields, the classical dynamics of the Rydberg electron becomes chaotic. This is *exactly* the regime where KAM theory, continued fractions, and Farey sequences become relevant.

### KAM Theory and Continued Fractions

KAM (Kolmogorov-Arnold-Moser) theory describes what happens when an integrable system is perturbed:

1. **Rational frequency ratios (p/q)**: Resonant tori are destroyed. Gaps open in phase space at rational winding numbers -- the analogue of Kirkwood gaps in the asteroid belt.
2. **Irrational frequency ratios**: KAM tori survive if the frequency ratio is "sufficiently irrational" (satisfies a Diophantine condition). The most robust tori have frequency ratios whose continued fraction coefficients are bounded -- the "most irrational" numbers like the golden ratio phi = [1;1,1,1,...].
3. **Continued fraction expansion determines stability**: The rate at which a frequency ratio can be approximated by rationals (measured by continued fraction convergents) determines whether the corresponding torus survives perturbation.

### Application to Rydberg Atoms

- **Stark effect (electric field)**: The Rydberg electron's parabolic quantum numbers map to action-angle variables. In strong fields, Stark manifolds from adjacent n overlap, creating a chaotic region with destroyed resonant tori. The surviving (KAM) tori have winding numbers with specific continued fraction properties.
- **Zeeman effect (magnetic field)**: The diamagnetic hydrogen problem is a paradigm of quantum chaos. Classical dynamics shows a transition from regularity to chaos, with KAM tori destroyed in Farey order -- low-denominator resonances (1/2, 1/3, 2/3) are destroyed first.
- **Crossed fields**: Both electric and magnetic fields create a fully 3D chaotic system where periodic orbits form a complete Farey hierarchy.

### "Kirkwood Gaps" in Atomic Spectra?

The analogy with celestial mechanics is precise:

| Celestial Mechanics | Atomic Physics |
|---|---|
| Asteroid belt | Rydberg energy spectrum |
| Jupiter's perturbation | External field perturbation |
| Kirkwood gaps at p/q resonances | Missing/broadened spectral lines at resonant winding numbers |
| KAM tori (stable orbits) | Quasi-periodic electron orbits (sharp spectral lines) |
| Golden ratio = most stable | Golden-ratio winding numbers = most robust atomic states |

The gaps in Rydberg spectra at rational winding numbers are a real, observed phenomenon -- they correspond to the destruction of resonant tori and the onset of ionization. This is not speculation; it is established physics.

### Key Papers

- Friedrich & Wintgen, "The hydrogen atom in a uniform magnetic field -- An example of chaos," Physics Reports 183, 37 (1989). The classic review.
- Delande & Gay, "Quantum chaos and statistical properties of energy levels," Phys. Rev. Lett. 57, 2006 (1986). First numerical demonstration of GOE statistics in diamagnetic hydrogen.
- Main et al., "Precision measurements for diamagnetic Rydberg states in hydrogen," J. Phys. B 19, L461 (1986). Experimental verification.

---

## 5. Quantum Chaos: Hydrogen in a Magnetic Field

**Rating: STRONG**

### The Paradigm System

The diamagnetic Kepler problem (hydrogen atom in a uniform magnetic field) is the single most important system in quantum chaos. It connects:

- **Classical chaos** (destruction of KAM tori, onset of ergodicity)
- **Quantum spectral statistics** (transition from Poisson to GOE level spacing)
- **Periodic orbit theory** (Gutzwiller trace formula applied to a real atom)
- **Experimental verification** (high-resolution spectroscopy of Rydberg atoms)

### Farey/Arnold Tongue Structure

The connection to Farey sequences and Arnold tongues is established through:

1. **Mode-locking in driven atoms**: When atoms are driven by periodic fields (e.g., microwave-driven Rydberg atoms), the response shows mode-locking at rational frequency ratios. The mode-locked regions (Arnold tongues) are organized by the Farey tree.

2. **Quantum accelerator modes**: The most direct experimental demonstration comes from cold atom experiments. Buchleitner et al. (Phys. Rev. Lett. 96, 164101, 2006) showed that quantum accelerator modes in kicked cold atoms are organized by the Farey tree of Arnold tongues. This is a purely quantum, non-dissipative analogue of classical mode-locking.

3. **Semiclassical scarring**: Some quantum eigenstates of the diamagnetic hydrogen atom are "scarred" -- they have enhanced probability density along classical periodic orbits. These periodic orbits are classified by Farey-ordered winding numbers.

### The Key Experimental Paper

**"Quantum Accelerator Modes from the Farey Tree"** -- Buchleitner, d'Arcy, Fishman, Gardiner, Guarneri, Ma, Rebuzzini, Summy, Phys. Rev. Lett. 96, 164101 (2006).

This paper explicitly demonstrates that:
- Cold cesium atoms subjected to periodic kicks from a standing laser wave exhibit quantum accelerator modes
- These modes correspond to stable islands in the classical phase space with rational winding numbers
- The hierarchy of these modes follows the Farey tree exactly
- Higher-order modes (deeper in the Farey tree) require finer experimental resolution to observe

### Assessment

This is a STRONG connection with both theoretical framework and experimental verification. The Farey tree is not an analogy -- it is the organizing principle for the observed quantum dynamics.

---

## 6. The Bohr Model and Shell Filling (2n^2)

**Rating: SPECULATIVE (weak)**

### The Pattern

Electron shell capacities follow 2n^2:
- n=1: 2 electrons
- n=2: 8 electrons
- n=3: 18 electrons
- n=4: 32 electrons

The factor 2 comes from spin (Pauli exclusion). The factor n^2 counts orbital states: sum from l=0 to n-1 of (2l+1) = n^2.

### Number-Theoretic Observations

- n^2 = sum of first n odd numbers (1 + 3 + 5 + ... + (2n-1)). This is a classical identity.
- The atomic magic numbers (closed-shell electron counts) are: 2, 10, 18, 36, 54, 86. Differences: 8, 8, 18, 18, 32 = 2(2^2), 2(2^2), 2(3^2), 2(3^2), 2(4^2). Each value appears twice because of the two angular momentum parity classes (l and l+1) that share the same n.
- Nuclear magic numbers (2, 8, 20, 28, 50, 82, 126) have a different structure involving spin-orbit coupling. The simpler harmonic oscillator magic numbers (2, 8, 20, 40, 70, ...) are twice the tetrahedral numbers from Pascal's triangle.

### Farey/Stern-Brocot Connection?

No established connection exists. The shell structure comes from:
1. SO(3) rotational symmetry (gives 2l+1 magnetic substates)
2. SO(4) dynamical symmetry of the Coulomb potential (gives the n^2 degeneracy)
3. SU(2) spin symmetry (gives the factor of 2)

These are continuous Lie group symmetries, not discrete number-theoretic structures. The Farey/Stern-Brocot framework describes the arithmetic of rationals and their ordering -- a fundamentally different mathematical domain.

### A Possible Research Direction

The *Madelung rule* for actual electron filling order (1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, ...) follows a diagonal pattern in the (n, l) plane. The rule "fill by increasing n+l, then by increasing n" has no deep theoretical derivation from first principles. Could there be a number-theoretic explanation for why this particular ordering minimizes total energy? This remains an open question in quantum chemistry, though it likely has a physical rather than number-theoretic answer.

---

## 7. Multi-Electron Atoms and Inter-Electron Resonances

**Rating: SPECULATIVE**

### The Problem

The multi-electron atom is a many-body Coulomb problem. Electron-electron repulsion creates correlations analogous to gravitational interactions in the N-body problem. Could there be resonance phenomena between electron orbits analogous to orbital resonances in celestial mechanics?

### What Exists

1. **Doubly excited states of helium**: The simplest multi-electron case. Two electrons in high-n states of helium form a three-body Coulomb problem. These doubly excited states show rich resonance structure:
   - "Pendular-planet states" (2025): Longer-lived resonances arising from avoided crossings in the two-electron phase space. Named by analogy with celestial mechanics.
   - Classification schemes use quantum numbers (K, T, A) that describe correlated electron motion, including radial and angular correlations.

2. **Planetary atom model**: In the semiclassical limit, a doubly excited atom with two electrons at large distances resembles a two-planet system. The stability analysis of this configuration mirrors celestial mechanics.

3. **Three-body Coulomb problem in 2D**: Studied using harmonic oscillator decomposition, revealing complex resonance structure above the ionization threshold.

### Farey Connection?

No published work directly applies Farey ordering to inter-electron resonances. However, the theoretical framework exists:
- If two electrons have orbital frequencies omega_1 and omega_2, their resonances occur at omega_1/omega_2 = p/q.
- These resonances should be ordered by the Farey sequence, with low-order resonances (small q) being strongest.
- The stability of non-resonant configurations would depend on continued fraction properties of the frequency ratio.

This is a genuinely open area that could yield new insights, especially for doubly excited Rydberg atoms where the semiclassical approximation is valid.

### Key Papers

- Madronero et al., "Series of molecular-like doubly excited states of a quasi-three-body Coulomb system," arXiv:2506.13495 (2025).
- Eiglsperger, Piraux, Madronero, "Spectral representation of the three-body Coulomb problem," Phys. Rev. A 81 (2010).

---

## 8. Zeta Function, Casimir Effect, and Density of States

**Rating: MODERATE**

### Casimir Effect and Zeta Regularization

The Casimir effect (attractive force between uncharged conducting plates in vacuum) requires summing over all vacuum fluctuation modes. The sum diverges and is regularized using the Riemann zeta function:

    Sum of n^3 -> zeta(-3) = 1/120

This gives the finite Casimir energy. The technique of zeta function regularization is now a standard tool in quantum field theory, applied to:
- Casimir energies in various geometries
- Hawking radiation from black holes
- Partition functions in curved spacetime
- One-loop effective actions

### Connection to Farey Discrepancy

The Farey discrepancy D(N) measures how uniformly the Farey fractions F_N are distributed in [0,1]. The Riemann Hypothesis is equivalent to the statement that D(N) = O(N^{-1/2+epsilon}) for all epsilon > 0.

The connection to physics:
1. **The same zeta function** that regularizes the Casimir effect encodes information about prime distribution (and hence Farey discrepancy).
2. **Spectral zeta functions**: For a quantum system with eigenvalues E_n, the spectral zeta function zeta_H(s) = sum E_n^{-s} generalizes the Riemann zeta function. Its values at specific points give physical quantities (Casimir energy, determinants of Laplacians, heat kernel coefficients).
3. **Gutzwiller-Selberg connection**: For quantum systems on hyperbolic surfaces, the Selberg zeta function (a product over periodic orbits) is the analogue of both the Riemann zeta function and the Gutzwiller trace formula.

### Number-Theoretic Spin Chains

Andreas Knauf studied "number-theoretical spin chains" where the partition function involves Farey fractions. The Farey fraction spin chain (Kleban and Ozluk, 1999) has a partition function related to the Riemann zeta function, with phase transitions in the thermodynamic formalism.

### Primon Gas

The "primon gas" is a toy model in statistical mechanics where:
- Single-particle states are labeled by primes p
- Energies are E_p = log(p)
- The partition function is Z(beta) = zeta(beta)
- This directly connects the Riemann zeta function to a quantum statistical mechanical system

### Assessment

The connection is MODERATE because while the Riemann zeta function appears in both the Casimir effect and in Farey sequence theory, the connection is through the *same mathematical object* (the zeta function) rather than through a direct physical mechanism linking Farey discrepancy to vacuum fluctuations. The deeper question -- whether the distribution of Farey fractions has direct physical consequences in quantum field theory beyond the zeta regularization technique -- remains open.

---

## 9. Quasicrystals, Penrose Tilings, and Fibonacci Anyons

**Rating: STRONG**

### Quasicrystals and the Stern-Brocot Tree

Quasicrystals are the most direct physical realization of Stern-Brocot/continued fraction mathematics in condensed matter physics.

**Key facts:**
- Quasicrystals have long-range order with forbidden symmetries (5-fold, 10-fold). Discovered by Shechtman (1982), Nobel Prize 2011.
- The golden ratio phi = (1+sqrt(5))/2 governs the fundamental ratios in quasicrystal structure.
- phi has continued fraction [1; 1, 1, 1, ...] -- all 1s -- making it the "most irrational" number (hardest to approximate by rationals, slowest continued fraction convergence).
- Rational approximants to quasicrystals (periodic structures approximating the quasiperiodic one) correspond to truncating the continued fraction of phi at successive Fibonacci ratios: 1/1, 2/1, 3/2, 5/3, 8/5, 13/8, ... These are exactly the Stern-Brocot tree convergents to phi.
- The Penrose tiling (2D quasicrystal model) has tile ratios governed by phi, and the sequence of wide/narrow rows follows the Fibonacci sequence.

### Electron States in Quasicrystals

- Electronic states in quasicrystals lack Bloch periodicity, so standard band theory fails.
- The density of states shows quasiperiodic structure linked to the tiling topology.
- Experimental imaging of electronic states in a synthetic Penrose tiling (Nature Communications, 2017) confirmed quasiperiodic electronic order.
- The Hofstadter butterfly (energy spectrum of electrons in a 2D lattice with magnetic field) has a fractal structure organized by the Farey sequence -- gaps in the spectrum occur at rational magnetic flux values, ordered by the Farey tree.

### Fibonacci Anyons and Topological Quantum Computing

A rapidly developing frontier (2022-2025):

1. **Fibonacci anyons**: Quasiparticles whose fusion rules produce Hilbert space dimensions following the Fibonacci sequence. They are computationally universal -- any quantum gate can be approximated by braiding Fibonacci anyons.

2. **Quasicrystal-anyon connection**: Amaral et al. (Symmetry, 2022) showed an isomorphism between the Fibonacci anyon fusion Hilbert space and lattice Hilbert spaces of quasicrystal tilings. Both have Fibonacci-dimensional subspaces. This suggests quasicrystals as physical platforms for topological quantum computing.

3. **Topological superconductivity in Fibonacci quasicrystals**: Kobialka et al. (Phys. Rev. B, 2024) showed that Fibonacci quasicrystal arrangements of magnetic atom chains on superconductors create additional topological regions with Majorana bound states.

4. **Experimental braiding**: Non-Abelian braiding of Fibonacci anyons demonstrated on a superconducting processor (Nature Physics, 2024).

5. **Quasicrystal inflation codes**: Fibonacci anyon braiding simulated within qubit quasicrystal inflation codes (arXiv, 2025), with exact local 3-qubit braid operators derived from Fibonacci tiling constraints.

### Assessment

This is STRONG because:
- The Stern-Brocot/continued fraction connection to quasicrystals is mathematically exact
- Electron states in quasicrystals are experimentally observed
- The Fibonacci/golden ratio structure governs both the crystallography and the quantum electronic properties
- Fibonacci anyons in quasicrystals are an active research frontier with experimental demonstrations

---

## 10. Open Problems and Opportunities

### Established and Active (high confidence these matter)

1. **Farey-organized periodic orbit quantization of atoms in fields**: Extending Cvitanovic's cycle expansion methods to higher-accuracy computation of atomic spectra in combined electric and magnetic fields. The convergence of cycle expansions for non-hyperbolic (intermittent) systems like the Farey map remains an active problem.

2. **Quasicrystal topological quantum computing**: Can real quasicrystal materials host Fibonacci anyons for fault-tolerant quantum computation? The isomorphism between quasicrystal tiling spaces and anyon fusion spaces needs physical realization.

3. **Hofstadter butterfly and Farey gaps**: Complete understanding of the fractal gap structure of the Hofstadter spectrum in terms of Farey arithmetic. Connections to topological invariants (Chern numbers) of the gaps.

### Promising but Underexplored (moderate confidence)

4. **Doubly excited Rydberg atoms as "planetary systems"**: Applying celestial mechanics tools (Farey resonance ordering, KAM stability analysis) to predict lifetimes and decay channels of doubly excited states. The "pendular-planet states" discovered in 2025 suggest this analogy has more to give.

5. **Farey structure of quantum accelerator modes**: Extending the Buchleitner et al. (2006) results to higher-order modes deeper in the Farey tree. Can one observe "noble" (golden-ratio-related) modes that are maximally stable?

6. **Madelung rule from number theory**: Is there a number-theoretic explanation for the electron filling order in multi-electron atoms? The (n+l, n) ordering has no first-principles derivation.

7. **Spectral zeta functions and Farey discrepancy**: Can the distribution of quantum energy levels be related to Farey discrepancy bounds? The connection through the Riemann zeta function is suggestive but not yet made precise.

### Speculative (lower confidence, but potentially transformative)

8. **Inter-electron resonances in atoms**: Do electron-electron frequency ratios in multi-electron atoms show Farey ordering? This would require semiclassical analysis of correlated electron motion in atoms with 3+ electrons.

9. **Hydrogen transition frequencies and Farey structure**: The Rydberg formula produces rational frequency ratios. Do these rationals, when ordered by the Farey sequence, reveal structure in atomic spectra that is invisible in the usual spectral series ordering (Lyman, Balmer, etc.)?

10. **RH connection through atomic physics**: The Riemann Hypothesis is equivalent to bounds on Farey discrepancy. Spectral zeta functions of quantum systems are analogues of the Riemann zeta function. Can physical constraints on quantum spectra (positivity, unitarity, causality) inform the RH? The Hilbert-Polya approach (2025 supersymmetric QM paper) is the latest attempt.

---

## Summary Rating Table

| # | Topic | Rating | Status |
|---|-------|--------|--------|
| 1 | Quantum numbers as Farey/SB structure | SPECULATIVE | No published connection |
| 2 | Bohr-Sommerfeld / EBK quantization | MODERATE | CF convergents approximate quantizing tori |
| 3 | Gutzwiller trace formula / periodic orbits | **STRONG** | Farey = natural orbit classification |
| 4 | Rydberg atoms in external fields | **STRONG** | KAM + CF = established framework |
| 5 | Quantum chaos (H in B field) | **STRONG** | Farey tree of Arnold tongues observed |
| 6 | Shell filling (2n^2) | SPECULATIVE | Lie group symmetry, not number theory |
| 7 | Multi-electron resonances | SPECULATIVE | Analogy exists, not yet explored |
| 8 | Zeta function / Casimir effect | MODERATE | Same zeta function, indirect link |
| 9 | Quasicrystals / Fibonacci anyons | **STRONG** | Exact CF/SB structure, active frontier |
| 10 | Open problems | -- | Several promising directions identified |

---

## Key References (Chronological)

### Foundational
- Einstein, A. (1917). On the quantum theorem of Sommerfeld and Epstein. Verh. Dtsch. Phys. Ges. 19, 82.
- Gutzwiller, M. C. (1990). Chaos in Classical and Quantum Mechanics. Springer.
- Cvitanovic, P. et al. (1990). Recycling of strange sets: Cycle expansions. Nonlinearity 3, 325.

### Quantum Chaos and Atoms
- Friedrich, H. & Wintgen, D. (1989). The hydrogen atom in a uniform magnetic field -- An example of chaos. Physics Reports 183, 37.
- Delande, D. & Gay, J.C. (1986). Quantum chaos and statistical properties of energy levels. Phys. Rev. Lett. 57, 2006.
- Cvitanovic, P. et al. (1998). Beyond the periodic orbit theory. Nonlinearity 11, 1209.

### Farey Tree in Quantum Systems
- Buchleitner, A. et al. (2006). Quantum accelerator modes from the Farey tree. Phys. Rev. Lett. 96, 164101.
- Wintgen, D. et al. (2007). Hydrogen atom in crossed E and B fields: Torus quantization via periodic orbits. Phys. Rev. A 75, 023406.

### Quasicrystals and Topology
- Shechtman, D. et al. (1984). Metallic phase with long-range orientational order and no translational symmetry. Phys. Rev. Lett. 53, 1951.
- Collins, L.C. et al. (2017). Imaging quasiperiodic electronic states in a synthetic Penrose tiling. Nature Comm. 8, 15961.
- Amaral, M. et al. (2022). Exploiting anyonic behavior of quasicrystals for topological quantum computing. Symmetry 14, 1780.
- Kobialka, A. et al. (2024). Topological superconductivity in Fibonacci quasicrystals. Phys. Rev. B 110, 134508.
- Xu, S. et al. (2024). Non-Abelian braiding of Fibonacci anyons with a superconducting processor. Nature Physics.

### Zeta Functions in Physics
- Elizalde, E. et al. (1994). Zeta regularization techniques with applications. World Scientific.
- Kleban, P. & Ozluk, A.E. (1999). A Farey fraction spin chain. Commun. Math. Phys.
- Knauf, A. (1999). Number theory, dynamical systems and statistical mechanics.

### Semiclassical Torus Quantization
- Takahashi, S. & Takatsuka, K. (2004). How periodic orbits converge to quantizing tori. Phys. Rev. A.

---

## Conclusion: Where Farey Meets the Atom

The strongest connections between Farey/Stern-Brocot/continued fraction structures and electron physics occur in three domains:

1. **Semiclassical atomic physics**: The Gutzwiller trace formula, periodic orbit classification, and quantum chaos in atoms under external fields. Here the Farey sequence is the natural organizational scheme for periodic orbits that determine quantum spectra.

2. **Quasicrystal physics**: The golden ratio, Fibonacci sequence, and continued fraction approximants govern both the atomic structure of quasicrystals and the quantum states of electrons within them. Fibonacci anyons provide a bridge to topological quantum computing.

3. **KAM theory applied to atoms**: Continued fractions determine which electron orbits are stable under perturbation, creating an exact analogy between atomic "Kirkwood gaps" and asteroid belt gaps.

The weakest connections are to the static quantum number structure of atoms (which is governed by Lie group symmetry, not number theory) and to shell filling patterns (which depend on the specific form of the Coulomb potential rather than on arithmetic properties of integers).

The most promising open direction for original research is applying Farey-based tools to **doubly excited Rydberg atoms** -- a domain where the celestial mechanics analogy is physically exact but number-theoretic tools have not yet been systematically deployed.
