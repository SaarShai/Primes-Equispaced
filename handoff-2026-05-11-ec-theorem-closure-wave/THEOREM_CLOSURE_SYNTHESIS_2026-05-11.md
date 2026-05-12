---
schema_version: 1
title: "EC smoothing theorem closure synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
sources:
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
  - handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
  - handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md
  - handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_AGENT_REVIEW.md
tags: [ec-ndc, smoothing, h1, h2, explicit-formula, theorem-closure]
---

# EC Smoothing Theorem Closure Synthesis

No theorem was promoted.

The wave made real progress on the H2 side: the smoothed `S_1,W` branch
mechanism and zero-summability now form a coherent conditional proof candidate.
But the full EC smoothing stabilization theorem is still blocked by H1
reciprocal Perron pole residues and by source/proof closure for the exact
fixed-curve endpoint-smoothed series.

## Result Table

| Slot | File | Status | Decision |
|---|---|---|---|
| S1 branch | `S1_BRANCH_THEOREM_CANDIDATE.md` | `PROOF_CANDIDATE` | Use as conditional theorem skeleton only. |
| S1 zero sum | `S1_ZERO_SUMMABILITY.md` | `PROOF_CANDIDATE` | Zero aggregate closes under `W2+ZC+BC`; branch continuation still open. |
| Sym2 | `S1_SYM2_FINITE_PART.md` | `RIGOROUS_REDUCTION` | Correct finite-part structure, but analytic Sym2 continuation/summability remains a dependency. |
| H2 package | `H2_POINTWISE_THEOREM_PACKAGE.md` | `PROOF_CANDIDATE` | Local bookkeeping is coherent; H2 not closed until S1/Sym2/Mgood dependencies close together. |
| H1 audit | `H1_H2_COMPOSITION_AUDIT.md` | `RIGOROUS_REDUCTION` | Main blocker: H1 has reciprocal poles, not logarithmic branches. |
| Source packet | `SOURCE_PACKET.md` | `AUDIT_ONLY` | Ordinary Mertens and EC zero counting are source-supported; exact S1/H2/H1 theorem is literature-blocked. |
| Referee | `ADVERSARIAL_REFEREE.md` | `NO_GO` | No theorem promotion; preserve as guarded reduction. |
| Diagnostics | `DENSE_S1_RESIDUAL_DIAGNOSTICS.md`; `DENSE_S1_AGENT_REVIEW.md` | `AUDIT_ONLY` | Finite evidence for zero-frequency structure; damping not isolated; independent review found no fatal flaw. |

## What Actually Advanced

The best new mathematical object is the conditional S1 branch theorem:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + Z_1,E,W(log K)/log K
   + O((log K)^(-2)) + O(K^(-eta)),
```

with `r=ord_{s=1}L(E,s)`. For an offcentral zero `rho=1+i gamma`, the local
branch contribution is

```text
-m_rho K^(i gamma) W_hat(i gamma)/log K.
```

The zero-summability agent closed the boundedness of `Z_1,E,W` under explicit
smooth-kernel and zero-counting hypotheses:

```text
sum_gamma |m_gamma W_hat(i gamma)| < infinity.
```

The source packet supports the zero-counting input for pure multiplicity
weights and ordinary prime-Mertens, but not the exact endpoint-smoothed S1/H2
theorem.

## Main Blocker

H1 cannot borrow the H2 branch damping. H2/S1 sees offcentral zeros through
logarithmic branches and gains a `1/log K` loss. H1 contains `1/L(E,1+z)`;
offcentral zeros are reciprocal poles, giving residues of the form

```text
K^(i gamma) W_hat(i gamma)/L'(rho)
```

for simple zeros, with no `1/log K` loss. Therefore a final pointwise fixed
curve theorem still needs a separate H1 pole-residue theorem. For positive
analytic rank `r`, it is enough to prove the reciprocal-zero aggregate is
`o((log K)^r)`. For rank zero, bounded simple offcentral residues already sit
at main scale, so the honest target is oscillatory or averaged unless stronger
cancellation is proved.

## Claim-Safe Statement

Allowed:

```text
The EC smoothing pointwise route has been reduced to two separate analytic
closures: a branch-contour theorem for H2/S1/Sym2 and a reciprocal-pole theorem
for H1. Under these hypotheses, exact Agent-3 local-factor bookkeeping gives
log P_E,W(K) = -r log log K + B_E,W + o(1).
```

Not allowed:

```text
A closed EC smoothing theorem.
A closed cross-curve universality claim.
H1 follows from the S1 branch theorem.
Smoothing alone kills all offcentral zero effects.
```

## Next Breakthrough Target

The fastest meaningful follow-up is **H1 reciprocal Perron control**, not more
H2 algebra:

```text
c_E,W(K)
 = (log K)^r / L^(r)(E,1)
   + Z_c(log K) + lower central powers + error,
```

then prove one of:

```text
Z_c(u)+E_c(u)=o(u^r)              for positive rank,
Z_c(u)=o(1)                       for rank zero pointwise,
or a declared averaged theorem     if pointwise cancellation fails.
```

Secondary target: source/prove the Sym2 finite-part theorem for the exact
good-prime object `chi_sym2(p)=a_p^2/p-1`, including the value or role of
`kappa_sym`.

## Do Not Promote Unless

- H1 is closed separately as a reciprocal-pole theorem.
- H2 is closed with exact Agent-3 good/bad local factors.
- `S_1,W`, `S_sym,W`, `M_good,W`, `R_ge3,W`, and bad-prime constants all appear.
- The theorem mode is declared once: pointwise, oscillatory, or averaged.
- Rank zero is separated.
- Analytic rank `ord_{s=1}L(E,s)` is used before any algebraic rank substitution.
- Every external theorem cited in a final writeup has the mandatory source packet.
