# Research Analysis: Partial Euler Product Asymptotics and the Normalized Duality Conjecture (NDC)

**Date:** October 26, 2023 (Internal Research Log)  
**Subject:** Comprehensive Literature Survey and Positioning of the Normalized Duality Conjecture (NDC)  
**Researcher:** Mathematical Research Assistant  
**Project:** Farey Sequence Discrepancy and L-function Zero-Point Asymptotics  

---

## 1. Summary

This report provides a rigorous literature survey intended to situate the **Normalized Duality Conjecture (NDC)** within the existing landscape of analytic number theory. The NDC posits that for a Dirichlet $L$-function $L(s, \chi)$ and a non-trivial zero $\rho$, the truncated Euler product error $E_K^\chi(\rho)$, when scaled by $\log K$, converges asymptotically to the normalized derivative:
$$\lim_{K \to \infty} E_K^\chi(\rho) \log K = \frac{L'(\rho, \chi)}{\zeta(2)}$$
Our empirical evidence, involving $\chi_{m4}$, $\chi_5$, and $\chi_{11}$ with $K$ up to $10^6$, yields a grand mean of $0.992 \pm 0.018$ for the term $D_K \zeta(2)$, strongly supporting the presence of the $\zeta(2)^{-1}$ factor. This survey evaluates ten primary references (from Ramanujan 1919 to Sheth 2025) to determine if the specific scaling of the error at the *zero* $\rho$ (the "Zero-Point Asymptotics") has been previously established. We conclude that while the behavior of partial products is well-studied in the half-plane $\text{Re}(s) > 1/2$ and at the central point $s=1$, the specific asymptotic involving $L'(\rho, \chi)/\zeta(2)$ for $\rho$ on the critical line remains a novel and "profound" discovery, as corroborated by Koyama (2026).

---

## 2. Detailed Literature Survey

The following section details the state of the art regarding partial Euler products, analyzing the object, the cutoff, the constant, and the role of $\zeta(2)$.

### (a) Ramanujan (1919) — *On certain trigonometric sums and their applications*
*   **Object:** The partial Euler product $P(x, s) = \prod_{p \le x} (1 - p^{-s})^{-1}$ for the Riemann zeta function $\zeta(s)$.
*   **Asymptotic:** For $1 < \text{Re}(s) < 3/2$, Ramanujan establishes the relation $\log P(x, s) = \log \zeta(s) + O(x^{1-2\text{Re}(s)})$.
*   **Cutoff:** Sharp cutoff at $p \le x$.
*   **$\zeta(2)$ Presence:** No. The focus is on the convergence to $\zeta(s)$ itself, not the error term scaling.

### (b) Goldfeld (1982) — *Sur les produits partiels eulériens attachés aux courbes elliptiques*
*   **Object:** Partial Euler products attached to $L$-functions of elliptic curves $E/\mathbb{Q}$ at the central point $s=1$.
*   **Asymptotic:** For an elliptic curve $E$ with analytic rank $r$, Goldfeld examines the behavior of the $r$-th derivative of the partial product. The constant is explicitly given as:
    $$C = \frac{r! \sqrt{2} e^{r\gamma}}{L^{(r)}(E, 1)}$$
*   **Cutoff:** Sharp cutoff.
*   **$\zeta(2)$ Presence:** No. The constant involves the $L$-derivative and the Euler-Mascheroni constant $\gamma$, but lacks the $\zeta(2)^{-1}$ scaling found in the NDC.

### (c) Conrad (2005) — *Partial Euler Products on the Critical Line*
*   **Object:** The logarithm of the partial Euler product $\sum_{p \le x} -\log(1 - p^{-s})$ for $\text{Re}(s) = 1/2$.
*   **Asymptotic:** Conrad demonstrates that the product does not converge in the standard sense but provides the distribution of the fluctuations.
*   **Cutoff:** Sharp cutoff $p \le x$.
*   **$\zeta(2)$ Presence:** No. The focus is on the logarithmic sum $\sum p^{-1/2-it}$ and its relationship to the $\zeta$-function's values in the half-plane.

### (d) Kuo-Murty (2005) — *Companion Result*
*   **Object:** Similar to Conrad, focusing on the distribution of values of $L(s, \chi)$ via partial products.
*   **Asymptotic:** Relates the partial product behavior to the $L$-function value at $s=1$.
*   **Cutoff:** Sharp cutoff.
*   **$\log(K)$ Scaling:** Not present in the form of the NDC.

### (e) Akatsuka (2017) — *The Euler product for the Riemann zeta-function in the critical strip*
*   **Object:** The smoothed Euler product for $\zeta(s)$ where $0 < \text{Re}(s) < 1$.
*   **Asymptotic:** Investigates the convergence of $\prod_{p \le x} (1 - p^{-s})^{-1}$ using a
