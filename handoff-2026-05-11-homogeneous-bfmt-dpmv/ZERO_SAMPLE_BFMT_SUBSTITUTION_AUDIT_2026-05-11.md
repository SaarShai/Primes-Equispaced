---
schema_version: 1
title: "Zero-Sample BFMT Substitution Audit"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
tags: [h1, gl2, ec, bfmt, dpmv, zero-sampling, substitution-audit]
---

# Zero-Sample BFMT Substitution Audit

Status: `RIGOROUS_REDUCTION`.

No final H1 theorem is promoted.  The coefficient-DPMV subproblem moves
substantially: the zero-sampling replacement for BFMT Theorem 3.1 passes the
visible BFMT Propositions 2.5, 2.6, 2.7 and Section 5 bookkeeping with only a
fixed polylogarithmic loss.

## Verdict

The finite audit target

```text
ZeroSample-BFMT-SubstitutionAudit(E,k=1/2)
```

passes at the level of BFMT's printed Section 4/5 estimates.

The replacement theorem is:

```text
ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2):
  In the fixed EC/newform normalized critical-line mode, every BFMT
  Proposition 2.5, 2.6, and 2.7 coefficient-family estimate remains valid
  with the right side multiplied by (log T)^C.
```

This is enough for the separated-zero H1 branch because the final BFMT
negative-moment target has `T^delta` slack.  It is not yet the full H1
reciprocal-derivative theorem:

```text
separated simple-zero coefficient DPMV: advanced;
EC-BFMT-BadSetBudget(E,c): still open;
multiple-zero Laurent control: still separate;
finite-box H1 contour/right-residue assumptions: still separate.
```

## Source Anchors

This packet uses the source protocol and files recorded in
`ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md`.

Additional checked anchors from the same extracted text:

- BFMT, PDF p. 11: "Using Theorem 3.1" begins the proof of Propositions
  2.5, 2.6, and 2.7.
- BFMT, PDF p. 11, Proposition 2.5 proof: the Theorem 3.1 error has
  `T^(beta_0 s_0)(log T)^2`.
- BFMT, PDF p. 12, Proposition 2.6 proof: the analogous support error is
  `T^(sum ell_h beta_h + s_{j+1} beta_{j+1})(log T)^2`.
- BFMT, PDF p. 16, equation (5.12): the `S_1` contribution is already
  `N(T)(log T)^O(1)`.
- BFMT, PDF p. 18, equations (5.14)-(5.17): the final branches are bounded
  by `T^(1+delta)` after absorbing subpower factors.
- Milinovich-Ng, PDF p. 1: their normalized newform satisfies Deligne's
  bound `|lambda_f(n)| <= d(n)`.

## Proposition-Level Replacement

Let the zero-sampling lemma be abbreviated as

```text
ZS(A):
sum_{T<gamma<=2T} |A(1/2+i gamma)|^2
  <<_E T(logT)^3 sum |a_n|^2/n.
```

Since `N_E(T) asymp_E T log T`, this is the BFMT Theorem 3.1 upper-bound
scale with an extra `(logT)^2`.

### Proposition 2.5

BFMT writes

```text
P_{0,v}(gamma)^s0
 = s0! sum_{Omega(n)=s0, p|n=>p<=T^beta0}
       b(n;Delta_v) nu(n) n^(-1/2-1/logT-i gamma).
```

The support condition is

```text
beta_0 s_0 <= 1 - loglogT/logT,
```

so the length is `<=T/logT`.  Applying `ZS(A)` directly to the scaled
coefficients gives

```text
sum_{T<gamma<=2T} |P_{0,v}(gamma)|^(2s0)
  << N_E(T)(logT)^2
     s0! b(Delta_v)^(2s0)
     (loglogT/Delta_v)^(2s0 eta(Delta_v))
     (loglogT beta_0)^s0.
```

This is BFMT Proposition 2.5 with an extra `(logT)^2`.

The factorial obstruction from the top-10 wave disappears: the estimate is
homogeneous and is applied to the scaled polynomial itself.

### Proposition 2.6

For the mixed family

```text
prod_{h=0}^j E_{ell_h}(kP_{h,j}(gamma))
  * P_{j+1,v}(gamma)^(s_{j+1}),
```

the support condition is

```text
sum_{h<=j} ell_h beta_h + s_{j+1} beta_{j+1}
  <= 1 - loglogT/logT.
```

Thus the full Dirichlet polynomial again has length `<=T/logT`.  Applying
`ZS(A)` to the whole product gives the same coefficient-square sum that BFMT
then estimates in equations (4.2)-(4.4), with one extra `(logT)^2` factor.

The terminal `P^(s_{j+1})` factorial coefficients do not need Milinovich-Ng
condition (40).  They are included in the actual coefficient `l2` norm and are
handled by BFMT's existing square-coefficient combinatorics.

If the EC/newform transcription inserts factors `lambda_f(p^a)`, Deligne's
bound `|lambda_f(n)|<=d(n)` increases these square sums by at most BFMT-legal
divisor factors on the same fixed `Omega` supports.  This is a `T^o(1)` or
fixed-polylog loss inside the same slack; a final transcription should record
the exact divisor-power exponent.

### Proposition 2.7

BFMT says the proof is "very similar" to Proposition 2.6.  The terminal family
has support

```text
sum_{h<=K} ell_h beta_h <= 1 - loglogT/logT.
```

The same zero-sampling substitution gives BFMT Proposition 2.7 with an extra
fixed `(logT)^C`.  This is already harmless in Section 5 because BFMT uses
Proposition 2.7 only to obtain

```text
S_1 << N(T)(logT)^O(1).
```

The exponent in `O(1)` changes, but the form does not.

## Section 5 Absorption

The extra loss from the substitution is a fixed `(logT)^C` in every use of
Propositions 2.5, 2.6, and 2.7.

### P2.5 insertion

BFMT equation (5.10) already has

```text
exp(O(logT/loglogT))
```

and other subpower terms.  Multiplying by `(logT)^C` only changes the
`O(logT/loglogT)` term, since

```text
C loglogT = o(logT/loglogT).
```

Thus the first P2.5-driven branch keeps the same `T^(1+delta)` conclusion.

### P2.7 insertion

BFMT equation (5.12) is already

```text
S_1 << N(T)(logT)^O(1).
```

The zero-sampling loss only changes the implicit exponent.

### P2.6 insertion

In the first parameter branch, BFMT obtains

```text
R_1 << N(T) exp(k^2(loglogT)^2) << T^(1+delta)
```

and

```text
R_2 << N(T)(logT)^O(1).
```

Multiplying by `(logT)^C` preserves both conclusions.  In the second branch,
equation (5.17) already carries

```text
exp(O(logT logloglogT/loglogT)).
```

The fixed polylog loss is again absorbed.

## Updated Target Hierarchy

The H1 separated-zero branch should now be recorded as:

```text
ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2)
  status: proof packet / rigorous reduction, pending final EC coefficient
          transcription notation.

SeparatedSimpleReciprocalBudget(E,c)
  follows if the rest of the BFMT negative-moment adaptation is transcribed
  with the zero-sampling propositions.

EC-BFMT-BadSetBudget(E,c)
  still independent and open.
```

This is better than the previous state.  The missing theorem is no longer a
Milinovich-Ng-like homogeneous zero-discrete mean value.  It is now a shorter
EC/newform transcription:

```text
BFMT-EC-Transcription(E,k=1/2):
  write the GL2 logarithmic approximation and coefficient families with
  lambda_f factors, insert the zero-sampling propositions, and verify the
  final separated negative first derivative moment.
```

## No-Promotion Boundary

Do not state:

```text
R_E,1(T)=o(T^2) is proved;
H1 rank-one is proved;
bad-set reciprocal budget is proved;
all multiple zeros are controlled;
Milinovich-Ng 4.1/4.3 proves BFMT;
GL1 sharp cutoff benefits from this.
```

The durable gain is narrower and real: the separated simple-zero coefficient
DPMV input has a homogeneous zero-sampling route with only polylog loss.

No Koyama correspondence or email drafts were read or edited.
