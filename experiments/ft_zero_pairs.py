import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def compute_pair_spectrum(csv_path, gamma_range=(0, 25), gamma_step=0.01):
    """
    Computes F_pair(gamma) = |Sum_p B_plus_C(p) * p^(-1/2 - i*gamma)|^2
    and extracts peak locations to check for gamma_k - gamma_l differences.
    """
    try:
        df = pd.read_csv(csv_path)
        if 'p' not in df.columns or 'B_plus_C' not in df.columns:
            raise ValueError("CSV must contain 'p' and 'B_plus_C' columns.")
    except FileNotFoundError:
        print(f"ERROR: File '{csv_path}' not found.")
        return None

    primes = df['p'].values
    weights = df['B_plus_C'].values
    
    # Filter valid primes and weights
    mask = (primes > 1) & (np.abs(weights) < 1e10) # Basic sanity check
    primes = primes[mask]
    weights = weights[mask]
    
    gammas = np.arange(gamma_range[0], gamma_range[1], gamma_step)
    spectrum = np.zeros_like(gammas, dtype=float)
    
    # Compute Dirichlet series sum for each gamma
    # Optimization: Vectorize where possible, but loop over gammas for stability
    log_primes = np.log(primes)
    p_inv_sqrt = primes**(-0.5)
    
    for i, g in enumerate(gammas):
        # Sum: sum( w * p^(-1/2) * exp(-i * g * log(p)) )
        phase = np.exp(-1j * g * log_primes)
        term = weights * p_inv_sqrt * phase
        spectrum[i] = np.abs(np.sum(term))**2
        
    return gammas, spectrum

def analyze_peaks(gammas, spectrum, targets=[3.99, 6.89, 10.88, 16.29], tol=0.5):
    """
    Finds peaks in spectrum, computes differences, matches against targets.
    """
    # Find peaks in the Power Spectrum (should be at gamma_k)
    peaks, _ = find_peaks(spectrum, height=np.max(spectrum)*0.1, distance=10)
    peak_gammas = gammas[peaks]
    
    print(f"Detected {len(peak_gammas)} peaks in Power Spectrum at gamma_k:")
    for g in peak_gammas:
        print(f"  Gamma_k ~ {g:.2f}")
        
    # Compute pairwise differences (gamma_k - gamma_l)
    diffs = []
    for i in range(len(peak_gammas)):
        for j in range(i + 1, len(peak_gammas)):
            diffs.append(abs(peak_gammas[i] - peak_gammas[j]))
            
    print(f"\nComputed pairwise differences (gamma_k - gamma_l):")
    matches = []
    for d in diffs:
        print(f"  Diff: {d:.2f}")
        for t in targets:
            if abs(d - t) < tol:
                matches.append((d, t))
                print(f"    -> MATCH: {d:.2f} vs Target {t}")
                
    return peak_gammas, diffs, matches

if __name__ == "__main__":
    # Run analysis
    result = compute_pair_spectrum('bc_verify_100000_c.csv')
    if result:
        gammas, spectrum = result
        analyze_peaks(gammas, spectrum)
    else:
        print("Script execution halted due to missing data file.")
