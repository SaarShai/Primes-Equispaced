#!/usr/bin/env python3
"""
GRH Pipeline v2: Systematic GRH verification across quadratic characters.

Uses the explicit formula approach: zeros of L(s,chi) appear as peaks in
  F_chi(gamma) = |sum_{p <= N} chi(p) * p^{-1/2} * exp(-i*gamma*log(p))|^2

Peak detection uses prominence (scipy) + global z-score.
"""

import numpy as np
from scipy.signal import find_peaks
from datetime import datetime
import time

# ─── Step 1: Sieve primes to N ─────────────────────────────────────────
N = 1_000_000
print(f"[1] Sieving primes to {N:,}...")
t0 = time.time()

is_prime = np.ones(N + 1, dtype=bool)
is_prime[0] = is_prime[1] = False
for i in range(2, int(N**0.5) + 1):
    if is_prime[i]:
        is_prime[i*i::i] = False

primes = np.where(is_prime)[0].astype(np.int64)
n_primes = len(primes)
log_primes = np.log(primes.astype(np.float64))
sqrt_primes = np.sqrt(primes.astype(np.float64))

print(f"    Found {n_primes:,} primes in {time.time()-t0:.1f}s.")

# ─── Step 2: Sieve Mobius to N ──────────────────────────────────────────
print(f"[2] Sieving Mobius function to {N:,}...")
t0 = time.time()

mu = np.zeros(N + 1, dtype=np.int8)
mu[1] = 1
spf = np.zeros(N + 1, dtype=np.int32)
for i in range(2, N + 1):
    if spf[i] == 0:
        for j in range(i, N + 1, i):
            if spf[j] == 0:
                spf[j] = i

for n in range(2, N + 1):
    p = spf[n]
    m = n // p
    if m % p == 0:
        mu[n] = 0
    else:
        mu[n] = -mu[m]

print(f"    Mobius sieve done in {time.time()-t0:.1f}s.")

# ─── Helpers ────────────────────────────────────────────────────────────
def legendre_symbol(a, q):
    if a % q == 0:
        return 0
    val = pow(int(a), (q - 1) // 2, q)
    return -1 if val == q - 1 else 1

def chi_mod4(n):
    if n % 2 == 0:
        return 0
    return 1 if (n % 4 == 1) else -1

def detect_peaks(F, gammas, global_z_thresh=2.0, prominence_factor=0.5):
    """
    Detect peaks using scipy prominence + global z-score filter.
    Returns list of (gamma, F_value, z_score).
    """
    mean_F = np.mean(F)
    std_F = np.std(F)
    if std_F == 0:
        return []

    # Find all local maxima with minimum prominence
    min_prom = prominence_factor * std_F
    peak_idx, properties = find_peaks(F, prominence=min_prom, distance=20)

    results = []
    for idx in peak_idx:
        z = (F[idx] - mean_F) / std_F
        if z > global_z_thresh:
            results.append((gammas[idx], F[idx], z))

    results.sort(key=lambda x: x[0])
    return results

def compute_spectral_A(chi_at_primes, gammas, log_primes, sqrt_primes):
    """Method A: F(gamma) = |sum_p chi(p)/sqrt(p) * exp(-i*gamma*log(p))|^2"""
    coeffs = chi_at_primes / sqrt_primes
    n_g = len(gammas)
    F = np.zeros(n_g, dtype=np.float64)
    CHUNK = 2000
    for s in range(0, n_g, CHUNK):
        e = min(s + CHUNK, n_g)
        g = gammas[s:e, None]
        phases = g * log_primes[None, :]
        S = np.sum(coeffs[None, :] * np.exp(-1j * phases), axis=1)
        F[s:e] = np.abs(S)**2
    return F

def compute_spectral_B(chi_mu_vals, gammas, primes, log_primes):
    """Method B: F(gamma) = gamma^2 * |sum_p M_chi(p)/p * exp(-i*gamma*log(p))|^2"""
    M_chi_cum = np.cumsum(chi_mu_vals)
    M_at_primes = M_chi_cum[primes]
    coeffs = M_at_primes / primes.astype(np.float64)
    n_g = len(gammas)
    F = np.zeros(n_g, dtype=np.float64)
    CHUNK = 2000
    for s in range(0, n_g, CHUNK):
        e = min(s + CHUNK, n_g)
        g = gammas[s:e, None]
        phases = g * log_primes[None, :]
        S = np.sum(coeffs[None, :] * np.exp(-1j * phases), axis=1)
        F[s:e] = gammas[s:e]**2 * np.abs(S)**2
    return F

# ─── Step 3: Run for all characters ────────────────────────────────────
MODULI = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
GAMMA_MIN, GAMMA_MAX = 1.0, 50.0
N_GAMMA = 10000
gammas = np.linspace(GAMMA_MIN, GAMMA_MAX, N_GAMMA)

KNOWN_ZEROS = {
    3: [8.04, 13.16],
    4: [6.02, 10.24, 12.59],
    5: [6.18, 8.72],
}

print(f"\n[3] Computing spectral functions for {len(MODULI)} quadratic characters + chi_4...")
print(f"    gamma range: [{GAMMA_MIN}, {GAMMA_MAX}], {N_GAMMA} points")
print(f"    Using {n_primes:,} primes up to {N:,}\n")

all_results = {}

for q in MODULI:
    t1 = time.time()

    chi_primes = np.array([legendre_symbol(int(p), q) for p in primes], dtype=np.float64)
    F_A = compute_spectral_A(chi_primes, gammas, log_primes, sqrt_primes)
    peaks_A = detect_peaks(F_A, gammas)

    chi_mu_vals = np.zeros(N + 1, dtype=np.float64)
    for n in range(1, N + 1):
        if mu[n] != 0:
            chi_mu_vals[n] = mu[n] * legendre_symbol(n, q)
    F_B = compute_spectral_B(chi_mu_vals, gammas, primes, log_primes)
    peaks_B = detect_peaks(F_B, gammas)

    elapsed = time.time() - t1
    all_results[q] = {
        'peaks_A': peaks_A, 'peaks_B': peaks_B,
        'n_peaks_A': len(peaks_A), 'n_peaks_B': len(peaks_B),
        'elapsed': elapsed,
    }
    fA = f"{peaks_A[0][0]:.2f}" if peaks_A else "none"
    fB = f"{peaks_B[0][0]:.2f}" if peaks_B else "none"
    print(f"    q={q:2d}: A={len(peaks_A):2d} peaks (first {fA:>6s}), "
          f"B={len(peaks_B):2d} peaks (first {fB:>6s}), ({elapsed:.1f}s)")

# chi_4
t1 = time.time()
chi4_primes = np.array([chi_mod4(int(p)) for p in primes], dtype=np.float64)
F_A4 = compute_spectral_A(chi4_primes, gammas, log_primes, sqrt_primes)
peaks_A4 = detect_peaks(F_A4, gammas)

chi_mu4 = np.zeros(N + 1, dtype=np.float64)
for n in range(1, N + 1):
    if mu[n] != 0:
        chi_mu4[n] = mu[n] * chi_mod4(n)
F_B4 = compute_spectral_B(chi_mu4, gammas, primes, log_primes)
peaks_B4 = detect_peaks(F_B4, gammas)

elapsed4 = time.time() - t1
all_results[4] = {
    'peaks_A': peaks_A4, 'peaks_B': peaks_B4,
    'n_peaks_A': len(peaks_A4), 'n_peaks_B': len(peaks_B4),
    'elapsed': elapsed4,
}
fA4 = f"{peaks_A4[0][0]:.2f}" if peaks_A4 else "none"
fB4 = f"{peaks_B4[0][0]:.2f}" if peaks_B4 else "none"
print(f"    q= 4: A={len(peaks_A4):2d} peaks (first {fA4:>6s}), "
      f"B={len(peaks_B4):2d} peaks (first {fB4:>6s}), ({elapsed4:.1f}s)")

# ─── Step 4: Compare against known zeros ────────────────────────────────
print(f"\n[4] Comparing peaks against known L-function zeros...")

TOLERANCE = 0.5
comparisons = {}

for q_known, zeros in KNOWN_ZEROS.items():
    res = all_results.get(q_known)
    if not res:
        continue
    for method, key in [('A', 'peaks_A'), ('B', 'peaks_B')]:
        peak_positions = [g for g, _, _ in res[key]]
        matches = []
        for z0 in zeros:
            closest = min(peak_positions, key=lambda g: abs(g - z0)) if peak_positions else None
            dist = abs(closest - z0) if closest is not None else float('inf')
            matches.append({
                'zero': z0,
                'closest_peak': closest,
                'distance': dist,
                'match': dist < TOLERANCE,
            })
        label = f"chi_{q_known}_{method}"
        comparisons[label] = {
            'q': q_known, 'method': method,
            'peaks': res[key], 'matches': matches,
            'n_peaks': len(res[key]),
        }
        n_m = sum(1 for m in matches if m['match'])
        print(f"    {label}: {n_m}/{len(zeros)} zeros matched")

# ─── Step 5: Report ─────────────────────────────────────────────────────
print(f"\n[5] Generating report...")

L = []
L.append("# GRH Pipeline v2: Quadratic Character Spectral Analysis")
L.append(f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
L.append(f"**Sieve limit:** N = {N:,}")
L.append(f"**Primes used:** {n_primes:,}")
L.append(f"**Gamma range:** [{GAMMA_MIN}, {GAMMA_MAX}], {N_GAMMA} points")
L.append(f"**Peak detection:** scipy prominence + global z > 2.0")
L.append(f"**Zero match tolerance:** {TOLERANCE}")

L.append("\n## Methods")
L.append("- **A (Prime Sum):** F(gamma) = |sum_p chi(p)/sqrt(p) * exp(-i*gamma*log(p))|^2")
L.append("- **B (Mertens):** F(gamma) = gamma^2 * |sum_p M_chi(p)/p * exp(-i*gamma*log(p))|^2")

L.append("\n## Summary Table")
L.append("")
L.append("| q | A: #Peaks | A: First | B: #Peaks | B: First | Time |")
L.append("|---|-----------|----------|-----------|----------|------|")
for q in MODULI + [4]:
    r = all_results[q]
    fA = f"{r['peaks_A'][0][0]:.2f}" if r['peaks_A'] else "—"
    fB = f"{r['peaks_B'][0][0]:.2f}" if r['peaks_B'] else "—"
    L.append(f"| {q:2d} | {r['n_peaks_A']:2d} | {fA:>6s} | {r['n_peaks_B']:2d} | {fB:>6s} | {r['elapsed']:.1f}s |")

L.append("\n## Validation Against Known L-function Zeros")
L.append("")

total_A = 0
total_B = 0
total_zeros = 0

for q_known, zeros in sorted(KNOWN_ZEROS.items()):
    L.append(f"### L(s, chi_{q_known})")
    L.append(f"Known zeros: {', '.join(f'{z:.2f}' for z in zeros)}")
    L.append("")

    for method in ['A', 'B']:
        label = f"chi_{q_known}_{method}"
        data = comparisons.get(label)
        if not data:
            continue
        L.append(f"**Method {method}** ({data['n_peaks']} peaks):")
        for m in data['matches']:
            status = "MATCH" if m['match'] else "MISS"
            if method == 'A':
                total_zeros += 1
                if m['match']:
                    total_A += 1
            else:
                if m['match']:
                    total_B += 1
            if m['closest_peak'] is not None:
                L.append(f"- Zero {m['zero']:.2f} -> peak {m['closest_peak']:.2f} "
                         f"(delta={m['distance']:.2f}) **{status}**")
            else:
                L.append(f"- Zero {m['zero']:.2f} -> no peaks **MISS**")
        L.append("")

L.append("\n## Verdict")
L.append("")
L.append(f"- **Characters tested:** {len(MODULI)} quadratic (q=3..47) + chi_4 = 15 total")
L.append(f"- **Known zeros checked:** {total_zeros} (chi_3, chi_4, chi_5)")
L.append(f"- **Method A matches:** {total_A}/{total_zeros}")
L.append(f"- **Method B matches:** {total_B}/{total_zeros}")

best = max(total_A, total_B)
best_m = "A" if total_A >= total_B else "B"
rate = best / total_zeros * 100 if total_zeros > 0 else 0
L.append(f"- **Best method:** {best_m} with {rate:.0f}% match rate")
L.append("")

if rate >= 75:
    L.append("**STRONG EVIDENCE:** The spectral method successfully detects L-function zeros")
    L.append("across multiple Dirichlet characters. The Farey spectroscope framework")
    L.append("generalizes beyond zeta to Dirichlet L-functions, consistent with GRH.")
elif rate >= 50:
    L.append("**PARTIAL EVIDENCE:** Some L-function zeros detected. Method shows promise")
    L.append("but may need larger N or finer gamma grid for robust verification.")
else:
    L.append("**WEAK/NEGATIVE:** Low match rate at this sieve limit. Further investigation needed.")

L.append("\n## Full Peak Lists (Top 10 per character)")
L.append("")
for q in MODULI + [4]:
    r = all_results[q]
    for method, key in [('A', 'peaks_A'), ('B', 'peaks_B')]:
        if r[key]:
            L.append(f"### q={q}, Method {method}")
            for g, f, z in r[key][:10]:
                L.append(f"  - gamma={g:.3f}, F={f:.2e}, z={z:.1f}")
            if len(r[key]) > 10:
                L.append(f"  - ... ({len(r[key])-10} more)")
            L.append("")

report = "\n".join(L)
output_path = "/Users/saar/Desktop/Farey-Local/experiments/GRH_PIPELINE_V2.md"
with open(output_path, 'w') as f:
    f.write(report)
print(f"\n[6] Report saved to {output_path}")

print(f"\n{'='*60}")
print(f"VERDICT: A={total_A}/{total_zeros}, B={total_B}/{total_zeros}")
print(f"Best: Method {best_m} at {rate:.0f}%")
print(f"{'='*60}")
