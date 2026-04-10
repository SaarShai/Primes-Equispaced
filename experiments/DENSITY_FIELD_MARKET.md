# Market Assessment: Farey Densification for 1D Density Fields

**Proven capability:** 5.5x fewer Gaussians than SOTA on synthetic 1D/3D density fields.
**Date:** 2026-03-29

---

## 1. Spectral Density Estimation (Signal Processing)

- **Bottleneck?** Moderate. Real-time density estimation is a known challenge (see TAKDE work on sliding-window KDE). Kernel bandwidth selection and component count are active research problems.
- **Market:** Signal processing software ~$2-3B. Embedded in larger DSP toolchains (MATLAB, SciPy ecosystem).
- **Customers:** Telecom companies, radar/sonar manufacturers, audio processing firms.
- **Does 5.5x matter?** Marginally. Most spectral estimation uses FFT-based methods, not Gaussian mixtures. Where KDE is used (real-time streaming), fewer components = faster updates. Niche win.
- **Verdict: LOW priority.** FFT dominates; KDE is secondary.

## 2. Probability Density Fitting / GMMs for ML

- **Bottleneck?** YES. GMM fitting via EM is slow, sensitive to initialization, and component count selection (BIC/AIC) is a known pain point. scikit-learn's GMM is widely used but struggles with high-component models.
- **Market:** ML infrastructure broadly ~$40-50B. GMM-specific tooling is a small slice but ubiquitous (clustering, anomaly detection, generative models, density estimation in every ML pipeline).
- **Customers:** Every ML team doing clustering, anomaly detection, or density estimation. Cloud ML platforms (AWS SageMaker, GCP Vertex AI).
- **Does 5.5x matter?** YES. Fewer components = faster inference, lower memory, better generalization. The GMM component reduction problem is actively researched (see GMMultiMixer 2025). Direct competition with existing compression methods.
- **Verdict: HIGH priority. Best product-market fit.** "Optimal GMM component selection via Farey densification" is a clear value proposition.

## 3. Particle/Beam/Plasma Physics

- **Bottleneck?** Moderate. PIC simulations use adaptive mesh refinement (AMR) for density profiles. AMR for PIC has shown 4x-1000x savings. Density profile representation matters for beam dumps, tokamak modeling.
- **Market:** HPC simulation software ~$5-8B. Plasma physics is a niche (~$500M) but growing with fusion energy investment.
- **Customers:** National labs (LLNL, SLAC, CERN), fusion startups (TAE, Commonwealth Fusion), defense contractors.
- **Does 5.5x matter?** Somewhat. These users already have sophisticated AMR. But initial density profile specification (beam profiles, plasma targets) could benefit. Entry barrier is high -- they write their own code.
- **Verdict: MEDIUM-LOW.** Hard to penetrate; users are code-native.

## 4. Financial Density Estimation (Option Pricing)

- **Bottleneck?** YES. Risk-neutral density estimation from option prices is a core quant finance problem. Current methods: kernel smoothing, Gauss-Hermite expansion, neural network approximation. Speed matters enormously (real-time pricing).
- **Market:** Quantitative finance software ~$15-20B. Derivatives pricing specifically ~$3-5B.
- **Customers:** Investment banks (Goldman, JPMorgan, Citadel), exchanges (CME, ICE), fintech (Bloomberg Terminal, Refinitiv).
- **Does 5.5x matter?** YES -- but differently. Quants care about tail accuracy more than component count. If Farey densification gives better tail representation with fewer basis functions, that is extremely valuable. Real-time recalibration with fewer components = direct latency win.
- **Verdict: HIGH priority if we can demonstrate tail accuracy.** Finance pays premium prices for marginal improvements.

## 5. Semiconductor Doping Profiles

- **Bottleneck?** Moderate. TCAD tools (Synopsys Sentaurus, Silvaco) model doping profiles as 1D density functions. Component count is not the primary bottleneck -- physics accuracy is.
- **Market:** Semiconductor modeling & simulation: $4.85B (2024) growing to $10.4B by 2032. TCAD is a subset (~$1-2B).
- **Customers:** TSMC, Samsung, Intel, GlobalFoundries, Synopsys, Cadence.
- **Does 5.5x matter?** Minimally for existing workflows. Doping profiles are typically represented analytically (Gaussian/complementary error functions), not as GMMs. The representation is not the bottleneck.
- **Verdict: LOW.** Wrong abstraction level for this domain.

## 6. Acoustic/Seismic Profiles

- **Bottleneck?** No. 1D velocity/density profiles are a starting point for seismic inversion, but the field has moved to 3D/4D full waveform inversion (FWI). 1D models are only used for initial guesses.
- **Market:** Seismic services ~$9.4B (2025). Processing software ~$2B.
- **Customers:** Schlumberger, Halliburton, CGG, TGS.
- **Does 5.5x matter?** No. The industry has moved past 1D. Even if we extended to 3D, FWI operates on grids, not Gaussian mixtures.
- **Verdict: VERY LOW.** Domain mismatch.

## 7. Network Traffic Density

- **Bottleneck?** No. Traffic monitoring uses time-series aggregation, histograms, and streaming statistics. Nobody represents bandwidth utilization as a Gaussian mixture.
- **Market:** Network traffic analysis ~$4.4B (2025), growing to ~$13B by 2037.
- **Customers:** Cisco, Splunk, Datadog, NETSCOUT, Gigamon.
- **Does 5.5x matter?** No. Wrong abstraction. Traffic is discrete events, not continuous density fields.
- **Verdict: VERY LOW.** Not a fit.

---

## Summary Ranking

| Application | Fit | Market Size | 5.5x Matters? | Priority |
|---|---|---|---|---|
| **GMM for ML** | HIGH | ~$40-50B (broad ML) | YES | **#1** |
| **Financial density** | HIGH | ~$3-5B (derivatives) | YES (tails) | **#2** |
| **Plasma/beam physics** | MED-LOW | ~$500M | Somewhat | #3 |
| **Spectral estimation** | LOW | ~$2-3B | Marginally | #4 |
| **Semiconductor TCAD** | LOW | ~$1-2B | No | #5 |
| **Seismic** | VERY LOW | ~$2B | No | #6 |
| **Network traffic** | VERY LOW | ~$4.4B | No | #7 |

---

## Software Product Assessment

### The Product: "FareyMix" -- Optimal Gaussian Mixture Compression Library

**What it does:** Given a 1D density field (empirical data, existing GMM, or functional form), returns the minimal Gaussian mixture representation that meets a user-specified accuracy threshold. Uses Farey-guided placement of components at number-theoretically optimal positions.

**API concept:**
```python
from fareymix import compress, fit

# Compress an existing GMM from 200 to ~36 components (5.5x reduction)
compressed = compress(existing_gmm, target_accuracy=0.99)

# Fit raw data directly with optimal component count
optimal_gmm = fit(data, method="farey", max_error=1e-3)
```

### Target Users (in priority order):

1. **ML engineers** fitting GMMs for clustering/anomaly detection (scikit-learn users). Pain: choosing K, slow EM convergence. Value: automatic optimal K, faster inference.

2. **Quantitative analysts** fitting risk-neutral densities from option data. Pain: balancing accuracy vs. speed for real-time pricing. Value: fewer components = lower latency with preserved tail accuracy.

3. **Simulation engineers** specifying initial density profiles for PIC/plasma codes. Pain: manual tuning of beam/plasma profiles. Value: compact, accurate profile specification.

### Business Model Options:

- **Open-source library + paid cloud API** (like Hugging Face model). Free for small-scale, metered for production.
- **Enterprise license** for financial firms (they pay $50K-500K/year for quant libraries).
- **Integration with scikit-learn** as a plugin (GMM component selection method). Massive distribution, low revenue per user.

### Honest Assessment:

**Strengths:**
- Clear, demonstrable advantage (5.5x is large)
- GMM compression is an active research problem (GMMultiMixer 2025)
- Easy to integrate (drop-in replacement for component selection)

**Weaknesses:**
- 1D only (current proof). Most real applications are multivariate. Extension to nD is the critical gap.
- The 5.5x advantage is on synthetic data. Real-world benchmarks needed.
- Competing with free tools (scikit-learn BIC/AIC). Hard to monetize unless targeting finance.
- The ML market wants multivariate GMMs. 1D is a niche within a niche.

### Bottom Line:

The **realistic addressable market for a 1D-only tool is small** (~$5-20M TAM). The technology becomes commercially significant ONLY if it extends to multivariate (nD) density fields. The 1D result is a proof of concept, not a product.

**Recommended path:** Publish the 1D result, demonstrate on 2D/3D GMMs, THEN productize. Target finance first (highest willingness to pay), ML second (largest volume).

**Kill criterion:** If Farey densification does not extend to nD with similar advantages, the commercial opportunity is negligible. The math must generalize.
