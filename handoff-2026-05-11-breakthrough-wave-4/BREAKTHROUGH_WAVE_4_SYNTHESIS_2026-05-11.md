---
schema_version: 1
title: "Breakthrough Wave 4 Synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.90
tags: [breakthrough-wave-4, h1, bfmt, gl2, reciprocal-derivative, h2, gl1, diagnostics]
---

# Breakthrough Wave 4 Synthesis

## Verdict

No unconditional/source-closed H1 theorem is promoted.

Wave 4 did produce a sharper conditional H1 stack. The separated BFMT branch
now has both local GL2 inputs conditionally available:

```text
GL2-BFMT-PrimePolynomialLowerBound(E)
GL2-ShiftDerivativeComparison(E,c)
```

but Agent 01 changes the separated branch bookkeeping: the GL2 lower bound is
conductor-normalized, with `C_E(t) asymp_E T^2`, not literally the zeta
archimedean term. Therefore the first new blocker is:

```text
Section5-GL2-ConductorAudit(E,k=1/2).
```

After that audit, the next independent blockers are:

```text
MinMod(E,c,A,h)
ProductLayer(E,c,A,h) or an equivalent complement tail
H1-MultipleEffectiveDegree-BFMT(E,W,r).
```

So the answer to the H1 question is: a complete conditional finite-box theorem
exists, but the finite-box theorem is not yet source-closed.

## Agent Packet Ledger

| agent | status | main result |
|---|---|---|
| 01 | `CONDITIONAL_THEOREM` | GL2 BFMT prime-polynomial lower bound closes only in conductor-normalized form; prime powers and bad primes cost `O_E(loglogT)`. |
| 02 | `CONDITIONAL_THEOREM` | Fixed-newform derivative-shift comparison closes under RH with `exp(O_(E,c)(logT/loglogT))` loss. |
| 03 | `CONDITIONAL_THEOREM` | Bad-set budget closes from `MinMod + ProductLayer`; count-only and pair-correlation-only routes still fail. |
| 04 | `CONDITIONAL_THEOREM` | Fixed-weight PV closure is reduced to an actual uniform dyadic-window PV hypothesis `H1-UDW-PV(E,W,r;H)`. |
| 05 | `RIGOROUS_REDUCTION` | Rank-one `R_E,1(T)=o(T^2)` is exactly a reciprocal-derivative high-tail problem; no fixed-EC tail theorem is sourced. |
| 06 | `CONDITIONAL_THEOREM` | H1 finite-box stack is complete only after all hidden assumptions are named. |
| 07 | `CONDITIONAL_THEOREM` | Multiple-zero terms require `D_alpha<r`; rank one requires `D_alpha<=0` plus aggregate control. |
| 08 | `CONDITIONAL_THEOREM` | S1 renormalized endpoint H2 closes conditionally with full right-lip retention/subtraction. |
| 09 | `CONDITIONAL_THEOREM` | H2/Sym2 composition is coherent in pointwise/profile/product-average modes; pointwise still needs `H2-PointwiseFinitePartClosure`. |
| 10 | `NO_GO` | GL1 sharp cutoff still needs its own moving-shell PV/absolute bound; smoothing/filtering does not transfer. |
| 11 | `RIGOROUS_REDUCTION` | Best secondary theorem-shaped task is Delta-2.5b registry execution; B+ and DPAC remain bounded side lanes. |
| 12 | `DIAGNOSTIC_ONLY` | EC numerics should distinguish residue domination from finite-grid artifact; no theorem promotion. |

## H1 Conditional Stack

The finite-box H1 theorem can be stated cleanly as a conditional theorem:

```text
C0. r=ord_(s=1)L(E,s)>=1.
C1. Fixed-kernel Mellin/Perron identity for c_E,W(e^u).
C2. Central residue normalization:
    Q_E,W(u)=(w_-1/L^(r)(E,1))u^r+O(u^(r-1)).
C3. Legal exponential finite-box heights and contour tails.
C4. No silent right-half residues.
C5. Fixed-newform RH/GRH and explicit formula inputs.
C6. Homogeneous zero-sampling BFMT coefficient transcription.
C7. Conductor-normalized separated BFMT:
    Agent01 + Agent02 + Section5-GL2-ConductorAudit(E,k=1/2).
C8. Bad-set complement:
    DirectComplementTail, or Agent03 MinMod + ProductLayer,
    or a stronger negative-moment/EC-WMC-type theorem.
C9. Multiple-zero control:
    H1-MultipleEffectiveDegree-BFMT(E,W,r).
```

Then

```text
c_E,W(e^u)=Q_E,W(u)+o(u^r)
          =(w_-1/L^(r)(E,1))u^r+o(u^r).
```

The simple-zero route is not a hidden assumption. It is:

```text
SeparatedEC-BFMT(E,c,k=1/2)
+ EC-BFMT-BadSetBudget(E,c)
=> R_E,1(T)=o(T^2).
```

Agent 04 supplies an alternative fixed-kernel PV mode:

```text
H1-UDW-PV(E,W,r;H)
=> simple-zero finite PV contribution is o(u^r),
```

but this is not implied by spacing, `l2` bounds, EC smoothing, or the separated
BFMT theorem.

## What Actually Improved

The GL2 BFMT local inputs are no longer vague missing boxes.

Agent 02 proves the derivative comparison, under fixed-newform RH:

```text
|L'(E,1+i gamma)|^(-1)
  <= exp(O_(E,c)(logT/loglogT))
     |L(E,1+1/logT+i gamma)|^(-1)
```

for simple separated zeros.

Agent 01 proves the prime-polynomial lower bound in the right GL2 form:

```text
log |L_E^*(s)|
 >= A_E(t;alpha,Delta)
    - Re sum_(p<=x) b_E(p;Delta) lambda_E(p) p^(-s)
    - C_E loglogT
    + small endpoint errors,
```

with

```text
A_E(t;alpha,Delta)
 = [log C_E(t)+O_E(1)]/(2 pi Delta)
     log(1-exp(-2 pi alpha Delta)) + O_E(1),
C_E(t) asymp_E T^2.
```

Prime squares, higher prime powers, and bad primes are harmless at
`O_E(loglogT)`. The non-harmless part is the changed conductor/gamma main
term. That is why `Section5-GL2-ConductorAudit(E,k=1/2)` is now the top task.

## Bad Set and Tail

Agent 03 turns the bad-set complement into a named conditional theorem:

```text
local cluster minimum modulus at scale 1/logT
+ inverse-product-distance layer cake
=> sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1)=o(T^2).
```

The pointwise minimum-modulus certificate is load-bearing:

```text
m_rho >= h(T)/T,   h(T)->infinity.
```

Pair counts or pair-correlation estimates may help the product-distance layer,
but they do not supply `m_rho`. Thus the old count-only bad-set route remains
dead.

Agent 05 confirms the exact rank-one absolute target:

```text
R_E,1(T)=sum_(T<|gamma|<=2T, simple)|L'(E,1+i gamma)|^(-1)=o(T^2).
```

This is equivalent to the high reciprocal-derivative tail being `o(T^2)`.
Milinovich-Ng positive moments, mollifier inputs, and signed estimates do not
provide that upper tail.

## Multiple Zeros

Agent 07 keeps the multiple-zero condition independent of BFMT. For each
retained critical-line exponent `alpha != 0`, after kernel zeros and same
exponent netting, the effective degree must satisfy:

```text
D_alpha < r.
```

For rank one:

```text
D_alpha <= 0
```

plus the degree-zero aggregate must be `o(u)`. Global offcentral simplicity is
sufficient but stronger than necessary.

## H2 Status

H2 improved, but it remains conditional.

Agent 08 closes the renormalized S1 endpoint theorem in conditional form:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)
```

provided right branches are absent, `o(1)`, or retained/subtracted as the full
cut-lip object:

```text
R_S1^+(K;E,W,eta,c).
```

The first Watson term alone is not enough when a right branch exists.

Agent 09 verifies that the Sym2/good-prime finite-part bookkeeping composes in
three modes:

```text
pointwise conditional theorem
profile theorem with retained oscillation
product-average theorem with explicit joint correlation input
```

The pointwise missing lemma is:

```text
H2-PointwiseFinitePartClosure(E,W,eta;c).
```

No H2 branch damping is imported into H1 reciprocal-pole residues.

## GL1 Sharp

Agent 10 is `NO_GO` for a new sharp GL1 theorem. The local residue algebra and
conditional finite-box wrapper are coherent, but the sharp cutoff retains the
critical harmonic weight

```text
1/((lambda-rho)L'(lambda,chi)).
```

The needed dyadic moving-shell statement is `o(U)`. Even linear reciprocal
mass gives only `O(U)`. Smoothed/filtering modes are separate theorem modes and
do not transfer back to the sharp cutoff without the same missing uniform tail.

## Secondary and Diagnostics

Agent 11 ranks the secondary lanes:

```text
1. Delta-2.5b registry execution
2. B+ sign-cluster classification
3. DPAC phase bridge hygiene
```

No Theorem B impact is claimed. B+ positivity remains dead.

Agent 12 freezes EC numerics as diagnostic only. The useful next numerical
question is whether finite smoothed behavior is:

```text
RESIDUE_DOMINATED_DIAGNOSTIC
```

or

```text
FINITE_GRID_ARTIFACT_DIAGNOSTIC.
```

The predeclared order is C2-prime first, then H1 residue fingerprints,
actual-vs-fake kernel filters, holdouts, and dense/jittered grids. No finite
gate promotes theorem closure before H1/H2 closure.

## Next Executable Breakthrough Task

The highest-leverage next task is:

```text
Section5-GL2-ConductorAudit(E,k=1/2).
```

Precise brief:

```text
Rerun BFMT Section 5 after replacing the zeta archimedean term by the GL2
conductor-normalized term A_E(t;alpha,Delta), with C_E(t) asymp_E T^2.
Verify that the k=1/2 separated negative first derivative moment still gives
sum_(rho in F_E(T,c)) |L'(E,rho)|^(-1) <<_(E,c,delta) T^(1+delta)
after all conductor/gamma, epsilon, and polylog losses are accounted for.
```

If this audit passes, the next task is not another separated-zero theorem. It
is the independent complement:

```text
prove MinMod(E,c,A,h) or a direct complement reciprocal tail.
```

Multiple-zero effective-degree control must remain in the finite-box theorem
statement throughout.

