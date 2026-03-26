# PROOF BREAKTHROUGH: Critical Correction and New Direction
## Session: 2026-03-26 (Hour 1: Telescoping/Structure Analysis)

---

## MAJOR FINDING: B+C > 0 is FALSE for Some Primes

The scheduled task claimed B+C > 0 is verified computationally to p=500. This is correct.
However, the claim fails starting at **p=1399**.

### Violation Table

| p    | B+C value       | 1+R      | Notes                    |
|------|----------------|----------|--------------------------|
| 1399 | -634.90        | -0.0065  | First violation          |
| 1409 | -89,662.25     | -0.9001  |                          |
| 1423 | -253,697.11    | -2.4974  |                          |
| 1427 | -447,856.77    | -2.9736  |                          |
| 1429 | -494,367.49    | -3.0029  |                          |
| 2633 | -636,918.97    | -3.0478  |                          |
| 2647 | -741,093.76    | -3.0661  |                          |
| 2657 | -1,103,898.18  | -3.098   | Worst known violation    |
| 2659 | -776,234.08    | -3.084   |                          |
| 2663 | -703,118.44    | -3.076   |                          |

**Count**: 10 violations found in primes [11, 2999].

### The R Bound Was Wrong

The task claimed |R| < 0.52 empirically. Actual range (verified to p=3000):
- **min R ≈ -3.098** (at p=2657)
- **max R ≈ +8.419** (at p=467)

The claim was based on insufficient verification range.

---

## WHAT THIS MEANS FOR THE PROOF

### ΔW ≤ 0 Still Holds

Even when B+C < 0, we have ΔW(p) ≤ 0. This means **new_D_sq compensates**: when B+C < 0, the new fractions k/p have large D_new(k/p)² values that more than cover the deficit.

### The Proof Cannot Go Through B+C ≥ 0

The original strategy was: ΔW ≤ 0 because new_D_sq ≥ dilution_raw and B+C ≥ 0. This fails.

The correct decomposition is:
```
ΔW ≤ 0  ⟺  new_D_sq + B_raw + delta_sq ≥ dilution_raw
            ⟺  new_D_sq + B_raw ≥ dilution_raw - delta_sq
```

When B+C < 0 (i.e., B_raw < -delta_sq), new_D_sq must exceed dilution_raw alone.

### The True Obstruction

Proving new_D_sq ≥ dilution_raw non-circularly IS the problem. The identity:
```
D/A ≥ 1 - K/p
```
uses conservation of wobble (ΔW ≤ 0) — so it's circular.

---

## KEY STRUCTURAL FACTS ESTABLISHED

### Fact 1: Injection Identity (Non-Circular)

For each k/p inserted into F_{p-1}, the left Farey neighbor f_j = a_j/b_j satisfies:
```
k·b_j - p·a_j = 1  (exact, non-circular)
b_j = k⁻¹ mod p
D_new(k/p) = D(f_j) + c_j
where c_j = 1 - n/(p·b_j)  (n = |F_{p-1}|, exact)
```

This gives the non-circular identity:
```
TERM_A (new_D_sq) = TERM_B_old + 2·TERM_C_cross + TERM_C_sq
where TERM_B_old = Σ D(f_j)²  (old fractions appearing as neighbors)
      TERM_C_cross = Σ D(f_j)·c_j
      TERM_C_sq = Σ c_j²  (TERM_C)
```

### Fact 2: TERM_C Lower Bound (Non-Circular, Verified)

```
TERM_C = Σ_{b=1}^{p-1} (1 - n/(p·b))²  ≥  0.35 · dilution_raw
```

- Analytically: TERM_C = (p-1) - 2n·H_{p-1}/p + n²·S₂(p-1)/p²
- Computationally verified for all primes 11 ≤ p ≤ 8100
- Minimum ratio ≈ 0.366 at p=2803

This gives D/A ≥ 0.35 non-circularly. Insufficient alone (need > 1), but firm.

### Fact 3: Per-Pair Symmetry

For any fraction a/b ∈ F_{p-1} with a < b/2, the complementary fraction (b-a)/b also appears. The pair contribution to B+C is:
```
t(a/b) + t((b-a)/b) = 2δ·(2D + 1 + δ)
where δ = δ(a/b), D = D(a/b)
```

This is positive iff D > -(1+δ)/2. For the pair to contribute negatively, D must be sufficiently negative relative to δ.

### Fact 4: Negative B_raw Growth

The negative part of B+C grows as O(N²·log N), not O(N). Per-pair cancellation is insufficient.

---

## REVISED PROOF STRATEGY

### What Still Works

1. **TERM_C ≥ 0.35·dil** — gives a non-circular floor on new_D_sq
2. **Injection identity** — exact, non-circular decomposition of new_D_sq
3. **Computational base** — ΔW ≤ 0 verified for all primes p ≤ 100,000

### What to Try Next (Hours 2-6)

#### Hour 2: Erdős-Turán Approach
- Use ET inequality: Farey discrepancy ≤ (1/H) + Σ|M̂(h)|/h
- Bound each Fourier coefficient separately
- May give conditional bound under RH

#### Hour 3: Per-Denominator SD(D_b) Bounds
- For fixed denominator b, study variance of D(a/b) across reduced a
- Character sum estimates via Gauss sums
- May give uniform bound across denominators

#### Hour 4: Large Sieve Method
- Apply large sieve inequality to the Farey fractions
- Relates to Montgomery-Vaughan results on Farey sequences
- Connection to ζ(1/2 + it)

#### Hour 5: Direct new_D_sq Analysis
- Using injection identity: new_D_sq = Σ (D(f_j) + c_j)²
- Show new_D_sq + B_raw = Σ D(f_j)² + 2Σ D(f_j)·c_j + TERM_C + B_raw
- Note B_raw = 2Σ_{old} D(f)·δ(f); the TERM_C_cross and B_raw may partially cancel

#### Hour 6: Violation Prime Analysis
- The 10 violation primes cluster near p∈{1399,1409,1423,...}
- Check if M(p) is large negative at these primes
- May reveal connection between B+C < 0 and large Mertens function values

---

## SCRIPTS CREATED THIS SESSION

1. **`bc_term_structure.py`** — analyzes per-term t(f) = 2D·δ + δ²; found negative_sum ~ O(N²·log N)
2. **`R_ratio_analysis.py`** — computes R = B_raw/delta_sq; found R ∈ (-3.1, +8.4)
3. **`bc_large_verify.py`** — fast Farey traversal verifying B+C; found 10 violations in [11,2999]
4. **`TERM_C_proof.py`** (from prior session) — verifies TERM_C/dil ≥ 0.35 for p ≤ 8100

---

## SUMMARY

**The claim "B+C > 0 for all primes p ≥ 11" is FALSE.**

First violation: p=1399. Worst violation found: p=2657 with 1+R ≈ -3.1.

The proof of ΔW ≤ 0 must be more subtle than the original decomposition suggested. The non-circular TERM_C bound (≥ 0.35·dil) is established but insufficient. The injection identity decomposition is the right framework; the next step is to show new_D_sq + B_raw ≥ dilution_raw using the exact structure of D(f_j) and c_j values.
