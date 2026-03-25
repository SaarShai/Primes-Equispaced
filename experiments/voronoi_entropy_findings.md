# Voronoi Entropy Monotonicity for Farey Sequences

**Date**: 2026-03-24
**Code**: `experiments/voronoi_entropy_proof.py`
**Status**: THEOREM (proved, not merely conjectured)

---

## Result

**Theorem.** The Shannon entropy of the arc-length distribution of the Farey sequence F_N on the unit circle is strictly increasing in N. That is, for all N >= 2:

    H(F_{N+1}) > H(F_N)

where H(F_N) = -sum_i w_i * log(w_i), and the w_i are the arc lengths between consecutive Farey fractions placed on the circle [0,1).

---

## Verification

Verified computationally for N = 2 to 1000 with zero violations.

| N   | H(F_N)     | |F_N| (points on circle) |
|-----|------------|-------------------------|
| 100 | 7.7603     | 3,044                   |
| 200 | 9.1460     | 12,232                  |
| 500 | 10.9713    | 76,116                  |
| 1000| 12.3557    | 304,192                 |

Smallest entropy increase observed: delta_H = 8.06e-04 at N = 990 (a highly composite number with phi(990) = 240).

---

## Proof

The proof is elementary and relies on a single key insight:

### Key Insight: No Renormalization Effect

When fractions are placed on the circle [0,1), the arc lengths automatically sum to 1. This means inserting a new fraction merely SPLITS an existing arc into two sub-arcs, without changing any other arc. The total "budget" (perimeter = 1) is unchanged.

This is fundamentally different from Shannon entropy of a probability distribution on a growing alphabet, where adding a new category forces renormalization of all existing probabilities.

### Proof Steps

1. **Setup.** F_N on the circle has arcs w_1, ..., w_n with sum(w_i) = 1. Entropy H = -sum w_i log(w_i).

2. **Transition F_N to F_{N+1}.** We add phi(N+1) >= 1 new fractions (those a/(N+1) with gcd(a, N+1) = 1).

3. **Each insertion splits one arc.** A new fraction falling in arc w splits it into w_1 + w_2 = w. The entropy change from this split is:

       Delta = w * h(w_1/w)

   where h(t) = -t*log(t) - (1-t)*log(1-t) is the binary entropy function. Since 0 < w_1/w < 1, we have h(w_1/w) > 0, so Delta > 0.

4. **Total change is the sum of splits.** Since arc lengths sum to 1 before and after, there is no renormalization effect. The total entropy change equals the sum of individual split contributions, all strictly positive.

5. **Conclusion.** H(F_{N+1}) - H(F_N) = sum of phi(N+1) strictly positive terms > 0.  **QED.**

### Numerical Confirmation of Proof Mechanism

The ratio (sum of split effects) / (actual delta_H) equals 1.0000000000 to 12+ decimal places for every N from 2 to 150. This confirms there is no hidden renormalization term.

---

## Why Entropy Behaves Differently from Wobble

The wobble W(N) = sum |w_i - 1/n| is NOT monotonically decreasing. It has 261 violations out of 499 steps (N=2 to 500). Yet entropy H(N) has ZERO violations.

**The fundamental difference:**

- **Entropy** depends only on arc lengths through -x*log(x). Splitting an arc always increases entropy. The mechanism is local and additive.

- **Wobble** compares arc lengths to 1/n, where n = |F_N| changes at each step. When n increases, the "target" 1/n shifts, and arcs that were close to 1/(n-1) are now farther from 1/n. This renormalization effect can increase wobble.

The correlation between delta_H and delta_W is only r = 0.66 -- they capture different aspects of uniformity.

---

## Entropy Increment Scaling

For primes p, the entropy increment scales approximately as:

    delta_H(F_p) ~ C / p

with the product delta_H * p converging to approximately 2.95. The smallest increments occur at highly composite numbers with relatively small phi(N)/N ratios.

**Corollaries:**

1. H(F_N) is bounded above by log(|F_N| - 1) and strictly increasing, hence convergent.

2. H(F_N) / log(|F_N|) -> 1 as N -> infinity (Farey equidistribution).

---

## Literature Status

Web searches for "Farey sequence entropy monotone" and related terms returned no matching results. The strict monotonicity of Voronoi entropy for Farey sequences does not appear to be a known theorem.

Related but distinct results:
- The Franel-Landau theorem connects Farey sequence discrepancy to the Riemann Hypothesis
- Shannon's monotonicity problem (Artstein-Ball-Barthe-Naor 2004) proves entropy increases for normalized sums of i.i.d. random variables -- a completely different setting
- Equidistribution of Farey sequences is classical, but the strict monotonicity of entropy at every single step is a sharper statement

**Assessment: This appears to be a new result.** The proof is elementary (one paragraph, using only strict concavity of -x*log(x)), but the observation that no renormalization occurs on the circle seems to be novel. In the interval setting (not on the circle), the situation would be more complicated because the "boundary arcs" would need different treatment.

---

## Connection to the Prime Circle Project

This result complements the wobble analysis:

1. **Wobble W(N) is non-monotone** -- it sometimes increases at composites and even at some primes. This is the "information paradox" explored in earlier experiments.

2. **Entropy H(N) is strictly monotone** -- it always increases. This gives a clean, provable uniformity measure for Farey sequences.

3. **The fingerprint density (r = -0.9963 with delta_W)** and the spectral Mertens identity (L_1 = M(N) + 1) remain the key connections to the Mertens function and RH.

4. **Entropy provides a one-sided bound**: since H always increases, the arc-length distribution is always "spreading out" in the entropy sense, even when wobble temporarily increases.
