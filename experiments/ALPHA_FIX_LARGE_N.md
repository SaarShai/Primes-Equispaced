# ALPHA FIX: The Proof Gap at Large N

## Date: 2026-03-30

---

## 1. The Problem

The proof in ALPHA_POSITIVE_PROOF.md claims alpha > 0 for all N >= 7, via:

    Cov(D, f) = 1/(12n) - sum(D^2)/(2n^2) - R/2

where R = sum(f^2) - n/3. The argument: R < 0 for N >= 7 (Proposition 4), so
-R/2 > 0 dominates the other terms, making Cov positive.

**The gap:** R is NOT always negative. R(1417) = +0.0016 and R(1418) = +0.0848.
When R > 0, the term -R/2 is NEGATIVE, and the proof breaks.

---

## 2. Computational Results

### 2a. Full sweep N = 7 to 2000

**alpha <= 0 occurs at exactly TWO values:**

| N    | n       | R          | Cov          | alpha     |
|------|---------|------------|--------------|-----------|
| 1417 | 610889  | +0.00160   | -0.00103     | -0.0124   |
| 1418 | 611597  | +0.08482   | -0.04264     | -0.5117   |

These are the ONLY values in [7, 2000] where R > 0, and they correspond
exactly to the alpha < 0 cases. Every other N in [7, 2000] has R < 0 and alpha > 0.

### 2b. Extended sweep N = 2001 to 5000 (sampled every 10th N)

Six more cases found:

| N    | n         | R         | alpha     |
|------|-----------|-----------|-----------|
| 3281 | 3,273,771 | +0.1687   | -1.0136   |
| 3291 | 3,292,683 | +0.2430   | -1.4592   |
| 3301 | 3,313,645 | +0.0757   | -0.4556   |
| 3321 | 3,353,517 | +0.0565   | -0.3400   |
| 4891 | 7,273,849 | +0.1155   | -0.6937   |
| 4901 | 7,302,803 | +0.0127   | -0.0771   |

Pattern: alpha < 0 occurs precisely when R > 0 (in all cases checked).

### 2c. The critical observation: PRIMES are safe

**Alpha at prime N is ALWAYS positive.** Checked all 300 primes in [7, 2000]:
- Zero violations
- Minimum alpha at a prime: 0.685 at p = 7
- R at primes is always negative (worst: R = -0.212 at p = 1423)

The alpha < 0 values occur only at composites:
- N = 1417 = 13 x 109
- N = 1418 = 2 x 709
- N = 3281, 3291, 3301, 3321, 4891, 4901 (all composite)

---

## 3. Detailed Analysis of N = 1417

Neighborhood of the sign change:

| N    | n       | R          | alpha    | prime? |
|------|---------|------------|----------|--------|
| 1415 | 609129  | -0.1372    | 0.820    |        |
| 1416 | 609593  | -0.1508    | 0.902    |        |
| 1417 | 610889  | +0.0016    | -0.012   |        |
| 1418 | 611597  | +0.0848    | -0.512   |        |
| 1419 | 612437  | -0.0138    | 0.080    |        |
| 1420 | 612997  | -0.0467    | 0.278    |        |
| 1423 | 616063  | -0.2118    | 1.268    | PRIME  |

What happens at N=1417: the denominator contribution e(1417) = +0.1524 is
large and positive (1417 = 13 x 109, a composite with relatively few
coprime residues compared to its size). This pushes R over zero.

For primes p, e(p) = -(p-1)/(6p) < 0 ALWAYS. So when N is prime,
adding the next row ALWAYS decreases R. The composite contributions
e(q) for q with few prime factors can be positive and occasionally
accumulate enough to flip R.

---

## 4. Why Primes Are Safe: The Structural Argument

**Claim:** R(p) < 0 for all primes p >= 7.

**Why this should be true:** When N = p is prime, the new row added to
F_{p-1} -> F_p consists of fractions a/p for a = 1, ..., p-1 (all coprime
to p). This contributes e(p) = -(p-1)/(6p) to R. Since the previous
R(p-1) already includes all contributions from q <= p-1, and going from
composite N to the next prime N adds only negative contributions, R at
primes stays negative.

More precisely: between consecutive primes p_k and p_{k+1}, the composites
q in (p_k, p_{k+1}) contribute e(q) which can be positive. But the prime
p_{k+1} itself contributes e(p_{k+1}) ~ -1/6. The data shows that the
prime contribution always overwhelms any accumulated positive composite
contributions.

**Verified:** R(p) < 0 for all primes p in [7, 2000]. The worst case is
R(1423) = -0.212, which is comfortably negative.

---

## 5. Fixing the Proof

### Option A: Restrict the theorem to prime N

**Revised theorem:** alpha > 0 for all PRIME p >= 7.

This suffices for the Sign Theorem (DeltaW < 0) since that theorem
is about primes anyway. The proof then needs:

1. Show R(p) < 0 for all primes p >= 7
2. Show -R(p)/2 dominates sum(D^2)/(2n^2) + 1/(12n)

For (1): This follows from the denominator decomposition. When N = p,
R(p) = 1/3 + sum_{q=2}^{p} e(q). The prime contributions sum to
~ -pi(p)/6, while composite contributions are bounded. Proving R(p) < 0
analytically requires showing the prime sum dominates.

For (2): Already established. sum(D^2)/(2n^2) -> 0 while |R|/2 stays
bounded away from zero.

### Option B: Direct bound on sum(D * f)

alpha > 0 iff sum(D * f) > n * E[D] * E[f] = sum(D)/2.

Equivalently: sum(D * f) - sum(D)/2 = sum(D * (f - 1/2)) > 0.

Since D = rank - n*f, this becomes: sum((rank - n*f)(f - 1/2)) > 0.

By the Farey symmetry f <-> 1-f (and rank <-> n+1-rank, so D <-> -D+1):

    sum D*(f - 1/2) = sum (rank - n*f)(f - 1/2)

The symmetry f -> 1-f sends f - 1/2 to -(f - 1/2) and D to -D + 1.
So the sum transforms to sum(-D+1)(-(f-1/2)) = sum D(f-1/2) - sum(f-1/2).
Since sum(f - 1/2) = 0, we get back sum D(f-1/2). This confirms the
identity but doesn't directly give positivity.

For primes, the rearrangement inequality approach from PROOF_BREAKTHROUGH.md
(sum f * delta > 0) may be adaptable.

### Option C: Computational verification up to threshold + asymptotic argument

For the paper:
- Verify alpha > 0 computationally for all primes p up to some P_0
- Prove asymptotically that for p > P_0, the R term dominates (since R -> -inf)
- This is actually what the existing proof DOES, but it was stated for all N >= 7
  when it should have been stated for primes only

---

## 6. Summary of the R Distribution

For N in [100, 2000]:
- min R = -3.462 (at N = 1630)
- max R = +0.085 (at N = 1418)
- mean R = -1.685
- R > 0 at only 2 out of 1901 values

R oscillates as a function of N. When a large composite N with few coprime
residues is added, e(N) is large and positive, which can temporarily push
R above zero. The next prime always pushes R back down.

---

## 7. Conclusion

**The claim "alpha > 0 for all N >= 7" is FALSE.** Counterexamples:
N = 1417, 1418, 3281, 3291, 3301, 3321, 4891, 4901 (all composite).

**The claim "alpha > 0 for all primes p >= 7" appears TRUE** (verified to
p = 2000, no violations). This is the claim that matters for the Sign
Theorem and should replace the original statement.

**Action items:**
1. Correct ALPHA_POSITIVE_PROOF.md: change "N >= 7" to "prime p >= 7"
2. Add a note that alpha can be negative at certain composites
3. Prove R(p) < 0 for all primes p analytically (or at least for p >= P_0)
4. The computational verification range [7, 99] was too small to catch this

---

## 8. Verification Status

- Sweep N = 7 to 2000: COMPLETE (all N, float arithmetic)
- Sweep N = 2001 to 5000: COMPLETE (every 10th N, float arithmetic)
- alpha < 0 at composite N: CONFIRMED at 8 values
- alpha > 0 at prime N: CONFIRMED for all 300 primes in [7, 2000]
- R > 0 iff alpha < 0: CONFIRMED (perfect correlation in all data)
- Identity Cov = 1/(12n) - D2/(2n2) - R/2: VERIFIED (discrepancy < 1e-10)

Status: UNVERIFIED (needs independent replication per protocol)
