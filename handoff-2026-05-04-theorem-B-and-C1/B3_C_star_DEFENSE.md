---
title: "B3 Theorem C* Defense Pass — devil's advocate against the audit"
type: derivation
domain: research
tier: working
confidence: 0.40
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Cohen-Devin-Fiorilli-Pratt-Södergren 2022, arXiv:2210.15782"
  - "Lester-Yiasemides 2023, arXiv:2310.07606 (large orthogonal family, support extended to (-4,4))"
  - "Lester-Yiasemides 2025, arXiv:2510.07647 (n-th centred moments, 1-level, support sum < 4)"
  - "Iwaniec-Luo-Sarnak 2000 §6 (ILS)"
  - "Hughes-Miller 2007 (n-level density refinements)"
  - "Bui-Florea-Keating 2017 (BFK)"
  - "Sound-Young 2010 (quadratic twists)"
  - "Petrow-Young 2018 (cubic moment, Petersson newforms)"
  - "Iwaniec 1990 §13 (large sieve for modular forms)"
  - "Heath-Brown 1979 (zero-density)"
supersedes: []
tags: [theorem-C, defense, ILS, level-averaging, Bombieri-Vinogradov, n-level-density]
---

# Bottom line

**Defense largely fails. Two of the three fatal flaws cannot be repaired with current literature; one (F1) finds a partial defense. Theorem C* as stated in `B3_theorem_C_progress.md` §2.3 is NOT presently defendable as fully unconditional.** However, the defense uncovers a *salvageable weaker statement* — a level-averaged 1-level density result with constant 2/(3π) at η < 4 (sum of supports), which is unconditional but does NOT close the M-N second-moment-of-derivative-at-zeros target without an additional 2-level identity.

Final verdict: rejection stands. Confidence in C* (as stated): demote 0.74 → 0.30. Salvageable weaker variant ("Theorem C*-1L") at 0.55.

---

# 1. Defense of (F1): unconditional 2-level support beyond η < 1?

## 1.1 The audit's claim

ILS 2000 §6 unconditional support is η < 1 for the 1-level density and η < 1/2 for individual N (η < 1 only after harmonic averaging). For 2-level the unconditional support is even smaller. Extending to η < 2 requires GRH or Hypothesis H.

## 1.2 Best counter-evidence

Three relevant published results extend the support:

(a) **Cohen-Devin-Fiorilli-Pratt-Södergren (CDFPS) 2022, arXiv:2210.15782.** "Extending the unconditional support in an Iwaniec-Luo-Sarnak family." For holomorphic newforms of fixed even weight k and prime level N → ∞, **harmonically weighted 1-level density** is shown unconditionally for test functions with Fourier support in (−Θ_k, Θ_k), where Θ_2 = 1.866… and Θ_k → 2 as k → ∞. The novelty is **zero-density estimates for Dirichlet L-functions** (Heath-Brown style), which provide the off-diagonal Kloosterman cancellation without GRH.

(b) **Lester-Yiasemides 2023, arXiv:2310.07606** and 2025, arXiv:2510.07647. For the **q-averaged** family (newforms of level q averaged over q ∼ Q), the unconditional support for the 1-level density (and the n-th centred moments thereof) extends to test functions whose Fourier-support sum lies in (−4, 4). This *is* a level-of-levels Bombieri-Vinogradov-type input, applied to the Dirichlet L-functions appearing in the Kloosterman expansion.

(c) **Hughes-Miller 2007** (n-level refinements): for orthogonal families, the n-level density unconditional support is bounded by 1/(n) times the 1-level support in many regimes. This *halves* the effective support for n = 2.

## 1.3 What this gives Theorem C*

CDFPS gives 1-level support → 2 for fixed prime N, k = 2: ~~Θ_2 = 1.866~~. **But the audit asks for 2-level density at η < 2, not 1-level.** Hughes-Miller suggests 2-level support is at most (1/2)·1.866 ≈ 0.93, *worse* than the 1-level case. The CDFPS technique does NOT directly extend to 2-level because the 2-level off-diagonal involves *pairs* of Dirichlet L-functions whose joint zero density is not controlled by Heath-Brown.

Lester-Yiasemides 2310.07606 gives 1-level density at sum-of-supports < 4 unconditionally for the q-averaged family — **exactly the family Theorem C* uses (G(X))**. This is the strongest defense of (F1) available in published literature. However: their result is **1-level density**, not the **2-level density** Theorem C*'s proof requires.

For 2-level density (the actual statistic Theorem C* needs in §2.2 Lemma B), the published unconditional support is η₁ + η₂ < 1 (ILS) or marginally better via CDFPS-style extensions (~ 1.86 with Heath-Brown zero-density). **Nothing in the literature reaches η₁ + η₂ < 2 unconditionally for 2-level density**, even with q-averaging.

## 1.4 (F1) verdict

**Partial defense.** ILS-style level-averaging + Heath-Brown zero-density extends 1-level support to (−4, 4) for q-averaged Petersson families. This is real and unconditional. **But** it does NOT extend the 2-level density support to η < 2. Theorem C* as stated requires 2-level at η < 2, which is the same conditional barrier as before.

**Saving move:** if Theorem C*'s proof can be re-engineered to require only **1-level density at η < 2** (rather than 2-level), then Lester-Yiasemides 2023/2025 closes the gap. This requires re-examining §2.3 of `B3_theorem_C_progress.md` and the `B3_unconditional_attempt.md` §3.5 IBP step, which we do under (F3) below.

---

# 2. Defense of (F2): Bombieri-Vinogradov for Petersson-Kloosterman?

## 2.1 The audit's claim

Bombieri-Vinogradov (BV) is a statement about Dirichlet characters / arithmetic progressions: Σ_{q ≤ Q} max_{(a,q)=1} |ψ(x;q,a) − x/φ(q)| ≪ x/(log x)^A, for Q = x^{1/2 − ε}. It does NOT apply to Petersson-Kloosterman sums S(m,n;c). The "level-of-levels" trick (summing the divisor function τ(c) = #{N | c}) gives only τ(c) ≪ c^ε, which is far weaker than BV-style cancellation.

## 2.2 Best counter-evidence

(a) **Lester-Yiasemides 2310.07606** §3 (the main technical input). Their proof DOES use a Bombieri-Vinogradov-type result, but **applied to Dirichlet L-functions arising on the spectral side of the Petersson formula**, not to Petersson-Kloosterman sums directly. The chain is:

  Petersson-Kloosterman S(m,n;c) → (Kuznetsov) → spectral expansion in Maass forms u_j → Dirichlet character L-functions L(s, χ) attached to each u_j → BV-on-average for Dirichlet L-functions → cancellation.

  This is a four-step indirection. BV applies at step 4, after Kuznetsov has converted Kloosterman into Dirichlet objects.

(b) **Iwaniec 1990 §13** ("Large sieve for modular forms"). This gives a genuine *spectral large sieve*: averaging over Maass forms u_j with eigenvalue λ_j ∈ [T, T+1] and over level N ≤ X, one obtains square-root cancellation in the joint (j, N) sum. This is the closest analogue to BV for the Petersson family.

(c) **Petrow-Young 2018** (Annals): generalised cubic moment and Petersson formula for newforms with level structure. Not BV per se but provides a *trace formula identity* that absorbs level averaging.

(d) **Deshouillers-Iwaniec 1982** §3, §4: the spectral large sieve for Kloosterman sums. Gives unconditional cancellation Σ_{c ≤ C} c^{-1} S(m,n;c) ≪ (mnC)^ε, using Kuznetsov + Selberg. This is *not* BV — it's a different averaging.

## 2.3 What this gives Theorem C*

Lester-Yiasemides shows that BV-on-Dirichlet-L (after Kuznetsov reduction) suffices to extend unconditional 1-level support to (−4, 4) when averaged over level. This is a real result and it does answer (F2) **for 1-level density only**.

For the 2-level density Theorem C* needs, the analogous chain breaks down: the 2-level density involves *products* of two Petersson-Kloosterman sums, after Kuznetsov these become products of two spectral expansions, and the BV input would need to apply to *quadratic forms* in Dirichlet L-functions. Such a "quadratic BV" is **not in the published literature** — it's essentially what Hypothesis H of ILS asks for.

Iwaniec-Kowalski Ch. 16 contains the closest available statement (large sieve for modular form coefficients), but it gives only η < 1 for 2-level density.

## 2.4 (F2) verdict

**Partial defense, same as (F1).** A genuine BV-style mechanism exists *after* the Kuznetsov reduction, but only for 1-level (linear) statistics. The 2-level (quadratic) case requires a quadratic BV that has not been proven. The audit's dismissal "τ(c) ≪ c^ε" is too quick — Lester-Yiasemides do better via Kuznetsov+BV — but the audit's conclusion (no η < 2 for 2-level) stands.

---

# 3. Defense of (F3): is the L'·L''·S_f integral really a 2-level density?

## 3.1 The audit's claim

L'(1+it)·L''(1+it)·S_f(t) is a triple product on the line t > 0 (off-critical-line for L', on-critical-line for L̃ via reflection). It is *not* a 2-level density of zeros — those live on the critical line and are statistics of pairs (γ_f, γ'_f). The "2-level density" framing is a category error.

## 3.2 Best counter-evidence

The audit is correct that L'·L''·S_f is not literally a 2-level density. But the *route* by which 2-level density enters is more subtle. Tracing `B3_unconditional_attempt.md` §3.5 carefully:

**Step (i)** Stieltjes IBP:
  ∫ |L'(1+it,f)|² dS_f(t) = − ∫ S_f(t) · 2 Re(L'·conj L''(1+it,f)) dt

**Step (ii)** Cauchy-Schwarz:
  |⟨S_f · g_f⟩_F|² ≤ ⟨S_f²⟩_F · ⟨|g_f|²⟩_F

**Step (iii)** S_f² variance via explicit formula:
  S_f(t) = − (1/π) Σ_γ_f log|t − γ_f| + (smooth)
  ⟨S_f(t)²⟩_F = pair correlation of zeros of f, evaluated at the test function (log|t−·|)² — **this is exactly the family-averaged 2-level density of zeros** (Montgomery-Bogomolny-Keating-Snaith framing).

**Step (iv)** ⟨|g_f|²⟩_F: this is a 4th moment of L on the line, controlled by KMV/HY moment formulas, NOT a zero statistic.

**So the 2-level density enters at step (iii), via the variance of S_f, NOT via L'·L''·S_f directly.** The audit's "category error" is correct as stated, but the original author meant the 2-level density of zeros enters through ⟨S_f²⟩ — which is a legitimate 2-level density statistic.

## 3.3 The bandwidth question (corrected)

`B3_theorem_C_progress.md` §4.2 claims the IBP "reduces 4-level to 3-level." Actually the bookkeeping gives:

- ⟨S_f²⟩_F = 2-level density (clean)
- ⟨|g_f|²⟩_F = ⟨∫ |L'·L''|² dt⟩_F ≪ T·log⁶(NT) by HY/KMV-type 4th moment of L'L'' (unconditional in *weight aspect* via Bessel decay; conditional in level aspect)

The fluctuation control needs:

  |⟨S_f · g_f⟩| ≪ T·log²(NT) ≪ main = T·log⁴(NT)

via Cauchy-Schwarz. This works if:

  ⟨S_f²⟩_F ≪ log²(NT) · ε(N,T)  with ε → 0,
  ⟨|g_f|²⟩_F ≪ T · log⁶(NT).

⟨S_f²⟩_F ≪ log² is implied by 2-level density at η₁ + η₂ < 2 (the test function (log|t-·|)² has bandwidth ~log T ~ 2). **If we replace this with η₁ + η₂ < 4 (Lester-Yiasemides level-averaged 1-level)**, we get a *stronger* control on a single S_f, but ⟨S_f²⟩ is intrinsically 2-level — Lester-Yiasemides does not directly bound it.

There IS a path: ⟨S_f²⟩_F can be Cauchy-Schwarz'd to ⟨S_f⟩_F · ⟨|S_f|³⟩_F^{1/2} or similar, where the 1-st moment ⟨S_f⟩_F **is** controlled by 1-level density. But this loses log savings and the exponent doesn't quite balance. Whether Lester-Yiasemides 1-level at η < 4 suffices to bound ⟨S_f²⟩_F at the rate log² × o(1) requires an explicit calculation **not yet performed**.

## 3.4 (F3) verdict

**Partial defense, fragile.** The "category error" is technically correct as a literal reading. The corrected understanding is:

- 2-level density enters via ⟨S_f²⟩_F (legitimate).
- Theorem C*'s proof needs ⟨S_f²⟩_F ≪ log²(NT) with savings.
- Currently, this requires 2-level density at η < 2 — *the original conditional gap*.
- Lester-Yiasemides gives 1-level at η < 4, which **may** bound ⟨S_f²⟩_F by an indirect argument (Hölder + 1-level control of S_f and of its higher moments), but this requires a specific calculation and might lose powers of log.

---

# 4. Honest verdict

## 4.1 Defendable as stated?

**No.** Theorem C* as stated in `B3_theorem_C_progress.md` §2.3 — "M_G(T,X) = (2/(3π))·⟨c_f⟩·T·log⁴(NT)·(1+o(1)) UNCONDITIONALLY via ILS §6 + BV + level-averaging giving 2-level density at η < 2" — does NOT hold up:

- (F1): no published 2-level density at η < 2 for level-averaged Petersson newforms.
- (F2): BV applies *only* to Dirichlet L-functions on the spectral side, *only* for 1-level (linear) statistics; not to the quadratic 2-level Kloosterman objects.
- (F3): the L'·L''·S_f integral is not literally a 2-level density, but 2-level density does enter through ⟨S_f²⟩_F. So the audit's category-error charge is technically correct but the original author's intent is recoverable. However, the recovery still requires 2-level density at η < 2, which we don't have.

The "Bombieri-Vinogradov + Linnik" gloss in `B3_theorem_C_progress.md` §2.2 conflates several distinct results and overstates what's available.

## 4.2 Salvageable weaker variant: "Theorem C*-1L"

There is a defendable but **strictly weaker** statement:

**Theorem C*-1L (proposed).** For G(X) = {(f,N) : N ≤ X squarefree, f ∈ S₂*(N)}, the family-averaged 1-level density of zeros of L(s,f) converges to the SO(even) 1-point function unconditionally for test functions with Fourier-support sum < 4 (Lester-Yiasemides 2023/2025).

This does NOT immediately give M_G(T) = (2/(3π))·T·log⁴(NT)·(1+o(1)). To bridge from 1-level density to the M-N second-moment-of-derivative requires **either**:

(a) An additional 2-level input (currently missing) → reverts to Theorem C* as originally stated.
(b) A reformulation of the M-N statistic as a *1-level* functional rather than via the IBP route. Specifically: directly compute ⟨Σ_γ |L'(ρ_f,f)|²⟩_F via approximate functional equation + Petersson + Lester-Yiasemides BV-of-Dirichlet, *without* the Stieltjes-IBP detour. This is a substantively different proof outline.

Outline (b) is plausible but not fully worked out. It corresponds to the Conrey-Iwaniec 2002 cubic moment style argument, adapted for L'. Confidence ~0.45.

## 4.3 Confidence updates

- Theorem C* as stated in `B3_theorem_C_progress.md` §2.3: 0.74 → **0.30**. The claim that "ILS §6 + BV + Linnik gives 2-level at η < 2 unconditionally" overstates what's published. Real status: 2-level at η < 2 is the same conditional gap (= Hypothesis H of ILS), not closed by level-averaging.
- "Theorem C*-1L" (level-averaged 1-level density at η < 4 unconditional, supports SO(even) framework but does not give the M-N constant directly): **0.55**.
- Outline (b) bridge from 1-level to M-N second moment: **0.45** — plausible but unworked.

## 4.4 Recommendation

1. **Demote Theorem C*** to "conjectural; equivalent to L4 (4-level)" alongside Theorem C in `B3_unconditional_attempt.md`. Update `B3_theorem_C_progress.md` §2 from "LANDS" to "PARTIAL — see C*-1L."
2. **Rewrite C*-1L** as a clean unconditional statement at the 1-level density layer, citing Lester-Yiasemides 2310.07606. This is genuinely new for the application but stops short of the M-N constant.
3. **Pursue outline (b)** as the path to the full M-N constant 2/(3π) unconditionally. Estimated 4–6 months focused work; main technical input is Conrey-Iwaniec cubic-moment-style direct computation of the L' second moment via Petersson + BV-of-Dirichlet (Lester-Yiasemides) without zero-statistics.
4. **Theorem B** (weight aspect, unconditional) remains the strongest unconditional result and should be the headline.

## 4.5 Where the audit is wrong

The audit's three-flaw rejection is technically correct but its (F2) framing — "BV doesn't apply to Petersson-Kloosterman" — is too strong. BV *does* apply, after Kuznetsov reduction, on the spectral side, and Lester-Yiasemides 2023/2025 use exactly this to close 1-level density at η < 4 unconditionally for level-averaged Petersson families. The audit missed this published result.

What the audit got right: this BV-via-Kuznetsov mechanism is **linear** (1-level) only; it does not extend to the quadratic 2-level statistic that Theorem C*'s proof requires.

# Done.

Net: rejection of Theorem C* (as stated) **stands**. Confidence 0.74 → 0.30. New target Theorem C*-1L at 0.55. Theorem B (weight aspect) remains the headline unconditional result.
