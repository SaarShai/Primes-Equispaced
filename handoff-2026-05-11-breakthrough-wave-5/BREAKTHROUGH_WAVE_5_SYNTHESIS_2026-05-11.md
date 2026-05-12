---
schema_version: 1
title: "Breakthrough Wave 5 Synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: NO_GO
confidence: 0.92
tags: [breakthrough-wave-5, h1, bfmt, gl2, reciprocal-derivative, h2, gl1, diagnostics]
---

# Breakthrough Wave 5 Synthesis

## Verdict

No H1 theorem is promoted. More sharply: the current separated EC-BFMT route at
`k=1/2` is killed by the conductor-normalized Section 5 audit.

Wave 4 identified the next blocker as:

```text
Section5-GL2-ConductorAudit(E,k=1/2).
```

Wave 5 resolves that blocker negatively. The GL2 analytic conductor has

```text
log C_E(t) = 2 log T + O_E(1),
```

so BFMT Lemma 2.4 entering Section 5 equation `(5.13)` changes the decisive
coefficient:

```text
2k -> 4k.
```

At `k=1/2`, the small-block sign condition becomes:

```text
a(2d-1) > 2,
```

which is unavailable in the BFMT support regime. Prime powers, bad primes,
zero-sampling, polylog losses, and the derivative-shift comparison are not the
obstruction.

The new first blocker is therefore:

```text
ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2),
```

or a genuinely different degree-2 separated negative-moment theorem.

## Agent Packet Ledger

| agent | status | main result |
|---|---|---|
| 01 | `NO_GO` | Section 5 GL2 conductor audit fails: `log C_E(t)=2logT+O_E(1)` changes `2k` to `4k`. |
| 02 | `NO_GO` | Margin referee confirms the first mismatch is the fixed conductor coefficient, not `T^o(1)`, polylog, endpoint, or support bookkeeping. |
| 03 | `NO_GO` | `SeparatedEC-BFMT(E,c,k=1/2)` is not proved from current inputs; weakest replacement is a new conductor-normalized sign lemma. |
| 04 | `NO_GO` | No source-closed `MinMod(E,c,A,h)`; standard tools give scales too weak for `h(T)/T`. |
| 05 | `RIGOROUS_REDUCTION` | `ProductLayer` sharpens to rooted inverse-product correlation `J_m(T;A)`, but remains independent of `MinMod`. |
| 06 | `RIGOROUS_REDUCTION` | Direct complement tail reduces to fixed-EC reciprocal derivative upper tails; no source-closed theorem. |
| 07 | `RIGOROUS_REDUCTION` | Replace `H1-MultipleEffectiveDegree-BFMT` with `H1-MultipleZeroDisposition(E,W,r)` or retained profile mode. |
| 08 | `NO_GO` | H1 finite-box referee names the first blocker: `ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2)`. |
| 09 | `CONDITIONAL_THEOREM` | H2 pointwise finite part closes conditionally with full `R_S1^+`; blockers remain regular left edge, Sym2 zero ledger, and right-profile cancellation. |
| 10 | `NO_GO` | GL1 sharp still needs actual moving-shell PV or absolute harmonic-weight bound; smoothing/filtering cannot transfer. |
| 11 | `RIGOROUS_REDUCTION` | Delta-2.5b registry execution plan is ready; no registry files edited and no Theorem B impact. |
| 12 | `DIAGNOSTIC_ONLY` | EC diagnostic residue classifier is predeclared after C2-prime; no theorem-promotion language. |

## H1 Result

The failed implication is:

```text
GL2-ShiftDerivativeComparison(E,c)
+ GL2-BFMT-PrimePolynomialLowerBound(E), conductor-normalized
+ ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2)
does not imply
SeparatedEC-BFMT(E,c,k=1/2)
```

from current Wave 5 inputs.

The exact failed step is BFMT Lemma 2.4 into Section 5 `(5.13)`. With

```text
T^(beta_j) = exp(2 pi Delta_j),
alpha = 1/log T,
2 pi alpha Delta_j = beta_j,
```

the zeta archimedean factor contributes:

```text
beta_j^(-1) log(1-exp(-beta_j)).
```

The fixed-curve GL2 conductor-normalized term contributes:

```text
(2+o(1)) beta_j^(-1) log(1-exp(-beta_j)).
```

After inversion and BFMT power `2k`, the small-block penalty doubles. At
`k=1/2`, this creates a fixed-power gap, not a polylogarithmic or `T^o(1)`
loss.

Consequences:

```text
SeparatedEC-BFMT(E,c,k=1/2)       not proved
R_E,1(T)=o(T^2)                   not proved
central-only finite-box H1        not proved
```

## Remaining H1 Blockers

The first blocker is the separated branch:

```text
ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2)
```

or a new degree-2 separated negative-moment theorem at `alpha=1/log T`.

If that blocker is repaired, the independent downstream blockers are still:

```text
Bad-set complement:
  DirectComplementTail(E,c), or
  MinMod(E,c,A,h)+ProductLayer(E,c,A,h), or
  fixed-EC reciprocal-tail / negative-moment / WMC theorem.

Multiple-zero disposition:
  H1-MultipleZeroDisposition(E,W,r),
  or retained profile P_mult,box(u) in the theorem conclusion.
```

Agent 04 kills the currently hoped-for source route to `MinMod`: selected
heights are not zero-centered microscopic boundary circles, and standard local
tools give scales such as

```text
exp(-C logT loglogT)
```

or at best `T^(-C)`, not `h(T)/T`.

Agent 05 improves the geometry side by reducing `ProductLayer` to rooted
singular local-correlation sums:

```text
J_m(T;A).
```

This is useful only after a value-scale input such as `MinMod` exists.

Agent 07 improves the finite-box statement: stop calling the multiple-zero
condition BFMT-specific. Use:

```text
H1-MultipleZeroDisposition(E,W,r).
```

Every crossed offcentral multiple-zero residue must be absent by named
simplicity, killed by kernel order, retained in a profile, or proved
central-negligible by effective degree and aggregate control.

## H2, GL1, Secondary, Diagnostics

H2 is better but still conditional. Agent 09 closes the algebraic pointwise
finite-part assembly in the exact local convention:

```text
S1 + (1/2) Sym2 - (1/2) Mertens -> coefficient -r.
```

It retains or subtracts the full `R_S1^+` right-lip term. The blockers are:

```text
RegularLogLeftEdge,
Sym2-ZeroLedger-RegularLog,
right-profile vanish/cancellation.
```

No H2 damping is imported into H1.

GL1 sharp remains `NO_GO`. The missing input is still:

```text
GL1-ActualMovingShellPV
```

or an absolute harmonic-weight theorem. Fixed smoothing/filtering cannot imply
sharp cutoff control.

Delta-2.5b is ready as an execution plan only. The proposed patch should add
the ramified correction divisor / axis-pole multiplicity proposition and remove
stale Open 7.2 / Open 10.2 language. No Theorem B impact is claimed.

EC numerics remain diagnostic only. The next diagnostic classifier runs only
after C2-prime and classifies outcomes as:

```text
RESIDUE_DOMINATED_DIAGNOSTIC
FINITE_GRID_ARTIFACT_DIAGNOSTIC
NUMERICS_PAUSE
```

## Next Executable Breakthrough Task

Do not run another BFMT transcription wave without a new idea for the
degree-2 conductor problem.

The next highest-leverage H1 task is:

```text
ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2)
```

with a precise target:

```text
Find a replacement for BFMT Section 5 that offsets the conductor degree
doubling log C_E(t)=2logT+O_E(1), while preserving the Dirichlet-polynomial
support constraints needed for the zero-sampling coefficient propositions.
```

If that looks structurally impossible, the alternative breakthrough task is a
new fixed-curve degree-2 separated negative-moment theorem for

```text
L(E,1+1/logT+i gamma)
```

on separated EC zeros, bypassing BFMT Section 5.

