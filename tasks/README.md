# Task Bundle — 2026-05-09

Five self-contained task prompts dispatched to advance the top 3 priorities committed in [`HANDOFF.md`](../HANDOFF.md).

## Tasks

| # | File | Direction | Target | Estimated wall-clock |
|---|---|---|---|---|
| **P1a** | [`P1a-T1-PARI-Mellin-KMV.md`](P1a-T1-PARI-Mellin-KMV.md) | T1 — KMV §5 leading constant via PARI/GP Mellin | Opus 4.7 extra-high | 1–4 hours |
| **P1b** | [`P1b-T2-orthogonal-MC.md`](P1b-T2-orthogonal-MC.md) | T2 — orthogonal Barnes-G coefficient `1/12` via Monte Carlo | Opus 4.7 extra-high | 4–24 hours |
| **P2** | [`P2-B-geq-0-identity-audit.md`](P2-B-geq-0-identity-audit.md) | B≥0 identity audit — `B·n'²/2 = Bern − Saw` vs original `B(p)` | Opus 4.7 extra-high | 4–12 hours |
| **P3a** | [`P3a-G1-delta-machine-bundle.md`](P3a-G1-delta-machine-bundle.md) | G1 — Δ-machine Compositio paper synthesis (~50pp) | Opus 4.7 extra-high | 8–24 hours |
| **P3b** | [`P3b-G3-lean-smoothed-dwf.md`](P3b-G3-lean-smoothed-dwf.md) | G3 — `SmoothedDwfFormula.lean` extension stub→full (~600 LOC) | **Aristotle** (harmonic.fun) | 4–8 weeks autonomous |

## Mandatory protocol (every task)

Embedded verbatim in each task file:

1. **NO fabrication** — every cited theorem must be verified by `curl + pdftotext` on the actual paper. Quote verbatim with page or equation number.
2. **Single confidence aggregation rule** — state at start of deliverable, never switch mid-document.
3. **Honest verdict** — if route fails, state precisely why; if succeeds, identify gaps.
4. **Cross-reference prior failures** — read the failure files listed in each task so as not to repeat work.
5. **Don't switch families** — Theorem B work stays on weight aspect Petersson family `F_k = S_k*(N)` squarefree N, k → ∞ along k = T^a, 1 < a < 2.

## API key requirements

| Task | Needs | Status |
|---|---|---|
| P1a, P1b, P2, P3a | Anthropic Opus 4.7 | `ANTHROPIC_API_KEY` set ✓ |
| P3b | Aristotle (harmonic.fun) | wired in `~/.farey_api_keys` (mode 600) ✓ |
| Fallback for P3a if Opus rate-limited | MIMO | wired in `~/.farey_api_keys` (mode 600) ✓ |

To export before dispatch:

```bash
set -a; source ~/.farey_api_keys; set +a
```

For MIMO calls: always set `"thinking":{"type":"disabled"}` else `content` returns empty, per [`delta-machine-roadmap.md`](../handoff-2026-05-04-theorem-B-and-C1/delta-machine-roadmap.md) note.

## Dispatch order recommendation

| Slot | Tasks | Rationale |
|---|---|---|
| Day 1 (parallel) | P1a + P1b + P2 | All three deliver verdicts within 1–2 days. P1a+P1b together close Theorem B-exact unconditional if both pass; P2 unblocks Paper B regardless of P1 outcome |
| Day 1 (background) | P3b kicked off to Aristotle if key available — runs autonomously for weeks | Long pole; start ASAP |
| Week 1+ (after P1+P2 land) | P3a only after P1 verdict known | If P1 lands, P3a can cite the unconditional Theorem B-exact result; if P1 fails, P3a still ships independently as Compositio paper |

## Done criteria for this round

| | Done when |
|---|---|
| **P1 round** | One of: (T1 + T2 both pass → unconditional Theorem B-exact deliverable) OR (T1 passes alone, T2 fails → cage-only result holds) OR (both fail → ratios-conjecture wall confirmed, P1 dropped) |
| **P2 round** | Identity audit verdict: BUGGY (B≥0 conjecture survives, Paper B positivity safe) OR CORRECT (Bern(3299)<0 is real counterexample, Paper B positivity dies, reframe as conjecture-with-evidence) |
| **P3a round** | `Delta_machine_paper_compositio_draft.md` exists at ≥40 pages, LaTeX-ready, all theorems cited verbatim |
| **P3b round** | `lake build SmoothedDwfFormula` returns 0; `R0_eq_neg_two`, `mellin_transform`, `contour_shift` lemmas all proved (no `sorry`) |
