---
schema_version: 5
title: "Primes-Equispaced Current Handoff (post 2026-05-09 session)"
type: handoff
domain: project
tier: working
confidence: 0.95
created: 2026-05-09
updated: 2026-05-09 (end of session)
verified: 2026-05-09
sources:
  - SESSION_SUMMARY_2026-05-09.md
  - log.md
  - handoff-2026-05-04-theorem-B-and-C1/THEOREM_B_HANDOFF.md
  - handoff-2026-05-04-theorem-B-and-C1/C1_SELF_RESIDUE_HANDOFF.md
  - handoff-2026-05-09-followup/*.md
  - paper/Delta_machine_paper_*.md
supersedes:
  - 2026-05-09 (mid-session) HANDOFF
tags: [handoff, primes-equispaced, theorem-B, b+-conjecture, mertens-lb, breakthrough-map]
---

# Primes-Equispaced Current Handoff

## Start here (post-Koyama-pivot, end of 2026-05-09 session)

→ [`handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md`](handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md) — final state of the Koyama-correspondence track resolution, with all 6 conjectures' verdicts, the constant correction (`1/ζ(2)` → `1/e^γ`), and honest significance assessment.

→ [`SESSION_SUMMARY_2026-05-09.md`](SESSION_SUMMARY_2026-05-09.md) — mid-session summary covering the pre-Koyama work (Theorem B / cage / B+ Mertens-restricted / Δ-machine).

## One-paragraph state

The 5 near-term routes to **Theorem B-exact unconditional `2/(3π)`** are all formally closed (S4, C2, geometric/motivic, C1 Synthesis (E), B'-denom). Only the multi-decade Grand Density Conjecture support-4 wall remains. **Conjecture B+ Mertens-restricted** survives (P2 retracted the Bern/Saw refutation as a wrong-displacement decomposition) and is reduced via R1 + SP-1a + SP-2 to a pure rank-displacement inequality `S_ψ(p) < B₀(p−1)` with both sides closed-form rationals via 10 new exact identities (none in any prior B+ literature). The remaining unconditional gap is **(MERTENS-LB)**: a one-sided sign bound on the Möbius-harmonic Mertens sum `1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'` — a fresh open problem of Pólya-conjecture shape (Pólya's `L(x) ≤ 0` was empirically true for huge ranges then disproved at large N).

## The breakthrough nominee

**(MERTENS-LB)** — a one-sided sign bound on the Möbius-harmonic Mertens sum surfaced by SP-2's new identity (C4):

> Prove: `1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'` for all `N ≥ N_0`, with explicit `c' > 1`.

Closes the SP-2 layer of B+ unconditional. Concrete, falsifiable. Plausibly attackable via Lambert series, Selberg's symmetry formula, explicit-formula direct estimation, or computational disproof at large N (Pólya-style — itself a major result if it lands). May transfer technique to the SP-1 layer.

## Koyama-track results (this session, post-pivot)

Pivoted from B+ Mertens-restricted track (which was killed by (MERTENS-LB) Pólya-flips) to Saar's correspondence with Koyama. **Three theorems proved, one constant corrected, one universality empirically falsified, one dispatched to Aristotle.**

| # | Conjecture | Verdict | Conf |
|---|---|---|---:|
| C1 | NDC universality | **PROVED, REVISED**: `D_K → 1/e^γ` (not `1/ζ(2)`) | ~0.94 |
| C2 | AK constant | **PROVED with correction**: `E_K · log K → L'/e^γ` (Aoki-Koyama 2023 eq. (1.4) p.235 had it; Saar/Koyama/my-prompt all missed it). Catch #16. | 0.97 |
| C3 | Subleading C_1 = −L''/(2L'²) | **PROVED** (Inoue 2021 framework, DRH-conditional) | 0.94 |
| C4 | B_∞ explicit formula | **PROVED UNCONDITIONALLY** | 0.96 |
| C5 | EC NDC universality | **EMPIRICALLY FALSIFIED** — rank-dependent constants | — |
| C6 | DPAC | dispatched to Aristotle (project `59d181d5-...`) | async |

**16 misattributions caught total** since 2026-05-03 (12 in research artifacts, 4 in my own dispatch briefs). The 4-way chain Saar→Koyama→Saar→me on AK 2023 eq. (1.4) was the most consequential — caught a 8% wrong-constant claim before publication.

## Three programs — current status

| Track | Status |
|---|---|
| **Paper A — Theorem B Annals headline** | Cage uncond `(17 ± √145)/(12π)` at 0.97 unchanged. B2 v3 Soshnikov α_ratio=1 lifted 0.86→0.90 by P1b orthogonal symmetry-independence verification. F(γ) bias envelope 0.88→0.95 (R4). 2/(3π) GRH-conditional 0.85; unconditional ≤0.05 (5 of 5 routes closed). |
| **Paper B — Compositio Farey side** | **Unblocked.** Conjecture B+ confidence restored 0.40→0.80 (P2). Reduction chain via R1 + SP-1a + SP-2 is theorem-grade. (MERTENS-LB) sub-problem named explicitly as load-bearing future work. |
| **Δ-machine paper — Compositio sibling** | **30,082-word draft + 605-line citation audit + 354-line theorem registry.** Strong-form polylog corrected to `O(√N (log N)^{k−1})` Theorem 2.3 (0.97). Cross-Selberg axis-pole structural fix landed (F2 — Open Problem 7.2 resolved). Bibliography corrected (CRS 2006 + Andrade-Best 2023 replacing wrong arXiv:0708.2922). Murty-Murty 2009 prior-art audit flagged as pre-submission requirement. |

## Aristotle async pipeline

| Project ID | Label | Status |
|---|---|---|
| `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad` | SmoothedDwfFormula | COMPLETE_WITH_ERRORS — accepted as scaffolding (option B); R₀ anchor solid; 2 Mathlib gaps named (uniform Stirling, Titchmarsh `1/ζ` polynomial growth) |
| `8e608890-f0ba-4a89-bbb0-a63b5bcab697` | R1_B_plus | IN_PROGRESS — 4 algebraic-identity theorems |

Poll: `./scripts/poll_aristotle.sh` (one-shot) or `./scripts/poll_aristotle.sh --watch`.

## Codified protocol (mandatory for any "this works" claim)

1. **PDF retrieval** of every cited theorem via `curl + pdftotext`
2. **Verbatim quote** with page or equation number
3. **Embed** the verbatim quote in the deliverable (audit log, theorem registry, footnote)
4. **Cross-check** arXiv ID + paper title + symmetry-class — these are the failure modes
5. **Single confidence aggregation rule** stated at top of any deliverable, never switched mid-document
6. **Adversarial reviewer pass** before any "PASS" verdict

This protocol caught **15 misattributions in this session** — 12 in research artifacts and 3 in my own dispatch briefs (R3 phantom Cohen-Friedlander, SP-1a-β wrong RH bound on `Σ|D|`, SP-1a-α.1 phantom ABT 2014). Without it the session would have shipped 15 confident wrong claims.

## Drop / defer

- TB-exact uncond via S4, C2, geometric, C1 Synthesis (E), B'-denom — all formally closed this session
- Theorem B level-aspect full uncond (honest 0.18-0.22 post audits)
- Paper C `K log K` arithmetic-surrogate (likely false)
- Force-unification posture (Posture B from PROGRAM_REORIENT)
- W2-prime / Koyama work not advancing Theorem B
- B'-denom Selberg-Beurling new exact route (F3 closed at 0.02)
- RH-on-ζ-only path to B+ (SP-1a-β closed at 0.20)
- ABT 2014 specialization (SP-1a-α.1 closed; paper was phantom; ETK + large-sieve falls short √log N)

## Suggested next moves (research-progress focus, no paper drafting)

| | Cost | Description |
|---|---|---|
| **(MERTENS-LB) literature audit** | Opus extra-high, ~1 day | Does any literature address one-sided Möbius-harmonic Mertens sum bounds? Pólya-analog status, partial results, computational reach |
| **(MERTENS-LB) computational sweep** | Opus extra-high, 1-3 days | Extend empirical verification to N = 10^9. If holds → strengthens; if fails → Pólya-style breakthrough |
| **SP-1a-β-α (GRH-on-Dirichlet-L route)** | Opus extra-high, 4-8 weeks | Closes Wall 3 (SP-1) of B+ conditional on GRH for L(s, χ_b); does NOT close Wall 2 |
| **BCL 2024 q-averaged → fixed-level transfer probe** | Opus extra-high, 3-6 weeks | Would unlock TB-exact uncond. Specialized literature attack. |
| **Open 7.2' axis-pole multiplicities for higher-rank cross-Selberg** | Opus extra-high, ~1-2 days | Δ-machine extension surfaced by F2 |
| **Aristotle Mathlib prereqs** (uniform Stirling on strips + Titchmarsh `1/ζ` polynomial growth) | Aristotle dispatcher | needs tighter signature design first to avoid vacuous-witness pattern |

## Conventions (now permanent)

- **Mandatory citation protocol** above
- **Computation guides; analytical proof required.** Exact-rational arithmetic where load-bearing
- **Don't switch families** mid-attack — Theorem B work stays on weight-aspect Petersson family `F_k = S_k*(N)` squarefree N, k → ∞ along k = T^a, 1 < a < 2
- **Cross-reference prior failures** (now 18 documented for TB-exact uncond + multi for B+) before any new attack
- **Prefer chunked Write/Edit calls** for any deliverable > 4,000 words — single Write of 30k+ words trips the stream watchdog (P3a's first attempt failed this way)
- **Stop naming specific paper-year-volume citations** in dispatch briefs unless personally PDF-verified — use framework names; let agents discover and verify

## Contact / async pipeline summary

| | |
|---|---|
| Anthropic Opus 4.7 | `ANTHROPIC_API_KEY` set in env |
| Aristotle (harmonic.fun) | wired in `~/.farey_api_keys`; `aristotlelib==1.0.1` venv at `/tmp/aristotle_venv/` |
| MIMO (Xiaomi MiMo) | wired in `~/.farey_api_keys`; wrapper `scripts/dispatch_mimo.sh` round-trip-tested 6/6; 5 chat models (mimo-v2-flash default) |
| To export keys before dispatch | `set -a; source ~/.farey_api_keys; set +a` |
