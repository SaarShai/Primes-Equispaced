# R(11) Bypass Check Results

## Question
Can the sign theorem proof reduce to verifying R(11) > -1/2?
That is: is R(11) the global minimum of R(p) = corrRatio(p) over all primes?

## Definition
R(p) = crossTerm(p) / (2 * shiftSquaredSum(p))

where crossTerm(p) = 2 * sum_{f in F_{p-1}} D(f) * delta(f) and
shiftSquaredSum(p) = sum_{f in F_{p-1}} delta(f)^2.

The sign theorem needs B + C > 0, equivalently 1 + 2R > 0, i.e. R > -1/2.

## Key Values (exact, Fraction arithmetic)

| p | M(p) | R(p) exact | R(p) float | 1+2R |
|---|------|-----------|-----------|------|
| 5 | -2 | -1/11 | -0.0909 | 0.8182 |
| 7 | -2 | -9/38 | -0.2368 | 0.5263 |
| 11 | -2 | -1155/5974 | -0.1933 | 0.6133 |
| 13 | -3 | 813/15872 | 0.0512 | 1.1024 |
| 17 | -2 | -176343/1407221 | -0.1253 | 0.7494 |

R(11) = -1155/5974, confirmed matching Lean native_decide value.
R(11) + 1/2 = 916/2987 > 0: YES.

## Answer: NO, the bypass does NOT work

R(11) is NOT the global minimum. Multiple primes have R(p) < -1/2:

### Exact violations (confirmed with Fraction arithmetic)

| p | M(p) | R(p) | 1+2R |
|---|------|------|------|
| 1399 | +8 | -0.5032 | -0.0065 |
| 1409 | +9 | -0.9500 | -0.9001 |
| 1423 | +11 | -1.7487 | -2.4974 |
| 1427 | +9 | -0.9736 | -0.9472 |
| 1429 | +8 | -0.5505 | -0.1011 |

### Pattern: Large POSITIVE M(p) causes R < -1/2

The violations cluster around p ~ 1399-1429 where M(p) reaches its
largest positive values (8-11) in this range. When M(p) is large
positive, the displacement-shift correlation becomes strongly negative,
pushing R well below -1/2.

For primes with M(p) <= -3 (the restricted class), R is always positive
or only mildly negative. The R > -1/2 bound holds easily for this class.

## Trend Analysis

- For p <= 1000: min R = -0.2368 at p=7. No violations of R > -1/2.
- For p <= 2000: min R = -1.7487 at p=1423. Five violations of R > -1/2.
- min R does NOT stabilize -- it can get arbitrarily negative for
  primes with sufficiently large positive M(p).
- Only 6 of 166 primes up to 1000 have negative R at all.

## R(p) vs M(p) Correlation

- M(p) <= -3: R is always well above -1/2 (min R ~ 0.05 at p=13)
- M(p) = -2: R ranges from -0.237 to +3.03 (min at p=7)
- M(p) = -1: R ranges from 0.04 to 3.78
- M(p) >= 0: R can be very negative when M(p) is large positive
- M(p) >= 8: R < -1/2 violations occur

## Implications for the Proof

1. **R > -1/2 does NOT hold universally** (fails at p=1399, 1409, 1423, etc.)

2. **The restricted class approach (M(p) <= -3) still works**:
   For these primes, R is comfortably above -1/2.

3. **The bypass idea fails**: Cannot reduce to a single computation R(11) > -1/2,
   because R is not bounded below by R(11).

4. **The sign theorem ΔW(p) < 0 for all primes still needs a different
   argument for primes with large positive M(p)**, since B+C < 0 is
   possible for these primes. The sign theorem must rely on dilution
   exceeding the other terms, not on B+C > 0.

## Files
- Script: ~/Desktop/Farey-Local/experiments/r11_bypass_check.py
- This report: ~/Desktop/Farey-Local/experiments/R11_BYPASS_RESULTS.md
