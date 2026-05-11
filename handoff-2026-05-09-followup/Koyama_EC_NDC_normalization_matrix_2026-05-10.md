# Koyama EC-NDC normalization matrix 2026-05-10

Scope: Agent B EC-NDC normalization matrix. Data sources only:

- `Koyama_EC_NDC.csv`
- `Koyama_EC_NDC_ap_table.csv`

Output matrix: `Koyama_EC_NDC_normalization_matrix_2026-05-10.csv`

## Method

Ranks were inferred only from the source `scale_label` column:

| curve | rank source | rank |
|---|---:|---:|
| 11a1 | `c_K (constant)` | 0 |
| 37a1 | `c_K / log K` | 1 |
| 389a1 | `c_K / (log K)²` | 2 |

Partial `L(2,E)` was computed from the 100 available prime rows, through `p=541`, using EC Euler factors at `s=2`:

- good reduction: `(1 - a_p/p^2 + 1/p^3)^-1`
- bad reduction: `(1 - a_p/p^2)^-1`

Computed partial `L(2,E)` estimates:

| curve | rank | bad prime in table | L2E_estimate |
|---|---:|---:|---:|
| 37a1 | 1 | 37 | 0.381702621298426499358925 |
| 11a1 | 0 | 11 | 0.545915496934310807456615 |
| 389a1 | 2 | 389 | 0.360336000925056599990789 |

The CSV includes 105 rows: 15 source `curve,K` rows times 7 normalization rows. Source columns are preserved, with appended `rank`, `normalization_name`, `normalized_value`, and `L2E_estimate`.

## Normalizations Tested

- `D`
- `D*zeta(2)`
- `D*exp(rank*EulerGamma)`
- `D/L2E_partial^rank`
- `D*zeta(2)/L2E_partial^rank`
- `D/Sym2_good_partial^rank`
- `D*zeta(2)/Sym2_good_partial^rank`

Sym2 status: only the good-prime partial placeholder is computed from the existing `a_p` table. Full Sym2 bad local factors are not present in the allowed sources, so full Sym2 normalization remains `DEFER`; the CSV marks those rows with `COMPUTED_GOOD_PRIME_PLACEHOLDER_FULL_SYM2_DEFER`.

## Stability Summary

Score used for screening: `max within-curve K CV + cross-curve mean CV`. Lower is better. No normalization is promoted: the best candidates still vary across all three curves by cross-curve ratio `1.42083`, and max within-curve K CV is `0.08567`.

| rank | normalization | score | max within-K CV | cross-curve CV | curve means (37a1, 11a1, 389a1) |
|---:|---|---:|---:|---:|---|
| 1 | `D/L2E_partial^rank` | 0.22741084 | 0.08567129 | 0.14173955 | 0.99504837, 0.70033092, 0.89548497 |
| 2 | `D*zeta(2)/L2E_partial^rank` | 0.22741084 | 0.08567129 | 0.14173955 | 1.63678897, 1.15199819, 1.47301374 |
| 3 | `D*exp(rank*EulerGamma)` | 0.34510250 | 0.08567129 | 0.25943121 | 0.67647370, 0.70033092, 0.36883894 |
| 4 | `D` | 0.68450808 | 0.08567129 | 0.59883679 | 0.37981257, 0.70033092, 0.11627159 |
| 5 | `D*zeta(2)` | 0.68450808 | 0.08567129 | 0.59883679 | 0.62476664, 1.15199819, 0.19125910 |
| 6 | `D/Sym2_good_partial^rank` | 1.11853593 | 0.08567129 | 1.03286464 | 0.15174873, 0.70033092, 0.01135888 |
| 7 | `D*zeta(2)/Sym2_good_partial^rank` | 1.11853593 | 0.08567129 | 1.03286464 | 0.24961666, 1.15199819, 0.01868460 |

## Promotion Decision

No normalization promoted. Best two candidates are the `L2E_partial^rank` pair above, but they are scalar multiples and not stable enough across all three curves under the promotion rule.
