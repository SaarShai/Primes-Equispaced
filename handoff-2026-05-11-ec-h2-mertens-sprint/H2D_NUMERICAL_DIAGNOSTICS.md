---
schema_version: 1
title: "H2-D numerical slope diagnostics"
date: 2026-05-11
type: report
tier: working
status: AUDIT_ONLY
confidence: 0.62
sources:
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-h2-mertens-sprint/H2D_slope_diagnostics.py
tags: [ec-ndc, smoothing, h2, mertens, diagnostics]
---

# H2-D Numerical Slope Diagnostics

status: `AUDIT_ONLY`

## Verdict

Do not promote. The existing seven-point grid gives a decent all-grid slope
match for the P-smoothed `alpha=0.75` product, but the three-point tail fit does
not show settled stabilization.

For `all/cP_only/P_only, alpha=0.75`, the H2 product diagnostics are exactly the
same, because H2 uses only `P` and all three modes have the same smoothed `P`
column. This numerical check therefore cannot distinguish the full `all`
normalization from the `cP_only` or `P_only` ablations.

## Target

H2 predicts

```text
log P_E,W(K) = -rank(E) log log K + B_E,W + o(1).
```

I fit `log P` against `log log K`. A matching slope has
`slope_logP_vs_loglogK = -rank`. Equivalently,
`log P + rank log log K` should have slope `0` and should stabilize.

Windows:

- all grid: `K=1000,3000,10000,30000,100000,300000,1000000`
- tail grid: `K>=100000`, i.e. `100000,300000,1000000`

## Mode Collapse For H2

H2 only tests the `P` column. The eight Agent 3 modes therefore collapse into
two product families.

| family       | modes                            | representative | all max abs err | tail max abs err | tail max adj range |
| ------------ | -------------------------------- | -------------- | --------------- | ---------------- | ------------------ |
| P-smoothed   | all, cP_only, P_only, PL2_only   | all            | 0.0390010461279 | 0.260617667793   | 0.117784807764     |
| unsmoothed P | sharp, c_only, L2_only, cL2_only | sharp          | 0.247657402465  | 0.204273082179   | 0.185461395153     |

The full per-mode/per-alpha fits are in `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-h2-mertens-sprint/H2D_slope_fits.csv` and the
per-mode summaries are in `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-h2-mertens-sprint/H2D_slope_mode_summary.csv`.

## Key Fits: `all`, `alpha=0.75`

| curve | rank | all slope       | all slope error  | all adj range   | tail slope      | tail slope error | tail adj range  | tail last step   |
| ----- | ---- | --------------- | ---------------- | --------------- | --------------- | ---------------- | --------------- | ---------------- |
| 11a1  | 0    | 0.0385134090158 | 0.0385134090158  | 0.0713258125404 | 0.12630534927   | 0.12630534927    | 0.0230276201305 | 0.0155925215169  |
| 37a1  | 1    | -1.02388301209  | -0.0238830120918 | 0.126956959844  | -0.739382332207 | 0.260617667793   | 0.068521749083  | -0.0209992948753 |
| 389a1 | 2    | -1.96099895387  | 0.0390010461279  | 0.206359093808  | -2.15524958839  | -0.155249588389  | 0.117784807764  | -0.117784807764  |

Read:

- all-grid slopes are close to `-rank`: max absolute slope error
  `0.0390010461279`.
- tail-grid slopes are not close: max absolute slope error
  `0.260617667793`.
- the rank-2 curve `389a1` has tail adjusted last step
  `-0.117784807764`,
  so the last endpoint is still moving visibly.

## Tail Adjusted Values: `all`, `alpha=0.75`

Values are `log P + rank log log K`.

| curve | rank | K=100000       | K=300000       | K=1000000      | last step        |
| ----- | ---- | -------------- | -------------- | -------------- | ---------------- |
| 11a1  | 0    | -1.691651501   | -1.68421640239 | -1.66862388087 | 0.0155925215169  |
| 37a1  | 1    | -2.13464860905 | -2.06612685996 | -2.08712615484 | -0.0209992948753 |
| 389a1 | 2    | -1.74649582805 | -1.65700193164 | -1.77478673941 | -0.117784807764  |

## Alpha Sweep For P-Smoothed Modes

The table uses `P_only`, but the same H2 product rows apply to `all`,
`cP_only`, and `PL2_only` for the same alpha.

| alpha | all max abs err | all RMS err     | tail max abs err | tail RMS err   | tail max adj range |
| ----- | --------------- | --------------- | ---------------- | -------------- | ------------------ |
| 0     | 0.276367355322  | 0.175699980331  | 0.234937004489   | 0.136165060235 | 0.0428330789128    |
| 0.25  | 0.176856432558  | 0.107725589635  | 0.24121368506    | 0.143386014357 | 0.0602085236591    |
| 0.5   | 0.0874491538022 | 0.0647496562965 | 0.194688402244   | 0.153017830855 | 0.125193623724     |
| 0.65  | 0.0543141869409 | 0.0331951534381 | 0.292674188224   | 0.227304418451 | 0.145747426041     |
| 0.75  | 0.0390010461279 | 0.034519378807  | 0.260617667793   | 0.189716494376 | 0.117784807764     |
| 0.85  | 0.144353378976  | 0.100573165089  | 0.254001427908   | 0.152538696055 | 0.0760540210046    |
| 0.92  | 0.249417178017  | 0.154718388707  | 0.184410756267   | 0.137840586122 | 0.088476731621     |

The all-grid optimum by max slope error is `alpha=0.75`. Tail diagnostics do
not select the same story cleanly: every tested alpha has tail max absolute
slope error at least about `0.18`, and the tail has only three points.

## Agent 3 Gate Reference

Read from the existing metrics CSV. These are old `X` gate values, not H2 slope
tests.

| mode    | old gate | ratio         | max CV          |
| ------- | -------- | ------------- | --------------- |
| all     | True     | 1.347375493   | 0.0632974273344 |
| cP_only | True     | 1.34745361991 | 0.0633191733115 |
| P_only  | True     | 1.36905147988 | 0.0651620935228 |

The old gate pass for `all, alpha=0.75` remains numerically real. The H2 product
test shows that the product part alone is identical for the `all/cP_only/P_only`
comparison, so that old pass is not evidence that the `L2^rank` denominator is
load-bearing.

## Caveats

- The tail fit has only three K values. It can flag instability, but it cannot
  falsify an asymptotic statement.
- The largest endpoint, `K=1000000`, has high leverage on the tail slope.
- The current data are three curves only: ranks `0,1,2`, one curve each.
- No new EC products, `a_p` values, holdout curves, or dense K grids were
  computed here.

## Exact Command

```bash
python3 handoff-2026-05-11-ec-h2-mertens-sprint/H2D_slope_diagnostics.py --raw-csv handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv --metrics-csv handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv --summary-md handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md --out-dir handoff-2026-05-11-ec-h2-mertens-sprint
```

## Source Hashes

- raw CSV SHA256: `3e0d3d504d78f6d0f807ba0677dc1e225d4075ec98b03b27d49b1a62bd6ddb9d`
- metrics CSV SHA256: `719de44ab103119e2fe53e3e31f0193404fd199107a5260b47eb4a8f03904448`
- summary markdown SHA256: `089629bddb929d6cc3c5d5bf0a6154a58fcaf1e424e2f962e3c99933c0417d8b`
- Python: `3.9.6`

## Outputs

- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-h2-mertens-sprint/H2D_adjusted_values.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-h2-mertens-sprint/H2D_slope_fits.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-h2-mertens-sprint/H2D_slope_mode_summary.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-h2-mertens-sprint/H2D_NUMERICAL_DIAGNOSTICS.md`

## Status Decision

`AUDIT_ONLY`: this is a numerical audit of existing reproduction data. It gives
supporting all-grid diagnostics for `alpha=0.75`, but tail-grid diagnostics are
too sparse and too unsettled to promote H2 or to declare a numerical no-go.

