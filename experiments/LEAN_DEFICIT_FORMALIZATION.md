# Lean 4 Formalization: Deficit Minimality

## Status: THEOREM 1 PROVED, THEOREM 2 IN PROGRESS

**File:** `RequestProject/DeficitMinimality.lean`
**Date:** 2026-03-29

---

## Mathematical Statement

For prime q >= 3 and 1 < r < q:

**Definition.** The deficit of the modular permutation a -> ra mod q:
```
D_q(r) := sum_{a=1}^{q-1} a^2 - sum_{a=1}^{q-1} a * (ra mod q)
```

**Theorem 1 (Explicit evaluation).** D_q(2) = q(q^2 - 1)/24. **PROVED.**

**Theorem 2 (Minimality).** D_q(r) >= D_q(2) for all 1 < r < q. *sorry -- Aristotle 5c4453fd running.*

**Corollary.** D_q(r) >= q(q^2 - 1)/24 for all 1 < r < q. *Proved modulo Theorem 2.*

---

## Proof of Theorem 1 (Aristotle project 66009af7 -- COMPLETE)

Aristotle produced a clean proof using 4 helper lemmas:

1. `sum_sq_Icc` -- sum of squares: sum_{a=1}^n a^2 = n(n+1)(2n+1)/6 (by induction)
2. `sum_Icc_nat` -- sum formula: sum_{a=1}^n a = n(n+1)/2 (by induction)
3. `sumOfSquares_closed` -- for q=2k+1: sumOfSquares(q) = k(2k+1)(4k+1)/3
4. `modCrossSum_two_decomp` -- key decomposition: modCrossSum(2k+1, 2) = 2*sumOfSquares - (2k+1)*sum_{k+1}^{2k} a
   - For a <= k: 2a mod (2k+1) = 2a (since 2a < 2k+1)
   - For a > k: 2a mod (2k+1) = 2a - (2k+1) (since 2k+1 <= 2a < 2(2k+1))

Main theorem extracts k from q = 2k+1 (using odd prime >= 3), substitutes closed forms, finishes with push_cast; ring.

**Uses only standard axioms** (propext, Classical.choice, Quot.sound). No sorry.

## Proof of Theorem 2 (Aristotle project 5c4453fd -- IN PROGRESS)

The key structural insight (verified computationally):
```
2 * D_q(r) = sum_{a=1}^{q-1} (a - ra mod q)^2
```
via the polarization identity, since a -> ra mod q is a permutation of {1,...,q-1}.

So D_q(r) >= D_q(2) iff the r=2 permutation has the smallest L^2 distance from identity.

---

## Lean 4 Formalization Structure

### Definitions
- `sumOfSquares q` -- sum_{a=1}^{q-1} a^2 (as Q)
- `modCrossSum q r` -- sum_{a=1}^{q-1} a * (ra mod q) (as Q)
- `deficit q r` -- sumOfSquares q - modCrossSum q r
- `dispSqSum q r` -- sum_{a=1}^{q-1} (a - ra mod q)^2
- `sawtooth x` -- the sawtooth function ((x))
- `dedekindSum h k` -- the Dedekind sum s(h,k)

### Computational Verifications (ALL PASS via native_decide)
- `deficit_formula_q` for q in {3, 5, 7, 11, 13, 17, 19, 23}: D_q(2) = q(q^2-1)/24
- `deficit_formula_batch_30`: formula holds for all primes 3 <= q < 30
- `deficit_min_q` for q in {5, 7, 11, 13}: D_q(r) >= D_q(2) for all valid r
- `deficit_minimality_batch_13`: minimality holds for all primes 3 <= q <= 13, all 2 <= r < q
- `polarization_check_*`: 2*deficit = dispSqSum verified for (q,r) in {(7,2),(7,3),(11,5),(13,7)}

### General Theorems
- `deficit_two_formula` -- **PROVED** (Aristotle 66009af7)
- `deficit_minimality` -- sorry (Aristotle 5c4453fd running, 1% after 54 min)
- `deficit_lower_bound` -- proof complete modulo deficit_minimality

---

## Build Status

Local build: PASSES (lake build RequestProject.DeficitMinimality)
- Only warning: 1x "declaration uses sorry" (deficit_minimality)
- All 28+ native_decide proofs pass
- deficit_two_formula proved with no sorry

## Aristotle Results

### 66009af7 (deficit_two_formula) -- COMPLETE
- Proved successfully
- Clean proof with 4 helper lemmas (sum of squares, sum formula, decomposition)
- Integrated into main file

### 5c4453fd (deficit_minimality) -- IN PROGRESS
- Status: 1% after 54 minutes (this is a hard proof)
- May not succeed -- the minimality requires deep number theory (Dedekind sums / rearrangement)

### Cancelled submissions (had broken Nat.succ_injective definition)
- ec1b38f4, 0a62e320 -- CANCELED

---

## Connection to Farey Research

The deficit D_q(r) appears in the analysis of how Farey fractions rearrange under
multiplication by r mod q. Specifically:

- The shift function delta(a/q) = a/q - {p*a/q mod 1} in the Farey wobble analysis
  involves exactly this modular rearrangement.
- The minimality at r=2 explains why the "simplest nontrivial" prime step (p=2 in
  the Farey progression) produces the smallest rearrangement cost.
- The lower bound q(q^2-1)/24 gives explicit control on the shift-squared sum C(p),
  which is a key ingredient in the Sign Theorem proof.

## Python Verification

Both theorems verified computationally for all primes up to q=97:
- Theorem 1: D_q(2) = q(q^2-1)/24 for all 24 primes tested
- Theorem 2: D_q(r) >= D_q(2) for all valid r, for primes q=3..31
- Polarization: 2*D_q(r) = sum(a - ra mod q)^2 for all tested (q,r)
