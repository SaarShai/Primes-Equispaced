---
schema_version: 1
title: "EC smoothing blocker sprint synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
sources:
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T2_STOCHASTIC_EULER_PRODUCT_MODEL.md
  - handoff-2026-05-11-ec-smoothing-blockers/C1_HOLDOUT_CURVE_PROTOCOL.md
  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md
  - handoff-2026-05-11-ec-smoothing-blockers/C3_LARGER_K_DENSE_GRID_PLAN.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
tags: [ec-ndc, smoothing, blockers, synthesis, theorem-target]
---

# EC Smoothing Blocker Sprint Synthesis

No theorem was promoted. The sprint converted the main blocker into a precise
analytic reduction plus a falsification battery.

## Executive Verdict

The closest meaningful breakthrough is no longer "EC universality." It is a
conditional theorem explaining fixed-curve stabilization of the smoothed
coefficient sum times smoothed Euler product:

```text
c_E,W(K) P_E,W(K) -> exp(B_E,W) / L^(r)(E,1)
```

for rank `r >= 1`, provided two hard analytic inputs are proved:

- `H1`: smoothed reciprocal Perron expansion with offcentral-zero residue
  control, including possible multiple zeros and reciprocal derivative growth;
- `H2`: smoothed EC-Mertens product expansion
  `log P_E,W(K) = -r log log K + B_E,W + o(1)`.

This would explain why smoothing can stabilize a fixed curve. It would not
explain cross-curve universality, and it would not make `L2^rank` load-bearing.

## Result Table

| Agent | Status | Main result | Decision |
|---|---|---|---|
| T1 | `RIGOROUS_REDUCTION` | Conditional smoothed Perron/product theorem with explicit `H1-H3`; endpoint smoothing improves Mellin decay from hard-cutoff `1/z` to smooth-kernel faster decay. | Use as theorem target. No promotion until `H1` and `H2` are citation/proof closed. |
| T2 | `RIGOROUS_REDUCTION` | Exact finite variance identity for smoothed additive Euler-product models; EC heuristic says the pass is `c/P` endpoint covariance damping. | Explains ablations and gives falsifiable predictions. |
| C1 | `COMPUTE_BLOCKED` | Predeclared 16-curve holdout protocol from local labels; missing local `ainvs`/`gp` blocks execution. | Next implementation needs metadata CSV, not more theory. |
| C2 | `RIGOROUS_REDUCTION` | Kernel/null-control protocol with gates G0-G5, Sato-Tate nulls, rank/curve permutations, leave-one-K/curve. | Implement as a copy/successor of the reproducer. |
| C3 | `COMPUTE_BLOCKED` | Larger/denser `K` protocol; `K=3e6` feasible exact run, `K=1e7` expensive without faster `a_p`. | Run cache-only dense replay first, then schedule `K=3e6`. |

## What Changed

The reproduced three-curve pass is real but no longer mysterious. T2's finite
model predicts exactly what the CSV shows:

- `all, alpha=0.75` passes.
- `cP_only, alpha=0.75` is almost identical.
- `P_only` and `PL2_only` pass at several alphas.
- `L2_only` stays essentially sharp-cutoff.

Therefore the current effect is most likely smoothing of endpoint/product-shell
variance and improved covariance alignment between `log c` and `log P`. The
current data do not support the sentence "`L2^rank` explains the normalization."

## Main Blockers

1. **Analytic H1.** The reciprocal coefficient Perron formula must control all
   offcentral zero residues. Smooth `W_hat` helps, but does not bound
   reciprocal zero derivatives or multiple-zero log powers by itself.
2. **Analytic H2.** The EC Euler product at `s=1` needs a smoothed Mertens
   theorem with the exact central coefficient `-rank(E) log log K`.
3. **Rank zero.** For rank `0`, central and offcentral residues can both be
   constant-scale. Pointwise stabilization needs stronger cancellation or a
   declared averaged statement.
4. **Ablations.** Proper ablations already pass old gates. Any theorem or
   empirical claim must identify a load-bearing component, not just a smoother
   endpoint.
5. **Holdout metadata.** Local files have holdout labels/ranks/conductors but
   not minimal `ainvs`; `gp` is not installed locally.
6. **Larger `K`.** Exact point counting is `O(sum_{p<=K} p)`. `K=3e6` is
   feasible; `K=1e7` needs either overnight compute or a faster `ellap` path.
7. **Null controls.** Sato-Tate randomization, rank permutations, curve
   permutations, kernel families, and leave-one tests are mandatory before
   promotion.

## Next Work Order

1. **Theorem sprint H2 first.** Try to prove or source-check the smoothed
   EC-Mertens expansion for `log P_E,W(K)` with coefficient `-rank(E)`.
   H2 is more directly tied to the Euler product and current data than the full
   reciprocal-zero H1 wall.
2. **Then H1.** Attack the smoothed reciprocal Perron residue aggregate,
   explicitly allowing multiple offcentral zeros and reciprocal derivative
   growth.
3. **Implement C2 controls.** Fork the reproducer; add kernel families,
   matched-mass controls, Sato-Tate nulls, rank/curve permutations, and
   leave-one metrics.
4. **Run C3 dense replay through `K=1e6`.** This is cache-only and should be
   cheap. It tests whether the seven-point grid is misleading before spending
   on `K=3e6`.
5. **Acquire C1 metadata.** Build a hash-recorded holdout curve metadata CSV
   with exact `ainvs`, conductor, rank, and convention checks against the three
   training curves.

## Do Not Promote Unless

- `H1` and `H2` are proved or citation-closed with the repository source
  protocol.
- The rank-zero case is separated or handled.
- A predeclared holdout set passes without alpha/mode retuning.
- Larger/denser `K` shows tail stabilization rather than endpoint damping.
- Kernel/null controls do not reproduce the same gate pass generically.
- Proper ablations stop matching the headline, or the headline is weakened to
  "smoothing suppresses endpoint drift" rather than an EC-NDC normalization.
