---
schema_version: 1
title: "Residue-control adversarial referee"
date: 2026-05-11
type: adversarial-referee
tier: working
status: NO_GO
confidence: 0.90
tags: [ec-ndc, h1, h2, residue-control, referee]
---

# Residue-Control Adversarial Referee

Status: `NO_GO`

Confidence: `0.90`

Recommendation: do not promote the combined H1/H2 EC smoothing theorem. Promote
only the guarded reduction package. The new wave clarifies the obstruction; it
does not discharge it.

Dependencies read:

- `HANDOFF.md`
- `L2_facts/farey-claim-ledger.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md`
- `handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md`
- extra available wave files:
  `H1_PRODUCT_AVERAGE_THEOREM.md`, `H2_SYM2_SOURCE_CLOSURE.md`,
  `DISPATCH_MANIFEST_2026-05-11.md`

Missing dependency: the manifest lists `H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`,
but that file was not present in the wave directory at audit time. Treat the
reciprocal-derivative source hunt as unresolved.

## Do Not Promote Unless

- H1 has a proved fixed-kernel Mellin/Perron identity and finite-height contour
  shift for the exact `W`, with original-line, horizontal, shifted-line,
  indentation, pole-avoidance, and truncation tails in one declared mode.
- H1 offcentral reciprocal residues are controlled independently:
  `sum |W_hat(i gamma)/L'(1+i gamma)|`, or the multiple-zero Laurent analogue,
  is proved/sourced, not guessed from EC zero counting.
- Every crossed zero with `Re(rho)>1` is ruled out by a stated hypothesis/source
  or retained as an exponentially growing term.
- Rank zero is not stated as a pointwise constant limit unless all nonzero H1
  reciprocal residues vanish/cancel, are explicitly filtered with tail control,
  or the theorem is changed to a product-level average/profile.
- Multiple offcentral zeros with effective degree `>= r` are ruled out,
  kernel-cancelled, residue-cancelled, retained, or averaged with proof.
- H2 is closed for the exact Agent-3 local factors: good
  `1-a_p/p+1/p`, bad `1-a_p/p`, and all of `S_1,W`, `S_sym,W`,
  `M_good,W`, `R_ge3,W`, and `B_bad,E,W`.
- S1 branch continuation and Sym2 finite part are proved for the endpoint
  kernel; zero summability alone is not branch continuation.
- The final theorem mode is one mode only: pointwise, oscillatory/profile, or
  arithmetic product-average. No mixing pointwise H1 with averaged/log H2.
- If averaged, the averaged object is
  `A_U[c_E,W(e^u) P_E,W(e^u)]`, with mean coefficients of `exp(Z_P)`, diagonal
  correlations, and infinite tail/offdiagonal extraction proved.
- Kernel filtering is declared as fixed/family, signed/positive,
  curve-dependent/independent, and all derivative growth costs are carried.
- Any external theorem used to discharge a blocker has the mandatory
  `curl + pdftotext + page/equation + short quote` packet.

## Fatal Blockers

1. H1 reciprocal poles remain the theorem killer.

For a simple offcentral zero,

```text
R_gamma(u) = e^(i gamma u) W_hat(i gamma)/L'(E,1+i gamma).
```

There is no H2-style `1/u` damping. The current files correctly identify this,
but no file proves the needed reciprocal-derivative or Laurent coefficient
control. EC zero counting controls pure multiplicities, not `1/L'(rho)`.

2. The H1 contour theorem is still conditional.

`H1_CONTOUR_SHIFT_THEOREM.md` gives a finite-box identity, not an asymptotic
theorem. The tails require quantified bounds on `1/L(E,1+z)`, `W_hat` and its
derivatives, height avoidance, and shifted-line integrability. Those are
listed as hypotheses. They cannot be silently converted into proof.

3. Rank zero blocks pointwise stabilization.

If `r=0`, any nonzero simple H1 residue is main scale:

```text
c_E,W(e^u) = 1/L(E,1) + Z_c(u) + o(1)
```

is the honest target. A constant-only theorem is false unless `Z_c` is killed,
retained, or averaged in the product itself.

4. Multiple zeros are catastrophic unless explicitly handled.

An offcentral zero of multiplicity `m` can contribute
`e^(i gamma u) u^(m-1-h_gamma)`. If the effective degree is `>= r`, it survives
or grows after H2 normalization. No current source proves all offcentral zeros
are simple, bounded multiplicity with safe Laurent growth, or kernel-killed.

5. H2 local algebra is coherent but not closed.

The H2 file repairs the local expansion and keeps the bad-prime/local-factor
terms. Good. But theorem promotion still needs branch continuation for
`S_1,W`, the exact good-prime `S_sym,W` finite part for
`chi_sym2(p)=a_p^2/p-1`, and a convention-safe handling of `kappa_sym`. Adjacent
Sym2 facts cannot be imported as this exact endpoint-smoothed theorem.

6. Product averaging is a different theorem, not a shortcut.

The product-average note is claim-safe only because it averages the product
itself and demands mean coefficients of `G(u)=exp(Z_P(u))`. Averaged `log P`,
geometric means, or pointwise `c` times a log-average of `P` do not imply the
arithmetic product constant. Infinite diagonal/offdiagonal extraction is still
a missing analytic theorem.

7. Kernel filtering is diagnostic, not proof.

Finite signed filtering can kill finitely many named H1 frequencies. It does
not control the tail. Positive kernels need a separate feasibility proof.
Curve-dependent or growing families change the theorem. Infinite filtering
needs an entire-function/zero-density theorem and cannot be smuggled in as
"smoothing."

8. Source hygiene is not yet promotion hygiene.

The new wave mostly avoids illegal source imports by labeling analytic inputs
as hypotheses. The danger is downstream: using ordinary Mertens, EC
zero-counting, or adjacent Sym2/adjoint facts as if they proved the exact
endpoint-smoothed S1/Sym2/H1 statements would violate the project citation
protocol.

## Attack Matrix

| Risk | Referee decision |
|---|---|
| Branch/pole confusion | Fatal if repeated. H2 has branches; H1 has reciprocal poles. No transfer. |
| Rank-zero overclaim | Fatal for constant pointwise theorem. Use profile or product average. |
| Multiple-zero disaster | Fatal unless effective degree `< r` or terms are handled. |
| Product/log-average mismatch | Fatal if averaged `log P` is used for product stabilization. |
| Kernel-dependent cheating | Fatal if finite/filtering/family kernels are presented as fixed smoothing. |
| Missing bad-prime/local terms | Currently guarded in H2 file; fatal if dropped in final theorem. |
| Derivative/Laurent bounds | Main unresolved analytic blocker. |
| Contour-tail assumptions | Main hidden-proof hazard. |
| Illegal source imports | No new direct import found here; promotion would need full source packets. |

## Promotion Boundary

Allowed claim:

```text
The H1/H2 EC smoothing path is reduced to matched conditional packages:
H1 reciprocal-pole control plus H2 branch/Sym2/local-factor closure, with a
separate rank-zero/profile/average decision.
```

Forbidden claim:

```text
The EC smoothing theorem is proved, or is a proof candidate, for fixed curves
and fixed kernels under the current files.
```

Final decision: no theorem promotion. The best current object is a rigorous
conditional reduction with exact blockers above.
