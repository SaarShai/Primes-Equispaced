# Farey Densification: Market Analysis & Dimensional Strategy

**Date:** 2026-03-29
**Status:** Research complete, recommendations included

---

## PART 1: Market Value of 1D Farey Applications

### Executive Summary

1D is where Farey densification has a genuine structural advantage: the mediant operation produces gap-filling points with provably optimal distribution properties. Six application domains were evaluated. Three have real commercial potential; three are interesting but harder to monetize.

---

### 1. Audio / Speech Processing

**Market size:** Audio DSP market ~$6-17B in 2024 (estimates vary by scope). Adaptive audio processing sub-segment ~$1.2B growing to $2.8B by 2035.

**Pain points:**
- Neural audio codecs (RVQ-based) struggle with codebook collapse and low utilization
- Adaptive bitrate allocation across frequency bands remains an open problem
- Edge/wearable devices need lower sampling rates without quality loss

**Where Farey fits:**
- Frequency band quantization: Farey mediants could place quantization levels where perceptual sensitivity is highest, adapting to content
- Non-uniform sampling grids for spectral analysis (NUDFT applications)
- Codebook initialization: Stern-Brocot tree provides a structured way to populate vector quantization codebooks that avoids collapse

**Key players:** Qualcomm (aptX Adaptive), Google (Lyra/SoundStream), Meta (EnCodec), Descript (neural codecs)

**Competitive landscape:** The Q2D2 paper (Dec 2025) already uses geometric 2D quantization grids (hexagonal, rhombic) for audio codecs. Farey-based grids would be a direct competitor/alternative with stronger theoretical guarantees about gap distribution.

**Assessment: MEDIUM-HIGH potential.** The codec space is moving fast toward learned/geometric quantization. Farey has a theoretical story to tell (provably optimal gap-filling) but needs benchmarks against Q2D2 and FlexiCodec.

**Estimated addressable market:** $50-200M (codec optimization layer within the broader audio DSP market)

---

### 2. Time Series Analysis (Financial, IoT, Sensor Streams)

**Market size:** Time series analysis software ~$2.5B in 2025 (CAGR 15%). IoT sensors market ~$24B in 2025 growing to $99B by 2030. Sensor data analytics ~$2.1B growing to $14B by 2035.

**Pain points:**
- IoT generates 175 zettabytes/year. Edge devices cannot transmit everything.
- Irregular/missing timestamps are a major headache (Databricks blog highlights this as a top challenge)
- Adaptive sampling at the edge: deciding WHEN to sample next is critical for battery life
- Financial high-frequency data: non-uniform tick data needs interpolation

**Where Farey fits:**
- Adaptive sampling schedule: Farey mediants can determine optimal next-sample timing between two known samples, filling gaps where signal changes most
- Missing data imputation: mediant-based interpolation for irregular time series
- Compression at the edge: Farey-structured sampling reduces data volume while preserving signal features

**Key players:** Databricks, InfluxDB, TimescaleDB, AWS IoT Analytics, Azure Stream Analytics

**Competitive landscape:** Current adaptive sampling is mostly threshold-based (sample when delta exceeds X) or ML-based (learn when to sample). Farey provides a deterministic, lightweight alternative that could run on microcontrollers without ML inference overhead.

**Assessment: HIGH potential.** The IoT edge sampling problem is real, growing fast, and Farey's lightweight deterministic nature is a genuine advantage over ML-based approaches on constrained hardware.

**Estimated addressable market:** $100-500M (adaptive edge sampling within the IoT analytics stack)

---

### 3. 1D Signal Compression (Audio Codecs, Seismic, ECG/EEG)

**Sub-domain 3a: Seismic Data**

**Market size:** Seismic data acquisition & processing ~$428M in 2025 (CAGR 8.7%). Broader seismic services ~$9.6B. Seismic data alone accounts for 54.7% of oil/gas data monetization.

**Pain points:** Modern campaigns generate petabytes. Compression during acquisition (before transmission) is critical. Shift to wireless/nodal systems increases compression needs.

**Where Farey fits:** Seismic traces are 1D signals. Farey-based adaptive quantization could optimize bit allocation along each trace based on signal complexity. The mediant property naturally allocates more precision where the signal varies most.

**Assessment: MEDIUM.** Niche but high-value per customer. Oil companies pay well for marginal improvements. Hard to break into without domain partnerships.

**Sub-domain 3b: ECG/EEG Wearables**

**Market size:** EEG devices ~$1.4B in 2025. Wearable EEG headsets ~$146M. ECG+EEG biometrics ~$1.7B. Growing fast with AI integration.

**Pain points:** Compressed sensing (CS) is already used for ECG, but reconstruction is expensive. Wearables need sub-milliwatt compression. Adaptive sampling rate is critical for battery life.

**Where Farey fits:**
- Adaptive sampling rate selection: Farey mediants between current and Nyquist rate based on signal activity
- Lightweight compression: no ML inference needed, pure arithmetic on Farey fractions
- This is perhaps the strongest 1D use case: constrained hardware, 1D signal, need for deterministic behavior (medical certification requires predictability)

**Key players:** Apple (Watch ECG), Samsung, Fitbit/Google, Muse (EEG), Emotiv, PiEEG

**Assessment: HIGH potential.** Medical wearables need deterministic, certifiable algorithms. Farey-based adaptive sampling is simpler to certify than ML-based approaches. FDA prefers interpretable algorithms.

**Estimated addressable market:** $20-100M (compression/sampling IP for wearable medical devices)

---

### 4. 1D Gaussian Splatting for Audio

**Current state:** No one has published on using 1D Gaussian splatting as an audio signal representation. The concept exists only as a pedagogical example (IPOL 2025 paper demonstrates 1D GS to teach the concept). All audio+GS work uses 3D GS for spatial audio or talking heads.

**Where Farey fits:** If 1D GS for audio emerges as a field, Farey densification would be a natural fit for placing Gaussians adaptively. The GaussianImage++ paper (Dec 2025) shows that densification strategy is THE key differentiator in 2D GS quality.

**Assessment: LOW (for now).** This is a research opportunity, not a market. Could become relevant if 1D GS for audio takes off, but there is no existing community or customers. Filing a position paper could establish priority.

**Estimated addressable market:** $0 today. Speculative future.

---

### 5. LiDAR Point Cloud Along Scan Lines

**Market size:** Automotive LiDAR ~$1.3B in 2025, projected $9.6-11.9B by 2030-2032 (CAGR 41-50%). Broader LiDAR ~$2.9B in 2025.

**Pain points:**
- Each LiDAR scan line IS a 1D signal (angular sweep at fixed elevation)
- Sparse regions between scan lines need densification for object detection
- Real-time processing: must process at sensor frame rate (10-20 Hz)
- HilComp (ICIC 2025) already uses Hilbert curves for ordering 3DGS point clouds

**Where Farey fits:**
- Along each scan line: Farey mediants can densify sparse regions between measured points
- Between scan lines: interpolation using Farey structure on the angular coordinate
- The 1D-along-scan-lines framing avoids the 2D/3D problems where Farey underperforms

**Key players:** Velodyne/Ouster, Hesai, Luminar, Cepton, Innoviz, Robosense

**Competitive landscape:** Current densification is ML-based (LiDARGen, PcdGS) or simple interpolation. Farey offers a deterministic, real-time alternative.

**Assessment: MEDIUM-HIGH.** The market is huge and growing explosively. The scan-line decomposition is a genuine insight. But breaking into automotive requires meeting ASIL-D safety standards, which is a long certification path.

**Estimated addressable market:** $50-300M (point cloud processing software within the automotive LiDAR stack)

---

### 6. Network Traffic / Packet Scheduling

**Market size:** Network management ~$10.4B in 2025. Network traffic analytics ~$6.8B. Combined adjacent markets $4-11B.

**Pain points:**
- QoS scheduling must decide when to send packets from competing flows
- Fairness + efficiency tradeoff is mathematically identical to Farey gap-filling
- 5G network slicing creates new scheduling challenges
- IoT industrial scheduling (6TiSCH) needs adaptive slot allocation

**Where Farey fits:**
- Packet scheduling as rational approximation: each flow gets a fraction of bandwidth; Farey mediants optimally interleave flows
- This is actually the closest mathematical analog to what Farey densification does: fair division of a 1D resource (time slots)
- Could produce provably fair scheduling with optimal jitter properties

**Key players:** Cisco, Juniper, Nokia, Ericsson, Qualcomm (5G modems)

**Assessment: MEDIUM.** Beautiful mathematical fit but very hard to sell. Network equipment vendors have entrenched scheduling algorithms. Would need to show measurable QoS improvement in a specific 5G/IoT scenario.

**Estimated addressable market:** $20-100M (scheduling algorithm IP, likely licensed)

---

### PART 1 SUMMARY: Ranked by commercial potential

| Rank | Domain | Market Fit | Size (Addressable) | Ease of Entry | Score |
|------|--------|-----------|-------------------|---------------|-------|
| 1 | **IoT/Time Series Edge Sampling** | HIGH | $100-500M | Medium | **A** |
| 2 | **ECG/EEG Wearable Compression** | HIGH | $20-100M | Medium-High | **A-** |
| 3 | **LiDAR Scan-Line Densification** | MEDIUM-HIGH | $50-300M | Low (certification) | **B+** |
| 4 | **Audio Codec Quantization** | MEDIUM-HIGH | $50-200M | Medium | **B+** |
| 5 | **Seismic Data Compression** | MEDIUM | $10-50M | Low (domain expertise) | **B** |
| 6 | **Packet Scheduling** | MEDIUM | $20-100M | Low (entrenched vendors) | **B-** |
| 7 | **1D Gaussian Splatting Audio** | LOW | $0 (speculative) | N/A | **C** |

**Top recommendation:** IoT edge sampling and ECG/EEG wearables. Both need lightweight, deterministic, certifiable algorithms. Both are 1D problems. Both markets are growing at >15% CAGR. Farey's mathematical properties (provably optimal gap-filling, no ML overhead, deterministic behavior) are genuine competitive advantages in these domains.

---

## PART 2: Is 2D/3D a Dead End?

### Honest Assessment of Current Results

Our 2D results showed error-guided densification beating Farey on real images. This is not surprising: images have spatial correlations and edges that a content-agnostic mathematical scheme cannot exploit. However, there are specific scenarios worth examining.

---

### 1. 2D via 1D Decomposition (Separable Approach)

**Idea:** Apply Farey along rows, then along columns independently.

**Analysis:**
- Separable processing is standard in image/video compression (DCT is separable)
- Advantage: each row/column IS a genuine 1D problem where Farey excels
- Disadvantage: misses diagonal features and 2D correlations
- GaussianImage++ (Dec 2025) shows that the key to 2D GS is content-aware densification, not mathematical regularity

**Verdict: QUICK TEST WORTHWHILE** but unlikely to beat content-aware methods on natural images. Could work for signals with separable structure (spectrograms, where frequency axis and time axis have different statistics).

**Specific test:** Apply Farey densification to spectrogram rows (frequency) and columns (time) separately. Compare against uniform grid and random placement. This is essentially the "video: Farey along time" idea below.

---

### 2. 2D Stern-Brocot Tree / Multidimensional Continued Fractions

**What exists:**
- Lennerstad (Blekinge Institute of Technology) proved the n-dimensional Stern-Brocot tree exists with a similar tree structure and subtree isomorphism
- Jacobi-Perron algorithm generalizes continued fractions to n dimensions
- TRIP-Stern sequences connect Stern sequences to triangle partition maps
- The periodicity problem for Jacobi-Perron is STILL OPEN (unknown if all algebraic irrationals of degree m+1 produce periodic expansions)

**Gap-filling properties:**
- The n-dimensional Stern-Brocot tree does enumerate rational n-tuples
- But the mediant operation in nD does not have the same optimality guarantees as in 1D
- In 1D, consecutive Farey fractions satisfy |p/q - p'/q'| = 1/(qq') -- this has no clean nD analog
- The "extra complication of prime sequences having different degrees" (Lennerstad) means the 2D tree structure is fundamentally more complex

**Verdict: KILL as a practical approach.** The math is beautiful but the 1D optimality properties that make Farey useful DO NOT generalize cleanly to 2D. The open periodicity problem for Jacobi-Perron after 150+ years is a red flag -- if the theory is not settled, practical applications are premature.

---

### 3. 3D for Point Clouds (via Space-Filling Curves)

**What exists:**
- HilComp (ICIC 2025) already uses Hilbert curves to order 3D Gaussians for compression
- The Hilbert curve + LDS paper (2025) shows this ordering preserves spatial coherence
- Our synthetic 3D density test showed Farey winning

**Why it might work:** Point clouds mapped to a 1D ordering via Hilbert/Z-curve reduce the 3D problem to a 1D problem. Farey densification along this 1D ordering could work because:
- Hilbert curve has known locality-preserving properties
- Nearby 3D points map to nearby 1D positions
- Farey mediants on the 1D sequence fill spatial gaps

**Why it might not:** The Hilbert mapping is not bijective in terms of distance -- two 3D-nearby points can be far apart on the curve at certain scales. Farey densification would insert points that are 1D-mediants but might not correspond to geometrically meaningful 3D positions.

**Verdict: WORTH ONE CAREFUL TEST.** Specifically: take a point cloud, map to Hilbert curve, apply Farey densification along the curve, map back to 3D, measure density uniformity. Compare against: (a) random densification, (b) direct 3D k-nearest-neighbor interpolation. If Farey along Hilbert beats random but loses to direct 3D, the result is expected and we should stop. If it beats direct 3D in any metric, that is publishable.

---

### 4. Where 2D Farey MIGHT Work: Privileged-Axis Problems

**Video (time axis):**
- Temporal interpolation between keyframes is a massive market (frame interpolation, slow-motion)
- Time axis IS 1D, and frame interpolation is essentially gap-filling along time
- But: modern frame interpolation uses optical flow + neural networks, which exploit spatial correlations
- Farey temporal interpolation would only make sense for deciding WHEN to place new keyframes, not WHAT they contain

**Panoramic images (angular axis):**
- 360-degree images have a periodic angular axis
- Farey sequence on a circle: this IS our core research (Farey sequences mod 1)
- Could determine optimal angular sampling for panoramic capture
- Niche but could be relevant for VR/AR camera systems

**Spectrograms (frequency-time):**
- Frequency axis has known structure (harmonic series, overtones)
- Time axis is where events happen
- Farey along frequency could place resolution where harmonic content is densest
- This is actually the audio codec application from Part 1, viewed as a 2D problem

**Verdict:** The only 2D scenarios that work are those decomposable into two independent 1D problems, one of which has natural Farey structure. This is NOT really 2D Farey -- it is 1D Farey applied to a privileged axis within a 2D domain.

---

### PART 2 SUMMARY: Kill/Keep Decisions

| Direction | Decision | Rationale |
|-----------|----------|-----------|
| Pure 2D Farey densification | **KILL** | Error-guided beats it on real images. No theoretical advantage. |
| 2D Stern-Brocot / Jacobi-Perron | **KILL** | 1D optimality does not generalize. Open problems after 150 years. |
| 2D separable (row+column) | **ONE TEST** | Try on spectrograms only. If it loses, kill. |
| 3D via Hilbert curve | **ONE TEST** | Clear experimental design. Publishable if it works. |
| Video temporal densification | **KILL** | Optical flow + neural nets dominate. Farey adds nothing. |
| Panoramic angular sampling | **DEPRIORITIZE** | Niche. Interesting but tiny market. |
| Spectrogram frequency-time | **REDIRECT to Part 1** | This is the audio codec application. Pursue as 1D. |

**The ONE most promising direction for a quick test:** 3D point cloud densification via Hilbert curve ordering. It has a clean experimental design, connects to active research (HilComp 2025), and the result is informative either way.

---

## OVERALL STRATEGIC RECOMMENDATION

1. **Double down on 1D.** The market analysis confirms that 1D applications have real, large, growing markets where Farey's properties provide genuine advantages.

2. **Lead with IoT edge sampling and medical wearables.** These are the highest-value targets with the best fit for Farey's properties (lightweight, deterministic, certifiable).

3. **Run exactly one 3D experiment** (Hilbert curve). Spend no more than 1-2 days. Either it works and we have a publication angle, or it does not and we fully commit to 1D.

4. **Kill everything else in 2D/3D.** Do not spend more cycles on pure 2D densification, 2D Stern-Brocot theory, or video temporal interpolation.

5. **For commercialization:** Build a small library (C or Rust) that implements Farey adaptive sampling for 1D signals. Benchmark against uniform sampling and threshold-based adaptive sampling on: (a) synthetic signals, (b) real ECG data, (c) real IoT sensor streams. This becomes the demo for potential partners/customers.
