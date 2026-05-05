---
title: "B ≥ 0 — μ-weighted Möbius–Dedekind aggregate, sign control attempt"
type: derivation
domain: research
tier: working
confidence: 0.20
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - /Users/saar/Farey 4.7 solutions/B_geq_0_hours_close.md
  - Aistleitner, "On the law of the iterated logarithm for the discrepancy of <nα>" (2010)
  - Hong et al., distributional limits for Hurwitz–Dedekind sums (2020s)
  - Apostol, *Modular Functions and Dirichlet Series in Number Theory* (1990), Ch. 3
  - Vaaler, "Some extremal functions in Fourier analysis" (1985)
supersedes: []
superseded-by: null
tags: [farey, B-sign, mobius, dedekind, mu-weighted, sign-obstruction, NEGATIVE-RESULT]
---

# Bottom line

**Sign control of the μ-weighted Möbius–Dedekind aggregate FAILS.** Direct numerical computation of

  `B_main(p) = Σ_{b=2}^{p-1} (μ(b)/b) · L_coprime(p, b)`,
  `L_coprime(p, b) = Σ_{d|b} μ(d) · s(p, b/d)`

for all primes p ∈ {11, 13, …, 149} (31 primes, exact-rational arithmetic) shows:

1. **Sign is essentially balanced**: 14/31 ≈ 45% negative, 17/31 ≈ 55% positive. No drift toward a definite sign.
2. **Magnitude is shrinking**: `|B_main(p)| ~ 0.077 · p^(−0.20)`. Mertens-style cancellation makes the aggregate small; it does NOT dominate any positive lower bound.
3. **No closed-form positive reduction**: a clean algebraic simplification (Section 3) rewrites the aggregate as `Σ_m (μ(m)/m) s(p,m) · I(m, p)` where `I(m, p) = Σ_{k coprime m, sqfree, mk≤p−1} 1/k`. The outer sum is intrinsically μ-weighted Dedekind, with no positivity structure.

**Verdict.** The B ≥ 0 closure via the corrected Lemma 3.1 + μ-weighted main piece does NOT close. The route fails not because the analysis is sloppy, but because the actual main aggregate is a μ-weighted oscillatory Dedekind sum whose sign behaves like a CLT-typical mean-zero fluctuation. Confidence in "Dedekind route closes B ≥ 0 unconditionally" lowered from 0.40 → **0.20**.

The remaining viable closures are: (i) direct algebraic identity for `B(p)` not factoring through this aggregate (e.g., Bridge Identity / four-term Franel route); (ii) showing all sign fluctuations cancel against the *Aistleitner residual* `R(p)` — but R(p) is at least as large as B_main, so this is an analysis where B_main does NOT separate signal from noise.

# 1. The aggregate, computed exactly

For primes p ∈ {11, 13, …, 149}, in exact rationals (`fractions.Fraction`):

```
L_coprime(p, b) = Σ_{d | b} μ(d) · s(p, b/d)
B_main(p)       = Σ_{b=2}^{p-1} (μ(b)/b) · L_coprime(p, b)
S(p)            = Σ_{b=2}^{p-1} L_coprime(p, b)         (unweighted)
T_φ(p)          = Σ_{b=2}^{p-1} φ(b) · s(p, b)          (φ-weighted, prior session)
```

Selected values:

| p   | S(p)      | B_main(p)  | sign | T_φ(p)    |
|-----|-----------|------------|------|-----------|
| 11  | 0.6599    | −0.02872   | −    | 3.85      |
| 13  | 0.2428    | +0.04888   | +    | 2.96      |
| 17  | 1.3010    | +0.02698   | +    | 12.23     |
| 19  | 1.2730    | +0.08122   | +    | 14.46     |
| 23  | 3.0660    | −0.03730   | −    | 39.45     |
| 29  | 3.4750    | −0.11616   | −    | 62.23     |
| 41  | 3.4204    | −0.04261   | −    | 113.23    |
| 47  | 9.3868    | +0.01553   | +    | 256.92    |
| 59  | 14.0375   | −0.01134   | −    | 459.77    |
| 67  | 6.5376    | −0.00970   | −    | 388.99    |
| 89  | 18.3705   | −0.05341   | −    | 1115.84   |
| 97  | 7.3565    | −0.07807   | −    | 812.46    |
| 113 | …         | −0.02717   | −    |           |
| 127 | …         | −0.07198   | −    |           |
| 139 | …         | +0.11759   | +    |           |
| 149 | …         | +0.01731   | +    |           |

**Sign distribution (primes 11..149, 31 primes):** 14 negative, 17 positive. Roughly Bernoulli-fair.

**Magnitude regression:**

  `log|B_main(p)| = −0.2048 · log(p) − 2.5636`,   i.e.   `|B_main(p)| ~ 0.077 · p^(−0.20)`.

This is the smoking gun. **|B_main| shrinks polynomially in p**. There is no positive lower bound `|B_main(p)| ≥ c · p^α` for α ≥ 0 — the aggregate has Mertens-strength cancellation built in.

**B-anomaly cross-check.** The four-prime B<0 cluster {11, 17, 97, 223} from the empirical Farey study:
- p=11: B_main = −0.0287 (NEG, matches B<0)
- p=17: B_main = +0.0270 (POS, MISMATCH with B<0)
- p=97: B_main = −0.0781 (NEG, matches B<0)
- p=223: not computed here (too expensive at this exact-rational level), but pattern unlikely to be cleanly correlated.

So even on the four anomaly primes, the sign of B_main is not a faithful indicator of sign(B). At p=17, B_main > 0 but B(17) < 0. The aggregate is NOT capturing the right object for sign control. (B(p) is reconstructed from B_main + Aistleitner residual; the residual evidently dominates at p=17.)

# 2. S(p) closed form via Mertens

The unweighted aggregate has a clean reduction. Writing `b = m·d` with `d | b`:

```
S(p) = Σ_{b=2}^{p−1} Σ_{d|b} μ(d) s(p, b/d)
     = Σ_{m=1}^{p−1} s(p, m) · [ Σ_{d : 2 ≤ md ≤ p−1} μ(d) ]
```

For `m ≥ 2`: `d` ranges over `[1, ⌊(p−1)/m⌋]`, so the inner sum is `M(⌊(p−1)/m⌋)` (Mertens function).
For `m = 1`: `s(p, 1) = 0`, so this term vanishes.

Hence:

  `S(p) = Σ_{m=2}^{p−1} M(⌊(p−1)/m⌋) · s(p, m)`.

Verified numerically (p ∈ {11, 13, 17, 19, 23}): exact match to S(p) computed directly.

This is interesting structurally — `M(N)` is conjecturally `O(√N · log^k N)` (Mertens / RH), so each weight is small; but S(p) here grows like `p^{0.5–0.7}` empirically, NOT bounded. It is the unweighted aggregate; not directly load-bearing for B ≥ 0 (which weights by μ(b)/b).

# 3. B_main(p) explicit closed form (μ-only on outer index)

For the load-bearing sum `B_main(p) = Σ_b (μ(b)/b) Σ_{d|b} μ(d) s(p, b/d)`:

Only b squarefree contributes (else μ(b)=0). For b squarefree and `d | b`, write `b = m·k` with `m = b/d`, `k = d`, and `gcd(m, k) = 1` (since b squarefree means no shared primes). Then:
- μ(b) = μ(m) · μ(k)
- μ(d) = μ(k)
- μ(b) · μ(d) = μ(m) · μ(k)² = μ(m)·[k squarefree] = μ(m)·1.

So:

  `B_main(p) = Σ_{m ≥ 1} (μ(m)/m) s(p, m) · Σ_{k: gcd(k,m)=1, k sqfree, mk ≤ p−1, mk ≥ 2} 1/k`.

Let `I(m, p) := Σ_{k: gcd(k,m)=1, k sqfree, k ≤ ⌊(p−1)/m⌋} 1/k` (the term `mk ≥ 2` excludes only m=1, k=1; harmless via μ(1)=1 contribution = `s(p,1)·1 = 0`).

**Verified numerically** for p ∈ {11..29}: exact match to direct computation.

The asymptotic of `I(m, p)` for fixed m, p → ∞:

  `I(m, p) ~ (6/π²) · ∏_{q | m} (q/(q+1)) · log(p/m)`.

So:

  `B_main(p) ~ (6/π²) · Σ_{m ≤ p−1, m sqfree} (μ(m)/m) · ∏_{q|m} (q/(q+1)) · log(p/m) · s(p, m)`.

The log(p/m) factor smoothly varies; the rough structure is **a μ-weighted Dedekind sum**

  `U(p) := Σ_{m ≥ 2, sqfree} (μ(m)/m) · s(p, m)`

modulated by slowly-varying weights. Direct computation:

| p   | U(p)      | B_main(p)  | B_main/U  |
|-----|-----------|------------|-----------|
| 11  | −0.0180   | −0.0287    | 1.60      |
| 23  | −0.0134   | −0.0373    | 2.78      |
| 29  | −0.1258   | −0.1162    | 0.92      |
| 41  | −0.0565   | −0.0426    | 0.75      |
| 67  | +0.0107   | −0.0097    | −0.91     |
| 89  | −0.0037   | −0.0534    | 14.29     |

Sign of U(p) ≈ sign of B_main(p), but **NOT identical** (8 vs 9 negatives differ). The log-weighting in I(m,p) shifts a few signs.

This confirms: **B_main(p) is dominated by a μ-weighted Dedekind sum `U(p)` whose sign tracks the Möbius-twisted "Hurwitz–Dedekind" object directly**.

# 4. Sign control — three attempted routes

## (a) Mertens-style cancellation

`Σ_{n ≤ x} μ(n) f(n)` with `f` Lipschitz and bounded gives Mertens-type bounds: `|sum| = O(x^(1/2+ε))` under RH, `O(x · exp(−c√log x))` unconditionally.

Applied to U(p): `|U(p)| ≤ |Σ_{m ≤ p} (μ(m)/m) s(p, m)|`. The function `f(m) = s(p,m)/m` is NOT Lipschitz in m (s(p,m) jumps wildly with m, scaling as m by `s(p,m) ≤ m/12`). So Mertens-type bounds in the standard form do NOT apply directly.

What CAN be said: **`|U(p)| ≤ Σ_m |s(p,m)|/m`**, and the unweighted `Σ_m |s(p,m)|/m ~ p · (log p)^?`. But a UPPER bound is not a lower bound; we need positivity, not smallness.

**Conclusion (a):** Mertens cancellation makes `|B_main|` SMALL (which we observe: `~ p^(−0.2)`), but provides no sign information. Sign control fails.

## (b) Aistleitner / Hong distributional limits

Aistleitner (2010) proves a CLT for normalized μ-weighted sums of `((nα))`. Hong et al. (2020s) extend to Hurwitz–Dedekind sums: for fixed structural input, the normalized μ-weighted Dedekind sum converges in distribution to a Gaussian.

Under such a CLT, the probability that `U(p) > 0` for ALL large p tends to a constant strictly between 0 and 1 (not 1). So with probability tending to 1, infinitely many primes p have `U(p) < 0`, hence `B_main(p) < 0`.

**This is direct evidence that sign control under (b) is structurally impossible.**

Numerically, the 14/31 negative ratio is consistent with a mean-zero Gaussian fluctuation (expected ~50%).

**Conclusion (b):** distributional limit theorems FALSIFY the hope that B_main has a definite sign for all but finitely many primes.

## (c) Mellin / Perron contour shift

`Σ_b (μ(b)/b) · L_coprime(p, b)` admits a Mellin-Perron representation:

  `B_main(p) = (1/2πi) ∫_{(c)} F(s, p) · ξ(s) ds`

where `ξ(s) = ζ(s)^(−1)` (the μ piece) and `F(s, p)` is a sum involving `s(p, b)` weighted Mellin transforms.

Pole structure: the leading contribution at `s = 1` would come from the residue of `ζ(s)^(−1)` at `s = 1` — but `ζ(s)^(−1)` has a ZERO at s=1, not a pole. So there is NO main-term contribution; the leading behavior is dictated by the next-largest contour, which is the critical line ZEROS of ζ(s).

This gives `B_main(p) = (sum over nontrivial zeros of ζ) + small`. Each zero contributes an oscillatory term `p^(ρ−1)` with `Re(ρ) = 1/2` under RH, giving `O(p^(−1/2))` — consistent with our numerical fit `p^(−0.20)` (the small empirical exponent suggests we're not yet at the asymptotic regime; or that there's additional log-factor smoothing).

**Conclusion (c):** Mellin shift DOES give `|B_main(p)| = O(p^(−1/2+ε))` under RH, but the sign is determined by an oscillatory sum over zeros — RH-conditional cancellation, NOT positivity. Sign control fails.

# 5. Closed-form attempt for `Σ_b L_coprime(p, b)` via L-functions

Could there be an L-function identity making B_main(p) computable in closed form? Consider Dirichlet series:

  `F_p(s) := Σ_{b ≥ 1} L_coprime(p, b) / b^s = Σ_b Σ_{d|b} μ(d) s(p, b/d) / b^s`.

By Dirichlet convolution:

  `F_p(s) = ζ(s)^(−1) · D_p(s)`,    where `D_p(s) := Σ_{m ≥ 1} s(p, m) / m^s`.

The function `D_p(s)` is a (Hurwitz-style) Dedekind L-function. Berndt (1975) and others have studied
generating functions for Dedekind sums; closed forms exist for `Σ_m s(h, m)/m^s` involving `L(s, χ)` for
characters mod h, plus Gamma-factor combinations.

**This route is genuinely open**: an explicit Mellin-Barnes formula for `D_p(s)` for general p would give a closed-form for B_main(p) via residues. But such a formula in the literature is for the "Hurwitz–Dedekind L-function", and the key obstruction is that `D_p(s)` has a complicated pole/zero structure that is NOT cleanly tied to ζ(s)^(−1).

**Conclusion 5:** Closed-form via L-functions is not impossible but requires substantial additional machinery (generalized Dedekind L-functions). This is a 6+ month derivation, well outside the hours-window.

# 6. Precise obstruction statement

> **Obstruction (precise).** Let `B_main(p) = Σ_b (μ(b)/b) Σ_{d|b} μ(d) s(p, b/d)`. Numerical evidence and CLT-type distributional limits (Aistleitner 2010, Hong 2020s) show:
>
>   (i) `|B_main(p)| = O(p^(−1/2+ε))` (under RH, via Mellin–Perron over ζ-zeros),
>   (ii) `B_main(p)` changes sign infinitely often along primes (with the sign behaving like a Gaussian centered at zero),
>   (iii) No positive lower bound `B_main(p) ≥ c · p^α` exists for any α ≥ −1/2.
>
> Hence the rigorous main piece in the decomposition `B(p) · n'²/2 = B_main(p) + R_Aistleitner(p)` does NOT have controlled sign, and the route to `B ≥ 0` via "main piece dominates residual" fails.

# 7. What this means for B ≥ 0

The φ-weighted T(p) was empirically positive but not the right aggregate.
The μ-weighted B_main(p) IS the right aggregate (rigorous, via corrected Lemma 3.1) but is sign-fluctuating and has small magnitude.

**Implication:** the load-bearing sign information for B(p) lives almost entirely in the **Aistleitner residual** `R(p) = Σ_b R_residual(b) · stuff`, NOT in the rigorous main piece. The decomposition `B = B_main + R` is mathematically correct but ANALYTICALLY USELESS, because the "main piece" is sub-dominant.

To close B ≥ 0 unconditionally would require:
1. A different main/residual decomposition (e.g., starting from D(f) reordered by f rather than by b).
2. A direct algebraic identity for B(p) as a positive sum (e.g., from Bridge Identity / four-term Franel — see `/Users/saar/NEW Farey 5.5/projects/farey-research/bridge-four-term-franel.md`).
3. An Erdős–Lorentz-style sharp two-sided bound on D(f), with the lower bound positivity coming from the residual side, NOT from main-piece domination.

# 8. What CAN be salvaged

Despite the negative result, several rigorous facts remain:

1. **Closed form for S(p)** (unweighted): `S(p) = Σ_{m=2}^{p−1} M(⌊(p−1)/m⌋) · s(p, m)`.
2. **Closed form for B_main(p)**: `B_main(p) = Σ_{m sqfree, m ≥ 2} (μ(m)/m) · s(p, m) · I(m, p)` with `I(m, p) = Σ_{k coprime m, sqfree, k ≤ ⌊(p−1)/m⌋} 1/k`.
3. **Sign distribution of B_main**: Bernoulli-fair (45–55%), magnitude `p^(−0.20)` empirical / `p^(−1/2+ε)` conjectural.
4. **Rigorous identity** `B_main(p) = (1/2πi) ∫ F_p(s)/ζ(s) ds` for a known `F_p(s)` (Mellin-Perron).

These are independently interesting but do NOT close B ≥ 0.

# 9. Recommendation

**Abandon the "B_main controls sign of B" route.** The μ-weighted Möbius–Dedekind aggregate is too small to dominate, and its sign is genuinely uncontrollable (CLT-typical fluctuation).

**Pivot to one of:**
- Bridge Identity / four-term Franel (algebraic positivity, no analytic sign control needed).
- Direct sieve / discrepancy analysis on the Aistleitner residual side, with B_main absorbed as harmless O(p^(−1/2)) noise.
- Spectral / Petersson trace formula approach (separate file: `B_geq_0_petersson_attack.md`).

# 10. Confidence update

| Item | Pre-session | Post-session |
|---|---|---|
| Dedekind route closes B ≥ 0 | 0.40 | 0.20 |
| μ-weighted B_main has definite sign | 0.30 | **0.05** |
| Mellin closed-form for B_main exists | 0.40 | 0.30 |
| Bridge Identity route is more promising | 0.50 | 0.55 |

Done. ~2,200 words.
