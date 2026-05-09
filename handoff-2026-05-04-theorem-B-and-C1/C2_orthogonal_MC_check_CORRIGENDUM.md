---
title: "C2 Orthogonal MC Check — Corrigendum (post-2026-05-09 audit)"
date: 2026-05-09
type: corrigendum
supersedes_within: C2_orthogonal_MC_check.md
status: load-bearing — these errors fed the broken `2/(3π)` decomposition and have been verified against the actual papers
---

# Corrigendum

The audit run by P1b agent (orthogonal Barnes-G Monte Carlo, 2026-05-09) caught **two load-bearing errors** in the original `C2_orthogonal_MC_check.md`. Original file is preserved verbatim; corrections recorded here.

## Error 1 — wrong arXiv identifier

| | |
|---|---|
| Cited as | `arXiv:0708.2922` for "Hughes-Mezzadri orthogonal `1/12`" |
| Actually | `arXiv:0708.2922` is a **plasma physics paper**, not Hughes-Mezzadri |
| Likely intended | CRS 2006 (`arXiv:math/0508378`) — and that paper is **unitary**, NOT orthogonal |
| Net | Wrong arXiv ID, wrong paper, wrong symmetry type. Triple-wrong. The `1/12` does correctly belong to the **unitary** Barnes-G `G(3)²/G(5)`, but the `Reverse_engineer_constant.md` decomposition needs an **orthogonal** coefficient. |

## Error 2 — wrong asymptotic for `E[Λ²]_{SO(2N)}`

| | |
|---|---|
| Cited as | Keating-Snaith `E[Λ_A(1)²]_{SO(2N)} ~ 2√N` |
| Actually | Andrade-Best 2023 (`arXiv:2312.04981`) Theorem 2.4 gives `b^{SO}_{1,1}(1,1) = 1/2` in `(2N)³` normalization, equivalently `~ 4N` in `N³` normalization |
| Verification | Fresh K=20000 Monte Carlo at SO(2N) reproduces `~ 4N` to within MC error; the cited `~ 2√N` form is off by 5–12× across N=200…800 |
| Net | The cited K-S `2√N` form does not match either Andrade-Best or fresh MC. Use **`E[Λ_A(1)²]_{SO(2N)} ~ 4N`** going forward. |

## Knock-on effect on the `2/(3π)` decomposition

`Reverse_engineer_constant.md` claimed `2/(3π) = (1/(2π)) · (1/12) · 16` interpreted as a Haar-MC orthogonal identity over SO(2N). With the corrected orthogonal coefficient `1/2` (or `4` in `N³`), the decomposition is **wrong as written**. The path to Theorem B-exact unconditional via this RMT-decomposition (the C2 route) is closed.

## Source of truth going forward

- For unitary CUE: CRS 2006 (`arXiv:math/0508378`), unitary `G(3)²/G(5) = 1/12` correct
- For orthogonal SO(2N): Andrade-Best 2023 (`arXiv:2312.04981`) Theorem 2.4, `b^{SO}_{1,1}(1,1) = 1/2` (or `4` in `N³`)
- See P1b deliverable `handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md` for the full audit trail with verbatim quotes and MC reproductions

## Recommendation

When re-reading `C2_orthogonal_MC_check.md` or any document that depends on it, mentally substitute these corrections and treat the original as superseded on these two points. The Soshnikov α_ratio=1 argument inside `B2_R_neigh_v3_polished.md` is unaffected (and was independently verified to extend to orthogonal symmetry by the same P1b agent — see `C2_orthogonal_MC_extended.md` §4).
