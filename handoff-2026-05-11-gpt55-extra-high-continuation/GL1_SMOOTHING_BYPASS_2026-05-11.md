---
schema_version: 1
title: "GL1 smoothing bypass and finite zero filtering"
date: 2026-05-11
agent: "GL1-Smoothing-Bypass"
type: theorem-reduction
tier: claim-safe
status: FINITE_FILTER_THEOREM_CONDITIONAL_SMOOTHED_LEADING
confidence: 0.86
sources:
  - handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
  - handoff-2026-05-11-gpt55-wave/GL1_PERRON_CLOSURE_PATH_2026-05-11.md
  - handoff-2026-05-11-gpt55-extra-high-continuation/BIGGEST_CHALLENGES_MATRIX_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
tags: [gl1, perron, smoothing, kernel-filtering, off-target-residues]
---

# GL1 Smoothing Bypass And Finite Zero Filtering

## Verdict

Smoothing gives a claim-safe GL1 theorem mode, but not an unconditional
sharp-cutoff bypass.

Promote:

```text
1. Exact smoothed Perron profile:
   target residue + explicit off-target residue profile + contour errors.

2. Finite signed kernel filtering:
   a compact smooth target-normalized cutoff can kill any prescribed finite
   set of off-target residues, with declared multiplicity orders.

3. Conditional smoothed leading theorem:
   if the remaining smoothed residue tail and contour errors are o(log K),
   then c_{W,K}(chi,rho) = log K/L'(rho,chi) + o(log K).
```

Do not promote:

```text
finite filtering => asymptotic constant;
ordinary smoothing => all off-target residues vanish;
smoothed theorem => original sharp-cutoff theorem.
```

For the fixed sharp cutoff, the old obstruction remains exactly: the Mellin
kernel `1/w` has no zeros at off-target points and only `1/|t|` vertical
decay, so off-target multiple zeros are unsuppressed and the simple-zero
aggregate is still the missing theorem.

## Notation

Let `chi` be primitive nonprincipal. Let `rho` be a simple noncentral zero of
`L(s,chi)`. For a cutoff `W`, define

```text
W_hat(w) = int_0^infty W(t) t^(w-1) dt,
c_{W,K}(chi,rho)
  = sum_{n>=1} mu(n) chi(n) n^(-rho) W(n/K).
```

The useful cutoff class is target-normalized:

```text
W(t) = 1 near 0,
W has compact support or rapid decay at infinity,
W_hat(w) = 1/w + kappa_W + O(w) near w=0,
```

and `W_hat` has declared vertical decay on the shifted Perron strip. A
`C^infty` compact endpoint cutoff gives super-polynomial decay away from
`w=0`; the repository smoothstep-scale kernel gives only finite polynomial
decay, e.g. `q=2` in the local notes.

## Exact Smoothed GL1 Profile

Assume a legal shifted Perron rectangle for

```text
F_{W,K}(w) = K^w W_hat(w) / L(rho+w,chi),
```

with no zero or kernel pole on the boundary. Then the finite-box identity is

```text
c_{W,K}(chi,rho)
 = Res_{w=0} F_{W,K}(w)
   + Z_off,W(K,T)
   + Z_triv,W(K,T)
   + Z_kernel,W(K,T)
   + C_rect,W(K,T),
```

where `Z_kernel,W` is absent for target-normalized `C_c^infty` cutoffs whose
Mellin transform has no pole in the strip except `0`.

The target residue is closed algebra. Since `rho` is simple,

```text
Res_{w=0} F_{W,K}(w)
 = log K / L'(rho,chi)
   + kappa_W / L'(rho,chi)
   - L''(rho,chi)/(2 L'(rho,chi)^2).
```

Thus smoothing preserves the leading coefficient if and only if
`Res_{w=0} W_hat(w)=1`. It changes the subleading constant by
`kappa_W/L'(rho,chi)`.

## Off-Target Residue Algebra

Let `lambda != rho` be an off-target zero of multiplicity `m`. Put

```text
w_lambda = lambda - rho,
L(lambda+z,chi) = a_m z^m + a_{m+1} z^(m+1) + ...,
a_m = L^(m)(lambda,chi)/m! != 0.
```

Let `h_lambda` be the vanishing order of `W_hat` at `w_lambda`; if
`W_hat(w_lambda) != 0`, then `h_lambda=0`. Write

```text
W_hat(w_lambda+z) = eta_h z^h + O(z^(h+1)),
eta_h = W_hat^(h)(w_lambda)/h!.
```

If `h_lambda >= m`, the off-target residue is killed. If `h_lambda < m`, then

```text
Res_{w=w_lambda} F_{W,K}(w)
 = K^(w_lambda)
   { a_m^(-1) eta_h (log K)^(m-h_lambda-1)/(m-h_lambda-1)!
     + lower powers of log K }.
```

Consequences under DRH, where `Re(w_lambda)=0`:

```text
h_lambda = 0, m=1: bounded oscillatory simple residue.
h_lambda = 0, m=2: another log K-scale term.
h_lambda = 0, m>2: larger than the target log K scale.
h_lambda >= m-1: no log K-scale or larger term remains.
h_lambda >= m: the residue is exactly absent.
```

This is the precise way smoothing can help: zeros of `W_hat` lower the
effective degree of off-target Laurent residues.

## Finite-Zero Filtered Theorem

Let `Lambda_0` be a finite set of off-target zeros. Assign each
`lambda in Lambda_0` an integer `r_lambda >= 1`; to kill its residue take
`r_lambda >= m_lambda`, and to remove only log-scale obstruction take
`r_lambda >= m_lambda-1`.

There exists a signed target-normalized `C_c^infty` cutoff `W` such that

```text
W_hat^(a)(lambda-rho) = 0
for every lambda in Lambda_0 and 0 <= a < r_lambda.
```

Construction sketch: start from a target-normalized smooth cutoff `W_0`. Add
finitely many signed smooth bumps supported in the transition region away from
`0`. The constraints above are finite linear Mellin-moment constraints. For
generic bump centers and enough bumps, the confluent exponential moment matrix
is invertible; solve the finite linear system. The perturbation does not change
the pole `W_hat(w)=1/w+...` at `w=0`.

Then the finite-box identity above holds with the chosen finite residues
deleted or degree-lowered exactly as prescribed.

Claim-safe filtered profile:

```text
c_{W,K}(chi,rho)
 = log K/L'(rho,chi)
   + C_target(W,rho,chi)
   + Z_tail,W,Lambda_0(K)
   + C_rect,W(K),
```

where `Z_tail,W,Lambda_0` omits the killed terms and contains every unfiltered
off-target residue explicitly.

This is a theorem profile, not a pointwise limit theorem, until the tail is
controlled.

## Conditional Smoothed Leading Theorem

Define `SmoothOffTargetControl(W;chi,rho)` to mean that there are legal heights
`T_K -> infinity` such that, after the target residue is extracted,

```text
Z_off,W(K,T_K)
+ Z_triv,W(K,T_K)
+ Z_kernel,W(K,T_K)
+ C_rect,W(K,T_K)
= o(log K).
```

Equivalently, all unfiltered effective residue polynomials and all contour
terms are collectively lower than the target `log K` scale.

Then:

```text
Theorem GL1-smoothed-leading.
Assume rho is simple, W is target-normalized and Perron-admissible, and
SmoothOffTargetControl(W;chi,rho) holds. Then

  c_{W,K}(chi,rho)
    = log K/L'(rho,chi) + o(log K).

If, in addition, the Aoki-Koyama product input gives
  E_K(chi,rho) log K -> L'(rho,chi)/e^gamma,
then the smoothed coefficient/product limit is
  c_{W,K}(chi,rho) E_K(chi,rho) -> e^(-gamma).
```

Stronger subleading versions require replacing the `o(log K)` control by
`o(1)` after retaining any bounded almost-periodic zero profile.

## What Smoothing Does Not Prove

Finite filtering does not control the infinite tail. If an unfiltered double
off-target zero exists on the critical line, it still contributes at `log K`
scale unless `W_hat(lambda-rho)=0`. If an unfiltered zero has multiplicity
`m`, a zero of order at least `m-1` is needed just to remove the leading-scale
obstruction.

For compact log-support kernels, all-zero filtering is structurally blocked.
After removing the pole at `0`, `w W_hat(w)` is an entire function of finite
exponential type. Such functions cannot generally vanish on the full
Dirichlet zero ordinate set, whose counting scale is `T log T`, unless the
kernel degenerates. Thus a nonzero compactly supported fixed cutoff cannot
be expected to kill every off-target zero.

For Schwartz/log-Schwartz bespoke filters, the finite-type obstruction may
disappear, but the result is no longer an ordinary fixed compact smoothing
theorem. One would need a new construction proving:

```text
1. W_hat has the required infinite zero set with multiplicity;
2. W_hat keeps the target pole at 0 with residue 1;
3. W_hat has enough vertical-strip decay for the same Perron contour;
4. the inverse Mellin kernel is admissible for the arithmetic sum;
5. the construction is fixed before looking at K and has controlled constants.
```

No such source-closed theorem is present in the repo notes.

## Fixed Sharp Cutoff: What Remains Impossible

For `W=1_{0<t<=1}`,

```text
W_hat(w)=1/w.
```

Therefore:

```text
1. No off-target zero can be kernel-cancelled, since 1/(lambda-rho) != 0.
2. Multiple off-target zeros retain the full degree m-1 polynomial in log K.
3. The vertical decay is only 1/|t|, so high-zero and horizontal-edge control
   is harder than for smooth cutoffs.
4. The needed simple-zero theorem remains exactly
   Z_simple(K,T_K)=o(log K), plus rectangle/truncation control.
5. A smoothed finite-filter theorem does not transfer back to the sharp cutoff
   without uniform estimates as W approaches the step function; those estimates
   are precisely the missing sharp residue theorem.
```

Thus the fixed sharp-cutoff Perron theorem is still blocked. Smoothing gives a
valid new theorem mode for `c_{W,K}`, and finite filtering gives a diagnostic
or profile theorem, but neither proves the original `c_K` asymptotic.

## Best Next Use

Use the finite-filtered theorem as a microscope:

```text
choose the first J off-target zeros,
construct a signed W_J with declared Mellin zeros,
compare c_{W_J,K} against the unfiltered smoothed c_{W,K},
track whether the remaining tail is O(1), o(log K), or still main-scale.
```

The theorem statement should always retain the tail unless a separate
residue-control theorem closes it.
