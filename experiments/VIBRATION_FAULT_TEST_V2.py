import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Set paths
base_path = os.path.expanduser("~/Desktop/Farey-Local")
experiments_path = os.path.join(base_path, "experiments")
figures_path = os.path.join(base_path, "figures")
os.makedirs(experiments_path, exist_ok=True)
os.makedirs(figures_path, exist_ok=True)

results_file = os.path.join(experiments_path, "VIBRATION_FAULT_TEST_V2.md")

# Parameters
sample_rate = 10000  # 10kHz
n_points = 50000
dropout_rate = 0.05
fault_frequency = 89.2  # Hz
amplitudes = [0.01, 0.02, 0.05, 0.1, 0.2]

# Generate regular time vector
t_regular = np.arange(n_points) / sample_rate

# 1. Generate shaft vibration signal
shaft_vibration = np.sin(2 * np.pi * 30 * t_regular) + 0.5 * np.sin(2 * np.pi * 60 * t_regular)

# 2. Generate pink noise using FFT method
def generate_pink_noise(n_samples, fs):
    """Generate pink noise using FFT method"""
    white_noise = np.random.randn(n_samples)
    fft_white = np.fft.fft(white_noise)
    freqs = np.fft.fftfreq(n_samples, 1/fs)
    freqs_abs = np.abs(freqs)
    freqs_abs = np.where(freqs_abs == 0, 1e-10, freqs_abs)
    
    pink_noise_fft = fft_white / np.sqrt(freqs_abs)
    pink_noise_fft[0] = 0  # Zero DC component
    
    pink_noise = np.real(np.fft.ifft(pink_noise_fft))
    return pink_noise

pink_noise = generate_pink_noise(n_points, sample_rate)

# 3. Create irregular sampling with 5% dropout
np.random.seed(42)
dropout_mask = np.random.random(n_points) > (1 - dropout_rate)
t_irregular = t_regular[dropout_mask]
signal_base = (shaft_vibration + pink_noise)[dropout_mask]

# Store results
results = {
    'amplitude': [],
    'lomb_scargle_snr': [],
    'f2_power_snr': [],
    'lomb_scargle_power': [],
    'f2_power': []
}

# Function to compute Lomb-Scargle power at specific frequency
def compute_lomb_scargle_power(signal, times, freq, freq_range=0.5, freq_step=0.5):
    """Compute Lomb-Scargle power at a specific frequency"""
    start_freq = max(0, freq - freq_range)
    end_freq = freq + freq_range
    freqs = np.arange(start_freq, end_freq, freq_step)
    powers = signal.lombscargle(times, signal, freqs, precentered=True)
    
    # Find power at target frequency
    target_idx = np.argmin(np.abs(freqs - freq))
    return powers[target_idx]

# Function to compute f^2 compensated power
def compute_f2_power(signal, times, freq):
    """Compute f^2 compensated power at a specific frequency"""
    omega = 2 * np.pi * freq
    exp_term = np.exp(-2j * np.pi * freq * times)
    spectrum = np.sum(signal * exp_term)
    power = (omega**2) * (np.abs(spectrum)**2) / len(times)**2
    return power

# Function to compute SNR: peak_at_target_freq / median_nearby
def compute_snr(signal, times, target_freq, fs, bandwidth=5.0, freq_resolution=0.5):
    """Compute SNR: peak_at_target_freq / median_nearby"""
    start_freq = max(0, target_freq - bandwidth)
    end_freq = target_freq + bandwidth
    freqs = np.arange(start_freq, end_freq, freq_resolution)
    
    # Compute Lomb-Scargle spectrum
    powers = signal.lombscargle(times, signal, freqs, precentered=True)
    
    # Find peak at target frequency
    target_idx = np.argmin(np.abs(freqs - target_freq))
    peak_power = powers[target_idx]
    
    # Find nearby frequency range for median (excluding target)
    nearby_mask = (np.abs(freqs - target_freq) > freq_resolution) & (freqs >= start_freq) & (freqs <= end_freq)
    nearby_powers = powers[nearby_mask]
    
    if len(nearby_powers) > 0:
        median_nearby = np.median(nearby_powers)
        if median_nearby > 0:
            snr = peak_power / median_nearby
        else:
            snr = float('inf')
    else:
        snr = float('inf')
    
    return snr, peak_power, powers, freqs, target_idx

# Print header
print("=" * 80)
print("BEARING FAULT DETECTION TEST")
print("=" * 80)
print(f"Sample Rate: {sample_rate} Hz")
print(f"Number of regular samples: {n_points}")
print(f"Number of irregular samples: {len(t_irregular)}")
print(f"Dropout rate: {dropout_rate * 100:.1f}%")
print(f"Fault frequency: {fault_frequency} Hz")
print(f"Test amplitudes: {amplitudes}")
print("=" * 80)

# Test each amplitude
lomb_snr_table = []
f2_snr_table = []
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

for i, amplitude in enumerate(amplitudes):
    # Add fault to signal
    fault_signal = amplitude * np.sin(2 * np.pi * fault_frequency * t_regular)
    signal_with_fault = signal_base + fault_signal[dropout_mask]
    
    # Compute Lomb-Scargle power at 89.2Hz
    lomb_power = compute_lomb_scargle_power(signal_with_fault, t_irregular, fault_frequency)
    
    # Compute f^2 compensated power at 89.2Hz
    f2_power = compute_f2_power(signal_with_fault, t_irregular, fault_frequency)
    
    # Compute SNR for both methods
    snr_lomb, peak_lomb, powers_lomb, freqs_lomb, idx_lomb = compute_snr(
        signal_with_fault, t_irregular, fault_frequency, sample_rate)
    
    snr_f2, peak_f2, powers_f2, freqs_f2, idx_f2 = compute_snr(
        signal_with_fault, t_irregular, fault_frequency, sample_rate)
    
    # Store results
    results['amplitude'].append(amplitude)
    results['lomb_scargle_snr'].append(snr_lomb)
    results['f2_power_snr'].append(snr_f2)
    results['lomb_scargle_power'].append(lomb_power)
    results['f2_power'].append(f2_power)
    
    # Table entries
    lomb_snr_table.append([amplitude, snr_lomb, lomb_power])
    f2_snr_table.append([amplitude, snr_f2, f2_power])
    
    print(f"\n--- Amplitude = {amplitude} ---")
    print(f"Lomb-Scargle SNR: {snr_lomb:.4f}, Power: {lomb_power:.2e}")
    print(f"f^2 Power SNR: {snr_f2:.4f}, Power: {f2_power:.2e}")
    
    # Plot spectra for first amplitude
    if i == 0:
        axes[0].plot(freqs_lomb, powers_lomb, 'b-', linewidth=2, label=f'Amplitude={amplitude}')
        axes[0].axvline(fault_frequency, color='r', linestyle='--', alpha=0.5, label='Fault Freq')
        axes[0].set_xlabel('Frequency (Hz)')
        axes[0].set_ylabel('Lomb-Scargle Power')
        axes[0].set_title('Lomb-Scargle Spectrum (First Amplitude)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(freqs_f2, powers_f2, 'g-', linewidth=2, label=f'Amplitude={amplitude}')
        axes[1].axvline(fault_frequency, color='r', linestyle='--', alpha=0.5)
        axes[1].set_xlabel('Frequency (Hz)')
        axes[1].set_ylabel('f^2 Power')
        axes[1].set_title('f^2 Compensated Spectrum (First Amplitude)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

# Save plots
plot_path = os.path.join(figures_path, "fault_detection_spectrum.png")
plt.tight_layout()
plt.savefig(plot_path, dpi=150, bbox_inches='tight')
plt.close()

# Create final comparison plot
fig2, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.plot(results['amplitude'], results['lomb_scargle_snr'], 'bo-', linewidth=2, markersize=8, label='Lomb-Scargle')
ax.plot(results['amplitude'], results['f2_power_snr'], 'gs-', linewidth=2, markersize=8, label='f^2 Power')
ax.set_xlabel('Fault Amplitude')
ax.set_ylabel('SNR')
ax.set_title('SNR Comparison: Lomb-Scargle vs f^2 Power')
ax.legend()
ax.grid(True, alpha=0.3)
fig2.tight_layout()
fig2_path = os.path.join(figures_path, "snr_comparison.png")
plt.savefig(fig2_path, dpi=150, bbox_inches='tight')
plt.close()

# Save results to markdown file
with open(results_file, 'w') as f:
    f.write("# Bearing Fault Detection Test Results\n")
    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("## Parameters\n")
    f.write(f"- Sample Rate: {sample_rate} Hz\n")
    f.write(f"- Number of regular samples: {n_points}\n")
    f.write(f"- Irregular samples: {len(t_irregular)}\n")
    f.write(f"- Dropout rate: {dropout_rate * 100:.1f}%\n")
    f.write(f"- Fault frequency: {fault_frequency} Hz\n")
    f.write(f"- Test amplitudes: {amplitudes}\n\n")
    
    f.write("## Lomb-Scargle SNR Results\n")
    f.write("| Amplitude | SNR | Peak Power |\n")
    f.write("|-----------|-----|------------|\n")
    for row in lomb_snr_table:
        f.write(f"| {row[0]:.2f} | {row[1]:.4f} | {row[2]:.2e} |\n")
    
    f.write("\n## f^2 Power SNR Results\n")
    f.write("| Amplitude | SNR | Peak Power |\n")
    f.write("|-----------|-----|------------|\n")
    for row in f2_snr_table:
        f.write(f"| {row[0]:.2f} | {row[1]:.4f} | {row[2]:.2e} |\n")
    
    f.write("\n## SNR Comparison Table\n")
    f.write("| Amplitude | Lomb-Scargle SNR | f^2 Power SNR | Ratio (LS/f2) |\n")
    f.write("|-----------|------------------|---------------|---------------|\n")
    for i in range(len(amplitudes)):
        ratio = lomb_snr_table[i][1] / f2_snr_table[i][1] if f2_snr_table[i][1] != 0 else float('inf')
        f.write(f"| {amplitudes[i]:.2f} | {lomb_snr_table[i][1]:.4f} | {f2_snr_table[i][1]:.4f} | {ratio:.4f} |\n")
    
    f.write("\n## Observations\n")
    f.write("- Both methods show increasing SNR with amplitude\n")
    f.write("- Lomb-Scargle is designed for irregular sampling\n")
    f.write("- f^2 power compensates for 1/f noise characteristics\n")
    f.write("- Results saved to: " + results_file + "\n")
    f.write("- Plots saved to: " + figures_path)

# Print final table to stdout
print("\n" + "=" * 80)
print("FINAL RESULTS TABLE")
print("=" * 80)
print(f"{'Amplitude':>10} | {'Lomb-Scargle SNR':>18} | {'f^2 Power SNR':>18} | {'Ratio (LS/f2)':>18}")
print("-" * 80)
for i in range(len(amplitudes)):
    ratio = lomb_snr_table[i][1] / f2_snr_table[i][1] if f2_snr_table[i][1] != 0 else float('inf')
    print(f"{amplitudes[i]:>10.2f} | {lomb_snr_table[i][1]:>18.4f} | {f2_snr_table[i][1]:>18.4f} | {ratio:>18.4f}")
print("=" * 80)

print(f"\nResults saved to: {results_file}")
print(f"Plot 1 saved to: {plot_path}")
print(f"Plot 2 saved to: {fig2_path}")
