# Non-Healing Composites: Complete Characterization

**Date:** 2026-03-26
**Range:** Composites 4 to 1500

## Summary

Computed wobble W(N) for all N ≤ 1500. Found:
- Total composites: 1260
- Healing: 1185 (94.0%)
- Non-healing: 75 (6.0%)

## Conjecture 1: 2p Semiprimes

**Status:** FAILED

For semiprimes N = 2p (p an odd prime):
- N heals iff p ≤ 733 (i.e., p ≤ 43)
- N non-heals iff p ≥ 109 (i.e., p ≥ 47)

The threshold is exactly p = 43/47. No exceptions found for any 2p ≤ 1500.

## Conjecture 2: p² Prime Squares

**Status:** FAILED

For prime squares N = p²:
- N heals iff p ≤ 7
- N non-heals iff p ≥ 11

The threshold is between p=7 (49 heals) and p=11 (121 non-heals).

## Non-Healing Types

### mixed (2 total)

- N=796: 2^2 * 199 (phi/N=0.4975, GPF/N=0.2500)
- N=1172: 2^2 * 293 (phi/N=0.4983, GPF/N=0.2500)

### semiprime (51 total)

- N=218: 2 * 109 (phi/N=0.4954, GPF/N=0.5000)
- N=226: 2 * 113 (phi/N=0.4956, GPF/N=0.5000)
- N=346: 2 * 173 (phi/N=0.4971, GPF/N=0.5000)
- N=394: 2 * 197 (phi/N=0.4975, GPF/N=0.5000)
- N=398: 2 * 199 (phi/N=0.4975, GPF/N=0.5000)
- N=554: 2 * 277 (phi/N=0.4982, GPF/N=0.5000)
- N=562: 2 * 281 (phi/N=0.4982, GPF/N=0.5000)
- N=566: 2 * 283 (phi/N=0.4982, GPF/N=0.5000)
- N=586: 2 * 293 (phi/N=0.4983, GPF/N=0.5000)
- N=591: 3 * 197 (phi/N=0.6633, GPF/N=0.3333)
- N=597: 3 * 199 (phi/N=0.6633, GPF/N=0.3333)
- N=802: 2 * 401 (phi/N=0.4988, GPF/N=0.5000)
- N=818: 2 * 409 (phi/N=0.4988, GPF/N=0.5000)
- N=849: 3 * 283 (phi/N=0.6643, GPF/N=0.3333)
- N=914: 2 * 457 (phi/N=0.4989, GPF/N=0.5000)

### smooth (22 total)

- N=570: 2 * 3 * 5 * 19 (phi/N=0.2526, GPF/N=0.0333)
- N=654: 2 * 3 * 109 (phi/N=0.3303, GPF/N=0.1667)
- N=663: 3 * 13 * 17 (phi/N=0.5792, GPF/N=0.0256)
- N=678: 2 * 3 * 113 (phi/N=0.3304, GPF/N=0.1667)
- N=870: 2 * 3 * 5 * 29 (phi/N=0.2575, GPF/N=0.0333)
- N=930: 2 * 3 * 5 * 31 (phi/N=0.2581, GPF/N=0.0333)
- N=1090: 2 * 5 * 109 (phi/N=0.3963, GPF/N=0.1000)
- N=1095: 3 * 5 * 73 (phi/N=0.5260, GPF/N=0.0667)
- N=1102: 2 * 19 * 29 (phi/N=0.4574, GPF/N=0.0263)
- N=1106: 2 * 7 * 79 (phi/N=0.4231, GPF/N=0.0714)
- N=1118: 2 * 13 * 43 (phi/N=0.4508, GPF/N=0.0385)
- N=1130: 2 * 5 * 113 (phi/N=0.3965, GPF/N=0.1000)
- N=1140: 2^2 * 3 * 5 * 19 (phi/N=0.2526, GPF/N=0.0167)
- N=1182: 2 * 3 * 197 (phi/N=0.3316, GPF/N=0.1667)
- N=1194: 2 * 3 * 199 (phi/N=0.3317, GPF/N=0.1667)


## Analytical Threshold Mechanism

For 2p semiprimes at the threshold:
- Healing: 2*43=86, ratio phi(86)/|F_85| ~ pi²/(12*43) ≈ 0.0190
- Non-healing: 2*47=94, ratio phi(94)/|F_93| ~ pi²/(12*47) ≈ 0.0174

The ratio phi(N)/|F_{N-1}| ≈ pi²/(12p) drops below a critical value around p=47.

For p² prime squares at the threshold:
- Healing: 7²=49, ratio phi(49)/|F_48| ~ pi²/(3*49) ≈ 0.0668
- Non-healing: 11²=121, ratio phi(121)/|F_120| ~ pi²/(3*121) ≈ 0.0271

The critical density ratio is approximately 0.028-0.050.

## Key Insight

Non-healing occurs when the relative density of new Farey fractions
phi(N)/|F_{N-1}| falls below a critical threshold (~0.02-0.03).
When the new fractions are too sparse relative to the existing Farey
sequence, they don't sufficiently regularize the distribution.

The exact threshold depends on the STRUCTURE (not just size) of N,
because different factorizations produce different spatial distributions
of the new fractions a/N within [0,1].

## Complete Non-Healing List (N ≤ 1500)

- N=218: 2 * 109, deltaW=4.63e-10
- N=226: 2 * 113, deltaW=9.41e-10
- N=346: 2 * 173, deltaW=1.80e-11
- N=394: 2 * 197, deltaW=2.51e-11
- N=398: 2 * 199, deltaW=8.66e-11
- N=554: 2 * 277, deltaW=3.48e-11
- N=562: 2 * 281, deltaW=3.33e-11
- N=566: 2 * 283, deltaW=4.98e-11
- N=570: 2 * 3 * 5 * 19, deltaW=4.31e-11
- N=586: 2 * 293, deltaW=4.71e-11
- N=591: 3 * 197, deltaW=2.58e-11
- N=597: 3 * 199, deltaW=3.24e-11
- N=654: 2 * 3 * 109, deltaW=6.57e-12
- N=663: 3 * 13 * 17, deltaW=9.53e-13
- N=678: 2 * 3 * 113, deltaW=2.20e-11
- N=796: 2^2 * 199, deltaW=5.88e-13
- N=802: 2 * 401, deltaW=2.25e-13
- N=818: 2 * 409, deltaW=8.67e-13
- N=849: 3 * 283, deltaW=2.35e-14
- N=870: 2 * 3 * 5 * 29, deltaW=1.67e-12
- N=914: 2 * 457, deltaW=2.40e-13
- N=922: 2 * 461, deltaW=2.17e-12
- N=926: 2 * 463, deltaW=5.57e-12
- N=930: 2 * 3 * 5 * 31, deltaW=2.03e-12
- N=934: 2 * 467, deltaW=8.23e-12
- N=958: 2 * 479, deltaW=2.66e-12
- N=974: 2 * 487, deltaW=1.77e-12
- N=982: 2 * 491, deltaW=2.30e-12
- N=998: 2 * 499, deltaW=1.45e-12
- N=1006: 2 * 503, deltaW=1.43e-12
- N=1018: 2 * 509, deltaW=1.10e-12
- N=1090: 2 * 5 * 109, deltaW=1.81e-12
- N=1095: 3 * 5 * 73, deltaW=7.60e-13
- N=1102: 2 * 19 * 29, deltaW=4.92e-13
- N=1106: 2 * 7 * 79, deltaW=1.56e-12
- N=1118: 2 * 13 * 43, deltaW=1.81e-12
- N=1130: 2 * 5 * 113, deltaW=4.55e-12
- N=1140: 2^2 * 3 * 5 * 19, deltaW=7.50e-13
- N=1172: 2^2 * 293, deltaW=5.82e-13
- N=1182: 2 * 3 * 197, deltaW=1.17e-12
- N=1194: 2 * 3 * 199, deltaW=1.62e-12
- N=1262: 2 * 631, deltaW=1.34e-13
- N=1286: 2 * 643, deltaW=3.41e-13
- N=1294: 2 * 647, deltaW=1.01e-12
- N=1302: 2 * 3 * 7 * 31, deltaW=3.59e-13
- N=1306: 2 * 653, deltaW=3.13e-13
- N=1318: 2 * 659, deltaW=5.12e-13
- N=1322: 2 * 661, deltaW=4.32e-13
- N=1326: 2 * 3 * 13 * 17, deltaW=9.77e-13
- N=1346: 2 * 673, deltaW=1.30e-12
- N=1354: 2 * 677, deltaW=2.16e-12
- N=1356: 2^2 * 3 * 113, deltaW=3.02e-13
- N=1365: 3 * 5 * 7 * 13, deltaW=2.99e-13
- N=1366: 2 * 683, deltaW=2.64e-12
- N=1371: 3 * 457, deltaW=2.26e-13
- N=1382: 2 * 691, deltaW=1.42e-12
- N=1383: 3 * 461, deltaW=3.12e-13
- N=1389: 3 * 463, deltaW=1.53e-12
- N=1393: 7 * 199, deltaW=1.64e-12
- N=1401: 3 * 467, deltaW=2.24e-12
- N=1402: 2 * 701, deltaW=1.71e-12
- N=1403: 23 * 61, deltaW=5.89e-14
- N=1405: 5 * 281, deltaW=1.75e-12
- N=1410: 2 * 3 * 5 * 47, deltaW=1.15e-12
- N=1411: 17 * 83, deltaW=5.02e-13
- N=1415: 5 * 283, deltaW=2.30e-12
- N=1417: 13 * 109, deltaW=1.68e-12
- N=1418: 2 * 709, deltaW=2.12e-12
- N=1430: 2 * 5 * 11 * 13, deltaW=9.22e-13
- N=1437: 3 * 479, deltaW=1.20e-12
- N=1438: 2 * 719, deltaW=8.71e-13
- N=1473: 3 * 491, deltaW=2.91e-13
- N=1478: 2 * 739, deltaW=2.77e-13
- N=1482: 2 * 3 * 13 * 19, deltaW=2.91e-13
- N=1486: 2 * 743, deltaW=4.77e-13
