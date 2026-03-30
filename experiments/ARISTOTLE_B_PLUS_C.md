# Aristotle Formalization: B + C Building Blocks

**Date:** 2026-03-30
**Status:** Submitted to Aristotle, awaiting results

## Overview

Three algebraic identities were submitted to the Aristotle automated theorem prover
(harmonic.fun) for formal verification in Lean 4. These are building blocks for the
B + C > 0 proof in our Farey discrepancy analysis.

**Context:** In our framework, B = 2 * sum(D * delta) and C = sum(delta^2), where D is
the displacement function and delta is the shift function. The quantity B + C controls
discrepancy growth when passing from F_{p-1} to F_p.

---

## Task 1: Algebraic Factorization Identity

**Claim:** B + C = sum(delta * (2*D + delta))

**Lean statement:**
```lean
theorem B_plus_C_eq_sum {n : Nat} (D delta : Fin n -> Rat) :
    2 * sum i : Fin n, D i * delta i + sum i : Fin n, delta i ^ 2
    = sum i : Fin n, delta i * (2 * D i + delta i)
```

**Aristotle job:** `c299e4d8-33e0-4eb2-813f-8eca1c617ccf`
**Status:** IN_PROGRESS

**Expected proof strategy:** Pull the linear combination under the sum using
`Finset.sum_add_distrib` and `Finset.mul_sum`, then close each summand with `ring`.

**Hand-crafted fallback proof:**
```lean
theorem B_plus_C_eq_sum {n : ℕ} (D δ : Fin n → ℚ) :
    2 * ∑ i : Fin n, D i * δ i + ∑ i : Fin n, δ i ^ 2 =
    ∑ i : Fin n, δ i * (2 * D i + δ i) := by
  rw [← Finset.sum_add_distrib, Finset.mul_sum]
  congr 1; ext i; ring
```

---

## Task 2: Completing-the-Square Identity

**Claim:** B + C = sum((D + delta)^2) - sum(D^2)

**Lean statement:**
```lean
theorem B_plus_C_complete_square {n : Nat} (D delta : Fin n -> Rat) :
    2 * sum i : Fin n, D i * delta i + sum i : Fin n, delta i ^ 2
    = sum i : Fin n, (D i + delta i) ^ 2 - sum i : Fin n, D i ^ 2
```

**Aristotle job:** `a403c3c5-5b38-43b2-8de0-656d122bd9d0`
**Status:** IN_PROGRESS

**Expected proof strategy:** Rewrite using `Finset.sum_sub_distrib` (or express as a
single sum via difference), expand (D+delta)^2 - D^2 = 2*D*delta + delta^2, then close
with `ring`.

**Hand-crafted fallback proof:**
```lean
theorem B_plus_C_complete_square {n : ℕ} (D δ : Fin n → ℚ) :
    2 * ∑ i : Fin n, D i * δ i + ∑ i : Fin n, δ i ^ 2 =
    ∑ i : Fin n, (D i + δ i) ^ 2 - ∑ i : Fin n, D i ^ 2 := by
  rw [← Finset.sum_sub_distrib]
  rw [← Finset.sum_add_distrib, Finset.mul_sum]
  congr 1; ext i; ring
```

---

## Task 3: Sum of Squares Non-Negativity

**Claim:** sum(f(i)^2) >= 0

**Lean statement:**
```lean
theorem sum_sq_nonneg {n : Nat} (f : Fin n -> Rat) :
    0 <= sum i : Fin n, (f i) ^ 2
```

**Aristotle job:** `0c8f222b-1115-4cbd-869d-12dcf95c1a9d`
**Status:** IN_PROGRESS

**Expected proof strategy:** Apply `Finset.sum_nonneg` with each term non-negative
by `sq_nonneg`.

**Hand-crafted fallback proof:**
```lean
theorem sum_sq_nonneg {n : ℕ} (f : Fin n → ℚ) :
    0 ≤ ∑ i : Fin n, (f i) ^ 2 := by
  apply Finset.sum_nonneg
  intro i _
  exact sq_nonneg (f i)
```

---

## Why These Matter

These three lemmas combine to give a lower bound on B + C:

1. **Task 2** gives: B + C = sum((D + delta)^2) - sum(D^2)
2. **Task 3** gives: sum((D + delta)^2) >= 0
3. Therefore: B + C >= -sum(D^2)

More importantly, the completing-the-square form shows that B + C > 0 is equivalent to
sum((D + delta)^2) > sum(D^2), i.e., the "wobble" (sum of squared displacements)
*increases* when passing from F_{p-1} to F_p. This is the geometric content of the
B + C > 0 condition.

The factored form from Task 1 is useful for bounding: since B + C = sum(delta*(2D+delta)),
we can analyze the sign by understanding when 2D + delta is typically positive (which
happens when D is positively correlated with delta, the key Mertens-driven phenomenon).

---

## Connection to Existing Formalization

These abstract lemmas complement the concrete Farey-specific results in:
- `CrossTermPositive.lean` -- B > 0 verified for primes with M(p) <= -3 up to p < 114
- `StrictPositivity.lean` -- C = sum(delta^2) > 0 for all primes
- The `quadratic_expansion_sum` lemma in CrossTermPositive.lean already proves a
  related identity for the Farey-specific D and delta functions

The new abstract versions work over arbitrary `Fin n -> Q` without requiring Farey
structure, making them reusable for any future applications.

---

## How to Check Results

```bash
export ARISTOTLE_API_KEY="..."
# Task 1:
~/.local/bin/aristotle result c299e4d8-33e0-4eb2-813f-8eca1c617ccf --destination /tmp/task1.lean
# Task 2:
~/.local/bin/aristotle result a403c3c5-5b38-43b2-8de0-656d122bd9d0 --destination /tmp/task2.lean
# Task 3:
~/.local/bin/aristotle result 0c8f222b-1115-4cbd-869d-12dcf95c1a9d --destination /tmp/task3.lean
```

---

## Update Log

- 2026-03-30: All three tasks submitted. Server under load, building Lean/Mathlib.
  Progress at 1% after ~17 minutes. Will update when results arrive.
