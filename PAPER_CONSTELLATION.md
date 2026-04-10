# Paper Constellation — Linked Papers, Each Telling One Story

## Design Principles
- Each paper has ONE central discovery
- Each is self-contained (reader doesn't need the others)
- Cross-references link them ("In [companion paper], we show...")
- Each targets the RIGHT reviewers for its topic
- Short, focused, publishable independently

---

## Paper A: "Per-Step Farey Discrepancy and the Prime-Composite Asymmetry"
**Central story:** ΔW(N) is a new object. Primes damage, composites heal.
**Content:**
- Definition of ΔW(N), basic properties
- Four-term decomposition (A-B-C-D)
- Damage/response mechanism
- D(1/p) = 1 - |F_p|/p dominance (65%)
- Injection Principle (each fraction enters a distinct gap)
- Computational evidence through N=100,000
- Lean 4 verification of core identities
**Target:** Experimental Mathematics or Journal of Number Theory
**Audience:** Farey sequence researchers, computational number theorists
**Length:** ~15 pages

## Paper B: "The Chebyshev Bias in Farey Sequences: Phase and Oscillation"
**Central story:** sgn(ΔW(p)) correlates with zeta zeros via explicit formula.
**Content:**
- Sign pattern: R=0.77 correlation with cos(γ₁ log p + φ)
- Phase φ = -arg(ρ₁·ζ'(ρ₁)) derived exactly (match mod 2π)
- Connection via Bridge Identity → M(p) → explicit formula
- Sign flip at p=243,799 explained by Chebyshev framework
- Rubinstein-Sarnak density prediction
**Target:** Mathematics of Computation
**Audience:** Analytic number theorists, Chebyshev bias researchers
**Length:** ~12 pages

## Paper C: "Prime Spectroscopy of Riemann Zeros" (MAIN PAPER)
**Central story:** Primes form a compressed sensing system for zeta zeros. Three theorems: detection, redundancy, stability.
**Content:**
- Spectroscope definition: F(γ) = γ²|Σ M(p)/p · e^{-iγ log p}|²
- Theorem 1 (Dichotomy, UNCONDITIONAL): spectroscope detects zeros regardless of RH
- Theorem 2 (Universality, GRH): any Σ1/p=∞ subset detects all zeros
  - Bounded gaps corollary (Maynard-Tao primes detect zeros)
  - Quantitative threshold: Σ1/p ≥ C(loglog T)^{1+ε}
- Theorem 3 (Upper RIP, UNCONDITIONAL): large sieve = restricted isometry property
  - Deterministic RIP: prime-indexed Fourier matrix as candidate for open CS problem
  - Resolution limit: 2π/log P
  - Phase transition: N* ~ (logP)²/2π matches 2750 observation
- Computational verification: 20/20 zeros, phase match to 0.003 rad, 5-term R=0.876
- Brief: GUE pair correlation (RMSE=0.066) as application
- Honest negatives: amplitude anti-correlates, pre-whitening is classical
**Target:** IMRN or Compositio Mathematica (NT); IEEE Trans. IT (CS community)
**Audience:** Analytic number theorists, compressed sensing researchers, computational NT
**Length:** 30-40 pages
**Focus:** One framework, three properties: detection → redundancy → stability.

## Paper D: "Universality: Every Prime Subset Encodes the Zeta Zeros"
**Central story:** Any 2750 primes detect all zeros. Holographic encoding.
**Content:**
- Computational demonstration across subset types
- Twin primes, residue classes, random subsets all work
- |M(p)| collapses — signed oscillation essential
- Interval-restricted subsets fail — range spanning required
- Conditional proof (GRH+LI+VK)
- Variance approach for unconditional result (open problem)
- Minimum subset analysis
**Target:** Proceedings of the AMS or IMRN
**Audience:** Analytic number theorists, information theorists
**Length:** ~12 pages

## Paper E: "GUE Statistics from Prime Arithmetic Data"
**Central story:** Random matrix pair correlation from spectroscope, not computed zeros.
**Content:**
- 20 detected zeros → 190 pairs → GUE RMSE=0.066
- Nearest-neighbor spacing matches Wigner surmise
- Level repulsion visible
- Montgomery connection via Wiener-Khinchin
- GUE regularization approach (open: W-K for distributions)
**Target:** Communications in Mathematical Physics or Journal of Statistical Physics
**Audience:** Random matrix theorists, mathematical physicists
**Length:** ~10 pages

## Paper F: "A Spectroscopic Test for the Chowla Conjecture"
**Central story:** New methodology for testing Chowla with explicit thresholds.
**Content:**
- Methodology: μ(n) periodogram normalized by |1/ζ(1+iγ)|²
- Detection threshold ε = 1.824/√N
- Evidence FOR Chowla at N=200K (CV=1.47%, 78x flatter than null)
- The false alarm and its resolution (|1/ζ| envelope)
- Unweighted test with σ=0.1 smoothing
- Direct lag-h verification (√N cancellation)
**Target:** Mathematika or Quarterly Journal of Mathematics
**Audience:** Analytic number theorists working on multiplicative functions
**Length:** ~10 pages

## Paper G: "Spectroscopic Verification of L-function Zeros"
**Central story:** The spectroscope generalizes to all degree-1 L-functions, with Siegel zero sensitivity.
**Content:**
- Twisted spectroscope F_χ for Dirichlet characters
- 108 characters surveyed, systematic GRH verification pipeline (5/7 matches at 500K)
- Siegel zero sensitivity: 465M sigma detection for q≤13
- Deuring-Heilbronn repulsion → spectroscope advantage for Siegel detection
- Dedekind zeta of Q(i) via combined spectroscope (ζ·L(s,χ₄) factorization)
- Detection thresholds as function of conductor q
**Target:** LMS Journal of Computation and Mathematics
**Audience:** Computational L-function community, LMFDB contributors, Siegel zero specialists
**Length:** ~15 pages
**Focus:** Degree-1 L-functions. Assumes reader knows the method from Paper C.

## Paper G': "Spectroscopy of Automorphic L-functions" (CONDITIONAL — needs computation)
**Central story:** Spectroscope reaches modular forms and elliptic curves.
**Content:**
- Tau spectroscope: τ(n) coefficients → L(s,Δ) zeros (Ramanujan connection)
- Elliptic curve spectroscope: a_p(E) → L(s,E) zeros (BSD connection)
- Possibly symmetric power L-functions (degree 3+)
- Comparison: what changes when coefficients aren't ±1?
**Target:** IMRN or Journal of Number Theory
**Audience:** Modular forms community, BSD specialists — different from G's audience
**Length:** ~10-12 pages
**Status:** Designs ready (19KB + 20KB), NO computation yet. Paper exists IFF computation detects zeros.
**Fallback:** If results are weak, tau/elliptic become "further directions" section in Paper G.

## Paper H: "Continued Fraction Invariants of Three-Body Periodic Orbits"
**Central story:** CF periodic table organizes 695 orbits. Figure-eight = golden ratio.
**Content:**
- F₂ = Γ(2) < SL(2,ℤ) bridge
- Exact surd arithmetic (fixes 17.7% corruption)
- S = arccosh(tr(M)/2) links entropy to CF
- Periodic table (9×8, 51 populated, 21 predictions)
- AUC = 0.980 blind prediction
- Empty cell search strategy
**Target:** Celestial Mechanics and Dynamical Astronomy
**Audience:** Dynamical systems, celestial mechanics
**Length:** ~15 pages

## Paper I: "422 Lean 4 Verified Results on Farey Sequences"
**Central story:** Largest formalization of Farey sequence theory.
**Content:**
- Bridge identity, injection principle, four-term decomposition
- Ramanujan sum evaluations
- Strict positivity results
- Displacement-shift identity
- Mediant minimality
- Contribution to Mathlib
**Target:** Journal of Automated Reasoning or ITP conference
**Audience:** Formal verification community
**Length:** ~12 pages

## Paper J: "An Unconditional Variance Bound for Spectroscopic Zero Detection"
**Central story:** The spectroscope has provably more variance than a zero-free model.
**Content:**
- Variance argument: integral_A^B F(gamma)dgamma exceeds zero-free prediction
- Why Siegel zeros don't affect band [10,18]
- Three identified gaps + repair paths (prime-only framework, off-diagonal, normalization)
- State main result as conjecture with proof strategy
- Include any partial results achieved
- Open problem: close the three gaps
**Target:** Journal of the London Mathematical Society or Acta Arithmetica
**Audience:** Analytic number theorists working on explicit formulas
**Length:** ~12 pages
**Status:** Approach identified, gaps documented, proof in progress

## Paper K: "Farey Sequences over Gaussian Integers"
**Central story:** ΔW extends to Z[i]. 2D discrepancy detects Dedekind zeta zeros.
**Content:**
- Gaussian Farey sequence definition and enumeration (1,344 pts done)
- 2D discrepancy ΔD* at Gaussian primes
- Dedekind zeta ζ_{Q(i)}(s) = ζ(s)·L(s,χ₄) — spectroscope via factorization
- Ford spheres in H³ (hyperbolic 3-manifold perspective)
- Comparison: what survives from ℤ, what's new in Z[i]
**Target:** Journal of Number Theory or Acta Arithmetica
**Audience:** Algebraic number theorists
**Length:** ~12 pages
**Status:** 1,344 pts enumerated. 2D spectroscope not yet computed.

## Paper M: "Horocycle Equidistribution and the Farey Spectroscope"
**Central story:** WHY the spectroscope works — ergodic theory foundation.
**Content:**
- Chain: ΔW → horocycle equidistribution on SL(2,ℤ)\H → spectral gap → zeta zeros
- Ford circles as horodisks in Poincaré disk
- Connection to Marklof-Strömbergsson theory of Farey statistics
- Spectral gap of Laplacian ↔ zero-free region of ζ(s)
- Spectroscope as computational evidence for the equidistribution chain
**Target:** Ergodic Theory and Dynamical Systems or GAFA
**Audience:** Ergodic theorists, homogeneous dynamics — NO overlap with other papers
**Length:** ~15 pages
**Status:** Chain identified (MPR-44), Ford circle figure created. Needs formalization.

---

## Links Between Papers
- A → B (ΔW leads to sign pattern)
- A → C (ΔW data feeds spectroscope)
- B → C (phase from explicit formula validates spectroscope)
- C → D (spectroscope enables universality observation)
- C → E (spectroscope produces zeros for GUE)
- C → F (same periodogram methodology applied to Chowla)
- C → G (spectroscope extends to L-functions)
- G → G' (higher-degree extensions, if computed)
- A → I (Lean verifies Paper A's identities)
- A → K (ΔW extends to new number ring)
- C → M (M explains WHY C works)
- C → J (J proves C must work)
- H stands alone (three-body, different field)

## Priority Order for Writing
1. A (foundation — everything builds on this)
2. C (headline result — THE METHOD)
3. D (most novel observation)
4. B (clean, focused)
5. F (methodology contribution)
6. G (L-function extensions — needs C first)
7. H (ready, different audience)
8. I (Mathlib contribution)
9. J (proof in progress — publish when gaps close or as open problem)
10. K (needs 2D computation)
11. M (needs formalization — highest theoretical ceiling)
12. G' (conditional on tau/elliptic computation results)

## Paper Survey (write last)
"A Survey of Spectroscopic Methods in Analytic Number Theory"
- Expository piece for Bulletin of the AMS or Mathematical Intelligencer
- Tells the whole story for non-specialists
- Written AFTER research papers exist
