---
title: "AGENT02 BFMT Epsilon Delta Margin Referee"
date: 2026-05-11
type: referee-packet
tier: working
status: NO_GO
confidence: 0.86
tags: [breakthrough-wave-5, h1, bfmt, gl2, conductor-normalized, epsilon-delta, no-go]
---

## Verdict

No legal Agent01 parameter ledger is available for the separated BFMT branch as
currently stated.

The fixed polylogarithmic losses, zero-sampling losses, `T^o(1)` coefficient
losses, and BFMT `Delta` endpoint errors are not the first obstruction.  They
are absorbable after reserving a small internal power margin.

The first mismatch is the conductor-normalized archimedean term.  Wave 4
Agent01 replaces the zeta `log T` term in BFMT Lemma 2.3 by

```text
log C_E(t) = 2 log T + O_E(1).
```

In BFMT Section 5 this doubles the linear archimedean coefficient.  The
`k=1/2` branch relies on the zeta coefficient `2k=1` being almost cancelled by
`a(2d-1)/r = 1 - O(epsilon)`.  The EC conductor-normalized branch has
coefficient `4k=2`, while the BFMT support/truncation constraints still force
`a(2d-1)/r < 1`.  The remaining gap is fixed, not polylogarithmic.

## Theorem Target

Stress-test the proposed separated EC BFMT conclusion:

```text
SeparatedEC-BFMT(E,c,k=1/2):
  sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  <<_(E,c,delta) T^(1+delta)
```

from the inputs:

```text
GL2-ShiftDerivativeComparison(E,c)
GL2-BFMT-PrimePolynomialLowerBound(E), conductor-normalized
ZeroSample-EC-BFMT-CoefficientTranscription(E,k=1/2)
```

The audit target is narrower than H1.  It does not include the bad-set
complement, multiple zeros, finite-box contour legality, or central residue
assembly.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/DISPATCH_MANIFEST_2026-05-11.md`: launches Agent01 Section 5 conductor audit and this margin referee.  The Agent01 Wave 5 packet is absent at write time.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md`: the GL2 lower bound is conductor-normalized and has `C_E(t) asymp_E T^2`; a literal zeta archimedean replacement is false.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT06_H1_FINITE_BOX_ASSEMBLY_REFEREE_2026-05-11.md`: names `Section5-GL2-ConductorAudit(E,k=1/2)` as the first unclosed separated-BFMT audit.
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md`: zero-sampling replacement costs only fixed polylogarithmic factors in Propositions 2.5, 2.6, 2.7.
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: claims the Section 5 losses are `T^o(1)`, but incorrectly places `k=1/2` in the `2k(1+epsilon)<=1` branch.
- `/tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt`: BFMT Theorem 1.1, Lemma 2.3, Propositions 2.5-2.7, and Section 5 equations (5.8)-(5.17).

## Margin Ledger

| item | stress test | result |
|---|---|---|
| BFMT branch at `k=1/2` | Need `2k(1+epsilon)>1` for every fixed `epsilon>0`. | Legal branch is the second branch, equations (5.6)-(5.7), not the first. Existing transcription has a branch-label error. |
| Zero-sampling DPMV loss | Extra `(log T)^C` in Propositions 2.5-2.7. | Legal by itself: `(log T)^C <= T^eta` for any reserved `eta>0`. |
| Shift-derivative loss | `exp(O_(E,c)(log T/loglog T))`. | Legal by itself: this is `T^o(1)`. |
| EC coefficient factors | Deligne/divisor factors and finite bad-prime removal. | Legal by itself under the zero-sampling audit: fixed polylog or `T^o(1)`. |
| Agent01 endpoint errors | `Delta^2 exp(pi Delta)/T + Delta log(1+Delta T)/sqrt(T)`. | Legal in BFMT range `T^beta=e^(2pi Delta)`, `beta<=beta_K<=c` with fixed small `c`: first term is `T^(-1+beta/2+o(1))`, second is `T^(-1/2+o(1))`. |
| Support wall | P2.5, P2.6, P2.7 require total support `<= 1-loglogT/logT`. | Legal only inside the printed BFMT parameter system. It does not absorb a fixed conductor exponent gap. |
| `Delta`-parameter scaling | `T^beta_j=e^(2pi Delta_j)`, so `2pi alpha Delta_j=beta_j`. | Legal bookkeeping. The problem is not the `Delta` conversion; it is the coefficient multiplying the archimedean term. |
| Conductor main term | Replace BFMT zeta `log T` by `log C_E(t)=2logT+O_E(1)`. | Not legal in the current ledger. It doubles the Section 5 linear archimedean contribution. |

## First Mismatch or Legal Range

First mismatch:

```text
BFMT Section 5, equation (5.13), before the large-branch bound (5.17).
```

In the zeta proof, the decisive large-branch exponent contains the linear
difference

```text
2k - a(2d-1)/r.
```

For `k=1/2`, BFMT uses the second branch and chooses parameters with

```text
a(2d-1)/r = 1 - O(epsilon),
2k = 1.
```

Thus the zeta difference is `O(epsilon)` and can be relabeled into the final
`delta`.

Agent01's conductor-normalized EC lower bound changes the archimedean main term
by the degree factor

```text
log C_E(t)/log T = 2 + o(1).
```

Therefore the same Section 5 slot becomes

```text
4k - a(2d-1)/r = 2 - a(2d-1)/r.
```

Under the BFMT support/truncation mechanism, the large-branch parameters have
`d<1`, `a<1`, and `r>1`, hence

```text
a(2d-1)/r < 1.
```

So the EC conductor-normalized difference is bounded below by a fixed positive
constant.  In the BFMT (5.13) exponential this produces a fixed power
`T^(c0+o(1))`, not a fixed polylogarithm and not `T^o(1)`.  Since the target is
`T^(1+delta)` for every fixed `delta>0`, this cannot be hidden by reducing
epsilon or by spending the polylog ledger.

No legal range is certified.  A future rescue would need a genuinely new
Section 5 parameter proof, not the current BFMT ledger plus "polylog
absorption".  In particular, any rescue must explicitly show how the doubled
archimedean coefficient is offset while preserving the P2.5/P2.6/P2.7 support
conditions.

## Dependency Impact

- Agent01 should not receive a green parameter ledger from this packet.
- Agent03 cannot promote `SeparatedEC-BFMT(E,c,k=1/2)` from the currently
  stated Wave 4/Wave 5 inputs.
- The zero-sampling coefficient audit remains useful but only closes the
  coefficient side; it does not address the conductor-normalized Section 5
  exponent gap.
- The bad-set budget, multiple-zero control, and finite-box H1 assembly are not
  reached by this no-go.
- The correction to carry forward is precise: replace every "conductor/gamma
  costs only polylog" statement in the separated BFMT branch by a mandatory
  conductor-normalized Section 5 exponent audit.
