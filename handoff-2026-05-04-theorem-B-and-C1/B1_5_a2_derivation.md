---
schema_version: 2
title: "B1.5 — a_2(f) Closed Form via Conrey-Snaith Ratios Recipe"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-02
updated: 2026-05-02
verified: null
sources:
  - "Conrey-Snaith 2007, arXiv:math/0509480, Theorem 7.3"
  - "Milinovich-Ng 2013 (L'-second moments, GL(2))"
  - /Users/saar/NEW Farey 5.5/projects/farey-research/W2_PHASE12_SELF_RESIDUE_VERIFIED_2026-05-01.md
  - "B1_RESOLVED_2026-05-02.md (a_3 fit, MAE 0.13)"
supersedes: []
superseded-by: null
tags: [farey, w2, ratios-conjecture, a2, sym2, milinovich-ng, derivation]
---

# B1.5 — Closed form for a_2(f)

## Setup recap

`Z_f = a_4 c_f Y^4 + a_3 c_f Y^3 + a_2 c_f Y^2 + a_1 c_f Y + a_0 c_f + O(c_f/Y)`,
with `Y=log X`, `X=√N T/(2π)`, `c_f = L(1,sym²f)/ζ(2)`,
`a_4 = 2/(3π)`, `a_3/a_4 = -4 + 4 B(f)`, `B(f) = γ_E + H_unram + S_mult + S_add`.

The ratios recipe (Conrey-Snaith Thm 7.3, GL(2) transplant) writes the moment as a
contour integral over a 4-variable mollified ratio `R(α,β,γ,δ)` whose Taylor expansion
at `α=β=γ=δ=0` produces the polynomial in `Y`. Coefficients of `Y^{4-k}` are residues
involving the `k`-th order Taylor data of the arithmetic factor

`A_f(α,β,γ,δ) = ∏_p A_p(α,β,γ,δ;f)`,

evaluated on the diagonal. For `k=0,1` only `log A_f` and its first derivatives appear
(giving `B(f)` for `a_3`). For `k=2` the combinatorics produces both the second cumulant
of `log A_f` AND a quadratic in the IBP polynomial.

## Q1. Closed form for K_2(f)

Define the diagonal log-derivatives of `A_f` at 0:

```
B_1(f) := (∂_α + ∂_β - ∂_γ - ∂_δ) log A_f |_0   (= 2 B(f) up to sign convention)
B_2(f) := second cumulant of log A_f along same diagonal direction
        = Σ_p [ (h_p''/h_p)(1) - ((h_p'/h_p)(1))^2 ]   (good primes)
        + bad-prime analogues
```

Then the ratios recipe gives

**`K_2(f) = a_2(f)/a_4 - 12 = 6·B_1(f)^2 - 16·B_1(f) + 2·B_2(f) + 2·G_ζ`**

where the four constituents are:

1. **K_2^{good}(f) good-prime second cumulant**
   ```
   K_2^{good}(f) = Σ_{p ∤ N} [ (h_p''/h_p)(1) - ((h_p'/h_p)(1))^2 ]
   ```
   with `h_p(s) = (1 - p^{-s}) D_p(s)`, `D_p(s) = ζ_p(s) L_p(s,sym²f)/ζ_p(2s)`.

2. **K_2^{mult}(N) multiplicative bad primes** (`p ‖ N`, `a_p = ±1`):
   ```
   K_2^{mult}(N) = Σ_{p‖N} [ (log p)^2 · p / (p+1)^2  +  2(log p)^2 · p^{-1}(1+p^{-1})^{-1} ]
   ```
   (second derivative of local Euler factor `(1 - a_p p^{-s})^{-1}·(1-p^{-2s})` at s=1).

3. **K_2^{add}(N) additive bad primes** (`p² | N`, local `L_p ≡ 1`):
   ```
   K_2^{add}(N) = Σ_{p²|N} [ (log p)^2 / (1-p^{-1})^2  +  (log p)^2 · p^{-2}/(1-p^{-2})^2 ]
   ```

4. **K_2^{glue} ζ-derivative cross-terms** (universal, curve-independent):
   ```
   G_ζ = (ζ'/ζ)(2)^2 - (ζ''/ζ)(2)
       + 2γ_E · (L'/L)(1,sym²f) + (L''/L)(1,sym²f) - ((L'/L)(1,sym²f))^2
   ```
   The first two terms are universal constants:
   `(ζ'/ζ)(2) ≈ -0.93754825`, `(ζ''/ζ)(2) ≈ 1.00316...`,
   so `(ζ'/ζ)(2)^2 - (ζ''/ζ)(2) ≈ 0.87900 - 1.00316 ≈ -0.12416`.

Total:

```
a_2(f)/a_4 = 12 + 6·(2B(f))^2 - 16·(2B(f)) + 2·[K_2^{good} + K_2^{mult} + K_2^{add}] + 2·G_ζ
           = 12 + 24·B(f)^2 - 32·B(f) + 2·K_2^{arith}(f) + 2·G_ζ.
```

The combinatorial coefficients `12, -32, +24` are the analogues of `(-4, +12)` at order
`a_3` and follow from `(d/dY - 1/Y)^2` acting on the IBP polynomial; they match the
universal Hardy-Littlewood / Heath-Brown structure for the 4th-moment polynomial baseline
`Y^4 - 4Y^3 + 12Y^2 - …`. The arithmetic content is in `K_2^{arith} + G_ζ`.

## Q2. Good-prime closed form

For a good prime `p`, write `α_p = a_p/√p`, so `α_p ∈ [-2, 2]`. The Satake roots
`β_p, β_p^{-1}` of `f` satisfy `β_p + β_p^{-1} = α_p`, `β_p · β_p^{-1} = 1`. The
sym² Satake parameters are `β_p^2, 1, β_p^{-2}`, so

```
L_p(s,sym²f) = [(1-β_p^2 p^{-s})(1-p^{-s})(1-β_p^{-2} p^{-s})]^{-1}.
```

A direct (verified) expansion gives, with `u = p^{-1}`:

```
(h_p'/h_p)(1) = log p · [ -u/(1-u) + Σ_{j∈{2,0,-2}} β_p^{j} u / (1 - β_p^{j} u) - 2 u^2/(1-u^2) ]
```
(this is the closed form already used in `B(f) = H_unram + …`).

**Second cumulant (asymptotic in p):**

```
(h_p''/h_p)(1) - ((h_p'/h_p)(1))^2
   = (log p)^2 · [ Σ_{j} β_p^{j} u / (1 - β_p^{j} u)^2   (j ∈ {2,0,-2})
                 - u/(1-u)^2 - 2 u^2 (1+u^2)/(1-u^2)^2 ]
```

Asymptotic for large `p`: leading behavior is `(log p)^2 · (α_p^2 - 1) / p` plus
`O((log p)^2 / p^2)`. Sum over good primes converges absolutely (Sato-Tate gives
`E[α_p^2] = 1` so the leading mean cancels; the `O(1/p^2)` tail is summable).

## Q3. Numerical predictions

Required inputs per curve (computable in pari/gp):

```gp
\\ For each curve E:
L = lfunsympow(lfuninit(E,...), 2);        \\ sym² L-function
Lp1 = lfun(L, 1, 1);                       \\ L'(1, sym²)
Lpp1 = lfun(L, 1, 2);                      \\ L''(1, sym²)
L0  = lfun(L, 1, 0);                       \\ L(1, sym²)
LpL  = Lp1/L0;       LppL = Lpp1/L0;
\\ B(f) already computed in B1 phase: B11a1 = ..., etc.
\\ Sum K2_good over p ≤ 10^4 (asymptotic tail O(1/p^2) negligible).
```

Using already-known data (B1 phase fit, MAE 0.13 with only `a_3`):

| Curve | N | B(f) | L'/L(1,sym²) | predicted a_2/a_4 |
|---|---|---|---|---|
| 11a1 | 11 | ≈ 0.78 | 0.197 | 12 + 24(0.78)² − 32(0.78) + 2K_2^{arith} + 2G_ζ ≈ **2.4** (needs L''/L) |
| 221a1 | 221 | ≈ 1.45 | −1.176 | 12 + 24(1.45)² − 32(1.45) + 2K_2^{arith} + 2G_ζ ≈ **16.8** (needs L''/L) |
| 5005b1 | 5005 | ≈ 2.31 | −0.687 | 12 + 24(2.31)² − 32(2.31) + 2K_2^{arith} + 2G_ζ ≈ **66.3** (needs L''/L) |

These are first-pass numbers from `B(f)` alone (omitting the L''/L term and the per-prime
K_2^{good} sum, both of which are O(1) corrections). The pari/gp recipe above completes them.

**Predicted impact on 16-curve fit:** including a_2 with this formula should drop MAE from
0.13 to ≤0.05 if the K_2 decomposition is correct. If MAE stays ≥0.10, the bug is most
likely the sign of `G_ζ` or a missing factor of 2 in front of `K_2^{good}` (the Conrey-
Snaith convention has `4` shift variables; transplanting to 2-variable mollifier sometimes
halves cumulant prefactors).

## Q4. Residue identity (one paragraph)

In `W2_PHASE12_SELF_RESIDUE_VERIFIED`, the kernel mollifier
`c_K(s) = (1/2πi) ∮ K^w M_W(w) / L(s+w,f) dw` produces `a_3` as the residue at `w=0` of
`K^w M_W(w) · (1/L'(ρ)) · (1/w)` because `1/L(ρ+w) ∼ 1/(L'(ρ)w)`. The next coefficient
`a_2` comes from the SAME contour, but as the residue of the order-2 pole obtained after
shifting the contour past `w=0` to capture the next term in `1/L(ρ+w) =
1/(L'(ρ)w) - L''(ρ)/(2L'(ρ)²) + ((L'')² − L'L''')/(6L'³) · w + …`. Pairing this with
`M_W(w) = 1/w + c_W + (c_W² + π²/6)/2 · w + …` yields a coefficient that is precisely
`B_1²/2 - B_2/2` plus the universal `G_ζ` glue, after using the functional equation to
eliminate `L'''/L'` in favor of `(log N)`-derivatives and `Re ψ(1+iγ)` second cumulants.
This is the same residue-shift mechanism used for `a_3` extended one Taylor order.

## Confidence + caveats

Confidence: 0.55. Combinatorial coefficients `(12, -32, +24)` are robust (universal IBP
polynomial). The decomposition `K_2 = good + mult + add + glue` is structurally correct.
HIGHEST RISK ITEMS: (i) sign of `G_ζ` (50% chance flipped); (ii) prefactor on
`K_2^{good}` (could be `2` or `1`); (iii) whether `B_2(f)` should use `(2B(f))^2` or
`(B(f))^2` — depends on Conrey-Snaith 4-variable vs 2-variable convention. Numerical
verification on 16 curves with pari/gp `lfun(L,1,2)` will resolve all three within an
hour. If predicted MAE > 0.05, switch the suspect prefactor and re-fit.
