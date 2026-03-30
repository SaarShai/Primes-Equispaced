# B EXACT AUDIT -- Definition-Verified Exact Computation

**Date:** 2026-03-30
**Method:** All arithmetic via Python `fractions.Fraction` -- zero floating point
**Script:** `b_exact_audit.py`

---

## Definitions Used (from `paper/main.tex`)

| Symbol | Definition | Source |
|--------|-----------|--------|
| F_N | Farey sequence of order N = p-1 | Sec 2 |
| n | \|F_N\| | Sec 2 |
| n' | \|F_p\| = n + (p-1) | Eq (4term) |
| D(f_j) | j - n * f_j (0-indexed rank) | Def 1 |
| delta(f) | f - {pf} = (a - (pa mod b))/b for f=a/b | Def 2 |
| B' | 2 * sum_{f in F_N, denom>1} D(f) * delta(f) | unnormalized cross term excl endpoints |
| C' | sum_{f in F_N, denom>1} delta(f)^2 | unnormalized shift-squared excl endpoints |

**Key note on delta:** Both `f - {pf}` and `(a - (pa mod b))/b` were computed independently and verified to be identical for every fraction at every prime tested.

---

## TASK 1: B' and C' for All Primes

### Exact Values

| p | N | n | n' | M(N) | M(p) | B' > 0? | B'/C' |
|---|---|---|-----|------|------|---------|-------|
| 11 | 10 | 33 | 43 | -1 | -2 | **NO** | -0.5177 |
| 13 | 12 | 47 | 59 | -2 | -3 | YES | 0.1199 |
| 17 | 16 | 81 | 97 | -1 | -2 | **NO** | -0.2773 |
| 19 | 18 | 103 | 121 | -2 | -3 | YES | 0.3320 |
| 23 | 22 | 151 | 173 | -1 | -2 | YES | 0.1325 |
| 29 | 28 | 243 | 271 | -1 | -2 | YES | 0.4296 |
| 31 | 30 | 279 | 309 | -3 | -4 | YES | 1.5560 |
| 37 | 36 | 397 | 433 | -1 | -2 | YES | 0.4213 |
| 43 | 42 | 543 | 585 | -2 | -3 | YES | 1.3535 |
| 47 | 46 | 651 | 697 | -2 | -3 | YES | 1.5616 |
| 53 | 52 | 831 | 883 | -2 | -3 | YES | 1.3997 |
| 71 | 70 | 1495 | 1565 | -2 | -3 | YES | 1.8179 |
| 97 | 96 | 2807 | 2903 | 2 | 1 | **NO** | -0.2109 |

### Critical Finding: B' is NOT always positive

**B' < 0 at p = 11, 17, 97.**

- p=11: M(N)=-1 (too small Mertens magnitude)
- p=17: M(N)=-1 (too small Mertens magnitude)
- p=97: M(N)=+2 (positive Mertens -- these are the primes where wobble *improves*, so B's sign is less relevant)

**B' > 0 for all primes where M(N) <= -2.** This is consistent with the paper's Observation that B > 0 for all tested primes with M(p) <= -3 (equivalently M(p-1) <= -2 for most of these).

### Endpoint Contributions

For all primes: D(0)*delta(0) = 0, D(1)*delta(1) = -1.
Therefore: B_full = B' - 2 (exactly).

### Cross-Term Identity Verified

The paper's Theorem (eq cross-term): `sum D(f)*delta(f)^2 = -1/2 * sum delta(f)^2 - 1/2`

**HOLDS EXACTLY for all 13 primes tested.** (Sums over all of F_N including endpoints.)

---

## TASK 2: Mobius Decomposition

### The Exact Identity

Defining R(f) = sum_{d<=N} mu(d) * sum_{m<=N/d} {f*m}, the following identity holds:

**B' + C' = -2 * sum_{f, denom>1} R(f) * delta(f)**

**Verified EXACTLY for all 13 primes.** (Interior sums only -- excluding b=1 endpoints.)

For full sums (including endpoints): B_full + C_full + 2*sum_R_delta_full = -1 (not 0). The -1 comes from the endpoint f=1 contributing R(1)*delta(1) = R(1)*1 = R(1), and B_full includes the D(1)*delta(1) = -1 term. This is consistent.

### Correction Term

Define: **correction = sum_{f, denom>1} R(f)*delta(f) - M(N)*C'/2**

| p | M(N) | correction/C' |
|---|------|--------------|
| 11 | -1 | 0.2589 |
| 13 | -2 | 0.4401 |
| 17 | -1 | 0.1386 |
| 19 | -2 | 0.3340 |
| 23 | -1 | -0.0662 |
| 29 | -1 | -0.2148 |
| 31 | -3 | 0.2220 |
| 37 | -1 | -0.2106 |
| 43 | -2 | -0.1767 |
| 47 | -2 | -0.2808 |
| 53 | -2 | -0.1999 |
| 71 | -2 | -0.4089 |
| 97 | 2 | -1.3946 |

### The Correct Formula (DERIVED AND VERIFIED)

From the exact identity B' + C' = -2*sum_R_delta, substituting the correction definition:

```
B' = -(1 + M(N)) * C' - 2 * correction
```

For M(N) < 0, this simplifies to:

```
B' = (|M(N)| - 1) * C' - 2 * correction
```

**This formula is VERIFIED EXACTLY for all primes with M(N) < 0 (p = 11 through 71).**

For p=97 where M(N) = +2 > 0, the general form B' = -(1+M(N))*C' - 2*correction = -3*C' - 2*correction still holds (it reduces to the base identity).

### The User's Formula Was Wrong

The user proposed: `B' = (|M(N)| - 2) * C' - 2 * correction`

The correct formula is: `B' = (|M(N)| - 1) * C' - 2 * correction`

**The error is exactly -C' (off by one unit of C').** This is because the derivation gives -(1+M(N)) for the coefficient, and for M(N) < 0: -(1+M(N)) = |M(N)| - 1, not |M(N)| - 2.

---

## TASK 3: M(p) = -3 Primes

For all M(p) = -3 primes in our test set, M(N) = M(p-1) = -2.

| p | M(N) | M(p) | B' > 0? | correction/C' | \|corr/C'\| < 1/2? |
|---|------|------|---------|---------------|-------------------|
| 13 | -2 | -3 | YES | 0.4401 | YES |
| 19 | -2 | -3 | YES | 0.3340 | YES |
| 43 | -2 | -3 | YES | -0.1767 | YES |
| 47 | -2 | -3 | YES | -0.2808 | YES |
| 53 | -2 | -3 | YES | -0.1999 | YES |
| 71 | -2 | -3 | YES | -0.4089 | YES |

**All M(p)=-3 primes have |correction/C'| < 1/2.** This means:

Using the corrected formula B' = (|M(N)|-1)*C' - 2*correction = C' - 2*correction (since |M(N)|=2):

- B' > 0 iff C' - 2*correction > 0 iff correction < C'/2 iff correction/C' < 1/2
- Since |correction/C'| < 1/2 for all tested M(p)=-3 primes, B' > 0 for all of them.

**Note:** p=71 has correction/C' = -0.409, getting close to the -1/2 boundary. Worth monitoring for larger M(p)=-3 primes.

### B' > 0 Sufficient Condition (Corrected)

For B' > 0 when M(N) < 0, we need:

```
(|M(N)| - 1) * C' > 2 * correction
```

When |M(N)| >= 2 (i.e., M(N) <= -2), the leading term is at least C', so B' > 0 provided correction/C' < (|M(N)|-1)/2.

For M(N) = -1 (i.e., |M(N)| = 1), the leading term vanishes: B' = -2*correction. So B' > 0 requires correction < 0.

This explains why B' < 0 at p=11 (M(N)=-1, correction=0.259 > 0) and p=17 (M(N)=-1, correction=0.139 > 0), but B' > 0 at p=23 and p=29 (M(N)=-1, correction < 0).

---

## Summary of Verified Facts

1. **B' > 0 is FALSE in general** -- it fails at p=11, 17, 97.

2. **B' > 0 for all tested primes with M(N) <= -2** (equivalently, M(p) <= -3 for most cases). This is the claim the paper actually makes.

3. **The exact identity B' + C' = -2 * sum R*delta holds** for interior sums (excluding b=1 endpoints). Verified exactly at all 13 primes.

4. **The cross-term identity sum D*delta^2 = -1/2 * sum delta^2 - 1/2 holds exactly.**

5. **The correct Mobius decomposition formula is:**
   ```
   B' = -(1 + M(N)) * C' - 2 * correction
   ```
   where correction = sum_R_delta - M(N)*C'/2.
   For M(N) < 0: B' = (|M(N)| - 1)*C' - 2*correction.
   **The previously proposed formula with (|M(N)|-2) is off by -C'.**

6. **For M(p)=-3 primes: |correction/C'| < 1/2 for all tested** (6 primes up to p=71).

7. **B' < 0 when M(N) = -1 and correction > 0** (p=11, 17). The sign of B' at M(N)=-1 depends on the sign of the correction term.
