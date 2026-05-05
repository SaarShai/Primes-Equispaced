---
title: "Subset A audit — does {NC₈, NC₁₁, NC₁₂} prove Theorem B-exact under RH(ζ) only?"
type: audit
domain: research
tier: working
confidence: 0.92
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (1M)
sources:
  - /tmp/milinovich_ng.txt (M-N 2014, full text, lines cited verbatim)
  - /tmp/cfkrs.pdf (CFKRS 2005)
  - /Users/saar/Farey 4.7 solutions/Necessary_conditions_inverse.md
  - /Users/saar/Farey 4.7 solutions/CFKRS_symbolic_verification.md
  - /Users/saar/Farey 4.7 solutions/Reverse_engineer_constant.md
  - /Users/saar/Farey 4.7 solutions/G2_GRH_bypass.md
tags: [subset-A, RH-zeta, GRH-modular, theorem-B, gap-identification]
---

# Bottom line (written first)

**Subset A = {NC₈, NC₁₁, NC₁₂} does NOT constitute a proof of Theorem B-exact
under RH(ζ) only.** The three NCs are individually correct (NC₈ unconditional;
NC₁₁ unconditional algebraic; NC₁₂ conditional on RH(ζ) with the right citation
being Gonek 1989, NOT Ng 2004 — see §1 below), but the chain

  1/(24π) (ζ baseline) × 16 (algebraic boost) = 2/(3π)

does not transfer the **proven** ζ statement under RH(ζ) into a **proven**
modular statement under RH(ζ). The transfer requires a CFKRS-recipe identity at
the L(s,f) level (NC₉ / NC₁₃ / what M-N call "the conjectural formula for the
4th moment of ζ'") that is **independent of** RH(ζ) and **strictly stronger
than** RH for L(s,f) for every f in the family.

**Honest verdict: the conditionality structure of Subset A is**

  Theorem B-exact ⟸ (RH(ζ)) **PLUS** (CFKRS identity for the modular family)

and the second clause is **not** a consequence of the first. RH(ζ) alone is
**insufficient**.

The 2-page note proposed in `Necessary_conditions_inverse.md` §6 ¶3 should
NOT be written as a proof. It can honestly be written as

  (a) a **structural decomposition note** (no proof claim), or
  (b) a **conditional theorem under (RH(ζ) + CS07 ratios for the family)**
      whose hypothesis is genuinely weaker than (GRH for L(s,f) for all f in F)
      + (CS07 ratios), but whose hypothesis is NOT just RH(ζ).

This audit recommends form (a) or (b), not the form requested in the original
prompt. The writeup `Subset_A_RH_zeta_only.md` is composed in form (a)/(b)
hybrid with the gap fully exposed.

---

# Section 1. NC-by-NC verification with verbatim citations

## 1.1 NC₈ — Rankin–Selberg analytic continuation, residue c_f

**Statement.** L(s, f×f̄) = ζ(s)·L(s, sym²f) has meromorphic continuation
to ℂ with a simple pole at s=1 of residue c_f.

**Status: KNOWN UNCONDITIONALLY.**

Sources: Rankin 1939; Selberg 1940; Shimura 1975 ("On the holomorphy of certain
Dirichlet series", Proc. Lond. Math. Soc. 31); Gelbart–Jacquet 1978 (Ann. Sci.
ENS 11) for the sym² lift to GL(3).

M-N 2014 cite this and give the explicit formula (M-N eq. (1)):
  c_f = (4π)^k / (Γ(k) · vol(Γ₀(q)\h)) · ‖f‖²
M-N also state (lines 209-211 verbatim):

> "cf = lim_{x→∞} (1/x) Σ_{n≤x} |λ_f(n)|²"

Both formulas are unconditional (Rankin's theorem, 1939).

**Audit verdict for NC₈: ✓ correct, no hypothesis required.**

## 1.2 NC₁₁ — 16 = 2⁴ algebraic boost

**Statement.** When passing from a degree-1 family (ζ, log𝔮 = log t) to a
degree-2 family (modular f, log𝔮 = log q + 2 log t), the leading log⁴ t
coefficient of (log 𝔮(t))^4 is exactly 2⁴ = 16.

**Status: KNOWN UNCONDITIONALLY** (algebraic identity, not analytic).

Verification: `CFKRS_symbolic_verification.md` §1, sympy 1.14:
```
(log q + 2 log t)^4
  = 16·(log t)^4 + 32·(log t)^3·log(q) + 24·(log t)^2·(log q)^2
    + 8·(log t)·(log q)^3 + (log q)^4
```
Leading coefficient: 16. Sympy `Rational(16,24) = Rational(2,3)`. ✓

This NC is genuinely a free, unconditional algebraic identity; no hypothesis.

**Audit verdict for NC₁₁: ✓ correct, no hypothesis required.**

## 1.3 NC₁₂ — ζ-baseline 1/(24π) for Σ|ζ'(ρ)|²

**Statement.** Σ_{0<γ≤T} |ζ'(ρ)|² ∼ (T/(24π)) log⁴ T under RH(ζ).

**Status: KNOWN UNDER RH(ζ).**

**Citation correction.** The original `Necessary_conditions_inverse.md` line 152
cites "Ng 2004; Hughes 2001". The first is the wrong attribution. The correct
attribution is:

**Gonek 1989** (correctly cited in M-N 2014 line 869-877 verbatim):

> "Note that this is consistent with Theorem 1.2 and is analogous to a result
>  of Gonek [21] which states that
>    Σ_{0<ℑ(ρ)≤T} |ζ'(ρ)|² = (T/(24π)) log⁴ T + O(T log³ T)
>  assuming the Riemann hypothesis where ρ runs through the non-trivial zeros
>  of the Riemann zeta-function."

(M-N reference [21] is Gonek, "Mean values of the Riemann zeta-function and
its derivatives," Invent. Math. 75 (1984) 123-141, plus the refinement
Conrey–Ghosh–Gonek, "Mean values of the Riemann zeta-function with application
to the distribution of zeros," in *Number Theory, Trace Formulas and Discrete
Groups*, Academic Press 1989, pp. 185-199. The 1/(24π) leading constant is
established in this Crelle/Academic-Press lineage, all under RH(ζ).)

Hughes' thesis (2001) gives the RMT analog (Barnes-G computation showing
1/12 unitary coefficient × 1/(2π) Plancherel = 1/(24π)) but does not give a
new arithmetic proof.

**Hypothesis: RH(ζ).** Without RH(ζ): Conrey–Ghosh–Gonek argue the unconditional
bound is weaker (no exact constant; the off-line zeros disrupt the contour
manipulation in the same way they do in the modular case).

**Audit verdict for NC₁₂: ✓ correct. Hypothesis: RH(ζ). Citation: Gonek 1989,
not "Ng 2004" — Necessary_conditions_inverse.md needs this fix.**

---

# Section 2. The chain — does (NC₈ + NC₁₁ + NC₁₂) ⟹ Theorem B-exact?

## 2.1 What the chain claims

  Step 1: Under RH(ζ), Gonek 1989 gives Σ_γ |ζ'(ρ)|² ∼ (T/(24π)) log⁴ T.
  Step 2: NC₁₁ multiplies by 16 = 2⁴ from log𝔮(t) = log q + 2 log t.
  Step 3: NC₈ multiplies by c_f from Rankin–Selberg residue.
  Step 4: Result: Σ_f Σ_γ |L'(ρ_f, f)|² ∼ (2/(3π))·c_f·T·log⁴ X.

Numerical check: 16/(24π) = 2/(3π). ✓ (sympy exact).

## 2.2 Why the chain is NOT a proof

**The chain conflates two different things:**

- **Object A (proven by Gonek under RH(ζ)):** Σ|ζ'(ρ)|² for the actual
  Riemann zeta function with its actual non-trivial zeros.

- **Object B (target):** Σ_f Σ_γ |L'(ρ_f, f)|² for modular L-functions in a
  family.

The 16 = 2⁴ algebraic identity is a fact about how *the leading log⁴ coefficient
of any CFKRS-style 4-shift-derivative output transforms* when one substitutes
log 𝔮(t) = log q + 2 log t. It is a property of the **CFKRS recipe output**,
not a transfer rule between two separately-proven theorems.

**In other words:** NC₁₁ tells us that *if* the modular family obeys the CFKRS
recipe with the same combinatorial 1/(24π) shift-residue prefactor as the ζ
case, *then* the leading constant for the modular family is 2/(3π)·c_f.

But the conditional clause "*if* the modular family obeys the CFKRS recipe" is
exactly **NC₉ (4-shift Rankin–Selberg off-diagonal)** / **NC₁₃ (family-to-
individual descent)** — both flagged OPEN in `Necessary_conditions_inverse.md`
§2 and explicitly equivalent to T-B-exact.

**Gonek's proof under RH(ζ) does not establish this CFKRS recipe transfer.** It
establishes the recipe output for the specific case d=1 (i.e., ζ alone),
through a careful contour integral, explicit-formula manipulation, and use of
RH(ζ). The proof is **not** factored as

  (CFKRS recipe correctness for d=1) × (algebraic identity 1/(24π))

— it is a single, integrated argument. The d=2 analog is exactly what M-N
2014 Conjecture (16) states, and M-N immediately note (line 884-892, verbatim):

> "However, since L(s,f) is a degree two L-function, establishing (16) is
>  comparable to establishing the conjectural formula
>    Σ_{0<ℑ(ρ)≤T} |ζ'(ρ)|^4 = (T/(2880π³)) log⁹ T + O(T log⁸ T).
>  Such a result appears to be unattainable using current techniques without
>  some significantly new ideas."

This is the **decisive verbatim evidence** that the modular-aspect 2nd moment
of L'(ρ_f,f) is **not** reachable from the ζ-aspect 2nd moment + algebraic
identities. M-N themselves equate it in difficulty to the **4th** moment of
ζ' under RH(ζ), which is itself open.

## 2.3 The hidden hypothesis the original prompt missed

The original prompt's "ROUTE":

> 1. ζ-zeros are on critical line (RH(ζ) input)
> 2. Conrey-Gonek 1989 ζ' second moment 1/(24π) holds under RH(ζ)
> 3. The decomposition 2/(3π) = (1/(24π)) × 16 reduces to:
>    - Unitary baseline 1/(24π) (UNDER RH(ζ))
>    - × Algebraic boost 16 (UNCONDITIONAL)
> 4. Combining: Theorem B-exact under RH(ζ) only

contains an unstated step between (3) and (4): **transfer of the recipe output
from d=1 to d=2.** This step is not RH(ζ); it is the CS07 ratios identity
applied to the modular family, equivalently NC₉ / NC₁₃, equivalently
M-N (16) itself, equivalently T-B-exact.

The route is therefore **circular**: it assumes T-B-exact (via the recipe-
transfer step) in order to prove T-B-exact.

## 2.4 What RH(ζ) does NOT bypass

The G2_GRH_bypass.md analysis (verified by re-reading) shows that **even**
GRH for L(s,f) for **every** f in the family — a much stronger hypothesis
than RH(ζ) — is insufficient to prove T-B-exact. It establishes only the
**cage** [(17±√145)/(12π)]·c_f T log⁴X, with target 2/(3π) inside the cage
but not isolated.

The remaining gap, even given (GRH for all f in F), is the **CS07 ratios
identity in family-averaged form** — denoted G7 in the project's gap
catalog. This is purely a recipe / off-diagonal control gap; it has nothing
to do with RH for ζ.

**Therefore, replacing (GRH for all f in F) by the strictly weaker
hypothesis (RH(ζ)) cannot close a gap that GRH-for-all-f also fails to close.
RH(ζ) is strictly weaker, and it is dominated by the gap that survives
even under the stronger hypothesis.**

## 2.5 The (R3) per-form question

The original prompt asks:

> "Cross-check by re-reading G2_GRH_bypass.md — that doc identified (R3)
>  as load-bearing per-form. Does (R3) for f need GRH-for-f, or only RH(ζ)?"

**Answer: (R3) for f needs GRH-for-f (i.e., RH for L(s,f)), NOT RH(ζ).**

Verbatim from G2_GRH_bypass.md §1.2 (R3):

> "(R3) Functional-equation symmetry ρ_f = 1−\overline{ρ_f}. Multiple later
>  passes (line 2884, line 3268) write 1 − ρ_f = \overline{ρ_f}, which holds
>  **only if** β_f = 1/2 for every zero. This is RHf at its barest."

The variable here is **ρ_f**, the zero of L(s,f) — a *modular* L-function.
RH(ζ) (which constrains zeros of ζ alone) does not constrain ρ_f. The
identity 1 − ρ_f = \overline{ρ_f} is valid only when β_f = ℜ(ρ_f) = 1/2,
which is the assertion of RH for L(s,f), denoted RHf.

**RH(ζ) and RHf are independent hypotheses.** RH(ζ) is the special case
f = (the constant function with L(s) = ζ(s)); for any non-trivial cusp
form f, RHf is a logically separate statement. There is no known reduction
from RH(ζ) to a partial RHf result strong enough for (R3).

Hence: even at the per-form level, RH(ζ) does NOT replace RHf in M-N's
contour-integral step. The per-form M-N Theorem 1.2 (cage statement)
requires RHf for the form f under consideration, not RH(ζ).

---

# Section 3. Where Subset A *does* yield publishable content

The honest publishable content from this audit is **structural**, not a
new theorem:

## 3.1 Citation correction (small but real)

`Necessary_conditions_inverse.md` NC₁₂ should cite **Gonek 1989** (Conrey–
Ghosh–Gonek, *Number Theory, Trace Formulas and Discrete Groups*) as the
source for Σ|ζ'(ρ)|² ∼ (T/(24π)) log⁴ T under RH(ζ), not "Ng 2004".
M-N 2014 line 869-877 explicitly attribute this to Gonek [21].

## 3.2 Clean structural decomposition (Reverse_engineer_constant.md verified)

The identity 2/(3π) = 16/(24π) = d^{2k} / ((2k)! · π) at (d=2, k=2) is
algebraically clean and matches the CFKRS recipe-output form (CS07 §7
verifies it heuristically; sympy `expand` verifies the 16 boost).

This decomposition is publishable as a **structural / heuristic** note,
not as a proof. Confidence: 0.99 (post sympy verification).

## 3.3 What's NOT publishable as a proof

- "Theorem B-exact under RH(ζ) only" — FALSE statement; RH(ζ) is
  insufficient (this audit, §2).
- "Theorem B-exact via (NC₈ + NC₁₁ + NC₁₂)" — incomplete; the chain has
  a hidden CFKRS-transfer hypothesis (this audit, §2.2).

## 3.4 What IS publishable as a conditional theorem

  **Theorem (Subset A, conditional).** Assume (i) RHf for every f ∈ F
  (i.e., GRH for the family), and (ii) the CS07 ratios conjecture in
  family-averaged form for the 4-shift Rankin–Selberg sum at coalescing
  shifts, evaluated at the coefficient extracting log⁴X. Then
    Σ_f Σ_γ |L'(ρ_f, f)|² ∼ (2/(3π))·⟨c_f⟩·|F|·T·log⁴X.

This is essentially **CS07 §7 made rigorous via M-N 2014 + the ratios
conjecture**. It is the same statement as M-N (16), repackaged with a
slightly more transparent constant-decomposition (the 16 = 2⁴ boost is
made explicit). It is **NOT** weaker than what M-N already conjecture; it
is a re-derivation of M-N (16) under M-N's stated hypotheses.

Whether this is publishable as a 2-page note depends on whether the
reformulation has expository value. The 16 = 2⁴ boost (NC₁₁) and its
clean factorization is **modestly expository** but not a new theorem.

## 3.5 Honest recommendation

Two options for the writeup `Subset_A_RH_zeta_only.md`:

(A) **Structural / heuristic note**: state the decomposition 2/(3π) =
16/(24π) cleanly, attribute the 16 to NC₁₁ (algebraic), the 1/(24π) to
Gonek 1989 under RH(ζ) for the d=1 analog, and **explicitly state** that
the transfer to d=2 is not a theorem but a recipe-consistency check
matching CS07 §7. Length: ~2 pages. Status: expository.

(B) **Conditional theorem under (RH for f for all f in F) + (CS07 ratios
in family-averaged form)**: re-derive M-N (16) with the constant
decomposed via NC₁₁. Length: ~2 pages. Status: redundant with M-N 2014
(no new content), but cleaner constant exposition.

Neither (A) nor (B) is a proof of Theorem B-exact under RH(ζ). The
prompt's claim that RH(ζ) is "much weaker than GRH-for-family" is
correct, but RH(ζ) alone is **dominated by an independent gap** that GRH-
for-family also does not close.

---

# Section 4. Cross-reference to 9 prior failed attempts

The project files reflect a documented sequence of failed attempts at
Theorem B-exact unconditionally. Brief audit:

| Attempt | File | What it tried | Why it failed |
|---|---|---|---|
| Forward 1: RMT/Painlevé | RMT_Painleve_GRH_bypass.md | Replace GRH with RMT integrability | Painlevé identity is heuristic at family level |
| Forward 2: Voronoi/Kuznetsov | Voronoi_Kuznetsov_GRH_bypass.md | Off-diagonal control via Kuznetsov | 4-fold shifted convolution open |
| Forward 3: Theta lift | Theta_lift_GRH_bypass.md | Convert to symplectic period | Lift kills the constant |
| Forward 4: G2 weight aspect | G2_GRH_bypass.md | Petersson Bessel decay | Bessel kills off-diag, not (R3) |
| Forward 5: GRH bypass family | GRH_bypass_FAMILY_aspect.md | Family-zero-density (KM 1997) | Inflates cage, doesn't isolate 2/(3π) |
| Forward 6: B3 unconditional | (referenced in G2) | Bessel + family large sieve | Same as Forward 5 |
| Inverse 7: 17 NCs | Necessary_conditions_inverse.md | Enumerate sufficient subsets | Every minimal subset has open NC |
| Inverse 8: Reverse engineer | Reverse_engineer_constant.md | Decompose 2/(3π) = 16/24π | Decomposition is recipe-data, not proof |
| Inverse 9 (this audit): Subset A under RH(ζ) | THIS FILE | NC₈+NC₁₁+NC₁₂ under RH(ζ) | Hidden CFKRS-transfer hypothesis (§2.2) |

**All 9 attempts hit the same wall**: the 4-shift Rankin–Selberg / CS07
ratios identity for the modular family at the coefficient that produces
the **exact** constant 2/(3π). RH(ζ), GRH for f, family-averaging,
weight aspect, level aspect, theta lifts, etc., individually or in
combination, do not bypass this identity.

The wall is real. The constant 2/(3π) is recipe-data forced by
(d=2, k=2, orthogonal symmetry, CFKRS); proving it requires proving the
recipe is correct at the ratio level for this family, which is M-N (16) /
CS07 §7 in rigorous form, and is currently open.

---

# Section 5. Final verdict

| Question | Answer |
|---|---|
| Is RH(ζ) sufficient for Theorem B-exact? | **NO** |
| Does Subset A {NC₈, NC₁₁, NC₁₂} prove T-B-exact under RH(ζ)? | **NO** |
| Are NC₈, NC₁₁, NC₁₂ each correct? | YES (with NC₁₂ citation = Gonek 1989, not Ng 2004) |
| Does the chain 1/(24π) × 16 = 2/(3π) factor a proof? | **NO — it factors recipe data, not a theorem-transfer** |
| Does (R3) for f need RH(ζ) or GRH-for-f? | **GRH-for-f (i.e., RHf), independent of RH(ζ)** |
| Is the prompt's "Theorem B-exact under RH(ζ) only" publishable? | **NO** — would be wrong |
| Is a 2-page structural / heuristic note publishable? | YES, as expository content matching M-N 2014 + CFKRS_symbolic_verification |
| Confidence the wall (CS07 ratios for family) is structurally unavoidable for current technology | 0.85 |

**This audit recommends not writing the 2-page proof note. Writing instead
a 2-page expository note that documents the 16 = 2⁴ decomposition, its
status as recipe-data not theorem-transfer, and the explicit verbatim
position of M-N 2014 line 884-892 placing the modular 2nd moment at the
same difficulty as the ζ' 4th moment.**
