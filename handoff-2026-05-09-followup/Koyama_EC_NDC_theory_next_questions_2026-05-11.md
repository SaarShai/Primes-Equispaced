---
schema_version: 1
title: "EC NDC theory next questions"
date: 2026-05-11
type: research-plan
tier: working
confidence: 0.88
status: OPEN
sources:
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_normalization_no_go_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md
tags: [ec-ndc, elliptic-curves, normalization, no-go]
---

# EC NDC theory next questions

## Current decision

Stop testing finite bad-prime factors for the current sharp-cutoff grid.  In
the existing data all bad primes lie below the first grid point, so any finite
bad-prime multiplier is a curve constant and cannot change within-curve CV.
The best tested proxy,

```text
D*zeta(2)/L2E_partial^rank,
```

remains a finite good-prime proxy and fails the strict promotion gate through
`K=1000000`.

## What might still be real

The negative result is not "no GL(2) analogue exists."  It says the tested
sharp-cutoff, finite-local-factor class is too small.  Plausible remaining
directions:

| Direction | Testable question |
|---|---|
| Smooth cutoff | Does replacing the hard prime cutoff by a Mellin-smooth weight reduce within-curve drift? |
| Completed normalization | Do Gamma, conductor, period, or Tamagawa factors enter before the Euler-product truncation is compared? |
| Symmetric-square denominator | Is the right GL(2) object closer to a reciprocal symmetric-square Euler product than to the finite `L2E_partial^rank` proxy? |
| Rank/BSD derivative | At a zero of order `r`, does the partial product need the leading BSD Taylor coefficient rather than a rank-power finite proxy? |
| Complex-zero analogue | Should EC-NDC be evaluated at noncentral zeros instead of the BSD central point? |
| Broader no-go | Can one prove that all per-curve constant normalizations fail for any grid whose bad primes are below the first cutoff? |

## Next concrete tasks

1. Smoothed EC diagnostic.
   Recompute the three curves with a one-parameter smooth prime cutoff and
   compare within-curve CV against the sharp-cutoff floor.

2. Per-curve constant no-go lemma.
   Write the elementary lemma explicitly: multiplying each curve's trajectory
   by a constant preserves its within-curve coefficient of variation.  Then
   classify which proposed corrections are only per-curve constants on the
   existing grid.

3. Completed-factor audit.
   Build a citation-closed source packet for GL(2) reciprocal partial Euler
   products.  Do not name paper/year claims in dispatch prompts until the PDF
   quote protocol is satisfied.

4. Noncentral-zero probe.
   If zeros are available for 11a1/37a1/389a1, test whether the NDC product at
   the first few noncentral zeros has a more stable normalization than the BSD
   central point.

## Promotion rule

No EC normalization should be promoted unless it beats all of:

- max within-curve CV below the existing strict gate;
- cross-curve ratio materially below the current `1.42` proxy benchmark;
- stability when `K` is extended or smoothed;
- exact statement of whether the object is finite partial, completed global,
  or heuristic.
