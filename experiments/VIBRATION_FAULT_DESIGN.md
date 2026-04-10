# Rigorous Test Design: Bearing Fault Detection with $f^2$ Spectral Compensation vs. Least Squares

## 1. Test Objective
To quantify the sensitivity gain of **$f^2$ Spectral Compensation** over standard **Least Squares (LS)** spectral estimation (Lomb-Scargle) in detecting weak bearing faults ($BPFO=89.2\text{ Hz}$) hidden within:
1.  Colored background noise ($1/f$).
2.  Dominant low-frequency shaft vibration (30 Hz).
3.  Irregular sampling (5% data dropouts).

## 2. Simulation Parameters

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Sampling Rate ($f_s$)** | 10 kHz | Nominal uniform sampling rate. |
| **Duration ($T$)** | 60 s | Total observation time ($N \approx 600,000$). |
| **Shaft Fundamental ($f_1$)** | 30 Hz | Primary rotating component. |
| **Shaft Harmonics** | $n \cdot f_1$ | 2nd to 10th harmonics included. |
| **Fault Frequency ($f_{BPFO}$)** | 89.2 Hz | Bearing fault (interference with 3rd harmonic at 90 Hz). |
| **Noise Type** | Pink ($1/f$) | Power Spectral Density (PSD) $\propto 1/f$. |
| **Dropout Rate** | 5% | Random removal of samples (irregular sampling). |
| **Fault Amplitude** | Variable | Sweep from $0.1\%$ to $10\%$ of shaft amplitude. |

## 3. Signal Generation Model

### A. Time Vector (Irregular)
Generate $N_{total}$ samples where 5% are randomly deleted.
Let $t$ be the original uniform grid. Let $\mathbb{M}$ be a random mask where $\mathbb{M}_i \in \{0, 1\}$ (0 = missing).
$$t_{\text{irreg}} = \{ t_i \mid \mathbb{M}_i = 1 \}$$
*Note: This creates a non-uniform time grid suitable for Lomb-Scargle analysis but invalid for standard FFT.*

### B. Signal Components
1.  **Shaft Vibration:**
    $$x_{\text{shaft}}(t) = \sum_{k=1}^{10} A_k \sin(2\pi \cdot k \cdot 30 \cdot t + \phi_k)$$
    *Assumption: $A_1 = 1.0$ (normalized), $A_k$ decays with $k$.*
2.  **Fault Signal:**
    $$x_{\text{fault}}(t) = A_{\text{fault}} \cdot \sin(2\pi \cdot 89.2 \cdot t + \phi_f)$$
    *Challenge: 89.2 Hz is spectrally close to 90 Hz (3rd harmonic). Windowing leakage will be a factor.*
3.  **Colored Noise:**
    Generate Gaussian white noise $w(t)$, filter via $H(z) = 1 - 0.975z^{-1}$ (approx $1/f$) or filter white noise via spectral shaping $\propto 1/\sqrt{f}$.
    Let $n_{\text{pink}}(t)$ be the pink noise with total RMS such that the $10\log(SNR_{\text{global}}) \approx 0 \text{ dB}$ to $10 \text{ dB}$ initially.

**Total Signal:**
$$x(t) = x_{\text{shaft}}(t) + x_{\text{fault}}(t) + n_{\text{pink}}(t)$$

## 4. Detection Methodologies

Both methods utilize the **Lomb-Scargle Periodogram (LSP)** to handle irregular sampling.

### A. Method 1: Least Squares (LS) Baseline
*   **Algorithm:** Standard LSP magnitude squared.
*   **Weighting:** Flat ($W(f) = 1$).
*   **Estimation:** Fit a sinusoid at $f_{BPFO}$ to the time series using Least Squares minimization of residuals.
    $$\hat{A}_{LS} = \arg \min_{A, \phi} \sum_{t \in \text{valid}} [x(t) - A \sin(2\pi f_{BPFO} t + \phi)]^2$$

### B. Method 2: $f^2$ Spectral Compensation
*   **Rationale:** In bearing diagnostics, high-frequency fault transients are often masked by low-frequency vibration ($1/f$ noise). The $f^2$ compensation acts as a high-pass spectral weight to boost high-frequency content relative to the $1/f$ decay.
*   **Algorithm:** LSP Magnitude Squared scaled by frequency squared.
*   **Weighting Function:**
    $$P_{\text{comp}}(f) = P_{\text{LSP}}(f) \cdot \left( \frac{f}{f_{BPFO}} \right)^2$$
    *Note: Normalized to the fault frequency to avoid scaling the absolute value improperly.*
*   **Estimation:** Apply threshold to the **compensated** spectrum at $f_{BPFO}$.

## 5. Execution Procedure

### Step 1: Monte Carlo Generation
Run $M=1000$ trials for each fault amplitude level $A_{\text{fault}} \in \{0.01, 0.05, 0.1, 0.2, 0.5, 1.0\}\%$.
*   Randomize phases $\phi$ for all components.
*   Randomize dropout locations for each trial.
*   Randomize pink noise seed.

### Step 2: Threshold Calibration (ROC Curve)
Using a set of $N_{\text{null}}$ trials where $A_{\text{fault}} = 0$:
1.  Compute $P_{\text{comp}}(f_{BPFO})$ for all trials.
2.  Determine threshold $\eta_{LS}$ and $\eta_{f^2}$ for a False Alarm Rate (FAR) of $1\%$ ($P_{fa}=0.01$).

### Step 3: Detection Probability Measurement
For each non-zero amplitude trial:
1.  Check if computed power $> \eta$.
2.  Record Success/Failure.
3.  Calculate Detection Probability $P_d$.

### Step 4: SNR Calculation
Calculate the effective SNR in the processed spectrum:
$$\text{SNR}_{\text{dB}} = 10 \log_{10} \left( \frac{\text{Peak Power at } 89.2\text{Hz}}{\text{Median Noise Power in } 50\text{-}150\text{Hz}} \right)$$

## 6. Expected Theoretical Results

1.  **LS Baseline:**
    *   The $1/f$ noise dominates at 30Hz. The 89.2Hz band is quieter but the noise floor is still colored.
    *   The 3rd harmonic at 90Hz will cause spectral leakage (smearing) into the 89.2Hz bin, reducing detectability.
    *   **Expected Threshold:** $\approx 3\% - 5\%$ amplitude for $95\%$ detection.

2.  **$f^2$ Compensation:**
    *   The weighting $W(f) \propto f^2$ attenuates low-frequency noise (30Hz) and amplifies high-frequency noise (89Hz) *relative to white*. However, because the original noise is $1/f$, the net slope becomes flatter (White-like) or slightly rising.
    *   Crucially, it suppresses the 30Hz harmonic leakage energy, "clearing" the floor around 89.2 Hz.
    *   **Expected Threshold:** $\approx 1\% - 2\%$ amplitude for $95\%$ detection.

## 7. Success Criteria

A test is considered **Successful** if:

1.  **Sensitivity Improvement:** The minimum detectable fault amplitude ($A_{\text{min}}$) for $f^2$ compensation is at least **50% lower** than for the LS method (e.g., $A_{\text{min, LS}} = 5\%$, $A_{\text{min, f2}} = 2\%$).
2.  **SNR Gain:** The spectral SNR at the fault frequency for $f^2$ must be greater by $\Delta \text{SNR} > 6 \text{ dB}$ compared to LS at low amplitudes.
3.  **Robustness:** Detection performance degradation at $95\%$ sampling (5% dropouts) is $\le 2 \text{ dB}$ compared to uniform sampling.
4.  **Specificity:** The 90Hz harmonic does not trigger a false positive at $f_{BPFO} = 89.2\text{ Hz}$ in $f^2$ trials (i.e., spectral separation is maintained).

## 8. Pseudocode Implementation Structure

```python
import numpy as np
from scipy.signal import get_window

def generate_pink_noise(N, fs):
    # Generate white noise and filter to 1/f power
    white = np.random.randn(N)
    freqs = np.fft.rfftfreq(N, 1/fs)
    # H(f) ~ 1/sqrt(f) for power 1/f (approximation)
    H = 1.0 / np.sqrt(freqs + 0.01) 
    signal = np.fft.irfft(np.fft.rfft(white) * H)
    return signal / np.std(signal)

def lomb_scargle_spectrum(signal, times, freqs, weight=None):
    # Returns standard LS LSP
    # Implement standard LSP math here
    pass

def run_detection_test():
    fs = 10000
    T = 60
    N = int(T * fs)
    
    # 1. Create Irregular Time Grid (5% dropout)
    time_full = np.linspace(0, T, N)
    drop_mask = np.random.rand(N) > 0.95 # Keep 95%
    t_irreg = time_full[drop_mask]
    
    # 2. Generate Signals
    shaft = np.sin(2 * np.pi * 30 * time_full) + 0.2 * np.sin(2 * np.pi * 60 * time_full)
    fault = 0.05 * np.sin(2 * np.pi * 89.2 * time_full) # 5% fault
    noise = generate_pink_noise(N, fs)
    
    signal = (shaft + fault + noise) * drop_mask # Apply mask (zeros elsewhere)
    
    # 3. Apply Methods
    # LS Method
    lsd = lomb_scargle_spectrum(signal, t_irreg, [89.2], weight='none')
    # f^2 Compensation
    lsd_comp = lomb_scargle_spectrum(signal, t_irreg, [89.2], weight='f2')
    
    # 4. Compute SNR
    snr_ls = 10 * np.log10( (lsd[0]**2) / noise_floor )
    snr_f2 = 10 * np.log10( (lsd_comp[0]**2) / noise_floor_f2 )
    
    return snr_ls, snr_f2
```

## 9. Conclusion on "What Success Looks Like"

*   **Visual:** In a plot of Power Spectrum (dB vs Hz), the **LS method** shows a noisy floor with a barely visible bump at 89.2 Hz, indistinguishable from the tail of the 90 Hz harmonic.
*   **Visual:** The **$f^2$ method** shows a "cleaned" baseline where the 30 Hz peak is suppressed, and the 89.2 Hz peak is clearly resolved from the 90 Hz interference due to the higher frequency resolution weighting.
*   **Quantitative:** The ROC Curve for $f^2$ shifts significantly to the left (lower SNR required) compared to LS. The detection threshold for $f^2$ compensation should be **< 1.5% amplitude** relative to shaft vibration, whereas LS fails below **~4.5%**.
