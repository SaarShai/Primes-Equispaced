---
title: "Agent 12 - EC diagnostic theory bridge"
date: 2026-05-11
status: DIAGNOSTIC_ONLY
tags: [breakthrough-wave-4, ec-ndc, smoothing, h1, residues, c2-prime, holdout, diagnostics]
---

# Agent 12 - EC Diagnostic Theory Bridge

## Verdict

Status: `DIAGNOSTIC_ONLY`.

No EC smoothing theorem is promoted. No finite EC smoothing gate should be used
as theorem closure before H1 reciprocal-pole control and H2 endpoint closure.

The right numerical role is narrower: decide whether the current finite
smoothed proxy is mainly seeing low H1 reciprocal residues or a finite-grid /
endpoint-kernel artifact. A successful diagnostic only redirects theorem work;
it does not prove stabilization.

## Diagnostic Target

Freeze the primary finite proxy:

```text
X_E,W(K) = zeta(2) * c_E,W(K) * P_E,W(K) / L2_E,W(K)^r
kernel = smoothstep
mode = all
alpha = 0.75
match = none
K grid = 1000,3000,10000,30000,100000,300000,1000000
training curves = 37a1,11a1,389a1
```

The theorem blocker it must probe is H1:

```text
Z_c(u) = sum_{gamma != 0} A_gamma W_hat(i gamma) exp(i gamma u),
u = log K,
A_gamma = 1 / L'(E,1+i gamma)        for simple offcentral zeros.
```

H2 branch terms can have extra `1/u` damping, but H1 residues do not. Therefore
the diagnostic must not ask "does smoothing look stable?" It must ask:

```text
Does killing named low H1 frequencies change the finite EC proxy in a way that
matched fake filters, grid jitter, and Sato-Tate nulls do not reproduce?
```

Decision labels:

| label | meaning |
|---|---|
| `RESIDUE_DOMINATED_DIAGNOSTIC` | finite data respond specifically to actual low H1 residues |
| `FINITE_GRID_ARTIFACT_DIAGNOSTIC` | pass is explained by grid/kernel/mass/endpoint effects, not actual H1 residues |
| `NUMERICS_PAUSE` | stochastic, metadata, holdout, dense-grid, or filter-specificity gates fail |

## Source Anchors

- `primes-equispaced/L2_facts/farey-current-state.md`: current EC C1 values and W2-prime warning; old pure-rank framing is superseded.
- `primes-equispaced/L2_facts/farey-claim-ledger.md`: deterministic C2 gates passed, full stochastic G3 failed empirical p gates, C2-prime is future-only, and H1/H2 remain theorem blockers.
- `primes-equispaced/handoff-2026-05-11-all-in-wave/EC_G3_FAILURE_DIAGNOSTIC_2026-05-11.md`: G3 failed because `st_iid p_ratio=0.062378167641325533 > 0.01` and `st_shared p_score=0.046511627906976744 > 0.02`; old/primary null pass counts were still zero.
- `primes-equispaced/handoff-2026-05-11-all-in-wave/EC_C2_PRIME_DIAGNOSTIC_PROTOCOL_2026-05-11.md`: fresh seeds `512..1023` iid and `128..255` shared; use CV/Pareto p-values; no retroactive G3 rescue.
- `primes-equispaced/handoff-2026-05-11-ec-smoothing-blockers/C1_HOLDOUT_CURVE_PROTOCOL.md`: 16 predeclared EC holdouts; metadata is missing locally; no alpha/mode retuning.
- `primes-equispaced/handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md`: G0-G5 kernel/null gates, primary anchors `ratio=1.3473754929960748`, `max_cv=0.063297427334436704`.
- `primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md`: finite signed kernel filtering can kill named residues, but is diagnostic only without tail control.
- `primes-equispaced/handoff-2026-05-11-all-in-wave/EC_POINTWISE_THEOREM_SPINE_2026-05-11.md`: positive-rank pointwise theorem remains conditional on legal-height H1 reciprocal-pole control plus H2 S1/Sym2 finite-part closure.

## Predeclared Tests

### T0 - Freeze And Provenance

Before generating any fresh data, freeze:

```text
script SHA256
AP cache SHA256
metadata SHA256
kernel definitions
K grids
zero lists
filter construction code
all pass/fail thresholds below
```

Reproduce the primary real anchor to tolerance `5e-13`:

```text
ratio = 1.3473754929960748
max_cv = 0.063297427334436704
```

Failure label: `NUMERICS_PAUSE`.

### T1 - C2-prime First

Run fresh C2-prime before holdouts or dense-K claims:

```text
st_iid seeds    = 512..1023
st_shared seeds = 128..255
```

Required diagnostic pass:

```text
st_iid old_pass_rate <= 0.01
st_iid primary_pass_rate <= 0.005
st_iid p_cv <= 0.01
st_iid p_pareto <= 0.01

st_shared old_pass_rate <= 0.02
st_shared p_cv <= 0.02
st_shared p_pareto <= 0.02
```

Ignore `p_ratio` and additive `p_score` as gates. Report them only.

Failure label: `NUMERICS_PAUSE`. Do not proceed to holdout or dense-grid
promotion work after a C2-prime fail.

### T2 - H1 Residue Fingerprint

For each real curve, precompute the first

```text
J in {1,2,4,8}
```

offcentral H1 ordinates `gamma_j` and, where numerically available, the
reciprocal derivative weights `1/L'(E,1+i gamma_j)`.

On the base grid, one log-jittered grid, and one dense tail grid, compute the
centered residual

```text
Y_E(u) = log X_E,W(exp u) - mean_u log X_E,W(exp u).
```

Residue fingerprint condition:

```text
spectral_mass(actual first J H1 windows)
  >= 0.60 * spectral_mass(total low-frequency diagnostic band)
```

and

```text
spectral_mass(actual first J H1 windows)
  >= 3 * spectral_mass(matched fake windows)
```

Fake windows are frozen before the run:

```text
shifted ordinates gamma_j + 0.37
permuted ordinates from the other training curves
grid-comb frequencies induced by the seven-point K grid
```

If actual H1 windows do not beat all fake windows on both the jittered and dense
grids, classify as `FINITE_GRID_ARTIFACT_DIAGNOSTIC` or `NUMERICS_PAUSE`
depending on whether C2-prime passed.

### T3 - Kernel-Filter Contrast

Construct signed log-kernels with:

```text
W_hat(0)=1
W_hat(i gamma_j)=0 for j<=J
```

for `J in {1,2,4,8}`. For each actual filter, also construct matched fake
filters with the same support, mass, roughness budget, and numerical condition
number, but zeros at the fake windows from T2.

Run each filter on:

```text
training curves
base K grid
log-jittered K grid
dense tail grid
```

Residue-dominated pass requires all clauses:

```text
actual-filter median max_cv reduction >= 30%
actual-filter median abs(tail_slope) reduction >= 30%
fake-filter median max_cv reduction <= 10%
fake-filter median abs(tail_slope) reduction <= 10%
actual-filter improvement is nondecreasing from J=1 to J=8, allowing one tie
classification agrees on base, jittered, and dense grids
```

Finite-grid artifact label if any clause holds:

```text
fake filters match or beat actual filters
actual filters improve base grid but not jittered/dense grids
grid-comb windows explain more residual mass than actual H1 windows
tail slopes exceed 0.03 in absolute value after filtering
```

### T4 - Holdout Curves

Run only after T1 passes and exact holdout metadata exists.

Use the predeclared 16 curves from the C1 holdout protocol:

```text
rank 0: 14a1,15a1,17a1,19a1,20a1,21a1,24a1
rank 1: 43a1,53a1,57a1,58a1,61a1
rank 2: 433a1,446d1,571b1
rank 3 sentinel: 5077a1
```

No alpha, mode, kernel family, or threshold may be retuned after seeing
holdouts.

Holdout residue-dominated pass requires:

```text
all-holdout primary ratio < 1.42083
all-holdout max_cv < 0.08567129
rank 0, rank 1, rank 2 strata each ratio < 1.42083
each non-sentinel holdout keeps within-curve CV < 0.08567129
5077a1 sentinel CV < 0.10
actual H1 filters beat matched fake filters on at least 10 of 15 non-sentinel holdouts
```

If holdouts pass the old finite gate but actual/fake filtering is not separated,
the correct label is `FINITE_GRID_ARTIFACT_DIAGNOSTIC`, not theorem evidence.

### T5 - Final Diagnostic Classifier

Return exactly one:

```text
RESIDUE_DOMINATED_DIAGNOSTIC
FINITE_GRID_ARTIFACT_DIAGNOSTIC
NUMERICS_PAUSE
```

`RESIDUE_DOMINATED_DIAGNOSTIC` requires T0-T4 to pass and actual H1 filters to
beat fake filters on training, jittered, dense, and holdout grids.

`FINITE_GRID_ARTIFACT_DIAGNOSTIC` requires C2-prime not to fail, plus evidence
that fake/grid filters explain the finite pass as well as actual H1 filters.

`NUMERICS_PAUSE` is the default if C2-prime fails, metadata is missing, AP cache
provenance fails, dense-grid instability appears, or the filter contrast is
inconclusive.

## Promotion Guardrails

- C2-prime is future-only. It cannot reclassify the failed G3 run.
- Kernel filtering is a microscope, not a proof. Killing finitely many residues
  does not control the H1 tail.
- Holdout success is still finite numerical evidence. It cannot close H1
  reciprocal derivative bounds, H1 fixed-weight PV, multiple-zero effective
  degree control, or H2 endpoint branch/Sym2 closure.
- Do not import H2 `1/u` branch damping into H1 reciprocal-pole residues.
- Do not use algebraic/script rank as analytic rank without a separate equality
  input.
- Do not call any outcome BSD evidence, `L(E,2)` evidence, universality, or EC
  stabilization.

## Stop/Pause Criteria

Pause EC numerics and move theory-first if any occurs:

```text
C2-prime fails on fresh seeds
holdout metadata or AP cache is missing/non-reproducible
primary anchor cannot be reproduced to 5e-13
fake filters match actual H1 filters
dense or jittered grids flip the diagnostic classification
tail slope abs value remains > 0.03 after actual filtering
proper ablations pass comparably to all-mode on holdouts
```

Reason to pause: further K-grid tuning would only optimize a finite proxy after
the stochastic or residue-specificity question failed. The live theorem blockers
would remain H1 reciprocal residues/PV/tails and H2 endpoint closure.

## Dependency Impact

If `RESIDUE_DOMINATED_DIAGNOSTIC`:

- prioritize H1 weighted-l1 / fixed-weight PV / reciprocal-tail work;
- package rank-zero as oscillatory/profile/averaged unless all retained
  residues are killed or controlled;
- use numerics only to choose which low zeros to retain in profiles.

If `FINITE_GRID_ARTIFACT_DIAGNOSTIC`:

- stop EC smoothing promotion work;
- do not run larger holdout sweeps until a new theorem-driven observable is
  specified;
- treat the old smoothstep pass as endpoint/grid covariance behavior.

If `NUMERICS_PAUSE`:

- spend no more compute on EC smoothing gates until the named failure is fixed;
- theory queue remains H1 legal-height reciprocal-pole control, multiple-zero
  effective degree handling, and H2 S1/Sym2 endpoint closure.
