# Pink Noise & Zeta-Zero Correlations in DeltaW Fluctuations

**Date:** 2026-03-24
**Data:** 9,588 primes from 11 to 99,991 (`wobble_primes_100000.csv`)
**Script:** `pink_noise_zeta.py`

---

## Investigation 1: Spectral Density of {DeltaW * p^2}

**Question:** Is the f^{-1.18} slope robust? How does it compare to GUE f^{-1}?

**Findings:**

| Method | Slope | R^2 |
|--------|-------|-----|
| Welch (512 segments) | -1.675 | 0.956 |
| Welch (1024 segments) | -1.668 | 0.923 |
| Welch (2048 segments) | -1.670 | 0.851 |
| Welch (4096 segments) | -1.674 | 0.688 |
| Binned periodogram (full) | -2.054 | 0.953 |
| Binned periodogram (mid-range) | -2.083 | 0.922 |

**Consensus Welch slope: f^{-1.67} (not f^{-1.18})**

The previous agent's measurement of -1.18 was on *|DeltaW|* magnitude directly. The scaled sequence DeltaW*p^2 has a steeper spectrum. This is actually **between pink noise (f^{-1}) and brown noise (f^{-2})**. The GUE prediction of f^{-1} does not match -- the spectrum is significantly steeper, suggesting stronger long-range correlations than random matrix theory predicts.

**Verdict:** The spectral slope is robust at approximately f^{-1.67}. This deviates from GUE (f^{-1}) but the deviation is interesting -- it is closer to a **fractional Brownian motion** with Hurst exponent H ~ 0.84 (since PSD slope = -(2H+1) for fBm, giving slope = -1.67 at H = 0.335... wait: for fBm, S(f) ~ f^{-(2H+1)}, so H = (1.67-1)/2 = 0.335). This corresponds to an *anti-persistent* process with mild long memory.

---

## Investigation 2: Full Autocorrelation Function

**Question:** Does the ACF match Montgomery's pair correlation?

**Findings:**

For |DeltaW| (raw magnitudes):
- Lag 1: r = 0.812 (agent reported 0.91 -- discrepancy likely due to different normalization or subset)
- Lag 5: r = 0.452
- Lag 10: r = 0.242

For DeltaW*p^2 (scaled):
- Lag 1: r = 0.997 (extremely high -- almost trivial due to p^2 scaling being smooth)

**ACF decay structure:**
- Exponential decay rate: lambda = 0.066, giving correlation length ~15 prime steps
- Power-law exponent: alpha = -1.058 (very close to -1)
- The R^2 values (0.95 exponential, 0.93 power-law) show both models fit reasonably well

**Montgomery comparison:** Montgomery's pair correlation predicts g(u) = 1 - (sin(pi*u)/(pi*u))^2 for zeta zero spacings. The ACF of |DeltaW| shows smooth exponential/power-law decay rather than the distinctive oscillatory "dip-then-recovery" shape of Montgomery. **The ACF does NOT match Montgomery's form** -- it is monotonically decreasing without the characteristic minimum near u=0.

This suggests the DeltaW autocorrelations arise from a different mechanism than zeta-zero spacing statistics. The long-range persistence is more consistent with the **smooth variation of p^2** modulating a locally correlated noise process.

---

## Investigation 3: Fourier Peaks at Zeta Zero Locations

**Question:** Does the Fourier transform of DeltaW*p^2 show peaks at zeta zero imaginary parts?

### Method A: FFT on uniform log-prime grid

15/15 zeros showed SNR > 2 sigma. However, the **null test also showed 100/100 random frequencies above 2 sigma**. This means the "peaks" are an artifact of the steep red spectrum -- at low frequencies, everything looks like a peak relative to nearby values.

**Verdict: FFT method is inconclusive (red noise artifact).**

### Method B: Direct Dirichlet-type sum F(t) = Sum DeltaW*p^2 * exp(i*t*log(p))

This is the correct test. Results:

| Zero | gamma_k | F at gamma | SNR |
|------|---------|-----------|-----|
| 1 | 14.135 | 0.453 | 3.11 |
| 2 | 21.022 | 0.083 | -0.30 |
| 3 | 25.011 | 0.190 | 1.73 |
| 4 | 30.425 | 0.129 | 1.20 |
| 5-15 | ... | declining | ~0-1 |

Only gamma_1 = 14.13 shows a clear peak (SNR 3.11). Mean SNR at zeta zeros: 0.91, vs. 1.20 for random frequencies.

**Verdict: No systematic Fourier peaks at zeta zeros.** The first zero gamma_1 is the only notable feature, and even it is not dramatically above the noise floor. The random null actually has higher mean SNR. The DeltaW spectrum does NOT have discrete peaks corresponding to individual zeta zeros.

### Method C: Least-squares oscillation fitting

Fitting cos(gamma*log(p)) + sin(gamma*log(p)) to DeltaW*p^2:

All 15 zeta zeros show highly significant oscillation amplitudes (t > 3 for all). **BUT** random frequencies also show significant amplitudes. The ratio of zeta-zero amplitudes to random amplitudes is 1.43x, indicating mild enrichment.

The first zero (gamma_1 = 14.13) has dramatically the largest amplitude (9.95), roughly 2x the next largest. This dominant low-frequency oscillation explains much of the "pink noise" character.

**Key insight:** The significance comes from the smooth, slowly-varying nature of DeltaW*p^2 rather than from discrete zeta-zero encoding. Any slowly-oscillating basis function will fit well because the signal itself has strong low-frequency power.

---

## Investigation 4: Mertens Function Connection

**Question:** Does DeltaW encode Mertens function oscillations carrying zeta-zero information?

### Cross-correlation: M(p)/sqrt(p) vs DeltaW*p^2

**r = 0.915** (after detrending both signals with cubic polynomials)

This is an extremely strong correlation. The Mertens function M(p)/sqrt(p) and the scaled wobble difference DeltaW*p^2 are almost perfectly linearly related. This is the most important finding of this analysis.

### Spectral coherence at zeta zeros

| Frequency band | Coherence |
|----------------|-----------|
| At zeta zeros (mean) | 0.780 |
| Overall mean | 0.681 |
| Enrichment | 1.15x |

The coherence is high everywhere (0.68 overall), with modest 15% enrichment at zeta-zero frequencies. This means M/sqrt(p) and DeltaW*p^2 move together at all frequencies, not just at zeta zeros.

---

## Synthesis

### What the data actually shows:

1. **DeltaW*p^2 is dominated by the Mertens function** (r = 0.915 correlation). This is the primary signal -- not noise, not random fluctuations, but a near-deterministic relationship.

2. **The spectral slope f^{-1.67} is NOT GUE-like.** It reflects the known spectral properties of M(x)/sqrt(x), which has a continuous spectrum with more power at low frequencies than GUE predicts. The Mertens function spectrum involves all zeta zeros simultaneously (via the explicit formula), creating a continuous red spectrum rather than discrete peaks.

3. **No discrete peaks at individual zeta zeros.** The explicit formula M(x) ~ Sum x^rho/rho involves ALL zeros with amplitudes 1/|rho| that decrease slowly. When sampled at primes, these interfere destructively, creating a smooth spectrum rather than isolated peaks. The direct sum test confirms this.

4. **The high autocorrelation (0.81 at lag 1) is explained by** the slow variation of M(p)/sqrt(p), not by GUE-type pair correlations. The decay is exponential/power-law, not Montgomery-shaped.

### Honest assessment:

The DeltaW fluctuations do contain zeta-zero information, but **only indirectly through the Mertens function**. The connection is:

```
DeltaW(p) * p^2  ~  M(p) / sqrt(p)  =  Sum_rho p^{rho - 1/2} / rho
```

This means zeta zeros collectively shape the "pink noise" envelope, but you cannot extract individual zeros from DeltaW. The signal is a **superposition of all zeros**, consistent with the known explicit formula, not a new or unexpected connection.

### What this means for the paper:

- The pink noise finding is **real and interesting** but it comes from the Mertens connection, which is already understood in analytic number theory.
- The f^{-1.67} slope may be worth reporting as an empirical characteristic of DeltaW*p^2, but it should not be claimed as evidence for a new zeta-zero connection.
- The 0.915 cross-correlation with M/sqrt(p) is the strongest result and provides a clean numerical bridge between Farey wobble differences and the Mertens function.
- Claims about GUE or Montgomery pair correlation are **not supported** by the data.
