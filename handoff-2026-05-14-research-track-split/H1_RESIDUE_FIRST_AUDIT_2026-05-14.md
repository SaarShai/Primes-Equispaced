---
schema_version: 2
title: "H1 Residue-First Audit (Stage 0 of Halo Plan)"
type: audit
domain: project
tier: working
status: GREEN
confidence: 0.86
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
supersedes: []
superseded-by:
tags: [stage-0, halo-route, residue-first, audit, door-C, h1]
---

# Stage 0 — Residue-First Audit (Door C)

## Verdict

```text
GREEN.
```

The H1 conclusion that consumes the offcentral aggregate is signed.
Positivity (the absolute-value series `R_B = sum |L'(rho)|^{-1}` or
equivalently `sum |W_hat(i gamma)/L'(rho)|`) is used in the repo only as a
sufficient condition `(H-abs-r)` en route to the signed conclusion
`Z_c(u) + I(u) = o(u^r)`. The halo route replaces `(H-abs-r)` by a
contour residue identity for the same `Z_c`. No upstream step requires
the absolute-value form.

Next move: Stage 1 (Door B boundary-arc extension + Door D numerator
audit). Density-method side-quest (§8.3 of halo plan) is no longer the
primary route, but remains as a safety net for Risk R1.

## What H1 Actually Requires (signed vs. positive)

Anchor: `H1_POSITIVE_RANK_CLOSURE.md` lines 47-72, 117-148.

| Line(s) | Object | Form |
|---|---|---|
| L52-56 | H1 minimal condition `(H-min-r)` | signed, `Z_c(u) + I(u) = o(u^r)` |
| L122-130 | Sufficient `(H-bd)`, `(H-deg)`, `(H-tail)` | `Z_ell(u) = O(1)` signed |
| L142-148 | Optional `(H-abs-r)` | absolute, `sum |c_{gamma,ell}| < infinity` |
| L161-169 | Simple-zero special case | signed `Z_0(u) = O(1)` implies `o(u^r)`; `(H-abs-r)` is sufficient |

`(H-abs-r)` is named "the simplest promotable" condition (L147), not the
required one. The minimal exact H1 requirement is `(H-min-r)`, which is
signed.

## Where `sum |Phi_T(rho)/L'(rho)|` Enters

Anchor: `H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md` L43-49 and
L96-150.

| Lines | Object | Comment |
|---|---|---|
| L43-49 | `R_{E,1}^simp(T) = sum_{rho simple} |(L_E^*)'(rho)|^{-1}` | positive l^1; this IS `(H-abs-r)` for the simple branch |
| L62-74 | Split `R_F + R_B` | both positive |
| L99-103 | `|L'(rho)|^{-1} <= T^{o(1)} alpha W_A X` (cluster-shift) | termwise absolute-value bound; entered AFTER abs values taken |
| L121-148 | `R_B(T,c) << T^{7/4+eps+o(1)} = o(T^2)` | positive budget |

The positivity is introduced inside the simple-zero stack itself, not by
the H1 derivation that consumes it. The stack's positive budget is one
realisation of `(H-abs-r)`, not a separate H1 requirement.

## Where The Signed Form Is Available

`H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md` L48-79 records the
finite-box identity:

```text
c_{E,W}(e^u)
 = Q_{E,W}(u)
   + sum_{rho != 1, |Im rho| < T} R_rho(u)
   + vertical/horizontal/truncation errors.
```

Each `R_rho(u)` is a signed complex residue from the Perron contour
shift. The sum `sum_{rho offcentral} R_rho(u) = Z_c(u)` is by
construction a signed contour residue aggregate — the residue theorem
gives

```text
Z_c(u)
 = (1/(2 pi i)) int_{partial Omega_T} e^{u z} W_hat(z) / L(E, 1+z) dz
```

for any contour `partial Omega_T` enclosing the offcentral zeros.

This is exactly the halo plan's `R_Phi(T)` with `Phi_T(s) =
e^{u(s-1)} W_hat(s-1)`. No transformation between objects is required;
they are identical by the residue theorem.

## Positivity-Risk Check

Searched the H1 chain for any upstream step that demands
`R_B = sum |L'(rho)|^{-1}` (or `sum |W_hat(i gamma)/L'(rho)|`) rather
than the signed sum:

| Candidate upstream step | File | Verdict |
|---|---|---|
| Convergence of `Z_0(u)` (rank>=1) | residue-control synthesis L102-107 | (H-abs-r) cited as **sufficient**, not necessary |
| `sum gamma W_hat e^{i gamma u}/L'` absolute uniform convergence | breakthrough synthesis L107-117 | this is **Cauchy-Schwarz route to (H-abs-r)**, not an independent requirement |
| `l^1` energy identity elsewhere | not found | no occurrence |
| Multiple-zero exceptional term retention | breakthrough synthesis L154-172, positive-rank L191-216 | uses signed `R_rho(u) = e^{i gamma u} P_rho(u)`; sum over `rho` is signed |
| Contour tail `I(u) = o(u^r)` | residue-control L48-56 | signed; independent of `R_B` form |

No upstream `l^1` energy identity surfaced. The closest positivity-like
move is Cauchy-Schwarz in the breakthrough wave, but that is a derivation
*of* `(H-abs-r)`, not a *use* of it for an l^2 energy argument.

## Why The Stack Looks Positive But Isn't Required To Be

The repo's simple-zero stack is a positive `(H-abs-r)`-style budget
because it is the easiest route to `(H-min-r)`. Halo route trades:

| Old sufficient input | New sufficient input |
|---|---|
| `(H-abs-r)`: `sum_gamma |W_hat(i gamma)/L'(rho)| < infinity` | `int_{boundary} |Phi_T/L| |ds| << M_T T^{7/4+eps}` |
| Needs: RootedPalmRepulsionExpMoment_2 OR rooted box law | Needs: AllZeroShiftedNeg_2(E) on shifted line |

Both yield `Z_c(u) = O(u^{r-1}) = o(u^r)`. The H1 derivation downstream
is unchanged: it only sees the signed `Z_c(u)` and the signed `I(u)`.

## Caveats

```text
1. Pointwise vs averaged mode. Halo gives Z_c(u) = O(1) globally if
   M_T = T^{o(1)} and AllZeroShiftedNeg_2 holds. For rank-zero, only
   the oscillatory profile / product-average theorem applies; halo
   contributes the same signed Z_c there.

2. Multiple-zero residues. R_rho(u) = e^{i gamma u} P_rho(u) with
   deg P_rho <= m-1. Halo route handles these uniformly via the same
   signed contour. (H-deg) for ell >= r still required, unchanged.

3. Contour-tail I(u). Halo does NOT touch I(u). Door D / Stage 1b
   numerator audit feeds into the same I(u) bound regardless of route.

4. R_B is still meaningful for the density-method (8.3) side-quest.
   Even though halo bypasses (H-abs-r), R_B = o(T^2) is still a clean
   conjectural target via the loose negative second moment of L'(rho).
   Both routes are alive.
```

## Recommendation

```text
Proceed to Stage 1.

Stage 1a (parallel):  HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md
                      (boundary-arc extension of noncluster H_A
                      stability with R > sqrt(1+A^2); already proved in
                      halo plan §5.1; write-up only).

Stage 1b (parallel):  H1_NUMERATOR_M_T_AUDIT_2026-05-14.md
                      (compute M_T = sup_halo |Phi_T| for the exact
                      Phi_T in the repo H1 statement; expect T^{o(1)}).

Stage 2 (sprint):     CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md
                      (AllZeroShiftedNeg_2 via Heap-Soundararajan +
                      Bui-Florea transfer for fixed-conductor GL2).

Side-quest (kept alive): DENSITY_METHOD_RB_LOOSE_2026-05-14.md
                      not the primary route now, but cheap insurance
                      against Risk R1.
```

## Boundary

Allowed to claim now:

```text
Door C audit verdict GREEN. The H1 conclusion is a signed contour
residue contribution; the repo simple-zero stack uses (H-abs-r) only
as the cheapest sufficient condition for that signed conclusion.
Halo route is a structurally valid replacement of (H-abs-r) with a
contour residue identity.
```

Not allowed to claim:

```text
The halo route is proved (Doors A, B for boundary-arc, D unaudited).
R_B = o(T^2) is unconditionally proved.
The H1 theorem is closed.
(H-abs-r) is necessary; (H-min-r) suffices.
```

Confidence breakdown:

```text
0.86  signed form is the correct H1 requirement
0.10  some downstream step we have not yet identified silently uses
      |R_rho| termwise (e.g., uniform-in-u argument in the contour
      truncation error analysis)
0.04  the H1 statement under proof is materially different from
      the residue-control-synthesis statement we audited
```

The 0.10 residual risk should be retired by Stage 1b (numerator audit
re-reads the H1 statement and contour truncation lines literally).
