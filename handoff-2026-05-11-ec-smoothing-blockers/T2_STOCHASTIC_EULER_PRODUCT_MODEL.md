---
schema_version: 1
title: "T2 stochastic Euler-product model for EC smoothing"
date: 2026-05-11
type: report
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.56
sources:
  - HANDOFF.md
  - L2_facts/farey-claim-ledger.md
  - handoff-2026-05-11-ec-smoothing-blockers/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py
tags: [ec-ndc, smoothing, random-euler-product, ablation, variance]
---

# T2 Stochastic Euler-Product Model

status: `RIGOROUS_REDUCTION`

## Verdict

The reproducible smoothing effect has a clean variance-reduction explanation, but not a theorem-grade EC normalization yet.

The rigorous part is an exact finite variance identity: smoothing can reduce within-`K` variance only through the grid-energy of the kernel and through covariance alignment between the smoothed `c_E` coefficient sum and the smoothed `P_E` Euler product. The EC-specific part remains a labeled random-Euler-product/Sato-Tate heuristic.

The current ablations give a finite no-go for using `L2^rank` as the load-bearing explanation of the observed pass: removing smoothed `L2` changes the old-gate metrics only at `~1e-4`, while `cP_only`, `P_only`, and `PL2_only` already pass the old gate.

## Source-Verified Facts Used

- The saved reproduction is complete through `K<=1000000` on curves `37a1`, `11a1`, `389a1`, with K grid `1000,3000,10000,30000,100000,300000,1000000`; see `AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md`.
- The old gate is cross-curve ratio `< 1.42083` and max within-curve CV `< 0.08567129`; same summary and `AGENT3_ec_smoothed_reproducer.py`.
- Best full smoothing is `all, alpha=0.75`: ratio `1.3473754929960748`, max CV `0.063297427334436704`; same summary/metrics CSV.
- Best passing non-all ablation is `cP_only, alpha=0.75`: ratio `1.3474536199105895`, max CV `0.063319173311522384`.
- `P_only` and `PL2_only` also pass at `alpha in {0.65,0.75,0.85,0.92}`; metrics CSV.
- Sharp cutoff fails: ratio `1.4238213854704775`, max CV `0.096692112053387638`; metrics CSV.
- `L2_only` never passes; its best ratio is `1.4237924788639904`, essentially sharp.
- The reproducer defines `X = zeta(2) * c * P / L2^rank`, with smoothstep weights applied independently to `c`, `P`, and `L2`; see `AGENT3_ec_smoothed_reproducer.py`.
- For good primes, the code uses `mu(p)=-a_p`, `mu(p^2)=p`, and local inverse factors `1-a_p/p+1/p`, `1-a_p/p^2+1/p^3`; see `Koyama_EC_NDC_extended_sweep.py`.

No external theorem citation is used below. Framework names only: Sato-Tate, random Euler product, partial summation.

## Exact Reduction

Let `G={K_1,...,K_m}` be the finite K grid. For a finite index set `I`, deterministic weights `w_i(K)`, and centered increments `xi_i` independent across `i` with variances `sigma_i^2`, define

```text
S(K) = sum_{i in I} w_i(K) xi_i.
```

Then the expected grid variance is exactly

```text
E Var_G S = sum_i sigma_i^2 Var_G(w_i).
```

For two components

```text
A(K)=sum_i u_i(K) xi_i,
B(K)=sum_i v_i(K) eta_i,
Var(eta_i)=omega_i^2,
E[xi_i eta_i]=tau_i,
```

the exact identity is

```text
E Var_G(A+B)
 = sum_i sigma_i^2 Var_G(u_i)
 + sum_i omega_i^2 Var_G(v_i)
 + 2 sum_i tau_i Cov_G(u_i,v_i).
```

This is the reduction. It is theorem-grade finite probability. To turn it into an EC theorem, one must prove that the relevant prime/coefficient increments satisfy a covariance model with explicit errors.

## EC Heuristic Specialization

This subsection is heuristic.

For good primes, write `lambda_p=a_p/sqrt(p)`. A random-Euler-product model treats `lambda_p` as centered with bounded variance `nu_E`.

The smoothed log Euler product has additive prime increments

```text
log P_{E,w}(K)
 = - sum_{p<=K} w(p/K) log(1-a_p/p+1/p).
```

Its centered first-order random term is approximately

```text
sum_{p<=K} w(p/K) lambda_p / sqrt(p),
```

so the model variance over the grid is

```text
nu_E * sum_p Var_G(w(p/K)) / p
```

plus lower-order deterministic/quadratic terms.

For the `L(E,2)` factor,

```text
log L2_{E,w}(K)
 = - sum_{p<=K} w(p/K) log(1-a_p/p^2+1/p^3),
```

the first-order random term is approximately

```text
sum_{p<=K} w(p/K) lambda_p / p^(3/2),
```

with model variance

```text
nu_E * sum_p Var_G(w(p/K)) / p^3.
```

That `p^-3` variance scale is the basic reason smoothing `L2` should be tiny at the tested K range. The observed CSV confirms it: at `alpha=0.75`, replacing `all` by `cP_only` changes cross-curve ratio by `0.00007812691451469789` and max CV by `0.000021745977085679824`; replacing `P_only` by `PL2_only` changes the ratio by `0.00008011437758814743`.

For `c_E`, the code-level local coefficients include the prime-linear term `-a_p/p`, opposite in sign to the first-order term of `log P_E`. Thus the model predicts strong negative covariance between `log c_E` and `log P_E`. Smoothing both with the same kernel should improve covariance alignment; smoothing only one component can leave endpoint phases mismatched.

## What The CSV Says About Covariance

Derived from `AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv` on the saved seven-point K grid.

Within-curve log-variance of `X` drops under `all, alpha=0.75`:

| curve | sharp `Var(log X)` | all `Var(log X)` | ratio |
|---|---:|---:|---:|
| `37a1` | `0.004047221648813158` | `0.001637392683501018` | `0.4046` |
| `11a1` | `0.0017857140677345858` | `0.00024020128165403587` | `0.1345` |
| `389a1` | `0.009470499635006067` | `0.004025913920285211` | `0.4251` |

The large cancellation is between `log c` and `log P`:

| curve | sharp corr(`log c`,`log P`) | all corr(`log c`,`log P`) |
|---|---:|---:|
| `37a1` | `-0.9786559873052391` | `-0.9876717092838493` |
| `11a1` | `-0.4965219245862345` | `-0.8891867082010895` |
| `389a1` | `-0.9741984362781737` | `-0.9907691749574515` |

This explains why `cP_only` is nearly identical to `all`: it carries the covariance mechanism. It also explains why `c_only` fails the within-K gate: it leaves the larger `P` endpoint phase sharp. At `alpha=0.75`, `c_only` has max CV `0.098971990137690119`, worse than the old cutoff.

## Theorem Candidates

### Candidate A: finite-grid smoothing theorem

Nature: rigorous, already reduced.

For any finite grid and any additive martingale/Euler-product model with independent centered increments and known covariance matrix per prime/coefficient, the exact variance identity above gives an explicit formula for the expected within-K variance of every ablation mode.

Required EC input:

```text
Covariance matrix for the prime-linear parts of log c_E, log P_E, and rank*log L2_E,
with an error term for composites and quadratic prime terms.
```

Expected output:

```text
E Var_G(log X_mode)
= sum_p V_p(mode) + error_E(G,Kmax),
```

where `V_p(mode)` is explicit from the kernel weights and the covariance matrix.

### Candidate B: random Euler-product variance asymptotic

Nature: heuristic theorem target.

Under a Sato-Tate-style prime trace model plus enough decorrelation to justify second-moment summation,

```text
Var_G(log P_w) ~= nu_E sum_p Var_G(w(p/K))/p,
Var_G(rank*log L2_w) ~= rank^2 nu_E sum_p Var_G(w(p/K))/p^3,
Cov_G(log c_w,log P_w) < 0,
```

with the `c,P` covariance having the same kernel when both are smoothed. This predicts that `cP_only` and `all` should track closely, while `L2_only` should not move the gate.

### Candidate C: partial-summation endpoint damping

Nature: heuristic theorem target.

Smoothstep replaces sharp endpoint increments by a compact C1 average over the terminal interval `[alpha K,K]`. If the residual endpoint term dominates the seven-point grid variance, smoothing reduces within-K variance even without changing the asymptotic normalization.

This is a dangerous mechanism: it can be true and still be mathematically uninteresting. It demands null kernels and phase-randomized controls before promotion.

## No-Go: `L2^rank` Is Not Load-Bearing For This Gate

This is a finite, source-verified no-go for the current claim shape, not a theorem about the true asymptotic normalization.

Observed ablations:

| mode | alpha | passes | ratio | max CV |
|---|---:|---:|---:|---:|
| `all` | `0.75` | `True` | `1.3473754929960748` | `0.063297427334436704` |
| `cP_only` | `0.75` | `True` | `1.3474536199105895` | `0.063319173311522384` |
| `P_only` | `0.85` | `True` | `1.366515830251503` | `0.060251761567118804` |
| `PL2_only` | `0.85` | `True` | `1.3665311924986026` | `0.060240037574336124` |
| `L2_only` | `0.00` | `False` | `1.4237924788639904` | `0.09682056722696666` |
| `sharp` | `0.00` | `False` | `1.4238213854704775` | `0.096692112053387638` |

Any explanation that says the observed old-gate pass is specifically caused by the `L2^rank` denominator predicts that removing smoothed `L2` should materially damage the pass. The CSV contradicts that prediction. `L2^rank` may still be part of a later asymptotic normalization, but it is not the load-bearing component in this finite smoothing phenomenon.

## Exact Holdout Predictions

Predeclare these before adding curves or larger K.

| Test | Prediction if this model is right | Falsifier |
|---|---|---|
| `all` vs `cP_only`, `alpha=0.75` | Cross-ratio difference `<= 0.002`; max-CV difference `<= 0.002`; grid mean of `log(X_all/X_cP)` within `0.002` of zero. | Difference `> 0.01` on a complete holdout grid. |
| `P_only` vs `PL2_only`, `alpha in {0.65,0.75,0.85,0.92}` | Metric differences `<= 0.002` for ratio and max CV. | `PL2_only` succeeds while `P_only` fails, or vice versa, by more than `0.01` in either metric. |
| `L2_only` | No old-gate pass; ratio and max-CV shifts from sharp `<= 0.01`. | `L2_only` passes while both `P_only` and `cP_only` fail. |
| `c_only` | May improve cross-curve ratio but should fail the within-K CV gate on curves with visible `P` endpoint variance. | `c_only` passes broadly while `P_only/cP_only` do not. |
| covariance diagnostic | Successful smoothing must coincide with more negative or better-aligned corr(`log c`,`log P`) and lower `Var(log c + log P)`. | Gate pass with no covariance improvement. |
| rank stress | Changing rank mainly affects level through `L2^rank`, not the smoothing gain; high-rank curves should not make `L2` smoothing suddenly load-bearing at `K<=1e6`. | Holdout high-rank curves where `all-cP` differences exceed `0.01` systematically. |

## Null Tests

Run these as controls, not as theorem evidence.

1. Prime-order permutation null: independently permute the `a_p` sequence across primes for each curve, preserving the multiset and bad-prime flags. Prediction: endpoint damping may reduce within-K variance, but the cross-curve alignment at `alpha=0.75` should not consistently reproduce the real-data ratio near `1.3474`.
2. Sign-randomization null: replace `a_p` by random signs times `|a_p|` at good primes. Prediction: `L2` ablations remain indistinguishable from their non-`L2` partners; `cP` can reduce variance only when the induced `log c/log P` covariance is negative.
3. Independent Sato-Tate-shaped null: sample centered `lambda_p` with the same variance scale and form the code-level local factors where positivity allows. Prediction: the explicit variance formula orders modes by covariance energy; it should not create curve-specific rank evidence.
4. Kernel-family null: compare smoothstep against at least two monotone C1 kernels with the same support parameter. Prediction: performance tracks `Var_G(log c + log P)` and kernel grid-energy, not the name of the kernel.
5. Alpha-sweep null: if every alpha and every kernel passes, the phenomenon is likely generic endpoint damping. Promotion requires a predeclared alpha, preferably `0.75`, to survive holdout without post-selection.

## Decision

Use this as a reduction and falsification plan, not a proof of EC universality.

The next theorem-grade target is:

```text
Prove an explicit covariance estimate for the smoothed prime-linear parts of
log c_E and log P_E, with an error term for composites, showing that common
kernel smoothing reduces Var_G(log(c_E P_E)).
```

Until that is proved, the safe claim is:

```text
Smoothing c_E and P_E reduces the tested variance because it aligns and damps
the dominant c/P endpoint covariance. The current data do not support
L2^rank as the load-bearing mechanism.
```
