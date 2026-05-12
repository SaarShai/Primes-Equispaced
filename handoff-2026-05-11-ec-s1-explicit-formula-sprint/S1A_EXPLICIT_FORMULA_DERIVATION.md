---
schema_version: 1
title: "S1-A smoothed explicit formula derivation for the EC trace sum"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.73
sources:
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
tags: [ec-ndc, s1, explicit-formula, smoothed-mertens, trace-sum]
---

# S1-A Explicit Formula Derivation

status: `RIGOROUS_REDUCTION`

No theorem is promoted. Under the exact local normalization from Agent 3, the
smoothed trace sum

```text
S_1,W(K) = sum_p W(p/K) a_p/p
```

has a Mellin explicit formula whose offcentral `L(E,s)` zeros contribute

```text
K^(rho-1) W_hat(rho-1) / log K
```

not a persistent `K^(rho-1)` term, provided the prime-linear Dirichlet series
has only logarithmic branch singularities there and the weighted zero series is
summable. Persistent oscillations belong to pole singularities, for example the
`-L'/L` level before removing the `log p` weight, or to any unaccounted
companion factor that introduces a pole in the prime-linear series itself.

Thus the S1 fork resolves as:

```text
pointwise lower-order offcentral zeros, conditional on branch-type singularities
and a zero-summability/contour hypothesis.
```

Without those hypotheses, the claim-safe output remains a rigorous reduction,
not a closed H2 theorem. Averaging is a fallback only if the zero aggregate
cannot be made pointwise summable or if pole terms persist from another factor.

## 1. Exact Local Normalization

Agent 3 computes

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),
log P_E,W(K) = -sum_p W(p/K) log A_p(1).
```

At good primes:

```text
A_p(1) = 1 - a_p/p + 1/p.
```

At bad primes, exactly as in the reproducer:

```text
A_p(1) = 1 - a_p/p.
```

The reproducer uses the real logarithm and aborts if these local factors are
non-positive. Bad primes are finite. For S1 they contribute only

```text
S_1,W^bad(K) = sum_{p bad} W(p/K) a_p/p
             = C_1^bad + o(1),
C_1^bad      = sum_{p bad} a_p/p,
```

for any admissible `W` with `W(t) -> 1` as `t -> 0`. All nontrivial asymptotic
work is at good primes.

At good primes write

```text
1 - a_p p^(-s) + p^(1-2s)
  = (1 - alpha_p p^(-s))(1 - beta_p p^(-s)),
alpha_p + beta_p = a_p,
alpha_p beta_p = p.
```

The good-prime logarithm is

```text
log L_good(E,s)
 = sum_p_good sum_{m>=1} (alpha_p^m + beta_p^m)/(m p^(ms)).
```

Put `s=1+z` and define

```text
A_E(z)      = sum_p_good a_p p^(-1-z),
chi_sym2(p) = a_p^2/p - 1,
B_E^sym(2z)= sum_p_good chi_sym2(p) p^(-1-2z),
M_good(2z) = sum_p_good p^(-1-2z).
```

Then, in the initial half-plane of absolute convergence and thereafter by the
assumed continuation,

```text
log L_good(E,1+z)
 = A_E(z)
   + (1/2) B_E^sym(2z)
   - (1/2) M_good(2z)
   + H_E(z),
```

where `H_E(z)` is the locally analytic contribution from `m >= 3` and any
remaining absolutely convergent good-prime terms. Therefore

```text
A_E(z)
 = log L_good(E,1+z)
   - (1/2) B_E^sym(2z)
   + (1/2) M_good(2z)
   - H_E(z).
```

This identity is the required starting point. It fixes the central coefficient
in analytic-rank language before any numerical rank is used.

Let

```text
r = ord_{s=1} L(E,s).
```

If

```text
L(E,1+z) = lambda_E z^r (1 + O(z)), lambda_E != 0,
```

and the symmetric-square prime trace has central logarithmic order `kappa_sym`
in the H2-B convention

```text
B_E^sym(2z) = kappa_sym log z + C_sym + o(1),
```

while

```text
M_good(2z) = log(1/z) + C_M + o(1),
```

then

```text
A_E(z)
 = (1/2 + kappa_sym/2 - r) log(1/z)
   + C_A
   + o(1).
```

Consequently the S1 central coefficient is

```text
c_0 = 1/2 + kappa_sym/2 - r.
```

For expected non-CM bookkeeping with `kappa_sym=0`, this is `1/2 - r`. The
final product coefficient becomes `-r` only after adding the quadratic and
harmonic pieces from H2-B/H2-E.

## 2. Kernel And Mellin Setup

Use the same admissible class as H2-E. The Agent 3 smoothstep is included:

```text
W_alpha(t) = 1                                      for 0 <= t <= alpha,
W_alpha(t) = 1 - u^2(3 - 2u), u=(t-alpha)/(1-alpha) for alpha < t < 1,
W_alpha(t) = 0                                      for t >= 1.
```

Assume `W` is compactly supported in `[0,1]`, `W(t) -> 1` as `t -> 0`, and its
Mellin transform

```text
W_hat(z) = integral_0^infty W(t) t^(z-1) dt
```

has a simple pole at `z=0` with residue `1`, and satisfies on fixed vertical
strips away from `0`

```text
W_hat(sigma+i tau) = O_W,sigma((1+|tau|)^(-2)).
```

For `alpha=0` in Agent 3,

```text
W_hat(z) = 1/z - 3/(z+2) + 2/(z+3).
```

For any `c > 1/2`, Hasse-size bounds give absolute convergence of `A_E(z)` on
`Re z = c`, and Mellin inversion gives

```text
S_1,W^good(K)
 = (1/(2 pi i)) integral_(c)
     K^z W_hat(z) A_E(z) dz.
```

Set `u = log K`. Then

```text
S_1,W^good(e^u)
 = (1/(2 pi i)) integral_(c)
     e^(u z) W_hat(z) A_E(z) dz.
```

The question is the singularity type of `A_E(z)`, not just the location of the
zeros.

## 3. Local Singularity Calculus

The needed inverse Mellin facts are local Laplace inversions.

### Central branch times kernel pole

If near `z=0`

```text
A_E(z) = c_0 log(1/z) + analytic finite part,
W_hat(z) = 1/z + w_0 + O(z),
```

then

```text
(1/(2 pi i)) integral e^(u z) W_hat(z) c_0 log(1/z) dz
 = c_0 log u + c_0 gamma_W + o(1),
```

where `gamma_W` is the kernel-dependent finite part. In `K` notation:

```text
c_0 log log K + constant + o(1).
```

This is why the central zero affects S1 at `log log K` scale.

### Offcentral logarithmic branch

Let `a != 0`, and suppose `W_hat` is regular at `a`. If locally

```text
A_E(z) = c_a log(1/(z-a)) + analytic finite part,
```

then

```text
(1/(2 pi i)) integral e^(u z) W_hat(z) c_a log(1/(z-a)) dz
 = c_a W_hat(a) e^(a u)/u
   + O_a,W(e^(a u)/u^2),
```

with the usual interpretation after choosing a branch cut from `a` away from
the shifted contour. Equivalently,

```text
c_a W_hat(a) K^a / log K
  + O_a,W(K^a/(log K)^2).
```

This is the key scale calculation. A logarithmic branch away from the pole of
`W_hat` loses one power of `log K`.

For a zero `rho=1+a` of `L(E,s)` with multiplicity `m_rho`, the contribution
from the `log L(E,1+z)` term is

```text
c_a = -m_rho,
```

because

```text
log L(E,1+z) = m_rho log(z-a) + analytic
             = -m_rho log(1/(z-a)) + analytic.
```

Companion symmetric-square or harmonic terms add their own coefficients to
`c_a` if they have a branch at the same `a`.

### Offcentral pole

If instead

```text
A_E(z) = d_a/(z-a) + analytic,
```

then the contribution is

```text
d_a W_hat(a) e^(a u) = d_a W_hat(a) K^a.
```

This is the persistent almost-periodic term warned about by H2-C. It is real,
but it is a pole-term phenomenon. It appears at the `-L'/L` level because zeros
are poles of the logarithmic derivative. It does not appear in the prime-linear
`a_p/p` sum after the `log p` weight has been integrated away, unless `A_E(z)`
itself has an offcentral pole.

### Kernel poles left of zero

Extra Mellin-transform poles of `W_hat`, such as `z=-2,-3` for the `alpha=0`
smoothstep, produce powers `K^-2`, `K^-3`, etc. They are lower-order and do not
change the H2 slope.

## 4. Explicit Formula Shape

Let `Sigma_A` be the nonzero branch set of `A_E(z)` in the shifted strip. Write
the local logarithmic coefficient at `a in Sigma_A` as `c_a`, so that

```text
A_E(z) = c_a log(1/(z-a)) + analytic near a.
```

Assume:

```text
sum_{a in Sigma_A}
  |c_a W_hat(a)| < infinity,
```

and enough strengthened summability with local branch radii to justify shifting
the contour and summing the local branch contributions termwise. Then

```text
S_1,W^good(K)
 = c_0 log log K
   + C_1,E,W^good
   + (1/log K) Z_1,E,W(log K)
   + O(1/(log K)^2)
   + O(K^(-eta)),
```

where

```text
c_0 = 1/2 + kappa_sym/2 - r,
```

and

```text
Z_1,E,W(u)
 = sum_{a in Sigma_A} c_a W_hat(a) exp(a u).
```

Adding bad primes:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + (1/log K) Z_1,E,W(log K)
   + O(1/(log K)^2)
   + O(K^(-eta)).
```

For an `L(E,s)` zero `rho=1+i gamma`, `gamma != 0`, and no companion collision,
the corresponding term is

```text
-m_rho W_hat(i gamma) K^(i gamma) / log K
  + O_gamma,W(1/(log K)^2).
```

Taking conjugate zeros together gives a real oscillatory term of size
`O(1/log K)` when the weighted zero series is summable.

## 5. Pointwise Modes By Zero Location

For a branch point `a = beta + i gamma`:

```text
branch contribution = c_a W_hat(a) K^beta exp(i gamma log K) / log K.
```

Therefore:

- If `beta < 0`, the term decays like `K^beta/log K`.
- If `beta = 0`, the term is oscillatory but lower-order, `O(1/log K)`, under
  the stated zero-summability hypothesis.
- If `beta > 0`, the term grows like `K^beta/log K`; pointwise H2-limit fails
  unless there is cancellation or no such branch.
- If `A_E(z)` has a pole at `a` with `beta = 0`, the term is persistent
  `c exp(i gamma log K)` and must be retained or averaged.

For the S1 trace sum under the branch-only hypotheses, offcentral zeros on
`Re(s)=1` are lower-order. They do not require averaging. What requires either
an explicit retained term or averaging is failure of one of these hypotheses:
non-summable zero aggregate, a genuine offcentral pole in `A_E`, or a companion
term whose pole survives in the final product package.

## 6. Stieltjes Check From `-L'/L`

The same scale appears if one starts from the logarithmic derivative.

The first-prime piece of `-L'/L` at `s=1+z` contains

```text
sum_p_good a_p log p p^(-1-z).
```

A zero `rho=1+a` of multiplicity `m_rho` gives a pole

```text
-L'/L(1+z) = -m_rho/(z-a) + analytic.
```

A smoothed `log p`-weighted prime sum therefore has an offcentral term

```text
-m_rho W_hat(a) K^a.
```

But

```text
A_E'(z) = -sum_p_good a_p log p p^(-1-z).
```

Integrating the pole in `z` gives the logarithmic branch

```text
A_E(z) = -m_rho log(1/(z-a)) + analytic
```

up to the same sign convention as above. In `u=log K`, this integration is
exactly the division by `u`. Thus the persistent `K^a` term is correct for the
`log p`-weighted explicit formula and incorrect for S1 unless the integration
constant is replaced by a pole.

This resolves the H2-B/H2-C discrepancy for S1:

```text
H2-B scale is correct for the prime-linear trace sum.
H2-C scale is the necessary warning for pole-level or unsuppressed companion
terms, and for any theorem that has not proved the branch calculation.
```

## 7. Exact Hypotheses For A Claim-Safe S1 Theorem

A pointwise S1 theorem may be stated only under all of the following.

1. Exact local factors:

   ```text
   A_p(1)=1-a_p/p+1/p   at good primes,
   A_p(1)=1-a_p/p       at bad primes.
   ```

2. Analytic rank convention:

   ```text
   r = ord_{s=1} L(E,s).
   ```

   Replacing `r` by algebraic/script rank requires BSD rank equality or
   per-curve analytic-rank verification.

3. Central expansions:

   ```text
   L(E,1+z)=lambda_E z^r(1+O(z)), lambda_E != 0,
   B_E^sym(2z)=kappa_sym log z + C_sym + o(1),
   M_good(2z)=log(1/z)+C_M+o(1).
   ```

4. Branch-only offcentral structure for `A_E(z)` in the contour strip:

   ```text
   A_E(z)=c_a log(1/(z-a)) + analytic
   ```

   at each offcentral singularity `a`, with no offcentral pole on `Re a >= 0`.

5. Zero-summability and contour control:

   ```text
   sum_a |c_a W_hat(a)| < infinity
   ```

   plus the corresponding strengthened bound needed for the `O(1/(log K)^2)`
   remainder and for horizontal/left-edge contour errors.

6. No right-half-plane branch obstruction:

   ```text
   Re a <= 0
   ```

   for all offcentral branch points relevant to the theorem, or else an
   explicit cancellation/subsequence/averaging statement is included.

7. The same theorem mode is used in H2 and any H1 composition: pointwise,
   oscillatory with retained zero terms, or logarithmically averaged.

Under these hypotheses,

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + O(1/log K)
```

for branch points on `Re a=0`, with the sharper displayed
`Z_1,E,W(log K)/log K` term available.

## 8. Consequences For H2

The S1 derivation supports the H2-limit trace input:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + o(1),
```

but only after the exact hypotheses in Section 7 are proved or assumed.

When combined with H2-B's local identity

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2)S_sym,W(K)
   - (1/2)M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K),
```

and with

```text
S_sym,W(K)  = -kappa_sym log log K + C_sym,E,W + o(1),
M_good,W(K)= log log K + C_M,E,W + o(1),
```

the coefficient becomes

```text
(1/2 + kappa_sym/2 - r)
  - kappa_sym/2
  - 1/2
 = -r.
```

So the central coefficient in the exact Agent 3 product is compatible with
H2-limit. The unresolved work is not the S1 zero scale; it is proving the
branch-only continuation, zero-summability, symmetric-square finite part, and
contour bounds in a source-closed or self-contained way.

## 9. Do Not Promote

Do not promote a pointwise H2 theorem from this note unless:

- the exact Agent 3 good/bad local factors are retained;
- the coefficient is stated first with analytic rank `r=ord_{s=1}L(E,s)`;
- the S1 central coefficient is `1/2 + kappa_sym/2 - r`, not `-r`;
- the quadratic/symmetric-square and harmonic pieces are included before
  claiming the product coefficient `-r`;
- every offcentral contribution is derived from a logarithmic branch integral
  or explicitly identified as a pole term;
- the zero series

  ```text
  sum_a |c_a W_hat(a)|
  ```

  and the contour-shift errors are proved or assumed in the theorem statement;
- any offcentral pole or non-summable zero aggregate is retained as an
  oscillatory term or removed by an explicitly averaged theorem;
- no external theorem is cited without the sprint protocol:
  `curl + pdftotext + verbatim quote + page/eq`;
- H1 composition uses the same theorem mode as H2.

## 10. Decision

Use this S1-A result as:

```text
RIGOROUS_REDUCTION.
```

The branch calculation resolves the pointwise zero-term scale for S1:

```text
offcentral logarithmic branches contribute K^(rho-1) W_hat(rho-1)/log K.
```

For zeros on `Re rho=1`, this is lower-order after weighted zero summability.
It is not a persistent pointwise obstruction for S1 itself. The product theorem
still must not be promoted until the symmetric-square companion term and all
zero/contour hypotheses are closed in the same normalization.
