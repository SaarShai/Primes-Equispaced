---
schema_version: 1
title: "Dense S1 residual diagnostics"
date: 2026-05-11
type: report
tier: working
status: AUDIT_ONLY
confidence: 0.42
dependencies:
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv
  - koyama-shared/data/pari_authoritative_zeros.json
tags: [ec-ndc, s1, diagnostics, zeros, smoothing]
---

# Dense S1 Residual Diagnostics

Status: `AUDIT_ONLY`

## Verdict

No theorem decision. The dense log-grid gives useful pressure against a pure
"no zero-frequency structure" null, but it does **not** distinguish robustly
between persistent zero terms and `1/log K`-damped zero terms.

The cleanest positive hint is `37a1`, first zero: the damped model with a
`1/log K` baseline beats the constant model by `Delta BIC = -53.39` and has
mod-5 cross-validation skill `0.415`. For `389a1`, first zero also strongly
beats constant, but the persistent model has the best BIC among the tested
forms (`Delta BIC = -53.40`) while damped variants are close, not decisive.

## What Was Tested

Using the saved `a_p` table through `10^6`, I rebuilt

```text
S_1,W(K)=sum_p W(p/K)a_p/p
```

on 121 logarithmically spaced `K` values from `1000` to `1000000`, with the
same smoothstep `alpha=0.75` convention used in the prior Agent 3 proxy.

The adjusted trace proxy is

```text
R_S1(K)=S_1,W(K)-(1/2-rank(E))loglogK.
```

This coefficient is the prior sprint's working S1 proxy, not a promoted
theorem coefficient. The diagnostic therefore tests frequency shape only.

For curves with PARI zero ordinates in the local JSON (`37a1`, `389a1`), I fit
the first three zero frequencies against four models:

```text
constant
constant + persistent zero mode
constant + zero mode / log K
constant + 1/log K baseline + zero mode / log K
```

## Primary Results

| curve | zero | best tested model | best Delta BIC vs constant | best CV skill | read |
|---|---:|---|---:|---:|---|
| `37a1` | 1 | damped zero + `1/logK` | `-53.385` | `0.415` | strongest support for damping-compatible residual |
| `37a1` | 2 | damped zero + `1/logK` | `-10.441` | `0.183` | weak secondary support |
| `389a1` | 1 | persistent zero | `-53.400` | `0.402` | zero-frequency structure, damping not isolated |
| `389a1` | 2 | damped zero | `-28.808` | `0.267` | damping-compatible but not decisive |

For a damped model, the implied oscillatory amplitude ratio from `K=1000` to
`K=1000000` is exactly `0.5`, because `log(1000000)=2log(1000)` on this grid.

## Interpretation

These data support continuing the theorem route: zero-frequency residuals are
visible enough that the explicit-formula mechanism is not numerically empty.
They do not promote the desired asymptotic. The 389a1 first-zero row is the
main warning: a persistent model can fit the same finite range at least as well
as a damped model.

The right next numerical test, if needed, is not broader parameter search. It
is a longer `K` range or a kernel family test with a predeclared first-zero
frequency and a predeclared damping exponent.

## Do Not Promote Unless

- the analytic proof closes branch continuation and zero-summability;
- the central coefficient is replaced by the final theorem coefficient;
- symmetric-square, `M_good`, bad-prime constants, and H1 compatibility are
  included before any product statement;
- persistent zero terms are either analytically ruled lower-order, explicitly
  retained, or averaged away;
- this diagnostic is cited only as `AUDIT_ONLY` finite evidence.

## Commands

```bash
python3 handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py
python3 -m py_compile handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py
shasum -a 256 handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_model_comparison.csv handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_grid.csv
```

## Outputs

- `DENSE_S1_residual_diagnostics.py`
- `DENSE_S1_residual_grid.csv`
- `DENSE_S1_model_comparison.csv`
- `DENSE_S1_metadata.csv`

## Hashes

- script: `24995bb174c376f43dd2d55765c56052ec1015070d4d941e974dd52fef26b439`
- comparison CSV: `f2ed4140642567bc25eda2f8ad87892ee6b85a2582e82abf2304c097327bc04c`
- residual grid CSV: `cc03e731cec758fb6117b9eec70e305f6418c5beefbcab12a5df7f013fb44594`

## Changed Files

- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_grid.csv`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_model_comparison.csv`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_metadata.csv`
