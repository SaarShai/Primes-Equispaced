# Fresh Proof Approaches for B + C > 0

## The Problem Restated

We need: B + C > 0 for primes p >= 11, where B + C = sum(D + delta)^2 - sum(D^2).

Equivalently: ||D + delta||^2 > ||D||^2, i.e., adding the shift delta to D *increases* the L2 norm.

Equivalently: 2<D, delta> + ||delta||^2 > 0, i.e., B + C = 2<D,delta> + C > 0.

Since C = ||delta||^2 > 0, we need: <D, delta> > -||delta||^2 / 2,
or by Cauchy-Schwarz it suffices to show: ||D|| * ||delta|| cos(theta) > -||delta||^2 / 2,
i.e., cos(theta) > -||delta|| / (2||D||).

---

## Approach 1: Fourier Analysis on the Inner Product <D, delta>

**Key idea:** Both D and delta can be expanded in terms of additive characters mod b (for the denominator-b stratum) or in terms of the classical Franel-Landau theory relating Farey discrepancy to exponential sums.

**Why this is promising:** The classical connection between Farey discrepancy and exponential sums (Franel, 1924) gives:

    D(a/b) ~ sum_k c_k e(k a/b)

where the Fourier coefficients c_k involve sums related to the Moebius function and are controlled by zero-free regions of zeta. Meanwhile, delta(a/b) = (a - pa mod b)/b is determined by the action of multiplication by p on (Z/bZ)*, which has a clean Fourier expansion in terms of Dirichlet characters mod b:

    pa mod b = sum_chi chi(p) * (character sum involving a)

The inner product <D, delta> then becomes a *double character sum* which may factor or simplify. The point is that D encodes global ordering information (rank in the full Farey sequence) while delta encodes local multiplicative information (p acting on residues). These live in "orthogonal worlds" --- D is about additive/ordering structure, delta is about multiplicative structure. Their inner product should be small precisely because of this mismatch.

**Concrete path:**
1. Write D(a/b) using the standard Franel representation involving floor functions and Euler's totient sums.
2. Write delta(a/b) using discrete Fourier transform on (Z/bZ)*.
3. Compute <D, delta> by exchanging sums. The cross terms should reduce to Ramanujan sums or Kloosterman-type sums.
4. Bound |<D, delta>| using Weil's bound on Kloosterman sums, giving |<D, delta>| = O(p^{3/2+eps}).
5. Compare with C = ||delta||^2 which should be Theta(p^2) or larger, giving B + C > 0 for large p.
6. Handle small p (11 <= p <= bound) by direct computation.

**What makes this special:** The interaction between Farey ordering (additive) and multiplication by p (multiplicative) is exactly the setting where character sum bounds excel. This is the Farey analogue of bounding correlations between arithmetic functions.

---

## Approach 2: Variance Domination via the Permutation Structure

**Key idea:** For each denominator b, delta acts as a *signed permutation displacement*. The map a -> pa mod b is a permutation of residues coprime to b, and delta measures how far each element moves. We can use the theory of random permutations to show that delta is "generic enough" that C dominates |B|.

**Why this is promising:** The sum-zero property (Fact 3: sum of delta over each denominator class is 0) means delta has no "DC component" within each class. It's purely oscillatory. Meanwhile, D has a smooth part (Fact 4: average -1/2 per class) and an oscillatory part. The cross term B = 2<D, delta> involves only the oscillatory part of D dotted with delta.

**Concrete path:**
1. Decompose D = D_smooth + D_osc where D_smooth = -1/2 within each class.
2. Then B = 2<D_smooth, delta> + 2<D_osc, delta> = 0 + 2<D_osc, delta> since sum of delta per class is 0.
3. Now D_osc measures how fractions with denominator b are *irregularly spaced* among all Farey fractions. The variance of D_osc over denominator b is related to the pair correlation of Farey fractions, which is well-studied (Boca-Cobeli-Zaharescu, 2001).
4. The key inequality becomes: |<D_osc, delta>| < C/2 = ||delta||^2 / 2.
5. By Cauchy-Schwarz: |<D_osc, delta>| <= ||D_osc|| * ||delta||, so it suffices to show ||D_osc|| < ||delta|| / 2.
6. ||D_osc||^2 can be bounded using pair correlation statistics of Farey fractions.
7. ||delta||^2 = C can be computed exactly using properties of modular multiplication.

**What makes this special:** The permutation property (Fact 3) kills the interaction with the smooth part, leaving only the oscillatory-oscillatory interaction. This is a *variance comparison* problem: is the Farey irregularity variance smaller than the multiplicative displacement variance? The answer should be yes because Farey fractions are remarkably well-distributed (this is essentially the content of the Riemann Hypothesis connection).

---

## Approach 3: Operator-Theoretic / Spectral Gap Argument

**Key idea:** View the map F -> (D + delta) as a linear operator on L^2(F_{p-1}), and show it is norm-expanding by analyzing its spectrum.

**Why this is promising:** The identity B + C = ||D + delta||^2 - ||D||^2 asks whether adding delta increases the norm. If we think of "adding delta" as applying the operator I + delta/D (heuristically), norm expansion follows if this operator has all singular values > 1, which is a spectral condition.

**Concrete path:**
1. Consider the |F_{p-1}|-dimensional real vector space with basis indexed by Farey fractions.
2. D is a fixed vector. delta is another vector. We need ||D + delta||^2 > ||D||^2.
3. This is equivalent to: the angle between D and delta satisfies cos(theta) > -||delta||/(2||D||).
4. The ratio ||delta||/||D|| can be estimated: ||delta||^2 = C is computable, ||D||^2 = sum D^2 relates to the second moment of Farey discrepancy (known: asymptotically (1/(2pi^2)) * |F_N|, by Franel-Landau).
5. So we need cos(theta) > -c/sqrt(p) for some constant c, i.e., D and delta are not too anti-aligned.
6. The spectral approach: expand D and delta in the eigenbasis of the "Farey graph Laplacian" (adjacency of Farey neighbors). Farey neighbors a/b, c/d satisfy |ad-bc|=1, giving a graph structure. The Laplacian spectrum of this graph is related to Maass forms and the Selberg eigenvalue conjecture.
7. If D and delta have most of their energy in different spectral bands (D in low frequencies, delta in high frequencies due to its oscillatory/permutation nature), their inner product is automatically small.

**What makes this special:** The Farey graph has deep connections to the modular group PSL(2,Z) and hyperbolic geometry. The spectral theory of the Laplacian on the modular surface is extremely well-developed. This approach would connect B+C>0 to the spectral gap of the modular surface, which is known (Selberg's 3/16 theorem, or even the full Ramanujan-Petersson conjecture for holomorphic forms).

---

## Approach 4: Convexity / Jensen's Inequality on Denominator Classes

**Key idea:** Instead of bounding B globally, analyze B + C as a sum over denominator classes and show each class contributes non-negatively (or that the negative contributions are dominated by the positive ones via a convexity argument).

**Why this is promising:** The sum B + C decomposes as:

    B + C = sum_b sum_{gcd(a,b)=1} [ (D(a/b) + delta(a/b))^2 - D(a/b)^2 ]
          = sum_b [ ||D_b + delta_b||^2 - ||D_b||^2 ]

where D_b, delta_b are the restrictions to denominator b. Each term asks: does adding delta_b to D_b increase the norm within the b-class?

**Concrete path:**
1. For each b, we have phi(b) fractions. delta_b is a mean-zero vector (by Fact 3). D_b has mean approximately -1/2 (by Fact 4).
2. Write D_b = -1/2 * 1 + D_b^osc where 1 is the all-ones vector. Then:
   ||D_b + delta_b||^2 = ||(-1/2)*1 + D_b^osc + delta_b||^2
                        = phi(b)/4 + ||D_b^osc + delta_b||^2  (cross term vanishes since delta_b has mean 0)
   ||D_b||^2 = phi(b)/4 + ||D_b^osc||^2
3. So the contribution from class b is: ||D_b^osc + delta_b||^2 - ||D_b^osc||^2 = 2<D_b^osc, delta_b> + ||delta_b||^2.
4. This reduces the problem to: for each b, show 2<D_b^osc, delta_b> + ||delta_b||^2 > 0, OR show the sum over b of these quantities is positive.
5. For individual b: ||delta_b||^2 is the sum of squares of displacements of the permutation a -> pa mod b. This equals (1/b^2) * sum (a - pa mod b)^2, which for "generic" permutations is ~ phi(b) * b^2 / 6.
6. |<D_b^osc, delta_b>| <= ||D_b^osc|| * ||delta_b||. If ||D_b^osc|| is small compared to ||delta_b|| (Farey fractions are well-equidistributed), each class contributes positively.
7. The classes where this might fail are small b (where phi(b) is small and D_b^osc could be large relative to delta_b). But small b means few fractions, so their total contribution is bounded.

**What makes this special:** This reduces a global problem to a collection of local problems (one per denominator), and the local problems are about comparing the irregularity of Farey fraction placement (D_b^osc) with the displacement of a specific permutation (delta_b). The permutation displacement is "intrinsic" and doesn't depend on global ordering, making it easier to bound.

---

## Approach 5: Probabilistic / Second Moment Method

**Key idea:** Treat the collection {delta(a/b)} as a "random-like" signed sequence and use second-moment methods to show that B + C concentrates around its mean, which is positive.

**Why this is promising:** As p grows, there are more and more denominators b < p, and for each one, multiplication by p mod b acts as an essentially independent permutation. The cross term B is a sum of many weakly correlated terms (one per denominator class), so by a central-limit or concentration argument, B should be close to its expected value of 0 (since delta is "unbiased"), while C grows like sum of variances.

**Concrete path:**
1. Write B = 2 * sum_b sum_{gcd(a,b)=1} D(a/b) * delta(a/b) = 2 * sum_b X_b where X_b = <D_b, delta_b>.
2. Model the permutation a -> pa mod b as "approximately random" for large b. Under a random permutation, E[X_b] = 0 and Var(X_b) can be computed.
3. Similarly, C = sum_b ||delta_b||^2 = sum_b Y_b where Y_b > 0 always.
4. The ratio R = B/(2C) = (sum X_b) / (sum Y_b).
5. By the law of large numbers heuristic: as the number of denominators grows, R -> E[X_b] / E[Y_b] = 0. So R is small, and in particular > -1/2.
6. To make this rigorous: use Chebyshev or Bernstein inequalities on sum X_b, with the variance bound coming from the near-independence of different denominator classes.
7. The "near-independence" can be established using the Chinese Remainder Theorem: for coprime b1, b2, the actions of p mod b1 and p mod b2 are independent.

**Quantitative bound:** If Var(sum X_b) = O(p^{2+eps}) and C = Theta(p^2), then P(B < -C) -> 0. But we need a deterministic bound, not probabilistic. The fix: use the variance bound *deterministically*: |sum X_b|^2 <= (number of terms) * sum X_b^2, and bound each X_b^2 individually.

**What makes this special:** This approach explains *why* B+C > 0 at a structural level: B is a sum of many nearly independent mean-zero terms, while C is a sum of positive terms of comparable total magnitude. The positivity of B+C is essentially a law-of-large-numbers phenomenon, which is why the bound improves (R -> 0) as p grows, with the worst case at the smallest prime p=11.

---

## Summary and Recommended Priority

| Approach | Core technique | Likely difficulty | Handles small p? |
|----------|---------------|-------------------|------------------|
| 1. Fourier/character sums | Explicit character sum bounds | Medium-High | Via computation |
| 2. Variance domination | Cauchy-Schwarz + Farey pair correlation | Medium | Possibly |
| 3. Spectral gap | Modular surface Laplacian | High | Unlikely |
| 4. Denominator-class decomposition | Local analysis + aggregation | Medium-Low | Yes (enumerate) |
| 5. Second moment / concentration | Independence + variance bounds | Medium | Via computation |

**Recommended order:** 4 then 2 then 5 then 1 then 3.

Approach 4 is the most concrete and breaks the problem into manageable pieces. Approach 2 refines it with quantitative bounds. Approach 5 gives the structural explanation. Approaches 1 and 3 are more ambitious but connect to deep number theory.

The critical insight across all approaches: **the permutation property (Fact 3) kills the smooth part of D, leaving only the oscillatory part, whose interaction with delta is controlled by equidistribution of Farey fractions.**
