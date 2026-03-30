# Decorrelation via Dedekind Sums: Analysis

**Date:** 2026-03-30
**Status:** Approach evaluated. Main decomposition is CIRCULAR, but new structural findings emerge.

---

## 1. Setup and Definitions

For prime p, Farey sequence F_{p-1} with |F_{p-1}| = n:
- D(f) = rank(f) - n*f (counting discrepancy)
- delta(f) = f - {p*f} (displacement)
- B = 2 * sum_f D(f)*delta(f)
- C = sum_f delta(f)^2
- W_new - W_old = B + C

We want to prove B >= 0 for all primes with M(p) <= -3.

## 2. The D_err Decomposition (CIRCULAR)

**Proposed approach:** Define D_err = D - alpha*(f - 1/2) and express B through decorrelation.

**Result:** After algebra:
```
sum D_err * delta = B/2 - alpha*C/2
```
Therefore B = 2*sum(D_err*delta) + alpha*C, which is just a rearrangement of B. The decorrelation approach IS the B >= 0 problem in disguise. **Cannot separate them.**

## 3. The Mobius Remainder R(f)

### Identity (verified computationally):

Using Mobius inversion on the Farey counting function:
```
rank(a/b) = 1 + sum_{c=1}^{N} sum_{e|c} mu(e) * floor(ca/(be))
```

Splitting floor(x) = x - {x}:
```
D(a/b) = 1 - f - R(f)
```
where:
```
R(a/b) = sum_{c=1}^{N} sum_{e|c} mu(e) * {ca/(be)}
```

### Key identity (verified exactly for p <= 300):
```
B + C = -2 * sum R(f)*delta(f) + 1
```
Note the +1 correction (from the constant term "1" in D = 1 - f - R).

## 4. The Mertens Main Term Decomposition

**Idea:** Write sum(R*delta) = M(p-1)*C/2 + correction, then bound correction.

**For M(p) <= -3:** Typically M(p-1) <= -2, so main_term = M(p-1)*C/2 <= -C.
Need: correction <= C/2 for B >= 0.

### Computation results (148 primes with M(p) <= -3, up to p = 1933):

| Statistic | Value |
|-----------|-------|
| Max correction/C | +0.667 (p=13) |
| Min correction/C | -3.837 |
| Mean correction/C | -1.696 |
| correction/C < 0.5 always? | **NO** (fails at p=13) |
| B >= 0 always? | **NO** (fails at p=13, B = -1.30) |

### Critical finding: The correction is NOT bounded by C/2.

For small primes (p=13), correction/C = +0.667 > 0.5, and indeed B < 0 there.
For larger primes, correction/C is typically negative and large in magnitude (down to -3.8).

**The Mertens decomposition does NOT give a useful bound on correction.**

## 5. Why the Correction Grows

The correction term involves:
```
correction = sum_{c=1}^{N} sum_{e|c, e>=2} mu(e) * sum_{a/b in F_N} {ca/(be)} * delta(a/b)
```

This is NOT smaller than the d=1 term. As p grows, the higher-order divisor terms accumulate and dominate. The Mobius sieve does NOT damp them sufficiently.

The ratio correction/C grows roughly like log(p) for M(p) = -3 primes (where M(p-1) = -2), because the "main term" is only -C while B grows faster.

## 6. Dedekind Sum Connection

For each denominator b, the sum of {pa/b} over a coprime to b relates to the Dedekind sum s(p, b).

**Verified:** Dedekind reciprocity s(h,k) + s(k,h) = (h/k + k/h + 1/(hk))/12 - 1/4 holds exactly for all tested cases.

**However:** The per-denominator contributions sum_Rd_b = sum_{a: gcd(a,b)=1} R(a/b)*delta(a/b) do NOT decompose cleanly into Dedekind sums because R involves ALL c from 1 to N, not just c = b.

The Dedekind structure applies within a single denominator's fractional parts, but our R sums ACROSS denominators. Dedekind reciprocity cannot be applied directly to bound the correction.

## 7. Structural Insight: The Off-by-One

The exact identity is:
```
B + C = -2 * sum_f R(f)*delta(f) + 1
```

The "+1" comes from D(f) = 1 - f - R(f) rather than D(f) = -f - R(f).

Expanding:
```
B + C = 2*sum(1-f-R)*delta + sum(delta^2)
      = 2*sum(delta) - 2*sum(f*delta) - 2*sum(R*delta) + sum(delta^2)
```

We verified: 2*sum((1-f)*delta) + sum(delta^2) = 1 exactly (not 0).

This means sum(delta) = 1/2 + sum(f*delta) - sum(delta^2)/2 is a non-trivial identity.

## 8. What Actually Controls B >= 0

From the data, B >= 0 for all M(p) <= -3 primes with p >= 19. The mechanism is:

1. **B grows like p^2** while **C grows like p** (roughly).
2. **B/C increases** with p, making the bound easier for larger primes.
3. The only failure is p = 13, where |M(p)| = 3 is the bare minimum threshold and the Farey sequence is too small for the averaging to kick in.

The real question is not bounding correction/C but understanding why B/C -> infinity.

## 9. Dead Ends and Live Leads

### Dead:
- D_err decorrelation: circular, reduces to B >= 0
- Mertens main term + correction bound: correction is unbounded relative to C
- Dedekind reciprocity on R*delta: R mixes all denominators, can't isolate

### Potentially live:
- **Direct B/C growth rate:** If we can show B = Theta(p^2 * C_M) where C_M depends on M(p), this would give B >= 0 for p large enough
- **Spectral approach:** Fourier expansion of D and delta might give sign information
- **Variance comparison:** B = 2*Cov(D, delta) in a natural measure; the covariance sign might follow from the injection structure

## 10. Conclusion

The Dedekind/Mobius approach to bounding sum(R*delta) does not yield a proof of B >= 0. The correction term in the Mertens decomposition grows faster than C/2, so the sufficient condition correction <= C/2 fails.

The decorrelation approach (expressing D_err in terms of Dedekind sums and using reciprocity) is circular: it reduces to B >= 0 itself.

**B >= 0 remains unproven analytically.** The empirical evidence is overwhelming (every prime p >= 19 with M(p) <= -3 tested up to p = 1933), but no decomposition of R*delta has yielded a tractable bound.

---

**Script:** `experiments/decorr_dedekind_computation.py`
**Connected to:** N2 (Mertens-Wobble correlation), B >= 0 problem
**Classification:** C1 (collaborative, minor novelty) -- the circularity result and structural findings are useful but not publication-grade on their own.
