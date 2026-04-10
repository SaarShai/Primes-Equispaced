# Test Specification: Spectral Botnet Detection Validation
**Document ID:** NET-SPEC-001  
**Version:** 1.0  
**Status:** Draft for Simulation & Validation

## 1. Executive Summary
The objective of this test is to rigorously evaluate the efficacy of spectral analysis techniques in detecting hidden C2 (Command & Control) communications within high-volume network traffic. The core hypothesis being tested is that **C2 signals at $f_{C2} = 0.033\text{ Hz}$ represent a "high-frequency" signal relative to the effective noise floor of Poisson-distributed traffic when utilizing $f^2$-compensated periodograms**, providing a superior signal-to-noise ratio (SNR) compared to the Lomb-Scargle (LS) algorithm in specific contexts.

This specification defines the traffic generation model, algorithmic comparison, metrics for success, and failure conditions ("kill switches").

## 2. Simulation Environment (Ground Truth)

### 2.1 Traffic Generation Logic
The simulation must generate a synthetic timestamp stream $T = \{t_1, t_2, \dots, t_N\}$ over a total duration $D$.

*   **Duration ($D$):** Minimum **1200 seconds** (20 minutes).
    *   *Rationale:* To achieve statistical significance for a 0.033 Hz signal (Period $T=30$s), we need at least 15–20 full cycles to separate signal from noise floor.
*   **Background Noise (Poisson Process):**
    *   Rate $\lambda = 10 \text{ Hz}$.
    *   Mean Gap $\mu = 0.1\text{s}$.
    *   Inter-arrival times $g_i \sim \text{Exp}(\lambda)$.
*   **C2 Signal (Hidden Periodicity):**
    *   Frequency $f_{C2} = 0.033\text{ Hz}$ (Period $\approx 30.30\text{s}$).
    *   Modulation: Adds event probability or timestamp perturbation.
    *   *Implementation:* For every $n$-th interval, add a jitter term or inject a burst. To ensure it is "detected" as periodicity, we model it as a **Periodic Jitter in Event Rate**.
    *   $P(\text{event at } t) = \lambda + A \cdot \sin(2\pi f_{C2} t + \phi)$.
    *   Jitter: Gaussian noise $\sigma_{jitter} = 0.1 \times T_{C2}$ (10% cycle jitter).
    *   *Constraint:* Amplitude $A$ must be tuned such that the signal-to-noise ratio is marginal (SNR $\approx 1:5$ in spectral domain).
*   **DDoS Interference (Masking Pulse):**
    *   Frequency $f_{DDoS} = 0.2\text{ Hz}$ (Period $= 5\text{s}$).
    *   Type: Burst/Boxcar modulation (ON for 1s, OFF for 4s).
    *   Amplitude: Significantly higher than C2 to test algorithm robustness against strong interference.

### 2.2 Input Data
The system under test (SUT) must ingest raw event timestamps $\{t_i\}$ in epoch seconds, not aggregated counts.

## 3. Algorithms Under Test

### 3.1 Method A: Lomb-Scargle (LS) Periodogram
*   **Standard:** The gold standard for unevenly sampled time series.
*   **Normalization:** Normalized to unit variance.
*   **Frequency Grid:** $0.001\text{ Hz}$ to $5.0\text{ Hz}$ (covers background Nyquist and signal).
*   **Null Hypothesis:** Red noise or white noise (Poisson).
*   **Output:** Peak power at specific frequencies with false alarm probability ($p_{fa}$).

### 3.2 Method B: $f^2$-Compensated Binned Periodogram
*   **Logic:** This test explicitly evaluates the "sweet spot" hypothesis.
*   **Binning:** Events aggregated into bins of size $\Delta t = 0.1\text{s}$.
*   **Raw Periodogram:** $P(f) = |FFT(\text{counts})|^2$.
*   **Compensation:** $P_{comp}(f) = \frac{P(f)}{f^2}$.
    *   *Note:* This weighting attempts to emphasize high-frequency variations and suppress low-frequency spectral leakage or drift.
*   **Detuning:** The SUT claims $f=0.033\text{ Hz}$ is a "sweet spot" under this weighting.
*   **Output:** $P_{comp}(f)$ profile.

## 4. Test Execution Protocol

1.  **Warm-up:** Generate 10,000 background events (approx. 1000s) to stabilize variance.
2.  **Run Sequence:** Generate traffic with fixed seed for repeatability.
3.  **Signal Injection:**
    *   **Run 1:** Only Poisson (Baseline).
    *   **Run 2:** Poisson + C2 (0.033 Hz).
    *   **Run 3:** Poisson + C2 + DDoS (0.2 Hz).
    *   **Run 4 (Stress):** Poisson + C2 + DDoS + Random Jitter Spike.
4.  **Repetition:** Execute 100 Monte Carlo simulations (random seeds) for statistical robustness.
5.  **Analysis:** Run both algorithms on each trace. Record peak locations and power values.

## 5. Success Criteria

### 5.1 Primary Metric: Detection Probability ($P_d$)
*   **Goal:** $P_d \geq 0.95$ for $f_{C2}$ with a confidence threshold of $p_{fa} < 0.05$ (standard spectral false alarm rate).
*   **LS Requirement:** LS must identify the 0.033 Hz peak as the local maximum in the low-frequency range (0.01–0.1 Hz) in at least 95% of Monte Carlo runs.
*   **f^2 Requirement:** The $f^2$-compensated periodogram must identify the 0.033 Hz peak with **equal or better SNR** than the LS algorithm.

### 5.2 Secondary Metric: Frequency Resolution
*   **Goal:** Estimated frequency error $|\hat{f} - f_{C2}| < 0.005\text{ Hz}$.
*   **Reasoning:** High-frequency jitter can smear peaks. The test validates that the algorithm resolves the "sweet spot" precisely.

### 5.3 Interference Rejection
*   **Goal:** The 0.2 Hz DDoS signal must **not** trigger a false positive at 0.033 Hz.
*   **Metric:** The ratio of Power($0.033$ Hz) / Power($0.2$ Hz) in the compensated domain must exceed a defined threshold (e.g., 3 dB gain required for the C2 peak relative to the DDoS aliasing).

### 5.4 The "Sweet Spot" Validation
*   **Claim:** "0.033 Hz is High Frequency relative to Poisson Spectrum."
*   **Validation:** We must show that the SNR at 0.033 Hz is significantly higher than at 0.01 Hz or 0.1 Hz.
*   **Measurement:** Plot $\text{SNR}(f) = P(f)/P_{noise}(f)$. The peak of this function should be at or near 0.033 Hz.

## 6. Failure Modes (The "Kill Switch")

The design concept should be considered **invalid or obsolete** if the following conditions are met:

### 6.1 The White Noise Fallacy
*   **Condition:** The $f^2$-compensated periodogram fails to outperform LS, or LS is significantly superior.
*   **Diagnosis:** Poisson processes exhibit *white* noise ($1/f^0$) in the count spectrum. Dividing by $f^2$ artificially suppresses low frequencies. If 0.033 Hz is physically low-frequency (as it is in absolute terms), $f^2$ compensation should **reduce** its visibility relative to higher frequencies.
*   **Kill Switch:** If the SNR of the $f^2$ method at 0.033 Hz is lower than the raw $f^2=0$ method, the premise of the "sweet spot" is falsified.

### 6.2 Spectral Leakage Masking
*   **Condition:** The 0.2 Hz DDoS pulse aliases into the 0.033 Hz bin due to binning artifacts.
*   **Diagnosis:** If the DDoS frequency is exactly 6x the C2 frequency ($0.2 / 0.033 \approx 6$), harmonics will overlap.
*   **Kill Switch:** If the DDoS interference causes a False Positive on the C2 frequency in >5% of trials, the binning strategy is insufficient for production.

### 6.3 Jitter Saturation
*   **Condition:** Jitter $\sigma_{jitter}$ causes the periodicity to smear over the detection window.
*   **Diagnosis:** If the Lomb-Scargle coherence drops below 0.5.
*   **Kill Switch:** If the detection success rate drops below 50% as jitter increases from 5% to 50% of the period, the algorithm is too fragile for real-world botnet behavior.

### 6.4 Sampling Bias (The "Sweet Spot" Illusion)
*   **Condition:** The 0.033 Hz frequency aligns perfectly with the binning window $\Delta t$ (e.g., $\Delta t = 30\text{s}$).
*   **Diagnosis:** If $f_{C2}$ is detected only because the binning aligns with the period (harmonic resonance).
*   **Kill Switch:** If detection success drops by >20% when $\Delta t$ is perturbed by $\pm 1\text{s}$, the detection is not robust to timing misalignment.

## 7. Analysis Deliverables
1.  **Receiver Operating Characteristic (ROC) Curves:** For both LS and $f^2$ methods.
2.  **Spectral Power Density Plots:** Showing the 0.2 Hz suppression and 0.033 Hz detection.
3.  **Failure Log:** Timestamped logs of all false positives and false negatives.
4.  **Physics Verification:** A plot of the theoretical Poisson noise floor vs. the measured noise floor to validate the "white noise" assumption.

---

### Critical Technical Note on the "High Frequency" Claim
*For the test lead:* Be aware that $f=0.033\text{ Hz}$ is an **extremely low frequency** (30s period) relative to a 10 Hz Poisson background. In standard spectral theory, dividing by $f^2$ (pre-whitening) suppresses *low* frequencies to expose high frequencies.
*   **Risk:** Applying $f^2$ compensation to a 0.033 Hz signal in a white-noise background will likely **diminish** the signal power relative to the noise compared to an unweighted analysis.
*   **Test Implication:** This test will likely prove that the "sweet spot" claim is **incorrect** unless the background noise is actually "Red Noise" ($1/f^2$) rather than Poisson (White). If the simulation confirms White Noise, the $f^2$ method will fail, suggesting the detection logic requires re-engineering to rely on LS or Count-based methods instead. This is a valid and rigorous scientific outcome.
