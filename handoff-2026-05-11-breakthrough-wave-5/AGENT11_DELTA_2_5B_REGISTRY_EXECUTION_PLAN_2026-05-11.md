---
title: "Agent 11 Delta-2.5b Registry Execution Plan"
date: 2026-05-11
type: theorem-registry-execution-plan
tier: theorem-level-secondary
status: RIGOROUS_REDUCTION
confidence: 0.91
tags: [breakthrough-wave-5, delta-machine, delta-2-5b, ramified-correction-divisor, axis-pole-multiplicity, no-theorem-b-impact]
---

## Verdict

Execute Delta-2.5b as a secondary theorem-registry patch:
add Proposition 2.5b, "Ramified correction divisor and axis-pole
multiplicities", and use it to replace the stale zeta x L(s, chi_3)
Open 7.2 / Open 10.2 slope-check language.

This is theorem-level local algebra after the finite ramified
polynomials P_p are known. It is not a Theorem B input. If the patch
cannot pass the acceptance checks below, archive the lane as
secondary-only and do not promote any main theorem claim.

Status: RIGOROUS_REDUCTION.

## Theorem Target

Target label:

```text
Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities).
```

Target statement:

```text
Let S_ram be a finite set of primes. For each p in S_ram, let

  P_p(z) = c_p prod_alpha (z - alpha)^{m_{p,alpha}},
  P_p(0) != 0.

Set

  E_ram(s) = prod_{p in S_ram} P_p(p^{-s})^{-1}

and let

  I(s) = A(s) M_W(s) E_ram(s),

where A(s) is the remaining global/unramified meromorphic factor and
M_W(s) is the Mellin transform factor.

For alpha = r exp(i theta), the local solutions of p^{-s} = alpha are

  s_{p,alpha,k}
    = -log r / log p - i(theta + 2*pi*k) / log p,
    k in Z.

The local contribution lies on the imaginary axis if and only if
|alpha| = 1. With divisor-order convention ord_{s0}(zero)>0 and
ord_{s0}(pole)<0,

  ord_{s0} I
    = ord_{s0}(A M_W)
      - sum_{p,alpha,k: s_{p,alpha,k}=s0} m_{p,alpha}.

Hence the actual pole multiplicity at s0 is max(0, -ord_{s0} I).
Zeros of A(s)M_W(s) may cancel some or all local ramified poles.
In the no-cancellation case, coincident local root multiplicities add.
```

Proof core:

```text
Since P_p(0) != 0, each root alpha is nonzero. The map s -> p^{-s}
has derivative -log(p)p^{-s}, nonzero at every preimage of alpha.
Thus a root of P_p of multiplicity m pulls back to a zero of
P_p(p^{-s}) of multiplicity m and to a pole of P_p(p^{-s})^{-1} of
multiplicity m. Product divisor orders add, including the orders of
A(s) and M_W(s). The axis criterion is
Re(s_{p,alpha,k}) = -log|alpha|/log p.
```

Required worked example:

```text
For zeta x L(s, chi_3),
  E_ram(s) = (1 - 3^{-2s})^{-1},
  P_3(z) = 1 - z^2,
  roots are +1 and -1,
  the combined axis lattice is s = i*pi*k/log 3.
```

This target does not assert higher-rank plus-tensor continuation or
upgrade Proposition 2.5 globally. It only supplies the local ramified
divisor and multiplicity bookkeeping once P_p is known.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT11_SECONDARY_DELTA_BPLUS_DPAC_TRIAGE_2026-05-11.md`: selects Delta-2.5b over B+ and DPAC as the only immediately theorem-shaped secondary task; explicitly says no Theorem B impact.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md`: gives the Proposition 2.5b statement, proof sketch, registry patch plan, draft patch plan, and no-Theorem-B boundary.
- `primes-equispaced/paper/Delta_machine_paper_theorem_registry.md`: current registry still contains stale zeta x L(s, chi_3) mismatch language in Proposition 2.5, Open 10.2, and the aggregate table; Proposition 2.5b is absent.
- `primes-equispaced/paper/Delta_machine_paper_compositio_draft.md`: Section 5.6 already contains the resolved ramified factor `(1 - 3^{-2s})^{-1}`, log-3 axis-pole lattice, and 6+ digit match, but earlier/later stale Open 7.2 and slope-mismatch text remains.
- `primes-equispaced/L2_facts/farey-claim-ledger.md`: top-10 secondary update says Delta-2.5b is the next theorem-shaped secondary task and preserves no Theorem B impact; B+ remains sign-cluster classification; DPAC remains proof hygiene.

## Patch Plan

Scope for the future patch:

```text
Patch only:
  primes-equispaced/paper/Delta_machine_paper_theorem_registry.md
  primes-equispaced/paper/Delta_machine_paper_compositio_draft.md

Do not edit Paper A, Theorem B files, B+ files, DPAC files, or
correspondence/email drafts.
```

### Registry edits

R1. In `Delta_machine_paper_theorem_registry.md`, inside Proposition
2.5, replace the stale zeta x L(s, chi_3) verification sentence with:

```text
  For zeta x L(s, chi_3), the old 12-19% slope mismatch is resolved
  by the ramified factor (1 - 3^{-2s})^{-1}: the full explicit formula
  with the log-3 axis-pole lattice matches the direct sieved sum to
  6+ digit accuracy at N = 3 * 10^5.
```

R2. In the same Proposition 2.5 comments, replace the stale
`N = 10^6` Open 10.2 language with:

```text
- **Comments.** The former zeta x L(s, chi_3) slope mismatch is not a
  pending numerical problem. It was a missing ramified-axis-pole term
  in the Section 5.6 explicit formula. The higher-rank/global
  conditionality of Proposition 2.5 is unchanged.
```

R3. Insert this block immediately after Proposition 2.5 and before
Proposition 2.6:

```text
### Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities)

- **Statement.** Let `S_ram` be a finite set of primes and
  `E_ram(s)=prod_{p in S_ram} P_p(p^{-s})^{-1}`, with each
  `P_p(0) != 0`. If
  `P_p(z)=c_p prod_alpha (z-alpha)^{m_{p,alpha}}`, then the local
  divisor of `E_ram` is supported at
  `s=-log|alpha|/log p - i(arg alpha + 2*pi*k)/log p`, `k in Z`.
  The contribution is on the imaginary axis if and only if
  `|alpha|=1`. For the full integrand
  `I(s)=A(s)M_W(s)E_ram(s)`,
  `ord_{s0} I = ord_{s0}(A M_W)
  - sum_{p,alpha,k: s_{p,alpha,k}=s0} m_{p,alpha}`. Hence zeros of
  `A(s)M_W(s)` may cancel local ramified poles; without cancellation,
  coincident local multiplicities add.
- **Source.** Agent 10 Delta registry patch plan; Agent 11 Delta-2.5b
  registry execution plan; F2 Cross-Selberg slope diagnosis.
- **Confidence.** **0.90.**
- **Bucket.** Proposition.
- **Load-bearing citations.** None new. This is local finite complex
  algebra after the finite ramified polynomials `P_p` are known.
- **Comments.** This does not assert higher-rank Selberg-class
  membership, global plus-tensor continuation, BCL transfer, or any
  Theorem B upgrade.
```

R4. Replace Open 10.2 with:

```text
- **Open 10.2 - Higher-rank ramified correction data.** For general
  cross-Selberg pairs, compute the finite ramified correction
  polynomials `P_p`, identify all axis-pole collisions, and check
  cancellations against `A(s)M_W(s)`. Proposition 2.5b gives the local
  divisor formula once the `P_p` are known; the remaining work is
  higher-rank input data and global continuation, not the resolved
  zeta x L(s, chi_3) numerical slope.
```

R5. In the aggregate confidence table, replace the Proposition 2.5
row with these two rows:

```text
| Proposition 2.5 (Cross-Selberg)    | Proposition | 0.82 | Macdonald-Cauchy + LWY 2005; F2 ramified-axis correction included |
| Proposition 2.5b (Ramified correction divisor) | Proposition | 0.90 | Local finite algebra; no new external theorem claim |
```

### Draft edits

D1. In `Delta_machine_paper_compositio_draft.md`, replace the stale
Proposition 2.5 proof-tail paragraph beginning with "The 12% mismatch
between predicted slope" through the following explanatory paragraph
with:

```text
the listed cases. For `(L_1, L_2) = (zeta, L(., chi_3))`, the former
12-19% slope mismatch is resolved in Section 5.6 by the ramified
factor `(1 - 3^{-2s})^{-1}` and its log-3 axis-pole lattice. This
repair is local to the ramified factor and does not remove the
higher-rank Selberg-class conditionality of Proposition 2.5. [proof end]

This proposition is **stated as a proposition** (confidence 0.78-0.85),
explicitly reflecting the conditional dependence on Selberg-class
membership of `L^{(+)}` in higher rank. The local ramified divisor
bookkeeping used in the resolved zeta x L(s, chi_3) case is isolated
as Proposition 2.5b.
```

Use the draft's existing proof-end symbol/style in place of
`[proof end]`.

D2. Insert Proposition 2.5b immediately after Proposition 2.5 and
before Section 4.3:

```text
> **Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities).**
> Let `S_ram` be a finite set of primes. For each `p in S_ram`, let
> `P_p(z)=c_p prod_alpha (z-alpha)^{m_{p,alpha}}` with `P_p(0) != 0`.
> Set `E_ram(s)=prod_{p in S_ram} P_p(p^{-s})^{-1}` and
> `I(s)=A(s)M_W(s)E_ram(s)`, where `A(s)` is the remaining
> global/unramified meromorphic factor. For `alpha=r exp(i theta)`,
> the local ramified preimages are
> `s_{p,alpha,k}=-log r/log p - i(theta+2*pi*k)/log p`, `k in Z`.
> The contribution lies on the imaginary axis if and only if
> `|alpha|=1`. At each `s0`,
> `ord_{s0} I = ord_{s0}(A M_W)
> - sum_{p,alpha,k: s_{p,alpha,k}=s0} m_{p,alpha}`.
> Hence the pole multiplicity is `max(0, -ord_{s0} I)`, with possible
> cancellation by zeros of `A(s)M_W(s)`.
> Confidence: 0.90.

*Proof.* Since `P_p(0) != 0`, every root `alpha` is nonzero. The map
`s -> p^{-s}` has nonzero derivative `-log(p)p^{-s}` at every preimage
of `alpha`, so a root of order `m` pulls back to a zero of order `m`
of `P_p(p^{-s})` and therefore to a pole of order `m` of its
reciprocal. Divisor orders add under products, including the orders of
`A(s)` and `M_W(s)`. The axis criterion follows from
`Re(s_{p,alpha,k})=-log|alpha|/log p`. [proof end]

This is a local finite-algebra proposition after the polynomials
`P_p` are known. It does not assert higher-rank Selberg-class
membership or global continuation.
```

D3. In Section 5.6, immediately after:

```text
with G(s) = L(s, chi_3)/zeta(2s).
```

insert:

```text
The ramified factor is the p=3 instance of Proposition 2.5b with
`P_3(z)=1-z^2`; its roots `+1` and `-1` generate the log-3 axis-pole
lattice below.
```

D4. Replace the final paragraph of Section 5.6.1 with:

```text
The formerly-Open Problem 7.2 is therefore resolved as a structural
fix to the Section 5.6 statement, not as a numerical extension to
higher `N`. Proposition 2.5b records the local axis-pole divisor
formula. The successor open problem (Open 7.2', Section 7.2 below) is
to compute the relevant ramified correction polynomials and
cancellation data for higher-rank cross-Selberg pairs.
```

D5. Replace Section 7.2 with:

```text
### Open 7.2'. Higher-rank ramified correction data

> **Open Problem 7.2'.** For cross-Selberg pairs beyond the resolved
> `(zeta, L(s, chi_3))` case, compute the finite ramified correction
> polynomials `P_p`, identify all axis-pole collisions from
> Proposition 2.5b, and determine whether zeros of the global factor
> `A(s)M_W(s)` cancel any local ramified poles.

This is no longer the old `N = 10^6` slope-check problem. The
`zeta x L(s, chi_3)` discrepancy is resolved by the explicit
`(1 - 3^{-2s})^{-1}` ramified factor and its log-3 axis-pole lattice.
The remaining open work is higher-rank ramified input data plus the
global continuation hypotheses already separated in Proposition 2.5
and Open 7.3.
```

D6. Update all local evidence and summary references that still treat
the slope mismatch as live:

```text
Section 4.6 summary table:
  add `Ramified correction divisor | Proposition 2.5b | 0.90 |
  Local finite algebra after P_p are known`.

Section 5 aggregate table:
  replace the Cross-Selberg row with a 6+ digit formula-match row at
  N = 3 * 10^5 using the ramified-axis correction.
  Replace "supports Proposition 2.5 with the noted slope mismatch"
  with "supports Proposition 2.5 with the ramified correction recorded
  in Proposition 2.5b".

Section 9.8:
  replace "notably Open Problem 7.2 at N = 10^6" with the higher-rank
  ramified correction-data continuation.

Appendix C confidence table:
  add `Proposition 2.5b | Ramified correction divisor | 0.90 |
  Proposition`.

Appendix F demotion note for Cross-Selberg:
  replace the stale "12% slope mismatch ... Open Problem 7.2 ... N =
  10^6" note with the Section 5.6 resolved-ramified-axis diagnosis.

Appendix L red flag #2:
  replace the live referee objection with a resolved historical note:
  the mismatch was caused by the omitted p=3 ramified-axis factor, and
  the remaining referee risk is higher-rank P_p/global-continuation
  input, not the zeta x L(s, chi_3) slope.

Appendix S one-page summary table:
  add `Proposition 2.5b | Ramified correction divisor | Proposition |
  0.90`.

Appendix T closing observations:
  replace Open 7.2 as CPU-bound with Open 7.2' as higher-rank
  ramified-data work, and remove "slope-fit mismatches" as a live
  adversarial-review target.
```

## Acceptance Checks

Packet-format acceptance for this handoff file:

```bash
packet="primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT11_DELTA_2_5B_REGISTRY_EXECUTION_PLAN_2026-05-11.md"

test -f "$packet"
sed -n '1,40p' "$packet"

rg -n "^title:|^date:|^type:|^tier:|^status: RIGOROUS_REDUCTION$|^confidence:|^tags:" "$packet"
rg -n "^## Verdict$|^## Theorem Target$|^## Source Anchors$|^## Patch Plan$|^## Acceptance Checks$|^## Overclaim Guardrails$|^## Dependency Impact$" "$packet"
```

Registry/draft positive checks after the future patch:

```bash
targets="primes-equispaced/paper/Delta_machine_paper_theorem_registry.md primes-equispaced/paper/Delta_machine_paper_compositio_draft.md"

rg -n -F "Proposition 2.5b" $targets
rg -n -F "Ramified correction divisor" $targets
rg -n -F "axis-pole" $targets
rg -n -F "P_3(z)=1-z^2" $targets
rg -n -F "roots `+1` and `-1`" $targets
rg -n -F "s = i*pi*k/log 3" $targets
rg -n -F "(1 - 3^{-2s})^{-1}" $targets
rg -n -F "higher-rank ramified correction data" $targets
```

Registry/draft stale-language rejection after the future patch:

```bash
targets="primes-equispaced/paper/Delta_machine_paper_theorem_registry.md primes-equispaced/paper/Delta_machine_paper_compositio_draft.md"

rg -n -F \
  -e "Open 7.2. Cross-Selberg sharp slope" \
  -e "Open 10.2" \
  -e "N = 10^6" \
  -e "listed as Open Problem 10.2" \
  -e "sharper numerics at" \
  -e "noted slope mismatch" \
  -e "proposition with 12" \
  -e "slope-fit mismatches" \
  -e "CPU-bound" \
  $targets
```

Pass condition: the stale-language rejection command returns no live
pending-slope hits. Historical mentions are allowed only when the same
sentence or neighboring sentence explicitly says former, old,
resolved, or no longer pending.

No-Theorem-B leakage check:

```bash
targets="primes-equispaced/paper/Delta_machine_paper_theorem_registry.md primes-equispaced/paper/Delta_machine_paper_compositio_draft.md"

rg -n -F -e "Theorem B" -e "BCL" -e "support-4" -e "fixed-level" -e "at-zeros" $targets
```

Pass condition: no new positive claims using those terms. Best pass is
zero hits in the registry/draft targets. If existing unrelated hits
are present, the patch diff must not add or strengthen them.

Worked-example check:

```bash
rg -n -F \
  -e "E_ram(s) = (1 - 3^{-2s})^{-1}" \
  -e "P_3(z)=1-z^2" \
  -e "roots `+1` and `-1`" \
  -e "log-3 axis-pole lattice" \
  primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
```

Pass condition: the zeta x L(s, chi_3) regression is explicitly tied
to Proposition 2.5b and not presented as a new numerical open problem.

## Overclaim Guardrails

- Do not claim any Theorem B consequence from Delta-2.5b.
- Do not claim BCL transfer, support-4 density, fixed-level
  de-averaging, or at-zeros second moments of L'.
- Do not claim unconditional higher-rank plus-tensor Selberg-class
  membership or global Cross-Selberg continuation from Proposition
  2.5b.
- Do not upgrade Proposition 2.5 as a whole to a theorem; only add the
  local ramified divisor proposition with confidence 0.90.
- Do not revive B+ positivity. B+ remains finite sign-cluster
  classification only.
- Do not infer B(p) sign from T(p-1).
- Do not state DPAC from linear independence. DPAC still needs finite
  phase avoidance, a certified bridge, or an external all-zero phase
  theorem.
- Do not add email/correspondence language or Paper A status changes.

Mandatory boundary text for the later patch:

```text
Boundary. Proposition 2.5b is local finite algebra after the ramified
polynomials P_p are known. It does not imply BCL, support-4
fixed-level density, at-zeros second moments of L', a fixed-level
weight-aspect transfer, or any Theorem B exact-route upgrade.
```

## Dependency Impact

Delta-2.5b improves secondary Delta theorem hygiene only. It converts
the resolved zeta x L(s, chi_3) ramified-axis diagnosis into a local
registry proposition and replaces the stale Open 7.2 / Open 10.2
`N = 10^6` slope-check framing with a higher-rank ramified-data task.

Main theorem dependency impact: none. Theorem B, H1/H2 EC smoothing,
GL1 sharp cutoff, B+ positivity, and pointwise zeta-zero DPAC remain
unchanged.

Failure mode: if the registry/draft patch cannot state Proposition
2.5b with the exact local divisor formula, the p=3 worked example, and
the no-Theorem-B boundary, archive this direction as secondary-only.
