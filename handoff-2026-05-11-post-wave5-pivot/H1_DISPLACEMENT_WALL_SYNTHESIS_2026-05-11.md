---
schema_version: 2
title: "H1 Displacement Wall Synthesis"
type: synthesis
domain: project
tier: working
confidence: 0.86
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-implementation-wave/H1_Q_GT_2_BAD_SET_ROUTE_2026-05-11.md
  - arxiv:1306.0854
  - arxiv:2310.03949
  - Rudnick-Sarnak 1996, Zeros of principal L-functions and random matrix theory
  - Hejhal 1994, triple correlation of zeros of the zeta function
  - Vaaler 1985, extremal functions in Fourier analysis
supersedes: []
superseded-by:
tags: [post-wave5, h1, displacement, palm, rooted-box, q3, bad-set, source-gap]
---

# H1 Displacement Wall Synthesis

Status: `WALL_NARROWED_NOT_BROKEN`.

No H1 theorem is promoted.

## Verdict

The serious displacement push did not produce a source-closed theorem. It did
break the fog around the obstruction.

The old hard blocker was the square Palm statistic at `q=2`. The new exact
wall is the weaker rooted small-box/inverse-product theorem

```text
PrimeScaleRootedPalmBox_beta(E,A;W),      beta > p,
```

with `p=q/(q-1)`. The best concrete choice is

```text
q = 3,        p = 3/2.
```

If the shifted negative moment and rooted box law both hold in this range, the
bad simple-zero branch has the power saving

```text
R_B(T,c) << T^(11/6+epsilon+o(1)).
```

Together with the separated branch, this closes the rank-one simple-zero H1
budget. Full H1 still separately requires multiple-zero disposition and the
finite-box contour hypotheses.

## What Is Actually Proved In-Repo

The following reduction is rigorous inside the current packet stack:

```text
ClusterShiftDerivativeComparison
+ Degree2WeakShiftedNeg_q(E)
+ RootedInvProdCorr_p(E,A)
=> R_B(T,c) << T^(2 - 1/(2q) + epsilon + o(1)).
```

The cluster input may be expanded as

```text
J_m^(p)(T;A)
 =
 sum_(rho0 in S_E(T))
 sum_(rho1,...,rhom distinct; 0<u_j<=A)
   prod_(j=1)^m u_j^(-p),

u_j = log T * |rho_j-rho0|.
```

A sufficient all-cluster condition is

```text
sum_(m>=1) C_A^m/m! * J_m^(p)(T;A) <<_(E,A,p) T log T.
```

Equivalently, a rooted box law with summable constants:

```text
nu_m,T^W(prod_j (0,r_j])
  <= C_m T log T prod_j r_j^beta,

sum_m K_A^m C_m/m! < infinity,
beta > p.
```

## Why The Obvious Routes Fail

1. Restricted n-level density does not prove the box law.

   Beurling-Selberg majorants for intervals `(0,r]` need bandwidth
   `Delta ~ 1/r` to see shrinking mass. Rudnick-Sarnak/Hejhal-style restricted
   support keeps the legal bandwidth bounded. With bounded bandwidth, the
   majorant has a fixed uncertainty floor and gives no useful decay as
   `r -> 0`.

2. Pair repulsion is only the first layer.

   The sine-kernel rooted Palm model gives

   ```text
   rho_1^Palm(u) = 1 - sinc(pi u)^2
                 = (pi^2/3)u^2 + O(u^4),
   ```

   so pair box mass is cubic:

   ```text
   int_0^r rho_1^Palm(u) du = (pi^2/9)r^3 + O(r^5).
   ```

   This would beat `p=3/2`, but it controls only `m=1`. H1 needs all rooted
   cluster layers with summable constants.

3. Finite cluster truncation is just the same wall renamed.

   A hard cap

   ```text
   n_A(rho) <= M
   ```

   plus `J_m^(3/2) << T log T` for `1<=m<=M` would suffice. No checked source
   gives such a cap for near-root clusters at scale `1/log T`. Without it, the
   high-mate tail is exactly the missing Palm summability.

4. Direct reciprocal-tail bypass is harder, not easier.

   A Palm-free route would need, for some `p>1`,

   ```text
   sum_(T<|gamma|<=2T) |L'(E,rho)|^(-p)
     = o(T^(p+1)/(log T)^(p-1)).
   ```

   No checked fixed-GL2/EC source supplies this. Existing adjacent sources cover
   separated zeta zeros, positive/shifted moments, simple-zero existence, or
   lower bounds in the wrong direction.

## The Model Crack

In the sine-kernel determinantal model, the rooted Palm process has Schur
complement kernel

```text
K^0(x,y) = S(x-y) - S(x)S(y),
```

and

```text
K^0(u,u) = 1 - S(u)^2 ~ (pi^2/3)u^2.
```

Hadamard bounds then give coordinatewise cubic box decay. For higher `m`, the
local density near the root has the form

```text
C_m prod_j u_j^2 prod_(i<j)(u_i-u_j)^2,
```

so the conjectural model easily gives `beta=3`, more than enough for the
`q=3,p=3/2` route.

The missing analytic theorem is not conceptual. It is the transfer from this
model behavior to one fixed EC/GL2 zero process with uniform shrinking-box
control and summable rooted cluster constants.

## Mainline Task

Promote one task, not a theorem:

```text
H1-RootedPalmBox_q3(E,A;W):
  prove PrimeScaleRootedPalmBox_beta(E,A;W)
  for some beta>3/2, all rooted cluster sizes, summable constants,
  at normalized scale 1/log T.
```

Parallel supporting task:

```text
Degree2WeakShiftedNeg_3-Audit(E):
  source-close or isolate the exact BFMT/DPMV gap for
  sum |L_E^*(rho+1/logT)|^(-3) << T^(7/2+epsilon).
```

## Boundary

Allowed to claim now:

```text
The H1 displacement method reduces the bad simple-zero branch to
Degree2WeakShiftedNeg_3(E) plus H1-RootedPalmBox_q3(E,A;W).
```

Not allowed to claim:

```text
RootedPalmBox_q3 is known.
Restricted n-level density implies the needed singular rooted law.
Pair repulsion alone closes H1.
Direct reciprocal tails are source-closed.
Full H1 follows without multiple-zero and contour hypotheses.
```

Confidence: `0.86` that this is the correct present boundary; `0.12` that
current literature already contains the fixed-EC rooted box theorem in the
needed all-cluster, shrinking-box form.
