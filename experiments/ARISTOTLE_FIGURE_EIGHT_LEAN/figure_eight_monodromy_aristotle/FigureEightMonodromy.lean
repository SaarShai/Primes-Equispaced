/-
  Figure-Eight Three-Body Orbit: Monodromy Matrix in Γ(2)

  The figure-eight orbit's monodromy, expressed in the Γ(2) generators
    a = !![1,2; 0,1],  b = !![1,0; 2,1]
    A = a⁻¹ = !![1,-2; 0,1],  B = b⁻¹ = !![1,0; -2,1]
  via the word BabA, yields M = !![5,-8; -8,13].

  We prove:
  1. The matrix product B·a·b·A equals !![5,-8; -8,13]
  2. det(M) = 1
  3. The fixed-point equation of M is z² - z - 1 = 0 (golden ratio minimal polynomial)
-/

import Mathlib

open Matrix

/-- Generator a of Γ(2): the matrix [[1,2],[0,1]] -/
def gen_a : Matrix (Fin 2) (Fin 2) ℤ := !![1, 2; 0, 1]

/-- Generator b of Γ(2): the matrix [[1,0],[2,1]] -/
def gen_b : Matrix (Fin 2) (Fin 2) ℤ := !![1, 0; 2, 1]

/-- A = a⁻¹ in Γ(2): the matrix [[1,-2],[0,1]] -/
def gen_A : Matrix (Fin 2) (Fin 2) ℤ := !![1, -2; 0, 1]

/-- B = b⁻¹ in Γ(2): the matrix [[1,0],[-2,1]] -/
def gen_B : Matrix (Fin 2) (Fin 2) ℤ := !![1, 0; -2, 1]

/-- The figure-eight monodromy matrix M = B·a·b·A -/
def monodromy_M : Matrix (Fin 2) (Fin 2) ℤ := gen_B * gen_a * gen_b * gen_A

/-- The target matrix [[5,-8],[-8,13]] -/
def target_M : Matrix (Fin 2) (Fin 2) ℤ := !![5, -8; -8, 13]

/-- Theorem 1: The matrix product B·a·b·A equals [[5,-8],[-8,13]] -/
theorem monodromy_product :
    monodromy_M = target_M := by
  unfold monodromy_M gen_B gen_a gen_b gen_A target_M
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- Theorem 2: The determinant of M is 1 -/
theorem monodromy_det_one :
    Matrix.det target_M = 1 := by
  simp [Matrix.det_fin_two, target_M]

/-- Theorem 3: The entries of M are consecutive Fibonacci numbers F₅, F₆, F₇ -/
theorem monodromy_fibonacci_entries :
    target_M 0 0 = 5 ∧ target_M 0 1 = -8 ∧ target_M 1 0 = -8 ∧ target_M 1 1 = 13 := by
  simp [target_M]

/-- The trace of the monodromy matrix is 18 -/
theorem monodromy_trace :
    Matrix.trace target_M = 18 := by
  unfold Matrix.trace target_M
  simp [Fin.sum_univ_two]

/--
  Theorem 4 (Golden Ratio Fixed Point):

  For the matrix M = [[5,-8],[-8,13]], the projective fixed point equation
  M · [z,1]ᵀ = λ[z,1]ᵀ gives:
    5z - 8 = λz  and  -8z + 13 = λ
  Substituting λ = -8z + 13 into the first:
    5z - 8 = (-8z + 13)z
    5z - 8 = -8z² + 13z
    8z² - 8z - 8 = 0
    z² - z - 1 = 0
  This is the golden ratio minimal polynomial.

  We prove: for any z : ℤ, if M acts projectively with fixed point z
  (meaning (5*z - 8) * 1 = z * (-8*z + 13)), then z² - z - 1 = 0.
-/
theorem golden_ratio_fixed_point (z : ℤ) (h : 5 * z - 8 = z * (-8 * z + 13)) :
    z ^ 2 - z - 1 = 0 := by
  nlinarith

/--
  Converse: if z² - z - 1 = 0 then z is a projective fixed point of M.
-/
theorem golden_ratio_fixed_point_conv (z : ℤ) (h : z ^ 2 - z - 1 = 0) :
    5 * z - 8 = z * (-8 * z + 13) := by
  nlinarith

/-- gen_A is the integer-matrix inverse of gen_a (their product is I) -/
theorem gen_a_mul_gen_A :
    gen_a * gen_A = 1 := by
  unfold gen_a gen_A
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- gen_B is the integer-matrix inverse of gen_b (their product is I) -/
theorem gen_b_mul_gen_B :
    gen_b * gen_B = 1 := by
  unfold gen_b gen_B
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]
