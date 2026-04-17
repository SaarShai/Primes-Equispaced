# Report: Skeptical Review of the Spectroscope Section
**To:** Farey Sequence Research Collaborative
**From:** Mathematical Research Assistant
**Date:** October 26, 2023
**Subject:** Critical Analysis of Spectroscope Section Claims (M1_PA_SPECTROSCOPE)
**File Output:** /Users/saar/Desktop/Farey-Local/experiments/M1_PA_SPECTROSCOPE.md

---

## 1. Summary

This document provides a comprehensive and skeptical review of the "Spectroscope Section" within the draft manuscript under consideration. The section asserts that a specific spectral function, constructed from Farey discrepancy data via the Mertens function, successfully detects the first three non-trivial zeros of the Riemann zeta function. The spectral function is defined as $F(\gamma) = \gamma^2 \left| \sum_{p \le P} \frac{M(p)}{p} e^{-i\gamma \log p} \right|^2$, where $M(p)$ is the Mertens function and $\gamma$ corresponds to the imaginary part of a Riemann zero. The paper claims this method is novel, operating from "Farey discrepancy data alone," and that the $\gamma^2$ factor is theoretically justified to correct for signal decay.

This review argues that while the computational implementation is valuable, the core theoretical claims lack novelty and rely on well-established explicit formulas that connect the Mertens function to the Riemann zeta function's zeros. The analysis highlights significant ambiguities regarding the "Farey discrepancy data alone" claim, as this is fundamentally data about the distribution of primes and Möbius values, mediated by the Mertens function. Furthermore, the spectral weighting factor $\gamma^2$ is a standard feature of such spectral estimators in analytic number theory, not a new derivation. The review concludes that the section presents known facts through a new computational lens, requiring significant caveats and theoretical justification to avoid overstating its contribution to the field. It suggests the work is best positioned as a computational verification rather than a theoretical breakthrough.

---

## 2. Detailed Analysis

### 2.1 Novelty and Historical Context (Question 1)

The primary claim of novelty rests on the assertion that a "spectral function built from per-step data detects the first three nontrivial zeta zeros." This assertion must be evaluated against the history of explicit formulas in analytic number theory. The connection between the distribution of primes (encoded in the Möbius function $\mu(n)$ and its partial sums $M(x)$) and the zeros of the Riemann zeta function $\zeta(s)$ is a classical result, dating back to Riemann himself (1859). The explicit formula for the Chebyshev function $\psi(x)$ and, by extension, the Mertens function $M(x)$, expresses them as oscillatory sums over the non-trivial zeros $\rho = \frac{1}{2} + i\gamma$.

Specifically, the classical explicit formula suggests that $M(x)$ oscillates with frequencies determined by $\gamma$. The function proposed in the spectroscope, $F(\gamma)$, is effectively a finite Fourier transform (or periodogram) of the sequence $\frac{M(p)}{p}$ over the logarithmic scale $\log p$. This is not a new construction. It is a direct application of the Wiener-Khinchin theorem applied to the arithmetic functions underlying the Prime Number Theorem. Csoka (2015), as cited in the context, and Van der Pol (1947), demonstrated Fourier analysis of primes detects zeros. Van der Pol's method essentially utilized the same principle: constructing a spectral density that peaks at the zeros.

Therefore, the specific form $F(\gamma) = \gamma^2 | \dots |^2$ is a rephrasing of classical spectral analysis of arithmetic functions. The novelty claim is weak because the functional form is the standard "spectral estimator" for detecting frequencies in arithmetic noise. To claim it as a "new detection method" is to ignore the extensive literature on spectral methods in number theory. The innovation likely lies in the computational optimization or the specific application to Farey sequence discrepancy data, but this must be distinguished from the theoretical novelty of the method itself.

### 2.2 Data Justification: Farey Discrepancy vs. Mertens Data (Question 2)

The paper claims the detection is achieved from "Farey discrepancy data alone." This is a potentially misleading statement of fact. The Farey discrepancy $\Delta W(N)$ is indeed related to the Mertens function $M(x)$ through a "Bridge Identity." However, the identity $\Delta W(p) \sim M(p)$ implies that the Farey discrepancy is a proxy for the Mertens function. If one calculates the spectrum of $\Delta W(p)$, one is calculating the spectrum of $M(p)$.

The distinction is semantic but crucial for scientific rigor. "Farey discrepancy data alone" suggests the source is the geometry of Farey sequences (fractions $a/b$). "Mertens function data in disguise" suggests the source is the number-theoretic properties of the Möbius function. Since the mathematical properties of $\Delta W(p)$ are inextricably linked to $\mu(n)$, the spectroscope is not analyzing pure Farey geometry independent of number theory; it is analyzing number-theoretic oscillations revealed through Farey counting.

To claim "Farey discrepancy data alone" implies that one could detect these zeros using Farey sequences without reference to the Möbius inversion that underpins the connection. This is not possible. The zeros of $\zeta(s)$ are not inherent in the Farey fractions themselves but are encoded in the error term of the Farey sequence counting function, which is explicitly derived via the Möbius function. Thus, the claim should be revised to "detection from Farey discrepancy data, via the Mertens function." This caveat is essential for transparency.

### 2.3 Theoretical Justification of the $\gamma^2$ Factor (Question 3)

The paper claims the $\gamma^2$ factor "corrects for the $1/\gamma$ decay" in the spectroscope signal. The theoretical justification for this factor is grounded in the density of the zeros and the variance of the spectral estimator. The Riemann-von Mangoldt formula gives the density of zeros as roughly $N(T) \approx \frac{T}{2\pi} \log \frac{T}{2\pi}$. However, in the context of spectral analysis of sums like $\sum M(n) n^{-s}$, the signal-to-noise ratio often scales with the frequency $\gamma$.

In the explicit formula for $M(x)$, the contribution of a zero $\rho$ to $M(x)$ is roughly $x^\rho / (\rho \zeta'(\rho))$. When taking the Fourier transform with respect to $\log x$ (which corresponds to the Mellin transform at $s=1/2+i\gamma$), the factor $\rho \approx 1/2 + i\gamma$ appears in the denominator. Thus, the amplitude of the signal decays like $1/|\rho| \approx 1/\gamma$ as $\gamma$ increases. To detect higher frequency zeros ($\gamma_3 = 25.01$ etc.), the signal strength naturally diminishes.

The proposed $\gamma^2$ factor is a standard pre-whitening technique in spectral analysis (similar to methods used in Csoka 2015). It normalizes the variance of the estimator. Without it, the lower zeros dominate the spectral plot, obscuring higher zeros. The theoretical justification holds: if $S(\gamma) \sim \sum x^\rho/(\rho \zeta'(\rho))$, then $|S(\gamma)|^2$ is roughly proportional to $1/\gamma^2$. Multiplying by $\gamma^2$ flattens the background noise level, allowing peaks at different $\gamma$ to be comparable. Therefore, the factor is theoretically sound and standard in the field, but the paper's implication that it is a specific *new* discovery of the authors is an overstatement. It should be referenced as a standard spectral correction.

### 2.4 Computational Parameters and Resolution (Question 4)

A critical component of any spectral detection claim is the resolution of the data. The paper claims detection of three zeros ($\gamma_1=14.13, \gamma_2=21.02, \gamma_3=25.01$). For a Fourier transform to resolve these distinct peaks, the data must be sampled with sufficient density and length.
The sum runs over $p \le P$. The resolution of the frequency domain is inversely proportional to the range of the transform. Here, the transform is over $\log p$. If $P$ is the upper limit of the summation, the frequency resolution $\Delta \gamma$ is approximately $1 / \log P$.
If $P$ is small, say $10^4$, $\log P \approx 9.2$. The resolution $\Delta \gamma \approx 0.1$. This is sufficient to resolve $\gamma_1$ from $\gamma_2$. However, if $P$ is too small, the windowing effects (spectral leakage) will smear the peaks, making $\gamma^2$ scaling necessary to see them.

The question asks "how large is P?". If $P \approx 10^5$, $\log P \approx 11.5$. If $P \approx 10^6$, $\log P \approx 13.8$. The paper must report $P$. Furthermore, we must consider the number of primes. The prompt context mentions "422 Lean 4 results," which might imply formal verification of these computations. However, without a specific $P$ value in the provided excerpt, the claim remains vulnerable. If $P$ is around $10^4$, detecting $\gamma_3=25.01$ is at the limit of resolution for a simple periodogram. The peaks are narrow (width $\sim 1/\log P$). A "skeptical" view demands a sensitivity analysis: What is the effect of truncation? Does the $\gamma^2$ factor artificially inflate the visibility of $\gamma_3$ due to noise amplification at higher frequencies?

### 2.5 Statistical Validity: Z-Scores and Null Hypothesis (Question 5)

The paper uses a "local z-score" to quantify detection. In spectral analysis of prime data, the null hypothesis is crucial. Typically, one assumes a "random noise" model where the phases of $M(p)$ are uncorrelated (related to the Chowla conjecture or GUE statistics).
If the phases are random, the spectral density follows a $\chi^2_2$ distribution (Rayleigh distribution for magnitude) under the null hypothesis of no signal. The z-score likely measures the significance of a peak height above the local mean of the background noise.
However, the "background noise" in prime spectra is not white noise. It has structure due to correlations between primes (Hardy-Littlewood conjectures). The standard z-score assumes Gaussian noise, which might not hold for $M(p)$.
More critically, the "z-score" claim implies a statistical significance test was performed. Is the significance $5\sigma$? Or just a "peak"? The prompt mentions "GUE RMSE=0.066", suggesting the background might be modeled via Gaussian Unitary Ensemble statistics.
If the z-score does not account for the "peak picking" bias (scanning over many $\gamma$ values increases the chance of a random fluctuation appearing significant), the claim is statistically weak. The paper must correct for multiple testing (Bonferroni or False Discovery Rate). If they tested 1000 frequencies to find 3 peaks, the p-value changes drastically. The skepticism here is that "local z-score" might not be robust against the non-Gaussian nature of the Farey/Mertens background.

### 2.6 Honest Assessment: New or Wrapper? (Question 6)

An honest assessment of the "Spectroscope Section" reveals that it is primarily a presentation of known facts (Mertens explicit formula) with a new visual/computational wrapper. The mathematics relies on the explicit formula:
$$ M(x) \approx \sum_{|\gamma| \le T} \frac{x^{\rho}}{\rho \zeta'(\rho)} + \text{error} $$
Taking the Mellin transform of this expression leads directly to the poles of the zeta function. The spectroscope is simply visualizing this transform. The "novelty" is in the application to *Farey discrepancy* specifically, and the use of the "pre-whitening" factor.
However, the paper frames it as "detecting zeros from Farey data alone," which implies the Farey data *itself* (geometric arrangement) reveals them independently of the arithmetic
