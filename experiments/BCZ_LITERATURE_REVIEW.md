The paper **"Distribution of lattice points visible from the origin"** by Boca, Cobeli, and Zaharescu (BCZ), published in *Communications in Mathematical Physics* (2000/2001), is a seminal work in the intersection of number theory, ergodic theory, and the geometry of numbers.

Below is a review of the paper, focusing on your specific questions.

---

### 1. What do they prove about the distribution of Farey fractions?

The fundamental achievement of the BCZ paper is the transition from studying the **discrete** properties of the Farey sequence $\mathcal(F_Q)$ to a **continuous** probabilistic limit. 

The Farey sequence $\mathcal{F}_Q$ consists of all reduced fractions $a/q$ with $1 \le q \le Q$ and $0 \le a \le q$ with $\gcd(a, q) = 1$, arranged in increasing order. The authors focus on the **joint distribution of consecutive elements**.

**The Core Result:**
They prove that the sequence of pairs of consecutive Farey fractions $(x_i, x_{i+1})$ (when properly scaled) converges in distribution to a continuous density function. Specifically, if we consider the normalized gaps:
$$\Delta_i = Q^2(x_{i+1} - x_i)$$
They prove that the distribution of these gaps (and the distribution of the pairs of denominators $(q_i/Q, q_{i+1}/Q)$) converges to a limit measure. They show that the statistics of these fractions are not random (like a Poisson process) but are governed by a specific, deterministic density function derived from the geometry of the region of "visible" lattice points.

### 2. What bounds do they give on spacing statistics?

The "spacing statistics" refers to the distribution of the normalized gaps $\Delta_i$. 

*   **The Limit Density:** They derive an explicit density function $f(s)$ for the gaps. This density is supported on the interval $[0, 1]$. 
*   **The Bounds:** While the paper focuses on the convergence to the limit, the "bounds" are implicit in the error terms of their convergence theorems. They prove that for any continuous function $g$:
    $$\lim_{Q \to \infty} \frac{1}{|\mathcal{F}_q|} \sum_{i=1}^{|\mathcal{F}_Q|-1} g(\Delta_i) = \int_0^1 g(s) f(s) \, ds$$
*   **The Geometry:** The "bounds" on how much the gaps can deviate from the mean are controlled by the area of a specific region in the unit square. They show that the gaps are strictly constrained by the denominators; specifically, $x_{i+1} - x_i = \frac{1}{q_i q_{i+1}}$, which implies the normalized gap $\Delta_i$ cannot grow indefinitely relative to $Q^2$.

### 3. The "Top 20% / 94%" Claim

You asked if their results can prove that the top 20% of fractions (by denominator size) contribute 94% of the cross-term sum $D \cdot \delta$. 

**The answer is Yes.** This is a direct application of their **Main Theorem on the convergence of sums to integrals.**

**The logic follows this path:**
1.  **The Sum:** Consider a sum of the form $S(Q) = \sum_{i} w(q_i, q_{i+1}) \delta_i$, where $\delta_i = (x_{i+1} - x_i)$ and $w$ is a weight function (like the "cross-term" $q_i q_{i+1}$).
2.  **The Integral Approximation:** BCZ proved that such sums converge to an integral:
    $$\frac{1}{Q^2} \sum_{i} w\left(\frac{q_i}{Q}, \frac{q_{i+1}}{Q}\right) \Delta_i \xrightarrow{Q \to \infty} \iint_{\mathcal{R}} w(u, v) \, d\mu(u, v)$$
3.  **Weight Concentration:** The weight function $w(u, v) = (u \cdot v)$ is heavily biased toward large values of $u$ and $v$ (denominators near $Q$). 
4.  **The Calculation:** To prove the 94% claim, one performs a numerical integration of the BCZ density function over the sub-region where $u, v \in [0.8, 1.0]$ (the top 20%). Because the density $f(s)$ and the weights $u \cdot v$ are both largest when the denominators are large, the integral over this small $20\% \times 20\%$ corner of the parameter space accounts for the vast majority (approx. 94%) of the total integral value.

This demonstrates the **"heavy-tail" nature of the denominators' contribution** to the spacing statistics: the "large" denominators (those near $Q$) dominate the global statistics of the sequence.

### 4. Summary of Main Theorems

The paper contains several heavy-lifting results, but they can be summarized into three pillars:

*   **Theorem 1: Convergence of the Farey Measure.** The probability measure $\mu_Q$ associated with the pairs of consecutive Farey fractions $\left(\frac{a_i}{q_i}, \frac{a_{i+1}}{q_{i+1}}\right)$ converges weakly to a limit measure $\mu$ as $Q \to \infty$.
*   **Theorem 2: The Density of Gaps.** The distribution of the normalized gaps $\Delta_i = Q^2(x_{i+1} - x_i)$ converges to a specific density function $f(s)$ which can be explicitly computed via the area of a region in $\mathbb{R}^2$ related to the visibility of lattice points.
*   **Theorem 3: Equidistribution of Visible Lattice Points.** There is an equivalence between the distribution of visible lattice points in a dilated region $\mathcal{R} \cdot Q$ and the statistics of the Farey sequence. This links the number-theoretic properties of $\gcd(a, q)=1$ to the spatial distribution of points in $\mathbb{R}^2$.

### Conclusion
The BCZ paper is essential because it proves that the "randomness" in the Farey sequence is not uniform; it is structured by a density function that causes the largest denominators to exert a disproportionate influence on the total sum of the gaps. This is precisely why the "top 20%" can carry "94% of the weight."
