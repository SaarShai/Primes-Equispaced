# Koyama paper-prep bundle — 2026-05-12

This folder contains the current canonical version of the
Technical/Computational section drafted in response to your
2026-05-12 note, together with its appendices and the supporting
status / scope notes.

## Files in this folder (read in this order)

1. **`COVER_NOTE_TO_KOYAMA_2026-05-12.md`** — short cover letter with
   two scope-confirmation questions, the list of Phase-1 cell
   discrepancies pending your review, and the Lean status notes.
   Read this first.

2. **`SECTION_DRAFT_2026-05-12.md`** — §X. Methodology, formalization,
   and numerical evidence (514 lines, ~10–12 typeset pages).
   Includes a §X-level References block at the end.

3. **`APPENDIX_A_BINFTY_PROOF.md`** — full pen-and-paper proof of
   Theorem X.4.1 (corrected $B_\infty$ identity). Includes §A.7 noting
   the conditional Lean formalisation in `CorrectedBInfty.lean`.

4. **`APPENDIX_B_CK_SUBLEADING_PROOF.md`** — full pen-and-paper proof
   of Theorem X.4.2 ($c_K$ leading + subleading) plus the
   Inoue/Soundararajan rate breakdown in §B.4. The pole-structure
   computation of §B.2 is the unconditional Lean closure in
   `LocalPerronResidue.lean`.

5. **`SCOPE_AUDIT_10E13_2026-05-12.md`** — authoritative internal
   note on what `x = 10^{13}` does and does not verify in our
   record (Phase-1 only, not analytic; see cover-note Q1).

6. **`LEAN_SORRY_STATUS.md`** — per-`sorry` inventory of the 9-file
   `formal-conjectures/` Lean roll-up. Currently 9 sorries; three
   files are fully proved.

7. **`HALO_GL1_SKETCH_2026-05-12.md`** — short technical note
   recording the negative finding for the GL(1) halo transfer to
   (SP-L) (§X.7 references this).

## Sibling artefacts (in `handoff-2026-05-12-paper-prep/`, parent folder)

- `APPENDIX_C_CITATIONS.md` — verbatim citation audit, kept in the
  reproducibility bundle (Supplementary S2). Not a paper appendix.
- `L2_PARI_CROSSCHECK_2026-05-12.md`, `L2_CROSSCHECK_2026-05-12.md`,
  `ARB_L2_SPOT_*.md` — supporting cross-stack verification logs.
- `local_dpac_attempts/` — Aristotle / local model dispatch records
  for the DPAC, $B_\infty$, and remaining-sorries attempts.

## Build status (as of 2026-05-12)

`lake build FormalConjectures` against `leanprover/lean4:v4.28.0` +
Mathlib commit `8f9d9cff…` succeeds on all **9 files** in
`formal-conjectures/` with **9 `sorry` warnings** (all annotated
`MATHLIB-PREREQ:` or `RESEARCH-OPEN:`). No `axiom` is introduced
anywhere.

Three files fully proved (0 `sorry`):

| File | Status |
|---|---|
| `LocalPerronResidue.lean` (Lemma X.3.1) | Unconditional |
| `CorrectedBInfty.lean` (Theorem X.4.1) | Conditional on one named `Filter.Tendsto` hypothesis |
| `DPAC_closure_attempt.lean` | DPAC for $K \in \{2,3,4\}$ unconditional + four bridges + obstruction certificate |

## Notation conventions

- Two distinct verified scales, kept rigorously separate:
  **replication scale** $x = 1.3 \cdot 10^{13}$ (Phase-1
  Dominance-of-$-1$), and **analytic-identity scale**
  $K \le 10^{7}$ (the four-pair $B_\infty$, $C_1$, and Aoki–Koyama
  drift evidence).
- `(AK)`, `(SP-L)`, `(NDC)` are the three named tagged equations
  in §X.4.
- "Q:Perron", "Q:DPAC", "Q:EC-recip" are the three primary open
  problems in §X.7; "Further questions" covers EC follow-ups.

## What is open for the section

- Headline DPAC at general $K$ — diagnostically LI-class (research-open).
- (SP-L) — open; the halo-route negative finding is recorded in
  `HALO_GL1_SKETCH_2026-05-12.md`.
- GL(2) reciprocal-derivative control (Q:EC-recip) — open.

## What is pending your input (per cover note)

- Two scope confirmations (cover-note questions 1–2).
- Resolution of the Phase-1 Table discrepancies (cover-note table
  of six cells with substantive disagreement flagged for $N=11$
  $a=10$, $N=19$ $a \in \{13, 18\}$).
