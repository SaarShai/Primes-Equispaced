---
title: "B'-denominator via Selberg-Beurling mollifier — structural assessment"
type: assessment
domain: research
tier: working
date: 2026-05-09
auditor: Opus 4.7 (1M ctx), extra-high reasoning
verdict: BLOCKED-FOR-EXACT / VIABLE-FOR-WEAKER (specifically: viable only as **already-published** Theorem B' for Re(γ) ≥ 1/4; gives no new unconditional route to Theorem B-exact at 2/(3π))
sources_verified:
  - "Conrey, J. B. *Mollifying the Riemann zeta-function* (AIM preprint, conference proceedings ~1998), retrieved 2026-05-09 via WebFetch + Read PDF; full text, with verbatim mollifier definition (page 91), Theorem 1 (page 91), and references (page 97)."
  - "Kowalski, E.; Michel, P.; VanderKam, J. *Rankin-Selberg L-functions in the level aspect*, Duke Math. J. 114 (2002) 1-66; PDF retrieved 2026-05-09 from people.math.ethz.ch/~kowalski/rankin-selberg.pdf via WebFetch + Read PDF; full text retrieved, all 50 pages."
  - "WebSearch on Selberg 1942 mollifier construction; WebSearch on Beurling-Selberg extremal majorants (Vaaler 1985)."
sources_attempted_but_not_retrieved:
  - "Selberg, A. *On the zeros of Riemann's zeta-function*, Skr. Norske Vid. Akad. Oslo I. No. 10 (1942), 1–59. Not retrieved (1942 Norwegian Academy publication, no PDF found via WebSearch)."
  - "Beurling, A. (unpublished 1937 manuscript on extremal functions for sgn(x)). Not retrieved."
  - "Bui-Florea cited in B_prime_denominator_FULL.md as 'arXiv:1611.10095'. **Verified via WebFetch: arXiv:1611.10095 is a CS paper on online deliberation systems by Speroni di Fenizio & Velikanov, NOT a Bui-Florea mollifier paper.** The actual Bui-Florea mollification paper is arXiv:1611.09582 (Dirichlet L-functions, GL(1)). The bundle's citation is wrong-identifier (off by one digit) AND wrong-domain (GL(1) Dirichlet, not GL(2) Petersson)."
prior_failures_consulted:
  - "handoff-2026-05-04-theorem-B-and-C1/B_prime_denominator_FULL.md (claim: Re(γ)>0 unconditional, conf 0.78)"
  - "handoff-2026-05-04-theorem-B-and-C1/B_prime_denominator_HONEST.md (claim: Re(γ) ≥ 1/4 only, conf 0.55)"
  - "handoff-2026-05-04-theorem-B-and-C1/B_prime_denominator_contour.md (the prior 1/L approach, conf 0.55)"
  - "handoff-2026-05-04-theorem-B-and-C1/B_prime_numerator_PROOF.md (numerator, conf 0.72)"
  - "handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md"
  - "handoff-2026-05-04-theorem-B-and-C1/RMT_Painleve_GRH_bypass.md"
  - "handoff-2026-05-04-theorem-B-and-C1/RankinSelberg_trace_attack.md"
  - "handoff-2026-05-04-theorem-B-and-C1/Voronoi_Kuznetsov_GRH_bypass.md"
  - "handoff-2026-05-04-theorem-B-and-C1/arxiv_2601_06292_analysis.md"
  - "handoff-2026-05-04-theorem-B-and-C1/Theta_lift_GRH_bypass.md"
  - "handoff-2026-05-04-theorem-B-and-C1/FirstPrinciples_creative_attack.md"
  - "handoff-2026-05-04-theorem-B-and-C1/E1_E2_E3_barrier_attack.md"
  - "handoff-2026-05-04-theorem-B-and-C1/Necessary_conditions_inverse.md"
  - "handoff-2026-05-04-theorem-B-and-C1/Disprove_attempt.md"
  - "handoff-2026-05-09-followup/S4_KMV_Mellin_verify.md (just landed)"
  - "handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md (just landed)"
  - "handoff-2026-05-04-theorem-B-and-C1/B_prime_denom_verify_16curves.{gp,out}"
tags: [B-prime, denominator, Selberg-Beurling, mollifier, structural-assessment, BLOCKED-for-exact]
---

# §0. Confidence aggregation rule (single rule, applied uniformly)

**Rule:** posterior confidence in any claim `C` = MIN over load-bearing inputs `I_i` of `P(I_i correct)`, where `P(I_i correct)` is set as follows:

| Status | P(correct) |
|---|---|
| Verified verbatim against retrieved primary source (curl/WebFetch + Read PDF, with quote and page) | 1.00 |
| Verified against repository file with verified provenance (1-step indirection) | 0.95 |
| Cited only via secondary repo file with no verified primary source | 0.50 |
| Explicitly marked `[UNVERIFIED]` by this agent | 0.10 |
| Explicitly **falsified** against retrieved primary source (citation error caught) | 0.00 |

The aggregation MIN means a single broken citation in a load-bearing chain caps the whole conclusion at the broken link's confidence. This matches the rule used in `S4_KMV_Mellin_verify.md` §9.

---

# §A. Precise statement of the B'-denominator strategy (verbatim from the bundle)

The strategy as articulated in the bundle has TWO published variants, with materially different scope. I quote the bottom-line statement of each verbatim.

## A.1 FULL.md (claim: unconditional for any fixed Re(γ) ≥ δ > 0)

From `B_prime_denominator_FULL.md` lines 28-34 (verbatim):

> **Theorem B' (single-ratio Petersson, FULL).** Let `F_N := S₂*(N)`, N squarefree, weight-2 newforms, harmonic weight `ω_f = 1/(4π⟨f,f⟩_N)`. Fix any `δ > 0`. For shifts `α, β, γ ∈ ℂ` with
> - `|α|, |β|, |γ| ≤ 1/log N`,
> - `Re(γ) ≥ δ` (any positive constant; **NOT shrinking with N**),
>
>   **R'_F(α,β; γ) := ⟨L(½+α,f) · L(½+β,f) / L(½+γ,f)⟩_{F_N} = G_3(α,β,γ; N) + O_δ(N^{-c(δ)}),**
>
> with `c(δ) = δ/4 - ε` (for small δ) and `c(δ) = 1/16 - ε` for δ ≥ 1/4.

The mollifier is defined verbatim in `B_prime_denominator_FULL.md` line 56-60:

> **Key idea (mollifier representation of 1/L on the open strip).** For any fixed `δ > 0`, use the **Selberg–Beurling mollifier** of length `M = N^{1/2 - η}` (η > 0 small):
>
>   N_M(s, f) := Σ_{m ≤ M} μ_f(m) · P_δ(log(M/m)/log M) · m^{-s},
>
> with `P_δ` a polynomial smoothly truncating at scale M (P_δ(0)=0, P_δ(1)=1, P_δ ∈ C^∞[0,1]).

## A.2 HONEST.md (the post-adversarial restriction: Re(γ) ≥ 1/4 only)

From `B_prime_denominator_HONEST.md` lines 26-56 (verbatim):

> The previous file `B_prime_denominator_FULL.md` claimed Theorem B' unconditionally for any fixed `Re(γ) > 0` with confidence 0.78. Adversarial review identified four fatal flaws:
>
> 1. **§4 off-diagonal arithmetic** (in FULL.md) yielded a POSITIVE exponent for δ < 1/4, silently breaking the small-δ claim.
> 2. **Soundararajan 2009** (`arXiv:math/0612106`) was cited for a "negative-second-moment bound `⟨1/|L(½+γ,f)|²⟩ ≪ (log N)^{O(1)}`". Verbatim from the abstract and §1: the paper concerns `M_k(T) = ∫_0^T |ζ(½+it)|^{2k} dt`, **assumes RH**, and gives upper bounds on the *measure* of `t` where `|ζ(½+it)|` is large. It contains no bound for negative moments of `1/|L(½+γ,f)|²` over a level-aspect family of GL(2) cusp forms. **The citation is wrong.**
> 3. **KMV 2002 (Duke 114) Theorem 2** was cited for an L⁴ bound `⟨|L(½+α,f)|⁴⟩ ≪ (log N)⁴`. Verbatim from the table of contents: KMV 2002 (Duke 114) Theorem 1.2 gives a *subconvex convexity-breaking bound* `|L(f⊗χ_D, ½+it)|² ≪ q^{1/2-1/96+ε}`; the rest of the paper is asymptotic moments of Rankin-Selberg `L(f⊗g, ½)` averaged over `f ∈ S_k*(q)`. **No `L⁴` bound for a single GL(2) L-function** in the level aspect appears in KMV-Duke.
> 4. **KPY 2019** is correctly arXiv:1710.00916, "Oscillatory integrals with uniformity in parameters", JTNB 31 (2019) 145–159. It does NOT have a "Proposition 1"; its results are Proposition 2.6, Lemma 3.1, Lemma 5.1, Lemma 5.2, Lemma 5.3, Main Theorem (§3).

Honest theorem statement, `B_prime_denominator_HONEST.md` lines 71-80 (verbatim):

> **Theorem B' (denominator, honest).** For squarefree `N → ∞`, uniformly in (S),
>
>   `R'_F(α, β; γ) = G_3(α, β, γ; N) + O_ε(N^{-1/16 + ε})`,
>
> where `G_3` is the explicit CFKRS-with-quotient main term given in §6 below.
>
> The exponent `1/16 - ε` is the **unconditional** off-diagonal saving from Weil + Petersson at this regime; we make no claim of improvement to `1/4 - ε` (which would require Kuznetsov + Kim-Sarnak inputs not used here).
>
> **What is OPEN (not addressed here):**
> - The strip `0 < Re(γ) < 1/4` ... **not a one-day algebraic fix** — it requires either (a) a substantially refined mollifier construction with δ-uniform constants, or (b) a different argument that does not rely on `M^D` truncation. Estimated effort: months.

## A.3 What the SESSION_SYNTHESIS row says

From `SESSION_SYNTHESIS_extra_high_round.md` line 31 (verbatim):

> 6. **B'-denominator** strategy via Selberg-Beurling mollifier replacing brittle 1/L contour shift — structurally cleaner. (Confidence pending B'-denom adversarial.)

And from line 67 (verbatim):

> | B'-denom Re(γ)>0 | 0.55 | 0.78 | **0.55** unchanged for Re(γ)≥1/4 only |

So the bundle's own honest reckoning, after adversarial audit, is **0.55, restricted to Re(γ) ≥ 1/4** — NOT the FULL.md claim of unconditional Re(γ) > 0. The "structurally cleaner" line in §"Real advances" is the **pre-audit** assessment; the post-audit row is the live one.

---

# §B. Selberg-Beurling mollifier — verbatim definition + properties from primary sources

## B.1 The Selberg 1942 mollifier (the actual canonical construction)

**Primary source retrieved:** Conrey, J. B. *Mollifying the Riemann zeta-function*, AIM preprint, conference proceedings (numbered pp. 89-98). Retrieved via WebFetch + Read PDF on 2026-05-09. This is the standard expository reference on the Selberg mollifier construction.

**Verbatim Conrey p. 91, "Mollifier definition":**

> The mollifiers we are interested in are given by:
>
>   M(s, θ) = Σ_{n≤y} μ(n) P(log(y/n) / log y) / n^s
>
> with y = t^θ and P(0) = 0.

**Verbatim Conrey p. 91, "Theorem 1 (Conrey [C2]). If θ < 4/7, then":**

> (1/T) ∫₀^T |M(½ + it, θ) ζ(½ + it)|² dt  ~  |P(1)|² + ∫₀¹ |P'(x)|² dx.

**Reference verbatim (p. 97):**

> [S1] A. Selberg, *On the zeros of Riemann's zeta-function*, Skr. Norske Vid. Akad. Oslo I. No. 10 (1942), 1–59.

**Properties of the Selberg mollifier (verbatim from Conrey p. 91, "Mollifier definition" paragraph):**
1. M is a Dirichlet polynomial of length y = t^θ (NOT an entire function of t — its truncation is sharp at length y).
2. Coefficients are Möbius times a polynomial weight.
3. P(0) = 0 is essential (otherwise the constant term spoils the cancellation).
4. The cutoff length y = t^θ is dictated by the **regime of t** (Riemann zeta on the critical line); it is NOT set by the regime of any shift parameter γ. **There is no shift γ in the Selberg construction.**
5. Theorem 1's regime of validity is θ < 4/7. The new approach (Conrey p. 94, "New approach to Theorem 1 via an explicit formula") is restricted to θ < 1/2.

## B.2 The Beurling-Selberg extremal majorant (a *different* construction)

**Verbatim WebSearch finding (2026-05-09):**

> The one-sided extremals for the signum function were later used by Selberg to obtain the solution of the extremal problem for characteristic functions of intervals.

> Vaaler's 1985 paper "Some extremal functions in Fourier analysis" appeared in the Bulletin of the American Mathematical Society. This work obtained extremal majorants and minorants of exponential type for a class of even functions on ℝ which includes log |x| and |x|^α, where -1 < α < 1.

**Properties:** entire functions of exponential type τ, majorizing/minorizing characteristic functions of intervals, with Fourier support in [-τ, τ]. The "Beurling-Selberg" name properly refers to THIS class of objects (different from the Selberg mollifier of B.1).

## B.3 Crucial naming-confusion observation

**The bundle's `B_prime_denominator_FULL.md` line 56 calls its construction "the Selberg–Beurling mollifier", but the construction it uses is the Selberg 1942 *mollifier* (B.1), NOT the Beurling-Selberg *extremal majorant* (B.2).** These are two distinct objects:

| Aspect | Selberg 1942 mollifier (B.1) | Beurling-Selberg extremal (B.2) |
|---|---|---|
| What it is | Dirichlet polynomial Σ_{n≤y} μ(n)P(...)/n^s | Entire function of exp. type majorizing char. fn. |
| Year | 1942 (Selberg, on the critical line) | 1937 (Beurling) + Selberg unpublished + Vaaler 1985 |
| Key property | Cancellation against ζ(s) on average | Pointwise majorization + Fourier support |
| Where it's used | Proportion-of-zeros-on-line proofs | Large sieve, gap conjectures, sphere packing |
| GL(2) analog | KMV mollification (Crelle 2000, Duke 2002) | Iwaniec-Sarnak large sieve |

The B'-denominator strategy is a Selberg-1942-style mollifier for `1/L(½+γ, f)`, NOT a Beurling-Selberg extremal majorant. The "Selberg-Beurling" name in the bundle is slightly inaccurate; the relevant tool is the Selberg-only mollifier. This naming imprecision does NOT by itself invalidate the strategy — but it is worth flagging because (a) it makes citation-checking harder, and (b) the actual content used (level-aspect mollifier of inverse-L of a Petersson family newform with shift γ) is **not directly addressed** by either Selberg 1942 (which is GL(1), no shift, on the critical line) or Beurling 1937 (which is band-limited entire-function approximation, no L-function).

## B.4 The closest published analog: KMV §9 (Duke 114, 2002)

**Primary source retrieved:** Kowalski-Michel-VanderKam, *Rankin-Selberg L-functions in the level aspect*, Duke Math. J. 114 (2002), 1-66. PDF retrieved on 2026-05-09; all 50 pages read in this conversation.

The mollifier used in KMV 2002 §9 (p. 32-37), **verbatim eq. (9.1)**:

> M^P(f ⊗ g) = Σ_{ℓ≤L, (ℓ,P)=1} μ(ℓ) λ_f(ℓ) λ_g(ℓ) / ℓ^{1/2} · (1/2πi) ∫_{(3)} (L/ℓ)^z dz/z^3 = Σ_{ℓ<L,(ℓ,P)=1} λ_f(ℓ)/ℓ^{1/2} · x_ℓ.

**Critical structural observation:** this mollifier multiplies $L(f \otimes g, 1/2)$ — the **Rankin-Selberg L-function** — by Möbius times $\lambda_f \lambda_g$ (Hecke eigenvalues of *both* forms). It is NOT an inverse of $L(f, 1/2 + \gamma)$ for a single GL(2) form. The family-aspect 2nd moment KMV proves (Theorem 7.3, p. 27) is the second moment of $L(f \otimes g, 1/2 + \mu)$ over the level family — Rankin-Selberg, not single GL(2).

**Verbatim KMV 2002 Theorem 7.3 (p. 27):**

> Let g and g' be primitive (non exceptional) cusp forms of square free level D, D' and nebentypus χ_D, χ_D', respectively. Assume that q is prime, coprime with DD', that χ_q is the trivial character and S_k*(q) = B_k(q). Let μ := δ + it, μ' = δ' + it' with |δ|, |δ'| ≤ 1/ log q ... For any ℓ < q and any ε > 0,
>
>   (qD)^μ (qD')^μ' M_{g,g'}(ℓ) = M_main_{g,g'}(ℓ) + ε_μ(g) ε_μ'(g') M_main_{ḡ,ḡ'}(ℓ)
>                               + ε_μ'(g') M_main_{g,ḡ'}(ℓ) + ε_μ(g) M_main_{ḡ,g'}(ℓ)
>                               + O_ε ((1+|t|+|t'|)^B q^ε (ℓ^{3/4} q^{-1/12} + ℓ^{17/8} q^{-1/4})).

Note the regime: |δ|, |δ'| ≤ 1/log q (not Re(γ) ≥ 1/4 as the B'-denom HONEST version requires). And the object is **Rankin-Selberg, not single GL(2)**.

**There is no Lemma 1.4 in KMV 2002 §1.** §1 contains only Theorems 1.1, 1.2, Corollary 1.3, Conjectures 1.4, 1.5 (the Rudnick-Sarnak QUE conjecture), Theorem 1.7. So the "KMV 2002 Lemma 1.4 root number distribution" cited in `B_prime_denominator_FULL.md` and HONEST.md does not exist in the source.

**There is no Lemma 2.1 or 2.4 in KMV 2002.** §2 is titled "Arithmetic interpretations of the results"; the only labeled item is Theorem 2.1 (Hecke linear independence). The "KMV 2002 Lem. 2.1" (mollifier identity) and "Lem. 2.4" (Cauchy-Schwarz + L^4) cited in `B_prime_denominator_FULL.md` lines 60, 165 do NOT exist in the source. They are invented.

## B.5 The bundle's Bui-Florea citation is wrong-identifier

**`B_prime_denominator_FULL.md` line 19 cites:** "Bui-Florea 2018 (BF), arXiv:1611.10095 (smooth mollifier in shift uniformity)".

**WebFetch result on arXiv:1611.10095 (verbatim):**

> Title: "System-Generated Requests for Rewriting Proposals"
> Authors: Pietro Speroni di Fenizio and Cyril Velikanov
> Abstract: The paper describes "an online deliberation system using mutual evaluation in order to collaboratively develop solutions."
> ... No, this paper is not by Bui and Florea, nor does it address mollifiers, Selberg-Beurling concepts, Dirichlet polynomials, or GL(2) forms.

The actual Bui-Florea mollification paper is arXiv:1611.09582 ("Mollification of the Fourth Moment of Dirichlet L-functions") — Dirichlet (GL(1)) L-functions, not GL(2) Petersson. So even with the correct identifier, Bui-Florea is the wrong domain.

This is a **third citation error** in `B_prime_denominator_FULL.md`, on top of the three caught by HONEST.md. The pattern is consistent with the SESSION_SYNTHESIS line 121 finding: "**5-of-5 prior agents inflated claims with same-shape mis-citation error**".

---

# §C. What the (Selberg) mollifier gives that 1/L contour-shift didn't

The honest answer is **structural — not analytic**. Specifically:

## C.1 What 1/L contour-shift attempted

From `B_prime_denominator_contour.md` lines 167-180 (verbatim):

> **the Petersson family-average and the contour-shift do NOT commute uniformly in γ when Re(γ) → 0**.
>
> Specifically: if we shift contours BEFORE family-averaging, we pick up f-dependent residues from L-zeros, and the family-sum of these residues is
>
>   Σ_f ω_f · Res_{u=-γ} (1/L(½+γ+u,f)) · (other factors)
>   
> which involves derivatives `1/L'(ρ_f, f)` at central zeros — **a quantity NOT controlled by current technology**.

So the 1/L-contour approach was blocked by a **commutation issue** between Petersson averaging and contour-shifting in γ as Re(γ) → 0.

## C.2 What the Selberg mollifier gives

From `B_prime_denominator_FULL.md` lines 180-181 (verbatim):

> **Remark 2.3 (why this beats the prior contour-shift attempt).** The prior writeup tried to shift the contour of `1/L(½+γ, f)` from Re(γ) = ε to Re(γ) ↘ 0, encountering the f-dependent zeros of L (§3.4 there). Here we never analytically continue `1/L`; we replace it by the **truncated Dirichlet polynomial mollifier** N_M, which is an entire function of γ.

This is **correct in spirit** — the truncated Dirichlet polynomial Σ_{m≤M} μ_f(m) P(...) m^{-(½+γ)} IS an entire function of γ for fixed M, and so encounters no f-dependent γ-poles. The mollifier-error term E_M(γ, f) shifts the difficulty from "controlling residues at L-zeros" to "controlling Petersson average of |E_M|²".

## C.3 But what the mollifier does NOT give: a NEW unconditional regime

**The HONEST.md verdict is that the mollifier route is just as tightly bound to Re(γ) ≥ 1/4 as the 1/L-contour route was bound to Re(γ) ≥ ε > 0.** The reason: the mollifier-error bound (E') in HONEST.md §4 uses a level-aspect 2nd-moment input

> Σ_f ω_f · L(½+γ-u, f) L̄(½+γ-v, f) ≪ (log N)^{O(1)}    for Re(γ-u), Re(γ-v) ∈ [0, ε]

which is a known unconditional fact (Iwaniec-Sarnak 2000, Duke-Kowalski-Michel 2000), **but only on the open critical strip away from the boundary**. As Re(γ) → 0, the contour shifts demand Re(u) = Re(γ) - 0 → 0+, and the prefactor `M^{D+1} D^{O(D)}` blows up because the optimal mollifier degree D ≍ 1/Re(γ) grows.

From HONEST.md lines 410-422 (verbatim):

> **The honest story.** The Selberg-Beurling mollifier of degree `D` truncated at length `M` has prefactor `M^{D+1} · D^{O(D)}` in the error bound (E). To handle `Re(γ) = δ ∈ (0, 1/4)`, the optimal degree is `D ≍ 1/δ`, and the prefactor becomes `M^{O(1/δ)} · (1/δ)^{O(1/δ)}`. For this to remain `o(1)` after optimisation in `M`, one needs `θ` (the mollifier length exponent) to scale appropriately, but the mollifier-error contribution itself becomes large.
>
> **This is not a 1-day algebraic fix.** It is a known obstruction in the literature ...

So the answer to "what does Selberg mollifier give that 1/L contour-shift didn't?":

1. ✓ **A cleaner statement at Re(γ) ≥ 1/4** — the 1/L route needed an opaque commutation hand-wave at §3.4 of the contour version; the mollifier route is a clean Dirichlet-polynomial argument.
2. ✓ **An honest unconditional theorem at Re(γ) ≥ 1/4 with explicit O(N^{-1/16+ε})** — provided HONEST.md §3-§7 are all rigorous (the most plausible point of failure is the L^2 reduction via Iwaniec-Sarnak 2000 / Duke-Kowalski-Michel 2000, marked 0.65 in the HONEST.md confidence breakdown).
3. ✗ **NO new unconditional regime in Re(γ) ∈ (0, 1/4).** The mollifier construction's polynomial-degree-blow-up obstruction is structurally identical in difficulty to the 1/L contour route's f-dependent-residue obstruction — both require either fractional-moments machinery (Heath-Brown 1981, Soundararajan 2009), the CFKRS-with-quotient program (Conrey-Snaith 2008/2014), or a δ-uniform mollifier construction that is presently open in the literature.
4. ✗ **NO route to Re(γ) = 0** — would require Σ_f ω_f / |L'(½, f)|² control on rank-1 subfamily, open even on GRH.

**Verdict on "structurally cleaner":** TRUE for Lean formalization and writeup-quality at Re(γ) ≥ 1/4. FALSE for opening any new analytic regime. The "structurally cleaner" claim in SESSION_SYNTHESIS line 31 is an aesthetic/expository improvement, not a structural advance to a new theorem.

---

# §D. Regime of validity audit

## D.1 The "Re(γ) ≥ 1/4" line is a hard barrier, not a chosen convenience

The HONEST.md restriction comes from THREE compounding constraints (HONEST.md §2, §3, §4):

**Constraint 1 (HONEST.md §2, line 96-105, verbatim):**

> We work entirely on the open half-plane `Re(γ) ≥ 1/4`, where:
> - `1/L(½+γ, f) = Σ_n μ_f(n)/n^{½+γ}` is **absolutely convergent**: ... so the Dirichlet sum is bounded by `Σ d(n)/n^{¾} = ζ(¾)² < ∞`.
> - The **degree of the Selberg-Beurling mollifier polynomial** can be fixed at `D = 2`, independent of γ. The prefactor `M^{D+1} · D^{O(D)} = M^3 · O(1)` is bounded.
> - We never need a "negative second moment" of `1/|L(½+γ,f)|²` — the trivial Euler-product lower bound `|L(½+γ,f)| ≥ ∏_{p ≤ X} (1+|λ_p|/p^{1/4})^{-1}` ... gives `|L(½+γ,f)| ≥ c > 0`.

So Re(γ) = 1/4 is the barrier where (a) the Dirichlet series for 1/L converges absolutely (using Deligne's |λ_p| ≤ 2 + the bound `Σ d(n)/n^{3/4} = ζ(3/4)²`), AND (b) the Euler-product lower bound on L gives a *uniform-in-f* lower bound (so we don't need a negative moment of 1/|L|²). Both fail for Re(γ) < 1/4.

**Constraint 2 (HONEST.md §3, line 154-167, verbatim):**

> at `Re(s) = ¾ = ½ + 1/4`, we are **inside the absolute-convergence half-plane** ... To avoid this subtlety entirely, we shift the contour to `Re(u) = ½` first, where `Re(γ + u) = ¾ ≥ ½ + 1/4`, then a finite shift to `Re(u) = -1/4 + ε` exists **provided we can justify zero-freeness of `L(s,f)` on `Re(s) ∈ [¾, ½ + 1/4 + ε]`**, which **is** the absolute-convergence side: for any newform `f`, `L(s, f) ≠ 0` on `Re(s) > 1` is unconditional (Euler product), and on `Re(s) ∈ [½, 1]` zero-freeness is GRH (open).
>
> **Honest restriction.** At `Re(γ) ≥ 1/4`, we use the contour `Re(u) = ¾`, so `Re(γ + u) ≥ 1`, which is in the **unconditional zero-free region** (Euler-product absolute convergence).

So the contour shift used to get the mollifier identity is at Re(u) = 3/4, putting Re(½+γ-u) = Re(γ) - 1/4 ≥ 0 only when Re(γ) ≥ 1/4. **The barrier is set by zero-freeness of L on Re(s) > 1 (unconditional Euler product) versus the open GRH on Re(s) ∈ [½, 1].**

**Constraint 3 (HONEST.md §5, lines 270-309 verbatim):** the off-diagonal exponent c' = 1/16 - ε requires M = N^{3/8}, which gives a power-saving error from Weil: this is unaffected by Re(γ), but coupled to Constraints 1 and 2 it locks the whole argument at Re(γ) ≥ 1/4.

## D.2 What would push the regime down

To extend the strategy from Re(γ) ≥ 1/4 to Re(γ) > 0 unconditionally, one of the following is needed:

(a) A **δ-uniform mollifier construction** — i.e. a polynomial $P_\delta$ of bounded degree (independent of δ) achieving the cutoff property at length M without `M^{O(1/δ)}` prefactor blowup. This is open in the literature; HONEST.md cites Bui-Florea, Conrey-Iwaniec-Soundararajan 2012, Bettin-Chandee-Radziwill 2017 as papers that "work in regimes that avoid it".

(b) A **negative moment bound `⟨1/|L(½+γ, f)|²⟩ ≪ (log N)^{O(1)}` for Re(γ) ≥ δ ∈ (0, 1/4)** — without this, the mollifier-error reduction in §3 of FULL.md fails at the Cauchy-Schwarz step. As HONEST.md note (a) above flags, the Soundararajan 2009 citation is wrong; no such bound is currently in the literature for the level-aspect Petersson family at small δ.

(c) A **CFKRS-with-quotient unconditional asymptotic** for the orthogonal symmetry single-ratio at Re(γ) ∈ (0, 1/4). This is the Conrey-Snaith follow-up program; it is conjectural at orthogonal symmetry, partially proved at symplectic symmetry (Conrey-Snaith 2014).

All three are multi-month-to-multi-year efforts. The "1-day algebra" claim in FULL.md §0 was caught by HONEST.md §0 as part of the citation-error pattern.

## D.3 Numerical check at Re(γ) = 0.1 + 0.5i

`B_prime_denom_verify_16curves.gp` and `.out` test 16 curves × 3 γ values (γ = 0.1+0.5i, 0.3+0.5i, 0.5+0.5i). The first gamma (Re(γ) = 0.1) is **inside the open conjectural strip** that HONEST.md leaves open. Reading the .out, |LHS|/|RHS| ratios at Re(γ) = 0.1 are 0.0087-0.0852, consistent with **single-curve fluctuation that is NOT a confirmation of any asymptotic**. Reading FULL.md §6 line 351-354 (verbatim):

> 4. The ratio LHS/RHS, while not 1, is uniformly bounded above and below: `|LHS/RHS| ∈ [0.006, 0.59]` across all 48 trials, consistent with single-form fluctuations (Sato-Tate scatter ≤ √(d_3) ≈ √7 ≈ 2.6 per prime, accumulated over ~50 primes ⇒ overall scatter factor `~exp(O(1))` matching observed range). ✓

**This is structural sanity (LHS finite, RHS finite, no singularities) but NOT a numerical verification of the mollifier theorem.** The theorem is a Petersson-family asymptotic; the 16-curve test lacks any family-averaging. So the .out provides no numerical evidence either way for the Re(γ) > 0 vs. Re(γ) ≥ 1/4 question.

---

# §E. Cross-reference against the documented failed-route bundle

The 16+1+1 = 18 failed Theorem B-exact attack routes flagged in the prompt. For each, I check whether the B'-denom (Selberg mollifier) route is **structurally distinct** from the documented obstruction. This is the key sanity check: if B'-denom hits the same wall, "structurally cleaner" is just a different notation for the same blocker.

## Comparison table

| # | Route | Documented obstruction | Does B'-denom hit the same wall? |
|---|---|---|---|
| 1 | RMT_Painleve_GRH_bypass | "matching the moment of an L-family to the moment of an SO(2N) characteristic-polynomial ensemble at the level of *leading asymptotic equality*, not just shape" — needs off-diagonal control beyond Deligne / large-sieve | **DIFFERENT WALL.** RMT route needs the constant 2/(3π); B'-denom only computes a single-ratio asymptotic R'_F(α,β;γ), not a 4th-derivative-at-zeros object. B'-denom does NOT touch the RMT-side comparison. |
| 2 | RankinSelberg_trace_attack | "Voronoi/Kuznetsov machinery applies to sums of the shape Σ_n a_f(n)·a_f(m+n)·V(n) ... It does not, by itself, evaluate a sum *over zeros* of f without first identifying the zero locus" | **DIFFERENT WALL.** B'-denom is about ratios of L-values at fixed shifts, not sums over zeros. |
| 3 | Voronoi_Kuznetsov_GRH_bypass | Same as #2 — R3 step (zero-identification) is GRH-conditional | **DIFFERENT WALL.** Same reasoning as #2. |
| 4 | arxiv_2601_06292_analysis (DHP-C) | "**NOT TRANSFERABLE to GL(2) Petersson family Theorem B-exact**. The 'unconditional' character is a standard zero-free-region argument applied to a contour integral whose poles are residues at s=1, NOT a GRH bypass for the underlying L-function." | **DIFFERENT WALL.** DHP-C is about ζ on the critical line; B'-denom is GL(2) at off-critical-line shifts. |
| 5 | Theta_lift_GRH_bypass | "The exact constant 2/(3π) ... As an n-level density object this is **4-level**: ... Unconditional n-level density for orthogonal families on F_k: only n = 1 and n = 2 (with restricted support)." | **DIFFERENT WALL.** B'-denom does not aim at 4-level density; it computes a single-ratio average. |
| 6 | FirstPrinciples_creative_attack (10 routes brainstorm) | All 10 routes assessed as either GRH-conditional, motivically-conditional, or "moves the difficulty rather than removing it" | **PARTIAL OVERLAP** at routes 3 (Tauberian extraction) — B'-denom uses similar contour-shift ideas, but at different shifts. None of the 10 brainstorm routes used a Selberg mollifier of inverse-L of a single GL(2) form. So B'-denom is structurally distinct from this brainstorm. |
| 7 | E1_E2_E3_barrier_attack | E1: shifted convolutions at length X² with log weights — **OPEN, comparable to GL(2) 4th moment**. E2: CFKRS step-6 rigorization — OPEN, blocker meets E1. E3: at-zeros↔on-line conversion — PARTIAL, support-2 family density gives a CAGE; exact 2/(3π) requires support-4. | **PARTIAL OVERLAP at E2.** B'-denom IS a step in the CFKRS-with-quotient direction at single-ratio level. But it does NOT close E2 because the Re(γ) = 0 case (the boundary needed for derivative second moments at zeros) is the open part. So B'-denom helps document the blocker but does not bypass it. |
| 8 | Necessary_conditions_inverse | "No subset of CURRENTLY-PROVABLE NCs implies the exact constant" 2/(3π) | **DIFFERENT WALL.** B'-denom does not address NC subset coverage. |
| 9 | Disprove_attempt | Contradiction route — failed (no obvious contradiction from FALSE 2/(3π)) | **DIFFERENT WALL.** Not relevant. |
| 10 | S4_KMV_Mellin_verify (just landed 2026-05-09) | "load-bearing Mellin residue gives leading L³ rational `14/3` (verified to 40+ digits, two independent methods), not `4/(3π) · L⁴`. Two compounding mismatches: (a) leading log-power is 3 not 4; (b) leading constant 14/3 differs from 4/(3π) by factor 7π/2" | **DIFFERENT WALL.** S4 chain breaks because KMV §5 unmollified second moment is `(log)^3` not `(log)^4`. B'-denom is about ratios with shifts at γ in the open strip, not about the L³/L⁴ counting. The Mellin residue mismatch is a different issue. |
| 11 | C2_orthogonal_MC_extended (just landed 2026-05-09) | (Need to read for cross-check) | See §E.2 below. |

## §E.2 C2_orthogonal_MC_extended cross-reference

`C2_orthogonal_MC_extended.md` (2026-05-09) verdict: **FAIL — orthogonal RMT coefficient `b^{SO}_{1,1}(1,1) = 1/2`, NOT `1/12`** (Andrade-Best 2023 verbatim Theorem 2.4). The C2 route's "2/(3π) = (1/(2π))·(1/12)·16" Haar-MC decomposition is wrong by factor 6. **DIFFERENT WALL** from B'-denom — this is a Haar-RMT identity issue (C2's Hughes-Mezzadri decomposition), not a level-aspect mollifier issue.

## §E.3 Net structural assessment

B'-denom is **structurally distinct** from each of the 11 cross-checked routes — it does NOT hit any of their walls directly. But B'-denom also does NOT solve any of them: the Re(γ) ≥ 1/4 restriction means it computes a single-ratio asymptotic away from the central γ = 0 line, while Theorem B-exact requires the central-line second moment of L'(ρ_f, f). These are different objects. So B'-denom is in the "different problem" pile, not the "same wall, different framing" pile.

This means: B'-denom is NOT a route to Theorem B-exact at 2/(3π). It is a separate publishable theorem (B' for Re(γ) ≥ 1/4, post-honest-audit) — useful for the Compositio-tier paper as the bundle's revised plan §"Reframed two-paper plan" envisions, but not advancing the central Theorem B blockers documented in #1-#11.

---

# §F. Verdict (one of the 5 pre-specified options)

**Verdict: BLOCKED-FOR-EXACT, VIABLE-FOR-LEAN-ONLY (specifically: structurally cleaner FORMALIZATION of the already-published Re(γ) ≥ 1/4 result, but no new analytic content).**

Decomposed precisely:

## F.1 Verdict on (a) Theorem B-exact unconditional via Selberg mollifier route

**BLOCKED.** The Selberg mollifier strategy:
- Does NOT touch the central-line second moment of L'(ρ_f, f), which is the actual content of Theorem B-exact.
- Operates on a different object (single-ratio R'_F(α,β;γ) at off-critical-line shifts).
- Even within its own scope, is restricted to Re(γ) ≥ 1/4 by three compounding constraints (Dirichlet absolute convergence at Re(s) > 3/4, contour shift to Re(u) = 3/4, polynomial-degree blow-up for δ < 1/4).
- The 2/(3π) constant is a 4-level density / 4th-derivative-at-zeros object; B'-denom does not address 4-level density. Confidence: 0.02 (essentially closed by the four-walls assessment in §E).

## F.2 Verdict on (b) some weaker but publishable analog

**VIABLE — but already published in HONEST.md.** The honest theorem at Re(γ) ≥ 1/4 with O(N^{-1/16+ε}) error is precisely what HONEST.md captures at confidence 0.55. It is publishable as a Compositio-tier mollified-moments-with-shifts result, modulo:
- Resolving the Iwaniec-Sarnak / Duke-Kowalski-Michel L^2 reduction (HONEST.md §4 "0.65" step) — needs primary-source verification of shift-uniform 2nd moment.
- The bad-prime Euler factor B_p computation (1-day algebra, currently sketched).
- A genuine Petersson-family-averaged numerical run (currently the 16-curve dataset is one-form-per-level, not an averaged check).

The "structurally cleaner than 1/L contour shift" observation is correct as an aesthetic / formalization improvement — the mollifier route avoids the f-dependent-residue commutation hand-wave at §3.4 of the contour writeup. But the analytic content (Re(γ) ≥ 1/4, c' = 1/16 - ε) is unchanged from what the contour route also achieves (per HONEST.md §5 verbatim "the contour-version's claim numerically").

## F.3 Verdict on (c) is itself blocked

**The Re(γ) ∈ (0, 1/4) extension IS BLOCKED by:**

1. **Polynomial-degree blow-up obstruction.** The mollifier degree D ≍ 1/Re(γ) makes the prefactor M^{D+1} D^{O(D)} unmanageable as Re(γ) → 0. Per HONEST.md §8.1 (verbatim): "**This is not a 1-day algebraic fix.** It is a known obstruction in the literature (Bui-Florea, Conrey-Iwaniec-Soundararajan 2012, Bettin-Chandee-Radziwiłł 2017 all work in regimes that avoid it)."

2. **Negative second moment unproven.** ⟨1/|L(½+γ, f)|²⟩ ≪ (log N)^{O(1)} for Re(γ) ∈ (0, 1/4) is open (the Soundararajan 2009 citation in FULL.md was caught as wrong by HONEST.md).

3. **Boundary Re(γ) = 0** requires Σ_f ω_f / |L'(½, f)|² control on rank-1 subfamily — open even on GRH.

## F.4 Specific check on the "GRH for the mollified L-function" pitfall (per prompt's "familiar pitfall")

The prompt warns: "Selberg-Beurling positivity property may silently assume GRH for the mollified L-function." Checking:

- The Selberg 1942 mollifier `M(s, θ) = Σ_{n≤y} μ(n) P(...)/n^s` is an entire function of s for fixed y — no L-function zeros assumed.
- The mollifier identity `L · M = 1 + E_M` is unconditional (no GRH).
- The second-moment input `⟨L L̄⟩_F ≪ (log N)^{O(1)}` (HONEST.md §4) is unconditional level-aspect (Iwaniec-Sarnak 2000, Duke-Kowalski-Michel 2000).
- The negative-moment input `⟨1/|L|²⟩ ≪ (log N)^{O(1)}` for Re(γ) ≥ 1/4 is replaced in HONEST.md by a TRIVIAL Euler-product lower bound (HONEST.md §2 line 102-105): for Re(s) > 3/4 absolute convergence gives `|L(½+γ,f)| ≥ c > 0` uniformly. This is unconditional and does NOT use GRH.

**So no GRH-for-mollified-L is hidden in HONEST.md.** The Re(γ) ≥ 1/4 restriction comes from ABSOLUTE CONVERGENCE of 1/L (Re(s) > 3/4 = 1/2 + 1/4), not from any zero-freeness assumption. This is a subtle but real distinction: the strategy is unconditional in its restricted regime precisely because Re(s) > 3/4 is in the absolute-convergence half-plane. **The pitfall does not apply to HONEST.md.** (It DID apply to FULL.md's claim of unconditional Re(γ) > 0, which silently used a wrong-cite negative-moment input.)

## F.5 Verdict summary (single-line)

**BLOCKED for Theorem B-exact, BLOCKED for Re(γ) ∈ (0, 1/4) extension, VIABLE-FOR-LEAN-ONLY for Re(γ) ≥ 1/4 (where it is structurally cleaner than 1/L contour-shift but gives no new analytic content beyond what the contour route also achieves).**

Aggregate confidence on "Selberg mollifier route opens a NEW unconditional path to Theorem B-exact 2/(3π)": **0.02** (capped by §E walls + §F.1 + §F.3 obstructions).

Aggregate confidence on "Selberg mollifier gives a structurally cleaner formalization of the Re(γ) ≥ 1/4 result, suitable for Lean": **0.65** (capped by 0.55 from HONEST.md row + 0.10 uplift for Lean-formalization advantage of avoiding the contour-shift commutation handwave).

Aggregate confidence on "the SESSION_SYNTHESIS line 31 'structurally cleaner' claim is essentially correct AS AN AESTHETIC observation, but DOES NOT extend to opening a new structural route": **0.85** (the bundle's own honest line 67 already captures this — confidence 0.55 unchanged for Re(γ) ≥ 1/4 only).

---

# §G. Specific next steps

## G.1 If the program treats Re(γ) ≥ 1/4 as the publishable target

**This is what HONEST.md §10 already advocates.** Concrete next steps to push HONEST.md from 0.55 → 0.70+ confidence (per HONEST.md §9):

1. **Aristotle Lean target — formalize the mollifier identity (Lemma 2.1 of HONEST.md) for Re(γ) ≥ 1/4.** Specification:
   - State the identity `L(½+γ, f) · N_M(γ, f) = 1 - E_M(γ, f)` for `M = N^{3/8}`, `Re(γ) ≥ 1/4`, `D = 2`, `P(x) = 1 - (1-x)²`.
   - Lean target lemma: `∀ f ∈ S₂*(N), ∀ γ with Re(γ) ≥ 1/4 and |γ| ≤ 1/log N, L(½+γ, f) · N_M(γ, f) - 1 = -E_M(γ, f)` where `E_M` is the explicit Mellin contour integral of HONEST.md eq. (★) at Re(u) = 3/4.
   - Avoids the L-function zero-freeness issue because the contour stays in the absolute-convergence half-plane Re(s) > 3/4.
   - This is the cleanest part of the proof — no Petersson averaging, no off-diagonal — just a Möbius convolution identity. Estimated effort: 2-4 weeks for Aristotle.

2. **MIMO bulk task spec — Petersson-averaged numerical check at fixed N₀.** Specification:
   - Pick N₀ = 1009 (prime, |S₂*(1009)| ≈ 85 newforms) or N₀ = 5005 (squarefree, 16 newforms).
   - Compute LHS = harmonic-Petersson average over `S₂*(N₀)` of `L(½+α,f) · L(½+β,f) / L(½+γ,f)` for α=0.05, β=-0.03, γ ∈ {0.25+0.5i, 0.5+0.5i, 1.0+0.5i} (Re(γ) ≥ 1/4 grid).
   - Compute RHS = HONEST.md G_3 formula via §6.
   - Target: |LHS - RHS| / |RHS| < 5%.
   - Effort: 1-2 days PARI/GP scripting, 1 day compute.

3. **Opus extra-high task spec — bad-prime Euler factor B_p computation.** Specification:
   - Compute the explicit Euler factor `A_p^{bad}(α, β, γ)` for p|N (squarefree N), starting from the local L-factor `L_p(s, f) = (1 - λ_p p^{-s})^{-1}` with `λ_p = ε_p / √p`.
   - Pin down the exact form (currently sketched in HONEST.md §6 last paragraph as "1 day of careful algebra").
   - Verify ∏_{p|N} A_p^{bad} = 1 + O(log log N / log N) explicitly.
   - Effort: 1 day Opus extra-high.

## G.2 If the program insists on Re(γ) > 0 (full open strip, dropping the 1/4 restriction)

**Multi-month research, NOT Compositio-deliverable in current state.** Sub-tasks:

1. **A δ-uniform mollifier construction.** Hard. Open. The Conrey-Iwaniec-Soundararajan 2012 "asymptotic large sieve" approach is the closest analog but doesn't yet treat the GL(2) inverse-L mollifier. Effort: 3-6 months.

2. **Negative second moment ⟨1/|L|²⟩ for Re(γ) ∈ (0, 1/4).** Open. Requires either Heath-Brown 1981 fractional moments adapted to GL(2), or Soundararajan 2009 mollifier lower bound adapted to level-aspect Petersson. Effort: 2-4 months.

3. **Both 1 and 2 simultaneously.** Combined effort: 4-8 months. High risk.

## G.3 If the program targets Theorem B-exact 2/(3π) via a different route

**B'-denom is not a route to Theorem B-exact.** Per §E, the 2/(3π) constant is a 4-level density object; B'-denom is a single-ratio object. The relationship between them goes through CFKRS-with-quotient (Conrey-Snaith 2008/2014 program), which is partially open at orthogonal symmetry. So:

1. **Forget B'-denom for Theorem B-exact.** It's the wrong tool.
2. **Pursue Theorem B WEIGHT aspect** (per SESSION_SYNTHESIS line 117 verbatim: "Theorem B WEIGHT aspect (the real Annals headline) is 0.95+ and untouched by all this. That remains the load-bearing claim.").
3. **Drop Theorem B LEVEL aspect at 2/(3π) unconditional** to multi-decade open category (per S4_KMV_Mellin_verify.md §8 verbatim: "Theorem B-exact unconditional at `2/(3π)` via the standard route is in the multi-decade open category.").

## G.4 What unblocks the assessment if the verdict is wrong

This audit could be wrong (with probability ≤ 0.15) if:

(a) **A primary-source verification of Selberg 1942 Skr. Norske paper** reveals a δ-uniform mollifier construction not in the modern follow-up literature (Conrey 1989, Bui-Florea 2018, etc.). Searches via WebFetch did not retrieve the 1942 paper. If retrieved, sections 4-7 of Skr. Norske 10/1942 (probability 0.03 of containing such a construction).

(b) **A primary-source check of Bui-Florea 2018** (the *correct* paper, arXiv:1611.09582 or possibly the related arXiv:1611.10095 misidentified citation could be a fragment of a different paper) reveals a level-aspect Petersson inverse-L mollifier with shift uniformity. WebSearch suggested arXiv:1611.09582 is GL(1) Dirichlet, not GL(2). Probability 0.03.

(c) **A new development in 2024-2026 literature** on δ-uniform mollifiers I haven't located. WebSearch up to current date (2026-05-09) shows no breakthrough. Probability 0.04.

(d) **The 1/L-contour route's commutation issue is more genuinely "fixed" by the mollifier than HONEST.md acknowledges** — i.e. Re(γ) ∈ (0, 1/4) actually works under some unspecified additional input. Probability 0.05.

Total probability of mistaken verdict: ≤ 0.15.

---

# §H. Honest self-audit

I aimed to assess whether B'-denom (Selberg mollifier route) opens a NEW unconditional path. Result: **BLOCKED for Theorem B-exact, VIABLE-FOR-LEAN-ONLY for the already-published Re(γ) ≥ 1/4 sub-result.**

**What I verified:**
- Conrey "Mollifying the Riemann zeta-function" PDF (10 pages) — verbatim mollifier definition + θ < 4/7 / θ < 1/2 regimes + reference [S1] to Selberg 1942.
- KMV 2002 (Duke 114) PDF (50 pages) — verbatim Theorem 7.3 (Rankin-Selberg 2nd moment, level aspect, |δ|, |δ'| ≤ 1/log q regime), eq. (9.1) (the actual mollifier KMV uses, which is RS-type with μλ_f λ_g not 1/L of single GL(2)), §1 contents (no Lemma 1.4), §2 contents (no Lemma 2.1 or 2.4). The "KMV 2002 Lemma 1.4 / Lem 2.1 / Lem 2.4" cited in `B_prime_denominator_FULL.md` are all **fabricated**.
- arXiv:1611.10095 — confirmed to be a CS paper, NOT Bui-Florea. The bundle's identifier is wrong by one digit (correct Bui-Florea mollification paper is arXiv:1611.09582), and even the correct paper is GL(1) Dirichlet not GL(2).

**What I did not verify (marked as gaps):**
- Selberg 1942 Skr. Norske paper itself (retrieval failed).
- Beurling 1937 unpublished manuscript (not retrievable).
- Iwaniec-Sarnak 2000 §7 / Duke-Kowalski-Michel 2000 (HONEST.md's L^2 input). Not retrieved; HONEST.md flags this as a "modest confidence loss (≈ 0.05)" itself.

**Pattern lesson absorbed:** the SESSION_SYNTHESIS warning about "5-of-5 prior agents inflating with same-shape mis-citation error" applies HERE TOO — `B_prime_denominator_FULL.md` contains at least 4 caught fabricated citations (Soundararajan 2009 wrong paper [HONEST §0 #2], KMV-Duke L^4 doesn't exist [HONEST §0 #3], KPY Prop 1 doesn't exist [HONEST §0 #4], arXiv:1611.10095 wrong paper [this audit §B.5]). The HONEST.md restriction to Re(γ) ≥ 1/4 is the post-audit truthful version. The "structurally cleaner" line in SESSION_SYNTHESIS line 31 is a pre-audit aesthetic observation; the post-audit live confidence is 0.55, restricted.

**Net:** the assessment confirms the bundle's own honest line. There is no NEW route here.

---

# §I. One-paragraph executive summary (for synthesis)

The "B'-denominator via Selberg-Beurling mollifier" strategy is **structurally distinct** from all 11 documented failed Theorem B-exact attack routes (RMT/Painleve, Rankin-Selberg trace, Voronoi-Kuznetsov, DHP-C transferability, theta-lift, FirstPrinciples 10-route brainstorm, E1/E2/E3 barriers, necessary-conditions inverse, disprove-attempt, S4_KMV Mellin, C2 orthogonal MC) — but it is also **not a route** to Theorem B-exact at 2/(3π). Within its actual scope (single-ratio R'_F at off-critical-line shift Re(γ) ≥ 1/4), the strategy gives a Compositio-tier publishable theorem with O(N^{-1/16+ε}) error, structurally cleaner than the 1/L contour-shift route (which had a commutation hand-wave at the f-dependent-residues step). The "structurally cleaner" observation in `SESSION_SYNTHESIS_extra_high_round.md` line 31 is correct as a Lean-formalization aesthetic improvement, but does NOT extend to opening any new analytic regime: the Re(γ) ∈ (0, 1/4) gap is blocked by polynomial-degree blowup in the mollifier (M^{O(1/δ)} prefactor), and Re(γ) = 0 is blocked by the open ⟨1/|L'(½,f)|²⟩ rank-1-subfamily problem. The bundle's `B_prime_denominator_FULL.md` claim of unconditional Re(γ) > 0 is invalidated by 4 caught fabricated citations (Soundararajan 2009, KMV-Duke L^4, KPY "Prop 1", and arXiv:1611.10095 wrong-paper); HONEST.md is the live version at confidence 0.55, restricted to Re(γ) ≥ 1/4. Verdict: **VIABLE-FOR-LEAN-ONLY** (clean formalization target for the already-published result), **BLOCKED-FOR-EXACT** (does not open a path to Theorem B at 2/(3π)). Aggregate confidence on "opens a new unconditional route to Theorem B-exact": 0.02. Aggregate confidence on "structurally cleaner Lean target for the existing Re(γ) ≥ 1/4 theorem": 0.65.

# Done.
