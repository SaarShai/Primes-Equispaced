---
title: "AGENT09 H2 Pointwise Finite-Part Closure"
date: 2026-05-11
type: theorem-closure
tier: working
status: CONDITIONAL_THEOREM
confidence: 0.78
tags: [breakthrough-wave-5, h2, pointwise, finite-part, s1, sym2, right-lip]
---

# Verdict

Status: `CONDITIONAL_THEOREM`.

`H2-PointwiseFinitePartClosure(E,W,eta;c)` closes as an exact conditional H2
theorem in the Agent 3 local convention once all retained H2 profile terms are
declared.  The non-profile pointwise theorem needs:

```text
R_S1^+(K;E,W,eta,c) = o(1)
```

or no S1 right branch, and `Z_sym,E,W(K)=o(1)` for the exact good-prime Sym2
ledger.  If an S1 right branch remains, the correct theorem is the
right-lip-renormalized one with the full `R_S1^+` subtracted.  First-Watson
right-branch subtraction is not enough.

No H1 conclusion is used or implied.  H2 branch damping does not transfer to
H1 reciprocal-pole residues.

# Theorem Target

Fix an elliptic curve `E/Q`, endpoint admissible `W`, and

```text
u = log K,
r = ord_(s=1) L(E,s).
```

Use the exact Agent 3 local factors:

```text
A_p(1) = 1 - a_p/p + 1/p    for good p,
A_p(1) = 1 - a_p/p          for bad p,
P_E,W(K) = product_p A_p(1)^(-W(p/K)).
```

Assume the exact H2 decomposition:

```text
log P_E,W(K)
 = S1_W(K)
   + (1/2) Ssym_W(K)
   - (1/2) Mgood_W(K)
   + Rge3_W(K)
   + Bbad_W(K).
```

Assume the Wave 4 S1 right-lip theorem in the same good-prime convention:

```text
S1_W(K)
 = (1/2 + kappa_sym/2 - r) log u
   + C1_E,W
   + R_S1^+(K;E,W,eta,c)
   + e1(K),
e1(K) = o(1),
```

where `e1=o(1)` includes the left/nonpositive branch Watson sum and the
regularized left-edge error.  For the unprofiled theorem additionally assume
`R_S1^+=o(1)`; otherwise subtract the full `R_S1^+`.

Assume the exact good-prime Sym2 finite-part ledger:

```text
Ssym_W(K)
 = -kappa_sym log u
   + Csym_E,W
   + Z_sym,E,W(K)
   + esym(K),
esym(K) = o(1),
```

with the pointwise hypothesis

```text
Z_sym,E,W(K) = o(1).
```

A sufficient Sym2 hypothesis from the ledger is: all offcentral Sym2
singularities in the shifted strip have `Re(rho)<=1`, and the weighted
zero/pole sum is finite.  A Sym2 singularity with `Re(rho)>1` is not allowed
in the unprofiled theorem unless an exact cancellation/profile lemma is added.

Assume the remaining local terms have finite parts:

```text
Mgood_W(K) = log u + CM_E,W + eM(K),      eM(K) = o(1),
Rge3_W(K)  = Cge3_E + ege3(K),            ege3(K) = o(1),
Bbad_W(K)  = Bbad_E + ebad(K),            ebad(K) = o(1).
```

Then the right-lip-renormalized theorem is

```text
log P_E,W(K)
 + r log u
 - R_S1^+(K;E,W,eta,c)
 = B_H2(E,W) + o(1),
```

where

```text
B_H2(E,W)
 = C1_E,W
   + (1/2) Csym_E,W
   - (1/2) CM_E,W
   + Cge3_E
   + Bbad_E.
```

If `R_S1^+=o(1)` or there is no S1 right branch, this gives the unprofiled
pointwise finite-part theorem:

```text
log P_E,W(K) + r log log K -> B_H2(E,W),
P_E,W(K) = exp(B_H2(E,W)) (log K)^(-r) (1+o(1)).
```

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT08_H2_S1_RENORMALIZED_RIGHT_BRANCH_2026-05-11.md`,
  lines 13-18: S1/H2 is conditional; first-Watson subtraction is invalid for a
  live right branch.
- Same file, lines 80-113: S1 hypotheses, central coefficient, and exact
  retained `R_S1^+`.
- Same file, lines 228-276: S1 closure mechanism and right-branch obstruction.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT09_H2_SYM2_COMPOSITION_FINAL_2026-05-11.md`,
  lines 90-145: exact H2 decomposition, finite parts, coefficient
  cancellation, and retained-profile warning.
- Same file, lines 246-265: named missing closure
  `H2-PointwiseFinitePartClosure(E,W,eta;c)`, right-branch, and Sym2 regular
  ledger dependencies.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md`,
  lines 113-140: Sym2 central finite part and `-kappa_sym log log K`.
- Same file, lines 149-193: Sym2 offcentral ledger; `Re(rho)>1` blocks a
  pointwise finite part unless explicitly canceled/retained.
- Same file, lines 198-249: H2 compatibility and the requirement
  `Z1=o(1)`, `Zsym=o(1)`.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md`,
  lines 48-153: exact decomposition and named dependencies.
- Same file, lines 153-204: conditional pointwise H2 candidate and constant.

# Pointwise Closure Attempt

Insert the three finite parts into the exact decomposition:

```text
log P_E,W(K)
 = [(1/2 + kappa_sym/2 - r)
    + (1/2)(-kappa_sym)
    - 1/2] log u
   + C1_E,W
   + (1/2) Csym_E,W
   - (1/2) CM_E,W
   + Cge3_E
   + Bbad_E
   + R_S1^+(K;E,W,eta,c)
   + Z_sym,E,W(K)/2
   + o(1).
```

The log coefficient is exact:

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

Thus

```text
log P_E,W(K)
 = -r log u
   + B_H2(E,W)
   + R_S1^+(K;E,W,eta,c)
   + Z_sym,E,W(K)/2
   + o(1).
```

Under the Sym2 pointwise hypothesis `Z_sym=o(1)`, subtracting the full S1
right lip gives:

```text
log P_E,W(K)
 + r log u
 - R_S1^+(K;E,W,eta,c)
 = B_H2(E,W) + o(1).
```

Under the stronger no-right/no-profile assumptions

```text
R_S1^+(K;E,W,eta,c) = o(1),
Z_sym,E,W(K) = o(1),
```

this is exactly `H2-PointwiseFinitePartClosure(E,W,eta;c)`.

This closure uses the S1 full-lip object only at H2 level.  It does not create
an H1 reciprocal-residue estimate.

# Missing Lemma or Closure

For unconditional, unprofiled H2, the exact missing package is:

```text
H2RightProfileVanishOrCancel(E,W,eta;c):
  R_S1^+(K;E,W,eta,c) + Z_sym,E,W(K)/2 = o(1).
```

A sufficient split form is:

```text
S1RightBranchAbsentOrSmall(E,W,eta;c):
  B_S1^+ = empty
  or R_S1^+(K;E,W,eta,c)=o(1),

Sym2ZeroLedgerPointwiseSmall(E,W,eta;c):
  Z_sym,E,W(K)=o(1)
  for the exact L_sym,E^good object.
```

To source-close those split hypotheses, the remaining analytic lemmas are:

```text
RegularLogLeftEdge(E,W,eta;c)
```

for the S1 finite-cut contour, and

```text
Sym2-ZeroLedger-RegularLog(E,W,eta;c)
```

for the exact good-prime Sym2 continuation, central order `kappa_sym`, and
weighted offcentral branch summability.

If Sym2 has a right singularity `rho` with `Re(rho)>1`, the current Sym2 ledger
does not provide a full right-lip theorem analogous to Wave 4 S1.  Its leading
term has size

```text
K^(Re rho - 1) / log K,
```

so pointwise finite-part closure is false unless an exact Sym2 right-profile
cancellation/retention lemma is supplied.

# Dependency Impact

- H2 pointwise finite part is available as a conditional theorem in the exact
  Agent 3 product convention.
- Final synthesis may cite the unprofiled theorem only when both
  `R_S1^+=o(1)` and `Z_sym=o(1)` are present.
- With a live S1 right branch, the valid output is the renormalized/profile
  theorem subtracting full `R_S1^+`.
- With a live Sym2 right singularity, this packet is only a rigorous reduction
  to a missing Sym2 right-profile cancellation/retention lemma.
- No H2 branch damping, right-lip estimate, or Sym2 `1/log K` factor is
  imported into H1.
