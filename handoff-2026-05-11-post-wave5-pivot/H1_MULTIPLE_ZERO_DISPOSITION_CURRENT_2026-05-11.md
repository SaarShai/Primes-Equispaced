---
schema_version: 2
title: "H1 Multiple Zero Disposition Current"
type: theorem-reduction
domain: project
tier: working
confidence: 0.86
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT07_MULTIPLE_ZERO_REMOVAL_OR_RETAINED_PROFILE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT07_MULTIPLE_ZERO_EFFECTIVE_DEGREE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT04_H1_FINITE_BOX_THEOREM_ASSEMBLY_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md
supersedes: []
superseded-by:
tags: [post-wave5, h1, multiple-zeros, laurent-control, retained-profile, conditional-stack]
---

# H1 Multiple Zero Disposition Current

Status: `RIGOROUS_PACKAGING_REDUCTION`.

No multiple-zero theorem is promoted.

## Verdict

The post-Wave-5 simple-zero branch does not change the multiple-zero algebra.
It only supplies the simple-zero input for the finite-box H1 theorem,
conditionally on `RootedPalmRepulsionExpMoment_2(E,A)`.

Therefore the correct remaining condition is still:

```text
H1-MultipleZeroDisposition(E,W,r).
```

Do not call it `H1-MultipleEffectiveDegree-BFMT`.  BFMT and the q=2 shifted
bad-set route are simple-zero tools.

## Current H1 Stack

The current rank-one pointwise central-only H1 route is:

```text
1. H1 finite-box contour package and no-silent-right-half-residue rule.

2. Simple-zero budget:
   WeakSeparatedEC-BFMT-H1-Audit(E,c)
   + Degree2WeakShiftedNeg_2(E)
   + RootedPalmRepulsionExpMoment_2(E,A)
   => R_E,1^simp(T)=o(T^2).

3. Multiple-zero disposition:
   H1-MultipleZeroDisposition(E,W,1).
```

This gives the central-only rank-one conclusion only if the multiple-zero
profile is absent, killed, retained outside the central-only claim, or
central-negligible.

## Disposition Modes

For every crossed offcentral multiple zero `rho=1+alpha`, let

```text
m = ord_(s=rho) L(E,s).
```

The Laurent residue has the form

```text
P_alpha(u)
  = e^(alpha u) sum_(ell=0)^(D_alpha) A_(alpha,ell)^net u^ell,
```

after kernel zeros, local Laurent cancellation, and same-exponent netting.

Every such term must be handled in exactly one mode:

```text
(A) absent by H1-OffcentralCriticalSimplicity(E);

(B) killed by H1-MultipleZeroKernelKill(E,W);

(C) retained in an explicit H1-RetainedMultipleZeroProfile(E,W;T_box);

(D) unretained and central-negligible:
    D_alpha < r, with lower-degree aggregate o(u^r).
```

Mode `(D)` is the old effective-degree condition without the misleading BFMT
suffix.

## Rank-One Specialization

For rank one, `r=1`.  Central-only pointwise H1 needs:

```text
D_alpha <= 0
```

for every unretained critical-line multiple-zero exponent, plus

```text
Z_0^mult(u)
 = sum_(Re alpha=0, alpha!=0, mult)
     A_(alpha,0)^net e^(alpha u)
 = o(u).
```

Absolute convergence or boundedness of `Z_0^mult` is a convenient sufficient
condition.

An uncancelled double zero with no kernel zero has generic degree `1`, equal to
the rank-one central degree, and blocks a central-only pointwise theorem unless
it is killed, cancelled, retained, or moved to a proved averaged/profile mode.

## Profile Theorem Alternative

If central-only H1 is too strong, use the honest profile conclusion:

```text
c_E,W(e^u)
 = Q_E,W(u) + P_mult,box(u) + o(u^r).
```

This mode can retain multiple-zero terms instead of proving they are
negligible.  It is not the same theorem as central-only H1; downstream H1/H2
composition must keep, subtract, average, or otherwise dispose of the same
profile.

## Boundary

Promote:

```text
Simple-zero conditional stack + H1-MultipleZeroDisposition(E,W,r)
is the current paper-safe H1 packaging.
```

Do not promote:

```text
offcentral simplicity,
bounded multiplicity,
kernel killing for a fixed W,
central-only H1,
full H1.
```

The next source task for this blocker is not BFMT.  It is either an
offcentral-simplicity/bounded-multiplicity theorem for the fixed EC, or a
Laurent coefficient/profile convergence theorem in the exact H1 mode.
