---
schema_version: 2
title: "Adversarial MIMO review of halo chain (Stages 0, 1a-followon, 1b, 2-mult, RvM)"
type: adversarial-review
domain: project
tier: working
status: REVIEW
confidence: 0.85
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_NUMERATOR_M_T_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md
supersedes: []
superseded-by:
tags: [adversarial, mimo, halo-route, review, 2026-05-14]
---

# Adversarial MIMO Review — Halo Chain

Reviewer: Xiaomi MiMo v2-flash. Dispatched 2026-05-14 via `scripts/dispatch_mimo.sh`. Full input: all five 2026-05-14 audit memos concatenated; ~1200 lines; ~5800-byte response.

Overall MIMO verdict: **Conditional Pass**. Three sharpenings flagged.

## Evaluation table

| MIMO objection | Document | MIMO claim | Triage | Action |
|---|---|---|---|---|
| Factor-of-2 in RvM density | Door B arc-uniformity | `(log T)^2 / (2 pi R)`, not `(log T)^2 / (pi R)` | **MIMO incorrect** — missed two-sidedness | None |
| Hidden Laurent coefficient bound | Door A multiplicity | `|L^{(m)}(rho)/m!|^{-1} <<_E (log T)^{O(m)}` cited but not internally derived | **Fair** — internal cite to `H1_POSITIVE_RANK_CLOSURE.md` L221-230 is present but light | Tighten in any future revision |
| RvM uniformity of `C_E` | RvM multiplicity lemma | `c_E` may not be uniform in `T` | **Mostly addressed** — lemma already states `C_E` is conductor-and-weight only; "uniform for `T >= 2`" note worth adding | Small addendum |
| Stage 1b sigma > 1/2 not cited | M_T numerator audit | Doesn't confirm H1 base enforces `sigma > 1/2` | **Mostly addressed** — audit DOES cite `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md` L137-138, L169 | None (already in audit) |
| Stage 0 sign-flip risk | Residue-first audit | Make `partial Omega_T` explicit in final consumption | **Cosmetic** — already implicit in finite-box identity | Nice-to-have |

## Detail on the factor-of-2 disagreement

MIMO writes:
```
"the integral int_{R alpha}^{O(T)} ((log T)/(2 pi)) / r^2 dr
 evaluates to (log T)/(2 pi) · (1/(R alpha) - 1/O(T)),
 which is (log T)^2 / (2 pi R), not (log T)^2 / (pi R)."
```

Door B audit's computation:
```
sum_{|gamma_j - gamma_0| > R alpha} 1/|gamma_j - gamma_0|^2
  = 2 * int_{R alpha}^{T} (log T / (2 pi)) / r^2 dr     [TWO-SIDED]
  = (log T / pi) · (1/(R alpha) - 1/T)
  = (log T)^2 / (pi R) + O(log T / T).
```

The factor 2 comes from two-sidedness: for each `r > 0` there are zeros at both `gamma_0 + r` and `gamma_0 - r` near the cluster center (RvM density is per unit length in `t`, contributing to both sides of `gamma_0`).

MIMO took the integral one-sided. The Door B audit's answer `R/pi` (two-sided) is correct.

Numerical sanity: for `R = 1.5`, the two-sided answer gives `1.5/pi ~ 0.477`, `e^{2R/pi} ~ 2.60`. The one-sided answer would give `0.239`, `e^{2R/pi} ~ 1.61`. Both are bounded, neither blows up, so the qualitative conclusion (bounded variation, no T-dependence) is robust under this ambiguity. The downstream Door B claim is unaffected.

## Real sharpenings worth actioning

Two are genuine improvements, low cost, can be inlined in the original files when convenient:

1. **Door A multiplicity extension §"Laurent coefficient bound"**: add an explicit half-line derivation (Hadamard factorization + RvM zero-density gives `|L^{(m)}(rho)/m!|^{-1} <= (log T)^{C m}` for some absolute `C`).
2. **RvM multiplicity lemma §1 or §2**: add the note "constant uniform for `|gamma| >= 2`, equivalently `T >= 2`, with `O(log T)` error term independent of `T` and `r`."

Both are textbook adjuncts to the existing prose; ~5 lines each.

## Cosmetic suggestions noted but not actioned

- Stage 0 audit: explicit contour boundary annotation. The finite-box identity in `H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md` L48-79 already names the boundary; not material here.
- Stage 1b: explicit re-citation of `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md`. Already cited in §6 of Stage 1b.

## Overall judgement

MIMO's adversarial review is **net positive**. It surfaced two legitimate sharpening targets (Laurent bound explicit derivation, RvM uniformity note) and one incorrect objection (factor of 2). No new analytic gaps. The halo chain's Conditional-Pass status from the original audit chain is unchanged.

## Cost and confidence

- MIMO dispatch cost: ~$0.01-0.02 (mimo-v2-flash, ~8K output tokens against ~1200-line input).
- Confidence in MIMO's verdict: 0.75 (one clean error noticed by this reviewer, other points correct or partial).
- Recommendation: rerun adversarial reviews via MIMO on each major audit memo as a low-cost sanity layer (cost ~$0.02/doc).

## Boundary

Allowed:

```
The halo chain (Stages 0, 1a-followon, 1b, 2-mult, RvM) survives an
independent adversarial review with two minor sharpenings flagged
and one MIMO-side error. Conditional-Pass status unchanged.
```

Not allowed:

```
MIMO confirms the halo chain is unconditional.
MIMO confirms Door A is closed.
The factor-of-2 in the RvM density computation is genuinely wrong.
```
