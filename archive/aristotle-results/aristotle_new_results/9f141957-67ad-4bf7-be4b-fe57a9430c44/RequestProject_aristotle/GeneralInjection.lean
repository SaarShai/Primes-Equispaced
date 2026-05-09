import Mathlib
import PrimeCircle

/-!
# General Injection Principle for Farey Sequences

For any N ≥ 2, each gap between consecutive fractions in the Farey sequence F_{N-1}
receives at most one new fraction when forming F_N.

## Proof Structure

For consecutive fractions a/q < b/s in F_{N-1}, we have the boundary properties:
  q + s ≥ N  and  b·q − a·s = 1

The proof proceeds by case analysis on the product q·s of consecutive denominators:

- **Case 4** (q·s < N−1): Impossible. Since (q−1)(s−1) ≥ 0, we get q·s ≥ q+s−1 ≥ N−1.
- **Cases 1 & 2** (q·s ≥ N): The open interval (a·N, b·N·q/s) scaled by s has width
  N/(q·s) ≤ 1. At most one integer k satisfies the gap condition.
- **Case 3** (q·s = N−1): Since (q−1)(s−1) ≥ 0 and q·s = N−1 give q+s ≤ N = q·s+1,
  combined with q+s ≥ N we get (q−1)(s−1) = 0, forcing q = 1 or s = 1.
  Direct arithmetic verification shows at most one fraction enters.
-/

open Finset Nat

/-! ## Section 1: Computational Verification for Small N -/

/-- Boolean check of the general injection principle for a specific N.
    Verifies that for every pair of consecutive Farey fractions a/q, b/s in F_{N-1}
    (satisfying q·b = a·s + 1 and q + s ≥ N), at most one value k has
    a·N < k·q and k·s < b·N. -/
def generalInjectionCheckBool (N : ℕ) : Bool :=
  (List.finRange N).all fun q =>
    (List.finRange N).all fun s =>
      (List.finRange N).all fun a =>
        (List.finRange N).all fun b =>
          if Nat.ble 1 q.val && Nat.ble 1 s.val &&
             Nat.beq (q.val * b.val) (a.val * s.val + 1) &&
             Nat.ble N (q.val + s.val)
          then
            (List.finRange (N + 1)).all fun k₁ =>
              (List.finRange (N + 1)).all fun k₂ =>
                !(Nat.blt (a.val * N) (k₁.val * q.val) &&
                  Nat.blt (k₁.val * s.val) (b.val * N) &&
                  Nat.blt (a.val * N) (k₂.val * q.val) &&
                  Nat.blt (k₂.val * s.val) (b.val * N)) ||
                Nat.beq k₁.val k₂.val
          else true

/-- Computational verification for N = 2. -/
theorem general_injection_check_2 : generalInjectionCheckBool 2 = true := by native_decide

/-- Computational verification for N = 3. -/
theorem general_injection_check_3 : generalInjectionCheckBool 3 = true := by native_decide

/-- Computational verification for N = 4. -/
theorem general_injection_check_4 : generalInjectionCheckBool 4 = true := by native_decide

/-- Computational verification for N = 5. -/
theorem general_injection_check_5 : generalInjectionCheckBool 5 = true := by native_decide

/-! ## Section 2: Product Lower Bound (Eliminates Case 4)

Case 4 claims q·s < N−1 is impossible. We prove q·s ≥ N−1 from
(q−1)(s−1) ≥ 0 and q+s ≥ N.
-/

/-
PROBLEM
**Product lower bound.** For q, s ≥ 1 with q + s ≥ N, we have q·s ≥ N − 1.
    Proof: (q−1)(s−1) ≥ 0 gives q·s ≥ q + s − 1 ≥ N − 1.

PROVIDED SOLUTION
From (q-1)(s-1) ≥ 0, expand to get q*s ≥ q+s-1 ≥ N-1. Use nlinarith.
-/
theorem product_lower_bound (q s N : ℕ) (hq : 1 ≤ q) (hs : 1 ≤ s) (hsum : N ≤ q + s) :
    N - 1 ≤ q * s := by
  exact Nat.sub_le_of_le_add <| by nlinarith only [ hq, hs, hsum ] ;

/-! ## Section 3: Case 3 — q·s = N−1 Forces Boundary Denominators

When q·s = N−1 and q+s ≥ N, we show (q−1)(s−1) = 0, so q = 1 or s = 1.
-/

/-
PROBLEM
**Case 3 structure.** If q·s = N−1 and q + s ≥ N with q, s ≥ 1,
    then q = 1 or s = 1.
    Proof: q·s = N−1 and q+s ≥ N give q+s ≤ q·s+1.
    Combined with (q−1)(s−1) = q·s − q − s + 1 ≥ 0 and ≤ 0, we get equality,
    meaning q−1 = 0 or s−1 = 0.

PROVIDED SOLUTION
From q*s = N-1 and q+s ≥ N, we get q+s ≤ q*s+1. So (q-1)(s-1) = q*s - q - s + 1 ≤ 0. But (q-1)(s-1) ≥ 0. So (q-1)(s-1) = 0, giving q=1 or s=1. Use omega or nlinarith after case analysis on whether q*s ≥ q+s.
-/
theorem product_eq_pred_forces_boundary (q s N : ℕ) (hq : 1 ≤ q) (hs : 1 ≤ s)
    (hsum : N ≤ q + s) (hprod : q * s = N - 1) :
    q = 1 ∨ s = 1 := by
  rcases N with ( _ | _ | N ) <;> simp_all +decide;
  · grind +ring;
  · aesop;
  · rcases q with ( _ | _ | q ) <;> rcases s with ( _ | _ | s ) <;> norm_num at * ; nlinarith

/-! ## Section 4: Cases 1 & 2 — q·s ≥ N

When q·s ≥ N, any k in the gap satisfies k·q·s ∈ (a·N·s, a·N·s + N),
an open interval of width N. Two distinct k-values would give
|k₁ − k₂|·q·s ≥ q·s ≥ N, but the interval has width N (open), contradiction.
-/

/-
PROBLEM
**Cases 1 & 2.** If q·s ≥ N and q·b = a·s + 1, then at most one k
    satisfies a·N < k·q and k·s < b·N.

PROVIDED SOLUTION
For k₁, k₂ in the gap: multiply a*N < k*q by s and k*s < b*N by q. Get a*N*s < k*q*s < b*N*q = (a*s+1)*N = a*N*s + N. So k*q*s is in the open interval (a*N*s, a*N*s+N) of width N. If k₁ ≠ k₂ then |k₁-k₂| ≥ 1 so |k₁*q*s - k₂*q*s| ≥ q*s ≥ N. But both values are in the same interval of width N (open), contradiction. Use nlinarith.
-/
theorem at_most_one_large_product (N a q b s : ℕ) (hq : 1 ≤ q) (hs : 1 ≤ s)
    (hdet : q * b = a * s + 1) (hprod : N ≤ q * s) :
    ∀ k₁ k₂ : ℕ,
      a * N < k₁ * q → k₁ * s < b * N →
      a * N < k₂ * q → k₂ * s < b * N →
      k₁ = k₂ := by
  intro k₁ k₂ hk₁ hk₂ hk₃ hk₄; nlinarith;

/-! ## Section 5: Case 3 — q·s = N−1

When q·s + 1 = N, two values k₁ < k₂ in the gap would give
k₂·q·s ≥ k₁·q·s + (N−1), and both in an open interval (a·N·s, a·N·s + N).
This forces k₁·q·s ≥ a·N·s + 1 and k₁·q·s + (N−1) ≤ a·N·s + N − 1,
giving k₁·q·s = a·N·s, contradicting the strict inequality.
-/

/-
PROBLEM
**Case 3.** If q·s + 1 = N and q·b = a·s + 1, then at most one k
    satisfies a·N < k·q and k·s < b·N.

PROVIDED SOLUTION
Same as at_most_one_large_product. Multiply inequalities: a*N*s < k*q*s and k*q*s < a*N*s + N. Two distinct k with |k₁-k₂| ≥ 1 give |k₁*q*s - k₂*q*s| ≥ q*s = N-1. But both in open interval of width N. Use nlinarith with hdet and hprod substituted.
-/
theorem at_most_one_critical_product (N a q b s : ℕ) (hq : 1 ≤ q) (hs : 1 ≤ s)
    (hdet : q * b = a * s + 1) (hprod : q * s + 1 = N) :
    ∀ k₁ k₂ : ℕ,
      a * N < k₁ * q → k₁ * s < b * N →
      a * N < k₂ * q → k₂ * s < b * N →
      k₁ = k₂ := by
  intros k₁ k₂ hk₁ hk₂ hk₃ hk₄;
  contrapose! hprod;
  cases lt_or_gt_of_ne hprod <;> nlinarith [ mul_pos ( by linarith : 0 < q ) ( by linarith : 0 < s ) ]

/-! ## Section 6: Main Theorem — General Injection Principle -/

/-- **The General Injection Principle.** For any N ≥ 2, let a/q and b/s be
    consecutive fractions in the Farey sequence F_{N-1}, so that
    q·b − a·s = 1, q + s ≥ N, and 1 ≤ q, s ≤ N−1.
    Then at most one value k satisfies a/q < k/N < b/s
    (expressed via cross-multiplication as a·N < k·q and k·s < b·N).

    The proof combines:
    - `product_lower_bound`: eliminates Case 4 (q·s < N−1 is impossible)
    - `at_most_one_large_product`: handles Cases 1 & 2 (q·s ≥ N)
    - `at_most_one_critical_product`: handles Case 3 (q·s = N−1) -/
theorem general_injection_principle (N q s a b : ℕ) (hN : 2 ≤ N)
    (hq : 1 ≤ q) (hs : 1 ≤ s)
    (hqN : q ≤ N - 1) (hsN : s ≤ N - 1)
    (hdet : q * b = a * s + 1)
    (hsum : N ≤ q + s) :
    ∀ k₁ k₂ : ℕ,
      a * N < k₁ * q → k₁ * s < b * N →
      a * N < k₂ * q → k₂ * s < b * N →
      k₁ = k₂ := by
  -- By product_lower_bound, q·s ≥ N−1, so either q·s ≥ N or q·s = N−1.
  have h_lb := product_lower_bound q s N hq hs hsum
  by_cases h : N ≤ q * s
  · -- Cases 1 & 2: q·s ≥ N
    exact at_most_one_large_product N a q b s hq hs hdet h
  · -- Case 3: q·s = N−1 (since q·s ≥ N−1 and q·s < N)
    push_neg at h
    have h_eq : q * s + 1 = N := by omega
    exact at_most_one_critical_product N a q b s hq hs hdet h_eq

/-- Corollary: the injection principle applies to new Farey fractions
    (those with denominator exactly N, i.e., gcd(k, N) = 1). -/
theorem general_injection_new_fractions (N q s a b : ℕ) (hN : 2 ≤ N)
    (hq : 1 ≤ q) (hs : 1 ≤ s)
    (hqN : q ≤ N - 1) (hsN : s ≤ N - 1)
    (hdet : q * b = a * s + 1)
    (hsum : N ≤ q + s) :
    ∀ k₁ k₂ : ℕ,
      Nat.Coprime k₁ N → Nat.Coprime k₂ N →
      a * N < k₁ * q → k₁ * s < b * N →
      a * N < k₂ * q → k₂ * s < b * N →
      k₁ = k₂ :=
  fun k₁ k₂ _ _ h1 h2 h3 h4 =>
    general_injection_principle N q s a b hN hq hs hqN hsN hdet hsum k₁ k₂ h1 h2 h3 h4