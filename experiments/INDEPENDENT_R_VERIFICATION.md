# Independent Verification: |R(p)| = O(log p / p)

**Date:** 2026-03-29
**Author:** Independent verification agent
**Claim under review:** |R(p)| = O(log p / p) -> 0 as p -> infinity

## Definitions

For prime p:
- F_{p-1} = Farey sequence of order p-1
- D(a/b) = rank(a/b in F_{p-1}) - |F_{p-1}| * (a/b)  [Farey displacement]
- delta(a/b) = (a - p*a mod b) / b  [multiplicative shift]
- C(p,b) = sum over a in (Z/bZ)* of D(a/b) * delta(a/b)
- V(b) = sum over a in (Z/bZ)* of delta(a/b)^2
- R(p) = sum_{b=2}^{p-1} C(p,b) / sum_{b=2}^{p-1} V(b)

## Results Table (Exact Fraction Arithmetic)

| p  | R(p) (float)     | |R(p)|       | |R|*p/log(p) | |R|*p       | |R|*sqrt(p) |
|----|------------------|-------------|-------------|------------|------------|
| 11 | -0.258852532497  | 0.258853    | 1.187449    | 2.847378   | 0.858517   |
| 13 | 0.059946910485   | 0.059947    | 0.303831    | 0.779310   | 0.216142   |
| 17 | -0.138625061513  | 0.138625    | 0.831786    | 2.356626   | 0.571566   |
| 19 | 0.165975980481   | 0.165976    | 1.071017    | 3.153544   | 0.723473   |
| 23 | 0.066249287150   | 0.066249    | 0.485963    | 1.523734   | 0.317720   |
| 29 | 0.214811679122   | 0.214812    | 1.850012    | 6.229539   | 1.156796   |
| 31 | 0.778001074987   | 0.778001    | 7.023332    | 24.118033  | 4.331727   |
| 37 | 0.210642590290   | 0.210643    | 2.158392    | 7.793776   | 1.281289   |
| 41 | 0.043818528796   | 0.043819    | 0.483782    | 1.796560   | 0.280575   |
| 43 | 0.676742011290   | 0.676742    | 7.736867    | 29.099906  | 4.437694   |
| 47 | 0.780823135946   | 0.780823    | 9.531761    | 36.698687  | 5.353054   |
| 53 | 0.699872656283   | 0.699873    | 9.342701    | 37.093251  | 5.095150   |
| 59 | 0.283699847989   | 0.283700    | 4.105000    | 16.738291  | 2.179140   |
| 61 | 0.631543704396   | 0.631544    | 9.371284    | 38.524166  | 4.932514   |
| 67 | 0.635260344935   | 0.635260    | 10.122605   | 42.562443  | 5.199830   |
| 71 | 0.908935586729   | 0.908936    | 15.139403   | 64.534427  | 7.658827   |
| 73 | 1.399105412397   | 1.399105    | 23.805072   | 102.134695 | 11.953962  |
| 79 | 1.281391874892   | 1.281392    | 23.167677   | 101.229958 | 11.389260  |
| 83 | 1.452502706010   | 1.452503    | 27.282660   | 120.557725 | 13.232929  |
| 89 | 0.986443362081   | 0.986443    | 19.559049   | 87.793459  | 9.306088   |
| 97 | -0.105428721411  | 0.105429    | 2.235461    | 10.226586  | 1.038352   |

## Analysis

### 1. Does |R(p)| -> 0?

**NO.** The values of |R(p)| do NOT decay to zero. They fluctuate wildly:
- |R(11)| = 0.259
- |R(73)| = 1.399
- |R(83)| = 1.453
- |R(97)| = 0.105

For p=73 and p=83, |R(p)| > 1. There is no visible decay trend.

### 2. Is |R(p)| = O(log p / p)?

**NO.** The ratio |R(p)| * p / log(p) is NOT bounded. It grows from ~1 at p=11 to ~27 at p=83:

- p=11: 1.19
- p=31: 7.02
- p=53: 9.34
- p=73: 23.81
- p=83: 27.28

The overall trend is clearly increasing, despite individual fluctuations. This is **inconsistent** with |R(p)| = O(log p / p).

Note: The script's automatic check reported "Appears BOUNDED" due to p=97 having an anomalously small |R(p)|. However, examining the full sequence shows clear growth.

### 3. Is |R(p)| = O(1/p)?

**NO.** The ratio |R(p)| * p grows from ~3 at p=11 to ~121 at p=83. Clearly unbounded.

### 4. Is |R(p)| = O(1/sqrt(p))?

**UNLIKELY.** The ratio |R(p)| * sqrt(p) grows from ~0.9 at p=11 to ~13.2 at p=83. This shows growth, ruling out O(1/sqrt(p)).

### 5. What IS the actual behavior?

The data suggests |R(p)| does NOT converge to zero at all. It appears to be O(1) or possibly even unbounded. Key observations:

- |R(p)| fluctuates between ~0.04 and ~1.45 in this range
- Several values exceed 1 (p=73: 1.40, p=83: 1.45)
- No clear decay pattern is visible
- The extreme fluctuations may be related to the arithmetic structure of specific primes

## Dedekind Sum Relation Check (p=13)

**Claim:** C(p,b) = sum_{d|b} mu(d) * s(p, b/d)

| b  | C(13,b) | Dedekind formula | Match? |
|----|---------|------------------|--------|
| 2  | 0       | 0                | YES    |
| 3  | 0       | 1/18             | NO     |
| 4  | 0       | 1/8              | NO     |
| 5  | -1/5    | 0                | NO     |
| 6  | 0       | 2/9              | NO     |
| 7  | 1/7     | -5/14            | NO     |
| 8  | 1/2     | -3/16            | NO     |
| 9  | 0       | -11/54           | NO     |
| 10 | 0       | 0                | YES    |
| 11 | -1/11   | 5/22             | NO     |
| 12 | 0       | 13/36            | NO     |

**RESULT:** The Dedekind sum relation does NOT hold. Only b=2 and b=10 match (both trivially zero for different reasons). The claimed identity C(p,b) = sum_{d|b} mu(d) * s(p, b/d) is FALSE for p=13.

## Verdict

### Claim: |R(p)| = O(log p / p)

**VERDICT: FALSE**

The evidence is unambiguous:
1. |R(p)| does not decay to zero over the tested range
2. |R(p)| * p / log(p) grows (reaching 27 by p=83), ruling out O(log p / p)
3. |R(p)| * p grows (reaching 121 by p=83), ruling out O(1/p)
4. |R(p)| * sqrt(p) grows (reaching 13 by p=83), ruling out O(1/sqrt(p))
5. The values actually GROW: |R(73)| = 1.40, |R(83)| = 1.45

The quantity R(p) appears to be O(1) at best, with no indication of decay to zero.

### Claim: Dedekind sum relation

**VERDICT: FALSE**

C(p,b) does not equal sum_{d|b} mu(d) * s(p, b/d) for p=13. The relation fails for 9 out of 11 values of b tested.

## Script Location

`~/Desktop/Farey-Local/experiments/independent_R_verification.py`

All computations used exact Fraction arithmetic (no floating point errors).
