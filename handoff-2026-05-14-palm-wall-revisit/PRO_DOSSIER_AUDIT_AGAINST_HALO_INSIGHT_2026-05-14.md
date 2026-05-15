---
schema_version: 2
title: "Pro Dossier Audit Against Today's Halo / Signed-Residue Insight"
type: audit
domain: project
tier: working
confidence: 0.82
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff pro.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/LEAN_SIGNED_VS_ABSOLUTE_GADGET_2026-05-14.md
  - primes-equispaced/formal-conjectures/SignedVsAbsoluteResidueGadget.lean
supersedes: []
superseded-by:
tags: [palm-wall, halo, signed-residue, audit, no-new-leverage]
---

# Pro Dossier Audit Against Today's Halo / Signed-Residue Insight

Status: `NO_NEW_LEVERAGE_FOUND`.

No theorem promoted. Wall remains as-stated in `handoff pro.md`.

## Question

Does today's signed-vs-absolute residue insight (Lean round-9 gadget, halo plan §2.2) expose any new attack surface inside the Pro Extended dossier's reductions, kill-list, or trap-list?

## One-Line Answer

No. The signed-residue identity is **structurally orthogonal** to the wall. It sidesteps `R_B` rather than tames it. The Pro dossier's reductions, the Holder exponent arithmetic, the failed-route catalogue, and the q=3 mainline task all remain valid and unchanged.

## Why The Insight Does Not Help The Wall

The wall is `R_B(T,c) = sum_(rho in B) |L_E^*'(rho)|^(-1)`, a positive `l^1` sum over bad-set zeros.

The two-zero collision gadget (Lean round-9, halo plan §2.2) proves:

```text
abs-residue sum   diverges as poles collide,
signed-residue sum converges to (f/h)'(a).
```

So absolute and signed sums differ by an arbitrary multiplicative amount in the collision regime. This says only that the absolute-value step (triangle inequality applied to the contour integral) is **lossy near close clusters**, which is the very thing the wall encodes. The insight confirms the wall is real for `R_B as a positive quantity`; it does not produce a new bound on `R_B`.

Stage 0 of the halo plan (in `HALO_UNCONDITIONAL_PLAN_2026-05-12.md`) makes this explicit:

```text
A deterministic two-zero example shows R_B = sum |1/L'(rho)| (positive l^1 budget)
is genuinely strictly larger than the signed residue sum, by an arbitrary
multiplicative amount.
```

Translation: the wall is `R_B > arbitrary x signed sum`. The halo route's escape is **drop R_B from the H1 reduction** and use the signed sum directly, which the offcentral contour bound permits via the divided-difference identity. The wall is left standing for any analysis that still requires `R_B`.

## Cross-Check Of Pro Dossier Reductions

Re-checking each promoted reduction:

| Reduction | Affected by signed insight? |
|---|---|
| Local cluster-shift derivative comparison (CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md) | No. Pointwise identity; uses absolute values cleanly because the local poles are *not* collapsing in the inequality direction. |
| Holder arithmetic (`mu_q/q + nu_p/p < 2` with `q=3, p=3/2`) | No. Pure exponent algebra independent of signed/absolute structure. |
| `R_F(T,c) << T^(3/2+eps)` separated branch | No. Separated zeros, no Palm structure. |
| Bad branch reduction `R_B <= T^o(1) alpha sum_B W_A(rho) X(rho)` | No. Holder step is independent of signed structure. |
| `R_B << T^(11/6+eps+o(1))` final exponent | No. Pure consequence of the two conditional inputs. |
| `Degree2WeakShiftedNeg_3(E)` target `T^(7/2+eps)` | No, but see Lane 3 brief. |
| `PrimeScaleRootedPalmBox_beta` for `beta > 3/2`, all m, summable constants | No. This *is* the wall. |

## Cross-Check Of Pro Dossier Kill-List

Re-checking each entry of the failed-routes list against the signed insight:

| Failed route | Does signed insight reopen it? |
|---|---|
| Restricted n-level density (RS/Hejhal support floor) | No. Support floor is on the test function, independent of absolute/signed of `1/L'`. |
| Pair-layer only / `m=1` | No. Higher cluster summability is the gap, signed cancellation is at the contour level not the cluster level. |
| Finite cluster truncation `n_A(rho) <= M` | No. Missing hard cap on near-root clusters; signed insight does not bound multiplicities. |
| Direct reciprocal tail bypass | **Mild reopening**: see below. |

## Mild Mild Mild Reopening: Reciprocal Tail Via Signed

The direct-tail no-go in the Pro dossier asks for

```text
sum_(rho simple) |L'(E,rho)|^(-p) = o(T^(p+1)/(log T)^(p-1)),    p>1.
```

as a Palm-free route. This is a positive moment of an absolute value. The signed-residue identity (round-9 gadget) shows that the absolute-value version blows up in the collision limit even when the underlying signed contour residue is bounded. So the direct-tail target is essentially as hard as the wall.

However, a **signed analogue** of the direct tail — `sum_rho s_rho |L'(E,rho)|^(-p)` for some choice of signs `s_rho in {-1,+1}` — *might* be bounded by an inverse-power test moment of `L` because of cancellation. No such target appears in any kill list. It is purely speculative.

This is not a wall-break candidate, but it is **the only non-trivial reading** of the signed insight against the Pro dossier. It is recorded as a candidate fresh angle in:

- `PALM_WALL_FRESH_ANGLE_SCOPING_2026-05-14.md` (Candidate E: signed reciprocal tail).

## Conclusion

The Pro dossier's wall stands. The signed-vs-absolute residue insight is the basis for the halo bypass and adds **no new leverage** to a direct wall-break attempt, except for a single speculative candidate (signed reciprocal tail) noted in the Lane-1 scoping memo.

If the goal remains a *direct break* of the Palm wall, today's halo-route work does **not** advance it. Recommendation: stay on the halo bypass; treat any direct-break attempt as research insurance, not the mainline.
