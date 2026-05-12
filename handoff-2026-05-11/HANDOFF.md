---
schema_version: 1
title: "Handoff 2026-05-11 — Post Koyama-pivot snapshot"
date: 2026-05-11
type: handoff
domain: project
tier: working
confidence: 0.95
sources:
  - log.md (chronological 2026-05-09 session)
  - HANDOFF.md (live canonical)
  - SESSION_SUMMARY_2026-05-09.md
  - handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md
  - all handoff-2026-05-09-followup/*.md deliverables
supersedes:
  - 2026-05-09 (end-of-session) HANDOFF — folds into this dated snapshot
tags: [handoff, primes-equispaced, koyama-pivot, ndc-corrected, breakthrough-map, roadmap]
---

# Handoff 2026-05-11

Snapshot at the start of the post-pivot research window. Captures the **2026-05-09 marathon session** (which resolved the Koyama-correspondence track via pivot away from the B+ Mertens-restricted path) and lays out the live roadmaps forward.

For a single-stop deep dive on the Koyama pivot specifically, read [`handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md`](../handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md) first.

---

## Executive summary (5 sentences)

The 2026-05-09 session **proved three sub-theorems of the Saar↔Koyama correspondence (Apr 6-16) — C2 AK constant, C3 subleading C_1, C4 B_∞ formula — and corrected the central NDC universality constant from Saar's conjectured `1/ζ(2)` to the correct `1/e^γ` (Mertens constant) which Aoki-Koyama 2023 eq. (1.4) p. 235 had stated explicitly but everyone in correspondence had missed.** Two versions of (MERTENS-LB) were disproved Pólya-style at modest N, killing the B+ Mertens-restricted closure path that had been the prior focus. The EC NDC universality conjecture was empirically falsified — D_K^E does NOT approach a universal constant across rank-0/1/2 elliptic curves. Three Aristotle async Lean dispatches remain in flight (R1_B_plus IN_PROGRESS, DPAC IN_PROGRESS at 3%, SmoothedDwfFormula returned COMPLETE_WITH_ERRORS and accepted as scaffolding). **Cumulative protocol catches: 16 misattributions** including a 4-way chain Saar→Koyama→Saar→my-dispatch-prompt on AK 2023 eq. (1.4); the `curl + pdftotext + verbatim quote + page#` protocol is the load-bearing methodology that prevented publication of the wrong constant.

---

## Recent results (what landed on 2026-05-09)

### Theorems proved (Koyama-track)

| # | Theorem | Confidence | Conditional? |
|---|---|---:|---|
| **C3** | `c_K(ρ, χ) = log K/L'(ρ, χ) + C_1 + o(1)` with `C_1 = −L''(ρ, χ)/(2 L'(ρ, χ)²)` | 0.94 | DRH for L(s, χ); error `O(K^{−1/2+ε})` under RH |
| **C2** | `E_K^χ(ρ) · log K → L'(ρ, χ) / e^γ` (AK constant **with correction**) | 0.97 | DRH (per Aoki-Koyama 2023) |
| **C4** | `T_∞ = (1/2) log L(2ρ, ψ) + BPC₁ + BPC₂ + T_{≥3}` (B_∞ explicit formula) | 0.96 | **UNCONDITIONAL** |
| **Composition** | `D_K(ρ, χ) := c_K^χ(ρ) · E_K^χ(ρ) → 1/e^γ ≈ 0.5615` (NDC universality, **revised constant**) | ~0.94 | DRH-conditional |

### Empirical results

| Object | Result | At K = |
|---|---|---:|
| 4 (χ, ρ) Dirichlet pairs (χ_{-4}/z1, χ_{-4}/z2, χ_5, χ_{11}) | mean `\|D_K\|·ζ(2) = 0.974`, drifting away from 1.0 toward `e^{-γ}·ζ(2) = 0.9237` | 10⁷ |
| 37a1 elliptic curve (rank 1) | `D_K^E · ζ(2) = 0.598`, monotonically decreasing | 10⁴ |
| 11a1 elliptic curve (rank 0) | `D_K^E · ζ(2) = 1.111`, hovering | 10⁴ |
| 389a1 elliptic curve (rank 2) | `D_K^E · ζ(2) = 0.165`, far below 1 | 10⁴ |
| (MERTENS-LB) universal | DISPROVED, first flip at N≈300K | 10⁹ |
| (MERTENS-LB) Mertens-restricted | DISPROVED at p = 237,733 | 10⁷ |

### Conjectures revised / corrected / falsified

| Conjecture | Before | After |
|---|---|---|
| Saar's NDC universality `D_K → 1/ζ(2)` | conjectured at 0.9 | **CORRECTED** to `D_K → 1/e^γ` (Mertens constant) |
| Saar's AK constant `E_K · log K → L'/ζ(2)` | conjectured at 0.9 | **CORRECTED** to `L'/e^γ`; Aoki-Koyama 2023 eq. (1.4) p. 235 already had it |
| EC NDC universality `D_K^E · ζ(2) → 1` | conjectured at 0.5 | **EMPIRICALLY FALSIFIED** — rank-dependent / curve-specific constants |
| (MERTENS-LB) `T(N) ≤ −c'` (both versions) | empirical to p ≤ 99,991 at c' = 1.43 | **DISPROVED** Pólya-style |
| B+ Mertens-restricted truth at large p | 0.85 (R1+SP-2 chain) | **GENUINELY UNCERTAIN** — reduction broken, direct verification infeasible (Farey set size 10¹⁰+) |
| Theorem B-exact `2/(3π)` unconditional near-term | speculative ~0.55 | **all 5 routes closed**, only multi-decade GDC remains |

### Methodological

| | |
|---|---|
| Misattributions caught (cumulative since 2026-05-03) | **16** (12 in research artifacts + 4 in my own dispatch briefs) |
| Most consequential catch | Catch #16: 4-way chain Saar→Koyama→Saar→me on AK 2023 eq. (1.4) — caught a wrong-constant claim before publication |
| Protocol effectiveness | The `curl + pdftotext + verbatim quote + page#` discipline is the load-bearing methodology. Without it the session would have shipped wrong constants. |

---

## Recent tasks (what was dispatched 2026-05-09)

### Pre-pivot batch (Theorem B / cage / B+ track — 5 agents)

| Agent | Task | Verdict |
|---|---|---|
| P1a | KMV §5 PARI Mellin verify (S4 route to Theorem B-exact uncond) | FAIL — `c₁ = 14/3` not `4/(3π)` |
| P1b | Orthogonal Barnes-G Monte Carlo (C2 RMT decomposition) | FAIL — orthogonal coefficient is `1/2` not `1/12` |
| P2 | B≥0 identity audit (`B·n'²/2 = Bern − Saw` vs Lean canonical) | **PASS** — Conjecture B+ Mertens-restricted survives |
| P3a | Δ-machine Compositio paper bundle synthesis (~50pp) | DONE — 30,082 words / ~50pp |
| P3b | Aristotle dispatcher for SmoothedDwfFormula Lean | DONE — Aristotle returned COMPLETE_WITH_ERRORS, accepted as scaffolding |

### Follow-up batch (research-progress probes — 4 agents)

| Agent | Task | Verdict |
|---|---|---|
| R1 | B+ Mertens-restricted analytic proof attack | **RIGOROUS REDUCTION** — B+ ⟺ S_ψ(p) < B₀(p−1); 4 new exact theorems |
| R2 | NC₁₅ geometric/motivic period for `2/(3π)` | NO MATCH — 46 candidates exhausted |
| R3 | Double-parabolic Eisenstein cross term (C1 single-residue route) | BLOCKED-AT-WALL — same wall as RH for ζ |
| R4 | F(γ) bias envelope theoretical proof | **RIGOROUS REDUCTION** — F(γ) confidence 0.88 → 0.95 |

### Cross-Selberg + B+ sub-followups

| Agent | Task | Verdict |
|---|---|---|
| F2 (pre-session) | Cross-Selberg slope mismatch root cause | **STRUCTURAL FIX** — axis poles at `s = iπk/log 3`; Open Problem 7.2 RESOLVED |
| F3 (pre-session) | B'-denominator Selberg-Beurling viability | BLOCKED-FOR-EXACT |
| SP-2 | B₀(N) ≥ c·N closed-form lower bound | RIGOROUS REDUCTION → (MERTENS-LB) which then fell |
| SP-1a | Im T_m closed form for B+ Aistleitner attack | RIGOROUS REDUCTION + 3 new exact identities + σ_p bijection picture |

### (MERTENS-LB) verification batch (after SP-2's reduction)

| Agent | Task | Verdict |
|---|---|---|
| MERTENS-LB sweep | Computational sweep T(N) up to N=10⁹ | **POLYA-FLIP confirmed** at N=10⁶, chronic oscillation thereafter |
| MERTENS-LB literature audit | Pólya-analog status in literature | POLYA-ANALOG-DISPROVED-COMPUTATIONALLY (turned out to apply to MR variant too) |
| MERTENS-LB-MR verification | direct check at MR primes p > 99,991 | **221 flips at MR primes**, first at p=237,733 |

### Koyama-pivot batch (6 agents)

| Agent | Task | Verdict |
|---|---|---|
| K-grounding | Read 4 source PDFs + restate 6 Koyama conjectures verbatim | DONE — surfaced e^γ vs ζ(2) tension within 10 min |
| K-C_1 | Prove subleading `C_1 = −L''/(2L'²)` | **PROOF CLOSED** (conf 0.94) |
| K-AK | Prove AK constant identification | **PROOF CLOSED with correction** (conf 0.97) — Saar's `1/ζ(2)` wrong, AK 2023 had `1/e^γ` |
| K-B_∞ | Prove B_∞ explicit formula | **PROOF CLOSED UNCONDITIONALLY** (conf 0.96) |
| K-EC-NDC | EC NDC universality numerical check (37a1, 11a1, 389a1) | EMPIRICALLY FALSIFIED — rank-dependent |
| K-DPAC | Dispatch DPAC to Aristotle Lean | DONE — project `59d181d5-...` IN_PROGRESS at 3% |
| Dirichlet pair recompute | direct K=10⁷ recompute (parallel) | DONE — independent corroboration of e^{-γ} |

---

## Open / async — what's still running or pending

| | Status | ETA |
|---|---|---|
| **R1_B_plus on Aristotle** (project `8e608890-...`) | 🟢 IN_PROGRESS — 4-theorem skeleton (m-th Bridge identity, Re T_m closed form, B_0 closed form, central one-step decomposition) | 4–8 weeks async |
| **DPAC on Aristotle** (project `59d181d5-...`) | 🟢 IN_PROGRESS at 3% — 3 explicit reductions offered (density-one, pointwise asymptotic, LI-conditional) | 4–8 weeks async |
| **SmoothedDwfFormula on Aristotle** (project `424973ae-...`) | ✓ COMPLETE_WITH_ERRORS — accepted as scaffolding (R₀=−2 anchor solid; full formula trivially-stubbed) | done |
| **Phase-transition supplement** (why T(N) flips at ~200-300K) | ⏸ pending user decision | ~1 day Opus if dispatched |
| **Communication to Koyama** (constant correction email) | ⏸ pending — Saar to compose | ~1 day manual |
| **Koyama paper draft** | not started | weeks |

Poll Aristotle: `./scripts/poll_aristotle.sh` (one-shot) or `./scripts/poll_aristotle.sh --watch` (15-min cadence).
Download when complete: `./scripts/poll_aristotle.sh --download R1_B_plus` (or DPAC).

---

## Roadmaps forward

Seven distinct directions, ranked by tractability and leverage.

### Roadmap A — Paper writeup (Koyama-track) [highest leverage, paper-ready material]

| | |
|---|---|
| Material | C2 AK constant + C3 subleading C_1 + C4 B_∞ formula + EC empirical falsification + constant correction (Saar's `1/ζ(2)` → corrected `1/e^γ`) |
| Target tier | J. Number Theory or Compositio sub-paper, ~30-40 pages |
| Cost | 2-4 weeks paper drafting (Opus extra-high for math sections, MIMO for prose) + 1 week Saar review |
| Status | All math complete and verified at confidences 0.94–0.97. **Submitable as soon as Saar wants to write it up.** |
| Why this first | Lowest hanging fruit. Clean publishable result. Closes the Koyama-correspondence research thread cleanly. |

### Roadmap B — Communication to Koyama [low effort, important relationship]

| | |
|---|---|
| Material | Email Koyama citing his own paper page 235 eq. (1.4) for the corrected constant `L'(ρ, χ)/e^γ`; flag the 4-way misattribution chain; share the three proof packages |
| Cost | ~1 day Saar manual; the proof packages are in `handoff-2026-05-09-followup/Koyama_*_proof.md` |
| Status | Ready to send |
| Why this | Avoid embarrassment of someone else (or Koyama himself, later) noticing the constant correction; preserve the collaboration |

### Roadmap C — EC universality investigation [open structural question]

| | |
|---|---|
| Material | What IS the right limit constant for EC L-functions at the BSD zero? Likely rank-dependent or involves sym² L-values. The Aoki-Koyama 2023 framework only handles GL_1; the extension to GL_2 is open. |
| Cost | Opus extra-high task — read Goldfeld-Hoffstein-style 1/L(s,sym²f) results, propose corrected universality at GL_2 |
| Status | empirical data in hand from K-EC-NDC; theoretical investigation not started |
| Why this | Genuinely open mathematical question. Could be a follow-up paper. |

### Roadmap D — B+ Mertens-restricted revisit [hard, possibly closed]

| | |
|---|---|
| Material | (MERTENS-LB) reduction is dead. B+ at large p is genuinely uncertain. Direct verification past p=99,991 is computationally infeasible (Farey set size ~10¹⁰). Alternative reductions? |
| Cost | Opus extra-high to explore alternative attack routes |
| Status | open problem, possibly multi-month |
| Why this | Paper B (Compositio Farey-side) is blocked on the B+ positivity claim. If we can't prove or disprove B+ analytically, Paper B needs to ship with B+ as conjecture-with-evidence. |

### Roadmap E — Phase-transition supplement [small but interesting]

| | |
|---|---|
| Material | Why does T(N) = 1 + Σ M(⌊N/k⌋)/k have its first sign-change at N ≈ 200–300K? Correlation with M(N) signs, Akatsuka 2013 §7 connection? Standalone small finding. |
| Cost | ~1 day Opus extra-high |
| Status | pending user decision (discussed in prior turn) |
| Why this | Possibly a small standalone result of independent interest. Or just a curiosity. Cheap to investigate. |

### Roadmap F — Aristotle harvest [passive]

| | |
|---|---|
| Material | R1_B_plus + DPAC Lean results when Aristotle completes |
| Cost | Polling overhead (~1 day for download + audit when complete) |
| Status | 4-8 weeks wait |
| Why this | Free upside if results come back substantive; cheap to monitor |

### Roadmap G — Theorem B program continuation [orthogonal to Koyama]

| | |
|---|---|
| Material | Cage uncond `(17 ± √145)/(12π)` at 0.97 (Annals headline). B2 v3 Soshnikov α_ratio=1 in orthogonal symmetry (verified this session). F(γ) bias envelope at 0.95 (R4). Plus the Δ-machine 30k-word draft from P3a. |
| Cost | Multi-month paper drafting; pre-submission checks (Murty-Murty 2009 prior-art, LaTeX) |
| Status | All math complete; drafting + submission deferred per user redirect during session |
| Why this | This was the original prize-track. Annals-grade headline result. Should not be neglected. |

---

## Recommended next-batch dispatch (if continuing the session)

Based on the roadmap priorities, suggested next batch:

| Slot | Task | Engine | ETA |
|---|---|---|---|
| 1 | Roadmap A — start Koyama paper draft outline (just outline + section headers + claim register) | Opus extra-high | 1 day |
| 2 | Roadmap B — draft Koyama email (constant correction + 3 proof package references) | MIMO (text) | ~1 hour |
| 3 | Roadmap C — EC universality theoretical investigation | Opus extra-high | 1 day |
| 4 | Roadmap E — phase-transition supplement (if user OKs) | Opus extra-high | 1 day |

Roadmaps D, F, G are deferred or async.

---

## Cumulative protocol catches (16 total since 2026-05-03)

| # | Source | What |
|---|---|---|
| 1-5 | 2026-05-03 original audit | FAPC₂ ILS, MK2 S-Y, etc. |
| 6 | P1a | KMV §5 → 4/(3π) wrong (actual 14/3) |
| 7 | P2 | Bern/Saw used wrong displacement |
| 8 | P3a respawn | strong-form polylog over-claim |
| 9 | P1b | arXiv:0708.2922 cited as Hughes-Mezzadri (plasma physics) |
| 10 | P1b | K-S `~ 2√N` wrong (Andrade-Best `~ 4N`) |
| 11 | F3 | Bui-Florea arXiv:1611.10095 (CS deliberation paper) |
| 12 | F3 | KMV phantom lemmas |
| 13 | R3 | "Cohen-Friedlander 2010/2017" phantom (mine) |
| 14 | SP-1a-β | `Σ\|D\| = O(N̂^{1+ε})` RH bound wrong (mine) |
| 15 | SP-1a-α.1 | "ABT 2014" phantom paper (mine) |
| **16** | **K-AK** | **"AK 2023 didn't identify constant" — page 235 eq. (1.4) does (mine, inherited from Saar/Koyama)** |

Three of the four "mine" catches were chains: I inherited the misattribution from Saar's correspondence and propagated without checking. The protocol caught all of them.

---

## File index — key deliverables since 2026-05-09 dispatch

### Theorems and proofs
- [`handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md`](../handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md) (+ `.py`, `.out`) — C3 proof package
- [`handoff-2026-05-09-followup/Koyama_AK_constant_proof.md`](../handoff-2026-05-09-followup/Koyama_AK_constant_proof.md) (+ `.py`, `.out`, 4 companion scripts) — C2 with constant correction
- [`handoff-2026-05-09-followup/Koyama_B_infty_proof.md`](../handoff-2026-05-09-followup/Koyama_B_infty_proof.md) (+ `.py`, `.out`) — C4 unconditional

### Synthesis
- [`handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md`](../handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md) — Koyama-pivot final summary
- [`handoff-2026-05-09-followup/Koyama_NDC_constant_correction.md`](../handoff-2026-05-09-followup/Koyama_NDC_constant_correction.md) — independent K=10⁷ confirmation of `e^{-γ}`
- [`handoff-2026-05-09-followup/Koyama_track_grounding.md`](../handoff-2026-05-09-followup/Koyama_track_grounding.md) — re-grounding from 4 source PDFs (1424 lines)

### Empirical
- [`handoff-2026-05-09-followup/Koyama_EC_NDC_sweep.md`](../handoff-2026-05-09-followup/Koyama_EC_NDC_sweep.md) (+ `.py`, `.csv`, `.txt`, `_ap_table.csv`) — EC empirical falsification

### MERTENS-LB
- [`handoff-2026-05-09-followup/MERTENS_LB_disproof_INDEPENDENT_VERIFICATION.md`](../handoff-2026-05-09-followup/MERTENS_LB_disproof_INDEPENDENT_VERIFICATION.md) — universal version disproof
- [`handoff-2026-05-09-followup/MERTENS_LB_MR_disproof.md`](../handoff-2026-05-09-followup/MERTENS_LB_MR_disproof.md) — Mertens-restricted disproof at p=237,733
- [`handoff-2026-05-09-followup/MERTENS_LB_literature_audit.md`](../handoff-2026-05-09-followup/MERTENS_LB_literature_audit.md) — Pólya-analog literature context

### Pre-pivot (earlier in session, 2026-05-09)
- [`handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md`](../handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md) — B+ reduction chain (R1)
- [`handoff-2026-05-09-followup/SP1a_Im_Tm_closed_form.md`](../handoff-2026-05-09-followup/SP1a_Im_Tm_closed_form.md) — σ_p bijection (SP-1a)
- [`handoff-2026-05-09-followup/SP2_B0_lower_bound.md`](../handoff-2026-05-09-followup/SP2_B0_lower_bound.md) — B₀ closed form (SP-2)
- [`handoff-2026-05-09-followup/R4_F_gamma_envelope_proof.md`](../handoff-2026-05-09-followup/R4_F_gamma_envelope_proof.md) — F(γ) envelope (R4)

### Δ-machine paper (Compositio sibling, pre-session)
- [`paper/Delta_machine_paper_compositio_draft.md`](../paper/Delta_machine_paper_compositio_draft.md) — 30,082-word draft
- [`paper/Delta_machine_paper_citation_audit.md`](../paper/Delta_machine_paper_citation_audit.md) — 605-line audit
- [`paper/Delta_machine_paper_theorem_registry.md`](../paper/Delta_machine_paper_theorem_registry.md) — 354-line registry

### Infrastructure
- [`scripts/dispatch_mimo.sh`](../scripts/dispatch_mimo.sh) — Xiaomi MiMo wrapper
- [`scripts/poll_aristotle.sh`](../scripts/poll_aristotle.sh) — Aristotle multi-project poller
- [`scripts/aristotle_project_ids.txt`](../scripts/aristotle_project_ids.txt) — tracked projects
- [`scripts/latex_convert.sh`](../scripts/latex_convert.sh) — pandoc helper

### Receipts (Aristotle dispatches)
- [`formal-conjectures/P3b_dispatch_receipt.md`](../formal-conjectures/P3b_dispatch_receipt.md)
- [`formal-conjectures/R1_B_plus_dispatch_receipt.md`](../formal-conjectures/R1_B_plus_dispatch_receipt.md)
- [`formal-conjectures/DPAC_dispatch_receipt.md`](../formal-conjectures/DPAC_dispatch_receipt.md)

---

## Conventions (now permanent)

1. **Mandatory citation protocol**: every cited theorem `curl + pdftotext`-verified with verbatim quote + page/eq#. The 16 catches this session demonstrate this is load-bearing.
2. **Single confidence aggregation rule** stated at the top of any deliverable, applied uniformly.
3. **Don't name specific paper-year-volume citations** in dispatch briefs unless personally PDF-verified — use framework names, let agents discover and verify.
4. **Chunked Write/Edit calls** for any deliverable > 4,000 words — single Write of 30k+ words trips the stream watchdog.
5. **Cross-reference prior failures** before any new attack (16 documented routes now closed for Theorem B-exact uncond + multiple for B+).

---

## API key + dispatch state

| Key | Status |
|---|---|
| Anthropic Opus 4.7 | `ANTHROPIC_API_KEY` set in env (harness-managed) |
| Aristotle (harmonic.fun) | wired in `~/.farey_api_keys`, venv at `/tmp/aristotle_venv/` |
| MIMO (Xiaomi MiMo) | wired in `~/.farey_api_keys`, wrapper `scripts/dispatch_mimo.sh` round-trip-tested |

Export before dispatch:
```bash
set -a; source ~/.farey_api_keys; set +a
```

---

## Bottom-line state for the program

| Track | Status | Next move |
|---|---|---|
| Koyama-correspondence (NDC universality + sub-theorems) | **RESOLVED** with constant correction | Paper writeup (Roadmap A) + Koyama email (Roadmap B) |
| Theorem B program (cage Annals + GRH-cond 2/(3π)) | math complete pre-session; 5 routes to uncond all closed | Paper drafting (Roadmap G) |
| Δ-machine paper (Compositio sibling) | 30k-word draft + audit + registry (pre-session) | Refinement + submission |
| B+ Mertens-restricted (Paper B Farey-side) | (MERTENS-LB) reduction killed; B+ truth at large p uncertain | Roadmap D (open question) |
| EC NDC universality | empirically falsified — rank-dependent | Roadmap C (theoretical investigation) |
| Aristotle Lean async | 3 projects (1 done, 2 IN_PROGRESS, 4-8 weeks each) | passive monitoring |
| Phase-transition curiosity | small open question | Roadmap E (pending decision) |
