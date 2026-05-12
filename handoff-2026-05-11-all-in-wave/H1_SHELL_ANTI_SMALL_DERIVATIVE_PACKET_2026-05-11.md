---
schema_version: 1
title: "H1 shell anti-small-derivative packet"
date: 2026-05-11
worker: "Worker A"
type: proof-attempt
tier: working
status: COMPLETE
outcome: "SUCCESS_CRITERION_2: sharper no-go plus reduced H1 target"
confidence: 0.84
tags: [ec-ndc, h1, shell-moment, anti-small-derivative, no-go]
---

# H1 Shell Anti-Small-Derivative Packet

Outcome: no theorem promotion. I do not see a new proof of

```text
J_E,2(T) = sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
        <= C_E T^(3-delta)
```

for a fixed EC/newform from the current spine. The useful output is sharper:
the standard inputs currently on the table cannot imply this shell moment,
even in a strong logical/model sense. The reduced target that can still close
positive-rank H1 is a weighted `l^1` reciprocal tail, strictly weaker than the
`l^2` shell moment.

## Sources Read

- `HANDOFF.md`
- `L2_facts/farey-claim-ledger.md`
- `handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md`
- `handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md`
- `handoff-2026-05-11-h1-shell-moment-wave/TC_HEIGHT_EXPONENT_AUDIT.md`
- `handoff-2026-05-11-gpt55-extra-high-continuation/H1_LZ_HEIGHT_VERIFICATION_2026-05-11.md`

No external source was added. `start.md` was requested by local instructions
but is absent under `primes-equispaced`.

## Sharper No-Go

The following inputs do not control the anti-small-derivative tail:

```text
GRH/no-right-half-zero
+ all offcentral zeros simple
+ local zero count N_E(T,2T) << T log^B T
+ zero spacing or pair-correlation-type separation
+ positive moments of L'(rho)
+ selected horizontal minimum-modulus heights for 1/L(E,s)
+ signed mollified first moments
```

Reason: none of these hypotheses excludes a sparse set of simple zeros with
very small derivative.

Model theorem. Fix any zero ordinates satisfying the desired zero-count and
spacing conditions. Attach derivative weights `d_gamma != 0`. For any `M>0`,
replace one weight in each dyadic shell by

```text
d_gamma = T^(-M)
```

and keep all other weights of size `1`. This leaves zero count, spacing,
pair-correlation data, simplicity, and all upper positive-moment bounds
unchanged or improved. It also does not interact with selected horizontal
height bounds, which are statements about values of `L` away from the zero.
But the reciprocal shell moment has

```text
J_E,2(T) >= T^(2M).
```

Choosing `M > (3-delta)/2` violates the desired `T^(3-delta)` bound. Thus any
proof using only these standard inputs must have hidden an anti-small-
derivative hypothesis.

This is not a counterexample inside the EC L-function class. It is a logical
separation result: the currently named standard inputs do not contain the
information needed to bound reciprocal derivatives.

## Why LZ Height Does Not Repair This

The Li-Zaharescu continuation file conditionally routes the horizontal contour
height:

```text
sup_strip |1/L(E,x+iT_n)| <= exp(A_E log T_n/loglog T_n) = T_n^o(1)
```

on selected unit-interval heights, under normalized EC/newform RH/no-right-
half-zero. This controls horizontal contour tails only.

It does not imply a lower bound for `|L'(rho)|` at every zero. A derivative
bound at `rho` would require a local lower bound on a zero-free circle around
`rho`,

```text
min_{|s-rho|=r_T} |L(E,s)| >= T^(-mu),
```

with `mu-kappa<1` when `r_T=T^(-kappa)`. Selected horizontal heights are too
remote and too sparse to give this circle bound for each zero. The shell
moment remains separate from `H-height`.

## Reduced Theorem Target

For positive analytic rank `r>=1`, H1 does not need the full naked `l^2`
moment if the goal is only to make the offcentral reciprocal residue aggregate
smaller than the central polynomial. It is enough to prove the weighted
absolute tail

```text
H1-weighted-l1(E,W,epsilon):
  A_W(T) :=
    sum_{T<|gamma|<=2T, simple}
      |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1)
  <= C_E,W T^(-epsilon)
```

for all large dyadic `T`, with multiple zeros handled by the existing Laurent
exceptional-term package.

For the current smoothstep-scale kernel,

```text
|W_hat(it)| << (1+|t|)^(-2),
```

this follows from the still-weaker unweighted `l^1` shell target

```text
R_E,1(T) :=
  sum_{T<|gamma|<=2T, simple} |L'(E,1+i gamma)|^(-1)
<= C_E T^(2-epsilon).
```

Indeed `A_W(T) << T^(-2) R_E,1(T) << T^(-epsilon)`.

The old shell-moment target implies this by Cauchy-Schwarz:

```text
R_E,1(T)
 <= N_E(T,2T)^(1/2) J_E,2(T)^(1/2)
 << T^(2-delta/2) log^B T,
```

so `H1-weighted-l1` is strictly weaker than `J_E,2(T)<=T^(3-delta)` as a
positive-rank H1 closure input.

## Reduced Closure Skeleton

Assume:

```text
1. finite-box H1 reciprocal Perron identity with central polynomial Q_E,W(u);
2. analytic rank r>=1 and leading central term q_r u^r, q_r != 0;
3. H-left closed by eta>1/2;
4. horizontal H-height controlled, e.g. by the conditional LZ selected-height
   route in the read spine;
5. original-line truncation and moving-box choices satisfy the existing
   contour-tail inequalities;
6. multiple-zero Laurent terms are absent, retained below degree r, killed by
   kernel zeros, or explicitly assumed O(u^(r-epsilon));
7. H1-weighted-l1(E,W,epsilon).
```

Then the simple offcentral residue series

```text
Z_W(u) =
  sum_{gamma simple}
    W_hat(i gamma) e^(i gamma u) / L'(E,1+i gamma)
```

converges absolutely, with dyadic tail `O(Y^(-epsilon))`. Hence

```text
Z_W(u) = O_E,W(1) = o(u^r).
```

The finite-box identity plus contour-tail limits gives

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r),
```

so positive-rank H1 closes at the required central scale. This avoids proving
the stronger `l^2` shell moment when only absolute convergence of the residue
profile is needed.

## Anti-Small-Derivative Routes For The Reduced Target

The reduced `l^1` target can be attacked by any one of:

```text
Pointwise:
  |L'(E,1+i gamma)| >= T^(-1+eta) log^(-B) T
  gives R_E,1(T) << T^(2-eta) log^B T.

Tail:
  N_E(T;V) := #{gamma in shell: |L'(rho)|^(-1)>V}
  <= C T^(2-epsilon) V^(-1-alpha)
  gives R_E,1(T) << T^(2-epsilon).

Borderline tail plus cap:
  N_E(T;V) <= C T^(2-epsilon) V^(-1), 1<=V<=T^A,
  and |L'(rho)|^(-1)<=T^A
  gives R_E,1(T) << T^(2-epsilon) log T,
  hence any smaller epsilon.

Local minimum modulus:
  zero-free circle radius T^(-kappa) and boundary lower bound T^(-mu)
  gives pointwise exponent eta=1-(mu-kappa), useful when mu-kappa<1.
```

These are still genuine anti-small-derivative inputs. The gain is that the
needed tail exponent is `l^1` and rank-aware, not the stronger `l^2` moment
originally named as `H1-shell-moment(E,delta)`.

## Risks

- The model no-go is a logical separation, not an EC counterexample.
- `H1-weighted-l1` closes positive-rank absolute residue control, but rank zero
  still needs the profile/product-average fallback unless coefficients die or
  are subtracted.
- Multiple zeros remain outside this packet except through the existing
  Laurent exceptional-term conditions.
- The LZ height route is conditional on normalized EC/newform RH/no-right-
  half-zero and does not address residues.
- The reduced target is sufficient only in theorem modes where absolute
  convergence of the offcentral residue series is acceptable; a PV/cancellation
  theorem could be weaker but would need uniformity in `u`.

## Verification

- Confirmed target directory existed before writing.
- Wrote exactly this file under `primes-equispaced`.
- Did not edit Koyama correspondence or any file outside the requested path.
- No code or numerical computation was needed.

## Changed Files

- `handoff-2026-05-11-all-in-wave/H1_SHELL_ANTI_SMALL_DERIVATIVE_PACKET_2026-05-11.md`

