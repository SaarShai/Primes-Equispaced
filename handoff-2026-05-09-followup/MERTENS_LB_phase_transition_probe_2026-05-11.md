---
schema_version: 1
title: "MERTENS-LB phase-transition probe"
date: 2026-05-11
type: result
tier: working
confidence: 0.96
status: COMPUTATIONAL_PROBE
sources:
  - handoff-2026-05-09-followup/MERTENS_LB_disproof_INDEPENDENT_VERIFICATION.md
  - handoff-2026-05-09-followup/MERTENS_LB_asymptotic_scan.tsv
  - handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.py
tags: [mertens-lb, phase-transition, polya-analog, b-plus]
---

# MERTENS-LB phase-transition probe

## Claim-safe summary

The old shorthand "first sign change at 200-300K" is too coarse.  The
post-ceiling transition relevant to the R1/SP-2 empirical range starts almost
immediately after the old ceiling `N=99991`:

| event | first N | T(N) | M(N) |
|---|---:|---:|---:|
| `T(N)>0` after `99991` | `108004` | `0.122176549391` | `11` |
| `T(N)>10` | `111812` | `10.019001209178` | `32` |
| `T(N)>50` | `116845` | `50.237912069456` | `112` |
| `T(N)>100` | `297331` | `100.089838956123` | `167` |

So the real transition statement is:

> The old verification ceiling `99991` sits just before a persistent
> post-ceiling instability.  Small positive excursions begin at `108004`,
> while the first large `T(N)>100` cluster begins near `297331`.

## Key values

| N | T(N) | M(N) |
|---:|---:|---:|
| `99991` | `-49.336132328891` | `-49` |
| `108004` | `0.122176549391` | `11` |
| `116845` | `50.237912069456` | `112` |
| `121618` | `1.846995534415` | `54` |
| `200000` | `-28.915715580357` | `-1` |
| `286899` | `0.501104` | `71` |
| `300296` | `157.644569284191` | `237` |
| `320058` | `0.735945` | `67` |
| `342767` | `-133.575658403449` | `-208` |

The scan over `[99992,350000]` found `278` positive clusters.  The widest and
highest cluster in that window is:

```text
286899-320058, peak at 300296, T=157.644569284191, width=33160
```

## Mechanism indicated by the decomposition

The phase change is dominated by the very high-`q` / very small-`k` terms
`M(floor(N/k))/k`, especially the first few terms.  The low-`q` bands are
comparatively stable and negative.

| N | q<=10 | 11-100 | 101-1k | 1k-10k | 10k-100k | >100k | T(N) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `99991` | `-1.145` | `-4.257` | `-4.303` | `-6.792` | `-33.839` | `0.000` | `-49.336` |
| `108004` | `-1.145` | `-4.259` | `-4.371` | `-6.927` | `4.824` | `11.000` | `0.122` |
| `116845` | `-1.145` | `-4.257` | `-4.292` | `-6.989` | `-46.080` | `112.000` | `50.238` |
| `300296` | `-1.145` | `-4.258` | `-4.323` | `-3.730` | `-28.067` | `198.167` | `157.645` |
| `342767` | `-1.145` | `-4.257` | `-4.330` | `-4.915` | `2.072` | `-122.000` | `-133.576` |

For example:

```text
N=300296:
  M(N)       = 237
  M(N/2)/2   = -26.5
  M(N/3)/3   = -12.333333
  1 + sum_{k<=10} M(floor(N/k))/k = 176.913492
  full T(N)  = 157.644569
```

At `N=342767`, the same small-`k` subtotal turns negative because `M(N)=-208`
despite compensating positive `M(N/2)/2` and `M(N/3)/3`.

## Research implication

The phase transition is not a mysterious global drift of the whole harmonic
sum.  It is a threshold where the small-`k` Mertens terms become large enough
to overpower a stable negative background.  Any theoretical explanation
should start from the finite initial segment

```text
1 + M(N) + M(floor(N/2))/2 + ... + M(floor(N/K0))/K0
```

and then prove a uniform envelope for the remaining tail.  This is closer to a
smoothed Mertens-function sign-cluster problem than to the original B+
positivity question.

## Next theorem target

For fixed small `K0`, prove or test a decomposition of the form

```text
T(N) = 1 + sum_{k<=K0} M(floor(N/k))/k + R_K0(N),
```

where `R_K0(N)` has a sign-biased, slowly varying envelope on the
post-ceiling range.  The computational probe suggests `K0=10` already
captures the sign-driving spikes, but not all cluster boundaries.
