#!/usr/bin/env python3
"""
Network Anomaly Detection Test: f^2 Spectral Compensation vs Lomb-Scargle
Tests detection of periodic botnet callback patterns in simulated network traffic.
"""

import numpy as np
from scipy.signal import lombscargle
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configuration
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Parameters
BACKGROUND_PACKETS = 10000
BACKGROUND_MEAN_INTERARRIVAL = 0.1  # seconds
BOTS_PERIODIC_PACKETS = 50
BOTS_PERIOD = 30  # seconds (f = 1/30 ≈ 0.033 Hz)
DDOS_PACKETS_PER_BURST = 20
DDOS_PERIOD = 5  # seconds (f = 1/5 = 0.2 Hz)
DDOS_DURATION = 100  # seconds

# Directories
EXPERIMENT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")
FIGURES_DIR = os.path.expanduser("~/Desktop/Farey-Local/figures")
os.makedirs(EXPERIMENT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

def generate_timestamps_with_jitter(jitter_std=0):
    """Generate simulated network timestamps with background, botnet, and DDoS signals."""
    timestamps = []
    
    # Background: Poisson process with mean 0.1s inter-arrival
    background_times = []
    current_time = 0
    for _ in range(BACKGROUND_PACKETS):
        current_time += np.random.exponential(BACKGROUND_MEAN_INTERARRIVAL)
        background_times.append(current_time)
    timestamps.extend(background_times)
    
    # Botnet C2: 50 periodic packets every 30 seconds with jitter
    botnet_times = []
    for i in range(BOTS_PERIODIC_PACKETS):
        base_time = i * BOTS_PERIOD
        jitter = np.random.normal(0, jitter_std)
        botnet_times.append(base_time + jitter)
    timestamps.extend(botnet_times)
    
    # DDoS pulse: burst of 20 packets every 5 seconds for 100 seconds
    ddos_times = []
    for burst_start in np.arange(0, DDOS_DURATION, DDOS_PERIOD):
        for _ in range(DDOS_PACKETS_PER_BURST):
            pulse_time = burst_start + np.random.uniform(0, DDOS_PERIOD / DDOS_PACKETS_PER_BURST)
            ddos_times.append(pulse_time)
    timestamps.extend(ddos_times)
    
    return np.array(sorted(timestamps))

def compute_lombscargle_power(timestamps, frequency):
    """Compute Lomb-Scargle periodogram at a specific frequency."""
    n = len(timestamps)
    if n < 2:
        return 0
    t = timestamps - timestamps.min()
    try:
        return lombscargle(t, np.ones(n), 2 * np.pi * frequency, normalization='psd')
    except:
        return 0

def compute_f2_compensated_power(timestamps, frequency):
    """
    Compute f^2 compensated periodogram.
    power = (2*pi*f)^2 * |sum exp(-2*pi*i*f*t)|^2
    """
    t = timestamps - timestamps.min()
    n = len(timestamps)
    omega = 2 * np.pi * frequency
    
    if omega == 0:
        return 0
    
    # Sum of complex exponentials
    sum_exp = np.sum(np.exp(-1j * omega * t))
    
    # Power with f^2 compensation
    power = (omega ** 2) * np.abs(sum_exp) ** 2
    
    return power

def compute_snr(power_spectrum, freq_array, signal_freq, noise_floor_window=0.01):
    """
    Compute Signal-to-Noise Ratio for detecting a frequency peak.
    """
    idx = np.argmin(np.abs(freq_array - signal_freq))
    signal_power = power_spectrum[idx]
    
    # Estimate noise floor from surrounding frequencies (excluding peak region)
    peak_width = 5
    start_idx = max(0, idx - peak_width)
    end_idx = min(len(power_spectrum) - 1, idx + peak_width)
    
    noise_indices = np.concatenate([np.arange(start_idx), np.arange(end_idx, len(power_spectrum))])
    noise_floor = np.median(power_spectrum[noise_indices])
    
    if noise_floor > 0:
        snr = 10 * np.log10(signal_power / noise_floor)
    else:
        snr = float('inf')
    
    return snr, signal_power, noise_floor

def run_detection_test(jitter_std=0):
    """Run detection test for a given jitter level."""
    timestamps = generate_timestamps_with_jitter(jitter_std)
    
    # Frequency range to test
    freq_min = 0.01
    freq_max = 0.3
    n_freqs = 500
    freq_array = np.linspace(freq_min, freq_max, n_freqs)
    
    # Compute periodograms for all frequencies
    ls_power = np.zeros(n_freqs)
    f2_power = np.zeros(n_freqs)
    
    for i, freq in enumerate(freq_array):
        ls_power[i] = compute_lombscargle_power(timestamps, freq)
        f2_power[i] = compute_f2_compensated_power(timestamps, freq)
    
    # Botnet signal (0.033 Hz) and DDoS signal (0.2 Hz)
    botnet_freq = 1.0 / BOTS_PERIOD  # ~0.033 Hz
    ddos_freq = 1.0 / DDOS_PERIOD  # 0.2 Hz
    
    # Compute SNRs
    botnet_ls_snr, botnet_ls_signal, botnet_ls_noise = compute_snr(ls_power, freq_array, botnet_freq)
    botnet_f2_snr, botnet_f2_signal, botnet_f2_noise = compute_snr(f2_power, freq_array, botnet_freq)
    
    ddos_ls_snr, ddos_ls_signal, ddos_ls_noise = compute_snr(ls_power, freq_array, ddos_freq)
    ddos_f2_snr, ddos_f2_signal, ddos_f2_noise = compute_snr(f2_power, freq_array, ddos_freq)
    
    return {
        'jitter_std': jitter_std,
        'timestamps': timestamps,
        'freq_array': freq_array,
        'ls_power': ls_power,
        'f2_power': f2_power,
        'botnet': {'ls_snr': botnet_ls_snr, 'f2_snr': botnet_f2_snr},
        'ddos': {'ls_snr': ddos_ls_snr, 'f2_snr': ddos_f2_snr}
    }

def print_results_table(results_list):
    """Print results table to stdout and prepare markdown content."""
    print("\n" + "=" * 80)
    print("NETWORK ANOMALY DETECTION: f^2 Spectral Compensation vs Lomb-Scargle")
    print("=" * 80)
    print(f"Simulation: {BACKGROUND_PACKETS} background, {BOTS_PERIODIC_PACKETS} botnet, {DDOS_PACKETS_PER_BURST} DDoS per burst")
    print(f"Botnet frequency: {1/BOTS_PERIOD:.3f} Hz (period: {BOTS_PERIOD}s)")
    print(f"DDoS frequency: {1/DDOS_PERIOD} Hz (period: {DDOS_PERIOD}s, duration: {DDOS_DURATION}s)")
    print("=" * 80)
    
    print(f"\n{'Jitter (s)':<12} {'Method':<12} {'Botnet SNR (dB)':<18} {'DDoS SNR (dB)':<18}")
    print("-" * 60)
    
    for res in results_list:
        botnet_snr = res['botnet']['ls_snr']
        f2_snr = res['botnet']['f2_snr']
        ddos_ls = res['ddos']['ls_snr']
        ddos_f2 = res['ddos']['f2_snr']
        
        print(f"{res['jitter_std']:<12} {'LS':<12} {botnet_snr:<18.2f} {ddos_ls:<18.2f}")
        print(f"{res['jitter_std']:<12} {'f^2 Comp':<12} {f2_snr:<18.2f} {ddos_f2:<18.2f}")

def save_results_markdown(results_list, experiment_dir):
    """Save results to markdown file."""
    md_path = os.path.join(experiment_dir, "NETWORK_ANOMALY_TEST.md")
    
    with open(md_path, 'w') as f:
        f.write("# Network Anomaly Detection: f^2 Spectral Compensation vs Lomb-Scargle\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Simulation Parameters:**\n")
        f.write(f"- Background packets: {BACKGROUND_PACKETS} (Poisson, mean {BACKGROUND_MEAN_INTERARRIVAL}s inter-arrival)\n")
        f.write(f"- Botnet C2: {BOTS_PERIODIC_PACKETS} packets every {BOTS_PERIOD}s (f = {1/BOTS_PERIOD:.3f} Hz)\n")
        f.write(f"- DDoS pulses: {DDOS_PACKETS_PER_BURST} packets every {DDOS_PERIOD}s for {DDOS_DURATION}s (f = {1/DDOS_PERIOD} Hz)\n\n")
        
        f.write("## Results Table\n\n")
        f.write("| Jitter (s) | Method | Botnet SNR (dB) | DDoS SNR (dB) |\n")
        f.write("|-----------|--------|----------------|---------------|\n")
        
        for res in results_list:
            botnet_ls = res['botnet']['ls_snr']
            f2_ls = res['botnet']['f2_snr']
            ddos_ls = res['ddos']['ls_snr']
            ddos_f2 = res['ddos']['f2_snr']
            
            f.write(f"| {res['jitter_std']:<10} | LS     | {botnet_ls:<18.2f} | {ddos_ls:<18.2f} |\n")
            f.write(f"| {res['jitter_std']:<10} | f^2 Comp| {f2_ls:<18.2f} | {ddos_f2:<18.2f} |\n")
        
        f.write("\n## Conclusion\n\n")
        
        # Analyze best method per jitter level
        for res in results_list:
            botnet_ls = res['botnet']['ls_snr']
            botnet_f2 = res['botnet']['f2_snr']
            
            if botnet_f2 > botnet_ls:
                f.write(f"**Jitter = {res['jitter_std']}s:** f^2 compensation performs better for botnet detection. ")
                f.write(f"SNR improvement: {botnet_f2 - botnet_ls:.2f} dB\n\n")
            else:
                f.write(f"**Jitter = {res['jitter_std']}s:** Lomb-Scargle performs better for botnet detection. ")
                f.write(f"SNR improvement: {botnet_ls - botnet_f2:.2f} dB\n\n")

def plot_periodograms(results_list, figures_dir):
    """Generate comparison plots."""
    plt.figure(figsize=(14, 6))
    
    # Select results with no jitter for main comparison
    no_jitter_res = results_list[0]
    
    plt.subplot(1, 2, 1)
    plt.plot(no_jitter_res['freq_array'], no_jitter_res['ls_power'], 'b-', label='Lomb-Scargle', linewidth=2)
    plt.plot(no_jitter_res['freq_array'], no_jitter_res['f2_power'], 'r--', label='f^2 Compensation', linewidth=2)
    plt.axvline(1/BOTS_PERIOD, color='gray', linestyle=':', label='Botnet freq')
    plt.axvline(1/DDOS_PERIOD, color='orange', linestyle=':', label='DDoS freq')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.title('Periodogram Comparison (No Jitter)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Zoom in on botnet region
    plt.subplot(1, 2, 2)
    plt.plot(no_jitter_res['freq_array'], no_jitter_res['ls_power'], 'b-', label='Lomb-Scargle', linewidth=2)
    plt.plot(no_jitter_res['freq_array'], no_jitter_res['f2_power'], 'r--', label='f^2 Compensation', linewidth=2)
    plt.xlim(0.01, 0.1)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power (dB)')
    plt.title('Botnet Region Zoom')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(figures_dir, "periodogram_comparison.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # Jitter sensitivity plot
    plt.figure(figsize=(10, 6))
    jitters = [res['jitter_std'] for res in results_list]
    botnet_ls_snr = [res['botnet']['ls_snr'] for res in results_list]
    botnet_f2_snr = [res['botnet']['f2_snr'] for res in results_list]
    
    plt.plot(jitters, botnet_ls_snr, 'bo-', label='Lomb-Scargle', markersize=10)
    plt.plot(jitters, botnet_f2_snr, 'rs--', label='f^2 Compensation', markersize=10)
    plt.xlabel('Jitter Standard Deviation (seconds)')
    plt.ylabel('Botnet Detection SNR (dB)')
    plt.title('Jitter Sensitivity Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    jitter_plot_path = os.path.join(figures_dir, "jitter_sensitivity.png")
    plt.savefig(jitter_plot_path, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    """Main execution function."""
    print("Starting Network Anomaly Detection Test...")
    print(f"Output directory: {EXPERIMENT_DIR}")
    
    # Run tests with different jitter levels
    jitter_levels = [0, 1, 3, 5]
    results_list = []
    
    for jitter_std in jitter_levels:
        print(f"\nRunning test with jitter_std={jitter_std}s...")
        result = run_detection_test(jitter_std)
        results_list.append(result)
        print(f"  Botnet detection: LS SNR = {result['botnet']['ls_snr']:.2f} dB, f^2 SNR = {result['botnet']['f2_snr']:.2f} dB")
        print(f"  DDoS detection: LS SNR = {result['ddos']['ls_snr']:.2f} dB, f^2 SNR = {result['ddos']['f2_snr']:.2f} dB")
    
    # Print results table
    print_results_table(results_list)
    
    # Save to markdown
    save_results_markdown(results_list, EXPERIMENT_DIR)
    print(f"\nResults saved to: {os.path.join(EXPERIMENT_DIR, 'NETWORK_ANOMALY_TEST.md')}")
    
    # Generate plots
    plot_periodograms(results_list, FIGURES_DIR)
    print(f"Figures saved to: {FIGURES_DIR}")
    
    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
