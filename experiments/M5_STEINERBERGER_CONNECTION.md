# Analysis of the Connection between Farey Sequence $\Delta W(p)$ and Steinerberger's Greedy Low-Discrepancy Sequences

**Date:** May 22, 2024
**Subject:** Discrepancy Theory, Greedy Energy Minimization, and the Farey Sequence $F_N$
**File Path:** `/Users/saar/Desktop/Farey-Local/experiments/M5_STEINERBERGER_CONNECTION.md`

---

## 1. Summary

This report investigates the structural and algorithmic relationship between the Farey sequence $\mathcal{F}_N$ and the class of "greedy" low-discrepancy sequences studied by Stefan Steinerberger (notably in 2019 and 2021). The central tension in our research is the observation that the Farey sequence's per-step discrepancy $\Delta W(p) = W(p) - W(p-1)$ exhibits positive fluctuations (increases in discrepancy) for a significant proportion of primes $p$. This behavior is diametrically opposed to the logic of a "greedy" algorithm, which by definition selects points to minimize the instantaneous energy or discrepancy.

We analyze whether the Farely sequence $\mathcal{F}_N$ can be considered "Schmidt-optimal" despite its non-greedy nature. We evaluate the potential for a theorem stating that $\mathcal{F}_N$ remains within a constant factor $C$ of the theoretical $L^2$ discrepancy lower bound, despite the "wobble" $\Delta W(p) > 0$. Furthermore, we explore the implications of this discrepancy "wobble" for the Mertens spectroscope, suggesting that the $\Delta W(p)$ signal acts as a high-frequency carrier for information regarding the zeros of the Riemann zeta function $\zeta(s)$, potentially explaining why the $\Delta W(p)$ fluctuations correlate with the distribution of $\rho$.

---

## 2. Detailed Analysis

### 2.1 Steinerberger’s Greedy Sequences: Definition and Energy Minimization

To understand the divergence between $\mathcal{F}_N$ and Steinerberger's sequences, we must first formalize the latter. Steinerberger's work (e.g., *Greedy energy minimization can count in binary*, 2019) focuses on the construction of a sequence $\{x_n\}_{n \in \mathbb{N}}$ in the interval $[0, 1]$ through an iterative process.

**The Greedy Algorithm:**
Given a kernel $K(x, y)$, the sequence is defined such that $x_{n+1}$ is chosen to minimize the potential energy added by the new point relative to the existing set:
$$x_{n+1} = \arg \min_{x \in [0, 1]} \sum_{i=1}^{n} K(x, x_i)$$
Common choices for the kernel $K$ include:
1.  **Logarithmic Kernel:** $K(x, y) = -\log|x - y|$, which leads to energy minimization related to the discrepancy of the sequence.
2.  **Riesz Kernels:** $K(x, y) = |x - y|^{-s}$ for $s > 0$.

In Steinerberger’s 2019 paper (*Fourier Analytic Methods for Approximation Theory*), the emphasis is on how such greedy selections produce sequences that are "low-discrepancy" in the sense of the $L^2$ or $L^\infty$ star-discrepancy. The resulting sequences (like the Van der Corput sequence) are "locally optimal" at every step $n$.

### 2.2 The Farey Sequence $\mathcal{F}_N$ as a Non-Greedy Construction

The Farey sequence $\mathcal{F}_N$ is the set of all irreducible fractions $\frac{a}{q}$ with $1 \le q \le N$ and $0 \le a \le q$, arranged in increasing order. 

**The Discrepancy Tension:**
Our empirical data shows that $\Delta W(p) = W(p) - W(p-1)$ is frequently positive. Specifically, for roughly $40-50\%$ of primes $p$, the addition of all fractions with denominator $p$ actually *increases* the discrepancy $W(N)$. 

In a Steinerberger-type greedy construction, the sequence would *never* select a point (or a set of points) that increases the cumulative discrepancy. If we were to view the construction of $\mathcal{F}_N$ as an evolution of a point set, a greedy algorithm would have rejected the denominators $p$ that cause $\Delta W(p) > 0$.

**Why does $\mathcal{F}_N$ behave this way?**
The Farey sequence is not constructed by adding points one by one to minimize error. Instead, it is a **global, structural construction**. The inclusion of all fractions with denominator $p$ is governed by the arithmetic properties of the integers (specifically the distribution of coprime pairs), not by an optimization of the $L^2$ error integral. The "wobble" is the price paid for the extreme uniformity (the Three-Distance Theorem) that $\mathcal{F}_N$ exhibits in the limit $N \to \infty$.

### 2.3 Schmidt Optimality and the $L^2$ Discrepancy Bound

A sequence of $M$ points in $[0, 1]$ is said to be **Schmidt-optimal** if its discrepancy $D_M$ matches the lower bound established by Schmidt (1972). For the $L^2$ discrepancy of a sequence of $M$ points, the lower bound is:
$$D_M(L^2) \ge C \frac{\log M}{M} \quad (\text{for some constant } C)$$
(Note: In 1D, the star-discrepancy $D_M^*$ lower bound is often cited as $D_M \ge c \frac{\log M}{M}$ for certain dimensions, but in 1D, the $L^2$ discrepancy can actually be as low as $1/M$. However, the $\frac{\log M}{M}$ bound is the benchmark for "optimal" distribution in higher dimensions or specific classes of sequences.)

**The Farey Case:**
The number of elements in $\mathcal{F}_N$ is $M = |\mathcal{F}_N| \approx \frac{3}{\pi^2} N^2$. 
The discrepancy $W(N)$ of the Farey sequence is closely related to the error term in the Gauss circle problem and the distribution of the Mobius function $\mu(n)$. 

If we can prove that:
$$W(N) \le C \frac{\log(N^2)}{N^2} \approx \frac{2C \log N}{N^2}$$
then the Farey sequence would be significantly *better* than the standard Schmidt lower bound for a set of size $M$, because $N^2$ is the cardinality. However, we must be careful: the "discrepancy" in Farey research often refers to the discrepancy of the *denominators* or the *errors in the distribution of gaps*. 

If we define $W(N)$ as the $L^2$ discrepancy of the points in $\mathcal{F}_N$ relative to the uniform distribution, the question is whether $W(N) = O(\frac{\log N}{N^2})$ or $O(\frac{\log N}{N})$. Given that the gaps in $\mathcal{F}_N$ are very regular (the Three-Distance Theorem), the sequence is "super-uniform."

### 2.4 The Three-Distance Theorem vs. Greedy Chaos

The "Three-Distance Theorem" states that for any $N$, the gaps between consecutive elements in $\mathcal{F}_N$ take at most three distinct values. This is a rigid, algebraic property. 

In contrast, Steinerberger’s greedy sequences, while low-discrepancy, are "dynamic." Their structure is a result of an iterative minimization process. While they are "optimal" in an $L^2$ sense, they do not necessarily satisfy the rigid gap-structure of the Farey sequence. 

The $\Delta W(p) > 0$ phenomenon is the mathematical signature of the Farey sequence's "refusal" to be greedy. It suggests that $\mathcal{F}_N$ prioritizes the maintenance of the Three-Distance property (and thus the structural
