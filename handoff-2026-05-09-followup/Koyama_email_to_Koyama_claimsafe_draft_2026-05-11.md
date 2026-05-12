---
schema_version: 1
title: "Claim-safe email draft to Koyama"
date: 2026-05-11
type: correspondence-draft
tier: working
confidence: 0.9
status: DRAFT_SOURCE_ANCHORED_DO_NOT_SEND_WITHOUT_USER_APPROVAL
sources:
  - handoff-2026-05-09-followup/Koyama_claimsafe_paper_outline_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_CLAIM_AUDIT_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
  - handoff-2026-05-11-gpt55-wave/AGENT2_PERRON_CITATION_AUDIT.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
  - handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
tags: [koyama, correspondence, claim-safe]
---

# Claim-safe email draft to Koyama

Subject: Corrected NDC constant, Perron obstruction, and conditional EC smoothing route

Dear Professor Koyama,

I wanted to follow up with a deliberately conservative status update on the
NDC direction.

I now think the original `1/zeta(2)` normalization should be withdrawn from
the GL(1) theorem posture.  I rechecked the Aoki-Koyama source directly.  On
p. 235, formula (1.4), the Dirichlet specialization of the DRH formula has
denominator `e^{m gamma} m!` ("with gamma being the Euler constant").  Thus,
for the simple-zero version of the AK/DRH input that we have been using, the
GL(1) Euler-product factor is governed by the Mertens constant:

```text
E_K(rho,chi) * log K -> L'(rho,chi) / e^gamma,
```

under the AK hypotheses, rather than `L'(rho,chi)/zeta(2)`.  In other words,
the corresponding product constant should be `e^{-gamma}` once the Perron
leading term is also available.

I am not treating this as a closed NDC theorem.  Two dependencies remain.
First, the Euler-product side should be stated in the same noncentral
Dirichlet-zero convention, or reduced cleanly to such a statement.  Second, we
have a local Perron residue calculation at the target zero, but I do not
currently regard the global Perron-leading statement

```text
c_K(chi,rho) = sum_{n<=K} mu(n) chi(n)n^(-rho)
             = log K / L'(rho,chi) + o(log K)
```

as closed.  The missing point is the nonlocal residue aggregate from
off-target zeros of `L(s,chi)` in the shifted Perron integral

```text
K^w / (w L(rho+w,chi)).
```

An off-target zero `lambda != rho` contributes at `w=lambda-rho`.  If it has
multiplicity `m`, the residue can have top scale `(log K)^(m-1)`.  In
particular, target-zero simplicity does not by itself close the theorem.  Even
if all crossed off-target zeros are simple, one still needs

```text
Z_simple(K,T_K)=o(log K)
```

plus the shifted rectangle and truncation estimates.  The explicit-formula
sources I checked keep this off-target zero sum explicit; they do not close it.
So the GL(1) package is currently: corrected constant, local target residue,
corrected `B_infty`, and an explicit shifted Perron obstruction.

On the EC/GL(2) side, the sharp-cutoff finite bad-prime fixes did not rescue a
universal analogue.  Smoothing did produce a reproducible finite pattern: the
saved script reproduces the three-curve smoothstep grid through `K<=1000000`,
and for the full proxy at `alpha=0.75` gives cross-curve ratio
`1.347375492996` with max within-curve CV `0.063297427334`.  However, ablations
such as `cP_only`, `P_only`, and `PL2_only` also pass the old gate, so I regard
this as a finite smoothing lead, not BSD evidence and not an `L(E,2)`
normalization theorem.

The theorem route now looks fixed-curve and conditional, not cross-curve
universal.  With one declared smoothing kernel, a pointwise fixed-curve result
would need a matched H2 product expansion

```text
log P_E,W(K) = -r log log K + B_E,W + o(1),
```

including the exact local factors `S_1,W`, `S_sym,W`, `M_good,W`, higher prime
powers, and bad-prime constants, together with a separate H1 reciprocal-Perron
input

```text
c_E,W(K) = (log K)^r / L^(r)(E,1) + o((log K)^r)
```

for analytic rank `r>=1`.  Rank zero has to be stated as an
oscillatory/profile or averaged theorem unless the offcentral reciprocal
residues are proved to cancel.  The key mismatch is that H2 sees offcentral
zeros through logarithmic branches with a `1/log K` loss, while H1 sees poles
of `1/L(E,1+z)` and gets no such damping.

Only one H1 contour-tail piece currently looks safe to me: the left line can
be shifted to

```text
Re z = -eta,     eta > 1/2,
```

because the functional equation reflects to the absolute reciprocal
Euler-product half-plane.  For `eta<=1/2`, the left-line reciprocal bound
remains a hypothesis.  The horizontal-height input is still open: for the
current smoothstep-scale kernel, with Mellin decay `q=2`, the generic
Cartan/Jensen route does not prove the needed `A_TC<2` minimum-modulus bound.

I would be very grateful for your view on three specific points:

1. Is there in your framework a noncentral Dirichlet Euler-product theorem
   matching the AK normalization with `m=ord_{s=rho} L(s,chi)`?
2. Do you know a shifted Perron or explicit-formula theorem that controls the
   off-target aggregate for

```text
K^w / (w L(rho+w,chi))
```

at `o(log K)` scale?
3. In the GL(2) / elliptic-curve setting, is there a fixed-curve reciprocal
   derivative or minimum-modulus input strong enough for H1, or should
   rank-zero be stated from the start as an oscillatory/profile theorem?

Best,
Saar

## Source anchor

- Aoki-Koyama source: Miho Aoki and Shin-ya Koyama, "Chebyshev's bias against
  splitting and principal primes in global fields", Journal of Number Theory
  245 (2023), 233-262, doi `10.1016/j.jnt.2022.10.005`.
- Repo audit anchor: `handoff-2026-05-11-gpt55-wave/AGENT2_PERRON_CITATION_AUDIT.md`
  records p. 235, eq. (1.4), and the short quote "with gamma being the Euler
  constant".
- Caveat preserved: the audit also flags that applying AK (1.4) directly to an
  arbitrary noncentral `rho = 1/2 + it` is not independently citation-closed
  from that PDF alone. This is why the email says "simple-zero version of the
  AK/DRH input" and asks Koyama for the shifted Perron/off-target residue
  theorem rather than promoting the full `D_K` limit.
- GL(1) shifted Perron anchor:
  `handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md` records the
  off-target multiple-zero obstruction and the remaining sufficient package
  `Z_simple(K,T_K)=o(log K)` plus rectangle/truncation estimates.
- EC smoothing anchor:
  `handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md`
  records the reproduced finite proxy and ablation downgrade.
- H1/H2 anchor:
  `handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md` and
  `handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md` record
  the fixed-curve conditional theorem mode and the `eta>1/2` left-tail limit.

## Send checklist

- Do not send without explicit user approval.
- Attach or link the corrected AK, local Perron, and `B_infty` proof packets.
- Keep "product constant should be" conditional unless the Perron theorem is
  closed before sending.
- Do not promote the smoothed EC proxy; keep the ablation caveat.
- Do not state `eta<=1/2` left-tail control, `H-height(A_TC<2)`, or rank-zero
  pointwise stabilization as closed.
