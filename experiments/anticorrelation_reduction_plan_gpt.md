# Anticorrelation Reduction Plan

This note converts the new scan into a concrete hybrid-proof target (finite exact checks + asymptotic analytical window).

## Core scan fact
- On scanned range, all `1399` primes with `p>=19` and `M(p)<=0` satisfy `C(p)<0`.
- Closest-to-zero point is `p=23`, `M=-2`, `C=-0.150502024922`.

## Exact base cases (already exact-rational)
| p | M(p) | C(p) exact | C(p) decimal |
|--:|--:|:--|--:|
| 19 | -3 | -1544259/1361360 | -1.134350208615 |
| 23 | -2 | -1911041/12697776 | -0.150502024922 |
| 29 | -2 | -3282893/564300 | -5.817637781322 |
| 31 | -4 | -133103604377/4436361072 | -30.002878985004 |
| 37 | -2 | -48776217793063/4011209802600 | -12.159976713621 |
| 41 | -1 | -88309431168347/40071985927974 | -2.203769768912 |

## Envelope after removing small primes
| lower bound p>=B | worst (closest to zero) p | M(p) | C(p) | C/p^2 |
|--:|--:|--:|--:|--:|
| 19 | 23 | -2 | -0.150502 | -0.000285 |
| 23 | 23 | -2 | -0.150502 | -0.000285 |
| 29 | 41 | -1 | -2.203770 | -0.001311 |
| 31 | 41 | -1 | -2.203770 | -0.001311 |
| 37 | 41 | -1 | -2.203770 | -0.001311 |
| 41 | 41 | -1 | -2.203770 | -0.001311 |
| 43 | 59 | -1 | -39.112291 | -0.011236 |
| 59 | 59 | -1 | -39.112291 | -0.011236 |
| 101 | 101 | 0 | -141.238357 | -0.013846 |
| 223 | 239 | -1 | -3980.084412 | -0.069678 |
| 500 | 541 | 0 | -20952.057795 | -0.071587 |
| 1000 | 1013 | 0 | -115518.377409 | -0.112572 |
| 2000 | 2017 | 0 | -590990.372101 | -0.145268 |
| 5000 | 5323 | -1 | -2721889.859132 | -0.096063 |
| 10000 | 14683 | 0 | -15133306.865298 | -0.070195 |
| 15000 | 15061 | 0 | -24879401.105211 | -0.109681 |

## Reduction candidate
- Candidate route: finite exact proof for `{19,23,29,31,37,41}` plus analytical proof on `p>=43`.
- In data, worst remaining case after `p>=43` is `p=59` with `C=-39.112291111285` (already far from 0).