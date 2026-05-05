---
type: decision
domain: research
title: "Program Reorient — Have We Drifted From the Original Δw(N) Farey Program?"
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
confidence: 0.78
tier: working
sources:
  - /Users/saar/NEW Farey 5.5/projects/farey-research/farey-discrepancy-directions.md
  - /Users/saar/NEW Farey 5.5/projects/farey-research/c1-spectroscope.md
  - /Users/saar/NEW Farey 5.5/projects/farey-research/W2_C1_FINAL_WRAP_2026-05-02.md
  - /Users/saar/NEW Farey 5.5/projects/farey-research/bridge-four-term-franel.md
  - /Users/saar/NEW Farey 5.5/HANDOFF_FAREY_NOVELTY_AND_LEAN_FOUNDATION.md
  - /Users/saar/NEW Farey 5.5/HANDOFF_FAREY_HARD_OPEN_PROBLEMS.md
  - /Users/saar/NEW Farey 5.5/HANDOFF_FAREY_SPECTROSCOPE_UNIFICATION.md
  - /Users/saar/Documents/Spark Obsidian Beast/Design Claude/wiki/Research/Farey-Per-Step-Explicit-Formula.md
  - /Users/saar/Documents/Spark Obsidian Beast/Design Claude/wiki/Research/Farey-C1-W2-Mechanism.md
  - /Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/Bridge_Identity.md
  - /Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/Four_Term_Decomposition.md
  - /Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/Farey_Spectroscope.md
  - /Users/saar/Farey 4.7 solutions/B3_theorem_C_progress.md
  - /Users/saar/Farey 4.7 solutions/AUTONOMOUS_PLAN.md
tags: [farey, program-decision, drift-audit, delta-w, c1, w2, petersson]
---

# Bottom Line

**Drifted, but not fully off-program.** Today's ratios-conjecture results (a_2 closed form, MAE 0.073) are 100% on the C1/W2 modular sub-track. They do NOT directly serve the original Δw(N) per-step Farey discovery. The new unconditional results (Theorem B weight aspect, Theorem C* level-averaged super-family) are on the SAME modular sub-track and similarly do NOT touch Δw(N).

The C1/W2 program is now self-sustaining: it has its own paper, its own Lean formalization, its own 16-curve numerical evidence. It has become a sibling problem to Δw(N), not a tool serving Δw(N).

The eventual paper, as currently structured, will be a GL(2)-modular L-function moments paper (Compositio/Annals analytic NT) — not a Farey paper. The original Farey program (paper 1: Bridge Identity / Four-Term / Δw; paper 2: Farey/Mertens/ψ Spectroscope) is alive but largely orthogonal to today's work.

# What the ORIGINAL Δw(N) Discovery Actually Is

The novel observation is the **per-step prime-insertion delta of the Farey sequence**:

  **Δw_f(N) := Σ_{(a,N)=1} f(a/N) − f̂(0)·φ(N)**

For the canonical character f(x) = e(x) = e^{2πix}, this collapses to the Ramanujan sum:

  **Δw(N) = c_N(1) = μ(N)**       (Möbius!)

Two foundational results sit underneath:

1. **Bridge Identity** (Lean-verified, our discovery): Σ_{f∈F_{p−1}} e^{2πipf} = M(p) + 2. Connects Farey exponential sums directly to Mertens. (`Farey Research/wiki/Bridge_Identity.md`)
2. **Four-Term Decomposition** (Lean-verified, our discovery, corrected 2026-04-13): ΔW(p) = A − B + C − D_term + ... — exact decomposition of the per-step Farey discrepancy with sign-resolution and 33000:1 cancellation phenomenon.
3. **Generating-function structure** (per-step explicit formula, derived 2026-05-02): D_f(s) := Σ Δw_f(N)/N^s = G_f(s) / ζ(s) with G_f(s) = Σ_{m≠0} f̂(m) σ_{1−s}(|m|). Contour shift gives Δw_f(N) = Σ_ρ [G_f(ρ)/ζ'(ρ)] · [N^ρ − (N−1)^ρ]/ρ + trivial-zeros + tail.
4. **Farey Spectroscope** (computational, our discovery): F(γ) = γ²·|Σ_p M(p)/p · e^{−iγ log p}|² detects the first 20/20 zeta zeros via local-z scoring. Universal across prime subsets. (`Farey Research/wiki/Farey_Spectroscope.md`)

What is **novel** about Δw(N) (beyond Franel-Landau classical theory): the signed per-step decomposition as a geometric object, the four-term decomposition itself, matched-filter recovery from prime-fingerprint structure, the 33000:1 cancellation, and the φ_1 = −1.6933 rad phase resolution. Franel-Landau already ties cumulative Farey discrepancy to RH norms; the original contribution is the **local per-prime structure** and its zeta-zero detection.

# Map: Today's Results × Δw(N)/Farey Relevance

| Result | Object | Direct Δw(N) relevance? | Notes |
|---|---|---|---|
| **a_2 closed form** (B1, MAE 0.073) | GL(2) holomorphic newform 2nd moment polynomial in log X | NO | Modular L-function moment problem; ζ does not appear except via L(sym²f) and Stieltjes constants. No Möbius/Ramanujan-sum content. |
| **Theorem 1 (Petersson family obstruction, B3)** | Why fixed k=2 N→∞ FAILS to give unconditional 2/(3π) | NO | Lives entirely on the modular side; tells us Bessel-Kloosterman only decays for k→∞, not for level-aspect at fixed weight. Δw(N) doesn't even have a Petersson family. |
| **Theorem B unconditional 2/(3π) (weight aspect)** | Σ_{f∈S_k^*(N)} weighted second moment of |L'(ρ_f, f)|² in k→∞ regime | NO | Weight-aspect averaging over a modular family. Δw(N) is a single-point ζ-only sum, not a family average. |
| **Theorem C* (level-averaged super-family)** | Σ_{N≤X} averaged second moment | NO | Same comment as B. The averaging is over modular curves, not over Farey denominators. |
| **Theorem A v2 cage** | Two-sided GRH-conditional cage inside which 2/(3π) sits | NO | Cage on Σ |L'(ρ_f, f)|². Same modular sub-track. |
| **c_W = −γ_E − E_1(1) (Lean)** | Mellin shift constant for kernel exp(−x)·1_{0<x≤1} | INDIRECT | The kernel-shift architecture transplants to Δw(N) — same M_W structure, different Dirichlet series. The constant itself is C1-specific, but the technique is shared. |
| **Barycentric identity** Σ_{j≠0} Q(z_j)·P'(a)/P'(z_j) = −Q(a) | CUE-Palm cancellation for derivative-ratio sums | NO | RMT side; does not touch Δw(N) explicit formula. |
| **R_2(u)·𝔇(u) = π²u²/3** (Christoffel-Uvarov special case) | CUE pair-correlation × derivative-ratio identity | NO | Same as above. |
| **Per-step explicit formula** Δw_f(N) = Σ_ρ [G_f(ρ)/ζ'(ρ)]·(...) | Δw_f(N) for any periodic f | YES — DIRECT | This IS the original program. Derived 2026-05-02 as part of the spectroscope-unification handoff. Mostly classical (Landau/Ingham reciprocal-ζ Perron formula); project contribution is identifying G_f. |
| **Cross-family meta-theorem (B1 of NOVELTY handoff)** | Reciprocal-L vs log-derivative-L vs derivative-at-zero second moment as three explicit-formula architectures | YES — INDIRECT | Places Δw alongside Mertens/ψ/Chebyshev in one schema. Adversarial-reviewed: the strong "unconditional explicit formula for Δw" claim was withdrawn. What remains is a smoothed Schwartz-cutoff version + a conditional unsmoothed version. |

**Score**: of 8 today-style result classes, 6 are pure C1/W2 modular work, 1 (c_W) is shared technique, 1 (per-step explicit formula) is genuinely on the Δw track but is the WEAKEST result in publishability terms (mostly classical reciprocal-ζ Perron). The strong/breakthrough work is on a sibling problem.

# Honest Verdict

**We have drifted.** Specifically:

- The C1 spectroscope started as "the modular descendant of the original Farey/Mertens spectroscope" — a tool to lift the Δw matched-filter machinery to L-functions.
- It has become a self-sufficient research project on GL(2) holomorphic newform second moments. It has its own conjecture stack (Conrey-Snaith ratios), its own family aspects (Petersson weight, level-averaged super-family), its own 16-curve numerical evidence, and its own paper-section-ready closed forms.
- Most of the breakthroughs in the last 18 hours (a_2 polynomial, Theorem B weight-aspect 2/(3π), Theorem C* level-averaged) are GL(2) analytic NT achievements with **no direct content for Δw(N)**.
- The piece that is genuinely on the Δw track — the per-step explicit formula — was adversarially downgraded: the unconditional version was overclaimed, the smoothed Schwartz version is ~standard Landau/Ingham machinery, and the project-specific contribution is just identifying G_f(s) = Σ f̂(m)·σ_{1−s}(|m|) as the Farey/Ramanujan generating function. **That alone is not a paper.**

The 18 hours of work served the C1/W2 paper, not the Δw paper.

# Top 3 Reconnection Moves (highest leverage Farey-tools fit)

If we want to put today's machinery to work on the **original** program:

1. **Δw_f via the smoothed-cutoff machinery + Lean foundation transplant.**
   The c_W constant, the Mellin-shift residue framework, and the κ=4 / barycentric identities all have analogues in the reciprocal-ζ setting. Concretely: prove the **smoothed Δw_f explicit formula** with rigorous tail bound O_A(N^{−A}) for Schwartz cutoff. Use the same Lean infrastructure (`CWMellinShift.lean`, endpoint-integral lemmas). This is a publishable analytic NT lemma even if classical-flavored, and it formalizes what is currently a hand-derivation. Expected output: 1 Lean theorem + 1 short paper section. Tractability: HIGH — most lemmas are already in `0b805444` batch.

2. **Bridge / Four-Term Decomposition × Petersson family-averaging (cross-pollination).**
   The Bridge Identity Σ_f e^{2πipf} = M(p) + 2 is a **prime-aspect** Farey identity. The Theorem B / C* work introduced Bessel-Kloosterman + Petersson-trace machinery. The natural question: does the four-term decomposition (A, B, C, D_term) admit a Petersson-family-averaged analogue when M(p) is replaced by Σ_f a_f(p)? If yes, we transfer the modular-side unconditional 2/(3π) work to the Farey-side B-term sign question (`Farey Research/wiki/Four_Term_Decomposition.md` lists "B≥0 unconditional" as the main open). Tractability: MEDIUM — speculative but has structural symmetry going for it.

3. **Farey Spectroscope F(γ) — finally give it a rigorous explicit formula via the cross-family meta-theorem.**
   `Farey_Spectroscope.md` reports 20/20 zero detection empirically with z=117.6 null-battery support, but lists "Analytical proof that local z grows monotonically" as open #5. Today's reciprocal-L family architecture (`D = G/L → residue at ρ = G(ρ)/L'(ρ)`) gives the precise prediction: F(γ) at γ = γ_n peaks because γ_n is a pole of `G(s)/ζ(s)` at s = ρ. Combine with the smoothed-cutoff infrastructure to get **rigorous local-z growth bounds**. This kills the last "computational/empirical" label on the original spectroscope and turns paper 2 into a real theorem. Tractability: MEDIUM-HIGH.

# Will the Eventual Paper Be About Farey, or About M-N?

**Honest answer: as currently developing, it will be M-N (GL(2) modular newform second moments).**

Evidence:
- All recent handoffs are about a_4, a_3, a_2, a_1, a_0 of the Σ |L'(ρ_f, f)|² polynomial.
- The Lean foundation in flight is for the M-N polynomial coefficients, not the Δw explicit formula.
- The 16-curve ladder evidence is for the modular polynomial fit, not for the four-term decomposition or the spectroscope.
- AUTONOMOUS_PLAN.md's three blockers (B1, B2, B3) are 3 modular sub-track problems.
- The novelty audit (Q-B / B.1) targets the CUE derivative-ratio identity — random matrix theory side, not Farey side.
- W2_C1_FINAL_WRAP §6 is explicit: "C1 specific connections to original Farey/Mertens/ψ spectroscopes... is a separate, mostly open problem."

This paper will likely cite the original Δw(N) program as motivation in the introduction and otherwise live in analytic NT. It is publishable on its own merits (Compositio-tier with Theorem B unconditional + Theorem C* + closed-form a_2; possibly Annals if the Petersson story tightens further). But it is **not the Farey paper** Saar set out to write.

The actual Farey paper(s) — Bridge Identity + Four-Term + Δw + Spectroscope F(γ) — exist as scaffolding in `Farey Research/wiki/`, are partially Lean-verified, but have NOT been advanced by the last 18 hours of work. Open problems there (per `Farey_Spectroscope.md`, `Four_Term_Decomposition.md`):

- Prove B ≥ 0 (or characterize sign) in the four-term decomposition unconditionally. Empirical up to p = 631; theoretical OPEN.
- Prove C/A ≥ c > 0 unconditionally. (Would close DiscrepancyStep.)
- Amplitude formula convergence at large N for spectroscope.
- Background growth O(N^{3/2}) analysis for spectroscope.
- Simple-zeros hypothesis via spectroscope peak shape.
- Lehmer phenomenon detection.
- Analytical proof that local-z grows monotonically (key for spectroscope publishability).
- Sign(R_2(p)) characterization vs M(p) correlation.
- Composite-bridge generalization with correction term.
- Schema unification across Farey/Mertens/ψ/Chebyshev outputs (brief's Q5).

**None of these were touched by today's work.**

# Recommendation

Pick one of two postures and commit:

A. **Two-paper plan.** Paper 1 = Farey (Bridge + Four-Term + Δw + Spectroscope, mostly already drafted). Paper 2 = M-N modular polynomial (all the new C1/W2 stuff). Treat them as siblings. Re-direct ~30% of compute to the Farey-paper open problems (especially B ≥ 0, local-z monotonicity).

B. **One-paper plan.** Force the connection. Pick one reconnection move above (probably #3 — rigorous Farey Spectroscope explicit formula via the cross-family meta-theorem) and make it the connective tissue between Δw and the modular-side machinery. Risk: forced unification has been adversarially flagged before ("the four families share the SKELETON, not a single observable").

Posture A is safer and more honest. Posture B is more ambitious but risks publishing a unified paper whose unification is structural-only.
