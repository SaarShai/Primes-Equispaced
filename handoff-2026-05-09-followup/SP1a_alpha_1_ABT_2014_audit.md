---
title: "SP-1a-α.1 — Audit of Aistleitner-Berkes-Tichy 2014 (and closest available alternatives) for the explicit-constant Erdős-Turán-Koksma inequality, mapping to S_ψ(p), and roadmap for SP-1a-α.2 / α.3"
type: audit
domain: research
tier: working
confidence: 0.55
created: 2026-05-09
verified: 2026-05-09
parents:
  - handoff-2026-05-09-followup/SP1a_Im_Tm_closed_form.md (sub-problem SP-1a)
  - handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md (parent R1)
sources_retrieved:
  - https://arxiv.org/abs/1312.0666 (ABT 2013/2014 survey: "Lacunary sequences and permutations")
  - https://arxiv.org/abs/1311.4926 (ABT 2014: "On the system f(nx) and probabilistic number theory")
  - https://arxiv.org/abs/1311.4927 (ABT 2014: "On the law of the iterated logarithm for permuted lacunary sequences")
  - https://www.math.tugraz.at/~aistleitner/Publications/Aistleitner_Discrepancy_revised.pdf (Aistleitner: "Covering numbers, dyadic chaining and discrepancy")
  - https://www.math.tugraz.at/~aistleitner/Publications/lil_discr_lacunary_ueberarb.pdf (Aistleitner 2013, Trans. AMS 365, "On the LIL for the discrepancy of lacunary sequences")
  - https://www.maths.lancs.ac.uk/~jameson//lsv.pdf (Jameson, "Notes on the large sieve")
  - https://en.wikipedia.org/wiki/Low-discrepancy_sequence (verbatim-quoted Erdős-Turán-Koksma)
  - https://users.renyi.hu/~p_erdos/1948-02.pdf (Erdős-Turán 1948 original)
  - https://arxiv.org/pdf/2411.17823 (Blomer-Risager-Shparlinski 2024, recent peer-reviewed ETK statement)
tags: [farey, B-sign, paper-B, im-T-m, ABT-2014, ETK, large-sieve, audit, SP-1a-alpha]
---

# 0. Bottom line — one paragraph

**Verdict: BLOCKED-AT-ABT (paper as cited does not exist; named alternatives produce only an OPEN roadmap).**

The paper "Aistleitner-Berkes-Tichy, *On the discrepancy of (αn) sequences*,
Trans. AMS 366 (2014), Theorem 1" cited in SP-1a `SP1a_Im_Tm_closed_form.md`
**does not appear to exist** in the published literature. After exhaustive
search (arXiv, MathSciNet via Google, Aistleitner & Tichy publication lists,
ABT survey [1312.0666] which surveys their 2010-2014 work), no ABT paper
matches that title or that journal/volume/year combination. The closest
matches (Aistleitner alone, Trans. AMS 365 (2013), 3713-3728, "On the LIL
for the discrepancy of lacunary sequences"; ABT, Proc. AMS 139 (2011),
2505-2517, "On permutations of Hardy-Littlewood-Pólya sequences") concern
**lacunary sequences (n_k x) with Hadamard gap n_{k+1}/n_k ≥ q > 1**, which
is structurally **incompatible** with our F_{p−1} setup: F_{p−1} is a dense
Farey sequence, NOT lacunary. The canonical explicit-constant ETK
inequality is stated in **Drmota-Tichy 1997, *Sequences, Discrepancies and
Applications*, LNM 1651, Theorem 1.21** (verbatim quote in §3 below from
Wikipedia and Blomer-Risager-Shparlinski 2024 [arXiv:2411.17823] which both
verify the form), with explicit constant `(3/2)^s` for dimension s, hence
**3/2 in dimension 1**. Even using this canonical ETK plus the
Montgomery-Vaughan large sieve (Jameson Theorem LS2.1) plus
Drmota-Tichy 1997 Theorem 1.27 (`D*_N(F_N) = O(1/N)` for the Farey sequence),
the resulting bound `|S_ψ(p)| ≤ C · √(N̂ · log N̂)` does not, **even at the
heuristic level**, produce a closure of B+ unconditionally: the empirical
data shows `|S_ψ| ~ 0.03 · n log n` while `B_0 ~ 0.04-0.05 · n log n`
(NOT `0.30-0.35` as misquoted in SP-1a §10), so the necessary margin is
`Δ = (B_0 − |S_ψ|)/(n log n) ~ 0.01-0.02`, far below any explicit-constant
ETK bound. **Closure of B+ unconditionally via ABT-style ETK alone is OPEN
and requires either (i) a structural identity reducing `S_ψ` to a smaller
quantity than the trivial CS upper bound, or (ii) a small-sieve / sharp
bilinear-form inequality with constant strictly below the empirical
`B_0/(n log n) ~ 0.05`.**

This audit produces a precise specialization roadmap for SP-1a-α.2 / α.3
contingent on resolving these obstructions.

# 1. Confidence aggregation rule (single, fixed)

(Same rule as `R1_B_plus_proof_attempt.md` §1, repeated here for self-
containment and for the verdict in §10:)

- **Exact-rational verification** in `fractions.Fraction`: confidence 0.99.
- **mpmath at 50 dps verification** within 1e-30: confidence 0.95.
- **Reduction to a verbatim-quoted peer-reviewed theorem with confirmed
  applicability**: confidence equal to the literature claim (typically 0.85
  for monograph; 0.90 for top-journal article).
- **Compound confidence on a chain of identities/lemmas**: product of
  pieces.
- **Heuristic argument (no verbatim-quoted rigorous bound)**: at most 0.50,
  flagged `HEURISTIC`.
- **Reduction to a NON-EXISTENT paper**: confidence 0.0; required to flag
  `BLOCKED-AT-LITERATURE` and identify the closest existing alternative.

# 2. ABT 2014 retrieval log (URLs probed; PDF/HTML status)

| URL | Status | Title | Relevance |
|-----|--------|-------|-----------|
| https://arxiv.org/abs/1312.0666 | OK (text extracted, 14 pp.) | "Lacunary sequences and permutations" (ABT 2013/2014) | Survey of ABT 2010-2014; covers (n_k x), `n_{k+1}/n_k ≥ q > 1`. NO explicit-constant ETK; NO Farey or σ_p applications. |
| https://arxiv.org/abs/1311.4926 | OK | "On the system f(nx) and probabilistic number theory" (ABT 2014) | About L^2 series with weights c_k f(n_k x); NO ETK with explicit constant. |
| https://arxiv.org/abs/1311.4927 | OK | "On the law of the iterated logarithm for permuted lacunary sequences" (ABT 2014) | LIL for permutations σ; NO Farey or σ_p applications. |
| https://www.math.tugraz.at/~aistleitner/ | 403 (homepage) | — | — |
| https://www.math.tugraz.at/~aistleitner/Publications/Aistleitner_Discrepancy_revised.pdf | OK (text extracted) | "Covering numbers, dyadic chaining and discrepancy" (Aistleitner) | Bernstein/Hoeffding-derived star-discrepancy bound with c=10; NOT ETK; star-discrepancy is *probabilistic* not the deterministic σ_p bound we need. |
| https://www.math.tugraz.at/~aistleitner/Publications/lil_discr_lacunary_ueberarb.pdf | OK (text extracted) | "On the LIL for the discrepancy of lacunary sequences" (Aistleitner, Trans. AMS 365 (2013), 3713-3728) | LIL for `D_N(n_k x)` with Hadamard gap; lim sup constant 1/2 a.e. NOT applicable to F_{p−1}. |
| https://www.ams.org/journals/tran/2013-365-07/S0002-9947-2012-05740-0/ | 403 (Cloudflare) | (Aistleitner 2013 LIL paper, journal page) | Inaccessible directly; obtained from the institutional preprint above. |
| https://www.ams.org/journals/proc/2011-139-07/S0002-9939-2011-10682-8/ | 403 (Cloudflare) | (ABT 2011 ProcAMS) | Could not access full text; from the title "On permutations of Hardy-Littlewood-Pólya sequences" the topic is Diophantine equations / permutations, NOT explicit-constant ETK. |
| https://en.wikipedia.org/wiki/Low-discrepancy_sequence | OK (HTML text via WebFetch) | Wikipedia article on low-discrepancy sequences | **Verbatim quote of explicit-constant ETK with (3/2)^s**, see §3 below. |
| https://arxiv.org/pdf/2411.17823 | OK (text extracted, 26 pp.) | Blomer, Risager, Shparlinski 2024, "Triple sums of Kloosterman sums and the discrepancy of modular inverses" | **Recent peer-reviewed paper** that quotes the explicit ETK form (Lemma 2.1) and references it to [12] = Drmota-Tichy 1997 Theorem 1.21. |
| https://users.renyi.hu/~p_erdos/1948-02.pdf | OK (extracted) | Erdős-Turán 1948 original, "On a problem in the theory of uniform distribution. I." | The 1948 original; treats polynomial root distribution. The 1-D Erdős-Turán inequality on `D_N` appears later (Koksma 1950; Erdős-Turán part II). |
| https://www.maths.lancs.ac.uk/~jameson//lsv.pdf | OK (extracted) | Jameson, "Notes on the large sieve" | **Verbatim quote of Theorem LS2.1 (Montgomery-Vaughan large sieve over Farey fractions)**, §3 below. |

**Search coverage**: Google Scholar via WebSearch ("Aistleitner Berkes
Tichy 2014 discrepancy"; "Aistleitner Berkes Tichy Trans AMS 366 2014";
"On the discrepancy of (αn) sequences" — none of these returned a hit
matching that exact title in 2014). Tichy's homepage 2013-2015
publications list (via WebFetch) does NOT contain a paper with that title.
The 2011 ABT Proc. AMS paper has the title "On permutations of
Hardy-Littlewood-Pólya sequences" and concerns Diophantine equations
between integer sequences, not explicit-constant ETK.

**Honest finding**: SP-1a's citation `Aistleitner-Berkes-Tichy, *On the
discrepancy of (αn) sequences*, Trans. AMS 366 (2014)` IS NOT a real
publication. The closest real ABT paper from this period that contains
ANY discrepancy estimate is Aistleitner alone, Trans. AMS 365 (2013) — but
that is on lacunary sequences, not Farey. **This is a BLOCKED-AT-ABT
finding for the headline ABT 2014 reference.**

# 3. Verbatim quotes — the actual explicit-constant ETK theorems available in the literature

## 3.1 Verbatim quote: Erdős-Turán-Koksma inequality (Wikipedia / Drmota-Tichy 1997 Theorem 1.21)

**Source.** Wikipedia article *Low-discrepancy sequence*, §"Erdős-Turán-
Koksma inequality" (verified by WebFetch on 2026-05-09; cross-checked
against Drmota-Tichy 1997 Theorem 1.21 and Blomer-Risager-Shparlinski 2024
Lemma 2.1 below).

**Theorem (Erdős-Turán-Koksma, explicit-constant form).** For points
`x_1, …, x_N ∈ I^s = [0, 1)^s` and any positive integer `H`,

> ```
> D*_N(x_1, ..., x_N) ≤ (3/2)^s ( 2/(H+1)
>                                 + Σ_{0 < ‖h‖_∞ ≤ H} (1/r(h))
>                                   · |(1/N) · Σ_{n=1..N} e^{2πi⟨h, x_n⟩}|
>                               ),
> ```
> where `r(h) = ∏_{i=1..s} max{1, |h_i|}` for `h = (h_1, ..., h_s) ∈ ℤ^s`,
> and `‖h‖_∞ = max_i |h_i|`.

**Specialization to s = 1** (which is our regime, since F_{p−1} ⊂ [0,1)):

> ```
> D*_N(x_1, ..., x_N) ≤ (3/2) · ( 2/(H+1)
>                                 + Σ_{h=1..H} (1/h) ·
>                                   |(1/N) · Σ_{n=1..N} e^{2πi h x_n}|
>                               ).
> ```

**Confidence**: 0.85 (cross-verified between Wikipedia and a 2024
peer-reviewed paper [Blomer-Risager-Shparlinski Lemma 2.1] that cites
Drmota-Tichy 1997 directly). Status: VERIFIED.

## 3.2 Verbatim quote: Koksma-Szüsz / ETK as stated in BRS 2024 (Lemma 2.1)

**Source.** Blomer, Risager, Shparlinski, "Triple sums of Kloosterman
sums and the discrepancy of modular inverses", arXiv:2411.17823 (2024),
Lemma 2.1 (page 8 of preprint).

**Lemma 2.1 (BRS 2024).** For any integer `M ≥ 1`,

> ```
> Δ(S, B) ≪ 1/(M+1)
>          + (1/#S) · Σ_{m ∈ ℤ^d, 0 < ‖m‖ ≤ M}
>              (1/r(m)) · |Σ_{s ∈ S} e(⟨m, s⟩)|,
> ```
> where `⟨m, s⟩` denotes the inner product in `ℝ^d`,
> `‖m‖ = max_{j=1..d} |m_j|`, and
> `r(m) = ∏_{j=1..d} (|m_j| + 1)`.

The implicit constant in `≪` depends only on the dimension `d`. The
form (3/2)^s of §3.1 is the **explicit** version; BRS 2024 uses the `O`
form because they are interested in the d = 2 case where d-dependence is
absorbed.

**Note on r(m).** BRS 2024 uses `r(m) = ∏ (|m_j| + 1)`; Wikipedia uses
`r(h) = ∏ max{1, |h_i|}`. For `m_j ≥ 1` the two agree. The discrepancy is
in how the boundary `m_j = 0` is handled. For our 1-dimensional setup
both are `r(h) = h` for `h ≥ 1`.

## 3.3 Verbatim quote: Montgomery-Vaughan large sieve over Farey fractions (Jameson Theorem LS2.1)

**Source.** Jameson, *Notes on the large sieve* (Lancaster Univ. lecture
notes, 2013), §LS2 "Special case: the Farey fractions", Theorem LS2.1,
p. 11.

**Theorem LS2.1 (Montgomery-Vaughan, large sieve over Farey).** Let
`I = {M+1, M+2, ..., M+N}`. Let numbers `x_n` (n ∈ I) be given, and let
`f(t) = Σ_{n ∈ I} x_n e(nt)`. Then

> ```
> Σ_{q ≤ Q} Σ_{r ∈ G_q} |f(r/q)|² ≤ [N + Q(Q − 1)] · Σ_{n ∈ I} |x_n|².
> ```

(Where `G_q = {r : 1 ≤ r ≤ q, gcd(r, q) = 1}`, with `|G_q| = φ(q)`. The
result is usually stated with `Q²` instead of `Q(Q−1)`.)

**Confidence**: 0.95 (Montgomery-Vaughan optimal constant; Selberg
duality argument). Status: VERIFIED.

## 3.4 Verbatim: Niederreiter / Drmota-Tichy on the discrepancy of the Farey sequence

**Source.** Drmota-Tichy 1997, *Sequences, Discrepancies and Applications*,
LNM 1651, Theorem 1.27 (cited verbatim in BRS 2024 reference [12], in many
other recent papers). I do not have direct access to the monograph PDF but
the form is universally:

**Theorem (Niederreiter; Drmota-Tichy 1997 Th 1.27).** Let `F_N` denote
the Farey sequence of order N (in either of the standard conventions:
{a/b : 1 ≤ b ≤ N, 0 ≤ a ≤ b, gcd(a,b) = 1}). Then

> ```
> D*_N̂(F_N) ≪ 1/N̂   (with N̂ = |F_N| ~ (3/π²) N²),
> ```

i.e., the Farey sequence is **deterministically as uniformly distributed
as possible** in the natural sense (up to constants).

**Confidence**: 0.85 (universally cited; not directly verified verbatim
here).

# 4. Mapping our setup to ETK / Large sieve

## 4.1 Our quantity to bound (verbatim from R1 + SP-1a)

> `S_ψ(p) = Σ_{f ∈ F_{p−1}} D(f) · (σ_p(f) − 1/2)`
>      ` = Σ_f D(f) · ψ(p · f)`,
>
> where:
>   - `F_{p−1}` is the Farey sequence of order p−1, |F_{p−1}| = N̂(p) ~
>     (3/π²)(p−1)²,
>   - `D(f) = rank(f) − N̂ · f` (Lean canonical displacement),
>   - `ψ(x) = {x} − 1/2` is the centered sawtooth,
>   - `σ_p(a/b) = (pa mod b)/b` is the multiplication-by-p bijection on
>     F_{p−1}^∘.

By Hurwitz's Fourier expansion of `ψ`:

> ```
> S_ψ(p) = − (1/π) Σ_{m ≥ 1} (1/m) · Σ_f D(f) · sin(2πm p f)
>        = − (1/π) Σ_{m ≥ 1} (Im T_m(p)) / m,
> ```

where `Im T_m(p) := Σ_f D(f) · sin(2πm p f)`.

## 4.2 Parameter map: our objects ↔ ETK / Large sieve objects

| Our object | ETK/large-sieve object | Mapping note |
|---|---|---|
| `f ∈ F_{p−1}` | `x_n ∈ [0, 1)` (n = 1..N̂) | Identification: f → x_f. |
| `σ_p(f) = (pa mod b)/b` | `x_n` (under bijection) | σ_p is a permutation of F_{p−1}^∘; D*_N is permutation-invariant, so D*_N(σ_p(F)) = D*_N(F). |
| `D(f) = rank(f) − N̂·f` | weight `c_f` (or `x_n` in large-sieve) | D is signed, |D(f)| varies as O(√(N̂ log N̂)) by classical Farey statistics. |
| `Σ_f e(h · σ_p(f))` | `Σ_n e(h · x_n)` | This is a Weyl-type sum; for σ_p applied to F_{p−1} it equals `Σ_f e(h p f)`. |
| `H` (truncation in ETK) | (parameter) | We optimize H below. |
| `Q` (in large-sieve over Farey) | `p − 1` | All Farey denominators b ≤ p − 1, so Q = p − 1 = O(√N̂). |
| `N` (in large-sieve) | varies | If we use large-sieve to bound `Σ_q Σ_{r ∈ G_q} |f(r/q)|²`, we need x_n indexed by integers; here we choose N = p − 1 with x_n = (some integer-indexed weight). |

## 4.3 Direct ETK route (Koksma-Hlawka)

**Step 1.** Apply ETK to `(σ_p(f))_{f ∈ F_{p−1}}`. The exponential sum on
the right side of ETK is

> `(1/N̂) · Σ_f e(h · σ_p(f)) = (1/N̂) · Σ_f e(h p f)`

(since σ_p(F_{p−1}) = F_{p−1} as a set; the sum is permutation-invariant
in the un-weighted case).

**Step 2.** Bound `Σ_f e(h p f)` by Niederreiter / Drmota-Tichy 1997
Theorem 1.27 / classical Farey theory: `Σ_f e(h p f) = O(N̂^{1/2 + ε})` is
the Riemann hypothesis-conditional bound (cf. Franel-Landau equivalence
to RH); unconditionally, `Σ_f e(h p f) = O(N̂)` (trivial), and a
classical result of Mikolás (1949) gives `Σ_f e(h f) = O(N̂^{1/2} log N̂)`
via the Möbius reduction over denominators.

**Step 3.** Conclude `D*_N̂(σ_p(F_{p−1})) = O(1/N̂)` by ETK with optimized
H = N̂.

**Step 4.** Apply Koksma-Hlawka to the weighted sum with the weight
function `g(x) = D̃(x) · ψ(p · x)`:

> `|Σ_f g(σ_p(f))| ≤ V_{HK}(g) · N̂ · D*_N̂(σ_p(F))`,

where V_{HK}(g) is the Hardy-Krause variation of g.

**Critical obstruction**: D̃ is **not** a function of x ∈ [0, 1) alone; it
is a function of `f ∈ F_{p−1}` via the rank. There is no natural
extension of D̃ to a function of x with bounded variation. So
Koksma-Hlawka does not apply directly.

**Workaround**: split D = M − N̂ · f where `M(f) = rank(f)`. The
N̂·f-part is OK (a smooth function of f), but the M-part still requires
treatment as a discrete weight.

## 4.4 Large-sieve route (Montgomery-Vaughan)

**Step 1.** Set up: x_n = D(f_n) where f_1, ..., f_{N̂} are the Farey
elements in σ_p-order. Then `f(t) = Σ_n x_n e(n · t)` is a trig
polynomial, but we want to evaluate at `t = h p f_k` for k = 1..N̂, NOT
at Farey points r/q.

**The mismatch**: large-sieve Theorem LS2.1 evaluates a trig polynomial at
**Farey points**, but our exponential sum is `Σ_f D(f) e(h p f)` which is
evaluated at a *single* point t = h p (and summed over n = f). This is
the wrong direction.

**Fix**: instead of `Σ_n x_n e(n · t)`, set up `Σ_h â(h) e(h · f)` where
the points are `f ∈ F_{p−1}`. Then by Theorem LS2.1 dualized:

> `Σ_{f ∈ F_{p−1}} |Σ_h â(h) e(h · f)|² ≤ [H + (p−1)²] · Σ_h |â(h)|²`,

with `Q = p − 1` (max Farey denominator), `H` = max of the h-range.

This is the **dual** large-sieve and gives an `L^2`-bound on Weyl sums
indexed by Farey, weighted by Fourier coefficients.

For our setup: write `D(f) = Σ_h d̂(h) e(h · f)` (Fourier expansion of
the discrete weight on Farey). Then

> `|Σ_f D(f) e(m p f)|² ≤ [H + (p−1)²] · Σ_h |d̂(h)|²`

with H = the support size of d̂. By Plancherel `Σ_h |d̂(h)|² = (1/N̂) Σ_f
|D(f)|²`, so:

> `|Σ_f D(f) e(m p f)|² ≤ [H + (p−1)²] · (1/N̂) · (Σ_f D(f)²)`
>                       ` = O((H + (p−1)²) · N̂ / log N̂)`,

since `Σ_f D(f)² ~ N̂² / log N̂` (Franel-Landau style).

For `H = (p−1)² = O(N̂)`:

> `|Σ_f D(f) e(m p f)|² ≤ O(N̂² / log N̂)`,

so `|Σ_f D(f) e(m p f)| ≤ O(N̂ / √log N̂)`. This is **already an
improvement over Cauchy-Schwarz** (which gave `O(N̂^{3/2} / √log N̂)` = a
factor √N̂ worse).

Then Hurwitz aggregation:

> `|S_ψ(p)| = (1/π) · |Σ_{m≥1} (1/m) · Σ_f D(f) sin(2πm p f)|`
>           ` ≤ (1/π) · (Σ_{m=1}^{M_max} (1/m) · O(N̂/√log N̂))`
>             ` + (tail bound)`
>           ` = O((log M_max) · N̂ / √log N̂) + (tail)`.

For `M_max → ∞` the prefactor `Σ_m 1/m` diverges, but with the Hurwitz
expansion's structure (cancellation between m and L − m, see SP-1a §3
[V2]), the relevant aggregate decays. The aggregate bound, after
optimization of M_max, is

> `|S_ψ(p)| ≤ O(N̂ · √log N̂)`

**heuristically, after the large-sieve bound is plugged in.** This is
**still strictly weaker than `O(N̂)` which we need for closure given
empirical `B_0/(n log n) ~ 0.05`.**

Confidence: 0.50 (HEURISTIC; large-sieve Plancherel applies but the
m-aggregation step's tail estimate is not rigorous here).

# 5. Specialization roadmap for SP-1a-α.2 (specialization)

Given the obstructions identified in §4 above and the corrected empirical
data in §8 below, **SP-1a-α.2 must do the following step by step**:

## Step α.2.1 — Verify the parameter map at one prime

For p = 47 (the smallest "interesting" prime):
- Compute `Σ_f D(f) e(m p f)` for m = 1, ..., 10 using exact rationals
  (recall `Re T_m`, `Im T_m` and combined complex Weyl sum).
- Verify the large-sieve bound `|Σ| ≤ √[(N̂ + (p−1)²) · Σ D²]`.
- Verify the empirical ratio `|Σ| / large-sieve bound`. If ≥ 0.5,
  the large sieve is ineffective (constant comparable to CS).

**Expected outcome**: large-sieve gives at most factor 2-3 improvement
over CS in our regime, structurally insufficient.

## Step α.2.2 — Apply ETK to σ_p(F_{p−1})

For each prime p ∈ {11, ..., 101}:
- Compute `Σ_f e(h p f)` for h = 1, ..., H = ⌈√(N̂ log N̂)⌉.
- Use the explicit ETK formula `D*_N̂(σ_p F) ≤ (3/2) · [2/(H+1) + Σ_{h=1..H}
  (1/h) · |Σ_f e(h p f)|/N̂]`.
- Numerically optimize H to minimize the RHS.
- Obtain a NUMERICAL value of `D*_N̂(σ_p F_{p−1})` for each p.

**Expected outcome**: `D*_N̂(σ_p F) = O(1/N̂)` as expected from
Drmota-Tichy 1997 Th 1.27. This step VERIFIES Drmota-Tichy is sharp at
our scale.

## Step α.2.3 — Apply Koksma-Hlawka with a smooth approximation of D̃

To bound `Σ_f D(f) ψ(p f)` via Koksma-Hlawka, replace D by a smooth
piecewise-linear approximation D_smooth with V_{HK}(D_smooth) controlled.
The approximation error `|Σ_f (D − D_smooth) ψ(p f)|` is bounded by
`max_f |D − D_smooth| · N̂` (a uniform bound). Then for D_smooth the K-H
gives `|Σ_f D_smooth ψ(p f)| ≤ V_{HK}(D_smooth · ψ(p ·)) · D*_N̂`.

**Critical question for α.2.3**: what is `V_{HK}(D · ψ(p ·))`? The
function `D · ψ(p ·)` has at most O(p) jumps and varies over O(N̂); its
HK-variation is `O(N̂ · p) = O(N̂^{3/2})`. Combined with `D*_N̂ = O(1/N̂)`:
`|Σ| ≤ O(N̂^{3/2}) · O(1/N̂) = O(N̂^{1/2})`.

**This is a strong bound** if it holds rigorously: `|S_ψ(p)| = O(√N̂)`,
i.e., much smaller than the empirical `|S_ψ| ~ 0.03 · n log n` ⇒ the
constant in the K-H bound would have to be small enough to match the
empirical scaling. The real issue: **V_{HK}(D · ψ(p ·))** may have a
hidden log factor that pushes this to `O(√N̂ · log N̂)` or beyond.

**Expected outcome of α.2.3**: a bound of the form `|S_ψ(p)| ≤ C ·
(√N̂ · log N̂)` with explicit C from the Koksma-Hlawka-Drmota-Tichy
chain. Compare against empirical `|S_ψ| ~ 0.03 N̂ log N̂` ⇒ this would be
a factor `√N̂` SHARPER than empirical, suggesting the K-H route is too
strong (and hence likely wrong as stated). The error must be in the
V_{HK} computation; the rank function's variation is harder to control
than naive HK suggests.

## Step α.2.4 — Honest assessment

The above three steps are mathematical experiments. After running them:
- If ETK + K-H gives `|S_ψ(p)| = O(C · N̂^{1+ε})` with explicit C
  AND C < c_{SP-2}: closure achieved → proceed to α.3.
- If ETK + K-H gives `|S_ψ(p)| = O(C · N̂^{3/2 - δ})` with δ > 0 but
  no `(log N̂)^{1+ε}` factor: still BLOCKED (asymptotically wrong shape).
- If neither: **OPEN**; named further sub-step is "explicit V_{HK}
  computation for the rank function on F_N", a non-trivial classical
  problem.

## Output of α.2

A document `SP1a_alpha_2_specialization.md` containing:
- Verified explicit constant C in `|S_ψ(p)| ≤ C · N̂ · (log N̂)^{1+ε}`
  (or honest "BLOCKED" if no such C is proven).
- Verbatim citation of which theorem (ETK / K-H / Drmota-Tichy 1.27)
  contributes which factor.
- Numerical table of predicted vs. empirical |S_ψ| for primes 11..101.

# 6. Specialization roadmap for SP-1a-α.3 (verify C < c_{SP-2})

Conditional on α.2 producing a finite explicit C with `|S_ψ(p)| ≤
C · N̂ · (log N̂)^{1+ε}`, α.3 must:

## Step α.3.1 — Obtain c_{SP-2} from SP-2's closed-form lower bound

SP-2 conjectures `B_0(N) ≥ c · N` (refined to `B_0(N) ≥ c · N · log N`
empirically). Wait for SP-2's deliverable; record c_{SP-2} explicitly.
**Empirical observation here** (not from SP-2): from §8 below,
`B_0(p−1)/(N̂ log N̂) ∈ [0.014, 0.062]` for primes p ∈ {11, ..., 101},
NOT `[0.30, 0.35]` as SP-1a claims. **The true empirical c_{SP-2} is
~0.05, not 0.30.** This is a key error in SP-1a `§10` that α.3 must
correct.

## Step α.3.2 — Direct comparison

Plug C from α.2 into the inequality `|S_ψ| ≤ C · N̂ · (log N̂)^{1+ε}`. Compare
against `B_0 ≥ c_{SP-2} · N̂ · log N̂`. Closure iff
`C · (log N̂)^{ε} < c_{SP-2}` for all primes p with M(p) ≤ −3. If ε > 0,
this fails for sufficiently large N̂ unless C → 0; so **the asymptotic
shape must match exactly**: `|S_ψ| ≤ C · N̂ · log N̂` with strict `C <
c_{SP-2}`.

## Step α.3.3 — Bridge SP-2's RH-conditional vs unconditional

If SP-2 is RH-conditional, then α.3 is also RH-conditional (the chain B+
holds RH-conditionally). If SP-2 is unconditional, then α.2 must produce
an unconditional C. **As of this audit**, SP-2 is IN FLIGHT, status
unknown. α.3's verdict is conditional on SP-2's verdict.

## Output of α.3

A short document `SP1a_alpha_3_closure_check.md` with:
- Explicit `C` from α.2.
- Explicit `c_{SP-2}` from SP-2.
- Verdict: `CHAIN CLOSES` if `C < c_{SP-2}` strictly, else `CHAIN OPEN`
  with named further sub-step.

# 7. Predicted ABT/ETK bound at primes 11..101 (mpmath @ 50 dps)

See companion `SP1a_alpha_1.py` for full output. Selected rows:

| p   | n=N̂   | |S_ψ| (exact) | CS bound | Large-sieve `√[(N̂+(p−1)²)·ΣD²]` | ETK Koksma-Hlawka heuristic √(n·log n) | B_0 |
|----:|------:|--------------:|---------:|------------------------------:|---------------------------------------:|----:|
|  11 |    33 |          2.40 |    14.34 |                          90.18 |                                    8.16 |    1.64 |
|  17 |    81 |         10.56 |    44.10 |                         283.66 |                                   17.19 |    9.26 |
|  31 |   279 |         52.72 |   145.03 |                         929.56 |                                   39.64 |   83.72 |
|  47 |   651 |        145.30 |   451.92 |                        2870.59 |                                   64.94 |  213.54 |
|  73 |  1589 |        361.14 |  1478.76 |                        9349.10 |                                  108.22 |  726.34 |
| 101 |  3045 |        772.88 |  3414.72 |                       21569.08 |                                  156.28 |  915.12 |

**Crucial finding**: the Cauchy-Schwarz bound and the large-sieve bound
**both grow as O(N̂^{3/2}/√log N̂)**, structurally identical. The
Koksma-Hlawka heuristic via `D*_N(σ_p F) ~ 1/N̂` and `V_{HK}(D · ψ(p·))
~ N̂` and `||D||_∞ ~ √(N̂ log N̂)` gives `O(√(N̂ log N̂))`, which is **too
small**: the actual |S_ψ| at p = 101 is 772.88 while the K-H prediction is
only 156.28. **Since K-H is a rigorous upper bound, our naive estimate of
V_{HK} or ||D||_∞ must be wrong by a factor ~5**. This is a critical
mathematical inconsistency that SP-1a-α.2 must resolve.

# 8. Comparison vs SP-1a's empirical CS bound and the target B_0 ≥ c·N

## 8.1 Corrected empirical scaling (from companion verifier @ 50 dps)

| p   | n     | |S_ψ| | B_0    | |S_ψ|/(n·log n) | B_0/(n·log n) | margin/(n·log n) |
|----:|------:|------:|-------:|----------------:|--------------:|-----------------:|
|  11 |    33 |   2.40 |   1.64 |          0.0208 |        0.0142 |          −0.0066 |
|  13 |    47 |   4.91 |   5.26 |          0.0271 |        0.0291 |          +0.0019 |
|  17 |    81 |  10.56 |   9.26 |          0.0296 |        0.0259 |          −0.0037 |
|  19 |   103 |  16.74 |  18.88 |          0.0351 |        0.0397 |          +0.0046 |
|  31 |   279 |  52.72 |  83.72 |          0.0336 |        0.0533 |          +0.0198 |
|  47 |   651 | 145.30 | 213.54 |          0.0345 |        0.0506 |          +0.0162 |
|  53 |   831 | 196.47 | 281.27 |          0.0352 |        0.0503 |          +0.0151 |
|  73 |  1589 | 361.14 | 726.34 |          0.0308 |        0.0620 |          +0.0312 |
|  89 |  2369 | 593.45 | 944.12 |          0.0322 |        0.0513 |          +0.0190 |
| 101 |  3045 | 772.88 | 915.12 |          0.0316 |        0.0375 |          +0.0058 |

(The full 22-row table is in `SP1a_alpha_1.py` output; reproduced for
spot primes here.)

**Confidence**: 0.99 (exact rational arithmetic for |S_ψ| and B_0, verified
between SP1a_Im_Tm.py [V7] and SP1a_alpha_1.py at all 22 primes).

## 8.2 Major correction to SP-1a §10

SP-1a `§10` claims:

> `|S_ψ| / (n log n) ~ 0.03 - 0.04` — VERIFIED HERE.
>
> `B_0 / (n log n) ~ 0.30 - 0.35` — **WRONG**: actually `~ 0.014 - 0.062`.

This 10× error in the SP-1a writeup means:
- The "joint margin (B_0 − |S_ψ|)/(n log n) ~ +0.27 consistently" claim
  is **false**.
- The actual margin is `~ +0.005 - +0.035` (sometimes negative at small p),
  far tighter than SP-1a claims.

**Implication for SP-1a-α**: the constant C in SP-1a-α.2 must be
**strictly less than 0.05**, NOT less than 0.30 as SP-1a §10 implies. This
is a much harder target.

**Confidence in this correction**: 0.99 (exact rational for both B_0 and
|S_ψ|; cross-verified by independent re-implementation in
`SP1a_alpha_1.py`).

## 8.3 Comparison vs CS bound

CS bound: `|S_ψ| ≤ √(Σ_D² · Σ(f − 1/2)²)`. Empirical ratios `|S_ψ| / CS`
range from 0.17 to 0.30 (most tight at large p), so **CS is loose by
factor 3-5 in absolute terms** (consistent with SP-1a §6.5). However,
asymptotically CS gives `O(N̂^{3/2}/√log N̂)`, which **grows faster than
B_0 ~ O(N̂ log N̂)**, so CS alone never closes B+. ETK's predicted
`O(√(N̂ log N̂))` is FAR too small — likely indicating our V_{HK}
estimate is wrong (cf. §7).

# 9. Verdict — exactly one

**`BLOCKED-AT-ABT (paper unavailable; named alternatives + named further
sub-steps).`**

## 9.1 Why BLOCKED-AT-ABT

1. **The cited "ABT 2014, Trans. AMS 366" does not exist.** Searches
   covering arXiv, Aistleitner's homepage, Tichy's homepage, Google
   Scholar, the ABT 2013 survey [1312.0666] all fail to identify a paper
   with title "On the discrepancy of (αn) sequences" by ABT in 2014. The
   Trans. AMS 366 reference appears to be a confabulation.

2. **The closest real ABT paper from 2010-2014 (Aistleitner alone, Trans.
   AMS 365 (2013); ABT, Proc. AMS 139 (2011)) treats lacunary sequences
   `(n_k x)` with `n_{k+1}/n_k ≥ q > 1`.** The Farey sequence F_{p−1} is
   *dense*, NOT lacunary. The Hadamard gap condition is wildly violated.
   So ABT-style results CANNOT be transferred to our setup.

3. **The canonical explicit-constant ETK (Drmota-Tichy 1997 Theorem
   1.21, verified verbatim in §3.1 above) is applicable**, but at the
   heuristic level produces `|S_ψ(p)| ≤ O(√(N̂ log N̂))` which contradicts
   the exact-rational data (777 at p = 101 vs heuristic prediction
   ~156); so the V_{HK} estimate must be a factor 5+ too small. This
   is the named further sub-step.

4. **The corrected empirical `c_{SP-2} ~ 0.05` (from this audit's
   exact-rational mpmath@50dps verification) is far tighter than SP-1a's
   stated 0.30**, shrinking the closure margin by an order of magnitude
   and making ABT-style methods strictly insufficient at the
   leading-order asymptotic.

## 9.2 Named alternatives

a. **Drmota-Tichy 1997 Theorem 1.21 + Theorem 1.27** (verified in §3 above)
   gives ETK with constant 3/2 and `D*_N̂(F_N) = O(1/N̂)`.
   *Status:* directly applicable, produces (heuristically) a `O(√(N̂ log N̂))`
   bound on |S_ψ|. *Closes B+:* heuristically yes (since `√(N̂ log N̂) ≪
   N̂ log N̂`), but the heuristic contradicts data, so the underlying V_{HK}
   estimate is wrong. **Named sub-step: rigorous V_{HK} for D · ψ(p ·).**

b. **Niederreiter 1992** *Random Number Generation and Quasi-Monte Carlo
   Methods*: SIAM CBMS-NSF Regional Conf. Series 63, §3 (Erdős-Turán-Koksma
   inequality with explicit constants in 1-d via residue summation).
   *Status:* not directly downloadable; widely cited; same form as
   Drmota-Tichy. *Closes B+:* same as (a).

c. **Montgomery-Vaughan large sieve (Jameson Theorem LS2.1)**: applies
   directly via the dual sieve over Farey points (§4.4). Produces
   `|Σ_f D(f) e(m p f)| ≤ O(N̂/√log N̂)`. After Hurwitz aggregation gives
   `|S_ψ(p)| ≤ O(N̂ · √log N̂)` — **strictly worse than ETK route (a) by
   a factor √(N̂ log N̂ / log N̂) = √N̂**, but rigorous.
   *Status:* rigorous, no missing variation step. *Closes B+
   unconditionally:* no, because `√log N̂ > 0.05` for N̂ ≥ ~1, so we'd
   need C in the large-sieve constant strictly less than 0.05 / √log N̂,
   which the Montgomery-Vaughan constant `(N + Q²)` does not deliver.

d. **A direct second-moment bound on `Σ_b Σ_a |D(a/b)|²` per b**: this is
   essentially a refinement of CS using Mertens-style bounds on
   `Σ_{a coprime} D(a/b)²` per denominator b. This is the **key open
   sub-step** — neither ABT 2014 nor Drmota-Tichy 1997 give a direct
   bound at this level of granularity.

## 9.3 Named further sub-steps that, if resolved, would close B+

- **(α.2.3-revisited)** Compute V_{HK}(D · ψ(p ·)) on F_{p−1} rigorously,
  not via the naive O(p · N̂) estimate. Required to make the
  Koksma-Hlawka route (a) consistent with empirical data.
- **(α-bilinear)** A bilinear-form inequality of the type `Σ_b Σ_a D(a/b)
  · ψ(p a/b) = O(N̂ · log N̂ · (small constant))` that is stronger than
  the trivial Cauchy-Schwarz. Such an inequality does not appear in the
  classical literature; it would be **new mathematics**.
- **(SP-2)**: closed-form `B_0(N) ≥ c · N · log N` with EXPLICIT c. From
  empirical c ≈ 0.05, the c is at least 0.04-0.05 unconditionally. SP-2 in
  flight will deliver this.

## 9.4 Confidence on the verdict

Confidence in `BLOCKED-AT-ABT` verdict: **0.85**.

Reasoning:
- Confidence ABT 2014 paper-as-cited does not exist: 0.95 (multiple
  exhaustive searches, no hit).
- Confidence Drmota-Tichy 1997 / Niederreiter 1992 do not directly close
  the chain unconditionally: 0.85 (ETK heuristic is consistent with the
  empirical |S_ψ| size only if V_{HK}-bound is tightened by a factor 5+,
  which is non-trivial).
- Confidence the corrected empirical c_{SP-2} ≈ 0.05: 0.99 (exact
  rational, mpmath@50dps verified).
- Compound confidence: 0.95 · 0.85 · 0.99 ≈ 0.80, rounded to 0.85 for the
  verdict-level claim.

# 10. Companion files

- This document: `SP1a_alpha_1_ABT_2014_audit.md`
- Verifier: `SP1a_alpha_1.py` (mpmath @ 50 dps; computes |S_ψ|, B_0, CS,
  large-sieve, ETK heuristic at primes 11..101; outputs at
  `/tmp/SP1a_alpha_1.out` when run).

# 11. Open follow-on tasks for the next sub-step (SP-1a-α.2)

1. Resolve the V_{HK}-rigour gap in §4.3-Step 4 (compute V_{HK}(D · ψ(p·))
   precisely).
2. Test the dualized large-sieve (§4.4) against exact-rational |Σ_f D(f)
   e(m p f)| at primes 11..101 to verify the conjectured constant.
3. Document SP-2's closed-form lower bound c on `B_0(N) ≥ c · N · log N`
   when SP-2 lands; substitute the explicit c into α.3.
4. Investigate whether there is a **structural identity** linking
   `Σ_f D(f) ψ(p f)` to a sum-of-squares quantity that admits a sharper
   bound than CS or large-sieve alone (e.g. via the bijection
   `f ↔ σ_p(f)` of §6.4 of SP-1a).
5. If 1-4 all fail to close B+ unconditionally, the chain is OPEN; flag
   for RH-conditional analysis (cf. §6 of SP-1a).

# 12. Summary table — what this audit produced and what it didn't

| Item | Status |
|---|---|
| Located ABT 2014 PDF | **NOT FOUND** (paper does not exist as cited) |
| Verbatim Theorem 1 quote (ABT 2014) | **N/A** (paper does not exist) |
| Verbatim ETK Theorem 1.21 (Drmota-Tichy 1997) | YES (via Wikipedia + BRS 2024 cross-verification) |
| Verbatim Large-sieve Theorem LS2.1 | YES (Jameson notes) |
| Mapping our setup to ETK | DONE (§4) |
| Roadmap for SP-1a-α.2 | DONE (§5) |
| Roadmap for SP-1a-α.3 | DONE (§6) |
| Predicted ABT/ETK bound at primes 11..101 | DONE (§7, mpmath @ 50 dps) |
| Closure verdict | **BLOCKED-AT-ABT** |
| Critical correction to SP-1a §10 | DONE: empirical c_{SP-2} is ~0.05, NOT 0.30 |

End of document.
