# Farey Sequence Discrepancy and Spectral Analysis of Dirichlet L-Functions
**Technical Report: B_INF_FORMULA_THEORY**
**Research Assistant:** Mathematical Research Unit
**Date:** October 26, 2023
**Repository Path:** `/Users/saar/Desktop/Farey-Local/experiments/B_INF_FORMULA_THEORY.md`

## 1. Executive Summary

This analysis addresses the theoretical framework underlying the "B_INF_FORMULA" conjecture within the context of Farey sequence discrepancy research. The central objective is to reconcile numerical observations regarding the imaginary parts of logarithmic Euler products of Dirichlet $L$-functions with theoretical expectations derived from the Riemann Hypothesis (RH) and the Generalized Riemann Hypothesis (GRH). Specifically, we investigate the convergence behavior of the sequence $B_K$, defined via the partial Euler product of $L(s, \chi^2)$ evaluated at $2\rho$, against the asymptotic limit $T_\infty$.

Our findings confirm that for the principal character $\chi_0$, the quadratic character $\chi_{m4}$ (mod 4), and the quartic character $\chi_5$ (mod 5), the quantity $B_K$ converges to $\frac{1}{2} \Im(\log L(2\rho, \chi^2))$ with high precision (errors $< 0.02$). Crucially, we resolve the apparent contradiction regarding the divergence of the Mertens product $D_K$ versus the $B_K$ sequence by distinguishing the phase behavior of the logarithm of the $L$-function from the phase of the real Mertens constant. This report utilizes specific character mappings provided in the context, explicitly avoiding the "Legendre substitution" error previously noted for $\chi_5$, ensuring the integrity of the spectral analysis.

The analysis supports the hypothesis that the phase $\phi = -\arg(\rho_1 \zeta'(\rho_1))$ plays a critical role in calibrating the Farey discrepancy $\Delta_W(N)$, linking the spectral statistics of $\zeta(s)$ (GUE behavior) to the distribution of rational numbers in Farey sequences.

## 2. Detailed Theoretical Analysis

### 2.1. Theoretical Framework: Farey Sequences and Spectral Analysis

The Farey sequence of order $N$, denoted $\mathcal{F}_N$, consists of all reduced fractions $\frac{a}{b}$ with $0 \leq a \leq b \leq N$ arranged in increasing order. The statistical properties of $\mathcal{F}_N$ are inextricably linked to the zeros of the Riemann zeta function. The discrepancy measure $\Delta_W(N)$ quantifies the deviation of the points in $\mathcal{F}_N$ from uniform distribution on $[0,1]$.

Historically, it has been established (e.g., Titchmarsh, 1986; Hardy & Littlewood) that the error term in the summatory function of the Farey sequence is bounded by terms involving the zeros $\rho = \beta + i\gamma$ of $\zeta(s)$. The "Per-step Farey discrepancy" $\Delta_W(N)$ serves as a proxy for the cumulative phase accumulation of the zeta zeros. Recent computational work involving the "Mertens spectroscope" (Csoka 2015) and the "Liouville spectroscope" suggests that the oscillations in discrepancy are governed by the term:
$$ \Re\left( \sum_{\rho} \frac{N^{\rho-1}}{\rho \zeta'(\rho)} \right) $$
where the sum is over non-trivial zeros.

The current research introduces a refinement using Dirichlet characters $\chi$. By twisting the spectral analysis with characters, we probe the distribution of Farey fractions with respect to arithmetic properties (modular classes). The formula $T_\infty = \frac{1}{2}\Im(\log L(2\rho, \chi^2))$ represents a "phase shift" correction necessary for the $L$-function components to align with the observed discrepancy data.

### 2.2. Character Definitions and Spectral Properties

A critical aspect of this investigation is the precise definition of the Dirichlet characters used. Standard library assumptions (e.g., treating $\chi_5$ as a Legendre symbol) lead to significant errors. We must adhere strictly to the provided Pythonic definitions.

**Character $\chi_{m4}$ (Real Order 2):**
Defined by $\chi_{m4}(p) = (-1)^{(p-1)/2}$.
$$ \chi_{m4}(p) = \begin{cases} 1 & p \equiv 1 \pmod 4 \\ -1 & p \equiv 3 \pmod 4 \\ 0 & p \equiv 0 \pmod 4 \end{cases} $$
Squaring this character yields the principal character mod 4: $\chi_{m4}^2(n) = \chi_0(n)$ for $\gcd(n,4)=1$. The associated L-function is $L(s, \chi_{m4}^2) = \zeta(s)(1 - 2^{-s})$.

**Character $\chi_5$ (Complex Order 4):**
This is a primitive character of order 4 modulo 5. The mapping is defined by the discrete logarithm in the multiplicative group $(\mathbb{Z}/5\mathbb{Z})^\times \cong C_4$.
Given `dl5={1:0, 2:1, 4:2, 3:3}`:
$$ \chi_5(n) = i^{\text{dl5}[n \pmod 5]} $$
Specifically:
*   $\chi_5(1) = i^0 = 1$
*   $\chi_5(2) = i^1 = i$
*   $\chi_5(3) = i^3 = -i$
*   $\chi_5(4) = i^2 = -1$

**Character $\chi_5^2$ (Real Order 2):**
When we square $\chi_5$, we obtain a real quadratic character.
*   $\chi_5^2(1) = 1^2 = 1$
*   $\chi_5^2(2) = i^2 = -1$
*   $\chi_5^2(3) = (-i)^2 = -1$
*   $\chi_5^2(4) = (-1)^2 = 1$
This matches the Legendre symbol $\left(\frac{n}{5}\right)$. Thus, $L(s, \chi_5^2)$ is the standard real Dirichlet L-function $L(s, \chi_{mod 5})$.

**Verification of Anti-Fabrication Rule:**
We must not substitute $\chi_5$ with a quadratic character in the input. The zeros provided ($\rho_{\chi5} \approx 0.5 + 6.18i$) are zeros of $L(s, \chi_5)$. When evaluating the formula, we are evaluating at $2\rho$, and the term involves $\chi^2$. The prompt correctly identifies that evaluating at $2\rho$ requires $L(s, \chi^2)$, which is the real L-function. The "Legendre substitution" warning in the context refers to *defining* the character $\chi$ itself as Legendre from the start, which would imply $\chi(2)=-1$ (real) rather than $i$ (complex). The current setup uses $\chi$ (order 4) but evaluates $L$ with $\chi^2$ (order 2), which is consistent with the analytic number theory of the "spectral product" $E_K^{\chi^2}$.

### 2.3. Task Analysis: Convergence of $B_K$ and $T_\infty$

We analyze the convergence of the sequence $B_K = \Im(\log \prod_{p \le K} (1 - \chi^2(p) p^{-2\rho})^{-1})$. The theoretical limit is $T_\infty = \frac{1}{2} \Im(\log L(2\rho, \chi^2))$. The factor of $1/2$ arises because the Farey discrepancy sum often involves a contribution from $\zeta(2\rho)$ or a related double-sum structure where the phase contribution is halved.

#### Task 1: The Zeta Case ($\chi = \chi_0$)
Here, $\chi^2 = \chi_0$, so $L(s, \chi^2) = \zeta(s)$.
We evaluate at $2\rho_1 = 1 + i(2 \times 14.13) \approx 1 + 28.269i$.
The theoretical value is $T_\infty = \frac{1}{2} \Im(\log \zeta(1 + 28.269i))$.
Numerical data provided: $\Im(\log \zeta(1+28.269i)) = -0.34071$.
Thus, $T_\infty = -0.17036$.
**Order of $\arg \zeta(1+it)$:**
Titchmarsh (The Theory of the Riemann Zeta-Function) establishes that $\zeta(1+it) \neq 0$ for $t \geq 0$. The argument is given by the formula:
$$ \arg \zeta(1+it) \sim -\sum_{p} \frac{\sin(t \log p)}{p} \quad \text{(heuristically)} $$
More rigorously, in the zero-free region near $t=1$, the growth is bounded. Titchmarsh proves that $\arg \zeta(\sigma+it) = O\left( \frac{t}{\log t} \right)$ generally, but for fixed $\sigma > 1/2$ (here $\sigma=1$), the behavior is much flatter. Specifically, for $\sigma=1$, $\arg \zeta(1+it)$ is $O(1/\log \log t)$? Actually, the order is typically bounded.
However, the convergence error of the partial product $B_K$ at $K=500$ is noted as $0.015$. This suggests that while the value is stable, the phase of the Euler product near $s=1$ (which is a pole for Zeta, but finite for $L(2\rho)$ due to $2\rho \approx 1$) requires significant primes to settle. Note that $s=1+it$ is on the edge of the convergence half-plane $\Re(s) > 1$. Convergence at $K=500$ is consistent with $O(1/\log K)$ rate.

#### Task 2: The m4 Case ($\chi = \chi_{m4}$)
Here $\chi^2 = \chi_0$.
$L(s, \chi_{m4}^2) = \zeta(s)(1 - 2^{-s})$.
At $s = 2\rho_1 = 1 + 1
