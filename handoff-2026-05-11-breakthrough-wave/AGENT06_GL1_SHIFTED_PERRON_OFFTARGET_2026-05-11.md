---
schema_version: 1
title: "Agent 06 - GL1 shifted Perron off-target control"
date: 2026-05-11
agent: "Agent 06"
type: theorem-reduction
tier: claim-safe
status: RIGOROUS_REDUCTION
confidence: 0.88
scope: "GL1-Sharp-OffTarget-Control for K^w/(w L(rho+w,chi))"
sources:
  - start.md
  - L1_index.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/BIGGEST_CHALLENGES_MATRIX_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/GL1_SMOOTHING_BYPASS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/GL1_PERRON_CLOSURE_PATH_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
  - primes-equispaced/handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
  - primes-equispaced/handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - primes-equispaced/handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
tags: [gl1, perron, off-target, principal-value, smoothing, koyama]
---

# Agent 06 - GL1 Shifted Perron Off-Target Control

Status enum: `RIGOROUS_REDUCTION`.

mode label: `SHARP_PV_CONDITIONAL_ONLY_SMOOTHED_FALLBACK`.

## Verdict

Simple off-target zeros remove the polynomial-in-`log K` obstruction from
multiple zeros, but they do not prove the sharp off-target aggregate is
`o(log K)`.

A strong moving fixed-weight PV theorem would close the sharp route
conditionally. But that theorem is essentially the missing
`GL1-Sharp-OffTarget-Control` input, not a consequence of simplicity, spacing,
ordinary symmetric PV language, or square-moment estimates.

Claim-safe decision:

```text
global off-target simplicity + strong moving PV + rectangle/truncation
  => sharp conditional theorem;

global off-target simplicity + weak/fixed-u PV/spacing/moments
  => no sharp theorem promotion;

without the strong PV input
  => retain conditional sharp statement or use smoothed/filtering fallback.
```

## Sharp Simple-Zero Sum

Let `chi` be primitive nonprincipal and let

```text
rho = 1/2 + i t
```

be the target simple noncentral zero. Put

```text
u = log K,
F_K(w) = K^w/(w L(rho+w,chi)).
```

After the target residue at `w=0`, a simple off-target zero
`lambda != rho` contributes

```text
K^(lambda-rho)/((lambda-rho)L'(lambda,chi)).
```

Under DRH, write `lambda = 1/2+i gamma` and

```text
alpha_lambda = gamma - t.
```

Then the sharp simple-zero aggregate at legal height `T_K` is

```text
Z_sharp(u,T_K)
  = sum_{lambda != rho, |alpha_lambda| <= T_K}
      exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi)).
```

The target term has size `u/L'(rho,chi)`. Therefore sharp leading needs

```text
Z_sharp(u,T_K) = o(u)
```

on the same moving height sequence used by the Perron rectangle, plus
trivial-zero, contour, and truncation errors `o(u)`.

## Conditional Sharp Theorem

Define `GL1-Sharp-FixedWeightPV(chi,rho)` to mean:

```text
There are legal Perron heights T_K -> infinity, with the same zero-avoiding
height convention used in the contour shift, such that

  Z_sharp(log K,T_K) = o(log K).

Equivalently, in dyadic form, for u in [U,2U],

  sup_{u in [U,2U]}
  |sum_{lambda != rho, |alpha_lambda| <= T(e^u)}
     exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi))|
    = o(U).
```

Then the sharp theorem is immediate bookkeeping:

```text
Theorem GL1-sharp-leading-conditional.
Assume:
  1. rho is simple and noncentral;
  2. all crossed off-target nontrivial zeros are simple, or all multiple-zero
     Laurent residues are separately o(log K);
  3. GL1-Sharp-FixedWeightPV(chi,rho);
  4. trivial-zero residues, shifted rectangle integrals, Perron truncation,
     and endpoint errors are o(log K) for the same heights.

Then

  c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

With the AK-side product input retained as a separate conditional input,
this would imply the corrected product limit

```text
c_K(chi,rho) E_K(chi,rho) -> e^(-gamma).
```

This is not promoted as proved. Assumption 3 is the hard missing theorem in
fixed-weight PV form.

## Why Weak PV Does Not Close Sharp

The word "PV" is not enough. The sharp cutoff needs a moving-height estimate
as `u=log K -> infinity`. The following weaker statements do not imply it:

```text
1. each fixed off-target simple zero is O(1);
2. a finite off-target set is O(1);
3. symmetric truncation pairs conjugate-looking terms;
4. fixed-u convergence of a principal-value zero series;
5. zero spacing plus l2/square-moment bounds for coefficients;
6. a bound of size O(log T_K), since log T_K is asymptotic to log K.
```

The obstruction is logical, not a counterexample to Dirichlet L-functions.
The abstract model

```text
alpha_n = n,
a_n = a_{-n} = 1/(2n),
S_T(u) = sum_{1 <= n <= T} cos(nu)/n
```

has perfect spacing and square-summable coefficients. But at resonant points
`u = 2 pi m`,

```text
S_T(u) = sum_{1 <= n <= T} 1/n = log T + O(1).
```

For the Perron-scale height `T_K = K/(log K)^B`, this gives

```text
log T_K = log K - B log log K,
```

which is not `o(log K)`. Therefore any proof using only spacing and
coefficient square moments would prove a false statement in this model.

The direct estimate that would be useful is a shell bound for the actual GL1
coefficients:

```text
B_j(U)
 = sup_{u in [U,2U]}
   |sum_{2^j < |alpha_lambda| <= 2^(j+1)}
      exp(i alpha_lambda u)/(i alpha_lambda L'(lambda,chi))|,

sum_{2^j <= T(e^U)} B_j(U) = o(U).
```

No current packet supplies this estimate. Without it, the sharp simple-zero
route remains conditional.

## Multiple-Zero Reminder

If an off-target zero `lambda` has multiplicity `m`, the local residue of
`F_K` has top term

```text
K^(lambda-rho) (log K)^(m-1)
---------------------------------------
(m-1)! (lambda-rho) a_m,
```

where

```text
L(lambda+z,chi) = a_m z^m + ...
```

Under DRH, `K^(lambda-rho)` has absolute value `1`. Thus:

```text
m = 1: bounded single oscillatory term;
m = 2: another log K-scale term;
m > 2: larger than the target log K scale.
```

So target-zero simplicity alone is formally insufficient. Even after global
off-target simplicity is assumed, the infinite simple-zero PV aggregate is
still the unsourced input.

## Smoothed/Filtering Fallback

The smoothed mode remains the only claim-safe non-sharp theorem mode in the
current packet set.

For a target-normalized Perron-admissible cutoff,

```text
W_hat(w) = 1/w + kappa_W + O(w)
```

and

```text
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
multiplicity `m` has effective residue degree `m-h-1` in `log K`; if
`h >= m`, that finite residue is killed. Hence finite signed filtering can
delete any prescribed finite off-target set, while retaining an explicit tail.

Claim-safe smoothed theorem mode:

```text
Assume rho is simple, W is target-normalized and Perron-admissible, and
SmoothOffTargetControl(W;chi,rho) holds:

  Z_off,W + Z_triv,W + Z_kernel,W + C_rect,W = o(log K)

for legal heights. Then

  c_{W,K}(chi,rho) = log K/L'(rho,chi) + o(log K).
```

This does not transfer to the sharp cutoff unless one proves uniform estimates
as `W` approaches the step kernel. Those uniform estimates are another form
of the missing sharp off-target theorem.

## Decision Table

| Input package | Result | Status |
|---|---|---|
| Target local residue | `log K/L'(rho,chi) + O(1)` local contribution | `PROVED_LOCAL` |
| Target zero simple only | does not control off-target residues | `INSUFFICIENT` |
| All off-target zeros simple | removes higher-degree Laurent obstruction | `HELPFUL_NOT_ENOUGH` |
| Simple zeros + weak/fixed-u PV | no moving `o(log K)` theorem | `NO_GO` |
| Simple zeros + `GL1-Sharp-FixedWeightPV` + rectangle control | sharp leading theorem | `CONDITIONAL` |
| Smoothed target-normalized kernel + `SmoothOffTargetControl` | smoothed leading theorem | `CONDITIONAL_SMOOTHED` |
| Finite signed filtering | finite residues killed, tail retained | `PROFILE_THEOREM` |

## Verification Notes

Read local context only. No new external theorem claim is made here, so no
`curl + pdftotext` source packet was needed.

Files read for this packet:

```text
start.md
token-economy.yaml
L0_rules.md
L1_index.md
primes-equispaced/L1_index.md
primes-equispaced/handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/BIGGEST_CHALLENGES_MATRIX_2026-05-11.md
primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/GL1_SMOOTHING_BYPASS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-gpt55-wave/GL1_PERRON_CLOSURE_PATH_2026-05-11.md
primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/LITERATURE_INPUTS_THEOREM_SOURCE_NOTE_2026-05-11.md
primes-equispaced/handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
primes-equispaced/handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
primes-equispaced/handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_FIXED_WEIGHT_PV_NOGO_CONDITIONAL_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md
```

Commands/checks used:

```text
./te doctor
rg --files / find for GL1, L1, KOYAMA, BIGGEST_CHALLENGES context
sed -n on the source packets listed above
git status --short before write
mkdir -p primes-equispaced/handoff-2026-05-11-breakthrough-wave
sed -n readback of this packet after write
rg status/TODO/protocol markers in this packet
rg trailing-whitespace and non-ASCII scans in this packet
```

No correspondence or email draft file was edited. No code tests apply to this
markdown-only theorem handoff.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT06_GL1_SHIFTED_PERRON_OFFTARGET_2026-05-11.md
```

No commit. No push.
