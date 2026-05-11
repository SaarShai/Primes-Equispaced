---
schema_version: 1
title: "Agent 10 - Delta registry patch plan"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 10 -- Delta Registry Patch Plan"
type: patch-plan
tier: claim-safe
status: RIGOROUS_REDUCTION
confidence: 0.90
scope: "Plan-only edits for the Delta theorem registry and paper draft; no registry/paper source edits applied"
sources:
  - start.md
  - token-economy.yaml
  - L0_rules.md
  - L1_index.md
  - primes-equispaced/L0_rules.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT10_DELTA_THEOREM_B_SENTINEL_2026-05-11.md
  - primes-equispaced/paper/Delta_machine_paper_theorem_registry.md
  - primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
tags: [delta-machine, theorem-registry, patch-plan, ramified-divisor, no-theorem-b-impact]
---

# Agent 10 - Delta Registry Patch Plan

Status enum: `RIGOROUS_REDUCTION`.

## Verdict

Patch only this:

```text
Add Proposition 2.5b:
Ramified correction divisor and axis-pole multiplicities.
```

Also replace stale Open 7.2 / Open 10.2 language about pushing
`zeta x L(s, chi_3)` to `N = 10^6`. The draft already resolves that
case in Section 5.6 by adding the missing log-3 axis-pole lattice.

Do not upgrade Theorem B. Do not edit Paper A / Theorem B files. Do not
route this through BCL, support-4 density, or fixed-level weight-aspect
claims.

## Proposition Statement

Use this exact proposition text, modulo house style for TeX symbols.

```text
Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities).

Let S_ram be a finite set of primes. For each p in S_ram, let

  P_p(z) = c_p prod_{alpha in R_p} (z - alpha)^{m_{p,alpha}},
  P_p(0) != 0.

Set

  E_ram(s) = prod_{p in S_ram} P_p(p^{-s})^{-1}

and let

  I(s) = A(s) M_W(s) E_ram(s),

where A(s) is the remaining global/unramified meromorphic factor and
M_W(s) is the Mellin transform factor.

For alpha = r exp(i theta), every local solution of p^{-s} = alpha is

  s_{p,alpha,k}
    = -log r / log p - i(theta + 2*pi*k) / log p,
    k in Z.

The local contribution lies on the imaginary axis if and only if
|alpha| = 1. With divisor-order convention ord_{s0}(zero)>0 and
ord_{s0}(pole)<0, the full integrand satisfies

  ord_{s0} I
    = ord_{s0}(A M_W)
      - sum_{p,alpha,k: s_{p,alpha,k}=s0} m_{p,alpha}.

Thus the actual pole multiplicity at s0 is max(0, -ord_{s0} I).
Zeros of A(s)M_W(s) at s0 may cancel some or all local ramified poles.
In the no-cancellation case, local root multiplicities and coincident
root/collision multiplicities add.
```

Proof sketch to include:

```text
Since P_p(0) != 0, every root alpha is nonzero. The map s -> p^{-s}
has derivative -log(p) p^{-s}, nonzero at every preimage of alpha.
Therefore a root of order m of P_p pulls back to a zero of order m of
P_p(p^{-s}), and hence to a pole of order m of P_p(p^{-s})^{-1}.
Products add divisor orders. The factors A(s) and M_W(s) add their own
divisor orders, so zeros may cancel local poles. The axis criterion is
Re(s_{p,alpha,k}) = -log|alpha|/log p.
```

No new external theorem claims are needed. This is finite local
complex algebra after the ramified polynomials `P_p` are known.

## Registry Patch Plan

Target:

```text
primes-equispaced/paper/Delta_machine_paper_theorem_registry.md
```

### Registry edit 1 - update Proposition 2.5 stale F2 note

Current lines 117-118 say:

```text
  Verified for ζ × L(s, χ_3) at leading-log order, slope predicted
  −0.303, observed −0.27 (12 % match) at N = 3·10^4.
```

Replace with:

```text
  For zeta x L(s, chi_3), the old 12-19% slope mismatch is resolved
  by the ramified factor (1 - 3^{-2s})^{-1}: the full explicit formula
  with the log-3 axis-pole lattice matches the direct sieved sum to
  6+ digit accuracy at N = 3 * 10^5.
```

Current lines 130-132 say:

```text
- **Comments.** The 12 % mismatch at N = 3·10^4 (and 19 % via slope
  fit) is honestly acknowledged in §5.3 of the draft; sharper
  numerics (N = 10^6) are listed as Open Problem 10.2.
```

Replace with:

```text
- **Comments.** The former zeta x L(s, chi_3) slope mismatch is not a
  pending numerical problem. It was a missing ramified-axis-pole term
  in the Section 5.6 explicit formula. The higher-rank/global
  conditionality of Proposition 2.5 is unchanged.
```

### Registry edit 2 - insert Proposition 2.5b after Proposition 2.5

Insert after the replacement comment above and before
`### Proposition 2.6 (Functoriality)`:

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
- **Source.** Agent 10 Delta registry patch plan; Agent 10 Delta /
  Theorem B sentinel; F2 Cross-Selberg slope diagnosis.
- **Confidence.** **0.90.**
- **Bucket.** Proposition.
- **Load-bearing citations.** None new. This is local finite complex
  algebra after the finite ramified polynomials `P_p` are known.
- **Comments.** This does not assert higher-rank Selberg-class
  membership, global plus-tensor continuation, BCL transfer, or any
  Theorem B upgrade.
```

### Registry edit 3 - replace stale Open 10.2

Current lines 299-301 say:

```text
- **Open 10.2 — Cross-Selberg sharp slope.** Push ζ × L(s, χ_3)
  numerical verification to N = 10^6 to distinguish predicted
  slope − 0.303 from observed − 0.361 at the 5σ level.
```

Replace with:

```text
- **Open 10.2 — Higher-rank ramified correction data.** For general
  cross-Selberg pairs, compute the finite ramified correction
  polynomials `P_p`, identify all axis-pole collisions, and check
  cancellations against `A(s)M_W(s)`. Proposition 2.5b gives the local
  divisor formula once the `P_p` are known; the remaining work is
  higher-rank input data and global continuation, not the resolved
  zeta x L(s, chi_3) numerical slope.
```

### Registry edit 4 - update aggregate summary table

Current line 333:

```text
| Proposition 2.5 (Cross-Selberg)    | Proposition | 0.82 | Macdonald–Cauchy + LWY 2005 |
```

Replace with:

```text
| Proposition 2.5 (Cross-Selberg)    | Proposition | 0.82 | Macdonald-Cauchy + LWY 2005; F2 ramified-axis correction included |
| Proposition 2.5b (Ramified correction divisor) | Proposition | 0.90 | Local finite algebra; no new external theorem claim |
```

## Paper Patch Plan

Target:

```text
primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
```

### Paper edit 1 - repair Proposition 2.5 stale mismatch text

Replace lines 952-964:

```text
the listed cases. The 12% mismatch between predicted slope `−0.303`
and observed slope `−0.27` for `(L_1, L_2) = (ζ, L(\cdot, χ_3))` at
`N = 3 \cdot 10^4` (slope-fit gives `−0.361` with 19% mismatch) is
honestly recorded; sharper numerics at `N = 10^6` are listed as Open
Problem 10.2. ∎

This proposition is **stated as a proposition** (confidence 0.78–
0.85), explicitly reflecting:
(a) the conditional dependence on Selberg-class membership of `L^{(+)}`
in higher rank;
(b) the 12–19% numerical mismatch in the slope fit at moderate `N`,
which suggests either a higher-order term we have not extracted or a
finite-`N` lattice-of-zeros effect; both are Open Problem 10.2.
```

with:

```text
the listed cases. For `(L_1, L_2) = (zeta, L(., chi_3))`, the former
12-19% slope mismatch is resolved in Section 5.6 by the ramified
factor `(1 - 3^{-2s})^{-1}` and its log-3 axis-pole lattice. This
repair is local to the ramified factor and does not remove the
higher-rank Selberg-class conditionality of Proposition 2.5. ∎

This proposition is **stated as a proposition** (confidence 0.78-0.85),
explicitly reflecting the conditional dependence on Selberg-class
membership of `L^{(+)}` in higher rank. The local ramified divisor
bookkeeping used in the resolved zeta x L(s, chi_3) case is isolated
as Proposition 2.5b.
```

### Paper edit 2 - insert Proposition 2.5b before Section 4.3

Insert after the replacement paragraph above and before current line
966 (`### 4.3. Functoriality: Delta : S -> E is a monoid homomorphism`):

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
`Re(s_{p,alpha,k})=-log|alpha|/log p`. ∎

This is a local finite-algebra proposition after the polynomials
`P_p` are known. It does not assert higher-rank Selberg-class
membership or global continuation.
```

### Paper edit 3 - connect Section 5.6 to Proposition 2.5b

After current line 1302:

```text
with $G(s) = L(s, \chi_3)/\zeta(2s)$.
```

insert:

```text
The ramified factor is the `p=3` instance of Proposition 2.5b with
`P_3(z)=1-z^2`; its roots `+1` and `-1` generate the log-3 axis-pole
lattice below.
```

### Paper edit 4 - repair Section 5.6.1 final paragraph

Current line 1327:

```text
The formerly-Open Problem 7.2 is therefore **resolved as a structural fix to the §5.6 statement**, not as a numerical extension to higher $N$. The successor open problem (Open 7.2', §7.2 below) addresses the *general* axis-pole structure for cross-Selberg pairs of higher rank.
```

Replace with:

```text
The formerly-Open Problem 7.2 is therefore **resolved as a structural
fix to the Section 5.6 statement**, not as a numerical extension to
higher `N`. Proposition 2.5b records the local axis-pole divisor
formula. The successor open problem (Open 7.2', Section 7.2 below) is
to compute the relevant ramified correction polynomials and
cancellation data for higher-rank cross-Selberg pairs.
```

### Paper edit 5 - replace stale Section 7.2

Replace current lines 1657-1671:

```text
### Open 7.2. Cross-Selberg sharp slope: ζ × L(s, χ_3) at N = 10^6

> **Open Problem 7.2.** Push the numerical verification of Proposition
> 2.5 (cross-Selberg pair) for `(L_1, L_2) = (ζ, L(s, χ_3))` to `N =
> 10^6` (currently `N = 3 · 10^4` per §5.6). Distinguish at the 5σ
> level the predicted slope `−0.303` from the observed slope `−0.27`
> (12% mismatch) or `−0.361` via slope fit (19% mismatch). Decide
> whether the gap is due to (a) the Macdonald--Cauchy error term
> `ε_p(s)` of Lemma 4.2.1 (which would contribute a `(\log N)^{1/2}`
> shift), or (b) the 50-zero truncation tail.

This open problem is computational. PARI/GP at `mp.dps = 50` and
`zerotype = exact` should reach `N = 10^6` in `~ 6` hours of CPU on a
single core. Resolution would either confirm or refute the
unconditional cross-Selberg slope at higher confidence.
```

with:

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

### Paper edit 6 - update Section 4.6 summary table

After current line 1063:

```text
| Cross-Selberg pair | Proposition 2.5 | 0.78–0.85 | Selberg-class membership of `L^{(+)}`, JPSS for higher rank |
```

insert:

```text
| Ramified correction divisor | Proposition 2.5b | 0.90 | Local finite algebra after `P_p` are known |
```

### Paper edit 7 - update Appendix C table

After current line 2807:

```text
| Proposition 2.5 | Cross-Selberg | 0.78–0.85 | Proposition |
```

insert:

```text
| Proposition 2.5b | Ramified correction divisor | 0.90 | Proposition |
```

### Paper edit 8 - update final one-page summary table

After current line 4196:

```text
| Proposition 2.5 | Cross-Selberg pair | Proposition | 0.78–0.85 |
```

insert:

```text
| Proposition 2.5b | Ramified correction divisor | Proposition | 0.90 |
```

### Paper edit 9 - update closing open-problem summary

Current lines 4247-4250 say:

```text
(4) **Open problems are stratified by tractability.** Open 7.2 (CPU-
bound) and Open 7.5 (Lean engineering) are within 6–12 months of
work. Open 7.1, 7.3, 7.9, 7.11, 7.12 are major problems of
analytic number theory; the Δ-machine reformulates but does not
```

Replace the first two sentences with:

```text
(4) **Open problems are stratified by tractability.** Open 7.2' is now
a higher-rank ramified-data problem, since the old zeta x L(s, chi_3)
slope mismatch is resolved by Proposition 2.5b and Section 5.6. Open
7.5 (Lean engineering) remains within 6-12 months of work. Open 7.1,
7.3, 7.9, 7.11, 7.12 are major problems of analytic number theory;
the Delta-machine reformulates but does not
```

## No-Theorem-B Boundary

Required guard text for any later registry/paper patch:

```text
Boundary. Proposition 2.5b is local finite algebra after the ramified
polynomials P_p are known. It does not imply BCL, support-4
fixed-level density, at-zeros second moments of L', a fixed-level
weight-aspect transfer, or any Theorem B exact-route upgrade.
```

Do not add:

```text
Theorem B-exact consequence;
BCL transfer consequence;
support-4 density consequence;
Paper A status change;
unconditional higher-rank plus-tensor continuation;
email or correspondence draft.
```

The Theorem B sentinel remains intact: Delta/Open 7.2' has no
Theorem B-exact impact.

## Verification Notes

Commands/checks run:

```text
./te doctor
sed -n targeted reads for start.md, token-economy.yaml, L0_rules.md,
  L1_index.md, primes-equispaced/L0_rules.md,
  primes-equispaced/L1_index.md
sed/rg targeted reads for Wave 1 synthesis, Agent 10 sentinel,
  Delta theorem registry, and Delta paper draft snippets
rg terms: Proposition 2.5, Open 7.2, Open 10.2, ramified,
  axis-pole, Theorem B, BCL, support-4
```

Observed:

```text
./te doctor returned ok: true.
Registry still contains stale zeta x L(s, chi_3) mismatch / N=10^6
language.
Paper Section 5.6 already resolves the mismatch via the log-3
axis-pole lattice.
Paper Section 7.2 still contains the stale old Open 7.2.
Agent 10 sentinel explicitly bars Theorem B impact.
```

Citation protocol:

```text
No new external theorem claims are added in this plan.
The new Proposition 2.5b is local finite algebra. Existing external
citations in Proposition 2.5 remain existing paper dependencies, not
new claims introduced here.
```

No Koyama correspondence or email draft was opened, edited, or
proposed.

No numerical computation was needed.

## Changed Files

Actual file created by this task:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md
```

Files intentionally not edited:

```text
primes-equispaced/paper/Delta_machine_paper_theorem_registry.md
primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
```
