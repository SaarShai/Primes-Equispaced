"""
MPR-20: Spectral analysis of ΔW sequence for zeta zero frequencies.
If ΔW oscillates at frequencies matching imaginary parts of zeta zeros
(14.134725..., 21.022040..., 25.010858..., 30.424876..., 32.935062...),
that would be a genuinely novel RH connection.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, time, sys
from fractions import Fraction

print("="*70, flush=True)
print("SPECTRAL ANALYSIS OF ΔW AT ZETA ZERO FREQUENCIES", flush=True)
print("="*70, flush=True)

# Known zeta zeros (imaginary parts)
ZETA_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918719, 43.327073, 48.005151, 49.773832]

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

def mertens(n):
    """Compute M(n) = sum mu(k) for k=1..n"""
    mu = [0]*(n+1)
    mu[1] = 1
    for i in range(1, n+1):
        for j in range(2*i, n+1, i):
            mu[j] -= mu[i]
    return [sum(mu[:k+1]) for k in range(n+1)]

def farey_wasserstein(N):
    """Compute W_1 discrepancy for F_N"""
    # Generate F_N
    fracs = []
    for q in range(1, N+1):
        for p in range(0, q+1):
            if Fraction(p, q) == Fraction(p, q):  # always true, but ensures reduced
                f = Fraction(p, q)
                if 0 <= f <= 1:
                    fracs.append(f)
    fracs = sorted(set(fracs))
    n = len(fracs)
    if n <= 1: return 0.0
    # W_1 = sum |f_i - i/(n-1)| / n
    W = sum(abs(float(fracs[i]) - i/(n-1)) for i in range(n)) / n
    return W

# Compute ΔW for a range of N
print("\nPhase 1: Computing ΔW(N) for N = 2 to 2000...", flush=True)
t0 = time.time()

MAX_N = 2000
W_values = [0.0, 0.0]  # W(0), W(1) = 0

for N in range(2, MAX_N + 1):
    W = farey_wasserstein(N)
    W_values.append(W)
    if N % 200 == 0:
        print(f"  N={N}, W={W:.8f} ({time.time()-t0:.1f}s)", flush=True)

print(f"Phase 1 done ({time.time()-t0:.1f}s)", flush=True)

# Compute ΔW
DeltaW = [0.0, 0.0]
for N in range(2, MAX_N + 1):
    DeltaW.append(W_values[N] - W_values[N-1])

# Separate prime and composite ΔW
prime_N = []
prime_DW = []
composite_N = []
composite_DW = []
all_N = list(range(2, MAX_N + 1))
all_DW = [DeltaW[N] for N in all_N]

for N in range(2, MAX_N + 1):
    if is_prime(N):
        prime_N.append(N)
        prime_DW.append(DeltaW[N])
    else:
        composite_N.append(N)
        composite_DW.append(DeltaW[N])

print(f"\n{len(prime_N)} primes, {len(composite_N)} composites in range", flush=True)

# Phase 2: FFT of ΔW sequence
print("\nPhase 2: Spectral analysis...", flush=True)

# FFT of full ΔW sequence
dw_array = np.array(all_DW)
dw_centered = dw_array - np.mean(dw_array)
fft = np.fft.rfft(dw_centered)
power = np.abs(fft)**2
freqs = np.fft.rfftfreq(len(dw_centered), d=1.0)  # frequency in cycles per unit N

# Convert to "angular frequency" comparable to zeta zeros
# Zeta zeros have imaginary part t, corresponding to oscillation e^{it*log(p)}
# We need to check if ΔW(N) has peaks at frequencies related to t/(2π)

# Also do FFT of prime-only ΔW (irregularly sampled - use Lomb-Scargle)
print("  Computing Lomb-Scargle periodogram for prime-indexed ΔW...", flush=True)

# Simple Lomb-Scargle implementation
def lomb_scargle(t, y, freqs):
    """Compute Lomb-Scargle periodogram"""
    t = np.array(t, dtype=float)
    y = np.array(y, dtype=float)
    y = y - np.mean(y)
    power = np.zeros(len(freqs))
    for i, f in enumerate(freqs):
        omega = 2 * np.pi * f
        tau = np.arctan2(np.sum(np.sin(2*omega*t)), np.sum(np.cos(2*omega*t))) / (2*omega) if omega > 0 else 0
        cos_term = np.cos(omega * (t - tau))
        sin_term = np.sin(omega * (t - tau))
        power[i] = (np.sum(y * cos_term)**2 / np.sum(cos_term**2) +
                     np.sum(y * sin_term)**2 / np.sum(sin_term**2)) / 2
    return power

# Test frequencies: focus around zeta zeros
# The natural variable is log(N), not N, because primes are distributed as N/log(N)
# Transform: use log(p) as the "time" variable for prime ΔW
log_primes = np.log(np.array(prime_N, dtype=float))
prime_dw_array = np.array(prime_DW)

# Scan frequencies from 0 to 60 (covers first 10 zeta zeros)
test_freqs = np.linspace(0.1, 60, 3000)
ls_power = lomb_scargle(log_primes, prime_dw_array, test_freqs)

# Also weight by p² (since ΔW ~ 1/p²)
weighted_dw = prime_dw_array * np.array(prime_N, dtype=float)**2
ls_power_weighted = lomb_scargle(log_primes, weighted_dw, test_freqs)

print("  Done.", flush=True)

# Phase 3: Check for peaks at zeta zeros
print("\nPhase 3: Checking for peaks at zeta zero frequencies...", flush=True)
print(f"  {'Zeta zero':>12}  {'LS power':>12}  {'Weighted':>12}  {'Rank':>6}  {'Percentile':>10}", flush=True)
print(f"  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*6}  {'-'*10}", flush=True)

sorted_power = np.sort(ls_power)[::-1]
sorted_weighted = np.sort(ls_power_weighted)[::-1]

zeta_results = []
for tz in ZETA_ZEROS:
    idx = np.argmin(np.abs(test_freqs - tz))
    p = ls_power[idx]
    pw = ls_power_weighted[idx]
    rank = np.sum(ls_power >= p)
    rank_w = np.sum(ls_power_weighted >= pw)
    pctile = 100 * (1 - rank / len(ls_power))
    pctile_w = 100 * (1 - rank_w / len(ls_power_weighted))
    print(f"  {tz:12.6f}  {p:12.4f}  {pw:12.1f}  {rank:6d}  {pctile:9.1f}%", flush=True)
    zeta_results.append({
        'zero': tz, 'power': float(p), 'weighted_power': float(pw),
        'rank': int(rank), 'percentile': float(pctile),
        'rank_weighted': int(rank_w), 'percentile_weighted': float(pctile_w)
    })

# Check: are zeta zeros collectively special?
zeta_powers = [r['power'] for r in zeta_results]
random_powers = []
np.random.seed(42)
for _ in range(10000):
    random_freqs = np.random.uniform(0.1, 60, 10)
    random_p = [ls_power[np.argmin(np.abs(test_freqs - f))] for f in random_freqs]
    random_powers.append(np.mean(random_p))
mean_zeta = np.mean(zeta_powers)
p_value = np.mean([rp >= mean_zeta for rp in random_powers])
print(f"\n  Mean power at zeta zeros: {mean_zeta:.4f}", flush=True)
print(f"  Mean power at random freqs: {np.mean(random_powers):.4f}", flush=True)
print(f"  P-value (zeta zeros collectively special): {p_value:.4f}", flush=True)

# Same for weighted
zeta_pw = [r['weighted_power'] for r in zeta_results]
random_pw = []
for _ in range(10000):
    random_freqs = np.random.uniform(0.1, 60, 10)
    random_p = [ls_power_weighted[np.argmin(np.abs(test_freqs - f))] for f in random_freqs]
    random_pw.append(np.mean(random_p))
mean_zeta_w = np.mean(zeta_pw)
p_value_w = np.mean([rp >= mean_zeta_w for rp in random_pw])
print(f"  Weighted p-value: {p_value_w:.4f}", flush=True)

# Phase 4: Plots
print("\nPhase 4: Generating plots...", flush=True)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: ΔW sequence
ax = axes[0, 0]
ax.plot(prime_N, prime_DW, '.', markersize=1, alpha=0.5, label='Prime ΔW')
ax.plot(composite_N, composite_DW, '.', markersize=0.5, alpha=0.3, color='gray', label='Composite ΔW')
ax.set_xlabel('N')
ax.set_ylabel('ΔW(N)')
ax.set_title('ΔW(N) = W(N) - W(N-1)')
ax.legend(fontsize=8)

# Plot 2: Lomb-Scargle (unweighted)
ax = axes[0, 1]
ax.plot(test_freqs, ls_power, linewidth=0.5)
for tz in ZETA_ZEROS:
    ax.axvline(tz, color='red', alpha=0.5, linewidth=0.8, linestyle='--')
ax.set_xlabel('Frequency (in log-prime space)')
ax.set_ylabel('Lomb-Scargle Power')
ax.set_title('Spectral analysis of prime ΔW (red = zeta zeros)')

# Plot 3: Lomb-Scargle (weighted by p²)
ax = axes[1, 0]
ax.plot(test_freqs, ls_power_weighted, linewidth=0.5, color='green')
for tz in ZETA_ZEROS:
    ax.axvline(tz, color='red', alpha=0.5, linewidth=0.8, linestyle='--')
ax.set_xlabel('Frequency (in log-prime space)')
ax.set_ylabel('Weighted LS Power')
ax.set_title('Spectral analysis of p²·ΔW (red = zeta zeros)')

# Plot 4: Zoom around first zeta zero
ax = axes[1, 1]
mask = (test_freqs > 10) & (test_freqs < 20)
ax.plot(test_freqs[mask], ls_power_weighted[mask], linewidth=1, color='green')
ax.axvline(14.134725, color='red', linewidth=2, label=f'ζ zero = 14.135')
ax.set_xlabel('Frequency')
ax.set_ylabel('Weighted LS Power')
ax.set_title('Zoom: first zeta zero region')
ax.legend()

plt.tight_layout()
plt.savefig('/Users/saar/Desktop/Farey-Local/experiments/deltaw_spectral.png', dpi=150)
print("  Saved deltaw_spectral.png", flush=True)

# Save results
results = {
    'max_N': MAX_N,
    'n_primes': len(prime_N),
    'zeta_results': zeta_results,
    'collective_p_value': float(p_value),
    'collective_p_value_weighted': float(p_value_w),
    'mean_zeta_power': float(mean_zeta),
    'mean_random_power': float(np.mean(random_powers)),
}
with open('/Users/saar/Desktop/Farey-Local/experiments/deltaw_spectral_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Summary
print("\n" + "="*70, flush=True)
print("SUMMARY", flush=True)
print("="*70, flush=True)
if p_value < 0.05:
    print(f"*** SIGNIFICANT: Zeta zeros are special in ΔW spectrum (p={p_value:.4f}) ***", flush=True)
elif p_value < 0.10:
    print(f"* MARGINAL: Zeta zeros show weak signal (p={p_value:.4f}) *", flush=True)
else:
    print(f"NOT SIGNIFICANT: Zeta zeros not special in ΔW spectrum (p={p_value:.4f})", flush=True)

if p_value_w < 0.05:
    print(f"*** SIGNIFICANT (weighted): p={p_value_w:.4f} ***", flush=True)
elif p_value_w < 0.10:
    print(f"* MARGINAL (weighted): p={p_value_w:.4f} *", flush=True)
else:
    print(f"NOT SIGNIFICANT (weighted): p={p_value_w:.4f}", flush=True)

print("\nDone!", flush=True)
