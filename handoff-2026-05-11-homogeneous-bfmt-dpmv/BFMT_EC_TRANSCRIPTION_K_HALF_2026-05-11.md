---
schema_version: 1
title: "BFMT EC transcription at k=1/2"
date: 2026-05-11
relay: "Relay[03]: farey-h1-bfmt-ec-transcription"
type: theorem-reduction
tier: working
status: CONDITIONAL_TRANSCRIPTION
confidence: 0.80
sources:
  - ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md
  - ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - ../breakthrough-wave-3/AGENT01_GL2_BFMT_ADAPTATION_BLUEPRINT_2026-05-11.md
  - ../top10-challenge-wave/AGENT04_EC_BFMT_BADSET_INVERSEGAP_BUDGET_2026-05-11.md
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
  - /tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt
  - /tmp/farey-homogeneous-bfmt-20260511/sheth_ec_arxiv_2312.05236.txt
tags: [h1, gl2, ec, bfmt, transcription, zero-sampling, reciprocal-derivative]
---

# BFMT EC Transcription At k=1/2

Status: `CONDITIONAL_TRANSCRIPTION`.

No final H1 theorem is promoted.

## Verdict

The BFMT separated-zero route for one fixed elliptic curve now reduces to two
local GL2 inputs, not to a Landau-Gonek/Milinovich-Ng DPMV theorem.

The coefficient side transcribes:

```text
BFMT coefficient propositions 2.5, 2.6, 2.7
+ EC/newform lambda_E(p) factors
+ homogeneous zero-sampling large sieve
=> same BFMT Section 5 bound with T^o(1) loss.
```

Thus, if the two local GL2 inputs below are supplied, then for every fixed
`c>0` and every `delta>0`,

```text
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  <<_(E,c,delta) T^(1+delta).
```

This is the separated simple-zero branch only.  The complement remains the
independent target

```text
EC-BFMT-BadSetBudget(E,c):
sum_(gamma notin F_E(T,c), simple) |L'(E,1+i gamma)|^(-1)=o(T^2).
```

## Normalization

Use

```text
L_E^*(s) = L(E,s+1/2) = sum_n lambda_E(n)n^(-s).
```

Then a critical zero of `L(E,s)` at `1+i gamma` is a zero

```text
rho_E = 1/2+i gamma
```

of `L_E^*`, and

```text
(L_E^*)'(rho_E)=L'(E,1+i gamma).
```

For good primes `p not | N_E`, write

```text
lambda_E(p)=alpha_hat_p+beta_hat_p,
|alpha_hat_p|=|beta_hat_p|=1.
```

Bad primes are finite and are omitted from the BFMT prime polynomials; their
Euler factors change only the constants depending on `E`.

The separated family is

```text
F_E(T,c) = {gamma in (T,2T]:
  L(E,1+i gamma)=0 is simple and
  |gamma-gamma'| >= c/log T for every other zero ordinate gamma'}.
```

## Required Local Inputs

### GL2 Shift-Derivative Comparison

For `gamma in F_E(T,c)`,

```text
log |L'(E,1+i gamma)|^(-1)
  <= log |L(E,1+1/logT+i gamma)|^(-1)
     + O_(E,c)(logT/loglogT).
```

This is the fixed-curve analogue of BFMT Lemma 2.1.  Milinovich-Ng record the
fixed-newform argument bound `S_f(t)=O(log t/loglog t)` on RH, but this packet
does not source-close the Hadamard/Kirila transcription.

### GL2 BFMT Prime-Polynomial Lower Bound

For `sigma=1/2+1/logT`, the needed lower bound is

```text
log |L_E^*(sigma+i gamma)|
  >= - Re sum_(p<=exp(2pi Delta), p not | N_E)
          b(p;Delta)lambda_E(p)p^(-sigma-i gamma)
     - C_E loglogT
     - BFMT_error(Delta,T).
```

The `C_E loglogT` allowance is deliberate.  Prime powers, bad primes, conductor
and gamma-factor terms may cost a fixed power of `log T`; BFMT Section 5 absorbs
that.  A narrow repo/wiki search plus old-session query found no source-backed
packet proving this GL2 lower bound, so it remains the main unclosed input.

## EC Coefficient Families

Keep BFMT's blocks

```text
I_0=(1,T^beta0],  I_j=(T^beta_(j-1),T^beta_j],
T^beta_j=e^(2pi Delta_j).
```

For `u<=v`, define the EC prime polynomial

```text
P^E_(u,v)(gamma)
  = sum_(p in I_u, p not | N_E)
      b(p;Delta_v) lambda_E(p) p^(-1/2-1/logT-i gamma).
```

Use the same truncated exponential

```text
E_ell(z)=sum_(s<=ell) z^s/s!
```

and the same BFMT parameter choices from Section 5.

The only arithmetic changes in the coefficient square sums are:

```text
sum_(p<=x) |lambda_E(p)|^2/p = loglog x + O_E(1),
|lambda_E(n)| <= d(n),
finite bad-prime removal = O_E(1).
```

Milinovich-Ng source anchors for these are Proposition 5.1 and Deligne's bound.

## Zero-Sampling Substitution

For any Dirichlet polynomial of length `N<=T`,

```text
A(s)=sum_(n<=N) a_n n^(-s),
```

the source-backed replacement is

```text
sum_(T<gamma<=2T) |A(1/2+i gamma)|^2
  <<_E T(logT)^3 sum_(n<=N) |a_n|^2/n.
```

Since `N_E(2T)-N_E(T) asymp_E T logT`, this is BFMT's upper-bound scale with
an extra `(logT)^2`.  It is homogeneous in the actual coefficients.

### Proposition 2.5

The transcribed identity is

```text
(P^E_(0,v)(gamma))^s0
 = s0! sum_(Omega(n)=s0, p|n=>p in I_0)
     b_E(n;Delta_v) nu(n)n^(-1/2-1/logT-i gamma),
```

where `b_E` is the completely multiplicative extension of
`b(p;Delta_v)lambda_E(p)`.

The support condition `beta_0 s0 <= 1-loglogT/logT` gives length `<=T/logT`.
Zero-sampling gives BFMT Proposition 2.5 with an extra factor

```text
(logT)^2 exp(O_E(s0)).
```

Under the BFMT Section 5 parameters, `s0 << logT/loglogT`, so this is `T^o(1)`.
The former factorial obstruction is gone because the estimate is applied to
the scaled polynomial itself.

### Proposition 2.6

For

```text
prod_(h<=j) E_(ell_h)(k P^E_(h,j)(gamma))
  * (P^E_(j+1,v)(gamma))^s_(j+1),
```

the support condition

```text
sum_(h<=j) ell_h beta_h + s_(j+1) beta_(j+1)
  <= 1-loglogT/logT
```

again gives length `<=T/logT`.  Apply zero-sampling to the whole expanded
Dirichlet polynomial.  The coefficient square sum is the BFMT one with
`|lambda_E(p)|^2` inserted in each prime block; Rankin-Selberg prime averages
and finite bad-prime removal add only `T^o(1)`.

No Milinovich-Ng condition (39) or (40) is needed.  The terminal factorial
coefficients live inside the natural `l2` norm.

### Proposition 2.7

The same argument applies to

```text
prod_(h<=K) E_(ell_h)(k P^E_(h,K)(gamma))
```

under

```text
sum_(h<=K) ell_h beta_h <= 1-loglogT/logT.
```

BFMT only needs this branch in Section 5 as

```text
S_1 << N_E(T)(logT)^O(1).
```

The EC/zero-sampling losses merely change the implicit exponent and a
subpower `T^o(1)` factor.

## Section 5 Check At k=1/2

For `k=1/2`, BFMT is in the branch `2k(1+epsilon)<=1` after choosing
`epsilon>0` small.

All new factors are among

```text
exp(O_(E,c)(logT/loglogT))       from shift-derivative comparison,
(logT)^C_E                      from GL2 log-lower-bound bookkeeping,
(logT)^2 T^o(1)                 from zero-sampling and lambda_E coefficients.
```

Each is `T^o(1)`.  BFMT's final estimates (5.12), (5.14), (5.15), and (5.16)
therefore remain

```text
<<_(E,c,delta) T^(1+delta)
```

after reducing the internal epsilon/delta margins.

## Updated Target Hierarchy

```text
ZeroSample-EC-BFMT-CoefficientTranscription(E,k=1/2)
  status: passed as conditional transcription; no DPMV theorem missing.

SeparatedEC-BFMT(E,c,k=1/2)
  follows from:
    GL2-ShiftDerivativeComparison(E,c)
    GL2-BFMT-PrimePolynomialLowerBound(E)
    zero-sampling coefficient propositions above.

EC-BFMT-BadSetBudget(E,c)
  still independent and open.
```

## No-Promotion Boundary

Do not state:

```text
R_E,1(T)=o(T^2) is proved;
the full H1 rank-one theorem is proved;
the GL2 BFMT prime-polynomial lower bound is source-closed;
the BFMT bad set is controlled by pair-correlation or count-only spacing;
multiple zeros are controlled by this packet.
```

No Koyama correspondence or email drafts were read or edited.
