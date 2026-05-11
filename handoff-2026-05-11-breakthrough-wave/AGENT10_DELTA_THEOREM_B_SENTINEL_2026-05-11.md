---
schema_version: 1
title: "Agent 10 - Delta / Theorem B sentinel"
date: 2026-05-11
agent: "Agent 10 -- Delta / Theorem B Sentinel"
type: theorem-registry-audit
tier: claim-safe
status: RIGOROUS_REDUCTION
confidence: 0.88
scope: "Delta Open 7.2' ramified axis-pole multiplicities; Theorem B exact-route guard"
sources:
  - start.md
  - token-economy.yaml
  - L0_rules.md
  - L1_index.md
  - primes-equispaced/L0_rules.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/HANDOFF.md
  - primes-equispaced/L2_facts/farey-current-state.md
  - primes-equispaced/L2_facts/farey-claim-ledger.md
  - primes-equispaced/SESSION_SUMMARY_2026-05-09.md
  - primes-equispaced/handoff-2026-05-11/HANDOFF.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT8_THEOREM_B_DELTA_SCOUT.md
  - primes-equispaced/handoff-2026-05-09-followup/Cross_Selberg_slope_diagnosis.md
  - primes-equispaced/paper/Delta_machine_paper_theorem_registry.md
  - primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
  - primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/Delta_machine_extended.md
  - primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/Delta_machine_multi_L.md
tags: [delta-machine, theorem-b, open-7-2-prime, axis-poles, theorem-registry]
---

# Agent 10 - Delta / Theorem B Sentinel

Status: `RIGOROUS_REDUCTION`.

## Verdict

The recent Delta/Open 7.2 work can become a theorem-registry upgrade only in a narrow form:

```text
Add a Delta local proposition:
Ramified correction divisor / axis-pole multiplicity formula.
```

Do not upgrade Theorem B. Do not reopen the closed Theorem B-exact routes. The BCL transfer remains closed for Theorem B-exact unconditional, and the Delta axis-pole proposition has no support-4 fixed-level density content.

Recommended registry action:

1. Replace stale Open 10.2 / Open 7.2 numerical-slope language with resolved-F2 language.
2. Add a new Proposition-level entry, e.g. `Proposition 2.5b (Ramified correction divisor)`, confidence `0.88-0.92`.
3. Keep broad higher-rank Cross-Selberg / plus-tensor global claims separate and conditional.
4. Coordinate with the draft: the draft says successor Open 7.2' is in section 7.2, but the current section 7.2 text still contains the old numerical Open 7.2.

No registry file was edited in this packet.

## Local Proposition Candidate

Let `S` be a finite set of ramified primes. For each `p in S`, let

```text
P_p(z) = c_p prod_alpha (z - alpha)^(m_p,alpha),
P_p(0) != 0.
```

Let

```text
I(s) = A(s) M(s) prod_(p in S) P_p(p^(-s))^(-1),
```

where `A(s)` is the remaining global/unramified meromorphic factor and `M(s)` is the Mellin transform factor.

For every zero `alpha = r exp(i theta)` of `P_p`, the local ramified factor has candidate poles at

```text
s_(p,alpha,k)
  = -log(r)/log(p) - i(theta + 2*pi*k)/log(p),
  k in Z.
```

The pole lies on the imaginary axis iff `|alpha| = 1`.

At any point `s0`, in divisor-order notation,

```text
ord_s0 I
  = ord_s0(A M)
    - sum_{p,alpha,k: s_(p,alpha,k)=s0} m_p,alpha.
```

Thus the actual pole multiplicity is

```text
max(0, -ord_s0 I).
```

In the generic no-cancellation case this is just:

```text
local root multiplicities
+ coincident-root/collision multiplicities
+ Mellin/global pole order.
```

If `A(s)M(s)` has a zero at the same point, it can cancel some or all of the local pole. The registry statement must include this cancellation clause.

Proof is finite local algebra. Since `P_p(0) != 0`, each root `alpha` is nonzero. The map `s -> p^(-s)` has derivative `-log(p) p^(-s)`, nonzero at every solution. Therefore a root of order `m` of `P_p` pulls back to a zero of order `m` of `P_p(p^(-s))`, hence a pole of order `m` of its reciprocal. Products add divisor orders. Mellin/global factors add their own divisor orders. Axis classification follows from `Re(s_(p,alpha,k)) = -log|alpha|/log p`.

## Regression Check: F2

For `zeta x L(s, chi_3)`, the ramified factor is

```text
(1 - 3^(-2s))^(-1).
```

Equivalently `P_3(z)=1-z^2`, with roots `alpha=+1,-1`. Both roots are on the unit circle. The formula gives

```text
s = i*pi*k/log 3,  k in Z,
```

matching the F2 axis-pole lattice. At `s=0`, the local pole collides with the Gaussian Mellin pole, giving the double pole responsible for the `c0 log N` term. This is exactly the structural fix in `Cross_Selberg_slope_diagnosis.md`: the old 12-19 percent slope mismatch was missing the log-3 axis-pole sum, not a failure of the leading slope.

## Adversarial Opportunity Scan

### Opportunity A: registry upgrade

Passes as a local proposition. It is independent of higher-rank functoriality once the finite ramified correction polynomials `P_p` are explicitly written down.

Claim-safe scope:

```text
Given P_p, classify local ramified pole lattice and multiplicities.
```

Do not state:

```text
All higher-rank Cross-Selberg pairs have the required Selberg-class global continuation.
```

That is still outside this local proposition.

### Opportunity B: stale registry repair

The registry still records Proposition 2.5 with old mismatch language and Open 10.2 as a numerical extension to `N=10^6`. Current handoff/draft/log say F2 resolved that mismatch structurally. This is a real registry-maintenance opportunity, not a new theorem.

Safe replacement:

```text
Open 7.2 resolved for zeta x chi_3 by explicit ramified axis poles.
Successor 7.2' asks for the general local ramified divisor formula.
```

### Opportunity C: improve the statement before promotion

Agent 8's proposed statement says multiplicities add. That is right for local collisions, but incomplete unless divisor-order cancellation is stated. A zero of `A(s)M(s)` at the same point can cancel local poles. The registry version should use the divisor formula above.

### No-Go A: Theorem B exact

No Theorem B-exact route appears.

Reasons inherited from current handoff and Agent 8:

- BCL is GRH-conditional in the checked source packet.
- BCL is `q`-averaged over levels, not fixed-level weight-aspect.
- BCL is 1-level density, not the 2-level / 4-shift data needed for the at-zeros second moment of `L'`.
- Even a hypothetical averaged transfer would still face the fixed-level support-4 Grand Density wall.

Therefore:

```text
Delta Open 7.2' does not change Paper A / Theorem B status.
```

### No-Go B: broad Cross-Selberg promotion

Do not upgrade the full broad Proposition 2.5 to theorem-grade from this packet. The old sources still carry global plus-tensor / Selberg-class membership caveats, and the local `P_p` proposition deliberately avoids that global assertion.

Also keep the higher-rank elementary-symmetric/Cauchy identity route under review. The local proposition does not need the contested global product identity; it only needs the already-computed finite polynomial `P_p`.

## Theorem-Registry Draft Entry

Suggested entry text:

```text
### Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities)

Statement. Let E_ram(s)=prod_{p in S} P_p(p^{-s})^{-1}, with each
P_p(0) != 0. If P_p(z)=c_p prod_alpha (z-alpha)^{m_p,alpha},
then the divisor of E_ram is supported at

  s = -log|alpha|/log p - i(arg alpha + 2*pi*k)/log p.

The contribution is on the imaginary axis iff |alpha|=1. At each s0,
local multiplicities add over all triples (p,alpha,k) giving s0.
For the full integrand A(s)M_W(s)E_ram(s), add the divisor orders of
A and M_W; zeros may cancel local poles.

Source. Agent 10 Delta/Theorem B sentinel; Agent 8 Delta scout; F2
Cross-Selberg slope diagnosis.

Confidence. 0.90.

Bucket. Proposition.

Comments. Pure local finite algebra after P_p is known. Does not assert
higher-rank Selberg-class membership or any Theorem B transfer.
```

## Verification Notes

Commands/checks run:

- `./te doctor` returned `ok: true`.
- Read boot/index files: `start.md`, `token-economy.yaml`, `L0_rules.md`, `L1_index.md`, `primes-equispaced/L0_rules.md`, `primes-equispaced/L1_index.md`.
- Targeted reads: current handoffs, L2 claim/current-state facts, session summary, Agent 8, wave synthesis, F2 diagnosis, Delta draft, theorem registry, and the relevant old Delta snippets.
- Targeted search terms: `Delta`, `Open 7.2`, `7.2'`, `axis-pole`, `ramified`, `Theorem B`, `theorem registry`, `BCL`, `support-4`.
- No broad archive page was used as evidence.
- No external theorem claim is newly made here. BCL source status is inherited from Agent 8's citation-protocol packet, not re-cited as a fresh claim.
- No Koyama correspondence/email draft was opened or edited.

No numerical computation was needed. The proof above is finite local complex analysis.

## Changed Files

Created:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT10_DELTA_THEOREM_B_SENTINEL_2026-05-11.md
```

No other file was intentionally changed.
