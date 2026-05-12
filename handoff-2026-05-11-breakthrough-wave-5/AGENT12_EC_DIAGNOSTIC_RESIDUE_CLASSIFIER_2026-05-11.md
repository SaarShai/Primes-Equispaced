---
title: "AGENT12 EC Diagnostic Residue Classifier"
date: 2026-05-11
type: diagnostic-spec
tier: working
status: DIAGNOSTIC_ONLY
confidence: 0.80
tags: [breakthrough-wave-5, ec-ndc, smoothing, c2-prime, h1, residues, finite-grid, diagnostics]
---

## Verdict

Status: `DIAGNOSTIC_ONLY`.

This packet predeclares the post-C2-prime classifier. It distinguishes two
finite-data explanations:

```text
RESIDUE_DOMINATED_DIAGNOSTIC
FINITE_GRID_ARTIFACT_DIAGNOSTIC
```

The default output is:

```text
NUMERICS_PAUSE
```

Run this only after a fresh C2-prime artifact passes on the predeclared seed
blocks. If C2-prime fails, is run on old seeds, or lacks reproducible hashes,
the residue classifier is not run and EC numerics pause.

## Diagnostic Target

Freeze the primary proxy:

```text
X_E,W(K) = zeta(2) * c_E,W(K) * P_E,W(K) / L2_E,W(K)^r
kernel = smoothstep
mode = all
alpha = 0.75
match = none
training curves = 37a1, 11a1, 389a1
base K grid = 1000,3000,10000,30000,100000,300000,1000000
```

Probe whether the finite residual is tied to named low H1 reciprocal residues:

```text
u = log K
Y_E(u) = log X_E,W(exp u) - mean_u log X_E,W(exp u)
Z_c(u) = sum_{gamma != 0} A_gamma W_hat(i gamma) exp(i gamma u)
A_gamma = 1 / L'(E,1+i gamma)      for simple offcentral zeros
```

The diagnostic question is:

```text
Do actual low H1 ordinates explain the finite proxy better than matched fake
ordinates, grid-comb frequencies, and endpoint/kernel controls?
```

The classifier does not test H2 branch damping and must not import any H2
`1/u` damping into H1 reciprocal-pole residues.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT12_EC_DIAGNOSTIC_THEORY_BRIDGE_2026-05-11.md`: Wave 4 diagnostic plan and thresholds.
- `primes-equispaced/handoff-2026-05-11-all-in-wave/EC_C2_PRIME_DIAGNOSTIC_PROTOCOL_2026-05-11.md`: fresh-seed C2-prime prerequisite and CV/Pareto gates.
- `primes-equispaced/handoff-2026-05-11-all-in-wave/EC_G3_FAILURE_DIAGNOSTIC_2026-05-11.md`: old G3 failed empirical p gates; no retroactive rescue.
- `primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md`: finite signed zero-filtering is diagnostic only and needs tail control outside this packet.
- `primes-equispaced/L2_facts/farey-claim-ledger.md`: current EC ledger; deterministic C2 passed, stochastic G3 failed, C2-prime is future-only, H1/H2 remain blockers.

## Predeclared Classifier

Return exactly one label:

```text
RESIDUE_DOMINATED_DIAGNOSTIC
FINITE_GRID_ARTIFACT_DIAGNOSTIC
NUMERICS_PAUSE
```

Prerequisite gate:

```text
C2-prime status = PASS
st_iid seeds = 512..1023
st_shared seeds = 128..255
script SHA256 recorded
AP cache SHA256 recorded
metadata SHA256 recorded
primary anchor reproduced to tolerance 5e-13
```

C2-prime pass requires:

```text
st_iid old_pass_rate <= 0.01
st_iid primary_pass_rate <= 0.005
st_iid p_cv <= 0.01
st_iid p_pareto <= 0.01

st_shared old_pass_rate <= 0.02
st_shared p_cv <= 0.02
st_shared p_pareto <= 0.02
```

Report `p_ratio` and additive `p_score`; do not use them as classifier gates.

Primary anchor:

```text
ratio = 1.3473754929960748
max_cv = 0.063297427334436704
old ratio cutoff = 1.42083
old CV cutoff = 0.08567129
```

Classifier rule:

```text
RESIDUE_DOMINATED_DIAGNOSTIC
  requires all reproducibility, C2-prime, actual-window spectral,
  actual-vs-fake filter, grid stability, dense-tail, and holdout clauses below.

FINITE_GRID_ARTIFACT_DIAGNOSTIC
  requires C2-prime PASS plus a reproducible result where fake windows,
  grid-comb windows, endpoint controls, or matched fake filters explain the
  finite proxy as well as actual H1 windows.

NUMERICS_PAUSE
  is returned for missing inputs, failed C2-prime, stale seeds, missing
  holdout metadata, AP-cache mismatch, dense-grid instability, or inconclusive
  actual/fake separation.
```

Quantitative residue/fake split:

```text
actual H1 window mass >= 0.60 * total low-band mass
actual H1 window mass >= 3.00 * best matched fake-window mass
actual filter median max_cv reduction >= 0.30
actual filter median abs(tail_slope) reduction >= 0.30
fake filter median max_cv reduction <= 0.10
fake filter median abs(tail_slope) reduction <= 0.10
post-filter abs(tail_slope) <= 0.03
```

Holdout residue split:

```text
all-holdout ratio < 1.42083
all-holdout max_cv < 0.08567129
rank 0 stratum ratio < 1.42083
rank 1 stratum ratio < 1.42083
rank 2 stratum ratio < 1.42083
each non-sentinel holdout CV < 0.08567129
5077a1 sentinel CV < 0.10
actual H1 filters beat matched fake filters on at least 10 of 15 non-sentinel holdouts
```

If the finite gate passes but the actual/fake split fails, return
`FINITE_GRID_ARTIFACT_DIAGNOSTIC`, not `RESIDUE_DOMINATED_DIAGNOSTIC`.

## Execution Protocol

1. Freeze provenance before fresh data:

```text
classifier spec SHA256
C2-prime runner SHA256
proxy runner SHA256
kernel-filter runner SHA256
AP cache SHA256
metadata SHA256
zero-list SHA256
base K grid
jitter K grid
dense K grid
holdout curve list
all thresholds in this packet
```

2. Verify the primary anchor:

```text
kernel = smoothstep
mode = all
alpha = 0.75
match = none
curves = 37a1,11a1,389a1
K grid = 1000,3000,10000,30000,100000,300000,1000000
ratio = 1.3473754929960748 +/- 5e-13
max_cv = 0.063297427334436704 +/- 5e-13
```

Failure returns `NUMERICS_PAUSE`.

3. Require C2-prime PASS on fresh seeds:

```text
st_iid seeds = 512..1023
st_shared seeds = 128..255
```

The existing all-in stochastic script starts at seed zero unless modified.
Therefore a valid C2-prime artifact must either use an explicit seed-list
runner or record seed-offset support before results are generated. Reusing the
old G3 seed block returns `NUMERICS_PAUSE`.

4. Build fixed grids:

```text
base grid = 1000,3000,10000,30000,100000,300000,1000000
jitter grid seed = 20260511
jitter rule = multiply each base K by exp(delta_j), delta_j in [-0.035,0.035],
              deterministic from the seed, rounded to distinct integers
dense replay grid = 12 points per decade from 1000 to 1000000, with base anchors forced
dense tail grid = 24 points per decade on [100000,1000000], with 300000 and 1000000 forced
```

If a later AP cache through `K=3000000` is hash-recorded before this classifier
runs, repeat dense-tail metrics on `[100000,3000000]`; otherwise do not
extrapolate beyond the cache.

5. Build actual H1 windows:

```text
curves = 37a1,11a1,389a1
J = 1,2,4,8
input per curve = first J positive offcentral H1 ordinates gamma_j
optional input = reciprocal weights 1/L'(E,1+i gamma_j)
window half-width = max(0.025, 0.10 * local nearest-neighbor gap)
low diagnostic band = [0, max_gamma_8 + 0.50]
```

If the first eight ordinates are unavailable for any training curve, return
`NUMERICS_PAUSE`.

6. Build matched fake windows before looking at spectral outcomes:

```text
shifted windows: gamma_j + 0.37
permuted windows: gamma_j from the other training curves
grid-comb windows: frequencies generated by pairwise differences in log K on the tested grid
```

Use the same window half-width and the same count `J` as the actual windows.

7. Compute spectral residual metrics:

```text
for each curve, grid, and J:
  compute Y_E(u)
  compute low-band spectral mass with the fixed estimator
  record actual-window mass
  record shifted-window mass
  record permuted-window mass
  record grid-comb-window mass
```

The fixed estimator may be Lomb-Scargle, least-squares sinusoid projection, or
direct Fourier projection, but it must be named and hash-recorded before the
run. Changing estimators after results returns `NUMERICS_PAUSE`.

Pass condition:

```text
actual mass >= 0.60 * total low-band mass
actual mass >= 3.00 * best fake mass
conditions hold on base, jitter, dense replay, and dense tail grids
```

8. Construct signed filters:

```text
W_hat(0) = 1
W_hat(i gamma_j) = 0 for j <= J
J = 1,2,4,8
```

For every actual filter, build matched fake filters with identical support
class, number of constraints, mass normalization, roughness budget, and
condition-number cap, but zeros at shifted, permuted, or grid-comb windows.

Filter feasibility gates:

```text
condition number <= 1e10
abs(W_hat(0)-1) <= 1e-10
max_j abs(W_hat(i gamma_j)) <= 1e-10
same numerical tolerances for fake filters
```

Failure returns `NUMERICS_PAUSE`.

9. Replay proxy under filters:

```text
datasets = training curves, holdout curves when metadata exists
grids = base, jitter, dense replay, dense tail
modes = filtered actual J=1,2,4,8 and matched fake J=1,2,4,8
metrics = ratio, max_cv, per-curve CV, tail_slope, endpoint_leverage
```

Residue-filter pass:

```text
actual-filter median max_cv reduction >= 30%
actual-filter median abs(tail_slope) reduction >= 30%
fake-filter median max_cv reduction <= 10%
fake-filter median abs(tail_slope) reduction <= 10%
actual improvement is nondecreasing from J=1 to J=8, allowing one tie
classification agrees on base, jitter, dense replay, and dense tail grids
post-filter abs(tail_slope) <= 0.03
```

10. Run holdouts only if exact metadata and AP caches are hash-recorded:

```text
rank 0: 14a1,15a1,17a1,19a1,20a1,21a1,24a1
rank 1: 43a1,53a1,57a1,58a1,61a1
rank 2: 433a1,446d1,571b1
rank 3 sentinel: 5077a1
```

Do not tune alpha, mode, kernel family, thresholds, or curve list after seeing
holdout values. Missing holdout metadata returns `NUMERICS_PAUSE`.

11. Emit the classifier report:

```text
label
all input hashes
C2-prime table
anchor reproduction table
actual/fake spectral table
actual/fake filter table
grid-stability table
holdout table
explicit stop/failure code when label = NUMERICS_PAUSE
```

## Promotion Guardrails

- C2-prime is future-only and cannot reclassify the failed G3 run.
- This classifier returns diagnostic labels only.
- Finite signed filtering removes finitely many named residues; it does not
  control the unfiltered H1 tail.
- A holdout pass is still finite numerical data.
- Do not use algebraic or script rank as analytic rank without a separate
  equality input.
- Do not attach BSD, `L(E,2)`, universality, or EC stabilization labels to
  any outcome.
- Do not replace failed actual/fake separation with larger K tuning.

## Stop Criteria

Return `NUMERICS_PAUSE` and stop EC numerical work on this lane if any item
occurs:

```text
C2-prime fails on fresh seeds
C2-prime uses old G3 seeds or unrecorded seed offsets
primary anchor fails 5e-13 reproduction
AP cache, metadata, zero list, or script hash is missing
first eight H1 ordinates are unavailable for a training curve
actual filters are infeasible or ill-conditioned
fake filters match or beat actual filters
actual-filter gains appear on base grid but fail on jitter or dense grids
grid-comb windows explain more mass than actual H1 windows
post-filter abs(tail_slope) > 0.03
holdout metadata is missing when holdout classification is attempted
proper ablations pass comparably to all-mode on holdouts
```

Reason to pause:

```text
Further K-grid or alpha tuning would optimize a finite proxy after the
stochastic, provenance, grid-stability, or residue-specificity question failed.
The live blockers would remain H1 reciprocal residues/PV/tails and H2 endpoint
closure.
```

## Dependency Impact

If output is `RESIDUE_DOMINATED_DIAGNOSTIC`:

- prioritize H1 reciprocal-residue, fixed-weight PV, and reciprocal-tail work;
- use the numerics only to identify which low zeros must be retained, killed,
  or modeled in a finite profile;
- keep rank-zero conclusions in oscillatory, averaged, or explicitly filtered
  form.

If output is `FINITE_GRID_ARTIFACT_DIAGNOSTIC`:

- stop EC finite-gate expansion on this proxy;
- treat the old smoothstep pass as endpoint/grid covariance behavior;
- require a new analytic observable before new holdout or larger-K
  compute.

If output is `NUMERICS_PAUSE`:

- spend no more compute on EC smoothing gates until the named failure is fixed;
- keep the theory queue on H1 legal-height reciprocal-pole control, H1
  fixed-weight PV, multiple-zero effective-degree handling, and H2 S1/Sym2
  endpoint closure.
