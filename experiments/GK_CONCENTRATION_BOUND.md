The discrepancy between the "50%" and "90%" results arises from a fundamental difference in how the summation over the numerators ($a$) is weighted.

Here is the breakdown of the two scenarios:

### 1. The "50%" Scenario (Divergent Sum)
This result assumes that every reduced fraction with denominator $b$ contributes to the sum with equal magnitude, or that the sum over numerators $a$ scales with the count of numerators $\phi(b)$ (Euler's totient function).
*   **Assumption:** The contribution for a fixed $b$ is proportional to $\phi(b)$.
*   **Heuristic:** Since $\phi(b) \sim b$, the sum over numerators adds a factor of $b$.
*   **Total Sum:** The total sum becomes approximately $\sum_{b \le p} \phi(b) \cdot \frac{1}{b^2} \approx \sum_{b \le p} \frac{1}{b}$.
*   **Mathematical Behavior:** This is a **logarithmically divergent sum** (the harmonic series).
*   **Split:** For a sum $\sum_{b=1}^p \frac{1}{b} \sim \log p$, the contribution from small denominators up to $\sqrt{p}$ is $\sum_{b=1}^{\sqrt{p}} \frac{1}{b} \sim \log \sqrt{p} = \frac{1}{2} \log p$. This captures roughly **50%** of the total sum.

### 2. The "90%" Scenario (Convergent Sum)
This result arises from the correct heuristic for $|D(a/b)|$, which is dominated by the cases where the numerator $a$ is small (specifically $a=1$).
*   **The Missing Factor:** The "missing factor" is the **count of numerators**, $\phi(b)$. The heuristic $|D(a/b)| \sim n/b$ (or the specific scaling of the kernel) holds significantly only for $a=1$ (and $a=b-1$). For $a > 1$, the values of $|D(a/b)|$ are typically much smaller or cancel out due to oscillation.
*   **Correction:** Instead of summing over all $\phi(b)$ numerators, the sum effectively collapses to just the dominant term ($a=1$).
*   **Total Sum:** The sum becomes $\sum_{b \le p} \frac{1}{b^2}$.
*   **Mathematical Behavior:** This is a **convergent sum** (related to $\zeta(2) = \pi^2/6$).
*   **Split:** In a convergent series, the terms decay rapidly. The sum $\sum_{b=\sqrt{p}+1}^{\infty} \frac{1}{b^2}$ is approximately $\int_{\sqrt{p}}^\infty \frac{dx}{x^2} = \frac{1}{\sqrt{p}}$.
*   **Result:** For large $p$, the term $1/\sqrt{p}$ is small. Thus, the sum up to $\sqrt{p}$ captures the overwhelming majority (essentially 100%, or roughly 90% for moderate $p$) of the total mass.

### Summary
The "missing factor" is **$\phi(b)$** (or the assumption that the sum over numerators is large). Removing this factor transforms the sum from a divergent logarithmic scale ($\sim \log p$) to a convergent scale ($\sim \text{const}$). This concentration of mass on small denominators explains why the restriction to $b \le \sqrt{p}$ captures 90% of the sum.
