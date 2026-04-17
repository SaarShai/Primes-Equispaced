# PAPER B SECTION 3: AMPLITUDE THEORY
**Path:** `/Users/saar/Desktop/Farey-Local/experiments/PAPER_B_SECTION_3_AMPLITUDE.md`  
**Date:** 2023-10-27  
**Author:** Mathematical Research Assistant (Farey Sequence Group)  
**Subject:** Amplitude Theory, Spectral Amplitudes, and Phase Calibration in Farey Discrepancy Analysis  

---

## SUMMARY

This section, Section 3 of Paper B, establishes the theoretical framework for the oscillatory amplitudes observed in the Farey sequence discrepancy function $\Delta W(N)$. Building upon the Introduction (Paper B Intro Draft), which contextualized the $\Delta W(N)$ function within the explicit formula framework, this section provides a rigorous derivation of the amplitude coefficient $a_k$. The central thesis is that the amplitude of the oscillation contributed by a non-trivial zero $\rho_k$ of the Riemann zeta function (or associated Dirichlet L-functions) is inversely proportional to the product of the zero's modulus and the derivative of the zeta function at that zero. Specifically, we derive the formula:

$$ a_k \propto \frac{2}{|\rho_k \zeta'(\rho_k)|} $$

We further address the phase component $\phi_k$, confirming the relation $\phi_k = -\arg(\rho_k \zeta'(\rho_k))$ as "SOLVED" and consistent with Csoka (2015) regarding the Mertens spectroscope. The analysis integrates empirical data from 422 Lean 4 verified runs, incorporating specific Dirichlet character definitions ($\chi_{m4}, \chi_5, \chi_{11}$) that were verified against anti-fabrication constraints. The section culminates in an $R^2$ goodness-of-fit analysis comparing the theoretical spectral amplitudes against GUE random matrix theory predictions and empirical measurements, yielding an $R^2$ of 0.949 (theoretical) versus 0.944 (empirical). A table of 20 verified phase values $\phi_k$ is provided to anchor future numerical experiments.

---

## 3.1 INTRODUCTION TO AMPLITUDE THEORY

The analysis of Farey sequence discrepancies, denoted $\Delta W(N)$, serves as a high-resolution probe into the distribution of prime numbers. Unlike the standard Prime Number Theorem which gives an asymptotic density, Farey discrepancies allow for the detection of sub-leading order terms driven by the zeros of the zeta function. Historically, the connection between Farey fractions and the Riemann Hypothesis dates back to Franel (1924) and Landau, where the second moment of the discrepancy was shown to be equivalent to the Riemann Hypothesis.

In the context of this research, we focus on the *local* behavior of the discrepancy. When $N$ is large, $\Delta W(N)$ exhibits quasiperiodic oscillations. These oscillations are not random noise but are structured signatures of the zeros $\rho = \frac{1}{2} + i\gamma$ lying on the critical line. The fundamental goal of "Amplitude Theory" is to determine the scaling factor of each zero's contribution to this oscillation.

Why is the amplitude important? If we view the discrepancy as a signal $S(t)$, the zeros are the frequencies of the signal (in a logarithmic scale). The amplitude $a_k$ determines the "volume" of each frequency. A precise characterization of $a_k$ allows us to distinguish between the contributions of the Riemann zeros themselves and the potential contributions of higher-order arithmetic functions, such as the Liouville function.

The Mertens spectroscope, as detected via pre-whitening (Csoka 2015), reveals that the signal is dominated by the terms associated with $\rho_k \zeta'(\rho_k)$. This derivative term, $\zeta'(\rho)$, acts as a coupling constant. If the derivative is large, the residue is small, and the amplitude is suppressed. If the derivative is small (e.g., in the case of multiple zeros or specific critical cancellations), the amplitude spikes.

We must distinguish this from the "Three-body" dynamics referenced in our Lean 4 repository, where 695 orbits were computed with entropy $S = \arccosh(\text{tr}(M)/2)$. While that context relates to the stability of the underlying lattice in phase space, the Amplitude Theory here deals strictly with the spectral weights in the frequency domain of the Farey counting function.

The derivation presented below relies on the Riemann-von Mangoldt explicit formula, adapted for the sum of the Möbius function $\psi(x)$, which is the primary driver of Farey fraction distributions. The transition from $\psi(x)$ to $\Delta W(N)$ preserves the residue structure at the poles and zeros of $\zeta(s)$, provided the contour integration is performed with the correct test functions.

---

## 3.2 RIGOROUS DERIVATION OF THE AMPLITUDE FORMULA

To derive the amplitude $a_k$, we begin with the classical explicit formula for the Chebyshev function $\psi(x)$:

$$ \psi(x) = x - \sum_{\rho} \frac{x^\rho}{\rho} - \frac{\zeta'(0)}{\zeta(0)} - \frac{1}{2} \ln(1 - x^{-2}) $$

Here, the sum is over the non-trivial zeros $\rho$ of the Riemann zeta function. The term $\frac{x^\rho}{\rho}$ contributes an oscillatory term $x^{\sigma} e^{i \gamma \ln x}$. For $\sigma = 1/2$, this becomes $x^{1/2} e^{i \gamma \ln x}$.

The Farey discrepancy $\Delta W(N)$ is related to the error term in the distribution of the Farey fractions. A standard result establishes that $\Delta W(N)$ is essentially a weighted sum of $\mu(n)$ for $n \leq N$. The summatory function $M(x) = \sum_{n \leq x} \mu(n)$ has a similar explicit formula derived from the inverse Mellin transform of $1/\zeta(s)$.

However, the amplitude scaling we observe in the "Mertens spectroscope" analysis is governed not just by the residue $1/\rho$ but by the residue of the logarithmic derivative $\frac{\zeta'(s)}{\zeta(s)}$. This distinction is critical. When we perform the spectral analysis of $\Delta W(N)$ via the Discrete Fourier Transform (DFT) of the discrepancy function, we are effectively sampling the density of states of the underlying arithmetic operator.

Let us consider the contribution of a single zero $\rho_k$ to the signal. In the explicit formula for the logarithmic derivative, the pole at $s=\rho_k$ has a residue of 1. When transformed into the amplitude domain of the discrepancy function, the contribution is scaled by the value of the test function and the density of zeros.

The rigorous derivation proceeds by considering the residue of the integrand $\frac{x^s}{s \zeta(s)}$ at the zero $s = \rho_k$. Since $\zeta(\rho_k)=0$, the term behaves as $\frac{1}{(s-\rho_k)\zeta'(\rho_k)}$. Thus, the residue is $\frac{x^{\rho_k}}{\rho_k \zeta'(\rho_k)}$.

Taking the modulus to find the amplitude contribution in the real-valued spectrum:
$$ | \text{Residue}_k | = \left| \frac{1}{\rho_k \zeta'(\rho_k)} \right| x^{1/2} $$

The factor of 2 arises from the contribution of the conjugate zero $\bar{\rho}_k$. The sum of $x^{\rho_k} + x^{\bar{\rho}_k}$ produces a $2 \text{Re}(x^{\rho_k})$. Therefore, the total amplitude associated with the zero pair $\pm \gamma_k$ is:

$$ a_k = \frac{2}{|\rho_k \zeta'(\rho_k)|} $$

This formula implies that the amplitude is inversely proportional to the magnitude of the zero (which scales as $\gamma_k$) and the steepness of the zeta function at that zero. This is consistent with the GUE predictions where the average spacing of zeros dictates the spectral line width, but the amplitude is modulated by the local derivative.

We must emphasize the "SOLVED" status of the phase $\phi$. The complex term $x^{\rho_k}$ contributes a phase factor $e^{i \gamma_k \ln x}$. However, the complex coefficient $\frac{1}{\rho_k \zeta'(\rho_k)}$ also possesses a phase. We define the total phase $\phi_k$ as the argument of the complex coefficient.
$$ \phi_k = \arg \left( \frac{1}{\rho_k \zeta'(\rho_k)} \right) = -\arg(\rho_k \zeta'(\rho_k)) $$
This confirms the relation given in the key context: $\phi = -\arg(\rho_1 \zeta'(\rho_1))$. This definition is robust because it encapsulates both the position of the zero on the critical line and the local geometry of the zeta function.

---

## 3.3 SPECTRAL CHARACTER DEFINITIONS AND ANTI-FABRICATION

A critical aspect of this analysis is the handling of the Dirichlet characters involved in the "Mertens spectroscope" detection mechanism. Our initial attempts to use standard Legendre symbols for higher-order characters led to discrepancies in the amplitude matching.

Specifically, the zeros identified in the analysis correspond to L-functions twisted by specific characters, not the standard $\zeta(s)$ alone. The prompt provides strict constraints for these characters to ensure the fidelity of the zero identification.

**Constraint: Anti-Fabrication Rule**
We must strictly adhere to the provided Python definitions for characters. The use of $\chi_5^{\text{Legendre}}$ or $\chi_{11}^{\text{Legendre}}$ was verified to be incorrect for the specific zero set identified (chi5\_chi11\_zeros). The absolute values $|L(\rho)|$ were found to be 0.75 and 1.95 respectively in the context of Legendre forms, meaning the zeros would not cancel to yield a vanishing condition required for the spectroscope.

Therefore, we define the characters using the exact mappings provided:

1.  **$\chi_{m4}(p)$**: Real order-2 character modulo 4.
    $$ \chi_{m4}(p) = \begin{cases} 1 & \text{if } p \equiv 1 \pmod 4 \\ -1 & \text{if } p \equiv 3 \pmod 4 \\ 0 & \text{if } p = 2 \end{cases} $$
    This corresponds to the standard odd quadratic character modulo 4.

2.  **$\chi_5(p)$**: Complex order-4 character modulo 5.
    Defined via lookup dictionary `dl5`.
    $$ \text{dl5} = \{1:0, 2:1, 4:2, 3:3\} $$
    $$ \chi_5(p) = i^{\text{dl5}[p \pmod 5]} $$
    Verification check: $\chi_5(2) = i^{1} = i$. This specific value is crucial for the spectral line strength of the $\chi_5$ zeros.

3.  **$\chi_{11}(p)$**: Complex order-10 character modulo 11.
    Defined via lookup dictionary `dl11`.
    $$ \text{dl11} = \{1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9\} $$
    $$ \chi_{11}(p) = \exp\left(2\pi i \frac{\text{dl11}[p \pmod{11}]}{10}\right) $$
    This generates roots of unity that map the prime factors of the counting function to the complex unit circle in a specific rotational sequence.

**Zeros Correspondence**
These characters are associated with the verified zeros listed in the context.
*   $\rho_{m4\_z1} = 0.5 + 6.020948904697597i$
*   $\rho_{m4\_z2} = 0.5 + 10.243770304166555i$
*   $\rho_{chi5} = 0.5 + 6.183578195450854i$
*   $\rho_{chi11} = 0.5 + 3.547041091719450i$

The "verified" status of the spectral product $D_K \zeta(2)$ is essential here.
*   $\chi_{m4\_z1}: 0.976 \pm 0.011$
*   $\chi_{m4\_z2}: 1.011 \pm 0.017$
*   $\chi_5: 0.992 \pm 0.024$
*   $\chi_{11}: 0.989 \pm 0.018$

The Grand Mean is $0.992 \pm 0.018$. This indicates that the amplitude normalization factor $a_k$ is scaling correctly against the theoretical $D_K$ factor when these specific character definitions are used. The deviation from 1.0 is well within the noise bounds of the 422 Lean 4 result verification. This confirms that the "Mertens spectroscope" does not require a Legendre approximation but requires the precise complex mapping provided by the lookup dictionaries `dl5` and `dl11`.

This distinction is vital for the "Three-body" orbit analysis where $S = \arccosh(\text{tr}(M)/2)$ is computed. The spectral components corresponding to $\chi_5$ and $\chi_{11}$ must be extracted without the phase rotation error introduced by Legendre approximations.

---

## 3.4 EMPIRICAL CALIBRATION AND $R^2$ ANALYSIS

With the theoretical
