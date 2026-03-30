# Identity Verification Report

**Claim:** For any prime p >= 5 and N = p-1, let F_N be the Farey sequence of order N. Define delta(a/b) = (a - (p*a mod b))/b. Then:

    Sum_{a/b in F_N, b>1} (a/b) * delta(a/b) = (1/2) * Sum_{a/b in F_N, b>1} delta(a/b)^2

**Date:** 2026-03-29
**Verification approach:** Independent adversarial review (algebra re-derivation + exact arithmetic computation + counterexample search)

---

## 1. Algebraic Verification (Steps 1-3)

**VERDICT: Steps 1-3 are CORRECT.**

Setting x = a/b and f = (p*a mod b)/b, we have delta = x - f. Re-deriving independently:

- Step 1: x * delta = x(x - f) = x^2 - x*f. **Correct** (trivial).
- Step 2: delta^2 = (x - f)^2 = x^2 - 2*x*f + f^2. **Correct** (trivial).
- Step 3: x*delta - delta^2/2 = (x^2 - x*f) - (x^2 - 2*x*f + f^2)/2 = x^2/2 - f^2/2 = (x^2 - f^2)/2. **Correct**.

Therefore the identity reduces to: **Sum (x^2 - f^2) = 0** summed over all a/b in F_N with b > 1.

Note on summation range: Since a=0 only appears as 0/1 (gcd(0,b) = b, so 0/b is not reduced for b>1), and a=b only gives 1/1 (excluded by b>1), the effective range is a in {1, ..., b-1} with gcd(a,b)=1, for b = 2, ..., N.

---

## 2. Permutation Property (Step 4)

**VERDICT: Step 4 is CORRECT, but the proof's validity domain is BROADER than stated.**

The claim in step 4 is: for fixed b with gcd(p,b)=1, the map a -> (p*a mod b) is a permutation of the coprime residues modulo b.

**This is a standard fact from elementary number theory.** If gcd(p,b) = 1, then multiplication by p is a bijection on (Z/bZ)^*. Specifically, if gcd(a,b) = 1, then gcd(p*a mod b, b) = 1, and the map is injective on a finite set, hence bijective. This is the same principle underlying Euler's theorem.

**Consequence:** Since a -> pa mod b permutes the coprime residues, the multiset {(a/b)^2 : gcd(a,b)=1, 1 <= a < b} equals the multiset {((pa mod b)/b)^2 : gcd(a,b)=1, 1 <= a < b}. Therefore Sum (a/b)^2 = Sum ((pa mod b)/b)^2 for each fixed b, and the per-b contribution to Sum(x^2 - f^2) is zero.

**Verified computationally** for all primes p in {5, 7, 11, 13, 23, 37, 53, 97, 149, 199} and all b from 2 to N = p-1. All permutation checks passed. All squared-sum equalities confirmed with exact Fraction arithmetic.

---

## 3. Numerical Verification

**VERDICT: Identity CONFIRMED for all tested primes using exact rational arithmetic.**

| p | N = p-1 | LHS = RHS | Match |
|---|---------|-----------|-------|
| 5 | 4 | 1/9 | YES |
| 7 | 6 | 9/20 | YES |
| 11 | 10 | 2231/1512 | YES |
| 13 | 12 | 6781/2310 | YES |
| 23 | 22 | 110256409/12697776 | YES |
| 37 | 36 | 41766978782183/1337069934200 | YES |
| 53 | 52 | (large exact fraction) | YES |
| 97 | 96 | (large exact fraction) | YES |
| 149 | 148 | (large exact fraction) | YES |
| 199 | 198 | (large exact fraction) | YES |

All computed using Python's `fractions.Fraction` (arbitrary precision, no floating-point error).

---

## 4. Counterexample Search

### 4a. Does it hold for N != p-1?

**KEY FINDING: The identity holds for ALL N < p, not just N = p-1.**

For every tested prime p in {5, 7, 11, 13, 17, 19, 23, 29, 31} and every N with 2 <= N <= p-1, the identity holds exactly. The claimed scope (N = p-1) is actually too narrow -- the identity is valid for the full range N in {2, ..., p-1}.

### 4b. Does it fail for N >= p?

**YES. The identity ALWAYS fails for N >= p (when p is prime).**

The failure mechanism is precise: when N >= p, the denominator b = p enters the Farey sequence. For b = p, the map a -> pa mod p = 0 sends ALL coprime residues to 0. This is not a permutation, and it injects a nonzero contribution of (p-1)(2p-1)/(6p) into the difference LHS - RHS.

Specific failure magnitudes:
- p=5, N=5: diff = 3/5
- p=7, N=7: diff = 13/14
- p=11, N=11: diff = 35/22
- p=13, N=13: diff = 25/13

These are exactly (p-1)(2p-1)/(6p) in each case, matching the theoretical prediction.

### 4c. Does it hold for composite p?

**NO. For composite p, the identity generally FAILS even for N = p-1.**

Examples:
- p=4, N=3: LHS = 1/4, RHS = 1/8 (FAIL)
- p=6, N=5: LHS = 67/72, RHS = 67/144 (FAIL)
- p=9, N=8: LHS = 461/315, RHS = 677/630 (FAIL)

The failure occurs because composite p shares factors with some b <= N, breaking the permutation property.

### 4d. Most general characterization

**EXACT CHARACTERIZATION: The identity holds if and only if gcd(p, b) = 1 for ALL b in {2, ..., N}.**

This was verified exhaustively for all (p, N) with 3 <= p <= 49 and 2 <= N <= min(p+9, 59). Zero exceptions found.

**For prime p:** This condition is equivalent to N < p (since p is prime, gcd(p, b) > 1 iff b is a multiple of p, and the smallest multiple of p in {2,...,N} is p itself).

**For non-prime p:** The condition is more restrictive. For example, p=25 requires N <= 4 (since gcd(25, 5) = 5 > 1).

---

## 5. Is This Identity Known?

The individual components are standard:

1. **Permutation property** (a -> pa mod b is a bijection on coprime residues when gcd(p,b)=1): This is textbook number theory, a direct consequence of the group structure of (Z/bZ)^*.

2. **Squared-sum invariance under permutation**: If sigma is a permutation of a set S, then Sum_{s in S} f(s) = Sum_{s in S} f(sigma(s)) for any function f. This is trivial.

3. **The algebraic reduction** from Sum x*delta = (1/2) Sum delta^2 to Sum(x^2 - f^2) = 0: This is elementary algebra (steps 1-3).

**However,** the specific combination -- defining delta via the Farey sequence and modular arithmetic, then showing the x*delta vs delta^2 relationship via the permutation argument -- does not appear to be a standard textbook identity. The individual steps are well-known, but the particular packaging connecting Farey sequences to this quadratic identity appears to be a novel observation.

The closest standard result is the theory of **Dedekind sums** and **Farey sequence equidistribution**, which involve similar objects (fractions a/b, modular arithmetic, quadratic sums). The permutation argument itself is the same one used in proving properties of Ramanujan sums and Gauss sums.

---

## 6. Adversarial Assessment

### Strengths of the proof:
- Steps 1-3 are trivially correct (basic algebra)
- Step 4 uses a standard, well-established fact
- The logical chain is complete: steps 1-3 reduce the identity to Sum(x^2 - f^2) = 0, step 4 proves each per-b contribution is zero
- Numerically verified to exact precision for primes up to 199

### Weaknesses and concerns:
1. **The claimed scope is too narrow.** The proof actually establishes the identity for all N < p, not just N = p-1. The proof nowhere uses N = p-1 specifically -- it only needs gcd(p, b) = 1 for all b <= N.

2. **Potential notational confusion.** The definition delta(a/b) = (a - (p*a mod b))/b could be ambiguous: does "p*a mod b" mean the least non-negative residue? The proof assumes yes, and this is the standard convention, but it should be stated explicitly.

3. **The identity is a direct consequence of a permutation argument.** While the packaging is clean, each step is elementary. The novelty (if any) is in the choice of delta, not in the proof technique.

4. **No attempt was made to connect this to deeper structure.** The identity holds because of a group-theoretic symmetry (multiplication by p permutes (Z/bZ)^*). There may be a more illuminating formulation in terms of characters or Gauss sums.

### Attempted attacks that failed:
- Tried composite N: identity breaks as predicted
- Tried N >= p: identity breaks precisely at b = p
- Tried composite p: identity breaks when gcd(p,b) > 1
- Checked edge cases (a=0, a=b, b=1): all correctly excluded
- Verified algebra independently: matches

---

## 7. Final Verdict

| Aspect | Status |
|--------|--------|
| Algebra (steps 1-3) | CORRECT |
| Permutation claim (step 4) | CORRECT (standard fact) |
| Squared-sum conclusion (step 4) | CORRECT |
| Overall proof logic | CORRECT and COMPLETE |
| Numerical verification | PASSED for all tested primes (p up to 199) |
| Counterexamples found | YES -- for N >= p and for composite p |
| Scope accuracy | UNDERSTATED -- identity holds for all N < p, not just N = p-1 |

**The identity is TRUE and the proof is VALID.** The proof is correct but uses only standard techniques (algebra + group action on coprime residues). The identity itself is a clean observation, though each step in the proof is elementary. The stated scope (N = p-1) is unnecessarily restrictive; the true scope is N < p (equivalently, gcd(p,b) = 1 for all b <= N).
