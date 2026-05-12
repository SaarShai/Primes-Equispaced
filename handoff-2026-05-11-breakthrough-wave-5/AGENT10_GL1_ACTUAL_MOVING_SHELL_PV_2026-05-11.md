---
title: "AGENT10 GL1 Actual Moving Shell PV"
date: 2026-05-11
type: theorem-attempt
tier: blocker-reattack
status: NO_GO
confidence: 0.91
tags: [breakthrough-wave-5, agent10, gl1, sharp-cutoff, moving-shell-pv, harmonic-weight, smoothing, filtering, no-go]
---

## Verdict

No sharp GL1 theorem is proved in this reattack.

The sharp theorem has a clean conditional route independent of EC H1, but the
remaining input is exactly one of the following GL1-specific statements:

```text
GL1-ActualMovingShellPV(chi,rho)
```

or the stronger absolute substitute

```text
GL1-AbsoluteHarmonicWeight(chi,rho).
```

Neither follows from the read anchors. Smoothing and finite filtering still do
not transfer to the sharp cutoff, because the transfer requires uniform control
of the high vertical transition/tail band where the sharp Mellin factor is the
critical harmonic weight `1/(lambda-rho)`.

Outcome:

```text
local target residue algebra: closed
sharp theorem from PV/absolute input: conditional only
actual moving shell PV: not proved
absolute harmonic-weight bound: not proved
smoothing/filtering to sharp cutoff: no-go without the same sharp tail bound
```

## Theorem Target

Let `chi` be primitive nonprincipal and let

```text
rho = 1/2 + i t
```

be a simple noncentral zero of `L(s,chi)`. Put `u=log K` and

```text
F_K(w) = K^w / (w L(rho+w,chi)).
```

The target residue is local:

```text
Res_(w=0) F_K(w)
  = u/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2).
```

For a simple off-target zero

```text
lambda = 1/2 + i gamma,
alpha_lambda = gamma - t,
```

the sharp residue is

```text
exp(i alpha_lambda u) / (i alpha_lambda L'(lambda,chi)).
```

Thus the live GL1 input is the actual moving principal value bound, on the
same legal Perron heights used for the rectangle:

```text
GL1-ActualMovingShellPV(chi,rho):
  sum_(2^j <= T_box(e^(2U))) B_j(U) = o(U),

B_j(U)
  = sup_(u in [U,2U])
      | sum_(2^j < |alpha_lambda| <= 2^(j+1))
          exp(i alpha_lambda u)
          / (i alpha_lambda L'(lambda,chi)) |.
```

Equivalently, the unshelled form needed at a legal height `T_box(e^u)` is

```text
Z_GL1(u,T_box)
  = sum_(lambda != rho, 0 < |alpha_lambda| <= T_box(e^u))
      exp(i alpha_lambda u)
      / (i alpha_lambda L'(lambda,chi))
  = o(u)
```

uniformly enough for the finite-box Perron shift.

Conditional sharp theorem candidate:

```text
If rho is simple and noncentral, the same legal heights have
rectangle/truncation/trivial-residue error o(u), all off-target Laurent
polynomial terms are excluded, retained below scale, or collectively o(u),
and GL1-ActualMovingShellPV holds, then

  c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

This candidate is purely GL1. It imports no EC H1 statement.

## Source Anchors

Read anchors:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT10_GL1_SHARP_OFFTARGET_CONTROL_2026-05-11.md
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT09_GL1_SHARP_OFFTARGET_CONTROL_2026-05-11.md
primes-equispaced/handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
primes-equispaced/L2_facts/farey-claim-ledger.md
```

Anchor state used:

```text
Wave 4 Agent10:
  sharp GL1 remains conditional on GL1-ActualMovingShellPV or GL1-ABS;
  smoothing transfer is circular without sharp tail control.

Top-10 Agent09:
  H1 DPMV/PV progress does not transfer to GL1 because the sharp coefficient
  is 1/((lambda-rho)L'(lambda,chi)).

All-in GL1 shifted Perron:
  local residue algebra is closed; global simplicity still leaves the
  simple-zero fixed-weight PV aggregate.

Claim ledger:
  Top-10 GL1 update and all-in GL1 packet both mark sharp GL1 as blocked
  without actual moving PV or critical weighted reciprocal-derivative input.
```

## Moving-Shell PV Attempt

The only direct proof shape is to control the actual coefficients

```text
b_lambda = 1 / (i alpha_lambda L'(lambda,chi)).
```

Dyadic decomposition reduces the Perron remainder to the shell supremum
`B_j(U)` above. If the shell sum is `o(U)` after summing all
`2^j <= T_box(e^(2U))`, then the sharp off-target residue aggregate is
`o(U)`.

The available smoothing/filtering data do not estimate `B_j(U)`. A fixed
smooth cutoff replaces the sharp harmonic coefficient by

```text
W_hat(i alpha_lambda) / L'(lambda,chi),
```

with extra vertical decay or zeros. That controls a different weighted sum.
Let `W_eta` approximate the sharp step, so

```text
W_hat_eta(w) -> 1/w.
```

The transfer error is

```text
Delta_eta(u,T)
  = sum_(lambda != rho, 0 < |alpha_lambda| <= T)
      exp(i alpha_lambda u)
      (W_hat_eta(i alpha_lambda) - 1/(i alpha_lambda))
      / L'(lambda,chi).
```

For fixed `eta`, smooth decay can make this manageable. To recover the sharp
cutoff, the constants must remain uniform as the transition band moves out.
The uncontrolled part is a sharp harmonic tail of the form

```text
sum_(eta^(-1) < |alpha_lambda| <= T_box(e^u))
  exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi)).
```

Uniformly proving that this is `o(U)` is the same moving-shell PV problem.
Thus the smoothing limit is circular unless the sharp tail theorem is already
available.

Filtering has the same boundary. Finite Mellin zeros can kill finitely many
specified off-target residues, but after the killed set the remaining infinite
tail still has the original harmonic sharp coefficient. Infinite filtering
would define a different coefficient theorem and would need its own
admissibility, inverse Mellin, and tail estimates.

## Absolute Bound Attempt

The absolute route would bypass cancellation by proving a critical l1 shell
bound. Define

```text
R_j(chi,rho)
  = sum_(2^j < |alpha_lambda| <= 2^(j+1))
      |L'(lambda,chi)|^(-1).
```

Then

```text
B_j(U) <= 2^(-j) R_j(chi,rho),
```

up to harmless fixed small-alpha shells. Hence it would be sufficient to prove

```text
GL1-AbsoluteHarmonicWeight(chi,rho):
  sum_(2^j <= T_box(e^(2U))) 2^(-j) R_j(chi,rho) = o(U).
```

This is stronger than the actual PV theorem and is also independent of EC H1.
It would close the sharp GL1 theorem together with the same finite-box
rectangle/truncation and Laurent-boundary hypotheses.

The bound is critical. If

```text
R_j(chi,rho) = O(2^j),
```

then each dyadic shell contributes only `O(1)`, so a Perron-scale height with
`J(U) = log_2 T_box(e^(2U)) asymp U` gives merely `O(U)`, not `o(U)`.
Any estimate of the form

```text
R_j(chi,rho) << 2^j (log 2^j)^A
```

is worse. Closure needs genuine averaged saving across the whole legal height
range, for example a dyadic Cesaro form strong enough to make

```text
(1/U) sum_(j <= J(U)) 2^(-j) R_j(chi,rho) -> 0.
```

No read source supplies this critical harmonic-weight reciprocal-derivative
bound for Dirichlet zeros shifted by the target zero `rho`.

## No-Go or Closure

Closure would be immediate from either live input:

```text
GL1-ActualMovingShellPV
  + GL1-Sharp-Rectangle
  + GL1-OffTargetLaurentBoundary
  => c_K(chi,rho) = log K/L'(rho,chi) + o(log K).

GL1-AbsoluteHarmonicWeight
  + GL1-Sharp-Rectangle
  + GL1-OffTargetLaurentBoundary
  => c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

But neither live input is proved.

No-go model for smoothing/filtering transfer:

```text
alpha_n = n,
b_n = b_(-n) = 1/(2n),
S_T(u) = sum_(1 <= n <= T) cos(nu)/n.
```

For every large interval `[U,2U]`, choose an integer `m` with
`2*pi*m in [U,2U]`. Then

```text
S_T(2*pi*m) = H_T = log T + O(1).
```

At sharp Perron height `T = exp(cU)` this is `cU + O(1)`, not `o(U)`.

The same model is harmless for fixed smooth kernels with rapid vertical decay:

```text
sum_n |W_hat(in)| < infinity.
```

It is also harmless after killing any finite set of modes, because the sharp
tail from the remaining modes still has size `log T` at resonance. Therefore
fixed smoothing success and finite filtering success do not logically imply
the sharp cutoff theorem. Any proof route using only those mechanisms would
prove a false statement in this harmonic model.

The model is not claimed to be the Dirichlet zero set. Its role is narrower:
it isolates the exact missing hypothesis. Spacing, conjugation symmetry,
fixed-kernel decay, finite filtering, square-summability of smoothed
coefficients, and fixed-u convergence do not imply the moving sharp harmonic
PV bound needed at Perron height.

## Dependency Impact

No theorem is promoted.

Dependency state:

```text
EC H1:
  irrelevant to this GL1 target; no H1 progress is imported.

GL1 sharp:
  remains blocked at GL1-ActualMovingShellPV or the stronger
  GL1-AbsoluteHarmonicWeight bound.

GL1 smoothed/filtering:
  remains a separate conditional theorem mode for c_(W,K), not evidence for
  sharp c_K unless uniform sharp-tail control is added.

Koyama e^(-gamma) product limit:
  still cannot be promoted from current packets because the coefficient-side
  sharp asymptotic c_K(chi,rho)=logK/L'(rho,chi)+o(logK) is not closed.
```

Next admissible attack:

```text
Prove the actual target-shifted moving PV cancellation for
1/(i alpha_lambda L'(lambda,chi)), or prove the dyadic absolute harmonic
weight bound above. Do not reroute through fixed smoothing or finite filters
unless the sharp transition/tail estimate is proved explicitly.
```
