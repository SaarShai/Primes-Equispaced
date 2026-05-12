---
schema_version: 1
title: "S1-C zero-term branch analysis for the smoothed EC trace"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.76
sources:
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
tags: [ec-ndc, s1, explicit-formula, zeros, branch-cut]
---

# S1-C Zero-Term Branch Analysis

status: `RIGOROUS_REDUCTION`

## Narrow Question

For

```text
S_1,W(K) = sum_p W(p/K) a_p/p,
```

and a zero

```text
rho = 1 + i gamma,    gamma != 0,
```

of `L(E,s)`, the model branch calculation gives a lower-order term

```text
-m_rho K^(i gamma) W_hat(i gamma) / log K
```

under the assumptions below. More exactly, the zero contributes a branch-cut
integral whose leading asymptotic is the displayed term. It is not a persistent
`K^(i gamma)` coefficient for `S_1,W`.

The persistent coefficient belongs to the logarithmically weighted trace, i.e.
the `-L'/L` side with an extra `log p`. Passing from that pole to the unweighted
prime-linear trace integrates the pole into a logarithmic branch point and costs
one factor of `1/log K`.

## Setup And Assumptions

Write

```text
A_E(z) = sum_p a_p p^(-1-z)
```

initially in its half-plane of convergence, and use Mellin inversion in the
form

```text
S_1,W(K)
  = (1/2 pi i) integral_(c) K^z W_hat(z) A_E(z) dz,
  c > 0,
```

where

```text
W_hat(z) = integral_0^infty W(t) t^(z-1) dt.
```

The branch calculation assumes:

1. `W_hat` is holomorphic at `z0=i gamma`. This holds for the smoothstep
   kernels at every nonzero imaginary `z0`; their pole at `0` is a separate
   central-zero issue.
2. Near `z0=i gamma`, the continuation of `A_E(z)` has local form

   ```text
   A_E(z) = m_rho log(z - z0) + H(z),
   ```

   where `H` is holomorphic near `z0`, and `m_rho=ord_rho L(E,s)` after
   subtracting any companion local pieces that are holomorphic at `z0`.
3. The branch is reached from `Re z > 0`, with a local cut from `z0` to the
   left. Changing branch conventions changes only the constant analytic part,
   not the branch-cut jump or the order in `K`.
4. The contour shift/localization needed to isolate this branch point is
   justified. This note analyzes the local zero term; it does not prove the
   global zero-sum convergence.

If another Euler factor or companion term has a logarithmic singularity at the
same `z0`, replace `m_rho` by the net coefficient of `log(z-z0)` in `A_E`.
If `A_E` had a pole at `z0` instead of a logarithmic branch point, the
conclusion would change to a persistent residue term. For the prime-linear
trace coming from `log L`, the model singularity is logarithmic.

## Model Integral

Let

```text
x = log K,       z0 = i gamma,       phi(z) = W_hat(z),
```

and isolate the singular part

```text
I_rho(K)
 = (m_rho / 2 pi i)
   integral_(c) exp(x z) phi(z) log(z - z0) dz.
```

The inverse Laplace model is

```text
(1 / 2 pi i) integral_(c) exp(x w) log w dw = -1/x,    x > 0.
```

Equivalently, deforming around the left-going branch cut
`z=z0-u`, `u>0`, gives the local branch integral

```text
I_rho(K)
 = -m_rho K^z0 integral_0^infty exp(-x u) phi(z0-u) du
   + smaller contour terms.
```

Watson expansion at `u=0` gives

```text
I_rho(K)
 = m_rho K^z0
   ( - phi(z0)/x + phi'(z0)/x^2 + O_W,gamma(x^(-3)) )
```

when `phi` is sufficiently regular near the cut. Therefore

```text
I_rho(K)
 = -m_rho K^(i gamma) W_hat(i gamma) / log K
   + O_W,gamma((log K)^(-2)).
```

This is the precise sense in which H2B's `K^(i gamma) W_hat(i gamma)/log K`
scenario is correct for `S_1,W`, up to sign and multiplicity conventions.

If `W_hat(i gamma)=0`, the leading term vanishes and the first possible
contribution is

```text
m_rho K^(i gamma) W_hat'(i gamma) / (log K)^2.
```

If the zero is not on `Re(s)=1`, so that `rho=beta+i gamma` and
`z0=rho-1`, the same calculation gives

```text
-m_rho K^(beta-1+i gamma) W_hat(rho-1) / log K
```

provided `W_hat` is holomorphic at `rho-1`.

## Logarithmic-Derivative Cross-Check

Near `rho`, the logarithmic derivative has a pole:

```text
-L'/L(1+z) = -m_rho/(z-z0) + holomorphic.
```

The corresponding log-weighted prime trace has model contribution

```text
-m_rho K^z0 W_hat(z0),
```

which is persistent when `Re z0=0`.

But

```text
A_E'(z) = m_rho/(z-z0) + holomorphic
```

locally, so

```text
A_E(z) = m_rho log(z-z0) + holomorphic.
```

Thus the persistent pole residue is not the zero term for
`sum_p W(p/K) a_p/p`. It is the zero term before removing the `log p` weight.
Removing that weight is exactly the integration that turns the pole into a
logarithmic branch point and produces the `1/log K` factor.

## Central Zero Contrast

The central zero has `z0=0`. This is different because the smooth weights used
in the sprint satisfy

```text
W_hat(z) = 1/z + holomorphic
```

at `z=0`. The interaction

```text
W_hat(z) A_E(z) ~ (1/z) c log(1/z)
```

produces

```text
c log log K + O(1),
```

not `1/log K`. This is why the central zero gives the main logarithmic drift,
while a fixed noncentral zero with `gamma != 0` gives only a decaying
oscillation in `S_1,W(K)`.

For the H2 bookkeeping of the previous sprint, the central coefficient of
`S_1,W` remains

```text
(1/2 + kappa_sym/2 - r) log log K,
```

subject to the symmetric-square and prime-harmonic split. The present note
only resolves the offcentral branch scale.

## Real Pairing

For real weights and real elliptic-curve coefficients, zeros occur in conjugate
pairs. A simple pair `1 +/- i gamma` contributes, to leading order,

```text
-(2 m_rho / log K) Re( K^(i gamma) W_hat(i gamma) ).
```

This is an oscillation in `log K`, but its amplitude is `O(1/log K)` for each
fixed zero frequency. Smoothstep decay of `W_hat(i gamma)` is still needed to
sum over many zeros, but it is not needed to make any fixed noncentral zero
decay in `K`.

## Conclusion For The H2 Fork

For the smoothed prime-linear trace `S_1,W(K)`, the local branch analysis
supports:

```text
noncentral zero at rho=1+i gamma
  -> branch integral
  -> -m_rho K^(i gamma) W_hat(i gamma)/log K
     + O((log K)^(-2)).
```

It does not support a persistent `c(gamma) K^(i gamma)` term in `S_1,W` under
the logarithmic-branch assumptions above.

The pointwise `B+o(1)` H2 obstruction from noncentral zeros is therefore not
forced by the first-order trace alone. Remaining pointwise risks are global,
not local:

- proving the continuation and singular decomposition of `A_E(z)` with the
  exact Agent 3 local-factor normalization;
- proving enough decay/convergence for the full offcentral zero sum;
- handling possible coincident singularities from companion terms;
- proving the symmetric-square finite part and the local product bookkeeping.

## Do Not Promote

Do not promote this note to a closed S1/H2 theorem unless:

- `A_E(z)=sum_p a_p p^(-1-z)` is derived from the exact Agent 3 local factor
  normalization, including bad-prime convention;
- the local coefficient of `log(z-i gamma)` in `A_E` is fixed with sign and
  multiplicity from the chosen branch of `log L(E,s)`;
- the global contour shift and all horizontal/left-contour remainders are
  bounded;
- the full zero sum

  ```text
  (1/log K) sum_{gamma != 0} m_rho K^(i gamma) W_hat(i gamma)
  ```

  is proved convergent or otherwise controlled in the theorem mode being used;
- the central coefficient is stated in analytic-rank language before any BSD
  rank substitution;
- the symmetric-square companion and prime-harmonic terms are included when
  composing back into the smoothed EC Mertens product;
- any external source claim is source-verified by the sprint rule
  `curl + pdftotext + verbatim quote + page/eq`.
