---
title: "G3 audit — Milinovich-Ng framing: theorem vs conjecture"
type: audit
domain: research
created: 2026-05-03
verified: 2026-05-03
sources:
  - "/tmp/milinovich_ng.txt (M-N 2014 arXiv:1306.0854 = PLMS 109, 1465-1506)"
gap: G3
status: corrections-recommended
tags: [farey, theorem-B, milinovich-ng, framing, audit]
---

# G3 audit — M-N framing: theorem vs conjecture

## 0. Ground truth (from /tmp/milinovich_ng.txt, M-N 2014)

What M-N 2014 actually proves vs. conjectures:

| M-N 2014 object | Status in M-N | What it says |
|---|---|---|
| **Theorem 1.1** | THEOREM (GRH-conditional) | N_f^s(T) ≫_ε T^{1−ε}: many simple zeros |
| **Theorem 1.2** | THEOREM (GRH-conditional) | Cage `[(17±√145)/(12π)] · c_f · T · log⁴ X` for Σ |L'(ρ_f,f)|² (lower + upper bound) |
| **Theorem 1.3, 1.4** | THEOREMS (GRH-conditional) | Higher-moment bounds for L'(ρ_f, f) |
| **Equation (16)** | **CONJECTURE** | Σ |L'(ρ_f,f)|² ~ (2/(3π)) c_f T log⁴ X |

M-N's verbatim wording around eq. (16) (lines 884–896):
> "establishing (16) is comparable to establishing the conjectural formula [for ζ⁴] … we expect that some substantially new ideas are necessary in order to establish the above conjecture for the second moment of L′(ρ_f, f)."

So: **eq. (16), 2/(3π) constant ⇒ M-N conjecture, NOT M-N theorem.**
The cage `[(17±√145)/(12π)]` ⇒ M-N Theorem 1.2 (GRH-conditional).

Common pre-history of the 2/(3π)-style at-zeros constants (for ζ, not for L(s,f)):
- Gonek 1984 / Conrey-Ghosh 1989 / Ng 2008 → GRH-conditional ζ analogues.
- Conrey-Snaith 2007 → ratios-conjecture-conditional general framework.
M-N's specific cusp-form eq. (16) for second moment of L'(ρ_f,f) is their conjecture.

---

## 1. Audit table — files where language drifts

Sweep of `/Users/saar/Farey 4.7 solutions/*.md` and the wiki page.
Only lines whose attribution or hedging needs correction are listed.
Lines that are already correct (or clearly hedge with "target" / "conjectural" / "M-N target") are NOT listed.

| File | Line | Current language | Issue | Corrected language |
|---|---|---|---|---|
| `B3_polar_mellin_factor_4_v2.md` | 17 | `"Milinovich-Ng 2014 arXiv:1306.0854 §§3-4 (M-N target 2/(3π))"` | "target" is OK but ambiguous in context where Theorem 1.2 cage is also from §§3-4 | `"Milinovich-Ng 2014 arXiv:1306.0854, eq. (16) — conjectural value 2/(3π) (M-N theorems are 1.2 cage, GRH-conditional)"` |
| `B3_polar_mellin_factor_4_v2.md` | 41 | `"Total = (2/(3π))·⟨c_f⟩·T·log⁴   ✓ M-N 2014."` | Reads as "matches M-N theorem". Misleading. | `"Total = (2/(3π))·⟨c_f⟩·T·log⁴   ✓ matches M-N 2014 eq. (16) **conjectural** value (family-averaged version proved here unconditionally)."` |
| `B3_polar_mellin_factor_4_v2.md` | 152 | `"GL₂ at-zeros = (1+1)·smooth = 2·smooth   (M-N 2014: 2/(3π))"` | Same, "M-N 2014: 2/(3π)" treated as established fact | `"GL₂ at-zeros = (1+1)·smooth = 2·smooth   (matches M-N 2014 conjecture eq. (16): 2/(3π))"` |
| `B3_polar_mellin_factor_4_v2.md` | 169 | `"Match to M-N target. ✓"` | "target" is acceptable — borderline | `"Match to M-N 2014 conjecture eq. (16). ✓"` |
| `B3_unconditional_attempt.md` | 32 | `"...the unconditional M-N cage holds in family-averaged form ... → 2/(3π) as N → ∞"` | Conflates: cage IS M-N's (Thm 1.2, GRH-conditional, NOT unconditional for individuals f); 2/(3π) is M-N's CONJECTURE. | `"... family-averaged refinement of the GRH-conditional M-N Theorem 1.2 cage [(17±√145)/(12π)], showing the family-averaged center converges to the M-N **conjectural** lower-edge value 2/(3π) (eq. (16))"` |
| `B3_unconditional_attempt.md` | 63 | `"M-N 2014 §4 prove: under no hypothesis, for any f ∈ F, any T,"` | **WRONG.** M-N Theorem 1.2 is GRH-conditional, not unconditional. | `"M-N 2014 §4 prove, **under GRH for L(s,f) and L(s,sym²f)**, for any f ∈ F, any T,"` |
| `B3_unconditional_attempt.md` | 73 | `"M-N's cage is the discriminant of a quadratic *moment inequality*"` | OK structurally but cage is GRH-conditional — should flag once at top | (no inline change needed; add header note: "All M-N statements below are GRH-conditional unless flagged.") |
| `B3_unconditional_attempt.md` | 83 | `"M-N compute S₄ and S_M unconditionally; equality in C-S would give u at the cage edge"` | **WRONG.** S₂, S₄, S_M in M-N are computed assuming GRH (it is needed to localize at zeros). | `"M-N compute S₄ and S_M **conditionally on GRH**; equality in C-S would give u at the cage edge"` |
| `B3_unconditional_attempt.md` | 221 | `"...matches the M-N conjectural value. The matching is unconditional once..."` | OK — already says "conjectural" | (no change) |
| `B3_unconditional_attempt.md` | 258 | `"the leading-coefficient computation in M-N §4 gives **2/(3π)** from a specific combinatorial integral"` | Reads as if M-N proved 2/(3π). They CONJECTURED it. | `"the leading-coefficient prediction in M-N §4 (eq. (16), conjectural) is **2/(3π)** from a specific combinatorial integral"` |
| `B3_unconditional_attempt.md` | 260 | `"I'll trust the M-N constant 2/(3π)"` | Sloppy — it's their conjecture, not constant | `"I'll trust the M-N **conjectural** constant 2/(3π) (eq. (16))"` |
| `B3_unconditional_attempt.md` | 562 | `"first **unconditional** proof of the M-N second-moment-of-derivative-at-zeros asymptotic"` | Right idea but worth saying "of the M-N **conjecture** eq. (16) in family-averaged form" | `"first **unconditional** proof of the M-N **conjectural** second-moment-of-derivative-at-zeros asymptotic (eq. (16)) in family-averaged form"` |
| `B3_unconditional_attempt.md` | 624 | `"M-N cage center 17/(12π) shifts to lower-cage value 2/(3π)"` | M-N's cage is theirs; 2/(3π) is the M-N conjectural value. Could be cleaner. | `"M-N (Thm 1.2, GRH-conditional) cage center 17/(12π) shifts to the M-N (eq. (16), conjectural) lower-edge value 2/(3π)"` |
| `B3_section_3_7_resolution.md` | 28 | `"**Mellin / M-N** (the actual ⟨|L'(ρ)|²⟩_zeros) **= 2/(3π)** in same units"` | "actual" is misleading. It's the conjectured value. | `"**Mellin / M-N conjecture eq. (16)** (the conjectured ⟨|L'(ρ)|²⟩_zeros) **= 2/(3π)** in same units"` |
| `B3_section_3_7_resolution.md` | 91 | `"**B.1 The M-N constant for ζ.** M-N Theorem 1.2 (under RH + Montgomery pair correlation):"` | **WRONG attribution.** M-N Thm 1.2 is for L(s,f), NOT for ζ. The ζ analogue 2/(3π) is Gonek 1984 / Conrey-Ghosh 1989 / Ng 2008 (under RH). M-N do reference these but they are NOT "M-N Theorem 1.2". | `"**B.1 The 2/(3π) constant for ζ.** Conrey-Ghosh-Gonek style result (under RH; Gonek 1984, Conrey-Ghosh 1989, Ng 2008): Σ_{γ≤T} \|ζ'(½+iγ)\|² = (1/(12π)) T log⁴ T (1+o(1)). [M-N 2014 eq. (16) is the conjectural cusp-form analogue at constant 2/(3π).]"` |
| `B3_section_3_7_resolution.md` | 100 | `"Decomposition (M-N Eq. 4.7-4.12)"` | Need to confirm M-N actually have Eq. 4.7-4.12 doing this decomposition. M-N PDF text shows Lemma 4.1 mean-value, Propositions 1.1, 1.2, etc. The ζ decomposition cited here is Conrey-Ghosh / Ng-style, not M-N's. | `"Decomposition (Ng 2008-style; M-N 2014 §4 transports same decomposition to L(s,f))"` |
| `B3_section_3_7_resolution.md` | 106 | `"**B.2 Petersson family, weight aspect — orthogonal symmetry.** The corresponding M-N-type contour analysis ... gives ... 2/(3π)"` | OK — uses "M-N-type" hedging | (minor) `"... gives the M-N conjectural value 2/(3π) (eq. (16))"` |
| `B3_section_3_7_resolution.md` | 132 | `"\| Mellin / M-N (correlated) \| 2/(3π) ≈ 0.2122 \|"` | Table cell — labels as if M-N (correlated) is theorem | `"\| Mellin / M-N conjecture eq. (16) (correlated) \| 2/(3π) ≈ 0.2122 \|"` |
| `B3_section_3_7_resolution.md` | 226 | `"Milinovich, M.B., Ng, N. 2014. arXiv:1306.0854 §4. [2/(3π) for ζ; framework]"` | **WRONG.** 2/(3π) for ζ is NOT M-N. M-N 2014 §4 is for L(s,f), conjecturally. | `"Milinovich, M.B., Ng, N. 2014. arXiv:1306.0854 §4 + eq. (16) [conjectural 2/(3π) for L(s,f) second moment of L'(ρ_f,f)]"` plus add `"Ng, N. 2008. [unconditional/GRH constant for ζ analogue]"` |
| `B3_log_counting_FINAL.md` | 14 | `"Milinovich-Ng 2014 §3.4 (target 2/(3π))"` | borderline — "target" is fine | (minor) `"M-N 2014 eq. (16), conjectural target 2/(3π)"` |
| `B3_log_counting_FINAL.md` | 131 | `"Total = **(2/(3π))·⟨c_f⟩·T·log⁴** = M-N 2014 ✓"` | Reads as = M-N theorem. | `"Total = **(2/(3π))·⟨c_f⟩·T·log⁴** = M-N 2014 conjecture eq. (16) ✓ (matched in family-averaged form)"` |
| `B3_lemma_3_1_fixed.md` | 127 | `"to go from the bare Stieltjes constant 1/(6π) to the M-N target 2/(3π)"` | borderline — "target" OK | (minor) replace "M-N target" → "M-N conjectural target (eq. (16))" |
| `B3_lemma_3_1_fixed.md` | 144 | `"recover M-N constant 2/(3π)"` | sloppy: it is their conjecture, not constant | `"recover M-N **conjectural** constant 2/(3π) (eq. (16))"` |
| `B3_theorem_A_v2.md` | 31 | `"M-N cage + Kim-Sarnak 2-level density at η < 57/64 ... within 0.72σ of the conjectural lower-cage value 2/(3π)"` | OK — already says "conjectural lower-cage value" | (no change) |
| `B3_theorem_A_v2.md` | 75 | `"Per-f cage (M-N 2014 §4, unconditional):"` | **WRONG.** M-N Theorem 1.2 is GRH-conditional. | `"Per-f cage (M-N 2014 §4, Theorem 1.2, **conditional on GRH for L(s,f) and L(s,sym²f)**):"` |
| `B3_theorem_A_v2.md` | 81 | `"M-N §3 Lemma 3.1"` | OK — citation, not framing | (no change; verify lemma number against PDF) |
| `B3_theorem_A_v2.md` | 174 | `"Gap 1 (constant identification, conjectural). The conjectural value 2/(3π) ..."` | already correct | (no change) |
| `B3_petersson_deep_solve.md` | 61 | `"This converts the M-N result, in family-averaged form, from "ratios-conjecture +"` | **WRONG.** "M-N result" suggests M-N proved 2/(3π). It's their conjecture. | `"This converts the M-N **conjecture eq. (16)**, in family-averaged form, from "ratios-conjecture-conditional" to "unconditional"."` |
| `B3_petersson_deep_solve.md` | 69 | `"the constant 2/(3π) in M-N is the *predicted* lower-cage value"` | Already correct — "predicted" | (no change) |
| `B3_petersson_deep_solve.md` | 193 | `"already known (it IS the M-N cage). Doesn't prove the lower cage value 2/(3π)."` | OK | (minor) `"... (it IS the GRH-conditional M-N cage of Thm 1.2). Doesn't prove the M-N conjectural lower-cage value 2/(3π) (eq. (16))."` |
| `B3_petersson_deep_solve.md` | 310 | `"the *family-averaged* statement of M-N is at most one Kloosterman-bound"` | OK structure | (minor) `"the family-averaged version of the M-N conjecture (eq. (16))"` |
| `B3_petersson_deep_solve.md` | 374 | `"\| 5 Selberg majorant \| Upper bound only \| Already in M-N cage \|"` | OK | (no change) |
| `B3_C_star_DEFENSE.md` | 27, 172, 175, 182, 183, 188, 189 | several "M-N second-moment" / "M-N constant 2/(3π)" / "M-N target" | All present-tense calls "M-N second moment" / "M-N constant" — should consistently say "M-N **conjectural** second moment / constant (eq. (16))" | bulk-replace: `"M-N second-moment-of-derivative"` → `"M-N (eq. (16), conjectural) second-moment-of-derivative"`; `"M-N constant 2/(3π)"` → `"M-N conjectural constant 2/(3π) (eq. (16))"` |
| `B3_CS_7_32_FROM_SCRATCH.md` | 37 | `"Total = (2/(3π)) · ⟨c_f⟩_{F_k} · T · log⁴(NkT) · (1+o(1))   ✓ M-N 2014."` | implies M-N theorem | `"Total = (2/(3π)) · ⟨c_f⟩_{F_k} · T · log⁴(NkT) · (1+o(1))   ✓ matches M-N 2014 conjecture eq. (16)."` |
| `B3_CS_7_32_FROM_SCRATCH.md` | 230 | `"This matches (★) and the M-N target."` | borderline | (minor) `"... and the M-N conjectural target (eq. (16))."` |
| `B3_CS_7_32_FROM_SCRATCH.md` | 253 | `"= (2T/(3π))·⟨c_f⟩·log⁴ ✓ M-N 2014"` | as above | `"... ✓ matches M-N 2014 conjecture eq. (16)"` |
| `B3_CS_7_32_FROM_SCRATCH.md` | 259 | `"orthogonal: (1+1) = 2  (M-N 2014)"` | as above | `"orthogonal: (1+1) = 2  (matches M-N 2014 conjecture eq. (16))"` |
| `B3_CS_7_32_FROM_SCRATCH.md` | 315 | `"to M-N 2014 conjectural value."` | already correct | (no change) |
| `B3_CS_7_32_FROM_SCRATCH.md` | 323 | `"M-N 2014 (3.10) (target 2/(3π))"` | "(3.10)" — verify; M-N 2014 eq. (16) is the conjecture statement; eq. (3.10) should be checked vs PDF | `"M-N 2014 eq. (16) (conjectural target 2/(3π))"` and verify any §3 internal eq. number against PDF |
| `B3_CS_eq_7_32_rigorous.md` | 30 | `"the M-N target 2/(3π)"` | borderline | (minor) `"the M-N conjectural target 2/(3π) (eq. (16))"` |
| `B3_CS_eq_7_32_rigorous.md` | 254 | `"Heath-Brown 1979 + CS 2007 + M-N 2014 all"` | If listed as agreement-of-three-theorems, misleading. Heath-Brown 1979 is for ζ; CS 2007 is ratios-conjectural; M-N 2014 eq. (16) is conjectural. | `"Heath-Brown 1979 (ζ, GRH-conditional) + CS 2007 (ratios-conjectural prediction) + M-N 2014 eq. (16) (conjectural for L(s,f)) all agree on the constant"` |
| `B3_Lprime_2nd_moment_RIGOROUS.md` | 209 | `"(M-N 2014 §4 for ζ; transported to Petersson family via CS 2007 §7 ...)"` | **WRONG attribution again.** M-N 2014 §4 is NOT for ζ; it is for L(s,f). The ζ analogue 2/(3π) is Conrey-Ghosh-Gonek-Ng (under RH). | `"(Conrey-Ghosh 1989 / Ng 2008 §4 for ζ under RH; M-N 2014 conjecture eq. (16) for L(s,f); transported to Petersson family via CS 2007 §7 ...)"` |
| `B3_Lprime_2nd_moment_RIGOROUS.md` | 224 | `"This is M-N's 2/(3π)."` | "M-N's 2/(3π)" — correct attribution as conjecture, but missing label | `"This matches M-N 2014 conjecture eq. (16): 2/(3π)."` |
| `B3_Lprime_2nd_moment_RIGOROUS.md` | 244 | `"matches M-N exactly via orthogonal symmetry kernel"` | "matches M-N" — does it match the conjecture or theorem? | `"matches the M-N (eq. (16)) conjectural value exactly via orthogonal symmetry kernel"` |
| `B3_Lprime_2nd_moment_RIGOROUS.md` | 265 | `"matching M-N 2014 unconditionally in weight aspect"` | M-N 2014 is conjectural; we match the conjecture's predicted value. | `"matching the M-N 2014 conjectural value (eq. (16)) unconditionally in weight aspect"` |
| `B3_theorem_C_star_1L.md` | 32, 124, 130, 142, 152, 155, 179, 187 | various "M-N constant 2/(3π)" / "M-N second moment" / "M-N statistic" / "conjecture of M-N" | line 130 already says "the conjecture of M-N" — good. Other lines should match. | bulk-replace `"M-N constant 2/(3π)"` → `"M-N conjectural constant 2/(3π) (eq. (16))"` ; `"M-N statistic"` → `"M-N (eq. (16)) statistic"` ; `"M-N second moment"` → `"M-N (eq. (16)) conjectured second moment"` |
| `MASTER_KEY_petersson_ratios_uncond.md` | 239 | `"the full 4-shift / CFKRS at the M-N constant 2/(3π) requires (M2)"` | implies "M-N constant" is a known constant, when it is M-N's conjectured value | `"the full 4-shift / CFKRS at the M-N conjectural constant 2/(3π) (eq. (16)) requires (M2)"` |
| `wiki/Research/Farey-Theorem-B-Unconditional.md` | 3, 32 | title `"Theorem B: Petersson Weight-Aspect M-N Constant Unconditional"` | "M-N Constant" suggests there is a fixed M-N constant we are proving | `"Theorem B: Petersson Weight-Aspect M-N Conjecture (eq. (16)) Unconditional"` (or `"... Family-Averaged M-N Conjectural Constant Unconditional"`) |
| `wiki/Research/Farey-Theorem-B-Unconditional.md` | 50 | `"first unconditional theorem of the Farey/W2/C1 program for the Milinovich-Ng cage's exact constant 2/(3π). M-N 2014 proved their cage [(17±√145)/(12π)]·c_f·T·log⁴X unconditionally for individual f, but the conjectural lower-edge constant 2/(3π) required GRH."` | **WRONG.** M-N 2014 proved their cage **conditionally on GRH for individual f**, NOT unconditionally. The "lower-edge constant 2/(3π)" is M-N's CONJECTURE (eq. (16)), not "conditional on GRH" — it was an independent conjecture. | `"first unconditional theorem of the Farey/W2/C1 program for the Milinovich-Ng conjectural lower-edge constant 2/(3π) (M-N 2014 eq. (16)). M-N 2014 proved their cage [(17±√145)/(12π)]·c_f·T·log⁴X (Theorem 1.2) **conditionally on GRH for L(s,f) and L(s,sym²f)** for individual f. The lower-edge constant 2/(3π) was M-N's separate conjecture (eq. (16)); they wrote that 'substantially new ideas' would be needed even given GRH. We close eq. (16) unconditionally in the family-averaged weight-aspect formulation."` |
| `wiki/Research/Farey-Theorem-B-Unconditional.md` | 132 | `"\| In M-N cage [0.132, 0.770] \| 15/16 ✓ \|"` | OK (cage is M-N's, GRH-conditional, but "in M-N cage" is fine as numerical reference) | (no change) |

Note: PAPER_DRAFT_TheoremB_WeightAspect.md is already correct — uses "Conjecture (Milinovich–Ng 2014)" cleanly throughout. Good.

---

## 2. Standardized language (canon — use everywhere)

**For the paper, abstract, and any in-program file going forward, use exactly these phrases.**

### 2.1 Naming canon

| Object | Canonical name | Status |
|---|---|---|
| `[(17±√145)/(12π)]·c_f·T·log⁴X` | **M-N cage** = M-N 2014 Theorem 1.2 | THEOREM (M-N), conditional on GRH for L(s,f) and L(s,sym²f) |
| `Σ \|L'(ρ_f,f)\|² ~ (2/(3π)) c_f T log⁴ X` for individual f | **M-N conjecture** = M-N 2014 eq. (16) | CONJECTURE (M-N); M-N: "substantially new ideas required" |
| Family-averaged version (this paper) | **Family-averaged M-N conjecture (weight-aspect)** = our Theorem B | THEOREM (Shai 2026), unconditional |
| `1/(12π)` for ζ | **ζ second-moment-of-zeros constant** | THEOREM (Gonek 1984 / Conrey-Ghosh 1989 / Ng 2008), conditional on RH for ζ |

### 2.2 Phrase templates

**When stating the goal:**
> "We prove unconditionally, in the weight-aspect family-averaged formulation, the constant 2/(3π) predicted by the Milinovich–Ng (2014) conjecture (eq. (16) of arXiv:1306.0854). The single-form (per-f) version remains open; M-N stated 'substantially new ideas' would be required."

**When citing the cage:**
> "the GRH-conditional M-N cage [(17±√145)/(12π)] (M-N 2014, Theorem 1.2)"

**When citing the constant:**
> "the M-N (eq. (16)) conjectural lower-edge constant 2/(3π)"
> NOT "the M-N constant 2/(3π)" (suggests theorem)
> NOT "the M-N target 2/(3π)" (vague — at minimum say "M-N conjectural target")

**When matching to the constant:**
> "matches the M-N 2014 conjecture eq. (16) prediction 2/(3π)"
> NOT "matches M-N" (ambiguous)
> NOT "✓ M-N 2014" (suggests theorem)

**When citing the ζ analogue:**
> "the GRH-conditional ζ analogue 1/(12π) (Conrey–Ghosh 1989; Ng 2008)"
> NOT "M-N's ζ result" — M-N 2014 is for L(s,f), not ζ.

### 2.3 Three-line elevator pitch (for the paper intro)

> Milinovich–Ng (2014) proved a GRH-conditional cage `[(17±√145)/(12π)]·c_f·T·log⁴X` for `Σ_{γ_f≤T} |L'(ρ_f,f)|²` (their Theorem 1.2), and conjectured (eq. (16)) the precise asymptotic with constant `2/(3π)`. They wrote that "substantially new ideas are necessary" to establish the conjecture. We prove the family-averaged weight-aspect version of their conjecture **unconditionally**: for the harmonic-Petersson average over `H_k(N,χ)` with `k → ∞`, the asymptotic holds with constant exactly `2/(3π)`.

---

## 3. Severity ranking

CRITICAL (factually wrong, fix before any external sharing):
- `B3_unconditional_attempt.md` line 63: "M-N 2014 §4 prove: under no hypothesis" — **GRH is required**
- `B3_unconditional_attempt.md` line 83: "M-N compute S₄ and S_M unconditionally" — **GRH-conditional**
- `B3_theorem_A_v2.md` line 75: "Per-f cage (M-N 2014 §4, unconditional)" — **GRH-conditional**
- `wiki/Research/Farey-Theorem-B-Unconditional.md` line 50: "M-N 2014 proved their cage ... unconditionally for individual f" — **GRH-conditional**
- `B3_section_3_7_resolution.md` line 91: "M-N Theorem 1.2 (under RH ...)" attributed to ζ — **wrong: M-N Thm 1.2 is for L(s,f). ζ analogue is Conrey-Ghosh / Ng.**
- `B3_section_3_7_resolution.md` line 226: "M-N 2014 §4 [2/(3π) for ζ; framework]" — **wrong: §4 is for L(s,f), not ζ.**
- `B3_Lprime_2nd_moment_RIGOROUS.md` line 209: "M-N 2014 §4 for ζ" — **same mis-attribution.**

HIGH (drift in framing, fix before paper-final):
- `B3_polar_mellin_factor_4_v2.md` lines 41, 152: "✓ M-N 2014" / "M-N 2014: 2/(3π)" reads as theorem
- `B3_unconditional_attempt.md` line 258, 260, 562, 624
- `B3_petersson_deep_solve.md` line 61
- `B3_log_counting_FINAL.md` line 131
- `MASTER_KEY_petersson_ratios_uncond.md` line 239
- `wiki/Research/Farey-Theorem-B-Unconditional.md` line 3, 32 (title)

MEDIUM (borderline; tighten if convenient):
- All "M-N target" instances → "M-N conjectural target (eq. (16))"

LOW (fine, citation discipline only):
- Correct lines that already say "conjectural" or "predicted"

---

## 4. Verification trail

- /tmp/milinovich_ng.txt lines 863–896: M-N 2014 eq. (16) explicitly called "the above conjecture" with "we expect that some substantially new ideas are necessary".
- /tmp/milinovich_ng.txt lines 43–66 (Theorems 1.1–1.4): all four explicitly say "assume the generalized Riemann hypothesis" — i.e. M-N 2014 has NO unconditional theorems for `Σ |L'(ρ_f,f)|²`.
- M-N's Theorem 1.2 (line 155 of the txt) confirmed for L(s,f) (not ζ).

## 5. Recommended next action

1. Apply CRITICAL fixes (7 lines) in a single sweep.
2. Apply HIGH fixes via search-and-replace using the canonical phrases in §2.2.
3. Re-run grep for `M-N` / `Milinovich` after fixes; verify no occurrence asserts theorem-status for 2/(3π).
4. Add a one-paragraph "Conventions" block at the top of `B3_unconditional_attempt.md` and `wiki/Research/Farey-Theorem-B-Unconditional.md` stating the M-N theorem-vs-conjecture canon (§2.1).
