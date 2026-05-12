---
schema_version: 1
title: "Agent 09 - GL1 Sharp Off-Target Control"
date: 2026-05-11
agent: "Top-10 Challenge Wave Agent 09"
type: theorem-attempt
tier: working
status: NO_GO
confidence: 0.89
sources:
  - ../start.md
  - HANDOFF.md
  - L0_rules.md
  - L1_index.md
  - handoff-2026-05-11-breakthrough-wave-3/AGENT10_GL1_H1_ACTUAL_PV_COUPLING_2026-05-11.md
  - handoff-2026-05-11-breakthrough-wave-2/AGENT07_GL1_MOVING_OFFTARGET_PV_2026-05-11.md
  - handoff-2026-05-11-breakthrough-wave/AGENT06_GL1_SHIFTED_PERRON_OFFTARGET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
  - handoff-2026-05-11-gpt55-extra-high-continuation/GL1_SMOOTHING_BYPASS_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/GL1_PERRON_CLOSURE_PATH_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT03_GL2_DPMV_SOURCE_CLOSURE_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT06_H1_ACTUAL_DYADIC_SHELL_PV_2026-05-11.md
  - https://arxiv.org/abs/2310.03949
  - https://arxiv.org/abs/1306.0854
tags: [top10-challenge, agent09, gl1, sharp-cutoff, perron, off-target, dpmv, no-go]
---

# Agent 09 - GL1 Sharp Off-Target Control

status: `NO_GO`

## Verdict

H1 DPMV/PV ideas do not transfer to the GL1 sharp cutoff as a theorem.

The only transfer is the deterministic wrapper from Agent 10:

```text
actual moving shell PV + same-height rectangle tails + Laurent boundary
  => leading term.
```

The arithmetic input does not transfer.  GL1 sharp has the target-dependent
critical coefficient

```text
b_lambda(chi,rho)
  = 1 / ((lambda-rho)L'(lambda,chi)).
```

Under the critical-line mode, with `rho=1/2+it`,
`lambda=1/2+i gamma`, and `alpha=gamma-t`, this is

```text
b_lambda = 1 / (i alpha L'(lambda,chi)).
```

That `1/alpha` factor is harmonic, not smoothing.  It creates a separate
critical-weight problem.  H1's useful absolute route uses smooth Mellin decay
`|W_hat(i gamma)| << |gamma|^(-q)`, with the current legal H1 packets using
`q=2`.  The GL1 sharp kernel has only `q=1`, and the target scale is only
`U=log K`.

Decision:

```text
H1 abstract shell wrapper: transfers.
H1 direct PV theorem: not proved and does not transfer.
H1 DPMV absolute-domination route: does not transfer to sharp GL1.
GL1 sharp theorem: still conditional on its own actual moving off-target PV
  or a stronger target-shifted weighted reciprocal-derivative theorem.
```

No sharp GL1 theorem is promoted.

## Sharp GL1 Target

Let `chi` be primitive nonprincipal and let `rho=1/2+it` be a simple
noncentral zero.  For

```text
F_K(w) = K^w / (w L(rho+w,chi)),
u = log K,
```

the target residue is local algebra:

```text
Res_(w=0) F_K(w)
  = u/L'(rho,chi) - L''(rho,chi)/(2L'(rho,chi)^2).
```

After extracting this residue, the simple off-target sum at legal Perron
height `T(e^u)` is

```text
Z_GL1(u,T)
 = sum_(lambda != rho, 0<|gamma_lambda-t|<=T)
     exp(i(gamma_lambda-t)u)
     / (i(gamma_lambda-t)L'(lambda,chi)).
```

The missing moving theorem is

```text
GL1-ActualMovingShellPV(chi,rho):
  sup_(u in [U,2U]) |Z_GL1(u,T(e^u))| = o(U)
```

on the same legal heights as the rectangle.  Dyadically, with

```text
B_j^GL1(U)
 = sup_(u in [U,2U])
   | sum_(2^j < |gamma_lambda-t| <= 2^(j+1))
       exp(i(gamma_lambda-t)u)
       / (i(gamma_lambda-t)L'(lambda,chi)) |,
```

the required input is

```text
sum_(2^j <= T(e^(2U))) B_j^GL1(U) = o(U).
```

This is exactly the unsourced sharp fixed-weight PV theorem, not a consequence
of the H1 DPMV packets.

## Absolute Route Test

The H1 top-10 packet separates two routes:

```text
direct PV:
  prove moving-window cancellation for the actual coefficients;

absolute route:
  dominate every shell by the l1 reciprocal-derivative mass.
```

For H1,

```text
a_gamma(E,W) = W_hat(i gamma) / L'(E,1+i gamma),
A_j^H1 <= 2^(-qj) R_E,1(2^j).
```

With `q=2`, the rank-one sufficient target is

```text
R_E,1(T) = o(T^2).
```

That is why BFMT/DPMV-style separated-zero progress could still matter for
H1 after the independent bad-set budget is supplied.

For GL1 sharp, the analogous absolute shell bound is

```text
A_j^GL1 <= 2^(-j) R_chi,rho(2^j),

R_chi,rho(T)
 = sum_(T < |gamma_lambda-t| <= 2T)
     |L'(lambda,chi)|^(-1).
```

Thus absolute domination would need

```text
sum_(2^j <= T(e^(2U))) 2^(-j) R_chi,rho(2^j) = o(U).        (GL1-ABS)
```

This is a critical-weight condition.  Even a BFMT-shaped estimate

```text
R_chi,rho(T) << T^(1+delta)
```

would give at best

```text
sum_(j<=J) 2^(delta j),
```

with `2^J` comparable to the sharp Perron height.  For Perron-scale heights
`T(e^U)` exponential in `U`, this does not imply `o(U)`.  Even a linear bound
`R_chi,rho(T)=O(T)` gives only `O(U)`, not the needed `o(U)`.  The absolute
GL1 route therefore needs a real average saving such as

```text
R_chi,rho(T) = o(T)
```

in dyadic Cesaro form, or a genuinely stronger weighted theorem.  No checked
DPMV source gives this.

## Direct PV Test

The direct PV route also does not transfer.

The coefficient model

```text
alpha_n = n,
b_n = b_(-n) = 1/(2n),
S_T(u) = sum_(1<=n<=T) cos(nu)/n
```

has spacing, symmetry, and square-summable coefficients.  At resonant `u`,

```text
S_T(u) = log T + O(1).
```

For sharp Perron heights `T_K=K/(log K)^B`, this is

```text
log T_K = log K - B loglog K,
```

not `o(log K)`.  Therefore spacing, conjugation symmetry, square moments,
fixed-u PV convergence, log-Cesaro cancellation, or profile convergence cannot
prove the moving sharp GL1 statement.  Any such proof would prove a false
statement in this model.

The actual Dirichlet zero ordinates and actual residues may have extra
structure.  The current packets and source checks do not provide a theorem
turning that structure into `GL1-ActualMovingShellPV`.

## Multiple-Zero Boundary

This no-go is independent of the multiple-zero obstruction.

If an off-target zero `lambda != rho` has multiplicity `m` and

```text
L(lambda+z,chi) = a_m z^m + ...,
```

then the sharp residue at `w=lambda-rho` has top term

```text
K^(lambda-rho) (log K)^(m-1)
---------------------------------------
(m-1)! (lambda-rho) a_m.
```

Under DRH there is no power saving in `K^(lambda-rho)`.  Hence:

```text
m=1: one bounded oscillatory term;
m=2: another log K-scale term;
m>2: larger than the target log K scale.
```

Global off-target simplicity removes only this Laurent-degree obstruction. It
still leaves the infinite simple-zero moving PV sum.

## Smoothing Boundary

Smoothing and finite filtering remain useful only as a different theorem mode.
For a target-normalized smooth cutoff,

```text
F_W(w) = K^w W_hat(w) / L(rho+w,chi),
W_hat(w) = 1/w + kappa_W + O(w),
```

zeros of `W_hat(lambda-rho)` can lower or kill finite off-target residues.
This does not prove the sharp cutoff because for the sharp step kernel

```text
W_hat(w) = 1/w,
```

there are no off-target Mellin zeros and only harmonic vertical decay.
Uniformly sending smooth cutoffs to the step kernel would require estimates
equivalent to the missing sharp off-target theorem.

## Source Check

External DPMV claims were checked by fresh `curl + pdftotext` in
`/tmp/farey-agent09-gl1-20260511`.

Commands:

```bash
curl -L --fail -sS -o bfmt_2310_03949.pdf https://arxiv.org/pdf/2310.03949
curl -L --fail -sS -o milinovich_ng_1306_0854.pdf https://arxiv.org/pdf/1306.0854
curl -L --fail --max-time 30 -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  bfmt_2310_03949.pdf bfmt_2310_03949.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  milinovich_ng_1306_0854.pdf milinovich_ng_1306_0854.txt
```

PDF hashes:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_2310_03949.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
```

Checked anchors:

```text
BFMT, arXiv:2310.03949, title:
  "Negative discrete moments of the derivative of the Riemann zeta-function".

BFMT Theorem 1.1, PDF p. 2, equation (1.2):
  negative moments over a separated zeta-zero subfamily, with
  k=1/2 giving T^(1+delta)-scale upper bound.

BFMT Theorem 3.1, PDF p. 8:
  zeta zero mean-square theorem for "any sequence of complex numbers".

Milinovich-Ng, arXiv:1306.0854, PDF p. 1 and p. 11:
  object is a normalized holomorphic newform L-function with critical line
  Re(s)=1/2.

Milinovich-Ng Proposition 4.1, PDF p. 19, equation (41):
  GL2 zero-discrete mean square for A(s), assuming coefficient conditions
  (39),(40), with extra Lambda_f*a terms.

Milinovich-Ng Proposition 4.3, PDF p. 19, equations (43),(44):
  prime-supported high moments only under the support condition x^m <= T^(2/3).
```

Source decision:

```text
BFMT: zeta DPMV source, not a GL1 Dirichlet shifted-Perron theorem.
Milinovich-Ng: GL2/newform source, not a GL1 Dirichlet shifted-Perron theorem.
Neither source proves GL1-ActualMovingShellPV or GL1-ABS.
```

## Final Boundary

Do not promote:

```text
H1 DPMV progress => GL1 sharp cutoff;
H1 direct PV ideas => GL1 actual moving shell PV;
BFMT/MN source-backed DPMV => GL1 critical weighted absolute bound;
global off-target simplicity => sharp leading term;
smoothed/filtering GL1 theorem => sharp c_K theorem.
```

Promotable future inputs:

```text
1. GL1-ActualMovingShellPV(chi,rho):
   the actual target-shifted moving shell sums are o(U);

2. GL1-CriticalWeightedReciprocalDerivative(chi,rho):
   sum_(2^j<=T(e^(2U))) 2^(-j)R_chi,rho(2^j)=o(U);

3. GL1-Sharp-Rectangle(chi,rho):
   the same legal heights also give trivial-residue, contour, endpoint, and
   Perron-truncation errors o(log K);

4. GL1-OffTargetLaurentBoundary(chi,rho):
   all multiple off-target residue polynomials are excluded, retained, or
   collectively o(log K).
```

With these, the existing conditional sharp theorem gives

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

Without them, GL1 sharp remains blocked.

## Protocol Check

Commands/checks used:

```text
./te doctor
./te wiki context "GL1 shifted Perron GL1-Sharp-OffTarget-Control GL1-ActualMovingShellPV"
sed/rg reads of required handoffs and GL1 shifted Perron packets
curl + xpdf pdftotext source checks for arXiv:2310.03949 and arXiv:1306.0854
git status --short on the assigned output path before writing
```

No Koyama correspondence or email draft was read or edited.

Changed file:

```text
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT09_GL1_SHARP_OFFTARGET_CONTROL_2026-05-11.md
```
