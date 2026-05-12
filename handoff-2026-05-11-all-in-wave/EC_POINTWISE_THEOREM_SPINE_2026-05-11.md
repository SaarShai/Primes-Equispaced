---
schema_version: 1
title: "EC pointwise theorem spine after H1 legal-height refinement"
date: 2026-05-11
type: theorem-reduction
tier: working
status: CONDITIONAL_SPINE_NO_THEOREM_PROMOTED
confidence: 0.82
sources:
  - handoff-2026-05-11-all-in-wave/H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H2_SYM2_ENDPOINT_PACKET_2026-05-11.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_SYM2_PRODUCT_AVERAGE_PACKAGE.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
tags: [ec-ndc, h1, h2, pointwise, theorem-spine]
---

# EC Pointwise Theorem Spine

status: `CONDITIONAL_SPINE_NO_THEOREM_PROMOTED`

## Verdict

No EC fixed-curve theorem is promoted.

The current positive-rank pointwise theorem path is now a clean conditional
spine:

```text
H1 legal-height reciprocal-pole control
+ H2 S1/Sym2 finite-part closure
+ same W, same pointwise mode
=> c_E,W(e^u) P_E,W(e^u) -> exp(B_H2(E,W))/L^(r)(E,1).
```

For the full Agent-3 proxy, add only after separate `H3` closure:

```text
zeta(2) exp(B_H2(E,W)) / (L^(r)(E,1) L(E,2)^r).
```

All ranks here are analytic ranks:

```text
r = ord_(s=1) L(E,s).
```

No algebraic/script rank substitution is allowed without a separate equality
input.

## Conditional Pointwise Theorem

Fix a curve `E/Q`, positive analytic rank `r>=1`, and the same admissible
endpoint-smoothed kernel `W` in H1 and H2. Put `u=log K`.

Assume H1:

```text
c_E,W(e^u)
 = u^r/L^(r)(E,1) + o(u^r).
```

A sufficient current H1 package is:

1. finite-box reciprocal Perron identity for the chosen `W`;
2. source-safe start line `sigma>1/2`, smoothstep-scale `q=2`, and legal
   moving heights `T_box(u)~exp(Cu)` with `C>sigma`;
3. `H-left` via `eta>1/2` and horizontal height input via the conditional
   Li-Zaharescu selected-height mechanism;
4. simple offcentral zeros satisfy the legal-height rank threshold

   ```text
   R_E,1(T)=o(T^2(logT)^(r-1));
   ```

5. every multiple-zero effective residue degree is `<r`, or else the term is
   cancelled, kernel-killed, explicitly retained, or the theorem mode is
   changed to profile/average.

Assume H2:

```text
P_E,W(e^u)=exp(B_H2(E,W)) u^(-r)(1+o(1)).
```

A sufficient current H2 package is:

1. exact local algebra for Agent-3 good and bad factors;
2. S1 branch finite part

   ```text
   S1_W(e^u)
    = (1/2 + kappa_sym/2 - r) log u + C1_E,W + o(1);
   ```

3. exact good-prime Sym2 finite part

   ```text
   Ssym_W(e^u) = -kappa_sym log u + Csym_E,W + o(1);
   ```

4. weighted good-prime Mertens finite part for the same `W`;
5. absolutely convergent good-prime `m>=3` local-log tail and finite bad-prime
   constant;
6. branch/zero summability and contour tails strong enough to make all H2
   offcentral branch terms `o(1)`.

Then multiplication gives

```text
c_E,W(e^u)P_E,W(e^u)
 = (u^r/L^(r)(E,1)+o(u^r))
   exp(B_H2(E,W))u^(-r)(1+o(1))
 -> exp(B_H2(E,W))/L^(r)(E,1).
```

This theorem is conditional because neither the H1 reciprocal-derivative
threshold nor the H2 endpoint finite-part package is source-closed.

## Rank-One Target

For analytic rank `r=1`, the simple-zero H1 target is especially sharp:

```text
R_E,1(T)=o(T^2).
```

Any log saving,

```text
R_E,1(T) <= C T^2/(log T)^delta,   delta>0,
```

is sufficient for the simple-zero weighted-l1 part along legal exponential
heights. This is weaker than absolute convergence of the full residue series,
which needs the stronger `T^2(logT)^(-1-delta)` style target.

## What H2 Does And Does Not Buy

H2 branch calculus damps offcentral zero terms by `1/u`:

```text
rho=1+i gamma
  -> K^(i gamma) W_hat(i gamma)/u.
```

This can make H2 pointwise nonoscillatory after weighted branch summability.

H1 is different. The same zero is a reciprocal pole:

```text
rho=1+i gamma
  -> K^(i gamma) W_hat(i gamma)/L'(E,rho)
```

for a simple zero. There is no `1/u` damping. Therefore H1 must be closed by
reciprocal-derivative/l1/PV/profile input, not by importing H2 branch damping.

## Rank Zero

Rank zero is not covered by the pointwise theorem spine.

The honest H1 shape is

```text
c_E,W(e^u)=1/L(E,1)+Z_c(u)+o(1),
```

unless every retained nonzero H1 residue is killed, cancelled, subtracted, or
proved `o(1)`. Use the conditional arithmetic product-average theorem or an
explicit oscillatory profile for rank zero.

## Minimal Closure Queue

Shortest current route to a positive-rank pointwise theorem:

1. Close H2 S1 branch continuation for the endpoint-smoothed fixed `W`.
2. Close exact good-prime Sym2 finite part for
   `chi_sym2(p)=a_p^2/p-1`, including the `kappa_sym` convention/value.
3. Close weighted good-prime Mertens transfer for the same `W`.
4. Close H1 finite-box reciprocal Perron tails in the legal exponential-height
   mode.
5. Prove the H1 simple-zero threshold

   ```text
   R_E,1(T)=o(T^2(logT)^(r-1)).
   ```

6. Handle multiple offcentral zeros by effective degree `<r`, cancellation,
   filtering, retention, or averaging.
7. Add the absolutely convergent `L(E,2)^r`/`zeta(2)` normalization only after
   the separate `H3` tail is stated.

Every external theorem used to close any item above still needs the repository
source protocol: `curl + pdftotext`, short quote, and page/equation.

## No-Promotion Line

Do not claim:

- fixed-curve EC stabilization;
- unconditional EC product average;
- rank-zero pointwise stabilization;
- H1 residue control from H2 branch damping;
- `kappa_sym=0` without checking the exact good-prime Sym2 object;
- BSD, `L(E,2)`, or cross-curve universality evidence from the finite EC
  smoothing numerics.
