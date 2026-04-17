#!/usr/bin/env python3
"""Verify: does the Goldbach residual spectroscope detect zeta zeros?"""
import numpy as np
import time

print("# Goldbach Spectroscope — Computational Verification")
print(f"# Date: 2026-04-12")
print()

# Step 1: Sieve primes up to N
N = 500000
print(f"Sieving primes up to {N}...")
t0 = time.time()
sieve = np.ones(N+1, dtype=bool)
sieve[0] = sieve[1] = False
for i in range(2, int(N**0.5)+1):
    if sieve[i]:
        sieve[i*i::i] = False
primes_set = set(np.where(sieve)[0])
print(f"  {len(primes_set)} primes in {time.time()-t0:.1f}s")

# Step 2: Compute r(2n) = #{p+q=2n, p,q prime} for even 2n up to N
MAX_2N = N
print(f"\nComputing r(2n) for 2n up to {MAX_2N}...")
t0 = time.time()
r = np.zeros(MAX_2N//2 + 1, dtype=np.int32)  # r[k] = r(2k)
primes_arr = np.array(sorted(primes_set))

for p in primes_arr:
    if p > MAX_2N:
        break
    # For each prime p, check if 2k - p is also prime
    for k in range(max(2, (p+2)//2), MAX_2N//2 + 1):
        q = 2*k - p
        if q < 2:
            continue
        if q > p:
            break  # avoid double counting by requiring q <= p... actually we want total count
        if q <= N and sieve[q]:
            r[k] += 1
            if q != p:
                r[k] += 1  # count (p,q) and (q,p) unless p=q

print(f"  Done in {time.time()-t0:.1f}s")
print(f"  r(10)={r[5]}, r(100)={r[50]}, r(1000)={r[500]}")

# Step 3: Hardy-Littlewood prediction
# r_HL(2n) ~ 2 * C2 * n / (log n)^2 * prod_{p|n, p>2} (p-1)/(p-2)
# C2 = prod_{p>2} (1 - 1/(p-1)^2) = 0.6601618...
C2 = 0.6601618
print(f"\nComputing Hardy-Littlewood predictions...")

# Simplified: just use 2*C2*n/log(n)^2 without singular series
hl = np.zeros_like(r, dtype=np.float64)
for k in range(3, len(r)):
    n = 2*k
    logn = np.log(n)
    if logn > 0:
        hl[k] = 2 * C2 * n / (logn * logn)

# Detrended residual
residual = np.zeros(len(r), dtype=np.float64)
for k in range(3, len(r)):
    if hl[k] > 0:
        residual[k] = r[k] / hl[k] - 1.0

print(f"  Mean residual: {np.mean(residual[100:len(r)]):.4f}")
print(f"  Std residual: {np.std(residual[100:len(r)]):.4f}")

# Step 4: Build spectroscope
# F(gamma) = gamma^2 * |sum residual(k) / k * e^{-i*gamma*log(k)}|^2
print(f"\nBuilding spectroscope...")
t0 = time.time()

gamma_grid = np.linspace(1.0, 50.0, 491)
logk = np.log(np.arange(3, len(r), dtype=np.float64))
weights = residual[3:] / np.arange(3, len(r), dtype=np.float64)

scores = np.zeros(len(gamma_grid))
for gi, gamma in enumerate(gamma_grid):
    phases = np.exp(-1j * gamma * logk)
    s = np.sum(weights * phases)
    scores[gi] = gamma * gamma * abs(s)**2

print(f"  Done in {time.time()-t0:.1f}s")

# Step 5: Find peaks and check against known zeros
mean_score = np.mean(scores)
std_score = np.std(scores)

print(f"\n=== TOP 10 PEAKS ===")
print(f"Background: mean={mean_score:.1f}, std={std_score:.1f}")
print(f"{'gamma':>8} | {'score':>10} | {'z-score':>8} | note")
print("-" * 50)

top_idx = np.argsort(scores)[::-1][:10]
for idx in top_idx:
    g = gamma_grid[idx]
    z = (scores[idx] - mean_score) / std_score
    note = ""
    if abs(g - 14.13) < 0.3: note = "<-- zeta gamma_1"
    elif abs(g - 21.02) < 0.3: note = "<-- zeta gamma_2"
    elif abs(g - 25.01) < 0.3: note = "<-- zeta gamma_3"
    elif abs(g - 30.42) < 0.3: note = "<-- zeta gamma_4"
    elif abs(g - 32.94) < 0.3: note = "<-- zeta gamma_5"
    print(f"{g:>8.1f} | {scores[idx]:>10.1f} | {z:>8.2f} | {note}")

# Step 6: Check at specific zeta zeros
print(f"\n=== DETECTION AT KNOWN ZEROS ===")
targets = [(14.1347, "gamma_1"), (21.0220, "gamma_2"), (25.0109, "gamma_3"), 
           (30.4249, "gamma_4"), (32.9351, "gamma_5")]
print(f"{'zero':>10} | {'gamma':>8} | {'score':>10} | {'z-score':>8} | detected?")
print("-" * 60)
for target_g, name in targets:
    idx = np.argmin(np.abs(gamma_grid - target_g))
    z = (scores[idx] - mean_score) / std_score
    det = "YES" if z > 2 else "no"
    print(f"{name:>10} | {gamma_grid[idx]:>8.1f} | {scores[idx]:>10.1f} | {z:>8.2f} | {det}")

# Step 7: Enhancement attempts
print(f"\n=== ENHANCEMENT: Möbius-weighted Goldbach ===")
# Try: weight by mu-structure instead of raw residual
# w(k) = sum_{p+q=2k} mu(p)*mu(q) / (2k)
# This should couple more directly to 1/zeta
mu = np.zeros(N+1, dtype=np.int8)
mu[1] = 1
for n in range(2, N+1):
    x, nf, p = n, 0, 2
    sq_free = True
    while p * p <= x:
        if x % p == 0:
            nf += 1; x //= p
            if x % p == 0: sq_free = False; break
        p += (1 if p == 2 else 2)
    if not sq_free: mu[n] = 0
    else:
        if x > 1: nf += 1
        mu[n] = (-1)**nf

# Möbius-weighted Goldbach sum
print("Computing Möbius-weighted Goldbach sums...")
mw = np.zeros(MAX_2N//2 + 1, dtype=np.float64)
for p in primes_arr:
    if p > MAX_2N: break
    mu_p = int(mu[p])
    if mu_p == 0: continue
    for k in range((p+2)//2, min(MAX_2N//2 + 1, (p + N)//2 + 1)):
        q = 2*k - p
        if 2 <= q <= N and sieve[q]:
            mw[k] += mu_p * int(mu[q])

weights_mw = mw[3:] / np.arange(3, len(mw), dtype=np.float64)
scores_mw = np.zeros(len(gamma_grid))
for gi, gamma in enumerate(gamma_grid):
    phases = np.exp(-1j * gamma * logk[:len(weights_mw)])
    s = np.sum(weights_mw[:len(phases)] * phases)
    scores_mw[gi] = gamma * gamma * abs(s)**2

mean_mw = np.mean(scores_mw)
std_mw = np.std(scores_mw)

print(f"\nMöbius-weighted peaks:")
print(f"{'zero':>10} | {'gamma':>8} | {'z-score':>8} | detected?")
print("-" * 45)
for target_g, name in targets:
    idx = np.argmin(np.abs(gamma_grid - target_g))
    z = (scores_mw[idx] - mean_mw) / std_mw if std_mw > 0 else 0
    det = "YES" if z > 2 else "no"
    print(f"{name:>10} | {gamma_grid[idx]:>8.1f} | {z:>8.2f} | {det}")

# Top peaks for Möbius-weighted
print(f"\nMöbius-weighted top 5:")
top_mw = np.argsort(scores_mw)[::-1][:5]
for idx in top_mw:
    g = gamma_grid[idx]
    z = (scores_mw[idx] - mean_mw) / std_mw
    note = ""
    if abs(g - 14.13) < 0.3: note = "<-- zeta gamma_1"
    elif abs(g - 21.02) < 0.3: note = "<-- zeta gamma_2"
    elif abs(g - 25.01) < 0.3: note = "<-- zeta gamma_3"
    print(f"  gamma={g:.1f}, z={z:.2f} {note}")

print(f"\nDone.")
