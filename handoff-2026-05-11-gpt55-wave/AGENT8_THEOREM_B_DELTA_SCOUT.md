---
title: "Agent 8 - Theorem B / Delta Route Scout"
date: 2026-05-11
status: RIGOROUS_REDUCTION
confidence:
  delta_axis_multiplicity_reduction: 0.86
  bcl_to_theorem_b_exact_unconditional: 0.04
  aggregate_scout: 0.82
dependencies:
  - BCL source audit: arXiv:2310.07606v3, PDF retrieved by curl; pdftotext unavailable here, text extracted with pypdf and page markers.
  - F2 local source: handoff-2026-05-09-followup/Cross_Selberg_slope_diagnosis.md
  - Prior no-go sources: BCL_2024_q_averaged_route.md; B_prime_denom_Selberg_Beurling_assessment.md; R2_NC15_geometric_motivic_period.md
verdict: "No Theorem B-exact route from BCL transfer. Viable next theorem route is Delta Open 7.2' as a local ramified Euler-factor axis-pole multiplicity theorem."
---

# Bottom Line

The BCL q-averaged line is closed for Theorem B-exact unconditional. The primary source states BCL is GRH-conditional, q-averaged over levels, and 1-level. That does not transfer to fixed-level or weight-aspect support-4, and it does not supply the 2-level / 4-shift data needed for the at-zeros second moment of `L'`.

The viable next theorem is narrower and belongs to the Delta paper: a local theorem classifying higher-rank Cross-Selberg axis-pole multiplicities from the ramified Euler correction polynomial. This is a rigorous reduction to finite local algebra, not a Theorem B route.

# Primary Source Anchors

BCL = Baluyot-Chandee-Li, "Low-lying zeros of a large orthogonal family of automorphic L-functions", arXiv:2310.07606v3.

- p.1 family: "level q, averaged over q ~= Q".
- p.3 Theorem 1.1: "Assume GRH"; support is "compactly supported in (-4, 4)".
- p.4 comparison: closer to `(-4,4)` remains hard "without additional hypotheses".
- p.18 proof after (4.6): "By GRH on L(s, sym2(f))".
- p.31 around (8.4): the reciprocal L-bound "follows from GRH".

These quotes are enough to close the unconditional-transfer premise. I do not use any unquoted BCL theorem claim below.

# Prior Failures Cross-Referenced

- `BCL_2024_q_averaged_route.md`: already caught the core premise error. BCL support `(-4,4)` is not unconditional and is 1-level, not 2-level.
- `B_prime_denom_Selberg_Beurling_assessment.md`: single-ratio / mollifier work is off-critical-line and restricted; it does not touch the central rank-1 derivative moment needed for exact `2/(3pi)`.
- `R2_NC15_geometric_motivic_period.md`: no geometric/motivic identity supplies `2/(3pi)`; all matches reduce to algebraic recipe constants.
- `Cross_Selberg_slope_diagnosis.md`: F2 resolved current-scope Open 7.2 by adding log-3 axis poles. The remaining extension is higher-rank multiplicity classification.

# Route A: BCL Transfer

Finding: closed for Theorem B-exact unconditional.

Obstructions:

1. Conditionality: BCL Theorem 1.1 assumes GRH. Its proof uses GRH in the symmetric-square term and in reciprocal Hecke L-bounds. This alone blocks any unconditional Theorem B route.
2. Family mismatch: BCL averages over `q ~= Q` with conductor varying in `q`. The fixed-level weight-aspect family has no corresponding `q` in the Kloosterman modulus, so the complementary-level trick has no fixed-level target.
3. Statistic mismatch: BCL is 1-level density. Theorem B-exact needs the at-zeros second moment of `L'`, equivalently a 2-level / 4-shift off-diagonal statement at support 4.
4. De-averaging wall: even a hypothetical q-averaged 2-level theorem would still need a fixed-level extraction. That is essentially the support-4 Grand Density Conjecture wall, not a bypass.

Conclusion: BCL remains useful context for q-averaged low-zero statistics, but it is not a route to Theorem B-exact unconditional.

# Route B: Higher-Rank Cross-Selberg Axis Poles

Finding: viable Delta theorem route by rigorous reduction.

Proposed theorem, local form:

Let a Cross-Selberg Dirichlet series have ramified correction

`E(s) = prod_{p in S} P_p(p^{-s})^{-1}`,

where each `P_p(z)` is a finite local polynomial. Factor

`P_p(z) = prod_alpha (1 - z/alpha)^{m_{p,alpha}}`.

Then the ramified correction contributes poles at all solutions of `p^{-s} = alpha`. Writing `alpha = r exp(i theta)`, these lie at

`s = -log(r)/log(p) - i(theta + 2pi k)/log(p)`, `k in Z`.

The pole is on the imaginary axis iff `|alpha| = 1`. Its multiplicity is the sum of the local root multiplicities over all `(p, alpha, k)` producing the same `s`, plus any independent pole order from the Mellin transform or the unramified factor at that same point.

Checks against F2:

- For `zeta x L(s, chi_3)`, F2 has `E(s) = (1 - 3^{-2s})^{-1}`.
- Here `P_3(z)=1-z^2`, roots `alpha=+-1`.
- The lattice is `s = i pi k / log 3`, exactly the F2 axis-pole set.
- At `s=0`, the local root plus the Gaussian Mellin pole gives the observed double pole and the `c_0 log N` term.

This theorem is finite local algebra once the local correction `P_p` is written down. It does not require proving higher-rank functoriality. A global Delta explicit formula in higher rank still needs the usual contour-growth and automorphic-source checks, but the axis-pole multiplicities themselves are local.

# Do Not Promote Unless

BCL/Theorem B:

- Do not claim unconditional support `(-4,4)` from BCL; the theorem is GRH-conditional.
- Do not use q-averaging as fixed-level de-averaging without a primary-source dispersion theorem for the exact Petersson family.
- Do not use 1-level density as a substitute for 2-level / 4-shift data.
- Do not promote to Theorem B-exact unless the fixed-level support-4 wall is independently closed.

Delta/Cross-Selberg:

- Do not state arbitrary higher-rank Cross-Selberg global Selberg-class membership without a separate primary-source audit.
- Do not ignore collisions: multiple `(p, alpha, k)` can produce the same pole and multiplicities add.
- Do not ignore Mellin-transform poles; they change polynomial-in-log degree.
- Do not conflate off-axis roots `|alpha| != 1` with axis oscillations. They move the contour residue line.
- Do not promote numerical slope matching unless the full ramified axis lattice is included.

# Recommended Next Theorem Route

Write `Open 7.2'` as a Delta-machine proposition:

**Ramified axis-pole multiplicity proposition.** Given the local ramified correction polynomials `P_p(z)` for a Cross-Selberg pair, the full axis-pole set and multiplicities are exactly the unit-circle root lattices of the `P_p`, with collision and Mellin-pole multiplicities added.

Proof plan:

1. Define `P_p(z)` from the local Euler correction.
2. Factor `P_p` over `C`.
3. Solve `p^{-s}=alpha` and classify `Re(s)=0`.
4. Compute residue order by adding local root multiplicity, coincident-root multiplicity, and Mellin/unramified pole order.
5. Specialize to `zeta x L(s, chi_3)` as the regression test for F2.

Expected scope: Delta paper extension only. Expected Theorem B impact: none.
