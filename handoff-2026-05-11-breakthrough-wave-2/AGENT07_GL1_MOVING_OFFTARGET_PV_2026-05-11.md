---
schema_version: 1
title: "Agent 07 - GL1 moving off-target PV"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 07 - GL1 Moving Off-Target PV"
type: theorem-reduction
tier: claim-safe
status: RIGOROUS_REDUCTION
confidence: 0.89
sources:
  - start.md
  - token-economy.yaml
  - L0_rules.md
  - L1_index.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT03_H1_ACTUAL_COEFFICIENT_MOVING_PV_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT06_GL1_SHIFTED_PERRON_OFFTARGET_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/GL1_SMOOTHING_BYPASS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
tags: [breakthrough-wave-2, agent07, gl1, perron, moving-pv, off-target, smoothing]
---

# Agent 07 - GL1 Moving Off-Target PV

status: `RIGOROUS_REDUCTION`

mode label: `SHARP_REDUCES_TO_ACTUAL_MOVING_PV_NO_SOURCE_CLOSURE`

## Verdict

The GL1 sharp cutoff theorem does not source-close from the current packets.

It reduces to one sharper input:

```text
GL1-ActualMovingShellPV(chi,rho):
  the actual off-target residue exponential sum, with coefficients
  1/((lambda-rho)L'(lambda,chi)), is o(log K) on the same moving
  Perron heights used by the sharp rectangle.
```

No GL1-specific structure in the read packets proves this input. The sharp
route is therefore:

```text
global off-target simplicity
+ GL1-ActualMovingShellPV
+ same-height rectangle/truncation control
  => sharp leading theorem;

current packets without that moving PV theorem
  => no sharp promotion; use conditional sharp wording or smoothed/filtering.
```

The GL1-specific advantage is real only after changing kernels. A smoothed
target-normalized kernel can add Mellin zeros and better vertical decay; the
fixed sharp kernel `1/w` has neither advantage.

## Sharp Moving Sum

Let `chi` be primitive nonprincipal and let

```text
rho = 1/2 + i t
```

be a simple noncentral target zero. Put

```text
u = log K,
F_K(w) = K^w/(w L(rho+w,chi)).
```

For a simple off-target zero `lambda != rho`, write under the critical-line
mode

```text
lambda = 1/2 + i gamma,
alpha_lambda = gamma - t.
```

The sharp residue is

```text
R_lambda(u)
  = exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi)).
```

After extracting the target residue

```text
Res_{w=0} F_K(w)
  = u/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2),
```

the needed simple-zero aggregate is

```text
Z_GL1(u,T)
 = sum_{lambda != rho, 0 < |alpha_lambda| <= T}
     exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi)).
```

The sharp theorem needs, for legal zero-avoiding heights `T(e^u)`,

```text
Z_GL1(u,T(e^u)) = o(u).
```

The dyadic uniform form that matches the H1 moving-window packets is:

```text
sup_{u in [U,2U]} |Z_GL1(u,T(e^u))| = o(U).
```

A checkable sufficient shell condition is:

```text
B_j^GL1(U)
 = sup_{u in [U,2U]}
   |sum_{2^j < |alpha_lambda| <= 2^(j+1)}
      exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi))|,

sum_{2^j <= T(e^(2U))} B_j^GL1(U) = o(U).
```

The finitely many very small nonzero `|alpha_lambda|` terms are harmless only
after the target is removed and those off-target zeros are simple; they
contribute `O(1)` fixed oscillations, not a proof for the high tail.

## Conditional Sharp Theorem Candidate

`GL1-sharp-leading-from-moving-PV`:

Assume:

```text
1. rho is simple and noncentral;
2. every crossed off-target nontrivial zero is simple, or every higher-order
   Laurent residue is separately o(log K);
3. GL1-ActualMovingShellPV(chi,rho) holds on the same legal heights;
4. trivial-zero residues, shifted vertical/horizontal integrals, endpoint
   terms, and Perron truncation are o(log K) for those heights.
```

Then:

```text
c_K(chi,rho)
  = log K/L'(rho,chi) + o(log K).
```

With the separate AK-side product input retained as an independent hypothesis,
this yields the corrected product limit:

```text
c_K(chi,rho) E_K(chi,rho) -> e^(-gamma).
```

This is a rigorous reduction, not a promoted theorem. Assumption 3 is the new
name for the missing theorem.

## Direct Comparison With H1 PV Obstruction

Wave 2 Agent 03 isolated the H1 actual-coefficient target:

```text
a_gamma(E,W) = W_hat(i gamma)/L'(E,1+i gamma),

sum_j sup_{u in [U,2U]}
 |sum_{2^j < |gamma| <= 2^(j+1)}
    a_gamma(E,W) exp(i gamma u)|
 = o(U^r).
```

The GL1 sharp target is the same moving exponential-sum problem with

```text
a_lambda^GL1 = 1/(i alpha_lambda L'(lambda,chi)),
target scale = U.
```

Thus GL1 does not escape the H1 obstruction. It specializes it.

The apparent GL1 advantage is the extra `1/alpha_lambda`. But for sharp Perron
heights the obstruction already has harmonic size. The model

```text
alpha_n = n,
a_n = a_(-n) = 1/(2n),
S_T(u) = sum_{1 <= n <= T} cos(nu)/n
```

has spacing, symmetric PV form, and square-summable coefficients, yet at
resonant `u` it has

```text
S_T(u) = log T + O(1).
```

For Perron-scale heights such as

```text
T_K = K/(log K)^B,
```

this is

```text
log T_K = log K - B log log K,
```

which is not `o(log K)`. Therefore a proof using only spacing, symmetric PV,
or coefficient `l2` control would prove a false statement in this model.

The actual Dirichlet zero ordinates and residues may have more structure than
the model. The read packets contain no theorem converting that structure into
the moving dyadic shell bound above.

## GL1-Specific Advantage Audit

Helpful but insufficient:

```text
1. A simple off-target zero is individually O(1), so global simplicity removes
   the higher-degree Laurent obstruction.
2. The coefficient has a natural 1/alpha_lambda factor.
3. The target residue is explicit and rank-one scale, log K.
```

Not enough:

```text
1. The sharp kernel is W_hat(w)=1/w, so it has no off-target zeros.
2. Its vertical decay is harmonic, exactly the scale of the resonance model.
3. Legal moving heights have log T comparable with log K in the sharp route.
4. Zero spacing, non-lattice language, LI heuristics, and square moments do
   not give a pointwise dyadic sup bound.
5. Reciprocal-derivative average information does not control the actual
   phases of 1/L'(lambda,chi) in the moving exponential sum.
```

Conclusion:

```text
GL1 has no source-closed sharp-cutoff advantage over H1 PV.
The only useful advantage is kernel-dependent smoothing/filtering, which
changes the theorem mode.
```

## Multiple-Zero Boundary

If an off-target zero `lambda` has multiplicity `m`, write

```text
L(lambda+z,chi) = a_m z^m + ...
```

Then the sharp residue at `w=lambda-rho` has top term

```text
K^(lambda-rho) (log K)^(m-1)
---------------------------------------
(m-1)! (lambda-rho) a_m.
```

Under the critical-line mode this has no power saving. Therefore:

```text
m = 1: bounded single oscillatory term;
m = 2: extra log K-scale oscillatory term;
m > 2: larger than the target log K scale.
```

The moving PV theorem above is only the simple-zero tail theorem. A sharp
cutoff statement must also assume global off-target simplicity or retain a
separate higher-order Laurent aggregate hypothesis.

## Smoothed Fallback Boundary

For a target-normalized Perron-admissible cutoff,

```text
W_hat(w) = 1/w + kappa_W + O(w),
F_{W,K}(w) = K^w W_hat(w)/L(rho+w,chi),
```

the target residue is

```text
Res_{w=0} F_{W,K}(w)
  = log K/L'(rho,chi)
    + kappa_W/L'(rho,chi)
    - L''(rho,chi)/(2 L'(rho,chi)^2).
```

If `W_hat` vanishes to order `h` at `lambda-rho`, an off-target zero of
multiplicity `m` has effective degree

```text
m - h - 1
```

in `log K`; if `h >= m`, that residue is killed. Hence finite signed filtering
can delete any prescribed finite off-target set, but the unfiltered infinite
tail must remain explicit.

Claim-safe fallback:

```text
Assume rho is simple, W is target-normalized and Perron-admissible, and
SmoothOffTargetControl(W;chi,rho) holds:

  Z_off,W + Z_triv,W + Z_kernel,W + C_rect,W = o(log K)

on legal heights. Then

  c_{W,K}(chi,rho) = log K/L'(rho,chi) + o(log K).
```

This is a theorem mode for `c_{W,K}`, not for the original sharp `c_K`.
Transferring it to `W=1_(0,1]` requires uniform estimates as `W` approaches
the step kernel, which is another form of the missing sharp moving PV theorem.

## Decision Table

| Input | Sharp result | Status |
|---|---|---|
| Target local residue only | local `log K/L'(rho,chi)` term | `INSUFFICIENT` |
| Target zero simple only | off-target zeros uncontrolled | `NO_GO` |
| All off-target zeros simple | removes Laurent degree obstruction | `HELPFUL_NOT_ENOUGH` |
| Spacing/l2/symmetric PV | fails against harmonic moving model | `NO_GO` |
| Actual GL1 moving shell PV + rectangle control | sharp leading theorem | `CONDITIONAL` |
| Smoothed target-normalized kernel + smooth tail control | smoothed leading theorem | `CONDITIONAL_SMOOTHED` |
| Finite signed filtering | finite residues killed, tail retained | `PROFILE_THEOREM` |

## Source Closure

No new external theorem claim is introduced here.

Read packets already source-audited the local Perron residue algebra and the
absence of a checked sharp off-target aggregate theorem in the current
dependency set. This packet uses those internal source-audited results and
does not add a new literature citation.

External theorem status:

```text
new source-closed theorem proving GL1-ActualMovingShellPV: not found;
new source-closed sharp cutoff theorem: not found;
smoothed/filtering theorem mode: conditional, internal packet supported.
```

## Verification Notes

Commands/checks:

```text
./te doctor
sed -n reads of start.md, token-economy.yaml, L0_rules.md, L1_index.md
sed -n reads of the targeted Wave 1 synthesis, Wave 2 Agent 03, Agent 06,
  GL1 shifted Perron packet, GL1 smoothing bypass, and Agent 1 GL1 packet
find of the Wave 2 handoff directory
git status --short on targeted paths before writing
```

Protocol checks:

```text
status enum used: RIGOROUS_REDUCTION
no Koyama correspondence/email drafts read or edited
no broad archives loaded
no code tests apply to this markdown theorem handoff
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT07_GL1_MOVING_OFFTARGET_PV_2026-05-11.md
```
