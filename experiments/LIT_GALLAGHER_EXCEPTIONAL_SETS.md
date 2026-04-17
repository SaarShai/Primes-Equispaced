# Research Report: Analysis of Gallagher's Exceptional Set Technique and Pointwise Convergence in Farey Discrepancy $D_K$

**Date:** May 22, 2024  
**Subject:** Investigation of Exceptional Sets in Sheth (2025b) and the Pointwise Convergence of $D_K$  
**Project:** Farey Sequence Discrepancy $\Delta W(N)$ and $L$-function Spectroscopy  
**File Path:** `/Users/saar/Desktop/Farey-Local/experiments/LIT_GALLAGHER_EXCEPTIONAL_SETS.md`

---

## 1. Summary

This report investigates the mathematical tension between the "almost everywhere" convergence results presented in Sheth (2025b) and the empirical evidence of pointwise convergence for the Farey discrepancy constant $D_K$ towards $1/\zeta(2)$. Using the framework of Gallagher’s (1980) exceptional set technique and the analytic tools found in Montgomery-Vaughan (Chapter 15), we analyze whether the convergence of $D_K \zeta(2) \to 1$ is subject to a set of "bad" parameters $K$ of finite logarithmic measure, or if the observed local verification ($|D_K| \zeta(2) \approx 0.984$ at $K=10^4$) implies a stronger, pointwise convergence. We conclude that while Gallagher’s method naturally permits an exceptional set, the transition to pointwise convergence requires a breakthrough in controlling the $L$-function's supremum norm over the critical line, specifically an advancement beyond current zero-density estimates.

---

## 2. Detailed Analysis

### I. Task 1: Survey of Gallagher (1980) and Montgomery-Vaughan (Ch 15)

The fundamental challenge in the distribution of primes and the error terms of arithmetic functions (like the Farey discrepancy $\Delta W(N)$) is that while the "average" behavior is well-governed by the Riemann Hypothesis (RH), individual values of $t$ (or $N$) can exhibit large oscillations driven by the local configuration of zeros $\rho = \beta + i\gamma$.

#### 1.1 Gallagher’s Exceptional Set Technique
In *“Some consequences of the Riemann hypothesis”* (Acta Arith. 37, 1980), Gallagher developed a method to bound the measure of the set of $t \in [T, 2T]$ for which an arithmetic estimate fails. The core of the technique is not to prove the estimate for *all* $t$, but to show that the set $S = \{t \in [T, 2T] : |\text{Error}(t)| > \epsilon\}$ satisfies:
$$\text{meas}(S) \ll T^{1-\delta}$$
for some $\delta > 0$. Gallagher's innovation lies in the use of **large sieve inequalities** and **zero-density estimates** to bound the contribution of the zeros $\rho$ that are "too far" from the critical line or "too clustered." 

In the context of Sheth (2025b), the "logarithmic measure" $\mu^x(S) = \int_{S} \frac{dt}{t}$ is the natural metric. A set $S$ has finite logarithmic measure if the integral converges as $T \to \infty$. This implies that as we move up the critical line, the "bad" values of $K$ (or $N$) become increasingly sparse, such that the probability of encountering a "bad" $K$ vanishes in the logarithmic sense.

#### 1.2 Montgomery-Vaughan (Ch 15) and the Analytic Foundation
Montgomery and Vaughan’s treatment of the Large Sieve and the distribution of zeros provides the machinery to quantify these exceptional sets. Specifically, Chapter 15 focuses on the distribution of the zeros of $\zeta(s)$ and $L(s, \chi)$. The "exceptional set" in their context often refers to the set of Dirichlet characters $\chi$ for which the $L$-function possesses a "Siegel zero" or where the distribution of $\gamma$ deviates from the GUE (Gaussian Unit-Ensemble) prediction.

The technique involves:
1.  **Smoothing:** Replacing the discrete sum over zeros with a smooth integral using a kernel (e.g., Beurling-Selberg).
2.  **Zero-Density Estimates:** Using bounds of the form $N(\sigma, T) \ll T^{A(1-\sigma)}$ to show that zeros with $\beta > 1/2$ are rare.
3.  **Mean-Value Theorems:** Applying $L^2$ estimates to show that the variance of the error term is small, which inherently allows for an exceptional set where the error is large.

### II. Task 2: The Nature of the Exceptional Set for $D_K$

We are examining the identity $D_K = c_K E_K$, where $E_K$ is the error term and $c_K$ is a scaling constant. The central question is: **Does the convergence of $D_K \zeta(2) \to 1$ require an exceptional set?**

#### 2.1 The "Almost Everywhere" Argument
Sheth's Theorem A implies that for any $\epsilon > 0$, the estimate $|D_K \zeta(2) - 1| < \epsilon$ holds for $K \notin S$, where $\int_S \frac{dK}{K} < \infty$. This is a "weak" convergence. It allows for the possibility that there exist infinitely many $K$ where $D_K$ deviates wildly from $1/\zeta(2)$, provided these $K$ are spaced far enough apart (e.g., $K_n = e^{n^2}$).

#### 2.2 The "Pointwise" Evidence
Our local computation at $K=10^4$ yields:
$$|D_K| \zeta(2) = 0.9837 \pm 0.01$$
This value is remarkably close to 1. The error is only $\approx 1.6\%$. If $D_K$ were subject to a significant exceptional set of $K$ values, one would expect a much wider dispersion in the $L^1$ or $L^2$ norm of the discrepancy across different $K$. 

The fact that the $D_K$ value for the specific $\chi_{-4}$ pair at $K=10^4$ is so stable suggests that we are not merely in a "good" window of the logarithmic measure, but that the convergence might be **pointwise**. In the theory of such discrepancies, pointwise convergence is usually equivalent to the non-existence of "large" clusters of zeros near the critical line that could constructively interfere to create a massive $\Delta W(N)$ spike.

### III. Task 3: Size of the Exceptional Set and AK2023

#### 3.1 Sheth's Set Size
In Sheth (2025b), the exceptional set $S$ is defined by its logarithmic measure. In practice, for $K$ in the range of $10^4$ to $10^6$, a set of finite log measure is nearly invisible unless the "bad" $K$ are extremely large. However, if the set $S$ contains values where $\Delta W(N)$ is $O(N^{1/2+\epsilon})$, these would be detectable as massive spikes in the "spectroscope."

#### 3.2 Koyama/Aoki (AK2023)
Koyama and Aoki (2023) focus on the distribution of the error term in the Farey sequence. While they address the statistical distribution (the $L^2$ behavior), their treatment of exceptional sets is primarily through the lens of zero-density. They prove that the distribution converges to a limiting distribution (related to the distribution of $\zeta$ zeros). Their work implies that "large" deviations are extremely rare, but they do not explicitly eliminate the existence of an exceptional set for the *constant* $D_K$.

If $D_K$ is the scaling factor for the error term, and the error term's distribution is determined by the zeros, then any $K$ that corresponds to a "near-miss" of a zero (a $\rho$ very close to the critical line or an unusually high density of zeros) would constitute an element of Sheth's exceptional set.

### IV. Task 4: The Missing Ingredient for Pointwise Proof

To prove $D_K \to 1/\zeta(2)$ **pointwise** (without an exceptional set), we must prove that the error term $E_K$ cannot exceed a certain threshold for *all* $K > K_0$.

#### 4.1 The Obstacle: The Supremum Norm
The current tools (Gallagher/Sheth) are $L^p$ tools. They bound the integral of the error. To move to pointwise, we need an $L^\infty$ bound:
$$\sup_{K \geq K_0} |D_K \zeta(2) - 1| \to 0$$
The "missing ingredient" is a **uniform bound on the oscillation of the $L$-function's argument near the critical line.** Specifically, we need to control the "local" influence of the zeros $\rho_j$ on the sum:
$$\sum_{\gamma < T} \frac{1}{\frac{1}{2} + i\gamma}$$
If we can prove that no cluster of zeros can ever exist such that their combined contribution to the Farey sum $\Delta W(N)$ exceeds $\epsilon \cdot N^{1/2}$, we achieve pointwise convergence. This is essentially a requirement for a "Strong Lindelöf" type property for the Farey sum, which is currently unproven.

### V. Task 5: Numerical Test Plan

To determine if we are looking at an exceptional set or pointwise convergence, we propose the following experiment:

**Goal:** Test the variance of the deviation $\delta(K) = |D_K \zeta(2) - 1|$ across a logarithmic scale.

1.  **Sampling Strategy:**
    *   Select $K$ values in a geometric progression: $K_n = 10^n$ for $n \in \{3, 4, 5, 6, 7\}$.
    *   For each $K_n$, compute $D_K \zeta(2)$ using the provided NDC pairs ($\chi_{-4}, \chi_5, \chi_{11}$).
2.  **Metric 1: Variance Decay:**
    *   Calculate $\text{Var}(\delta(K_n))$. 
    *   If $\text{Var}(\delta(K_n)) \to 0$ as $n \to \infty$, it supports the **Pointwise Hypothesis**.
    *   If $\text{Var}(\delta(K_n))$ remains bounded or grows, it supports the **Exceptional Set Hypothesis**.
3.  **Metric 2: Extreme Value Analysis:**
    *   Search for "spikes" in $\delta(K)$. 
    *   Compute the ratio $\mathcal{R} = \max(\delta(K)) / \text{mean}(\delta(K))$. 
    *   If $\mathcal{R} \approx 1$, the distribution is tight (Pointwise). If $\mathcal{R} \gg 1$, we have found an element of the exceptional set (Sheth).
4.  **Computational Implementation:**
    *   Use `mpmath` for high-precision evaluation of $L(s, \chi)$ at the provided $\rho$ values.
    *   Implement the $S = \text{arccosh}(\text{tr}(M)/2)$ trace formula for the
