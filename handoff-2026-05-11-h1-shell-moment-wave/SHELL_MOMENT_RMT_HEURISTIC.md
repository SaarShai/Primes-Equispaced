---
schema_version: 1
title: "Shell moment RMT heuristic"
date: 2026-05-11
agent: "Agent 3"
type: heuristic-audit
tier: working
status: AUDIT_ONLY
confidence: 0.74
sources:
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md
tags: [ec-ndc, h1, shell-moment, rmt, heuristic]
---

# Shell Moment RMT Heuristic

Status: `AUDIT_ONLY`.

Confidence: `0.74`.

Dependencies:

- Same normalization as the H1 wave: fixed elliptic curve/GL2 object with
  critical line written as `s=1+i gamma`.
- Simple offcentral zeros. Multiple zeros make `|L'(rho)|^(-2)` infinite and
  are outside this model calculation.
- EC/GL2 zero count in shells: `N_E(T,2T) ~ T log T` up to constants.
- Smoothstep-scale H1 kernel decay `q=2`, so the proof-wave dyadic target is
  `theta < 3`.
- Characteristic-polynomial derivative model is used only as heuristic.

## Do Not Promote Unless

- A fixed-EC/GL2 theorem proves the reciprocal derivative shell upper bound,
  or a source packet cites one using the project protocol:
  `curl + pdftotext + short quote + page/eq`.
- The RMT estimate below is labelled heuristic/model-only, not theorem.
- Any statement about small derivative tails includes the simplicity and
  level-repulsion assumptions.
- Any use of zeta/Gonek-style reciprocal derivative predictions is labelled
  analogy only unless a fixed-EC/GL2 source is checked.
- The target `J_E,2(T) <= T^(3-delta)` is described as sharp for H1 dyadic
  summability at `q=2`, not sharp as an RMT prediction for `J_E,2(T)`.

## Executive Verdict

Under the characteristic-polynomial derivative heuristic,

```text
J_E,2(T) := sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
```

should have size

```text
J_E,2(T) = T * (log T)^(O(1))
```

and more naturally `~ C_E T` after the correct arithmetic normalization.

Thus the shell target

```text
J_E,2(T) <= T^(3-delta)
```

is very likely true in the model and is much too weak as a prediction for the
moment itself. It is sharp only as the Cauchy-Schwarz summability threshold
for the current `q=2` H1 kernel. RMT suggests any fixed `delta < 2` should be
morally safe after log losses.

The target is not expected to be dominated by rare events in expectation.
However, finite samples and high moments are tail-sensitive: unusually close
pairs of zeros can create large terms, and no rigorous H1 theorem may ignore
that tail.

## Model Calculation

Use the local unitary characteristic-polynomial derivative model at height
`T`. The effective matrix size is

```text
N ~ log analytic conductor ~ log T
```

up to degree/conductor constants. A unit height window contains about `N`
zeros. The derivative of the characteristic polynomial at one eigenvalue has
negative second moment of scale

```text
average_eigenvalue |Lambda'(eigenvalue)|^(-2) ~ N^(-1)
```

in the normalization matching L-function derivative size.

Therefore one unit height window contributes

```text
N zeros * N^(-1) ~ 1.
```

A dyadic shell has length `T`, hence

```text
J_E,2(T) ~ C_E T
```

with possible arithmetic constants and log-normalization losses depending on
the exact GL2 conductor normalization.

This matches the usual Gonek-style exponent for zeta reciprocal derivatives,
but no external zeta theorem or conjecture is cited here as a source claim.
This file uses the analogy only as heuristic context.

## Comparison With H1 Target

The H1 dyadic lemma needs

```text
J_E,2(T) <= C_E T^theta (log T)^B,
theta < 2q - 1.
```

For `q=2`, this is

```text
theta < 3.
```

If the model gives `theta=1`, the H1 requirement has about two powers of
slack:

```text
T * polylog(T) << T^(3-delta)
```

for every fixed `delta < 2`.

So:

```text
RMT sharp exponent for J_E,2:       theta = 1, up to logs.
H1 summability threshold at q=2:    theta < 3.
Requested shell target:             theta = 3-delta.
```

Conclusion:

```text
likely true: yes, under the model;
too weak as moment prediction: yes;
too strong: no, unless delta >= 2 is demanded;
rare-event dominated: not in expectation, but tail-sensitive.
```

## Small Derivative Tail Risk

In the unitary model, a very small derivative at an eigenvalue is mainly caused
by a very close neighboring eigenvalue. If `s` is normalized nearest-neighbor
spacing, unitary level repulsion gives the small-spacing heuristic

```text
Prob(s <= x) ~ C x^3.
```

The derivative has a local factor proportional to `s`, so

```text
Prob(|normalized derivative| <= x) ~ C x^3.
```

Then

```text
E |D|^(-2) < infinity
```

because the density near zero behaves like `x^2`, and

```text
int_0 x^(-2) x^2 dx
```

is finite at zero.

But this is close enough to the edge that higher negative moments are
dangerous. For example, the same heuristic predicts divergence at sufficiently
large negative moment order. Equivalently, the random variable
`|D|^(-2)` has a heavy tail of rough order

```text
Prob(|D|^(-2) > y) ~ C y^(-3/2).
```

Implications:

- The first moment relevant to `J_E,2` is expected finite.
- Variance and higher tail diagnostics may be unstable.
- Extreme close pairs can cause visible spikes in finite data.
- Pair correlation or level repulsion alone does not prove the required
  arithmetic derivative bound.
- Multiple zeros are fatal unless excluded or retained separately.

## Sharpness For Proof Strategy

The target `T^(3-delta)` is sharp for the existing H1 proof strategy because
the Cauchy-Schwarz shell estimate gives

```text
|A_T(u)| <= T^((1 - 2q + theta)/2) * polylog(T).
```

For `q=2`, dyadic summability requires

```text
1 - 4 + theta < 0,
theta < 3.
```

At `theta=3`, the dyadic exponent is zero and the shell series need not
converge absolutely. Thus `3` is the exact no-cancellation threshold for this
kernel and this proof shape.

This sharpness does not mean RMT expects `J_E,2(T)` near `T^3`. The model
expects `T`, far below the proof threshold.

## Source Status

External theorem citations: none.

Reason: this deliverable is an RMT/heuristic audit. No external RMT theorem is
promoted. The characteristic-polynomial derivative estimates above are
model-only and must be source-checked before use as cited claims in a paper.

Required source protocol for any future promotion:

```text
curl source PDF
pdftotext source PDF
record SHA256
quote the exact sentence/equation
record PDF page and equation/theorem number
state use and limit
```

## Final Classification

For the H1 shell moment:

```text
J_E,2(T) <= T^(3-delta)
```

is:

```text
likely true under RMT/characteristic-polynomial heuristics;
too weak as a prediction of the actual derivative moment;
sharp only as the q=2 dyadic summability threshold;
not expected to be expectation-dominated by rare events;
still rigorously exposed to small-derivative and multiple-zero tails.
```

