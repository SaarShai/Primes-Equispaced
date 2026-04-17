# Farey Sequence Discrepancy and L-Function Spectroscopy: Verification of the $T_\infty$ Limit

## Summary

This report details a computational verification of the limiting logarithmic amplitude formula $T_\infty \approx (1/2) \log L(2\rho, \chi^2)$ within the context of Farey sequence discrepancy research. The primary objective was to execute high-precision numerical experiments using `mpmath` with a decimal precision of 40 digits ($dps=40$) to analyze the behavior of the partial sum operator $D_K(\rho)$ as $K \to \infty$. The study utilized three distinct Dirichlet characters: the trivial character $\chi_0$, the quadratic character modulo 4 ($\chi_{m4}$), and the complex character modulo 5 ($\chi_5$).

Our analysis confirms that for the trivial character and the character $\chi_{m4}$ (where $\chi^2 = \chi_0$), the limit $B_\infty = \arg(D_K)$ converges to $(1/2) \arg \zeta(1+2\rho)$. However, for the character $\chi_5$, where $\chi_5^2 \neq \chi_0$, the limiting argument diverges from the trivial case, consistent with the evaluation of the distinct $L$-function $L(s, \chi_5^2)$. The "Anti-Fabrication Rule" was strictly enforced, utilizing exact Python dictionary mappings for character values rather than standard Legendre symbol assumptions. We conclude that the Koyama "missing link" formula holds for the trivial and quadratic cases, but requires distinct $L$-function evaluation for higher-order complex characters.

## Detailed Analysis

### 1. Theoretical Framework: Farey Discrepancy and Spectroscopy

The investigation centers on the asymptotic behavior of the Farey sequence discrepancy $\Delta_W(N)$. Recent theoretical developments, notably those attributed to Koyama, suggest a profound connection between the spectral properties of the Farey series and the zeros of associated $L$-functions. Specifically, we examine the operator $D_K$, which represents the weighted sum of discrepancies over Farey fractions up to denominator $K$.

The core hypothesis under testing is the limiting relationship:
$$ T_\infty \approx \frac{1}{2} \log L(2\rho, \chi^2) $$
where $\rho = \sigma + i\gamma$ represents a non-trivial zero of the $L$-function associated with the character $\chi$. In our specific execution, we fixed $\rho$ at the first zero of the Riemann zeta function, $\rho = 0.5 + 14.13472514i$. Consequently, the evaluation point for the $L$-function becomes $2\rho = 1 + 28.26945028i$.

The quantity $B_K$ is defined as the imaginary part of the logarithm of the discrepancy operator:
$$ B_K = \text{Im}(\log D_K(\rho)) = \arg(D_K(\rho)) $$
The convergence behavior of $B_K$ toward $B_\infty$ is the critical metric for verifying the formula. The Mertens spectroscope, referenced in our context, provides the mechanism for detecting zeta zeros through pre-whitening techniques, but the core spectral link here is the logarithmic amplitude $T_\infty$.

### 2. Implementation Constraints and Character Definitions

A critical component of this research involves the strict definition of Dirichlet characters. The prompt explicitly issues an "ANTI-FABRICATION RULE": standard Legendre symbol implementations ($\chi_5\_{\text{Legendre}}$ and $\chi_{11}\_{\text{Legendre}}$) are identified as incorrect for the specific zero loci provided in the spectral data. Specifically, incorrect character definitions lead to $|L(\rho)|$ values of $0.75$ and $1.95$ respectively, which correspond to non-zeros in our spectral window.

Therefore, we adopted the exact Python dictionary-based definitions provided:

1.  **Modulo 4 Character ($\chi_{m4}$):**
    $$ \chi_{m4}(p) = \begin{cases} 1 & \text{if } p \equiv 1 \pmod 4 \\ -1 & \text{if } p \equiv 3 \pmod 4 \\ 0 & \text{if } p = 2 \end{cases} $$
    This is a real-order-2 character. Note that $\chi_{m4}^2 = \chi_0$ (the trivial character).

2.  **Modulo 5 Character ($\chi_5$):**
    The dictionary definition provided is `dl5={1:0, 2:1, 4:2, 3:3}`. The value is computed as:
    $$ \chi_5(p) = i^{\text{dl5}[p \pmod 5]} $$
    For example, $\chi_5(2) = i^1 = i$. This character has complex order-4. Consequently, $\chi_5^2$ is a quadratic character (order-2), but it is *not* the Legendre symbol in the standard sense without the specific `dl5` mapping context.
    The mapping for the square is derived from the exponent multiplication modulo the order of the multiplicative group.

3.  **Modulo 11 Character ($\chi_{11}$):**
    Defined via `dl11={1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9}` with $\chi_{11}(p) = \exp(2\pi i \cdot \text{dl11}[p\%11] / 10)$.
