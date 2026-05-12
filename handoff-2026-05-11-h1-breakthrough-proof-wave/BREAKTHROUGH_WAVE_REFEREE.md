---
schema_version: 1
title: "Breakthrough wave referee"
date: 2026-05-11
type: adversarial-referee
tier: working
status: NO_GO
confidence: 0.92
tags: [ec-ndc, h1, breakthrough-wave, referee]
---

# Breakthrough Wave Referee

Status: `NO_GO`

Confidence: `0.92`

External citations: none. This is an internal referee audit of the wave files and their embedded source packets.

Dependencies read:

- `HANDOFF.md`
- `L2_facts/farey-claim-ledger.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`
- `handoff-2026-05-11-h1-residue-control-wave/RESIDUE_CONTROL_ADVERSARIAL_REFEREE.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/DISPATCH_MANIFEST_2026-05-11.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H2_SYM2_PROOF_ATTEMPT_2.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/KERNEL_FILTER_DIAGNOSTIC_IMPLEMENTATION.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/kernel_filter_moments.py`

Missing dependencies for running agents: none as files by final scan. The manifest still says slots 1-7 are running/in progress, but all listed slot outputs are now present. Missing dependencies are analytic: fixed-weight H1 shell upper bounds, reciprocal height/left-line contour bounds, Laurent control, exact H2 branch/Sym2 closure, and joint product-mean tail extraction.

## Do Not Promote Unless

- A fixed-curve, fixed-kernel H1 shell bound is proved for
  `sum_{T<|gamma|<=2T} W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)`,
  uniformly in `u`, with dyadically summable errors.
- No lower-bound or mollified-moment statement is used as an upper bound for
  reciprocal derivatives or Laurent coefficients.
- The fixed-weight/mollifier transfer handles all shells, including
  `T < exp(u/theta)`, without circular residual estimates.
- H1 contour passage proves the original-line, horizontal, shifted-line,
  indentation, truncation, and height-avoidance tails for the same `W`.
- Multiple offcentral zeros are ruled out, kernel-killed, retained, averaged,
  or controlled by Laurent coefficient bounds; effective degrees `>= r` are
  never hidden in an error term.
- Rank zero is stated as an oscillatory profile, explicit filtered theorem, or
  arithmetic product average. No constant pointwise rank-zero limit is claimed.
- H1 and H2 use one theorem mode only: pointwise, profile, arithmetic product
  average, geometric/log average, or finite part. No mode mixing.
- H2 closes `S_1,W`, `S_sym,W`, `M_good,W`, `R_ge3,W`, and bad-prime constants
  for the exact Agent-3 local factors.
- Kernel filtering is diagnostic unless the kernel class, normalization,
  positivity/sign, curve-dependence, filtered set, and unfiltered tail are all
  part of the theorem.
- Any external theorem later used to close a blocker has the mandatory
  `curl + pdftotext + page/equation + short quote + SHA` packet.

## Verdict

No breakthrough proof candidate is present. The wave strengthens the negative
audit: Li-Zaharescu-style and mollifier-transfer routes do not currently adapt
to fixed-weight H1 upper bounds. The surviving outputs are useful reductions:
multiple-zero bookkeeping, contour-tail hypotheses, rank-zero profile/product
average, H2 conditional branch package, and finite kernel-filter diagnostics.

## Fatal Gaps

1. **Li-Zaharescu route remains `NO_GO`.** The dyadic Cauchy-Schwarz lemma is
   valid only after a new upper bound such as
   `sum_shell |L'(rho)|^-2 <= T^theta(log T)^B` with the kernel-dependent
   summability threshold. The wave does not prove or source that input.

2. **Fixed-weight transfer is not a transfer.** The H1 weight
   `W_hat(i gamma)e^(i gamma u)` is not a Li-Zaharescu Dirichlet-polynomial
   weight. Approximating the phase requires length tied to `K=e^u`, leaving
   low/medium shells uncontrolled. Bounding approximation residuals already
   needs the reciprocal-derivative upper control being sought.

3. **Contour tails reduce to new reciprocal bounds.** Legal heights and zero
   separation are not enough. The contour-tail file correctly isolates
   `H-height` and `H-left`; checked inputs do not supply crossed-strip
   bounds for `1/L(E,s)` compatible with the same height sequence.

4. **Multiple zeros are still load-bearing.** A single offcentral zero of
   multiplicity `m` can contribute `e^(i gamma u)u^(m-1-h)`. If the effective
   degree is `>= r`, positive-rank central closure fails. In rank zero, any
   nonzero degree `>=1` term grows. Many-simple-zero input does not remove the
   exceptional set.

5. **Rank-zero constant claims are forbidden.** The rank-zero package is
   coherent only as `Q_0+Z_c(u)+o(1)` or as a separate arithmetic average of
   `c_E,W(e^u)P_E,W(e^u)`. Averaged `log P`, geometric means, or H2 branch
   damping do not kill H1 reciprocal-pole oscillations.

6. **H2 is still conditional and separate.** The local coefficient bookkeeping
   is good, but endpoint-smoothed `S_1,W`, exact good-prime Sym2 finite part,
   no right-branch/pole assertions, and `kappa_sym` normalization remain proof
   or source dependencies. H2 cannot be imported into H1 pole control.

7. **Kernel filter can cheat if promoted.** The script solves finite moment
   constraints and the smoke test succeeds numerically, but it uses a
   log-Gaussian Schwartz moment with `W_hat(0)=1`, not the endpoint Mellin-pole
   normalization `W_hat(z)=1/z+O(1)` used for the H1 central polynomial. It
   is a finite signed/possibly curve-dependent diagnostic, not fixed-kernel
   asymptotic stabilization or tail control.

8. **Source protocol is not the current failure.** Present files mostly guard
   external facts or label source targets as unverified. Promotion would still
   require full source packets for every analytic blocker above.

## Safe Promotion Boundary

Allowed:

```text
The breakthrough wave gives guarded reductions and diagnostics. Fixed-curve
H1 remains blocked by reciprocal-derivative/Laurent control, quantitative
contour-tail height avoidance, multiple-zero handling, and rank-zero mode
selection. The rank-zero profile/product-average package is paper-usable as a
conditional fallback, not as pointwise stabilization.
```

Forbidden:

```text
Li-Zaharescu or mollified moments prove fixed-weight H1.
Smoothing kills rank-zero H1 residues.
Kernel filtering proves fixed-kernel asymptotics.
H2 branch damping transfers to H1 reciprocal poles.
Averaged log P implies arithmetic average of cP.
The EC smoothing theorem is proved or proof-candidate-ready.
```

Final decision: keep the wave as `NO_GO` for theorem promotion and as a
conditional reduction packet for future H1/H2 work.
