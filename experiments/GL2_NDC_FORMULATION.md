# Research Report: GL(2) NDC Formulation and Farey Discrepancy Spectroscopy

**Date:** October 26, 2023
**To:** Research Team, Farey Sequence & Spectroscopy Group
**From:** Mathematical Research Assistant
**Subject:** Analysis of GL(2) NDC (Normalized Discrepancy Conjecture) for Elliptic Curves (37a1)

---

## 1. Summary

This report provides a comprehensive analysis of the transition from the established GL(1) (Riemann Zeta) framework to the GL(2) (Elliptic Curve L-function) framework within the context of Farey sequence discrepancy spectroscopy. The primary objective is to resolve the numerical divergence observed in the naive calculation of the coefficient sum $c_K^E$ for the elliptic curve $E = 37a1$ ($y^2+y=x^3-x$).

Our analysis confirms that the "Mertens spectroscope" mechanism, previously validated via the `csoka 2015` framework and `Lean 4` (422 results), relies heavily on the smoothness of the partial sums near the critical line. While the GL(1) canonical pairs ($\chi_{m4}, \chi_5, \chi_{11}$) exhibit stable convergence of $D_K * \zeta(2) \to 1$, the GL(2) analog fails pointwise for small $K$ due to the oscillatory nature of the inverse L-function coefficients at the first zero $\rho_E$.

We identify that the Approximate Functional Equation (AFE) approach (Task 1) and Cesaro smoothing (Task 3) are necessary to stabilize the detection of $\rho_E$. The root number $W=-1$ (Task 2) dictates a sign-flip symmetry in the functional equation which directly influences the spectral gap. We conclude that while pointwise convergence is theoretically ideal, Cesaro convergence is sufficient for the spectroscope's detection threshold, provided the smooth cutoff $V(t)$ satisfies the decay conditions derived from the incomplete Gamma function.

The precise formulation for the GL(2) NDC conjecture is provided in Section 7 and is intended for storage at the specified path.

---

## 2. Detailed Analysis

### 2.1 GL(1) Context and Verification
Before addressing the GL(2) divergence, we must establish the baseline validity of the GL(1) model upon which the spectroscope is built. The prompt provides strict "NDC CANONICAL" definitions for character pairs. To maintain the integrity of the analysis and adhere to the **ANTI-FABRICATION RULE**, we reiterate the exact mappings used for the Riemann Zeta function case.

The character $\chi_{m4}$ is defined over $\mathbb{Z}/4\mathbb{Z}$:
$$
\chi_{m4}(p) = \begin{cases} 
1 & \text{if } p \equiv 1 \pmod 4 \\
-1 & \text{if } p \equiv 3 \pmod 4 \\
0 & \text{if } p = 2
\end{cases}
$$
This is a real, order-2 Dirichlet character. The associated zeros used for testing, $\rho_{m4\_z1} = 0.5 + 6.020948904697597i$, have been verified against the $D_K * \zeta(2)$ computation yielding $0.976 \pm 0.011$.

Similarly, the complex characters are defined via discrete logarithms (`dl`):
$$
\chi_5(p) = i^{\text{dl5}[p \pmod 5]}, \quad \text{where } \text{dl5} = \{1:0, 2:1, 4:2, 3:3\}
$$
This complex character has order 4. Crucially, $\chi_5(2) = i$. The zero $\rho_{\chi5} = 0.5 + 6.183578195450854i$ corresponds to the L-function $L(s, \chi_5)$. The GL(1) verification shows that $D_K * \zeta(2)$ (Grand Mean $0.992 \pm 0.018$) converges to 1. This validates the "Mertens spectroscope" hypothesis: the discrete Fourier transform of the discrepancy $\Delta W(N)$ acts as a filter that isolates zeros of $L(s)$ or $\zeta(s)$ at height $\gamma$.

The phase $\phi = -\arg(\rho_1 \zeta'(\rho_1))$ is calculated to be "SOLVED" within the GL(1) context. This phase is critical for the "pre-whitening" step in the spectroscope, ensuring that the oscillatory terms align constructively at the zero.

Furthermore, the "3-body" context ($S=\text{arccosh}(\text{tr}(M)/2)$ with 695 orbits) likely refers to the spectral geometry of the moduli space of the relevant L-functions or a toy model of the trace formula. The RMSE for GUE statistics ($0.066$) is consistent with Random Matrix Theory predictions for the pair correlation of zeros, further grounding our confidence in the statistical model used for $D_K$.

### 2.2 GL(2) Transition and 37a1 Analysis
We now transition to the Elliptic Curve $E = 37a1$, defined by $y^2 + y = x^3 - x$. The conductor is $N=37$ (prime), and the rank is $r=1$. The first non-trivial zero is $\rho_E = 0.5 + 5.003839i$.

The coefficients $a_p$ for this curve are determined by the number of points $\#E(\mathbb{F}_p)$ via $a_p = p + 1 - \#E(\mathbb{F}_p)$. The prompt provides the verified correct coefficients:
$$
a_2=-2, a_3=-3, a_5=-2, a_7=-1, a_{11}=-5, a_{13}=-2, a_{17}=0, a_{19}=0, a_{23}=2, a_{29}=6, a_{31}=-4, a_{37}=0
$$
We define the partial sum $c_K^E$ as:
$$
c_K^E(\rho_E) = \sum_{k \le K} \mu(k) a_k k^{-\rho_E}
$$
**The Divergence Problem:**
Numerical experiments for $K \le 2000$ show $\text{Re}(c_K^E) < 0$. This contradicts the GL(1) intuition where $D_K * \zeta(2)$ trends positively toward 1.
The diagnosis provided in the context is the "asymptotic onset" condition: $K \sim \exp(\pi \Im(\rho_E))$.
Calculating this onset:
$$
K_{onset} \approx \exp(\pi \cdot 5.0038) \approx \exp(15.72) \approx 6.8 \times 10^6
$$
This exponential dependence on the imaginary part of the zero is a hallmark of the inverse Mellin transform behavior. The function $k^{-s}$ oscillates rapidly with frequency proportional to $\Im(s)$. At $\Im(s) \approx 5$, the oscillations require a very large window $K$ to average out the "Gibbs phenomenon" inherent in the hard cutoff $\mathbf{1}_{k \le K}$.

**Cesaro Smoothing:**
The prompt notes that a Cesaro mean of $|D_K^E \zeta(2)|$ at $K=500$ is $1.017$. This suggests that while the raw sum $c_K^E$ is oscillating wildly (hence the negative real part at finite $K$), the average value is correct. This is a classic signal processing issue: the raw sum has a high-frequency noise component (oscillations) superimposed on the DC bias (the theoretical value).

### 2.3 Task 1: The Approximate Functional Equation (AFE)
The fundamental issue with the naive sum is that it approximates the inverse L-function $L(s, E)^{-1}$ via a truncated Dirichlet series. However, $L(s, E)$ is defined on the critical line $\text{Re}(s)=1/2$. To evaluate it numerically with high precision, we utilize the **Approximate Functional Equation**.

For a general L-function $L(s)$, the AFE states:
$$
L(s) = \sum_{n=1}^\infty \frac{a_n}{n^s} V\left(\frac{n}{\sqrt{N} y}\right) + \epsilon(s) \sum_{n=1}^\infty \frac{\bar{a}_n}{n^{1-s}} V\left(\frac{n y}{\sqrt{N}}\right)
$$
where $y = \sqrt{\text{Im}(s)}$. $V(z)$ is a smooth weight function derived from the Gamma factors of the functional equation (specifically, related to the incomplete Gamma function $\Gamma(s/2)$).

**Modification of $c_K^E$:**
To fix the convergence of $c_K^E$, we must replace the hard step function $\mathbf{1}_{k \le K}$ with a smooth cutoff $V$ that mimics the AFE weight.
Let us define a smoothed coefficient sum $c_K^E(V)$:
$$
c_K^E(V) = \sum_{k=1}^\infty \mu(k) a_k k^{-\rho_E} V\left(\frac{k}{K}\right)
$$
Alternatively, to align with the inverse L-function structure more closely, we use the dual sum structure provided by the functional equation:
$$
\frac{1}{L(s, E)} \approx \sum_{k=1}^\infty \mu_E(k) k^{-s} V\left(\frac{k}{\sqrt{N}}\right) + W \sqrt{N} \dots
$$
In the context of the spectroscope, the modification to $c_K^E$ involves applying the weight $V(k/K)$ to the coefficients $\mu(k)a_k$.
The function $V(t)$ decays rapidly for $
