---
schema_version: 1
title: "Agent 01 BFMT Proposition 2.5 Coefficient Audit"
date: 2026-05-11
agent: "Agent 01"
type: coefficient-audit
tier: working
status: NO_GO
confidence: 0.86
tags: [bfmt, milinovich-ng, gl2, dpmv, h1, reciprocal-derivative]
---

# Agent 01 BFMT P2.5 Coefficient Audit

Status: `NO_GO`.

## Verdict

`BFMT-CoefficientErrorCheck` fails for the BFMT Proposition 2.5
`P_{0,v}^{s_0}` coefficient family if the only GL2 replacement is
Milinovich-Ng Proposition 4.1.

The local arithmetic checks are mostly favorable:

- support is acceptable if the BFMT Proposition 2.5 margin
  `beta_0 s_0 <= 1 - loglogT/logT` is imposed;
- Milinovich-Ng conditions (39) and (40) are provable for the unscaled inner
  BFMT Dirichlet polynomial;
- the GL2 off-diagonal main term vanishes exactly for exact `Omega(n)=s_0`
  support;
- fixed bad primes are harmless.

The route dies at the error terms in Milinovich-Ng Proposition 4.1.  BFMT
Proposition 2.5 expands

```text
P_{0,v}(gamma)^{s_0} = s_0! * A_v(1/2 + 1/logT + i gamma),
```

so applying Milinovich-Ng to the coefficient-normalized inner polynomial
`A_v` and then multiplying by `(s_0!)^2` makes the
`T(logT)^{4-2 eta}` error too large by a fixed power of `T` at `k=1/2`.
The square-root GL2 convolution error has the same non-homogeneous defect.
Applying Proposition 4.1 directly to the scaled coefficients would avoid this
factor, but then the required absolute partial-sum hypotheses are not supplied
by BFMT and are not a consequence of Proposition 2.5.

Therefore the BFMT `T^(1+delta)` separated-zero estimate does not survive this
Milinovich-Ng Proposition 4.1 substitution.  A new homogeneous GL2
Landau-Gonek/DPMV theorem is required.

## Source Protocol

Workspace:

```bash
/tmp/farey-agent01-bfmt-p25-20260511
```

PDF extraction:

```bash
curl -L --fail -s -o bfmt_2310_03949.pdf https://arxiv.org/pdf/2310.03949
curl -L --fail -s -o milinovich_ng_1306_0854.pdf https://arxiv.org/pdf/1306.0854
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 bfmt_2310_03949.pdf bfmt_2310_03949.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 milinovich_ng_1306_0854.pdf milinovich_ng_1306_0854.txt
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_2310_03949.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
```

Small quote anchors, kept short:

- BFMT Proposition 2.5, PDF p. 8: "Assume RH."
- BFMT Theorem 3.1, PDF p. 8: "any sequence of complex numbers."
- Milinovich-Ng Proposition 4.1, PDF p. 19: "satisfying (39) and (40)."

The arXiv source files were also fetched to disambiguate formula layout.  In
Milinovich-Ng Proposition 4.1 the convolution error is

```text
O(T(logT)^(4-2eta) + T logT * sqrt(C_a)),
```

where

```text
C_a = sum_{n>=1} |(Lambda_f * a)(n)|^2 / n^(1+1/logT).
```

The pdftotext layout flattens this square root ambiguously; the source TeX
contains it explicitly.

## Coefficient Family

For BFMT Proposition 2.5, write

```text
L = log T,       L2 = log log T,       y = T^beta0,       s = s_0.
```

The inner coefficient family is

```text
a_v(n) =
  b(n;Delta_v) nu(n) n^(-1/L)
```

on the support

```text
p | n => p <= y,
Omega(n) = s,
```

and `a_v(n)=0` otherwise.  BFMT then has

```text
P_{0,v}(gamma)^s = s! * sum_n a_v(n) n^(-1/2-i gamma).
```

The support exponent is exactly

```text
theta_0 = beta_0 s.
```

Under the stated BFMT Proposition 2.5 hypothesis

```text
beta_0 s <= 1 - L2/L,
```

the support length is `<= T/logT`.  Milinovich-Ng Proposition 4.1 assumes
`Y asymp T`; padding `a_v(n)` by zero up to a length `Y asymp T` is harmless.

At `k=1/2`, BFMT's later second-regime parameter choice has

```text
beta_0 = C_0 L2/L,       s = floor(1/beta_0),
```

with `C_0 = 2 + O(epsilon+delta)` as the small auxiliary parameters tend to
zero.  This gives `s = (1/C_0 + o(1)) L/L2`.  The printed floor choice gives
`beta_0 s <= 1`; the sharper `1-L2/L` margin is not automatic for every `T`.
This is a minor integer-margin issue for literal BFMT parameters, but not the
main GL2 obstruction below.  The no-go below holds even if the support margin
is granted.

## Conditions (39) And (40)

Let

```text
B_v = b(Delta_v) * (log(L/Delta_v))^eta(Delta_v).
```

For the P2.5 range, the worst case is `v=0`, and BFMT gives

```text
B_v <= L2^(1+o(1)).
```

Also

```text
sum_{p<=y} 1/p = log log y + O(1) = O(log L2).
```

For `x >= 3`, Rankin's trick with the exact `nu` generating factor gives

```text
sum_{n<=x} |a_v(n)|
 <= x * sum_n |b(n;Delta_v)| nu(n) / n
 <= x/s! * (B_v * sum_{p<=y} 1/p)^s.
```

Since

```text
e B_v loglog y / s = O(L2^2 log L2 / L) = o(1),
```

the final factor is `T^{-c+o(1)}` for large `T`, after weakening constants.
Thus condition (39) holds for any fixed `0 < eta <= 1/2`.

Similarly, using `nu(n)^2 <= nu(n)`,

```text
sum_{n<=x} |a_v(n)|^2
 <= x * sum_n |b(n;Delta_v)|^2 nu(n)^2 / n
 <= x/s! * (B_v^2 * sum_{p<=y} 1/p)^s.
```

Here

```text
e B_v^2 loglog y / s = O(L2^3 log L2 / L) = o(1),
```

so condition (40) holds, again for the unscaled inner polynomial `A_v`.

Important limitation: these checks are for `A_v`, not for the scaled polynomial
`s! A_v = P_{0,v}^s`.  Milinovich-Ng Proposition 4.1 is not a homogeneous
arbitrary-coefficient theorem in the way BFMT Theorem 3.1 is; the hypotheses
(39)/(40) constrain coefficient scaling.

## Off-Diagonal Term

Milinovich-Ng Proposition 4.1 has the main off-diagonal term

```text
-(T/pi) Re sum_{n<=Y} (Lambda_f * a_v)(n) conjugate(a_v(n)) / n.
```

For this exact BFMT P2.5 support it vanishes.

Reason: if `a_v(n) != 0`, then `Omega(n)=s`.  In

```text
(Lambda_f * a_v)(n) = sum_{dm=n} Lambda_f(d) a_v(m),
```

the term `d=1` contributes zero because `Lambda_f(1)=0`.  Every `d>1`
supported by `Lambda_f` is a prime power, so `Omega(m)<s`; hence
`a_v(m)=0`.  Thus

```text
(Lambda_f * a_v)(n) conjugate(a_v(n)) = 0
```

for every `n`.  This part of the GL2 audit passes exactly.

## GL2 Convolution Error

The remaining convolution quantity is

```text
C_v = sum_{m>=1} |(Lambda_f * a_v)(m)|^2 / m^(1+1/L).
```

Using Milinovich-Ng's bound `|Lambda_f(n)| <= 2 Lambda(n)` and the exact
`Omega=s` support, a crude but sufficient upper bound is

```text
C_v <= T^o(1) L^2 D_v,
```

where

```text
D_v = sum_n |a_v(n)|^2 / n^(1+2/L)
    <= 1/s! * (sum_{p<=y} |b(p;Delta_v)|^2/p)^s.
```

This says the convolution series itself is not arithmetically explosive.
However Milinovich-Ng Proposition 4.1 uses `sqrt(C_v)`, not `C_v`, in the
error term.  After multiplying by `(s!)^2` to recover the moment of
`P_{0,v}^s`, this square-root error has the wrong homogeneity:

```text
E_conv,MN = T logT * (s!)^2 * sqrt(C_v).
```

The BFMT P2.5 target scale is

```text
M_BFMT = T logT * s! * H_v^s,
H_v = sum_{p<=y} |b(p;Delta_v)|^2/p = T^o(1).
```

Since at `k=1/2`

```text
log(s!) = (1/C_0 + o(1)) L,
log(H_v^s) = o(L),
log(D_v) = -(1/C_0 + o(1)) L,
```

the estimate furnished by Proposition 4.1, after inserting the general
convolution bound above, allows a term larger than the BFMT target by a fixed
power.  Proposition 4.1 therefore cannot certify the BFMT bound here; the
allowed loss cannot be absorbed into `T^delta` for arbitrary small `delta`.

This is already a no-go as a black-box use of Proposition 4.1.

## The Fatal Error Term

Even before the convolution square-root issue, Milinovich-Ng Proposition 4.1
contains the generic error

```text
T (log T)^(4-2 eta).
```

Applied to the unscaled inner polynomial and then multiplied by `(s!)^2`, the
black-box Proposition 4.1 bound includes the allowance

```text
E_0,MN = T (log T)^(4-2 eta) (s!)^2.
```

Compare with the BFMT P2.5 target:

```text
M_BFMT = T logT * s! * H_v^s.
```

The ratio is

```text
E_0,MN / M_BFMT
  = (log T)^(3-2 eta) * s! / H_v^s
  = T^(1/C_0 - o(1)).
```

For the `k=1/2` parameter range, `C_0 = 2 + o(1)`, so the loss is essentially
`T^(1/2-o(1))`.  This is not a log loss and cannot be hidden in BFMT's final
`T^(1+delta)` theorem for arbitrary `delta>0`.

This is the decisive failure.

## Bad Primes

For a fixed elliptic curve/newform, bad primes are finite.  They may be removed
from the BFMT prime blocks or retained with constants depending on the fixed
form.  Milinovich-Ng's source also records the global bound

```text
|Lambda_f(n)| <= 2 Lambda(n)
```

for their holomorphic newform normalization.  Either treatment changes only
fixed constants or `T^o(1)` factors.  Bad primes are not the obstruction.

## Consequence For The Separated-Zero Estimate

BFMT's separated-zero proof needs Proposition 2.5 with essentially the BFMT
right-hand side.  Milinovich-Ng Proposition 4.1 gives that main diagonal, and
the GL2 off-diagonal vanishes, but the non-homogeneous errors are too large
after the necessary `s_0!` expansion factor.

Therefore this route does not prove

```text
sum_{gamma in F_E(T,c)} |L'_E(1+i gamma)|^(-1) <<_{E,c,delta} T^(1+delta).
```

The current BFMT separated-zero adaptation is dead at Proposition 2.5 unless
one proves a stronger GL2 zero-discrete mean-value theorem with BFMT-compatible
homogeneous errors, for example an error of schematic type

```text
O(T^(beta_0 s_0) (log T)^A * D_v)
```

or a GL2 Landau-Gonek theorem matching BFMT Theorem 3.1 for arbitrary
coefficients of length `T^(1-o(1))`.

Milinovich-Ng Proposition 4.3 does not rescue this P2.5 block: its prime-power
high-moment hypothesis has the support wall `x^m <= T^(2/3)`, while BFMT P2.5
at `k=1/2` uses total support `T^(1-o(1))` after the required margin.

## Final Classification

`NO_GO`: BFMT Proposition 2.5 coefficients do not pass
`BFMT-CoefficientErrorCheck` against Milinovich-Ng Proposition 4.1.  The
surviving target is not a coefficient audit but a new homogeneous GL2
Landau-Gonek/DPMV input.
