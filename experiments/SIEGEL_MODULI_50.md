# Siegel-Modulus Scan up to q=50

Computed a Mobius sieve to 500,000 and used all 41,538 primes up to 500,000. The gamma scan used 2,000 points on [0.01, 3.00], and each quadratic character was evaluated by the prime sum

`F_chi(gamma) = |sum_(p <= 500000) chi(p) p^(-0.5 - i gamma)|`.

Runtime for the full sweep was 0.57 seconds. As a sieve sanity check, the linear Mobius sieve matched `sympy.mobius` on the first 20 values. The final Mertens value `M(500,000)` from the sieve is -6.

## Peak Summary

| q | peak_height | peak_gamma | z_score |
|---:|------------:|-----------:|--------:|
| 3 | 1.571512 | 0.010000 | 4.238248 |
| 5 | 2.258388 | 0.010000 | 2.851731 |
| 7 | 1.158162 | 0.010000 | 2.642763 |
| 11 | 1.197718 | 0.010000 | 0.319097 |
| 13 | 1.833443 | 0.010000 | 2.396520 |
| 17 | 1.505347 | 0.010000 | 2.230216 |
| 19 | 2.862025 | 1.499765 | 1.820948 |
| 23 | 1.383767 | 1.499765 | -0.220242 |
| 29 | 1.738299 | 0.010000 | 0.531755 |
| 31 | 1.056742 | 1.302326 | 0.135919 |
| 37 | 1.544007 | 0.010000 | 0.720618 |
| 41 | 1.223306 | 0.010000 | 0.082247 |
| 43 | 3.175207 | 0.902961 | 2.329617 |
| 47 | 1.842988 | 1.499765 | 0.724009 |

## Sensitivity Discussion

The weakest candidate in z-score terms is modulus `q=23`, with peak height `1.383767` at `gamma=1.499765` and z-score `-0.220242`. Over the full scan window its baseline mean and standard deviation are

- mean = 1.518774
- std = 0.612992

Using the heuristic `peak height ~ 1 / |1 - beta|` for a Siegel zero at `beta`, there are two natural scales:

- Matching the observed weakest peak gives `|1 - beta| ~ 1 / 1.383767 = 0.722665`.
- Requiring a conservative `3 sigma` excess over the weakest background means a detectable height of about `3.357750`, so `|1 - beta| <= 0.297818`.

The second number is the more conservative detectability threshold: with this prime range and this statistic, a Siegel-zero-style resonance would need to lie within roughly `0.297818` of 1 to rise `3 sigma` above the weakest character background.

## Conclusion

Across prime moduli `3 <= q <= 50`, the low-lying quadratic-character peaks are modest rather than explosive. On this finite dataset there is no sign of the huge `~1 / |1 - beta|` amplification one would expect from an extremely near-1 Siegel zero. Interpreting the weakest-character background conservatively, this scan would only be sensitive to a Siegel-zero-style effect if `|1 - beta|` were on the order of `0.297818` or smaller. Nothing in the present table suggests such an outlier.
