---
schema_version: 1
title: "Koyama GL(1) theorem registry -- claim-safe"
date: 2026-05-10
type: theorem-registry
tier: claim-safe
scope: "GL(1) Dirichlet-character Koyama track; EC/DPAC included only as boundary claims"
sources:
  - handoff-2026-05-09-followup/KOYAMA_PIVOT_FINAL_SUMMARY.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
  - handoff-2026-05-09-followup/Koyama_NDC_constant_correction.md
  - handoff-2026-05-09-followup/Koyama_track_grounding.md
tags: [koyama, gl1, dirichlet, theorem-registry, ndc, ak, perron, b-infty]
---

# Koyama GL(1) theorem registry

Purpose: freeze the claim status after the 2026-05-09 sprint, with no
promotion unless dependencies are closed in the cited files.

## Status key

| Status | Meaning in this registry |
|---|---|
| `PROVED` | Dependency-closed in the cited notes, under the hypotheses stated in the claim. |
| `CONDITIONAL` | Valid only assuming a named conjectural/external theorem package or an explicitly listed unclosed lemma. |
| `NUMERICAL` | Computed evidence only; not a theorem. |
| `FALSIFIED` | Contradicted by a sourced theorem/conditional theorem or by decisive computation for the exact stated claim. |
| `DEFER` | Plausible or locally derived, but not dependency-closed enough for theorem use. |

## Global promotion rules

1. Cite the Aoki-Koyama Dirichlet constant as **Aoki-Koyama 2023, (1.4), p.235**. Do not cite it as eq. (1.5) for the Dirichlet case.
2. Treat `D_K -> e^{-gamma}` as `CONDITIONAL` unless the Perron-leading theorem for `c_K` is dependency-closed for the same `(chi,rho)`.
3. Separate the local double-pole residue from the global asymptotic
   `c_K = log K / L'(rho,chi) + C_1 + o(1)`. The former is local algebra; the latter needs contour and other-zero control.
4. Do not state `1/zeta(2)` as the GL(1) NDC limit. It is a historical numerical conjecture, now superseded.

## Notation

Let `chi` be primitive non-principal, `rho = 1/2 + it` a simple noncentral zero
of `L(s,chi)`, and

```text
E_K(chi,rho) = prod_{p<=K} (1 - chi(p) p^{-rho})^{-1}
c_K(chi,rho) = sum_{n<=K} mu(n) chi(n) n^{-rho}
D_K(chi,rho) = c_K(chi,rho) E_K(chi,rho)
```

For `B_infty`, let `psi` be the primitive character inducing `chi^2`, with
conductor `f | q`.

## Registry

| ID | Claim | Status | Dependencies / reason |
|---|---|---|---|
| AK-1 | `E_K(chi,rho) log K -> L'(rho,chi)/e^gamma`. | `CONDITIONAL` | This is the simple-zero specialization of Aoki-Koyama 2023, (1.4), p.235, i.e. the DRH statement for Dirichlet L-functions. It is not `L'/zeta(2)`. The `sqrt(2)` branch applies only at the central real point `s=1/2` with `chi^2=1`, not at noncentral zeros. |
| AK-2 | `E_K(chi,rho) log K -> L'(rho,chi)/zeta(2)`. | `FALSIFIED` | Conflicts with AK-1 by the fixed factor `e^gamma/zeta(2) ~= 1.0828`. K=10^7 data in `Koyama_NDC_constant_correction.md` also favors the AK-1 normalization. |
| P-0 | Local residue of `K^w / (w L(w+rho,chi))` at `w=0` equals `log K / L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2)`. | `PROVED` | Direct Laurent expansion at a simple zero. This proves the local double-pole coefficient only. |
| P-1 | Perron leading theorem: `c_K(chi,rho) = log K / L'(rho,chi) + o(log K)`. | `DEFER` | Numerically supported, and locally explained by P-0, but the cited notes do not fully close the shifted-contour dependencies. Other zero residues and truncation tails must be controlled for the exact shifted kernel. |
| P-2 | Global subleading theorem: `c_K = log K/L' + C_1 + o(1)` with `C_1 = -L''/(2 L'^2)`. | `DEFER` | P-0 proves the proposed `C_1` residue. It does not by itself prove that all nonlocal Perron contributions are `o(1)`. Promote only after P-1 plus subleading tail control are dependency-closed. |
| NDC-1 | Corrected GL(1) NDC: `D_K(chi,rho) -> e^{-gamma}`. | `CONDITIONAL` | Formal composition of AK-1 and P-1: `[log K/L'] * [L'/(e^gamma log K)]`. Current registry keeps it conditional because P-1 is not dependency-closed here. |
| NDC-2 | Saar's original GL(1) NDC package: `D_K(chi,rho) -> 1/zeta(2)` together with Perron-leading cancellation. | `FALSIFIED` | With P-1 assumed, it implies AK-2, which conflicts with AK-1. Numerically, K=2e6 could mimic `1/zeta(2)` inside the natural `1/log K` finite-size window; K=10^7 starts drifting toward the AK normalization. |
| NUM-1 | K=10^7 Dirichlet-pair recomputation favors `e^{-gamma}` over `1/zeta(2)`. | `NUMERICAL` | Mean `|D_K| zeta(2)` drifts from Saar's `0.992` at K=2e6 to `0.974` at K=1e7; AK-ratio mean `0.942` is close to `zeta(2)/e^gamma ~= 0.9237`. |
| BINF-1 | Corrected `B_infty` proposition below. | `PROVED` | Euler-product log expansion, primitive/imprimitive correction, boundary-line convergence for the `k=2` prime sum, and absolute convergence for the remaining tails. No DRH/GRH needed as stated in `Koyama_B_infty_proof.md`. |
| BINF-0 | Shorthand `T_infty = (1/2) log L(2rho,chi^2) + T_{>=3}` with no corrections. | `DEFER` | Not citation-ready as an exact identity. Use BINF-1 with `BPC1`, `BPC2`, and `T_{>=3}` separated. |
| EC-1 | Elliptic-curve NDC universality `D_K^E zeta(2) -> 1`. | `FALSIFIED` | Boundary/non-GL(1) claim. The final summary reports rank/curve-dependent constants, not a universal value. Do not use in the GL(1) theorem statement. |
| DPAC-1 | Dirichlet Polynomial Avoidance for fixed K at zeta zeros. | `DEFER` | Formalized/open; async Aristotle dispatch was still in progress. Numerics and R4 transfer are positive but not a theorem in the cited files. |

## Corrected B_infty proposition

`PROVED` proposition to use in a note:

```text
T_infty(chi,rho)
  = (1/2) log L(2rho,psi)
    + BPC1(chi,rho)
    + BPC2(chi,rho)
    + T_{>=3}(chi,rho),

B_infty(chi,rho) = exp(T_infty(chi,rho)).
```

Components:

```text
BPC1 = (1/2) sum_{p divides q, p does not divide f} log(1 - psi(p) p^{-2rho})

BPC2 = -(1/2) sum_{j>=2} (1/j) sum_p chi(p)^{2j} p^{-2j rho}

T_{>=3} = sum_{k>=3} (1/k) sum_p chi(p)^k p^{-k rho}
```

Component status:

| Component | Status | Notes |
|---|---|---|
| `BPC1` | `PROVED` | Finite primitive/imprimitive correction. For the sprint pairs: nonzero for `chi_{-4}`; zero for `chi_5` and `chi_{11}`. |
| `BPC2` | `PROVED` | Absolutely convergent log-Euler-product correction from replacing the `k=2` prime sum by `log L(2rho,psi)`. |
| `T_{>=3}` | `PROVED` | Absolutely convergent because `Re(k rho) >= 3/2` for `k>=3`; explicit tail bounds are in `Koyama_B_infty_proof.md`. |

The exact proposition is character-specific. It proves the structure of
`B_infty`; it does not by itself prove any universal NDC constant.

## Promotion / downgrade ledger

Promoted:

- `P-0` local double-pole residue: `PROVED`.
- `BINF-1` corrected `B_infty` identity with `BPC1`, `BPC2`, `T_{>=3}`: `PROVED`.
- AK citation correction: standardized to Aoki-Koyama 2023, (1.4), p.235.

Downgraded:

- `D_K -> e^{-gamma}`: from "proved" language in the final summary to `CONDITIONAL`.
- `c_K = log K/L' + C_1 + o(1)`: from global theorem language to `DEFER`; only the local residue is `PROVED`.
- `E_K log K -> L'/e^gamma`: from unqualified "proved" to `CONDITIONAL` on AK's DRH statement.
- `E_K log K -> L'/zeta(2)` and `D_K -> 1/zeta(2)`: `FALSIFIED`.
- EC NDC universality: kept outside GL(1), marked `FALSIFIED` for the simple universal form.

## Citation checklist

- [ ] Cite Aoki-Koyama as: **Aoki-Koyama 2023, (1.4), p.235** for the Dirichlet `L^{(m)}(s,chi)/(e^{m gamma} m!)` constant.
- [ ] State explicitly that AK (1.4) is a DRH/EDRH statement; do not present it as unconditional.
- [ ] Include the central-point caveat: the `sqrt(2)` factor is only for `chi^2=1` and `s=1/2`.
- [ ] Cite Akatsuka 2013 only for the zeta-side analog and Mertens normalization; do not use it as the Dirichlet citation.
- [ ] Cite the Koyama book excerpt only for the Taylor expansion / bounded higher-order-prime terms; not for `1/zeta(2)` as a theorem.
- [ ] When citing C1, say "local double-pole residue" unless the global contour proof has been supplied.
- [ ] For `B_infty`, include `psi`, `BPC1`, `BPC2`, and `T_{>=3}`. Do not use the shorthand formula as exact.
- [ ] Separate complex limits from modulus-only numerical checks. Most sprint tables report absolute values.
- [ ] Keep EC claims out of the GL(1) theorem statement.

## Short-note readiness verdict

Ready for a short note:

- Corrected AK constant audit: `L'/e^gamma`, cited as Aoki-Koyama 2023, (1.4), p.235, under DRH.
- Corrected `B_infty` proposition with `BPC1`, `BPC2`, and `T_{>=3}`.
- Numerical appendix explaining why K=2e6 could mimic `1/zeta(2)` and why K=1e7 favors `e^{-gamma}`.

Not ready as a proved theorem:

- `D_K -> e^{-gamma}` without an explicit dependency-closed Perron-leading proof.
- `c_K = log K/L' + C_1 + o(1)` as a global asymptotic; the local residue is ready, the global error control is not.
- Any GL(2)/elliptic-curve universality claim.

Publication-safe headline:

> In the GL(1) Koyama setting, the `1/zeta(2)` constant should be replaced
> by the Mertens constant `e^{-gamma}` under the Aoki-Koyama DRH constant
> and a Perron-leading hypothesis; the unconditional new theorem from this
> sprint is the corrected `B_infty` identity.
