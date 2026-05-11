---
schema_version: 1
title: "Breakthrough Wave 2 Synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
tags: [breakthrough-wave-2, h1, h2, gl1, b-plus, dpac, delta]
---

# Breakthrough Wave 2 Synthesis

Status: `RIGOROUS_REDUCTION`. No theorem is promoted.

Wave 2 narrowed rather than broadened. The main EC pointwise wall is still H1
rank-one reciprocal-pole control, but the wall is now sharper. H2 improved
materially because the exact good-prime Sym2 finite-part theorem is
source-closed as a component. Full H2 is still not promoted because the S1
branch-contour theorem remains open.

## Packet Ledger

| agent | packet | result | durable outcome |
|---|---|---|---|
| 01 | `AGENT01_H1_DERIVATIVE_SOURCE_CLOSURE_2026-05-11.md` | `RIGOROUS_REDUCTION` | Checked Li-Zaharescu, de Faveri, and Bui-Florea-Milinovich style inputs. No checked source proves fixed-curve `R_E,1(T)=o(T^2)`. The clean external target is a GL2/EC negative first moment or separated-zero theorem with an explicit bad-set reciprocal budget. |
| 02 | `AGENT02_H1_NEAR_MULTIPLE_ZERO_BUDGET_2026-05-11.md` | `RIGOROUS_REDUCTION` | Near-colliding zeros are a real small-`L'(rho)` mechanism. Spacing or local statistics alone do not control reciprocal derivatives; a bad-set budget or zero-free-circle plus quantitative minimum-modulus theorem is required. |
| 03 | `AGENT03_H1_ACTUAL_COEFFICIENT_MOVING_PV_2026-05-11.md` | `RIGOROUS_REDUCTION` | Replaced abstract spacing models with the actual coefficients `W_hat(i gamma)/L'(E,1+i gamma)`. The moving PV target is now an actual-coefficient dyadic shell theorem, not a generic spacing consequence. |
| 04 | `AGENT04_H1_FINITE_BOX_THEOREM_ASSEMBLY_2026-05-11.md` | `RIGOROUS_REDUCTION` | Assembled the conditional finite-box H1 theorem using legal exponential heights, `H-left`, Li-Zaharescu horizontal height input, simple-zero `R_E,1` target, and multiple-zero effective-degree conditions. |
| 05 | `AGENT05_H2_S1_BRANCH_CONTOUR_2026-05-11.md` | `RIGOROUS_REDUCTION` | Reduced S1 endpoint closure to a named missing theorem, `S1-CutPlane-LogGrowth(E,W,eta)`, plus right-branch bookkeeping. Branch-only continuation is coherent but not yet a legal infinite contour shift. |
| 06 | `AGENT06_H2_GOOD_PRIME_SYM2_CLOSURE_2026-05-11.md` | `RIGOROUS_REDUCTION` | Component source closure: exact good-prime Sym2 finite part is closed with `kappa_sym=0` under the standard global adjoint/Sym2 ramified-factor reconciliation. This does not promote full H2 because S1 is still open. |
| 07 | `AGENT07_GL1_MOVING_OFFTARGET_PV_2026-05-11.md` | `RIGOROUS_REDUCTION` | GL1 sharp cutoff has no special escape hatch: off-target simple zeros still require actual moving PV plus rectangle/truncation control. Smoothing/filtering remains a separate fallback, not a sharp-cutoff transfer. |
| 08 | `AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md` | `RIGOROUS_REDUCTION` | Converted the B+ tier-1B bridge into an execution-ready compute spec: exact command contract, TSV schemas, chunk/repeat certification, and runtime split. No long compute was run. |
| 09 | `AGENT09_DPAC_LEAN_BRIDGE_PATCH_PLAN_2026-05-11.md` | `RIGOROUS_REDUCTION` | Produced exact Lean theorem signatures for non-vacuous finite phase avoidance and complex-power normalization. No Lean files were edited; `dpac_of_LI` remains avoided. |
| 10 | `AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md` | `RIGOROUS_REDUCTION` | Drafted precise registry and paper-section edits for the ramified correction divisor proposition, with an explicit no-Theorem-B-impact boundary. No paper/registry edits were made in this wave. |

## Main Findings

### H1 Rank-One Reciprocal Derivatives

The rank-one H1 target remains:

```text
R_E,1(T) = sum_{T < |gamma| <= 2T, simple}
          |L'(E,1+i gamma)|^(-1) = o(T^2).
```

Wave 2 source-checked plausible imported routes and did not find a closure.
The exact sufficient theorem candidates are now:

```text
Pointwise anti-small derivative:
|L'(E,1+i gamma)| >= h(T) log(T)/T, h(T) -> infinity,
for all relevant simple zeros in the dyadic shell.
```

```text
Layer-cake tail:
int_1^infinity #{T < |gamma| <= 2T:
                 |L'(E,1+i gamma)|^(-1) >= V} dV = o(T^2).
```

```text
Separated-zero plus bad-set budget:
sum_{gamma in F_T} |L'(E,1+i gamma)|^(-1) is small enough,
and sum_{gamma notin F_T} |L'(E,1+i gamma)|^(-1)=o(T^2).
```

The attractive but killed shortcuts are also clearer: selected contour heights,
zero counting, many-simple-zero theorems, spacing alone, and square-moment or
spacing inputs for PV do not imply the reciprocal budget.

### H1 Moving PV

The actual moving PV theorem must use the true coefficients:

```text
a_gamma(E,W) = W_hat(i gamma) / L'(E,1+i gamma).
```

The needed theorem is a dyadic actual-coefficient shell estimate strong enough
to imply `Z_PV(u)=o(u^r)` in the legal moving windows. Conjugation symmetry,
Mellin decay, non-lattice spacing, and H2 branch damping do not close it.

### H1 Finite-Box Package

The finite-box H1 theorem is now assembled as a conditional theorem section.
It has clean inputs:

- legal exponential Perron heights;
- `H-left` and Li-Zaharescu-routed horizontal height as contour inputs;
- simple-zero reciprocal target `R_E,1(T)=o(T^2(logT)^(r-1))`;
- rank-one specialization `R_E,1(T)=o(T^2)`;
- multiple-zero effective-degree `< r`, or explicit retention/filtering/averaging.

This is paper-ready as a conditional theorem, not as a promoted theorem.

### H2 Endpoint Closure

H2 split into one closed component and one live blocker.

Closed component:

```text
S_sym,W(K) = C_sym,E
             - (1/log K) sum_{rho != 1}
                 m_rho K^(rho-1) W_hat(rho-1)
             + O((log K)^(-2)) + O(K^(-eta)),
```

with `kappa_sym=0` under the standard adjoint/Sym2 reconciliation. The source
anchors are Iwaniec-Luo-Sarnak and Hoffstein-Lockhart as quoted in Agent 06.

Open component:

```text
S1-CutPlane-LogGrowth(E,W,eta).
```

This theorem must legalize the S1 cut-plane contour shift with log growth on
horizontals, integrability on left/cut lips, local cut remainder summability,
and explicit handling of right branches. Without it, full pointwise H2 is not
promoted.

### GL1 Sharp Cutoff

GL1 has the same moving-PV obstruction in different clothes. Target-zero
simplicity and off-target simplicity remove higher-order residues but still
leave the simple-zero off-target aggregate for
`K^w/(w L(rho+w,chi))`. The sharp theorem remains conditional on
`GL1-ActualMovingShellPV` plus rectangle/truncation control.

### B+, DPAC, Delta

B+ is now compute-plan complete for the tier-1B bridge, but no compute was run.
The bridge remains classification, not positivity.

DPAC now has exact Lean patch signatures for non-vacuous finite phase
avoidance and normalization. It remains a formal bridge plan, not a theorem.

Delta has a registry/paper patch plan for the ramified correction divisor and
axis-pole multiplicities. The plan explicitly preserves no Theorem B impact.

## Acceptance Check

Wave 2 satisfies the acceptance criterion by strict reduction and component
source closure:

- `S_sym,W` exact good-prime finite part is source-closed as a component.
- H2 as a whole is reduced to `S1-CutPlane-LogGrowth(E,W,eta)` plus right-branch handling.
- H1 rank-one is reduced to a sharper fixed-curve reciprocal-derivative theorem, with several tempting source routes killed.
- GL1 sharp cutoff is reduced to the same actual moving PV phenomenon, with no GL1-specific shortcut.

No theorem is promoted.

## Next Single Highest-Leverage Theorem Target

The next single highest-leverage theorem target is:

```text
EC/GL2 fixed-curve negative first reciprocal derivative moment
with bad-set budget:

For each fixed elliptic curve E/Q and dyadic T, prove a separated-simple-zero
bound plus complement budget strong enough to imply
R_E,1(T)=o(T^2)
for analytic-rank-one H1.
```

This target is higher leverage than more numerical EC work because it attacks
the remaining load-bearing H1 wall directly. The near-term H2 target
`S1-CutPlane-LogGrowth(E,W,eta)` is the cleanest way to finish H2, but even a
closed H2 theorem does not produce pointwise EC stabilization without H1.

## Updated Files

```text
handoff-2026-05-11-breakthrough-wave-2/DISPATCH_MANIFEST_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
HANDOFF.md
index.md
L1_index.md
log.md
L2_facts/farey-claim-ledger.md
```
