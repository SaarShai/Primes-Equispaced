---
schema_version: 1
title: "S1-E numerical zero-frequency diagnostics"
date: 2026-05-11
type: report
tier: working
status: AUDIT_ONLY
confidence: 0.38
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2D_NUMERICAL_DIAGNOSTICS.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv
  - koyama-shared/data/pari_authoritative_zeros.json
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_zero_frequency_diagnostics.py
tags: [ec-ndc, s1, explicit-formula, zeros, numerical-diagnostics]
---

# S1-E Numerical Zero-Frequency Diagnostics

status: `AUDIT_ONLY`

## Verdict

Do not promote. Existing data allow a product residual and an `S1` trace proxy
on the seven Agent 3 `K` values, but they do not isolate a zero-frequency
mechanism.

The `37a1` residual has a real-looking fit to some listed PARI zero
frequencies. The same signal appears in the reconstructed `S1` proxy. However,
this is still only seven `K` values, a three-parameter sinusoid per tested
frequency, and eight frequencies per curve. It is a weak numerical hint, not a
detection.

The `389a1` fits are not stable: moderate in-sample `R^2` becomes negative
leave-one-out skill.

No local zero data for `11a1` is present in
`koyama-shared/data/pari_authoritative_zeros.json`, so `11a1` is included only
in the residual/proxy series, not in the zero-frequency fits.

## Inputs Used

No historical outputs were modified. No new EC coefficients or zeros were
computed.

- product rows: Agent 3 raw CSV, `mode=all`, `alpha=0.75`
- `S1` proxy: reconstructed from saved AP cache as
  `sum_p W(p/K) a_p/p`
- zero frequencies: first 8 PARI imaginary parts for `37a1` and `389a1`
- grid: `K=1000,3000,10000,30000,100000,300000,1000000`

## Series Isolated

Product residual:

```text
R_P(K) = log P_E,W(K) + rank(E) log log K.
```

Trace proxy, using the H2/S1 central coefficient from the current packaging:

```text
R_S1(K) = sum_p W(p/K) a_p/p - (1/2 - rank(E)) log log K.
```

Bad-prime differences are constant on this grid because the bad primes are
inside the weight plateau for `K >= 1000`.

| curve | product residual range | product last step | `S1` adjusted range | `S1` last step |
|---|---:|---:|---:|---:|
| `11a1` | `0.0713258125404` | `0.0155925215169` | `0.0737458625012` | `0.0160572853388` |
| `37a1` | `0.126956959844` | `-0.0209992948753` | `0.128088430434` | `-0.0206283717983` |
| `389a1` | `0.206359093808` | `-0.117784807764` | `0.208139274952` | `-0.117324322745` |

The `S1` adjusted series closely tracks the product residual up to an almost
constant local-log correction, as expected from the H2 bookkeeping.

## Zero-Frequency Test

For each listed zero ordinate `gamma`, I fit

```text
y(log K) = b0 + b1 cos(gamma log K) + b2 sin(gamma log K)
```

against either `R_P` or `R_S1`. With `n=7`, this leaves only 4 residual degrees
of freedom. Leave-one-out skill is measured against a constant model; positive
is better than constant, negative is worse.

| curve | series | first zero `gamma` | first zero `R^2` | first zero LOO skill | best in-sample `gamma` | best in-sample `R^2` | best in-sample LOO skill |
|---|---|---:|---:|---:|---:|---:|---:|
| `37a1` | product residual | `5.00317001400666` | `0.719899187932` | `0.441811688405` | `15.6038578732043` | `0.823734951846` | `0.587452887018` |
| `37a1` | `S1` adjusted | `5.00317001400666` | `0.719017811474` | `0.426626233990` | `15.6038578732043` | `0.818434089203` | `0.573732124403` |
| `389a1` | product residual | `2.87609907126047` | `0.401679263606` | `-0.142960600774` | `9.63307880218491` | `0.603682326833` | `-0.236782868215` |
| `389a1` | `S1` adjusted | `2.87609907126047` | `0.392388048668` | `-0.162972152176` | `9.63307880218491` | `0.608788444643` | `-0.224979101550` |

Read:

- `37a1`: compatible with a zero-frequency oscillatory component, but not
  enough data to identify coefficients or distinguish true zeros from aliasing.
- `389a1`: no useful out-of-sample support for the zero-frequency model.
- Selecting the best of eight zero frequencies is post-hoc; the first-zero row
  is the cleaner predeclared check.

## Caveats

- Seven `K` points are sparse. This can flag possible oscillation, not prove it.
- A single zero-frequency fit has three parameters; testing eight frequencies
  per curve is multiple-comparison prone.
- The grid spans about `3.16` cycles for the first `389a1` zero and `5.50`
  cycles for the first `37a1` zero, with large phase jumps between adjacent
  `K` values. Aliasing risk is high.
- No dense log-`K` grid exists here, so there is no frequency-resolution test.
- These diagnostics do not decide the H2-B vs H2-C branch:
  `K^(i gamma)/log K` and persistent `K^(i gamma)` terms cannot be separated
  on this data.

## Exact Command

```bash
python3 handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_zero_frequency_diagnostics.py
```

## Source Hashes

- script SHA256: `5ba57c62676fedd3f294123e15079d7176f398bb8979e5a1ad4884c323e7c925`
- raw CSV SHA256: `3e0d3d504d78f6d0f807ba0677dc1e225d4075ec98b03b27d49b1a62bd6ddb9d`
- AP cache SHA256: `830c19a1bd5d134e83e662f65bfb2b3fce252fef1ed5d74234234bec14920132`
- PARI zero JSON SHA256: `88dfb6f3a0185f9477cd32365fc3bf72545aab4305b63990fa2ad2b1988ef909`
- Python: `3.9.6`

## Outputs

- `handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_residual_series.csv`
- `handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_zero_frequency_fits.csv`
- `handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_zero_frequency_summary.csv`
- `handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_run_metadata.csv`
- `handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_zero_frequency_diagnostics.py`

## Status Decision

`AUDIT_ONLY`: the numerics are compatible with an oscillatory zero-term story
for `37a1`, but too sparse and too post-hoc to promote any theorem mode. They
do not contradict the H2 synthesis warning that offcentral zero terms must be
derived, retained, or averaged.
