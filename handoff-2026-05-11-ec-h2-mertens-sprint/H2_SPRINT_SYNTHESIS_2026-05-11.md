---
schema_version: 1
title: "H2 smoothed EC-Mertens sprint synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2A_LITERATURE_AUDIT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2D_NUMERICAL_DIAGNOSTICS.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
tags: [ec-ndc, h2, smoothed-mertens, synthesis, claim-safe]
---

# H2 Smoothed EC-Mertens Sprint Synthesis

No theorem was promoted.

The naive pointwise H2

```text
log P_E,W(K) = -rank(E) log log K + B_E,W + o(1)
```

is not claim-safe. The sprint produced a precise conditional replacement and a
clear obstruction map.

## Verdict

Use H2 only as a `RIGOROUS_REDUCTION`.

The coefficient `-rank(E)` is plausible for the exact Agent 3 local factors,
but only after mandatory local bookkeeping:

```text
log P_E,W(K)
 = S_1,W(K) + (1/2)S_sym,W(K) - (1/2)M_good,W(K)
   + R_ge3,W(K) + B_bad,E,W(K).
```

The final `-r` coefficient comes from cancellation between:

- the trace term `S_1,W(K)`;
- the quadratic/symmetric-square term `S_sym,W(K)`;
- the universal prime-harmonic term `M_good,W(K)`.

Here `r=ord_{s=1}L(E,s)`. Replacing `r` by algebraic `rank(E)` needs BSD rank
equality or a per-curve rank verification.

## Agent Outcomes

| Agent | Status | Result | Decision |
|---|---|---|---|
| H2-A | `RIGOROUS_REDUCTION` | Audited sources do not prove pointwise smoothed H2 for Agent 3 factors. Sharp BSD-Mertens plus smoothing transfer would imply H2; Sheth-style finite-log-measure exceptional set is insufficient for pointwise H2. | Use as citation guardrail. |
| H2-B | `RIGOROUS_REDUCTION` | Exact local expansion derives the right coefficient conditionally; identifies the first-order trace and symmetric-square finite-part PNT inputs. | This is the main analytic theorem target. |
| H2-C | `NO_GO` | Naive `B+o(1)` pointwise H2 is unsafe because noncentral zeros can contribute oscillatory terms unless killed, averaged, or proved lower order. | Repair H2 before composing with H1. |
| H2-D | `AUDIT_ONLY` | Existing seven-point data match slopes roughly (`-1.02`, `0.04`, `-1.96` for ranks 1,0,2 at `alpha=0.75`), but tail fits are unsettled. | Numerics do not contradict H2, but do not prove it. |
| H2-E | `RIGOROUS_REDUCTION` | Packaged weakest useful theorem with exact constants, rank cases, and closure/falsification criteria. | Use as the current theorem template. |

## Repaired H2 Targets

### H2-limit, conditional

For fixed curve `E`, admissible kernel `W`, and `r=ord_{s=1}L(E,s)`:

```text
log P_E,W(K) = -r log log K + B_E,W + o(1)
```

provided the smoothed first-order EC prime finite part and the smoothed
symmetric-square finite part both exist, and offcentral zero/prime-shell terms
are `o(1)`.

### H2-osc, safer pointwise form

If offcentral zero terms are not proved lower order, use:

```text
log P_E,W(K)
 = -r log log K + B_E,W + Z_E,W(log K) + o(1),
```

where `Z_E,W` is an explicit almost-periodic zero term. This is the honest
pointwise target unless a smoothing explicit formula proves `Z_E,W=o(1)`.

### H2-avg

If `Z_E,W` persists, use a logarithmic average in `u=log K`:

```text
1/T int_T^(2T) (log P_E,W(exp u) + r log u) du -> B_E,W.
```

This may be easier to prove, but it forces the final EC smoothing theorem to be
averaged too.

## Main Open Discrepancy

H2-B and H2-C disagree in strength, not in bookkeeping.

H2-B suggests that for a smoothed log-product explicit formula, a noncentral
zero at `rho=1+i gamma` contributes roughly

```text
K^(i gamma) W_hat(i gamma) / log K,
```

so smoothstep plus summable zero weights could make it lower order.

H2-C warns that without that branch-cut calculation proved, the safe explicit
formula contains a persistent term

```text
c(gamma) K^(i gamma).
```

The next theorem sprint should resolve this exact issue: derive the smoothed
explicit formula for the prime-linear trace term and determine whether the
offcentral zero contribution is `O(1/log K)`, persistent, or only removable by
averaging.

## Literature State

The audit found no source-closed theorem proving H2 as needed.

Allowed citation-safe statement:

```text
Pointwise sharp BSD-Mertens for the exact local factors, plus an explicit
smoothing-transfer lemma, implies H2 with coefficient -ord_{s=1}L(E,s).
```

Disallowed shortcut:

```text
Sheth proves H2.
```

The audited Sheth result is exceptional-set/off finite logarithmic measure and
does not close the pointwise theorem needed here.

## Numerical State

The saved Agent 3 data are compatible with the slope:

| curve | rank | all-grid slope for `log P` vs `log log K` at `alpha=0.75` | target |
|---|---:|---:|---:|
| `37a1` | 1 | `-1.02388301209` | `-1` |
| `11a1` | 0 | `0.03851340902` | `0` |
| `389a1` | 2 | `-1.96099895387` | `-2` |

But the tail fit over `K>=100000` is not settled, especially for `389a1`.
Numerics support continuing the theorem route; they do not promote H2.

## Next Move

Do one focused theorem sprint:

```text
Smoothed explicit formula for S_1,W(K)=sum_p W(p/K)a_p/p.
```

Required output:

- exact contour/Mellin or Stieltjes formula;
- central-zero coefficient `(1/2 + kappa_sym/2 - r) log log K`;
- treatment of noncentral zeros: lower-order, explicit oscillatory, or averaged;
- compatible symmetric-square finite-part statement.

Do not spend more compute on EC universality until this offcentral-zero term is
settled or the theorem is intentionally weakened to an averaged result.

## Do Not Promote Unless

- H2 is stated with analytic rank `ord_{s=1}L(E,s)` unless BSD/rank equality is
  explicitly assumed.
- The quadratic/symmetric-square term is present.
- Bad-prime constants use the Agent 3 convention.
- Offcentral zero terms are proved lower-order, explicitly retained, or averaged.
- Any source claim has `curl + pdftotext + verbatim quote + page/eq`.
- H1 composition uses the same pointwise/averaged mode as H2.
