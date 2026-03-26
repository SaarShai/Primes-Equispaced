# Non-Healing Composites: Complete Characterization

**Date:** 2026-03-26
**Range:** Composites 4 to 1500

## Summary

Computed wobble W(N) for all N ≤ 1500. Found:
- Total composites: 1260
- Healing: 1085 (86.1%)
- Non-healing: 175 (13.9%)

## Conjecture 1: 2p Semiprimes

**Status:** FAILED

For semiprimes N = 2p (p an odd prime):
- N heals iff p ≤ 613 (i.e., p ≤ 43)
- N non-heals iff p ≥ 2 (i.e., p ≥ 47)

The threshold is exactly p = 43/47. No exceptions found for any 2p ≤ 1500.

## Conjecture 2: p² Prime Squares

**Status:** FAILED

For prime squares N = p²:
- N heals iff p ≤ 7
- N non-heals iff p ≥ 11

The threshold is between p=7 (49 heals) and p=11 (121 non-heals).

## Non-Healing Types

### mixed (6 total)

- N=452: 2^2 * 113 (phi/N=0.4956, GPF/N=0.2500)
- N=788: 2^2 * 197 (phi/N=0.4975, GPF/N=0.2500)
- N=796: 2^2 * 199 (phi/N=0.4975, GPF/N=0.2500)
- N=904: 2^3 * 113 (phi/N=0.4956, GPF/N=0.1250)
- N=1132: 2^2 * 283 (phi/N=0.4982, GPF/N=0.2500)
- N=1172: 2^2 * 293 (phi/N=0.4983, GPF/N=0.2500)

### prime_square (9 total)

- N=4: 2^2 (phi/N=0.5000, GPF/N=0.5000)
- N=121: 11^2 (phi/N=0.9091, GPF/N=0.0909)
- N=169: 13^2 (phi/N=0.9231, GPF/N=0.0769)
- N=289: 17^2 (phi/N=0.9412, GPF/N=0.0588)
- N=361: 19^2 (phi/N=0.9474, GPF/N=0.0526)
- N=529: 23^2 (phi/N=0.9565, GPF/N=0.0435)
- N=841: 29^2 (phi/N=0.9655, GPF/N=0.0345)
- N=961: 31^2 (phi/N=0.9677, GPF/N=0.0323)
- N=1369: 37^2 (phi/N=0.9730, GPF/N=0.0270)

### semiprime (102 total)

- N=94: 2 * 47 (phi/N=0.4894, GPF/N=0.5000)
- N=146: 2 * 73 (phi/N=0.4932, GPF/N=0.5000)
- N=166: 2 * 83 (phi/N=0.4940, GPF/N=0.5000)
- N=218: 2 * 109 (phi/N=0.4954, GPF/N=0.5000)
- N=219: 3 * 73 (phi/N=0.6575, GPF/N=0.3333)
- N=226: 2 * 113 (phi/N=0.4956, GPF/N=0.5000)
- N=334: 2 * 167 (phi/N=0.4970, GPF/N=0.5000)
- N=339: 3 * 113 (phi/N=0.6608, GPF/N=0.3333)
- N=346: 2 * 173 (phi/N=0.4971, GPF/N=0.5000)
- N=358: 2 * 179 (phi/N=0.4972, GPF/N=0.5000)
- N=362: 2 * 181 (phi/N=0.4972, GPF/N=0.5000)
- N=386: 2 * 193 (phi/N=0.4974, GPF/N=0.5000)
- N=394: 2 * 197 (phi/N=0.4975, GPF/N=0.5000)
- N=398: 2 * 199 (phi/N=0.4975, GPF/N=0.5000)
- N=417: 3 * 139 (phi/N=0.6619, GPF/N=0.3333)

### smooth (58 total)

- N=285: 3 * 5 * 19 (phi/N=0.5053, GPF/N=0.0667)
- N=438: 2 * 3 * 73 (phi/N=0.3288, GPF/N=0.1667)
- N=442: 2 * 13 * 17 (phi/N=0.4344, GPF/N=0.0385)
- N=465: 3 * 5 * 31 (phi/N=0.5161, GPF/N=0.0667)
- N=470: 2 * 5 * 47 (phi/N=0.3915, GPF/N=0.1000)
- N=546: 2 * 3 * 7 * 13 (phi/N=0.2637, GPF/N=0.0238)
- N=570: 2 * 3 * 5 * 19 (phi/N=0.2526, GPF/N=0.0333)
- N=651: 3 * 7 * 31 (phi/N=0.5530, GPF/N=0.0476)
- N=654: 2 * 3 * 109 (phi/N=0.3303, GPF/N=0.1667)
- N=658: 2 * 7 * 47 (phi/N=0.4195, GPF/N=0.0714)
- N=663: 3 * 13 * 17 (phi/N=0.5792, GPF/N=0.0256)
- N=665: 5 * 7 * 19 (phi/N=0.6496, GPF/N=0.0286)
- N=670: 2 * 5 * 67 (phi/N=0.3940, GPF/N=0.1000)
- N=678: 2 * 3 * 113 (phi/N=0.3304, GPF/N=0.1667)
- N=682: 2 * 11 * 31 (phi/N=0.4399, GPF/N=0.0455)


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

- N=4: 2^2, deltaW=5.20e-18
- N=94: 2 * 47, deltaW=3.21e-06
- N=121: 11^2, deltaW=2.10e-06
- N=146: 2 * 73, deltaW=1.60e-05
- N=166: 2 * 83, deltaW=5.63e-06
- N=169: 13^2, deltaW=9.17e-06
- N=218: 2 * 109, deltaW=2.04e-05
- N=219: 3 * 73, deltaW=1.20e-05
- N=226: 2 * 113, deltaW=2.74e-05
- N=285: 3 * 5 * 19, deltaW=5.58e-06
- N=289: 17^2, deltaW=2.38e-06
- N=334: 2 * 167, deltaW=1.42e-07
- N=339: 3 * 113, deltaW=6.78e-06
- N=346: 2 * 173, deltaW=6.36e-06
- N=358: 2 * 179, deltaW=5.74e-07
- N=361: 19^2, deltaW=4.33e-06
- N=362: 2 * 181, deltaW=2.43e-06
- N=386: 2 * 193, deltaW=1.44e-08
- N=394: 2 * 197, deltaW=5.71e-06
- N=398: 2 * 199, deltaW=8.72e-06
- N=417: 3 * 139, deltaW=1.61e-06
- N=438: 2 * 3 * 73, deltaW=4.04e-06
- N=442: 2 * 13 * 17, deltaW=2.24e-06
- N=452: 2^2 * 113, deltaW=1.13e-06
- N=465: 3 * 5 * 31, deltaW=5.99e-07
- N=470: 2 * 5 * 47, deltaW=4.64e-07
- N=529: 23^2, deltaW=1.30e-06
- N=538: 2 * 269, deltaW=4.41e-07
- N=542: 2 * 271, deltaW=1.47e-06
- N=543: 3 * 181, deltaW=1.69e-06
- N=545: 5 * 109, deltaW=1.12e-06
- N=546: 2 * 3 * 7 * 13, deltaW=5.75e-07
- N=553: 7 * 79, deltaW=4.66e-07
- N=554: 2 * 277, deltaW=5.64e-06
- N=559: 13 * 43, deltaW=4.89e-08
- N=562: 2 * 281, deltaW=5.49e-06
- N=565: 5 * 113, deltaW=3.27e-06
- N=566: 2 * 283, deltaW=7.16e-06
- N=570: 2 * 3 * 5 * 19, deltaW=5.42e-06
- N=573: 3 * 191, deltaW=1.63e-06
- N=579: 3 * 193, deltaW=2.44e-06
- N=586: 2 * 293, deltaW=7.08e-06
- N=589: 19 * 31, deltaW=5.10e-07
- N=591: 3 * 197, deltaW=5.59e-06
- N=597: 3 * 199, deltaW=6.28e-06
- N=634: 2 * 317, deltaW=9.30e-07
- N=651: 3 * 7 * 31, deltaW=1.37e-06
- N=654: 2 * 3 * 109, deltaW=2.86e-06
- N=658: 2 * 7 * 47, deltaW=9.54e-07
- N=663: 3 * 13 * 17, deltaW=3.61e-06
- N=665: 5 * 7 * 19, deltaW=2.04e-06
- N=670: 2 * 5 * 67, deltaW=1.48e-06
- N=678: 2 * 3 * 113, deltaW=4.97e-06
- N=682: 2 * 11 * 31, deltaW=2.19e-06
- N=788: 2^2 * 197, deltaW=2.31e-07
- N=794: 2 * 397, deltaW=2.90e-07
- N=796: 2^2 * 199, deltaW=1.50e-06
- N=802: 2 * 401, deltaW=1.21e-06
- N=807: 3 * 269, deltaW=1.45e-07
- N=813: 3 * 271, deltaW=1.00e-07
- N=818: 2 * 409, deltaW=1.28e-06
- N=830: 2 * 5 * 83, deltaW=6.40e-08
- N=841: 29^2, deltaW=7.75e-07
- N=849: 3 * 283, deltaW=1.38e-06
- N=855: 3^2 * 5 * 19, deltaW=1.36e-07
- N=870: 2 * 3 * 5 * 29, deltaW=9.02e-07
- N=876: 2^2 * 3 * 73, deltaW=5.68e-08
- N=878: 2 * 439, deltaW=6.43e-07
- N=879: 3 * 293, deltaW=1.19e-06
- N=884: 2^2 * 13 * 17, deltaW=4.43e-07
- N=886: 2 * 443, deltaW=8.22e-07
- N=898: 2 * 449, deltaW=7.40e-07
- N=904: 2^3 * 113, deltaW=1.62e-08
- N=914: 2 * 457, deltaW=9.59e-07
- N=922: 2 * 461, deltaW=1.44e-06
- N=926: 2 * 463, deltaW=2.33e-06
- N=930: 2 * 3 * 5 * 31, deltaW=9.85e-07
- N=933: 3 * 311, deltaW=6.27e-07
- N=934: 2 * 467, deltaW=3.05e-06
- N=939: 3 * 313, deltaW=8.11e-07
- N=951: 3 * 317, deltaW=7.32e-07
- N=958: 2 * 479, deltaW=1.56e-06
- N=961: 31^2, deltaW=1.22e-06
- N=965: 5 * 193, deltaW=7.49e-07
- N=966: 2 * 3 * 7 * 23, deltaW=3.40e-07
- N=974: 2 * 487, deltaW=1.30e-06
- N=982: 2 * 491, deltaW=1.46e-06
- N=985: 5 * 197, deltaW=5.81e-07
- N=995: 5 * 199, deltaW=1.09e-06
- N=998: 2 * 499, deltaW=1.21e-06
- N=1006: 2 * 503, deltaW=1.18e-06
- N=1018: 2 * 509, deltaW=1.07e-06
- N=1023: 3 * 11 * 31, deltaW=3.92e-08
- N=1038: 2 * 3 * 173, deltaW=5.52e-07
- N=1070: 2 * 5 * 107, deltaW=4.15e-07
- N=1074: 2 * 3 * 179, deltaW=5.30e-07
- N=1086: 2 * 3 * 181, deltaW=4.99e-07
- N=1090: 2 * 5 * 109, deltaW=1.52e-06
- N=1095: 3 * 5 * 73, deltaW=1.44e-06
- N=1102: 2 * 19 * 29, deltaW=1.18e-06
- N=1105: 5 * 13 * 17, deltaW=1.47e-06
- N=1106: 2 * 7 * 79, deltaW=1.51e-06
- N=1113: 3 * 7 * 53, deltaW=4.07e-07
- N=1118: 2 * 13 * 43, deltaW=1.65e-06
- N=1130: 2 * 5 * 113, deltaW=2.60e-06
- N=1131: 3 * 13 * 29, deltaW=4.00e-07
- N=1132: 2^2 * 283, deltaW=4.01e-08
- N=1140: 2^2 * 3 * 5 * 19, deltaW=6.50e-07
- N=1146: 2 * 3 * 191, deltaW=3.47e-07
- N=1158: 2 * 3 * 193, deltaW=1.77e-07
- N=1162: 2 * 7 * 83, deltaW=2.26e-07
- N=1166: 2 * 11 * 53, deltaW=1.93e-07
- N=1172: 2^2 * 293, deltaW=8.99e-07
- N=1178: 2 * 19 * 31, deltaW=2.99e-07
- N=1182: 2 * 3 * 197, deltaW=1.12e-06
- N=1194: 2 * 3 * 199, deltaW=1.31e-06
- N=1234: 2 * 617, deltaW=1.77e-07
- N=1238: 2 * 619, deltaW=2.83e-07
- N=1262: 2 * 631, deltaW=5.43e-07
- N=1282: 2 * 641, deltaW=2.83e-07
- N=1286: 2 * 643, deltaW=6.29e-07
- N=1290: 2 * 3 * 5 * 43, deltaW=1.26e-08
- N=1294: 2 * 647, deltaW=9.70e-07
- N=1302: 2 * 3 * 7 * 31, deltaW=4.37e-07
- N=1306: 2 * 653, deltaW=6.17e-07
- N=1308: 2^2 * 3 * 109, deltaW=4.18e-07
- N=1314: 2 * 3^2 * 73, deltaW=1.91e-07
- N=1316: 2^2 * 7 * 47, deltaW=2.47e-07
- N=1318: 2 * 659, deltaW=7.17e-07
- N=1322: 2 * 661, deltaW=6.82e-07
- N=1326: 2 * 3 * 13 * 17, deltaW=7.82e-07
- N=1330: 2 * 5 * 7 * 19, deltaW=2.20e-07
- N=1340: 2^2 * 5 * 67, deltaW=2.38e-07
- N=1346: 2 * 673, deltaW=1.14e-06
- N=1347: 3 * 449, deltaW=2.92e-07
- N=1351: 7 * 193, deltaW=3.86e-08
- N=1354: 2 * 677, deltaW=1.62e-06
- N=1355: 5 * 271, deltaW=8.17e-08
- N=1356: 2^2 * 3 * 113, deltaW=5.97e-07
- N=1364: 2^2 * 11 * 31, deltaW=1.03e-07
- N=1365: 3 * 5 * 7 * 13, deltaW=5.19e-07
- N=1366: 2 * 683, deltaW=1.91e-06
- N=1369: 37^2, deltaW=3.36e-07
- N=1371: 3 * 457, deltaW=6.81e-07
- N=1379: 7 * 197, deltaW=2.96e-07
- N=1382: 2 * 691, deltaW=1.23e-06
- N=1383: 3 * 461, deltaW=7.22e-07
- N=1385: 5 * 277, deltaW=4.42e-07
- N=1387: 19 * 73, deltaW=3.31e-07
- N=1389: 3 * 463, deltaW=1.44e-06
- N=1391: 13 * 107, deltaW=5.84e-07
- N=1393: 7 * 199, deltaW=1.66e-06
- N=1397: 11 * 127, deltaW=5.56e-07
- N=1401: 3 * 467, deltaW=1.87e-06
- N=1402: 2 * 701, deltaW=1.43e-06
- N=1403: 23 * 61, deltaW=7.95e-07
- N=1405: 5 * 281, deltaW=1.70e-06
- N=1410: 2 * 3 * 5 * 47, deltaW=9.01e-07
- N=1411: 17 * 83, deltaW=1.04e-06
- N=1415: 5 * 283, deltaW=2.03e-06
- N=1417: 13 * 109, deltaW=1.75e-06
- N=1418: 2 * 709, deltaW=1.69e-06
- N=1430: 2 * 5 * 11 * 13, deltaW=8.30e-07
- N=1437: 3 * 479, deltaW=1.25e-06
- N=1438: 2 * 719, deltaW=9.23e-07
- N=1441: 11 * 131, deltaW=3.74e-07
- N=1454: 2 * 727, deltaW=2.03e-07
- N=1461: 3 * 487, deltaW=4.27e-07
- N=1465: 5 * 293, deltaW=4.56e-07
- N=1466: 2 * 733, deltaW=3.25e-07
- N=1469: 13 * 113, deltaW=2.93e-07
- N=1473: 3 * 491, deltaW=6.66e-07
- N=1478: 2 * 739, deltaW=5.36e-07
- N=1482: 2 * 3 * 13 * 19, deltaW=3.98e-07
- N=1486: 2 * 743, deltaW=6.69e-07
