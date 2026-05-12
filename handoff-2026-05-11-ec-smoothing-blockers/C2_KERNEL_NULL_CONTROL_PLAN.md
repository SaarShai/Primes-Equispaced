---
schema_version: 1
title: "C2 kernel and null-control falsification plan"
date: 2026-05-11
type: plan
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
sources:
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv
tags: [ec-ndc, smoothing, kernels, null-controls, falsification]
---

# C2 Kernel And Null-Control Falsification Plan

status: `RIGOROUS_REDUCTION`

Execution outcome labels for a future run, not this document's status:

- `NO_GO`: at least one required gate fails after execution.
- `PROOF_CANDIDATE`: all required C2 gates pass after execution.

## Baseline To Falsify

Current reproducer tests `K=1000,3000,10000,30000,100000,300000,1000000`,
alphas `0,0.25,0.5,0.65,0.75,0.85,0.92`, and modes
`sharp,c_only,P_only,L2_only,cP_only,cL2_only,PL2_only,all`.

Old gate:

- `cross_curve_ratio < 1.42083`
- `max_within_cv < 0.08567129`

Observed anchors from the saved metrics:

| case | ratio | max CV | status |
|---|---:|---:|---|
| `all, alpha=0.75` | `1.3473754929960748` | `0.063297427334436704` | passes old gate |
| `cP_only, alpha=0.75` | `1.3474536199105895` | `0.063319173311522384` | passes old gate |
| `P_only, alpha=0.85` | `1.366515830251503` | `0.060251761567118804` | passes old gate |
| best non-passing low-ratio ablation, `cL2_only, alpha=0` | `1.3077350110801771` | `0.11332518873918335` | fails CV |

Interpretation: the old gate is not specific to the full `L2^rank` denominator.
C2 must test whether the signal is just endpoint damping, kernel mass matching,
or label leakage.

## Primary Definitions

For each scenario `s`, curve label `c`, kernel `q`, kernel parameter `theta`,
mode `m`, alpha `a`, and cutoff `K`, compute the same quantity as Agent3:

`X(s,c,q,theta,m,a,K) = zeta(2) * c_K * P_K / L2_K^r_assigned`.

For a fixed group `g=(s,q,theta,m,a)`:

- `mu_c(g) = mean_K X(g,c,K)` over the declared K grid.
- `cv_c(g) = stdev_K X(g,c,K) / abs(mu_c(g))`, population stdev.
- `cross_curve_ratio(g) = max_c mu_c(g) / min_c mu_c(g)`.
- `cross_curve_cv(g) = stdev_c mu_c(g) / mean_c mu_c(g)`.
- `max_within_cv(g) = max_c cv_c(g)`.
- `score(g) = log(cross_curve_ratio(g)) + max_within_cv(g)`.

Use population standard deviations to match the existing
`coefficient_of_variation` implementation.

## Kernel Families

Let `t=x/K`, `u=(t-alpha)/(1-alpha)`, and set all compact kernels to `1` for
`t <= alpha`, their tail formula for `alpha < t < 1`, and `0` for `t >= 1`.

Predeclared primary alpha: `0.75`.

Primary kernel suite:

| kernel | parameters | tail formula |
|---|---|---|
| `smoothstep` | none | `1 - u^2*(3 - 2*u)` |
| `hann` | none | `0.5*(1 + cos(pi*u))` |
| `riesz` | `beta in {1,2,4}` | `(1-u)^beta` |
| `exponential` | `lambda in {1,3,6}` | `exp(-lambda*u/(1-u))` |
| `gaussian` | `sigma in {0.35,0.50,0.75}` | `(exp(-0.5*(u/sigma)^2)-exp(-0.5/sigma^2))/(1-exp(-0.5/sigma^2))` |

Matched-mass controls:

- Baseline continuous mass is smoothstep at `alpha=0.75`:
  `M0 = integral_0^1 w(t) dt = 0.875`.
- `match=continuous`: for each kernel parameter, choose `alpha*` satisfying
  `alpha* + (1-alpha*) * integral_0^1 tail_q(u,theta) du = 0.875`.
- `match=discrete_n`: for each `(K,q,theta)`, solve by bisection for `alpha*`
  such that `sum_{1<=n<=K} w_q(n/K;alpha*,theta)` equals the smoothstep
  `alpha=0.75` sum on the same `n` support.
- `match=discrete_p`: same as `discrete_n`, but on primes `p<=K`.
- `match=discrete_both`: use `discrete_n` for `c_K` and `discrete_p` for
  `P_K,L2_K`.

Required kernel runs:

1. `match=none`, fixed `alpha=0.75`, all primary kernels.
2. `match=continuous`, mass `0.875`, all primary kernels.
3. `match=discrete_both`, mass matched to smoothstep `alpha=0.75`, all primary
   kernels.
4. Alpha sensitivity grid `0.50,0.65,0.75,0.85,0.92` for
   `smoothstep,hann,riesz(beta=2),exponential(lambda=3),gaussian(sigma=0.50)`.

## Null Controls

### N1: Randomized Sato-Tate `a_p`

Create `scenario=st_iid` with seeds `0..511`.

For each seed, curve label, and good prime `p`, draw
`theta` from Sato-Tate density `(2/pi)sin^2(theta)` on `[0,pi]`, set
`a_p = round(2*sqrt(p)*cos(theta))`, and clamp to
`[-floor(2*sqrt(p)), floor(2*sqrt(p))]`. Preserve the original bad-prime
reduction and original bad-prime `a_p`.

Sampling must use `numpy.random.default_rng(seed)` and deterministic rejection
sampling in lexicographic loop order `(curve label, prime)`: propose
`theta ~ Uniform(0,pi)`, `y ~ Uniform(0,1)`, accept iff
`y <= sin(theta)^2`.

Also create `scenario=st_shared` with seeds `0..127`, using one Sato-Tate draw
per prime shared by all three curve labels. This isolates rank/conductor labels
from independent local-factor noise.

### N2: Rank-Label Permutations

Create all six permutations of assigned ranks `{0,1,2}` across labels
`37a1,11a1,389a1`.

- `rank_perm=identity`: assigned ranks `(1,0,2)`.
- enumerate nonidentity permutations in lexicographic tuple order.
- Nonidentity controls: use the same real `a_p` and reductions, but replace
  `L2_K^rank` by `L2_K^r_assigned`.
- Keep output labels fixed.

This directly tests whether the `L2^rank` denominator is load-bearing.

### N3: Curve-Label Permutations

Create all six permutations of source curve local data across fixed output
labels.

- Keep output labels, conductors, and assigned ranks fixed.
- enumerate source-label permutations in lexicographic tuple order.
- For label `c`, compute `c_K,P_K,L2_K` from the `a_p` and reduction table of
  source curve `pi(c)`.
- Record `source_curve`.

This tests whether the signal depends on the actual curve-local data aligned
with the label, not only on having three EC-like sequences.

### N4: Leave-One-K-Out

For every primary real-data group, recompute metrics after removing each one of
the seven K values.

Report:

- `loo_k_pass_count` out of `7` under the old gate.
- `loo_k_ratio_min`, `loo_k_ratio_max`, `loo_k_ratio_range`.
- `loo_k_maxcv_min`, `loo_k_maxcv_max`, `loo_k_maxcv_range`.

Baseline smoothstep `all, alpha=0.75` read-only diagnostics:

- all seven leave-one-K subsets pass the old gate.
- ratio range is `1.331450602331709` to `1.3705117170902625`.
- max CV range is `0.051639475223074015` to `0.06809071081444831`.

### N5: Leave-One-Curve-Out

Use fixed predeclared primary group first:
`real,smoothstep,all,alpha=0.75,match=none`.

For each held-out curve `h`:

- `train_geo_mean_h = exp(mean_{c!=h} log(mu_c))`.
- `holdout_ratio_h = max(mu_h, train_geo_mean_h) / min(mu_h, train_geo_mean_h)`.
- `holdout_cv_h = cv_h`.

Baseline read-only diagnostics:

| held out | holdout ratio |
|---|---:|
| `37a1` | `1.159726273261443` |
| `11a1` | `1.3467724722662582` |
| `389a1` | `1.1612847818639083` |

Optional selection stress test: choose the best `(kernel,theta,alpha)` on the
two training curves only by minimizing `score_train`, then evaluate the held-out
curve without refitting.

## Gates

### G0: Reproducibility Gate

Pass only if:

- script SHA256, input AP cache SHA256, K grid, alpha grid, modes, and curve list
  are printed in the summary;
- every raw row has `product_complete=True`;
- no `X,c,P,L2,L2_rank_power` value is `nan`, `inf`, or nonpositive;
- baseline `real,smoothstep,all,alpha=0.75,match=none` exactly reproduces
  ratio `1.3473754929960748` and max CV `0.063297427334436704` to absolute
  tolerance `5e-13`.

### G1: Primary Real-Data Survival Gate

Pass only if the fixed primary group
`real,smoothstep,all,alpha=0.75,match=none` satisfies:

- old gate passes;
- `score <= log(1.3473754929960748) + 0.063297427334436704 + 0.005`;
- all seven leave-one-K subsets pass the old gate;
- each fixed leave-one-curve `holdout_ratio_h < 1.42083`;
- each fixed leave-one-curve `holdout_cv_h < 0.08567129`.

### G2: Kernel-Robust But Not Kernel-Tuned Gate

Pass only if:

- at least `4` of the `5` primary representatives
  `smoothstep,hann,riesz(beta=2),exponential(lambda=3),gaussian(sigma=0.50)`
  pass the old gate at fixed `alpha=0.75`;
- at least `4` of those `5` pass under `match=continuous`;
- at least `4` of those `5` pass under `match=discrete_both`;
- the best kernel is not allowed to be selected after seeing all alpha values:
  the reported headline remains the predeclared `smoothstep, alpha=0.75`.

Fail interpretation:

- only smoothstep passes: likely kernel tuning artifact;
- only matched-mass variants pass: likely mass/endpoint artifact;
- all kernels pass but nulls also pass: smoothing artifact not falsified.

### G3: Sato-Tate Null Gate

For `st_iid` seeds `0..511`, using the fixed primary kernel group:

- `null_old_pass_rate <= 0.01`;
- `null_primary_pass_rate <= 0.005`, where primary pass means old gate plus
  `score <= real_primary_score + 0.005`;
- empirical `p_score = (1 + count(score_null <= score_real))/(513) <= 0.01`;
- empirical `p_ratio = (1 + count(ratio_null <= ratio_real))/(513) <= 0.01`.

For `st_shared` seeds `0..127`:

- `null_old_pass_rate <= 0.02`;
- `p_score <= 0.02`.

If either Sato-Tate null regularly passes, the smoothing signal is compatible
with random EC-sized local factors and must not be promoted.

### G4: Rank And Curve Label Specificity Gate

Rank permutations:

- identity must pass G1;
- `0` of the `5` nonidentity rank permutations may pass the old gate for
  fixed `smoothstep,all,alpha=0.75`;
- `rank_identity_score + 0.02 < min_nonidentity_rank_score`.

Curve-label permutations:

- identity must pass G1;
- `0` of the `5` nonidentity curve-label permutations may pass the old gate for
  fixed `smoothstep,all,alpha=0.75`;
- `curve_identity_score + 0.02 < min_nonidentity_curve_score`.

If nonidentity permutations pass, the result is label-alignment fragile and
must stay unpromoted.

### G5: Tail Stability Gate

Using `K >= 100000` for the fixed primary group:

- tail-only old gate passes;
- `max_c abs(slope_c) <= 0.03`, where `slope_c` is OLS slope of
  `log(X(c,K))` versus `log(K)` on tail K values.

Baseline smoothstep `all, alpha=0.75` tail diagnostics:

- tail-only ratio `1.4023997514636641`;
- tail-only max CV `0.05158036084512034`;
- slopes: `37a1=0.024791742743129768`,
  `11a1=0.00007641727925834057`, `389a1=-0.01892703701094014`.

## Expected Outputs

Future C2 execution should write these files, not overwrite Agent3 outputs:

- `handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_RAW_2026-05-11.csv`
- `handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_METRICS_2026-05-11.csv`
- `handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_NULL_SUMMARY_2026-05-11.csv`
- `handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_SUMMARY_2026-05-11.md`

Required raw CSV columns:

`scenario,seed,kernel,kernel_param,match_mode,match_basis,match_target_mass,mode,alpha,effective_alpha_n,effective_alpha_p,curve,source_curve,true_rank,assigned_rank,conductor,K,c,P,D,D_zeta2,L2,L2_rank_power,X,p_max,prime_count,product_complete`.

Required metrics CSV columns:

`scenario,seed,kernel,kernel_param,match_mode,mode,alpha,cross_curve_ratio,cross_curve_cv,max_within_cv,score,passes_old_gate,passes_primary_gate,mean_37a1,mean_11a1,mean_389a1,cv_37a1,cv_11a1,cv_389a1,tail_ratio,tail_max_cv,tail_slope_37a1,tail_slope_11a1,tail_slope_389a1,loo_k_pass_count,loo_k_ratio_min,loo_k_ratio_max,loo_k_ratio_range,loo_k_maxcv_min,loo_k_maxcv_max,loo_k_maxcv_range`.

Required null summary columns:

`null_family,kernel,kernel_param,match_mode,mode,alpha,n_trials,old_pass_count,old_pass_rate,primary_pass_count,primary_pass_rate,real_ratio,real_max_within_cv,real_score,best_null_ratio,best_null_max_within_cv,best_null_score,p_ratio,p_score,gate_status`.

Required summary markdown:

- exact command;
- Python and NumPy versions;
- script and AP-cache SHA256;
- tables for G0 through G5 with `PASS` or `FAIL`;
- first failing gate named in one line;
- "do not promote unless" section retained verbatim.

## Minimal Code Changes Needed

Patch only a copy or successor of `AGENT3_ec_smoothed_reproducer.py`; do not
rewrite the existing Agent3 result files.

Minimal implementation checklist:

1. Add `kernel_weight(t, kernel, alpha, param)` and move current
   `smooth_weight` into the `smoothstep` branch.
2. Add `--kernels`, `--kernel-params`, and `--match-mode
   none,continuous,discrete_n,discrete_p,discrete_both`.
3. Add `kernel_tail_integral(kernel,param)` using closed forms for
   `smoothstep,hann,riesz` and numerical quadrature for `exponential,gaussian`.
4. Add `solve_alpha_for_mass(points, kernel, param, target_mass)` by bisection
   on `[0,0.999999]`.
5. Add `--scenario real,st_iid,st_shared,rank_perm,curve_perm` and
   `--null-seeds`.
6. Add pure transformation helpers that return view dictionaries for
   `ap`, `reduction`, `assigned_rank`, and `source_curve`; avoid mutating the
   original cache dictionaries in place.
7. Extend raw row keys with scenario/kernel/null metadata.
8. Extend `compute_metrics` to group by
   `(scenario,seed,kernel,kernel_param,match_mode,mode,alpha)`.
9. Add leave-one-K, leave-one-curve, tail slope, and null empirical p-value
   calculations after raw metrics are computed.
10. Add a new report writer for C2 output paths under
    `handoff-2026-05-11-ec-smoothing-blockers/`.

No mathematical code outside the reproducer needs to change. No AP cache format
change is required.

## Decision Rule

Set final C2 status as follows:

- `NO_GO` if any of G0 through G5 fails.
- `PROOF_CANDIDATE` only if all of G0 through G5 pass.

Do not promote unless G0, G1, G2, G3, G4, and G5 all pass, and the independent
T1/T2/C1/C3 blockers also clear. Passing C2 alone is not evidence for BSD,
`L(E,2)` universality, or theorem-grade EC NDC.
