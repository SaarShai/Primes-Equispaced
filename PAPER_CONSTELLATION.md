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

## Paper C: "Spectroscopic Detection of Zeta Zeros from Arithmetic Data"
**Central story:** The compensated Mertens spectroscope detects all 20 zeros.
**Content:**
- Spectroscope definition + γ² pre-whitening (cite classical pre-whitening)
- Local z-score normalization (why global z fails)
- 20/20 detection with z up to 65σ
- Scaling analysis (25M optimal)
- Null battery (5/6 tests pass, z=117.6)
- Psi spectroscope comparison
- Honest: amplitude anti-correlates, pre-whitening is classical, application is new
**Target:** Experimental Mathematics
**Audience:** Computational number theorists, spectral analysis community
**Length:** ~18 pages

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

## Paper G: "L-Function Zero Detection via Twisted Spectroscopy"
**Central story:** Spectroscope extends to Dirichlet L-functions and beyond.
**Content:**
- Twisted spectroscope F_χ for 108 characters
- GRH verification pipeline (5/7 matches at 500K)
- Siegel zero sensitivity (465M sigma, q≤50)
- Dedekind zeta of Q(i) via combined spectroscope
- Tau spectroscope for modular forms (if computed)
- Elliptic curve spectroscope (if computed)
**Target:** LMS Journal of Computation and Mathematics
**Audience:** Computational L-function community, LMFDB contributors
**Length:** ~15 pages

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

---

## Links Between Papers
- A → B (ΔW leads to sign pattern)
- A → C (ΔW data feeds spectroscope)
- B → C (phase from explicit formula validates spectroscope)
- C → D (spectroscope enables universality observation)
- C → E (spectroscope produces zeros for GUE)
- C → F (same periodogram methodology applied to Chowla)
- C → G (spectroscope extends to L-functions)
- A → I (Lean verifies Paper A's identities)
- H stands alone (three-body, different field)

## Priority Order for Writing
1. A (foundation — everything builds on this)
2. C (headline result)
3. D (most novel observation)
4. B (clean, focused)
5. F (methodology contribution)
6. H (ready, different audience)
7. I (Mathlib contribution)
8. G (needs more computation)
9. E (needs GUE regularization)
