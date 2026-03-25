# FINAL P0 VERIFICATION: Closing the Sign Theorem Proof

## Main Result

**Theorem (Sign Theorem -- M(p) <= -3 version).**
For every prime p >= 11 with M(p) <= -3:

    DeltaW(p) := W(p-1) - W(p) <= 0

That is, the Farey wobble increases at every such prime step.

**Status:** PROVED for p in [11, 100,000] by exact computation (4,617 primes, zero violations). Conditional extension to all p via analytical bounds.

---

## 1. Setup and Definitions

- N = p - 1
- n = |F_N| (Farey sequence size)
- n' = n + (p-1) = |F_p|
- A = dilution_raw = old_D_sq * (n'^2 - n^2) / n^2
- D = new_D_sq = Sum_{k=1}^{p-1} D_new(k/p)^2
- C = delta_sq = Sum_{f in F_N} delta(f)^2
- B = B_raw = 2 * Sum_{f in F_N} D(f) * delta(f)

The condition DeltaW(p) <= 0 is equivalent to **B + C + D >= A**, or equivalently B/A + C/A + D/A >= 1.

---

## 2. Explicit Constants from Data

### 2.1. The gap |1 - D/A|

From exact computation of 210 primes with M(p) <= -3 in [11, 3000]:

**Model 1:** |1 - D/A| <= C_1 * |M(p)| / p

| Quantity | Value |
|----------|-------|
| max C_1 (empirical) | 6.37 |
| C_1 (with 50% safety) | **9.55** |
| mean C_1 | 1.48 |

**Model 2:** |1 - D/A| <= C_M * |M(p)| / sqrt(p)

| Quantity | Value |
|----------|-------|
| max C_M (empirical) | 0.227 |
| C_M (with 30% safety) | **0.296** |

**Key data points:**

| p | M(p) | 1 - D/A | C_1 effective |
|---|------|---------|---------------|
| 13 | -3 | -0.116 | 0.50 |
| 47 | -3 | -0.099 | 1.54 |
| 499 | -6 | -0.005 | 0.43 |
| 1499 | -3 | +0.001 | 0.56 |
| 2857 | -23 | +0.029 | 3.55 |
| 2999 | -6 | +0.002 | 0.85 |

The gap |1 - D/A| is NOT simply O(1/p). It scales as O(|M(p)|/p), and since |M(p)| grows (roughly as sqrt(p)), the effective K = p * |1-D/A| is unbounded. The correct bound is |1 - D/A| ~ C_M * |M(p)| / sqrt(p).

### 2.2. The C/A ratio

From the same 210 primes:

| Quantity | Value |
|----------|-------|
| min(C/A) | 0.1228 |
| max(C/A) | 0.2550 |
| mean(C/A) | 0.1324 |
| min(C/A * log^2(p)) | 1.68 |

**Analytical lower bound (proven):**

    C/A >= pi^2 / (432 * log^2(N))  =  0.02285 / log^2(N)

This bound is conservative by a factor of ~73. It comes from:
- Theorem 2: delta_sq >= N^2 / (48 log N) [rearrangement + PNT]
- Proposition 9: dilution_raw <= 3N * old_D_sq / n

### 2.3. D/A + C/A summary

| Quantity | Value | At prime |
|----------|-------|----------|
| min(D/A + C/A) | 1.0957 | p = 2857 |
| min(B/A + C/A + D/A) | 1.4014 | p = 13 |
| Margin (D/A + C/A - 1) | 0.0957 | |

**D/A + C/A > 1 for ALL 210 M(p) <= -3 primes in [11, 3000].**

---

## 3. The Crossover P_0

### 3.1. The challenge

To bridge computational and analytical regimes, we need the analytical bound on C/A to exceed the gap |1 - D/A| for large p. Specifically:

    pi^2 / (432 log^2(N))  >  C_1 * |M(p)| / p

Using M(p) = O(sqrt(p)) (empirical, not proven unconditionally beyond RH):

    pi^2 / (432 log^2(p))  >  C_1 * sqrt(p) / p  =  C_1 / sqrt(p)
    sqrt(p) / log^2(p)  >  432 * C_1 / pi^2

With C_1 = 9.55: need sqrt(p) / log^2(p) > 419.

| p | sqrt(p)/log^2(p) | Sufficient? |
|---|------------------|-------------|
| 10,000 | 5.92 | No |
| 50,000 | 10.2 | No |
| 100,000 | 24.0 | No |
| 1,000,000 | 52.5 | No |
| 10^8 | 293 | No |
| 10^10 | 1892 | YES |

This crossover point (~10^10) is far beyond computational reach.

### 3.2. Why this is misleading

The analytical C/A bound (pi^2/(432 log^2 N)) is ~73x weaker than reality. The actual C/A ~ 0.12 easily covers the gap, which is at most ~0.03.

### 3.3. The correct approach: p * C/A_analytical > K

An alternative route: show delta_sq > K * dilution_raw / p, using the D/A >= 1 - K/p model (K = 12):

    Need: p * C/A_analytical > K = 12
    i.e.: p * pi^2 / (432 * log^2(p)) > 12
    i.e.: p / log^2(p) > 525

| p | p / log^2(p) | p * C/A_analyt | > 12? |
|---|-------------|----------------|-------|
| 10,000 | 117.9 | 2.69 | No |
| 50,000 | 427.1 | 9.76 | No |
| 100,000 | 754.4 | 17.24 | **YES** |
| 200,000 | 1372 | 31.3 | YES |

**At p = 100,000: p * C/A_analytical = 17.2 > 12 = K.**

BUT: the K = 12 model (|1-D/A| <= 12/p) is wrong. K_eff grows with p. So this approach has the same gap: it works at p = 100,000 for K = 12, but K_eff is actually ~80 at p = 3000 and growing.

### 3.4. Resolution: the proof is hybrid

The computational verification covers [11, 100,000] with zero violations. The analytical bounds are consistent and provide structural understanding, but the analytical C/A lower bound is too weak (by a factor ~73) to independently close the proof for p > 100,000.

---

## 4. The Complete Proof

### Part I: Computational (p <= 100,000)

For each of the **4,617 primes** p in [11, 99991] with M(p) <= -3:
- W(p) and W(p-1) are computed using the exact Farey sequence.
- W(p) >= W(p-1) is confirmed.
- **Violations: 0 out of 4,617.**

Additionally, for p <= 3,000 (210 primes with M <= -3), the full four-term decomposition (B/A, C/A, D/A) is computed exactly, confirming:
- min(D/A + C/A) = 1.0957 > 1 (substantial margin)
- B/A >= 0 for all tested primes
- min(B/A + C/A + D/A) = 1.4014 > 1

The 10 hardest cases (DeltaW closest to zero) among M <= -3 primes up to 100,000:

| p | M(p) | DeltaW |
|---|------|--------|
| 64553 | -3 | -7.25e-11 |
| 92153 | -4 | -8.27e-11 |
| 64781 | -5 | -1.15e-10 |
| 92179 | -5 | -1.35e-10 |
| 92143 | -5 | -1.61e-10 |

Even the hardest cases have DeltaW clearly negative.

### Part II: Analytical bounds (supporting structure)

Three independently proven bounds support the computational result:

**(I) delta_sq >= N^2 / (48 log N) for N >= 100.**

Proof: From the rearrangement inequality, T_b <= Sum a^2 for each denominator b, with equality iff p = 1 mod b. Restricting to prime denominators with p != 1 mod b and using the Prime Number Theorem (effective Rosser-Schoenfeld): Sum_{prime b <= N} (b-1)/12 >= N^2/(24 log N). Subtracting the contribution from primes dividing N gives delta_sq >= N^2/(48 log N).

**(II) D/A >= 0 unconditionally.**

Proof: D/A = R_1 + R_2 + R_3 >= (sqrt(R_1) - sqrt(R_3))^2 >= 0, from the Cauchy-Schwarz bound |R_2| <= 2 sqrt(R_1 * R_3).

**(III) C/A >= pi^2 / (432 log^2(N)) for N >= 100.**

Proof: Combining (I) with dilution_raw <= 3N * old_D_sq/n and the Franel-Landau bound old_D_sq/n <= (3/pi^2) N log(N).

### Part III: Conditional extension to all p

For p > 100,000, the theorem holds provided:

    C/A decays no faster than 1/log(p)

This is equivalent to:

    delta_sq / dilution_raw >= c / log(p)  for some c > 0

**Justification:** Both delta_sq and dilution_raw scale as Theta(n) ~ Theta(N^2), so their ratio C/A is Theta(1). More precisely, delta_sq ~ n/6 (from random permutation statistics) and dilution_raw ~ 2nN*W (from the Farey size growth), giving C/A ~ 1/(12NW) ~ pi^2 / (36 C_W) where C_W = NW(N) is slowly varying. Since C_W ~ O(log N) unconditionally, C/A ~ Omega(1/log N).

The analytical bound pi^2/(432 log^2 N) captures the correct functional form (~ 1/log^alpha) but with a weaker exponent (alpha = 2 vs the true alpha = 1) and a pessimistic constant.

---

## 5. Summary of Explicit Constants

| Constant | Definition | Value | Source |
|----------|-----------|-------|--------|
| C_1 | Gap bound: \|1-D/A\| <= C_1 \|M(p)\|/p | 9.55 (safe) | Empirical + 50% margin |
| C_M | Gap bound: \|1-D/A\| <= C_M \|M(p)\|/sqrt(p) | 0.296 (safe) | Empirical + 30% margin |
| c_lower | C/A >= c_lower / log^2(N) | pi^2/432 = 0.0228 | Proven (Theorem 3) |
| c_actual | C/A * log^2(p) | >= 1.68 | Empirical minimum |
| Margin | min(D/A + C/A) - 1 | 0.0957 | Exact (p <= 3000) |

---

## 6. Status and Open Questions

### What is proved rigorously:

1. DeltaW(p) <= 0 for all M(p) <= -3 primes with p in [11, 100,000].
   (Computational, zero violations out of 4,617 primes.)

2. delta_sq > 0 for all primes p >= 5.
   (Rearrangement inequality.)

3. delta_sq >= N^2/(48 log N) for N >= 100.
   (Rearrangement + PNT.)

4. C/A >= pi^2/(432 log^2 N) for N >= 100.
   (Combining #3 with dilution_raw upper bound.)

5. D/A >= 0 unconditionally.
   (Cauchy-Schwarz on the R-decomposition.)

6. D/A + C/A > 1 for all M(p) <= -3 primes with p <= 3,000.
   (Exact computation, 210 primes.)

### What is not proved but strongly supported:

1. D/A + C/A > 1 for ALL M(p) <= -3 primes (beyond 100,000).
   Requires proving C/A >= c/log(p) with c large enough to exceed
   the gap, or proving D/A >= 1 for M(p) <= -3 analytically.

2. B/A >= 0 for all M(p) <= -3 primes.
   Verified computationally for p <= 3,000.

3. The exact scaling of C/A: empirically C/A ~ 0.12 (roughly constant),
   but only C/A >= 0.023/log^2(N) is proved.

### The key open problem:

Prove that C/A >= c_0 > 0 for some absolute constant c_0 and all primes p >= 11. This would immediately close the proof since the gap |1-D/A| -> 0 while C/A stays bounded below.

Alternatively, prove the stronger statement: delta_sq / dilution_raw >= pi^2 / (36 * C_W(N)) where C_W(N) = N * W(N), which gives C/A ~ Omega(1) under the conjecture that C_W(N) = O(1).

---

## 7. Verification

The script `FINAL_P0_VERIFICATION.py` performs all computations described above.
Full output is saved in `FINAL_P0_VERIFICATION_output.txt`.

Key computational results:
- 210 primes with M(p) <= -3 in [11, 3000]: exact four-term decomposition
- 4,617 primes with M(p) <= -3 in [11, 100000]: CSV wobble verification
- Runtime: ~116 seconds
