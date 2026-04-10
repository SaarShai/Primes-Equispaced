import numpy as np
import json
import matplotlib.pyplot as plt
from collections import Counter

def load_orbit_data(filepath):
    """Load orbit data from JSON file with robust structure detection."""
    with open(filepath, 'r') as f:
        raw_data = json.load(f)
    
    # Inspect and navigate the structure
    if isinstance(raw_data, dict):
        for key in ['orbits', 'data', 'periods', 'result', 'orbits_data']:
            if key in raw_data and isinstance(raw_data[key], list):
                return raw_data[key], raw_data[key]
        # Return the dict itself if it's a single orbit
        return raw_data, raw_data
    elif isinstance(raw_data, list):
        return raw_data, raw_data
    else:
        raise ValueError(f"Unexpected data type: {type(raw_data)}")

def extract_periods(data):
    """Extract periods from orbit data with flexible key handling."""
    periods = []
    for d in data:
        if isinstance(d, dict):
            period = None
            for key in ['period', 'T', 'time_period', 'T_k', 'period_k']:
                if key in d:
                    period = d[key]
                    break
            if period is not None and isinstance(period, (int, float)):
                periods.append(period)
        elif isinstance(d, (int, float)):
            periods.append(d)
    
    return np.array(periods)

def compute_period_spectroscope(periods, weights=None):
    """Compute period spectroscopy F(omega) = |sum w_k * exp(-i*omega*log(T_k))|^2"""
    if len(periods) == 0:
        raise ValueError("No periods to analyze")
    
    if weights is None:
        weights = np.ones(len(periods))
    
    # Normalize weights
    weights = weights / np.sum(weights)
    
    log_periods = np.log(periods)
    
    # Determine frequency range
    omega_min = -20
    omega_max = 20
    omega = np.linspace(omega_min, omega_max, 4000)
    
    # Compute spectroscopy
    spectroscopy = np.zeros(len(omega), dtype=complex)
    for k, (T_k, w_k) in enumerate(zip(log_periods, weights)):
        spectroscopy += w_k * np.exp(-1j * omega * T_k)
    
    return omega, np.abs(spectroscopy)**2

def find_peaks(spectroscopy, threshold=0.7):
    """Find significant peaks in spectroscopy."""
    spec_norm = spectroscopy / np.max(spectroscopy)
    peak_threshold = np.max(spec_norm) * threshold
    peak_indices = np.where(spec_norm > peak_threshold)[0]
    
    peaks = []
    for i in peak_indices:
        if i > 0 and i < len(peak_indices) - 1:
            peak_val = spec_norm[i]
            if peak_val > spec_norm[max(0, i-5)] or peak_val > spec_norm[min(len(peak_indices)-1, i+5)]:
                peaks.append((i, peak_val))
    
    return peaks

def extract_cf_data(orbits):
    """Extract CF partial quotients from orbit data."""
    cf_values = []
    for d in orbits:
        if isinstance(d, dict):
            if 'cf' in d:
                cf_values.extend(d['cf'])
            elif 'continued_fraction' in d:
                cf_values.extend(d['continued_fraction'])
            elif 'braid' in d:
                # If braid word, might relate to CF
                pass
        elif isinstance(d, list):
            cf_values.extend(d)
    return cf_values

def main():
    filepath = '/Users/saar/Desktop/Farey-Local/experiments/threebody_full_data.json'
    
    print("Attempting to load data from " + filepath + "...")
    data, raw_data = load_orbit_data(filepath)
    
    periods = extract_periods(data)
    print(f"Loaded {len(periods)} periods from {len(data)} orbit entries.")
    
    if len(periods) == 0:
        print("ERROR: No periods found in data!")
        return
    
    print(f"Period range: [{periods.min():.4f}, {periods.max():.4f}]")
    
    # Compute spectroscopy with different weights
    weights_1_over_T = 1.0 / periods
    weights_uniform = np.ones(len(periods))
    
    print("\nComputing period spectroscopy...")
    omega, spec = compute_period_spectroscope(periods, weights=weights_1_over_T)
    spec_norm = spec / np.max(spec)
    peaks = find_peaks(spec_norm)
    
    print(f"\nFound {len(peaks)} significant peaks (threshold: 0.7)")
    for i, (idx, amp) in enumerate(peaks):
        print(f"  Peak {i+1}: frequency={omega[idx]:.4f}, amplitude={amp:.4f}")
    
    # Plot spectroscopy
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(omega, spec, label='w_k = 1/T', linewidth=1.5)
    ax.set_xlabel('Frequency (omega)')
    ax.set_ylabel('Spectroscopy Amplitude |F(ω)|²')
    ax.set_title('Period Spectroscopy: Three-Body Orbits')
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig('threebody_period_spectrogram.png', dpi=150)
    print("\nPlot saved to threebody_period_spectrogram.png")
    
    plt.close()
    
    # Analyze CF partial quotients
    print("\nAnalyzing CF partial quotients distribution...")
    cf_data = extract_cf_data(data)
    if len(cf_data) > 0:
        cf_counts = Counter(cf_data)
        print(f"\nMost common partial quotients: {cf_counts.most_common(10)}")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(cf_counts.keys(), cf_counts.values())
        ax.set_xlabel('Partial Quotient')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of CF Partial Quotients')
        plt.savefig('threebody_cf_distribution.png', dpi=150)
        print("Plot saved to threebody_cf_distribution.png")
        plt.show()
    else:
        print("No CF partial quotients found in data.")

if __name__ == '__main__':
    main()
