#!/usr/bin/env python3
"""
Compute spectroscope with M(p)/sqrt(p) weighting for ALL primes up to 500K.
Compare filtered (M(p)<=-3) vs unfiltered to test whether filter or weight matters.
Also test accuracy across 20 zeros.
"""
import numpy as np
import time

print("="*70)
print("MERTENS SPECTROSCOPE: ALL PRIMES vs FILTERED")
print("="*70)

MAX_P = 500000
print(f"\nStep 1: Sieve Mobius function to {MAX_P}...")
t0 = time.time()

# Mobius sieve
mu = np.zeros(MAX_P + 1, dtype=np.int8)
mu[1] = 1
is_prime = np.ones(MAX_P + 1, dtype=bool)
is_prime[0] = is_prime[1] = False
primes_list = []

for i in range(2, MAX_P + 1):
    if is_prime[i]:
        primes_list.append(i)
        mu[i] = -1
        for j in range(2*i, MAX_P + 1, i):
            is_prime[j] = False
        # Mark multiples of i^2 as having mu=0
        i2 = i * i
        for j in range(i2, MAX_P + 1, i2):
            mu[j] = 0
    if mu[i] == 0:
        continue
    for p in primes_list:
        if i * p > MAX_P:
            break
        if i % p == 0:
            mu[i * p] = 0
            break
        mu[i * p] = -mu[i]

# Compute Mertens function M(n) = cumulative sum of mu
M = np.cumsum(mu)
print(f"  Sieve done in {time.time()-t0:.1f}s")

# Extract primes and their Mertens values
primes = np.array(primes_list, dtype=np.float64)
M_at_primes = M[primes_list].astype(np.float64)
N_all = len(primes)
print(f"  Total primes <= {MAX_P}: {N_all}")
print(f"  M(p) range: [{M_at_primes.min():.0f}, {M_at_primes.max():.0f}]")

# Filter: M(p) <= -3
mask_m3 = M_at_primes <= -3
primes_m3 = primes[mask_m3]
M_m3 = M_at_primes[mask_m3]
N_m3 = len(primes_m3)
print(f"  Primes with M(p)<=-3: {N_m3} ({N_m3/N_all*100:.1f}%)")

# Known zeta zeros (first 20)
ZEROS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
         37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
         52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
         67.0798, 69.5464, 72.0672, 75.7047, 77.1448]

# Spectroscope computation
gammas = np.linspace(5, 85, 25000)

def spectroscope(weights, p_vals):
    """F(gamma) = |sum w_j/sqrt(p_j) * exp(-i*gamma*log(p_j))|^2"""
    sqrt_p = np.sqrt(p_vals)
    log_p = np.log(p_vals)
    amp = weights / sqrt_p
    
    # Chunk to avoid memory issues
    G = len(gammas)
    N = len(p_vals)
    chunk = 5000
    F = np.zeros(G)
    for start in range(0, G, chunk):
        end = min(start + chunk, G)
        phases = np.outer(gammas[start:end], log_p)
        re = np.cos(phases) @ amp
        im = np.sin(phases) @ amp
        F[start:end] = re**2 + im**2
    return F

def analyze_zeros(F, label, zeros=ZEROS):
    """Find peaks near each known zero, report accuracy."""
    mean_F, std_F = np.mean(F), np.std(F)
    results = []
    for gz in zeros:
        mask = (gammas >= gz - 1.2) & (gammas <= gz + 1.2)
        if not mask.any():
            results.append((gz, np.nan, np.nan, np.nan))
            continue
        idx = np.argmax(F[mask])
        peak = gammas[np.where(mask)[0][idx]]
        height = F[np.where(mask)[0][idx]]
        z = (height - mean_F) / std_F if std_F > 0 else 0
        err = abs(peak - gz) / gz * 100
        results.append((gz, peak, err, z))
    
    print(f"\n  {label} ({len([r for r in results if not np.isnan(r[2])])} zeros analyzed):")
    print(f"  {'zero':>8s} {'peak':>8s} {'err%':>8s} {'z-score':>8s}")
    for gz, peak, err, z in results:
        if np.isnan(err):
            print(f"  {gz:8.3f}     N/A      N/A      N/A")
        else:
            print(f"  {gz:8.3f} {peak:8.3f} {err:8.3f} {z:8.1f}")
    
    valid = [r for r in results if not np.isnan(r[2])]
    if valid:
        avg_err = np.mean([r[2] for r in valid])
        avg_z = np.mean([r[3] for r in valid])
        n_detected = sum(1 for r in valid if r[3] > 2)
        print(f"  Average error: {avg_err:.3f}%")
        print(f"  Average z-score: {avg_z:.2f}")
        print(f"  Zeros with z>2: {n_detected}/{len(valid)}")
    return results

# ============================================================
print("\n" + "="*70)
print("TEST A: M(p)/sqrt(p) on ALL primes (no filter)")
print("="*70)
t0 = time.time()
w_all = M_at_primes / np.sqrt(primes)
F_all = spectroscope(w_all, primes)
print(f"  Computed in {time.time()-t0:.1f}s")
r_all = analyze_zeros(F_all, f"M/sqrt(p), ALL {N_all} primes")

# ============================================================
print("\n" + "="*70)
print("TEST B: M(p)/sqrt(p) on FILTERED primes (M<=-3 only)")
print("="*70)
t0 = time.time()
w_m3 = M_m3 / np.sqrt(primes_m3)
F_m3 = spectroscope(w_m3, primes_m3)
print(f"  Computed in {time.time()-t0:.1f}s")
r_m3 = analyze_zeros(F_m3, f"M/sqrt(p), FILTERED {N_m3} primes")

# ============================================================
print("\n" + "="*70)
print("TEST C: Unit weight on ALL primes")
print("="*70)
t0 = time.time()
F_unit_all = spectroscope(np.ones(N_all), primes)
print(f"  Computed in {time.time()-t0:.1f}s")
r_unit_all = analyze_zeros(F_unit_all, f"Unit weight, ALL {N_all} primes")

# ============================================================
print("\n" + "="*70)
print("TEST D: Unit weight on FILTERED primes")
print("="*70)
t0 = time.time()
F_unit_m3 = spectroscope(np.ones(N_m3), primes_m3)
print(f"  Computed in {time.time()-t0:.1f}s")
r_unit_m3 = analyze_zeros(F_unit_m3, f"Unit weight, FILTERED {N_m3} primes")

# ============================================================
print("\n" + "="*70)
print("TEST E: M(p)/sqrt(p) on WRONG-SIGN primes (M(p) > 0)")
print("="*70)
mask_pos = M_at_primes > 0
primes_pos = primes[mask_pos]
M_pos = M_at_primes[mask_pos]
N_pos = len(primes_pos)
print(f"  Primes with M(p)>0: {N_pos}")
if N_pos > 100:
    t0 = time.time()
    w_pos = M_pos / np.sqrt(primes_pos)
    F_pos = spectroscope(w_pos, primes_pos)
    print(f"  Computed in {time.time()-t0:.1f}s")
    r_pos = analyze_zeros(F_pos, f"M/sqrt(p), WRONG-SIGN {N_pos} primes")

# ============================================================
print("\n" + "="*70)
print("SUMMARY: Filter vs Weight comparison (first 5 zeros)")
print("="*70)

def avg_metrics(results, n=5):
    valid = [r for r in results[:n] if not np.isnan(r[2])]
    return np.mean([r[2] for r in valid]), np.mean([r[3] for r in valid])

configs = [
    ("M/sqrt(p), ALL primes", r_all),
    ("M/sqrt(p), filtered M<=-3", r_m3),
    ("Unit, ALL primes", r_unit_all),
    ("Unit, filtered M<=-3", r_unit_m3),
]

print(f"\n  First 5 zeros:")
print(f"  {'Config':35s} {'Avg err%':>10s} {'Avg z':>8s}")
for label, res in configs:
    e, z = avg_metrics(res, 5)
    print(f"  {label:35s} {e:10.3f} {z:8.2f}")

print(f"\n  First 10 zeros:")
print(f"  {'Config':35s} {'Avg err%':>10s} {'Avg z':>8s}")
for label, res in configs:
    e, z = avg_metrics(res, 10)
    print(f"  {label:35s} {e:10.3f} {z:8.2f}")

print(f"\n  All 20 zeros:")
print(f"  {'Config':35s} {'Avg err%':>10s} {'Avg z':>8s}")
for label, res in configs:
    e, z = avg_metrics(res, 20)
    print(f"  {label:35s} {e:10.3f} {z:8.2f}")

print("\nDone!")
