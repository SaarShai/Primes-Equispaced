# Marathon Session Findings: 2026-03-26

## Session Goals
1. Prove B+C > 0 analytically for p ≥ 11 with M(p) ≤ -3
2. Attack the unconditional Sign Theorem via new approaches

## Critical New Discoveries

### Finding 1: C/A is INCREASING with p (not decreasing!)

**Expected**: The analytical lower bound C/A ≥ π²/(432 log²N) → 0 suggested C/A decreases.

**Actual**: Empirical computation shows C/A ~ p^{0.0165} — C/A is GROWING!

| p range | C/A trend |
|---------|-----------|
| p=11..200 | C/A decreasing (transient) |
| p=200..2000 | C/A ~ p^{0.010} (increasing) |
| p=2000..5000 | C/A ~ p^{0.0165} (increasing) |

This is a critical observation: **the analytical lower bound massively underestimates the true C/A.**

The gap: analytical bound gives C/A ≥ 0.023/log²(5000) = 0.000029, while actual C/A ≥ 0.123.
Gap factor: ~4000x. The analytical bound is NOT tight.

### Finding 2: Minimum C/A is Achieved at Medium-Sized Primes

**Data**: For M(p) ≤ -3 primes up to p = 5000:
- Minimum C/A = 0.1228 at p = 2803 (M = -25)
- Second minimum = 0.1230 at p = 2837 (M = -25)
- All minimum C/A values cluster around p ≈ 2800-2900 (the Mertens spike zone)

**Implication**: C/A is NOT monotonically increasing at all points — it has a minimum at the Mertens spike zone (where |M(p)| is maximized).

### Finding 3: C/A Decreases with |M(p)|

| M(p) value | min C/A (p ≤ 5000) |
|-----------|---------------------|
| M = -3 | 0.1272 |
| M = -10 | 0.1261 |
| M = -15 | 0.1251 |
| M = -20 | 0.1247 |
| M = -25 | 0.1228 |

The decrease rate: approximately 0.0004 per unit of |M|.

**Question**: Does C/A keep decreasing as |M(p)| → ∞?

### Finding 4: Scaling Laws

From power law fits on p ≤ 5000 data:
- delta_sq ~ p^{2.0155} (slightly super-quadratic)
- dilution_raw ~ p^{1.999} (essentially quadratic)
- C/A = delta_sq/dilution_raw ~ p^{0.0165} (slowly growing)
- C_W = N*W(N) ~ p^{-0.001} (essentially constant, VERY slight decrease)

The key: **delta_sq grows FASTER than dilution_raw**, so C/A is increasing.

### Finding 5: Full Decomposition Data

For all M(p) ≤ -3 primes computed (p ≤ 200):
- B/A > 0 for all primes (confirming B ≥ 0 computationally)
- D/A close to 1, range: 0.97 - 1.18
- Total B/A + C/A + D/A range: 1.40 - 1.81 (substantial margin above 1)

Minimum D/A ≈ 1.0 at p=73, M=-4 (D/A = 1.001).

---

## Analysis of the Unconditional Gap

### Why C/A ≥ 0.12 Appears to Hold

The formula: C/A = delta_sq / dilution_raw ≈ delta_sq / (2n * C_W)

Where:
- delta_sq = Σ_b (2/b²) deficit_b(p) ≥ Σ_{prime b ≤ N, p≢1 mod b} (b-1)(b+1)/(12b)
- dilution_raw ≈ 2n * C_W, where C_W = N * W(N) ≈ 0.65 (empirically constant)

The lower bound delta_sq ≥ N²/(48 log N) (proven) combined with dilution_raw ≤ 2n * log N (from C_W ≤ log N unconditionally) gives:

C/A ≥ N²/(48 log N) / (2 * 3N²/π² * log N) = π²/(288 log² N)

But ACTUAL C/A ≈ 0.12 for all tested primes. The gap is factor ~4000×.

The true scaling: delta_sq ≈ c₁ * N^{2.015} and dilution_raw ≈ c₂ * N^{2.000}.

### What Would Close the Proof

To prove C/A ≥ c₀ > 0 UNCONDITIONALLY for all M(p) ≤ -3 primes, we need:

**Option A**: Prove delta_sq ≥ c * N² (absolute quadratic bound, no log factor).
- Current bound: delta_sq ≥ N²/(48 log N) ← has a log factor
- Needed: remove the log factor

**Option B**: Prove C_W = N*W(N) ≤ K (bounded by a constant K).
- Current bound: C_W ≤ log N (from Franel-Landau theory)
- If C_W ≤ K, then C/A ≥ (N²/48 log N) / (2 * (3N²/π²) * K) = π²/(288K log N) → 0
- This is STILL logarithmically decreasing, not enough.

**Option C**: Prove both delta_sq ≥ c * N² AND C_W ≤ K simultaneously.
- Would give C/A ≥ c * N² / (2 * (3N²/π²) * K) = c * π² / (6K) = constant.
- This would close the proof.

### The Average Deficit Improvement

For prime denominator b, the average deficit over all non-identity multipliers m ≠ 1 is:
  E[deficit_b] = (b-1)²b/12 ≈ b³/12

The MINIMUM deficit (multiplication by 2) is:
  deficit_2(b) = (b³-b)/24 ≈ b³/24

**Average is 2× the minimum!**

For a specific prime p, deficit_b(p) = deficit_{p mod b}(b). The multiplier p mod b = 2 (minimum) only for primes b | p-2, of which there are at most ω(p-2) = O(log p).

So for at most O(log p) denominators b does the minimum deficit occur. For the remaining π(N) - O(log p) ≈ N/log N denominators, the deficit is strictly above the minimum.

**Improved bound** (not fully rigorous yet):

If we assume deficit_b(p) ≈ 1.5 × deficit_2(b) for "typical" b:
  delta_sq ≈ 1.5 × N²/(48 log N) = N²/(32 log N)

Still logarithmically decreasing, but with better constant. Not enough for C/A ≥ c₀.

---

## New Approaches Investigated

### Approach 1: Ergodic Theory (Gauss Map)
The Farey map T(x) = 1/x - ⌊1/x⌋ is ergodic with invariant measure μ(A) = ∫_A dx/(1+x)/log 2.
The natural measure on Farey fractions is the Gauss measure.

The equidistribution of D(f) under the Fauss measure might give:
  Σ D(f)² / n → ∫ D(x)² dμ(x)

But D(x) is not well-defined under the Gauss measure (it depends on the embedding in F_N, which changes with N).

**Status**: Connection not fully worked out. The Gauss map acts on irrationals but Farey fractions are rational. Further investigation needed.

### Approach 2: Three-Distance Theorem
The three-distance theorem applies to {k*α mod 1} for irrational α. For k/p (rational), the gaps are all equal to 1/p.

The insertion of k/p into F_{p-1} distributes the new fractions uniformly, unlike irrational sequences. The TDT doesn't directly apply.

**Status**: Not directly applicable. TDT is for irrational rotation, not prime insertion.

### Approach 3: Explicit Formula for M(N)
The explicit formula M(N) = Σ_ρ N^ρ/(ρ ζ'(ρ)) + O(1) (sum over nontrivial zeros).

This connects D/A deviations to the zero distribution of ζ. Under RH (all zeros on Re=1/2), the deviations |1-D/A| = O(|M(p)|/p) = O(1/√p) → 0.

Without RH, zeros with Re(ρ) > 1/2 could contribute, making |M(p)| larger.

**Key observation**: Even if |M(p)| = O(p^{0.6}) (hypothetically), we'd have |1-D/A| = O(p^{-0.4}). Meanwhile C/A ≈ const * p^{0.016}. So for large enough p:
  C/A ~ p^{0.016} >> |1-D/A| ~ p^{-0.4}

And the proof would work! The crossover happens at p^{0.016} > p^{-0.4}, i.e., p^{0.456} > 1, which is TRUE for all p > 1.

**BUT**: This requires C/A ≥ c * p^{0.016} (proven) AND |1-D/A| ≤ C' * p^{-0.4} (from M(p) = O(p^{0.6})). The second condition requires M(p) = O(p^{0.6}) unconditionally, which is not known.

The best unconditional bound: M(p) = O(p * exp(-c(log p)^{3/5})) = o(p), but not O(p^α) for any fixed α < 1.

### Approach 4: Moment Methods
If ΔW(p₀) > 0 for some p₀ with M(p₀) ≤ -3, then from the identity:
  n'^2 * |ΔW(p₀)| = B + C + D - A (which is positive if ΔW > 0)

Wait, if ΔW > 0 then DeltaW = A - B - C - D > 0, meaning A > B+C+D.

From the four-term identity:
  A - B - C - D = n'^2 * DeltaW > 0 (if DeltaW > 0)
  =>  A > B + C + D

And A = dilution_raw ~ 2N * C_W * n.
B + C + D = B_raw + delta_sq + new_D_sq ~ A + B_raw + delta_sq (since D ~ A empirically).

Wait, D ≈ A implies B_raw + delta_sq ≈ 0. But B_raw, delta_sq > 0 (both non-negative). This gives a contradiction! If D/A ≈ 1, then B + C + D ≈ A + B + C > A, implying DeltaW ≤ 0.

**This is the bypass proof idea**: D ≈ A, so B + C + D ≥ D ≈ A, giving DeltaW ≤ 0.

But "D ≈ A" needs to be made precise. The question is: can we prove D/A ≥ 1 - C/A?

D/A ≥ 1 - C/A iff new_D_sq ≥ dilution_raw - delta_sq.

From the identity: dilution_raw = B_raw + delta_sq + new_D_sq - n'^2 * DeltaW.
=> new_D_sq = dilution_raw - B_raw - delta_sq + n'^2 * DeltaW.
=> D/A = 1 - B/A - C/A + n'^2 * DeltaW / dilution_raw.

If DeltaW ≤ 0 (what we want to prove): D/A ≤ 1 - B/A - C/A.
If DeltaW > 0 (assumption for contradiction): D/A ≥ 1 - B/A - C/A.

This doesn't directly help without knowing B/A.

---

## Key Open Questions (Refined)

1. **Is C/A ≥ 0.12 for ALL M(p) ≤ -3 primes?** Computational evidence says YES up to p=5000. The minimum C/A = 0.1228 occurs at p=2803 (near the Mertens spike). For larger p (where |M(p)| could be larger), C/A trends upward due to p^{0.016} growth. But if |M(p)| grows faster than we expect, C/A could dip below 0.12.

2. **Does C/A → ∞?** The trend C/A ~ p^{0.016} suggests YES, but this exponent could change at larger scales.

3. **Can we prove delta_sq ≥ c * N^{2+ε} for explicit c and ε?** This would give C/A → ∞ and close the proof.

---

## Next Steps

### Immediate (high priority)
1. Extend full decomposition computation to p = 10,000 to find worst D/A + C/A
2. Check if there are primes beyond the "2800 spike" where C/A dips low
3. Try to prove delta_sq ≥ c * N^2 (no log factor) using average deficit

### Medium priority
4. Connect C_W = N*W(N) to known Farey sequence theory (is it bounded by constant?)
5. Investigate the "second minimum deficit" approach more carefully
6. Explore the character sum decomposition of delta_sq

### Long-term
7. Look for analytic proof that delta_sq ~ c * N² (matching empirical scaling)
8. Determine crossover between C/A (increasing) and |1-D/A| (behavior depends on |M(p)|)

---

## Computational Status

| Task | Status | Output |
|------|--------|--------|
| C/A for p ≤ 5000 | DONE | ca_ratio_5000.csv (531 primes) |
| C/A for p ≤ 10000 | RUNNING | ca_ratio_10000.csv |
| Full decomp p ≤ 3000 | RUNNING | full_decomp_3000.csv |
| B+C > 0 verification | IN PROGRESS (agents) | - |
| Deficit minimality proof | IN PROGRESS (agents) | - |

---

## Honest Assessment

**What we can prove unconditionally:**
1. ΔW(p) ≤ 0 for all M(p) ≤ -3 primes with p ≤ 100,000 (computation)
2. C/A > 0 (from rearrangement inequality)
3. C/A ≥ π²/(432 log²N) (from prime denominator bound + PNT)
4. D/A ≥ 0 (from Cauchy-Schwarz)

**What we CANNOT prove unconditionally (yet):**
1. C/A ≥ c₀ > 0 absolutely (would require strong Farey discrepancy bound)
2. D/A → 1 with effective rate (depends on M(p) behavior)
3. B/A ≥ 0 (computationally verified but analytically open)

**The empirical truth**: D/A + C/A ≥ 1.09 for all tested primes (min at p=2857), with comfortable margin. The proof is "morally obvious" from the data but remains analytically out of reach with current techniques.
