---
schema_version: 1
title: "Koyama research decision memo 2026-05-10"
date: 2026-05-10
type: decision-memo
tier: claim-safe
scope: "Koyama GL(1), EC-NDC, Path B rank/conductor, DPAC hygiene"
sources:
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_normalization_matrix_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_EC_Euler_factor_theory_2026-05-10.md
  - koyama-shared/results/PATH_B_DECONFOUNDING_2026-05-10.md
  - formal-conjectures/DPAC_HYGIENE_STATUS_2026-05-10.md
tags: [koyama, ndc, gl1, elliptic-curves, path-b, dpac, decision-memo]
---

# Koyama research decision memo

## Executive verdict

The 2026-05-10 sprint resolves the safety status of the Koyama work:

- GL(1) is short-note-ready only in a conditional form. The corrected constant is `e^{-gamma}`, not `1/zeta(2)`, but `D_K -> e^{-gamma}` is not promoted as proved until the Perron-leading theorem for `c_K` is dependency-closed.
- The unconditional GL(1) theorem to promote is the corrected `B_infty` identity with `BPC1`, `BPC2`, and `T_{>=3}`. The local Perron double-pole residue is also proved, but only local.
- EC-NDC simple universality is falsified. No tested normalization is promoted. The best numerical proxy is `D/L2E_partial^rank`, but the local-factor theory rejects bare `L(2,E)` as the mechanism and points to a mixed adjoint/Sym^2 residual.
- Path B rank-only evidence fails the conductor-control acceptance bar. Treat W2 as plausible but conductor-confounded.
- DPAC is hygiene/scaffold work only. LI does not imply DPAC as stated; a log-prime/exponential phase independence hypothesis is required.

No email, public claim, or paper theorem should cite a promoted NDC universality theorem from this sprint.

## Decision table

| Claim | Status | Decision |
|---|---|---|
| `E_K(chi,rho) log K -> L'(rho,chi)/e^gamma` | `CONDITIONAL` | Use only as Aoki-Koyama 2023 (1.4), p.235 under DRH/EDRH. |
| `E_K(chi,rho) log K -> L'(rho,chi)/zeta(2)` | `FALSIFIED` | Do not use. Conflicts with AK normalization and K=1e7 numerics. |
| Local double-pole residue for `K^w/(w L(w+rho,chi))` | `PROVED` | Promote as local algebra at a simple zero. |
| Global Perron leading `c_K = log K/L' + o(log K)` | `DEFER` | Needed before the NDC limit can be theorem language. |
| Global subleading `c_K = log K/L' - L''/(2L'^2) + o(1)` | `DEFER` | Local residue is not enough; nonlocal residues/tails remain open. |
| Corrected GL(1) NDC `D_K -> e^{-gamma}` | `CONDITIONAL` | Conditional corollary of AK plus Perron-leading. Not proved in current files. |
| Original GL(1) NDC `D_K -> 1/zeta(2)` | `FALSIFIED` | Superseded. |
| Corrected `B_infty` formula | `PROVED` | Safe theorem: include `psi`, `BPC1`, `BPC2`, and `T_{>=3}`. |
| EC-NDC `D_K^E zeta(2) -> 1` | `FALSIFIED` | Current sweep is rank/curve-dependent. |
| `D/L2E_partial^rank` EC normalization | `NUMERICAL` | Best current proxy, but fails promotion by cross-curve ratio `1.42083`. |
| Mixed EC residual `D_mix = D_K^E zeta(2)/C_mix(K)` | `DEFER` | Best next experiment from local-factor theory. |
| Path B isolated rank law | `DEFER` | Current data fail once `log(conductor)` is included. |
| DPAC from zeta-zero LI | `FALSIFIED` as stated | Replace with strengthened phase-independence conditional if used. |
| Full DPAC | `DEFER` | Research-open; Aristotle artifact is a two-sorry scaffold. |

## EC-NDC reconciliation

Agent B's matrix says `D/L2E_partial^rank` and `D*zeta(2)/L2E_partial^rank` are the best tested normalizations, with max within-curve K CV `0.08567129` and cross-curve CV `0.14173955`. They still fail the promotion rule because the cross-curve ratio is `1.42083`.

Agent C's local-factor derivation says bare `L(2,E)` has the wrong first local term: its log starts with `a_p/p^2`, while the EC sweep at `s=1` needs the same-root square contribution `(a_p^2 - 2p)/(2p^2)` after removing the linear `a_p/p` term. Therefore `L2E_partial^rank` is at most a finite-data proxy, not the mechanism to publish.

Next EC observable:

```text
D_mix(K) = D_K^E * zeta(2) / C_mix(K)

C_mix(K)
  = (e^gamma log K)^(1/2)
    * product_{p <= K, good} exp(-a_p/p) * (1 - a_p/p + 1/p)^(-1)
    * C_bad(E)
```

Fallback quick check:

```text
C_2(K)
  = (e^gamma log K)^(1/2)
    * exp(sum_{p <= K, good} (a_p^2 - 2p)/(2p^2))

D_2(K) = D_K^E * zeta(2) / C_2(K)
```

## Path B decision

The EC-only `PATH_B_20FORMS.csv` contains an upward rank signal, but rank and conductor are nearly locked together:

- `corr(rank, logN) = 0.972107`.
- `logN` alone fits better than rank alone.
- In `rank + logN`, the rank coefficient flips negative.
- In `rank + logN + interaction`, the rank main effect is essentially zero at mean log conductor.
- The lone rank-3 point `5077a1` has leverage `0.870262`.

Acceptance result: fail. Do not state W2 as an isolated rank law. The next useful dataset is conductor-matched controls near conductors `389-571`, near `5077`, and near rank-4 candidate conductors `19747`, `214850`, and `234446`.

## DPAC decision

`DPAC_full.lean` is useful as a scaffold, but the bridge `dpac_of_LI` is unsafe. LI among zeta-zero ordinates does not control the phases `exp(-i gamma log p)` for primes `p <= K`. Any DPAC bridge needs an explicit finite log-prime/exponential phase independence hypothesis or a theorem implying it.

Safe DPAC packaging:

- Full DPAC: `DEFER`.
- `dpac_of_LI`: downgrade; unsafe as stated.
- Density-one result: abstract conditional counting lemma only.
- Aristotle result: build scaffold with two `sorry` holes, not a proof.

## Next queue

1. GL(1) short note: state AK under DRH/EDRH, promote only the local Perron residue and corrected `B_infty`, and label `D_K -> e^{-gamma}` as conditional on Perron-leading.
2. EC compute: implement `C_mix(K)` and `C_2(K)` columns for 37a1, 11a1, and 389a1 at existing checkpoints. If they improve stability, push 37a1 and 11a1 toward `K=1e6`.
3. Path B controls: build conductor-matched EC controls before any rank-4/5 claim.
4. DPAC hygiene: rename or annotate the unsafe LI bridge before future formal work, so no downstream note treats it as a theorem.

## Publication-safe headline

In the GL(1) Koyama setting, the `1/zeta(2)` constant should be replaced by `e^{-gamma}` under Aoki-Koyama's DRH constant and a still-open Perron-leading hypothesis. The unconditional theorem from this sprint is the corrected `B_infty` identity; EC universality and DPAC remain outside the promoted theorem set.
