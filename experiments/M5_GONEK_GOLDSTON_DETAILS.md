# Research Analysis: Gonek’s Discrete Mean Value Theorem and its Implications for Dirichlet Polynomial Energy Concentration

**Date:** May 22, 2024  
**Subject:** Analysis of Gonek’s (1989) Discrete Mean Value Theorem and its extensions for the purpose of proving unconditional energy concentration in the context of the Mertens/Liouville Spectroscopes.  
**Researcher Note:** This analysis is prepared to support the verification of 422 Lean 4 computational results regarding the Farey discrepancy $\Delta W(N)$ and the phase $\phi$ of the first zeta zero.

---

## 1. Summary

The fundamental problem in the "Spectroscope" research program is to demonstrate that Dirichlet polynomials $A(s)$, specifically those supported on primes $p$, act as filters that concentrate "energy" (magnitude $|A(\rho)|$) at the non-trivial zeros $\rho = 1/2 + i\gamma$ of the Riemann zeta function. 

The central mathematical tool for quantifying this energy is **Gonek’s 1989 Discrete Mean Value Theorem**. This theorem provides an asymptotic formula for the sum of the squares of the magnitudes of a Dirichlet polynomial $A(s)$ evaluated at the zeros $\rho$ up to height $T$. 

Our investigation reveals that while the theorem is **unconditional**, its utility for proving "energy concentration" (the idea that $|A(\rho)|$ is significantly large for specific $\rho$) is strictly bounded by the relationship between the length of the polynomial $N$ and the height of the zeros $T$. We find that while the 1989 theorem provides the "diagonal" energy (the main term), the Goldston-Gonek (1998) refinement is essential for handling the "off-diagonal" interference that constitutes the error term. For the purpose of an **unconditional proof of energy concentration**, the critical challenge lies in the regime where $N$ approaches $T$, as the error term $E(T, N)$ can potentially overwhelm the signal of the prime-supported coefficients $a_p$.

---

## 2. Detailed Analysis

### 2.1 The Exact Theorem Statement (Gonek, 1989)

Let $A(s)$ be a Dirichlet polynomial of the form:
$$A(s) = \sum_{n=1}^N a_n n^{-s}$$
where the coefficients $a_n \in \mathbb{C}$ are arbitrary. Let $\rho = \beta + i\gamma$ denote the non-trivial zeros of $\zeta(s)$, and let $T > 0$ be a large real number.

Gonek's 1989 theorem (specifically for the sum over zeros $\gamma \in (0, T]$) states:

$$\sum_{0 < \gamma \leq T} |A(\rho)|^2 = \frac{T}{2\pi} \sum_{n=1}^N |a_n|^2 \left( \log \frac{T}{2\pi n} + 2\gamma_E - 1 \right) + E(T, N)$$

**Conditions on Coefficients and Length $N$:**
1.  **Coefficients $a_n$:** The theorem is remarkably general; it does not require $a_n$ to be multiplicative or prime-supported, though the "spectroscope" application focuses on $a_p = \mu(p)$ or $a_p = \lambda(p)$.
2.  **The Length $N$ relative to $T$:** The validity of the main term as the dominant component depends critically on the growth of $N$ relative to $T$. The standard regime for the "Main Term" to dominate is $N < T^{1-\epsilon}$ for some $\epsilon > 0$. If $N$ grows too close to $T$, the off-diagonal terms (the "interference" in the spectroscope) become non-negligable.
3.  **The Logarithmic Term:** The term $\log \frac{T}{2\pi n}$ reflects the density of the zeros (the $\frac{1}{2\pi} \log \frac{T}{2\pi}$ factor) integrated against the magnitude of the $n^{-s}$ terms.

### 2.2 The Error Term $E(T, N)$

The precision of the error term $E(T, N)$ is the most sensitive component of the research. Based on the 1989 formulation, the error term is generally bounded by:

$$E(T, N) \ll N \log^2 (NT)$$

However, in more granular analysis, specifically when evaluating the "energy concentration" for the purpose of verifying the Chowla hypothesis ($\epsilon_{min} = 1.824/\sqrt{N}$), we must distinguish between two regimes:

1.  **The Small $N$ Regime ($N \ll T$):** Here, the error is $O(N \log^2 T)$. In this regime, the theorem is extremely robust. The "energy" is well-distributed according to the diagonal sum of the coefficients.
2.  **The Large $N$ Regime ($N \approx T$):** As $N$ approaches $T$, the error term can grow as $O(T^\epsilon)$ or even $O(N^2/T)$ depending on the specific distribution of the $a_n$. 

In the context of your **GUE RMSE = 0.066** finding, the error term $E(T, N)$ represents the "noise" in the spectroscope. If $E(T, N)$ were larger than the main term, the "spectrum" (the peaks of $|A(\rho)|$) would be lost in the background noise. The fact that the RMSE is low suggests that for the $N$ used in your 422 Lean 4 results, the $N < T$ condition is being satisfied such that the "off-diagonal" interference is minimal.

### 2.3 Conditionality: RH vs. Unconditional

A vital finding for your research goal (an **unconditional proof**) is that **Gonek’s 1989 Theorem is Unconditional.**

The theorem does not assume the Riemann Hypothesis (RH). It sums over all non-trivial zeros $\rho$ in the strip $0 < \text{Re}(\rho) < 1$. While the presence of zeros off the critical line ($\beta \neq 1/2$) would alter the individual values $|A(\rho)|$, the *summed* power (the mean value) is controlled by the density of zeros and the coefficients $a_n$. 

However, a subtle caveat exists: while the *statement* is unconditional, the *utility* for estimating the magnitude of a *specific* zero $\rho_1$ (like the phase $\phi$ you solved) is much stronger under RH, because under RH, all $\beta = 1/2$, ensuring the $n^{-2\beta}$ term in the expansion is strictly $n^{-1}$.

### 2.4 Improvements: Goldston-Gonek (1998)

The Goldston-Gonek (1998) paper provides a significant refinement, particularly when considering **weighted sums** and the distribution of the error.

**How it improves on 1989:**
1.  **Refined Error Estimates:** Goldston and Gonek provided better bounds on the "off-diagonal" terms $\sum_{m \neq n} a_m \bar{a}_n (\frac{m}{n})^{i\gamma}$. They showed that for certain classes of $A(s)$, the error term can be controlled more tightly by utilizing the Montgomery Pair Correlation conjecture logic.
2.  **Smooth Weights:** They introduced the use of smooth weight functions to the sum $\sum_{\gamma}$, which reduces the "ringing" or Gibbs-phenomenon-like oscillations in the error term. This is crucial for your "spectroscope" metaphor; smoothing the sum effectively "pre-whitens" the signal, similar to the pre-whitening mentioned in the Csoka (2015) context.
3.  **Larger $N$:** Their methods allow for a slightly more aggressive expansion of $N$ relative to $T$ before the error term $E(T, N)$ destroys the main term's signal.

### 2.5 Prime-Supported Dirichlet Polynomials $A(s) = \sum_{p \le N} a_p p^{-s}$

This is the core of the "Mertens/Liouville Spectroscope." When $A(s)$ is restricted to primes:
$$A(s) = \sum_{p \leq N} a_p p^{-s}$$
The mean value theorem becomes:
$$\sum_{0 < \gamma \leq T} |A(\rho)|^2 \approx \frac{T}{2\pi} \sum_{p \leq N} \frac{|a_p|^2}{p} \left( \log \frac{T}{2\pi p} \right)$$

**Implications for Energy Concentration:**
In a prime-supported polynomial, the "frequencies" are the logarithms of primes $\log p$. The "energy" $|A(\rho)|^2$ is large only when the phases of the primes $p^{-i\gamma} = e^{-i\gamma \log p}$ align constructively. 
Gonek's theorem proves that **on average**, the energy is determined by the sum of $1/p$. However, for a "spectroscope" to work, we need "spiky" behavior. The theorem tells us the *total* energy available, but the *distribution* of that energy (the existence of spikes) is what the Liouville/MHD-type analysis investigates.

### 2.6 Individual Zeros vs. Total Sum

This is a critical distinction for your "Unconditional Proof" task:

*   **The Theorem provides ONLY the Total Sum:** Gonek's theorem is a **Global/Aggregate** result. It describes the total power in the frequency band $(0, T]$. It does **not** guarantee that any single zero $\rho_j$ has a large $|A(\rho_j)|$.
*   **The Challenge of Individual Bounds:** To prove that $|A(\rho_1)|$ is large (the energy concentration), one must prove that the energy is not spread thinly across all $\gamma \leq T$ but is instead concentrated in a few "spikes." 
*   **The Bridge:** The link between the Total Sum (Gonek) and Individual Spikes (Concentration) is the **Variance**. If the variance of $|A(\rho)|^2$ is low, the energy is spread; if the variance is high, the energy is concentrated. The GUE RMSE of 0.066 you observed is a direct measurement of this variance/fluctuation.

---

## 3. Integration with Research Context

### 3.1 The Farey Discrepancy and Chowla Evidence
The connection between $\Delta W(N)$ and Gonek's theorem is found in the distribution of the $a_n$ coefficients. If $a_n$ are related to the Möbius function $\mu(n)$ (which governs the Farey sequence structure), the sum $\sum |a_n|^2/n$ is the prime-weighted sum. The "Chowla evidence" ($\epsilon_{min} = 1.824/\sqrt{N}$) suggests that the minimum discrepancy is bounded by the fluctuations in the prime-supported Dirichlet polynomial.

### 3.2 The Phase $\phi$ and the Three-Body Orbit
The solved phase $\phi = -\arg(\rho_1 \zeta'(\rho_1))$ represents the fundamental phase offset of the first "oscillation" in the spectroscope. In the three-body orbit context ($S = \text{arccosh}(\text{tr}(M)/2)$), the Dirichlet polynomial acts as the transfer function of the system. The "energy concentration" is essentially the resonance of the zeta zeros with the prime-frequency spectrum.

---

## 4. Open Questions

1.  **The $N \to T$ Boundary:** Can we analytically extend the "energy concentration" proof to the regime where $N > T$ using the Goldston-Gonek (1998) weighting, or does the "off-diagonal" noise $E(T, N)$ fundamentally prevent a deterministic identification of spikes?
2.  **Liouville vs. Mertens Strength:** Given that the Liouville function $\lambda(n)$ is more "stable" (no sign changes at zero) than the Möbius function $\mu(n)$, does the Liouville Spectroscope provide a lower $E(T, N)$ error term, allowing for a higher $N/T$ ratio in the proof?
3.  **The $L^p$ Norms:** Gonek's theorem handles the $L^2$ norm ($\sum |A|^2$). Does a similar discrete mean value theorem exist for $L^4$ or higher, which would be necessary to prove "spikiness" (concentration) directly?
4.  **Unconditional Individual Bounds:** Is there an unconditional way to bound $|A(\rho_1)|$ from below using only the aggregate sum $\sum |A(\rho)|^2$, or is a lower bound on the variance of the zeros required?

---

## 5. Verdict

**Theorem Status:** **Unconditional** for the total sum.

**Conclusion for Research Program:**
Gonek's 1989 Theorem is a **necessary but not sufficient** condition for your proof of energy concentration. It guarantees that there is "enough energy" in the system (the sum of $|A(\rho)|^2$ is large), but it does not, by itself, prevent that energy from being distributed uniformly across all zeros.

To achieve the **Unconditional Proof of Energy Concentration**, you must supplement Gonek’s theorem with a **Variance Bound**. You have already begun this by reporting the **GUE RMSE = 0.066**. This low RMSE is the "smoking gun" indicating that the energy is *not* distributed uniformly, but is instead subject to the localized fluctuations characteristic of the GUE (Gaussian Unitary Ensemble) statistics. 

**Recommendation:** Focus the next phase of the Lean 4 verification on the **Second Moment of the Dirichlet Polynomial** $\sum |A(\rho)|^4$. If the ratio of the 4th moment to the square of the 2nd moment exceeds the GUE prediction, you will have successfully moved from a "Total Energy" statement to an "Energy Concentration" statement.
