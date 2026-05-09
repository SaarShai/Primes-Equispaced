---
schema_version: 1
title: "Session Summary 2026-05-09"
date: 2026-05-09
type: session-summary
tier: working
confidence: 0.95
sources:
  - log.md
  - HANDOFF.md
  - handoff-2026-05-09-followup/*.md
  - paper/Delta_machine_paper_*.md
  - formal-conjectures/*_dispatch_receipt.md
tags: [session, breakthrough-map, mertens-lb, b+-conjecture, theorem-B-exact]
---

# Session Summary 2026-05-09

A ~5-hour multi-agent research session. 18+ Opus extra-high agents dispatched, 12 misattributions caught in research artifacts, 3 in my own dispatch briefs. Net effect: the program now has a sharply-defined map of what's possible vs what's blocked.

---

## Three-sentence executive summary

We made **significant clarification progress** — the map of Theorem B-exact and Conjecture B+ closure routes is now sharp, with all 5 near-term routes to TB-exact unconditional formally closed and B+ uncondtional reduced to two named open sub-problems via a new closed-form chain. **Two structurally-distinct walls remain**: the multi-decade GDC support-4 wall (TB-exact `2/(3π)`) and the Pólya-analog **(MERTENS-LB) inequality** (B+ Mertens-restricted, layer SP-2). The single highest-leverage near-term breakthrough is **(MERTENS-LB)** — a one-sided sign bound on the Möbius-harmonic Mertens sum `Σ_{k=1}^N M(⌊N/k⌋)/k`, a fresh angle surfaced by SP-2's new identity (C4) and not addressed by any prior literature.

---

## What still stands solid

| | Confidence |
|---|---:|
| Cage uncond `(17 ± √145)/(12π)` (Annals headline) | **0.97** |
| Cage center `17/(12π)`, half-width `√145/(12π)` algebraic identity (Lean-verified) | 0.99 |
| `2/(3π)` GRH-conditional | **0.85** |
| Conjecture B+ Mertens-restricted (empirical, holds at 4,600+ primes) | **0.85** |
| F(γ) bias envelope (R4): isolated zeros Theorem-grade, general Proposition-grade | **0.95** |
| B2 v3 Soshnikov `α_ratio = 1` (after orthogonal symmetry-independence verified) | **0.90** |
| MK3 universal Selberg-class kernel | 0.95 |
| Smoothed Δw_f explicit formula `R₀ = -2` | 0.96 |
| FAPC₂ squarefree extension, 14 of 16 ladder curves | 0.93 |
| Theorem 1 Petersson family obstruction | 0.96 |

---

## What's in our way (the open structural walls)

### Wall 1 — TB-exact unconditional `2/(3π)` (Annals-grade prize)

| | |
|---|---|
| Wall identity | Support-4 fixed-level density / Grand Density Conjecture for Petersson family `S_k*(N)` |
| Multi-decade-open per | M-N 2014's own statement (comparable to unconditional 4th-moment of `\|ζ'(ρ)\|⁴`) |
| Closed near-term routes | S4 KMV (P1a), C2 RMT decomp (P1b), geometric/motivic (R2), C1 Synthesis (E) (R3), B'-denom Selberg-Beurling (F3). **5 of 5 closed this session.** |
| Live attack candidates | BCL 2024 q-averaged → fixed-level transfer; family-averaged Plancherel-Sato-Tate residue pinning |
| Confidence "TB-exact uncond closes near-term" | **≤ 0.05** |

### Wall 2 — B+ Mertens-restricted unconditional, layer SP-2

| | |
|---|---|
| Wall identity | **(MERTENS-LB)**: `1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'` for all `N ≥ N_0`, with explicit `c' > 1` |
| Surfaced by | SP-2's new identity (C4), 2026-05-09 |
| Pólya-analog risk | shape resembles Pólya's `L(x) ≤ 0` — true for huge ranges, **disproved by Haselgrove 1958** at large N |
| Empirics | holds at all 4,600+ Mertens-restricted primes ≤ 99,991, minimum ratio 0.4383 at p=13 |
| Literature status | OPEN — no theorem provides one-sided sign bound on this Möbius-harmonic Mertens sum |
| GRH-conditional path | does NOT close MERTENS-LB |
| Confidence "(MERTENS-LB) provable in months" | open, ~0.30 estimate |
| Confidence "B+ closes analytically in 1–3 months" | dropped from R1's 0.55 to **0.20** |

### Wall 3 — B+ Mertens-restricted unconditional, layer SP-1

| | |
|---|---|
| Wall identity | sharp bound `\|S_ψ(p)\| ≤ C · N̂ · log(N̂)` with explicit `C < c_{SP-2} ≈ 0.05` |
| Best unconditional bound | `O(N̂ · √log N̂)` via large-sieve dual route (improvement over CS's `O(N̂^{3/2}/√log N̂)`); **`√log N` short** |
| Best GRH-conditional path | SP-1a-β-α via Selberg 1942 mollifier + GRH for L(s, χ_b), 4–8 weeks |
| Confidence "Wall 3 closes unconditionally" | likely BLOCKED at √log N gap |

---

## The single highest-leverage breakthrough nomination

### **(MERTENS-LB)** — sign bound on the Möbius-harmonic Mertens sum

> Prove: `1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'` for all `N ≥ N_0`, with explicit `c' > 1`.

**Why it's the right target:**

1. **Concrete and falsifiable** — single inequality on a single explicit Mertens-class sum
2. **Closes Wall 2 of B+ unconditional** directly
3. **The companion identity (C4) is brand new** — `1 + S(N) = Σ_{k=1}^N M(⌊N/k⌋)/k` from SP-2 isn't in any prior B+ literature; fresh angle
4. **Plausibly attackable** via: Lambert-series identities; Selberg's symmetry formula `Σ Λ(n)·M(N/n) = ...`; explicit-formula direct estimation; computational disproof at large N (Pólya-style — itself a major result if it lands)
5. **Once in hand may transfer to Wall 3** — both walls are about Mertens-class sums on Farey-related domains; a proof technique for MERTENS-LB might inspire `|S_ψ|` closure
6. **Near-term tractable** vs Wall 1's multi-decade GDC

### Backup nomination: BCL 2024 q-averaged → fixed-level transfer (would unlock Wall 1)

### Deepest possible: a unifying theorem connecting Petersson L-function densities to Mertens-function behavior via the Bridge identity `Σ_{f∈F_{p−1}} e^{2πipf} = M(p) + 2`

---

## Reduction chain after R1 + SP-1a + SP-2

The B+ chain is now in **pure rank-displacement form** with both sides closed-form rationals:

$$
\textbf{B}^+ \;\Longleftrightarrow\; S_\psi(p) < B_0(p-1) \quad\text{for primes with } M(p) \le -3
$$

where:

| | |
|---|---|
| `S_ψ(p)` | `= Σ_{f ∈ F_{p−1}} D(f)·(σ_p(f) − 1/2)` (R1 + SP-1a, σ_p bijection identity) |
| `B₀(N)` | `= 1/12 − (N̂/12)·(2 + S(N)) − (N̂/2)·‖δ‖²` (SP-2 closed form) |
| `S(N)` | `= Σ_{b=2}^N h(b)/b` with `h(b) = Π_{p\|b}(1 − p)` |
| `1 + S(N)` | `= Σ_{k=1}^N M(⌊N/k⌋)/k` ← **(C4) new Möbius-harmonic Mertens identity** |
| `D(f)` | `= rank(f) − N̂·f` (Lean canonical displacement) |
| `σ_p(a/b)` | `= (pa mod b)/b` (multiplication-by-p bijection on `F_{p−1}^∘`) |

10 new exact identities total (4 from R1, 3 from SP-1a, 3 from SP-2), all exact-rational verified, none in any prior B+ literature.

---

## All session deliverables (index)

### Verdict deliverables (handoff-2026-05-09-followup/)

| File | Verdict | What |
|---|---|---|
| [`S4_KMV_Mellin_verify.md`](handoff-2026-05-09-followup/S4_KMV_Mellin_verify.md) | **FAIL** (0.92) | KMV §5 leading is `14/3` not `4/(3π)`; S4 route dead |
| [`C2_orthogonal_MC_extended.md`](handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md) | **FAIL** (0.97) + 2 cite catches + B2 v3 lift | Orthogonal Barnes-G is `1/2` not `1/12` |
| [`B_geq_0_identity_audit_FINAL.md`](handoff-2026-05-09-followup/B_geq_0_identity_audit_FINAL.md) | **PASS** (0.97) | Identity buggy; B+ Mertens-restricted survives |
| [`R1_B_plus_proof_attempt.md`](handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md) | **RIGOROUS REDUCTION** (0.97) | 4 new exact theorems; B+ → SP-1 + SP-2 |
| [`R1_B_plus.lean`](handoff-2026-05-09-followup/R1_B_plus.lean) | Lean skeleton | dispatched to Aristotle (project `8e608890-...`) |
| [`R2_NC15_geometric_motivic_period.md`](handoff-2026-05-09-followup/R2_NC15_geometric_motivic_period.md) | **NO MATCH** (0.85) | 46 candidates, all algebraic-equivalents or no-match; `2/(3π)` is recipe-derived not motivic |
| [`R3_double_parabolic_Eisenstein_assessment.md`](handoff-2026-05-09-followup/R3_double_parabolic_Eisenstein_assessment.md) | **BLOCKED-AT-WALL** (≤0.10) | C1 single-residue route dead; same wall as RH-for-ζ; +catch #13 |
| [`R4_F_gamma_envelope_proof.md`](handoff-2026-05-09-followup/R4_F_gamma_envelope_proof.md) | **RIGOROUS REDUCTION** (0.95) | F(γ) bias envelope 0.88 → 0.95 |
| [`Cross_Selberg_slope_diagnosis.md`](handoff-2026-05-09-followup/Cross_Selberg_slope_diagnosis.md) | **STRUCTURAL FIX** (0.94) | Open Problem 7.2 resolved — axis poles at `iπk/log 3` |
| [`B_prime_denom_Selberg_Beurling_assessment.md`](handoff-2026-05-09-followup/B_prime_denom_Selberg_Beurling_assessment.md) | **BLOCKED-FOR-EXACT, VIABLE-FOR-LEAN-ONLY** (0.97) | B'-denom dead for new routes; +catches #11, #12 |
| [`SP1a_Im_Tm_closed_form.md`](handoff-2026-05-09-followup/SP1a_Im_Tm_closed_form.md) | **RIGOROUS REDUCTION** (0.99) | 3 new identities, σ_p bijection picture, CS bound structurally insufficient |
| [`SP1a_beta_RH_conditional_B_plus.md`](handoff-2026-05-09-followup/SP1a_beta_RH_conditional_B_plus.md) | **STRUCTURAL OBSTRUCTION** | RH-on-ζ-only path dead; +catch #14 (mine) |
| [`SP1a_alpha_1_ABT_2014_audit.md`](handoff-2026-05-09-followup/SP1a_alpha_1_ABT_2014_audit.md) | **BLOCKED-AT-ABT** (0.85) | ABT 2014 paper doesn't exist; ETK + large-sieve falls short √log N; +catch #15 (mine) |
| [`SP2_B0_lower_bound.md`](handoff-2026-05-09-followup/SP2_B0_lower_bound.md) | **RIGOROUS REDUCTION** (0.99 closed-form, 0.45 unconditional) | NEW closed form `B₀(N) = 1/12 − (N̂/12)(2 + S(N)) − (N̂/2)‖δ‖²` and Möbius-harmonic Mertens identity (C4); reduces to (MERTENS-LB) |

### Δ-machine paper

| File | Status |
|---|---|
| [`paper/Delta_machine_paper_compositio_draft.md`](paper/Delta_machine_paper_compositio_draft.md) | 30,082 words / ~50pp Compositio draft (10 §§ + 20 appendices) |
| [`paper/Delta_machine_paper_citation_audit.md`](paper/Delta_machine_paper_citation_audit.md) | 605-line GREEN/YELLOW/RED/WHITE classification |
| [`paper/Delta_machine_paper_theorem_registry.md`](paper/Delta_machine_paper_theorem_registry.md) | 354-line theorem-by-theorem confidence registry |
| [`paper/Delta_machine_paper_AUDIT_EDIT_LIST.md`](paper/Delta_machine_paper_AUDIT_EDIT_LIST.md) | F1 audit: 0 BLOCKING / 1 HIGH / 1 MEDIUM / 1 LOW |
| Draft cross-Selberg axis-pole fix applied | §5.6 + new §5.6.1 (former Open Problem 7.2 resolved) |
| Draft Hughes-Mezzadri citation fixed | replaced phantom arXiv:0708.2922 with verified CRS 2006 + Andrade-Best 2023 |

### Aristotle Lean dispatches (formal-conjectures/)

| File | Status |
|---|---|
| [`P3b_dispatch_receipt.md`](formal-conjectures/P3b_dispatch_receipt.md) | SmoothedDwfFormula project `424973ae-...` — COMPLETE_WITH_ERRORS (vacuous-witness pattern; 2 honest Mathlib gaps) |
| [`R1_B_plus_dispatch_receipt.md`](formal-conjectures/R1_B_plus_dispatch_receipt.md) | R1_B_plus project `8e608890-...` — IN_PROGRESS (algebraic identities, less vacuous-witness risk) |
| [`SmoothedDwfFormula_full.lean`](formal-conjectures/SmoothedDwfFormula_full.lean) | Aristotle output — accepted as scaffolding (option B); R₀ anchor solid, full formula trivially-stubbed |

### Infrastructure (scripts/)

| File | Purpose |
|---|---|
| [`dispatch_mimo.sh`](scripts/dispatch_mimo.sh) + [`.md`](scripts/dispatch_mimo.md) | Xiaomi MiMo OpenAI-compatible API wrapper, round-trip-tested |
| [`poll_aristotle.sh`](scripts/poll_aristotle.sh) | multi-project Aristotle status / download / watch helper |
| [`aristotle_project_ids.txt`](scripts/aristotle_project_ids.txt) | tracked projects: SmoothedDwfFormula, R1_B_plus |
| [`latex_convert.sh`](scripts/latex_convert.sh) | pandoc → LaTeX → PDF helper (deferred until pandoc installed) |

### Bundle corrigenda

| File | What it corrects |
|---|---|
| [`handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC_check_CORRIGENDUM.md`](handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC_check_CORRIGENDUM.md) | catches #9 (arXiv:0708.2922 plasma physics) and #10 (K-S `2√N` should be Andrade-Best `4N`) |

---

## Misattribution catches — the protocol works in both directions

**15 misattributions caught since 2026-05-03.** Pattern: `cite paper+theorem# with exponent/threshold not matching actual paper text`.

| # | Where | What |
|---|---|---|
| 1-5 | 2026-05-03 audit round | FAPC₂ ILS η<3/2 (actual η<1), MK2 S-Y 8th-moment (fabricated), MK2 CLL category error, MK2 IK Lemma 5.2 nonexistent, etc. |
| 6 | P1a (S4 KMV) | KMV §5 → 4/(3π) (actual: 14/3) |
| 7 | P2 (B≥0 audit) | Bern/Saw used `D = i/(n−1) − f` (Lean canonical: `rank − N̂·f`) |
| 8 | P3a respawn | strong-form polylog `O((log N)^{k−1})` over-claimed (correct: `O(√N (log N)^{k−1})`) |
| 9 | P1b (orthogonal MC) | arXiv:0708.2922 cited as Hughes-Mezzadri (actual: plasma physics, Speroni di Fenizio & Velikanov) |
| 10 | P1b | K-S `~ 2√N` (actual: Andrade-Best `~ 4N`) |
| 11 | F3 (B'-denom) | "Bui-Florea 2018, arXiv:1611.10095" (actual arXiv:1611.10095 = CS paper on online deliberation) |
| 12 | F3 | KMV 2002 "Lemma 1.4 / Lem 2.1 / Lem 2.4" — these lemmas don't exist in KMV §1 or §2 |
| 13 | R3 (Eisenstein) | **MY OWN PROMPT**: "Cohen-Friedlander 2010/2017 subconvexity" — paper doesn't exist |
| 14 | SP-1a-β | **MY OWN PROMPT**: `Σ\|D\| = O(N̂^{1+ε})` under RH (actual: `O(N̂^{5/4+ε/2})`) |
| 15 | SP-1a-α.1 | **MY OWN PROMPT**: "ABT 2014 Trans. AMS 366" — paper doesn't exist; closest real ABT papers are about lacunary sequences, structurally incompatible |

**The mandatory `curl + pdftotext + verbatim quote + page#` protocol is the load-bearing mitigation.** Without it, this session would have shipped 15 confident wrong claims. With it, all 15 were caught at dispatch time.

**Going forward** (lesson for prompt-writing): I will stop naming specific paper-year-volume citations in dispatch briefs unless I've personally PDF-verified them. Use general framework names ("Erdős-Turán-Koksma inequality", "Aistleitner-style discrepancy bounds") and let agents discover and verify the actual references.

---

## Confidence map — before vs after session

| Direction | Pre-session | Post-session |
|---|---:|---:|
| TB-exact uncond near-term routes | speculative ~0.55 | **0/5 routes survive; multi-decade GDC remains** |
| Cage uncond `(17 ± √145)/(12π)` | 0.97 | unchanged |
| `2/(3π)` GRH-conditional | 0.85 | unchanged |
| B+ Mertens-restricted truth | 0.40 (post 2026-05-03) | **0.85 restored** (P2) |
| B+ closes analytically in 1–3 months | R1's 0.55 | **0.20** (SP-2 found Pólya-analog) |
| F(γ) bias envelope | 0.88 | **0.95** (R4) |
| B2 v3 Soshnikov α_ratio=1 (orthogonal) | 0.86 with 0.04 gap | **0.90** (P1b byproduct) |
| `2/(3π)` is geometric/motivic | speculative | **0.15** (R2 falsified) |
| Adelic κ_∞ = 2/3 | 0.40 | **0.15** (R2 trigamma probe) |
| Higher-order polylog conjecture form | claimed `O((log N)^{k−1})` | corrected to `O(√N (log N)^{k−1})` Theorem |
| Bern/Saw refutation route | live, threatening | retracted |
| Cross-Selberg slope mismatch | open, 12-19% | **resolved as structural fix** (F2) |
| C1 single-residue closes TB-exact | speculative | **≤ 0.10** (R3) |
| B'-denom new route to TB-exact | speculative ~0.55 | **0.02** (F3) |
| C1 mechanism F(γ) | 0.88 | 0.95 |
| Misattribution catches (cumulative) | 5 (2026-05-03) | **15 total** |

---

## What's actually achievable now

| | |
|---|---|
| **Months** (deliverable today, not blocked) | (i) Cage uncond `(17 ± √145)/(12π)`; (ii) `2/(3π)` GRH-conditional; (iii) Δ-machine paper's 30k-word draft refinement; (iv) F(γ) bias envelope rigorous theorem; (v) cross-Selberg axis-pole fix in §5.6 (already applied); (vi) the 10 new exact identities from R1+SP-1a+SP-2 as a Theorem-grade reduction chain for B+; (vii) B+ as conjecture-with-strong-evidence at 0.85 |
| **1–2 years if (MERTENS-LB) lands** | B+ unconditional Theorem-grade (the load-bearing positivity claim) |
| **1–3 years if BCL 2024 transfer lands** | TB-exact unconditional `2/(3π)` (Annals headline) |
| **Multi-decade open** | GDC support-4; both walls of B+ if (MERTENS-LB) follows Pólya-style failure |

---

## Aristotle async pipeline

| Project | Status | Notes |
|---|---|---|
| `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad` SmoothedDwfFormula | COMPLETE_WITH_ERRORS | option B accepted: file is scaffolding; R₀ anchor solid; 2 Mathlib prereq gaps named (uniform Stirling, Titchmarsh `1/ζ` polynomial growth) |
| `8e608890-f0ba-4a89-bbb0-a63b5bcab697` R1_B_plus | IN_PROGRESS | 4 algebraic-identity theorems from R1; less vacuous-witness risk than P3b |

Poll: `./scripts/poll_aristotle.sh` (one-shot) or `./scripts/poll_aristotle.sh --watch` (15-min cadence).
