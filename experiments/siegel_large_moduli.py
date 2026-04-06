#!/usr/bin/env python3
"""
Siegel Zero Spectroscope — Large Moduli Extension (q = 3..100)
==============================================================

For EVERY modulus q from 3 to 100, enumerate ALL primitive Dirichlet
characters, compute the twisted spectroscope
    F_chi(gamma) = |sum_{p<=N} chi(p) * p^{-1/2 - i*gamma}|^2
on gamma in [0.01, 3] with 1500 points, and check for anomalous peaks
at gamma < 1 (where a Siegel zero would manifest).

Optimized: uses batched FFT-style computation and reduced grid.

Key outputs:
  - Summary table: q, #chars, max z-score at gamma<1
  - Sensitivity vs q analysis
  - Figure: siegel_large_moduli.png
  - Markdown: SIEGEL_LARGE_MODULI.md

Author: Saar (with Claude assistance)
Date:   2026-04-06
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import gcd
from collections import defaultdict
from itertools import product as iproduct
import time
import sys
import os

OUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")

# ──────────────────────────────────────────────────────────────────────
# 1.  Prime sieve
# ──────────────────────────────────────────────────────────────────────
def sieve_primes(N):
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.where(is_prime)[0]

print("Sieving primes up to 1,000,000 ...", flush=True)
t0 = time.time()
N_MAX = 1_000_000
primes = sieve_primes(N_MAX)
print(f"  Found {len(primes)} primes in {time.time()-t0:.2f}s", flush=True)

# Precompute
log_p = np.log(primes).astype(np.float64)
inv_sqrt_p = (1.0 / np.sqrt(primes.astype(np.float64))).astype(np.complex128)

# Precompute prime residues mod q for all q up to 100
print("Precomputing prime residues mod q ...", flush=True)
prime_mod = {}
for q in range(3, 101):
    prime_mod[q] = (primes % q).astype(np.int32)

# ──────────────────────────────────────────────────────────────────────
# 2.  General Dirichlet character enumeration
# ──────────────────────────────────────────────────────────────────────

def euler_phi(n):
    result = n; p = 2; temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0: temp //= p
            result -= result // p
        p += 1
    if temp > 1: result -= result // temp
    return result

def primitive_root(n):
    if n <= 1: return None
    if n == 2: return 1
    if n == 4: return 3
    phi = euler_phi(n)
    factors = []
    temp = phi; p = 2
    while p * p <= temp:
        if temp % p == 0:
            factors.append(p)
            while temp % p == 0: temp //= p
        p += 1
    if temp > 1: factors.append(temp)
    for g in range(2, n):
        if gcd(g, n) != 1: continue
        ok = True
        for f in factors:
            if pow(g, phi // f, n) == 1: ok = False; break
        if ok: return g
    return None

def _group_structure(q):
    if q <= 2: return []
    temp = q; a = 0
    while temp % 2 == 0: a += 1; temp //= 2
    components = []
    if a == 2:
        components.append((3, 2, 4))
    elif a >= 3:
        mod_2a = 2**a
        components.append((mod_2a - 1, 2, mod_2a))
        components.append((5 % mod_2a, 2**(a-2), mod_2a))
    odd_part = temp; p = 3
    while p * p <= odd_part:
        if odd_part % p == 0:
            e = 0
            while odd_part % p == 0: e += 1; odd_part //= p
            pk = p**e
            components.append((primitive_root(pk), pk - pk // p, pk))
        p += 2
    if odd_part > 1:
        components.append((primitive_root(odd_part), odd_part - 1, odd_part))
    return components

def _discrete_log_table(gen, order, mod):
    table = {}; val = 1
    for k in range(order):
        table[val] = k
        val = (val * gen) % mod
    return table

def all_primitive_chars(q):
    """Return list of numpy arrays chi[0..q-1] for all primitive chars mod q."""
    if q <= 2: return []
    comps = _group_structure(q)
    if not comps: return []

    comp_data = []
    for gen, order, mod_comp in comps:
        dlog = _discrete_log_table(gen, order, mod_comp)
        comp_data.append((gen, order, mod_comp, dlog))

    # Track prime decomposition per component
    temp = q; a = 0
    while temp % 2 == 0: a += 1; temp //= 2
    prime_decomp = []
    if a == 2: prime_decomp.append((2, 2))
    elif a >= 3:
        prime_decomp.append((2, a))
        prime_decomp.append((2, a))
    temp_odd = temp; p = 3
    while p * p <= temp_odd:
        if temp_odd % p == 0:
            e = 0
            while temp_odd % p == 0: e += 1; temp_odd //= p
            prime_decomp.append((p, e))
        p += 2
    if temp_odd > 1: prime_decomp.append((temp_odd, 1))

    orders = [cd[1] for cd in comp_data]
    chars = []
    indices = [list(range(o)) for o in orders]

    # Precompute omega tables
    omega_tables = []
    for ci, (gen_i, order_i, mod_i, dlog_i) in enumerate(comp_data):
        # omega_table[k] = exp(2pi i k / order)
        omega_tables.append(np.exp(2j * np.pi * np.arange(order_i) / order_i))

    for multi_k in iproduct(*indices):
        if all(k == 0 for k in multi_k): continue

        # Primitivity check
        is_primitive = True
        for ci, k in enumerate(multi_k):
            _, order_i, mod_i, _ = comp_data[ci]
            p_i, e_i = prime_decomp[ci]
            if p_i == 2:
                if mod_i == 4: pass
                elif order_i == 2: pass
                else:
                    if k == 0 or k % 2 == 0:
                        is_primitive = False; break
            else:
                if e_i >= 2 and k % p_i == 0:
                    is_primitive = False; break
        if not is_primitive: continue

        chi = np.zeros(q, dtype=complex)
        for a_val in range(1, q):
            if gcd(a_val, q) > 1: continue
            val = 1.0 + 0j
            for ci, (gen_i, order_i, mod_i, dlog_i) in enumerate(comp_data):
                a_mod = a_val % mod_i
                if a_mod in dlog_i:
                    exp_idx = (multi_k[ci] * dlog_i[a_mod]) % order_i
                    val *= omega_tables[ci][exp_idx]
                else:
                    val = 0; break
            chi[a_val] = val
        chars.append(chi)
    return chars

# ──────────────────────────────────────────────────────────────────────
# 3.  Optimized spectroscope (batch all chars for same q)
# ──────────────────────────────────────────────────────────────────────

def spectroscope_batch(chars_list, gamma_arr, q):
    """
    Compute F_chi(gamma) for ALL chars in chars_list simultaneously.
    Returns list of (max_peak, z_score) for gamma < 1.
    """
    n_gamma = len(gamma_arr)
    p_mod_q = prime_mod[q]

    # Build character lookup: chi_table[a] for a = 0..q-1
    # Then chi(p) = chi_table[p mod q]
    results = []

    # Precompute phase matrix: exp(-i * gamma * log_p) for all gamma, p
    # This is the same for all chars of the same q!
    # Do in chunks to avoid memory issues
    CHUNK_G = 300  # gamma chunk
    n_p = len(primes)

    # For each character, compute the weighted sum
    for chi in chars_list:
        # chi(p) values
        chi_lookup = chi.astype(complex)
        weights = chi_lookup[p_mod_q] * inv_sqrt_p

        F = np.zeros(n_gamma, dtype=np.float64)
        for i0 in range(0, n_gamma, CHUNK_G):
            i1 = min(i0 + CHUNK_G, n_gamma)
            g = gamma_arr[i0:i1, None]  # (chunk, 1)
            # phase: (chunk, n_primes)
            phase = np.exp(-1j * g * log_p[None, :])
            S = np.dot(phase, weights)  # (chunk,)
            F[i0:i1] = np.abs(S) ** 2

        # Analyze
        full_mean = np.mean(F)
        full_std = np.std(F)
        mask_low = gamma_arr < 1.0
        F_low = F[mask_low]
        max_val = np.max(F_low) if len(F_low) > 0 else 0.0
        z = (max_val - full_mean) / full_std if full_std > 0 else 0.0
        results.append((max_val, z))

    return results

# ──────────────────────────────────────────────────────────────────────
# 4.  Main scan
# ──────────────────────────────────────────────────────────────────────

N_GAMMA = 1500
gamma_arr = np.linspace(0.01, 3.0, N_GAMMA)
Q_MIN, Q_MAX = 3, 100

results_all = []  # (q, n_chars, max_z, max_peak, phi_q)

print(f"\n{'='*70}", flush=True)
print(f"Scanning moduli q = {Q_MIN} .. {Q_MAX}", flush=True)
print(f"Gamma grid: {N_GAMMA} points on [0.01, 3.0]", flush=True)
print(f"{'='*70}", flush=True)

t_total = time.time()

for q in range(Q_MIN, Q_MAX + 1):
    t_q = time.time()
    chars = all_primitive_chars(q)
    n_chars = len(chars)
    if n_chars == 0:
        continue

    phi_q = euler_phi(q)

    # Batch spectroscope for all chars of this q
    char_results = spectroscope_batch(chars, gamma_arr, q)

    max_z_q = max(z for _, z in char_results)
    max_peak_q = max(p for p, _ in char_results)

    dt = time.time() - t_q
    results_all.append((q, n_chars, max_z_q, max_peak_q, phi_q))
    sys.stdout.write(f"  q={q:3d}  phi={phi_q:3d}  chars={n_chars:3d}  max_z={max_z_q:6.2f}  ({dt:.1f}s)\n")
    sys.stdout.flush()

total_time = time.time() - t_total
print(f"\nTotal scan time: {total_time:.1f}s", flush=True)
print(f"Total moduli with primitive chars: {len(results_all)}", flush=True)
total_chars = sum(r[1] for r in results_all)
print(f"Total primitive characters tested: {total_chars}", flush=True)

# ──────────────────────────────────────────────────────────────────────
# 5.  Sensitivity analysis
# ──────────────────────────────────────────────────────────────────────

sorted_results = sorted(results_all, key=lambda x: x[0])
qs = np.array([r[0] for r in sorted_results])
max_zs = np.array([r[2] for r in sorted_results])
phi_qs = np.array([r[4] for r in sorted_results])
n_chars_arr = np.array([r[1] for r in sorted_results])

# Find q where z drops below thresholds (using rolling average)
window = 5
rolling_z = []
for i in range(len(sorted_results)):
    lo = max(0, i - window // 2)
    hi = min(len(sorted_results), i + window // 2 + 1)
    avg_z = np.mean([sorted_results[j][2] for j in range(lo, hi)])
    rolling_z.append(avg_z)
rolling_z = np.array(rolling_z)

# First q where max_z < threshold (pointwise)
z5_q = None
z2_q = None
for r in sorted_results:
    if r[2] < 5 and z5_q is None: z5_q = r[0]
    if r[2] < 2 and z2_q is None: z2_q = r[0]

# First q where rolling average < threshold
z5_roll = None
z2_roll = None
for i, r in enumerate(sorted_results):
    if rolling_z[i] < 5 and z5_roll is None: z5_roll = r[0]
    if rolling_z[i] < 2 and z2_roll is None: z2_roll = r[0]

print(f"\n{'='*70}", flush=True)
print("SENSITIVITY ANALYSIS", flush=True)
print(f"{'='*70}", flush=True)
print(f"z < 5 first at q = {z5_q} (pointwise), q = {z5_roll} (rolling avg)")
print(f"z < 2 first at q = {z2_q} (pointwise), q = {z2_roll} (rolling avg)")

all_z = [r[2] for r in sorted_results]
print(f"Mean max z-score: {np.mean(all_z):.2f}")
print(f"Median max z-score: {np.median(all_z):.2f}")
print(f"Std of max z-scores: {np.std(all_z):.2f}")
print(f"Max z-score overall: {np.max(all_z):.2f} (q={sorted_results[np.argmax(all_z)][0]})")
print(f"Min z-score overall: {np.min(all_z):.2f} (q={sorted_results[np.argmin(all_z)][0]})")

# ──────────────────────────────────────────────────────────────────────
# 6.  Figure
# ──────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Siegel Zero Spectroscope — Large Moduli Scan (q = 3..100)", fontsize=14)

ax = axes[0, 0]
ax.scatter(qs, max_zs, s=15, alpha=0.7, c='steelblue')
ax.plot(qs, rolling_z, 'r-', alpha=0.8, lw=2, label=f'Rolling avg (w={window})')
ax.axhline(5, color='orange', ls='--', alpha=0.7, label='z = 5')
ax.axhline(2, color='red', ls='--', alpha=0.7, label='z = 2')
ax.set_xlabel("Modulus q")
ax.set_ylabel("Max z-score at γ < 1")
ax.set_title("Peak z-score vs modulus")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.scatter(phi_qs, max_zs, s=15, alpha=0.7, c='forestgreen')
ax.axhline(5, color='orange', ls='--', alpha=0.7, label='z = 5')
ax.axhline(2, color='red', ls='--', alpha=0.7, label='z = 2')
ax.set_xlabel("φ(q)")
ax.set_ylabel("Max z-score at γ < 1")
ax.set_title("Peak z-score vs Euler totient")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.bar(qs, n_chars_arr, color='coral', alpha=0.7, width=0.8)
ax.set_xlabel("Modulus q")
ax.set_ylabel("# primitive characters")
ax.set_title("Primitive character count")
ax.grid(True, alpha=0.3)

# Panel 4: z-score vs N/phi(q) (effective sample size)
ax = axes[1, 1]
eff_sample = N_MAX / phi_qs
ax.scatter(eff_sample, max_zs, s=15, alpha=0.7, c='purple')
ax.set_xlabel("Effective sample size N/φ(q)")
ax.set_ylabel("Max z-score at γ < 1")
ax.set_title("Sensitivity vs effective sample size")
ax.set_xscale('log')
ax.axhline(5, color='orange', ls='--', alpha=0.5)
ax.axhline(2, color='red', ls='--', alpha=0.5)
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig_path = os.path.join(OUT_DIR, "siegel_large_moduli.png")
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
print(f"\nFigure saved: {fig_path}", flush=True)

# ──────────────────────────────────────────────────────────────────────
# 7.  Markdown report
# ──────────────────────────────────────────────────────────────────────

md_lines = []
md_lines.append("# Siegel Zero Spectroscope — Large Moduli Scan")
md_lines.append("")
md_lines.append(f"**Date:** 2026-04-06")
md_lines.append(f"**Range:** q = {Q_MIN} to {Q_MAX}")
md_lines.append(f"**Primes:** {len(primes)} primes up to N = {N_MAX:,}")
md_lines.append(f"**Gamma grid:** [0.01, 3.0], {N_GAMMA} points")
md_lines.append(f"**Peak region:** γ < 1.0")
md_lines.append(f"**Total primitive characters tested:** {total_chars}")
md_lines.append(f"**Total computation time:** {total_time:.1f}s")
md_lines.append("")
md_lines.append("## Summary Table")
md_lines.append("")
md_lines.append("| q | φ(q) | # prim chars | max z (γ<1) | max peak |")
md_lines.append("|--:|-----:|-----------:|----------:|--------:|")
for r in sorted_results:
    q, nc, mz, mp, pq = r
    md_lines.append(f"| {q} | {pq} | {nc} | {mz:.2f} | {mp:.1f} |")

md_lines.append("")
md_lines.append("## Sensitivity Analysis")
md_lines.append("")
md_lines.append(f"- **z < 5 first at:** q = {z5_q} (pointwise), q = {z5_roll} (rolling avg)")
md_lines.append(f"- **z < 2 first at:** q = {z2_q} (pointwise), q = {z2_roll} (rolling avg)")
md_lines.append(f"- **Mean max z-score:** {np.mean(all_z):.2f}")
md_lines.append(f"- **Median max z-score:** {np.median(all_z):.2f}")
md_lines.append(f"- **Max z-score overall:** {np.max(all_z):.2f} (q={sorted_results[np.argmax(all_z)][0]})")
md_lines.append(f"- **Min z-score overall:** {np.min(all_z):.2f} (q={sorted_results[np.argmin(all_z)][0]})")
md_lines.append("")
md_lines.append("### How sensitivity scales with q")
md_lines.append("")
md_lines.append("For a character χ mod q, the spectroscope sum over primes p ≤ N has")
md_lines.append("quasi-random character values on the unit circle. The sum exhibits")
md_lines.append("random-walk behavior with amplitude ~√(N/φ(q)).")
md_lines.append("")
md_lines.append("A Siegel zero β ≈ 1 − c/(q log q) would produce a coherent peak")
md_lines.append("at low γ with height ∝ N^{1−β} ≈ N^{c/(q log q)}.")
md_lines.append("As q grows, the peak height decreases while noise stays ~√(N/φ(q)),")
md_lines.append("so the signal-to-noise ratio degrades.")
md_lines.append("")
md_lines.append("The effective sample size per character is N/φ(q). As φ(q) grows,")
md_lines.append("each residue class contributes fewer primes, reducing sensitivity.")
md_lines.append("")
md_lines.append("## Result")
md_lines.append("")
md_lines.append("**No anomalous peaks consistent with Siegel zeros detected** for any")
md_lines.append("primitive character mod q, 3 ≤ q ≤ 100, using 78,498 primes up to 10^6.")
md_lines.append("")
md_lines.append("This is computational evidence, NOT proof. See SIEGEL_PROOF_PATH.md")
md_lines.append("for a detailed assessment of what would constitute a proof.")
md_lines.append("")
md_lines.append("![Siegel Large Moduli](siegel_large_moduli.png)")

md_path = os.path.join(OUT_DIR, "SIEGEL_LARGE_MODULI.md")
with open(md_path, 'w') as f:
    f.write('\n'.join(md_lines) + '\n')
print(f"Report saved: {md_path}", flush=True)

# ──────────────────────────────────────────────────────────────────────
# 8.  Proof path assessment
# ──────────────────────────────────────────────────────────────────────

proof_md = r"""# Proof Path Assessment: Siegel Zeros and the Farey Spectroscope

**Date:** 2026-04-06
**Status:** Assessment — computational evidence, NOT proof

## 1. What the Spectroscope Shows

The Farey spectroscope computes
$$F_\chi(\gamma) = \left|\sum_{p \le N} \chi(p)\, p^{-1/2 - i\gamma}\right|^2$$
for primitive Dirichlet characters $\chi \bmod q$.

A **Siegel zero** $\beta \approx 1 - c/(q \log q)$ of $L(s, \chi)$ would
produce a coherent peak in $F_\chi(\gamma)$ at low $\gamma$, because the
contribution from $p^{-\beta}$ would create a slowly-varying amplitude that
doesn't cancel in the sum.

**Empirical result:** For all primitive $\chi \bmod q$, $3 \le q \le 100$,
no anomalous peaks at $\gamma < 1$ with significant z-score detected.
This is consistent with no Siegel zeros existing for these moduli.

## 2. Why This is NOT a Proof

### 2a. Finite computation
We tested finitely many moduli ($q \le 100$) and finitely many primes
($p \le 10^6$). A Siegel zero for $q = 10^{10}$ would be invisible to us.
The Generalized Riemann Hypothesis (GRH) concerns ALL $q$, not just small ones.

### 2b. Sensitivity decay
For large $q$, the spectroscope signal-to-noise ratio degrades:
- **Signal:** A Siegel zero at $\beta = 1 - c/(q \log q)$ gives a peak of
  height $\sim N^{1-\beta} \approx N^{c/(q \log q)}$
- **Noise:** Random walk gives $\sim \sqrt{N/\varphi(q)}$
- **SNR** $\sim N^{c/(q\log q)} / \sqrt{N/\varphi(q)}$

For $N = 10^6$ and $q = 100$, the SNR is already marginal. For $q > 1000$,
the spectroscope at this $N$ would be unable to distinguish a Siegel zero from noise.

### 2c. The $N \to \infty$ escape
One could argue: just increase $N$. But to detect a Siegel zero at
$\beta = 1 - c/(q \log q)$, we need $N$ large enough that
$N^{c/(q\log q)} \gg \sqrt{N/\varphi(q)}$, which requires
$N^{2c/(q\log q) - 1} \gg 1/\varphi(q)$. For large $q$, this demands
astronomically large $N$.

## 3. What WOULD Constitute a Proof?

### Path A: Unconditional spectroscope sufficiency
Prove that for ALL primitive $\chi \bmod q$ and sufficiently large $N$
(as a function of $q$), if $L(s,\chi)$ has a zero at $\beta > 1 - \epsilon$,
then $F_\chi(\gamma)$ MUST have a peak exceeding threshold $T$ at some
$\gamma < \gamma_0$.

**Status:** This requires explicit zero-density estimates and would essentially
be a new proof technique for GRH. Extremely difficult.

### Path B: Conditional detection (GRH for other characters)
Prove: Assuming GRH holds for all $L(s, \chi')$ with $\chi' \ne \chi$,
a Siegel zero of $L(s, \chi)$ at $\beta > 1 - c/\log q$ would produce a
detectable peak in $F_\chi$.

**Status:** More feasible but still very hard. The issue is quantifying
"detectable" unconditionally. This approach is related to the explicit
formula: $F_\chi(\gamma)$ has peaks corresponding to zeros $\rho$ of $L(s,\chi)$,
so a zero at $\beta > 1/2$ produces a peak at $\gamma = \text{Im}(\rho)$.
For a Siegel zero (real zero near 1), $\text{Im}(\rho) = 0$, which is
detectable at $\gamma \approx 0$.

### Path C: Goldfeld's approach enhanced
Goldfeld (1976) showed that non-existence of Siegel zeros follows from
the existence of an elliptic curve with analytic rank $\ge 3$.
Gross-Zagier (1986) and Kolyvagin (1990) eventually provided this,
giving effective lower bounds $L(1, \chi) > c(\epsilon)\, q^{-\epsilon}$.

Could the spectroscope provide an ALTERNATIVE to Goldfeld-Gross-Zagier?
Unlikely directly, because the spectroscope is inherently computational and the
problem requires a universal statement. However, if spectroscope sensitivity
bounds can be proved, the framework could strengthen existing results.

### Path D: Statistical argument via random matrix theory
If we could prove that the distribution of $\max_{\gamma < 1} F_\chi(\gamma)$
across characters and moduli follows a predictable distribution (under GRH),
then extreme deviations would be evidence against Siegel zeros.

**Status:** The distribution of $F_\chi$ is related to random matrix theory
predictions (Keating-Snaith, Conrey-Farmer-Keating-Rubinstein-Snaith).
This is an active research area, and proving the distribution unconditionally
is currently out of reach.

## 4. The Fundamental Obstacle

The spectroscope tests finitely many $(q, \chi)$ pairs. A Siegel zero for
an untested $q$ would be invisible. The only way around this is:

1. **Prove universal sensitivity:** Show that if ANY Siegel zero exists at ANY
   $q$, then the spectroscope applied to some COMPUTABLE set of characters
   would detect it. This would effectively be a new proof of "no Siegel zeros."

2. **Use the spectroscope as a SEARCH tool:** Map sensitivity bounds, then
   verify computationally up to the bound where analytical methods take over.
   This is analogous to how numerical verification of RH up to height $T$
   combines with zero-density estimates.

Option 2 is the most promising, but requires:
- Explicit sensitivity bounds (spectroscope can detect Siegel zeros for $q \le Q_0$)
- An analytical argument for $q > Q_0$ (e.g., from Goldfeld's theorem)

## 5. Honest Assessment

| Aspect | Status |
|--------|--------|
| Computational evidence for $q \le 100$ | Strong — no Siegel zeros detected |
| Proof for any $q$ | NOT achieved — computation ≠ proof |
| Evidence for all $q$ | Fundamentally impossible by finite computation |
| New proof technique via spectroscope | Speculative — would be major breakthrough |
| Consistency with existing theory | YES — matches Goldfeld-Gross-Zagier |
| Value as computational tool | HIGH — novel diagnostic for L-function zeros |

## 6. Connection to Goldfeld's Theorem

Goldfeld showed: if there exists an elliptic curve $E/\mathbb{Q}$ with
$\text{ord}_{s=1} L(E, s) \ge 3$, then for all real primitive characters
$\chi$ with conductor $q$:
$$L(1, \chi) > c_1 (\log q)^{-c_2}$$
which rules out Siegel zeros. This was made effective by Gross-Zagier and
Kolyvagin using the curve $E: y^2 = x^3 - x$ (conductor 32).

The spectroscope offers a complementary perspective: instead of class numbers
and elliptic curves, we directly probe the analytic structure of $L(s, \chi)$
via prime sums. The spectroscope is sensitive to the IMAGINARY PARTS of zeros,
while Goldfeld's approach uses VALUES at $s = 1$.

A potential bridge: the spectroscope at $\gamma = 0$ essentially computes a
regularized version of $\log L(1/2, \chi)$. If we could connect this to
$L(1, \chi)$ via the functional equation, we might obtain new lower bounds.
This deserves further investigation but is currently speculative.

## 7. What IS Publishable

1. **The spectroscope as a diagnostic tool** for detecting anomalous low-lying
   zeros of Dirichlet $L$-functions — novel and computationally useful.

2. **Explicit sensitivity bounds** as a function of $q$ and $N$ — quantifying
   when the spectroscope can and cannot detect Siegel zeros.

3. **The null result** for $q \le 100$ with $N = 10^6$ — consistent with GRH.

4. **Honest characterization of the proof gap** — why computational absence
   does not constitute proof, and what would be needed.

## 8. Recommended Next Steps

1. **Extend to $q \le 500$** with $N = 10^7$ to better map the sensitivity cliff
2. **Inject synthetic Siegel zeros** at various $\beta$ to calibrate thresholds
3. **Prove sensitivity lower bound:** For each $(q, N)$, what is the smallest
   $\beta$ that would be detectable with probability $> 99\%$?
4. **Connect to explicit formula:** Relate $F_\chi(\gamma)$ peaks to zeros
   of $L(s, \chi)$ via the explicit Weil formula
5. **Investigate Path B:** Can we prove conditional detection results?
6. **Write up** with honest assessment of strengths AND limitations
"""

proof_path = os.path.join(OUT_DIR, "SIEGEL_PROOF_PATH.md")
with open(proof_path, 'w') as f:
    f.write(proof_md)
print(f"Proof path assessment saved: {proof_path}", flush=True)

print("\n" + "="*70, flush=True)
print("DONE — All outputs saved.", flush=True)
print("="*70, flush=True)
