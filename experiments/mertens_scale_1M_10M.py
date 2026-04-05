#!/usr/bin/env python3
"""
Scale the Mertens spectroscope to 1M and 10M primes.
With gamma^2 matched filter.
"""
import numpy as np, time, sys

ZEROS = [14.1347,21.0220,25.0109,30.4249,32.9351,
         37.5862,40.9187,43.3271,48.0052,49.7738,
         52.9703,56.4462,59.3470,60.8318,65.1125,
         67.0798,69.5464,72.0672,75.7047,77.1448]

gammas = np.linspace(5, 85, 25000)

def sieve_mertens(MAX_N):
    """Sieve Mobius function and compute Mertens, return primes and M(p)."""
    t0 = time.time()
    # Bit-sieve for speed
    is_prime = np.ones(MAX_N + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    mu = np.zeros(MAX_N + 1, dtype=np.int8)
    mu[1] = 1
    
    for i in range(2, int(MAX_N**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, MAX_N + 1, i):
                is_prime[j] = False
            # mu sieve: mark i^2 multiples as 0
            for j in range(i*i, MAX_N + 1, i*i):
                mu[j] = 0
    
    # Linear sieve for mu
    primes_list = []
    mu2 = np.zeros(MAX_N + 1, dtype=np.int8)
    mu2[1] = 1
    is_prime2 = np.ones(MAX_N + 1, dtype=bool)
    is_prime2[0] = is_prime2[1] = False
    
    for i in range(2, MAX_N + 1):
        if is_prime2[i]:
            primes_list.append(i)
            mu2[i] = -1
        for p in primes_list:
            if i * p > MAX_N: break
            is_prime2[i * p] = False
            if i % p == 0:
                mu2[i * p] = 0
                break
            mu2[i * p] = -mu2[i]
    
    M = np.cumsum(mu2)
    primes = np.array(primes_list, dtype=np.float64)
    M_p = M[primes_list].astype(np.float64)
    elapsed = time.time() - t0
    print(f"  Sieved to {MAX_N}: {len(primes)} primes in {elapsed:.1f}s")
    return primes, M_p

def spectroscope_with_filter(primes, M_p, gammas, apply_gamma2=False):
    """Compute F(gamma) with M(p)/sqrt(p) weight on all primes."""
    sqrt_p = np.sqrt(primes)
    log_p = np.log(primes)
    amp = (M_p / sqrt_p) / sqrt_p  # effective: M(p)/p
    
    G = len(gammas)
    F = np.zeros(G)
    chunk = 3000
    for s in range(0, G, chunk):
        e = min(s + chunk, G)
        phases = np.outer(gammas[s:e], log_p)
        re = np.cos(phases) @ amp
        im = np.sin(phases) @ amp
        F[s:e] = re**2 + im**2
    
    if apply_gamma2:
        F = F * gammas**2
    return F

def analyze(F, gammas, label, zeros=ZEROS):
    mean_F, std_F = np.mean(F), np.std(F)
    print(f"\n  {label}:")
    print(f"  {'zero':>8s} {'peak':>8s} {'err%':>8s} {'z':>8s}")
    n_detected = 0
    for gz in zeros:
        mask = (gammas >= gz - 1.0) & (gammas <= gz + 1.0)
        if not mask.any(): continue
        idx = np.argmax(F[mask])
        peak = gammas[np.where(mask)[0][idx]]
        h = F[np.where(mask)[0][idx]]
        z = (h - mean_F) / std_F
        err = abs(peak - gz) / gz * 100
        det = "*" if z > 2 else " "
        print(f"  {gz:8.3f} {peak:8.3f} {err:8.3f} {z:8.1f} {det}")
        if z > 2: n_detected += 1
    print(f"  Zeros with z>2: {n_detected}/{len(zeros)}")
    return n_detected

# ============================================================
# Scale up
# ============================================================
for MAX_N in [1_000_000, 5_000_000, 10_000_000]:
    print(f"\n{'='*70}")
    print(f"MAX_N = {MAX_N:,}")
    print(f"{'='*70}")
    
    primes, M_p = sieve_mertens(MAX_N)
    N = len(primes)
    print(f"  N = {N:,} primes")
    
    t0 = time.time()
    F_raw = spectroscope_with_filter(primes, M_p, gammas, apply_gamma2=False)
    print(f"  Raw spectroscope computed in {time.time()-t0:.1f}s")
    n_raw = analyze(F_raw, gammas, f"Raw F(gamma), N={N:,}")
    
    t0 = time.time()
    F_matched = spectroscope_with_filter(primes, M_p, gammas, apply_gamma2=True)
    print(f"  Matched filter computed in {time.time()-t0:.1f}s")
    n_matched = analyze(F_matched, gammas, f"gamma^2 matched filter, N={N:,}")
    
    print(f"\n  SUMMARY: Raw detects {n_raw}/20, Matched detects {n_matched}/20")
    
    sys.stdout.flush()
    
    # Memory cleanup for large arrays
    del F_raw, F_matched, primes, M_p

print("\nDone!")
