import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def load_zeros(n_zeros=30):
    """Load first n_zeros zeros of Riemann zeta function."""
    zeros_30 = [
        14.13472514202492,
        21.02203963877154,
        25.01085758014569,
        30.42487612585951,
        32.9350615877304,
        37.58617815882215,
        40.9187190121472,
        43.3270732807647,
        48.005150881051,
        49.773832478291,
        52.970321478539,
        53.420212690437,
        56.446228750734,
        59.347044395184,
        59.404175113664,
        62.938412654054,
        65.322999667962,
        67.44804097824,
        69.89667400865,
        71.419169747333,
        73.83269845449,
        74.86572456813,
        77.60547041807,
        77.94823140674,
        80.21735334659,
        83.96501660691,
        84.98566266676,
        88.00769467023,
        88.56046359021,
        89.4235405913,
    ]
    return zeros_30[:n_zeros]

def compute_pair_correlations(gammas):
    """Compute all pairwise differences and normalized alphas."""
    n = len(gammas)
    alpha_values = []
    gamma_mean = np.mean(gammas)
    for i in range(n):
        for j in range(i+1, n):
            diff = gammas[j] - gammas[i]
            alpha = diff * np.log(gamma_mean) / (2 * np.pi)
            alpha_values.append(alpha)
    return np.array(alpha_values)

def montgomery_formula(alpha):
    """Compute Montgomery's pair correlation formula: 1 - (sin(pi*alpha)/(pi*alpha))^2"""
    result = np.ones_like(alpha)
    nonzero = np.abs(alpha) > 1e-10
    result[nonzero] = 1 - (np.sin(np.pi * alpha[nonzero]) / (np.pi * alpha[nonzero]))**2
    return result

def wigner_surmise(s):
    """Compute Wigner surmise for nearest neighbor spacing: pi*s/2 * exp(-pi*s^2/4)"""
    return (np.pi / 2) * s * np.exp(-np.pi / 4 * s**2)

def compute_rmse(alpha_values, montgomery_values, alpha_range=(0, 4)):
    """Compute RMSE in specified alpha range."""
    mask = (alpha_values >= alpha_range[0]) & (alpha_values <= alpha_range[1])
    if np.sum(mask) == 0:
        return np.nan
    rmse = np.sqrt(np.mean((alpha_values[mask] - montgomery_values[mask])**2))
    return rmse

def compute_nn_spacing(gammas):
    """Compute nearest neighbor spacings."""
    diff = np.diff(gammas)
    mean_diff = np.mean(diff)
    nn_normalized = diff / mean_diff
    return nn_normalized, mean_diff

def plot_results(alpha_values_30, alpha_values_20, montgomery_30, montgomery_20, results):
    """Create visualization of results."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.hist(alpha_values_30[alpha_values_30 >= 0], bins=50, density=True, alpha=0.6, label='30 zeros')
    ax1.hist(alpha_values_20[alpha_values_20 >= 0], bins=50, density=True, alpha=0.6, label='20 zeros')
    x = np.linspace(-2, 6, 1000)
    ax1.plot(x, montgomery_formula(x), 'r-', linewidth=2, label='Montgomery')
    ax1.set_xlabel('Alpha (normalized spacing)')
    ax1.set_ylabel('Normalized frequency')
    ax1.set_title('Pair Correlation: Data vs Montgomery')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    gammas_30 = np.array(load_zeros(30))
    nn_30 = compute_nn_spacing(gammas_30)[0]
    ax2.hist(nn_30[nn_30 >= 0], bins=50, density=True, alpha=0.6, label='30 zeros')
    y = np.linspace(0, 1, 100)
    ax2.plot(y, wigner_surmise(y), 'r-', linewidth=2, label='Wigner')
    ax2.set_xlabel('Normalized spacing')
    ax2.set_ylabel('Normalized frequency')
    ax2.set_title('Nearest Neighbor Spacing')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pair_correlation_analysis.png', dpi=150)
    plt.close()
    print("Visualization saved as: pair_correlation_analysis.png")

def run_analysis():
    """Run the complete analysis."""
    print("Loading zeta zeros data...")
    zeros_30_full = load_zeros(30)
    zeros_30 = np.array(zeros_30_full)
    zeros_20 = zeros_30[:20]
    print("Loaded", len(zeros_30), "zeros (first", len(zeros_30), "Riemann zeta zeros)")
    print("First zero: gamma_1 =", zeros_30[0], "Last zero: gamma_", len(zeros_30), "=", zeros_30[-1])
    print("Mean gamma:", np.mean(zeros_30))
    
    results = {}
    
    for n in [20, 30]:
        print("\nProcessing", n, "zeros (", n*(n-1)//2, "pairs)...")
        gammas = zeros_30[:n]
        print("Computing pairwise differences...")
        alpha_values = compute_pair_correlations(gammas)
        gamma_mean = np.mean(gammas)
        print("Computing Montgomery formula...")
        montgomery_values = montgomery_formula(alpha_values)
        print("Computing RMSE in range [0, 4]...")
        rmse = compute_rmse(alpha_values, montgomery_values)
        print("Computing nearest neighbor spacing...")
        nn_spacing, mean_nn = compute_nn_spacing(gammas)
        
        results[n] = {
            'pairs': n*(n-1)//2,
            'rmse': rmse,
            'gamma_mean': gamma_mean,
            'nn_spacing_mean': mean_nn,
            'alpha_values': alpha_values,
            'montgomery_values': montgomery_values,
            'nn_spacing': nn_spacing
        }
        print("  Found", len(alpha_values), "normalized alpha values")
        print("  RMSE (alpha in [0,4]):", rmse)
    
    print("\n" + "="*60)
    print("PAIR CORRELATION ANALYSIS OF RIEMANN ZETA ZEROS")
    print("="*60)
    
    for n, data in results.items():
        print("\nResults with", n, "zeros (", data['pairs'], "pairs):")
        print("  RMSE (alpha in [0,4]):", data['rmse'])
        print("  Mean gamma:", data['gamma_mean'])
        print("  Mean nearest neighbor spacing:", data['nn_spacing_mean'])
    
    rmse_20 = results[20]['rmse']
    rmse_30 = results[30]['rmse']
    
    print("\n" + "="*60)
    print("COMPARISON: Does more data improve Montgomery match?")
    print("="*60)
    print("RMSE with 20 zeros (", results[20]['pairs'], "pairs):", rmse_20)
    print("RMSE with 30 zeros (", results[30]['pairs'], "pairs):", rmse_30)
    print("Difference (30 - 20):", rmse_30 - rmse_20)
    
    if rmse_30 < rmse_20:
        print("\nMORE DATA IMPROVES the match to Montgomery conjecture")
        print("As predicted by random matrix theory (GUE statistics)")
    elif rmse_30 > rmse_20:
        print("\nMORE DATA WORSENS the match to Montgomery conjecture")
        print("May indicate statistical fluctuations with small samples")
    else:
        print("\nNO CHANGE in match quality with more data")
        print("Results may be consistent with conjecture")
    
    try:
        plot_results(results[30]['alpha_values'], results[20]['alpha_values'],
                    results[30]['montgomery_values'], results[20]['montgomery_values'], results)
    except Exception as e:
        print("Note: Could not save visualization:", str(e))
    
    return results

if __name__ == "__main__":
    results = run_analysis()
    print("\nAnalysis complete!")
