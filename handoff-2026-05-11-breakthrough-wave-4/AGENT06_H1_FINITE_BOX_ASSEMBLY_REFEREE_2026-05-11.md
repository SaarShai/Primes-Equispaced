---
title: "AGENT06 H1 finite-box assembly referee"
date: 2026-05-11
type: theorem-reduction
tier: working
status: CONDITIONAL_THEOREM
confidence: 0.90
tags: [breakthrough-wave-4, h1, finite-box, referee, bfmt, reciprocal-derivative, multiple-zeros]
---

# Verdict

`CONDITIONAL_THEOREM`.

The Wave 4 packets assemble into a complete conditional finite-box H1 theorem,
but not into a source-closed H1 theorem. The conditional stack is valid only
after naming all load-bearing inputs:

```text
finite-box contour legality
+ fixed-newform RH/GRH and explicit formula inputs
+ GL2 conductor-normalized BFMT Section 5 audit
+ separated EC-BFMT
+ bad-set reciprocal derivative complement
+ no-silent-right-half-residue rule
+ multiple-zero effective-degree and aggregate control
=> finite-box H1 central term with lower-order offcentral contribution.
```

No packet proves the final H1 statement unconditionally. The first unclosed
source audit inside the separated BFMT branch is the conductor-normalized
Section 5 rerun forced by Agent01. The first unclosed analytic complement after
the separated branch is Agent03's minimum-modulus/value-size layer.

# Theorem Target

Fix an elliptic curve `E/Q`, analytic rank

```text
r = ord_(s=1) L(E,s) >= 1,
u = log K,
```

and a fixed H1 kernel `W` with

```text
W_hat(z)=w_-1/z + holomorphic at z=0,
|W_hat(x+it)| <<_W (1+|t|)^(-2)
```

on the finite-box contour strips. Use project normalization

```text
rho = 1+i gamma
```

for EC zeros.

Target conclusion:

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)
           = (w_-1/L^(r)(E,1)) u^r + o(u^r)
```

in the same pointwise finite-box mode as the prior H1 finite-box theorem.

Primary absolute route for simple critical-line zeros:

```text
R_E,1(T) =
  sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-1)
  = o(T^2).
```

This is the rank-one exact target and is stronger than the finite-box
`o(T^2(log T)^(r-1))` simple-zero budget for every fixed `r>=1`.

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: separated EC-BFMT at `k=1/2` reduces to two GL2 local inputs plus zero-sampling coefficient transcription; bad set and multiple zeros are explicitly outside scope.
- `AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md`: supplies the prime-polynomial lower bound only in conductor-normalized form; literal zeta archimedean bookkeeping is false.
- `AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`: supplies the derivative-shift comparison for simple separated zeros under fixed-newform RH.
- `AGENT03_EC_BFMT_BADSET_BUDGET_2026-05-11.md`: gives a conditional bad-set theorem from `MinMod + ProductLayer`; pair counts alone do not control reciprocal derivatives.
- `AGENT04_H1_FIXED_WEIGHT_PV_THEOREM_2026-05-11.md`: gives a deterministic fixed-weight PV substitute, conditional on the actual dyadic-window maximal cancellation budget.
- `AGENT05_H1_RECIPROCAL_TAIL_THEOREM_2026-05-11.md`: reduces rank-one simple-zero H1 to a reciprocal-derivative upper tail; no fixed-curve tail theorem is source-closed.
- `AGENT07_MULTIPLE_ZERO_EFFECTIVE_DEGREE_2026-05-11.md`: multiple zeros are independent of BFMT simple-zero control and require effective-degree plus aggregate control.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT07_H1_FINITE_BOX_THEOREM_SECTION_2026-05-11.md`: names the finite-box contour, central-normalization, legal-height, no-right-residue, simple-zero, and multiple-zero hypotheses.

# Dependency Graph

```text
Fixed-newform RH/GRH
  -> Agent02: GL2-ShiftDerivativeComparison(E,c)
  -> Agent01: GL2-BFMT-PrimePolynomialLowerBound(E), conductor-normalized

BFMT EC transcription
  + homogeneous zero-sampling coefficient propositions
  + Agent02
  + Agent01
  + NEW: Section5-GL2-ConductorAudit(E,k=1/2)
  -> SeparatedEC-BFMT(E,c,k=1/2):
       sum_(rho in F_E(T,c)) |L'(E,rho)|^(-1)
       <<_(E,c,delta) T^(1+delta)

Agent03:
  MinMod(E,c,A,h) + ProductLayer(E,c,A,h)
  -> EC-BFMT-BadSetBudget(E,c):
       sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2)

SeparatedEC-BFMT(E,c,k=1/2)
  + EC-BFMT-BadSetBudget(E,c)
  -> Agent05 absolute simple-zero route:
       R_E,1(T)=o(T^2)

Finite-box contour package
  + no-silent-right-half-residue rule
  + R_E,1(T)=o(T^2)
  + Agent07 H1-MultipleEffectiveDegree-BFMT(E,W,r)
  -> c_E,W(e^u)=Q_E,W(u)+o(u^r)

Alternative simple-zero route:
  Agent04 H1-UDW-PV(E,W,r;H)
  -> simple-zero finite PV contribution is o(u^r)
  -> may replace R_E,1(T)=o(T^2) for this fixed W,
     but does not remove multiple-zero or right-half-residue hypotheses.
```

# Referee Report

## Agent01

Accepted only with a new named audit:

```text
Section5-GL2-ConductorAudit(E,k=1/2).
```

Agent01 correctly rejects the literal zeta-form lower bound. The GL2
archimedean term uses

```text
C_E(t) asymp_E T^2
```

not the zeta `T` scale. The prior BFMT transcription treats the lower-bound
bookkeeping as a `(\log T)^C` loss, but Agent01 changes the main
conductor-normalized archimedean term. A final separated-branch theorem must
rerun BFMT Section 5 with this replacement and verify the final
`T^(1+delta)` estimates still survive after epsilon/delta margin reduction.

Without that audit, `SeparatedEC-BFMT(E,c,k=1/2)` is not source-closed.

## Agent02

Accepted as a local separated-zero input under fixed-newform RH. It proves only

```text
|L'(E,1+i gamma)|^(-1)
<= exp(O_(E,c)(logT/loglogT))
   |L(E,1+1/logT+i gamma)|^(-1)
```

for simple separated zeros. It gives no bad-set, multiple-zero, or finite-box
closure.

## Agent03

Accepted as a conditional bad-set theorem, not as a proof from spacing.

The minimum-modulus layer is load-bearing:

```text
MinMod(E,c,A,h):  m_rho >= h(T)/T, h(T)->infinity.
```

This is not a zero-count, pair-correlation, or spacing consequence. It is a
value-size lower bound on zero-free cluster boundaries. Calling it a bad-set
budget without naming `MinMod` would hide the missing reciprocal-derivative
input. `ProductLayer` controls geometry; `MinMod` controls scale. Both are
required for Agent03's complement theorem.

## Agent04

Agent04 is an alternative simple-zero closure mode, not an additional
requirement on the absolute BFMT route. Its hypothesis

```text
H1-UDW-PV(E,W,r;H)
```

is an actual fixed-coefficient dyadic-window cancellation theorem. It may
replace the absolute `R_E,1(T)=o(T^2)` route for the fixed kernel `W`, but it is
not implied by spacing, `l2`, profile bounds, or the BFMT separated branch.
With separated BFMT available, Agent04 reduces PV work to the bad set; it does
not close that bad-set PV work.

## Agent05

Agent05 is the absolute-value route used in the primary stack. It proves a
rigorous reduction:

```text
SeparatedEC-BFMT(E,c,k=1/2) + complement tail/budget
=> R_E,1(T)=o(T^2).
```

It does not prove the reciprocal tail. Agent03's `MinMod + ProductLayer` is one
acceptable complement condition; direct tail, negative moment, or EC-WMC-style
conditions are stronger alternatives.

## Agent07

Agent07 is independent and mandatory unless replaced by a stronger explicit
multiple-zero condition such as global offcentral simplicity.

BFMT controls only simple separated zeros. Agent03/05 also sum only simple
zeros. Therefore multiple-zero Laurent residues must still satisfy

```text
D_alpha < r
```

after kernel zeros, internal cancellation, and exact same-exponent netting,
plus lower-degree aggregate control. For rank one this is `D_alpha <= 0` and
the degree-zero aggregate must be `o(u)`.

# Complete Conditional Stack or First Blocker

Complete conditional theorem, absolute BFMT route:

Assume all of the following.

```text
C0. Analytic rank:
    r=ord_(s=1)L(E,s)>=1.

C1. Fixed kernel and Perron identity:
    W has the stated pole/decay, and the exact fixed-kernel Mellin/Perron
    identity for c_E,W(e^u) holds on Re z=sigma, 1/2<sigma<3/2.

C2. Central normalization:
    Q_E,W(u)=Res_(z=0) e^(uz)W_hat(z)/L(E,1+z)
    has top coefficient w_-1/L^(r)(E,1).

C3. Legal exponential finite box:
    for some 1/2<eta<1 and C>sigma there are heights
    T_box(u)=exp(Cu+O(1)) at which original-line tail, shifted-left line,
    and horizontal edges are all o(u^r).

C4. No silent right-half residues:
    every crossed pole with Re z>0 is absent, kernel-killed, explicitly
    retained outside the central-only claim, or controlled by a named theorem.

C5. Fixed-newform RH/GRH and standard explicit-formula package:
    enough to support Agents 01 and 02 and the separated-zero normalization.

C6. Zero-sampling coefficient transcription:
    BFMT propositions 2.5, 2.6, 2.7 transcribe to the fixed EC coefficients
    with only T^o(1) losses.

C7. Conductor-normalized separated BFMT:
    Agent02 shift comparison, Agent01 conductor-normalized lower bound, and
    Section5-GL2-ConductorAudit(E,k=1/2) imply
    SeparatedEC-BFMT(E,c,k=1/2).

C8. Bad-set complement:
    either DirectComplementTail(E,c), or Agent03's
    MinMod(E,c,A,h)+ProductLayer(E,c,A,h), or a stronger negative-moment /
    EC-WMC-style theorem, gives
    EC-BFMT-BadSetBudget(E,c).

C9. Multiple-zero control:
    H1-MultipleEffectiveDegree-BFMT(E,W,r), including D_alpha<r for every
    retained critical-line multiple-zero exponent, lower-degree aggregate
    control, and the right-half residue rule for multiple zeros.
```

Then

```text
c_E,W(e^u)=Q_E,W(u)+o(u^r)
          =(w_-1/L^(r)(E,1))u^r+o(u^r).
```

Derivation of the simple-zero input is explicit, not assumed:

```text
C7 gives sum_(F_E(T,c)) |L'(E,rho)|^(-1) << T^(1+delta).
C8 gives sum_(B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2).
Therefore R_E,1(T)=o(T^2).
```

Alternative conditional theorem:

Replace `C7+C8` by Agent04's actual fixed-weight PV hypothesis
`H1-UDW-PV(E,W,r;H)` for the chosen kernel and height mode. This closes the
simple-zero finite PV contribution for that `W`, but `C0-C4` and `C9` remain
mandatory.

First blocker for an unconditional/source-closed promotion:

```text
Section5-GL2-ConductorAudit(E,k=1/2)
```

inside the separated branch. After that, the next independent blockers are

```text
MinMod(E,c,A,h) for bad clusters,
ProductLayer(E,c,A,h) or an equivalent complement tail,
H1-MultipleEffectiveDegree-BFMT(E,W,r).
```

# Dependency Impact

- Do not promote final H1 from Agents 01-02 alone. They address only separated
  simple zeros and still require the conductor-normalized Section 5 audit.
- Do not cite Agent03 as a pair-correlation closure. Its minimum-modulus layer
  is an independent value-size hypothesis.
- Treat Agents 04 and 05 as substitute simple-zero modes: fixed-weight PV route
  versus absolute reciprocal-tail route. The primary BFMT assembly uses Agent05;
  Agent04 is not additionally required.
- Keep Agent07 in every central-only finite-box H1 theorem unless global
  offcentral simplicity, kernel killing, or an explicit retained-oscillation
  theorem replaces it.
- Clean carry-forward target: prove `Section5-GL2-ConductorAudit`, then prove a
  fixed-curve local minimum-modulus theorem or a direct complement reciprocal
  tail, while maintaining the independent multiple-zero audit.
