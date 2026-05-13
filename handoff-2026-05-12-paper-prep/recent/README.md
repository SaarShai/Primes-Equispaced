# Bundle contents

This folder contains the draft Technical/Computational section of
the joint paper and its supporting material.

## Primary deliverable (sent to Koyama 2026-05-12)

| File | Purpose |
|---|---|
| `COVER_NOTE_TO_KOYAMA_2026-05-12.md` | Cover letter (body of the email). Two scope-confirmation questions and the list of Phase-1 table cells pending reconciliation. Both scope questions have been confirmed by Koyama's 2026-05-12 reply. |
| `SECTION_DRAFT_2026-05-12.md` | §X. Methodology, formalization, and numerical evidence. |
| `APPENDIX_A_BINFTY_PROOF.md` | Full pen-and-paper proof of Theorem X.4.1 (corrected $B_\infty$ identity). |
| `APPENDIX_B_CK_SUBLEADING_PROOF.md` | Full pen-and-paper proof of Theorem X.4.2 ($c_K$ leading + subleading), with the Laurent-algebra for the local Perron double-pole residue in §B.2. |
| `LEAN_SORRY_STATUS.md` | Per-`sorry` inventory of the 9-file Lean lake project. Two sorries remain (DPAC headline, LI-class); seven files are fully proved. |
| `HALO_GL1_SKETCH_2026-05-12.md` | Supplementary technical sketch: GL(1) halo-route reduction toward (SP-L). Negative finding. |

## Compiled LaTeX bundle

| Folder | Purpose |
|---|---|
| `latex/` | `paper.tex` driver, the three converted subfiles (`section_X.tex`, `appendix_A.tex`, `appendix_B.tex`), `references.bib` (18 entries), the `clean.py` regeneration pipeline, and the compiled `paper.pdf` (17 pages). Builds reproducibly via `python3 clean.py && tectonic paper.tex`. |

## Forward-looking discussion documents (drafted while Koyama is reviewing Phase-1 cells)

| File | Purpose |
|---|---|
| `INTRO_AND_ABSTRACT_OUTLINE_2026-05-13.md` | Bullet-form skeleton for the joint paper's Abstract + Introduction. |
| `ABSTRACT_DRAFT_2026-05-13.md` | Three prose Abstract variants (full / tight / minimal) drafted against the outline. |
| `INTRODUCTION_DRAFT_2026-05-13.md` | First-pass Introduction prose (~900 words, 5 subsections). |
| `SP_L_SUFFICIENT_PACKAGES_2026-05-13.md` | Focused technical note on three sufficient packages (Routes I–III) that would close (SP-L). |
| `MIDWEEK_UPDATE_TO_KOYAMA_DRAFT.md` | Pre-drafted brief status update for whenever Koyama's reconciliation arrives (week of May 20). Includes send-decision criteria and §X.5.1 variants depending on his cell-flip resolution. |
