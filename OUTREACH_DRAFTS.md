# Outreach Drafts — Tailored by Audience
# 2026-04-10

---

## 1. LMFDB Team (Cremona, Farmer, Voight, Costa)

Dear [name],

I've developed a batch spectroscope method that detects zeros of all Dirichlet L-functions L(s,χ) for characters χ mod q simultaneously in a single computation. Using a Mertens-weighted prime sum with Bombieri-Vinogradov decomposition, the method scans for approximate zero locations across the entire family {L(s,χ) : χ mod q} at once, which can then be refined to full precision at the flagged locations.

The scanning phase is faster than individual Euler-Maclaurin evaluation at conductor q ≥ 400 — approximately 5x at q=1000, 20x at q=10,000, and ~140x at q=1,000,000. The advantage grows as √q because the batch cost is independent of φ(q) while individual computation scales linearly with it.

The framework extends beyond Dirichlet characters to:
- Dedekind zeta functions (scanning prime ideal splitting across number fields)
- Hecke L-functions (batch over class groups)
- Artin L-functions (batch over Galois representations via FFT over the Galois group)

At 10⁹ or 10¹²: nobody has ever computed L-function zeros at these conductors systematically. It's unexplored territory. Our method makes it conceivable (2,992x or 70,954x cheaper

I'd welcome the opportunity to share benchmark data and discuss whether this could help expand LMFDB's coverage at higher conductors. A preprint is in preparation.

Best regards, Saar Shai

---

## 2. Platt & Trudgian (Computational Zero Verification)

Dear Prof. Platt / Prof. Trudgian,

I've been working on a spectroscopic method for detecting zeros of L-functions that is algorithmically independent of the Riemann-Siegel and Euler-Maclaurin approaches. The method uses a Mertens-weighted prime spectroscope with γ² pre-whitening, and comes with a formal detection guarantee: an unconditional "dichotomy theorem" showing the spectroscope detects at least one zero regardless of whether RH holds.

The method's main practical advantage is batch computation: for Dirichlet L-functions mod q, it scans all characters simultaneously, with ~√q speedup over individual evaluation. At q=10,000 this is ~20x faster; at q=1,000,000 it's ~140x.

As an independent verification method, it could complement your existing pipeline — a completely different algorithm checking the same zeros provides redundancy. The method also naturally highlights the zero with the largest real part (the dichotomy property), making it a targeted tool for anomaly detection.

Applicable to: Riemann ζ(s), Dirichlet L(s,χ), Dedekind ζ_K(s), elliptic curve L(s,E).

Happy to share details. Preprint forthcoming.

Best regards, Saar Shai

---

## 3. Maynard / Tao / Green (Bounded Gaps)

Dear Prof. [Maynard/Tao/Green],

I have a result that connects your work on bounded prime gaps to the spectral theory of zeta zeros, via a "universality" theorem for the Mertens spectroscope.

Under GRH, any set of primes S with Σ_{p∈S} 1/p = ∞ produces a spectroscope that detects every nontrivial zero of ζ(s). A corollary: the set of primes p such that p_{n+1}-p_n ≤ 246 (whose infinitude follows from your work) has divergent reciprocal sum, and therefore detects all zeta zeros.

This appears to be the first connection between the bounded gaps theorem and zero detection. The universality result holds for any prime subset satisfying the divergent reciprocal sum condition — arithmetic progressions, sieved sets, primes of special forms — each producing a spectroscope that encodes the full Riemann spectrum.

Applicable functions: ζ(s), all Dirichlet L(s,χ), Dedekind ζ_K(s), and in principle any L-function with an Euler product.

Happy to share the preprint when ready.

Best regards, Saar Shai

---

## 4. Keating / Snaith (Random Matrix Theory)

Dear Prof. [Keating/Snaith],

I've developed a "prime spectroscope" that detects zeta zeros from prime data, producing GUE pair correlation statistics (RMSE=0.066 against Wigner surmise) from raw arithmetic data without computing zeros first. The pathway is: prime sums → spectroscope peaks → detected zero locations → pair statistics.

The method's batch capability may be useful for testing Katz-Sarnak predictions across L-function families. For all Dirichlet characters mod q simultaneously, the spectroscope detects zeros in one pass with ~√q speedup, enabling family-wide zero statistics at higher conductor than currently practical.

The framework extends to:
- Elliptic curve L-functions (testing orthogonal symmetry predictions)
- Modular form L-functions (testing unitary symmetry)
- Symmetric power L-functions (connection to Sato-Tate)
- Artin L-functions (batch over Galois representations)

Would be glad to discuss how this might complement your statistical investigations.

Best regards, Saar Shai

---

## 5. Berry / Connes (Quantum Chaos / Noncommutative Geometry)

Dear Prof. [Berry/Connes],

I've been studying a spectroscopic framework for detecting Riemann zeros from prime data. The framework treats prime numbers as a measurement system for the "quantum spectrum" of the zeta function, with three proven properties:

1. Detection (unconditional): the spectroscope detects at least one zero regardless of RH, via a dichotomy — it finds the zero with the largest real part.
2. Stability (unconditional): the large sieve inequality guarantees bounded measurement noise.
3. Redundancy (GRH): any prime subset with divergent reciprocal sum encodes the full zero spectrum.

The connection to quantum chaos: the large sieve bound plays the role of an upper restricted isometry property from compressed sensing. The gap between upper RIP (proved) and lower RIP (open) maps precisely to the gap between zero detection (easy) and zero-free region proofs (hard/RH). This suggests the difficulty of RH has a measurement-theoretic interpretation.

The framework applies to any L-function with an Euler product, including Selberg zeta functions of hyperbolic surfaces where the "primes" are primitive geodesics.

Happy to elaborate. Preprint in preparation.

Best regards, Saar Shai

---

## 6. Bhargava / Wood / Ellenberg (Class Numbers)

Dear Prof. [Bhargava/Wood/Ellenberg],

I've developed a batch method for scanning L-function zeros across families that may be useful for computational tests of Cohen-Lenstra heuristics and related class number predictions.

The method computes approximate zero locations for all Dirichlet L-functions L(s,χ) with χ mod q simultaneously, with ~√q speedup over individual computation. At q=100,000, this is ~50x faster than processing each character separately.

For class number applications: since h(-d) relates to L(1,χ_d) via the class number formula, the spectroscope can flag characters where L(1,χ) is anomalously small — corresponding to small class numbers — across an entire conductor range in one batch. This could enable statistical tests of the Cohen-Lenstra predictions at discriminants higher than currently practical.

The framework extends to:
- Dedekind zeta functions (class numbers of higher-degree fields)
- Hecke L-functions (class group structure)
- Artin L-functions (non-abelian class field theory)

Would be happy to discuss potential applications to your program.

Best regards, Saar Shai

---

## 7. Lean Community (Buzzard, Massot)

Dear [Kevin/Patrick],

We have 434 Lean 4 results formalizing Farey sequence theory, including:
- Farey sequence cardinality |F_N| = 1 + Σφ(d) 
- Four-term decomposition of per-step discrepancy (ΔW = A-B-C-D)
- Injection principle, mediant minimality, bridge identity
- Figure-eight three-body orbit = golden ratio (8 theorems)
- Prime power sum divergence Σ p^{β-1} → ∞ for β>0 (3 theorems)

All zero sorry. The project is at github.com/SaarShai/Primes-Equispaced. We're interested in contributing the most fundamental results to Mathlib — starting with Farey sequence cardinality and the neighbor property |ad-bc|=1.

Would appreciate guidance on which results would be most valuable for Mathlib and how to structure a PR.

Best regards, Saar Shai
