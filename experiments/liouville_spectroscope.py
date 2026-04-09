#!/usr/bin/env python3
"""
Liouville Spectroscope: compare Mertens vs Liouville spectral transforms
at known zeta zeros.

Computes:
  F_M(gamma) = gamma^2 * |sum_{p prime} M(p)/p * exp(-i*gamma*log(p))|^2
  F_L(gamma) = gamma^2 * |sum_{p prime} L(p)/p * exp(-i*gamma*log(p))|^2

Then measures local z-scores at the first 20 zeta zeros for each.
"""

import numpy as np
import time
import os

# ── 1. Sieve for Omega(n), Mobius, primes ───────────────────────────────
N = 500_000
print(f"Sieving up to N={N}...")
t0 = time.time()

# smallest prime factor for Mobius
spf = np.zeros(N + 1, dtype=np.int32)
# Omega(n) = number of prime factors with multiplicity
omega = np.zeros(N + 1, dtype=np.int32)
# number of distinct prime factors (for Mobius)
omega_distinct = np.zeros(N + 1, dtype=np.int32)
# is squarefree
squarefree = np.ones(N + 1, dtype=bool)

primes = []
is_prime = np.ones(N + 1, dtype=bool)
is_prime[0] = is_prime[1] = False

for p in range(2, N + 1):
    if is_prime[p]:
        primes.append(p)
        spf[p] = p
        # Mark Omega for multiples
        for m in range(p, N + 1, p):
            if m != p:
                is_prime[m] = False
            if spf[m] == 0:
                spf[m] = p
            omega_distinct[m] += 1
            # Count multiplicity
            val = m
            while val % p == 0:
                omega[m] += 1
                val //= p
            # Check squarefree
            if omega[m] - (omega[m] - 1) > 0:
                # simpler: check if p^2 divides m
                pass

# Fix squarefree properly
for p in primes:
    p2 = p * p
    if p2 > N:
        break
    for m in range(p2, N + 1, p2):
        squarefree[m] = False

# Mobius function
mu = np.zeros(N + 1, dtype=np.int8)
for n in range(1, N + 1):
    if squarefree[n]:
        mu[n] = (-1) ** omega_distinct[n]
    else:
        mu[n] = 0

# Liouville function
lam = np.ones(N + 1, dtype=np.int8)  # lambda(n) = (-1)^Omega(n)
for n in range(1, N + 1):
    lam[n] = (-1) ** omega[n]

t1 = time.time()
print(f"Sieve done in {t1 - t0:.2f}s. Found {len(primes)} primes.")

# ── 2. Cumulative sums M(n) and L(n) ───────────────────────────────────
print("Computing cumulative sums M(n) and L(n)...")
M = np.cumsum(mu.astype(np.int64))  # M(n) = sum_{k=1}^{n} mu(k)
L = np.cumsum(lam.astype(np.int64))  # L(n) = sum_{k=1}^{n} lambda(k)

# Extract at primes
primes_arr = np.array(primes, dtype=np.int64)
M_at_primes = M[primes_arr]
L_at_primes = L[primes_arr]
log_primes = np.log(primes_arr.astype(np.float64))
inv_primes = 1.0 / primes_arr.astype(np.float64)

print(f"  M(500000) = {M[N]},  L(500000) = {L[N]}")
print(f"  Primes used: {len(primes_arr)}")

# ── 3. Spectroscope computation ─────────────────────────────────────────
gamma_min, gamma_max = 5.0, 85.0
n_gamma = 20000
gammas = np.linspace(gamma_min, gamma_max, n_gamma)

print(f"Computing spectroscopes over {n_gamma} gamma points in [{gamma_min}, {gamma_max}]...")
t2 = time.time()

# Vectorized: for each gamma, compute sum over primes
# F(gamma) = gamma^2 * |sum_p f(p)/p * exp(-i*gamma*log(p))|^2

# Pre-compute weights
w_M = M_at_primes.astype(np.float64) * inv_primes  # M(p)/p
w_L = L_at_primes.astype(np.float64) * inv_primes  # L(p)/p

F_M = np.zeros(n_gamma)
F_L = np.zeros(n_gamma)

# Process in chunks to manage memory
chunk_size = 500
n_chunks = (n_gamma + chunk_size - 1) // chunk_size

for ic in range(n_chunks):
    i0 = ic * chunk_size
    i1 = min(i0 + chunk_size, n_gamma)
    g = gammas[i0:i1]  # shape (chunk,)

    # phases: shape (chunk, n_primes)
    phases = np.outer(g, log_primes)  # gamma * log(p)
    exp_phases = np.exp(-1j * phases)

    # Mertens transform
    s_M = np.dot(exp_phases, w_M)  # shape (chunk,)
    F_M[i0:i1] = g**2 * np.abs(s_M)**2

    # Liouville transform
    s_L = np.dot(exp_phases, w_L)  # shape (chunk,)
    F_L[i0:i1] = g**2 * np.abs(s_L)**2

t3 = time.time()
print(f"Spectroscopes computed in {t3 - t2:.2f}s")

# ── 4. Known zeta zeros and local z-scores ──────────────────────────────
# First 20 nontrivial zeta zeros (imaginary parts)
zeta_zeros = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840
])

def local_zscore(gammas, F, gamma0, half_window=1.5):
    """Compute local z-score: (F(gamma0) - mean) / std in a window around gamma0."""
    mask = np.abs(gammas - gamma0) <= half_window
    if mask.sum() < 10:
        return np.nan, np.nan
    local_vals = F[mask]
    # Value at closest point to gamma0
    idx = np.argmin(np.abs(gammas - gamma0))
    peak = F[idx]
    mean_val = np.mean(local_vals)
    std_val = np.std(local_vals)
    if std_val < 1e-15:
        return peak, np.nan
    return peak, (peak - mean_val) / std_val

print("\n" + "="*80)
print("LOCAL Z-SCORES AT FIRST 20 ZETA ZEROS")
print("="*80)
print(f"{'Zero':>6} {'gamma':>10} {'z_Mertens':>12} {'z_Liouville':>12} {'Ratio L/M':>10}")
print("-"*60)

z_M_list = []
z_L_list = []
ratios = []

for i, g0 in enumerate(zeta_zeros):
    if g0 < gamma_min or g0 > gamma_max:
        continue
    _, z_M = local_zscore(gammas, F_M, g0, half_window=1.5)
    _, z_L = local_zscore(gammas, F_L, g0, half_window=1.5)

    z_M_list.append(z_M)
    z_L_list.append(z_L)

    if not np.isnan(z_M) and z_M > 0.01:
        ratio = z_L / z_M
        ratios.append(ratio)
    else:
        ratio = np.nan

    print(f"  {i+1:>3}   {g0:>10.6f} {z_M:>12.4f} {z_L:>12.4f} {ratio:>10.4f}")

z_M_arr = np.array(z_M_list)
z_L_arr = np.array(z_L_list)
ratios_arr = np.array(ratios)

print("-"*60)
print(f"  Mean z_Mertens:   {np.nanmean(z_M_arr):.4f}")
print(f"  Mean z_Liouville: {np.nanmean(z_L_arr):.4f}")
print(f"  Mean ratio L/M:   {np.nanmean(ratios_arr):.4f}")
print(f"  Median ratio L/M: {np.nanmedian(ratios_arr):.4f}")
print(f"  Std ratio L/M:    {np.nanstd(ratios_arr):.4f}")

# ── 5. Theory prediction ────────────────────────────────────────────────
# Theoretical ratio: |zeta(2*rho)| * sqrt(pi^2/6)
# zeta(2*rho) for first few zeros (approximate magnitudes)
print("\n" + "="*80)
print("THEORETICAL PREDICTION: |zeta(2*rho)| * sqrt(pi^2/6)")
print("="*80)
sqrt_pi2_6 = np.sqrt(np.pi**2 / 6)
print(f"  sqrt(pi^2/6) = {sqrt_pi2_6:.6f}")
print(f"  If |zeta(2*rho)| ~ 1, predicted ratio ~ {sqrt_pi2_6:.4f}")
print(f"  If |zeta(2*rho)| ~ 2, predicted ratio ~ {2*sqrt_pi2_6:.4f}")

# ── 6. Figure ────────────────────────────────────────────────────────────
print("\nGenerating figure...")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Panel A: Mertens spectroscope
ax = axes[0]
ax.plot(gammas, F_M, color='steelblue', linewidth=0.5, alpha=0.8)
for g0 in zeta_zeros:
    if gamma_min <= g0 <= gamma_max:
        ax.axvline(g0, color='red', alpha=0.3, linewidth=0.5)
ax.set_title(r'Mertens Spectroscope: $F_M(\gamma) = \gamma^2 |\sum M(p)/p \, e^{-i\gamma\log p}|^2$',
             fontsize=12)
ax.set_ylabel(r'$F_M(\gamma)$')
ax.set_xlim(gamma_min, gamma_max)

# Panel B: Liouville spectroscope
ax = axes[1]
ax.plot(gammas, F_L, color='darkgreen', linewidth=0.5, alpha=0.8)
for g0 in zeta_zeros:
    if gamma_min <= g0 <= gamma_max:
        ax.axvline(g0, color='red', alpha=0.3, linewidth=0.5)
ax.set_title(r'Liouville Spectroscope: $F_L(\gamma) = \gamma^2 |\sum L(p)/p \, e^{-i\gamma\log p}|^2$',
             fontsize=12)
ax.set_ylabel(r'$F_L(\gamma)$')
ax.set_xlim(gamma_min, gamma_max)

# Panel C: Ratio of z-scores
ax = axes[2]
valid = np.array([(g0, r) for g0, r in zip(zeta_zeros, ratios) if not np.isnan(r)])
if len(valid) > 0:
    ax.bar(valid[:, 0], valid[:, 1], width=0.8, color='purple', alpha=0.7, label='z_L / z_M')
    ax.axhline(np.nanmean(ratios_arr), color='orange', linestyle='--', linewidth=2,
               label=f'Mean ratio = {np.nanmean(ratios_arr):.3f}')
    ax.axhline(sqrt_pi2_6, color='green', linestyle=':', linewidth=2,
               label=f'Theory (|zeta(2rho)|=1): {sqrt_pi2_6:.3f}')
    ax.axhline(1.0, color='gray', linestyle='-', linewidth=1, alpha=0.5)
ax.set_title('Z-score Ratio: Liouville / Mertens at Zeta Zeros', fontsize=12)
ax.set_xlabel(r'$\gamma$ (imaginary part of zeta zero)')
ax.set_ylabel('Ratio z_L / z_M')
ax.set_xlim(gamma_min, gamma_max)
ax.legend(loc='upper right')

plt.tight_layout()
fig_path = os.path.expanduser('~/Desktop/Farey-Local/figures/liouville_spectroscope.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
print(f"Figure saved: {fig_path}")

# ── 7. Summary statistics ───────────────────────────────────────────────
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
n_pos_M = np.sum(z_M_arr > 2)
n_pos_L = np.sum(z_L_arr > 2)
print(f"  Zeros with z > 2 (Mertens):   {n_pos_M}/{len(z_M_arr)}")
print(f"  Zeros with z > 2 (Liouville): {n_pos_L}/{len(z_L_arr)}")
print(f"  Mean z-score Mertens:   {np.nanmean(z_M_arr):.4f}")
print(f"  Mean z-score Liouville: {np.nanmean(z_L_arr):.4f}")
print(f"  Mean L/M ratio:         {np.nanmean(ratios_arr):.4f}")
print(f"  Is Liouville ~2.6x better? {'YES' if np.nanmean(ratios_arr) > 2.0 else 'NO'} (ratio={np.nanmean(ratios_arr):.3f})")
print(f"\nDone. Total time: {time.time() - t0:.1f}s")
