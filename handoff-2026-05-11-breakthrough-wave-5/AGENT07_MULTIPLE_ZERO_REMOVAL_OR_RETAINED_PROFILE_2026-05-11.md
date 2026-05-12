---
title: "Agent 07 multiple-zero removal or retained profile"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.88
tags: [breakthrough-wave-5, h1, multiple-zeros, retained-profile, kernel-killing, simplicity, bfmt]
---

# Verdict

Replace the name

```text
H1-MultipleEffectiveDegree-BFMT(E,W,r)
```

in paper-facing statements. BFMT does not control multiple zeros, so the suffix
is misleading.

Clean replacement:

```text
H1-MultipleZeroDisposition(E,W,r)
```

Every crossed offcentral multiple-zero residue is handled in exactly one of
these modes:

```text
absent by a named offcentral-simplicity hypothesis;
kernel-killed to full pole order;
retained in an explicit multiple-zero profile;
or, for central-only mode, satisfies the Wave 4 effective-degree and aggregate
condition.
```

This is a successful simplification only at theorem-packaging level. It does
not source-close global/offcentral simplicity, does not prove fixed-kernel
infinite zero killing, and does not let a central-only theorem discard a
surviving degree-`>=r` profile. If the final claim remains

```text
c_E,W(e^u)=Q_E,W(u)+o(u^r),
```

then the Wave 4 condition is still the minimal checkable fallback.

# Theorem Target

Let

```text
r = ord_(s=1) L(E,s) >= 1,
u = log K,
c_E,W(e^u) = (1/(2 pi i)) int e^(u z) W_hat(z)/L(E,1+z) dz.
```

Assume the Wave 4 finite-box contour package, central normalization, legal
height sequence, simple-zero BFMT/bad-set input, and no-silent-right-half
residue rule.

For a crossed offcentral multiple zero `rho=1+alpha`, `m=ord_(s=rho)L(E,s)`,
write the net residue polynomial as

```text
P_alpha(u)
  = e^(alpha u) sum_(ell=0)^(D_alpha) A_(alpha,ell)^net u^ell.
```

For a legal finite-box height `T_box(u)`, let

```text
P_mult,box(u)
  = sum_(alpha: rho=1+alpha crossed multiple zero, |Im alpha|<=T_box(u))
      P_alpha(u),
```

after same-exponent netting and after removing residues already declared
kernel-killed.

Profile theorem target:

```text
c_E,W(e^u) = Q_E,W(u) + P_mult,box(u) + o(u^r).
```

If a stable infinite profile is desired, add a declared convergence/tail mode:

```text
P_mult,box(u) = P_mult(u) + o(u^r)
```

pointwise, in Besicovitch/profile mode, log-Cesaro mode, or product-average
mode. Then

```text
c_E,W(e^u) = Q_E,W(u) + P_mult(u) + o(u^r)
```

in that same mode.

Central-only corollary:

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)
```

requires

```text
P_mult,box(u)=o(u^r),
```

which expands back to the Wave 4 effective-degree and aggregate condition.

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT07_MULTIPLE_ZERO_EFFECTIVE_DEGREE_2026-05-11.md`: BFMT-separated branch is simple-zero only; multiple-zero Laurent residues need `D_alpha<r` plus lower-degree aggregate control for central-only H1.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT06_H1_FINITE_BOX_ASSEMBLY_REFEREE_2026-05-11.md`: Wave 4 assembly keeps multiple-zero control as independent condition `C9`, separate from separated BFMT and bad-set budget.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md`: H1 multiple-zero/Laurent control is a positive-rank theorem package, not a promoted unconditional theorem.
- `primes-equispaced/L2_facts/farey-claim-ledger.md`: current ledger records that H1 still needs `H1-MultipleEffectiveDegree-BFMT(E,W,r)` after Wave 4, and that multiple-zero effective degrees `>=r` block positive-rank central closure unless retained, killed, or averaged.
- Supporting algebra: `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT03_H1_MULTIPLE_ZERO_LAURENT_2026-05-11.md`.

# Simplification Attempts

## 1. Simplicity

Paper-clean sufficient hypothesis:

```text
H1-OffcentralCriticalSimplicity(E):
  every crossed critical-line zero rho != 1 of L(E,s) is simple.
```

Then there are no critical-line multiple-zero Laurent polynomials to audit.
The simple-zero contribution is handled by the BFMT-separated plus bad-set
route, or by a declared fixed-weight PV substitute.

Status:

```text
sufficient but not sourced.
```

Do not call this "global simplicity" without care: if `r>1`, the central zero
at `s=1` is multiple by definition. The usable hypothesis is offcentral
simplicity. The anchors do not prove it, and BFMT deliberately works only on a
simple separated family.

## 2. Kernel Killing

Paper-clean sufficient hypothesis:

```text
H1-MultipleZeroKernelKill(E,W):
  for every crossed offcentral multiple zero rho=1+alpha,
  ord_(z=alpha) W_hat(z) >= ord_(s=rho) L(E,s).
```

Then every local multiple-zero pole of `W_hat(z)/L(E,1+z)` is cancelled and
`P_alpha(u)=0`.

Status:

```text
sufficient but much stronger than needed and not sourced for the fixed kernel.
```

The weaker generic condition

```text
ord_(z=alpha) W_hat(z) >= m-r
```

only lowers the degree below the central degree. It still leaves lower-degree
aggregate control, so it is not a clean replacement for the Wave 4 condition.
Finite diagnostic filters can kill finitely many named residues, but the
current endpoint kernel is fixed and there is no source for infinite killing
without breaking the H1/H2 kernel setup.

## 3. Retained Profile

Paper-clean theorem mode:

```text
H1-RetainedMultipleZeroProfile(E,W;T_box):
  keep P_mult,box(u) in the theorem conclusion.
```

This removes the need to prove `D_alpha<r` for retained terms. The conclusion
is not central-only:

```text
c_E,W(e^u)=Q_E,W(u)+P_mult,box(u)+o(u^r).
```

Status:

```text
valid theorem mode, not a central-only promotion.
```

If `P_mult,box(u)` has degree `r` terms, the normalized H1 object has an
oscillatory profile. If it has degree `>r` terms, those terms dominate the
central scale unless the theorem explicitly retains, subtracts, damps, or
averages them.

# Retained Profile Mode

Use this paper statement when not assuming offcentral simplicity or exact
kernel killing.

```text
Theorem: H1 finite-box with retained multiple-zero profile.

Assume the finite-box H1 contour hypotheses, central normalization, legal
heights, no-silent-right-half-residue rule, and simple-zero budget. For every
crossed offcentral multiple zero, form the exact Laurent residue polynomial
P_alpha(u) after kernel cancellation and same-exponent netting. Then

  c_E,W(e^u)=Q_E,W(u)+P_mult,box(u)+o(u^r),

where P_mult,box is the sum of all retained multiple-zero residue polynomials
crossed by the legal finite box.
```

Optional stable-profile upgrade:

```text
H1-MultipleZeroProfileConvergence(E,W;mode):
  P_mult,box(u) converges to P_mult(u) with box-tail o(u^r)
  in the declared pointwise/profile/averaged/product mode.
```

Then the theorem becomes

```text
c_E,W(e^u)=Q_E,W(u)+P_mult(u)+o(u^r)
```

in that same mode.

This theorem is cleaner than hiding the profile inside a smallness hypothesis.
It is also honest: the paper does not claim a pointwise constant or central
term when a retained profile survives at central scale.

# Minimal Hypothesis

Recommended replacement for Wave 5 forward use:

```text
H1-MultipleZeroDisposition(E,W,r):
  Every crossed offcentral multiple-zero residue is either

  (A) absent by H1-OffcentralCriticalSimplicity(E);
  (B) killed by H1-MultipleZeroKernelKill(E,W);
  (C) retained in H1-RetainedMultipleZeroProfile(E,W;T_box);
  (D) unretained and central-negligible:
      D_alpha < r for every retained critical-line exponent alpha, and
      sum_(ell=0)^(r-1) u^ell
        sum_(Re alpha=0, alpha!=0, mult)
          A_(alpha,ell)^net e^(alpha u)
      = o(u^r).
```

Mode `(D)` is exactly the Wave 4 central-only condition, minus the misleading
`BFMT` suffix. It is minimal in the following sense:

```text
central-only H1 needs P_mult,box(u)=o(u^r);
the effective-degree/aggregate condition is the residue-level expansion of
that requirement after kernel zeros, internal cancellation, and same-frequency
netting.
```

Simplicity and full kernel killing are clean sufficient shortcuts. Retained
profile is a clean replacement only when the theorem conclusion is allowed to
retain the profile.

# Dependency Impact

- Agent08 should not inherit the name `H1-MultipleEffectiveDegree-BFMT`.
  Replace it by `H1-MultipleZeroDisposition(E,W,r)`.
- The separated BFMT branch and `EC-BFMT-BadSetBudget(E,c)` remain unchanged:
  they only supply the simple-zero budget.
- A central-only H1 theorem still needs mode `(D)` unless mode `(A)` or `(B)`
  is explicitly assumed.
- A profile H1 theorem can use mode `(C)` and drop the degree-`<r` demand, but
  downstream H1/H2 composition must retain the same profile or prove an
  averaged/product-profile theorem.
- No source anchor proves offcentral simplicity or fixed-kernel infinite
  killing. They are optional stronger hypotheses, not consequences of Wave 4.
