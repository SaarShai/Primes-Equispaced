---
schema_version: 1
title: "H2-B analytic proof attempt for smoothed EC Mertens product"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.67
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T2_STOCHASTIC_EULER_PRODUCT_MODEL.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
tags: [ec-ndc, h2, smoothed-mertens, explicit-formula, symmetric-square]
---

# H2-B Analytic Proof Attempt

status: `RIGOROUS_REDUCTION`

No unconditional theorem is promoted. The exact local expansion gives the
desired coefficient `-rank(E)` once the first-order EC prime sum and the
quadratic symmetric-square finite part are put in the same normalization. The
remaining gap is a source-closed explicit-formula/PNT input with enough
off-central-zero control.

## 1. Exact object and bad-prime convention

The reproducer defines, for the same smooth weight `W` used on the prime side,

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),
log P_E,W(K) = - sum_p W(p/K) log A_p(1).
```

At good primes,

```text
A_p(1) = 1 - a_p/p + 1/p.
```

At bad primes, exactly as in the reproducer,

```text
A_p(1) = 1 - a_p/p.
```

The bad-prime contribution is finite:

```text
B_bad,E,W(K) = - sum_{p bad} W(p/K) log(1 - a_p/p)
             = B_bad,E + o(1),
B_bad,E     = - sum_{p bad} log(1 - a_p/p),
```

using the real-log positivity convention enforced by the script.

## 2. Smoothing kernel

For `0 <= alpha < 1`, the reproducer's smoothstep cutoff is

```text
W_alpha(t) = 1                                             0 <= t <= alpha,
W_alpha(t) = 1 - u^2(3 - 2u), u=(t-alpha)/(1-alpha)         alpha < t < 1,
W_alpha(t) = 0                                             t >= 1.
```

For `alpha = 0`, this is `W_0(t)=1-3t^2+2t^3` on `[0,1]`.

Let

```text
W_hat(z) = integral_0^infty W(t) t^(z-1) dt.
```

Then `W_hat(z)` has a simple pole at `z=0` with residue `1`. For the
smoothstep kernels it has vertical decay `O_W((1+|Im z|)^-2)` on fixed strips
away from `z=0`. In the special `alpha=0` case,

```text
W_hat(z) = 1/z - 3/(z+2) + 2/(z+3).
```

Mellin inversion gives, for any prime Dirichlet series `D(z)=sum_p b_p p^(-z)`
initially convergent on `Re z > sigma`,

```text
sum_p b_p W(p/K)
  = (1/2 pi i) integral_(c) K^z W_hat(z) D(z) dz.
```

The pole of `W_hat` at `0` is what turns a logarithmic singularity
`c log(1/z)` in `D(z)` into `c log log K`.

## 3. Good-prime local logarithm

At a good prime write

```text
1 - a_p p^(-s) + p^(1-2s)
  = (1 - alpha_p p^(-s))(1 - beta_p p^(-s)),
alpha_p + beta_p = a_p,
alpha_p beta_p = p,
|alpha_p| = |beta_p| = sqrt(p).
```

Then at `s=1`,

```text
-log(1 - a_p/p + 1/p)
  = sum_{m>=1} (alpha_p^m + beta_p^m)/(m p^m).
```

The first terms are

```text
-log(1 - a_p/p + 1/p)
 = a_p/p
   + (a_p^2 - 2p)/(2p^2)
   + (a_p^3 - 3p a_p)/(3p^3)
   + O(p^(-2)).
```

Equivalently, with `lambda_p = a_p/sqrt(p)`,

```text
-log(1 - a_p/p + 1/p)
 = lambda_p/sqrt(p)
   + (lambda_p^2 - 2)/(2p)
   + O(p^(-3/2)).
```

The terms with `m >= 3` are absolutely summable:

```text
sum_p sum_{m>=3} |alpha_p^m + beta_p^m|/(m p^m)
  << sum_p p^(-3/2) < infinity.
```

Hence they contribute a finite constant plus `O_W(K^(-1/2))`.

## 4. Exact decomposition of log P

For good primes define the normalized symmetric-square trace

```text
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Then

```text
(a_p^2 - 2p)/(2p^2)
  = chi_sym2(p)/(2p) - 1/(2p).
```

Therefore the exact smoothed product expansion is

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K),
```

where

```text
S_1,W(K)      = sum_{p good} W(p/K) a_p/p,
S_sym,W(K)    = sum_{p good} W(p/K) chi_sym2(p)/p,
M_good,W(K)   = sum_{p good} W(p/K)/p,
R_ge3,W(K)    = sum_{p good} W(p/K)
                sum_{m>=3} (alpha_p^m + beta_p^m)/(m p^m).
```

This identity is the main useful output. It shows why the coefficient cannot be
read from `sum a_p/p` alone. The quadratic term contributes the universal
`-1/2 log log K`; the first-order term must include a compensating `+1/2`
baseline before the rank shift.

The script's `L2` factor is not this quadratic term. Its good-prime logarithm
starts with `a_p/p^2`, hence is absolutely convergent at `s=2` and cannot
produce any `log log K` coefficient.

## 5. Relation to L(E,s)

For `z` near `0`, the good-prime logarithm of `L(E,1+z)` has the same local
pieces:

```text
log L_good(E,1+z)
 = A_E(z)
   + (1/2) B_sym,E(2z)
   - (1/2) M_good(2z)
   + H_E(z),
```

where

```text
A_E(z)        = sum_{p good} a_p p^(-1-z),
B_sym,E(2z)   = sum_{p good} chi_sym2(p) p^(-1-2z),
M_good(2z)    = sum_{p good} p^(-1-2z),
H_E(z)        = absolutely convergent local remainder from m>=3
                and the higher local powers needed to match standard factors.
```

Let

```text
r = ord_{s=1} L(E,s).
```

If

```text
L(E,1+z) = lambda_E z^r (1 + O(z)),
```

then

```text
log L(E,1+z) = r log z + log lambda_E + O(z).
```

The prime harmonic term has

```text
M_good(2z) = log(1/z) + C_good - log 2 + o(1).
```

If the symmetric-square first prime series has logarithmic order `kappa_sym`
at `s=1`, meaning

```text
B_sym,E(2z) = kappa_sym log z + C_sym,E + o(1),
```

then the first-order EC prime series must have

```text
A_E(z)
 = (1/2 + kappa_sym/2 - r) log(1/z) + C_1,E + o(1).
```

For the expected non-CM case `kappa_sym=0`, this is

```text
A_E(z) = (1/2 - r) log(1/z) + C_1,E + o(1).
```

Thus the product-side coefficient is

```text
(1/2 + kappa_sym/2 - r)       from S_1
  + (-kappa_sym/2)             from (1/2) S_sym
  - 1/2                        from -(1/2) M_good
  = -r.
```

So possible symmetric-square logarithmic terms change the split between the
linear and quadratic pieces, but not the final coefficient, provided all pieces
come from the same local factorization of `L(E,s)`.

## 6. PNT / explicit-formula input needed

The decomposition proves H2 once the following smoothed estimates are available
with `o(1)` error:

```text
M_good,W(K)
  = log log K + C_M,E + o(1),

S_sym,W(K)
  = -kappa_sym log log K + C_sym,E,W + o(1),

S_1,W(K)
  = (1/2 + kappa_sym/2 - r) log log K + C_1,E,W + o(1),

R_ge3,W(K)
  = C_ge3,E + O_W(K^(-1/2)),

B_bad,E,W(K)
  = B_bad,E + o(1).
```

The first line is ordinary prime Mertens/PNT with finitely many bad primes
removed. The second is the symmetric-square PNT/finite-part statement. The
third is the EC first-order PNT at the central point. It is equivalent to the
logarithmic singular expansion of `A_E(z)` above.

Under these inputs,

```text
log P_E,W(K)
  = -r log log K + B_E,W + o(1),
```

with

```text
B_E,W
 = C_1,E,W
   + (1/2) C_sym,E,W
   - (1/2) C_M,E
   + C_ge3,E
   + B_bad,E.
```

This is the desired H2 statement.

## 7. Conditional theorem

**Theorem candidate.** Fix an elliptic curve `E/Q` and a reproducer smoothstep
weight `W`. Let `r=ord_{s=1} L(E,s)`. Assume:

1. The local factors use the good/bad convention above and all bad local logs
   are taken in the reproducer's positive real branch.
2. The logarithm of `L(E,s)` has exact central order `r`:

   ```text
   L(E,1+z) = lambda_E z^r (1 + O(z)), lambda_E != 0.
   ```

3. The symmetric-square prime trace satisfies the smoothed finite-part
   expansion

   ```text
   S_sym,W(K) = -kappa_sym log log K + C_sym,E,W + O((log K)^(-eta)).
   ```

4. The first-order EC prime series satisfies the explicit-formula expansion

   ```text
   S_1,W(K)
    = (1/2 + kappa_sym/2 - r) log log K
      + C_1,E,W + O((log K)^(-eta)).
   ```

5. The off-central zero contribution in the Mellin explicit formula is
   bounded by `O((log K)^(-eta))`. A sufficient form is

   ```text
   (1/log K) sum_{rho != 1} m_rho K^(Re rho - 1)
     |W_hat(rho - 1)| = O((log K)^(-eta)),
   ```

   together with the analogous symmetric-square zero sum. Under a GRH-shaped
   zero location `Re rho = 1` and the smoothstep decay
   `W_hat(1+i gamma - 1)=W_hat(i gamma)=O(|gamma|^-2)`, this reduces to a
   summable zero-weight condition.

Then

```text
log P_E,W(K) = -r log log K + B_E,W + O((log K)^(-eta')),
```

for some `eta' > 0`, with `B_E,W` as in Section 6.

For rank zero this gives a finite limit:

```text
log P_E,W(K) = B_E,W + o(1).
```

For positive rank it gives the claimed decay:

```text
P_E,W(K) = exp(B_E,W) (log K)^(-r) (1 + o(1)).
```

## 8. Explicit-formula shape and the smoothing gain

The product-side problem is easier than the reciprocal-coefficient Perron
problem in T1. Zeros of `L(E,s)` enter `log L`, hence enter the prime series as
logarithmic branch points, not poles of `1/L`.

At the central zero `z=0`, the branch point coincides with the pole of
`W_hat(z)`, producing the main term `-r log log K`.

At a noncentral zero `rho=1+i gamma`, the branch point is at `z=i gamma`.
Since `W_hat` has no pole there, the local branch-cut contribution has size
roughly

```text
K^(i gamma) W_hat(i gamma) / log K.
```

Thus smoothstep decay can make the offcentral sum `O(1/log K)` if the weighted
zero series is summable. With a hard cutoff, `W_hat(i gamma)=1/(i gamma)`,
which is much less forgiving.

If a zero with `Re rho > 1` is allowed, the same term becomes

```text
K^(Re rho - 1) / log K,
```

and H2 fails in this pointwise form unless there is additional cancellation.

## 9. What is proved here and what is still a gap

Proved in this note:

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K),
```

with `R_ge3,W(K)` convergent, bad primes finite, and final coefficient
`-rank(E)` forced by the central order of `L(E,s)` once the first-order and
symmetric-square PNT inputs are available.

Not proved here:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - rank(E)) log log K + C_1,E,W + o(1),
```

with source-verified explicit constants and offcentral-zero error control.
That is the real H2 analytic input. The reduction identifies the exact target
and shows that the quadratic/symmetric-square term is mandatory; omitting it
gives the wrong coefficient for the first-order `a_p/p` sum.

## 10. Decision

Use H2 in the next theorem package only in this conditional form:

```text
If the smoothed first-order EC prime PNT and the smoothed symmetric-square
finite-part PNT hold with the zero-sum bound in Section 7, then

log P_E,W(K) = -rank(E) log log K + B_E,W + o(1)

for the exact local factors used by the reproducer.
```

Do not cite this as a closed theorem until the PNT/explicit-formula inputs are
source-verified or proved in-repo.
