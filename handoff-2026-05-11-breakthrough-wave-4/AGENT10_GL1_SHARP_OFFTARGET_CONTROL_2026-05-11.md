---
title: "AGENT10 GL1 Sharp OffTarget Control"
date: 2026-05-11
status: NO_GO
tags: [breakthrough-wave-4, agent10, gl1, sharp-cutoff, off-target, principal-value, smoothing, filtering, no-go]
---

## Verdict

No sharp GL1 theorem is proved.

The target is independent of EC H1 in form, but the available packets do not
prove its arithmetic input. The sharp cutoff leaves the harmonic coefficient

```text
1 / ((lambda-rho)L'(lambda,chi)).
```

That weight is exactly critical at Perron height. Smooth or filtered kernels
can create a separate smoothed theorem mode, but transferring back to the
sharp cutoff requires a uniform estimate for the missing sharp tail. That
uniform estimate is the same `GL1-Sharp-OffTarget-Control` target, not a
consequence of smoothing.

Decision:

```text
local target residue algebra: closed
deterministic finite-box wrapper: closed conditionally
sharp off-target PV aggregate: not proved
smoothed/filtering transfer to sharp cutoff: no-go without the same missing PV
GL1 theorem candidate independent of EC H1: conditional only
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

The target residue is local algebra:

```text
Res_{w=0} F_K(w)
  = u/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2).
```

For a simple off-target zero

```text
lambda = 1/2 + i gamma,
alpha_lambda = gamma - t,
```

the sharp off-target residue is

```text
R_lambda(u)
  = exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi)).
```

The sharp principal-value target is therefore:

```text
GL1-Sharp-OffTarget-Control(chi,rho):
  for legal zero-avoiding Perron heights T(e^u),

  Z_GL1(u,T(e^u))
    = sum_{lambda != rho, 0 < |alpha_lambda| <= T(e^u)}
        exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi))
    = o(u).
```

The dyadic moving form needed by the finite-box wrapper is:

```text
B_j^GL1(U)
  = sup_{u in [U,2U]}
      |sum_{2^j < |alpha_lambda| <= 2^(j+1)}
          exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi))|,

sum_{2^j <= T(e^(2U))} B_j^GL1(U) = o(U).
```

Together with same-height rectangle/truncation control and off-target Laurent
boundary control, this would give:

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

This theorem target is GL1-specific. It does not require EC H1, but it still
requires its own fixed target-shifted PV theorem.

## Source Anchors

Read first, as requested:

```text
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT09_GL1_SHARP_OFFTARGET_CONTROL_2026-05-11.md
primes-equispaced/handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
primes-equispaced/L2_facts/farey-current-state.md
primes-equispaced/L2_facts/farey-claim-ledger.md
```

Adjacent narrow checks used to avoid duplicating stale conclusions:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT10_GL1_H1_ACTUAL_PV_COUPLING_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT07_GL1_MOVING_OFFTARGET_PV_2026-05-11.md
primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/GL1_SMOOTHING_BYPASS_2026-05-11.md
```

Ledger state used:

```text
Top-10 GL1 update:
  H1 DPMV/PV progress does not prove sharp GL1 off-target control.

GL1/H1 Wave 3 PV coupling:
  one deterministic wrapper exists, but GL1 and H1 coefficient hypotheses
  remain separate.

GL(1) smoothing/filtering continuation:
  smoothed kernels give a separate theorem mode; finite filters kill finite
  residues only; no sharp transfer without uniform off-target estimates.
```

No new external theorem claim is introduced.

## Proof Attempt

### Attempt 1: finite-box closure

The contour identity has the right shape. After extracting the target residue,
the sharp finite-box formula can be written schematically as

```text
c_K(chi,rho)
  = Res_{w=0} F_K(w)
    + Z_GL1(u,T)
    + Z_Laurent,off(u,T)
    + Z_triv(u,T)
    + C_rect(u,T).
```

If all crossed off-target zeros are simple, or if the higher Laurent terms are
separately retained or shown to be `o(u)`, then `Z_Laurent,off` reduces to the
simple-zero sum `Z_GL1`. If

```text
Z_GL1(u,T(e^u)) = o(u)
```

and the same height gives

```text
Z_triv(u,T(e^u)) + C_rect(u,T(e^u)) = o(u),
```

then the target theorem follows immediately:

```text
c_K(chi,rho) = u/L'(rho,chi) + o(u).
```

This proves only the conditional wrapper. It does not estimate `Z_GL1`.

### Attempt 2: absolute domination

Let

```text
R_chi,rho(T)
  = sum_{T < |alpha_lambda| <= 2T}
      |L'(lambda,chi)|^(-1).
```

The sharp harmonic coefficient gives the absolute shell bound

```text
B_j^GL1(U) <= 2^(-j) R_chi,rho(2^j).
```

So an absolute route would close from

```text
sum_{2^j <= T(e^(2U))} 2^(-j) R_chi,rho(2^j) = o(U).       (GL1-ABS)
```

This is a critical weighted reciprocal-derivative theorem. It is not supplied
by the anchors.

Why this is critical:

```text
R_chi,rho(T) << T^(1+delta)
```

would give a divergent dyadic sum at Perron heights. Even

```text
R_chi,rho(T) = O(T)
```

gives only `O(log T(e^(2U)))`, which is `O(U)` for sharp Perron heights, not
`o(U)`. The absolute route needs a genuine average saving such as dyadic
Cesaro `R_chi,rho(T)=o(T)` strong enough along the whole legal height range,
or a log-saving summable variant.

That would be a GL1 theorem candidate independent of EC H1:

```text
GL1-CriticalWeightedReciprocalDerivative(chi,rho):
  sum_{2^j <= T(e^(2U))} 2^(-j) R_chi,rho(2^j) = o(U).
```

But this is a new hypothesis, not a proved consequence of the current source
anchors.

### Attempt 3: direct principal value cancellation

The direct route would prove cancellation in the actual weighted exponential
sum:

```text
sum_{0 < |alpha_lambda| <= T(e^u)}
  exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi)) = o(u).
```

The anchors do not contain a theorem forcing this cancellation from spacing,
symmetry, square moments, linear independence, or fixed-u convergence. Those
features are too weak. The test model is

```text
alpha_n = n,
b_n = b_{-n} = 1/(2n),
S_T(u) = sum_{1 <= n <= T} cos(nu)/n.
```

It has clean spacing, conjugation symmetry, and square-summable shell
coefficients. But every large interval `[U,2U]` contains resonant values of
`u` modulo `2*pi`, and there

```text
S_T(u) = log T + O(1).
```

For sharp Perron heights such as

```text
T_K = K/(log K)^B,
```

this is

```text
log T_K = log K - B log log K,
```

not `o(log K)`. Thus any proof using only those abstract PV features would
prove a false statement in the harmonic model.

The actual Dirichlet zero ordinates and actual residues may have extra
arithmetic structure. No read anchor converts that structure into the needed
uniform moving PV bound.

### Attempt 4: smoothing transfer

For a target-normalized smooth cutoff,

```text
F_{W,K}(w) = K^w W_hat(w)/L(rho+w,chi),
W_hat(w) = 1/w + kappa_W + O(w)
```

near `w=0`. The target residue stays leading:

```text
Res_{w=0} F_{W,K}(w)
  = log K/L'(rho,chi)
    + kappa_W/L'(rho,chi)
    - L''(rho,chi)/(2L'(rho,chi)^2).
```

Smoothing helps because `W_hat` may decay faster on vertical lines and may
vanish at chosen off-target points. For fixed `W`, a conditional theorem is
valid:

```text
SmoothOffTargetControl(W;chi,rho)
  => c_{W,K}(chi,rho) = log K/L'(rho,chi) + o(log K).
```

To transfer this to the sharp cutoff, take a family `W_eta` with
`W_hat_eta(w) -> 1/w`. The difference between smoothed and sharp off-target
sums is

```text
Delta_eta(u,T)
  = sum_{lambda != rho, 0 < |alpha_lambda| <= T}
      exp(i alpha_lambda u)
      (W_hat_eta(i alpha_lambda) - 1/(i alpha_lambda))
      / L'(lambda,chi).
```

A sharp transfer would need

```text
sup_{u in [U,2U]} |Delta_eta(u,T(e^u))| = o(U)
```

with constants uniform enough to let `eta -> 0` on the Perron scale.

But for any ordinary smoothing approximation, `W_hat_eta(i alpha)` agrees
with `1/(i alpha)` only on bounded or moderately bounded vertical ranges and
then decays or oscillates differently. The missed transition/tail is a sharp
harmonic sum over a growing band:

```text
sum_{eta^(-1) < |alpha_lambda| <= T(e^u)}
  exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi)),
```

up to harmless local weights. Bounding this uniformly by `o(U)` is exactly a
tail version of `GL1-Sharp-OffTarget-Control` or `GL1-ABS`.

So smoothing does not transfer because the limiting operation is not
uniform at the harmonic weight. The constants that make fixed smooth kernels
safe are allowed to blow as the kernel approaches the step function, and
controlling that blow-up is the missing sharp theorem.

### Attempt 5: finite and infinite filtering

Finite filtering can impose

```text
W_hat^(a)(lambda-rho)=0
```

for finitely many off-target zeros and finitely many derivative orders. This
kills or lowers those finite residues. It does not touch the infinite tail
unless a separate tail theorem is added.

Filtering every off-target zero is not available in the compact smooth cutoff
class. After removing the target pole, `w W_hat(w)` is an entire function of
finite exponential type for compact log-support kernels, while the Dirichlet
zero ordinate set has counting scale `T log T`. A nonzero finite-type entire
function cannot generally vanish on that full set with the required
multipities without degenerating.

Noncompact bespoke filters would be a different theorem. They would require a
new construction proving admissibility, inverse Mellin control, vertical-strip
decay, the target pole residue, and a fixed zero set independent of `K`. Even
then the result would be a filtered coefficient theorem, not the original
sharp `c_K`.

## Transfer Failure or Closure

Closure is available only under a new GL1-specific input:

```text
GL1-ActualMovingShellPV(chi,rho)
```

or the stronger absolute substitute:

```text
GL1-CriticalWeightedReciprocalDerivative(chi,rho).
```

With either input, plus same-height rectangle/truncation control and
off-target Laurent boundary control, the sharp theorem follows from the
finite-box identity and is independent of EC H1.

Without such an input, smoothing/filtering cannot be transferred to the sharp
cutoff. Exact failure point:

```text
fixed smooth W:
  added Mellin decay/zeros control a different coefficient c_{W,K};

sharp W=1_{0<t<=1}:
  W_hat(w)=1/w has no off-target zeros and only harmonic decay;

limit W_eta -> sharp:
  requires uniform control of Delta_eta over the high vertical transition
  band, which is the same sharp harmonic PV tail.
```

Therefore the attempted proof is circular if it uses smoothing to reach the
sharp cutoff. It assumes precisely the off-target estimate it was supposed to
prove.

## Dependency Impact

No theorem is promoted.

Dependency state:

```text
EC H1:
  not needed for the GL1 target, and no H1 result is imported.

GL1 sharp:
  remains conditional on GL1-ActualMovingShellPV or GL1-ABS, plus rectangle
  and Laurent-boundary hypotheses.

GL1 smoothing/filtering:
  remains a valid separate conditional theorem mode for c_{W,K}; cannot be
  cited for sharp c_K without a uniform sharp-tail theorem.

Koyama/e^{-gamma} product limit:
  still cannot be promoted from the current packets, because the coefficient
  side c_K(chi,rho)=logK/L'(rho,chi)+o(logK) is not closed.
```

Next admissible theorem-shaped target:

```text
Prove, source, or explicitly assume

  sum_{2^j <= T(e^(2U))} 2^(-j)
    sum_{2^j < |gamma_lambda-t| <= 2^(j+1)}
      |L'(lambda,chi)|^(-1)
  = o(U),

or prove the corresponding actual moving PV cancellation directly.
```
