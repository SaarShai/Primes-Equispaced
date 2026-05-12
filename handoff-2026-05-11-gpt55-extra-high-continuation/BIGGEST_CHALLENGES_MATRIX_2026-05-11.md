---
schema_version: 1
title: "Biggest challenges matrix after GPT-5.5 continuation launch"
date: 2026-05-11
type: research-matrix
tier: working
status: CLAIM_SAFE_COORDINATOR_STATE
confidence: 0.86
sources:
  - HANDOFF.md
  - handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/WAVE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
tags: [koyama, gl1, ec-ndc, h1, h2, obstruction-matrix]
---

# Biggest challenges matrix

No theorem is promoted here. This file records the coordinator state at the
launch of the 2026-05-11 GPT-5.5 xhigh continuation wave.

## P0: GL(1) shifted Perron off-target residues

Current safe result:

```text
local target-zero Perron residue is algebraically stable.
AK-side product constant has the e^{-gamma} normalization under AK/DRH input.
```

Missing theorem:

```text
For primitive nonprincipal chi and target zero rho, control the nonlocal
residue aggregate for

  F_K(w) = K^w / (w L(rho+w,chi))

so that all off-target residues plus rectangle/truncation errors are o(log K).
```

Sufficient claim-safe package:

```text
all crossed off-target zeros are simple;
Z_simple(K,T_K) = o(log K);
shifted rectangle/truncation terms are o(log K).
```

Stronger package:

```text
all higher-order off-target Laurent residues are explicitly bounded or retained
in a profile theorem, with total contribution o(log K) for the pointwise limit.
```

Closed/invalid shortcuts:

- Target-zero simplicity alone.
- Citing Inoue/Soundararajan-style explicit formulas as if they remove the
  off-target aggregate.
- Stating `D_K -> e^{-gamma}` as proved before this theorem closes.

Useful next output:

```text
Theorem P-GL1, conditional version:
  If OffTargetResidueControl(chi,rho) holds, then
  c_K(chi,rho) = log K/L'(rho,chi) + O(1) + o(log K),
  hence c_K E_K -> e^{-gamma} under the AK/DRH input.
```

Smoothed bypass mode:

```text
handoff-2026-05-11-gpt55-extra-high-continuation/GL1_SMOOTHING_BYPASS_2026-05-11.md
```

For a target-normalized smooth kernel with

```text
W_hat(w)=1/w+kappa_W+O(w),
```

the target residue remains `log K/L' + O(1)`. If `W_hat` vanishes to order
`h` at `lambda-rho`, an off-target zero of multiplicity `m` contributes only
degree `m-h-1` in `log K`; if `h>=m`, it is killed. Finite signed smooth
filtering can kill any prescribed finite off-target set. This gives a
claim-safe smoothed/profile theorem mode for `c_{W,K}`, but it does not transfer
back to the sharp cutoff without exactly the uniform estimates currently
missing.

Literature state:

```text
handoff-2026-05-11-gpt55-extra-high-continuation/LITERATURE_INPUTS_THEOREM_SOURCE_NOTE_2026-05-11.md
```

maps Aoki-Koyama to the product constant, Inoue/Soundararajan to negative
explicit-formula context, and finds no source closing the sharp shifted
nonlocal remainder.

## P0: EC H1 reciprocal-pole control

Current safe result:

```text
central H1 algebra gives the leading central polynomial, with top coefficient
proportional to (log K)^r/L^{(r)}(E,1).
```

The obstruction is not H2-style branch damping. H1 has reciprocal poles:

```text
offcentral simple zero contribution:
  K^(i gamma) W_hat(i gamma) / L'(E,1+i gamma)
```

No `1/log K` saving appears automatically.

Named theorem inputs:

```text
H1-shell-moment(E,delta):
  J_E,2(T) = sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^{-2}
             <= C_E T^(3-delta)
```

for the current smoothstep-scale decay `q=2`; or

```text
H1-fixed-weight-PV(E,W,r):
  the fixed weight sum
    sum W_hat(i gamma) e^(i gamma u)/L'(E,1+i gamma)
  has uniform cancellation Z_PV(u)=o(u^r) in the required windows.
```

The PV route is now packaged in
`handoff-2026-05-11-h1-shell-moment-wave/H1_FIXED_WEIGHT_PV_NOGO_CONDITIONAL_2026-05-11.md`:

```text
for r>=1, H1-fixed-weight-PV plus contour tails and multiple-zero handling
implies c_E,W(e^u)=Q_E,W(u)+o(u^r);
for r=0, the safe output is Q_0+Z_PV(u)+I_PV(u), not a constant limit.
```

Contour tail status, updated by
`handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md`:

```text
H-left: closed if the shifted line uses eta > 1/2.
H-height: source-routed/proof-candidate via Li-Zaharescu selected heights:
  sup |1/L| <= exp(A log T/loglog T)=T^o(1),
  enough for q=2 horizontal contour decay after EC normalization/reflection.
  Verification status: PARTIAL, conditional on normalized EC/newform
  RH/no-right-half-zero; not unconditional.
```

Closed/invalid shortcuts:

- Direct Li-Zaharescu/mollifier transfer to fixed H1 weights.
- Generic Cartan/Jensen as a proof of `A_TC<2`.
- Spacing plus square moments as pointwise PV closure.
  The model `sum cos(nu)/n` has perfect spacing and strong `l^2` shell bounds
  but diverges at resonant `u`, so this implication is logically false.

Remaining verification caveat:

```text
The adversarial source check confirms EC/newform normalization, strip coverage,
moving-box horizontal-tail compatibility, and gamma-factor reflection, but also
finds the LZ proof uses a no-right-half-zero hypothesis. Even when assumed,
this closes only horizontal contour height, not H1 residues/PV.
```

Useful next output:

```text
Either prove H1-shell-moment(E,delta), prove H1-fixed-weight-PV(E,W,r), or
state the EC theorem only as profile/product-average with the zero series
retained.
```

## P1: EC H2/Sym2 endpoint-smoothed closure

Current safe result:

```text
log P_E,W(K)
 = S_1,W(K) + (1/2)S_sym,W(K) - (1/2)M_good,W(K)
   + R_ge3,W(K) + B_bad,E,W(K).
```

Promotable H2 requires all local factors above, analytic rank
`r=ord_{s=1}L(E,s)`, and one declared theorem mode.

Pointwise target:

```text
log P_E,W(K) = -r log log K + B_E,W + o(1).
```

Safer target if zero terms persist:

```text
log P_E,W(K)
 = -r log log K + B_E,W + Z_E,W(log K) + o(1),
```

or a log-Cesaro/dyadic averaged theorem.

Main proof fork:

```text
derive the endpoint-smoothed explicit formula for
  S_1,W(K) = sum_p W(p/K) a_p/p
and decide whether offcentral branch terms are O(1/log K), persistent, or only
average-removable.
```

Closed/invalid shortcuts:

- "Sheth proves H2" without exact local-factor and pointwise transfer.
- Composing H2 with H1 as if H1 also gained branch damping.
- Replacing analytic rank by algebraic rank without BSD/rank verification.

## P1: EC rank-zero theorem mode

Current safe package:

```text
handoff-2026-05-11-gpt55-extra-high-continuation/RANKZERO_PROFILE_PACKAGE_2026-05-11.md
```

Rank-zero should not be forced into pointwise constant stabilization. The H1
profile has main scale

```text
c_E,W(e^u) = q_0 + Z_c(u) + o(1),
q_0 = w_(-1)/L(E,1),
a_gamma = W_hat(i gamma)/L'(E,1+i gamma).
```

Claim-safe consequence:

```text
If Z_c has any retained nonzero almost-periodic frequency, a pointwise constant
limit is impossible without coefficient death, kernel killing with tail control,
subtraction, or averaging.
```

Product-average mode:

```text
A_U(c_E,W P_E,W)
 -> exp(B_H2)(q_0 d_0 + sum_gamma a_gamma d_(-gamma))
```

under H1/H2 profile hypotheses and joint tail extraction. In the nonoscillatory
H2 special case and normalized kernel, this reduces to

```text
exp(B_H2)/L(E,1).
```

This is paper-shaped as a conditional/profile section, not a fixed-curve
constant theorem.

## P1: EC numerical evidence

Current safe result:

```text
smoothed finite proxy through K <= 1000000 is reproducible on the three-curve
grid, but many ablations pass the old gate.
```

Null-control update:

```text
handoff-2026-05-11-gpt55-extra-high-continuation/EC_NULL_CONTROL_GATES_2026-05-11.md
status: NO_GO
first failing gate: G2_primary_alpha_null_rejection
```

At the predeclared primary `all, alpha=0.75`:

```text
ratio = 1.3473754929960748,
max CV = 0.063297427334436704.
```

But predeclared nulls `cP_only`, `P_only`, and `PL2_only` also pass at
`alpha=0.75`; the best null `cP_only` is only
`7.97e-05` worse by the score metric, far below the required `0.01`
load-bearing margin.

Negative result:

```text
finite bad-prime factors are per-curve constants on the tested grid and cannot
fix within-curve CV failures for the sharp-cutoff class.
```

Promotable numerical next step:

```text
predeclared holdout curves,
larger/denser K grid,
kernel/null controls,
and ablation gates showing the proposed factor is load-bearing.
```

Until then:

```text
finite smoothing is a mechanism lead, not BSD or L(E,2) evidence.
The old smoothstep gate is failed as a load-bearing normalization gate.
```

## P1: Koyama correspondence

Current state:

```text
handoff-2026-05-09-followup/Koyama_email_to_Koyama_claimsafe_draft_2026-05-11.md
```

was source-anchored in this continuation pass. It now cites the AK p.235
formula anchor and keeps the Perron-leading step conditional.

Do not send without explicit user approval.

Best question to Koyama:

```text
Is there a theorem in the AK/DRH or explicit-formula framework that controls
the shifted off-target residue aggregate for K^w/(w L(rho+w,chi)) at o(log K)?
```

## Secondary blockers

Path B:

```text
GP/PARI controls are still externally blocked; current local data are a
failure-to-promote diagnostic, not a total theorem-level falsification.
```

DPAC:

```text
finite phase avoidance is a claim-safe analytic proof sketch only; no
Lean-verified theorem and no zeta-zero ordinate bridge.
```

Paper B/B+:

```text
B+ positivity is false in the Lean-canonical definition. The remaining useful
program is sign-cluster classification.
```
