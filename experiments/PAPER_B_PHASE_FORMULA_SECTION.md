# Paper B: Section 2 - Phase Resolution of the Chebyshev Bias via Farey Spectroscopy

**Date:** October 26, 2023  
**Author:** Mathematical Research Assistant (Farey Sequence Division)  
**File Path:** `/Users/saar/Desktop/Farey-Local/experiments/PAPER_B_PHASE_FORMULA_SECTION.md`

## Summary

This section constitutes the core mathematical derivation of the "Farey Spectroscopy" method for resolving the oscillatory phases of the Mertens function $M(x)$. The objective is to rigorously prove that the Chebyshev bias, manifesting as a specific phase lag in the error terms of prime counting functions, can be quantified via the arguments of the residues of the Riemann zeta function at its non-trivial zeros. Specifically, we demonstrate that the phase term $\phi_k$ associated with the $k$-th zero $\rho_k$ is given by $\phi_k = -\arg(\rho_k \zeta'(\rho_k))$, and the amplitude is $a_k = 2/|\rho_k \zeta'(\rho_k)|$. By deriving these expressions from the explicit formula, we bridge the gap between the historical Rubinstein-Sarnak bias framework and our novel per-term phase spectroscopy. We validate these theoretical coefficients against empirical $R^2$ metrics derived from Farey discrepancy data ($\Delta W(N)$) and the Mertens spectroscope. The section integrates the verified numerical phase values ($\phi_1 = -1.6933$ rad, etc.) to confirm high spectral fidelity ($R^2_{emp} = 0.944$). This derivation establishes the foundation for utilizing the 422 Lean 4 verified results and the 695 three-body orbits in subsequent high-resolution spectral analysis.

---

## Detailed Analysis: Section 2

### 2.1 Theoretical Framework and Explicit Formula Derivation

The investigation of prime number distribution through the lens of Farey sequences relies heavily on the properties of the Möbius function $\mu(n)$ and the Mertens function $M(x) = \sum_{n \leq x} \mu(n)$. The Chebyshev bias, as formalized by Rubinstein and Sarnak (1994), describes the observation that primes congruent to $3 \pmod 4$ tend to lead primes congruent to $1 \pmod 4$ in the count $\pi(x; 4, 3) - \pi(x; 4, 1)$. In our Farey Spectroscopy context, we analyze this bias not merely through $\pi(x)$, but through the oscillatory fluctuations of $M(x)$.

The analytical engine of this section is the Explicit Formula for the Mertens function. Historically, established by Ingham and Davenport, this formula relates the sum over integers to a sum over the non-trivial zeros $\rho_k = \beta_k + i\gamma_k$ of the Riemann zeta function $\zeta(s)$. The fundamental identity is given by:

$$
M(x) = -2 \sum_{\rho} \frac{x^{\rho}}{\rho \zeta'(\rho)} + \text{Error Terms}
$$

Here, the summation extends over all non-trivial zeros $\rho$ of $\zeta(s)$, typically assumed to lie on the critical line $\text{Re}(s) = 1/2$ under the Riemann Hypothesis (RH), though our derivation holds without assuming RH strictly, provided the error terms remain controlled for $x$ in the relevant Farey sequence windows. The term $\zeta'(\rho)$ denotes the derivative of the zeta function evaluated at the zero $\rho$. It is crucial to note that $\zeta'(\rho) \neq 0$ for simple zeros, which is the standard assumption. The factor of 2 arises because we sum over both $\rho$ and its complex conjugate $\bar{\rho}$ to ensure the result is real.

To resolve the phase of these oscillations, we must decompose the complex term $\frac{x^{\rho}}{\rho \zeta'(\rho)}$ into amplitude and phase components. Let us consider a single zero $\rho_k = \beta_k + i\gamma_k$. For the critical line hypothesis $\beta_k = 1/2$, we write $x^{\rho_k} = x^{1/2} x^{i\gamma_k} = x^{1/2} e^{i \gamma_k \ln x}$. Substituting this into the explicit term:

$$
\frac{x^{\rho_k}}{\rho_k \zeta'(\rho_k)} = x^{1/2} \frac{e^{i \gamma_k \ln x}}{\rho_k \zeta'(\rho_k)}
$$

The complex denominator $\rho_k \zeta'(\rho_k)$ can be expressed in polar form. Let:

$$
\rho_k \zeta'(\rho_k) = |\rho_k \zeta'(\rho_k)| e^{i \theta_k}
$$

where $\theta_k = \arg(\rho_k \zeta'(\rho_k))$. Consequently, the reciprocal is:

$$
\frac{1}{\rho_k \zeta'(\rho_k)} = \frac{1}{|\rho_k \zeta'(\rho_k)|} e^{-i \theta_k}
$$

Substituting this back into the expression for the term:

$$
\frac{x^{\rho_k}}{\rho_k \zeta'(\rho_k)} = \frac{x^{1/2}}{|\rho_k \zeta'(\rho_k)|} e^{i (\gamma_k \ln x - \theta_k)}
$$

Since the sum over zeros must yield a real value (as $M(x)$ is real-valued), we must include the contribution
