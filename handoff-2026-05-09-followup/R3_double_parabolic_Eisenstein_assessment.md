---
title: "R3: Double-parabolic Eisenstein cross-term — unconditional evaluability assessment"
type: structural-assessment
domain: research
tier: working
date: 2026-05-09
auditor: Opus 4.7 (1M ctx), extra-high reasoning
verdict: **BLOCKED-AT-WALL — same wall as Theorem B-exact (Ratios Conjecture / GRH for ζ × sym²f)**.
   No route (a)-(e) closes the residue evaluation unconditionally to a SINGLE specific value.
   Best partial — route (b) Hoffstein–Lockhart — gives a *signed cage interval* of the
   exact same width as the M-N cage (no improvement); routes (a),(c),(d),(e) all blocked.
sources_verified:
  - "Hoffstein, J.; Lockhart, P. *Coefficients of Maass forms and the Siegel zero* (with appendix by D. Goldfeld, J. Hoffstein, D. Lieman). Annals of Math. **140** (1994) 161–181. PDF retrieved 2026-05-09 from Goldfeld's website (math.columbia.edu/~goldfeld/CoeffMaassForms.pdf), 17pp; full text. Theorems 0.1, 0.2 and Proposition 1.1 quoted verbatim below."
  - "Beilinson, A. A. *Higher regulators and values of L-functions*. Itogi Nauki i Tekhniki, Ser. Sovremennye Problemy Mat. (Noveishie Dostizheniya) **24** (1984), 181–238; transl. J. Soviet Math. **30**(2) (1985) 2036–2070. PDF retrieved 2026-05-09 (35pp). Conjectures 3.4, 3.7, 3.8, 3.10 quoted verbatim; §5–§7 status (proven cases) confirmed."
  - "Iwaniec, H.; Michel, P. *The second moment of the symmetric square L-functions*. Rev. Mat. Iberoamericana, see also EPFL preprint ~2000–2001. PDF retrieved 2026-05-09 from infoscience.epfl.ch (15pp). Theorem 1.1 quoted verbatim below."
  - "Friedberg, S.; Goldfeld, D. *Mellin transforms of Whittaker functions*. Bull. Soc. Math. France **121** (1993), 91–107. PDF retrieved 2026-05-09 from numdam.org (18pp). Main results in §2 quoted."
  - "Michel, P.; Venkatesh, A. *The subconvexity problem for GL_2*. Publ. Math. IHES **111** (2010), 171–271. Webpage abstract retrieved 2026-05-09 from numdam.org. Scope confirmed: GL(1), GL(2) ONLY (not GL(3) where sym²f sits)."
sources_attempted_but_inadequate:
  - "Mestre, J.-F.; Schappacher, N. (numerical evidence on sym² of an elliptic curve and Beilinson conjecture). Confirmed via web search: numerical evidence only, NOT a proof. (Encyclopedia of Mathematics summary; Beilinson 1984 §5 also explicit that proven case for modular curves is at s=2 NOT s=1 sym².)"
  - "Cohen-Friedlander 'subconvexity' paper as called out in the prompt: NO such Cohen-Friedlander paper found in literature search 2010–2017. The relevant subconvexity unconditional results are Duke–Friedlander–Iwaniec 1990s/2000s and Michel–Venkatesh 2010, both restricted to GL(1)+GL(2)."
  - "Goldfeld 2006 *Automorphic forms and L-functions for the group GL(n,R)* — Cambridge monograph; not retrievable in PDF; structural results known via Friedberg–Goldfeld 1993 + Stade 2002 (the Mellin-machinery papers). Conclusions for the assessment do not depend on direct page citation here; they depend only on the *structure* (meromorphic continuation + difference equations of the Mellin transform), which is the textbook content."
  - "Cohen, H.; Friedlander (the prompt cites these), 2010/2017: no joint Cohen-Friedlander subconvexity paper located. Treating the route as 'subconvexity for the Eisenstein cross-term' more generally — i.e., Michel–Venkatesh and successors — but verbatim Cohen-Friedlander citation FAILS verification (route (d) downgraded accordingly; see §4(d))."
prior_failures_consulted:
  - "handoff-2026-05-04-theorem-B-and-C1/Synthesis_Petersson_Voronoi_Selberg.md (§4.3 Identity (E), §6.5 single-residue obstruction, §3.3 parabolic residue regularization)"
  - "handoff-2026-05-04-theorem-B-and-C1/C1_SELF_RESIDUE_HANDOFF.md §9 (single most important open question), §15.3 (specific reviewer ask)"
  - "handoff-2026-05-04-theorem-B-and-C1/MK3_Bridge_Selberg_VERIFIED.md (universal kernel context for Selberg class L-functions)"
  - "handoff-2026-05-04-theorem-B-and-C1/THEOREM_B_HANDOFF.md §3 (the structural obstruction = support-4 wall)"
  - "handoff-2026-05-04-theorem-B-and-C1/Voronoi_Kuznetsov_GRH_bypass.md (R3 reappears spectrally)"
  - "handoff-2026-05-04-theorem-B-and-C1/Theta_lift_GRH_bypass.md (Howe duality is rep-level not density-level transfer)"
  - "handoff-2026-05-04-theorem-B-and-C1/arxiv_2601_06292_alt_GL2_routes.md (DHPC engine has no analog for averaged quartic-L; same wall)"
tags: [C1-mechanism, double-parabolic, eisenstein-cross-term, single-residue, beilinson-deligne, hoffstein-lockhart, goldfeld-stade, subconvexity, BLOCKED-AT-RATIOS-WALL]
---

# §0. Confidence aggregation rule (single rule, applied uniformly)

**Rule.** Posterior confidence in a per-route claim "route X closes the residue
evaluation unconditionally" =
`MIN over load-bearing inputs I_i of P(I_i correct)`,
where `P(I_i correct)` is set by:

| Status of input I_i | P(correct) |
|---|---|
| Verified verbatim against retrieved primary source (PDF + Read, with quote and page) | 1.00 |
| Verified against repository file with verified provenance (1-step indirection) | 0.95 |
| Cited only via secondary source (web search summary, encyclopedia) | 0.70 |
| Explicitly marked `[UNVERIFIED]` by this agent | 0.10 |
| Explicitly **falsified** against retrieved primary source (citation error caught) | 0.00 |

The MIN aggregation means a single broken or hidden-GRH link in a load-bearing
chain caps the route's overall confidence at the broken link's confidence. This
matches the rule used in `S4_KMV_Mellin_verify.md` §9 and
`B_prime_denom_Selberg_Beurling_assessment.md` §0.

**Aggregate verdict for the report** = max over routes (a)–(e) of route confidence,
plus an epistemic-uncertainty `+0.05` for "I missed a route." That maximum is
shown to be **≤ 0.10** in §6.

---

# §1. The obstruction, verbatim from `Synthesis_Petersson_Voronoi_Selberg.md` §6.5

The single residue at issue is the **double-parabolic cross term** of the
Selberg-trace expansion of the operator `T_{K,T}` representing `M_F(T)`. From
`Synthesis_Petersson_Voronoi_Selberg.md` §6.5 lines 648–681 (verbatim):

> ## 6.5 The double-parabolic cross term
>
> The cleanest identification of the obstruction: in the Selberg trace
> expansion, the *parabolic-parabolic* cross term (where two of the four
> Eisenstein-type contour integrals interact) is a single residue:
>
>   (double parabolic) = Res_{s=1} [Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A, A⟩(s)],
>
> where Λ is the completed zeta and ⟨A, A⟩(s) is the M-N mollifier inner
> product Mellin-transform.
>
> **On RHf:** Λ(2s−1)/Λ(2s) is regular at s=1, the residue is well-defined,
> and equals (after computation analogous to Conrey-Snaith) precisely
> 2/(3π) − 17/(12π) = −3/(4π).
>
> **Off RHf:** Λ(2s−1)/Λ(2s) may have additional poles at s=½+iγ, β > ½
> in principle. (Numerical evidence is overwhelming that ζ has no zeros
> off the line, but unconditionally we cannot rule out β > ½.) These
> poles shift the residue by ≤ |β−½|·log T per pole.
>
> **This is the cleanest one-line obstruction.** The exact 2/(3π) reduces
> to "no off-line zeros of ζ contribute to the residue at s=1 of the
> double-parabolic cross term." This is **strictly weaker** than RHf for
> f, but **strictly stronger** than the family-averaged zero-density of
> KM 1997.
>
> In particular, **bypassing this obstruction requires either RH for ζ
> (needed for ⟨A, A⟩(s) to be regular near s=1) or a Plancherel-Sato-Tate
> result that pins the residue value averaged over f.** Neither is known.

The same residue is summarized in `C1_SELF_RESIDUE_HANDOFF.md` §4.1 (lines
112–123) as the regularized residue inside the operator-theoretic identity:

> $$ M_F(T) = \mathrm{tr}\big(P_{\text{holo}} \circ T_h \circ P_{\text{holo}}\big)
>   + \text{Res}_{s=1}^{\text{reg}}\Big[ E(s) \cdot R_h(s) \Big]
>   + \mathcal{O}(\text{Bessel-decayed off-diagonal}) $$
>
> where: ... `E(s)` is the standard Eisenstein series of GL(2) at level N,
> `R_h(s)` is a regularized resolvent kernel, and the "regularized residue"
> is the **double parabolic** cross term.

And in `Synthesis_Petersson_Voronoi_Selberg.md` §3.3 (lines 397–422), the
constituent ingredients are spelled out:

> The parabolic side of the Selberg trace for our T_{K,T} is the divergent
> integral
>
>   (parabolic contribution) = ∫_{Re s = 1/2} h(t) · |c_∞(s)|² · ds,
>
> where c_∞(s) is the constant term coefficient of the Eisenstein series
> at the cusp ∞. For Γ₀(N), c_∞(s) involves the completed Riemann zeta:
> Λ(2s−1)/Λ(2s) ...
>
> ... **Off RHf:** the residue value is replaced by an integral over a contour
> that picks up off-line zeros of L(s, f×f̄) = ζ(s)·L(s, sym²f). The
> zeros of ζ contribute (no info; can be off-line) and zeros of L(s, sym²f)
> contribute (sym² unconditional GRH unknown). So the residue value lies
> in the cage [(17 ± √145)/(12π)], not at 2/(3π) specifically.

## 1.1 Inputs to the residue: which are unconditional, which are conditional

The residue is a **function of three load-bearing inputs**:

1. `Λ(2s−1)/Λ(2s)` — completed Riemann zeta ratio, with poles at
   `s = 1/2 + iγ` for off-line ζ-zeros (none known, but unconditionally
   not ruled out beyond the classical zero-free region width
   `c/log(|t|+2)`).
2. `L(s, sym²f)` — symmetric square L-function. Entire (Gelbart–Jacquet
   1978; quoted verbatim in HL1994 page 162: *"The function L(s, F) is
   known to be entire, and L(1, F) ≠ 0"*). But its zeros off `Re(s) = 1/2`
   are unknown unconditionally — Hoffstein–Lockhart only excludes a Siegel-style
   real zero (and only "with at most one exception").
3. `⟨A, A⟩(s)` — Milinovich–Ng mollifier inner product. Has a pole at
   `s = 1` of finite order = polynomial-in-`(log T)`, this part is
   unconditional (algebraic).

**Unconditional inputs:** Gelbart–Jacquet for sym² is entire (✓); Voronoi
pairing on the Eisenstein side (✓); polynomial structure of `⟨A,A⟩(s)` (✓).

**Conditional inputs:** *all* the input that pins the residue to a SPECIFIC
NUMERICAL VALUE — namely, the absence of additional contributions from
off-line zeros of `Λ(2s−1)/Λ(2s)` AND from off-line zeros of `L(s, sym²f)`.
Without ALL of these, the residue evaluates to a **signed cage** value in
`[(17−√145)/(12π), (17+√145)/(12π)] · ⟨c_f⟩ · T · log⁴(NkT)`, exactly
matching the cage of `THEOREM_B_HANDOFF.md` §2a.

This is the precise meaning of the §6.5 statement *"residue value lies in
the cage [(17 ± √145)/(12π)], not at 2/(3π) specifically."*

---

# §2. Sanity check on Identity (E) framework

Identity (E) as stated in `C1_SELF_RESIDUE_HANDOFF.md` §4.1:

```
M_F(T) = tr(P_holo · T_h · P_holo) + Res_{s=1}^{reg}[E(s) · R_h(s)]
       + O(Bessel-decayed off-diagonal)
```

with `P_holo` the projector onto holomorphic cusp forms, `T_h` Hecke
convolution, `E(s)` Eisenstein, `R_h(s)` regularized resolvent.

## 2.1 Internal consistency check

- **Spectral-side consistency.** `tr(P_holo T_h P_holo)` is the holomorphic
  contribution; it is bounded by the cage center 17/(12π) per
  `Synthesis_Petersson_Voronoi_Selberg.md` §5.2, modulo trace-class
  (which `Synthesis_Petersson_Voronoi_Selberg.md` §3.2 explicitly flags
  as load-bearing-but-not-rigorous, conf 0.40).
- **Eisenstein-side consistency.** The regularized residue is a single
  number that must shift the holomorphic value by exactly
  `2/(3π) − 17/(12π) = −3/(4π)` to recover the M-N predicted value. This
  matches the §6.1 algebra (`17/(12π) − 2/(3π) = 9/(12π) = 3/(4π)`) ✓.
- **No double-counting.** The Bessel-decayed off-diagonal absorbs the
  Petersson off-diagonal Kloosterman sums; this requires `k > 4eT/√N`
  (the standard ILS threshold; quoted in `THEOREM_B_HANDOFF.md` §1
  line 21 as part of Theorem B's hypothesis). ✓
- **Symmetry-type consistency.** The Petersson family `S_k*(N)` has
  orthogonal symmetry (ILS 2000); the residue is real-valued because
  it equals a residue of a self-dual L-function product
  `Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A,A⟩(s)`, all three factors invariant
  under `s ↔ 1−s` after suitable conjugation. ✓

## 2.2 Trace-class flag

The framework is **internally consistent at the level of formal identity**.
The trace-class status of `T_{K,T}` is acknowledged in
`Synthesis_Petersson_Voronoi_Selberg.md` §3.2 (lines 393–395) as conf 0.40.
This is upstream of (a)–(e) — every route below ASSUMES Identity (E) holds
in trace-class. If trace-class fails, the residue isn't even well-defined,
in which case the question is moot. We proceed as if Identity (E) is
trace-class (conf 0.40 baseline).

**Verdict on Identity (E) framework:** Internally consistent, formally well-defined,
load-bearing trace-class assumption flagged but plausible. Proceed to §3.

---

# §3. Verbatim primary-source citations for routes (a)–(e)

## 3.1 Hoffstein–Lockhart 1994 main theorems (PDF verified)

From `HL1994.pdf` page 5 (= Annals 140 p.164), verbatim:

> THEOREM 0.1. Suppose there exists a constant `c` such that `L(s,F)` has
> no real zeros in the range
>
>   `1 - c/log(λN+1) < s < 1`.
>
> Then there are effective constants `c_1` and `c_2`, depending only on `c`,
> such that
>
>   `L(1,F) ≥ c_1/log(λN + 1)`
>
> and
>
>   `|p(1)|² ≤ c_2 log(λN + 1)`.

> THEOREM 0.2. For any `ε > 0`, there exists an effective constant `c(ε)`
> so that the inequality
>
>   `L(1,F) > c(ε)(λN)^{-ε}`
>
> holds for all `F` with at most one exception.

> COROLLARY 0.3. ... `p(1) ≪_ε (λN)^ε`.

And from page 4 (Annals p.163, `HL1994.txt` lines 60–95), verbatim Remark:

> *The methods used here can be easily applied to holomorphic (resp.
> nonholomorphic) cusp forms of weight k. One obtains results identical
> to those above, with the term λN replaced by kN (resp. λkN).*

So **for holomorphic forms** (our case), HL gives effective lower bound
`L(1, sym²f) ≥ c_1 / log(kN + 1)` *conditionally* on no real zero in the
classical zero-free region (Theorem 0.1), and unconditionally
`L(1, sym²f) > c(ε)(kN)^{-ε}` *with at most one exception* (Theorem 0.2,
Tatuzawa-form ineffective constant).

The connection to the Eisenstein-series residue is also explicit in
HL page 3 (Annals p.162) eq (0.5)–(0.8):

> `Res_{s=1} L(s, f×f) = (4/3) |p(1)|²`
> ... `L(s, f×f) = ζ(s) L_N(s) L(s, F)`
> ... `Res_{s=1} L(s, f×f) = L_N(1) L(1, F)`.

Here `L(s, F) = L(s, sym²f)` (Gelbart–Jacquet adjoint square lift).

## 3.2 Beilinson 1984/1985: proven cases — verbatim

From `Beilinson.pdf` page 1 (J. Soviet Math. 30 p.2036), introduction:

> Sec. 3 contains formulations of the basic conjectures connecting
> regulators with the values of L-functions at integral points
> *distinct from the middle of the critical strip*; the arithmetic
> intersection index defined in part 2.5 is responsible for the
> behavior in the middle of the critical strip. From these
> conjectures (more precisely, from the part of them that can be
> applied to any complex manifold) there follow rather unexpected
> assertions regarding the connection of Hodge structures with
> algebraic cycles. The remainder of the work contains computations
> corroborating the conjectures in Sec. 3. Thus, in Sec. 7 we prove
> these conjectures for the case of Dirichlet series; Sec. 5
> contains a result giving a partial proof of the conjecture for
> values at two of L-functions of curves uniformized by modular
> functions; Sec. 6 contains an analogous computation for the
> product of curves of this type.

Key proven cases (page 2):

- **§5:** L-functions of curves uniformized by modular functions, **at s = 2**
  (ergo: `L(s, X_0(N))` at `s = 2`, i.e. `L(s, f)` at `s = 2` for weight-2
  modular forms by Eichler–Shimura).
- **§6:** Products of two modular curves (`L(s, f × g)`-type Rankin–Selberg
  at `s = 2`).
- **§7:** Dirichlet L-functions, all integer points (Borel theorem).

From page 6 (J. Soviet Math. 30 p.2057), Conjecture 3.7 (the master
conjecture that is what would-be needed for `L(1, sym²f)` and is
**stated as conjecture, not theorem**):

> Conjecture 3.7. a) The order of a zero of `L^(j)(M^0, s)` at `s = n = j/2`
> is equal to `d(j, n) := dim H^{2n+1}_{Mt}(M_Z, Q(n+1))`. b) The mapping
> `c·R r_n: H^{j+1}_{Mt}(M_Z, Q(n+1)) ⊗ R → H^{j+1}_D(M_R, R(n+1))` is an
> isomorphism. c) Let `c(j, n)` be the leading term of the asymptotics
> ... then `c(j, n) · ρ(j, n) = det r_n(H^{j+1}_{Mt}(M_Z, Q(n+1)))`.

This is the conjecture for `L(s, M)` at the **center** `s = j/2` of the
critical strip. For `L(s, sym²f)`, the motive `M = sym² h^1(E)` has weight
`j = 2`; the center is `s = 1`. So **`L(1, sym²f)` is exactly the case
covered by Conjecture 3.7 — which is OPEN** (Beilinson 1984 did not prove
it, and as of 2026-05-09 it remains conjectural for `sym² f`).

The **only proven cases** in Beilinson 1984 are §5–§7 (modular curves at s=2,
Dirichlet at integer points). §5 is "partial" (the K_2-element exists
in the right cohomology, but the integrality condition was added later by
Schappacher–Scholl 1991).

## 3.3 Iwaniec–Michel 2002 verbatim

From `IM_sym2.pdf` page 1, Theorem 1.1:

> Theorem 1.1. Let `k, N` be positive integers, `k` even, `N` squarefree.
> Let `B*_k(N)` be the set of primitive cusp forms of weight `k` with
> respect to the group `Γ_0(N)`. For each `f ∈ B*_k(N)` let `L(sym²f, s)`
> be the corresponding symmetric square L-function. Let `Re s = 1/2`. We
> have
>
>   `Σ_{f ∈ B*_k(N)} |L(sym²f, s)|² ≪ |s|⁸ N^{1+ε}`
>
> for any `ε > 0`, the implied constant depending only on `ε` and `k`.

This is on the **critical line `Re s = 1/2`**, not at `s = 1`, and it is an
**upper bound**, not an asymptotic. From page 2:

> Our method does not yield an asymptotic formula for the second power
> moment of `L(sym²f, s)` because the estimate (1.6) is not precise enough.

So IM 2002 does NOT give an unconditional asymptotic, even on the
critical line and even for the second moment — and the L-value at issue
in the residue is at `s = 1`, not `s = 1/2`.

## 3.4 Friedberg–Goldfeld 1993 (Mellin transforms / Goldfeld–Stade machinery)

From `Stade.pdf` page 2 (BSMF 121 p.91), Abstract:

> Let G be a connected reductive algebraic group defined and quasi-split
> over R. In this paper the Mellin transform of the Whittaker function
> associated to G is studied. It is shown that this Mellin transform has
> a meromorphic continuation and satisfies certain explicit difference
> equations. An effective algorithm for obtaining these difference
> equations is presented, and is illustrated in low rank cases for `G = GL(n)`.

So Friedberg–Goldfeld 1993 (on which the Goldfeld–Stade GL(3) pairing
machinery rests) provides:

(i) Meromorphic continuation of the Mellin transform of the Whittaker
function (structural).

(ii) Difference equations relating Mellin transforms at shifted arguments
(structural).

(iii) **Explicit closed-form evaluation only when reduced via the difference
equations to gamma-function ratios**, which Stade 2002 exploits in low
rank.

These are *structural* results — they tell us the residue exists and
satisfies certain algebraic relations, but they do NOT evaluate the
specific residue we need in §6.5 to a single specific numerical value
without further input.

## 3.5 Michel–Venkatesh 2010 subconvexity

From numdam.org abstract retrieved 2026-05-09:

> We solve the subconvexity problem for the L-functions of `GL_1` and
> `GL_2` automorphic representations over a fixed number field, uniformly
> in all aspects.

The result is for **`GL_1` and `GL_2`** automorphic representations.
`L(s, sym²f)` is a **`GL_3`** L-function (Gelbart–Jacquet lift). MV 2010
does **not directly cover `L(s, sym²f)`**. Subconvexity for `GL_3` L-functions
(in the relevant aspect for `L(1, sym²f)`) is partially open.

## 3.6 The "Cohen–Friedlander" citation requested in the prompt

Citation as supplied: "Cohen–Friedlander 2010 / 2017 — subconvexity for
Eisenstein series at the central point."

**Verdict (2026-05-09 web search):** No joint Cohen–Friedlander paper of
this title or scope located. The relevant unconditional results for
"subconvexity for the Eisenstein cross-term" in our regime are
Duke–Friedlander–Iwaniec 1990s/2000s subconvexity (GL(2)) and
Michel–Venkatesh 2010 (GL(1)+GL(2)). I treat route (d) as
"subconvexity unconditional, broadly construed" and note explicitly that
the requested verbatim Cohen–Friedlander citation **fails verification**.

---

# §4. Per-route assessment

## (a) Beilinson–Deligne motivic interpretation of the Eisenstein residue

**Route claim.** The Eisenstein-side residue at `s=1` admits a Beilinson
regulator interpretation as a determinant of a regulator map on motivic
cohomology of a motive `M = sym² h^1(X_0(N))`. If the Beilinson conjecture
were proven for this motive at `s=1`, the residue's value would be pinned
to `det(regulator) · (rational number)`, evaluable in principle.

**Regime of validity (verbatim from Beilinson 1984 page 6, J. Soviet Math.
30 p.2057).** Conjecture 3.7 governs the L-value at the *center* of the
critical strip `s = j/2` for motive of weight `j`. For `M = sym² h^1`,
weight `j = 2`, so center is `s = 1`. **This is exactly our case.**

**Proven cases (verbatim Beilinson 1984 page 1, J. Soviet Math. 30 p.2036):**
*"Sec. 7 we prove these conjectures for the case of Dirichlet series; Sec. 5
contains a result giving a partial proof of the conjecture for values at
two of L-functions of curves uniformized by modular functions; Sec. 6
contains an analogous computation for the product of curves of this type."*

So Beilinson PROVED:
- Dirichlet L-functions at integer points (§7).
- Modular curve L-functions `L(s, X_0(N))` at `s = 2` (§5, partial — integrality
  refined later).
- Product of modular curves (§6).

Beilinson DID NOT prove:
- `L(s, sym² f)` at `s = 1`. This is `j = 2, n = 1 = j/2` — the **center** of
  the critical strip per Conjecture 3.7. **Open as of 2026-05-09.**

**Mestre–Schappacher numerical evidence** (encyclopedia summary): *numerical
evidence only*, NOT a proof.

**Hidden-GRH check.** Beilinson Conjecture 3.7 itself does not assume RH —
but its STATEMENT for the leading coefficient of an L-function at `s = j/2`
INCLUDES the order of vanishing as the dimension of a motivic-cohomology
group, which is itself NOT KNOWN UNCONDITIONALLY to be finite for sym²f
without RH-type input. Specifically, the assertion `dim H^3_M(M_Z, Q(2))`
finite is an instance of the **Bass conjecture** for motivic cohomology,
which is open.

Even if the conjecture were proven, the relation
`L(1, sym²f) = c · det(regulator)` would give the *value of L at s=1*, not
the *residue* we need (the residue at `s=1` of the *triple product*
`Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A,A⟩(s)`). The triple product's residue
mixes contributions from poles of `Λ(2s−1)/Λ(2s)` (which depend on ζ-zero
location, NOT addressed by Beilinson), and from the polynomial structure
of `⟨A,A⟩(s)`. So Beilinson would only handle ONE of the THREE factors,
even hypothetically.

**Per-input confidence (rule §0):**
- Beilinson Conjecture 3.7 statement: 1.00 (PDF-verified).
- Conjecture 3.7 PROVEN for sym² at s=1: **0.00** — *falsified* (confirmed open).
- Mestre–Schappacher numerical evidence is a proof: 0.00 — *falsified*
  (encyclopedia explicitly: "numerical evidence").
- Even granted Beilinson, residue computation needs ζ-zero location:
  separately conditional on RH for ζ.

**Verdict (a): BLOCKED-AT-BEILINSON-CONJECTURE.** Confidence route closes
unconditionally: **0.00**.

This route does not hit the support-4 wall — it hits a **different** wall
(Beilinson Conjecture 3.7 for sym²f at s=1), which is also a multi-decade
open problem. It is not structurally cheaper than the support-4 wall.

---

## (b) Effective Hoffstein–Lockhart bounds on `L(1, sym²f)`

**Route claim.** HL Theorem 0.1 / 0.2 (verbatim §3.1 above) give effective
lower bound `L(1, sym²f) ≥ c_1 / log(kN+1)` (conditional on no Siegel zero)
or `> c(ε)(kN)^{-ε}` unconditional with at most one exception. If this
PINS the residue to a specific value, then route (b) closes.

**Regime of validity.** HL applies to:
- Lower bound on `L(1, F)` for `F = sym²f` (Gelbart–Jacquet adjoint square
  lift), holomorphic newform `f` of weight `k`, level `N`.
- Bound is a **lower bound only** — `L(1, F) ≫ 1/log(kN)` (HL Thm 0.1).
  No matching upper bound except `L(1, F) ≪ (kN)^ε` (HL eq 0.10, citing
  Iwaniec 1990 Thm 2).

**Does HL evaluate the residue we need?**

The residue is
`Res_{s=1}[Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A,A⟩(s)]`.

`L(s, sym²f)` is regular at `s=1` (Gelbart–Jacquet); its value `L(1, sym²f)`
is finite and nonzero. So the residue is taken from the *other* factors:
`Λ(2s−1)/Λ(2s)` has a simple pole at `s=1` (since `Λ(1)` is well-defined
and nonzero, but `Λ(2s−1)` has a pole at `s=1` from `Λ(s)` having a pole
at `s=1`); `⟨A,A⟩(s)` has a pole of order `(deg A)·2` at `s=1`. So the
residue is

`Res_{s=1} = (residue prefactor from Λ and ⟨A,A⟩) · L(1, sym²f) + (lower-order).`

where the prefactor is computable EXPLICITLY (it's a rational expression
in the polynomial coefficients of the M-N mollifier `A` plus `Res_{s=1} ζ
= 1` plus standard gamma factors at `s=1`). This is the on-RHf evaluation.

**Off-RHf, the residue value is shifted by contributions from off-line
zeros of `ζ` and `L(s, sym²f)`** — see §1 above and `Synthesis ... §6.5
lines 663–676`.

**HL bounds `L(1, sym²f)` from below by `1/log(kN)` and from above by
`(kN)^ε` — this gives a CAGE of width `(kN)^ε · log(kN)` around the
unknown true value of `L(1, sym²f)`.** This cage is *consistent* with the
M-N cage but does NOT pin the value.

Critically: HL bounds **do NOT control `Λ(2s−1)/Λ(2s)`'s additional poles**
from off-line ζ-zeros. Even if `L(1, sym²f)` is known to a specific value
(which HL does not give), the off-line `ζ`-zero contribution is governed
by RH for ζ, not by HL.

**Hidden-GRH check.** HL Theorem 0.1 (effective constant): conditional on
"no real zero of `L(s, F)` in `1 − c/log(λN+1) < s < 1`" — this is a
**Siegel zero hypothesis**, weaker than RH for sym² but not unconditional.
HL Theorem 0.2 (unconditional): "for all F with at most one exception,
ineffective constant" — Tatuzawa-style; the constant is INEFFECTIVE, so
**cannot pin the residue to a specific number**.

For our application we need an EXACT VALUE, not a lower bound. HL
provides neither (i) an exact evaluation of `L(1, sym²f)`, nor (ii) any
control on the off-line ζ-zero contribution to `Λ(2s−1)/Λ(2s)`.

**Per-input confidence:**
- HL Theorem 0.1 (PDF-verified): 1.00.
- HL Theorem 0.1 gives EXACT VALUE not just lower bound: **0.00** (only lower
  bound, verbatim).
- HL Theorem 0.1 unconditional (no Siegel-zero hypothesis): **0.00**
  (Theorem 0.1 is conditional on no Siegel zero; Theorem 0.2 is the
  unconditional version, but with INEFFECTIVE constant and "at most one
  exception" caveat — neither pins the residue).
- HL bounds `Λ(2s−1)/Λ(2s)` off-line ζ-zero contribution: **0.00** (HL
  is for sym² only, not ζ).

**Verdict (b): BLOCKED-AT-HIDDEN-GRH-FOR-ZETA + INEFFECTIVE-CONSTANT.**
Confidence: **0.00** for "closes residue unconditionally to specific value";
**0.85** for "gives a cage interval consistent with M-N cage, no improvement
in width" (this is exactly what `Synthesis ... §6.5` already states; HL is
the route by which the lower-cage edge is pinned).

This route hits the **same wall** as the existing support-4 route, just
via a different L-function: it requires controlling ζ-zeros (RH for ζ) AND
controlling sym²f-zeros (Siegel-zero hypothesis on sym²f). RH for ζ is
the strongest form of the obstruction; the multi-decade open Generalized
Riemann Hypothesis is a strict super-set.

---

## (c) Goldfeld–Stade GL(3) pairing

**Route claim.** Goldfeld–Stade machinery (Friedberg–Goldfeld 1993; Stade
2002; Bump 1989; Goldfeld 2006 ch. 6–7) gives explicit Mellin–Barnes
integrals for GL(3) Whittaker pairings with closed-form evaluation in
gamma factors. If the C1 residue can be expressed as a GL(3) Whittaker
pairing in a regime where Goldfeld–Stade applies, it might be evaluable.

**Regime of validity (verbatim §3.4 above, Friedberg–Goldfeld 1993
abstract).** Mellin transform of GL(n,R) Whittaker function has
*meromorphic continuation* and satisfies *explicit difference equations*.
Closed-form evaluation in gamma ratios obtains in low rank (n ≤ 4) and
specific parameter regimes (Stade 1990, 2001, 2002; Bump 1989 ch. 5).

**Does our residue reduce to a Goldfeld–Stade pairing?**

The residue `Res_{s=1}[Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A,A⟩(s)]` lives at
the **edge of the critical strip** for `L(s, sym²f)`, which is a `GL(3)`
L-function. The Goldfeld–Stade Mellin–Barnes form for `L(1, sym²f)` is
known unconditionally (this is the Rankin–Selberg integral on the
GL(3) × GL(2) side; Bump 1989 ch. 5 and Goldfeld 2006 ch. 6).

But this only gives `L(1, sym²f) = (gamma ratios) · ∫ (Eisenstein on GL(2))
· (cusp form on GL(3))` — an *integral representation*, NOT a closed-form
**evaluation** of `L(1, sym²f)` to a specific number. The integral itself
involves the cusp form `f`'s data (Hecke eigenvalues `λ_f(p)`), which
varies with `f`. Evaluating it requires either (i) summing the Hecke
data (which gives back the L-series we started from), or (ii) pinning
the spectral parameters.

**The closed-form Goldfeld–Stade evaluation handles only the
*archimedean local factor* (gamma ratios in `s`)**, not the *Hecke data*
which is intrinsically arithmetic and varies by form. So Goldfeld–Stade
gives `L(1, sym²f) = Γ_∞(1) · L_p(1)` (unconditional decomposition) but
the value `L_p(1)` is the *finite* part, which depends on `λ_f(p)` for
each prime — that's the very arithmetic content that we're trying to
pin down for the residue evaluation.

Furthermore: the residue we need also has the `Λ(2s−1)/Λ(2s)` factor,
which is a `GL(1)` (Riemann zeta) factor, and its off-line zero
contribution is **not addressed by Goldfeld–Stade** (which is a `GL(n)`
Whittaker machine, not a `GL(1)` zero-location result).

**Hidden-GRH check.** Goldfeld–Stade machinery is unconditional structurally
(meromorphic continuation, difference equations), but unconditional
*evaluation* of the resulting integral as a specific number requires:
(i) RH for ζ (to handle `Λ(2s−1)/Λ(2s)`), (ii) absence of off-line
sym²f-zeros (a GRH for sym² statement), or (iii) some Plancherel formula
that averages the Hecke data over `f`.

**Per-input confidence:**
- Friedberg–Goldfeld 1993 main result (PDF-verified): 1.00.
- Goldfeld–Stade Mellin–Barnes evaluates archimedean local factor: 1.00.
- Goldfeld–Stade evaluates *finite-place L-data unconditionally*: **0.00**
  — *falsified*; finite places are intrinsically arithmetic.
- Goldfeld–Stade addresses `Λ(2s−1)/Λ(2s)` off-line ζ-zero contribution:
  **0.00** — *falsified*; not in scope.

**Verdict (c): BLOCKED-AT-FINITE-PLACES + HIDDEN-GRH-FOR-ZETA.**
Confidence: **0.00** for "closes residue unconditionally"; **0.10**
for "gives an explicit gamma-factor expression with the Hecke data
left implicit" (this is structural, not new vs. M-N's contour
identity).

This route hits a wall **not on the support-4 ladder** but at the
intrinsic arithmetic content of the L-function. It is structurally
distinct from support-4 GDC but no easier — it amounts to evaluating the
finite-place Euler product to a specific number, which is the same
problem.

---

## (d) Cohen–Friedlander subconvexity (broadly construed: subconvexity for the Eisenstein cross-term)

**Route claim.** Subconvex bounds for `L(1/2, f × E)` (cusp × Eisenstein)
or for sym² L-functions are unconditional for some symmetry types
(Michel–Venkatesh 2010; Duke–Friedlander–Iwaniec). If the C1 residue
reduces to such an L-value at the central point `s = 1/2`, the
subconvex bound makes the residue evaluation unconditional with explicit
power-saving error.

**Regime of validity (verbatim §3.5 above, MV2010 abstract).**
*"We solve the subconvexity problem for the L-functions of `GL_1` and
`GL_2` automorphic representations over a fixed number field, uniformly
in all aspects."*

So MV 2010 covers GL(1) (Dirichlet, Hecke characters) and GL(2)
(holomorphic and Maass cusp forms, Eisenstein) — but **NOT GL(3)**, where
sym²f sits.

**Does our residue reduce to a subconvex GL(2) bound?**

The residue is at `s = 1`, the *edge* of the critical strip for sym²f
(which is GL(3)). Subconvex bounds at the central point `s = 1/2`
don't directly help at the edge `s = 1`. Edge bounds for sym² are governed
by HL (route (b)), which we already showed is blocked.

The `⟨A,A⟩(s)` factor is a polynomial-in-(log T) factor, fully unconditional
(M-N mollifier).

The `Λ(2s−1)/Λ(2s)` factor at `s = 1` becomes a residue at a SHIFTED zeta —
specifically `Res_{s=1} Λ(2s−1) = Λ-residue at s=1 = ζ-residue at s=1 = 1`.
For this part subconvexity is unconditional (`ζ(1+ε)` is not even subconvex,
just bounded). But the **OFF-LINE zeros of ζ contributing to `Λ(2s−1)/Λ(2s)`**
are not bounded by subconvexity — they require RH for ζ.

**Cohen–Friedlander (the prompt-cited paper).** Verification: no joint
Cohen–Friedlander 2010/2017 subconvexity paper located in 2026-05-09 web
search. The prompt's citation **fails verification**. I cannot confirm
or refute its claimed scope.

**Hidden-GRH check.** MV 2010 subconvexity is unconditional within its
GL(1)+GL(2) scope. Extending to GL(3) (where sym²f lives) is a major
open problem; Munshi 2014, Blomer–Buttcane 2017 give partial GL(3)
subconvexity (specific aspects) but NOT enough to pin a specific residue
value at `s=1`.

**Per-input confidence:**
- MV 2010 subconvexity for GL(1)+GL(2) (web-abstract verified): 0.95.
- MV 2010 covers GL(3) sym²f: **0.00** — *falsified*; explicitly GL(1)+GL(2).
- Cohen–Friedlander 2010/2017 verbatim: **0.00** — citation **falsified**
  (no such paper located).
- Subconvexity at `s=1/2` controls residue at `s=1`: **0.00** — different
  point of strip.
- Subconvexity controls off-line ζ-zero contribution to `Λ(2s−1)/Λ(2s)`:
  **0.00** — different problem (ζ-zero location, not bound size).

**Verdict (d): BLOCKED-AT-WRONG-S-VALUE + HIDDEN-GRH-FOR-ZETA + CITATION-FALSIFIED.**
Confidence: **0.00**.

This route hits both the support-4-equivalent wall (RH for ζ) AND a
wrong-point-in-strip wall (subconvex at `s=1/2` ≠ residue at `s=1`).

---

## (e) Other routes

I list four candidate routes discovered during the literature search,
each evaluated structurally.

### (e.1) Multiple Dirichlet series moments (Diaconu–Goldfeld–Hoffstein 2003)

**Setup.** DGH 2003 (Compositio 139:297–360, web-search verified) prove
that "straightforward conjectures about the meromorphic continuation
and polar divisors of certain such [multiple Dirichlet] series imply,
as a consequence, precise asymptotics ... for moments of zeta functions
and quadratic L-series."

**Verdict.** The asymptotics for moments of L-functions are CONDITIONAL
on conjectures about meromorphic continuation of multiple Dirichlet
series. For our application (averaging the residue value over
`f ∈ S_k*(N)`), this gives conditional formulas, not unconditional
evaluation. Confidence: **0.05**.

### (e.2) Mazur–Stein period methods

**Setup.** Periods of automorphic forms (Mazur, Stein, Pollack-Stevens
overconvergent forms) connect L-values to integrals of differentials
on modular curves. For `L(1, sym²f)` this would be a specific period
integral.

**Verdict.** This is essentially Beilinson regulator interpretation in
disguise (route (a)) — periods are the analytic side of the regulator.
Same wall: requires Beilinson Conjecture 3.7 for `sym²f` at `s=1` to be
proven. Confidence: **0.05**.

### (e.3) Beuker hypergeometric identities

**Setup.** Hypergeometric identities (Beukers, Vasyunin) sometimes give
closed-form evaluations of L-values at specific integer points, e.g.
`L(2, χ) = 2 Im(Li_2(e^{2πi/N}))`-type.

**Verdict.** These identities apply to GL(1) Dirichlet L-values. For
`L(1, sym²f)` (GL(3)), no analogous closed-form is known. The standard
representation `L(1, sym²f) = (k-1)/(8π³) · ⟨f,f⟩^{-1}` (HL eq 0.5
combined with Petersson normalization) is the closest, and this is just
a restatement of Petersson norm — does not pin the *residue* to a
specific number without further input. Confidence: **0.02**.

### (e.4) Weighted Selberg–Beurling mollifier replacement of `⟨A,A⟩(s)`

**Setup.** Replace the M-N mollifier `A` with a Selberg–Beurling extremal
mollifier in the residue formula. SB mollifiers have explicit Mellin
transforms with controlled zero-locations (Conrey 1998, Vaaler 1985).

**Verdict.** This DOES sharpen `⟨A,A⟩(s)` analysis (per `B_prime_denom_Selberg_Beurling_assessment.md`
in this followup directory). But the *residue value* at `s=1` is
still governed by the OTHER two factors (`Λ(2s−1)/Λ(2s)` and `L(s, sym²f)`),
which a mollifier replacement does not address. The companion
`B_prime_denom...` assessment in this same followup explicitly verdicts
"BLOCKED-FOR-EXACT" via this route. Confidence: **0.02**.

**Verdict (e): No "other route" closes the gap.** Best per-route confidence:
0.05 (DGH conditional). Aggregate (e): **0.05**.

---

# §5. Hidden-GRH check, summary table

For each route, I record where unproved Riemann-Hypothesis-grade input
silently appears.

| Route | Unconditional theorem statement valid? | Hidden RH/GRH? | Other hidden conjecture? |
|---|---|---|---|
| (a) Beilinson–Deligne | Beilinson Conj. 3.7 OPEN for sym²f at s=1 | RH not directly; but Beilinson presumes Bass conjecture (motivic cohomology finiteness) | Beilinson Conj. 3.7, Bass Conj. |
| (b) HL effective | Thm 0.1 conditional on Siegel-zero hypothesis; Thm 0.2 unconditional but ineffective + 1 exception | RH for ζ (in `Λ(2s−1)/Λ(2s)` factor) — UNADDRESSED by HL | "No Siegel zero" for sym²f |
| (c) Goldfeld–Stade GL(3) | Mellin continuation + diff. eqns are unconditional structural | RH for ζ — UNADDRESSED; finite-place L-data is the actual unknown | none beyond standard |
| (d) Subconvexity (MV2010 / "Cohen-Friedlander") | MV 2010 unconditional for GL(1)+GL(2); citation Cohen-Friedlander **falsified** | RH for ζ — UNADDRESSED; wrong point (s=1/2 vs s=1) | GL(3) subconvexity at s=1 (open) |
| (e.1) DGH multi Dirichlet | unconditional structural | RH not directly | Multi-Dirichlet meromorphic-continuation conjecture (open) |
| (e.2) Mazur–Stein periods | structural | same as (a) | Beilinson Conj. 3.7 |
| (e.3) Beuker identities | proven for GL(1) only | none for GL(1); NOT proven for GL(3) | none |
| (e.4) SB mollifier | unconditional for `⟨A,A⟩(s)` factor only | RH for ζ — UNADDRESSED | none |

**The common hidden-GRH input across (b), (c), (d), (e.4):** RH for ζ,
needed to bound the off-line ζ-zero contribution to `Λ(2s−1)/Λ(2s)`.
**(a) and (e.2)** require Beilinson Conjecture 3.7 for sym²f — which is
itself an open multi-decade problem.

**No route is unconditional in the sense needed** to pin the residue to
the specific value `−3/(4π)`.

---

# §6. Final verdict

## 6.1 Per-route summary

| Route | Verdict | Confidence |
|---|---|---|
| (a) Beilinson–Deligne motivic | BLOCKED-AT-BEILINSON-CONJECTURE-3.7 + BASS-CONJECTURE | 0.00 |
| (b) HL effective `L(1, sym²f)` | BLOCKED-AT-HIDDEN-RH-FOR-ζ + INEFFECTIVE-CONSTANT | 0.00 |
| (c) Goldfeld–Stade GL(3) pairing | BLOCKED-AT-FINITE-PLACES + HIDDEN-RH-FOR-ζ | 0.00 |
| (d) Subconvexity / "Cohen-Friedlander" | BLOCKED-AT-WRONG-S + CITATION-FALSIFIED + HIDDEN-RH-FOR-ζ | 0.00 |
| (e.1) DGH multi Dirichlet | BLOCKED-AT-MULTI-DIR-CONJECTURE | 0.05 |
| (e.2) Mazur–Stein periods | BLOCKED-AT-BEILINSON-CONJECTURE-3.7 (reduces to (a)) | 0.05 |
| (e.3) Beukers identities | BLOCKED-AT-GL(1)-ONLY | 0.02 |
| (e.4) Selberg–Beurling mollifier | BLOCKED-AT-OTHER-FACTORS | 0.02 |

## 6.2 Aggregate verdict

**Aggregate** = max over routes (0.05) + epistemic-uncertainty (+0.05 for
"a route I missed") = **0.10** confidence "C1 single-residue route closes
Theorem B-exact unconditionally."

## 6.3 Walls hit

| Wall | Routes hit | Cross-reference |
|---|---|---|
| **RH for ζ** (controls `Λ(2s−1)/Λ(2s)` off-line zeros) | (b), (c), (d), (e.4) | `Synthesis ... §6.5 lines 668–671`; `Voronoi_Kuznetsov_GRH_bypass §4 (R3-sp1)` |
| **Beilinson Conjecture 3.7** for sym²f at s=1 | (a), (e.2) | Beilinson 1984 §3 (PDF p.6, J.SovMath p.2057) |
| **GL(3) subconvexity at s=1** (Munshi, Blomer-Buttcane partial) | (d) (extension) | open |
| **Multiple-Dirichlet-series meromorphic continuation conjecture** | (e.1) | DGH 2003 explicitly hypothetical |
| **Beilinson Bass / motivic cohomology finiteness** | (a) | open |

The C1 single-residue route hits **the same wall (RH for ζ)** as the
Voronoi+Kuznetsov spectral route does for its R3 obstruction (per
`Voronoi_Kuznetsov_GRH_bypass.md` §4: *"the spectral parameter lies on
the critical line, which is the spectral analogue of GRH"*). It does
NOT hit the support-4 GDC wall directly — but the wall it does hit
(RH for ζ) is **strictly stronger** than the support-4 wall (since RH
for ζ is the strongest case of the L-function analog at `n=∞`).

## 6.4 Final classification

**`BLOCKED-AT-WALL: RH-for-ζ + Beilinson-3.7-for-sym²f + GL(3)-subconvexity-at-s=1.`**

The C1 single-residue route is **not** structurally distinct from the
support-4 GDC wall in the sense of "closing the gap independently":
both routes ultimately require either RH-grade input on ζ (and/or sym²f)
or a Plancherel-Sato-Tate input that pins the parabolic residue value.
This matches `Synthesis ... §7.5` (lines 769–800) verbatim:

> *"The R3 obstruction is preserved across all three trace formulas
> because the three trace formulas are *the* three projectors of a
> single L² decomposition; any obstruction visible in one is visible
> (in different clothing) in all three."*

## 6.5 Comparison to prior verdicts

| Prior file | Wall identified | Same as C1 §6.5 wall? |
|---|---|---|
| `Voronoi_Kuznetsov_GRH_bypass.md` §4 | R3 in spectral form (Bessel asymptotic on σ=1/2) | **Yes** (both require RH for L-zeros to lie on σ=1/2) |
| `Theta_lift_GRH_bypass.md` §4 | Density-level transfer not a Howe-duality theorem | Different (rep-vs-density), but unconditional 4-level density still needed |
| `arxiv_2601_06292_alt_GL2_routes.md` §3.6 | DHP-C engine has no analog for averaged quartic-L | **Yes** (Rankin-Selberg averaging needs unconditional pin, same as our residue) |
| `THEOREM_B_HANDOFF.md` §3 | support-4 GDC at fixed level | Strictly weaker than our RH-for-ζ wall, BUT same family of obstructions |

The C1 route is **structurally distinct from the support-4 GDC wall** in
the sense of WHICH conditional input it needs (RH for ζ + Beilinson
3.7 vs. fixed-level 4-level density), but the conditional input is
**not strictly weaker** than support-4 GDC — both are on the same
"unproved RH-grade input" side of the boundary. Closing C1 single-residue
unconditionally would, ironically, require even stronger input (RH for ζ
is supposed harder than fixed-level support-4 in current technology).

## 6.6 Confidence on Theorem B-exact unconditional via C1 route

**Updated confidence**: ≤ 0.05 (was ≤ 0.05 in the brief; this assessment
**confirms** rather than improves it). The C1 mechanism path is BLOCKED
at the same wall as the Voronoi+Kuznetsov spectral route and the
DHP-C-cuspidal-extension route, just expressed more cleanly.

---

# §7. Specific obstruction + recommendations

## 7.1 If VIABLE-FOR-EXACT (none)

No route closes. NO Opus extra-high task spec, MIMO bulk task spec, or
Aristotle Lean target is warranted on the C1 single-residue route at
this time.

## 7.2 The specific obstruction

The C1 single-residue obstruction reduces to:

**(O.C1)** *Pin the residue value*
`R_{C1} := Res_{s=1}[Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A,A⟩(s)]`
*to the specific number `−3/(4π) · ⟨c_f⟩ · T · log⁴(NkT)` UNCONDITIONALLY,
without using RH for ζ, RH for sym²f, or Beilinson Conjecture 3.7.*

**Decomposition of (O.C1) into three sub-obstructions:**

(O.C1.a) Bound the off-line ζ-zero contribution to `Λ(2s−1)/Λ(2s)` at
`s = 1`. **Equivalent to RH for ζ in the regime needed.**

(O.C1.b) Pin `L(1, sym²f)` to a specific value (or family-averaged value)
unconditionally. HL gives lower bound `≫ 1/log(kN)` and upper bound
`≪ (kN)^ε`, so a cage of width `(kN)^ε · log(kN)`. **A specific value
is open.**

(O.C1.c) Verify that `⟨A,A⟩(s)` mollifier polynomial structure correctly
combines with (O.C1.a) and (O.C1.b) to give `−3/(4π)`. This is purely
algebraic (no RH needed); it's the M-N constant identification.

## 7.3 Recommendations (per the brief's "If BLOCKED, the specific obstruction")

1. **Stop pursuing C1 single-residue as a path to Theorem B-exact unconditional.**
   Confidence ≤ 0.05; same wall as 16 prior failed routes per
   `THEOREM_B_HANDOFF.md` §9; structural fact `Synthesis ... §7.5`.

2. **Publish §6.5 obstruction identification as auxiliary structural result.**
   Per `Synthesis ... §7.6` (lines 803–823), the §6.5 identification IS
   publishable — it sharpens the Conrey–Snaith Ratios obstruction into a
   single Eisenstein-side residue computation. This is the *correct
   value* of the C1 mechanism, NOT closing Theorem B-exact.

3. **Reframe the open question.** The single most important open question
   in `C1_SELF_RESIDUE_HANDOFF.md` §9 should be replaced by:
   > Can `R_{C1}` be evaluated to a specific value via a
   > *family-averaged Plancherel-Sato-Tate* result that pins
   > `⟨L(1, sym²f) · (off-line ζ-zero contributions)⟩_F` averaged over
   > `f ∈ S_k*(N)` unconditionally?
   This is what `Synthesis ... §7.7 (D2)` (lines 832–838) already
   identifies as the cleanest restatement of the Ratios obstruction. It
   is the same open problem; the C1 mechanism does not provide a new
   handle on it.

4. **Cross-check (e.4) Selberg–Beurling mollifier route at the
   `⟨A,A⟩(s)` factor.** This is a *cosmetic* improvement on the
   `⟨A,A⟩(s)` factor only; verified BLOCKED in the companion
   `B_prime_denom_Selberg_Beurling_assessment.md`. No further work needed.

5. **Do not commission Aristotle Lean formalization of the C1 single-residue
   evaluation.** Without an unconditional theorem, there is nothing to
   formalize. The Lean cage half-width formalization
   (`CageHalfWidth.lean`) already covers the publishable cage statement.

6. **Update `C1_SELF_RESIDUE_HANDOFF.md` §15.3 to record this assessment.**
   The reviewer ask "*The double-parabolic cross term in §6.5 — can it be
   evaluated unconditionally via: (a) Beilinson-Deligne / (b) HL / (c)
   Goldfeld-Stade GL(3) / (d) other?*" should be answered: "**No to all
   four; same wall as RH for ζ.** See R3 assessment 2026-05-09."

---

# §8. Caveats and remaining uncertainty

- **Trace-class status of `T_{K,T}`** (`Synthesis ... §3.2`, conf 0.40)
  is a separate gap that this assessment did not address. If trace-class
  fails, the residue isn't well-defined and the question is moot. This
  assessment proceeds AS IF trace-class is granted.

- **Cohen–Friedlander citation in the brief**: I could not verify a paper
  by Cohen and Friedlander on subconvexity at the central point matching
  the prompt's description. Web search returned Duke–Friedlander–Iwaniec
  and Michel–Venkatesh as the closest matches. If the prompt-cited
  Cohen–Friedlander paper exists with a different title/scope, this
  assessment of route (d) might need adjustment — but the conclusions
  (BLOCKED at hidden RH for ζ AND wrong-point-in-strip) survive any
  reasonable interpretation of the route.

- **"Other routes" (e.1)–(e.4)** are not exhaustive. I identified four
  candidate routes from a 4-hour literature search. I add `+0.05` epistemic
  uncertainty to the aggregate verdict for "a route I missed." Even with
  this slack, the aggregate confidence stays ≤ 0.10.

- **Hoffstein–Lockhart 1994 Theorem 0.1 is conditional on a
  Siegel-zero-style hypothesis**, while Theorem 0.2 is unconditional but
  with INEFFECTIVE constant. Both are insufficient to pin a SPECIFIC
  residue value. This is the cleanest version of the (b) verdict —
  HL provides a CAGE consistent with the M-N cage, NOT a specific
  evaluation.

- **Beilinson 1984 §5–§7** are the proven cases. None covers `L(1, sym²f)`,
  which sits at the *center* of the critical strip per Conjecture 3.7
  (since `j = 2, n = 1 = j/2`). I verified this against the verbatim
  Conjecture 3.7 statement on PDF p.6 (J. Soviet Math. 30 p.2057).

---

# §9. Bottom line

**Verdict:** `BLOCKED-AT-WALL-Y` where Y = **{RH for ζ, Beilinson Conjecture
3.7 for sym²f at s=1, GL(3) subconvexity at s=1}**, with primary wall
**RH for ζ** (in the `Λ(2s−1)/Λ(2s)` factor of the residue).

**Aggregate confidence on "C1 single-residue route closes Theorem B-exact
unconditionally":** **≤ 0.10**.

**Aggregate confidence on "the C1 §6.5 obstruction identification is
publishable as auxiliary structural content":** unchanged from
`Synthesis ... §7.4` line 754 = **0.50** (the obstruction identification
is genuinely cleaner than the diffuse Ratios Conjecture statement).

**Aggregate confidence on "Theorem B-exact unconditional via the C1 route
in the next 12 months":** **≤ 0.02** (same as `THEOREM_B_HANDOFF.md` §10
P3 line 213: "P(submission) <0.01, Timeline >10 years, Annals tier,
Multi-decade open problem").

**The C1 single-residue path saves no cycles versus the support-4 GDC
path; both hit RH-grade walls.** Time should be redirected to:

(i) Publish the cage statement (Theorem B') with the §6.5 obstruction
identification as auxiliary structural content (per
`Synthesis ... §7.6`).

(ii) Consider P2 Inventiones-tier paper (1–3 year timeline) per
`THEOREM_B_HANDOFF.md` §10 P2: q-averaged σ ≈ 3.5 Δ-machine via
BCL 2024 + Hoffstein–Lockhart. NOT C1 single-residue — that path
is closed for unconditional Theorem B-exact.

— End of assessment.
