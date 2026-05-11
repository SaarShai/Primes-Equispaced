---
schema_version: 2
title: Farey Claim Ledger
type: fact
domain: project
tier: semantic
confidence: 0.9
created: 2026-04-24
updated: 2026-05-10
verified: 2026-05-10
sources:
  - raw/farey-archive/state-docs/CLAIM_STATUS.md.txt
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
  - projects/farey-research/data/W2_PRIME_FIT.json
  - projects/farey-research/recent-results-review.md
  - handoff-2026-05-09-followup/B_plus_direct_counterexamples.md
  - handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md
  - handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_2026-05-10.md
  - formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md
  - koyama-shared/results/PATH_B_CONTROL_QUEUE_2026-05-10.md
supersedes:
  - raw/farey-archive/old-obsidian-wiki/Research/W2_Rank_Linear_Law.md.txt
superseded-by: 
tags: [farey, claims, ledger, supersession]
---

# Farey Claim Ledger

## Confirmed Or Strong

- Delta anchor: `E[C1^2] = 0.950231842` over 683 zeros at `K = 10^4`.
- 37a1 and 389a1 500-zero EC values: `2.189911545`, `3.113923728`.
- 5077a1 rank-3 anchor: `E[C1^2] = 4.617` over 500 zeros.
- Rank-0 EC cluster: mean `1.886`, CV `8.9%`, 200 zeros each.
- Rankin-Selberg identity check: `L(Sym^2 f,2)/<f,f> = 8*pi^3/N` verified to about 1% for 37a1 and 389a1.
- Four-term Farey decomposition and Farey spectroscope connection survive the C1 bugfix.
- Koyama GL(1): local Perron double-pole residue at a simple zero is proved as local algebra; corrected `B_infty` identity is proved when `psi`, `BPC1`, `BPC2`, and `T_{>=3}` are included.
- Koyama follow-up sprint: the exact missing GL(1) ingredient is now isolated as a shifted Perron nonlocal remainder lemma for `K^w/(w L(w+rho,chi))`.

## Falsified Or Retracted

- Pointwise universal `E[C1^2] ~= 1/zeta(2)` is dead.
- GL(1) NDC constant `1/zeta(2)` is superseded/falsified; the claim-safe replacement is conditional `e^{-gamma}`, not an unconditional theorem in current files.
- EC-NDC simple universality `D_K^E*zeta(2) -> 1` is falsified by the 37a1/11a1/389a1 sweep.
- EC-NDC mixed residual diagnostics do not currently promote a normalization: the implemented `D_mix_good_truncated` and `D_2_good_truncated` ratios are worse than the `1.42083` benchmark, and the available `a_p` table is truncated at `p=541`.
- DPAC from zeta-zero linear independence alone is unsafe as stated; it needs a strengthened log-prime/exponential phase-independence hypothesis.
- Delta first-zero half-value framing is dead; corrected value is about `0.004` at `K = 10^4`.
- General W1 soft universality across all forms is false as stated; Delta may still tend to 1.
- Raw Koyama proportionality `E[C1^2] proportional to L(Sym^2 f,k)/<f,f>` is falsified by direction for 37a1 vs 389a1.
- Simple Gamma/Deligne normalization of the raw Sym2/Petersson ratio is not currently supported; recent review found no simple collapse to the observed `E[C1^2]` scale.
- Pure-rank W2 is superseded; conductor-control data require a log-conductor term or stronger formulation.
- Chebyshev sign theorem was disproved at `p = 243799`.
- Conjecture B+ Mertens-restricted positivity is disproved in the Lean-canonical `crossTerm`: `B(237733) < 0` with `M(237733) = -20`, and `B(243799) < 0` with `M(243799) = -3`.
- Turan A2 was retracted to an open conjecture; fabricated citation risk is recorded.

## Open Claims

- W2 prime mechanism: explain the rank/control and `log(N)` structure in off-central second moments. Recent review supports keeping the `log(N)` term live; omitted rank/conductor bias alone probably does not explain the full coefficient, but this remains heuristic until recomputed.
- Delta limit: prove, disprove, or weaken `E[C1^2(Delta,rho)] -> 1`.
- Deligne-completed Sym2 correction: still possible only with a more specific formula; simple Gamma-period fixes failed the review gate.
- Dominance of -1: blocked until Koyama gives the exact modulus/residue/dynamic definition; the latest reply says dynamic `x` behavior matters and the 13 trillion baseline is not enough.
- Pair correlation of off-central modular zeros: compute normalized spacings and compare to GOE/GSE/GUE.
- Paper C arithmetic surrogate theorem: do not use as theorem language; recent review says the proposed cuspidal-form `K log K`-type asymptotic is likely wrong and should be reformulated as density/proportion/mollifier work.
- Koyama GL(1) Perron-leading theorem: close or cite `c_K(chi,rho) = log K/L'(rho,chi) + o(log K)` before any theorem-language use of `D_K -> e^{-gamma}`.
- EC-NDC mixed residual: extend the `a_p` table to actual `K=100000` products before deciding whether the truncated negative diagnostic survives complete data; current `L(2,E)^rank` normalization is numerical proxy only and not promoted.
- Path B conductor controls: run the B1 `350-650` and B2 `4500-5600` conductor-matched control queues before any rank-isolated sentence.
- DPAC hygiene: use explicit `LogPrimePhaseAvoidance`, `FiniteLogPrimePhaseIndependence`, or a cited `LogPrimePhaseTheorem`; keep density-one packaging as conditional counting only.

## Supersession Rules

Use this ledger before drafting papers, correspondence, or queue tasks. If a new result changes a claim, update this page, the specific project page, and `log.md`; keep the raw evidence in `raw/farey-archive/`.
