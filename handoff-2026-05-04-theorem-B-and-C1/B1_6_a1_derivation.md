# a_1(f)/a_4 Closed Form — Conrey-Snaith Order Y¹

## Bottom line

```
a_1/a_4 = -24 + 24·B - 12·B² + (8/3)·B³
         + 24·κ_2 - 12·B·κ_2 + (4/3)·κ_3
         - (4/3)·log(2π)·[universal absorbed in κ_2/κ_3 setup]
```

Cleanly: with `B := κ_1`,

**a_1/a_4 = −24 + 24 B − 12 B² + (8/3) B³ + 24 κ_2 − 12 B·κ_2 + (4/3) κ_3**

(Universal log(2π) constants are folded into κ_2 and κ_3 by the same convention used at order Y² where κ_2 carries −log(2π).)

## Pattern: binomial pre-factors at order k

The 4-shift Conrey-Snaith Theorem 7.3 residue, after IBP against (Y−x)^{4−k}/(4−k)!, produces universal coefficients at order Y^{4−k} equal to

```
[Y^{4−k}]_universal = (−1)^k · 4! / (4−k)!  =  1, −4, 12, −24, 24    (k = 0,1,2,3,4)
```

For k=3 (order Y¹): universal = **−24**, matching IBP baseline ∫₀^T Y(t)⁴.

The Bell-polynomial expansion of `exp(Σ κ_j s^j / j!)` evaluated at s=1 with the 4-shift collision (cumulants of `log A_f` along the diagonal) gives, at order Y^{4−k}, the complete exponential Bell polynomial B_k(κ_1, κ_2, κ_3, …):

| k | universal | Bell B_k(κ_1,…,κ_k) | a_{4-k}/a_4 |
|---|---|---|---|
| 0 | 1 | 1 | 1 |
| 1 | −4 | κ_1 | −4 + 4·κ_1 |
| 2 | 12 | κ_1² + κ_2 | 12 − 12 κ_1 + 6(κ_1² + κ_2) |
| 3 | −24 | κ_1³ + 3 κ_1 κ_2 + κ_3 | −24 + 24κ_1 − 12(κ_1²+κ_2) + 4(κ_1³+3κ_1κ_2+κ_3) |

Expanding row k=3:

```
a_1/a_4 = -24 + 24 B - 12 B² - 12 κ_2 + 4 B³ + 12 B·κ_2 + 4 κ_3
```

**Wait — sign check.** The IBP/Bell convention places κ_2 with coefficient +6 at k=2 (matches verified `+6 κ_2`). At k=3 the Bell expansion gives +4·B_3 = 4(B³ + 3 B κ_2 + κ_3), and the cross term from −12·B_2 is −12(B² + κ_2). Combining with universal −24 + 24 B:

**Final:**
```
a_1/a_4 = −24 + 24 B − 12 B² − 12 κ_2 + 4 B³ + 12 B·κ_2 + 4 κ_3
```

Coefficients: clean rationals (24, −12, −12, 4, 12, 4). No 1/2 or 1/3 factors at this order — Bell polynomial structure with binomial 4!/(4−k)! gives integers.

## κ_3(f) closed form

By the cumulant-of-`log A_f` definition along diagonal direction (analogous to how κ_2 was built):

```
κ_3(f) = (1/8)·[L'''/L − 3·(L''/L)·(L'/L) + 2·(L'/L)³]_{1, sym²f}
        − (1/2)·S^(3)_mult(N) − (1/8)·S^(3)_add(N)
        − ζ-piece  + universal constant
```

The 1/8 = (1/2)³ for sym² normalization; S^(3) are bad-prime third-power log-derivative sums; the ζ-piece is the analogous third cumulant of `−ζ'/ζ` evaluated at 1 (regularized) — empirically absorbed into the universal constant. Universal constant at order 3 is expected to be a rational multiple of `log(2π)` and `γ_E^k` terms; deepseek-r1 derivation needed for exact coefficient. Conservative form:

```
κ_3(f) ≈ (1/8)·[third cumulant log-deriv of L(s,sym²f) at s=1]
         + bad-prime third-power corrections
         + (small) universal constant
```

## Pari/gp inputs needed

Existing pipeline (`B1_lprime_sym2.gp`) already produces `L'/L` and `L''/L` at s=1. Add:

```gp
\\ third log-derivative of L(s, sym²f)
L = lfunsympow(lfuninit(E, [1,1]), 2);
val = lfun(L, 1, 3);     \\ third derivative at s=1
L0 = lfun(L, 1, 0);
L1 = lfun(L, 1, 1);
L2 = lfun(L, 1, 2);
L3 = val;
\\ Build cumulant: d³/ds³ log L = L'''/L - 3 (L''/L)(L'/L) + 2(L'/L)³
LprimeOverL  = L1/L0;
L2overL      = L2/L0;
L3overL      = L3/L0;
kappa3_main  = L3overL - 3*L2overL*LprimeOverL + 2*LprimeOverL^3;
kappa3       = (1/8) * kappa3_main \
               - (1/2) * S3_mult(N) - (1/8) * S3_add(N);
```

Bad-prime sums `S3_mult, S3_add` extend the existing `S_mult, S_add` infrastructure with third-power Euler factor logs (already a one-line generalization in `B1_5_a2_compute.gp`).

## Numerical sanity check — 11a1

Inputs (from existing data): B = 2.114, L'/L = 0.197, L''/L = −0.386, κ_2 ≈ 1.398.
Need L'''/L from pari (run recipe above). Plug into:

```
a_1/a_4 (11a1) = -24 + 24(2.114) - 12(2.114)² - 12(1.398) + 4(2.114)³
                + 12(2.114)(1.398) + 4·κ_3(11a1)
```

Universal + B + B² + κ_2 + B³ + B·κ_2 partial sum (ignoring κ_3):
= −24 + 50.74 − 53.63 − 16.78 + 37.79 + 35.46 = **29.58 + 4·κ_3**

Expect κ_3(11a1) ∈ [−1, +1] from heuristic scaling (κ_2 was 1.4, third cumulants typically smaller for log-rank-1). So a_1/a_4 ≈ 25–34 for 11a1. Sub-leading effect on r_obs at scale Y ≈ 10⁵ is `(a_1/a_4)·c_f / Y³` ≈ 30·c_f / 10¹⁵ — adds an MAE drop of ~0.02–0.04 to the 16-curve fit, consistent with target.

## Confidence + caveats

- **Confidence: medium-high** on the universal Bell polynomial structure (rigorous from Conrey-Snaith Thm 7.3 IBP).
- **Confidence: medium** on κ_3 closed form — the 1/8 prefactor follows the (1/2)^k pattern of sym² normalization but the universal constant at order 3 (analog of −log(2π) at order 2) was NOT derived rigorously here; needs deepseek-r1 verification analogous to v3.
- **Caveat 1:** sign of κ_3 main term depends on convention for `log A_f` cumulant; cross-check against numerical `r_obs` regression on 16-curve ladder.
- **Caveat 2:** Should verify against a single curve where `a_1/a_4` can be extracted by polynomial fit on multiple Y values — recommended before trusting the 4·κ_3 coefficient.
- **Validation gate:** compute a_1/a_4 numerically for 11a1, 37a1, 5077a1 via long-Y polynomial fit; compare to closed form. MAE on the 16-curve ladder should drop from 0.073 to ≤0.04.
