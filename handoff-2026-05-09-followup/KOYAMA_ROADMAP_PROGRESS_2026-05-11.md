---
schema_version: 1
title: "Koyama roadmap progress"
date: 2026-05-11
type: synthesis
tier: working
confidence: 0.92
status: ROADMAP_ADVANCED_NO_THEOREM_PROMOTED
sources:
  - handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_claimsafe_paper_outline_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_email_to_Koyama_claimsafe_draft_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_theory_next_questions_2026-05-11.md
  - handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.md
tags: [koyama, roadmap, progress, claim-safe]
---

# Koyama roadmap progress

## What changed in this pass

The older 2026-05-09 handoff remains useful as a roadmap, but its theorem
language must be read through the 2026-05-10/11 claim-safe state.  This pass
advanced four roadmap items without promoting a new theorem:

| Roadmap item | Progress |
|---|---|
| A: Koyama paper | Added a claim-safe paper outline that reframes the note around corrected constants plus the shifted Perron obstruction. |
| B: Koyama email | Added a draft email that reports the corrected `e^{-gamma}` constant while explicitly asking about the missing Perron remainder theorem. |
| C: EC universality | Added theory next questions after the finite bad-prime no-go; next work moves to smoothing, completed factors, symmetric-square/BSD diagnostics, or broader no-go lemmas. |
| E: MERTENS-LB phase transition | Corrected the coarse "200-300K first flip" story: first post-`99991` positive is `N=108004`; first `T(N)>100` is `N=297331`; the spike is small-`k` Mertens driven. |

## Current decisions

No theorem promoted.

The paper/email track is still valuable, but the thesis is now:

```text
corrected GL(1) constants and exact obstruction, not closed NDC universality.
```

The full `D_K -> e^{-gamma}` statement remains a conditional corollary:

```text
AK/DRH constant + shifted global Perron-leading theorem.
```

The EC track remains negative for the tested class; finite bad-prime corrections
are no longer a good use of compute.

## New durable artifacts

- `handoff-2026-05-09-followup/Koyama_claimsafe_paper_outline_2026-05-11.md`
- `handoff-2026-05-09-followup/Koyama_email_to_Koyama_claimsafe_draft_2026-05-11.md`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_theory_next_questions_2026-05-11.md`
- `handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.md`
- `handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.py`

## Next best actions

1. Close citations before correspondence.
   The email draft must not be sent until the AK page/equation quote is embedded
   directly.

2. Attack shifted Perron directly.
   Look for or prove off-target residue control for `K^w/(w L(rho+w,chi))`,
   including higher-order residues.

3. Run smoothed EC diagnostic.
   This is the next concrete computational test after the finite bad-prime
   no-go.

4. Turn the Mertens phase probe into a lemma target.
   Isolate `1 + sum_{k<=K0} M(floor(N/k))/k` and prove/tune a tail envelope.
