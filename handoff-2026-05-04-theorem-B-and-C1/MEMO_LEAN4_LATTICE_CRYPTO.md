# Technical Memo: Lean 4 Support for Lattice-Based Cryptography Security Proofs

**Author:** Saar Shai
**Date:** 2026-05-02
**Status:** Draft v3

## Summary

Lean 4 verification, as developed in this project, can mechanize the
non-hardness obligations of lattice-based security proofs: sampler support,
parameter inequalities, normalization conventions, encoding/decoding
correctness, failure-probability bookkeeping, and reduction-interface
discipline. Cryptographic hardness assumptions (LWE, Module-LWE, SIS,
Module-SIS) remain external. The project's current number-theoretic Lean
work — completed Lean proofs of explicit-formula kernel constants, plus
boundary-formalization of Petersson family-average machinery — is a working
demonstration of that same split applied to a different but structurally
similar domain.

**Top points.**

- Lean 4 can certify **sampler contracts** for centered-binomial,
  bounded-uniform, rejection, and discrete-Gaussian samplers used in ML-KEM
  and ML-DSA.
- Lean 4 can certify **parameter, normalization, and NTT invariants**
  (modulus q, q ≡ 1 mod 2n, ring/module dimensions, compression bit-widths,
  Cooley–Tukey indexing, twiddle tables) that informal proofs assume
  implicitly.
- Lean 4 can certify **algebraic correctness** of encode/decode and
  compression/decompression, plus the inequalities that bound decapsulation
  failure probability δ and propagate it through the IND-CCA2 reduction
  after the Fujisaki–Okamoto transform.
- Lean 4 can formalize the **reduction interface** to LWE / Module-LWE /
  Module-SIS — game definitions, hybrid transitions, distribution-replacement
  preconditions — exposing exactly which assumptions the reduction needs
  (precedents: CryptHOL formalized LWE + BDD→LWE; SSProve formalized an
  LWE-PKE IND-CPA reduction; EasyCrypt formalized full Module-LWE→Kyber).
- Lean 4 can certify **constant-time / secret-independence policy** on a
  Lean reference implementation, supplying the upstream half of the
  side-channel argument that Jasmin/F\* discharge at the machine-code level.
- Lean 4 cannot prove the underlying lattice problems hard. Hardness stays
  in the assumption set, explicit and auditable.
- Concrete software claims still require a verified-code or extraction link
  (e.g., Lean → C, or pairing with Jasmin / F\* artefacts).

## Why Lean 4 fits lattice cryptography

NIST has standardized module-lattice schemes through **FIPS 203** (ML-KEM,
Module-Lattice-Based KEM) and **FIPS 204** (ML-DSA, Module-Lattice-Based
Digital Signature), both finalized in 2024. These specifications hinge on
finite rings/modules over ℤ_q, bounded noise distributions (centered binomial
η), hash-derived randomness (XOF / SHAKE), NTT-friendly polynomial rings
(ℤ_q[X]/(X^n+1) with q=3329 for ML-KEM, q=8380417 for ML-DSA),
compression/decompression maps, and stated failure-probability bounds. Small
deviations in sampling, normalization, or encoding can invalidate the
informal proof's assumptions without invalidating the surface API.

Lean 4 + mathlib4 supplies the relevant ingredients: finite types, ZMod q,
polynomial rings and quotients, finite-support distributions, rewriting and
linear-arithmetic tactics, and a kernel small enough to audit. The Post-Bias
Lean artefacts already exhibit the right object pattern (`SamplerSpec`,
`rejection_sample_support_correct`, `avoid_list_sound`); the lattice analogues
are direct rewrites over (ℤ_q)^n / R_q^k modules.

## Concrete Lean 4 contributions

**1. Formal sampler contracts.** State and prove:

- every coefficient of the sampled secret/error vector lies in the declared
  bounded support (e.g., centered-binomial η on {-η,…,η});
- the output has the declared dimension k or polynomial degree < n;
- rejection sampling does not output forbidden values (exact support of the
  conditional distribution);
- deterministic seed expansion via XOF is modeled as an explicit oracle
  assumption rather than hidden in prose;
- any modeled implementation optimization preserves the declared output
  distribution.

**2. Parameter, normalization, and NTT invariants.** Lattice proofs depend
on arithmetic identities a code-level reviewer cannot easily audit: q
prime, q ≡ 1 mod 2n so that 2n-th roots of unity exist for NTT,
compression `Compress_q(x,d) = ⌈(2^d/q)·x⌋ mod 2^d`, Barrett/Montgomery
reductions, modular inverse conventions, Cooley–Tukey / Gentleman–Sande
butterfly indexing, twiddle-factor tables. Lean can state these as
`Decidable` propositions or computed lemmas and prove the NTT/inverse-NTT
round-trip identity, refusing specifications that fail them. The Almeida
et al. EasyCrypt/Jasmin Kyber proof and the F\* HACL\* implementations
both exhibit verified NTT layers; the Lean 4 contribution is to do this
inside mathlib4's polynomial-ring framework rather than against a
specialized DSL.

**3. Correctness and failure-probability bookkeeping.** For ML-KEM-style
KEMs, decapsulation correctness reduces to a coefficient inequality of the
form `‖e₁·s + e₂ − e·r + Δ‖_∞ < ⌈q/4⌋`. Lean separates:

- algebraic correctness of encode/decode and compress/decompress (exact);
- coefficient-bound inequalities relating noise parameter η and modulus q;
- finite-domain / probabilistic bounds on coefficient growth in the formal
  model;
- the δ-failure bound entering the IND-CCA2 game-hop after the Fujisaki–
  Okamoto transform (the precedent in Almeida et al. is to model δ
  explicitly and propagate it through the reduction);
- explicit oracle assumptions on randomness and hash functions.

The benefit is proof hygiene: which inequalities are theorems, which
remain assumptions, and how δ propagates into the final security bound.

**4. Reduction-interface checking.** Security proofs reduce attacks to
LWE / Module-LWE / SIS / Module-SIS. Lean formalizes:

- game definitions and adversary signatures;
- hybrid transitions (IND-CPA → IND-CCA via FO transform);
- the exact preconditions under which a distribution may be replaced by a
  uniform one (LWE indistinguishability hypothesis, with parameters);
- the constraint that no extra assumption is silently introduced by an
  optimization or parameter change.

This catches the common failure where a proposal claims a known reduction
while using a sampler, normalization, or parameter set the reduction did
not cover. Precedent in adjacent assistants: CryptHOL has formalized
LWE plus a BDD→LWE reduction (Lochbihler); SSProve has formalized an
LWE-based PKE IND-CPA reduction; EasyCrypt has the full Module-LWE→Kyber
IND-CCA2 reduction. None of these has been replicated in Lean 4 — a
clear deliverable.

**5. Constant-time / secret-independence at the model level.** Side-channel
resistance is part of the security argument for ML-KEM and ML-DSA, not an
afterthought. Jasmin and F\* express this as an information-flow property
of compiled code. Lean 4 cannot, alone, certify constant-time machine
code, but it can certify constant-time *policy* on a Lean reference
implementation: every branch and memory access depending on secret data
is rejected by a type/effect discipline or an explicit predicate. This
is the upstream half of the constant-time proof; the downstream
machine-code half still requires a verified-code link (Jasmin, CompCert,
or future Lean→C extraction).

## Methodology bridge from current project

The project's current number-theoretic work is not lattice cryptography, and
no claim about ML-KEM, ML-DSA, LWE, or Module-LWE is asserted on its basis.
It does, however, demonstrate the same Lean-4 workflow this memo proposes,
applied to analytic-number-theory objects:

- **Completed Lean proof: explicit-formula kernel constant.** The kernel
  constant `c_W = -γ_E - E₁(1)` (Euler–Mascheroni minus exponential integral
  at 1) for the project's L-function explicit-formula machinery has a
  finished Lean 4 proof. This is exactly the split proposed for lattice
  crypto: formalize the part that admits a closed-form theorem, leave the
  surrounding analytic inputs explicit.
- **Boundary formalization: Petersson family-average machinery.** The
  Petersson trace formula and second-moment bounds for weight-2 newforms
  (Iwaniec–Sarnak, Kowalski–Michel–VanderKam) carry Lean boundary work
  separating what is formally derived from what is assumed (zero-density
  bounds, GRH-substitute hypotheses).
- **Distributional proof hygiene.** A recent normalization episode in the
  per-curve `L'/L(1, sym²f)` refit caught a pari/gp arithmetic-vs-analytic
  norm mismatch (`a_p² − p` vs `λ_p² − 1`, FE `s ↔ 3-s` vs `s ↔ 1-s`) that
  shifted the regression MAE from ≈ 1.55 to ≈ 0.13 once the integer-shift
  identity `(L'/L)_anal(1, sym²f) = (L'/L)_arith(2, sym²f)` was applied.
  This is structurally the same hazard a lattice sampler/parameter contract
  is designed to catch: same name, different distribution or
  normalization, broken proof.

The methodological transfer:

> The number-theoretic Lean work gives this project a tested formalization
> discipline — isolate the exact mathematical object, prove what can be
> proved, keep analytic or hardness inputs explicit — that we will transfer
> to cryptographic sampler and parameter verification.

## Related formal-verification precedents

Lattice-cryptography formal verification is active across proof assistants;
Lean 4 is one of several viable substrates. Relevant precedents:

- **EasyCrypt + Jasmin verified ML-KEM / Kyber** — Almeida, Barbosa, Barthe,
  Grégoire, Laporte, Oliveira, Pacheco, Schwabe, Strub et al. End-to-end
  verified Kyber implementation: IND-CCA2 security reduction to Module-LWE
  in EasyCrypt (modeling the Fujisaki–Okamoto transform and δ failure
  bound), constant-time machine code in Jasmin. IACR ePrint 2021/745;
  IEEE S&P. Closest precedent for the sampler/parameter/correctness/
  reduction factoring this memo proposes.
- **HACL\* / EverCrypt** (F\*, Protzenko, Bhargavan, Polubelova,
  Zinzindohoue et al.) — verified low-level cryptographic primitives with
  code extraction to C, including post-quantum primitives. HACL\*: Zinzindohoue
  et al., ACM CCS 2017. EverCrypt: Protzenko et al., USENIX Security.
  Precedent for the Lean → verified-code link required for production claims.
- **SSProve** (Abate, Haselwarter, Rivas, Scherer, Tabareau, Tassarotti,
  Winterhalter et al., Coq) — foundational framework for modular game-based
  cryptographic proofs; CSF 2021, arXiv:2104.11322. Demonstrated on an
  LWE-based PKE IND-CPA reduction (LWE hardness axiomatized). The
  reduction-interface pattern in §4 above is the Lean analogue.
- **CryptHOL** (Lochbihler, Isabelle/HOL) — probabilistic-program semantics
  for cryptographic reductions; demonstrates hybrid-argument formalization
  and has been used to formalize the LWE problem and basic LWE-PKE
  IND-CPA security.
- **FCF — Foundational Cryptography Framework** (Petcher & Morrisett, Coq,
  ITP 2015) — probabilistic relational Hoare logic; general-purpose, mostly
  applied to classical schemes. Useful methodology precedent.
- **Barthe–Grégoire–Zanella-Béguelin, "Computer-aided cryptography"** (CACM,
  survey) — vision and methodology of computer-aided crypto proofs that
  EasyCrypt later realized for Kyber.
- **mathlib4** — Lean 4 mathematical library; supplies finite group/ring
  algebra, polynomial rings, ZMod, probability mass functions (`PMF`),
  `Mathlib.Probability.*`. Foundation present; PQC-specific layer not yet
  built.
- **NIST FIPS 203 / FIPS 204** (2024) — final standards; the formal target
  specifications. NIST IR 8413 (Moody et al., 2022) gives the standardization
  status report.

## Lean 4 Strengths

1. **Unified substrate.** Existing efforts split across EasyCrypt (proofs) +
   Jasmin (code) + Coq/Isabelle (foundations). Lean 4 + mathlib4 can
   plausibly cover lattice mathematics, game-based proofs, and a Lean-native
   reference implementation in one kernel.
2. **Foundational reductions.** CryptHOL has BDD→LWE; further core
   reductions (GapSVP→LWE, Module-LWE↔LWE) are not mechanized in any
   assistant in completed form. mathlib4's algebra and probability give
   Lean a plausible path here.
3. **Advanced sampler verification.** The Falcon FFT-based discrete
   Gaussian sampler, with its floating-point arithmetic, has resisted
   end-to-end formal proof. Lean 4's metaprogramming and computable
   real-arithmetic developments are candidate tooling.
4. **Tactic automation for game-hopping.** Reduction proofs are still
   highly manual in SSProve / EasyCrypt. Lean 4's tactic and elaboration
   framework permits domain-specific automation for distribution-replacement
   and probability-bound steps.
5. **Verified-in-Lean reference implementation.** Lean 4 compiles to native
   code, narrowing the model–code gap relative to assistants without
   executable semantics.

(The continuous methodology this project already exercises - on adjacent
number-theoretic objects (kernel-constant proof, Petersson-boundary
formalization, normalization-mismatch capture) - supplies a tested working
discipline for entering this gap.

