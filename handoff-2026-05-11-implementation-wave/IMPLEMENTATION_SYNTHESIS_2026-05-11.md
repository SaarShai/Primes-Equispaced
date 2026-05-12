---
schema_version: 1
title: "Implementation Wave Synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: IMPLEMENTED_NO_THEOREM_PROMOTED
confidence: 0.84
tags: [implementation-wave, h1, h2, gl1, theorem-b, delta, b-plus, ec-diagnostics]
---

# Implementation Wave Synthesis

Status: `IMPLEMENTED_NO_THEOREM_PROMOTED`.

No theorem is promoted.

## What Changed

This wave turns the completed GPT-5.5/xhigh plan into repo-local execution
artifacts:

- `H1_Q_GT_2_BAD_SET_ROUTE_2026-05-11.md`: replaces the first bad-set attack
  from the square `q=2,p=2` Palm statistic to the weaker `q>2,p<2` route.
- `H2_RIGHT_LIP_RENORMALIZED_ENDPOINT_2026-05-11.md`: makes the first H2
  theorem target right-lip-renormalized with full `R_S1^+` retained.
- `GL1_SHARP_PERRON_BOUNDARY_2026-05-11.md`: records the sharp-cutoff blocker
  and the separate smoothed/profile theorem mode.
- `THEOREM_B_SUPPORT4_BOUNDARY_2026-05-11.md`: keeps Theorem B exact as a
  support-4 fixed-level moonshot, not a near-term task.
- `BPLUS_TIER1B_EXECUTION_BOUNDARY_2026-05-11.md`: freezes B+ as finite
  sign-cluster classification, not positivity.
- `EC_C2_PRIME_IMPLEMENTATION_2026-05-11.md`: implements the C2-prime
  diagnostic boundary and records the new seed-offset script support.

Concrete code/edit changes:

- `EC_STOCHASTIC_NULLS_2026-05-11.py` now supports `--gate c2-prime`,
  `--iid-seed-start`, `--shared-seed-start`, `p_cv`, and `p_pareto`.
- `Delta_machine_paper_theorem_registry.md` and
  `Delta_machine_paper_compositio_draft.md` now include local ramified
  correction divisor bookkeeping as `Proposition 2.5b`, with stale slope
  mismatch language replaced.

## Research State

Main route:

```text
WeakSeparatedEC-BFMT-H1(E,c)
+ Degree2WeakShiftedNeg_q(E)
+ RootedInvProdCorr_p(E,A), p=q/(q-1)<2
=> R_E,1^simp(T)=o(T^2)
```

This is strictly better targeted than the older square Palm-first route.

H1 still needs multiple-zero disposition and finite-box contour hypotheses.
H2 is now best stated with retained/subtracted right-lip profile first. GL1
sharp remains blocked by actual moving-shell PV. B+ positivity is false.
EC numerics remain diagnostic only.

## Verification

Required verification after this edit wave:

```bash
python3 -m py_compile primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py
python3 primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py \
  --gate c2-prime --iid-seed-start 512 --iid-seeds 1 \
  --shared-seed-start 128 --shared-seeds 1 --max-k 1000 \
  --k-grid 1000 --force \
  --raw-csv /tmp/ec_c2prime_raw.csv \
  --metrics-csv /tmp/ec_c2prime_metrics.csv \
  --summary-csv /tmp/ec_c2prime_summary.csv \
  --report /tmp/ec_c2prime_report.md
```

Full C2-prime is not run here; the predeclared full run is the 512 iid and
128 shared fresh-seed block, which is intentionally a separate compute job.

