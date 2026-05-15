---
schema_version: 2
title: "Degree-2 Weak Shifted Negative Moment q=3 Source-Close Brief"
type: source-close-brief
domain: project
tier: working
confidence: 0.74
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff pro.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/WAVE4_PROMOTION_PLAN_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md
  - https://arxiv.org/abs/2310.03949
supersedes: []
superseded-by:
tags: [palm-wall, shifted-moment, q3, source-close, k-three-halves, depends-on-wave4]
---

# Degree-2 Weak Shifted Negative Moment q=3 Source-Close Brief

Status: `BRIEF_ONLY — DEPENDS_ON_WAVE_4`.

No theorem promoted. Target is one **conditional** sub-task of the Palm-wall Pro dossier stack (`handoff pro.md` Challenge 2). Closure is independent of the rooted box law (Challenge 1).

## Target

```text
Degree2WeakShiftedNeg_3(E):
  sum_(rho in S_E(T)) |L_E^*(rho + 1/log T)|^(-3)
    <<_(E, eps) T^(7/2+eps).
```

`S_E(T) = {simple critical zeros rho = 1/2 + i gamma : T < |gamma| <= 2T}`.

## Why This Closes Half The Palm Stack

The Holder reduction (`handoff pro.md` §"Holder Reduction") splits the bad-set budget into

```text
R_B(T,c) <= T^o(1) alpha (sum_B X(rho)^q)^(1/q) (sum_B W_A(rho)^p)^(1/p).
```

With `q = 3, p = 3/2`:

- `Degree2WeakShiftedNeg_3` controls the first factor.
- `PrimeScaleRootedPalmBox_(beta>3/2)` controls the second factor.

The second factor remains the **Palm wall** — no fresh angle here. The first factor is the **paired sub-task** and, unlike the Palm box law, has a concrete BFMT route. Source-closing it is structurally independent of the wall: it reduces the bad-branch problem to **only** the Palm box law.

In other words, today's brief is a half-wall: it does not break the Palm wall, but it removes one of the two conditional inputs that the Pro dossier requires.

## Reduction To Wave 4 Inputs At k=3/2

The q=2 audit (`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md`, `CONDITIONAL_PASS_FOR_SHIFTED_Q2`) closes at `T^{5/2+eps}` via the BFMT second-branch exponent computation

```text
2k = q, 4k = 2q,
exponent = 1 + 2k * (4k-A)/(4k-A+B),
A = a(2d-1)/r = 1 + O(eps),
B = 2d-1 = 1 + O(eps),
```

with the fixed-conductor flip `log C_E(t) = 2 log T + O_E(1)`.

At `k = 3/2`, `2k = 3`, `4k = 6`:

```text
(4k - A)/(4k - A + B) = (6 - 1)/(6 - 1 + 1) = 5/6,
exponent = 1 + 3 * 5/6 = 1 + 5/2 = 7/2.
```

Target met. So `Degree2WeakShiftedNeg_3(E)` is structurally identical to the q=2 audit modulo the conductor-flip multiplier `4k = 6` instead of `4k = 4`.

The conditional inputs are the same family as q=2, lifted to k=3/2:

```text
GL2-BFMT-PrimePolynomialLowerBound(E)               [q-independent algebra]
ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=3/2)
fixed-newform RH / explicit-formula normalization
```

The q=2 Wave-4 sub-task 2.4 audit (`WAVE4_PROMOTION_PLAN_2026-05-14.md`) source-closes the analogous inputs at `k=1`. The q=3 closure needs the same inputs at `k=3/2`.

## Risk Audit At k=3/2 Vs k=1

Three trip-wires from the Wave-5 NO-GO that survive at higher k. All bear watching:

| Trip-wire | k=1 status (q=2) | k=3/2 status (q=3) |
|---|---|---|
| Small-block sign condition `a(2d-1) > 2k` (Wave 5 L38-46) | Needs `a > 2`, unavailable. Routed via second branch (Prop 2.6/2.7). | Needs `a > 3`, also unavailable. **Same routing applies** — second branch exponent 7/2 < target. |
| BFMT support `sum_h ell_h beta_h + s_(j+1) beta_(j+1) <= 1 - loglog T/log T` | Holds because `s_0 << log T/loglog T`. | Same support condition, but each block term scales with `k`. At k=3/2, factor `exp(O_E(s_0 k))` = `T^o(1)` survives only because `s_0 = O(log T/loglog T)`. **Verify polylog `(log T)^{O_E(k)}` overhead.** |
| Zero-sampling factorial `s_0! ~ (log T)^{O(s_0)}` | Folded into `T^o(1)`. | Same fold; **but** the coefficient `(log T)^{O_E(s_0 k)}` is `k`-linear in the exponent. Net `T^{o(1)}` only if `s_0 k loglog T = o(log T)`, equivalent to `k loglog T = o(loglog T · log T / log T) = o(1)`. **Borderline pass at k=3/2 with explicit `O_E(1)` overhead.** |
| Conductor-flip second-branch power `2k * (4k-A)/(4k-A+B)` | `2 * 3/4 = 3/2`. Total exponent `5/2`. | `3 * 5/6 = 5/2`. Total exponent `7/2`. **Matches target.** |

The decisive new risk is the **polylog overhead from `k`-linear bookkeeping**, not a new structural obstruction. There is no `2k > 2` threshold that breaks the routing at k=3/2.

## Headline Cost / Schedule

| Step | Cost |
|---|---|
| Wait for Wave 4 k=1 audit to land (sub-task 2.4 of `WAVE4_PROMOTION_PLAN_2026-05-14.md`) | 7-10d (in flight) |
| Lift k=1 audit → k=3/2 audit (same template, conductor-flip `4k = 6`, polylog bookkeeping) | 3-5d |
| Adversarial pass + MIMO check | 1d |
| Total after Wave 4 lands | **4-6d** |

If Wave 4 returns a clean `T^{5/2+eps}` for q=2 in the next sprint, q=3 closure follows mechanically and adds **<1 week** to the existing critical path.

## Probability And Up-Side

| Scenario | Probability | Net effect |
|---|---|---|
| q=2 audit lands clean → k=3/2 lift succeeds → `T^{7/2+eps}` conditional | 0.55 | One half of Pro dossier Challenge 2 closed (conditional on same Wave 4 inputs as Door A). Palm wall reduces to Challenge 1 only. |
| q=2 audit lands clean → k=3/2 polylog overhead exceeds `T^{eps}` margin | 0.20 | Need explicit `(log T)^{O_E(1)}` recovery; up-side at `T^{7/2+O(log log T)}`, still inside `T^{7/2+eps}` after relabeling. |
| q=2 audit returns NO-GO at sub-task 2.4 | 0.20 | q=3 brief is moot; Door A and Palm-wall-Challenge-2 both stall. |
| Hidden small-block sign trip at k=3/2 not seen in q=2 | 0.05 | Real risk: would force `k <= 1` boundary. Need explicit second-branch routing verification at k=3/2. |

Net probability of clean q=3 closure: **~0.55**, conditional on the q=2 Wave-4 audit landing. The downside scenarios are mostly survivable (relabeling, retry); only the fourth scenario forces a route change.

## Recommended Action

1. **Do not dispatch independent agents on q=3 right now.** It is downstream of the Wave 4 k=1 audit which is in flight. Wait for that to land.
2. After Wave 4 q=2 closes (estimated within sub-task 2.4 of `WAVE4_PROMOTION_PLAN_2026-05-14.md`, 7-10d), file a follow-on audit memo titled `DEGREE2_WEAK_SHIFTED_NEG_Q3_AUDIT.md` with template copied from the q=2 audit and conductor-flip arithmetic updated to `4k=6`.
3. Adversarial pass: dispatch MIMO on the q=3 memo identically to today's halo-chain adversarial layer; cost negligible (~$0.02).
4. If clean: Pro dossier Challenge 2 is conditionally closed. The Palm wall reduces to Challenge 1 (the rooted box law) alone. This **does not break the wall** but removes one of its two pillars.

## Boundary

Promote:

```text
The structural BFMT route for Degree2WeakShiftedNeg_3 at k=3/2 has the
correct second-branch exponent 7/2 and is mechanically downstream of the
in-flight Wave 4 k=1 audit. Risk is concentrated in polylog overhead, not
in any new structural obstruction.
```

Do not promote:

```text
Degree2WeakShiftedNeg_3(E) as proved or conditional yet.
Independent k=3/2 closure ahead of the q=2 audit landing.
Closure of the Palm wall via this brief — this is only half the wall.
```

Confidence: 0.74 that the brief's reduction is correct; 0.55 that the audit closes cleanly after Wave 4 lands.
