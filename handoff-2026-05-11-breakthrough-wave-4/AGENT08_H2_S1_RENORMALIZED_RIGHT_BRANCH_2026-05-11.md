---
title: "AGENT08 H2 S1 Renormalized Right Branch"
date: 2026-05-11
status: CONDITIONAL_THEOREM
tags: [breakthrough-wave-4, h2, s1, cut-plane, renormalized-log-growth, right-branch]
---

# Verdict

`S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)` is closed as a conditional
cut-plane theorem, not as an unconditional EC theorem.

The endpoint H2 statement is valid under explicit hypotheses if the right
branch ledger is either empty or retained/subtracted as the full cut-lip
object. The first Watson term alone is not an admissible subtraction when a
right branch exists.

Final status: `CONDITIONAL_THEOREM`.

# Theorem Target

Fix an elliptic curve `E/Q`, analytic rank

```text
r = ord_{s=1} L(E,s),
u = log K,
```

and an endpoint admissible kernel `W` with

```text
W_hat(z) = 1/z + O(1)              at z=0,
|W_hat^(j)(sigma+it)| << (1+|t|)^-2, j=0,1,
```

on `-eta <= sigma <= c`, away from kernel poles. For good primes define

```text
A_E(z) = sum_{p good} a_p p^(-1-z).
```

In the cut strip write every logarithmic branch point `a` as

```text
A_E(z) = c_a log(1/(z-a)) + holomorphic.
```

At the central branch,

```text
c_0 = 1/2 + kappa_sym/2 - r,
kappa_sym = ord_{s=1} L_sym,E^good(s).
```

Let

```text
B^- = {a != 0 : -eta < Re a <= 0},
B^+ = {a != 0 : 0 < Re a <= c}.
```

For `a=beta+i gamma`, define

```text
M_a = sup_{0 <= v <= beta+eta}
  ( |W_hat(a-v)| + |W_hat'(a-v)| ).
```

Assume:

1. Mellin inversion holds on `Re z=c` for `S_1,W^good(K)`.
2. The Wave 2 good-prime identity continues `A_E(z)` to the cut strip with
   only logarithmic branches and finite listed ramified corrections.
3. The weighted branch sum is finite:

   ```text
   sum_{a in B^- union B^+} |c_a| M_a < infinity.
   ```

4. `RegularLogLeftEdge(E,W,eta;c)` holds: after subtracting the central and
   finite-height local logarithmic branch terms, horizontal edges have
   polynomial-log growth and the left-edge weighted integral is bounded and
   convergent along an ordinate sequence avoiding branch ordinates.
5. Sym2 normalization and ordinary H2 bookkeeping use the same good-prime
   convention as `S1_SYM2_FINITE_PART.md` and `H2_POINTWISE_THEOREM_PACKAGE.md`.
6. Right branches are handled by exactly one of:

   ```text
   B^+ = empty,
   R_S1^+(K;E,W,eta,c) = o(1),
   or subtract/retain R_S1^+(K;E,W,eta,c).
   ```

Then

```text
S_1,W^good(K)
 = c_0 log u
   + C_1,E,W,c
   + (1/u) sum_{a in B^-} c_a K^a W_hat(a)
   + R_S1^+(K;E,W,eta,c)
   + O_E,W(u^-2)
   + O_E,W(K^-eta),
```

where the full retained right-lip term is

```text
R_S1^+(K;E,W,eta,c)
 = sum_{a in B^+} c_a K^a
     int_0^(Re a + eta) e^(-uv) W_hat(a-v) dv.
```

Under the standard `kappa_sym=0` good-prime Sym2 closure and the H2
decomposition

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E + o(1),
```

the endpoint H2 theorem is:

```text
log P_E,W(K)
 + r log log K
 - R_S1^+(K;E,W,eta,c)
 = C_H2,E,W,c + O_E,W(1/log K) + O_E,W(K^-eta),
```

with `R_S1^+=0` in the no-right-branch mode. Equivalently,

```text
P_E,W(K) exp(-R_S1^+(K;E,W,eta,c))
 = exp(C_H2,E,W,c) (log K)^(-r) (1+o(1)).
```

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT08_H2_S1_RENORMALIZED_LOG_GROWTH_2026-05-11.md`
  supplies the renormalized cut-plane theorem, the exact full right-lip
  object, and the warning that first Watson subtraction is insufficient.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md`
  supplies the conditional branch theorem, central coefficient
  `1/2 + kappa_sym/2 - r`, and offcentral logarithmic branch convention.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md`
  supplies the dyadic proof that endpoint decay `|W_hat|+|W_hat'| << |t|^-2`
  closes the pure zero/branch weighted sums under `N(T)=O(T log T)`.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md`
  supplies the compatible good-prime Sym2 finite-part convention and the
  cancellation of `kappa_sym` inside H2.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md`
  supplies the exact Agent 3 H2 decomposition and the coefficient check
  giving `-r`.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md`
  records source-supported narrow inputs: EC zero counting for multiplicity
  sums, ordinary Mertens, and limits of the cited literature. It does not
  source-close the endpoint S1 branch theorem.

# Branch/Regularization Analysis

The old literal global branch assertion fails at endpoint decay `q=2`.
Accumulating the branch-index jump along the left edge produces size

```text
N(t) |W_hat(-eta+it)| ~ (t log t) t^-2,
```

whose integral diverges like `int (log t)/t dt`.

The renormalized replacement is to work in finite cut rectangles and subtract
the local logarithmic branch model before taking the left edge:

```text
A_E^reg,T(z)
 = A_E(z) - c_0 log(1/z)
   - sum_{a in B, |Im a| <= T+1} c_a log(1/(z-a)).
```

`RegularLogLeftEdge(E,W,eta;c)` is exactly the missing analytic input: it says
the regularized horizontal and left boundaries are controlled after the local
branch models are removed. This input is independent of H1 reciprocal-residue
questions; it gives no estimate for `1/L'(rho)`.

For each branch `a=beta+i gamma`, the cut-lip contribution is not a residue.
It is the Laplace integral

```text
I_a(K)
 = c_a K^a int_0^(beta+eta) e^(-uv) W_hat(a-v) dv.
```

For `beta <= 0`, Watson expansion is summable:

```text
sum_{a in B^-} I_a(K)
 = (1/u) sum_{a in B^-} c_a K^a W_hat(a)
   + O_E,W(u^-2) + O_E,W(K^-eta).
```

For `beta > 0`, Watson expansion remains true locally but is not a finite-part
subtraction:

```text
I_a(K) - c_a K^a W_hat(a)/u = O_a,W(K^beta u^-2),
```

and `K^beta u^-2` does not tend to zero. Therefore the full right-lip
aggregate `R_S1^+` is the minimal stable retained/subtracted object.

In the standard right ledger, Sym2 and zeta good-prime factors are absolutely
convergent at `Re(1+2a)>1`; hence right branches in S1 come from right-of-line
zeros of `L_good(E,s)`:

```text
a = rho - 1,
Re rho > 1,
c_a = -ord_{s=rho} L_good(E,s).
```

Thus right-branch absence is an RH/GRH-type hypothesis for this ledger, not a
consequence of the current source packet.

# Closure or Obstruction

Closure:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)
```

is a conditional theorem under the six hypotheses in the theorem target. The
proof is Cauchy's theorem in finite cut rectangles:

1. start from Mellin inversion on `Re z=c`;
2. subtract the finite branch model and shift to `Re z=-eta`;
3. evaluate the central branch as `c_0 log log K + constant`;
4. evaluate every noncentral branch as its exact cut-lip integral `I_a(K)`;
5. sum Watson expansions only on `B^-`;
6. retain or subtract `R_S1^+`;
7. pass to the ordinate sequence supplied by `RegularLogLeftEdge`.

Endpoint H2 then follows from the exact decomposition:

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

Obstruction:

If a right branch `a` with `Re a=beta>0` is present and neither `R_S1^+` nor an
exact full-lip cancellation theorem is used, pointwise H2 finite-part closure
fails. In particular, subtracting only

```text
B_S1^+(K;E,W,c)
 = (1/log K) sum_{a in B^+} c_a K^a W_hat(a)
```

leaves a remainder of size `K^beta/(log K)^2` for that branch. Hence the
non-subtracted/non-retained theorem

```text
log P_E,W(K) + r log log K = C_H2,E,W + o(1)
```

is valid only under `B^+=empty` or `R_S1^+=o(1)`; otherwise the correct
statement is the right-lip-renormalized H2 theorem displayed above.

# Dependency Impact

- H2 branch status: sharpened to `CONDITIONAL_THEOREM` with explicit
  retained/subtracted `R_S1^+`.
- H2 final assembly may use this packet only in a matching mode:
  no-right-branch, full-lip-retained, or full-lip-subtracted.
- Agent09 must not use first-Watson right-branch subtraction as a finite-part
  theorem unless it also proves full-lip cancellation.
- The remaining S1 analytic blocker is `RegularLogLeftEdge(E,W,eta;c)` plus
  exact good-prime Sym2 normalization/zero ledger. EC zero summability alone is
  not enough.
- No H2 branch damping transfers to H1 residue closure. This packet contains
  no reciprocal derivative, principal-value shell, or BFMT input.
