# Summary of changes
Created `RequestProject/MediantMinimality.lean` with all theorems fully proved (no active `sorry`). Here's what was done:

## Core theorems (proved)
- **`farey_gap_formula`** — If bc − ad = 1 then c/d − a/b = 1/(bd).
- **`mediant_minimality`** — If bc − ad = 1 and a/b < p/q < c/d then q ≥ b + d.

## Gap bound variants (all proved)
- **`farey_gap_bound`** — Gap ≥ 1/N² when b, d ≤ N.
- **`farey_gap_bound_strict`** — Gap > 1/(N(N+1)) when b + d > N (consecutive Farey neighbours).
- **`farey_gap_bound_nat`** — ℕ version of the gap bound (uses `b * c = a * d + 1` to avoid ℕ subtraction issues).
- **`mediant_minimality_nat`** — ℕ version of mediant minimality.

## False statement identified and corrected
- **`farey_gap_upper_bound`** (original): claimed gap ≤ 1/N with only b, d ≤ N. This is **false** — counterexample: a=0, b=1, c=1, d=1, N=5 gives gap = 1 > 1/5. The false version is commented out with an explanation.
- **`farey_gap_upper_bound`** (corrected): proves gap ≤ 1/b (since d ≥ 1, bd ≥ b).
- **`farey_gap_upper_bound'`**: proves gap ≤ 1/N with the additional hypothesis `N < b + d` (which holds for consecutive Farey neighbours of order N). This makes the original statement true.

All proofs use only standard axioms (`propext`, `Classical.choice`, `Quot.sound`).