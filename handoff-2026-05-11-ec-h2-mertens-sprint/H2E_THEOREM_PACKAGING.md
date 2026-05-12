---
schema_version: 1
title: "H2-E theorem packaging for weakest useful smoothed EC-Mertens input"
date: 2026-05-11
type: theorem-template
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.64
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T2_STOCHASTIC_EULER_PRODUCT_MODEL.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
tags: [ec-ndc, h2, mertens, smoothing, theorem-template]
---

# H2-E Theorem Packaging

Status: `RIGOROUS_REDUCTION`

No theorem is promoted. The weakest useful H2 is a fixed-curve, fixed-kernel
smoothed EC-Mertens statement for the exact local factors in the Agent 3
reproducer:

```text
log P_E,W(K) = -r log log K + B_E,W + o(1),
```

where `r = ord_{s=1} L(E,s)` is the analytic rank. Replacing `r` by the
metadata/algebraic rank used in a script is an extra dependency, not part of
this packaging.

The slope-only statement

```text
log P_E,W(K) = -r log log K + O(1)
```

is useful as a diagnostic but is not enough to close the H1 composition. The
composition needs the finite part `B_E,W`.

## 1. Exact Object

Fix an elliptic curve `E/Q`. For each prime `p`, let `a_p` and the good/bad
reduction convention be exactly the reproducer convention.

At good primes:

```text
A_p(1) = 1 - a_p/p + 1/p.
```

At bad primes:

```text
A_p(1) = 1 - a_p/p.
```

For an admissible smoothing kernel `W`, define

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),
log P_E,W(K) = - sum_p W(p/K) log A_p(1).
```

This is the `P` factor in `X = zeta(2) * c * P / L2^rank` from the reproducer.
The H2 theorem concerns only `P`. The `L2` factor is absolutely convergent and
belongs to the separate T1 `H3` tail.

For the sprint's tested smoothstep kernel, with `0 <= alpha < 1`,

```text
W_alpha(t) = 1                                      for 0 <= t <= alpha,
W_alpha(t) = 1 - u^2(3 - 2u), u=(t-alpha)/(1-alpha) for alpha < t < 1,
W_alpha(t) = 0                                      for t >= 1.
```

## 2. Kernel Assumptions

The H2 template should allow the smoothstep and nearby monotone controls. A
safe admissible class is:

- `W:[0,infty) -> [0,1]`, compactly supported in `[0,1]`;
- `W(t)=1` on `[0,alpha]` for some `0 <= alpha < 1`;
- `W` is `C^1`, piecewise `C^2`, with `W(1)=W'(1)=0`;
- the Mellin transform

  ```text
  W_hat(z) = integral_0^infty W(t)t^(z-1) dt
  ```

  has a simple pole at `z=0` with residue `1`;
- on fixed vertical strips away from `z=0`,

  ```text
  W_hat(sigma+i tau) = O_W,sigma((1+|tau|)^(-2)).
  ```

For H2 specifically, also isolate the kernel prime-harmonic finite part:

```text
M_E,W^good = lim_{K -> infinity}
  (sum_{p good} W(p/K)/p - log log K),
```

if the limit exists. For fixed `E`, excluding finitely many bad primes only
changes the constant.

## 3. Local Expansion And Constants

At good primes set

```text
lambda_p = a_p / sqrt(p).
```

The exact logarithm decomposes as

```text
-log A_p(1)
  = a_p/p + (lambda_p^2 - 1)/(2p) - 1/(2p) + R_p,
```

where

```text
R_p = -log(1 - a_p/p + 1/p)
      - a_p/p
      - (a_p^2 - 2p)/(2p^2).
```

The `R_p` tail is absolutely summable under the usual Hasse-size local bound;
for this packaging it is a named proof obligation, not a cited theorem.

Define the required finite parts:

```text
C_E,W^trace = lim_{K -> infinity}
  (sum_{p good} W(p/K) a_p/p - (1/2 - r) log log K),

C_E,W^quad = lim_{K -> infinity}
  (1/2 * sum_{p good} W(p/K) (lambda_p^2 - 1)/p),

C_E^rem = sum_{p good} R_p,

B_E^bad = - sum_{p bad} log(1 - a_p/p).
```

Then the packaged constant is

```text
B_E,W =
  C_E,W^trace
  + C_E,W^quad
  - (1/2) M_E,W^good
  + C_E^rem
  + B_E^bad.
```

This is the bookkeeping that makes the `-r` coefficient visible:

```text
(1/2 - r) log log K - (1/2) log log K = -r log log K.
```

Any proof that skips either the trace term or the quadratic/symmetric-square
term has not derived the coefficient for the exact product.

## 4. Weakest Useful H2 Statement

**Theorem template H2-limit.** Let `E/Q` be fixed and let `r = ord_{s=1}L(E,s)`.
Let `W` be admissible. Assume:

1. The good-prime trace finite part `C_E,W^trace` exists with coefficient
   `(1/2 - r)`.
2. The quadratic finite part `C_E,W^quad` exists, with all symmetric-square or
   adjoint zero/pole terms accounted for.
3. The local remainder `C_E^rem` is absolutely convergent and the finitely many
   bad-prime factors use the same convention as the reproducer.
4. The kernel prime-harmonic finite part `M_E,W^good` exists.
5. Every offcentral zero, pole, and prime-shell term entering the explicit
   formula for the two non-absolutely-convergent sums is `o(1)` after the
   smoothed weighting, or cancels inside the displayed finite parts.

Then

```text
log P_E,W(K) = -r log log K + B_E,W + o(1),
```

with `B_E,W` as above. Equivalently,

```text
P_E,W(K) = exp(B_E,W) / (log K)^r * (1 + o(1)).
```

**Rate upgrade H2-eta.** If each hypothesis has error `O((log K)^(-eta))` for
some `eta > 0`, then

```text
P_E,W(K) = exp(B_E,W) / (log K)^r
           * (1 + O((log K)^(-eta))).
```

T1 only needs H2-limit for convergence, but H2-eta gives a usable numerical
rate.

## 5. Rank Cases

### Positive analytic rank `r >= 1`

H2 says `P_E,W(K)` decays like `(log K)^(-r)`. This is the product-side
counterweight to the T1 Perron-side leading term `(log K)^r / L^(r)(E,1)`.

The positive-rank case is the cleanest H1 composition because the central
Perron polynomial has a dominant top power, provided H1 already suppresses
offcentral reciprocal-zero residues below that scale.

### Rank zero `r = 0`

H2 says

```text
log P_E,W(K) = B_E,W + o(1).
```

This can be true while the full `c_E,W(K)P_E,W(K)` still fails to have a
pointwise limit. In rank zero the central term in `c_E,W(K)` is constant-scale,
so bounded offcentral reciprocal-zero residues from H1 are also constant-scale.

Closure for rank zero therefore requires the strong rank-zero H1 version:

```text
c_E,W(K) = 1/L(E,1) + o(1),
```

or an explicitly declared averaged theorem. A bounded almost-periodic remainder
is not enough.

### Script rank versus analytic rank

The reproducer uses `curve.rank` in the `L2^rank` denominator. The H2 theorem
uses analytic rank because the coefficient is a zero order of `L(E,s)`. Any
handoff claiming `-rank(E)` must specify whether rank is analytic, algebraic, or
verified equal for the finite curve list.

## 6. Dependencies And Proof Obligations

Minimum analytic obligations:

- Prove the trace Mertens finite part

  ```text
  sum_{p good} W(p/K) a_p/p
    = (1/2 - r) log log K + C_E,W^trace + o(1).
  ```

- Prove the quadratic/symmetric-square finite part

  ```text
  1/2 * sum_{p good} W(p/K)(lambda_p^2 - 1)/p
    = C_E,W^quad + o(1).
  ```

- Prove the universal harmonic term for the same `W`:

  ```text
  sum_{p good} W(p/K)/p = log log K + M_E,W^good + o(1).
  ```

- Prove `sum R_p` converges absolutely and that the smoothed tail tends to the
  unsmoothed full sum.

- Account for bad primes with the reproducer's exact local factor
  `1 - a_p/p`.

- Show the branch of `log A_p(1)` is real and consistent. The reproducer aborts
  on non-positive local factors; the theorem should exclude or prove away that
  case.

- Bound or cancel all offcentral zero terms. A term of the form

  ```text
  K^(rho-1) * W_hat(rho-1) * local_zero_factor
  ```

  with `Re(rho)=1` and `rho != 1` is not automatically `o(1)`. Smoothstep
  improves high-zero summability, but it does not by itself remove low-zero
  oscillation or control reciprocal derivatives.

- State whether the theorem is pointwise in `K`, logarithmically averaged, or
  restricted to a subsequence. The H1 composition needs pointwise H2 unless the
  final theorem is also averaged.

No external source is cited in this file. Any future citation closure must use
the sprint source protocol from the manifest.

## 7. Composition With H1

T1's positive-rank H1 target is

```text
c_E,W(K) =
  (log K)^r / L^(r)(E,1)
  + O((log K)^(r-delta))
```

after offcentral reciprocal-zero terms are controlled.

Combine it with H2-limit:

```text
P_E,W(K) =
  exp(B_E,W) / (log K)^r * (1 + o(1)).
```

Then, for `r >= 1`,

```text
c_E,W(K) P_E,W(K)
  = exp(B_E,W) / L^(r)(E,1) + o(1).
```

With the T1 `H3` tail for the absolutely convergent `L2` product, the reproduced
full proxy would have the fixed-curve asymptotic

```text
X_E,W(K)
  = zeta(2) * exp(B_E,W)
    / (L^(r)(E,1) * L(E,2)^r)
    + o(1),
```

provided the exponent `r` in `L2^r` is the same rank used in H2.

This is a fixed-curve theorem. It does not imply cross-curve universality or
explain why the three training curves have close means.

## 8. What Would Count As Closure

H2 closure requires one of the following:

- A self-contained proof of the H2-limit theorem above for the exact local
  factors and the smoothstep admissible class.
- A source-verified theorem audit proving the same statement, including exact
  local factors, smoothing kernel, bad primes, rank convention,
  symmetric-square/adjoint terms, and offcentral zero terms.
- A narrower but complete theorem for one fixed `E` and one fixed predeclared
  kernel, preferably `W_0.75`, with the same constant bookkeeping.

Operational closure checklist:

- `B_E,W` is defined as a finite part and all pieces are proved to exist.
- The coefficient of `log log K` is derived as `-r`, not fitted.
- Rank zero is separated and does not borrow positive-rank cancellation.
- The theorem says pointwise, averaged, or subsequence, and H1 uses the same
  mode.
- Numerical H2 diagnostics on the saved curves do not contradict the predicted
  slopes for ranks `0`, `1`, and `2`.
- The statement remains true with the Agent 3 local factors, not a nearby
  completed or normalized Euler product.

## 9. What Would Falsify H2

Any of these would falsify the H2-limit statement as packaged:

- For the exact Agent 3 `P`, a larger/dense `K` diagnostic shows

  ```text
  log P_E,W(K) + r log log K
  ```

  has persistent drift instead of approaching a finite part.

- The fitted slope of `log P_E,W(K)` against `log log K` converges to a value
  different from `-r` for a fixed predeclared curve/kernel.

- A rank-zero curve shows nonzero logarithmic drift in `log P_E,W(K)`.

- A positive-rank curve shows the wrong rank coefficient after exact bad-prime
  and quadratic terms are included.

- The quadratic/symmetric-square term contributes an additional uncancelled
  `c log log K`.

- Offcentral zero terms produce a non-decaying almost-periodic component in
  `log P_E,W(K) + r log log K`.

- The theorem only works after changing local factors, smoothing `L2`, fitting
  alpha after inspection, or replacing pointwise convergence by averaging
  without saying so.

Failure of cross-curve universality does not falsify H2. H2 is a fixed-curve
Mertens input; universality is a separate claim.
