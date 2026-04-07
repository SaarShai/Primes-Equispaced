# 2. Mathematical Construction

In this section, we establish the formal framework for the spectral analysis of the Mertens function restricted to prime inputs. We define the Mertens spectroscope, elucidate the mechanism generating spectral peaks, derive the necessary frequency-dependent compensation to handle the power-law decay of the signal, and define the local significance metric.

## 2.1 The Mertens Spectroscope

We begin by defining the spectral intensity function, referred to as the Mertens spectroscope, denoted by $F(\gamma)$. Let $\gamma \in \mathbb{R}$ represent the frequency parameter. The spectroscope is constructed from the Möbius function evaluated at primes, $\mu(p)$, which we denote here as $M(p)$. The definition is given by the squared modulus of the weighted Dirichlet series evaluated on the critical line:

$$
F(\gamma) = \left| \sum_{p \leq X} \frac{M(p)}{p} \exp\left(-i \gamma \log p\right) \right|^2,
$$

where the sum runs over primes $p$ up to a cutoff $X$. This function measures the power spectrum of the oscillatory components inherent in the Mertens distribution.

To understand the origin of the peaks in $F(\gamma)$, we invoke the Explicit Formula for the Mertens function $M(x) = \sum_{n \leq x} \mu(n)$. This formula expresses the summatory function as a sum over the non-trivial zeros $\rho$ of the Riemann zeta function:

$$
M(x) = \sum_{\rho} \frac{x^\rho}{\rho \zeta'(\rho)}.
$$

Substituting $\rho = \sigma + i\gamma_k$ and assuming the Riemann Hypothesis (such that $\sigma = 1/2$), the term $x^\rho$ becomes $x^{1/2} e^{i \gamma_k \log x}$. Consequently, the oscillatory frequency of the $k$-th zero, $\gamma_k = \text{Im}(\rho_k)$, dictates the dominant frequency in the time-domain signal $M(x)$. When restricted to prime arguments and weighted by $1/p$, the spectral transform captures these same oscillations. Therefore, local maxima in $F(\gamma)$ manifest at $\gamma = \gamma_k$ corresponding to the imaginary parts of the zeta zeros.

## 2.2 Compensation and Spectral Flattening

While the explicit formula explains the *location* of the peaks, it also characterizes their *amplitude*. From the explicit formula, the contribution of the $k$-th zero to the signal amplitude is proportional to the coefficient $c_k$:

$$
c_k \approx \frac{1}{\rho_k \zeta'(\rho_k)}.
$$

For zeros on the critical line, $\rho_k = 1/2 + i\gamma_k$. The magnitude of the denominator is dominated by the imaginary part for large $\gamma_k$, yielding the scaling approximation $|c_k| \sim 1/\gamma_k$. Since the spectroscope $F(\gamma)$ measures the squared amplitude, the background level of the spectrum exhibits a power-law decay:

$$
F(\gamma) \sim |c_k|^2 \sim \frac{1}{\gamma_k^2}.
$$

This decay obscures significant peaks at high frequencies. To address this, we introduce a compensating factor $\gamma^\alpha$. We seek an exponent $\alpha$ that normalizes the spectrum such that the signal-to-noise ratio is uniform across frequencies. Based on the derivation above ($|c_k|^2 \sim \gamma_k^{-2}$), setting $\alpha = 2$ cancels the decay. Thus, we define the compensated spectroscope:

$$
F_{\text{comp}}(\gamma) = \gamma^\alpha F(\gamma),
$$

where we adopt $\alpha=2$ as the canonical choice to flatten the expected background distribution of the Mertens data.

## 2.3 Local Z-Score and Pre-whitening

To statistically evaluate the significance of a detected peak, we compute the local z-score. Let $\mu_{\text{local}}(\gamma)$ and $\sigma_{\text{local}}(\gamma)$ denote the running mean and standard deviation of the compensated spectrum within a frequency window surrounding $\gamma$. The local z-score, $z_{\text{local}}$, is defined as:

$$
z_{\text{local}}(\gamma) = \frac{F_{\text{comp}}(\gamma) - \mu_{\text{local}}(\gamma)}{\sigma_{\text{local}}(\gamma)}.
$$

This standardization transforms the flattened signal into a distribution where a value of $|z_{\text{local}}| > 3$ typically indicates a statistically significant resonance above the expected noise floor.

**Note on Pre-whitening:** The operation of multiplying by $\gamma^2$ in the definition of $F_{\text{comp}}$ constitutes a form of pre-whitening. Standard spectral estimation assumes "white noise" with a flat variance spectrum. However, the Mertens data exhibits "colored noise" with a $1/\gamma^2$ power law structure inherent to the arithmetic properties of $\zeta'(s)$ and the distribution of primes. The compensation explicitly removes this structural bias, allowing the z-score metric to treat deviations across the spectrum with equal statistical weight.
