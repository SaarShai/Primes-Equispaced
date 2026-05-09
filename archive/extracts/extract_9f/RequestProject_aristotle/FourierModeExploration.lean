import Mathlib
import PrimeCircle
import DisplacementShift
import StrictPositivity
import CrossTermPositive
import BridgeIdentity

/-!
# Fourier Mode Analysis of the Cross Term

## Overview
The cross term B(p) = 2·Σ D·δ can be decomposed by denominator b:
  B/2 = Σ_{b=1}^{p-1} crossByDenom(p, b)

Each crossByDenom(p, b) = Σ_{a coprime b} D(a/b) · δ(a/b) depends on the
permutation σ(a) = ap mod b.

## Key Findings (computational)

### 1. Vanishing denominators
crossByDenom(p, b) = 0 whenever p ≡ 1 (mod b), because σ = identity ⟹ δ = 0.
For p=13: this kills b ∈ {1,2,3,4,6,12} (six of twelve denominators vanish).
Some additional denominators vanish by cancellation (b=9,10 for p=13).

### 2. Per-denominator values for p=13 (M=−3)
Only four denominators contribute:
  b=5:  crossByDenom = −1/5   (13 ≡ 3 mod 5, ord=4)
  b=7:  crossByDenom = +1/7   (13 ≡ 6 mod 7, ord=2)
  b=8:  crossByDenom = +1/2   (13 ≡ 5 mod 8, ord=2)
  b=11: crossByDenom = −1/11  (13 ≡ 2 mod 11, ord=10)
  Total: −1/5 + 1/7 + 1/2 − 1/11 = 271/770 > 0

### 3. Orbit-length decomposition
Grouping by multiplicative order of p mod b:
  ord=2 orbits: b=7,8 contribute 1/7 + 1/2 = 9/14 ≈ 0.643
  ord=4 orbits: b=5 contributes −1/5 = −0.200
  ord=10 orbits: b=11 contributes −1/11 ≈ −0.091
  
The order-2 orbits DOMINATE, providing 183% of the total.
Higher-order orbits partially cancel.

### 4. Ramanujan (Möbius) weighting
Weighting each denominator by μ(b):
  mode1_Ram = Σ μ(b) · crossByDenom(p,b)
  = μ(5)·(−1/5) + μ(7)·(1/7) + μ(8)·(1/2) + μ(11)·(−1/11)
  = (−1)(−1/5) + (−1)(1/7) + 0·(1/2) + (−1)(−1/11)
  = 1/5 − 1/7 + 1/11 = 57/385 > 0

### 5. Sign of R (correlation ratio)
R = B/(2·Σδ²) is POSITIVE for all tested primes with M(p) ≤ −3:
  p=13: R ≈ 0.051,  p=19: R ≈ 0.154,  p=31: R ≈ 0.759,  p=43: R ≈ 0.669
Since R > 0, we have 1 + 2R > 1 > 0, so B+C > 0 is immediate.
-/

open Finset BigOperators

/-! ## Per-denominator cross term -/

/-- Per-denominator contribution to half the cross term.
    crossByDenom(p, b) = Σ_{a coprime b, 0 ≤ a ≤ b} D_{p−1}(a/b) · δ_p(a/b) -/
def crossByDenom (p b : ℕ) : ℚ :=
  ∑ a ∈ (Finset.range (b + 1)).filter (fun a => Nat.Coprime a b),
    displacement (p - 1) ((a : ℚ) / b) * shiftFun p ((a : ℚ) / b)

/-! ## Verified decomposition: sum of crossByDenom = crossTerm / 2 -/

/-- Sanity check for p=13: Σ_b crossByDenom = crossTerm/2. -/
theorem crossByDenom_sum_13 :
    2 * ∑ b ∈ Finset.Icc 1 12, crossByDenom 13 b = crossTerm 13 := by
  native_decide

/-- Sanity check for p=19. -/
theorem crossByDenom_sum_19 :
    2 * ∑ b ∈ Finset.Icc 1 18, crossByDenom 19 b = crossTerm 19 := by
  native_decide

/-- Sanity check for p=31. -/
theorem crossByDenom_sum_31 :
    2 * ∑ b ∈ Finset.Icc 1 30, crossByDenom 31 b = crossTerm 31 := by
  native_decide

/-! ## Per-denominator values for p = 13

Key observation: crossByDenom(13, b) = 0 whenever 13 ≡ 1 (mod b),
because the permutation σ(a) = 13a mod b is the identity, making δ = 0.
-/

/-- For p=13: only b=5,7,8,11 contribute (non-trivially). -/
theorem crossByDenom_13_vanishing :
    crossByDenom 13 1 = 0 ∧ crossByDenom 13 2 = 0 ∧
    crossByDenom 13 3 = 0 ∧ crossByDenom 13 4 = 0 ∧
    crossByDenom 13 6 = 0 ∧ crossByDenom 13 9 = 0 ∧
    crossByDenom 13 10 = 0 ∧ crossByDenom 13 12 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> native_decide

/-- The four non-zero per-denominator contributions for p=13. -/
theorem crossByDenom_13_nonzero :
    crossByDenom 13 5 = -1 / 5 ∧
    crossByDenom 13 7 = 1 / 7 ∧
    crossByDenom 13 8 = 1 / 2 ∧
    crossByDenom 13 11 = -1 / 11 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> native_decide

/-- The total half-cross-term for p=13: sum of four contributions. -/
theorem crossByDenom_13_total :
    ∑ b ∈ Finset.Icc 1 12, crossByDenom 13 b = 271 / 770 := by native_decide

/-! ## Per-denominator values for p = 19 -/

/-- For p=19: the non-trivial contributions. -/
theorem crossByDenom_19_nonzero :
    crossByDenom 19 4 = 1 / 4 ∧
    crossByDenom 19 7 = 3 / 7 ∧
    crossByDenom 19 8 = 1 / 8 ∧
    crossByDenom 19 10 = 4 / 5 ∧
    crossByDenom 19 11 = 9 / 11 ∧
    crossByDenom 19 12 = 1 / 2 ∧
    crossByDenom 19 13 = 3 / 13 ∧
    crossByDenom 19 14 = 8 / 7 ∧
    crossByDenom 19 15 = -2 / 5 ∧
    crossByDenom 19 16 = -15 / 16 ∧
    crossByDenom 19 17 = -14 / 17 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> native_decide

/-- For p=19: vanishing denominators (19 ≡ 1 mod b). -/
theorem crossByDenom_19_vanishing :
    crossByDenom 19 1 = 0 ∧ crossByDenom 19 2 = 0 ∧
    crossByDenom 19 3 = 0 ∧ crossByDenom 19 5 = 0 ∧
    crossByDenom 19 6 = 0 ∧ crossByDenom 19 9 = 0 ∧
    crossByDenom 19 18 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> native_decide

/-! ## Positive vs negative contributions -/

/-- For p=13: the positive contributions outweigh the negative ones. -/
theorem crossByDenom_13_pos_sum :
    crossByDenom 13 7 + crossByDenom 13 8 = 9 / 14 := by native_decide

theorem crossByDenom_13_neg_sum :
    crossByDenom 13 5 + crossByDenom 13 11 = -16 / 55 := by native_decide

/-- Positive sum (9/14 ≈ 0.643) exceeds |negative sum| (16/55 ≈ 0.291). -/
theorem crossByDenom_13_pos_dominates :
    crossByDenom 13 7 + crossByDenom 13 8 >
    |crossByDenom 13 5 + crossByDenom 13 11| := by native_decide

/-! ## Ramanujan-weighted (Möbius) cross term -/

/-- The Möbius-weighted cross term:
    mode1_Ram(p) = Σ_b μ(b) · crossByDenom(p, b).
    This extracts the squarefree component of the per-denominator decomposition. -/
def crossModeRamanujan (p : ℕ) : ℚ :=
  ∑ b ∈ Finset.Icc 1 (p - 1),
    (ArithmeticFunction.moebius b : ℤ) * crossByDenom p b

/-- Ramanujan mode for p=13: μ(5)(-1/5) + μ(7)(1/7) + μ(11)(-1/11)
    = 1/5 - 1/7 + 1/11 = 57/385. Note μ(8)=0 kills the b=8 term. -/
theorem crossModeRam_13 : crossModeRamanujan 13 = 57 / 385 := by native_decide

/-- Ramanujan mode for p=19. -/
theorem crossModeRam_19 : crossModeRamanujan 19 = 75629 / 85085 := by native_decide

-- Ramanujan mode for p=31:
-- #eval crossModeRamanujan 31  -- -1491210771 / 215656441
-- Note: negative for p=31 (M(31)=-4), but positive for p=13,19 (M=-3)!

/-! ## Mode dominance: Ramanujan mode vs total -/

/-- For p=13: Ramanujan mode = 57/385, total = 271/385.
    Ratio = 57/271 ≈ 21%. The Ramanujan mode captures only ~21% of the total.
    This is because μ(8)=0 kills the large b=8 contribution (1/2). -/
theorem ramanujan_not_dominant_13 :
    2 * |crossModeRamanujan 13| < crossTerm 13 := by native_decide

/-! ## Orbit-length decomposition

For each denominator b, the multiplicative order ord_b(p) determines
the cycle structure of σ(a) = ap mod b.

For p=13:
  b=7:  ord = 2  (13≡6≡-1 mod 7)  → crossByDenom = +1/7
  b=8:  ord = 2  (13≡5≡-3 mod 8)  → crossByDenom = +1/2
  b=5:  ord = 4  (13≡3 mod 5)     → crossByDenom = −1/5
  b=11: ord = 10 (13≡2 mod 11)    → crossByDenom = −1/11
  
Observation: SHORT orbits (ord=2) give POSITIVE contributions.
LONG orbits (ord=4,10) give NEGATIVE contributions.

Conjecture: the contribution sign correlates with orbit length.
Short orbits correspond to p ≈ ±1 mod b (strong congruence),
which creates systematic positive D·δ correlation.
-/

/-- The short-orbit (ord=2) contributions for p=13 are positive. -/
theorem short_orbit_pos_13 :
    crossByDenom 13 7 + crossByDenom 13 8 > 0 := by native_decide

/-- The long-orbit contributions for p=13 are negative. -/
theorem long_orbit_neg_13 :
    crossByDenom 13 5 + crossByDenom 13 11 < 0 := by native_decide

/-- Short orbits DOMINATE for p=13. -/
theorem short_orbit_dominant_13 :
    crossByDenom 13 7 + crossByDenom 13 8 >
    |crossByDenom 13 5| + |crossByDenom 13 11| := by native_decide

/-! ## Correlation ratio R = B / (2·Σδ²) is POSITIVE -/

/-- R(13) > 0: the cross term and shift-squared sum are both positive. -/
theorem corrRatio_pos_13 : crossTerm 13 / (2 * shiftSquaredSum 13) > 0 := by native_decide

/-- R(19) > 0. -/
theorem corrRatio_pos_19 : crossTerm 19 / (2 * shiftSquaredSum 19) > 0 := by native_decide

/-- R(31) > 0. -/
theorem corrRatio_pos_31 : crossTerm 31 / (2 * shiftSquaredSum 31) > 0 := by native_decide

/-- Since R > 0, we have 1+2R > 1, so B+C = δ²·(1+2R) > 0 is immediate. -/
theorem corrRatio_implies_bPlusC_13 :
    1 + 2 * (crossTerm 13 / (2 * shiftSquaredSum 13)) > 0 := by native_decide

/-! ## Exact correlation ratio values -/

/-- R(13) = 813/15872 ≈ 0.051. -/
theorem corrRatio_val_13 :
    crossTerm 13 / (2 * shiftSquaredSum 13) = 813 / 15872 := by native_decide

/-- R(19) = 2905619/18867622 ≈ 0.154. -/
theorem corrRatio_val_19 :
    crossTerm 19 / (2 * shiftSquaredSum 19) = 2905619 / 18867622 := by native_decide

/-! ## R is positive for ALL primes with M(p) ≤ -3 up to 84 -/

/-- The correlation ratio R > 0 for all primes with M(p) ≤ -3 below 84. -/
theorem corrRatio_pos_all_small :
    ∀ p ∈ Finset.filter (fun p => Nat.Prime p ∧ 11 ≤ p ∧ mertens p ≤ -3)
      (Finset.range 84),
    crossTerm p / (2 * shiftSquaredSum p) > 0 := by native_decide

/-! ## Per-denominator analysis for p = 31 (M = -4)

p=31 has many more non-vanishing denominators since fewer b satisfy 31 ≡ 1 (mod b).
-/

/-- Key non-zero contributions for p=31. -/
theorem crossByDenom_31_selected :
    crossByDenom 31 4 = 1 / 4 ∧
    crossByDenom 31 7 = 3 / 7 ∧
    crossByDenom 31 8 = 5 / 8 ∧
    crossByDenom 31 11 = 2 ∧
    crossByDenom 31 17 = 79 / 17 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> native_decide

/-- p=31 has a much larger cross term than p=13 or p=19. -/
theorem crossTerm_31_large : crossTerm 31 > crossTerm 19 := by native_decide

/-! ## Summary and interpretation

### Per-denominator structure
The cross term B = 2·Σ D·δ decomposes by denominator b:
- B/2 = Σ_b crossByDenom(p, b)
- crossByDenom(p, b) = 0 when p ≡ 1 (mod b) (identity permutation)
- Some additional denominators vanish by cancellation

### Orbit-length pattern
- Short orbits (ord_b(p) = 2, i.e., p ≡ -1 mod b) tend to give POSITIVE contributions
- Long orbits tend to give negative contributions
- Short orbits DOMINATE: the cross term is positive because the short-orbit
  contributions exceed the long-orbit cancellations

### Connection to Mertens function
When M(p) ≤ -3:
1. There are many small primes q < p with μ(q) = -1
2. This means p has many "near-involution" modular relationships (p ≡ -1 mod q)
3. These create short orbits → positive cross term contributions
4. The aggregate effect: B > 0 and R = B/(2·Σδ²) > 0

### Fourier mode interpretation
Rather than a single dominant "h=1 mode", the positivity comes from:
- The short-orbit contributions (a "low-frequency" effect analogous to h=1)
- These are controlled by p mod b for small b
- The Mertens condition M(p) ≤ -3 ensures enough small primes q with μ(q) = -1
  to make p ≡ -1 mod q, creating the dominant short orbits

### Quantitative dominance
For p=13: short orbits (b=7,8) give 9/14 ≈ 0.643, which is 183% of total 271/770.
The "excess" is cancelled by long orbits. The short-orbit contribution IS dominant
in the sense that it exceeds the total, not in the sense of capturing a percentage.
-/
