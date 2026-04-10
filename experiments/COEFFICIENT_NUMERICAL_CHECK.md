Yes, your derivation and the resulting conclusion are mathematically consistent with the explicit formula for the Mertens function $M(x)$.

Here is the confirmation of the consistency between your "spectroscope" derivation and the standard number-theoretic results.

### 1. The Explicit Formula for $M(x)$
The standard explicit formula for the Mertens function $M(x) = \sum_{n \leq x} \mu(n)$ is derived from the inverse Mellin transform of $1/\zeta(s)$. The relevant Mellin transform relation is:
$$ \frac{1}{s\zeta(s)} = \int_1^\infty \frac{M(x)}{x^{s+1}} \, dx $$
The function $f(s) = \frac{1}{s\zeta(s)}$ has simple poles at the non-trivial zeros $\rho$ of $\zeta(s)$. To find the residue at a zero $\rho$, we look at the term:
$$ \text{Residue at } \rho = \lim_{s \to \rho} (s-\rho) \frac{x^s}{s\zeta(s)} = \frac{x^\rho}{\rho \zeta'(\rho)} $$
Thus, the oscillating contribution of $M(x)$ is:
$$ M(x) \sim \sum_{\rho} \frac{x^\rho}{\rho \zeta'(\rho)} $$
**Conclusion:** The coefficient attached to the oscillatory term $x^\rho$ is indeed $\frac{1}{\rho \zeta'(\rho)}$.

### 2. The Spectroscope Weighting
You are applying a specific normalization to the prime values to construct the "spectroscope" observable.
1.  **Initial Weight:** You define the initial effective weight as $M(p)/p$.
    $$ \frac{M(p)}{p} \sim \sum_{\rho} \frac{p^\rho}{p \cdot \rho \zeta'(\rho)} = \sum_{\rho} \frac{p^{\rho-1}}{\rho \zeta'(\rho)} $$
2.  **Periodogram Factor:** You apply an additional factor of $1/\sqrt{p}$ (inside the periodogram).
    $$ \text{Effective Amplitude} = \frac{M(p)}{p} \cdot \frac{1}{\sqrt{p}} = \frac{M(p)}{p^{3/2}} $$
3.  **Substitution:** Substituting the explicit formula:
    $$ \frac{1}{p^{3/2}} \sum_{\rho} \frac{p^\rho}{\rho \zeta'(\rho)} = \sum_{\rho} \frac{p^{\rho - 3/2}}{\rho \zeta'(\rho)} $$
    Assuming the Riemann Hypothesis (or generally evaluating the contribution at $\rho = 1/2 + i\gamma_k$):
    $$ p^{\rho - 3/2} = p^{(1/2 + i\gamma_k) - 3/2} = p^{i\gamma_k - 1} $$
    So the effective expression becomes:
    $$ \sum_{\rho} \frac{p^{i\gamma_k - 1}}{\rho_k \zeta'(\rho_k)} $$

### 3. Confirming the Coefficient ($\rho$ vs $\rho-1$)
The core of your question is whether the coefficient is $\frac{1}{\rho \zeta'(\rho)}$ or $\frac{1}{(\rho-1)\zeta'(\rho)}$.

*   **The $\rho$ Denominator:** As shown in step 1, the factor $1/\rho$ arises from the $1/s$ factor in the integrand of the inverse Mellin transform. It is intrinsic to the definition of $M(x)$.
*   **The $\rho-1$ Denominator:** The term $(\rho-1)$ would typically appear if one were looking at a pole at $s=1$ (which generates the main term $x$) or if there were a shift in the functional equation argument. However, for the contribution of the zeros $\rho$ themselves in the Mertens function, there is no mechanism that introduces a $(\rho-1)$ factor in the denominator. The residues at $\rho$ are solely determined by the derivative of the denominator $\zeta(s)$ (giving $\zeta'(\rho)$) and the pole factor $s$ (giving $\rho$).

### 4. Consistency with Observed Behavior
*   **Convergence:** With the weight $p^{i\gamma_k - 1}$, the series converges very rapidly (as $1/p$), which is necessary for a stable spectral density estimation.
*   **Resonance:** At the resonance frequency $\gamma_j$, the term $p^{i\gamma_j}$ contributes constructively, weighted by the residue $\frac{1}{\rho_j \zeta'(\rho_j)}$.
*   **Mathematical Consistency:** The coefficient $1/(\rho \zeta'(\rho))$ is the standard residue for the Mellin inversion of $1/(s\zeta(s))$.

**Final Confirmation:**
Your derivation is correct. The coefficient is **$\frac{1}{\rho \zeta'(\rho)}$**, not $\frac{1}{(\rho-1)\zeta'(\rho)}$. This aligns perfectly with the mathematical theory of the Riemann explicit formula for the Mertens function.
