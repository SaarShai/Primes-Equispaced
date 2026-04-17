#!/usr/bin/env python3
"""Compute the avoidance ratio: min|c_K| at zeta zeros vs generic points."""
from mpmath import mp, mpf, mpc, exp, log, fabs, pi, zetazero
mp.dps = 30

def mobius(n):
    if n == 1: return 1
    x, nf, p = n, 0, 2
    while p * p <= x:
        if x % p == 0:
            nf += 1; x //= p
            if x % p == 0: return 0
        p += (1 if p == 2 else 2)
    if x > 1: nf += 1
    return (-1) ** nf

def c_K(s, K, mu):
    return sum(mu[k] * mp.power(k, -s) for k in range(2, K+1) if mu[k] != 0)

# Precompute
MU = {k: mobius(k) for k in range(1, 201)}

# Zeta zeros (first 200)
print("Computing 200 zeta zeros...")
gammas = [zetazero(j).imag for j in range(1, 201)]
print(f"  gamma_1 = {gammas[0]}, gamma_200 = {gammas[-1]}")

# Generic points (2000 in [0, 1000])
generic_t = [mpf(i) * 1000 / 2000 for i in range(1, 2001)]

print("\n=== PART 1: Avoidance Ratios ===\n")
print(f"{'K':>4} | {'min|c_K| zeros':>16} | {'min|c_K| generic':>16} | {'ratio':>8} | {'mean zeros':>12} | {'mean generic':>12}")
print("-" * 90)

for K in [5, 10, 15, 20, 30, 50]:
    # At zeta zeros
    vals_zeros = [fabs(c_K(mpc(0.5, g), K, MU)) for g in gammas[:100]]
    min_z = min(vals_zeros)
    mean_z = sum(vals_zeros) / len(vals_zeros)
    min_z_idx = vals_zeros.index(min_z)

    # At generic points
    vals_generic = [fabs(c_K(mpc(0.5, t), K, MU)) for t in generic_t]
    min_g = min(vals_generic)
    mean_g = sum(vals_generic) / len(vals_generic)

    ratio = float(min_z / min_g) if min_g > 0 else float('inf')
    print(f"{K:>4} | {float(min_z):>16.6f} | {float(min_g):>16.6f} | {ratio:>8.2f}x | {float(mean_z):>12.4f} | {float(mean_g):>12.4f}")

print("\n=== PART 2: 10 Closest Approaches (K=10) ===\n")
vals_10 = [(j+1, gammas[j], fabs(c_K(mpc(0.5, gammas[j]), 10, MU))) for j in range(100)]
vals_10.sort(key=lambda x: x[2])

print(f"{'j':>4} | {'gamma_j':>14} | {'|c_10(rho_j)|':>14}")
print("-" * 40)
for j, g, v in vals_10[:10]:
    print(f"{j:>4} | {float(g):>14.6f} | {float(v):>14.6f}")

print("\n=== PART 3: Near-misses (c_10 zeros near zeta zeros) ===\n")
# Scan for approximate zeros of c_10 on Re(s)=1/2
print("Scanning for c_10 zeros on critical line, t in [0, 300]...")
step = mpf("0.1")
t = mpf("0.1")
c10_zeros = []
prev_re = float(c_K(mpc(0.5, t), 10, MU).real)
prev_im = float(c_K(mpc(0.5, t), 10, MU).imag)

while t < 300:
    t += step
    val = c_K(mpc(0.5, t), 10, MU)
    cur_re = float(val.real)
    cur_im = float(val.imag)
    absv = float(fabs(val))
    if absv < 0.15:  # near a zero
        c10_zeros.append((float(t), absv))
    prev_re, prev_im = cur_re, cur_im

# Find local minima
if c10_zeros:
    # Cluster nearby points
    clusters = []
    current = [c10_zeros[0]]
    for i in range(1, len(c10_zeros)):
        if c10_zeros[i][0] - current[-1][0] < 1.0:
            current.append(c10_zeros[i])
        else:
            clusters.append(min(current, key=lambda x: x[1]))
            current = [c10_zeros[i]]
    clusters.append(min(current, key=lambda x: x[1]))

    # Find nearest zeta zero to each c_10 near-zero
    print(f"Found {len(clusters)} near-zero regions of c_10")
    print(f"\n{'t_min':>10} | {'|c_10|':>10} | {'nearest gamma':>14} | {'distance':>10}")
    print("-" * 55)
    for t_min, abs_min in sorted(clusters, key=lambda x: x[1])[:15]:
        # Find nearest zeta zero
        dists = [(abs(t_min - float(g)), float(g)) for g in gammas]
        nearest_dist, nearest_g = min(dists)
        print(f"{t_min:>10.4f} | {abs_min:>10.6f} | {nearest_g:>14.6f} | {nearest_dist:>10.4f}")
else:
    print("No near-zeros found!")

print("\nDone.")
