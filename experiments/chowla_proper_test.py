#!/usr/bin/env python3
"""
Proper Chowla conjecture test via normalized spectroscope.

Previous test found "structure" in residual that turned out to be
the smooth envelope |1/zeta(1+ig)|^2 — expected, not a Chowla signal.

This test normalizes AGAINST that envelope, so any remaining structure
would be a genuine Chowla anomaly.
"""

import numpy as np
import time
import sys

# ── 1. Mobius sieve ──────────────────────────────────────────────────
def mobius_sieve(N):
    """Compute mu(n) for n=0..N via sieve."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    smallest_prime = np.zeros(N + 1, dtype=np.int64)

    for p in range(2, N + 1):
        if not is_prime[p]:
            continue
        # p is prime
        for m in range(p, N + 1, p):
            if m != p:
                is_prime[m] = False
            smallest_prime[m] = p

    # Compute mu via factorization
    mu[1] = 1
    for n in range(2, N + 1):
        p = smallest_prime[n]
        if (n // p) % p == 0:
            mu[n] = 0  # p^2 | n
        else:
            mu[n] = -mu[n // p]

    return mu


def primes_up_to(N):
    """Simple sieve of Eratosthenes."""
    sieve = np.ones(N + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for p in range(2, int(N**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = False
    return np.nonzero(sieve)[0]


# ── Parameters ───────────────────────────────────────────────────────
N = 200000
GAMMA_MIN, GAMMA_MAX = 5.0, 60.0
N_GAMMA = 15000
N_SHUFFLE = 20
PRIME_CAP = 1000  # primes up to this for zeta product

print(f"Chowla proper test: N={N}, gamma in [{GAMMA_MIN},{GAMMA_MAX}], {N_GAMMA} pts")
print(f"Null trials: {N_SHUFFLE}")
sys.stdout.flush()

# ── 2. Compute mu(n) ────────────────────────────────────────────────
t0 = time.time()
mu = mobius_sieve(N)
print(f"Mobius sieve: {time.time()-t0:.2f}s, sum(mu)={np.sum(mu[1:])}")
sys.stdout.flush()

# Precompute arrays
ns = np.arange(1, N + 1, dtype=np.float64)
log_ns = np.log(ns)
mu_vals = mu[1:].astype(np.float64)
weights = mu_vals / ns  # mu(n)/n for weighted version

gammas = np.linspace(GAMMA_MIN, GAMMA_MAX, N_GAMMA)

# ── 3. Weighted spectroscope F_w(gamma) ─────────────────────────────
print("Computing weighted spectroscope F_w(gamma)...")
sys.stdout.flush()
t0 = time.time()

# F_w(gamma) = |sum_{n=1}^N mu(n)/n * exp(-i*gamma*log(n))|^2
# Process in chunks to manage memory
CHUNK = 500
F_w = np.zeros(N_GAMMA)
for i in range(0, N_GAMMA, CHUNK):
    g_chunk = gammas[i:i+CHUNK]
    # phase[j,k] = g_chunk[j] * log_ns[k]
    phase = np.outer(g_chunk, log_ns)
    # sum_val[j] = sum_k weights[k] * exp(-i * phase[j,k])
    sum_val = np.dot(np.exp(-1j * phase), weights)
    F_w[i:i+CHUNK] = np.abs(sum_val)**2

print(f"F_w computed: {time.time()-t0:.2f}s")
sys.stdout.flush()

# ── 4. Expected envelope |1/zeta(1+ig)|^2 ───────────────────────────
print("Computing |1/zeta(1+ig)|^2 envelope...")
sys.stdout.flush()
t0 = time.time()

primes = primes_up_to(PRIME_CAP)
print(f"  Using {len(primes)} primes up to {PRIME_CAP}")

# 1/zeta(s) = prod_p (1 - p^{-s})
# For s = 1 + i*gamma:
# p^{-(1+ig)} = p^{-1} * exp(-ig * log(p))
# So 1/zeta(1+ig) = prod_p (1 - p^{-1} * exp(-ig*log(p)))
# |1/zeta(1+ig)|^2 = prod_p |1 - p^{-1} * exp(-ig*log(p))|^2

log_primes = np.log(primes.astype(np.float64))
inv_primes = 1.0 / primes.astype(np.float64)

envelope = np.ones(N_GAMMA)
for idx_p in range(len(primes)):
    # |1 - p^{-1} * exp(-ig*log(p))|^2
    # = 1 - 2*p^{-1}*cos(g*log(p)) + p^{-2}
    cos_vals = np.cos(gammas * log_primes[idx_p])
    factor = 1.0 - 2.0 * inv_primes[idx_p] * cos_vals + inv_primes[idx_p]**2
    envelope *= factor

print(f"Envelope computed: {time.time()-t0:.2f}s")
sys.stdout.flush()

# ── 5. Normalized ratio R(gamma) ────────────────────────────────────
R = F_w / envelope

print(f"\n=== WEIGHTED SPECTROSCOPE (normalized) ===")
print(f"R = F_w / |1/zeta|^2")
print(f"  mean(R)   = {np.mean(R):.6f}")
print(f"  std(R)    = {np.std(R):.6f}")
print(f"  CV(R)     = {np.std(R)/np.mean(R):.6f}")
print(f"  min(R)    = {np.min(R):.6f}")
print(f"  max(R)    = {np.max(R):.6f}")
print(f"  max/min   = {np.max(R)/np.min(R):.4f}")
sys.stdout.flush()

# ── 6. Peaks in R? ──────────────────────────────────────────────────
# Check if R has significant peaks via FFT of R
R_centered = R - np.mean(R)
fft_R = np.abs(np.fft.rfft(R_centered))
fft_freqs = np.fft.rfftfreq(len(R_centered))

# Top 10 FFT peaks (excluding DC)
top_idx = np.argsort(fft_R[1:])[-10:][::-1] + 1
print(f"\nTop 10 FFT peaks in R(gamma):")
for idx in top_idx:
    print(f"  freq={fft_freqs[idx]:.6f}, amplitude={fft_R[idx]:.6f}")
sys.stdout.flush()

# ── 7. Null distribution (weighted) ─────────────────────────────────
print(f"\nComputing {N_SHUFFLE} null trials (weighted, shuffled mu)...")
sys.stdout.flush()
t0 = time.time()

null_cvs = []
null_means = []
null_maxmin = []
rng = np.random.default_rng(42)

for trial in range(N_SHUFFLE):
    mu_shuf = mu_vals.copy()
    rng.shuffle(mu_shuf)
    w_shuf = mu_shuf / ns

    F_null = np.zeros(N_GAMMA)
    for i in range(0, N_GAMMA, CHUNK):
        g_chunk = gammas[i:i+CHUNK]
        phase = np.outer(g_chunk, log_ns)
        sum_val = np.dot(np.exp(-1j * phase), w_shuf)
        F_null[i:i+CHUNK] = np.abs(sum_val)**2

    R_null = F_null / envelope
    null_cvs.append(np.std(R_null) / np.mean(R_null))
    null_means.append(np.mean(R_null))
    null_maxmin.append(np.max(R_null) / np.min(R_null))

    if (trial + 1) % 5 == 0:
        print(f"  trial {trial+1}/{N_SHUFFLE} done")
        sys.stdout.flush()

null_cvs = np.array(null_cvs)
null_means = np.array(null_means)
null_maxmin = np.array(null_maxmin)

real_cv = np.std(R) / np.mean(R)
print(f"\nNull distribution (weighted):")
print(f"  CV: real={real_cv:.6f}, null mean={np.mean(null_cvs):.6f} +/- {np.std(null_cvs):.6f}")
print(f"  z-score of real CV vs null: {(real_cv - np.mean(null_cvs))/np.std(null_cvs):.2f}")
print(f"  max/min: real={np.max(R)/np.min(R):.4f}, null mean={np.mean(null_maxmin):.4f}")
print(f"Weighted null took {time.time()-t0:.1f}s")
sys.stdout.flush()

# ── 8. UNWEIGHTED spectroscope ───────────────────────────────────────
print(f"\n=== UNWEIGHTED SPECTROSCOPE ===")
print("Computing F_u(gamma) = |sum mu(n) * exp(-ig*log(n))|^2 ...")
sys.stdout.flush()
t0 = time.time()

F_u = np.zeros(N_GAMMA)
for i in range(0, N_GAMMA, CHUNK):
    g_chunk = gammas[i:i+CHUNK]
    phase = np.outer(g_chunk, log_ns)
    sum_val = np.dot(np.exp(-1j * phase), mu_vals)
    F_u[i:i+CHUNK] = np.abs(sum_val)**2

print(f"F_u computed: {time.time()-t0:.2f}s")

# For unweighted, the expected envelope is different.
# sum mu(n) n^{-ig} relates to 1/zeta(ig), which has poles.
# Better to just test flatness directly and compare to null.
F_u_mean = np.mean(F_u)
F_u_cv = np.std(F_u) / F_u_mean
print(f"  mean(F_u) = {F_u_mean:.2f}")
print(f"  std(F_u)  = {np.std(F_u):.2f}")
print(f"  CV(F_u)   = {F_u_cv:.6f}")
print(f"  max/min   = {np.max(F_u)/np.min(F_u):.4f}")
sys.stdout.flush()

# ── 9. Null distribution (unweighted) ───────────────────────────────
print(f"\nComputing {N_SHUFFLE} null trials (unweighted)...")
sys.stdout.flush()
t0 = time.time()

null_u_cvs = []
null_u_maxmin = []

for trial in range(N_SHUFFLE):
    mu_shuf = mu_vals.copy()
    rng.shuffle(mu_shuf)

    F_null_u = np.zeros(N_GAMMA)
    for i in range(0, N_GAMMA, CHUNK):
        g_chunk = gammas[i:i+CHUNK]
        phase = np.outer(g_chunk, log_ns)
        sum_val = np.dot(np.exp(-1j * phase), mu_shuf)
        F_null_u[i:i+CHUNK] = np.abs(sum_val)**2

    null_u_cvs.append(np.std(F_null_u) / np.mean(F_null_u))
    null_u_maxmin.append(np.max(F_null_u) / np.min(F_null_u))

    if (trial + 1) % 5 == 0:
        print(f"  trial {trial+1}/{N_SHUFFLE} done")
        sys.stdout.flush()

null_u_cvs = np.array(null_u_cvs)
null_u_maxmin = np.array(null_u_maxmin)

print(f"\nNull distribution (unweighted):")
print(f"  CV: real={F_u_cv:.6f}, null mean={np.mean(null_u_cvs):.6f} +/- {np.std(null_u_cvs):.6f}")
print(f"  z-score of real CV vs null: {(F_u_cv - np.mean(null_u_cvs))/np.std(null_u_cvs):.2f}")
print(f"  max/min: real={np.max(F_u)/np.min(F_u):.4f}, null mean={np.mean(null_u_maxmin):.4f}")
print(f"Unweighted null took {time.time()-t0:.1f}s")
sys.stdout.flush()

# ── 10. Correlation of R with known zeta features ────────────────────
# Check if R correlates with known zeta zeros
known_zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
               37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
               52.970321, 56.446248, 59.347044]

print(f"\n=== R(gamma) near known zeta zeros ===")
for z in known_zeros:
    if GAMMA_MIN <= z <= GAMMA_MAX:
        idx = np.argmin(np.abs(gammas - z))
        # Average R in a small window around zero
        window = 5  # points
        lo, hi = max(0, idx - window), min(N_GAMMA, idx + window + 1)
        R_local = np.mean(R[lo:hi])
        print(f"  zero={z:.3f}: R_local={R_local:.6f} (vs mean {np.mean(R):.6f})")

# ── 11. Final verdict ────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"VERDICT")
print(f"{'='*60}")

# Criteria for Chowla consistency:
# 1. CV of R should be comparable to null
# 2. z-score should be within [-3, 3]
# 3. No extreme peaks

z_weighted = (real_cv - np.mean(null_cvs)) / np.std(null_cvs)
z_unweighted = (F_u_cv - np.mean(null_u_cvs)) / np.std(null_u_cvs)

print(f"\nWeighted (normalized) spectroscope:")
print(f"  CV(R) = {real_cv:.6f}")
print(f"  z-score vs null: {z_weighted:.2f}")
if abs(z_weighted) < 3:
    print(f"  -> CONSISTENT with Chowla (z within 3 sigma)")
else:
    print(f"  -> ANOMALOUS (z outside 3 sigma) — possible Chowla tension")

print(f"\nUnweighted spectroscope:")
print(f"  CV(F_u) = {F_u_cv:.6f}")
print(f"  z-score vs null: {z_unweighted:.2f}")
if abs(z_unweighted) < 3:
    print(f"  -> CONSISTENT with Chowla (z within 3 sigma)")
else:
    print(f"  -> ANOMALOUS (z outside 3 sigma) — possible Chowla tension")

print(f"\nOverall: ", end="")
if abs(z_weighted) < 3 and abs(z_unweighted) < 3:
    print("NO evidence against Chowla conjecture after proper normalization.")
    print("Previous 'structure' was entirely the |1/zeta| envelope — expected.")
elif abs(z_weighted) >= 3 or abs(z_unweighted) >= 3:
    print("SOME anomaly detected — investigate further.")
    print("But check if it's a finite-N effect before claiming Chowla tension.")

print()
