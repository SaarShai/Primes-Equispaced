---
schema_version: 1
title: "EC C2-prime Implementation"
date: 2026-05-11
type: compute-protocol
tier: working
status: DIAGNOSTIC_ONLY
confidence: 0.82
tags: [ec-ndc, smoothing, c2-prime, diagnostics]
---

# EC C2-prime Implementation

Status: `DIAGNOSTIC_ONLY`.

## Verdict

EC numerics remain diagnostic only. No numerical diagnostic promotes a theorem.

Implemented script support:

```text
--gate c2-prime
--iid-seed-start
--shared-seed-start
p_cv
p_pareto
```

in:

```text
handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py
```

This makes the fresh C2-prime block addressable without reusing the seen G3
seeds.

## Full C2-prime Command Shape

Do not run holdouts or larger `K` first. Full C2-prime is:

```bash
python3 handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py \
  --gate c2-prime \
  --iid-seed-start 512 --iid-seeds 512 \
  --shared-seed-start 128 --shared-seeds 128 \
  --force
```

The command above overwrites default stochastic output files only with
`--force`; for a clean archival run, pass fresh C2-prime-specific output paths.

## Gate

iid pass:

```text
old_pass_rate <= 0.01
primary_pass_rate <= 0.005
p_cv <= 0.01
p_pareto <= 0.01
```

shared pass:

```text
old_pass_rate <= 0.02
p_cv <= 0.02
p_pareto <= 0.02
```

`p_ratio` and additive `p_score` are report-only in C2-prime.

## Boundary

If C2-prime fails, pause EC numerics and return to H1/H2 theory.

If C2-prime passes, the next diagnostic is a residue classifier. Even
`RESIDUE_DOMINATED_DIAGNOSTIC` would only say the finite proxy is probably
seeing low H1 residues. Theorem promotion still requires source-closed H1 and
H2 for the same kernel `W`, analytic rank input, multiple-zero disposition,
and separate H3 before adding `zeta(2)/L(E,2)^r`.

