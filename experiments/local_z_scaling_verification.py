#!/usr/bin/env python3
"""
Verify that LOCAL z-scores improve monotonically with N.
Scale to 10M and 50M primes.
Test at ALL 20 zeros, not just gamma_1.
"""
import numpy as np, time, sys

ZEROS = [14.1347,21.0220,25.0109,30.4249,32.9351,
         37.5862,40.9187,43.3271,48.0052,49.7738,
         52.9703,56.4462,59.3470,60.8318,65.1125,
         67.0798,69.5464,72.0672,75.7047,77.1448]

gammas = np.linspace(5, 85, 25000)

def sieve_mertens(MAX_N):
    t0 = time.time()
    mu = np.zeros(MAX_N+1, dtype=np.int8); mu[1] = 1
    is_p = np.ones(MAX_N+1, dtype=bool); is_p[0]=is_p[1]=False
    pl = []
    for i in range(2, MAX_N+1):
        if is_p[i]: pl.append(i); mu[i] = -1
        for p in pl:
            if i*p > MAX_N: break
            is_p[i*p] = False
            if i%p == 0: mu[i*p] = 0; break
            mu[i*p] = -mu[i]
    M = np.cumsum(mu)
    primes = np.array(pl, dtype=np.float64)
    M_p = M[pl].astype(np.float64)
    print(f"  Sieved to {MAX_N:,}: {len(primes):,} primes in {time.time()-t0:.1f}s")
    return primes, M_p

def compute_spectroscope(primes, M_p, gammas):
    amp = M_p / primes  # M(p)/p
    log_p = np.log(primes)
    G = len(gammas)
    F = np.zeros(G)
    chunk = 2000
    for s in range(0, G, chunk):
        e = min(s+chunk, G)
        ph = np.outer(gammas[s:e], log_p)
        re = np.cos(ph) @ amp
        im = np.sin(ph) @ amp
        F[s:e] = re**2 + im**2
    return F * gammas**2  # matched filter

def local_z(F, gammas, gz, local_window=8.0, excl_window=1.5):
    """Local z-score: compare peak to background within +-local_window, excluding +-excl_window around ALL known zeros."""
    # Find peak near gz
    peak_mask = (gammas >= gz - 1.2) & (gammas <= gz + 1.2)
    if not peak_mask.any(): return np.nan, np.nan, np.nan
    idx = np.argmax(F[peak_mask])
    peak_g = gammas[np.where(peak_mask)[0][idx]]
    peak_h = F[np.where(peak_mask)[0][idx]]
    err = abs(peak_g - gz) / gz * 100
    
    # Local background: within +-local_window of gz, excluding all known zero windows
    bg_mask = (gammas >= gz - local_window) & (gammas <= gz + local_window)
    for z in ZEROS:
        bg_mask &= ~((gammas >= z - excl_window) & (gammas <= z + excl_window))
    
    if bg_mask.sum() < 20: return peak_h, err, np.nan
    bg_mean = np.mean(F[bg_mask])
    bg_std = np.std(F[bg_mask])
    lz = (peak_h - bg_mean) / bg_std if bg_std > 0 else 0
    return peak_h, err, lz

# Test sizes
sizes = [100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]

print("="*90)
print("LOCAL Z-SCORE SCALING VERIFICATION")
print("="*90)

all_results = {}

for MAX_N in sizes:
    print(f"\n{'='*70}")
    print(f"N_max = {MAX_N:,}")
    print(f"{'='*70}")
    
    primes, M_p = sieve_mertens(MAX_N)
    N = len(primes)
    
    t0 = time.time()
    F = compute_spectroscope(primes, M_p, gammas)
    print(f"  Spectroscope computed in {time.time()-t0:.1f}s")
    
    # Global z for comparison
    mean_F, std_F = np.mean(F), np.std(F)
    
    results = []
    for gz in ZEROS:
        peak_h, err, lz = local_z(F, gammas, gz)
        # Global z
        peak_mask = (gammas >= gz-1.2) & (gammas <= gz+1.2)
        if peak_mask.any():
            idx = np.argmax(F[peak_mask])
            ph = F[np.where(peak_mask)[0][idx]]
            gz_score = (ph - mean_F)/std_F
        else:
            gz_score = np.nan
        results.append((gz, peak_h, err, lz, gz_score))
    
    all_results[MAX_N] = results
    
    print(f"\n  {'zero':>8s} {'peak_h':>10s} {'err%':>7s} {'local_z':>8s} {'global_z':>9s}")
    n_local_det = 0
    n_global_det = 0
    for gz, ph, err, lz, gz_s in results:
        ld = '*' if (not np.isnan(lz) and lz > 2) else ' '
        gd = '*' if (not np.isnan(gz_s) and gz_s > 2) else ' '
        if ld == '*': n_local_det += 1
        if gd == '*': n_global_det += 1
        lz_str = f"{lz:8.1f}" if not np.isnan(lz) else "     N/A"
        print(f"  {gz:8.3f} {ph:10.1f} {err:7.3f} {lz_str} {ld} {gz_s:9.1f} {gd}")
    
    print(f"\n  Detections (z>2): local={n_local_det}/20, global={n_global_det}/20")
    
    del F, primes, M_p
    sys.stdout.flush()

# Summary table
print(f"\n{'='*90}")
print(f"SCALING SUMMARY")
print(f"{'='*90}")
print(f"\n{'N_max':>10s} {'N_primes':>10s} {'global det':>11s} {'local det':>10s} {'avg local_z':>12s} {'avg err%':>9s}")
for MAX_N in sizes:
    res = all_results[MAX_N]
    valid_lz = [r[3] for r in res if not np.isnan(r[3])]
    valid_err = [r[2] for r in res if not np.isnan(r[2])]
    n_local = sum(1 for r in res if not np.isnan(r[3]) and r[3] > 2)
    n_global = sum(1 for r in res if not np.isnan(r[4]) and r[4] > 2)
    avg_lz = np.mean(valid_lz) if valid_lz else 0
    avg_err = np.mean(valid_err) if valid_err else 0
    N_p = len([1 for _ in range(MAX_N)])  # approx
    # Get actual N from results
    print(f"{MAX_N:10,} {'~':>10s} {n_global:11d} {n_local:10d} {avg_lz:12.2f} {avg_err:9.3f}")

print("\nDone!")
