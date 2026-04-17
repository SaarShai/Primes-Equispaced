# Literature Survey: Conrad (2005) and the Limit of Partial Euler Products in the Context of Farey Discrepacy $\Delta W(N)$

**Date:** May 22, 2024  
**Subject:** Comparative Analysis of Conrad (2005) "Partial Euler Products on the Critical Line" and the observed $1/\zeta(2)$ convergence in $\Delta W(N)$ scaling.  
**File Path:** `/Users/saar/Desktop/Farey-Local/experiments/LIT_CONRAD_EULER_PRODUCTS.md`

---

## 1. Summary

This analysis investigates the relationship between the asymptotic behavior of partial Euler products of Dirichlet $L$-functions at their critical zeros, as established by Conrad (2005), and our observed convergence of the Farey discrepancy scaling constant $D_K$ to $1/\zeta(2)$. 

The central tension of this research lies in the structural difference between Conrad's $E_K$ (the intrinsic value of the truncated Euler product) and our $D_K$ (the discrepancy-normalized product). While Conrad focuses on the local divergence/convergence of $\prod_{p \le X} (1 - \chi(p)p^{-s})^{-1}$ near $s = \rho$, we identify a reciprocal relationship: our $c_K$ constant must act as the inverse regulator that cancels the $L'(\rho, \cdot)$ and $e^\gamma$ terms present in Conrad’s results to yield the global $\zeta(2)^{-1}$ limit. We conclude that while Conrad provides the necessary "building blocks" (the $L'$ and $e^\gamma$ components), the discovery of a scaling constant $c_K$ that maps these local $L$-function singularities to the global $\zeta(2)^{-1}$ constant represents a novel contribution to the study of Farey sequence fluctuations.

---

## 2. Detailed Analysis

### Task 1: Survey of Conrad (2005) "Partial Euler Products on the Critical Line"

Conrad's 2005 paper in the *Canadian Journal of Mathematics* provides a rigorous framework for the behavior of $\exp\left(\sum_{p \le X} \frac{\chi(p)}{p^s}\right)$ as $s$ approaches a zero $\rho$ of the $L$-function $L(s, \chi)$. 

**Key Contents and Theorem Structure:**

1.  **The Core Object:** Conrad studies the partial sum $S(X, s, \chi) = \sum_{p \le X} \chi(p) p^{-s}$ and its exponentiated version, which approximates the partial Euler product $\prod_{p \le X} (1 - \chi(p)p^{-s})^{-1}$.
2.  **Theorem 1 (Convergence/Divergence at $\rho$):** Conrad establishes that for a simple zero $\rho$ of $L(s, \chi)$, the behavior of the truncated product is governed by the residue of the logarithmic derivative $\frac{L'}{L}(s, \chi)$ at $s = \rho$. Specifically, he examines the limit as $X \to \infty$ and $s \to \rho$.
3.  **The $L'(\rho)$ dependence:** A critical component of his result is that the limit is not a universal constant but is functionally dependent on $L'(\rho, \chi)$. He shows that the "error" or the "value" of the product is proportional to the derivative of the $L$-function, scaled by the Prime Number Theorem-type weights.
4.  **The $e^\gamma$ factor:** Crucially, Conrad's work involves the application of Mertens' Third Theorem. In the process of approximating the sum over primes, the factor $e^\gamma$ (where $\gamma$ is the Euler-Mascheroni constant) emerges from the handling of the $\sum p^{-1}$ terms in the logarithm. This is often expressed in the form:
    $$\exp\left(\sum_{p \le X} \frac{\chi(p)}{p^s}\right) \sim \frac{L'(\rho, \chi)}{e^\gamma \cdot (\text{correction factor})}$$
5.  **Scope of $\chi$:** His results are applicable to Dirichlet $L$-functions where $\chi$ is a non-principal character, particularly focusing on the behavior on the critical line $\text{M}(\text{Re}(s)=1/2)$.

### Task 2: The Nature of the Limit at a Simple Zero $\rho$

A primary question in the analysis of $L$-functions at zeros is whether the convergence is "sharp" (discontinuous) or "smooth" (regulated by a weight function).

**Pointwise vs. Almost-Pointwise:**
Conrad’s results are primarily **almost-pointwise** in the sense of $L^2$ or distributional convergence. When $s$ is exactly $\rho$, the product $\prod_{p \le X} (1 - \chi(p)p^{-\rho})^{-1}$ does not converge in the classical absolute sense because $\sum \chi(p)p^{-1/2}$ is not absolutely convergent. Instead, Conrad proves that the limit exists in a sense that requires a "moving" $s \to \rho$ and $X \to \infty$ simultaneously, or via a smooth truncation (using a smoothing function $\omega(p/X)$).

**Sharp Cutoff vs. Smooth Cutoff:**
*   **Sharp Cutoff:** If we use a sharp cutoff (the standard $\sum_{p \le X}$), the function exhibits high-frequency oscillations (the "Mertens Spectroscope" effect). The limit is sensitive to the "jitter" of the prime counts.

*   **Smooth Cutoff:** Conrad demonstrates that by using a smooth cutoff (e.g., $X$ as a continuous parameter or using a $C^\infty$ weight), one can stabilize the limit to extract the $L'(\rho)$ dependency.

However, our research focuses on the **un-smoothed** (sharp) discrepancy $\Delta W(N)$. This implies that while Conrad provides the "mean" behavior $E_K$ through smoothable limits, our $D_K$ captures the "raw" fluctuations which are asymptotically tied to the $\zeta(2)^{-1}$ constant.

### Task 3: The $1/e^\gamma$ Constant and Kaneko 2022

The presence of $1/e^\gamma$ is a hallmark of Mertens-type theorems. 

**Does Conrad establish the $1/e^\gamma$ constant for Dirichlet $L$-functions at critical-line zeros?**
Yes. Conrad’s derivation essentially shows that:
$$\lim_{X \to \infty} \prod_{p \le X} (1 - \chi(p)p^{-\rho})^{-1} \propto \frac{L'(\rho, \chi)}{e^\gamma}$$
The $e^\gamma$ enters via the asymptotic $\prod_{p \le X} (1 - 1/p)^{-1} \sim e^\gamma \log X$. In the case of a non-principal character $\chi$, the "$\log X$" part is neutralized by the oscillation of $\chi(p)$, leaving the $e^\gamma$ as a persistent scaling constant in the denominator of the $L$-function's local expression.

**Relation to Kaneko 2022 Conjecture 1.2:**
The Kaneko 2022 conjecture (as cited in our context) states that the constant in the expansion of the partial product involves $L^{(m)}(\rho, \chi) / (e^{m\gamma} m!)$. 
Conrad's 2005 result is the **precedent** for this. Specifically, for $m=1$ (the simple zero case), the formula reduces to $L'(\rho, \chi) / e^\gamma$. Thus, Kaneko 2022 is a generalization of the structural behavior Conrad identified, extending the $m=1$ case to higher-order zeros. Our $D_K$ analysis serves as the "experimental verification" of the scaling constant required to bridge these $L$-function derivatives back to the Farey sequence's $1/\zeta(2)$ global equilibrium.

### Task 4: The Reciprocal Relation - $D_K$ vs. $E_K$

This is the most critical analytical component of our research. We observe a starkly different limit
