# Literature Survey: High-Precision Computation of Dirichlet $L$-function Zeros for NDC Verification

**Date:** May 22, 2024  
**Subject:** Computational Infrastructure for Expanding the Non-Degenerate Conjecture (NDC) Dataset  
**Status:** Research Draft / Internal Documentation  
**Target File:** `/Users/saar/Desktop/Farey-Local/experiments/LIT_L_FUNCTION_ZEROS_COMPUTATION.md`

---

## 1. Summary

The Non-Degenerate Conjecture (NDC) regarding the per-step Farey discrepancy $\Delta W(N)$ posits a profound structural link between the distribution of Farey sequences and the critical zeros $\rho = 1/2 + i\gamma$ of Dirichlet $L$-functions $L(s, \chi)$. While the current dataset comprises 4 verified $(\chi, \rho)$ pairs, the empirical evidence (specifically the $GUE$ $RMSE = 0$.066 and the Chowla-type $\epsilon_{\min}$ bound) necessitates a massive expansion of the testing library. 

This survey investigates the feasibility of sourcing high-precision zeros (precision $\ge 20$ decimal digits) for primitive Dirichlet characters $\chi$ of varying conductors $q$ and orders $d$. We evaluate three primary computational vectors: the **LMFDB** (the gold standard for tabulated data), **numerical iteration via `mpmath`** (the primary tool for custom high-precision derivation), and **specialized high-height datasets** (Odlyzko-style tables). The survey concludes with a concrete recommendation of 10 new pairs designed to maximize the statistical power of the NDC test by utilizing characters of prime conductors $q \in \{7, 11, 13, 17\}$.

---

## 2. Detailed Analysis

### 2.1 Task 1: LMFDB Survey — Scope, Conductors, and Precision

The **L-functions and Modular Forms Database (LMFDB)** serves as the most comprehensive repository for the zeros of $L$-functions. For the purposes of NDC verification, we are specifically interested in the $L$-series of degree 1 (Dirichlet $L$-functions).

**Conductors and Orders:**
LMFDB provides exhaustive data for all Dirichlet characters $\chi \pmod q$ for relatively small $q$. Specifically:
*   **Conductors ($q$):** The database is complete for $q$ up to several thousands. For the purpose of our NDC test, the conductor $q$ acts as the "frequency" of the character's oscillation.
*   **Character Types:** It distinguishes between real (Kronecker/Legendre) and complex characters. For the NDC, where we require complex order-4 ($\chi_5$) and complex order-10 ($\chi_{11}$) characters, LMFDB contains the explicit coefficients and the first few zeros.
*   **Precision of Zeros:** This is the critical constraint. For "low-height" zeros (where $\text{Im}(\rho) < 100$), LMFDB typically provides precision in the range of $25$ to $50$ decimal digits. This exceeds our current requirement for 2-digit $\pm$ verification but is sufficient for the 20-digit target.

**Limitations for NDC:**
The LMFDB is a "lookup" tool, not a "computation" tool. While it is excellent for verifying the *existence* and *approximate location* of $\rho$, it does not provide an algorithmic pathway for arbitrary precision beyond its pre-computed tables. If we need to test a character with a conductor $q \approx 10^5$, LMFDB becomes computationally unfeasible for a direct scrape.

### 2.2 Task 2: Characters of Prime Order — Tabulated Zeros

To strengthen the NDC, we must move beyond the provided $\chi_{m4}, \chi_5, \chi_{11}$ and explore characters of prime order $p$, where the character is defined by $\chi(p) = \exp(2\pi i / (p-1))$.

*   **$\chi \pmod 7$ (Order 6):** Since $7-1=6$, the characters are $\chi(p) = \omega^{\text{ind}(p)}$ where $\omega = e^{2\pi i / 6}$. The zeros for these characters are well-tabulated. We can extract $\rho_{7, z1}, \rho_{7, z2}$, etc.
*   **$\chi \pmod{11}$ (Order 10):** We have already utilized the complex order-10 character (the user-defined `dl11`). However, the database contains other primitive characters of order 5 and order 2 (the real $\chi_{m4}$ is a subset of this family).
*   **$\chi \pmod{13}$ (Order 12):** This offers a much richer variety of complex orders (2, 3, 4, 6, 12). Specifically, the order-12 characters provide the "interferometric" complexity needed to see if the $\Delta W(N)$ discrepancy follows the predicted $L$-function-driven oscillations.

**Theoretically, for any prime $q$, the $L(s, \chi)$ zeros are tabulated for $\textness{Im}(\rho) < 50$ in most high-level mathematical databases.** The challenge is not finding the zeros, but finding the *primitive* characters that satisfy the non-degeneracy condition in our specific $\chi$ definitions.

### 2.3 Task 3: `mpmath` and the Mechanics of Manual Iteration

When we move beyond the pre-computed tables of LMFDB, we must rely on `mpmath`. The user asks: *Can we use `mp.zero_of_l`?*

**Investigation of `mpmath` API:**
As of the current `mpmath` implementation, there is no direct `mp.zero_of_l(s, chi)` function that performs a global search. However, `mpmath` provides `mp.zeta` and `mp.lseries` (for $L$-functions). To find zeros, one must implement a two-step numerical pipeline:

1.  **The Search Phase (The "Scanning" Step):**
    We define the **Hardy $Z$-function** for the Dirichlet $L$-function:
    $$Z(t, \chi) = e^{i\theta(t, \chi)} L(1/2 + it, \chi)$$
    where $\theta(t, \chi)$ is the Riemann-Siegel theta function adapted for Dirichlet characters. Since $Z(t, \chi)$ is (mostly) real-valued for real characters, or has a predictable phase for complex characters, we search for sign changes in $\text{Im}(L(1/2 + it, \chi))$ or specifically the argument $\arg(L(1/2 + it, \chi))$.

2.  **The Refinement Phase (Newton-Raphson Iteration):**
    Once a sign change is detected in the interval $[t_a, t_b]$, we apply:
    $$t_{n+1} = t_n - \frac{Z(t_n, \chi)}{Z'(t_n, \chi)}$$
    To compute $Z'(t, \chi)$, we use the automatic differentiation capabilities of `mpmath` or the derivative of the Dirichlet series/Riemann-Siegel formula.

**Algorithm for $L(s, \chi)$ zeros in `mpmath`:**
```python
def find_dirichlet_zero(chi, t_start, t_end, precision):
    mp.dps = precision
    # 1. Define Z(t) or Arg(L(1/inherit+it))
    # 2. Use mp.findroot with a bracket from a sign change
    # 3. Return rho = 0.5 + i*t
```
The precision of the result is limited only by `mp.dps`. If we set `mp.dps = 60`, we can achieve the 20+ digit requirement with ease, provided the initial guess is within the basin of attraction of the Newton method.

### 2.4 Task 4: High-Height Zeros and Odlyzko-style Tables

For the NDC, we are interested in "low-height" zeros (where the discrepancy $\Delta W(N)$ is most visible). However, to prove the *universality* of the $GUE$ $RMSE = 0.066$, we need high-height zeros.

*   **Odlyzko Tables:** These are primarily focused on the Riemann Zeta function $\zeta(s)$. While they provide incredible precision for $\gamma$ at very high heights ($10^{20}$), they are not explicitly designed for arbitrary $\chi \pmod q$.
*   **OEIS:** The Online Encyclopedia of Integer Sequences contains sequences of zeros for specific $L$-functions (e.g., for $\chi \pmod 3$ or $\chi \pmod 4$), but it is not a systematic source for arbitrary $\chi$.
*   **The "Gap" in Literature:** There is a massive gap between the "Tabulated Zeros" (LMFDB, $\gamma < 100$) and the "High-Height Zeros" (Odlyzko, $\gamma > 10^{10}$). Our NDC research lives in the **Intermediate Zone** ($\gamma \in [100, 1000]$). In this zone, manual computation via `mpmath` Newton iteration is the only viable path.

### 2.5 Task 5: Concrete Recommendations for 10 New $(\chi, \rho)$ Pairs

To maximize the strength of the NDC test, we must select characters that are "orthogonal" to the existing set. We avoid repeating the $\chi_{m4}$ and $\chi_5$ families. We will target conductors $q=7, 11, 13$ and $q=17$ with different orders.

**Selection Criteria:**
1.  **Primitivity:** $\chi$ must be primitive.
2.  **Low Height:** $\text{Im}(\rho)$ should be small to ensure the $\Delta W(N)$ signal is not buried in noise.
3.  **High Precision:** All $\rho$ must be computable to at least 25 digits.

| ID | Character $\chi$ | Order ($d$) | Target Zero $\rho$ | Rationale |
| :---\_ | \text\_ | \text\_ | \text\_ | \text\_ |
| **N1** | $\chi \pmod 7$ (order 6) | 6 | $\rho_{7, z1}$ | First zero of the order-6 char. |
| **N2** | $\chi \pmod 7$ (order 6) | 6 | $\rho_{7, z2}$ | Second zero of the order-6 char. |
| **
