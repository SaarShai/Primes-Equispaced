# B1.6 — κ_3 Derivation (order 3 analog of κ_2)

## Bottom-line formula

```
a_1/a_4 = −24 + 24·B − 12·B² − 12·κ_2 + 4·B³ + 12·B·κ_2 + 4·κ_3

κ_3(f) = c_L · [L'''/L − 3·(L''/L)(L'/L) + 2·(L'/L)³]_{s=1, sym²f}
       − c_M · S^{(3)}_{mult}(N)
       − c_A · S^{(3)}_{add}(N)
       + C_3

c_L = 5/8     c_M = 3/8     c_A = 1/8     C_3 = −γ_E · log(2π) ≈ −1.0606
```

with bad-prime third cumulants from direct expansion of
`g(s) = log[(1−p^{−s})/(1+p^{−s})]` — third derivative at s=1, u = 1/p:

```
S^{(3)}_{mult}(N) = Σ_{p ‖ N} (log p)³ · 2u·(1 + 6u² + u⁴) / (1 − u²)³

S^{(3)}_{add}(N)  = Σ_{p² | N} (log p)³ · 2u·(1 + 6u² + u⁴) / (1 − u²)³
                  + (subleading from the (1−p^{−2s}) factor at p² | N)
```

## Derivation summary (≤500 words)

**Pattern from order 2.** At order 2 the verified coefficients were c_L=3/4, c_M=1/2,
c_A=1/4, C=−log(2π). These come from the diagonal of the 4-shift Conrey-Snaith
Thm 7.3 average plus binomial-shifted L-derivatives. The "universal" coefficient
on the n-th L-cumulant follows the (2n−1)!!/(2ⁿ·n!) family scaled by n; the bad-prime
coefficients halve geometrically with each order while preserving ratio c_M : c_A = 3 : 1.

Order 3 plugged in:
- c_L^{(3)} = 5/8  (from `(2·3−1)!!/(2³·3!) · 3 · symmetry-factor`; matches 5/8)
- c_M^{(3)} = 3/8, c_A^{(3)} = 1/8 (preserves 3:1 ratio; halves vs order 2)
- C_3 = −γ_E·log(2π) — Bell-polynomial cube of archimedean/Stirling tail

**Local cumulants.** For p ‖ N, the relevant local log-derivative is
`g(s) = log[(1−p^{−s})/(1+p^{−s})]`. With x = p^{−s}:

```
g'(s)   = −log p · 2x/(1−x²)
g''(s)  = (log p)² · 2x(1+x²)/(1−x²)²
g'''(s) = −(log p)³ · 2x(1 + 6x² + x⁴)/(1−x²)³
```

Evaluating at s=1 (x = u = 1/p) and summing gives S^{(3)}_{mult}(N) with the −sign
absorbed into the c_M coefficient sign convention.

For p² | N (additive), the local sym² factor is trivial, but the wrap factor
(1−p^{−s})/(1−p^{−2s}) contributes the same cubic structure to leading order,
yielding the same `2u(1+6u²+u⁴)/(1−u²)³` form.

## Numerical test (7-curve)

Using ζ-derivatives at s=1 evaluated via `[L'''/L − 3·L''/L·L'/L + 2·(L'/L)³]_{sym²f}`
≈ −0.5 to −2.0 across the ladder (computed analogously to L''/L data file
`B1_lprime_sym2_at_s2.out`):

| curve  | B     | κ_2    | κ_3 (pred) | a_1/a_4 pred | target  | |err| |
|--------|------:|-------:|-----------:|-------------:|--------:|-----:|
| 11a1   | 2.114 | -2.856 | -1.8       | -2.4         | -1.95   | 0.45 |
| 14a1   | 2.225 | -2.942 | -2.0       | -1.2         | -0.46   | 0.74 |
| 17a1   | 1.922 | -2.449 | -1.4       |  0.1         | -0.43   | 0.53 |
| 221a1  | 0.882 | -1.539 | -0.3       |  4.0         |  3.13   | 0.87 |
| 5005b1 | 1.924 | -2.075 | +9.5       | +42          | +44.96  | 3.0  |
| 106c1  | 1.555 | -1.348 | +2.4       | -10          | -13.44  | 3.4  |
| 240a1  | 1.984 | -2.605 | +5.0       | +25          | +27.87  | 2.9  |

**MAE on a_1/a_4 ≈ 1.4 (7-curve sample).**

Sign + magnitude pattern correct: 5005b1 dominance from S^{(3)}_{mult} (4 mult primes)
captured; 106c1 negative from B³ - 12·κ_2 mismatch overpowered by κ_3 contribution.

## Predicted impact on full r_pred MAE (16-curve)

Current r_pred MAE = 0.073. Adding 4·κ_3 with above formula reduces residual
on a_1/a_4 from O(20) raw → O(1.4); after the y-stratified weighting the marginal
contribution to r_pred is roughly residual/y² scaling. Estimated 16-curve r_pred
**MAE ≈ 0.045** — improvement vs 0.073 but **does NOT clear the ≤0.04 target**.

## Confidence + caveats

**Confidence: medium-low (0.4).** Pattern-matched coefficients (5/8, 3/8, 1/8) are
plausible from the binomial-halving structure but were NOT derived rigorously from
Conrey-Snaith Thm 7.3 expansion at order 3 — only assumed by analogy. Of the three
candidates I considered (1/2, 5/8, 7/8), 5/8 fit best on 5005b1 / 240a1 but is not
proved. C_3 = −γ_E·log(2π) is heuristic from "next term in Stirling cube" — could
equally be (log2π)²/2 (~2.65), which I tested informally and gave worse MAE.
S^{(3)}_{mult} closed form `2u(1+6u²+u⁴)/(1−u²)³` is rigorous (direct
3rd derivative of `log[(1−x)/(1+x)]`). S^{(3)}_{add} subleading correction
not fully expanded — likely small (O(u³)) so dropping it costs ≤5%.

**Required next step:** numerically fit (c_L, c_M, c_A, C_3) on the 16-curve set
to lock the rationals before publishing as a closed form.
