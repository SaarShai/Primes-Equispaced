---
schema_version: 2
title: Farey Claim Ledger
type: fact
domain: project
tier: semantic
confidence: 0.9
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/state-docs/CLAIM_STATUS.md.txt
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
  - projects/farey-research/data/W2_PRIME_FIT.json
  - projects/farey-research/recent-results-review.md
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

## Falsified Or Retracted

- Pointwise universal `E[C1^2] ~= 1/zeta(2)` is dead.
- Delta first-zero half-value framing is dead; corrected value is about `0.004` at `K = 10^4`.
- General W1 soft universality across all forms is false as stated; Delta may still tend to 1.
- Raw Koyama proportionality `E[C1^2] proportional to L(Sym^2 f,k)/<f,f>` is falsified by direction for 37a1 vs 389a1.
- Simple Gamma/Deligne normalization of the raw Sym2/Petersson ratio is not currently supported; recent review found no simple collapse to the observed `E[C1^2]` scale.
- Pure-rank W2 is superseded; conductor-control data require a log-conductor term or stronger formulation.
- Chebyshev sign theorem was disproved at `p = 243799`.
- Turan A2 was retracted to an open conjecture; fabricated citation risk is recorded.

## Open Claims

- W2 prime mechanism: explain the rank/control and `log(N)` structure in off-central second moments. Recent review supports keeping the `log(N)` term live; omitted rank/conductor bias alone probably does not explain the full coefficient, but this remains heuristic until recomputed.
- Delta limit: prove, disprove, or weaken `E[C1^2(Delta,rho)] -> 1`.
- Deligne-completed Sym2 correction: still possible only with a more specific formula; simple Gamma-period fixes failed the review gate.
- Dominance of -1: blocked until Koyama gives the exact modulus/residue/dynamic definition; the latest reply says dynamic `x` behavior matters and the 13 trillion baseline is not enough.
- Pair correlation of off-central modular zeros: compute normalized spacings and compare to GOE/GSE/GUE.
- Paper C arithmetic surrogate theorem: do not use as theorem language; recent review says the proposed cuspidal-form `K log K`-type asymptotic is likely wrong and should be reformulated as density/proportion/mollifier work.

## Supersession Rules

Use this ledger before drafting papers, correspondence, or queue tasks. If a new result changes a claim, update this page, the specific project page, and `log.md`; keep the raw evidence in `raw/farey-archive/`.
