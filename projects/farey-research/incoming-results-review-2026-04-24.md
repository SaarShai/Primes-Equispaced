---
schema_version: 2
title: Incoming Results Review 2026-04-24
type: project
domain: project
tier: working
confidence: 0.82
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/recent-outputs/library-experiments/K01_GEMINI_CV_GRANT_BULLETS.clean.md.txt
  - raw/farey-archive/recent-outputs/library-experiments/K02_GEMINI_KOYAMA_OUTLINE.md.txt
  - raw/farey-archive/recent-outputs/library-experiments/K03_MISTRAL_KOYAMA_ADVERSARIAL.md.txt
  - raw/farey-archive/recent-outputs/library-experiments/K04_COHERE_DOMINANCE_MINUS_ONE_QUESTIONS.md.txt
  - raw/farey-archive/recent-outputs/library-experiments/K05_GEMINI_W2_PARAGRAPH.md.txt
  - raw/farey-archive/recent-outputs/library-experiments/K06_COHERE_BUGFIX_SYM2_PARAGRAPH.md.txt
  - raw/farey-archive/recent-outputs/desktop-experiments/D01_M1B_DYNAMIC_PRIME_BIAS_FEASIBILITY.md.txt
  - raw/farey-archive/recent-outputs/desktop-experiments/W01_M1B_W2_REGRESSION_CANONICAL.md.txt
  - raw/farey-archive/recent-outputs/desktop-experiments/C01_M1B_MU_F_AUDIT.md.txt
  - raw/farey-archive/recent-outputs/library-experiments/T01_MISTRAL_W2_MECHANISM.md.txt
supersedes: []
superseded-by:
tags: [farey, compute-results, koyama, w2-prime, roadmap]
---

# Incoming Results Review 2026-04-24

Reviewed the incoming first-wave and Koyama-focused outputs through `K06`. This page records high-level consequences only; raw outputs remain unpromoted evidence until a later manual review approves them for correspondence or papers.

## Major Findings

- **W2 prime is the main mathematical lead.** `W01` exactly reproduces the 22-point fit:
  `E[C1^2] = 0.478539 - 0.166792 * rank + 0.472697 * log(N)`, with `R^2 = 0.809819`.
- The `log(N)` term is statistically live in the current fit: its 95% CI excludes zero, while the rank coefficient CI includes zero. Do not describe rank as significant in the multivariate model.
- **The C1 bugfix gate looks healthy.** `C01` found active M1B scripts aligned with `mu_E(p^2)=p` and `mu_Delta(p^2)=p^11`; stale old-formula text appears only as wrong-formula discussion.
- **Dominance of `-1` is blocked on definition, not compute imagination.** `D01` says full prime storage is impossible at `10^14+`, but dynamic segmented residue tallies are feasible for a narrow modulus/residue grid.
- **Koyama draft material is uneven.** `K05` is useful after softening; `K06` should not be used as written because it wrongly says the bug was Farey-sequence-related; `K02` is meta-outline only; `K03` is useful as an overclaim checklist but incomplete and too hesitant about the narrow raw Sym2 falsification.
- **T01 is heuristic only.** It points toward explicit-formula / Rankin-Selberg mechanisms, but fixed-weight EC gamma factors alone should not be treated as the source of `log(N)`, and rank leakage should be tied to the elliptic-curve central zero rather than vague Sym2 vanishing.

## Koyama-Relevant Conclusions

- Lead with gratitude and the grant/CV facts.
- Describe Saar as contributing computational number theory, Lean/formal verification, and reproducible large-scale verification.
- Present W2 prime as empirical state: log-conductor is live in the current 22-point fit, and rank-only phrasing is superseded.
- Present raw Sym2/Petersson falsification narrowly but firmly: the exact raw proportionality predicts the wrong 37a1 vs 389a1 direction; this does not rule out completed or Deligne-normalized variants.
- Keep Delta separate: `E[C1^2](Delta)=0.950231842` is an anchor, not part of EC rank behavior.
- Ask for the exact Dominance-of-`-1` setup before compute: modulus, residue classes, statistic, dynamic `x` grid, target range, baseline data/script, and acceptable output format.

Do not use:

- `K06` paragraph as written.
- Any claim that Dominance-of-`-1` is a Sym2 or Fourier `-1` term.
- Any claim that W2 prime is proved.
- Any claim that rank is significant in the current multivariate fit.
- Any claim that simple Gamma/Deligne corrections are globally impossible; only say simple variants tried so far did not resolve the discrepancy.

## Literature Anchors To Verify

- Prime-race framing: Rubinstein-Sarnak style prime number races and logarithmic density are the right background for Koyama's dynamic-`x` request.
- Elliptic-curve Euler products/rank scaling: Sheth's partial Euler product work is directly relevant background.
- Low-lying zeros and rank effects: one-level density in elliptic-curve families is the comparison class for rank leakage.
- Explicit formula / analytic conductor: use primary references before claiming any `log(N)` mechanism.

## Breakthrough Criteria

- W2 prime becomes a credible discovery only after leave-one-out diagnostics, bootstrap/leverage review, and at least one conductor-control extension survive.
- Dominance-of-`-1` becomes actionable only after Koyama provides the exact statistic.
- The Delta anchor becomes paper-ready only after a K-sweep and normalization-gate review.
- Theory claims need a mechanism that distinguishes archimedean conductor effects, arithmetic conductor effects, and central-zero leakage.

## Next Queue

Use [[projects/farey-research/active-agent-queue]] for dispatch. Treat all new outputs as unreviewed until Saar asks for review.
