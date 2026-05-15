---
schema_version: 2
title: "Palm-Wall Fresh-Angle Scoping (Outside Halo-Route Work)"
type: scoping
domain: project
tier: working
confidence: 0.70
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff pro.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-14-palm-wall-revisit/PRO_DOSSIER_AUDIT_AGAINST_HALO_INSIGHT_2026-05-14.md
  - https://arxiv.org/abs/2310.03949
  - https://arxiv.org/abs/1306.0854
  - Heap-Soundararajan, negative moments / log-distribution methods
  - Bui-Keating-Smith fixed-conductor refinements (literature class)
  - Conrey-Farmer-Keating-Rubinstein-Snaith, ratios conjecture
supersedes: []
superseded-by:
tags: [palm-wall, fresh-angle, scoping, no-go-tagged, halo-orthogonal]
---

# Palm-Wall Fresh-Angle Scoping

Status: `SCOPING_ONLY`.

No theorem promoted. No new direct-break route source-closed.

## Scope

The Palm-wall direct break has been NO-GO since 2026-05-12. The GPT-5.5 Pro Extended dossier (`handoff pro.md`) catalogued all then-known routes and their kills. The halo route bypasses the wall but does not break it.

This memo enumerates **candidate fresh angles outside today's halo-route work**, with cost/probability and explicit kill-criterion check against the Pro dossier trap list. No source closure is claimed.

Outcome: 5 candidates surveyed. **None is a high-probability break.** Two (Candidates D, F) are not in any existing kill list and merit a low-cost discovery pass before being ruled out.

## Candidate Summary Table

| Candidate | Description | Pro-dossier trap status | Probability | Cost |
|---|---|---|---|---|
| A | CFKRS ratios algebraic skeleton at q=3 | Not in trap list; conditional only | 0.04 | weeks |
| B | Bui-Keating-Smith finite-T determinantal refinement for fixed E | Item 4 of Challenge 1 (open) | 0.08 | months |
| C | Heap-Soundararajan log-distribution for fixed weight-2 newform | Subsumed by BFMT — already used | 0.02 | wasted |
| D | Hybrid absolute/signed contour decomposition by cluster size | Not in trap list | 0.18 | 2-4 weeks |
| E | Signed reciprocal-tail moment | Not in trap list (kill-list bypass) | 0.06 | 2-3 weeks |
| F | Twist-family upper-bound transfer to fixed E (Linnik dispersion) | Borderline trap (averages); novel hybrid | 0.05 | 3-5 weeks |

Probabilities are subjective Bayesian; sum is not constrained to 1.

## A — CFKRS Ratios Algebraic Skeleton

**Idea.** The Conrey-Farmer-Keating-Rubinstein-Snaith ratios conjecture predicts every shifted-moment integrand for L-functions, including negative orders. Even though the full conjecture is open, its **algebraic recursion** is rigorous and matches lower-order moments. Extract from the recursion an unconditional upper bound on the q=3 shifted negative moment.

**Trap check.** Not in Pro dossier kill list. Not "averaging over E" because ratios is per-form. Not "fixed-test correlation" because shifted moments are the target itself. Survives.

**Probability.** Low (0.04). Ratios recursion has been mined for two decades; no unconditional negative-moment upper bound at fixed weight-2 newform with the needed `T^{q+1/2+eps}` strength has emerged.

**Cost.** Weeks of literature spelunking + recursion algebra. Risk of zero output is high.

**Next action.** Skip unless a researcher with prior CFKRS experience flags a specific lemma.

## B — Bui-Keating-Smith Finite-T Determinantal Refinement For Fixed E

**Idea.** Pro dossier Challenge 1 item 4 explicitly requests: "A new finite-T determinantal/negative-association substitute for fixed EC/GL2." Bui-Keating-Smith built such refinements for `zeta` with finite-T error bands matching the conjectural local model. Transcribe their finite-T setup to fixed weight-2 newform.

**Trap check.** Item 4 of Challenge 1 — open by Pro dossier's own framing. Survives trivially.

**Probability.** Moderate-low (0.08). The transcription is technically reasonable; the obstruction is that BKS-style refinements give finite-T error at the **scale of typical local statistics**, not at the singular `1/log T` scale that the Palm box law needs. Bridge from typical-scale to singular-scale is the unsolved problem.

**Cost.** Months. Requires deep BKS apparatus knowledge.

**Next action.** Skip unless a collaborator with BKS expertise is available. Not worth dispatching cold.

## C — Heap-Soundararajan Log-Distribution For Fixed Weight-2 Newform

**Idea.** Selberg CLT + Radziwill-Soundararajan upper bounds for the distribution of `log|L|` on the critical line give a tail estimate for `|L|^{-q}`. Apply at the shifted point `1/2 + 1/log T + i gamma` to close `Degree2WeakShiftedNeg_q(E)`.

**Trap check.** This is exactly what BFMT (`arxiv:2310.03949`) does, transcribed to fixed weight-2 newform in `BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`. The Heap-Soundararajan / Radziwill machinery is already inside the BFMT closure. So this candidate is **subsumed by existing work**, not fresh.

**Probability.** Effectively zero as a new angle (0.02 for "maybe missed a sharpening").

**Cost.** Wasted unless a specific BFMT bookkeeping line is identified.

**Next action.** Drop.

## D — Hybrid Absolute/Signed Contour Decomposition By Cluster Size

**Idea.** The H1 contour bound applies triangle inequality globally, yielding `R_B` as a positive `l^1` sum. The halo route replaces triangle inequality with a signed-residue identity, killing absolute values everywhere. **Hybrid:** apply triangle inequality only for small clusters (m <= M_0 where pair-correlation tools work), and signed cancellation for the tail (m > M_0).

Concretely, decompose

```text
sum_(rho in B_E(T,c)) |L_E^*'(rho)|^(-1) ?=? sum_(small clusters) |.| + sum_(large clusters, signed) ...
```

with the second sum bounded by the divided-difference contour identity at finite shift, **not by a Palm box law**.

**Trap check.** Pro dossier trap 5 ("fixed finite cluster truncation without a hard theorem") forbids absolute-value truncation alone. The hybrid is different: it does **not** truncate the absolute sum; it splits between absolute (small m, source-closed via pair correlation when m=1, m=2) and signed (large m, source-closed via halo identity). Not literally in trap list.

**Caveat.** The hybrid requires that the contour bound can be split this way without the halo route's offcentral-only restriction degrading to pointwise H1. This is not obviously true: the halo identity gives **offcentral** H1, not pointwise. If the original pointwise H1 contour bound cannot accept signed residues even for the large-m tail, the hybrid fails immediately.

**Probability.** 0.18 — the highest in this table. If the contour decomposition works algebraically, the analytic content is already in repo (small-m pair correlation source-closed; large-m signed identity is the halo route core).

**Cost.** 2-4 weeks for a contour-bound feasibility check + small-m source close.

**Next action.** Most cost-effective candidate. Dispatch a focused 1-week research probe asking: "**can the H1 contour bound at finite shift `delta` be split into (small-m, abs) + (large-m, signed) terms, both bounded with source-closed inputs?**" If feasibility check is YES, escalate to full audit. If NO, kill.

## E — Signed Reciprocal-Tail Moment

**Idea.** Pro dossier Challenge 3 (direct reciprocal tail) was killed in absolute form. The signed analogue

```text
sum_rho s_rho |L'(E,rho)|^(-p),     s_rho in {-1, +1} algebraically determined,
```

may be bounded by an inverse-power test moment of `L` via cancellation, where the absolute-value version is not.

**Trap check.** Not in trap list. Trap 7 ("direct reciprocal derivative `l^1` tail") concerns the absolute version.

**Probability.** Low (0.06). Identifying the right sign pattern `s_rho` is the crux. The natural choice — sign of `L^{(2)}(rho)` or `Re(1/L'(rho))` — does not have a known per-zero distribution result.

**Cost.** 2-3 weeks of contour-bound algebra.

**Next action.** Skip unless Candidate D's feasibility check returns a specific sign assignment as a byproduct.

## F — Twist-Family Upper-Bound Transfer To Fixed E

**Idea.** Average the rooted box law over imaginary-quadratic twists `E^d` for `d` in a dyadic range. For each twist, `L(E^d, s)` is a different L-function; the wall lifts to a family. Heuristically the family average **is** bounded by Sato-Tate / Linnik-dispersion arguments. Identify the original `E` (i.e., `d=1`) among the twists via a fixed-`E` mollifier or positivity argument.

**Trap check.** Borderline. Pro dossier traps "averaging over E" but only when used to *prove* a fixed-E statement directly. The proposed angle uses twist averaging only as a **probe**; the actual transfer to `d=1` requires a separate per-form argument. Novel hybrid, not literally in trap list.

**Probability.** Low (0.05). The probe-to-transfer step is essentially the Bombieri-Friedlander-Iwaniec amplification trick. There is no clean precedent for transferring a twist-family rooted box law to a single member.

**Cost.** 3-5 weeks. Needs L-function-of-twist family expertise.

**Next action.** Skip unless Candidate D fails.

## Net Recommendation

Six candidates surveyed. Five are low-probability; one (Candidate D, hybrid contour decomposition) is **0.18 with 2-4 week cost**, and is **not in any existing kill list**.

If a direct-break attempt is desired, the recommended single action is:

```text
Dispatch a 1-week feasibility check on Candidate D:
  Can the H1 contour bound at finite shift be split into
  (small-m, absolute, source-closed via pair/triple correlation) +
  (large-m, signed, controlled by halo divided-difference identity),
  with both pieces source-closed under existing Wave 4 inputs?
```

If the feasibility check returns NO, the Palm wall is **structurally stable** under all currently visible angles outside the halo route, and the rational allocation is to continue Door A closure on the halo bypass.

If the feasibility check returns YES, escalate to a 3-4 week full audit.

## Boundary

Promote:

```text
Six fresh-angle candidates surveyed against Pro dossier trap list.
Candidate D (hybrid contour decomposition) is the only one with
probability > 0.1 and cost < 1 month that is not in the kill list.
```

Do not promote:

```text
Any candidate as a source-closed wall break.
Hybrid contour decomposition feasibility (not yet checked).
Twist-family transfer or signed reciprocal tail as viable routes.
Heap-Soundararajan as a fresh angle (subsumed by BFMT).
```

Confidence in the recommendation: 0.70 that Candidate D is the right single probe to spend a week on; 0.30 that even D is ultimately a no-go and the wall stays.
