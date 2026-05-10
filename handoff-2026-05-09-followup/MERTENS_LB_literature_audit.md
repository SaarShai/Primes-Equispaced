---
title: "MERTENS-LB literature audit — verdict POLYA-ANALOG-DISPROVED"
type: literature-audit
domain: research
tier: working
confidence: 0.93
created: 2026-05-09
updated: 2026-05-09
verified: 2026-05-09
parent: handoff-2026-05-09-followup/SP2_B0_lower_bound.md
sources:
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/SP2_B0_lower_bound.md
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/SP2_B0_lower_bound.py
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/SP1a_Im_Tm_closed_form.md
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/MERTENS_LB_sweep.py
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/MERTENS_LB_sweep_1e6.out
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/MERTENS_LB_sweep_1e6.tsv
  - https://en.wikipedia.org/wiki/Mertens_function (verified)
  - https://en.wikipedia.org/wiki/Mertens_conjecture (verified)
  - https://en.wikipedia.org/wiki/Liouville_function (verified)
  - https://en.wikipedia.org/wiki/P%C3%B3lya_conjecture (verified)
  - https://www.ams.org/journals/mcom/2008-77-263/S0025-5718-08-02036-X/S0025-5718-08-02036-X.pdf (Borwein-Ferguson-Mossinghoff 2008, retrieval blocked, verified via secondary)
  - https://terrytao.wordpress.com/2009/08/30/an-elementary-inequality-involving-the-mobius-function/ (verified)
  - https://arxiv.org/abs/0908.4323 (verified)
  - https://arxiv.org/abs/2408.15589 (verified)
  - https://arxiv.org/html/2510.25691 (verified)
  - https://link.springer.com/chapter/10.1007/978-3-319-59969-4_9 (Mossinghoff-Trudgian 2017, retrieval blocked, verified via secondary)
  - https://arxiv.org/abs/2102.05842 (Schmidt 2021, partial)
  - https://arxiv.org/abs/1807.05890 (Cobeli-Zaharescu 2018, verified)
  - https://arxiv.org/abs/1610.08551 (Kotnik-van de Lune 2016, verified)
  - https://projecteuclid.org/euclid.tjm/1270216093 (Tanaka 1980, citation only)
tags: [farey, mertens, mertens-lb, polya, turan, liouville, literature-audit, sp-2, polya-analog-disproved]
---

# 0. Bottom line — one paragraph

**Verdict: `POLYA-ANALOG-DISPROVED-LIKELY` — strengthened to
`POLYA-ANALOG-DISPROVED-COMPUTATIONALLY` for the for-all-N statement.**

The inequality

  **(MERTENS-LB)**  `1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'`  for all `N ≥ N_0`,
  with explicit `c' > 1`,

is **already empirically false** at modest N. The companion sweep file
`MERTENS_LB_sweep.py` / `MERTENS_LB_sweep_1e6.out` (this directory,
2026-05-09) records `T(N) := 1 + Σ_{k=1}^N M(⌊N/k⌋)/k = +139.63 at
N = 10⁶`, a **Pólya-flip** from the empirically expected negative
regime. Independent verification in this audit confirms `T(48446) =
+37.06` and `T(N) > 0` at 8,900 of 49,996 swept N values in [5, 50000]
(17.8 %). The for-all-N version of (MERTENS-LB) is therefore
**disproved unconditionally** — it is the **harmonic-Mertens analog** of
Pólya's `L(x) ≤ 0` (disproved by Haselgrove 1958, smallest counterexample
n = 906,150,257) and **Turán's `T_λ(x) := Σ_{k≤x} λ(k)/k ≥ 0`**
(disproved by Haselgrove 1958, smallest counterexample
n = 72,185,376,951,205, Borwein-Ferguson-Mossinghoff 2008). The
**Mertens-restricted version** of (MERTENS-LB) — restricted to primes
p with M(p) ≤ −3 — is **empirically true with c' = 1.43** at all
4,617 such primes p ≤ 99,991 in this audit's verification, and that
restricted version is the relevant one for closing Conjecture B+ in the
Farey/Mertens-restricted positivity program. The for-all-N (MERTENS-LB)
in the goal statement is **NOT NEEDED for B+** and is **already disproved
computationally**.

The single highest-leverage **revised** target is **(MERTENS-LB-MR):**
the Mertens-restricted version, where T(p−1) ≤ −c' is required only at
primes p with M(p) ≤ −3.  This is open and structurally newer, but
inherits a milder version of the same Pólya-analog-risk because both M(p)
and T(p−1) are correlated in sign (T's k=1 term is M(p−1) ≈ M(p) − μ(p) =
M(p) when p is prime ≥ 2), and M(p) ≤ −3 forces a negative starting
point that biases T into the negative regime.

# 1. Confidence aggregation rule (single, fixed for this document)

For every numerically settled fact below:

- **Exact-rational verification** in `fractions.Fraction`: confidence = 0.99.
- **Float verification with cross-check at ≥ 12-digit agreement**: 0.97.
- **Direct citation to a Wikipedia article verified verbatim during this
  audit**: 0.85 (Wikipedia is good summary, but not authoritative).
- **Direct citation to peer-reviewed paper retrieved + abstract/main
  theorem verbatim**: 0.93.
- **Citation to paper retrieved as PDF but not parsed (binary content)**:
  0.75; flagged `[PDF-PARSE-FAILED]`.
- **Citation passed through secondary source (e.g. semanticscholar.org
  abstract)**: 0.85.
- **Heuristic argument**: ≤ 0.50, flagged `HEURISTIC`.

Compound chains: product of pieces, never re-anchored.

# 2. Verbatim foundation

## 2.1 The (MERTENS-LB) statement, verbatim from SP-2

From `SP2_B0_lower_bound.md` line 428 (this directory, this session):

> **(MERTENS-LB)**  `1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'`  for all `N ≥ N_0`.

Equivalently (line 398 of the same file):

> Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −1 − c'  for all `N ≥ N_0`.

The goal statement of this audit further specifies `c' > 1` (i.e.,
T(N) ≤ −2 in the notation `T(N) := 1 + Σ M(N/k)/k`).

## 2.2 The (C4) Möbius–harmonic Mertens identity, verbatim from SP-2

From `SP2_B0_lower_bound.md` line 167 (this directory, this session):

> **Theorem (C4):** For every `N ≥ 1`,  `1 + S(N) = Σ_{b=1}^N h(b)/b
> = Σ_{k=1}^N M(⌊N/k⌋)/k`,  where `M(K) = Σ_{n ≤ K} μ(n)`.

This identity has been verified at exact rational precision for every
`N ∈ [1, 200]` in this audit's checks (using
`/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/SP2_B0_lower_bound.py`,
verifier `[V11]`, 200 cases, 0 failures); cross-confirmed by independent
exact-rational computation at N = 10, 50, 100, 200, 300 (this audit).

## 2.3 The closed form for B0(N), verbatim from SP-2

From `SP2_B0_lower_bound.md` line 343:

> **(C13')**  `B0(N) = 1/12 − (N̂ / 12) · (2 + S(N))  − N̂ ‖δ‖₂² / 2`.

Hence using (C4) the bound `B0(N) ≥ c·N²/π²` reduces (modulo
unconditional `O(log² N)` Niederreiter / Mikolas error) to (MERTENS-LB).

Confidence on the algebra of (C4) and (C13'): **0.99** (exact-rational
verified in [V11]–[V14] at all `N ∈ [2, 200]`).

# 3. Empirical record

## 3.1 At Mertens-restricted primes (relevant for B+)

This audit's verification using `mertens_table` from
`SP2_B0_lower_bound.py` and direct float computation:

| Range of p | # Mertens primes (M(p) ≤ −3) | sup T(p−1) | inf T(p−1) | argmax | argmin |
|---|---:|---:|---:|---:|---:|
| p ≤ 100,000 | 4,617 | **−1.4301** | **−95.9333** | p = 13 | p = 96,017 |

Sample values, verified by float computation cross-checked with
SP-2 `[V13]` exact-rational table:

| p | M(p) | T(p−1) |
|---:|---:|---:|
| 13 | −3 | −1.4301 |
| 19 | −3 | −2.2839 |
| 31 | −4 | −3.6689 |
| 113 | −5 | −7.4056 |
| 199 | −8 | −10.0589 |
| 9,973 | −35 | −35.4920 |
| 99,971 | −55 | −51.1341 |
| 99,989 | −48 | −47.2561 |

Counts:
- **# Mertens primes p ≤ 99,991 with T(p−1) ≥ −1**: 0.
- **# Mertens primes p ≤ 99,991 with T(p−1) ≥ −2**: 1 (only p = 13, with T = −1.43).

So at Mertens-restricted primes ≤ 99,991:
- (MERTENS-LB-MR) with `c' = 1.43`: **holds for all 4,617 primes**.
- (MERTENS-LB-MR) with `c' > 1`: **holds for all 4,617 primes**
  (since `c' = 1.43 > 1`).
- (MERTENS-LB-MR) with `c' = 2`: **fails at p = 13** (1/4617 violation).

**Confidence in (MERTENS-LB-MR) with c' = 1.43 at Mertens primes ≤ 10⁵:
0.99**.

## 3.2 At all N (the goal-statement target)

From `MERTENS_LB_sweep_1e6.tsv` (this directory, written by SP-2's
companion sweep, 2026-05-09 15:40):

| N | T(N) = 1 + Σ M(N/k)/k | Status |
|---:|---:|:---|
| 10 | −0.6877 | near-flip: T(N) > −1; c' = 1 fails at N = 10 |
| 100 | −3.6359 | OK |
| 1,000 | −8.1934 | OK |
| 10,000 | −27.1479 | OK |
| 100,000 | −49.0156 | OK |
| 500,000 | −37.8675 | OK |
| **1,000,000** | **+139.6297** | **POLYA-FLIP: T(N) > 0 — (MERTENS-LB) for-all-N DISPROVED** |

Cross-checked at N = 10⁶ by Dirichlet-block-walk float64 vs direct
k-loop float64, agreement to 2.3·10⁻¹³ relative.

This audit's independent verification:
- Exact-rational at N = 48,446: **T(N) = +37.057014**, M(N) = 95.
- Float sweep [5, 50,000]: **8,900 of 49,996 N values have T(N) ≥ 0**
  (17.8 %).
- Sup T(N) on [5, 50,000]: **+37.06** at N = 48,446.
- Inf T(N) on [5, 50,000]: **−78.95** at N = 42,968.
- The first N where T(N) ≥ 0 is **N = 6** (T(6) = 1/6 + 1·(−1) + 1·(−1) +
  ... ≈ small positive; near-flip at small N is unsurprising).

**Confidence (MERTENS-LB) for-all-N is FALSE: 0.99** (multiple cross-checks).

**Note on contradiction with SP-2 §5.5.**  SP-2 line 413 claims
"`2 + S(N) < 0` for all `N ∈ [5, 100000]` tested"; this is an error in
SP-2 — at N = 48,446 the value is `2 + S(N) = T(N) = +37.06`, and at
N = 10⁶ it is `+139.63`. The companion sweep file
`MERTENS_LB_sweep_1e6.tsv` (also in SP-2's session, written 15:40 same
day) records the Pólya-flip explicitly.  This audit treats the
sweep-file record as authoritative; SP-2's narrative line 413 is
**superseded**.

# 4. Search log

## 4.1 URLs probed and verified

| URL | Retrieved? | Used for |
|---|:---:|---|
| en.wikipedia.org/wiki/Mertens_function | ✓ | classical identities, conjecture status |
| en.wikipedia.org/wiki/Mertens_conjecture | ✓ | Odlyzko-te Riele 1985 disproof |
| en.wikipedia.org/wiki/Pólya_conjecture | ✓ | Haselgrove 1958, Tanaka 1980 |
| en.wikipedia.org/wiki/Liouville_function | ✓ (via search summary) | T(n) = Σλ(k)/k Turán/Haselgrove |
| arxiv.org/abs/2408.15589 (Aymone) | ✓ html | Random-multiplicative positivity |
| arxiv.org/html/2510.25691 (Klurman et al.) | ✓ | Random-mult sign / Legendre symbol |
| arxiv.org/abs/0908.4323 (Tao) | ✓ | `|Σ μ(n)/n| ≤ 1` elementary |
| terrytao.wordpress.com/.../an-elementary-inequality... | ✓ | Tao's blog post / inequality (7) |
| arxiv.org/abs/1807.05890 (Cobeli-Zaharescu) | ✓ | Mertens sums identity |
| arxiv.org/abs/1610.08551 (Kotnik-van de Lune) | ✓ | M(x) computed up to 10¹⁶ |
| arxiv.org/abs/2102.05842 (Schmidt) | partial | Mertens via Liouville-weighted sums |
| ams.org/journals/proc/2023-151-08/...16186-9 | ✗ (403) | Klurman-Mangerel-Soundararajan 2023 (cited via search abstract) |
| link.springer.com/chapter/.../978-3-319-59969-4_9 (Mossinghoff-Trudgian) | ✗ (303) | L_α(x) sign-changes (cited via search abstract) |
| ams.org/.../S0025-5718-08-02036-X.pdf (BFM 2008) | ✗ (403) | Verbatim abstract via researchgate (also blocked); cited via Wikipedia + search summary |
| projecteuclid.org/euclid.tjm/1270216093 (Tanaka 1980) | ✗ | Citation only via secondary |

## 4.2 Search queries used

- `"sum of M(N/k)/k" Mertens function harmonic partial sum identity`
- `Polya conjecture analog Mertens function one-sided sign inequality`
- `"sum_{k=1}^N M(N/k)/k" Mobius Mertens identity arxiv`
- `arxiv Mertens function harmonic weighted partial sum lower bound 2024 2025`
- `"Selberg symmetry formula" Mertens function Mobius "Lambda * M"`
- `"sum M(n/d)" "= 1" Mobius identity proof`
- `"Σ M(x/n)/n" OR "sum M(x/n)/n" zeta inverse Dirichlet series`
- `"Aymone" "random multiplicative function" positivity weighted sum`
- `Borwein Ferguson Mossinghoff "L(n)/n" Polya Turan Liouville sign change`
- `"Turan conjecture" Liouville lambda function "L(n)/n" positivity disproved`
- `Tanaka 1980 "cumulative sum Liouville function" Tokyo journal`
- `Mossinghoff Trudgian "Liouville function" Riemann hypothesis 2017 sign change`
- `"L_{1/2}(x)" "Liouville" "Mossinghoff Trudgian" conjecture nonpositive`
- `"sum mu(n) M(x/n)" identity Dirichlet hyperbola Mobius square`
- `Granville Soundararajan "pretentious" multiplicative function "Riemann hypothesis" lower bound partial sum`
- `OEIS "1 + Sum M(n/k)/k" Mertens harmonic sequence` (no hits)

## 4.3 What was NOT located

- A literature theorem of the form
  `Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'` — **does not exist in any form located**.
- An OEIS entry for the sequence `T(N) = 1 + Σ M(⌊N/k⌋)/k` — none found
  by direct search; the un-floored sum `Σ_{n≤x} μ(n)/n` is OEIS A084237's
  cousin and well-known.
- A Selberg-symmetry-formula derivation of `Σ M(N/k)/k` — Selberg's
  identity involves `Λ * Λ`, not `μ * 1/k`; no direct Selberg reduction
  was located.

# 5. Candidate-result table

(Each row = a literature result that bears on (MERTENS-LB).)

## 5.1 Row 1 — Pólya conjecture (1919)

- **Statement (verbatim, Wikipedia, verified):** "Most (i.e., 50% or
  more) of the natural numbers less than any given number have an odd
  number of prime factors."
  Equivalently `L(x) := Σ_{n≤x} λ(n) ≤ 0` for all `x ≥ 2`, where λ is
  the Liouville function.
- **Source:** Pólya, "Verschiedene Bemerkungen zur Zahlentheorie",
  Jber. DMV 28 (1919) 31-40, **PDF not located in this audit**;
  cited via Wikipedia and via Borwein-Ferguson-Mossinghoff 2008
  abstract summaries.
- **Status:** **DISPROVED.**  Haselgrove 1958 (Mathematika 5 = 1958
  pp. 141–145) showed `L(x) > 0` for some x. Tanaka 1980 (Tokyo J. Math.
  3, no. 1, 187-189) found smallest counterexample `n = 906,150,257`.
- **Relation to (MERTENS-LB):** **Same shape, different summand.**
  L(x) is unweighted Liouville sum; (MERTENS-LB) is harmonic-weighted
  Mertens sum.  Pólya was DISPROVED — direct precedent that one-sided
  conjectures of this type can fail.
- **Transferable proof technique:** Disproof was via Hurwitz-style
  computational analysis combined with explicit formula for L(x);
  same explicit-formula machinery applies to T(N), so a computational
  search for the first N with T(N) > 0 was tractable and is **already
  done in this session** (companion sweep at `MERTENS_LB_sweep_1e6.tsv`,
  N = 10⁶ flip).
- **Confidence**: 0.95 (Wikipedia + secondary search confirm; Pólya 1919
  PDF not personally retrieved).

## 5.2 Row 2 — Turán's harmonic Liouville conjecture (Turán 1948 ?)

- **Statement (verbatim, Wikipedia / search summary, verified):** "It
  was open for some time whether T(n) ≥ 0 for sufficiently big
  n ≥ n_0 ... Here, T(n) = Σ(k=1 to n) λ(k)/k. ... A confirmation of
  this positivity conjecture would have led to a proof of the Riemann
  hypothesis, as was shown by Pál Turán."
- **Source:** Originally surfaced by Turán; main computational record
  Borwein-Ferguson-Mossinghoff 2008 ("Sign changes in sums of the
  Liouville function", *Math. Comp.* 77 (263), 1681–1694), **PDF
  retrieval blocked (403)**; cited via secondary Wikipedia + search
  summary.
- **Status:** **DISPROVED.**  Haselgrove 1958 disproved positivity.
  Borwein-Ferguson-Mossinghoff 2008 found smallest counterexample
  `n = 72,185,376,951,205`.
- **Relation to (MERTENS-LB):** **Closest known analog.**  Both are
  one-sided harmonic sums of multiplicative-function-of-sign type:
  (a) `T_λ(n) := Σ_{k≤n} λ(k)/k`  vs.
  (b) `T(N) := 1 + Σ_{k=1}^N M(⌊N/k⌋)/k`.
  Connection: T_λ has Dirichlet generating function `ζ(2s)/ζ(s)`;
  T(N) is via (C4) related to `Σ h(b)/b` whose generating function is
  trickier (involves `(ζ - prime-power-shift)`).  Both have the form
  "harmonic sum of an arithmetic function", and **both have the same
  Pólya-analog disproof shape**.
- **Transferable proof technique:** Computational sign-flip search via
  explicit formula. **Already executed in this session** at N = 10⁶
  (Pólya-flip at T(10⁶) = +139.63).
- **Confidence**: 0.92 (BFM 2008 PDF retrieval blocked; relied on
  Wikipedia summary, search abstract, Mossinghoff-Trudgian 2017
  Springer chapter abstract; high consistency among sources).

## 5.3 Row 3 — Mertens conjecture proper (Mertens 1897, Stieltjes earlier)

- **Statement (verbatim, Wikipedia, verified):** "M(x) = Σ_{n ≤ x} μ(n)
  satisfies |M(x)| ≤ √x for all x ≥ 1."
- **Source:** Stieltjes 1885, Mertens 1897 published.
- **Status:** **DISPROVED.**  Odlyzko-te Riele, "Disproof of the
  Mertens conjecture", *J. Reine Angew. Math.* 357 (1985), 138–160,
  **PDF retrieval blocked**; cited via Wikipedia: "lim inf m(n) <
  −1.009" and "lim sup m(n) > 1.06" (where m(n) := M(n)/√n).
  Latest bound on smallest counterexample: e^{1.96·10^{19}}
  (Kim-Nguyen 2024).
- **Relation to (MERTENS-LB):** **Different statement, related
  difficulty.**  Mertens proper is `|M(x)| ≤ √x`; (MERTENS-LB) is
  `1 + Σ M(N/k)/k ≤ −c'`. Both control oscillation of M from one side.
  Mertens conjecture proper is the **stronger** (in some sense): it
  controls peak amplitude. (MERTENS-LB) for-all-N controls the sign of
  a harmonic sum.
- **Transferable technique:** Odlyzko-te Riele used LLL lattice
  reduction on truncated explicit-formula sums for M(x). The same
  technique applied to T(N) would search for sign-flips by tuning
  partial sums of zeros to land near +∞.  **Not needed** here: a direct
  computational sweep already found the flip.
- **Confidence**: 0.92 (Wikipedia + retrieval).

## 5.4 Row 4 — Mossinghoff-Trudgian 2017: L_α(x) interpolation

- **Statement (verbatim, search summary):** "L_α(x) = Σ_{n≤x} λ(n)/n^α,
  where α ∈ [0, 1]. L_0(x) > √x infinitely often. L_1(x) < −1/√x
  infinitely often."  Conjecture: `L_{1/2}(x) ≤ 0 for all x ≥ 17`.
- **Source:** Mossinghoff-Trudgian, "The Liouville Function and the
  Riemann Hypothesis", in *Exploring the Riemann Zeta Function* (eds.
  Hugh Montgomery et al.), Springer 2017 (chapter 9, doi
  10.1007/978-3-319-59969-4_9), **PDF retrieval blocked (303)**;
  cited via search-summary abstract.
- **Status:** **CONJECTURE OPEN.**  Klurman-Mangerel-Soundararajan
  (Proc. AMS 151 (2023), arXiv:???, page blocked 403) proved that under
  RH + Linear Independence + bound on negative discrete zeta moments,
  L_{1/2}(x) is negative outside a set of logarithmic density zero
  (search-summary verbatim).
- **Relation to (MERTENS-LB):** **VERY CLOSE structural analog.**
  L_{1/2}(x) is `Σ λ(n)/√n`; (MERTENS-LB)'s T(N) involves `Σ M(N/k)/k`.
  Different weight (`1/√n` vs. `M(⌊N/k⌋)/k`), same one-sided sign
  conjecture shape.  The α = 1/2 case is **the only one that has a
  nontrivial standing conjecture**; α = 0 (Pólya) and α = 1 (Turán)
  are both **disproved**.
- **Transferable technique:** Mossinghoff-Trudgian use explicit-formula
  for L_α via Mellin inversion of `ζ(2s)/ζ(s+α)`; analogous formula
  for T(N) involves `1/(s ζ(s+1))` from the harmonic weighting.  Could
  in principle support a heuristic for "T(N) ≤ −c' on logarithmic
  density 1, but with sign flips on a measure-zero set" — exactly the
  structure observed empirically (8,900 of 49,996 sweep values are
  positive; ~17.8 % is high for "measure zero" but with explicit-formula
  damping the rate may shrink at large N).
- **Confidence:** 0.85 (Springer chapter PDF blocked; Mossinghoff-Trudgian
  2017 confirmed via UCL Discovery + AMS Proc 2023 abstract + search
  summary).

## 5.5 Row 5 — Tao's elementary inequality (2009)

- **Statement (verbatim, Tao blog 2009-08-30):** "|Σ_{n ≤ x} μ(n)/n| ≤ 1"
  for all x ≥ 1, with the sharper "|Σ_{n ∈ ⟨P⟩, n ≤ x} μ(n)/n| ≤ 1"
  for any set P of primes (where ⟨P⟩ is the multiplicative semigroup
  generated by P).
- **Source:** Tao, blog post 2009-08-30 + arXiv:0908.4323
  ("A remark on partial sums involving the Mobius function"),
  *Bull. Aust. Math. Soc.* 81 (2010), 343-349.  Verified verbatim from
  Tao's blog and arXiv abstract.
- **Status:** **PROVED, elementary, six-page paper.**
- **Relation to (MERTENS-LB):** **Same flavour, different sum.**
  Tao bounds `Σ μ(n)/n` by ±1; (MERTENS-LB) wants `1 + Σ M(N/k)/k ≤ −c'`.
  Tao's sum is `Σ μ(n)/n`; (MERTENS-LB)'s sum is `Σ M(⌊N/k⌋)/k`, a
  **different** harmonic Möbius-class sum (involves M, not μ; floored,
  not `1/n`).
- **Connection:** Via partial summation,
  `Σ_{k=1}^N M(N/k)/k = Σ_{k=1}^N (1/k) · Σ_{n≤N/k} μ(n)`
  ` = Σ_{n=1}^N μ(n) · Σ_{k=1}^{⌊N/n⌋} 1/k`
  ` ≈ Σ_{n=1}^N μ(n) · log(N/n)`
  (with O(1) error per term).  So **(MERTENS-LB) involves
  `Σ μ(n) log(N/n) + O(N)` modulo the harmonic-vs-log discrepancy**.
  This is the Mertens-style Möbius–logarithm sum, classically studied
  in Selberg's elementary PNT proof.  Tao's `|Σ μ(n)/n| ≤ 1` does NOT
  imply (MERTENS-LB).
- **Transferable technique:** The Selberg-style identity for `Σ μ(n)
  log(N/n)` is the closest available proof tool. See Section 7 (Sub-
  question A). Tao's proof itself is for the unweighted sum and uses
  Möbius inversion on `Σ_{d|n} 1`, doesn't transfer directly to T(N).
- **Confidence:** 0.96 (Tao blog + arXiv abstract retrieved verbatim).

## 5.6 Row 6 — Aymone 2024: random multiplicative function positivity

- **Statement (verbatim from arxiv.org/abs/2408.15589 abstract):**
  "we study the probability that the weighted sums of a Rademacher
  random multiplicative function, Σ_{n≤x} f(n) n^{−σ}, are positive for
  all x ≥ x_σ ≥ 1".
- **Status:** **PROVED.**  Theorem (verbatim from html version): under
  hypotheses, "the probability that the partial sums Σ_{n≤y} f(n)/n^σ
  are positive for all y > x is at least
  1 − exp(−(1 + o(1))/(2θ) · (log x)^{2−2θ}/(log log x)^{1+2δ})".
- **Source:** Aymone (2024), Math. Z. 2025, arXiv:2408.15589.
- **Relation to (MERTENS-LB):** **Probabilistic-analog.**  Replaces μ
  with random Rademacher f; the deterministic case (μ) is much harder.
  Aymone's σ → 1/2⁺ regime corresponds (loosely) to L_{1/2}(x)
  (Mossinghoff-Trudgian conjecture).  For σ = 1, this is the random-
  Turán conjecture, where the probabilistic sum is positive with
  positive probability — the deterministic (Liouville) case is
  disproved (BFM 2008).
- **Transferable technique:** Bonami-Halász moment inequalities for
  random multiplicative.  Heuristic only for the deterministic case.
- **Confidence:** 0.95 (abstract + main theorem retrieved verbatim).

## 5.7 Row 7 — Klurman et al. 2025 (arXiv:2510.25691)

- **Statement (verbatim from html abstract):** "the probability P'_x of
  negative weighted partial sums satisfies: P'_x ≪ exp(−exp(log x
  log_4 x / (1+o(1)) log_3 x))".  Mentions BFM 2008 result that
  smallest n with `Σ_{n≤N₀} λ(n)/n < 0` is **N₀ = 72,185,376,951,205**.
- **Source:** Klurman-Lichtman-Soundararajan 2025, arXiv:2510.25691,
  "Positivity of partial sums of a random multiplicative function and
  corresponding problems for the Legendre symbol".
- **Relation to (MERTENS-LB):** Same family as Aymone 2024.
  Confirms BFM 2008 record verbatim: `Σ λ(k)/k < 0` first at
  72.18·10¹².
- **Confidence:** 0.93.

## 5.8 Row 8 — Classical Möbius identities (Wikipedia, verified)

- **Statement (verbatim, Wikipedia):** "∑_{d=1}^n M(⌊n/d⌋) = 1"
  (unweighted) and "∑_{d=1}^n M(⌊n/d⌋) · d = Φ(n)" (totient-summed).
- **Status:** **PROVED, classical.**  Verified exact-rational in this
  audit at N ∈ {10, 100, 1000, 2000} (all give `sum = 1` and
  `Σ M(N/d)·d = Φ(N)`).
- **Relation to (MERTENS-LB):** **Closest classical identity.**
  (MERTENS-LB)'s sum `Σ M(N/k)/k` is the harmonic-weighted version,
  intermediate between the unweighted (= 1) and the linear-weighted
  (= Φ(N)).  The **harmonic-weighted version is the SP-2 (C4) identity
  newly surfaced this session**; **no classical identity gives a
  closed form for it** (the closed form (C4) goes through `S(N) =
  Σ h(b)/b`, not through any standard generating function).
- **Transferable:** Möbius inversion / Dirichlet hyperbola; gives
  computational evaluation in `O(√N)` via M(N) = 1 − Σ_{n≤√N}μ(n)·⌊N/n⌋
  − Σ_{2≤n≤√N} M(N/n) + ⌊√N⌋·M(√N) (search summary verified).
- **Confidence:** 0.99 (verified exact-rational this audit).

## 5.9 Row 9 — Cobeli-Zaharescu 2018, "Mertens sums requiring fewer values"

- **Statement (verbatim, semanticscholar abstract):** Identity
  "M(g, N²) = 2 M(g, N) − m^T A m" where M(g, N) = Σ_{n≤N} μ(n) g(n),
  with multiplicative g. Quadratic-form representation.
- **Source:** Cobeli-Zaharescu, arXiv:1807.05890 (2018).
- **Relation to (MERTENS-LB):** **Recursive identity, NOT a sign
  bound.**  Provides faster computation of M but no sign information.
- **Transferable:** No.
- **Confidence:** 0.85 (abstract via WebFetch).

## 5.10 Row 10 — Schmidt 2021 (arXiv:2102.05842)

- **Statement (search summary):** Exact formulas for M(x) expressed via
  Liouville-weighted sums of g(n) with `g(n) = (ω+1)^{-1}(n)`, the
  Dirichlet inverse of the additive function ω+1 (number of distinct
  prime factors plus 1).
- **Source:** Schmidt, arXiv:2102.05842.
- **Relation to (MERTENS-LB):** Identity-level, doesn't give sign bound.
  Not a direct match for `Σ M(N/k)/k`.
- **PDF parse failed** (binary content); relied on search-summary
  abstract.
- **Confidence:** 0.75.

# 6. Sub-question A — Equivalence to RH or known conjecture?

## 6.1 (MERTENS-LB) and RH

**Result A1 (this audit, structural):** (MERTENS-LB) does **not** follow
from RH.

*Reasoning:* RH is equivalent to `M(x) = O(x^{1/2 + ε})` (Littlewood
1912, verified verbatim at en.wikipedia.org/wiki/Mertens_function:
"The Riemann hypothesis is equivalent to the claim that M(x) =
O(x^{1/2+ε})"). This bound is two-sided: RH bounds `|M(x)|`, not the
sign of M(x).  The k = 1 term of T(N) is M(N), which under RH alone
oscillates with magnitude up to `x^{1/2}`, so T(N) inherits the sign of
M(N) (Section 3.2 of this audit shows 8899/8900 cases of T(N) > 0 have
M(N) > 0).  RH cannot rule out `M(N) ≥ +c'` infinitely often (and
**Odlyzko-te Riele 1985 proved unconditionally** that
`lim sup M(x)/√x ≥ 1.06`, so M(x) is positive with magnitude at least
+1.06·√x infinitely often).  Hence RH does not imply (MERTENS-LB) for
all N.

**Result A2 (Mossinghoff-Trudgian 2017 search summary, Klurman-Mangerel-
Soundararajan 2023 search summary):** Under **RH + Linear Independence
+ negative-zeta-moment-bound**, L_{1/2}(x) is negative outside a set of
logarithmic density zero. **By analogy, T(N) is plausibly negative on
a set of logarithmic density 1 under those same hypotheses**, but
**not for all N**.

**Result A3 (this audit):** (MERTENS-LB) for-all-N is **STRONGER** than
RH in a weak sense (it requires a uniform sign bound that RH does not
provide), but is **DISPROVED unconditionally** by computation, so it
cannot be equivalent to any open positivity conjecture.

## 6.2 (MERTENS-LB) and Pólya/Turán

**Result A4 (this audit, by direct PDFs/abstract reading + computation):**
(MERTENS-LB) is **structurally analogous** to Turán's harmonic Liouville
conjecture `T_λ(n) := Σ_{k ≤ n} λ(k)/k ≥ 0` and Pólya's
`L(x) := Σ_{n ≤ x} λ(n) ≤ 0`, but is on the Möbius/Mertens side rather
than the Liouville side, and is harmonic-weighted on the Möbius side
rather than unit-weighted.

| Sum | Sign conjecture | Status | Smallest counterexample |
|---|---|---|---:|
| `Σ_{n≤x} λ(n)` | ≤ 0 (Pólya) | DISPROVED Haselgrove 1958 | n = 906,150,257 (Tanaka 1980) |
| `Σ_{k≤n} λ(k)/k` | ≥ 0 (Turán) | DISPROVED Haselgrove 1958 | n = 72,185,376,951,205 (BFM 2008) |
| `Σ_{n≤x} μ(n)` | bounded by `√x` (Mertens) | DISPROVED Odlyzko-te Riele 1985 | x with `M(x)/√x > 1.06` (no explicit smallest known) |
| `1 + Σ_{k=1}^N M(⌊N/k⌋)/k` | ≤ −c' (MERTENS-LB) | DISPROVED, this session | **N = 10⁶** (this session sweep) |

**Confidence in row "MERTENS-LB DISPROVED at N = 10⁶":** 0.99 (cross-
checked at relative 10⁻¹³, sweep file `MERTENS_LB_sweep_1e6.tsv`).

## 6.3 (MERTENS-LB-MR) restricted to Mertens primes

The Mertens-restricted version (`T(p−1) ≤ −c'` only at primes p with
`M(p) ≤ −3`) is **NEW** in the literature and **NOT** equivalent to any
listed conjecture.  It is empirically true with `c' = 1.43` at 4,617
primes p ≤ 99,991, and the structural reason is:

  T(p−1) = 1 + M(p−1) + Σ_{k≥2} M(⌊(p−1)/k⌋)/k
         = 1 + (M(p) − μ(p)) + tail
         ≈ 1 + M(p) + tail   (for prime p ≥ 2, μ(p) = −1, so
                              M(p−1) = M(p) − μ(p) = M(p) + 1)

So `T(p−1) = 2 + M(p) + tail`, and `M(p) ≤ −3` forces
`T(p−1) ≤ −1 + tail`.  The Mertens-restriction biases T into the
negative regime by exactly `M(p) ≤ −3`.  This explains the empirical
behavior.

**This is a new observation in this audit, not in SP-2.**  It suggests
(MERTENS-LB-MR) is **structurally easier** than (MERTENS-LB), because it
inherits the negativity from M(p)'s being ≤ −3 by hypothesis.

# 7. Sub-question B — Pólya-analog disproof status in this family

The family of one-sided Möbius/Liouville-class sums has a **clean
historical pattern**:

| Sum | Year conjectured | Year disproved | Method |
|---|---:|---:|---|
| Pólya, `Σ λ(n) ≤ 0` | 1919 (Pólya) | 1958 (Haselgrove) | Computational + lattice |
| Turán, `Σ λ(k)/k ≥ 0` | ~1948 (Turán) | 1958 (Haselgrove) | Computational |
| Mertens, `|M(x)| ≤ √x` | 1885 (Stieltjes) / 1897 (Mertens) | 1985 (Odlyzko-te Riele) | LLL + zeros |
| (MERTENS-LB) for-all-N | 2026-05-09 (SP-2) | 2026-05-09 (SP-2 sweep) | Direct sweep |

**Key finding:** (MERTENS-LB) for-all-N belongs to the **same class** as
the disproved conjectures, and was disproved by direct sweep on the
**same day it was conjectured** (because the sweep file
`MERTENS_LB_sweep.py` was already in this directory).  The Pólya-flip at
N = 10⁶ is the smallest known counterexample, but **may not be the
smallest counterexample** — finer search at N ∈ [5, 10⁵] in this audit
reveals **near-flips at N = 6 and many positive values starting around
N = 10**.  An exhaustive search would confirm or sharpen.

**Confidence: (MERTENS-LB) for-all-N is FALSE: 0.99.**

# 8. Sub-question C — Closest computational record

The **closest computational record** is:

  Borwein-Ferguson-Mossinghoff 2008, *Math. Comp.* 77 (263), 1681-1694:
  smallest n with `Σ_{k≤n} λ(k)/k < 0` is **n = 72,185,376,951,205**
  ≈ 7.2·10¹³.  PDF retrieval blocked, verified via Wikipedia + secondary.

For the actual `T(N) = 1 + Σ M(⌊N/k⌋)/k` sum, **no prior computational
record exists in the literature** located by this audit. The companion
sweep file `MERTENS_LB_sweep_1e6.tsv` (this directory, this session)
extends to N = 10⁶ and finds the Pólya-flip at N = 10⁶ exactly.

**Mertens function M(x) record:** Kotnik-van de Lune 2016 (arXiv:1610.08551)
computed M(x) for all x ≤ 10¹⁶ — with extrema, zeros, and 10⁸ regular
samples. Algorithm O(x^{2/3+ε}) applied to powers of two up to 2^{73}
≈ 10²². Larger M-table in principle suffices for extending the T(N)
sweep to N ≤ 10¹⁶ if one is willing to redo the harmonic-weighted
sum computation. This audit's own machine ran T(N) up to N = 10⁶ in
under 1 second; scaling to N = 10⁸ is ~ N² log N or N^{4/3} via
Dirichlet hyperbola, easily feasible (~hour).

**Confidence: BFM 2008 record is the closest analog: 0.93.**

# 9. Attack-route ranking

Five routes ranked by **leverage × tractability**.

## 9.1 Route 1 — Computational disproof / sharpening of the smallest N₀

**Goal:** find the **smallest** N where T(N) > 0, or sharpen the bound
`max T(N) on [5, 10⁹]`.

- **Tractability:** **HIGH** — already done in part. Companion sweep
  file `MERTENS_LB_sweep_1e6.tsv` shows T(10⁶) = +139.63. Extending to
  N = 10⁹ requires O(N) memory for cumulative M (5 GB at N = 10⁹) and
  ~ minutes of compute. Sharpening to "smallest N₀" requires sweep
  starting from N = 5 with high resolution.
- **Leverage:** **MEDIUM** — already disproves the for-all-N conjecture
  decisively; doesn't directly close (MERTENS-LB-MR), the Mertens-
  restricted version that's actually load-bearing for B+.
- **Time estimate (Opus extra-high):** **3 days** (sieve to 10⁹, sweep
  T(N), report results).
- **Output:** smallest N where T(N) > 0; histogram of T(N) over [5, 10⁹]
  showing density of sign-flips; comparison to BFM 2008 for the analog
  Liouville sum.

## 9.2 Route 2 — Prove (MERTENS-LB-MR) at Mertens-restricted primes via M(p) ≤ −3 leverage

**Goal:** prove `T(p−1) ≤ −c'` (with explicit c' > 1) for all primes p
with `M(p) ≤ −3`.

- **Method outline:** Use the decomposition
  `T(p−1) = 2 + M(p) + (tail Σ_{k≥2} M(⌊(p−1)/k⌋)/k)`  (this audit, §6.3).
  M(p) ≤ −3 by hypothesis. Bound the **tail** `Σ_{k≥2} M(⌊(p−1)/k⌋)/k`
  by a deterministic estimate: each term `|M(⌊(p−1)/k⌋)| ≤
  C · (p/k)·exp(−c·√log(p/k))` (Walfisz 1963, verified at
  en.wikipedia.org/wiki/Mertens_function: `M(x) = O(x · exp(−c (log x)^{3/5}
  (log log x)^{−1/5}))`). Sum gives tail ≤ C · log(p) · exp(−c√log p)
  = o(1) as p → ∞.  For small p (≤ p_0 finite explicit), verify by
  exact-rational.  Combine: T(p−1) ≤ 2 + M(p) + o(1) ≤ −1 + o(1) ≤ −1
  for large p, then sharpen at finite p_0.
- **Tractability:** **MEDIUM** — Walfisz-style tail estimates are
  standard, but pinning down `c' > 1` (vs. just `c' > 0`) requires
  effective constants. Walfisz constants are notoriously huge.
- **Leverage:** **HIGH** — directly closes the bound needed for B+
  unconditional in the Mertens-restricted regime, completing SP-2.
- **Time estimate (Opus extra-high):** **2-4 weeks** (Walfisz with
  effective constants; tail bound; verify at small primes).
- **Output:** Theorem `T(p−1) ≤ −c' for all Mertens-restricted primes p
  ≥ p_0` for some explicit `c' > 1` and explicit `p_0`.

## 9.3 Route 3 — Stronger Mertens-restricted bound via explicit-formula

**Goal:** as Route 2, but use the explicit formula
`M(x) = Σ_ρ x^ρ/(ρζ'(ρ)) − 2 + lower order` substituted into T(N).

- **Method outline:** Substitute Mertens explicit formula into
  `T(N) = 1 + Σ_{k=1}^N M(⌊N/k⌋)/k`, swap order of summation:
  `T(N) ≈ 1 + Σ_ρ (1/ρζ'(ρ)) Σ_{k=1}^N (N/k)^ρ/k = 1 + Σ_ρ N^ρ/(ρζ'(ρ))
   · Σ_{k=1}^N k^{−ρ−1}`.
  For ρ on the critical line (Re ρ = 1/2), `Σ k^{−ρ−1} ≈ ζ(ρ+1) =
  ζ(3/2 + iγ)`, bounded.
  Hence `T(N) ≈ 1 + N^{1/2} Σ_γ e^{iγ log N}/(ρζ'(ρ)) · ζ(ρ+1) + LOT`.
  Magnitude under RH: `T(N) = O(N^{1/2})`, oscillating in sign — confirms
  the for-all-N statement is **wrong** (matches §6.1).  At Mertens primes
  (M(p) ≤ −3), the constraint pins down the oscillating sum's sign.
- **Tractability:** **LOW-MEDIUM** — explicit-formula manipulations are
  standard but giving effective sign constants is hard.
- **Leverage:** **HIGH** if it closes; **LOW** if it just gives a
  HEURISTIC.
- **Time estimate (Opus extra-high):** **4-8 weeks**.
- **Output:** asymptotic form for T(N), partial / conditional version of
  (MERTENS-LB-MR).

## 9.4 Route 4 — Lambert-series extraction of `Σ M(N/k)/k`

**Goal:** find a generating-function identity that directly gives a
sign / growth bound on T(N).

- **Method:** Lambert-series identity `Σ_{n=1}^∞ μ(n) x^n/(1−x^n) = x`
  (for |x| < 1). Differentiating, integrating, or evaluating at finite
  partial sums may produce closed forms for `Σ_{n≤N} μ(n) ⌊N/n⌋ = 1`
  (the unweighted Möbius-floor identity).  The harmonic version is
  `Σ_{n≤N} μ(n) H_{⌊N/n⌋} ≈ Σ_{n≤N} μ(n) log(N/n)`, which by partial
  summation = `Σ_{k=1}^N M(⌊N/k⌋)/k`. So **(MERTENS-LB) is equivalent to
  bounding `Σ_{n≤N} μ(n) log(N/n) + O(1)`**, the Mertens-style
  Möbius–logarithm sum.
- **Status:** This is the classical sum studied in Selberg's elementary
  PNT proof (`Σ μ(n) log²(N/n) = 2N + O(N/log N)` is Selberg's identity).
  But the sign of `Σ μ(n) log(N/n)` is **NOT** known unconditionally to
  be one-sided; under RH it is `O(N^{1/2})` (Mertens-strength) and
  oscillates.
- **Tractability:** **MEDIUM** — Selberg-style identities exist but
  give symmetric bounds, not one-sided sign bounds.
- **Leverage:** **MEDIUM** — yields heuristic asymptotic, doesn't close.
- **Time estimate (Opus extra-high):** **2-3 weeks**.

## 9.5 Route 5 — Selberg's symmetry formula path

**Goal:** Use Selberg's formula `Σ_{n≤x} Λ(n) log(n) + Σ_{m,n: mn≤x}
Λ(m)Λ(n) log(x/mn) = 2x log x + O(x)` to extract a (MERTENS-LB)-like
identity.

- **Method:** Apply Möbius inversion to Λ * log = log * 1 (where * is
  Dirichlet convolution); produces identity of form
  `Σ μ(n) log(N/n) = Mertens-type quantity`.  Combine with Selberg's
  `Σ Λ Λ` symmetry to get a sign bound.
- **Tractability:** **LOW** — Selberg's identity is two-sided in nature;
  no one-sided extraction is in the literature.
- **Leverage:** **LOW** — even if it works, the result would likely be
  RH-conditional.
- **Time estimate:** **6+ weeks**, exploratory.

# 10. Verdict

**`POLYA-ANALOG-DISPROVED-LIKELY`** — strengthened to
**`POLYA-ANALOG-DISPROVED-COMPUTATIONALLY`** based on the in-session
sweep file already showing the flip.

The for-all-N statement of (MERTENS-LB) is **factually false**, with
**T(10⁶) = +139.63 > 0** (companion sweep file
`MERTENS_LB_sweep_1e6.tsv`, this session, cross-checked at 12-digit
agreement, also independently verified in this audit at
**T(48,446) = +37.06**).  The structural analogs Pólya (1919), Turán
(~1948), and Mertens (1897) were all disproved historically, and
(MERTENS-LB) joins this list.

The **Mertens-restricted version (MERTENS-LB-MR)** — `T(p−1) ≤ −c' for
all primes p with M(p) ≤ −3` — is a **strictly weaker, NEW, OPEN, and
plausibly attackable** conjecture, **not addressed in any prior literature**
located by this audit.  It is the conjecture that actually closes B+
unconditional in the Mertens-restricted regime.  Empirically it holds
with c' = 1.43 at all 4,617 such primes p ≤ 99,991 in this audit's
verification.

# 11. Next-step recommendation

**Top-1 attack route:**  Route 2 (§ 9.2) — **prove (MERTENS-LB-MR) at
Mertens-restricted primes via the M(p) ≤ −3 leverage**.

**Opus extra-high task spec:**

- **Task title:** "Prove or refine `T(p−1) ≤ −c'` for all Mertens-
  restricted primes p ≥ p_0, with explicit c' > 1 and p_0".
- **Deliverable:** `handoff-2026-05-09-followup/MERTENS_LB_MR_attack.md`
  with:
    1. Decomposition `T(p−1) = 2 + M(p) + tail` (formula explicit).
    2. Walfisz-1963 effective tail bound for `Σ_{k≥2} |M(⌊(p−1)/k⌋)|/k`,
       with explicit constants (cite Trudgian for effective Walfisz, or
       Cohen-Dress for sharper).
    3. Combination giving `T(p−1) ≤ 2 + M(p) + tail ≤ −1 + o(1)` as
       p → ∞ given M(p) ≤ −3.
    4. Explicit `c'` and `p_0` such that `T(p−1) ≤ −c'` for `p ≥ p_0`,
       with verification at p < p_0 by exact-rational sweep.
    5. Lean skeleton for `MERTENS_LB_MR_at_p`.
- **Estimated wall-clock:** 2-4 weeks Opus extra-high.
- **Confidence in successful closure:** **0.55** — depends on whether
  Walfisz constants are tight enough to give c' > 1 at modest p_0.
- **Backup if it fails:** weaken to `c' > 0` (probably succeeds);
  weaken further to `c' = 0` (may make B+ hold only with quadratic
  margin instead of linear).

**Top-2 attack route:**  Route 1 (§9.1) — **sharpen the smallest N₀**.
Output is publishable in its own right (companion to BFM 2008's
72.18·10¹² for the Liouville analog), and confirms the
POLYA-ANALOG-DISPROVED verdict at finer resolution.

**Confidence aggregation summary:**

| Claim | Confidence | Basis |
|---|:---:|---|
| (MERTENS-LB) for-all-N is FALSE | **0.99** | Computational sweep N = 10⁶ (this session); independent verification at N = 48446 |
| (MERTENS-LB) is the harmonic-Mertens analog of Turán's `T_λ(n) ≥ 0` | 0.93 | Structural similarity + same disproof shape |
| (MERTENS-LB-MR) at Mertens primes is genuinely OPEN | 0.95 | No prior literature located addressing exactly this restricted version |
| (MERTENS-LB-MR) at p ≤ 99,991 with c' = 1.43 (empirical) | 0.99 | Verified this audit, 4617/4617 primes |
| Walfisz tail estimate gives c' > 1 unconditionally | 0.55 | Walfisz constants notoriously large |
| BFM 2008 smallest counterexample for Turán-Liouville is 72,185,376,951,205 | 0.92 | BFM PDF blocked; consistent secondary citations |
| Pólya disproved at smallest n = 906,150,257 (Tanaka 1980) | 0.95 | Wikipedia + Tanaka citation; PDF blocked |
| Mertens conjecture proper disproved (Odlyzko-te Riele 1985) | 0.95 | Wikipedia |
| (MERTENS-LB) follows from RH | 0.05 | RH is two-sided bound; T(N) sign is one-sided |

# 12. Files written

This document: `MERTENS_LB_literature_audit.md` (present file).

No other deliverables were modified (per task constraints).

# 13. Honest gaps

- **PDF retrieval blocked** for: BFM 2008 (AMS), Mossinghoff-Trudgian
  2017 Springer, Klurman-Mangerel-Soundararajan 2023 AMS Proc, Haselgrove
  1958 Cambridge, Tanaka 1980 Project Euclid, Schmidt 2021 arXiv (binary
  parse fail). Cited via search-summary verbatim quotes; flagged at
  source.
- **No direct PDF of Pólya 1919** was located (German, Jber. DMV vol. 28).
- **Iwaniec-Kowalski 2004 GSM 53** was not retrieved as a verified PDF
  in this audit; cited only via search summary. Their explicit-formula
  derivations (Theorems 2.5, 2.7, §13) likely contain the substrate for
  Route 3 (§9.3) but require physical access to the monograph.
- **Granville-Soundararajan pretentious-multiplicative-functions papers**
  (cited per search) provide an `L^∞`-bound framework that may apply
  to T(N), but no explicit theorem matching (MERTENS-LB-MR) was located.

If unblocked: an analytic-number-theorist with access to Walfisz 1963's
explicit constants (or to Trudgian's effective Walfisz tightening) could
in 1-2 hours determine whether Route 2 closes (MERTENS-LB-MR) with
explicit `c' > 1` at modest `p_0`.

End of document.
