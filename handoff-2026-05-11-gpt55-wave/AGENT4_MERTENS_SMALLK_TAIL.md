# Agent 4: MERTENS-LB Small-k/Tail Lemma

Status: NO_GO

Confidence: 0.97 for dense finite envelopes through `N=1000000`; 0.93 for log-grid no-go through `N=1000000000`; 0.55 for the replacement `K0=200` gate.

Dependencies: local identity `T(N)=1+sum_{b<=N} h(b)/b` from `SP2_B0_lower_bound.md`; local `MERTENS_LB_sweep.py` Mobius/Mertens table; existing `MERTENS_LB_asymptotic_scan.tsv`. No new external theorem claim is used.

## Sources read

- `HANDOFF.md`
- `handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.md`
- `handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.py`
- `handoff-2026-05-09-followup/MERTENS_LB_disproof_INDEPENDENT_VERIFICATION.md`
- `handoff-2026-05-09-followup/MERTENS_LB_asymptotic_scan.tsv`
- `handoff-2026-05-09-followup/SP2_B0_lower_bound.md`

## Exact split

For fixed `K`,

`T(N)=1+sum_{k<=K} M(floor(N/k))/k + R_K(N)`.

The exact q-block tail is

`R_K(N)=sum_{q<=floor(N/(K+1))} M(q) * (H_floor(N/q) - H_max(K, floor(N/(q+1))))`.

Proof: partition integers `k>K` by `q=floor(N/k)`. The block is
`floor(N/(q+1))+1 <= k <= floor(N/q)`, truncated below by `K+1`.

This is the right proof target if a tail lemma is still desired. It exposes that fixed `K` leaves a low-q Mertens aggregate, not a harmless error term.

## Reproduction

Helper added:

`python3 handoff-2026-05-11-gpt55-wave/AGENT4_mertens_tail_probe.py --dense-max 1000000 --ks 5,10,20,50,100,200`

Log-grid no-go:

`python3 handoff-2026-05-11-gpt55-wave/AGENT4_mertens_tail_probe.py --dense-max 1000 --sample-max 1000000000 --ks 10,20,50,100,200`

Both runs returned `mertens_anchor_check=True`. Dense `T` was recomputed by the SP-2 prefix identity, not by the phase-probe block walker; anchors match the probe:

| N | T(N) | M(N) |
|---:|---:|---:|
| 99991 | -49.336132328892 | -49 |
| 108004 | 0.122176549391 | 11 |
| 116845 | 50.237912069456 | 112 |
| 297331 | 100.089838956122 | 167 |
| 300296 | 157.644569284190 | 237 |
| 342767 | -133.575658403447 | -208 |
| 1000000 | 139.629678512921 | 212 |

## Dense finite envelope

Exact dense range: every integer `N in [99992,1000000]`.

Thresholds after `99991`:

| threshold | first N | T(N) | M(N) |
|---:|---:|---:|---:|
| `T>0` | 108004 | 0.122176549391 | 11 |
| `T>10` | 111812 | 10.019001209177 | 32 |
| `T>50` | 116845 | 50.237912069456 | 112 |
| `T>100` | 297331 | 100.089838956122 | 167 |
| `T>200` | 992839 | 200.876501973527 | 304 |

Positive clusters in `[99992,350000]`: `278`. Widest/highest cluster:
`286899-320058`, peak `N=300296`, `T=157.644569284190`, width `33160`.

Tail ranges:

| dense range | K | min R_K | at N | max R_K | at N |
|---|---:|---:|---:|---:|---:|
| `[99992,350000]` | 10 | -22.681030 | 265743 | -7.025699 | 232367 |
| `[99992,350000]` | 50 | -14.852734 | 348521 | -11.087700 | 116089 |
| `[99992,1000000]` | 10 | -29.302073 | 684457 | -6.819153 | 975103 |
| `[99992,1000000]` | 50 | -19.154468 | 946660 | -11.087700 | 116089 |
| `[99992,1000000]` | 200 | -14.158482 | 941438 | -8.664532 | 122085 |

Finite lemma available:

`[99992,1000000]`: `-29.303 < R_10(N) < -6.819`.

This certifies the phase-probe claim in the post-ceiling window: the large positive spikes there are genuinely from the first ten Mertens terms.

## No-go beyond the finite window

Exact sample range: 94 log-spaced rows from `MERTENS_LB_asymptotic_scan.tsv` with `100000 <= N <= 1000000000`; fresh Mertens prefix built to `1000000000`.

| K | min R_K | at N | max R_K | at N | positive samples | first positive |
|---:|---:|---:|---:|---:|---:|---|
| 10 | -211.024524 | 901571137 | 136.787796 | 660693448 | 14 | `5069907`, `R_10=5.730053` |
| 20 | -137.907188 | 732824533 | 89.606097 | 812830516 | 8 | `60953689`, `R_20=4.522959` |
| 50 | -74.792384 | 660693448 | 22.133894 | 595662143 | 4 | `234422881`, `R_50=0.794984` |
| 100 | -54.610103 | 234422881 | 10.320270 | 484172367 | 1 | `484172367`, `R_100=10.320270` |
| 200 | -44.586656 | 732824533 | -4.784747 | 393550075 | 0 | NA |

Thus the global envelopes `R_10<0`, `R_20<0`, `R_50<0`, and `R_100<0` are computationally falsified on the existing asymptotic grid. Do not use them as theorem candidates.

## Replacement target

Use two separate statements:

1. Finite computational lemma: for all `N in [99992,1000000]`, `R_10(N)<0`, with the explicit interval above.
2. Next analytic/computational gate: test `K0=200`, not `K0=10`, for larger windows. The current sampled target is `R_200(N)<0`; on the 94-point grid through `1e9`, it survives with max `-4.784747`.

Proof route for any promoted tail lemma must start from the q-block formula above and control the weighted low-q Mertens aggregate directly. A fixed small `K0` should be treated as a finite-window device, not an asymptotic theorem.

## Do not promote unless

- Do not promote any global fixed-`K0<=100` negative-tail lemma; it is already falsified on sampled data.
- Do not promote `K0=200` beyond "sample-survived"; it has not been densely scanned above `1e6`.
- Do not use the dense `[99992,1000000]` `R_10` certificate outside that exact range.
- Do not cite external Mertens/RH/Walfisz-style bounds for this file without primary-source quote plus page/equation.
