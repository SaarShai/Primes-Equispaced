---
schema_version: 5
title: "Primes-Equispaced Current Handoff (post 2026-05-10 continuation)"
type: handoff
domain: project
tier: working
confidence: 0.95
created: 2026-05-09
updated: 2026-05-10
verified: 2026-05-10
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

## Start here (post-Koyama decision memo + 2026-05-10 B+ correction)

→ [`handoff-2026-05-09-followup/B_plus_direct_counterexamples.md`](handoff-2026-05-09-followup/B_plus_direct_counterexamples.md) — **2026-05-10 correction:** Conjecture B+ Mertens-restricted is directly false. Lean-canonical `B(p)<0` at `p=237733` with `M(p)=-20`, and at `p=243799` with `M(p)=-3`.

→ [`handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md`](handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md) — several-hour Koyama follow-up sprint synthesis. Perron-leading remains `DEFER`; EC mixed residual diagnostics do not promote a normalization; Path B has a conductor-control queue; DPAC needs log-prime phase hypotheses.

→ [`handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md`](handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md) — claim-safe 2026-05-10 Koyama decision memo. Supersedes older unconditional promotion language: `D_K -> e^{-gamma}` is conditional until the Perron-leading theorem is dependency-closed.

→ [`handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md`](handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md) — May 9 Koyama-correspondence summary. Keep for sources and history, but apply the May 10 decision memo before drafting theorem claims.

→ [`SESSION_SUMMARY_2026-05-09.md`](SESSION_SUMMARY_2026-05-09.md) — mid-session summary covering the pre-Koyama work (Theorem B / cage / B+ Mertens-restricted / Δ-machine).

## One-paragraph state

The 5 near-term routes to **Theorem B-exact unconditional `2/(3π)`** are all formally closed (S4, C2, geometric/motivic, C1 Synthesis (E), B'-denom). Only the multi-decade Grand Density Conjecture support-4 wall remains. **Conjecture B+ Mertens-restricted is now directly falsified** in the Lean-canonical `crossTerm` definition: `B(237733) = -3.018492026640170e10` with `M(237733)=-20`, and `B(243799) = -9.190201299936827e9` with `M(243799)=-3`. R1 + SP-1a + SP-2 remain theorem-grade exact identities and reduce B+ to `S_ψ(p) < B₀(p−1)`, but that inequality is false at explicit Mertens-restricted primes. `(MERTENS-LB)` and `(MERTENS-LB-MR)` are both false; they are now negative results, not proof targets.

## Current breakthrough nominee

**No B+ positivity proof target remains.** The useful research target is now classification: characterize the sign clusters of Lean-canonical `B(p)` among primes with `M(p) <= -3`, and explain why `T(p-1)` and `B(p)` decouple (`p=243799` has `T(p-1)<0` but `B(p)<0`). The strongest positive track is the claim-safe Koyama GL(1) note: corrected AK constant under DRH/EDRH, local Perron residue, corrected `B_∞`, and `D_K -> e^{-gamma}` only as conditional on Perron-leading.

## Koyama-track results (claim-safe after 2026-05-10 review)

Pivoted from B+ Mertens-restricted track to Saar's correspondence with Koyama. The May 10 decision memo keeps the constant correction but downgrades promotion language where dependencies are not closed.

| # | Conjecture | Verdict | Conf |
|---|---|---|---:|
| C1 | NDC universality | **CONDITIONAL, REVISED**: `D_K -> e^{-gamma}` (not `1/zeta(2)`), pending dependency-closed Perron-leading | — |
| C2 | AK constant | **CONDITIONAL on AK/DRH**: `E_K * log K -> L'/e^gamma` from Aoki-Koyama 2023 (1.4), p.235; Catch #16 | 0.97 |
| C3 | Perron/C1 term | **LOCAL RESIDUE PROVED; GLOBAL ASYMPTOTIC DEFER**. Do not state `c_K = log K/L' + C_1 + o(1)` as closed. | — |
| C4 | `B_∞` explicit formula | **PROVED** only with `psi`, `BPC1`, `BPC2`, and `T_{>=3}` included | 0.96 |
| C5 | EC NDC universality | **FALSIFIED** for simple `D_K^E*zeta(2)->1`; no normalization promoted. Mixed residual diagnostics were implemented, but the available `a_p` table stops at `p=541` and the truncated ratios are worse than the current benchmark. | — |
| C6 | DPAC | **DOWNGRADED/DEFER**. Aristotle artifact is a two-sorry scaffold; LI bridge is unsafe without log-prime phase independence. | — |

**16 misattributions caught total** since 2026-05-03 (12 in research artifacts, 4 in my own dispatch briefs). The 4-way chain Saar→Koyama→Saar→me on AK 2023 eq. (1.4) was the most consequential — caught a 8% wrong-constant claim before publication.

## Three programs — current status

| Track | Status |
|---|---|
| **Paper A — Theorem B Annals headline** | Cage uncond `(17 ± √145)/(12π)` at 0.97 unchanged. B2 v3 Soshnikov α_ratio=1 lifted 0.86→0.90 by P1b orthogonal symmetry-independence verification. F(γ) bias envelope 0.88→0.95 (R4). 2/(3π) GRH-conditional 0.85; unconditional ≤0.05 (5 of 5 routes closed). |
| **Paper B — Compositio Farey side** | **Reframe as negative/identity paper.** Conjecture B+ Mertens-restricted is false (`p=237733`, `p=243799`). R1 + SP-1a + SP-2 identities remain valuable; the positivity theorem does not. |
| **Δ-machine paper — Compositio sibling** | **30,082-word draft + 605-line citation audit + 354-line theorem registry.** Strong-form polylog corrected to `O(√N (log N)^{k−1})` Theorem 2.3 (0.97). Cross-Selberg axis-pole structural fix landed (F2 — Open Problem 7.2 resolved). Bibliography corrected (CRS 2006 + Andrade-Best 2023 replacing wrong arXiv:0708.2922). Murty-Murty 2009 prior-art audit flagged as pre-submission requirement. |

## Aristotle async pipeline

| Project ID | Label | Status |
|---|---|---|
| `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad` | SmoothedDwfFormula | COMPLETE_WITH_ERRORS — accepted as scaffolding (option B); R₀ anchor solid; 2 Mathlib gaps named (uniform Stirling, Titchmarsh `1/ζ` polynomial growth) |
| `8e608890-f0ba-4a89-bbb0-a63b5bcab697` | R1_B_plus | IN_PROGRESS — 4 algebraic-identity theorems |
| `59d181d5-b207-4882-a5ba-0786ec51d361` | DPAC | COMPLETE_WITH_ERRORS — downloaded; useful scaffold, but `dpac_of_LI` and the main conjecture remain `sorry`/research-open |

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
- Conjecture B+ Mertens-restricted positivity itself — directly false at `p=237733` and `p=243799`

## Suggested next moves (research-progress focus, no paper drafting)

| | Cost | Description |
|---|---|---|
| **B+ counterexample cluster map** | local C sweep, ~1 day | Scan Mertens-restricted primes around 200K-1M for Lean-canonical `B(p)` sign, cluster structure, and relation to `T(p-1)` |
| **Koyama claim-safe short note** | 1-3 days | Use the new claim-safe outline; promote corrected `B_∞` and local Perron residue; state AK/NDC only under DRH/EDRH + Perron-leading; include EC negative result and the mixed-residual truncation caveat |
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
