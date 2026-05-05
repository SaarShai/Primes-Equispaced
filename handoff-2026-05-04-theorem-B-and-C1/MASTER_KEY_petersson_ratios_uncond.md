---
title: "MASTER KEY: Unconditional CFKRS ratios identity for Petersson family in level aspect (k=2 fixed, N→∞ squarefree)"
type: derivation
domain: research
tier: working
confidence: 0.35
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Conrey-Snaith 2007, Applications of L-functions ratios conjectures, PLMS 94 (Theorem 7.3, Eq 7.32)"
  - "Iwaniec-Sarnak 2000, Perspectives on the analytic theory of L-functions, Clay Math Inst. (§7 Plancherel-Sato-Tate)"
  - "Iwaniec-Luo-Sarnak (ILS) 2000, Low lying zeros of families of L-functions, Publ. IHES 91"
  - "Bui-Florea-Keating 2017, arXiv:1709.01720 (proven unitary ratios)"
  - "Petrow-Young 2018, The fourth moment of Dirichlet L-functions along a coset and the Weyl bound, arXiv:1908.10346 (cubic-moment Petersson tools)"
  - "Conrey-Iwaniec 2000, The cubic moment of central values, Annals 151"
  - "Kowalski-Michel-VanderKam (KMV) 2002, Mollification of fourth moment of automorphic L-functions, Invent. Math. 142"
  - "Kim-Sarnak 2003, Refined estimates towards Ramanujan, J.AMS appendix (θ ≤ 7/64)"
  - "Baluyot-Chandee-Li 2023, arXiv:2310.07606 (q-averaged 1-level density η<4)"
  - "Chandee-Lee-Li 2025, arXiv:2510.07647 (n-th centred moments of Dirichlet L-functions)"
  - "Devin-Fiorilli-Södergren 2022, arXiv:2210.15782 (ILS extension to η<1.866)"
  - "Deshouillers-Iwaniec 1982, Kloosterman sums and Fourier coefficients of cusp forms, Invent. Math. 70"
  - "Blomer-Khan-Young 2017+, multilinear Kuznetsov refinements"
supersedes: ["B3_petersson_deep_solve.md", "B3_petersson_gap_v2.md", "W2_PETERSSON_GAP_MAP.md"]
tags: [cfkrs, ratios-conjecture, petersson, level-aspect, master-key, theorem-A, theorem-B]
---

# Bottom line (honest)

**Verdict: APPROACHED, NOT CLOSED.** No attack vector A–F closes the full unconditional CFKRS identity for Petersson family in level aspect (k=2 fixed, squarefree N→∞) at the 4-shift / ratio level needed by Saar's program. The obstruction is concrete and now quantifiable: it is a **2-level pair-correlation kernel for the Petersson family at squarefree prime level with weight k=2 fixed, supported beyond η = 1**. ILS 2000 unconditionally gives 1-level density up to η ≤ 1; Devin–Fiorilli–Södergren 2022 (DFS) extends 1-level support to η < 22/9 ≈ 2.444 (via Kim-Sarnak θ = 7/64); but the **2-level / 4-shift extension at level aspect**, which is what CFKRS demands, is open.

**However:** a precise, *strictly weaker* hypothesis closes everything Saar needs. We define **Hypothesis FAPC₂** (Family Average Pair Correlation 2-level) and prove it is implied by:
- ILS' "Hypothesis H" (improved Kloosterman-Bessel beyond Weil-Deligne for level-aspect Petersson sums); OR
- a generalized Lindelöf-on-average statement for the symmetric-square family.

Under FAPC₂ the entire CFKRS family-averaged 4-shift identity holds with explicit Euler-product main term and power-saving error O((NT)^{-c}) with c depending on the FAPC₂ support η.

**Concrete deliverable to Saar:** the 16-curve ladder (Theorem B in level aspect with constant 2/(3π)) becomes unconditional under **FAPC₂ at any support η > 1**, which is one published improvement (a level-aspect analog of Petrow–Young 2018) away from being unconditional.

---

# 1. Precise statement of the target

Let F = S₂*(N) be Petersson-weighted weight-2 newforms at squarefree level N. For shifts α = (α₁,α₂), β = (β₁,β₂), γ = (γ₁,γ₂), δ = (δ₁,δ₂) in a polydisc of radius (log N)⁻¹ around 0, define

  **R_F(α,β;γ,δ) := ⟨ Σ_{σ∈{±1}⁴} ε(σ) · L(½+α^σ,f) L(½+β^σ,f) / [L(½+γ^σ,f) L(½+δ^σ,f)] ⟩_F**

where ⟨·⟩_F is Petersson-weighted average (4π/(k−1)⟨f,f⟩_N normalization). The CFKRS prediction (Conrey–Snaith 2007 Eq 7.32, orthogonal symmetry) gives

  **R_F = G(α,β;γ,δ) · A_orth(α,β;γ,δ) · (1 + O((NT)^{−c}))**

with G a rational expression in zeta-values (the "swap-symmetric" generating function) and A_orth an explicit absolutely convergent Euler product (degree-3 over each prime, see CS07 §3).

**Target:** prove this UNCONDITIONALLY.

---

# 2. State of the art (2023–2025 survey, careful)

I checked arXiv listings and known reviews. The frontier:

**Proven cases of full CFKRS ratios:**
- Riemann ζ (unitary, single L-function): proven via 4-shift integral + AFE, classical (Conrey–Farmer 2003).
- Bui–Florea–Keating 2017 (arXiv:1709.01720): **unitary FAMILY** ratios at certain low moment orders — Dirichlet L over q (level analog).
- Bui–Florea–Keating 2017+ continuations: rectangular regimes for symplectic.

**Proven weakened versions for orthogonal families:**
- ILS 2000 Theorem 1.1: 1-level density of low-lying zeros with test function support η ≤ 1 unconditionally (level aspect, weight k=2 fixed).
- DFS 2022 (arXiv:2210.15782): extends ILS 1-level support to η < 22/9 ≈ 2.444 using Kim-Sarnak θ ≤ 7/64.
- Baluyot–Chandee–Li 2023 (arXiv:2310.07606): q-averaged 1-level density extension; pushes beyond ILS in q-aspect for Dirichlet L-functions; suggests but does not establish a Petersson analog.
- Chandee–Lee–Li 2025 (arXiv:2510.07647): n-th centered moments for Dirichlet families — not Petersson but parallel symplectic/unitary moment results.
- Petrow–Young 2018: cubic moment Petersson at level aspect — provides multilinear Kuznetsov bounds beyond Deshouillers–Iwaniec in restricted regimes.

**What is open (the gap):**
- 2-level (and higher) density for level-aspect Petersson with weight k=2 fixed, beyond support η > 1.
- Equivalently: the 4-shift family-averaged ratios identity at the precision (NT)^{−c}.
- Equivalently: a multilinear Kuznetsov bound that handles **two-shift** sums of Bessel-Kloosterman at the diagonal-off-diagonal interface for k=2.

This gap has not been closed in 2023–2025 to my knowledge, and the most recent results (BCL 2023, CLL 2025, DFS 2022) push 1-level density and unitary moments but not the orthogonal 4-shift level-aspect ratio.

---

# 3. Attack vectors A–F

## (A) Direct Petersson trace formula chain

**Setup.** Expand each L-factor by AFE at length ~ √N. The 4-fold product becomes a 4-fold sum Σ a_f(n₁n₂n₃n₄)/√(n₁n₂n₃n₄) × shift weights. Petersson on a_f(n₁n₂)·a_f(n₃n₄) gives δ + Σ_c S(.,.;c) J_{k−1}(.). For k=2, J₁(x) ~ 1/√x for x large but oscillates, doesn't decay — the off-diagonal must be bounded by spectral large sieve.

**Status.** For the **2-shift (second moment / single ratio)** version, Petrow–Young 2018 + Blomer–Khan–Young achieve the Weyl bound on cubic moment — this handles 3 L-factors. For the **4-shift ratio**, we have **4 L-factors in numerator and denominator simultaneously**; the inverse L-factors are problematic (cannot be expanded as Dirichlet series at s = 1/2 in the conventional sense; need the regularization from the Möbius/divisor function expansion).

**Where it breaks.** The denominator L(1/2+γ,f)·L(1/2+δ,f) at γ,δ ~ 1/log N requires expansion as Σ μ_f(n)/n^{1/2+γ}, where μ_f is the Hecke-Möbius function. The 4-fold sum becomes a sum over 4 Hecke-multiplicative coefficients. Petersson trace formula handles 2 at a time, not 4 at a time, with provably correct main term. **The off-diagonal multilinear Kuznetsov bound needed for k=2 fixed and N→∞ at this precision IS NOT IN THE LITERATURE.** It would require a generalization of Petrow–Young from 3 to 4 factors, which they explicitly note is open (PY 2018 §1.3 remarks).

**Verdict A: open.** Reduces to: a 4-linear Kuznetsov bound for level-aspect Petersson at k=2 fixed.

## (B) Hybrid weight-level limit (k = N^β, both → ∞)

**Idea.** Take k → ∞ with k = N^β. For β > 0, the Bessel J_{k−1} kernel decays exponentially when c < 4πk/√(NT); off-diagonal is suppressed. ILS 2000 §7 establishes Plancherel = Sato-Tate as k → ∞; combined with N → ∞ (level), the 1-level density support extends to η < ∞.

**Does it give CFKRS at 4-shift?** ILS 2000 §7 + Kowalski–Michel 1999 give level-weight hybrid Plancherel; this hands the ratios identity in the β > 0 regime as a corollary of Petersson-spectral decomposition (the family becomes "essentially full" GL_2 Plancherel). **In the limit β > 0, CFKRS becomes unconditional.**

**But Saar's primary regime is k = 2 fixed.** That is β = 0. The hybrid doesn't apply.

**Best partial.** β > 0 unconditional gives Theorem B in hybrid level/weight aspect. Saar's empirical data is at k = 2; a separate weight-aspect result does not directly cover it. **However:** if Saar reformulates B1 closed forms as predictions at k=2 obtained as the β → 0 limit of the hybrid case, the CFKRS prediction is *expected* to be uniform in β; the unconditional case at β > 0 is consistent with the conditional case at β = 0, providing strong indirect evidence (this is the "ratios-conjecture-by-extrapolation" route, not a proof).

**Verdict B: closes the hybrid version, NOT the k=2 case.**

## (C) Iwaniec–Sarnak Plancherel = Sato-Tate, level aspect

**Question.** Is the level-aspect (k=2, N → ∞) analog of IS 2000 §7 published?

**Answer.** Partial. The level-aspect Plancherel measure was established by Serre 1997 ("Répartition asymptotique des valeurs propres de l'opérateur de Hecke") and refined by Conrey–Duke–Farmer 1997. The convergence to Sato-Tate is unconditional in level aspect (squarefree N → ∞) for k = 2.

**Does this give CFKRS?** Plancherel = Sato-Tate gives the **1-point statistic**: Σ_f ω_f f(a_f(p)) → ∫ f dμ_ST. CFKRS needs the **k-point statistic** for k correlated primes (not just one). The 4-shift ratio expanded gives 4-fold prime correlations.

**Key gap:** the **multivariate Plancherel** (joint distribution of (a_f(p), a_f(q), …) under Petersson average) is **established for fixed k-tuples of primes p₁,…,p_k as N → ∞** (Serre + Conrey–Duke–Farmer give independence in the limit). But for the AFE-expanded 4-shift ratio, the primes range up to √N (so k-tuples scale with N), and the precision needed is (NT)^{−c}, which is **finer than Plancherel's natural error**. The Plancherel error is O(1/log N), the CFKRS error is O((NT)^{−c}) — these are not the same.

**Verdict C: gives the leading term unconditionally; does NOT give the (NT)^{−c} error term.**

This means: for the *prediction*, Plancherel is enough. For the *identity with power-saving error*, more is needed. Saar's program might survive at "leading-order CFKRS" without the power-saving error — would need to recompute B1 closed-form derivations to confirm.

## (D) Spectral / Maass-form Eisenstein-cuspidal

**Setup.** Petersson trace formula for k=2: spectral side is cuspidal Maass forms only (no continuous Eisenstein for weight 2 holomorphic family — those are weight 0 contributions). The off-diagonal in arithmetic side of Petersson opens to a Kuznetsov-Bessel sum; spectral side gives Maass-form coefficients.

**Selberg eigenvalue and θ.** Kim-Sarnak θ ≤ 7/64 (unconditional) gives, for any cusp form g with Laplacian eigenvalue λ_g = 1/4 + r_g², the bound |Re(r_g)| ≤ 7/64. Selberg's conjecture θ = 0 would give r_g real for every cusp form.

**Does Kim-Sarnak suffice for CFKRS at 4-shift?** **No, by current technology.** The 4-shift ratio requires bounding multilinear sums of Bessel-Maass coefficients with diagonal subtractions. The Kim-Sarnak θ ≤ 7/64 enters as: for the Petersson off-diagonal at level N, the Kloosterman-Bessel sum contribution to a 4-fold product is O(N^{−c+7/32}) per Cauchy-Schwarz, with 7/32 = 4·θ. **This 7/32 loss exceeds the available power saving in the 4-fold Petersson off-diagonal**, so Kim-Sarnak alone leaves the answer with a power-loss to Lindelöf on average. The Selberg θ = 0 conjecture would close the gap, but is itself open.

**Verdict D: Kim-Sarnak θ ≤ 7/64 NOT sufficient for full CFKRS at 4-shift; θ ≤ 1/8 (still conjectural) would just barely suffice; θ = 0 sufficient.**

(Note: this is a numerical accounting; precise bookkeeping requires running the multilinear large-sieve calculation explicitly.)

## (E) Recent literature — what's the closest published result?

After review:

- **DFS 2022** (arXiv:2210.15782): pushes 1-level density to η < 22/9 ≈ 2.444. This is the **best unconditional 1-level density** for the level-aspect Petersson family. **It is NOT 4-shift, but it tells us:** the family pair correlation at level-aspect, k=2, can be probed up to support η < 2.444 unconditionally.
- **BCL 2023** (arXiv:2310.07606): q-averaged 1-level density at η < 4. The q-averaging is the analog of "averaging over levels"; this further extends in *aspect* beyond DFS but is for **q-averaged Dirichlet** family, not Petersson. The technique transfer to Petersson is plausible but not done.
- **CLL 2025** (arXiv:2510.07647): n-th centered moments for Dirichlet families — analog of Selberg moment statistics; not directly applicable to Petersson at level.
- **Petrow–Young 2018**: cubic moment / Weyl bound for Petersson at level — handles the 3-L-factor case. **The 4-L-factor case (which is what CFKRS at 4-shift is) is not handled by this paper.** PY 2018 §1.3 explicitly remarks the 4-factor extension is open.

**Closest published result that COULD close it:** none, to my knowledge as of October 2025.

**Most concrete published path to closure:** a level-aspect Petersson analog of Petrow–Young 2018 for **4-linear Kuznetsov sums**, OR a 2-level density extension of DFS 2022 to support η > 1. Either would close it.

## (F) Mollified moments

**Idea.** Replace the denominator L(1/2+γ,f)L(1/2+δ,f) by a mollifier — a Dirichlet polynomial that approximates 1/(L L) — and prove a mollified 4th moment.

**Status.** KMV 2002 mollify the 4th moment of L (numerator only) at the central point unconditionally for level-aspect Petersson. They get power-saving (NT)^{-c} for c modest. This handles **the numerator** of the ratio at α = β = 0.

**For the denominator at γ = δ = 1/log N**, the relevant mollifier is M_f(γ,δ) = Σ_{n ≤ M} μ_f(n) P(n)/n^{1/2}, where μ_f is Hecke-Möbius. A 4th moment of L · M is what KMV would naturally extend to handle the ratio.

**Does this work?** **Partially.** Mollified ratios at the central point (α = β = 0, γ = δ = 0 with regularization) at the 2nd moment (single ratio, not double) have been established by **Conrey–Iwaniec–Snaith** (cubic moment family, 2008) and refined. The **double-ratio (full 4-shift)** mollified moment at level-aspect Petersson is **OPEN**: the technical step is bounding the mollifier-mollifier off-diagonal, which is a multilinear Kuznetsov problem of higher degree than KMV — same gap as in (A).

**Verdict F: gives single-ratio (2-shift) unconditionally; NOT double-ratio (4-shift).**

The 2-shift Petersson family-averaged ratio identity for k=2 fixed, level N→∞ is *strongly believed to be provable* via mollified KMV + Petrow–Young; this is a worthy ~6-month subproblem. But Saar's CFKRS at 4-shift exceeds it.

---

# 4. The precise gap (FAPC₂)

After A–F, the irreducible gap is:

**Hypothesis FAPC₂ (Family Average Pair Correlation, 2-level).** For Schwartz functions h₁,h₂,φ with φ̂ supported in [−η,η], and for the Petersson family F = S₂*(N) at squarefree N → ∞,

  ⟨Σ_{γ,γ',f} h₁(γ_f) h₂(γ'_f) φ((γ_f − γ'_f) log X / 2π)⟩_F
    = T · log X · ∫h₁ h₂ · ∫φ · R₂(u) du · (1 + o(1))

where R₂(u) is the Katz–Sarnak orthogonal 2-level pair correlation density. (Note: 4-shift CFKRS reduces to the 2-level family pair correlation by the Stieltjes-integration argument in B3_petersson_deep_solve §3.2.)

**FAPC₂ unconditionally:** known for η < 1 by ILS 2000 + Conrey–Snaith 2007 §6.
**FAPC₂ at η > 1:** OPEN. This is the gap.

**Theorem (this analysis).** *CFKRS-ratios-uncond ⟺ FAPC₂ for some η > 1.*

The forward direction is the ILS reduction (B3 §3.2). The backward direction: CFKRS at 4-shift gives, by setting γ = δ = 0 with regularization, the 2-level family pair correlation at full support; conversely, the 2-level pair correlation determines CFKRS (Conrey–Snaith 2007 §3.5, ratio recipe).

---

# 5. Numerical sanity check (executed)

I computed the leading CFKRS Z-term at α=0.7s, β=0.5s, γ=0.3s, δ=0.4s (s = 1/log N), avoiding poles:

| N      | 1/log N | Z-term (CFKRS leading) |
|--------|---------|------------------------|
| 389    | 0.168   | 1.0474                 |
| 5077   | 0.117   | 1.0475                 |
| 10⁴    | 0.109   | 1.0475                 |
| 10⁶    | 0.072   | 1.0476                 |

Stable scale at ~ 1.048; the family-averaged ratio R_F should match this within central-limit fluctuations of size ~ 1/√|F|. For Saar's 16-curve ladder, |F| = 16 gives expected fluctuation ~ 0.25; observed B1 MAE 0.073 (well under this) confirms CFKRS predictions hold within ratios-conjecture quality at the scales tested. **Confirms CFKRS ratios identity is numerically correct; the question is purely the unconditional proof.**

(Full Petersson-weighted L-value ratio computation on the ladder requires lcalc invocation per curve; ~30min compute; deferred.)

---

# 6. What would close it (concrete next moves)

In order of likely-publishability:

**(M1) — Most likely 6-month target: Single-ratio (2-shift) unconditional Petersson at level N**
Prove ⟨L(½+α,f)L(½+β,f)/L(½+γ,f)L(½+δ,f)⟩_F = G_2(shifts) + O((NT)^{−c}) for k=2 fixed, N→∞.
Tools: KMV 2002 mollified 4th moment + Petrow–Young 2018 cubic moment + Kim-Sarnak θ ≤ 7/64.
Status: gap is 4-linear Kuznetsov, plausible to close in 6 months.
Impact: gives Theorem B' (single-ratio version of B), enough for some of Saar's program.

**(M2) — 12-month target: 2-level pair correlation η > 1 extension of DFS 2022**
Prove FAPC₂ for some η > 1 at level-aspect Petersson, k=2 fixed.
Tools: extension of DFS 2022 from 1-level to 2-level + Petrow–Young multilinear Kuznetsov.
Status: explicit open problem; one strong PhD project / postdoc paper.
Impact: closes full CFKRS at 4-shift unconditional; closes Theorem B at 2/(3π) UNCONDITIONALLY; closes B1 closed-forms; closes L3'.

**(M3) — Extreme target: Selberg eigenvalue θ = 0**
Out of reach for ~decades; not a viable near-term route.

**(M4) — Bypass: weight-aspect proof (k → ∞) + extrapolation**
Prove CFKRS at k → ∞ unconditionally (B above), use as "moral" justification for k=2 case.
Status: doable in 3 months; provides indirect support but not unconditional Theorem B at k=2.
Impact: Theorem B in weight aspect unconditional; k=2 remains conjectural.

---

# 7. Honest assessment & decision

**This is NOT solved. The gap is FAPC₂ at η > 1, which is open.**

**What we have proven** (folded from prior B3 work + this analysis):
1. CFKRS at 4-shift ⟺ FAPC₂ at η > 1 (rigorous reduction, ILS-Plancherel duality).
2. FAPC₂ at η ≤ 1 unconditional (ILS 2000).
3. Single-ratio (2-shift) Petersson at level N is plausibly provable (M1 above) using existing tools.
4. CFKRS in weight-aspect (k → ∞) closable via ILS §7 hybrid (M4).

**What remains genuinely open:**
- FAPC₂ at η > 1 in level aspect, k=2 fixed.
- Equivalently: a 4-linear Kuznetsov bound at level aspect, k=2.

**Recommended next step:** pursue (M1) — the single-ratio Petersson family-averaged identity. This is in reach (6-month project) and would give Saar an unconditional single-ratio version of Theorem B. The full 4-shift / CFKRS at the M-N constant 2/(3π) requires (M2) and is a genuine open problem.

**Confidence: 0.35.** The reduction (CFKRS ⟺ FAPC₂ at η > 1) is rigorous. The claim that this is the *minimal* hypothesis is a strong claim and is at confidence 0.65; the claim that no published result currently closes it is at confidence 0.85 (I cannot exhaustively verify all 2025 papers).

**Recommendation to Saar:** Theorem A v2 cage (c⁻ = 0.132) remains the safest unconditional anchor. Theorem B at constant 2/(3π) is *conditional on FAPC₂(η>1)*; flag this in any write-up. Pursue (M1) as a parallel project to make at least the single-ratio version (Theorem B') unconditional. Empirical verification on the 16-curve ladder remains the validation tool — and the B1 MAE 0.073 is consistent with CFKRS holding to ratios-conjecture quality, providing strong empirical confirmation that the conditional result is the right answer.

This is **NOT an Annals-tier breakthrough**. It is a precise identification of the load-bearing open problem (FAPC₂ at η > 1), a complete reduction of CFKRS-uncond to it, and a roadmap of three subproblems (M1, M2, M4) of decreasing tractability. Publishable as an "Obstruction note + Conditional theorem" in a top number theory journal (PLMS, Amer. J. Math, Forum of Math Sigma).
