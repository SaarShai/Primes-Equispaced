---
schema_version: 1
title: "Koyama GL(1) claim-safe short-note outline"
date: 2026-05-10
type: note-outline
tier: claim-safe
scope: "GL(1) Dirichlet-character Koyama note; NDC kept conditional"
sources:
  - handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
  - handoff-2026-05-09-followup/Koyama_NDC_constant_correction.md
tags: [koyama, gl1, dirichlet, ndc, claim-safe, outline]
---

# Koyama GL(1) short-note outline

## Claim contract

This outline is publication-safe only if it keeps the theorem set small:

- State the Aoki-Koyama constant under DRH/EDRH: for a primitive non-principal Dirichlet character `chi` and a simple noncentral zero `rho` of `L(s,chi)`,
  `E_K(chi,rho) log K -> L'(rho,chi)/e^gamma`.
- State the local Perron double-pole residue:
  `Res_{w=0} K^w/(w L(w+rho,chi)) = log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2)`.
- State the corrected `B_infty` identity with `psi`, `BPC1`, `BPC2`, and `T_{>=3}`.
- State that `1/zeta(2)` is falsified for the GL(1) NDC constant.
- State the elliptic-curve simple universality claim as a negative result only.

Do not state `D_K(chi,rho) -> e^{-gamma}` as a proved theorem unless the Perron-leading theorem for `c_K` has been closed elsewhere. Default status here: conditional.

## Proposed title

Correcting the constant in a GL(1) Koyama product and an explicit `B_infty` factor

## Abstract skeleton

Let

```text
E_K(chi,rho) = prod_{p <= K} (1 - chi(p) p^{-rho})^{-1},
c_K(chi,rho) = sum_{n <= K} mu(n) chi(n) n^{-rho},
D_K(chi,rho) = c_K(chi,rho) E_K(chi,rho).
```

For primitive non-principal `chi` and a simple noncentral zero `rho` of `L(s,chi)`, Aoki-Koyama's DRH/EDRH partial-Euler-product formula gives

```text
E_K(chi,rho) log K -> L'(rho,chi)/e^gamma,
```

not `L'(rho,chi)/zeta(2)`. A local Perron computation gives the double-pole residue

```text
log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2),
```

but this is only local residue algebra unless the global Perron-leading estimate is proved. Consequently the corrected NDC limit

```text
D_K(chi,rho) -> e^{-gamma}
```

is presented only as conditional on the Perron-leading hypothesis
`c_K(chi,rho) = log K/L'(rho,chi) + o(log K)`.

The unconditional GL(1) theorem in this note is the corrected `B_infty` identity:

```text
T_infty(chi,rho)
  = (1/2) log L(2rho,psi)
    + BPC1(chi,rho)
    + BPC2(chi,rho)
    + T_{>=3}(chi,rho),

B_infty(chi,rho) = exp(T_infty(chi,rho)),
```

where `psi` is the primitive character inducing `chi^2`. This identity replaces the shorthand formula using only `(1/2) log L(2rho,chi^2)` plus a tail.

## Section outline

### 1. Notation and hypotheses

- `chi`: primitive non-principal Dirichlet character.
- `rho = 1/2 + it`: simple noncentral zero of `L(s,chi)`.
- `E_K`, `c_K`, and `D_K` as above.
- Avoid central real point caveat by assuming `t != 0`; otherwise Aoki-Koyama has the separate `sqrt(2)` branch when `chi^2 = 1` and `s = 1/2`.

### 2. Corrected AK constant under DRH/EDRH

Claim to state:

```text
E_K(chi,rho) log K -> L'(rho,chi)/e^gamma.
```

Status: conditional on Aoki-Koyama 2023, equation (1.4), p.235, under DRH/EDRH.

Do not write:

```text
E_K(chi,rho) log K -> L'(rho,chi)/zeta(2).
```

That constant is superseded by the Aoki-Koyama normalization and by the K=10^7 recomputation trend.

### 3. Local Perron residue

Use the shifted Perron kernel

```text
K^w/(w L(w+rho,chi)).
```

At a simple zero,

```text
1/L(w+rho,chi)
  = 1/(L'(rho,chi) w)
    - L''(rho,chi)/(2 L'(rho,chi)^2)
    + O(w),
K^w/w
  = 1/w + log K + O(w).
```

Therefore the local residue at `w=0` is

```text
log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2).
```

Status: proved as local algebra. Do not promote it to the global asymptotic

```text
c_K(chi,rho) = log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2) + o(1)
```

without a contour proof controlling other zero residues and tails.

### 4. Conditional corrected NDC corollary

Assume the separate Perron-leading hypothesis:

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

Composing with the AK constant gives

```text
D_K(chi,rho)
  = c_K(chi,rho) E_K(chi,rho)
  -> e^{-gamma}.
```

Status: conditional. This section should be written as a corollary with an explicit hypothesis, not as the main theorem.

### 5. Corrected `B_infty` theorem

Let `psi` be the primitive character of conductor `f | q` inducing `chi^2`. Define

```text
BPC1(chi,rho)
  = (1/2) sum_{p | q, p not | f} log(1 - psi(p) p^{-2rho}),

BPC2(chi,rho)
  = -(1/2) sum_{j >= 2} (1/j) sum_p chi(p)^{2j} p^{-2j rho},

T_{>=3}(chi,rho)
  = sum_{k >= 3} (1/k) sum_p chi(p)^k p^{-k rho}.
```

The theorem:

```text
T_infty(chi,rho)
  = (1/2) log L(2rho,psi)
    + BPC1(chi,rho)
    + BPC2(chi,rho)
    + T_{>=3}(chi,rho),

B_infty(chi,rho) = exp(T_infty(chi,rho)).
```

Status: proved unconditionally in the cited `B_infty` proof, under the stated simple-zero/on-line setup and standard boundary convergence inputs. This is the strongest clean theorem for the short note.

### 6. Constant correction and numerical note

Record the correction plainly:

```text
1/zeta(2) is not the GL(1) NDC constant.
```

Safe numerical framing:

- `K = 2e6` was within the natural `1/log K` window where `1/zeta(2)` could look plausible.
- `K = 1e7` recomputation drifts away from `1/zeta(2)` and toward the Aoki-Koyama/Mertens normalization.
- Numerical evidence supports the correction but is not a substitute for the missing Perron-leading proof.

### 7. Boundary: elliptic-curve negative result

Keep EC out of the GL(1) theorem. If mentioned, say only:

```text
The simple elliptic-curve universality claim D_K^E zeta(2) -> 1 is falsified by the current sweep; no EC normalization is promoted here.
```

Do not promote `D/L2E_partial^rank` or any mixed EC residual as a theorem. The decision memo treats the former as a numerical proxy and the latter as deferred.

## Theorem packaging

Use exactly this hierarchy:

1. Theorem A: Aoki-Koyama constant specialization, conditional on DRH/EDRH.
2. Lemma B: local Perron double-pole residue.
3. Theorem C: corrected `B_infty` identity.
4. Conditional Corollary D: if Perron-leading holds, then `D_K -> e^{-gamma}`.
5. Remark E: `1/zeta(2)` is falsified; EC simple universality is also negative.

## Phrases to avoid

- "We prove `D_K -> e^{-gamma}`."
- "The Perron expansion gives `c_K = log K/L' + C_1 + o(1)`."
- "`1/zeta(2)` is a secondary normalization."
- "The EC case obeys the same universality."
- "The shorthand `B_infty = exp((1/2) log L(2rho,chi^2) + T_{>=3})` is exact."

## One-paragraph publication-safe summary

In the GL(1) Koyama setting, the constant suggested by the earlier `1/zeta(2)` numerics should be replaced by the Aoki-Koyama/Mertens constant `e^{-gamma}`: under Aoki-Koyama's DRH/EDRH partial-Euler-product theorem,
`E_K(chi,rho) log K -> L'(rho,chi)/e^gamma`. A local Perron computation gives the double-pole residue
`log K/L'(rho,chi) - L''(rho,chi)/(2L'(rho,chi)^2)`, but the global Perron-leading estimate remains a separate dependency. Thus `D_K(chi,rho) -> e^{-gamma}` is only a conditional corollary here. The unconditional claim to promote is the corrected `B_infty` formula with the primitive inducing character `psi`, the finite bad-prime correction `BPC1`, the absolutely convergent log-Euler correction `BPC2`, and the `k >= 3` tail. The former `1/zeta(2)` GL(1) NDC constant and the simple EC universality claim are negative results, not promoted theorems.
