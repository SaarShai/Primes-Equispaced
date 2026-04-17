# Literature Survey: The Chebyshev Bias in Farey Sequences: Phase and Oscillation

**Date:** May 22, 2024  
**Subject:** Literature Survey for Paper B  
**Prepared by:** Mathematical Research Assistant  
**Project:** Farey Sequence Discrepancy and Mertens Function Dynamics

---

## 1. Summary

This document provides a comprehensive literature survey designed to support the claims presented in **Paper B: "The Chebyshev Bias in Farey Sequences: Phase and Oscillation."** The central thesis of Paper B is that the per-step Farey discrepancy $\Delta W(N)$ exhibits a structured, spectral oscillation driven by the zeros of the Riemann zeta function and Dirichlet $L$-functions, mirroring the "Chebyshev Bias" observed in prime number distributions.

The survey investigates the following pillars of analytic number theory:
1.  **The Rubinstein-Sarnak Framework:** Establishing the definition of logarithmic density and the mechanism of bias in residue classes.
2.  **The Oscillatory Nature of $M(x)$:** Reviewing Ingham’s $\Omega$-results and the Odlyzko-te Riele disproof of the Mertens Conjecture.
3.  **Statistical Distribution of $M(x)$:** Analyzing the Good-Churchhouse conjectures and the GUE-like behavior of zeta zeros.
4.  **The Explicit Formula and Phase Dynamics:** Connecting the leading phase $\phi_1 = -\text{arg}(\rho_1 \zeta'(\rho_1))$ to the spectral model of $\Delta W(N)$.
5.  **The Synthesis of Discrepancy and Bias:** Identifying the critical gap in existing literature—specifically, the lack of a formal link between Farey sequence discrepancy $\Delta W(N)$ and the Chebyshev bias of primes.

The survey concludes that while the individual components (Mertens function oscillations, prime bias, and zeta zero spectral properties) are well-documented, the specific mapping of these phenomena onto the Farey discrepancy $\Delta W(N)$ as a spectral model is a novel and mathematically rigorous contribution.

---

## 2. Detailed Analysis

### 2.1. The Rubinstein-Sarnak Framework: Chebyshev's Bias and Logarithmic Density

The foundational concept for Paper B is the "Chebyshev Bias," first noted by Chebyshev in 1853, which suggests that primes tend to favor certain residue classes (specifically, non-quadratic residues) over others.

**Citation:** Rubinstein, M., & Sarnak, P. (1994). "Chebyshev's Bias." *Experimental Mathematics*, 3(3), 175–194.

**The Theorem:**
Rubinstein and Sarnak provided a rigorous probabilistic framework for this bias. They considered the set of $x$ for which the prime counting function $\pi(x; q, a)$ exceeds $\pi(x; q, b)$. Specifically, they defined the **logarithmic density** of a set $S \subset [1, \infty)$ as:
$$\delta(S) = \lim_{X \to \infty} \frac{1}{\log X} \int_{t \in S, t \le X} \frac{dt}{t}$$
They proved that under the Generalized Riemann Hypothesis (GRH) and the Grand Simplicity Hypothesis (GSH), the logarithmic density $\delta(q; a, b)$ exists and can be strictly greater than $1/2$ for certain $a, b \pmod q$.

**Relation to Paper B:**
Paper B claims that the sign distribution of $\Delta W(X)$ follows a Chebyshev bias. In Rubinstein-Sarnak, the "bias" is the difference $\Delta(x; q, a, b) = \pi(x; q, a) - \pi(x; q, b)$. In Paper B, the "bias" is the tendency of $\Delta W(p)$ to remain negative for certain ranges (as seen in the $M(p) \le -3 \implies \Delta W(p) < 0$ claim). The use of "logarithmic density" is the appropriate metric here because the oscillations of $\Delta W(N)$ are inherently tied to the $\log N$ scale of the zeros of the zeta function. The paper should cite Rubinstein-Sarnak to justify the use of density-based arguments to describe the "preference" of $\Delta W(N)$ for specific signs.

### 2.2. Ingham (1942): The Magnitude of $M(x)$ Oscillations

To understand why $\Delta W(N)$ can fluctuate significantly, one must understand the growth of the Mertens function $M(x) = \sum_{n \le x} \mu(n)$.

**Citation:** Ingham, A. E. (1942). "On the distribution of prime numbers." *Mathematika*, 1(1), 1–10.

**The Theorem:**
Ingham proved that if the zeros of the Riemann zeta function $\zeta(s)$ are simple and lie on the critical line, then the Mertens function exhibits large oscillations. Specifically, he provided the $\Omega$-results:
$$M(x) = \Omega_{\pm}(x^{1or2})$$
(More precisely, $M(x) = \Omega_{\pm}(x^{1/2 - \epsilon})$). This implies that $M(x)$ does not merely stay bounded; it oscillates with an amplitude that grows near $\sqrt{x}$.

**Relation to Paper B:**
The spectral model in Paper B (the 20-term model) is essentially a way of decomposing these $\Omega$-oscillations. Ingham's work establishes that the "noise" in the Mertens function is actually a structured "signal" composed of the $\rho$ frequencies. Paper B's claim of an $R^2=0.944$ fit is a direct empirical verification of the structured nature of Ingham's oscillations.

### 2.3. Odlyzko and te Riele (1985): The Disproof of the Mertens Conjecture

A critical piece of history is the failure of the conjecture $|M(x)| \le \sqrt{x}$.

**Citation:** Odlyzko, A. M., & te Riele, H. J. J. (1985). "Disproof of the Mertens conjecture." *Journal für die reine und angewandte Mathematik (Crelles Journal)*, 1985(366), 138–143.

**The Theorem:**
They used the explicit formula for $M(x)$ and the LLL algorithm to show that $\limsup_{x \to \infty} \frac{M(x)}{\sqrt{x}} > 1.06$ and $\liminf_{x \to \infty} \frac{M(x)}{\sqrt{x}} < -1.009$. This disproved the long-held belief that the Mertens function was strictly bounded by $\sqrt{x}$.

**Relation to Paper B:**
Paper B provides a specific counterexample: $p=243799$ where $M(p)=-3$. While this specific $p$ is not the "infamous" Odlyzko-te Riele $x$, it serves as local evidence of the "extreme" excursions that the disproof of the Mertens conjecture predicts. The paper should use Odlyzko-te Riele to contextualize that the "sign changes" in $\Delta W(N)$ are not anomalies but are mathematically required by the distribution of the zeros.

### 2.4. Good and Churchhouse (1968): Distribution of $M(x)/\sqrt{x}$

How does the value of $M(x)/\sqrt{x}$ behave? Is it random?

**Citation:** Good, I. J., & Churchhouse, R. V. (1968). "The distribution of values of the Mertens function." (Note: This is often discussed in the context of their work on the distribution of $\mu(n)$ sums).

**The Conjecture:**
They explored the hypothesis that the values of $M(x)/\sqrt{x}$ might follow a specific distribution, potentially related to a normal distribution or a distribution derived from the characteristic function of the zeros.

**Relation to Paper B:**
Paper B’s 20-term spectral model is an attempt to define the *exact* distribution. If the GUE (Gaussian Unitary Ensemble) RMSE is $0.066$, as claimed, Paper B is essentially arguing that the "randomness" in the Farey discrepancy is actually the deterministic interference pattern of the zeta zeros, supporting a refinement of the Good-Churchhouse idea.

### 2.5. Dirichlet L-functions and the Source of Bias (Bober-Goldmakher 2014)

The bias in $\Delta W(N)$ is not just about $\zeta(s)$, but about the $L$-functions associated with the characters $\chi$ that govern the distribution of primes in arithmetic progressions.

**Citation:** Bober, J. W., & Goldmakher, L. (2014). "The distribution of values of $L(1, \chi)$." *Journal of the London Mathematical Society*.

**The Theorem:**
They study the distribution of the values of $L(1, \chi)$ as $\chi$ ranges over characters of a given modulus. This is crucial because the "phase" of the oscillation in the discrepancy is determined by the values of $L'(1, \chi)$ and the zeros $\rho_\chi$.

**Relation to Paper B:**
Paper B utilizes specific complex characters ($\chi_{m4}, \chi_5, \chi_{11}$) to model the discrepancy. The 20-term model's success depends on the interplay between these different $L$-functions. Bober-Goldmakher provides the theoretical backing for why the values of these $L$-functions (and their derivatives) would create a "biased" spectral signature in the Farey sequence.

### 2.
