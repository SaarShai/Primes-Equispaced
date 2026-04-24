---
schema_version: 2
title: W2 Prime Rank Plus Log Conductor Model
type: project
domain: project
tier: semantic
confidence: 0.8
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - projects/farey-research/data/W2_PRIME_FIT.json
  - projects/farey-research/data/PATH_B_20FORMS.csv
  - projects/farey-research/data/CONDUCTOR_CONTROL_37b.json
  - raw/farey-archive/state-docs/CLAIM_STATUS.md.txt
  - projects/farey-research/recent-results-review.md
supersedes: []
superseded-by: 
tags: [farey, w2-prime, rank, conductor, regression]
---

# W2 Prime Rank Plus Log Conductor Model

## Status

W2 prime is the current working replacement for the old pure-rank W2 story.

Empirical 22-point model:

`E[C1^2] = 0.478539 - 0.166792 * rank + 0.472697 * log(N)`.

Fit facts:

- `R^2 = 0.809819`
- rank-only `R^2 = 0.687348`
- `gamma_logN p = 0.0024066`
- `beta_rank p = 0.470742`

Interpretation: log-conductor is robust in this fit; rank remains a live mechanism question because conductor-control and rank-stress points show structure not explained by the old pure-rank mean fit.

## Evidence

- Low-conductor rank-0 EC cluster: mean `E[C1^2] = 1.886`.
- Rank-0 conductor 37 controls: mean `E[C1^2] = 2.052`.
- 37a1 rank 1 at conductor 37: `E[C1^2] = 2.189911545`.
- 389a1 rank 2: `E[C1^2] = 3.113923728`.
- 5077a1 rank 3: `E[C1^2] = 4.617`.

## Research Question

Find the mechanism coupling off-central C1 second moments to conductor and rank-related low-lying structure.
Candidate route: explicit formula terms plus central-zero residue leaking into off-central averages.

## Recent Review Notes

- The recent conductor-bias simulation is useful but heuristic: it suggests rank/conductor collinearity alone is probably too small to explain the observed `0.472697 * log(N)` coefficient.
- The Samba mechanism note gives a plausible route through `D_E(s) = sum |mu_E(n)|^2 n^{-s}`, Sym2-family averages, and Rankin-Selberg second moments. Treat it as a derivation target, not as proof.
- The OpenRouter Deligne/Gamma review argues simple archimedean or Deligne-period rescalings do not collapse the raw Sym2/Petersson ratio to the observed C1 second moments.
- Several recent M1 outputs used stale `1.087/1.175` baselines or returned `CANNOT COMPUTE`; they should not be used to update this model.

## Next Verification

- Recompute wider rank-0 high-conductor samples from LMFDB labels.
- Run leave-one-out diagnostics on the 22-point fit.
- Compare fixed-conductor or narrow-conductor rank contrasts before writing correspondence.
- Separate 200-zero exploratory values from 500-zero anchor values in every table.
