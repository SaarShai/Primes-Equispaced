---
schema_version: 1
title: "Koyama Perron-leading gap audit"
date: 2026-05-10
type: gap-audit
tier: claim-safe
scope: "GL(1) Perron-leading closure for c_K(chi,rho)"
sources:
  - handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
tags: [koyama, gl1, perron, audit, ndc, dependency-closure]
---

# Perron-leading gap audit

## Outcome

`c_K(chi,rho) = log K/L'(rho,chi) + o(log K)` is **not promoted** from the current file set.

Status: `DEFER`.

Reason: the local double-pole residue is `PROVED`, but the global shifted-Perron remainder is not dependency-closed. The current notes still need a lemma proving that all nonlocal contributions for the exact kernel

```text
K^w / (w L(w+rho,chi))
```

are `o(log K)` after the `w=0` residue is extracted.

Consequently, the corrected GL(1) NDC

```text
D_K(chi,rho) = c_K(chi,rho) E_K(chi,rho) -> e^{-gamma}
```

stays `CONDITIONAL`, not `PROVED`: it is the formal product of AK's conditional Euler-product asymptotic and the still-deferred Perron-leading theorem.

## Status table

| Dependency | Status | Audit decision |
|---|---|---|
| Setup: primitive non-principal `chi`, simple noncentral zero `rho = 1/2 + it`, `L'(rho,chi) != 0` | `CONDITIONAL` | Accept as the working hypothesis of the GL(1) track. Simplicity/noncentrality must remain stated. |
| Perron representation for `c_K`: `c_K = (1/2pi i) int K^w/[w L(w+rho,chi)] dw + truncation` | `CONDITIONAL` | Standard Perron setup is plausible, but the exact transfer from published explicit formulae for `M^*(x,chi)` to this shifted kernel is asserted, not fully written as a dependency-closed theorem in the current notes. |
| Local Laurent expansion of `1/L(w+rho,chi)` at `w=0` | `PROVED` | Direct Taylor reciprocal at a simple zero. |
| Local double-pole residue at `w=0`: `log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2)` | `PROVED` | Registry P-0 promotes only this local algebra. |
| Other nontrivial zero residues for `w = rho_j - rho`, `rho_j != rho` | `DEFER` | Current C1 proof identifies terms `K^{i(gamma_j-gamma)}/((rho_j-rho)L'(rho_j))`, but does not prove their truncated aggregate is `o(log K)` for the exact shifted kernel. Oscillation is described, not converted into a uniform bound. |
| Trivial-zero residues | `PROVED` | Current notes bound them by a summable `O(K^{-1/2})`-type contribution; they are not the obstruction. |
| Shifted contour and horizontal sides | `DEFER` | The C1 proof explicitly derives a contour balance that is "not good enough", then appeals to Soundararajan-style bounds through an unproved transfer to the shifted-kernel non-residue. |
| Perron truncation/tail for the exact shifted kernel | `DEFER` | Needed jointly with contour choice and zero-residue truncation. Current registry says "other zero residues and truncation tails must be controlled for the exact shifted kernel." |
| Global Perron leading: `c_K = log K/L' + o(log K)` | `DEFER` | Local residue plus numerics are insufficient under the sprint promotion rule. |
| Global Perron subleading: `c_K = log K/L' - L''/(2L'^2) + o(1)` | `DEFER` | Stronger than leading; also needs all nonlocal contributions to be `o(1)`. |
| AK Euler-product constant: `E_K log K -> L'(rho,chi)/e^gamma` | `CONDITIONAL` | Aoki-Koyama 2023 (1.4), p.235, under DRH/EDRH; not unconditional. |
| False AK constant: `E_K log K -> L'(rho,chi)/zeta(2)` | `FALSIFIED` | Contradicts AK (1.4) by fixed constant factor and K=10^7 numerics in the existing docs. |
| Corrected GL(1) NDC: `D_K -> e^{-gamma}` | `CONDITIONAL` | Formal composition of AK plus Perron-leading. Not proved until Perron-leading leaves `DEFER`. |
| Original GL(1) NDC with the old `1/zeta(2)` constant | `FALSIFIED` | Superseded by AK normalization; registry marks it falsified. |
| Corrected `B_infty` identity with `psi`, `BPC1`, `BPC2`, `T_{>=3}` | `PROVED` | Useful supporting GL(1) theorem, but it does not close the additive Perron-leading gap. |

## Evidence from existing docs

### Later registry controls the promotion standard

The decision memo says:

> "GL(1) is short-note-ready only in a conditional form. The corrected constant is `e^{-gamma}`, not `1/zeta(2)`, but `D_K -> e^{-gamma}` is not promoted as proved until the Perron-leading theorem for `c_K` is dependency-closed."

It also classifies:

```text
Global Perron leading `c_K = log K/L' + o(log K)` | DEFER
Global subleading `c_K = log K/L' - L''/(2L'^2) + o(1)` | DEFER
Corrected GL(1) NDC `D_K -> e^{-gamma}` | CONDITIONAL
```

The theorem registry gives the exact rule:

> "Separate the local double-pole residue from the global asymptotic `c_K = log K / L'(rho,chi) + C_1 + o(1)`. The former is local algebra; the latter needs contour and other-zero control."

And it records P-1:

> "Perron leading theorem: `c_K(chi,rho) = log K / L'(rho,chi) + o(log K)`. | `DEFER` | Numerically supported, and locally explained by P-0, but the cited notes do not fully close the shifted-contour dependencies. Other zero residues and truncation tails must be controlled for the exact shifted kernel."

### What is actually proved locally

`Koyama_C1_subleading_proof.md` proves the residue algebra for

```text
F(w) = K^w / (w L(w+rho,chi)).
```

At a simple zero,

```text
1/L(w+rho,chi)
  = 1/(L'(rho,chi) w)
    - L''(rho,chi)/(2 L'(rho,chi)^2)
    + O(w),
```

so the coefficient of `1/w` in `F(w)` is

```text
log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2).
```

That proves P-0 only. It does not prove the remaining residues and contour integrals are lower order.

### Why the C1 "PROOF CLOSED" verdict is not enough

The C1 file itself exposes the missing pieces. It writes the decomposition with:

```text
(other zeros' contributions)
...
(trivial zeros and J_1, J_2, J_3 contour pieces)
```

For other zeros it gives terms of the form:

```text
K^{i(gamma_j - gamma)} / ((rho_j - rho) L'(rho_j,chi)).
```

Their magnitudes do not decay with `K`. The text says these oscillations "average to zero", but no lemma proves the required aggregate bound for the truncated moving zero set. For the leading theorem the needed bound is only `o(log K)`, but it still must be proved.

For the shifted contour, the file derives:

```text
K^{-1/2+epsilon} K^{1/2+2epsilon} exp(C(log log K)^2)
  = K^{3epsilon} exp(C(log log K)^2),
```

and correctly notes this is "not good enough". It then invokes a Soundararajan-style bound for `M(K)` and says the shifted-kernel error is "bounded by (essentially)" a normalized `M^*(K,chi)` non-residue term. That "essentially" is exactly the missing dependency: the transfer to the exact shifted kernel is not stated as a theorem with hypotheses and constants.

Therefore the local proof can be cited; the global Perron-leading theorem cannot.

## External theorem citations already present

No browsing used.

AK constant theorem, quoted in `Koyama_AK_constant_proof.md` from Aoki-Koyama 2023 (1.4), p.235:

> "In case of Dirichlet L-functions L(s,χ) for non-principal Dirichlet characters χ, DRH states that it holds on Re(s)=1/2 that"

```text
lim_{x->infty} ((log x)^m prod_{p<=x}(1 - chi(p)/p^s)^(-1))
  = L^(m)(s,chi) / (e^(m gamma) m!)
    * { sqrt(2) if chi^2=1, s=1/2; 1 otherwise }.
```

For simple noncentral zero `rho`, this gives:

```text
E_K(chi,rho) log K -> L'(rho,chi)/e^gamma
```

under DRH/EDRH, hence `CONDITIONAL`.

Inoue theorem quoted in `Koyama_C1_subleading_proof.md`:

> "Theorem 1. Let `x > 0`, `q >= 2`, `T >= max{T_0, exp(q^{1/3}), 2/x}` ... there exists a `T_nu in [T,2T]` satisfying"

```text
M^*(x,chi)
  = sum_{|gamma| < T_nu} Res/contribution at zeros
    + Res_{s=0}(x^s/(L(s,chi)s))
    + ...
```

Audit use: supports explicit-formula context for `M^*(x,chi)`, but does not by itself close the shifted-kernel `c_K(rho,chi)` remainder.

`Koyama_B_infty_proof.md` cites Akatsuka 2013 Lemma 2.1 / equation (2.5) for boundary-line conditional convergence:

```text
sum_{p <= X} p^{-1-2it_0} = c(t_0) + O((log X)^(-1)), t_0 != 0.
```

Audit use: closes the `B_infty` boundary prime-sum identity, not the Perron-leading additive remainder.

## Minimal missing lemma

To promote P-1, add and prove this lemma.

**Shifted Perron nonlocal remainder lemma.** Let `chi` be primitive non-principal and `rho = 1/2 + it` a simple noncentral zero of `L(s,chi)`. For a valid truncated Perron rectangle for

```text
c_K(chi,rho) = sum_{n <= K} mu(n) chi(n) n^{-rho},
```

with kernel

```text
K^w / (w L(w+rho,chi)),
```

after extracting the `w=0` residue,

```text
R_K :=
  c_K(chi,rho)
  - Res_{w=0} K^w/(w L(w+rho,chi))
```

satisfies

```text
R_K = o(log K).
```

The proof must explicitly bound:

1. the aggregate of all nontrivial-zero residues `w = rho_j - rho`, `rho_j != rho`, including the dependence on the truncation height;
2. the shifted vertical contour and horizontal sides for the same kernel;
3. the Perron truncation error and endpoint convention;
4. the parameter choice linking height, horizontal displacement, and `K`.

For P-2/subleading, replace the conclusion by `R_K = o(1)`.

## Final decision

Do not promote

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K)
```

as `PROVED` from the current docs.

Publication-safe statement:

```text
The local Perron double-pole residue is proved. The global Perron-leading
asymptotic remains deferred pending a shifted-Perron nonlocal remainder
lemma. Under AK's DRH/EDRH Euler-product asymptotic and that missing
Perron-leading lemma, D_K(chi,rho) -> e^{-gamma}.
```
