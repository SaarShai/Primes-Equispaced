---
schema_version: 1
title: "Agent 05 H2 S1 branch-contour legality"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 05 -- H2 S1 Branch-Contour Legality"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.80
tags: [ec-ndc, h2, s1, branch-contour, explicit-formula]
---

# Agent 05 H2 S1 Branch-Contour Legality

## Status Enum

- `CLOSED`: proved here or imported as already source-checked.
- `CONDITIONAL`: theorem-level implication proved from stated hypotheses.
- `PROOF_CANDIDATE`: coherent proof skeleton, not source-closed.
- `BLOCKED`: exact theorem input still missing.
- `NOT_PROMOTED`: do not cite as an unconditional EC theorem.

Overall status: `RIGOROUS_REDUCTION`, `NOT_PROMOTED`.

## Verdict

The branch-only continuation of

```text
A_E(z)=sum_(p good) a_p p^(-1-z)
```

is reduced to a clean logarithm identity in the strip `Re z > -1/4`. In that
identity, offcentral singularities are logarithmic branch points, not poles.
Thus the local S1 zero term has the expected scale

```text
c_a K^a W_hat(a)/log K.
```

This closes the algebraic branch mechanism conditionally on exact analytic
inputs for the good-prime symmetric-square object.

The legal infinite cut contour shift is still `PROOF_CANDIDATE`, not
source-closed. The precise missing theorem is a cut-plane logarithmic-growth
and truncation lemma for the relevant logarithms, strong enough to pass to
infinitely many left-going cuts with the endpoint Mellin kernel.

Pointwise `C+o(1)` for `S_1,W` also needs a no-right-branch input. If
`L(E,s)` has a zero with `Re s > 1`, the formula gets a retained term

```text
K^(rho-1) W_hat(rho-1)/log K,
```

which grows. That is not a contour-legality problem; it is a theorem-mode
blocker.

## Context Used

- `start.md`
- `token-economy.yaml`, `L0_rules.md`, root `L1_index.md`
- `primes-equispaced/L1_index.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT04_H2_SYM2_ENDPOINT_CLOSURE_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md`
- `primes-equispaced/handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md`
- targeted supporting reads: `S1A_EXPLICIT_FORMULA_DERIVATION.md`,
  `S1B_SOURCE_AUDIT.md`, `S1_ZERO_SUMMABILITY.md`,
  `THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md`

## Source Protocol Status

No new external theorem is promoted here.

Imported from `SOURCE_PACKET.md`:

- Sheth, arXiv:2312.05236v4: source-supported EC zero counting
  `N_E(T)=O_E(T log T)` and reciprocal-square zero convergence. Used only as
  already-closed pure S1 zero-summability input.
- Friedlander-Iwaniec chapter: source-supported ordinary prime Mertens. Not
  used to close branch-contour legality.
- Iwaniec-Luo-Sarnak and Hoffstein-Lockhart: adjacent symmetric-square/GL(3)
  support only. Not used to assert the exact good-prime Sym2 finite-part or
  cut-contour theorem.

`SOURCE_PACKET.md` remains decisive: no audited source proves the exact
fixed-curve endpoint-smoothed formula for `S_1,W(K)`.

## Branch-Only Continuation Attempt

Fix `0 < eta < 1/4`, `c > 1/2`, and an admissible endpoint kernel `W` with

```text
W_hat(z)=1/z+O(1) at z=0,
W_hat(sigma+it), W_hat'(sigma+it) << (1+|t|)^(-2)
```

on `-eta <= sigma <= c`, away from kernel poles.

For good primes write

```text
alpha_p+beta_p=a_p,   alpha_p beta_p=p,
lambda_p=a_p/sqrt(p),
chi_sym2(p)=lambda_p^2-1=a_p^2/p-1.
```

In the initial convergence half-plane,

```text
log L_good(E,1+z)
 = A_E(z)
   + (1/2)D_sym(1+2z)
   - (1/2)M_good(1+2z)
   + H_E(z),
```

where

```text
D_sym(s)=sum_(p good) chi_sym2(p)p^(-s),
M_good(s)=sum_(p good) p^(-s),
```

and `H_E(z)` is the `m>=3` good-prime correction. By Hasse bounds,
`H_E(z)` is holomorphic for `Re z > -1/6`; the Sym2 and zeta higher-power
corrections below are holomorphic for `Re z > -1/4`.

Assuming the exact good-prime Sym2 object

```text
L_sym,E^good(s)
 = product_(p good)
   (1-u_p^2 p^(-s))^(-1)
   (1-p^(-s))^(-1)
   (1-v_p^2 p^(-s))^(-1)
```

has meromorphic continuation in the needed region, the first-prime series has
the multivalued continuation

```text
A_E(z)
 = log L_good(E,1+z)
   - (1/2)log L_sym,E^good(1+2z)
   + (1/2)log zeta_good(1+2z)
   + Phi_E(z),
```

with `Phi_E` holomorphic for `Re z > -1/4`.

Conclusion: in this representation `A_E` has only logarithmic branch
singularities in the strip. No offcentral pole can appear unless one of the
input objects is not represented by logarithms or the holomorphic correction
claim fails.

Status: `CONDITIONAL`.

## Branch Coefficients

Use the convention

```text
A_E(z)=c_a log(1/(z-a)) + holomorphic
```

near a branch point `a`.

For a noncolliding singularity,

```text
c_a =
  - ord_(s=1+a) L_good(E,s)
  + (1/2) ord_(s=1+2a) L_sym,E^good(s)
  - (1/2) ord_(s=1+2a) zeta_good(s).
```

Positive order means zero; negative order means pole.

At `a=0`,

```text
r = ord_(s=1) L(E,s),
kappa_sym = ord_(s=1) L_sym,E^good(s),
ord_(s=1) zeta_good(s) = -1,
```

so

```text
c_0 = 1/2 + kappa_sym/2 - r.
```

For a noncolliding zero `rho=1+i gamma` of `L(E,s)`, multiplicity `m_rho`,

```text
c_(i gamma) = -m_rho.
```

This matches the previous S1 branch theorem candidate and keeps analytic rank
only.

Status: `CLOSED` as algebra from the logarithm identity; `BLOCKED` only where
the exact Sym2 object itself is not source-closed.

## Finite Cut Contour Formula

For finite height `T`, remove small disks around the finitely many branch
points in

```text
-eta <= Re z <= c,   |Im z| <= T,
```

and take left-going cuts from each branch point. Cauchy's theorem gives the
finite-cut identity

```text
S_1,W^good(K)
 = c_0 log log K
   + C_T(E,W)
   + sum_(a != 0, |Im a| <= T) c_a K^a W_hat(a)/log K
   + R_T(K),
```

where the displayed branch term is the first Watson term from the cut integral.
The next local term is

```text
O_a,W(K^(Re a)/(log K)^2)
```

with derivative control of `W_hat` on the cut segment. Branch collisions only
add their logarithmic coefficients; they do not change the `1/log K` scale.

Status: `PROOF_CANDIDATE`.

## Infinite Cut Shift: Missing Theorem

To pass `T -> infinity`, the exact missing theorem is:

```text
S1-CutPlane-LogGrowth(E,W,eta).
```

Required statement:

For the three logarithmic factors

```text
L_good(E,1+z),
L_sym,E^good(1+2z),
zeta_good(1+2z),
```

on the cut strip `-eta <= Re z <= c`, there exists a truncation sequence
`T_n -> infinity`, avoiding branch ordinates, such that:

1. On horizontal edges `Im z = +/-T_n`, away from cut neighborhoods,

   ```text
   |log F(linear z)| << (log T_n)^B
   ```

   for a fixed `B`.

2. On the left edge and cut lips, the regular part times `W_hat(z)` is
   absolutely integrable.

3. The sum of local cut remainders satisfies

   ```text
   sum_a |c_a| sup_(0<=v<=eta)
     (|W_hat(a-v)| + |W_hat'(a-v)|) < infinity
   ```

   after excluding or explicitly retaining right-half-plane branches.

4. The left-edge integral is

   ```text
   O(K^(-eta))
   ```

   uniformly in the final asymptotic passage.

Pure `L(E,s)` zero-summability on `Re rho=1` is already closed as input. The
missing part is the cut-plane growth/truncation theorem and the corresponding
Sym2/zeta companion control in the exact normalization.

Status: `BLOCKED`.

## Pointwise Consequences By Branch Location

For a branch point `a=beta+i gamma`,

```text
branch contribution = c_a K^beta exp(i gamma log K) W_hat(a)/log K.
```

Therefore:

- `beta < 0`: power-decaying; harmless for finite part.
- `beta = 0`: lower order `O(1/log K)` under the already-closed S1
  weighted zero-summability input.
- `beta > 0`: grows like `K^beta/log K`; pointwise `C+o(1)` fails unless
  this branch is absent, canceled, or explicitly retained in another theorem
  mode.

Thus the pointwise S1 theorem needs:

```text
NoRightBranch_S1(E,eta):
  every offcentral branch of A_E in Re z >= 0 has Re z = 0,
  and the Re z = 0 weighted branch sum is summable.
```

For the `L(E,s)` part, this is a no-zero-to-the-right-of-the-central-line
input in the shifted strip. It is not source-closed here.

Status: `BLOCKED` for unconditional pointwise `C+o(1)`.

## Claim-Safe Theorem

Under:

1. exact Agent 3 good/bad local normalization;
2. analytic rank `r=ord_(s=1)L(E,s)`;
3. exact good-prime Sym2 continuation in the displayed normalization;
4. `S1-CutPlane-LogGrowth(E,W,eta)`;
5. no unretained right-half-plane branches;
6. weighted branch summability on `Re a=0`;

one obtains

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + (1/log K) sum_(a != 0, Re a = 0)
       c_a K^a W_hat(a)
   + o(1/log K)
   + O(K^(-eta)).
```

In particular,

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + o(1).
```

This theorem is conditional, not promoted.

## Exact Blockers

1. `S1-CutPlane-LogGrowth(E,W,eta)` is not source-verified and not fully
   proved in-repo.
2. Exact good-prime Sym2 analytic continuation/finite-part/zero-summability
   remains a separate H2 blocker; do not set `kappa_sym=0` from adjacent
   sources.
3. `NoRightBranch_S1(E,eta)` is needed for pointwise finite part. Without it,
   retain the `K^a/log K` terms.
4. No audited source proves the exact fixed-curve endpoint-smoothed S1 theorem.
5. This H2 branch damping does not transfer to H1 reciprocal-pole residues.

## Do Not Promote Unless

- `S1-CutPlane-LogGrowth(E,W,eta)` is proved or source-verified.
- The exact good-prime Sym2 object is reconciled with a source-verified global
  adjoint/Sym2 object.
- Right-half-plane branches are excluded or retained explicitly.
- The theorem mode is declared once: pointwise, oscillatory, or averaged.
- Analytic rank is used; no algebraic-rank substitution appears without a
  separate assumption.
- H1 is not claimed from H2 branch damping.

## Verification Notes

- Ran `./te doctor`: ok.
- Confirmed Wave 1 synthesis and Agent 04 identify S1 branch-contour legality
  as an H2 blocker while pure S1 zero-summability is closed.
- Checked `S1_BRANCH_THEOREM_CANDIDATE.md`, `S1A`, `S1B`,
  `S1_ZERO_SUMMABILITY.md`, and `SOURCE_PACKET.md`.
- No new `curl`/`pdftotext` packet was created; no new external theorem is
  cited as closing the gap.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT05_H2_S1_BRANCH_CONTOUR_2026-05-11.md
```
