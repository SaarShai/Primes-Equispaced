# Summary of changes
## Summary

I proved `rank_sum` in `CWBound.lean`, but first had to **correct the statement** because the original was false.

### The bug in the original statement
The original claimed `Σ rank(f) = n*(n-1)/2`, but `fareyRank` is defined with `≤` (inclusive), so ranks range from 1 to n, not 0 to n-1. Counterexample: for N=1, fareySet = {(0,1),(1,1)}, ranks = {1,2}, sum = 3 ≠ 1 = 2*1/2.

### The corrected statement
```lean
lemma rank_sum (N : ℕ) :
    ∑ ab ∈ fareySet N, (fareyRank N ((ab.1 : ℚ) / ab.2) : ℚ) =
      (fareySet N).card * ((fareySet N).card + 1) / 2
```
The correct formula is **n*(n+1)/2** (sum of 1+2+...+n).

### Proof structure
The proof uses a double-counting / symmetry argument with three helper lemmas:

1. **`farey_frac_injective`**: Distinct elements of `fareySet N` give distinct rational values. This uses cross-multiplication and coprimality to show that reduced fractions in lowest terms are unique.

2. **`farey_eq_singleton`**: The filter of elements with equal fraction value is a singleton (immediate from injectivity).

3. **`farey_rank_upper_rank`**: For each element, rank + upper_rank = n+1. Uses inclusion-exclusion: the "≤" and "≥" filters cover all of `fareySet N`, and their intersection is the singleton from step 2.

4. **`rank_sum`** (main): Uses `Finset.sum_comm` to show `Σ upper_rank = Σ rank` (swapping the double sum), then combines with step 3 to get `2·Σ rank = n*(n+1)`.

### Other changes
- Fixed `import RequestProject.X` → `import X` across all `.lean` files (the project uses flat module names, not a `RequestProject/` directory).
- Added a comment explaining why the original `n*(n-1)/2` formula was incorrect.
- All proofs use only standard axioms (propext, Classical.choice, Quot.sound).