---
schema_version: 1
title: "Agent 09 S1 right-branch classification"
date: 2026-05-11
agent: "Breakthrough Wave 3 Agent 09 - S1 Right-Branch Classification"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
tags: [ec-ndc, h2, s1, right-branch, retained-terms]
---

# Agent 09 S1 Right-Branch Classification

Status: `RIGOROUS_REDUCTION`.

## Verdict

`NoRightBranch_S1(E,eta)` is not proved unconditionally.

For the exact S1 good-prime object

```text
A_E(z) = sum_{p good} a_p p^(-1-z),
```

the only right-branch source in the Wave 2 logarithm identity is the shifted
nonzero-order ledger of the good-prime elliptic-curve factor `L_good(E,s)`.

In the standard EC local normalization, this means:

```text
right S1 branches a with Re a > 0
  = shifted right-of-central zeros a = rho - 1 of L(E,s),
    up to finite bad-local bookkeeping.
```

The Sym2 and zeta good-prime factors do not create right branches in the
S1 right half-plane because their arguments have real part `>1` there, where
their exact Euler products are absolutely convergent and locally nonvanishing.

Thus the classification is:

```text
Absent: only under a no-right-zero input for L(E,s).
Finite retainable: not established by current sources.
Unavoidable obstruction: yes, for any H2 theorem that drops right branches.
Legal theorem mode: retain the right-branch sum explicitly.
```

## Source Protocol

No new external theorem is imported in this packet.

Inputs used:

- Wave 2 Agent 05: S1 logarithm identity and the missing
  `S1-CutPlane-LogGrowth(E,W,eta)` theorem.
- Wave 2 Agent 06: exact good-prime Sym2 normalization and `kappa_sym=0`
  under its cited source protocol.

All new claims below are conditional algebra from those packets and elementary
Euler-product bookkeeping in the half-plane of absolute convergence. No
theorem is promoted here.

## Definitions

Fix `0 < eta < 1/4`, a right edge `c > 1/2`, and the endpoint kernel `W`.
The prompt shorthand `NoRightBranch_S1(E,eta)` is used below in the finite
contour form `NoRightBranch_S1(E,eta;c)`, since the crossed right branches are
controlled by the right edge `c`. Use analytic rank only:

```text
r = ord_{s=1} L(E,s).
```

Wave 2 Agent 05 gives the branch identity, in the cut strip, in the form

```text
A_E(z)
 = log L_good(E,1+z)
   - (1/2) log L_sym,E^good(1+2z)
   + (1/2) log zeta_good(1+2z)
   + Phi_E(z),
```

where `Phi_E` is holomorphic in the required strip.

For a branch point `a`, write

```text
A_E(z) = c_a log(1/(z-a)) + holomorphic.
```

Then

```text
c_a =
  - ord_{s=1+a} L_good(E,s)
  + (1/2) ord_{s=1+2a} L_sym,E^good(s)
  - (1/2) ord_{s=1+2a} zeta_good(s).
```

Define the right-branch ledger crossed by the S1 contour:

```text
Z_S1^+(E;c)
 = { rho : 1 < Re rho <= 1+c,
           ord_{s=rho} L_good(E,s) != 0 }.
```

For `rho in Z_S1^+(E;c)`, put `a=rho-1` and
`m_rho=ord_{s=rho} L_good(E,s)`.

## Classification Theorem

Theorem `S1_RightBranch_Ledger(E,W,eta,c)`.

Assume the Wave 2 S1 logarithm identity above and the exact good-prime Sym2
normalization. Then every right branch of `A_E(z)` in

```text
0 < Re z <= c
```

is exactly one of the shifted points

```text
a = rho - 1,  rho in Z_S1^+(E;c),
```

and its coefficient is

```text
c_{rho-1} = -m_rho.
```

Equivalently,

```text
NoRightBranch_S1(E,eta;c)
  <=>  Z_S1^+(E;c) is empty.
```

In the standard EC bad-prime convention, the finite bad-local factors introduce
no right-half-plane branches in this S1 strip; they are left-side bookkeeping.
Therefore `NoRightBranch_S1` is exactly a no-right-of-central-zero condition
for the elliptic-curve L-function in the contour range. This is RH/GRH-type
input and is not proved here.

Proof.

Let `a` satisfy `Re a > 0`. Then `Re(1+2a) > 1`.

For `zeta_good(1+2a)`, the good-prime Euler product is absolutely convergent
and has no local vanishing factor in `Re(1+2a)>1`. It contributes no branch.

For `L_sym,E^good(1+2a)`, the exact good-prime local factors are

```text
(1-u_p^2 p^(-s))^(-1)
(1-p^(-s))^(-1)
(1-v_p^2 p^(-s))^(-1),
```

with `s=1+2a`. Since `Re s > 1`, each logarithm is absolutely summable over
good primes and no local factor vanishes. It contributes no branch.

`Phi_E` is holomorphic in the strip. Hence the only possible branch term for
`Re a>0` comes from `log L_good(E,1+a)`, with coefficient
`-ord_{s=1+a} L_good(E,s)`. This proves the ledger and coefficient formula.

If `L_good` is rewritten as the global EC factor with the finitely many bad
local factors removed, the standard bad local factors are either trivial or
of the form `(1 +/- p^(-s))^(-1)`. Removing such a factor only introduces
finite factors `1 +/- p^(-s)`, whose zeros have `Re s=0`, hence shifted
location `Re z=-1`. They are outside the S1 strip `Re z > -1/4`.

## Retained-Term H2 Theorem

Define the retained right-branch term

```text
B_S1^+(K;E,W,c)
 = -(1/log K) sum_{rho in Z_S1^+(E;c)}
      m_rho K^(rho-1) W_hat(rho-1).
```

If the right ledger is infinite, this expression is part of the theorem data:
it is legal only under the same weighted branch summability required by
`S1-CutPlane-LogGrowth(E,W,eta)`. Current sources do not prove that the ledger
is finite.

Conditional theorem `H2_WithRetainedRightBranches(E,W,eta,c)`.

Assume:

1. the exact S1 logarithm identity;
2. `S1-CutPlane-LogGrowth(E,W,eta)`;
3. the exact good-prime Sym2 closure of Wave 2 Agent 06, so `kappa_sym=0`;
4. weighted summability of all retained branch lips in the S1 cut shift;
5. no silent deletion of branches with `Re a > 0`.

Then the S1 term has the form

```text
S_1,W^good(K)
 = (1/2 - r) log log K
   + C_1,E,W
   + B_S1^+(K;E,W,c)
   + (1/log K) sum_{a != 0, Re a = 0}
       c_a K^a W_hat(a)
   + o(1).
```

The `Re a = 0` branch sum is `O_E,W(1/log K)` under the same weighted
summability input, hence it is `o(1)` for the finite part.

Consequently the H2 good-prime product theorem must be stated as

```text
log P_E,W^good(K)
 = -r log log K
   + C_H2,E,W
   + B_S1^+(K;E,W,c)
   + o(1),
```

or, equivalently,

```text
log P_E,W^good(K)
 + r log log K
 - B_S1^+(K;E,W,c)
 = C_H2,E,W + o(1).
```

The unretained pointwise H2 finite-part theorem

```text
log P_E,W^good(K) + r log log K = C_H2,E,W + o(1)
```

is valid only after adding `NoRightBranch_S1(E,eta;c)` or an equivalent
cancellation statement strong enough to remove `B_S1^+`.

## Obstruction Boundary

A right branch `a=beta+i gamma`, `beta>0`, contributes

```text
c_a K^beta exp(i gamma log K) W_hat(a) / log K.
```

This is not an endpoint-contour error and not H2 damping. It is a crossed
branch contribution of the exact S1 object. If it is not absent, it must be
retained. Dropping it is a theorem error.

Therefore:

- `NoRightBranch_S1(E,eta;c)` is not promoted.
- H2 can proceed only in retained-term mode unless a no-right-zero theorem is
  assumed.
- This packet gives no H1 reciprocal-pole damping and no H1 derivative moment
  estimate.
- Analytic rank only: `r=ord_{s=1} L(E,s)`.
- No Koyama correspondence or email-draft material is involved.

## Output For Coordinator

Use this replacement in any H2 statement that does not assume
`NoRightBranch_S1`:

```text
RightBranchRetained_S1(E,W,eta,c):
  B_S1^+(K;E,W,c)
  = -(1/log K) sum_{rho in Z_S1^+(E;c)}
       m_rho K^(rho-1) W_hat(rho-1)
  is retained explicitly.
```

Then state H2 as

```text
log P_E,W^good(K)
 + r log log K
 - B_S1^+(K;E,W,c)
 = C_H2,E,W + o(1).
```

Do not state pointwise `C_H2,E,W+o(1)` without either:

```text
Z_S1^+(E;c) = empty,
```

or a separately proved exact cancellation theorem for `B_S1^+`.

## Verification Notes

Commands run:

```text
./te doctor
sed -n '1,220p' start.md
sed -n '1,260p' primes-equispaced/handoff-2026-05-11-breakthrough-wave-3-plan.md
sed -n '1,260p' primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
sed -n '1,520p' primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT05_H2_S1_BRANCH_CONTOUR_2026-05-11.md
sed -n '1,340p' primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT06_H2_GOOD_PRIME_SYM2_CLOSURE_2026-05-11.md
rg right-branch/S1 references in the Wave 2 and Wave 3 handoff files
```

Changed files:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT09_S1_RIGHT_BRANCH_CLASSIFICATION_2026-05-11.md
```
