import numpy as np
from scipy import stats
from scipy.signal import find_peaks

# (1) Compute mu(n) for n=1 to N using linear sieve
N = 100000
mu_vals = np.zeros(N + 1, dtype=int)
mu_vals[1] = 1
primes = []
is_composite = np.zeros(N + 1, dtype=bool)

for i in range(2, N + 1):
    if not is_composite[i]:
        primes.append(i)
        mu_vals[i] = -1
    for p in primes:
        if i * p > N:
            break
        is_composite[i * p] = True
        if i % p == 0:
            mu_vals[i * p] = 0
            break
        else:
            mu_vals[i * p] = -mu_vals[i]

mu = mu_vals[1:]  # indices 1 to N

# (2) Compute spectroscope F(gamma)
gamma_min = 5
gamma_max = 80
num_points = 20000
gammas = np.linspace(gamma_min, gamma_max, num_points)

n_vals = np.arange(1, N + 1)
F = np.zeros(num_points, dtype=float)

for idx, gamma in enumerate(gammas):
    exp_term = np.exp(-1j * gamma * np.log(n_vals))
    S = np.sum(mu * exp_term / n_vals)
    F[idx] = np.abs(S)**2

# (3) Apply gamma^2 compensation (from explicit formula envelope ~ gamma^{-2})
F_compensated = F * gammas**2

# (4) Find peaks
peaks, _ = find_peaks(F_compensated, distance=50, height=np.max(F_compensated) * 0.3)

# (5) Pre-whiten: divide F by expected envelope (~gamma^{-2}), so multiply by gamma^2
F_whitened = F * gammas**2

# (6) Check flatness using chi-squared statistic
baseline = np.median(F_whitened)
F_normalized = F_whitened / baseline

chi2_stat, chi2_pvalue = stats.chisquare(F_whitened)

print("=" * 60)
print("Chowla Conjecture Spectroscope Test")
print("=" * 60)
print(f"Range: γ ∈ [{gamma_min}, {gamma_max}]")
print(f"Number of points: {num_points}")
print(f"Möbius values computed for n = 1 to {N}")
print(f"Number of peaks detected: {len(peaks)}")
if len(peaks) > 0:
    print(f"Peak γ values (first 10): {gammas[peaks[:10]]}")
print(f"Mean F (raw): {np.mean(F):.6f}")
print(f"Mean F_whitened: {np.mean(F_whitened):.6f}")
print(f"Std F_whitened: {np.std(F_whitened):.6f}")
print(f"Chi-squared statistic: {chi2_stat:.6f}")
print(f"Chi-squared p-value: {chi2_pvalue:.6f}")
print("=" * 60)

if chi2_pvalue > 0.05:
    print("✓ Residual appears FLAT - consistent with Chowla conjecture")
else:
    print("⚠ Residual shows structure - potential deviations from Chowla")

print("=" * 60)
