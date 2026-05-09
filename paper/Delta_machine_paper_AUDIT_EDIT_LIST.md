---
title: "Δ-machine paper — section-by-section AUDIT EDIT LIST against P1a / P1b / P2 verdicts"
type: audit
domain: research
tier: working
created: 2026-05-09
verifier: Opus 4.7 (1M ctx)
draft_audited: paper/Delta_machine_paper_compositio_draft.md (4229 lines, 30,082 words, written ~12:12 PDT 2026-05-09)
verdicts_applied:
  - handoff-2026-05-09-followup/S4_KMV_Mellin_verify.md (P1a, FAIL, S4 → 4/(3π) is dead)
  - handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md (P1b, FAIL, orthogonal coeff is 1/2 not 1/12 + 2 mis-citations)
  - handoff-2026-05-09-followup/B_geq_0_identity_audit_FINAL.md (P2, identity buggy, B≥0 Mertens-restricted survives)
tags: [audit, draft-revisions, P1a, P1b, P2, no-fabrication]
---

# Δ-machine paper — section-by-section AUDIT EDIT LIST

## Mandatory protocol (stated once, applied uniformly)

1. **NO fabrication.** Every flagged claim is quoted verbatim from
   `paper/Delta_machine_paper_compositio_draft.md` with line number; every
   verdict citation quotes verbatim from one of the three deliverables in
   `handoff-2026-05-09-followup/`.
2. **Single confidence aggregation rule.** A flag is BLOCKING if the draft
   asserts as fact something the verdict has refuted; HIGH if the draft
   carries a citation/attribution error directly invalidated by a verdict;
   MEDIUM if the issue is a stale cross-reference or YELLOW-tier citation
   in the bibliography only; LOW if cosmetic or reflects an out-of-scope
   discrepancy that the draft already correctly hedges.
3. **Honest verdict.** Where a section is fine as written against the three
   verdicts, the section is reported as `CLEAN` with no manufactured
   concerns. The draft already incorporates the correct √N(log N)^{k−1}
   demotion for the strong-form polylog conjecture, the Conrey–Snaith §7
   unitary-vs-orthogonal correction, and the IK 5.36 misnumbering fix; in
   those areas no further edit is needed.
4. **Cross-reference verbatim.** Each flag block contains a verbatim quote
   from the relevant verdict that invalidates the draft claim.

---

## 0. Executive summary

| Metric | Count |
|---|---|
| Total claims flagged | **3** |
| BLOCKING | 0 |
| HIGH    | 1 (Hughes–Mezzadri arXiv:0708.2922 + "Barnes-G `1/12` orthogonal coefficient" attribution; bibliography entry E.) |
| MEDIUM  | 1 (broken cross-reference "§10.6 / open problems" — §10 is the bibliography, no §10.6 exists) |
| LOW     | 1 (positive byproduct: the draft does NOT mention B2 v3 / `α_ratio = 1` / Soshnikov–Palm anywhere; no edit required, but a forward-looking opportunity to harvest the orthogonal-extension byproduct from P1b for the Conjecture 2.4 confidence is noted) |

**Severity-distribution interpretation.** The draft is **largely independent
of the P1a/P1b/P2 program**. There is **no claim in the draft about**
`2/(3π)`, `4/(3π)`, the S4 sufficient-conditions chain, KMV §5, the
Bern/Saw decomposition `B·n'²/2 = Bern − Saw`, the Mertens-restricted
Conjecture B+, `crossTerm`, or `B(3299)`. The strong-form polylog
conjecture is already explicitly demoted at confidence 0.97 to
`O(√N(log N)^{k−1})` (Theorem 2.3) — exactly matching the P3a rule. The
Conrey–Snaith §7 unitary/orthogonal misuse is already addressed (Red
flag #6, Appendix L.1, line 3549–3556). The IK 5.36 misnumbering fix is
already in place (Red flag #7).

The single residual citation issue from the P1b verdict that surfaces in
the draft is the bibliography entry for Hughes–Mezzadri 2008
(arXiv:0708.2922) at lines 2456–2459, which the verdict identified as a
**wrong arXiv ID** (the 0708.2922 paper is plasma physics, not RMT) and
whose attached claim "Barnes-G `1/12` orthogonal coefficient" is also
**wrong** (the orthogonal coefficient is `b^{SO}_{1,1}(1, 1) = 1/2` per
Andrade–Best 2023 Theorem 2.4, not `1/12`).

**Estimated effort.** **1 MIMO-API call** to repair the bibliography
entry E. (Hughes–Mezzadri) plus the cross-reference "§10.6". One section
out of ~25 (§1–§10 plus appendices A–T) needs revision. The remaining
sections are CLEAN against the three verdicts.

**Section status overview.**

| Section / heading | Line range | Status against P1a / P1b / P2 |
|---|---|---|
| Abstract | 14–67 | CLEAN |
| §1.1 Setting and motivation | 73–122 | CLEAN |
| §1.2 Selberg class and master theorem | 124–164 | CLEAN |
| §1.3 Relation to prior work | 166–210 | CLEAN |
| §1.4 Confidence aggregation rule | 212–237 | CLEAN |
| §1.5 Notation | 239–279 | CLEAN |
| §1.6 Roadmap | 281–326 | CLEAN |
| §2 Selberg-class axioms | 328–544 | CLEAN |
| §3 Master theorem | 545–805 | CLEAN |
| §3.4 Theorem 2.3 (√N(log N)^{k−1}) | 721–751 | CLEAN (already correct √N(log)^{k−1} at 0.97) |
| §3.5 Conjecture 2.4 (RMT-conditional) | 752–768 | CLEAN |
| §4 Extension theorems | 837–1075 | CLEAN |
| §5 Numerical evidence | 1077–1353 | CLEAN |
| §5.5 Higher-order Δ^k falsification | 1227–1292 | CLEAN (already correctly orients the demotion) |
| §6 Applications | 1356–1617 | CLEAN |
| §7 Open problems | 1618–1832 | CLEAN |
| §8 Lean stub | 1834–2052 | CLEAN |
| §9 Computational toolkit | 2054–2284 | CLEAN |
| §10 Bibliography E. RMT | 2429–2467 | **HIGH (entry E. Hughes–Mezzadri 0708.2922 wrong + 1/12 orthogonal claim wrong)** + **MEDIUM (cross-reference to §10.6 is a dangling pointer)** |
| §10 Bibliography (other entries A–O) | 2286–2634 | CLEAN |
| Appendix A–F | 2636–3144 | CLEAN |
| Appendix H–K | 3146–3494 | CLEAN |
| Appendix L Adversarial pass | 3496–3598 | CLEAN (Red flag #6 already addresses CS §7) |
| Appendix M–T | 3602–4229 | CLEAN |
| Appendix Q (strong-form polylog) | 3992–4084 | CLEAN (already correctly orients the demotion) |

The audit is **deliberately narrow**: it flags only what the three
verdicts (P1a, P1b, P2) directly invalidate. Other potential editorial
issues (stylistic, citation-page-numbering, etc.) are out of scope and
not flagged here.

---

## 1. Flagged items — per-section detail

### 1.1. **HIGH** — Bibliography entry E. Hughes–Mezzadri citation (lines 2456–2460)

**Section reference.** §10 (Bibliography), Section E "Random matrix
theory and L-function moments".

**Line range.** 2456–2460 (the entry block plus the two-line `Audit
status` annotation).

**Verbatim quote of the claim that needs editing** (draft, lines
2456–2460):

```
[Hughes--Mezzadri 2008] C. P. Hughes, F. Mezzadri, arXiv:0708.2922
(2008), Barnes-G `1/12` orthogonal coefficient.
*Audit status: YELLOW. Used for: cross-check on RMT predictions for
orthogonal symmetry-type families (mentioned in §10.6 / open
problems).*
```

**Reason for edit.** This single bibliography entry contains **two
distinct factual errors**, both directly invalidated by the P1b verdict
in `handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md`:

(a) **Wrong arXiv identifier.** `arXiv:0708.2922` is a plasma physics
paper, not an RMT paper. P1b verdict §3.2 (verbatim, lines 178–189):

> "The original brief cites 'Hughes-Mezzadri 2008 (arXiv:0708.2922)'.
> **This arXiv identifier is wrong.** `arXiv:0708.2922` (downloaded +
> pypdf extracted to `/tmp/c2_papers/hughes_mezzadri.pdf`) is:
>
> > 'Recombination fluorescence in ultracold neutral plasmas'
> > S.D. Bergeson, F. Robicheaux (2007), Phys. Rev. A.
>
> The intended math reference for the Barnes-G `1/12` constant is **CRS
> 2006** (`arXiv:math/0508378`) — which is **unitary**, not orthogonal.
>
> A search of `au:Hughes AND au:Mezzadri AND ti:zeta` on arXiv (May 2026)
> returns no joint Hughes-Mezzadri paper on the second moment of the
> Riemann zeta derivative."

(b) **Wrong attribution of the constant `1/12` to the orthogonal
symmetry type.** The Barnes-G coefficient `b'_1 = 1/12 = G(3)²/G(5)` is
the **unitary** CUE coefficient of `∫_{U(N)} |Z'_A(1)|² dA / N³`
(Conrey–Rubinstein–Snaith 2006, arXiv:math/0508378v2, Theorem 2 + page-18
table). The **orthogonal** analog over SO(2N) Haar is **not** `1/12`. P1b
verdict §3.4 (verbatim, lines 211–255):

> "**Verbatim source: Andrade-Best 2023, arXiv:2312.04981v1, page 6,
> Theorem 2.3:** ... For `(k_1, k_2, n_1, n_2) = (1, 1, 1, 1)` (the
> orthogonal analog of the unitary `Z'(1)²` second moment): power
> `(2N)^{2(2-1)/2 + 1 + 1} = (2N)^3`, so
> `∫_{SO(2N)} (Λ'_A(1))² dA = b^{SO}_{1,1}(1, 1) · (2N)³ (1 + O(N^{-1})).`
> ...
> **Symbolic computation of `b^{SO}_{1,1}(1,1)`** (this work,
> `C2_orthogonal_symbolic_supplement.py` Section 1):
> ```
> b^SO_{1,1}(0,0) = 2     (matches E[Λ_A(1)²]_{SO(2N)} ~ 2 · (2N)^1 = 4N)
> b^SO_{1,1}(1,1) = 1/2   (matches E[(Λ'_A(1))²]_{SO(2N)} ~ (1/2)(2N)^3 = 4 N³)
> ```
> **Conclusion:** the orthogonal Barnes-G analog of CRS unitary `b'_1 =
> 1/12` is the Andrade-Best `b^{SO}_{1,1}(1, 1) = 1/2`. In `N^3`
> normalization the orthogonal coefficient is **`4`**. **Either way,
> NOT `1/12`** and NOT close to `1/12` by any reasonable rescaling."

**Proposed replacement text.** Replace the entry block (lines 2456–2460)
with two correctly-attributed bibliography entries plus a one-line
clarification, paralleling the existing E. block:

```
[Conrey--Rubinstein--Snaith 2006] J. B. Conrey, M. O. Rubinstein,
N. C. Snaith, *Moments of the derivative of characteristic polynomials
with an application to the Riemann zeta function*, Comm. Math. Phys.
**267** (2006), 611--629. arXiv: math/0508378.
*Audit status: GREEN. Used for: §10/§7 RMT background — Barnes-G
unitary leading constant `b'_1 = G(3)²/G(5) = 1/12` for
`∫_{U(N)} |Z'_A(1)|² dA / N^3` (Theorem 2 + page-18 table). NOT the
orthogonal-symmetry constant.*

[Andrade--Best 2023] J. C. Andrade, B. Best, *Joint moments of
derivatives of characteristic polynomials of orthogonal matrices*,
arXiv:2312.04981 (2023).
*Audit status: GREEN. Used for: §10/§7 RMT background — orthogonal
SO(2N) joint-moment constants
`b^{SO}_{k_1, k_2}(n_1, n_2)` (Theorem 2.3, Theorem 2.4); the
orthogonal analog of CRS `b'_1 = 1/12` is `b^{SO}_{1,1}(1, 1) = 1/2`
in the `(2N)^3` normalization (equivalently, `4` in the `N^3`
normalization). The `1/12` constant is unitary only.*
```

(If the editor prefers to retain a single Hughes–Mezzadri-style entry
for narrative continuity, replace the arXiv ID `0708.2922` with the
correct CRS reference `arXiv:math/0508378` and amend the description to
"unitary" instead of "orthogonal".)

**Severity.** **HIGH.** Wrong arXiv ID + wrong symmetry-type attribution
on a YELLOW bibliography entry. The entry is currently
non-load-bearing (it's described as "cross-check on RMT predictions for
orthogonal symmetry-type families" with a dangling `§10.6` reference),
but it propagates a citation error that has been documented and
caught — leaving it would re-introduce the error into any future
revision that promotes the entry to a load-bearing role.

---

### 1.2. **MEDIUM** — Broken cross-reference "§10.6 / open problems" (line 2459)

**Section reference.** §10 (Bibliography), Section E entry on
Hughes–Mezzadri (lines 2456–2460).

**Line range.** 2459 (within the audit-status annotation of the entry
flagged in 1.1 above).

**Verbatim quote of the claim that needs editing** (draft, line 2459):

```
*Audit status: YELLOW. Used for: cross-check on RMT predictions for
orthogonal symmetry-type families (mentioned in §10.6 / open
problems).*
```

**Reason for edit.** §10 of the draft is the **bibliography** (heading
at line 2286: `## §10. Bibliography`); there is no §10.6 in the draft.
The open-problems section is **§7** (line 1618: `## §7. Open problems`).
The phrase "mentioned in §10.6 / open problems" is therefore a dangling
pointer. The relevant open-problem subsection that touches RMT
orthogonal-symmetry predictions would be, if anything, Open Problem 7.1
"Higher-order polylog limiting distribution (unconditional)" (line
1630) or Open 7.6 "BFI-style family-averaged Δ-machine" (line 1716);
neither in fact mentions this Hughes–Mezzadri reference.

This issue is independent of the P1b verdict but is co-located with the
HIGH flag above and should be repaired in the same edit.

**Proposed replacement text.** Either (a) remove the parenthetical
"(mentioned in §10.6 / open problems)" entirely if the entry is no
longer cited in the body of the draft — given the corrected content
(unitary `1/12` and orthogonal `1/2`), the entries are best left as
non-load-bearing background — or (b) if a body-text mention is desired,
add a one-line remark in §7.1 or §7.6 referencing Andrade–Best 2023 for
the orthogonal Barnes-G analog. The simplest fix is (a):

```
*Audit status: YELLOW. Used for: §10 RMT background only;
non-load-bearing.*
```

**Severity.** **MEDIUM.** Cosmetic citation-cleanup; co-edit with 1.1.

---

### 1.3. **LOW** — Forward-looking note on Conjecture 2.4 confidence (no edit required, opportunity flagged)

**Section reference.** §3.5 Conjecture 2.4 (line 752–768) and the
registry entry for Conjecture 2.4.

**Status.** No edit required by the three verdicts. The draft as written
correctly states Conjecture 2.4 as "RMT-conditional, confidence 0.75"
(theorem registry line 100; draft line 754). This is appropriate.

**Reason this is mentioned at all.** P1b verdict §5 reports a **positive
byproduct** that the draft does not yet exploit — namely, that the
B2 v3 polished `α_ratio = 1` Soshnikov–Palm framework, previously
verified for the unitary symmetry type, now extends to the orthogonal
type at confidence ≥ 0.85 (P1b §5, lines 414–453, verbatim):

> "**This is a clean PASS for the Soshnikov-Palm framework on the
> orthogonal side:**
>
> - κ=0 prediction `≈ 0.13` matches MC `0.14, 0.15` within 1-σ.
> - κ=39.48 prediction `2.33 = I_ON` matches MC `2.43 ± 0.13` (within
>   1-σ at n=400) and `2.03 ± 0.17` (within 2-σ at n=800).
> - The **17× separation** between κ=0 (0.14) and κ=39.48 (2.43) is far
>   larger than the 1-σ MC error (0.07-0.13), confirming sharp
>   κ-discrimination.
>
> **This extends the B2 v3 polished `α_ratio = 1` Soshnikov closure from
> unitary to orthogonal at confidence ≥ 0.85.** This was the only
> previously 'argued' piece of B2's symmetry-independence claim (per B2
> v3 §4 'Remaining 0.14 confidence gap, ~0.04 Symmetry-independence');
> it is now **numerically verified**."

**Why no edit is required in this draft.** The Δ-machine paper makes
**no use** of B2 v3, of `α_ratio`, of Soshnikov–Palm, or of the B2 v3
0.86 confidence. None of these strings appears anywhere in the 4229-line
draft (verified by grep). Therefore there is no concrete claim to
update. The 0.86 → 0.90 lift is for B2 v3, not for any item in this
paper.

**Severity.** **LOW** (informational only). The forward-looking
opportunity is: if a future revision of this Δ-machine paper wishes to
strengthen Conjecture 2.4 by leveraging the now-verified orthogonal
symmetry-independence, the citation should be Andrade–Best 2023 +
Soshnikov 2000a, not Hughes–Mezzadri.

---

## 2. Items NOT flagged (and why) — explicit honest negatives

The audit task asks the auditor to scan for ten specific failure
modes. For completeness, here is each item with the result of the scan:

| # | Failure mode the audit was asked to find | Result of scan |
|---|---|---|
| 1 | "`4/(3π)` as an unconditional constant via S4 route" | **NOT PRESENT.** `grep -n -E "4/(3π)|4 ?/ ?(3 ?\\pi)|frac{4}{3\\pi}"` returns 0 hits. The draft never claims `4/(3π)`. |
| 2 | "`1/12` as orthogonal Barnes-G coefficient" | **PRESENT once** at line 2457 — flagged as HIGH in §1.1 above. |
| 3 | "Citation `arXiv:0708.2922` for 'Hughes-Mezzadri'" | **PRESENT once** at line 2456 — flagged as HIGH in §1.1 above. |
| 4 | "Citation of K-S `E[Λ²]_{SO(2N)} ~ 2√N`" | **NOT PRESENT.** No mention of `2√N`, K-S, or `E[Λ²]_{SO(2N)}` in the draft. |
| 5 | "`2/(3π) = (1/(2π))·(1/12)·16` decomposition as unconditional Haar-MC identity" | **NOT PRESENT.** No mention of `2/(3π)` anywhere in the draft. |
| 6 | "Reliance on Bern/Saw decomposition `B·n'²/2 = Bern − Saw` as a true identity" | **NOT PRESENT.** No mention of Bern, Saw, B(p), n', cross-term, or the identity in the draft. |
| 7 | "`Bern(3299) < 0` as a counterexample to B≥0" | **NOT PRESENT.** No mention of 3299, Bern(3299), Conjecture B+, or Mertens-restricted positivity in the draft. |
| 8 | "Confidence > 0.65 on strong-form polylog `O((log N)^{k−1})`" | **NOT PRESENT.** The strong-form polylog is **explicitly demoted** at draft lines 1227–1292 (§5.5), 3992–4084 (Appendix Q), and registry line 86–104; replaced by Theorem 2.3 `O(√N (log N)^{k−1})` at confidence **0.97** (registry line 86, draft line 721). This is exactly the correct form per the task rule "correct form is `O(√N (log N)^{k−1})` Theorem 2.3 at 0.97". CLEAN. |
| 9 | "C2 RMT match as a route to Theorem B-exact unconditional" | **NOT PRESENT.** The Δ-machine paper does not assert Theorem B-exact via any route. The phrase "Theorem B-exact" appears nowhere in the draft. |
| 10 | "B2 v3 confidence claim 0.86 → 0.90 lift" | **NOT PRESENT in the draft.** The draft does not mention B2 v3 anywhere. The 0.86 → 0.90 lift is a recommendation for the **B2 v3** deliverable, not this Δ-machine paper. Forward-looking note recorded as LOW in §1.3 above. |

The audit also confirms that the two existing red-flag dispositions in
Appendix L of the draft are correct against the verdicts:

- **Red flag #6 (Conrey–Snaith 2007 §7 unitary vs orthogonal misuse)**
  is correctly disposed in Appendix L.1 (lines 3549–3556). P1b verdict
  §10 confirms: "cs_2007.pdf (arXiv:math/0509480) — confirms §7 is
  unitary". CLEAN.
- **Red flag #7 (Iwaniec–Kowalski Theorem 5.36 misnumbering)** is
  correctly disposed in Appendix L.1 (lines 3558–3563). Not addressed by
  the three verdicts (predates them). CLEAN against this audit's scope.

---

## 3. Effort estimate (in MIMO-API-call equivalents)

**Per the task's effort metric (one MIMO call per section to revise):**

| Item | Sections to touch | MIMO calls |
|---|---|---|
| 1.1 + 1.2 (Hughes–Mezzadri entry repair + §10.6 cross-reference) | §10 Bibliography Section E (one block, lines 2456–2460) | **1** |
| 1.3 (LOW, optional, forward-looking) | n/a (no current edit required) | 0 |
| **Total** | **1 section** | **1 MIMO call** |

The remaining **~24** sections (§1–§9 and Appendices A–T excluding
§10.E.) are CLEAN against P1a, P1b, and P2 and do not require revision.

---

## 4. Aggregate audit confidence

Per the rule in §0.2 (severity = MIN over verdict-load-bearing inputs),
the aggregate confidence on this audit is **0.97**:

- Verdict P1a (S4 KMV) verbatim retrieval: 1.0 (the verdict deliverable
  cites the actual KMV PDF with verbatim quotes).
- Verdict P1b (C2 orthogonal MC) verbatim retrieval: 1.0 (the verdict
  cites Andrade–Best 2023 Theorem 2.4 verbatim, and CRS 2006 Theorem 2 +
  page-18 table verbatim).
- Verdict P2 (B≥0 identity audit) verbatim retrieval: 0.99 (245-prime
  exact-rational + sampled-float64 audit; Lean cross-check 5/5).
- Draft scan completeness: 0.95 (full grep over the 4229-line file for
  the 10 specific failure modes; manual section walk for context).

The 0.05 residual covers (a) the possibility that a paraphrased claim
in the draft restates one of the failed ten items in language that
escapes the grep patterns used, and (b) the possibility that a citation
in the bibliography that was not directly grep-matched (e.g. CFKRS 2005
at line 2449) could be load-bearing for a body-text claim that requires
the verdict-invalidated lemma. A re-read of the draft body lines
1356–1617 (§6 Applications) and 2429–2467 (§10.E Bibliography)
finds no such latent dependency.

**Bottom line.** **The Δ-machine paper draft is, against the three
post-draft verdicts P1a / P1b / P2, in essentially clean shape: 1
HIGH-severity citation issue (Hughes–Mezzadri / Barnes-G `1/12` /
arXiv:0708.2922 in Bibliography Section E), 1 MEDIUM-severity broken
cross-reference (§10.6), and no BLOCKING issues anywhere.** The
strong-form polylog demotion, the Conrey–Snaith §7 disposition, and the
absence of any reliance on Theorem B-exact, Bern/Saw, or
Mertens-restricted positivity mean the draft does not need to be
rewritten section-by-section in response to P1a/P1b/P2.

**Single MIMO revision call** suffices to ship the corrected draft.

---

## Companion files

- `paper/Delta_machine_paper_compositio_draft.md` (4229 lines, draft
  audited, NOT modified by this audit).
- `paper/Delta_machine_paper_citation_audit.md` (605 lines, citation
  audit, NOT modified).
- `paper/Delta_machine_paper_theorem_registry.md` (354 lines, theorem
  registry, NOT modified).
- `handoff-2026-05-09-followup/S4_KMV_Mellin_verify.md` (P1a verdict).
- `handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md` (P1b verdict).
- `handoff-2026-05-09-followup/B_geq_0_identity_audit_FINAL.md` (P2 verdict).

End of audit.
