---
schema_version: 1
title: "S1-F symmetric-square companion term for H2"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.72
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
tags: [ec-ndc, h2, s1, symmetric-square, explicit-formula]
---

# S1-F Symmetric-Square Companion Term For H2

status: `RIGOROUS_REDUCTION`

No theorem is promoted. The S1 trace term alone is not enough for H2. For the
exact Agent 3 product, the quadratic local-log term forces both a
symmetric-square finite part and a universal prime-harmonic finite part.

## Verdict

For good primes let

```text
lambda_p = a_p / sqrt(p),
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Then H2 needs the companion decomposition

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K),
```

where

```text
S_sym,W(K)  = sum_{p good} W(p/K) chi_sym2(p)/p,
M_good,W(K) = sum_{p good} W(p/K)/p.
```

The universal term `-(1/2)M_good,W(K)` contributes
`-(1/2)log log K`. Omitting it gives the wrong coefficient. The
symmetric-square term is expected to be constant-scale in the usual case, but
that is a theorem input, not local algebra.

## Agent 3 Normalization

The reproducer uses

```text
good p: A_p(1) = 1 - a_p/p + 1/p,
bad  p: A_p(1) = 1 - a_p/p,
log P_E,W(K) = -sum_p W(p/K) log A_p(1).
```

At a good prime,

```text
-log(1 - a_p/p + 1/p)
 = a_p/p
   + (a_p^2 - 2p)/(2p^2)
   + O(p^(-3/2)),
```

and

```text
(a_p^2 - 2p)/(2p^2)
 = (1/2)(a_p^2/p - 1)/p - (1/2)(1/p).
```

This is the source of `S_sym,W` and `M_good,W`. The Agent 3 `L2` factor is not
this quadratic term; its good-prime logarithm starts at `a_p/p^2` and is
absolutely convergent for the H2 coefficient problem.

## Prime-Harmonic Term

The required ordinary prime input is

```text
M_good,W(K)
 = log log K + C_M,E,W^good + o(1),
```

with the constant defined by the finite part

```text
C_M,E,W^good =
  lim_{K -> infinity} (sum_{p good} W(p/K)/p - log log K).
```

Equivalently, if `C_M,W` is the same finite part over all primes, then

```text
C_M,E,W^good = C_M,W - sum_{p bad} 1/p
```

for kernels with `W(0)=1`. This is an ordinary weighted prime-Mertens theorem
plus finite bad-prime removal.

No offcentral `zeta` zero can create a `Re(s)=1` oscillation in this term.
In a source-closed proof, nontrivial `zeta` zeros enter with `Re(rho)-1 < 0`
in the Mellin variable and are power-decaying. The only H2-scale output of
`M_good,W` is the displayed `log log K` and its finite part.

## Symmetric-Square Finite Part

Let

```text
D_sym,E(s) = sum_{p good} chi_sym2(p) p^(-s)
```

initially for `Re(s)>1`. The needed theorem is a weighted first-prime
explicit formula for

```text
S_sym,W(K)
 = (1/2 pi i) integral_(c)
     K^z W_hat(z) D_sym,E(1+z) dz.
```

Name

```text
kappa_sym = ord_{s=1} L_sym,E(s),
```

with positive order for a zero and negative order for a pole, where
`L_sym,E` is the symmetric-square or adjoint object whose first unramified
prime trace is `chi_sym2(p)`.

The theorem needed by H2 is:

```text
S_sym,W(K)
 = -kappa_sym log log K
   + C_sym,E,W
   + Z_sym,E,W(K)
   + o(1),
```

where `C_sym,E,W` is a finite part and `Z_sym,E,W(K)` is either proved
`o(1)` or explicitly retained. In the expected noncentral-finite-part case
`kappa_sym=0`, this reduces to

```text
S_sym,W(K) = C_sym,E,W + Z_sym,E,W(K) + o(1).
```

Setting `kappa_sym=0` requires a source-verified nonzero finite central value
statement for the exact normalization being used. It should not be inserted
by analogy.

## Offcentral Sym2 Zeros And Poles

The companion term should be derived from `log L_sym`, not directly from
`-L_sym'/L_sym`. If `rho` is a zero or pole of `L_sym,E` and

```text
m_rho = ord_{s=rho} L_sym,E(s),
```

then locally

```text
D_sym,E(s) = m_rho log(s-rho) + holomorphic terms
```

up to the absolutely convergent higher-prime-power correction.

Consequences for the Mellin formula:

- If `rho = 1`, the logarithmic branch point sits at the pole of `W_hat(z)` at
  `z=0`, giving the only symmetric-square `log log K` term:

  ```text
  -m_1 log log K.
  ```

- If `rho = 1 + i gamma` with `gamma != 0`, then `W_hat` is analytic at
  `z=i gamma`. The branch-point contribution has the lower-order shape

  ```text
  -m_rho K^(i gamma) W_hat(i gamma) / log K
  ```

  plus smaller powers of `1/log K`, provided the zero sum can be shifted and
  summed.

- If `Re(rho)<1`, the same term has an additional factor
  `K^(Re(rho)-1)` and decays faster.

- If any zero or pole with `Re(rho)>1` is allowed, pointwise H2 fails unless
  another term cancels it.

Thus offcentral symmetric-square zeros or poles do not create new
`log log K` terms. In the log-prime formulation they also do not create
constant-size oscillations; they create `K^(i gamma)/log K` oscillations,
assuming the branch-cut explicit formula is justified. A persistent
`K^(i gamma)` term belongs to a logarithmic-derivative formula before
integrating back to the prime-log sum, or to a theorem gap that must be
spelled out.

The smoothstep kernel helps only with summability over high zeros through the
decay of `W_hat`. It does not remove the first few fixed frequencies; it makes
their expected contribution lower order by the extra `1/log K` from the
logarithmic branch point.

## Effect On Final H2

The S1 trace theorem must be stated with the same `kappa_sym`:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + Z_1,E,W(K)
   + o(1),
```

where

```text
r = ord_{s=1} L(E,s).
```

Together with

```text
S_sym,W(K)  = -kappa_sym log log K + C_sym,E,W + Z_sym,E,W(K) + o(1),
M_good,W(K) =  log log K + C_M,E,W^good + o(1),
```

the coefficient in `log P_E,W(K)` is

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

The constant is

```text
B_E,W =
  C_1,E,W
  + (1/2) C_sym,E,W
  - (1/2) C_M,E,W^good
  + C_ge3,E
  + B_bad,E.
```

The theorem mode is:

```text
log P_E,W(K)
 = -r log log K
   + B_E,W
   + Z_1,E,W(K)
   + (1/2) Z_sym,E,W(K)
   + o(1).
```

Pointwise H2-limit follows only if both zero terms are `o(1)`. For the
symmetric-square companion term, the expected offcentral contribution is
already `O(1/log K)` under the needed zero-sum theorem. If S1 still has a
persistent zero term, this companion term does not repair it; final H2 must be
oscillatory or averaged.

## Theorem Needed

The missing source-closed input is a fixed-curve, fixed-kernel theorem:

```text
Sym2-W finite-part theorem.
For the exact Agent 3 good-prime normalization and an admissible W,
D_sym,E(s) has a controlled logarithmic explicit formula at s=1,
all bad-prime and higher-prime-power corrections are finite,
and

S_sym,W(K)
 = -kappa_sym log log K + C_sym,E,W + o(1)
```

or the same statement with the explicit
`-(1/log K) sum_{rho != 1} m_rho K^(rho-1) W_hat(rho-1)` term retained and
proved to be `o(1)` under stated zero-location and zero-sum hypotheses.

Separately, H2 needs the ordinary weighted prime-Mertens finite part for
`M_good,W(K)`. That input supplies the mandatory `-1/2 log log K` contribution
to `log P_E,W(K)`.

No external citation is used in this file. Any future promotion must
source-verify the symmetric-square analytic continuation, central
zero/pole/nonvanishing statement, zero-counting needed for the smoothed
zero sum, and the exact local normalization.

## Do Not Promote Unless

- The exact Agent 3 local factors are used, including the bad-prime convention.
- `S_1,W` is not used alone; `S_sym,W` and `M_good,W` are present in the H2
  coefficient calculation.
- `C_M,E,W^good` and `C_sym,E,W` are defined as finite parts for the same
  smoothing kernel `W`.
- `kappa_sym = ord_{s=1}L_sym,E(s)` is stated before any claim that
  `S_sym,W(K)` is constant-scale.
- Any claim `kappa_sym=0` is source-verified for the exact symmetric-square or
  adjoint normalization.
- Offcentral symmetric-square zeros and poles are derived from the log-prime
  Mellin formula; they are either proved `o(1)` or retained explicitly.
- No persistent symmetric-square oscillation is silently dropped; if a theorem
  uses a logarithmic-derivative formula, it must integrate back to the
  log-prime sum.
- Final H2 is declared pointwise, oscillatory, or averaged, and H1 composition
  uses the same mode.
- The final coefficient is stated first with analytic rank
  `ord_{s=1}L(E,s)`, not script rank, unless rank equality is separately
  assumed or verified.
