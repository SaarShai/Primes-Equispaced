---
title: "Agent 07 multiple-zero effective degree against BFMT-separated branch"
date: 2026-05-11
type: theorem-reduction
tier: working
status: CONDITIONAL_THEOREM
confidence: 0.90
tags: [breakthrough-wave-4, h1, bfmt, multiple-zeros, laurent-control, effective-degree]
---

# Verdict

The new BFMT-separated branch does not control actual multiple zeros. It only
controls simple zeros in the separated family, and the remaining simple-zero
complement is delegated to `EC-BFMT-BadSetBudget(E,c)`.

Thus the multiple-zero question survives unchanged as a Laurent/effective-degree
condition inside the finite-box H1 Perron theorem. The exact degree condition is:

```text
D_alpha < r
```

for every retained critical-line multiple-zero exponent `alpha != 0`, after
kernel zeros, internal Laurent/kernel cancellation, and exact same-exponent
netting. For rank one this is

```text
D_alpha <= 0.
```

This is paper-ready as a conditional section, not as an unconditional theorem.
The minimal added hypothesis is the named multiple-zero effective-degree and
aggregate-control hypothesis below. Global simplicity is sufficient but not
minimal.

# Theorem Target

Let

```text
r = ord_(s=1) L(E,s) >= 1,
u = log K,
c_E,W(e^u) = (1/(2 pi i)) int e^(u z) W_hat(z)/L(E,1+z) dz.
```

Assume the finite-box H1 contour theorem in the same pointwise mode, central
normalization

```text
Q_E,W(u) = (w_-1/L^(r)(E,1)) u^r + O(u^(r-1)),
```

the BFMT-separated simple-zero branch plus bad-set budget sufficient to give
the simple-zero H1 budget, and the multiple-zero hypothesis stated in the
Condition section. Then

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r).
```

For rank one, the BFMT side supplies only the simple-zero input

```text
R_E,1(T) = sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-1) = o(T^2)
```

after both the separated BFMT theorem and `EC-BFMT-BadSetBudget(E,c)`.
Multiple zeros are not included in this sum.

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: BFMT transcription is separated simple-zero only; explicit no-promotion boundary says multiple zeros are not controlled by that packet.
- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`: rank-one H1 simple-zero target is exactly `R_E,1(T)=o(T^2)`.
- `primes-equispaced/L2_facts/farey-current-state.md`: arithmetic normalization uses EC zeros as `rho=1+i gamma`.
- `primes-equispaced/L2_facts/farey-claim-ledger.md`: current ledger records that BFMT progress does not remove the load-bearing multiple-zero effective-degree hypothesis.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT03_H1_MULTIPLE_ZERO_LAURENT_2026-05-11.md`: local Laurent algebra and effective-degree definition.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT07_H1_FINITE_BOX_THEOREM_SECTION_2026-05-11.md`: finite-box theorem statement names `H1-MultipleEffectiveDegree(E,W,r)`.
- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT07_H1_FINITE_BOX_DPMV_INTEGRATION_2026-05-11.md`: DPMV/BFMT integration states that multiple-zero Laurent control is independent of the separated/bad-set split.

# Laurent/Eff-Degree Analysis

Let `rho != 1` be a crossed zero of `L(E,s)`, with

```text
alpha = rho - 1,
m = ord_(s=rho) L(E,s).
```

Near `z=alpha`,

```text
1/L(E,1+z)
 = sum_(j=1)^m b_(rho,-j)(z-alpha)^(-j) + holomorphic.
```

The finite-box H1 residue is

```text
R_rho(u)
 = e^(alpha u) sum_(ell=0)^(m-1) A_(rho,ell) u^ell,

A_(rho,ell)
 = (1/ell!) sum_(j=ell+1)^m
     b_(rho,-j) W_hat^(j-1-ell)(alpha)/(j-1-ell)!.
```

If

```text
nu_rho = ord_(z=alpha) W_hat(z),
```

then the generic local top degree is

```text
d_gen(rho) = m - 1 - nu_rho.
```

This generic degree is not the theorem condition. The theorem condition must
use the effective degree after all legal cancellations.

Group all residues with the same exponent `alpha` and define

```text
A_(alpha,ell)^net
 = sum_(rho: rho-1=alpha) A_(rho,ell)
```

plus any same-exponent contour terms declared in the same finite-box theorem.
Then

```text
D_alpha = max { ell : A_(alpha,ell)^net != 0 },
```

with `D_alpha=-infinity` if all net coefficients vanish.

Distinct nonzero critical-line frequencies do not lower each other's pointwise
degree. Conjugate pairing only rewrites the term as a real oscillation. A
degree-`d` same-frequency obstruction disappears pointwise only when its net
degree-`d` coefficient is zero, or when a separately proved PV/averaged theorem
is the declared mode.

# Condition

Paper-ready hypothesis:

```text
H1-MultipleEffectiveDegree-BFMT(E,W,r):

For every crossed multiple zero rho=1+alpha with Re alpha=0 and alpha != 0,
form the net coefficients A_(alpha,ell)^net as above.

1. Degree exclusion:
   D_alpha < r
   for every retained critical-line multiple-zero exponent alpha.

2. Lower-degree aggregate control:
   for 0 <= ell < r,
   Z_ell^mult(u)
     = sum_(Re alpha=0, alpha!=0, mult) A_(alpha,ell)^net e^(alpha u)
   satisfies
   sum_(ell=0)^(r-1) u^ell Z_ell^mult(u) = o(u^r).

3. Right-half residues:
   every Re alpha > 0 multiple-zero residue is absent, kernel-killed,
   explicitly retained outside the central-only claim, or controlled by the
   same no-silent-right-half-residue hypothesis as the finite-box theorem.
```

A clean sufficient version of item 2 is

```text
Z_ell^mult(u)=O(1)       for every 0 <= ell < r.
```

An even more checkable sufficient version is absolute convergence:

```text
sum_(Re alpha=0, alpha!=0, mult) |A_(alpha,ell)^net| < infinity,
0 <= ell < r.
```

Generic individual-zero screen:

```text
m - 1 - nu_rho < r,
equivalently m <= r + nu_rho.
```

Rank-one specialization:

```text
D_alpha <= 0.
```

Generically this says

```text
m <= 1 + nu_rho.
```

So an uncancelled double zero with no kernel zero has generic degree `1`, equal
to the central rank-one term, and blocks the pointwise central-only statement.
A double zero with a simple kernel zero has degree at most `0`; it is lower
degree, but its degree-zero aggregate still needs item 2.

# Minimal Added Hypothesis

The separated BFMT branch plus bad-set budget should be integrated with the
following additional hypothesis, and no stronger assumption is needed for this
part:

```text
H1-MultipleEffectiveDegree-BFMT(E,W,r)
```

For the rank-one BFMT application this becomes:

```text
H1-MultipleEffectiveDegree-BFMT(E,W,1):
  every retained critical-line multiple-zero exponent has D_alpha <= 0,
  and
  Z_0^mult(u)
    = sum_(Re alpha=0, alpha!=0, mult) A_(alpha,0)^net e^(alpha u)
  is o(u).
```

Boundedness or absolute convergence of `Z_0^mult` is a convenient sufficient
form. It is not supplied by BFMT, by zero counting, or by the simple-zero
reciprocal derivative budget.

Stronger but nonminimal alternatives:

```text
all offcentral critical zeros are simple;
W_hat has zero order >= m at every offcentral multiple zero;
all multiple-zero residues are explicitly retained in an oscillatory/profile theorem;
a proved PV/averaged theorem replaces pointwise central-only closure.
```

# Dependency Impact

- The BFMT-separated theorem, if completed, reduces only the simple separated
  zero contribution.
- `EC-BFMT-BadSetBudget(E,c)` is still required to upgrade the simple-zero
  branch to `R_E,1(T)=o(T^2)` in rank one.
- Multiple zeros remain outside both simple-zero packets. They must be handled
  by `H1-MultipleEffectiveDegree-BFMT(E,W,r)`.
- For rank one, the exact central-only stack is:

```text
BFMT-separated simple-zero bound
+ EC-BFMT-BadSetBudget(E,c)
+ finite-box boundary/no-right-residue hypotheses
+ H1-MultipleEffectiveDegree-BFMT(E,W,1)
=> c_E,W(e^u) = (w_-1/L'(E,1)) u + o(u).
```

- Do not cite the BFMT-separated branch as proving global simplicity, bounded
  multiplicity, Laurent coefficient bounds, or multiple-zero disappearance.
