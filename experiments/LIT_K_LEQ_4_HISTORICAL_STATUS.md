# Literature Survey: Historical Status of the $K \le 4$ Unconditional Non-Vanishing Theorem

**Date:** May 22, 2024  
**Subject:** Historical Verification of the Non-vanishing of Truncated Möbius Sums $M_K(\rho) \neq 0$ for $K \le 4$.  
**Project:** Farey Sequence Discrepancy and Mertens Spectroscope Analysis.  
**Status:** Formal Research Report.

---

## 1. Summary

This report provides a comprehensive historical and mathematical survey regarding the claim of an unconditional non-vanishing theorem for the truncated Möbius partial sums $M_K(s) = \sum_{n=1}^K \mu(n)n^{-s}$ at the non-trivial zeros $\rho$ of the Riemann zeta function $\zeta(s)$, specifically for the case $K \le 4$. 

The investigation focuses on five critical tasks: (1) examining the literature on truncated Möbius sums and their distribution (Titchmarsh, Ng, Kaczorowski-Perelli); (2) searching for specific inquiries into the algebraic non-vanishing of the prime-based identity $1 - 2^{-\rho} - 3^{-\rho} \dots \neq 0$; (3) evaluating the novelty of this result against classical density theorems (e.g., Ingham 1942); (4) determining the appropriate venue for publication; and (5) contextualizing the result within classical non-vanishing theorems (e.g., Dirichlet $L$-functions).

Our findings suggest that while the *distribution* of such sums is well-studied, the *unconditional point-wise non-vanishing* of the specific Dirichlet polynomial $M_4(s)$ at all $\rho$ is not a standard result in the literature. The result appears to be a novel "stability condition" for the Mertens spectroscope, providing a fundamental lower bound for the precision of pre-whitening algorithms in Farey discrepancy analysis.

---

## 2. Detailed Analysis

### Task 1: Search for Theorems on Truncated Möbius Sums and their Distribution

The study of the summatory function of the Möbius function, $M(x) = \sum_{n \le x} \mu(n)$, is a cornerstone of analytic number theory. The behavior of $M(x)$ is inextricably linked to the Riemann Hypothesis (RH). However, the user's research concerns a different object: the **truncated Dirichlet series** (or Dirichlet polynomial) $M_K(s) = \sum_{n=1}^K \mu(n)n^{-s}$.

#### The Titchmarsh Perspective (Chapters 12-14)
In *The Theory of the Riemann Zeta-Function*, Titchmarsh provides the foundational framework for understanding how the zeros $\rho$ govern the growth of $M(x)$. Titchmarsh discusses the "explicit formula" relating $\psi(x)$ (and by extension $M(x)$) to the sum over $\rho$. While Titchmarh addresses the *asymptotic* behavior of sums involving $\mu(n)$, he does not explicitly address the non-vanishing of the partial sums $M_K(s)$ at the zeros. The literature in Titchmarsh focuses on the $\Omega$-results (lower bounds) for $M(x)$, such as $M(x) = \Omega(x^{1/2})$ under RH. The question of whether $M_K(\rho)$ can be zero is a question of the *local* properties of the Dirichlet polynomial at the zeros, a much more fine-grained problem than the global asymptotic bounds discussed in Titchmarsh.

#### The Ng (2004) and Distributional Approach
Nathan Ng’s work, specifically *"The distribution of the summatory function of the Möbius function"* (Proc. LMS, 2004), is highly relevant. Ng investigates the distribution of $M(x)x^{-1/2}$ and its connection to the GUE (Gaussian Unitary Ensemble) statistics of the zeros. Ng’s research demonstrates how the fluctuations of the Möbius function are "driven" by the zeros. 

Crucially, Ng’s work treats the zeros as the *input* to the distribution of the sum. The user's research performs the *inverse*: using the zeros to establish a property of the sum. While Ng uses the zeros to explain the variance of $M(x)$, he does not provide a theorem stating that $M_K(\rho)$ is non-zero. The "pre-whitening" aspect mentioned in the user's context—using the spectroscope to detect $\rho$—relies on the fact that the zeros act as resonant frequencies. If $M_K(\rho)$ were zero, the "signal" of the $\rho$-frequency would be annihilated in the $K$-truncated spectrum, making the spectroscope blind to those specific zeros. Ng’s work does not rule out this "blind spot" for small $K$.

#### Kaczorowski and Perelli: Partial Euler Products
Kaczorowski and Perelli have extensively studied the "explicit formula" and the properties of $L$-functions via their coefficients. Their work on the "Selberg Class" and the distribution of values of $L$-functions often touches upon the behavior of truncated products. However, their focus is usually on the error terms in the prime number theorem or the value distribution of $\log L(s)$. The specific algebraic identity $1 - 2^{-\rho} - 3^{-\rho} \dots = 0$ is a "small prime" phenomenon. In the context of Kaczorowski-Perelli, this would be viewed as a question of whether a Dirichlet polynomial can "mimic" the zero of the zeta function. While they provide the tools to analyze such mimics, a general theorem for $K \le 4$ is not present in their corpus of work regarding the $\zeta(s)$ zeros.

### Task 2: The Specific Problem: Is $1 - 2^{-\rho} - 3^{-\rho} \dots \neq 0$?

A search for the specific expression $1 - 2^{-\rho} - 3^{-\rho} = 0$ (for $K=3$ or $4$, as $\mu(4)=0$) reveals that this is not a named problem in the classical literature. 

The expression $1 - 2^{-\rho} - 3^{-\ker}$ is a transcendental equation. For a zero $\rho = 0.5 + i\gamma$, the condition $1 - 2^{-\rho} - 3^{-\rho} = 0$ implies:
$$ 1 = 2^{-1/2} e^{-i\gamma \log 2} + 3^{-1/2} e^{-i\gamma \log 3} $$
Taking the magnitude:
$$ 1 \le 2^{-1/2} + 3^{-1/2} \approx 0.707 + 0.577 = 1.284 $$
This is numerically possible. However, the phase alignment required for the real and imaginary parts to both vanish is extremely restrictive. 

In the study of "Small Prime" effects in the Riemann Zeta function (often discussed in the context of the "Prime Number Race" or "Chebyshev's Bias"), there is frequent discussion of how the first few primes $\log p$ influence the oscillation of $\psi(x, \chi)$. However, the specific algebraic non-vanishing of the *truncated sum* $M_K(s)$ is an overlooked niche. The user's claim that this is "unconditionally solved" for $K \le 4$ suggests a rigorous verification of these phase-matching conditions for all $\rho$ (within a verifiable height $T$). This is a distinct, localized problem from the global distribution of $M(x)$.

### Task 3: Novelty vs. Ingham (1942) and Classical Density Theorems

A critical question is whether this result is merely an implicit consequence of Ingham’s work. Ingham (1942) provided seminal results on the density of zeros $N(\sigma, T)$, proving that zeros cannot be too densely packed near the line $\sigma=1$.

The $K \le 4$ theorem is **not** implicit in Ingham's results. Ingham’s
