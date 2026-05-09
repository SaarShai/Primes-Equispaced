/-
# Shannon Entropy Monotonicity for Farey Gap Distributions

When going from Farey sequence F_N to F_{N+1}, mediants are inserted.
Each mediant insertion splits a gap g into g₁ + g₂ = g with g₁, g₂ > 0.
By strict concavity of η(x) = -x log x, the entropy contribution increases:
  η(g₁) + η(g₂) > η(g₁ + g₂)
Hence the total Shannon entropy is strictly increasing in N.

We formalize the core entropy-splitting inequality and the monotonicity result
for abstract gap distributions modelling this phenomenon.
-/
import Mathlib

open Real Finset BigOperators

noncomputable section

/-- Shannon entropy of a distribution given as a list of gap widths. -/
def shannonEntropy (gaps : List ℝ) : ℝ :=
  (gaps.map negMulLog).sum

/-
Core splitting inequality: strict concavity of negMulLog implies that splitting
    a single weight into two positive parts strictly increases the negMulLog contribution.
    That is, η(a) + η(b) > η(a + b) for a, b > 0 where η(x) = -x log x.
-/
theorem negMulLog_split (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    negMulLog (a + b) < negMulLog a + negMulLog b := by
  simp +decide [ Real.negMulLog ] at *;
  nlinarith [ mul_pos hb ha, mul_pos hb ( sub_pos.mpr ha ), mul_pos ha ( sub_pos.mpr hb ), mul_pos hb ( sub_pos.mpr hb ), mul_pos ha ( sub_pos.mpr ha ), Real.log_lt_log ( by linarith ) ( by linarith : a + b > a ), Real.log_lt_log ( by linarith ) ( by linarith : a + b > b ) ]

/-
Replacing one gap by two positive sub-gaps that sum to it strictly increases entropy.
-/
theorem shannonEntropy_split_increases
    (pre post : List ℝ) (g a b : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hab : a + b = g) :
    shannonEntropy (pre ++ [g] ++ post) < shannonEntropy (pre ++ [a, b] ++ post) := by
  -- Unfold the definition of Shannon entropy.
  unfold shannonEntropy

  -- Both sides are sums over lists. The pre and post parts cancel.
  have h_cancel : (pre.map negMulLog).sum + (negMulLog g) + (post.map negMulLog).sum < (pre.map negMulLog).sum + (negMulLog a + negMulLog b) + (post.map negMulLog).sum := by
    simpa [ ← hab ] using negMulLog_split a b ha hb;
  simpa [ add_assoc ] using h_cancel

/-- A Farey gap configuration: gaps are positive and sum to 1. -/
structure FareyGapDist where
  gaps : List ℝ
  gaps_pos : ∀ g ∈ gaps, 0 < g
  gaps_sum : gaps.sum = 1
  gaps_nonempty : gaps ≠ []

/-- The Shannon entropy of a Farey gap distribution. -/
def FareyGapDist.entropy (d : FareyGapDist) : ℝ :=
  shannonEntropy d.gaps

/-- Splitting a gap in a FareyGapDist produces a valid FareyGapDist. -/
def FareyGapDist.splitGap (d : FareyGapDist) (pre post : List ℝ)
    (g a b : ℝ) (ha : 0 < a) (hb : 0 < b) (hab : a + b = g)
    (hdecomp : d.gaps = pre ++ [g] ++ post) : FareyGapDist where
  gaps := pre ++ [a, b] ++ post
  gaps_pos := by
    intro x hx
    simp [List.mem_append, List.mem_cons] at hx
    rcases hx with hx | hx | hx | hx
    · exact d.gaps_pos x (by rw [hdecomp]; simp [List.mem_append]; left; exact hx)
    · rw [hx]; exact ha
    · rw [hx]; exact hb
    · exact d.gaps_pos x (by rw [hdecomp]; simp [List.mem_append]; right; right; exact hx)
  gaps_sum := by
    have h1 := d.gaps_sum
    rw [hdecomp] at h1
    simp only [List.append_assoc, List.sum_append, List.sum_cons, List.sum_nil] at h1 ⊢
    linarith
  gaps_nonempty := by simp

/-- The main result: splitting a gap in a Farey gap distribution strictly increases entropy. -/
theorem FareyGapDist.entropy_strict_increases (d : FareyGapDist)
    (pre post : List ℝ) (g a b : ℝ) (ha : 0 < a) (hb : 0 < b) (hab : a + b = g)
    (hdecomp : d.gaps = pre ++ [g] ++ post) :
    d.entropy < (d.splitGap pre post g a b ha hb hab hdecomp).entropy := by
  unfold FareyGapDist.entropy FareyGapDist.splitGap shannonEntropy
  simp only
  rw [hdecomp]
  exact shannonEntropy_split_increases pre post g a b ha hb hab

end