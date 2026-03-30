# Five-Block Mertens Analysis: M(p)=-3 Primes up to 50,000

**Date:** 2026-03-30
**Status:** COMPLETED -- Results are NEGATIVE for the five-block approach

## Setup

For each prime p with M(p)=-3, compute:
- M(floor(p/j)) for j = 2, 3, 4, 5, 6
- S = M(p/3) + M(p/4) + M(p/5) + M(p/6)
- T = M(p/2) + M(p/3) + M(p/4) + M(p/5) + M(p/6) (full five-block sum)

**Goal:** Check if S <= -2 always holds for p >= 43. If yes, combined with kernel bound, Term2 < 0 closes analytically.

## Key Result: S <= -2 FAILS

**The five-block sum S = M(p/3)+M(p/4)+M(p/5)+M(p/6) does NOT stay <= -2.**

### Summary Statistics (p >= 43, 143 primes total)

| Metric | Value |
|--------|-------|
| S <= -2 | 100/143 (69.9%) |
| S > 0 | 35/143 (24.5%) |
| max(S) | **25** at p=36307 |
| min(S) | -77 |

### Distribution of S (p >= 43)

| S range | Count |
|---------|-------|
| S <= -10 | 27 |
| -10 < S <= -5 | 37 |
| -5 < S <= -2 | 8 |
| S = -1 | 5 |
| S = 0 | 3 |
| S = 1 to 3 | 7 |
| S = 5 to 9 | 13 |
| S >= 15 | 5 |

### Worst Failures (S >> 0)

| p | M(p/2) | M(p/3) | M(p/4) | M(p/5) | M(p/6) | S | T=M2+S |
|---|--------|--------|--------|--------|--------|---|--------|
| 36307 | -17 | 17 | 0 | 2 | 6 | **25** | 8 |
| 36341 | -15 | 15 | 2 | 5 | 3 | **25** | 10 |
| 36389 | -13 | 14 | 2 | 9 | 0 | **25** | 12 |
| 36683 | -22 | 20 | 3 | 5 | -3 | **25** | 3 |
| 45569 | -25 | 9 | 15 | 3 | -3 | **24** | -1 |
| 45631 | -22 | 8 | 11 | 7 | -3 | **23** | 1 |
| 36781 | -22 | 18 | 1 | 6 | -2 | **23** | 1 |
| 13441 | -17 | -4 | 16 | 1 | 8 | **21** | 4 |
| 13399 | -15 | -11 | 16 | 4 | 11 | **20** | 5 |

The pattern: around p ~ 36000-36700, M(p/3) shoots up to 15-20, dragging S positive.

## Two-Block Check: M(p/2) <= -2

| Metric | Value |
|--------|-------|
| M(p/2) <= -2 | 73/145 (50.3%) |
| First failure | p=13 (M(6)=-1) |

Two-block fails at about half the primes. This was already known (p=131 counterexample).

## Full Five-Block Sum T = M(p/2)+S

Including M(p/2) helps significantly (it is usually large and negative):

| Metric | Value |
|--------|-------|
| T <= -2 | 118/143 (82.5%) |
| T > 0 | 19/143 (13.3%) |
| max(T) | **13** at p=41143 |

Still fails. T reaches +13, so even the full five-block sum does not stay negative.

## How Many of {M(p/3), ..., M(p/6)} are <= -1? (p >= 43)

| Count <= -1 | # Primes |
|-------------|----------|
| 0 of 4 | 5 |
| 1 of 4 | 15 |
| 2 of 4 | 36 |
| 3 of 4 | 48 |
| 4 of 4 | 39 |

Only 27% of primes have all four blocks negative. In 14% of cases, at most one is negative.

## Conclusion

**The five-block approach does NOT close Term2 < 0 analytically.** Specifically:

1. S = M(p/3)+M(p/4)+M(p/5)+M(p/6) reaches as high as +25, far exceeding the -2 threshold needed.
2. Even the full sum T including M(p/2) reaches +13.
3. The failures cluster around specific ranges (p ~ 36000-36700) where M(n) has large positive excursions near n ~ 12000.
4. The two-block assumption M(p/2) <= -2 fails at ~50% of primes, confirming known issues.

**What this means:** Any approach that relies on individual M(p/j) values being uniformly bounded below will fail, because the Mertens function has significant positive excursions. A proof strategy must either:
- Use cancellation between terms (some positive, some negative)
- Incorporate the kernel weights (1/j contributions are smaller for larger j)
- Work with averaged/smoothed quantities rather than pointwise bounds
- Find a completely different decomposition

## Raw Data

Full CSV at: /tmp/five_block_data.csv (145 rows with all values)
