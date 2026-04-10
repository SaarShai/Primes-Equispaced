# C_W >= 1/4 Formalization in Lean 4

## Theorem Statement

For the Farey sequence F_N with n = |F_N|:
```
  sum_{f in F_N} D(f)^2 >= n/4
```
where D(f) = rank(f) - n*f is the displacement.

In Lean 4 terms: `wobbleNumerator N >= (fareySet N).card / 4` for all N >= 1.

## Proof Strategy (3 steps)

1. **Displacement sum identity:** sum D = -n/2
   - Farey symmetry: sum f = n/2 (involution f <-> 1-f)
   - Rank sum: sum rank(f) = n(n-1)/2 (ranks are a permutation of {0,...,n-1})
   - Combining: sum D = n(n-1)/2 - n*(n/2) = -n/2

2. **Cauchy-Schwarz:** (sum D)^2 <= n * sum D^2

3. **Combine:** n^2/4 <= n * sum D^2, hence sum D^2 >= n/4

## Files Created

### `RequestProject/AbstractCauchySchwarz.lean` -- FULLY PROVEN (0 sorry)

Abstract Cauchy-Schwarz bound: if sum a_i = -|s|/2 then sum a_i^2 >= |s|/4.

Uses Mathlib's `sq_sum_le_card_mul_sum_sq` (from `Mathlib.Algebra.Order.Chebyshev`).

**Status: Compiles cleanly, no sorry.**

### `RequestProject/CWBound.lean` -- 3 sorry remaining

Main theorem `cw_bound` proven modulo 3 lemmas:

| Lemma | Status | Difficulty |
|-------|--------|------------|
| `rank_sum` | sorry | Hard (needs injective rank -> permutation argument) |
| `farey_sum_symmetry` | sorry | Medium (needs Finset.sum_involution with (a,b)->(b-a,b)) |
| `displacement_sum_eq` | sorry | Easy once rank_sum + farey_sum_symmetry done (algebra) |
| `sum_sq_ge_quarter_of_sum_eq_neg_half` | PROVEN | Done via sq_sum_le_card_mul_sum_sq |
| `cw_bound` | PROVEN (modulo sorry lemmas) | Applies abstract CS to displacement_sum_eq |
| `cw_bound_1/2/3/5` | PROVEN (native_decide) | Computational verification for N=1,2,3,5 |

## Aristotle Submissions

| ID | Target | Status | Result |
|----|--------|--------|--------|
| `0cce1dcf` | All lemmas in CWBound.lean | IN_PROGRESS (12%) | Pending |
| `8c1bcdb7` | farey_sum_symmetry | IN_PROGRESS (8%) | Pending |
| `ec8df342` | rank_sum | COMPLETE | No sorry closed |
| `8dee4922` | AbstractCauchySchwarz | COMPLETE | **Proved sum_sq_ge_quarter_of_sum_eq_neg_half** |
| `9f141957` | Combined | IN_PROGRESS (7%) | Pending |
| Several others | Various focuses | IN_PROGRESS | Pending |

## Remaining Work

The 3 sorry lemmas need manual proof or further Aristotle attempts:

1. **`rank_sum`** -- hardest. Needs to show fareyRank is injective on fareySet, maps into range n, hence is a bijection to {0,...,n-1}. The sum then equals 0+1+...+(n-1) = n(n-1)/2.

2. **`farey_sum_symmetry`** -- use `Finset.sum_involution` with the map (a,b) -> (b-a, b) which sends a/b to (b-a)/b = 1 - a/b. Need to show: gcd(b-a, b) = gcd(a,b), the map is an involution, and the fixed point analysis. The pair (a/b, (b-a)/b) sums to 1, so sum over all pairs = n/2.

3. **`displacement_sum_eq`** -- follows from rank_sum + farey_sum_symmetry by expanding displacement = rank - n*f and distributing the sum.

## Verification

Computational verification via `native_decide` passes for N = 1, 2, 3, 5, confirming the statement is correct.

## Date

2026-03-29
