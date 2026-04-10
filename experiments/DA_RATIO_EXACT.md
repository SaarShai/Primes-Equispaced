# D/A Ratio Exact Analysis

## Four-Term Decomposition

```
DW(p) = W(p-1) - W(p) = A - B - C - D

where:
  A = dilution        = old_D_sq * (1/n^2 - 1/n'^2)
  B = cross term      = (2/n'^2) * SUM D_old(f_j) * shift(f_j)
  C = shift-squared   = (1/n'^2) * SUM shift(f_j)^2
  D = new-frac discr  = (1/n'^2) * SUM D_{F_p}(k/p)^2

  n = |F_{p-1}|,  n' = |F_p| = n + p - 1
  D_old(f_j) = j - n*f_j        (old discrepancy, 0-indexed rank)
  shift(f_j) = floor(p*f_j) - (p-1)*f_j
             = a/b - (pa mod b)/b   for f_j = a/b
  D_{F_p}(k/p) = rank(k/p in F_p) - n'*(k/p)
```

All values computed with exact `Fraction` arithmetic (no floating-point errors).
93 primes, p in [5, 499].


## Key Finding 1: Exact Identities (Verified)

The following hold exactly (not approximately) for all primes in range:

1. **Four-term decomposition**: DW = A - B - C - D
2. **D/A identity**: 1 - D/A = (B + C + DW)/A = (B + C)/A + DW/A
3. **Zero-sum property**: SUM_{k=1}^{p-1} D_old_virtual(k/p) = 0
4. **D_raw decomposition**: D_raw = S_virt + 2*X_cross + S_kp
   where S_virt = SUM D_virt^2, X_cross = SUM D_virt*(k/p), S_kp = (p-1)(2p-1)/(6p)
5. **Sum invariance**: SUM D_{F_p}(k/p)^2 = SUM (D_virt(k/p) + k/p)^2
   (proven: holds because SUM D_{F_p}(k/p) = -(p-1)/2, making the shift by 1 cancel in L2)


## Key Finding 2: D/A Ratio Statistics

| Quantity | Value |
|----------|-------|
| D/A range | [0.560, 1.181] |
| D/A mean | 1.019 |
| D/A at p=5 | 0.560 (minimum) |
| D/A at p=19 | 1.181 (maximum) |
| |1-D/A| for p >= 100 | max 0.0515 |
| |1-D/A| for p >= 200 | max 0.0257 |
| |1-D/A| for p >= 400 | max 0.0200 |

**Observation**: D/A > 1 for 76/93 primes (D exceeds A, i.e., new-fraction variance exceeds dilution).

The 17 primes with D/A < 1 (D < A): {5, 7, 193, 223, 227, 241, 281, 313, 331, 347, 353, 397, 401, 409, 421, 439, 463}.


## Key Finding 3: Sign of DW

- DW < 0 (wobble decreases) for **91/93** primes
- DW >= 0 only for p = 5 and p = 7
- **All primes p >= 11** have DW < 0
- All M(p) <= -3 primes have DW < 0
- Even M(p) = 0 and M(p) = -1 primes (all 17) have DW < 0

**Bypass condition** (C + D > A, ensuring DW < 0 without needing B > 0):
- Holds for **91/93** primes (fails only for p = 5, 7)


## Key Finding 4: The 1 - D/A Formula

From the exact identity:
```
1 - D/A = (B + C + DW) / A
        = (B + C)/A + DW/A
```

The term (B + C)/A grows toward 1 as p increases (reaching ~1.2 at p=467).
The term DW/A is negative for p >= 11 and nearly cancels (B+C)/A.

**The near-unity of D/A is a consequence of massive cancellation between (B+C)/A and DW/A.**

| p | M(p) | (B+C)/A | DW/A | 1-D/A |
|---|------|---------|------|-------|
| 5 | -2 | 0.000 | +0.440 | +0.440 |
| 11 | -2 | 0.092 | -0.147 | -0.055 |
| 31 | -4 | 0.484 | -0.580 | -0.096 |
| 73 | -4 | 0.643 | -0.645 | -0.001 |
| 113 | -5 | 0.805 | -0.812 | -0.007 |
| 199 | -8 | 1.053 | -1.065 | -0.012 |
| 443 | -9 | 1.126 | -1.126 | -0.000 |
| 499 | -6 | 1.059 | -1.065 | -0.005 |


## Key Finding 5: Scaling of B/A and C/A

### C/A (shift-squared / dilution)

C/A converges to approximately **0.134** as p grows.

| p | C/A |
|---|-----|
| 41 | 0.182 |
| 101 | 0.155 |
| 251 | 0.137 |
| 401 | 0.134 |
| 499 | 0.134 |

This convergence to pi^4/(9*6) = pi^4/54 ~ 0.1797... is NOT exact.
The limiting value appears to be around 0.134.

### B/A (cross-term / dilution)

B/A does NOT scale simply with M(p)/p. Instead, B/A grows roughly toward 1
as p increases, with the growth rate depending on M(p):

| p | M(p) | B/A |
|---|------|-----|
| 31 | -4 | 0.294 |
| 73 | -4 | 0.474 |
| 113 | -5 | 0.656 |
| 199 | -8 | 0.920 |
| 443 | -9 | 0.993 |
| 499 | -6 | 0.925 |

**B/A is NOT proportional to M(p)/p**. The ratio B*p/(A*M) diverges with p.


## Key Finding 6: M(p) <= -3 Bounds

For the 45 primes with M(p) <= -3:
- All have DW < 0 (no exceptions)
- Maximum |1-D/A| = 0.181 (at p=19, M=-3)
- Maximum c where |1-D/A| <= c*|M(p)|/p is c = 2.88 (at p=431, M=-3)

**However, |1-D/A| is NOT bounded by c*|M(p)|/p for any fixed c.**
The ratio |1-D/A|*p/|M(p)| grows with p, reaching 2.88 at p=431.

What IS true: |1-D/A| is bounded and decreasing overall.
For M(p) <= -3 and p >= 100: max |1-D/A| = 0.052 (at p=107, M=-3).
For M(p) <= -3 and p >= 200: max |1-D/A| = 0.024 (at p=293, M=-8).


## Key Finding 7: The Relationship is NOT Simply M(p)-Dependent

The residual 1-D/A depends on the full structure of how p interacts with
F_{p-1}, not just through M(p). Primes with the same M(p) value can have
very different 1-D/A:

| p | M(p) | 1-D/A |
|---|------|-------|
| 73 | -4 | -0.0015 |
| 313 | -4 | +0.0005 |
| 317 | -4 | -0.0195 |
| 433 | -4 | -0.0028 |

This variation within fixed M(p) shows that 1-D/A encodes more arithmetic
information than M(p) alone.


## Detailed Data Table

| p | M(p) | A | B | C | D | DW | D/A | 1-D/A |
|---|------|---|---|---|---|----|----|-------|
| 5 | -2 | 0.0295159 | -0.0018365 | 0.0018365 | 0.0165289 | +0.0129870 | 0.5600 | +0.4400 |
| 7 | -2 | 0.0157966 | -0.0024931 | 0.0024931 | 0.0130590 | +0.0027376 | 0.8267 | +0.1733 |
| 11 | -2 | 0.0083457 | -0.0008263 | 0.0015960 | 0.0088008 | -0.0012249 | 1.0545 | -0.0545 |
| 13 | -3 | 0.0066145 | 0.0002022 | 0.0016866 | 0.0073807 | -0.0026551 | 1.1158 | -0.1158 |
| 19 | -3 | 0.0043185 | 0.0002916 | 0.0008783 | 0.0051010 | -0.0019524 | 1.1812 | -0.1812 |
| 31 | -4 | 0.0022052 | 0.0006494 | 0.0004174 | 0.0024166 | -0.0012782 | 1.0959 | -0.0959 |
| 73 | -4 | 0.0005586 | 0.0002647 | 0.0000946 | 0.0005594 | -0.0003602 | 1.0015 | -0.0015 |
| 113 | -5 | 0.0002666 | 0.0001749 | 0.0000396 | 0.0002684 | -0.0002164 | 1.0070 | -0.0070 |
| 199 | -8 | 0.0001034 | 0.0001089 | 0.0000138 | 0.0001046 | -0.0001215 | 1.0117 | -0.0117 |
| 293 | -8 | 0.0000463 | 0.0000493 | 0.0000061 | 0.0000474 | -0.0000565 | 1.0236 | -0.0236 |
| 443 | -9 | 0.0000218 | 0.0000245 | 0.0000029 | 0.0000219 | -0.0000276 | 1.0002 | -0.0002 |
| 499 | -6 | 0.0000159 | 0.0000147 | 0.0000021 | 0.0000167 | -0.0000176 | 1.0052 | -0.0052 |


## Summary of Main Results

1. The four-term decomposition DW = A - B - C - D is exact (verified with Fraction arithmetic).

2. D/A is close to 1, with |1-D/A| < 0.052 for all p >= 100. The exact identity is
   1 - D/A = (B + C + DW)/A, where (B+C)/A and DW/A nearly cancel.

3. DW < 0 for all primes p >= 11 (91/93 in range). Only p=5 and p=7 have DW >= 0.

4. The bypass condition C + D > A holds for all p >= 11, meaning even without
   the cross term B, new-fraction effects dominate dilution.

5. For M(p) <= -3: DW < 0 always. The maximum |1-D/A| is 0.181 (at p=19).

6. The relationship between 1-D/A and M(p) is NOT simply proportional.
   1-D/A encodes detailed arithmetic beyond M(p) alone. No clean formula
   1-D/A = f(M(p), p) with a simple f was found.

7. The key structural identity: 1-D/A reflects the balance between
   how cross-correlations (B) and shift variance (C) compare to
   the wobble change (DW) relative to dilution (A).


---
*Generated by DA_ratio_exact_analysis.py, 93 primes, p in [5, 499]*
*All computations use exact Python Fraction arithmetic (no floating-point rounding)*
