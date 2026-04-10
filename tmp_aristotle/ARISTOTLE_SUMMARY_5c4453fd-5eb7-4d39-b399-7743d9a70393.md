# Summary of changes
Successfully proved `deficit_minimality` and all related theorems in `RequestProject/DeficitMinimality.lean`. The file now compiles with zero `sorry` statements.

## What was proved

**Theorem `deficit_minimality`**: For prime q ≥ 3 and 1 < r < q, `deficit q r ≥ deficit q 2`.

**Theorem `deficit_two_formula`**: For odd prime q ≥ 3, `deficit q 2 = q(q²-1)/24`.

**Theorem `deficit_lower_bound`**: Combines the above: `deficit q r ≥ q(q²-1)/24`.

## Proof strategy for `deficit_minimality`

The proof uses a clean polarization + pointwise bound argument:

1. **`deficit_eq_half_disp_sq`**: The deficit equals half the sum of displacement squared: `deficit q r = (1/2) * ∑ (a - ra mod q)²`. This follows from the fact that multiplication by r mod q is a permutation (so `∑(ra mod q)² = ∑ a²`).

2. **`disp_sq_ge_min`** (pointwise bound): For each a, `(a - ra mod q)² ≥ min(c, q-c)²` where `c = a*(q+1-r) mod q`. This holds because `a - ra mod q ≡ a(1-r) ≡ c (mod q)`, so the displacement is either `c` or `c-q`, giving square `c²` or `(q-c)²`, both ≥ `min(c, q-c)²`.

3. **`sum_min_sq_perm`**: Since `a ↦ a*(q+1-r) mod q` is also a permutation, `∑ min(c, q-c)² = ∑ min(a, q-a)²`.

4. **`disp_sq_two`**: For r=2, each `(a - 2a mod q)² = min(a, q-a)²` exactly.

Combining: `deficit q r ≥ (1/2) ∑ min(a, q-a)² = deficit q 2`.

All axioms used are standard (propext, Classical.choice, Quot.sound).