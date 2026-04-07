This is a sophisticated observation that moves the problem from **resolution-limited spectroscopy** to **statistical moments analysis**. 

You have correctly identified the fundamental constraint: if the resolution $\Delta \approx 2\pi/\log X$ is much larger than the spacing $\delta$ of a Lehmer pair, the "spectroscope" cannot resolve two distinct Dirac-like peaks. Instead, the two peaks undergo a **coalescence event** in the Fourier domain.

Here is the mathematical breakdown of whether we can detect this via kurtosis and the challenges involved.

---

### 1. The Geometry of the Merging Peaks
Let us model the "spectroscope" output at a specific frequency (zero height $\gamma$) as a sum of peaks. If we assume the instrument's impulse response is Gaussian (a common assumption for windowed Fourier transforms), a single zero at $\gamma_0$ produces:
$$f_1(x) = A \exp\ness\left( -\frac{(x-\gamma_0)^2}{2\sigma^2} \right)$$
where $\sigma$ is the resolution limit ($\approx 1/\log X$).

A Lehmer pair consists of two zeros at $\gamma_0 - \epsilon/2$ and $\gamma_0 + \epsilon/2$. The observed signal is:
$$f_{pair}(x) = A \left[ \exp\left( -\frac{(x-(\gamma_0-\epsilon/2))^2}{2\sigma^2} \right) + \exp\left( -\frac{(x-(\gamma_0+\epsilon/2))^2}{2\sigma^2} \right) \right]$$

### 2. How Kurtosis Changes
Kurtosis ($\beta_2$) measures the "tailedness" or "peakedness" of a distribution. To detect the pair, we look at the **excess kurtosis** ($\gamma_2 = \beta_2 - 3$).

**The Transition:**
1.  **Case 1: $\epsilon \ll \sigma$ (The Single Peak Regime):** When the spacing is much smaller than the resolution, the two Gaussians overlap almost perfectly. The sum behaves like a single Gaussian. The excess kurtosis is $\approx 0$.
2.  **Case 2: $\epsilon \approx \sigma$ (The Merging Regime):** As the zeros move apart, the peak begins to flatten. The "top" of the peak becomes less "pointy" and more "plateau-like."
3.  **Case 3: $\epsilon > \sigma$ (The Resolved Regime):** The peaks are distinct.

**The Signature:**
The merging of two Gaussian peaks into one results in a **platykurtic** distribution. A platykurtic distribution has **negative excess kurtosis** ($\gamma_2 < 0$). 

Mathematically, as the spacing $\epsilon$ increases relative to $\sigma$, the distribution moves from a single peak (kurtosis $\approx 3$) to a "bimodal" distribution where the center is a dip (kurtosis $\to$ much lower). In the window where the peaks are unresolved, the "broadening" you mentioned is specifically a **flattening of the summit**. 

**Conclusion on Kurtosis:** You can detect the presence of the pair by looking for a statistically significant **drop in kurtosis** (an increase in "flatness") at a specific frequency, compared to the expected kurtosis of the background "forest" of zeros.

### 3. Can we actually detect this? (The "Noise" Problem)
While the theory holds, the "spectroscope" faces a massive Signal-to-Noise Ratio (SNR) problem.

**A. The "Forest" Interference:**
The zeros of the zeta function are not isolated. The "background" of the spectrum is not white noise; it is a dense "forest" of all other zeros $\gamma_n$. Each zero adds its own width $\sigma$ to the local density. The "signal" (the change in kurtosis from one Lehmer pair) is buried under the cumulative variance of thousands of other overlapping peaks.

**B. The Precision Requirement:**
To detect a drop in kurtosis, you need to accurately measure the 4th moment of the signal. The variance of the estimator for kurtosis is notoriously high. To distinguish a $\gamma_2 = -0.01$ (a slight flattening) from $\gamma_2 = 0$ (a single peak) in a crowded spectrum, you would need an extremely high number of "samples" (primes) to reduce the statistical uncertainty below the magnitude of the flattening.

**C. The Scaling Limit:**
As you increase $X$ to improve resolution, the number of peaks in your spectrum increases. While $\Delta$ shrinks, the "interference" from the sheer density of zeros grows. You are essentially trying to find a "flat" spot on the top of a mountain range that is itself composed of overlapping smaller mountains.

### Summary
*   **Can we detect broadening?** Yes, via the transition from a Gaussian peak to a platykurtic (flat-topped) peak.
*   **The Metric:** Look for **negative excess kurtosis** ($\gamma_2 < 0$) in the local power spectrum.
*   **The Difficulty:** Extremely high. The "signal" is a subtle change in the shape of a peak that is already obscured by the overlapping tails of the entire Riemann spectrum. 

**Verdict:** It is mathematically possible to detect the *signature* of a Lehmer pair without resolving it, but it requires a precision in the 4th moment calculation that likely exceeds the computational benefits of increasing $X$ in any practical "spectroscope."
