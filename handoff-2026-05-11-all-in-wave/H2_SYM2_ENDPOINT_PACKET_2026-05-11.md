---
schema_version: 1
title: "H2/Sym2 endpoint packet"
date: 2026-05-11
type: closure-packet
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.80
tags: [ec-ndc, h2, sym2, product-average, endpoint]
---

# H2/Sym2 Endpoint Packet

Outcome: no EC fixed-curve theorem is promoted. The exact H2 local algebra is closed. The endpoint-smoothed H2 limit is a conditional theorem package, still blocked by S1 branch continuation and exact Sym2 finite part. Product-average can be stated conditionally with fewer pointwise cancellation requirements, but not with fewer analytic/profile requirements overall.

## Sources Read

- `HANDOFF.md`
- `L2_facts/farey-claim-ledger.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/H2_SYM2_PRODUCT_AVERAGE_PACKAGE.md`
- supporting checks: `S1_ZERO_SUMMABILITY.md`, `H1_H2_COMPOSITION_AUDIT.md`, `THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md`, `H2_SYM2_SOURCE_CLOSURE.md`, `H1_PRODUCT_AVERAGE_THEOREM.md`

## Theorem Package Now Stateable

Fix an elliptic curve `E/Q`, an admissible endpoint-smoothed kernel `W`, and analytic rank

```text
r = ord_(s=1) L(E,s).
```

Use exactly the Agent 3 local factors:

```text
A_p(1) = 1 - a_p/p + 1/p    good p
A_p(1) = 1 - a_p/p          bad p
P_E,W(K) = product_p A_p(1)^(-W(p/K)).
```

Closed proposition, exact local H2 algebra. For good primes set

```text
lambda_p = a_p/sqrt(p),
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Then

```text
log P_E,W(K)
 = S1_W(K)
   + (1/2) Ssym_W(K)
   - (1/2) Mgood_W(K)
   + Rge3_W(K)
   + Bbad_W(K),
```

with

```text
S1_W     = sum_(p good) W(p/K) a_p/p,
Ssym_W   = sum_(p good) W(p/K) chi_sym2(p)/p,
Mgood_W  = sum_(p good) W(p/K)/p,
Rge3_W   = sum_(p good) W(p/K) R_p,
Bbad_W   = -sum_(p bad) W(p/K) log(1-a_p/p).
```

The `R_p` tail after subtracting `a_p/p + (a_p^2-2p)/(2p^2)` is absolutely convergent by the Hasse bound. This proposition is the only unconditional H2 theorem-level item in the current packet.

Conditional pointwise H2 theorem. If, with the same `kappa_sym`,

```text
S1_W(e^u)     = (1/2 + kappa_sym/2 - r) log u + C1_E,W + o(1),
Ssym_W(e^u)   = -kappa_sym log u + Csym_E,W + o(1),
Mgood_W(e^u)  = log u + CM_E,W + o(1),
Rge3_W(e^u)   = Cge3_E + o(1),
Bbad_W(e^u)   = Bbad_E + o(1),
```

then

```text
log P_E,W(e^u) = -r log u + B_H2(E,W) + o(1),
P_E,W(e^u) = exp(B_H2(E,W)) u^(-r) (1+o(1)),
```

where

```text
B_H2(E,W)
 = C1_E,W + (1/2)Csym_E,W - (1/2)CM_E,W + Cge3_E + Bbad_E.
```

The coefficient check is exact:

```text
(1/2 + kappa_sym/2 - r) + (1/2)(-kappa_sym) - 1/2 = -r.
```

Conditional branch criterion. If S1/Sym2 singularities are logarithmic branches and the weighted zero/pole sums plus contour tails are controlled, an offcentral singularity `rho` contributes

```text
-(1/u) m_rho e^((rho-1)u) W_hat(rho-1) + lower terms.
```

Thus zeros on `Re rho=1` are `1/u`-damped for H2. This is not available for H1 reciprocal Perron poles.

## Missing Lemmas

H2 blockers:

- Endpoint S1 branch-contour theorem for `A_E(z)=sum_(p good) a_p p^(-1-z)`: Mellin inversion, branch-only continuation, no offcentral poles in the shifted strip, valid infinite-cut contour shift, and horizontal/left-edge bounds.
- S1 zero summability is only partially closed: EC zero counting plus smoothstep decay supports pure multiplicity sums, but it does not prove branch continuation or contour legality.
- Exact Sym2 finite-part theorem for the good-prime object with first coefficient `a_p^2/p - 1`: continuation, central order `kappa_sym`, finite part, offcentral zero/pole summability, and no uncancelled `Re rho>1` term.
- Do not set `kappa_sym=0` unless verified for this exact good-prime normalization.
- Weighted good-prime Mertens transfer for the same `W` and finite bad-prime removal. Unweighted prime Mertens is source-supported; the weighted transfer remains an in-repo lemma.
- External source packets for any theorem promoted beyond in-repo assumptions.

Composition/product blockers:

- H1 reciprocal Perron expansion for the same `W`: central polynomial, offcentral reciprocal Laurent residues, multiple-zero degrees, reciprocal derivative/Laurent coefficient control, and contour tails.
- Positive rank pointwise composition needs `Z_c(u)+E_c(u)=o(u^r)`. Rank zero needs either `Z_c(u)=o(1)`, explicit oscillatory retention, filtering with tail control, or product averaging.
- Multiple offcentral zeros with effective degree `>= r` must be ruled out, cancelled, retained in a profile, or averaged.
- Product-average needs mean coefficients of `G(u)=exp(Z_P(u))`, not just an averaged statement for `log P`.
- Infinite diagonal/offdiagonal tail extraction for the joint H1/H2 frequency series.

## Product-Average Status

Promotable only as a conditional arithmetic product-average theorem:

```text
A_U(F) = (1/U) int_U^(2U) F(u) du.
```

Assume

```text
c_E,W(e^u) = u^r H_c(u) + mean-small error,
H_c(u) = q_r + sum h_gamma e^(i gamma u),
q_r = 1/L^(r)(E,1),

P_E,W(e^u) = exp(B_H2) u^(-r) G(u)(1+mean-small error),
G(u)=exp(Z_P(u)),
```

and finite-truncation diagonal limits plus joint tail control. Then

```text
A_U(c_E,W(e^u) P_E,W(e^u))
 -> exp(B_H2(E,W)) (q_r d_0 + sum h_gamma d_(-gamma)),
```

where `d_eta` are dyadic mean coefficients of `G`.

This uses fewer pointwise cancellation inputs than fixed-curve stabilization: H1 nonzero main-scale frequencies, including rank-zero simple residues, may be retained and averaged. It does not use fewer analytic inputs overall. It trades pointwise cancellation for explicit H1/H2 profiles, dyadic mean coefficients of `exp(Z_P)`, and joint tail extraction.

Not promotable:

- unconditional EC product-average;
- arithmetic average from averaged `log P` alone;
- pointwise rank-zero stabilization from smoothing alone;
- H1 residue control from H2 `1/u` branch damping.

Special case. If H2 is pointwise nonoscillatory (`G=1`) and the H1 product-tail hypothesis holds, the conditional product-average constant is

```text
exp(B_H2(E,W)) / L^(r)(E,1),
```

with `L(E,1)` in rank zero. This remains an arithmetic average, not a pointwise limit.

## Confidence

- `0.90` exact local H2 algebra.
- `0.76` conditional pointwise H2 package as a coherent reduction.
- `0.70` product-average theorem algebra conditional on profiles and tails.
- `0.86` no-promotion verdict.

## Verification

- Checked required source packets and nearby synthesis/referee/product-average files.
- Confirmed `H2_SYM2_PRODUCT_AVERAGE_PACKAGE.md` is present.
- No external theorem was newly cited or source-promoted.
- No Koyama correspondence/email drafts touched.

## Changed Files

- `handoff-2026-05-11-all-in-wave/H2_SYM2_ENDPOINT_PACKET_2026-05-11.md`

## Risks

- The exact Sym2 object may differ by ramified/local conventions if a future global adjoint source is imported; finite corrections must be reconciled before using `kappa_sym`.
- Averaged product constants are sensitive to diagonal H1/H2 frequency coincidences and to exponentiating H2 profiles.
- Rank substitutions remain unsafe without analytic-rank equality input.
- The old EC numerical smoothing gate remains a failed load-bearing gate; no finite-window diagnostic supports theorem promotion here.
