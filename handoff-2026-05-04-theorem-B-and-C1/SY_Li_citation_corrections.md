---
title: "S-Y → Li 2024 Citation Audit Report (2026-05-03 Sonnet 4.6 pass, rate-limit resume)"
type: audit
domain: research
tier: episodic
confidence: 0.97
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Sonnet 4.6 (citation audit, 4h budget, resumed after rate-limit at 8:20pm)
tags: [citation-audit, soundararajan-young, li-2024, grh-conditional, quadratic-twists]
---

# Ground truth

**S-Y 2010 (JEMS 12:1097-1116):**
- Subject: second moment of L(½, f⊗χ_d) over fundamental discriminants d.
- Family: symplectic quadratic-twist family (NOT Petersson weight-aspect).
- Asymptotic: GRH-CONDITIONAL. Only the lower bound is unconditional.
- Does NOT contain: 8th-moment bounds, on-line results, Petersson family results.

**Li 2024 (Inventiones 237:697-733):**
- Proves the 2nd-moment-of-quadratic-twists asymptotic UNCONDITIONALLY.
- ONLY at central point s = ½ (not on the line, not a density result).
- NOT applicable to: Petersson weight-aspect family, L' at zeros, 2-level density.

---

# File-by-file audit (2026-05-03 Sonnet 4.6, rate-limit resume)

Files audited: 8. Files requiring edits: 1.

---

## 1. AUTONOMOUS_PLAN.md

S-Y appears only in harvester log lines (§comparison with prior art). No mathematical claims made. Classification: **B (adjacent)**. No edit needed.

---

## 2. B3_unconditional_attempt.md

Line 346 (§5.1 Vector δ): Already corrected — reads "(GRH-conditional asymptotic; unconditional lower bound only)" with Li 2024 cited. Also notes neither result transfers (different family, central-point ≠ L' at zeros). Classification: **C (already corrected)**. No edit needed.

---

## 3. G6_cross_term_C_f.md

Frontmatter sources line 15: Already annotated "GRH-conditional asymptotic; unconditional lower bound only; unconditional asymptotic proved in Li 2024, Inventiones 237:697-733". Body uses S-Y only as lit benchmark in §4.3, not load-bearing. Classification: **C (already corrected)**. No edit needed.

---

## 4. GRH_bypass_FAMILY_aspect.md

§1 (F3) and §2.4 Route 4: Both already have full correction NOTE. Section 1 item (F3) lines 57-63 reads "S-Y asymptotic is GRH-conditional; only the matching lower bound is unconditional. The unconditional asymptotic at s = 1/2 (central point only, NOT on the line) was proved in Li 2024 (Inventiones 237:697–733)." Section 2.4 already corrected. Classification: **C (already corrected)**. No edit needed.

---

## 5. RankinSelberg_trace_attack.md

Lines 360-361: S-Y in bibliography search list only (Class B, no claim). §5.2 (E1): Already has full correction with Li 2024. Classification: **C (already corrected)**. No edit needed.

---

## 6. TheoremB_level_aspect_honest.md

Frontmatter sources line 14: Already annotated "NOT eighth moment; asymptotic GRH-conditional; only lower bound unconditional; unconditional asymptotic at central point proved in Li 2024, Inventiones 237:697-733". §1.6 lines 111-117: Full explicit correction present, including "Conf the MK2 citation of S-Y for the 8th moment was fabricated: 0.85." Classification: **C (already corrected)**. No edit needed.

---

## 7. MK2_lift_to_0.85.md — ONLY FILE REQUIRING EDITS

Two stale passages found and corrected in this session:

**Edit 1 — frontmatter sources (Class B):**
- Old: `"Soundararajan-Young 2010, JEMS 12 (family-averaged moments of GL_2 L-functions)"`
- New: full description — "second moment of quadratic twists of modular L-functions; asymptotic GRH-conditional; unconditional lower bound only; NOT a family-averaged moment result for the Petersson weight-aspect family; unconditional asymptotic at central point proved in Li 2024, Inventiones 237:697-733"

**Edit 2 — SL2 block in Section 5 (Class A, load-bearing):**
- Old: "The GL_2 analog at the central point, family-averaged, follows from S-Y 2010 §6 (cited above) with exponent 16... CONFIDENCE in SL2: 0.85."
- New: S-Y input removed; explanation that S-Y covers wrong family (symplectic quadratic-twist, not orthogonal Petersson); Li 2024 scope noted (central point only, not applicable); direct AFE/Heath-Brown argument substituted (exponent 24 from §3.3); SL2 confidence revised to **0.75** (consistent with §3.4 aggregation table which already stated "0.75 revised down after removing fabricated S-Y attribution"); projected MK2 lift ceiling drops from 0.90 to **0.80**.

Classification: **A (load-bearing)** for Edit 2.

Both edits applied. File verified.

---

## 8. Theta_lift_GRH_bypass.md

Frontmatter sources already annotated "GRH-conditional asymptotic"; Li 2024 listed. §5.2 (E1) already corrects fake brief claim with full Li 2024 citation. Classification: **C (already corrected)**. No edit needed.

---

# Re-attempt verdict

**NO re-attempts needed for any file.**

Rationale for Class A correction in MK2_lift_to_0.85.md SL2:
- SL2 confidence 0.85 → 0.75 only affects the optional "push-to-0.90" projection.
- The main MK2 body confidence (0.86) is UNAFFECTED — SL2 is a sub-lemma, not part of the core chain.
- The honest Theorem B level-aspect confidence (0.18–0.22) is established in TheoremB_level_aspect_honest.md, driven by the FAPC₂(η>1) gap, NOT by MK2 L3 or SL2. The MK2 chain is already superseded.
- The Class A correction in GRH_bypass_FAMILY_aspect.md (Routes 1–5) does not change route verdicts — all routes failed for structural reasons unrelated to S-Y conditionality.

**Li 2024 substitution warning:** Li 2024 (Inventiones 237:697-733) is valid ONLY as an unconditional central-point quadratic-twist 2nd-moment reference. It must NOT be substituted:
- Where 2-level density was needed (Li 2024 is not a density result).
- On Re(s) = 1 (Li 2024 is at s = ½ only).
- For the Petersson weight-aspect family S_k*(N).

---

# Summary table

| File | Classification | Edit made | Re-attempt? |
|---|---|---|---|
| AUTONOMOUS_PLAN.md | B | None | No |
| B3_unconditional_attempt.md | C | None | No |
| G6_cross_term_C_f.md | C | None | No |
| GRH_bypass_FAMILY_aspect.md | C | None | No |
| RankinSelberg_trace_attack.md | C | None | No |
| TheoremB_level_aspect_honest.md | C | None | No |
| MK2_lift_to_0.85.md | A+B | 2 edits: frontmatter corrected; SL2 conf 0.85→0.75, push ceiling 0.90→0.80 | No |
| Theta_lift_GRH_bypass.md | C | None | No |
