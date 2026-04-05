**Derivation of Periodogram Properties Under GRH:**

---

### **(1) Signal at Resonance ~ N²**

The periodogram is defined as:  
$$
F(\gamma) = \left| \sum_{p} w(p) p^{-i\gamma} \right|^2,
$$  
where the sum is over primes $ p $, and $ w(p) $ are weights. When $ \gamma $ coincides with an embedded frequency $ \gamma_k $, the sum $ \sum w(p) p^{-i\gamma_k} $ becomes large. Assuming constructive interference (e.g., $ w(p) $ aligns with the oscillatory terms $ p^{-i\gamma_k} $), the magnitude of the sum scales with the number of primes $ N $. Thus, the squared magnitude (signal) scales as:  
$$
\text{Signal} \sim N^2.
$$  
This follows because the sum over $ N $ terms with constructive alignment yields $ O(N) $, and squaring gives $ O(N^2) $.

---

### **(2) Cross-Term Noise ~ N by PNT**

Cross-term noise arises from random fluctuations in the sum when $ \gamma $ is not an embedded frequency. Assuming $ w(p) $ are uncorrelated with $ \gamma $, the variance of the sum $ \sum w(p) p^{-i\gamma} $ is proportional to the number of primes $ N $. By the Prime Number Theorem (PNT), the number of primes $ N $ up to a maximum prime $ X $ satisfies $ N \sim \frac{X}{\log X} $. However, the problem directly states that cross-term noise scales as $ N $, reflecting the contribution of $ N $ random terms. Thus:  
$$
\text{Cross-term noise} \sim N.
$$

---

### **(3) SNR ~ N**

Signal-to-noise ratio (SNR) is the ratio of signal to noise:  
$$
\text{SNR} = \frac{\text{Signal}}{\text{Noise}} \sim \frac{N^2}{N} = N.
$$  
This reflects the dominance of the signal over noise as the number of primes increases.

---

### **(4) Peak Width ~ $ \frac{2\pi}{\log X} $**

The peak width of the periodogram is inversely proportional to the spread of the signal in the logarithmic domain. Primes are distributed such that their logarithms are roughly uniformly spaced (by the Prime Number Theorem). The spread of primes in the logarithmic scale is $ \log X $, leading to:  
$$
\text{Peak width} \sim \frac
ive to one another.
*   The sum represents a random walk of $N$ vectors of unit length in the complex plane.
*   The magnitude of the sum of $N$ random unit vectors typically scales as $\sqrt{N}$.
*   Therefore, the background noise power is:
    $$ P_{\text{noise}} \approx (\sqrt{N})^2 = N $$

### 4. Signal-to-Noise Ratio (SNR)

The Signal-to-Noise Ratio is the ratio of the signal power to the noise power:
$$ \text{SNR} = \frac{P_{\text{signal}}}{P_{\text{noise}}} \approx \frac{N^2}{N} = N $$
Using the approximation $N \approx X / \log X$, the SNR is indeed proportional to $X / \log X$ (which is much larger than 0 for large $X$).

### 5. Detection Error and Resolution (The Peak Width)

The "detection error" in frequency estimation corresponds to the **frequency resolution** of the system. Just as in standard Fourier analysis, the uncertainty in determining the precise frequency $\gamma$ is inversely proportional to the total duration of the observation time window.

*   **Time Domain:** The effective "time" in this analysis is $\ln p$. The signal exists from $\ln 2$ to $\ln X$.
*   **Duration ($T$):** The effective duration is $T = \ln X$.
*   **Rayleigh Limit:** The width of the spectral peak $\Delta \gamma$ (which defines the precision of the frequency $\gamma_k$) is determined by the Fourier uncertainty principle:
    $$ \Delta \gamma \sim \frac{2\pi}{T} $$
*   **Scaling:** Substituting $T = \ln X$:
    $$ \text{Peak Width} \sim \frac{2\pi}{\ln X} $$

### 6. Synthesis

The prompt connects these two facts:
1.  **The Peak Width:** Due to the finite domain of primes up to $X$ (mapping to time $\ln X$), the spectral peaks have a finite width proportional to $1/\log X$.
2.  **Detection Error:** To "detect" or locate a zero, the precision is bounded by the width of the peak. You cannot resolve a frequency better than the width of your peak.

Therefore, the error in detecting the location of the zero (the frequency uncertainty) is proportional to the peak width:
$$ \text{Error} \sim \frac{1}{\log X} $$

**Conclusion on Lomb-Scargle:**
While the standard Fourier Transform assumes uniformly spaced samples, the Lomb-Scargle periodogram is a generalization designed specifically for irregularly sampled data (like the logarithms of primes). However, the **fundamental limit of resolution** for any frequency estimator (Lomb-Scargle, standard FFT, or Maximum Likelihood) is dictated by the total time span of the data. Since the data spans $\ln X$, the resolution (and thus the detection error) remains $O(1/\log X)$, regardless of the specific algorithm used.
ive" phases of the oscillation or simply by re-weighting terms, the SNR still scales linearly with the number of primes (or $N$) in the asymptotic limit. Therefore, the error rate decays exponentially with respect to $n$ (or $N$), maintaining the same scaling behavior.

**Detailed Steps:**
1.  **Identify Scaling:** The coherent sum signal power scales as $(N/\log N)^2$, which corresponds to the square of the number of primes $n^2$. The noise power scales as $N (\log N)^2 \approx n (\log n)^3$.
2.  **Calculate SNR:** The ratio SNR $\sim n / (\log n)^3$.
3.  **Filter Effect:** The filter $M(p) \le -3$ acts as a selection criterion. It effectively selects a subset of primes. Unless this subset has a drastically different density scaling (e.g., reducing to $O(1)$ terms), the scaling with $n$ remains linear.
4.  **Convergence:** Since SNR $\sim n$, the error rate converges exponentially ($e^{-n}$). The filter does not change the power-law exponent of the SNR, hence the convergence rate class remains exponential.

**Result:** The filter does not change the convergence rate (it remains exponential in $N$).
