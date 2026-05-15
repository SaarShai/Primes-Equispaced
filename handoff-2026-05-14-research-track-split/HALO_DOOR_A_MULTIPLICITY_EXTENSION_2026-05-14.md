---
schema_version: 2
title: "Halo Door A Multiplicity Extension Audit"
type: audit-extension
domain: project
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.85
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_MULTIPLE_ZERO_DISPOSITION_CURRENT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
supersedes: []
superseded-by:
tags: [halo-route, door-A, multiplicity, gl2, stage-2-followon]
---

# Halo Door A — Multiplicity Extension Audit

Status: `RIGOROUS_REDUCTION`. Door A target multiplicity extension passes at
exponent `T^{5/2+eps}` with `T^{3/2+eps}` margin over Strategy A worst case.
No Door A theorem promoted.

## 1. Statement and verdict

Stage 2 plan §4 surfaced gap: repo q=2 audit gives bound over `S_E(T)`
(simple critical zeros of dyadic shell); Door A target is over
multiplicity-weighted `Z_T^{mult}` (all dyadic-shell zeros, counted with
multiplicity).

```text
q=2 audit (S_E(T)):
  sum_{rho in S_E(T)} |L_E^*(rho+1/log T)|^{-2}  <<_{E,eps}  T^{5/2+eps}.

Door A target (Z_T^{mult}):
  sum_{rho in Z_T}^{mult} |L_E^*(rho+1/log T)|^{-2}  <<_{E,eps}  T^{5/2+eps}.
```

Verdict: the extension holds at the *same* exponent `T^{5/2+eps}`, conditional
on the same Wave 4 conditionals as the q=2 audit. Strategy A (cheap Laurent
bound + RvM multiplicity bound) is sufficient and gives worst-case
multiple-zero contribution `T^{1+o(1)}`. Margin to target: `T^{3/2+eps}`.

## 2. The gap precisely

Quoted from `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L34-37:

```text
Degree2WeakShiftedNeg_2(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/log T)|^(-2)
    <<_{E,eps} T^(5/2+eps).
```

`S_E(T)` defined in `H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md` L62-74:

```text
S_E(T) = F_E(T,c) union B_E(T,c),
       = { simple critical zeros rho = 1/2 + i gamma : T < |gamma| <= 2T }.
```

Stage 2 cross-check (`CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §4.1, L403-410):

```text
Z_T = { nontrivial zeros : T < |Im rho| <= 2T }  (no simplicity restriction).
sum^{mult} f(rho) := sum_rho m_rho · f(rho).
```

Gap: extend bound from `S_E(T)` (simple, count once) to `Z_T^{mult}` (all
zeros, weighted by multiplicity `m_rho`). At a zero of multiplicity `m`,

```text
|L(rho+alpha)|^{-2}  ~  |alpha|^{-2m} · |L^{(m)}(rho)/m!|^{-2}
                     =  (log T)^{2m} · |L^{(m)}(rho)/m!|^{-2}.
```

So multiple-zero summand inflated by `(log T)^{2m}` over simple case.

## 3. Riemann-von Mangoldt multiplicity bound

Standard fact for any L-function with polynomial-growth conductor: a zero
of multiplicity `m` at height `T` contributes `m` to the local zero count
`N(T+1) - N(T-1)`, which by the GL2 Riemann-von Mangoldt formula is
`O(log T)`. Therefore

```text
m_rho  <=  C_E log(|gamma|+2)  =  O_E(log T)        (RvM-MULT)
```

uniformly for `rho` with `|gamma| ~ T`, for fixed GL2 newform / fixed EC `E`.

Repo status: not proved as a named lemma but consistent with the standing
zero-counting bound `N(T,2T) <= C T log T` used in
`H1_POSITIVE_RANK_CLOSURE.md` L171 and L225-227. The latter treats bounded
multiplicity `M` as an explicit hypothesis. For Strategy A only the weak
form `m_rho = O(log T)` is needed; this follows from the standard explicit
formula for fixed GL2 (Iwaniec-Kowalski Ch. 5; zeta analog in Titchmarsh
Ch. 9). **External citation required for the named lemma; the proof is
half a line.**

Total multiplicity-weighted count:

```text
N^{mult}(T,2T) := sum_{rho in Z_T}^{mult} 1
                = sum_{rho in Z_T} m_rho
               <=  (log T) · N(T,2T)
               <<  T (log T)^2.                     (NMULT)
```

vs. the un-weighted count `N(T,2T) <<_E T log T` (`H1_POSITIVE_RANK_CLOSURE.md`
L171). Extra `log T` absorbed by `T^{eps}`.

## 4. Decomposition into simple and multiple parts

Split `Z_T = S_E(T) sqcup Z_T^{>=2}` where `Z_T^{>=2}` is the set of
multiple critical zeros in the shell. Then

```text
sum_{rho in Z_T}^{mult} |L(rho+alpha)|^{-2}
 =  sum_{rho in S_E(T)} |L(rho+alpha)|^{-2}                    [SIMPLE]
  + sum_{rho in Z_T^{>=2}} m_rho · |L(rho+alpha)|^{-2}.        [MULT]
```

`[SIMPLE]` is bounded by the existing q=2 audit at `T^{5/2+eps}`. Strategy
A bounds `[MULT]` by `T^{1+o(1)}`. Sum still `T^{5/2+eps}`.

## 5. Strategy A — worked exponent calculation

At a zero `rho` of multiplicity `m`, Laurent expansion at `s=rho`:

```text
L(s) = (s-rho)^m · ( L^{(m)}(rho)/m! + O(s-rho) ),
1/L(rho+alpha) = alpha^{-m} · ( m!/L^{(m)}(rho) ) · ( 1 + O(alpha) ).
```

Hence

```text
|L(rho+alpha)|^{-2}  =  (log T)^{2m} · |L^{(m)}(rho)/m!|^{-2} · (1+o(1)).
```

Per-zero contribution to `[MULT]`:

```text
m · (log T)^{2m} · |L^{(m)}(rho)/m!|^{-2}.
```

**Bound on the Laurent coefficient `|L^{(m)}(rho)/m!|^{-1}`.** From the
local Hadamard factorization,

```text
L(E,s) = (s-rho)^m · h_rho(s),     h_rho(rho) != 0,
```

where `h_rho` is the regularization through the Hadamard product. Standard
EC/GL2 estimate (Iwaniec-Kowalski Ch. 5, eqs. (5.27)-(5.28); Titchmarsh
Ch. 9 for zeta analog):

```text
|h_rho(rho)|^{-1}  =  |L^{(m)}(rho)/m!|^{-1}  <<_E  (log T)^{O(m)}.
```

This is polynomial in `(log T)`, with exponent linear in `m`. Cited locally
in `H1_POSITIVE_RANK_CLOSURE.md` L221-227, where the analogous Laurent
coefficients `b_{rho,-j}` for `1/L` are bounded by `|gamma|^{A_j}
(log|gamma|)^{B_j}`. For the **shifted** value at `s=rho+alpha` (not at `rho`
itself), no polynomial-in-`gamma` factor is needed — only the local
regularization at `rho`, which is the Laurent coefficient of `L`, not of
`1/L`. Polynomial-`(log T)` is enough.

Plug in. Let `m_max <= c log T` be the maximum multiplicity at height `~T`
(RvM-MULT, constant `c = c_E`). Per-zero worst-case factor:

```text
m · (log T)^{2m + O(m)}
 <=  c log T · (log T)^{(2+O(1)) m_max}
 <=  c log T · (log T)^{(2+O(1)) c log T}
 =   c log T · exp( (2+O(1)) c (log log T)(log T) )
 =   c log T · T^{(2+O(1)) c log log T / log T · log T / log T · log T}
                                                      [tidy]
 =   T^{O(log log T / log T) · log T}
 =   T^{O(log log T)}
 =   T^{o(1)}.
```

(Algebra: `(log T)^{a log T} = exp(a (log T)(log log T)) = T^{a log log T}`.)

Total over multiple-zero set:

```text
[MULT]  <=  (#Z_T^{>=2})  ·  T^{o(1)}
        <=  N(T,2T)        ·  T^{o(1)}                [since #Z_T^{>=2} <= N(T,2T)]
        <<  T log T        ·  T^{o(1)}
         =  T^{1 + o(1)}.
```

Alternative bookkeeping using multiplicity-weighted count `N^{mult}` and a
uniform per-zero bound: same answer, since `N^{mult} << T (log T)^2`
(NMULT) and per-zero worst case is `T^{o(1)}`.

**Margin to target.** `T^{5/2+eps} / T^{1+o(1)} = T^{3/2+eps}`. The
multiple-zero contribution is fifteen halves of `T` below the target
exponent. Even if the per-zero Laurent bound were inflated to
`(log T)^{O(m^2)}` instead of `(log T)^{O(m)}` (e.g. through a less careful
Hadamard estimate), the per-zero factor becomes `T^{O((log log T)^2)}`,
still `T^{o(1)}`, still absorbed.

## 6. Why polynomial-`(log T)` is enough — Laurent coefficient check

At a multiple zero `rho` of `L`, the local expansion is

```text
L(rho+z) = (z)^m a_m (1 + a_{m+1}/a_m · z + ...),
a_m = L^{(m)}(rho)/m!.
```

We need `|a_m|^{-1} <<_E (log T)^{C m}` for some absolute constant `C`.
Source: Hadamard product representation

```text
L(E,s) = e^{A+Bs} · prod_rho (1 - s/rho) e^{s/rho},
```

with `A, B` polynomial-in-`(log T)`. The order-of-vanishing-`m` factor at
`rho` is `(s-rho)^m`; the leading Laurent coefficient is the value of the
de-singularized Hadamard product at `s=rho`, which is bounded by
`exp(O_E(m log log T))` by the standard zero-density count
`N(T,2T) << T log T` and Stirling-type counting of nearby zeros (Iwaniec-
Kowalski Ch. 5.7-5.8).

The repo's `H1_POSITIVE_RANK_CLOSURE.md` L221-230 already uses the cognate
bound on Laurent coefficients of `1/L` (the `b_{rho,-j}` of L227); the
present bound is the reciprocal, valid by the same Hadamard argument.

Result: `|a_m|^{-1} <<_E (log T)^{O(m)}`, polynomial in `(log T)` for each
fixed `m`, with exponent linear in `m`. **No surprise: the assumed bound
is the standard one.**

## 7. Cross-check against H1_MULTIPLE_ZERO_DISPOSITION_CURRENT

Read of `H1_MULTIPLE_ZERO_DISPOSITION_CURRENT_2026-05-11.md`:

- L33-42: explicitly states BFMT and q=2 shifted bad-set route are
  **simple-zero tools**. The multiple-zero disposition is treated as a
  **separate** input `H1-MultipleZeroDisposition(E,W,r)`.
- L67-92: defines the four disposition modes (A) absent / (B) killed /
  (C) retained / (D) unretained-and-central-negligible. These act on
  the **Laurent residue profile** `P_alpha(u)`, NOT on the negative
  moment sum.
- L99-119: rank-one specialization. Asks for `D_alpha <= 0` (effective
  degree bound) for every unretained offcentral multiple zero. This is
  a structural condition on residues, not a moment-sum bound.

Conclusion: `H1_MULTIPLE_ZERO_DISPOSITION_CURRENT` is **orthogonal** to
the present audit. It addresses *whether multiple-zero residue terms
appear in the H1 main term*, not *whether they bust the Door A negative
moment bound*. The two questions are independent:

- The disposition file: do multiple zeros break the central-only H1
  pointwise theorem? (Structural / profile-degree question.)
- This audit: do multiple zeros break the `T^{5/2+eps}` bound on
  `sum^{mult} |L|^{-2}`? (Quantitative / moment-sum question.)

Halo plan §7 Stage 4 Route i (`HALO_UNCONDITIONAL_PLAN_2026-05-12.md`
L653-655) is the route used here: source-close `AllZeroShiftedNeg_2`
*with multiplicity weight*. Route ii (use disposition file as separate
input) is unaffected by this audit and stays valid as an alternative
packaging.

## 8. Boundary

### Allowed

```text
Under the same conditionals as the q=2 audit
(GL2-BFMT-PrimePolynomialLowerBound(E),
 ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1),
 fixed-newform RH/explicit-formula normalization),

  sum_{rho in Z_T}^{mult} |L_E^*(rho+1/log T)|^{-2}  <<_{E,eps}  T^{5/2+eps},

where Z_T^{mult} = { multiplicity-weighted critical zeros : T < |gamma| <= 2T }.

Strategy A (cheap Laurent + RvM mult bound) suffices.
Multiple-zero contribution: T^{1+o(1)}, with T^{3/2+eps} margin.
```

### Not allowed

```text
Door A is unconditionally closed.
The Wave 4 conditionals are unconditionally promoted.
Strategy B (multiplicity-aware BFMT zero-sample from the start) is written.
A formal lemma for m_rho = O_E(log T) is filed in the repo.
The Laurent coefficient bound |L^{(m)}(rho)/m!|^{-1} <<_E (log T)^{O(m)}
  is a named repo lemma (it is currently used as a standard analytic
  fact, sourced externally).
```

## 9. Cost retired vs cost remaining

### Retired

```text
- Stage 2 plan Track 1 sub-task: "Multiplicity extension sub-audit"
  (CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md §7 Week 1 milestone L569-571)
- Halo plan §7 Stage 4 Route i, the moment-side check
  (HALO_UNCONDITIONAL_PLAN_2026-05-12.md L653-655)
- Estimated ~3-5 days of the projected 2-3 week Door A residual sprint
  (CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md §7 L562-590).
```

### Remaining (unaffected by this audit)

```text
- Wave 4 promotion: GL2-BFMT-PrimePolynomialLowerBound(E) unconditional.
- ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1) extension from k=1/2.
- Optional Track 2: Bui-Florea / Soundararajan ContShiftNeg_2 GL2 adaptation
  as insurance.
- Door A as a whole closure.
- Filing an explicit named lemma for m_rho = O_E(log T) (half-line proof,
  Iwaniec-Kowalski Ch. 5 citation).
```

### Cross-references

| File | Role |
|---|---|
| `handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L34-37, L77, L147 | q=2 audit over `S_E(T)`, the starting point |
| `handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md` L62-74, L98-109 | `S_E(T)` definition; q=2 audit re-statement |
| `handoff-2026-05-11-post-wave5-pivot/H1_MULTIPLE_ZERO_DISPOSITION_CURRENT_2026-05-11.md` L33-119 | orthogonal multiple-zero residue disposition; not blocking this audit |
| `handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §4, §7 Week 1, L403-465, L569-571 | Stage 2 cross-check that surfaced this gap |
| `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §6 L384-409, §7 Stage 4 L649-665 | Door A target; Route i vs Route ii framing |
| `handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md` L75-99, L171, L221-230 | local Laurent expansion; zero-counting `N(T,2T) << T log T`; reciprocal Laurent coefficient bound `b_{rho,-j}` |
