---
schema_version: 1
title: "Koyama claim-safe paper outline"
date: 2026-05-11
type: outline
tier: working
confidence: 0.9
status: OUTLINE_ONLY_NO_THEOREM_PROMOTION
sources:
  - handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_CLAIM_AUDIT_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_normalization_no_go_2026-05-11.md
tags: [koyama, paper-outline, claim-safe, ndc]
---

# Koyama claim-safe paper outline

## Working title

Corrected constants and obstructions in the Saar-Koyama NDC program.

## Paper posture

Do not write the paper as a closed NDC theorem.  The claim-safe paper is:

1. corrected GL(1) constant: `1/zeta(2)` is replaced by `e^{-gamma}`;
2. local Perron residue at the target zero;
3. corrected `B_infty` formula with the missing terms included;
4. exact statement of the remaining shifted Perron obstruction;
5. EC numerical falsification/no-go for the tested sharp-cutoff finite
   bad-prime class.

This gives a useful note even if the global Perron-leading theorem remains
open.

## Claim register

| Claim | Paper status |
|---|---|
| AK constant `E_K * log K -> L'(rho,chi)/e^gamma` | State only under the exact AK/DRH hypotheses and after embedding the verified AK quote/page/eq. |
| Local residue at target zero | Proved local algebra. |
| Global Perron-leading `c_K = log K/L' + o(log K)` | Defer unless shifted off-target residue control is proved or cited. |
| NDC limit `D_K -> e^{-gamma}` | Conditional corollary only: AK + global Perron-leading. |
| `B_infty` formula | Proved with `psi`, `BPC1`, `BPC2`, and `T_{>=3}` included. |
| EC universality `D_K^E*zeta(2)->1` | Falsified numerically for the tested curves and sharp cutoff. |
| EC finite bad-prime rescue | No-go for the tested sharp-cutoff class; per-curve constants leave within-curve CV invariant. |

## Section outline

1. Introduction.
   State the historical constant error, the corrected constant, and the exact
   obstruction.  The abstract must include "conditional on shifted Perron
   residue control" if the NDC limit is mentioned.

2. Source-grounded definitions.
   Define Koyama/Saar objects, normalizations, branch choices, and cutoff.
   Include the mandatory citation protocol: every external theorem gets
   page/equation number and short verified quote in an appendix or footnote.

3. Corrected AK constant.
   Present the `e^{-gamma}` constant.  Do not rely on inherited memory of AK
   2023; embed the page 235 / equation (1.4) quote from the verified proof
   packet before correspondence or submission.

4. Local Perron residue.
   Prove the target-zero double-pole local contribution.  End the section with
   the precise global gap: off-target zeros, including possible higher-order
   residues, must be controlled.

5. The shifted Perron obstruction.
   State the missing theorem as a proposition/conjecture.  Include the
   sufficient package from the GPT-5.5 synthesis:

```text
all crossed off-target zeros are simple,
Z_simple(K,T_K)=o(log K),
and the shifted rectangle/truncation terms are o(log K).
```

6. Corrected `B_infty`.
   Give the explicit formula with all terms.  Do not abbreviate to the old
   incomplete form.

7. EC computations and no-go.
   Report the `K=1000000` negative evidence and the finite bad-prime no-go.
   Use `L2E_partial^rank` wording, not completed/global `L(E,2)`.

8. Outlook.
   List the next theorem targets: shifted Perron control, smoothed EC
   diagnostics, and possible broader no-go classes.

## Submission readiness gate

Before external circulation:

- run a citation-closure pass on every named source;
- embed the AK quote rather than merely citing inherited notes;
- remove all "proved NDC" phrasing unless the shifted Perron theorem is closed;
- rerun the claim audit on the final draft.
