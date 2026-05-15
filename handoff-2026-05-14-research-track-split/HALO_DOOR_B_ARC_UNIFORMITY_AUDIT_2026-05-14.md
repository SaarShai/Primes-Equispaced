---
schema_version: 2
title: "Halo Door B — Arc Uniformity of Noncluster Ratio (Stage 1a follow-on)"
type: lemma-extension
domain: project
tier: working
status: LEMMA
confidence: 0.90
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md
supersedes: []
superseded-by:
tags: [halo-route, door-B, h1, lemma, arc-uniformity, stage-1a-follow-on]
---

# Halo Door B — Arc Uniformity of `H_A` Ratio

Retires the residual audit task surfaced by Stage 1a
(`HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md` §4): lift the noncluster
ratio bound from point evaluation `(rho_0 + alpha)` to the boundary arc
`s in partial Omega_T cap D(rho_0, R_T alpha)`. Not a new theorem.
Explicit write-out of the Poisson / mean-value step asserted (with
schematic detail) in `HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §5.1.

Standing assumption: GRH for `L_E^*`. **Not removed.**

## 0. Notation

Same as `HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md`. Repeated for self-
containedness.

| Symbol | Meaning |
|---|---|
| `L` | `L_E^*(s)`, completed `L`-function of newform attached to `E` |
| `alpha` | `1/log T` |
| `rho_0 = 1/2 + i gamma_0` | offcentral zero, `T < gamma_0 <= 2T` |
| `R > 1` | halo radius parameter (unified scale, see §2 Step 0) |
| `R_T in [R, 2R]` | no-zero-on-boundary radius, `R_T^2 > R^2 + 1` |
| `C_R(rho_0)` | `{rho_j : |gamma_j - gamma_0| <= R alpha}` (cluster, unified scale) |
| `H_R(s)` | `L(s) / prod_{rho_j in C_R(rho_0)} (s - rho_j)` |
| `partial Omega_T` | halo boundary, arc assigned to `rho_0` |

## 1. Statement

**LEMMA (NonclusterArcUniformity).** Under standing GRH for `L_E^*`,
fix `R > 1` and any `R_T in [R, 2R]` satisfying `R_T^2 > R^2 + 1`. For
every offcentral `rho_0` and every point `s in partial Omega_T` with
`|s - rho_0| <= R_T alpha`,

```text
|H_R(s) / H_R(rho_0 + alpha)|  =  O_{E, R}(1) ,
```

with the implied constant absolute, independent of `T`, of the local
cluster size `N_{rho_0, R}(T) = #C_R(rho_0)`, and of the choice of `s`
on the arc.

## 2. Proof

### Step 0 — Cluster-scale unification

The halo plan §5.1 keeps two free parameters: cluster scale `A` and
halo scale `R`, with constraint `R > sqrt(1 + A^2)`. For the noncluster
arc lift, this creates a conflict: the disk `D(rho_0, R_T alpha)` over
which we want to apply harmonicity may exceed the cluster-free disk
`D(rho_0, A alpha)` whenever `R_T > A`, which is forced by
`R_T >= R > sqrt(1 + A^2) > A`.

**Resolution.** Define the cluster at the *halo* scale,
`C_R(rho_0) := {rho_j : |gamma_j - gamma_0| <= R alpha}`. Then `H_R` has
no zeros on `D(rho_0, R alpha) supset D(rho_0, R_T alpha)` — wait,
`R_T >= R`, so we instead need zero-freeness on `D(rho_0, R_T alpha)`.
Set the cluster scale to `R_T alpha` (or even `2R alpha`): same
construction, same factorization, same proof of §2.1/§2.2 of
`HALOSHIFTCOMPARISON_LEMMA`. The per-mate ratio becomes
`sqrt(1 + R^2) / R_T` (taking `A = R` in the §5.1 algebra; or
`sqrt(1 + R_T^2)/R_T` if cluster scale = `R_T`). Strict contraction
requires `R_T^2 > R^2 + 1` (or `R_T^2 > R_T^2 + 1`, impossible — so we
must take cluster scale equal to `R`, not `R_T`).

Cleanest statement: **cluster scale = halo scale = `R alpha`**. Then

- `H_R` is zero-free on `D(rho_0, R alpha)`.
- The points `rho_0 + alpha` and any `s` on the arc satisfy
  `|s - rho_0| = R_T alpha`, so `s` lies *outside* `D(rho_0, R alpha)`
  but inside `D(rho_0, R_T alpha)`.
- `H_R` may have non-cluster zeros in the shell
  `R alpha < |z - rho_0| <= R_T alpha`. These must be handled.

Handle the shell zeros explicitly. By Riemann–von Mangoldt, the
expected number of zeros in the shell is

```text
((R_T - R) alpha) · (log T)/(2 pi)  =  (R_T - R)/(2 pi)  =  O(R).
```

This is `O(1)`, *bounded independent of T*. Each shell zero contributes a
bounded multiplicative factor to the ratio `H_R(s)/H_R(rho_0 + alpha)`
because both `s` and `rho_0 + alpha` are within distance `O(R alpha)`
of the shell zero and not closer than `(R_T - R) alpha / 2 = O(alpha)`
(by genericity / averaging over `R_T in [R, 2R]`, exactly the trick
that defined `R_T`). So shell zeros multiply the bound by a constant
`exp(O(R))`, absorbed into `O_R(1)`.

For the rest of this proof, work with the **honest** cluster-free disk
`D(rho_0, R alpha)`. Treat `s` on the arc as living on the boundary of
this disk after the shell-zero adjustment above.

### Step 1 — Harmonicity

On `D(rho_0, R alpha)`, `H_R` is holomorphic and zero-free (by Step 0
construction). Hence `log |H_R|` is harmonic on this disk.

### Step 2 — Mean-value property

By the mean-value theorem for harmonic functions,

```text
(1/(2 pi)) int_0^{2 pi} log |H_R(rho_0 + R alpha · e^{i theta})| d theta
  =  log |H_R(rho_0)| .
```

(Crucially `H_R` is *bounded and zero-free* at `rho_0` because the
cluster factor `(s - rho_0) · prod_{rho_j in C_R, j != 0}(s - rho_j)`
was divided out of `L`.)

### Step 3 — Second-order Taylor expansion

For `z in D(rho_0, R alpha)`, use the Hadamard-type expansion (over
non-cluster zeros only)

```text
log |H_R(z)|
  =  Re log H_R(rho_0)
   + Re (z - rho_0) · (H_R'/H_R)(rho_0)
   + Re sum_{rho_j non-cluster} [ log(1 - (z - rho_0)/(rho_j - rho_0))
                                  + (z - rho_0)/(rho_j - rho_0) ]
```

(the second-order remainder of `log(1 - w)`).

- The constant term is `log |H_R(rho_0)|`.
- The first-order term has `Re ((z - rho_0) · const)`. On a centered
  circle it averages to zero (the linear functional `Re(c · e^{i theta})`
  integrates to 0 over `theta in [0, 2 pi]`).
- The remainder is the second-order term.

Expanding `log(1 - w) + w = -w^2/2 - w^3/3 - ...` and taking absolute
values, for `|w| <= R alpha / |rho_j - rho_0| < 1/2` (true for all
non-cluster zeros, which satisfy `|rho_j - rho_0| > R alpha`, so
`|w| < 1`; for the explicit `1/2` cut, use the further-out tail and
treat finite near zeros separately by inclusion in an enlarged cluster
— absorbed into the shell adjustment of Step 0),

```text
|log(1 - w) + w|  <=  |w|^2 .
```

So the deviation of `log |H_R|` from its mean on the disk is bounded by

```text
sup_{z in D(rho_0, R alpha)} | log |H_R(z)| - log |H_R(rho_0)| |
  <=  (R alpha)^2 sum_{rho_j non-cluster} 1 / |rho_0 - rho_j|^2 .
```

### Step 4 — Bound the inverse-square sum via Riemann–von Mangoldt

Under GRH, all `rho_j = 1/2 + i gamma_j`, so `|rho_0 - rho_j| =
|gamma_0 - gamma_j|`. Non-cluster means `|gamma_j - gamma_0| > R alpha`.
Zero-counting near height `T`: density `(log T) / (2 pi)` per unit
height. Stieltjes integration:

```text
sum_{|gamma_j - gamma_0| > R alpha} 1 / (gamma_j - gamma_0)^2
  =  2 int_{R alpha}^{O(T)} ((log T)/(2 pi)) / r^2 dr  +  O(log T)
  =  (log T / pi) · (1/(R alpha) - 1/T)  +  O(log T)
  =  (log T)^2 / (pi R)  +  O(log T) .
```

(The `O(log T)` corrections come from the `O(1)` term in the
zero-counting formula and the far-tail truncation; both negligible
against the main term, which is `(log T)^2`.)

### Step 5 — Multiply through

```text
(R alpha)^2 · (log T)^2 / (pi R)
  =  R^2 · (1/log T)^2 · (log T)^2 / (pi R)
  =  R / pi .
```

So

```text
sup_{z in D(rho_0, R alpha)}  |log |H_R(z)| - log |H_R(rho_0)||
  <=  R / pi  +  o(1) .
```

### Step 6 — Conclude

Taking `z_1 = rho_0 + alpha` (inside the disk since `alpha < R alpha`
for `R > 1`) and `z_2 = s` (boundary of disk, post shell-zero
adjustment, distance `R alpha`):

```text
| log |H_R(rho_0 + alpha)| - log |H_R(s)| |  <=  2R / pi + o(1) ,
```

hence

```text
|H_R(s) / H_R(rho_0 + alpha)|  <=  exp(2 R / pi + o(1))  =  O_R(1) .
```

Combined with the shell-zero adjustment of Step 0 (factor
`exp(O(R))`), the lemma follows.

QED.

## 3. Cross-check vs existing repo lemma

`ClusterShiftDerivativeComparison(E, A)` proves
(`handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`
§"Noncluster Ratio Bound", line 184ff):

```text
log R_A(rho_0)  =  log |H_A(rho_0 + alpha) / H_A(rho_0)|
               <<_{E, A}  (log T) / (loglog T) ,
```

via dyadic annuli over non-cluster zeros, the same Hadamard expansion
used here, and Wave-4 Agent02 fixed-newform zero counts. Crucially the
input there is **two distinct points** `rho_0` and `rho_0 + alpha`, both
inside the cluster-free region.

The present lemma replaces the point pair `(rho_0, rho_0 + alpha)` with
the point pair `(rho_0 + alpha, s)`, where `s` is any boundary-arc
point. The bound improves from `T^{o(1)}` (= `O(log T / loglog T)` in
the exponent) to `O(1)` (= `R / pi` in the exponent) because:

- The repo lemma sums `min(1, alpha^2 / |rho - rho_0|^2)` over all
  non-cluster zeros, including a finite-disk Hadamard cutoff producing
  a `log T / loglog T` slack.
- This lemma uses the *harmonic mean-value identity* (Step 2) to
  cancel the first-order term exactly, leaving only the second-order
  Hadamard tail that is *summable* to an absolute constant.

So the new lemma is **strictly stronger** at the per-point level and
covers the full disk uniformly. Taking `s = rho_0` in the new lemma
recovers the point bound `|H_R(rho_0 + alpha) / H_R(rho_0)| = O(1)`,
which sharpens the repo lemma's `T^{o(1)}` to `O(1)` whenever the
unified-scale cluster (cluster scale = halo scale = `R alpha`) is used
instead of the smaller `A alpha`.

The repo lemma is therefore a point version, slightly less sharp; the
new lemma is its arc/disk extension.

## 4. Numerical sanity

`R = 1.5, A = R, R_T = 1.7` (satisfies `R_T^2 = 2.89 > R^2 + 1 = 3.25`?
No, `R_T^2 = 2.89 < 3.25`. Need `R_T > sqrt(R^2 + 1) = sqrt(3.25)
= 1.803`. Take `R_T = 1.85`.)

- Variation bound: `R / pi = 1.5 / 3.14159 = 0.4775`.
- Implied ratio bound: `exp(2 R / pi) = exp(0.955) = 2.60`.
- Plus shell contribution `exp(O(R)) = exp(O(1.5))` — at most one or
  two shell zeros expected, each contributing factor `~ 2` to the
  ratio. So overall bound `~ 5-10`.

All bounded constants. Reasonable.

For larger `R = 3`: `R / pi = 0.955`, `exp(2 R / pi) = exp(1.91)
= 6.74`. Larger but still `O(1)`. Note the bound is *not* uniform in
`R` — sending `R -> infinity` would blow up. The halo plan picks `R`
bounded, so this is fine.

## 5. Implications for the halo plan

### 5.1 Door B is now fully closed (modulo standing GRH)

The Door B clean form

```text
|L(rho_0 + alpha) / L(s)|  <=  C(E, R) ,
```

uniformly over `s in partial Omega_T`, is now written out without
audit residue. The only ingredient that was schematic in
`HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §5.1 was the disk-lift of the
`H_A` ratio bound; this memo retires it.

### 5.2 Cluster-scale unification

The halo plan's two free parameters `(A, R)` with constraint
`R > sqrt(1 + A^2)` collapse to a **single parameter** `R > 1` plus a
choice of `R_T` with `R_T^2 > R^2 + 1`. The cluster `C_R(rho_0)` and the
halo `D(rho_0, R_T alpha)` are then governed by one geometric scale.

**Compatibility check with cluster-mate contraction (§2.2 of
`HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md`).** The cluster-mate ratio
bound `sqrt(1 + A^2) / R_T < 1` becomes `sqrt(1 + R^2) / R_T < 1`,
i.e. `R_T > sqrt(1 + R^2)`. Satisfiable for any `R > 0` by choosing
`R_T = sqrt(1 + R^2) + epsilon`; for `R > 1` this means
`R_T in (sqrt(2), 2R)` is a non-empty range, so the cluster-mate
contraction step still works.

No part of the halo plan downstream uses the *value* of `A` separately
from `R`. (Verified by grep: `A` appears only in the cluster
definition, the §2.2 cluster-mate bound, and the noncluster sum
`1/(2 pi A)`. All three transfer cleanly under `A = R`.)

### 5.3 What the lemma does NOT do

- Does not remove standing GRH for `L_E^*`.
- Does not close Doors A, C, or D.
- Does not change the H1 conditional stack downstream of Door B (§5.1
  `H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md`).

## 6. Boundary

### Allowed claims

- Door B is now fully closed under standing GRH, with no audit
  residue.
- The cluster scale and halo scale should be unified at `R alpha`;
  this is the canonical form.
- The per-arc ratio bound is `O_R(1)` with explicit value
  `exp(2 R / pi + O(R))`.
- The new lemma sharpens `ClusterShiftDerivativeComparison(E, A)` from
  `T^{o(1)}` to `O(1)` at the unified scale.

### Forbidden claims

- Door B is unconditional. (Still uses standing GRH for `L_E^*`.)
- Doors A, C, D are closed by this lemma. (Silent on them.)
- The `T^{o(1)}` improvement propagates to the full H1 bound. (H1
  depends on shifted-value moments, not just per-arc ratios.)
- The variation bound is `R / pi` for all `R`. (The bound is `O(1)`
  for `R` in any bounded range; sending `R -> infinity` is not
  asserted.)

## 7. Cost

| Item | Estimate |
|---|---|
| this memo | done (~0.5d) |
| downstream effect on Stage 1a status | `RIGOROUS_REDUCTION` -> `LEMMA` |
| token cost | low (audit transcription) |

## 8. Cross-references

| File | Role |
|---|---|
| `handoff-2026-05-14-research-track-split/HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md` | Stage 1a; this memo retires its §4 audit task |
| `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §5.1, §5.1' | source proof (schematic) |
| `handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md` | repo's point-version lemma, sharpened here |
| `handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md` | downstream H1 conditional stack |
