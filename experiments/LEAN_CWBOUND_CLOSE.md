# CWBound.lean Cleanup Report

**Date:** 2026-03-30

## Summary

CWBound.lean had **4 compilation errors** (not `sorry` statements). All have been fixed and the file now compiles cleanly with zero errors and zero warnings.

## What Was Wrong

CWBound.lean had these errors:
1. **Duplicate declaration**: `fareyCount_eq_card` was already defined in `SignTheorem.lean`
2. **Missing argument**: `fareyCount_pos N` requires `(hN : 1 ≤ N)` but was called without it
3. **Unknown identifier**: `fareyCount_sq_pos` and `fareyCount_cast_pos` were not defined in the main codebase (only in old Aristotle result directories)
4. **Unsolved goal** in `cw_ge_quarter_inv`: the proof strategy referenced missing lemmas

## Fixes Applied

### CWBound.lean (rewritten)
- Removed duplicate `fareyCount_eq_card` (already in SignTheorem.lean)
- Added 3 new auxiliary lemmas:
  - `fareyCount_cast_pos`: proves `(fareyCount N : Q) > 0` for all N (no hypothesis needed since `fareyCount N = 1 + sum >= 1`)
  - `fareyCount_cast_ne_zero`: corollary, `(fareyCount N : Q) != 0`
  - `fareyCount_sq_pos`: proves `(fareyCount N : Q)^2 > 0`
- Fixed `fareySet_card_pos` to pass `hN` to `fareyCount_pos`
- Rewrote `cw_ge_quarter_inv` proof using `positivity` and `nlinarith`
- All theorems compile: `cw_ge_quarter_inv`, `cw_ge_quarter_inv_1/2/3`, `wobbleNumerator_ge_fareyCount_div_four`, `sum_sq_ge_quarter_of_sum_eq_pos_half`

### CauchySchwarzBound.lean
- Replaced `exact?` on line 110 with `exact sq_sum_le_card_mul_sum_sq` (the Lean suggestion)

### DAConvergence.lean
- Removed as requested (it compiled fine but was unused -- not imported by any other file)

## Remaining Sorry Count

Only **2 sorry** remain in the entire RequestProject, both in unrelated files:
- `MediantMinimality.lean:116`
- `SignConj.lean:65`

**CWBound.lean and its full dependency chain (PrimeCircle, DisplacementShift, SignTheorem, AbstractCauchySchwarz, CauchySchwarzBound, FareySymmetry) are sorry-free.**

## Note on the Original Request

The user asked to close `rank_sum` and `farey_sum_symmetry` sorry lemmas in CWBound.lean. These lemma names do not exist in the codebase. The actual issues were compilation errors (not sorry). The mathematical content the user described (Gauss's formula for rank sum, involution f <-> 1-f for Farey symmetry) is already fully proved:
- **Rank sum / Gauss formula**: proved in `CauchySchwarzBound.lean` lines 37-72 (via sorted enumeration of fareySet)
- **Farey sum symmetry (sum f = n/2)**: proved in `CauchySchwarzBound.lean` lines 74-85 AND independently in `FareySymmetry.lean` lines 96-106 (via the involution `f -> 1-f`)

Both are used in `displacement_sum` (CauchySchwarzBound.lean line 32) which feeds into the Cauchy-Schwarz bound. The entire CW >= 1/(4n) proof chain is now complete and compiles.
