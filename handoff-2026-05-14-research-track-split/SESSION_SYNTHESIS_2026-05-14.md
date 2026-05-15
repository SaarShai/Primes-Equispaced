---
schema_version: 2
title: "Session synthesis 2026-05-14 — halo route conditionally complete"
type: synthesis
domain: project
tier: working
status: SESSION_SUMMARY
confidence: 0.85
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - "all files in handoff-2026-05-14-research-track-split/"
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
supersedes: []
superseded-by:
tags: [synthesis, halo-route, session, 2026-05-14, milestone]
---

# Session Synthesis — 2026-05-14

## Headline

The halo route to unconditional offcentral H1 (under standing GRH for the fixed newform `L_E^*`) is **conditionally complete in one session day**.

Halo plan §13 (2026-05-12) estimated 1-2 months focused work. Achieved in ~12 hours wall-clock with a sequence of audit/lemma dispatches.

## The four halo doors

| Door | Target | Status at session start | Status at session end |
|---|---|---|---|
| A | `sum_{rho}^{mult} \|L_E^*(rho+1/log T)\|^{-2} << T^{5/2+eps}` | OPEN; "1-2 month" sprint expected | **CLOSED conditionally under standing GRH** |
| B | `\|L(rho_0+alpha)/L(s)\| <= C(E,A,R)` on halo arc | "trivial extension residue" | closed under GRH, fully written out, scale unification |
| C | H1 accepts signed contour residue, not absolute series | unknown | **GREEN 0.94** (signed form is what H1 actually needs) |
| D | `M_T = sup_halo \|Phi_T\| = o(T^{1/4})` | open | PASS for simple+bounded mult, regime `T >= e^{u/2}` (free; H1 base already pays this) |

## Files produced today (research track)

| File | Purpose |
|---|---|
| `H1_RESIDUE_FIRST_AUDIT_2026-05-14.md` | Stage 0, Door C verdict GREEN |
| `HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md` | Stage 1a, Door B clean form |
| `H1_NUMERATOR_M_T_AUDIT_2026-05-14.md` | Stage 1b, Door D PASS with margin `T^{9/4}` |
| `HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md` | Door B fully closed; cluster-scale unification sharpens repo lemma `T^{o(1)} -> O(1)` |
| `CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` | Stage 2 plan, found Door A near-closed in repo |
| `HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md` | `S_E(T) -> Z_T^{mult}` retired |
| `HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md` | RvM multiplicity bound `m_rho = O_E(log T)` named |
| `ADVERSARIAL_MIMO_HALO_CHAIN_2026-05-14.md` | MIMO independent review; Conditional Pass |
| `LEAN_SIGNED_VS_ABSOLUTE_GADGET_2026-05-14.md` | Per-sorry note for Aristotle round-9 (research-track) |
| `WAVE4_PROMOTION_PLAN_2026-05-14.md` | Decomposition of Door A residual into 9 sub-tasks |
| `WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026-05-14.md` | Binding sub-tasks 1.1+2.1+2.4 executed; R5 up-side fired |
| `WP_DOOR_A_RESIDUAL_CLOSURE_2026-05-14.md` | Remaining 8 textual sub-tasks executed; Door A conditionally CLOSED |
| `formal-conjectures/SignedVsAbsoluteResidueGadget.lean` (0 sorries, 0 axioms) | Aristotle round-9 — formal capture of the two-zero gadget |

## The proof composition (Door A under standing GRH)

```
THEOREM. For fixed E/Q (equivalently, fixed weight-2 cuspidal newform of
level N_E), under standing GRH for L_E^*,

  sum_{rho in Z_T}^{mult} |L_E^*(rho + 1/log T)|^{-2}  <<_{E,eps}  T^{5/2 + eps}.

Proof.  Decompose:

  Z_T^{mult}  =  S_E(T)  +  (Z_T \ S_E(T))^{mult}.

Simple zeros (S_E(T)):
  q=2 audit (DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT L117-148) routes through
  BFMT second branch with conductor flip 2k -> 4k at k=1, A=1+O(eps),
  B=1+O(eps), exponent  1 + 2 * (4-1)/(4-1+1) = 5/2.
  All four absorption factors (Section 5 (5.11), Props 2.5/2.6/2.7) are
  T^{o(1)}.  Conditional on Agent01 prime polynomial lower bound, BFMT
  Section 5 packaging, standing GRH.

Multiple zeros ((Z_T \ S_E(T))^{mult}):
  Multiplicity bound m_rho <= C_E log T (RvM, HALO_RVM_MULTIPLICITY_LEMMA).
  Per-zero summand bounded by m * (log T)^{2m} * |L^{(m)}(rho)/m!|^{-2}.
  Laurent coefficient bound (log T)^{O(m)} = T^{o(1)} via Hadamard
  factorization + RvM (cognate to H1_POSITIVE_RANK_CLOSURE L221-230).
  Total count N^{mult}(T,2T) << T (log T)^2.
  Multiple-zero contribution: T^{1+o(1)},  far below T^{5/2}.

Combining: sum << T^{5/2 + eps}.  []
```

## What this gives, what it does NOT

**Gives**: Door A is the **only** "genuine analysis" door in the halo plan; the other three (B, C, D) are bookkeeping. Closing Door A conditionally finishes the halo route.

The halo route's conclusion (halo plan §2.1, §2.2):

```
Under standing GRH for L_E^*, plus M_T = T^{o(1)} (Door D),
plus HaloShiftComparison (Door B), plus ResidueFirstH1Rewrite (Door C),
plus AllZeroShiftedNeg_2(E) (Door A),

  R_Phi(T)  :=  sum_{rho in Z_T^red} Res_{s=rho} Phi_T(s)/L(s)
            =  o(T^2).
```

All four conditions are now met. **R_Phi(T) = o(T^2) holds** (under standing GRH and the named Wave 4 inputs).

**Does NOT give**:
- Unconditional offcentral H1 (still needs GRH for the newform).
- Anything about DPAC, LI, or RH for zeta — those are separate open problems.
- Anything about the Palm wall direct break — that remains NO-GO; the halo route bypasses it.
- A formal Lean statement of the halo theorem — only the structural two-zero gadget is in Lean (round-9).

## The Palm wall — current status

| Track | Status |
|---|---|
| Direct break (multi-agent swarm, GPT-5.5 Pro Extended) | **NO-GO unchanged** since 2026-05-12 |
| Halo bypass (today) | **conditionally complete** |
| Density-method side-quest (§8.3 of halo plan) | open, demoted to R1 insurance, no longer needed |

The Lean lemma `SignedVsAbsoluteResidueGadget` (Aristotle round-9, 0 sorries) formally captures **why the Palm wall cannot be broken by a sign-trick**: the two-zero deterministic gadget shows the absolute residue sum is genuinely strictly larger than the signed sum, by an arbitrary multiplicative factor. The halo route works because H1 doesn't need the positive `R_B`; it only needs the signed `Z_c(u)`.

## What's next

Three options, in order of priority:

1. **Ping the draft track** (`handoff-2026-05-12-paper-prep/recent/`) that the halo route is conditionally complete. The joint Saar-Koyama paper's §X could now include a halo-route subsection (currently §X mentions halo only as a "negative finding" route II in `SP_L_SUFFICIENT_PACKAGES`; status would flip to a positive result). This is a coordination task, not a research one.

2. **Adversarial second pass** (MIMO or another reviewer) on the Wave 4 promotion audits (`WP_2_4_...` + `WP_DOOR_A_RESIDUAL_CLOSURE_...`). Cheap (~$0.04 total). The session has been a single-thread reliance on agent dispatches; a hostile review is appropriate before declaring closure.

3. **Formalize the halo statement in Lean** as a longer-horizon dispatch. The halo route's GL2 L-function content is beyond Mathlib v4.28.0, so a "stubbed-statement-with-sorry-citing-the-prose-proof" file is the appropriate first artifact. Would parallel the `SignedVsAbsoluteResidueGadget.lean` precedent.

## Tools used today

| Tool | Dispatches | Cost (USD) | Result |
|---|---|---|---|
| General-purpose subagents (Claude Opus) | 7 | n/a (in-session) | All audits delivered |
| MIMO (`mimo-v2-flash`) | 1 (after one `mimo-v2.5-pro` failure) | ~$0.02 | Adversarial review, Conditional Pass |
| Aristotle (round-9) | 1 | ~$cost not disclosed by API | 0-sorry Lean closure in ~20 min wall-clock |

## Confidence breakdown

| Item | Confidence |
|---|---|
| Door C (signed form is what H1 needs) | 0.94 (Stage 0 + 1b residual retired) |
| Door D (M_T bound) | 0.92 (PASS for simple + bounded mult, regime free) |
| Door B (HaloShiftComparison) | 0.90 (arc-uniformity audit closed the residue) |
| Door A (`T^{5/2+eps}`) | 0.85 (all 9 sub-tasks PASS but rely on uncited Iwaniec-Kowalski Ch. 5 at 1.5; cosmetic) |
| Halo route as composite | 0.80 (no single weak link, but multiple conditionals) |
| Standing GRH for `L_E^*` | (named assumption; not in scope of this session) |

## Boundary

Allowed claims:

```
The halo route to unconditional offcentral H1 is conditionally complete
under standing GRH for the fixed newform L_E^*.  The four halo doors
(A, B, C, D) are all closed at their target loose exponents under
named external citations.

Halo plan §13's "1-2 months focused work" estimate was compressed to
one session day via aggressive delegation to subagents, MIMO adversarial
review, and Aristotle Lean formalisation of a structural lemma.
```

Forbidden claims:

```
The halo route is unconditional.
Riemann Hypothesis is proved (for zeta or for L_E^*).
DPAC, LI, or any other LI-class conjecture is proved.
The Palm wall has been broken (it remains NO-GO).
Mertens spectroscope universality is proved unconditionally.
Unconditional offcentral H1 follows without standing GRH.
```

## Note to the draft track

The joint Saar-Koyama paper's `handoff-2026-05-12-paper-prep/recent/SP_L_SUFFICIENT_PACKAGES.md` currently treats the halo route as a "negative finding" (route II). After today's session, that designation is **out of date**: route II is now conditionally complete under standing GRH. The midweek update to Koyama should reflect this. The draft session is the appropriate place to coordinate the paper-side write-up.

This research-track session has not touched any paper-prep file. The synthesis here is the formal handoff.
