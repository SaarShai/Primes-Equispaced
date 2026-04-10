import Mathlib

/-!
# Mediant Minimality and Farey Gap Bounds

This file proves the **mediant minimality theorem** — that between two Farey neighbours
a/b and c/d (with bc − ad = 1), every fraction p/q strictly between them satisfies
q ≥ b + d — and the **Farey gap formula** — that c/d − a/b = 1/(bd).

We then derive several gap‐bound variants (`farey_gap_bound`, etc.) as corollaries.

## Main results

* `farey_gap_formula` — If bc − ad = 1 then c/d − a/b = 1/(bd).
* `mediant_minimality` — If bc − ad = 1 and a/b < p/q < c/d then q ≥ b + d.
* `farey_gap_bound` — The gap between Farey neighbours of order N is ≥ 1/N².
* `farey_gap_bound_strict` — Strict variant: the gap is > 1/(N(N+1)).
* `farey_gap_bound_nat` — Natural-number version of the gap bound.
-/

open scoped Classical

/-! ## Core results -/

/-- **Farey gap formula.** If bc − ad = 1, then c/d − a/b = 1/(bd). -/
theorem farey_gap_formula (a b c d : ℤ)
    (hb : 0 < b) (hd : 0 < d)
    (hdet : b * c - a * d = 1) :
    (c : ℚ) / d - a / b = 1 / (b * d) := by
  have hb' : (b : ℚ) ≠ 0 := Int.cast_ne_zero.mpr (ne_of_gt hb)
  have hd' : (d : ℚ) ≠ 0 := Int.cast_ne_zero.mpr (ne_of_gt hd)
  rw [div_sub_div _ _ hd' hb', div_eq_div_iff (mul_ne_zero hd' hb') (mul_ne_zero hb' hd')]
  have : (b : ℚ) * c - a * d = 1 := by exact_mod_cast hdet
  linear_combination (↑d * ↑b : ℚ) * this

/-- **Mediant minimality.** If bc − ad = 1 and a/b < p/q < c/d then q ≥ b + d.

The classical proof: bp − aq ≥ 1 and cq − dp ≥ 1 since both are positive integers,
so q = q(bc − ad) = (cq − dp)·b + (bp − aq)·d ≥ b + d. -/
theorem mediant_minimality (a b c d p q : ℤ)
    (hb : 0 < b) (hd : 0 < d) (hq : 0 < q)
    (hdet : b * c - a * d = 1)
    (h1 : a * q < p * b)
    (h2 : p * d < c * q) :
    b + d ≤ q := by
  have hbp_aq : 1 ≤ b * p - a * q := by linarith
  have hcq_dp : 1 ≤ c * q - d * p := by linarith
  have key : q = (c * q - d * p) * b + (b * p - a * q) * d := by nlinarith
  nlinarith [mul_le_mul_of_nonneg_right hbp_aq (le_of_lt hd),
             mul_le_mul_of_nonneg_right hcq_dp (le_of_lt hb)]

/-! ## Gap bound variants -/

/-
PROBLEM
**Farey gap bound.** If b, d ≤ N and bc − ad = 1, then c/d − a/b ≥ 1/N².

PROVIDED SOLUTION
Use farey_gap_formula to rewrite the gap as 1/(bd). Then since b ≤ N and d ≤ N with b,d > 0, we have bd ≤ N*N, so 1/(bd) ≥ 1/(N*N). Use div_le_div and mul_le_mul for the ℚ arithmetic.
-/
theorem farey_gap_bound (a b c d N : ℤ)
    (hb : 0 < b) (hd : 0 < d) (hN : 0 < N)
    (hbN : b ≤ N) (hdN : d ≤ N)
    (hdet : b * c - a * d = 1) :
    1 / ((N : ℚ) * N) ≤ (c : ℚ) / d - a / b := by
  field_simp;
  norm_cast; nlinarith [ mul_le_mul_of_nonneg_left hbN hd.le, mul_le_mul_of_nonneg_left hdN hb.le ] ;

/-
PROBLEM
**Farey gap bound (strict).** When b + d > N (which holds for consecutive Farey
    neighbours of order N when N ≥ 2), the gap is strictly greater than 1/(N(N+1)).

PROVIDED SOLUTION
Use farey_gap_formula to get gap = 1/(bd). We need 1/(N(N+1)) < 1/(bd). Since b ≤ N and d ≤ N with N < b+d, we need bd < N(N+1). From b+d > N, b ≤ N, d ≤ N, and b,d ≥ 1, we get bd ≤ N² but actually we need bd < N(N+1). Since b+d > N and b ≤ N and d ≤ N, at least one of b,d < N or we can argue bd ≤ N*N < N*(N+1). Actually: bd = b*d. Since b ≤ N, d ≤ N, bd ≤ N². And N² < N(N+1). So 1/(bd) ≥ 1/N² > 1/(N(N+1)).
-/
theorem farey_gap_bound_strict (a b c d N : ℤ)
    (hb : 0 < b) (hd : 0 < d) (hN : 0 < N)
    (hbN : b ≤ N) (hdN : d ≤ N)
    (hsum : N < b + d)
    (hdet : b * c - a * d = 1) :
    1 / ((N : ℚ) * (N + 1)) < (c : ℚ) / d - a / b := by
  -- By farey_gap_formula, we have_gap = 1/(bd).
  have h_gap : (c : ℚ) / d - a / b = 1 / (b * d) := by
    rw [ div_sub_div, mul_comm ] <;> try positivity;
    exact congrArg₂ _ ( mod_cast by linarith ) ( by ring );
  rw [ h_gap, div_lt_div_iff₀ ] <;> norm_cast <;> nlinarith

/-
PROBLEM
**Farey gap bound (ℕ version).** Natural-number version using ℕ subtraction.

PROVIDED SOLUTION
Cast everything to ℤ, use hdet (b*c = a*d + 1 in ℕ) to get b*c - a*d = 1 in ℤ, then apply farey_gap_bound with the ℤ versions of the hypotheses.
-/
theorem farey_gap_bound_nat (a b c d N : ℕ)
    (hb : 0 < b) (hd : 0 < d) (hN : 0 < N)
    (hbN : b ≤ N) (hdN : d ≤ N)
    (hdet : b * c = a * d + 1) :
    1 / ((N : ℚ) * N) ≤ (c : ℚ) / d - a / b := by
  rw [ div_sub_div, div_le_div_iff₀ ] <;> norm_cast <;> try positivity;
  rw [ Int.subNatNat_eq_coe ] ; push_cast ; nlinarith [ mul_le_mul_right hbN (d : ℕ), mul_le_mul_right hdN (b : ℕ) ]

/-
PROBLEM
The following statement is FALSE. Counterexample: a=0, b=1, c=1, d=1, N=5.
   Then bc − ad = 1, gap = 1/1 = 1, but 1/N = 1/5 < 1.
   The issue is that 1/(bd) ≤ 1/N requires N ≤ bd, which does not follow from
   b ≤ N and d ≤ N alone (e.g. b = d = 1).

theorem farey_gap_upper_bound (a b c d N : ℤ)
    (hb : 0 < b) (hd : 0 < d) (hN : 0 < N)
    (hbN : b ≤ N) (hdN : d ≤ N)
    (hdet : b * c - a * d = 1) :
    (c : ℚ) / d - a / b ≤ 1 / N := by
  sorry

**Farey gap upper bound (corrected).** The gap is at most 1/b (since d ≥ 1).

PROVIDED SOLUTION
Use farey_gap_formula to get gap = 1/(bd). Since d ≥ 1, bd ≥ b, so 1/(bd) ≤ 1/b.
-/
theorem farey_gap_upper_bound (a b c d : ℤ)
    (hb : 0 < b) (hd : 0 < d)
    (hdet : b * c - a * d = 1) :
    (c : ℚ) / d - a / b ≤ 1 / b := by
  rw [ div_sub_div, div_le_div_iff₀ ] <;> norm_cast <;> nlinarith [ sq_nonneg ( b - d ) ]

/-
PROBLEM
**Farey gap upper bound (with b + d > N).** For consecutive Farey neighbours
    of order N (where b + d > N), the gap is at most 1/N.

PROVIDED SOLUTION
Use farey_gap_formula to get gap = 1/(bd). We need 1/(bd) ≤ 1/N, i.e., N ≤ bd. Since N < b+d, b ≤ N, d ≤ N, all positive integers: N < b+d ≤ 2N. Also bd ≥ b+d-1 ≥ N (since for positive integers b,d: bd = bd ≥ b+d-1 when b,d ≥ 1, because (b-1)(d-1) ≥ 0 gives bd ≥ b+d-1). And b+d > N gives bd ≥ b+d-1 ≥ N.
-/
theorem farey_gap_upper_bound' (a b c d N : ℤ)
    (hb : 0 < b) (hd : 0 < d) (hN : 0 < N)
    (hbN : b ≤ N) (hdN : d ≤ N)
    (hsum : N < b + d)
    (hdet : b * c - a * d = 1) :
    (c : ℚ) / d - a / b ≤ 1 / N := by
  rw [ div_sub_div, div_le_div_iff₀ ] <;> norm_cast at * <;> nlinarith;

/-
PROBLEM
**Mediant minimality (ℕ version).**

PROVIDED SOLUTION
Cast everything to ℤ. From hdet (b*c = a*d + 1 in ℕ) we get (b:ℤ)*(c:ℤ) - (a:ℤ)*(d:ℤ) = 1. From h1 and h2 (strict inequalities in ℕ) we get the corresponding ℤ inequalities. Then apply mediant_minimality with the ℤ versions. The result b+d ≤ q in ℤ gives b+d ≤ q in ℕ.
-/
theorem mediant_minimality_nat (a b c d p q : ℕ)
    (hb : 0 < b) (hd : 0 < d) (hq : 0 < q)
    (hdet : b * c = a * d + 1)
    (h1 : a * q < p * b)
    (h2 : p * d < c * q) :
    b + d ≤ q := by
  nlinarith [ mul_pos hq hb, mul_pos hq hd ]