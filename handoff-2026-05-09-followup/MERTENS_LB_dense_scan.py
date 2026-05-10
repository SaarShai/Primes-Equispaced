#!/usr/bin/env python3
"""
Dense scan: T(N) for every N in [1, NMAX], computing in float64 with
Dirichlet block walks for speed.  Output:
  - log of every N where T(N) > 0 (Polya-disproof of MERTENS-LB)
  - log of every N where T(N) > -1 (c'=1 fails)
  - global min and max of T(N) over the scan range
  - quasi-period structure (at what N does T(N) cross zero)
"""
import sys, time
sys.path.insert(0, "/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup")
from MERTENS_LB_sweep import mobius_sieve, cumsum_int32
import numpy as np

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
print(f"Dense scan over N in [1, {NMAX}]", flush=True)

t0 = time.time()
mu = mobius_sieve(NMAX)
M = cumsum_int32(mu)
print(f"  sieve+cumsum: {time.time()-t0:.1f}s", flush=True)

# For each N <= NMAX, compute T(N) = 1 + sum_{k=1}^N M(N//k)/k
# Memoize harmonic prefix H[k] = sum_{j=1}^k 1/j as float64.
print(f"Computing harmonic prefix H[1..{NMAX}]...", flush=True)
t0 = time.time()
H = np.empty(NMAX + 1, dtype=np.float64)
H[0] = 0.0
# vectorized prefix sum
inv = 1.0 / np.arange(1, NMAX + 1, dtype=np.float64)
H[1:] = np.cumsum(inv)
print(f"  H done in {time.time()-t0:.1f}s.  H[NMAX] = {H[NMAX]:.6f} (~ ln(NMAX)+gamma = {np.log(NMAX)+0.577216:.6f})", flush=True)

print(f"Sweeping T(N) for every N in [1, {NMAX}]...", flush=True)
t0 = time.time()

# We will produce arrays:
T_arr = np.empty(NMAX + 1, dtype=np.float64)
T_arr[0] = 1.0  # placeholder

# Track flips
flips_pos = []   # T(N) > 0
flips_neg1 = []  # T(N) > -1
min_T = float("inf"); min_T_N = 0
max_T = float("-inf"); max_T_N = 0
min_neg_T = float("inf"); min_neg_T_N = 0  # smallest |T| with T < 0  (i.e. closest to 0 from below)

last_print = time.time()
for N in range(1, NMAX + 1):
    # Block walk: for k from 1, q = N//k, k1 = N//q, contribution M[q]*(H[k1]-H[k-1])
    s = 0.0
    k = 1
    while k <= N:
        q = N // k
        k1 = N // q
        if k1 > N: k1 = N
        s += int(M[q]) * (H[k1] - H[k-1])
        k = k1 + 1
    T = 1.0 + s
    T_arr[N] = T
    if T > 0:
        flips_pos.append((N, T))
    if T > -1:
        flips_neg1.append((N, T))
    if T < min_T:
        min_T = T; min_T_N = N
    if T > max_T:
        max_T = T; max_T_N = N
    if T < 0 and -T < min_neg_T:
        min_neg_T = -T; min_neg_T_N = N
    if time.time() - last_print > 5:
        elapsed = time.time() - t0
        rate = N / elapsed
        eta = (NMAX - N) / rate
        print(f"  N={N:>10}, T={T:>14.4f}, rate={rate:.0f}/s, ETA {eta:.0f}s", flush=True)
        last_print = time.time()

print(f"Scan done in {time.time()-t0:.1f}s", flush=True)

# Save T_arr for later analysis
np.save(f"/tmp/T_arr_NMAX_{NMAX}.npy", T_arr)
print(f"Saved /tmp/T_arr_NMAX_{NMAX}.npy", flush=True)

print(f"\n=== STATS ===", flush=True)
print(f"Total N scanned: {NMAX}", flush=True)
print(f"# N with T(N) > 0:   {len(flips_pos)}", flush=True)
print(f"# N with T(N) > -1:  {len(flips_neg1)}", flush=True)
print(f"min T(N) = {min_T:.6f} at N = {min_T_N}", flush=True)
print(f"max T(N) = {max_T:.6f} at N = {max_T_N}", flush=True)
print(f"closest-to-0 T(N) [T<0]: T = -{min_neg_T:.6f} at N = {min_neg_T_N}", flush=True)

print(f"\nFirst 30 N with T(N) > 0:", flush=True)
for N, T in flips_pos[:30]:
    print(f"  N={N:>8}: T={T:.6f}", flush=True)
if len(flips_pos) > 30:
    print(f"  ... ({len(flips_pos) - 30} more)", flush=True)
    print(f"Last 10 N with T(N) > 0:", flush=True)
    for N, T in flips_pos[-10:]:
        print(f"  N={N:>8}: T={T:.6f}", flush=True)

print(f"\nFirst 30 N with T(N) > -1 (i.e. c'=1 fails):", flush=True)
for N, T in flips_neg1[:30]:
    print(f"  N={N:>8}: T={T:.6f}", flush=True)
if len(flips_neg1) > 30:
    print(f"  ... ({len(flips_neg1) - 30} more)", flush=True)
