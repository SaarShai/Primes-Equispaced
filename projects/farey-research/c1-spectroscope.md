---
schema_version: 2
title: C1 Spectroscope
type: project
domain: project
tier: semantic
confidence: 0.95
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - projects/farey-research/data/PHASE1_500ZEROS_CORRECTED.json
  - projects/farey-research/data/PHASE1_EC_RECOMPUTE.json
  - projects/farey-research/scripts/phase1_ec_recompute.py
  - projects/farey-research/results/PHASE1_RECOMPUTE_SUMMARY.md.txt
supersedes: []
superseded-by: 
tags: [farey, c1, spectroscope, bugfix]
---

# C1 Spectroscope

## Definition

`C1(f,rho) = |c_K(rho,f)| * |L'(rho,f)| / (log K + gamma_Euler)`.

`c_K(rho,f) = sum_{n <= K} mu_f(n) * exp(-n/K) * n^{-rho}`.

Default numerical setting is `K = 10^4`, averaged over off-central zeros.

## Normalization Rules

- Weight-2 EC: use arithmetic line `rho = 1 + i gamma`.
- Delta weight-12: use arithmetic center `rho = 6 + i gamma`.
- Denominator is `log(K) + gamma_Euler`.
- `mu_f(p^2) = p^{k-1}` for good primes.
- For EC weight 2, `mu_E(p^2) = p`; for Delta, `mu_Delta(p^2) = p^11`.

## Canonical Working Files

- `projects/farey-research/scripts/phase1_ec_recompute.py`
- `projects/farey-research/scripts/phase1_delta_500zeros.py`
- `projects/farey-research/scripts/rank3_5077a1.py`
- `projects/farey-research/scripts/within_class_rank0.py`
- `projects/farey-research/scripts/conductor_control_test.py`
- `projects/farey-research/data/PHASE1_EC_RECOMPUTE.json`
- `projects/farey-research/data/PHASE1_500ZEROS_CORRECTED.json`
- `projects/farey-research/data/RANK3_5077A1.json`
- `projects/farey-research/data/RANK0_CLUSTER.json`
- `projects/farey-research/data/CONDUCTOR_CONTROL_37b.json`

## Do Not Repeat

- Do not use Hecke `a_{p^2}` as `mu_f(p^2)`.
- Do not combine arithmetic coefficients with analytic `rho = 1/2 + i gamma`.
- Do not use `phase1_500zeros.py` EC section unless reverified; Delta part is the trusted use case.
- Do not promote model-written proof claims without numerical or citation verification.
