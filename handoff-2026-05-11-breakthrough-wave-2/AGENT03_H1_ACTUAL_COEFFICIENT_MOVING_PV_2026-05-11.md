---
schema_version: 1
title: "Agent 03 - H1 actual-coefficient moving PV"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 03 - H1 Actual-Coefficient Moving PV"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.83
sources:
  - start.md
  - token-economy.yaml
  - L0_rules.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/DISPATCH_MANIFEST_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT01_H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT02_H1_FIXED_WEIGHT_PV_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_FIXED_WEIGHT_PV_NOGO_CONDITIONAL_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT05_EC_COMPOSITION_RANK_ZERO_PRODUCT_AVERAGE_2026-05-11.md
tags: [breakthrough-wave-2, agent03, ec-ndc, h1, actual-coefficients, moving-pv, fixed-weight]
---

# Agent 03 - H1 Actual-Coefficient Moving PV

status: `RIGOROUS_REDUCTION`

## Verdict

No fixed-curve EC theorem is promoted.

The actual-coefficient pointwise route is a clean moving-window theorem
candidate:

```text
a_gamma(E,W) = W_hat(i gamma) / L'(E,1+i gamma)
```

must satisfy a dyadic-window exponential-sum bound with these actual
coefficients, in the same legal-height scheme as the H1 contour.

For analytic rank one the useful shell condition is exactly:

```text
sum_(2^j <= H(2U)) B_j(E,W;U) = o(U),

B_j(E,W;U)
 = sup_(u in [U,2U])
   |sum_(2^j < |gamma| <= 2^(j+1))
      W_hat(i gamma) e^(i gamma u) / L'(E,1+i gamma)|.
```

For analytic rank `r >= 1`, replace `o(U)` by `o(U^r)`.

This is not proved by the current packets. It is the actual missing theorem.
The Wave 1 PV no-go remains valid as a proof-strategy obstruction, but the
sharper Wave 2 conclusion is:

```text
spacing/l2/profile inputs are irrelevant unless they imply the actual
B_j(E,W;U) shell budget above, absolute residue convergence, or coefficient
death/filtering for the same W.
```

## Setup

Use analytic rank only:

```text
r = ord_(s=1) L(E,s),
u = log K.
```

For simple offcentral zeros on the H1 line,

```text
rho = 1+i gamma,     gamma != 0,
a_gamma = W_hat(i gamma) / L'(E,rho).
```

Same-ordinate residues are combined before forming `a_gamma`. Multiple-zero
Laurent terms are not hidden in this packet; they must be killed by kernel
zeros, cancelled, retained explicitly, averaged, or proved to have effective
degree `< r`.

Let `H(U)` denote the legal H1 box height used by the finite-box contour on
the dyadic window `u in [U,2U]`. In the existing H1 packets this is an
exponential moving height,

```text
H(U) = exp(kappa U + O(1))
```

for some contour-dependent `kappa > 0`; the exact value is not needed here.

Define the cumulative actual-coefficient sum

```text
Z_H(u)
 = sum_(0 < |gamma| <= H) a_gamma e^(i gamma u).
```

## Moving-Window Theorem Candidate

`H1-actual-moving-PV(E,W,r)`:

Assume the local finite-height H1 contour identity

```text
c_E,W(e^u) = Q_E,W(u) + Z_H(u) + M_H(u) + I_H(u),
```

where `Q_E,W` is the central polynomial with leading coefficient
`1/L^(r)(E,1)` in the repository normalization, `M_H` contains the
offcentral multiple-zero Laurent terms, and `I_H` contains the shifted-line,
horizontal, original-line, and indentation errors.

Assume:

```text
1. legal heights:
   H = H(U) is allowed by the same contour scheme on u in [U,2U];

2. actual cumulative moving PV:
   sup_(u in [U,2U]) |Z_(H(U))(u)| = o(U^r);

3. contour tails:
   sup_(u in [U,2U]) |I_(H(U))(u)| = o(U^r);

4. multiple-zero boundary:
   every unretained offcentral Laurent term has effective degree < r,
   or is cancelled/kernel-killed/averaged in the declared theorem mode.
```

Then

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)          (r >= 1)
```

uniformly on dyadic windows.

The dyadic-shell condition in the verdict is a checkable sufficient condition
for item 2:

```text
sum_(2^j <= H(2U)) B_j(E,W;U) = o(U^r).
```

For rank one this says the moving Cesaro mean of actual shell suprema is
little-o:

```text
(1/U) sum_(2^j <= H(2U)) B_j(E,W;U) -> 0.
```

This is the exact shell target for a PV proof. It is stronger than a
Besicovitch/profile statement and weaker than absolute convergence.

## Relation To The Wave 1 PV No-Go

Wave 1 proved a logical no-go:

```text
zero spacing + coefficient l2 control
```

does not imply pointwise PV cancellation. Its model used artificial
coefficients and resonant lattice frequencies.

This packet does not use that model as an EC counterexample. For EC H1 the
only relevant coefficients are

```text
W_hat(i gamma) / L'(E,1+i gamma).
```

The Wave 1 obstruction still blocks any proof that only mentions spacing,
zero counting, or l2 magnitude data. To beat it one must use at least one
actual EC-specific input that changes the displayed shell sums themselves:

```text
actual phase cancellation:
  prove the B_j(E,W;U) shell budget;

absolute anti-small-derivative control:
  prove sum |W_hat(i gamma)/L'(rho)| is finite or has rank-one
  dyadic Cesaro budget o(U);

coefficient death:
  prove W_hat(i gamma)=0 or same-frequency aggregate a_gamma=0 for
  every surviving obstructing gamma;

mode change:
  keep the actual profile and prove only Besicovitch, log-Cesaro, or
  arithmetic product-average statements.
```

No current packet supplies the first three for a fixed EC and the current
fixed weight.

## EC-Specific Structure Audit

### Conjugation Symmetry

For real `W` and the usual EC functional-equation normalization,

```text
a_(-gamma) = conjugate(a_gamma).
```

Symmetric sums become

```text
2 Re(a_gamma e^(i gamma u)).
```

This makes the H1 profile real. It does not make it small.

Status: `NO_GO` as a pointwise PV mechanism.

### Mellin Decay

If

```text
|W_hat(i t)| <= C_W (1+|t|)^(-q),
```

then actual coefficient size is reduced by `T^(-q)` on a shell. For the
current smoothstep-scale packets, `q=2`.

This interacts with reciprocal-derivative budgets:

```text
absolute route:
  J_E,2(T) << T^(2q-1-delta);

profile/B^2 route:
  J_E,2(T) << T^(2q-delta);

moving PV route:
  J_E,2(T) << T^(2q-delta)
  plus an independent actual phase/sup theorem for B_j(E,W;U).
```

For `q=2`, absolute pointwise control needs `J_E,2(T) << T^(3-delta)`;
`J_E,2(T) << T^(4-delta)` is only profile-scale unless paired with the actual
moving shell theorem.

Status: `RIGOROUS_REDUCTION`.

### Functional Equation And Hadamard Coupling

The actual residue `1/L'(rho)` is not arbitrary. It is tied to the whole zero
configuration and to local near-multiple behavior.

This can beat the abstract model only if it yields one of:

```text
lower bounds / tail bounds for |L'(rho)|;
cluster cancellation of combined same-frequency residues;
direct phase decorrelation in B_j(E,W;U);
or contour control of 1/L(E,1+z) that implies the cumulative moving PV.
```

The read packets do not contain such a fixed-curve theorem.

Status: `RIGOROUS_REDUCTION` as a possible source, `NO_GO` as a closed input.

### Non-Lattice Or GUE-Like Zero Spacing

Non-lattice ordinates remove the exact integer resonance from the Wave 1 toy
model, but they do not prove the moving sup bound.

For pointwise dyadic suprema, randomness or linear independence is not a
substitute for an upper bound: finite phase blocks can recur, and spacing says
nothing about the actual phases of `1/L'(rho)`. These facts can support
averaged energy estimates only after coefficient-size hypotheses.

Status: `NO_GO` for pointwise moving PV.

### Kernel Zero Filtering

If a fixed admissible kernel satisfies

```text
W_hat(i gamma)=0
```

at all obstructing offcentral ordinates, then the corresponding actual
coefficients vanish and H1 residues are killed.

This is a genuine way around the abstract no-go, but it is not the present
fixed-weight theorem unless the same EC-dependent `W` is declared and proved
admissible for the H1 and H2 objects. It also changes the product-composition
problem because H2 must use the same kernel and normalization.

Status: `RIGOROUS_REDUCTION` as a separate filtered-kernel route; not a
promotion of the current fixed-weight PV theorem.

### H2 Branch Damping

H2 branch terms can carry endpoint damping. H1 simple residues are reciprocal
poles and do not receive that `1/u` damping.

Status: `NO_GO` for H1.

## Stronger Current No-Go

The stronger current no-go is not that EC actual coefficients fail. That has
not been proved.

The stronger no-go is:

```text
From the EC structures currently present in the Wave 1 packets, there is no
deduction of

  sup_(u in [U,2U]) |Z_(H(U))(u)| = o(U^r)

or of the shell sufficient condition

  sum_(2^j <= H(2U)) B_j(E,W;U) = o(U^r).
```

Consequences:

```text
r >= 1:
  positive-rank pointwise H1 closes only conditionally on actual moving PV,
  absolute residue convergence/Cesaro l1, or coefficient death.

r = 0:
  a convergent nonzero actual profile
    Z_W(u)=sum a_gamma e^(i gamma u)
  is main scale. A pointwise constant theorem requires coefficient death,
  exact cancellation, subtraction, or an averaged theorem mode.
```

If absolute convergence holds and any actual `a_gamma != 0`, then the rank-zero
profile is a nonconstant almost-periodic oscillation; it cannot be promoted to
a pointwise constant limit.

## Mode Boundaries

Pointwise positive-rank mode:

```text
Prove H1-actual-moving-PV(E,W,r), contour tails, and multiple-zero effective
degree < r. Then c_E,W(e^u)=Q_E,W(u)+o(u^r).
```

Absolute mode:

```text
Prove sum |W_hat(i gamma)/L'(rho)| < infinity,
or for rank one prove the dyadic Cesaro l1 shell budget o(U).
This bypasses PV phase cancellation.
```

Besicovitch/profile mode:

```text
Prove sum |a_gamma|^2 < infinity plus the needed close-pair control.
Then the zero profile exists only in B^2/dyadic mean square.
This is not pointwise H1.
```

Dyadic log-Cesaro mode:

```text
Fixed nonzero H1 frequencies average to zero after tail justification.
This is an averaged theorem in u=log K, not pointwise stabilization.
```

Product-average mode:

```text
Average c_E,W(e^u) P_E,W(e^u) itself.
The constant includes diagonal H1/H2 correlations
  exp(B_H2)(q_r d_0 + sum h_gamma d_(-gamma)).
Do not replace this by averaged log P or by a pointwise constant theorem.
```

Filtered-kernel mode:

```text
If W_hat kills offcentral ordinates, H1 residues can vanish.
This is a different declared kernel route and must be rechecked through H2.
```

## Verification Notes

Commands/checks:

```text
./te doctor
sed reads of targeted context files only after start.md/L1_index.md
git status --short on the target output directory and named context files
test -e target Agent 03 output before writing
```

External theorem claims: none added. Therefore no new `curl + pdftotext`
source packet was required.

Protocol checks:

```text
status enum used: RIGOROUS_REDUCTION
analytic rank only
no H2 branch damping used for H1
no Koyama correspondence/email drafts edited or used as source
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT03_H1_ACTUAL_COEFFICIENT_MOVING_PV_2026-05-11.md
```
