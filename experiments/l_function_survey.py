#!/usr/bin/env python3
"""
L-function Spectroscope Survey
==============================
Extends the Farey spectroscope F(gamma) = |sum R(p) p^{-1/2-i*gamma}|^2
to Dirichlet L-functions using twisted spectroscopes:
    F_chi(gamma) = |sum chi(p) R(p) p^{-1/2-i*gamma}|^2

Scans primitive Dirichlet characters mod q for q=3..20, detects peaks,
and compares against known L-function zeros.
"""

import numpy as np
import csv
from scipy.signal import find_peaks
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import gcd
from itertools import product as iterproduct
import os
import time

# ── Configuration ──────────────────────────────────────────────────────────
INPUT_CSV = os.path.expanduser("~/Desktop/Farey-Local/experiments/R_bound_200K_output.csv")
OUTPUT_CSV = os.path.expanduser("~/Desktop/Farey-Local/experiments/l_function_survey_results.csv")
OUTPUT_FIG = os.path.expanduser("~/Desktop/Farey-Local/figures/l_function_survey_heatmap.png")

GAMMA_MIN, GAMMA_MAX = 5.0, 60.0
N_GAMMA = 15000
MODULI_FOR_PLOT = [3, 4, 5, 7, 8, 11, 12, 13]
PEAK_PROMINENCE_FACTOR = 3.0

# Known zeros of L(s, chi) for validation
KNOWN_ZEROS = {
    (1, 0): [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774],
    (3, 1): [8.040, 13.164, 17.727, 22.680, 25.855],
    (4, 1): [6.021, 10.244, 12.588, 16.131, 19.130, 21.022],
    (5, 1): [6.18, 8.72, 12.67, 16.38],
    (5, 2): [6.64, 9.83, 13.88],
    (7, 1): [4.13, 7.09, 9.53],
    (7, 2): [5.20, 8.06, 10.25],
    (8, 1): [4.38, 7.47, 9.90],
    (8, 2): [6.021, 10.244, 12.588],
}

# ── Data loading ──────────────────────────────────────────────────────────

def load_data(path):
    """Load R(p) data, skipping first 2 status lines."""
    primes = []
    R_vals = []
    M_vals = []
    with open(path, 'r') as f:
        # Skip 2 status lines
        next(f)
        next(f)
        reader = csv.DictReader(f)
        for row in reader:
            primes.append(float(row['p']))
            R_vals.append(float(row['R']))
            M_vals.append(int(row['M_p']))
    return np.array(primes), np.array(R_vals), np.array(M_vals)


# ── Character construction ──────────────────────────────────────────────────

def euler_totient(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def primitive_root(n):
    if n <= 1:
        return None
    if n == 2:
        return 1
    if n == 4:
        return 3
    phi = euler_totient(n)
    phi_factors = []
    temp = phi
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            phi_factors.append(p)
            while temp % p == 0:
                temp //= p
        p += 1
    if temp > 1:
        phi_factors.append(temp)
    for g in range(2, n):
        if gcd(g, n) != 1:
            continue
        if all(pow(g, phi // pf, n) != 1 for pf in phi_factors):
            return g
    return None


def discrete_log_table(n, g):
    phi = euler_totient(n)
    dlog = {}
    val = 1
    for k in range(phi):
        dlog[val] = k
        val = (val * g) % n
    return dlog


def _factor_prime_powers(n):
    factors = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            pk = 1
            while n % p == 0:
                pk *= p
                n //= p
            factors.append(pk)
        p += 1
    if n > 1:
        factors.append(n)
    return factors


def _decompose_2k(n, q, half):
    pow5 = {}
    val = 1
    for b in range(half):
        pow5[val] = b
        val = (val * 5) % q
    nm = n % q
    if nm in pow5:
        return 0, pow5[nm]
    nm2 = (-n) % q
    if nm2 in pow5:
        return 1, pow5[nm2]
    return 0, 0


def _characters_2k(q):
    k = 0
    temp = q
    while temp > 1:
        temp //= 2
        k += 1
    phi = q // 2
    half = max(phi // 2, 1)
    characters = []
    for sign_bit in range(2):
        for j in range(half):
            chi = {}
            omega = np.exp(2j * np.pi * j / half) if half > 1 else 1.0
            sign_val = (-1.0) ** sign_bit
            for n in range(q):
                if gcd(n, q) != 1:
                    chi[n] = 0.0 + 0.0j
                else:
                    a, b = _decompose_2k(n % q, q, half)
                    chi[n] = (sign_val ** a) * (omega ** b)
            characters.append(chi)
    return characters


def get_all_characters(q):
    if q == 1:
        return [{}]
    phi = euler_totient(q)
    g = primitive_root(q)
    if g is not None:
        dlog = discrete_log_table(q, g)
        characters = []
        for j in range(phi):
            chi = {}
            omega = np.exp(2j * np.pi * j / phi)
            for n in range(q):
                if gcd(n, q) != 1:
                    chi[n] = 0.0 + 0.0j
                else:
                    chi[n] = omega ** dlog[n]
            characters.append(chi)
        return characters
    return _characters_via_crt(q)


def _characters_via_crt(q):
    ppowers = _factor_prime_powers(q)
    if len(ppowers) == 1:
        return _characters_2k(q)
    char_lists = [get_all_characters(pk) for pk in ppowers]
    characters = []
    for combo in iterproduct(*char_lists):
        chi = {}
        for n in range(q):
            if gcd(n, q) != 1:
                chi[n] = 0.0 + 0.0j
            else:
                val = 1.0 + 0.0j
                for i, pk in enumerate(ppowers):
                    val *= combo[i][n % pk]
                chi[n] = val
        characters.append(chi)
    return characters


def is_principal(chi_dict, q):
    for n in range(1, q):
        if gcd(n, q) == 1:
            val = chi_dict.get(n % q, 0)
            if abs(val - 1.0) > 1e-8:
                return False
    return True


def is_primitive_character(chi_dict, q):
    if q <= 1:
        return True
    primes_of_q = []
    temp = q
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            primes_of_q.append(p)
            while temp % p == 0:
                temp //= p
        p += 1
    if temp > 1:
        primes_of_q.append(temp)
    for p in primes_of_q:
        q_over_p = q // p
        found = False
        for n in range(1, q):
            # n ≡ 1 (mod q/p): when q/p=1, all n satisfy this
            if (n - 1) % q_over_p == 0 and gcd(n, q) == 1 and n != 1:
                val = chi_dict.get(n % q, 0)
                if abs(val) > 0.5 and abs(val - 1.0) > 1e-8:
                    found = True
                    break
        if not found:
            return False
    return True


def character_order(chi_dict, q):
    phi = euler_totient(q)
    for n in range(2, q):
        if gcd(n, q) == 1:
            val = chi_dict.get(n % q, 0)
            if abs(val) > 0.5 and abs(val - 1.0) > 1e-8:
                for k in range(1, phi + 1):
                    if abs(val**k - 1.0) < 1e-8:
                        return k
    return 1


# ── Spectroscope computation (vectorized) ────────────────────────────────

def compute_spectroscope(primes, R_vals, gammas, chi_func=None):
    """
    Vectorized: F_chi(gamma) = |sum chi(p) R(p) p^{-1/2 - i*gamma}|^2
    Uses matrix multiplication: phases[i,j] = exp(-i * gamma_i * log(p_j))
    """
    log_p = np.log(primes)  # shape (N_primes,)

    if chi_func is not None:
        chi_vals = np.array([chi_func(int(p)) for p in primes], dtype=complex)
        coeffs = (R_vals * chi_vals) / np.sqrt(primes)
    else:
        coeffs = R_vals / np.sqrt(primes)

    # Phase matrix: shape (N_gamma, N_primes)
    # phases[i,j] = exp(-1j * gammas[i] * log_p[j])
    # Do in chunks to limit memory (~6300 primes * 15000 gammas * 16 bytes ~ 1.5 GB)
    CHUNK = 3000
    F = np.zeros(len(gammas))
    S = np.zeros(len(gammas), dtype=complex)
    for start in range(0, len(primes), CHUNK):
        end = min(start + CHUNK, len(primes))
        # outer product: gammas[:, None] * log_p[None, start:end]
        phase_mat = np.exp(-1j * gammas[:, None] * log_p[None, start:end])
        S += phase_mat @ coeffs[start:end]

    F = np.abs(S) ** 2
    return F


def find_spectroscope_peaks(gammas, F, prominence_factor=3.0):
    median_F = np.median(F)
    if median_F < 1e-15:
        median_F = np.mean(F) + 1e-15
    prominence = prominence_factor * median_F
    peaks, _ = find_peaks(F, prominence=prominence, distance=5)
    return gammas[peaks], F[peaks], median_F


def match_peaks_to_zeros(peak_gammas, known_zeros, tolerance=0.5):
    matches = []
    for z in known_zeros:
        if len(peak_gammas) == 0:
            break
        dists = np.abs(peak_gammas - z)
        best = np.argmin(dists)
        if dists[best] < tolerance:
            matches.append((peak_gammas[best], z, dists[best]))
    return matches


# ── CSV output ──────────────────────────────────────────────────────────

def save_results_csv(results, path):
    fields = ['q', 'chi_index', 'is_primitive', 'order', 'is_principal',
              'num_peaks', 'first_peak', 'snr', 'max_peak_height',
              'peaks_matched', 'peak_positions']
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()

    # 1. Load data
    print("Loading R(p) data...")
    primes, R_vals, M_vals = load_data(INPUT_CSV)
    print(f"  Loaded {len(primes)} qualifying primes, "
          f"p in [{int(primes[0])}, {int(primes[-1])}]")

    # 2. Gamma grid
    gammas = np.linspace(GAMMA_MIN, GAMMA_MAX, N_GAMMA)

    # 3. Baseline: untwisted spectroscope
    print("\nComputing baseline (untwisted) spectroscope...")
    t1 = time.time()
    F_zeta = compute_spectroscope(primes, R_vals, gammas)
    print(f"  Done in {time.time()-t1:.1f}s")

    peaks_zeta, heights_zeta, median_zeta = find_spectroscope_peaks(gammas, F_zeta)
    snr_zeta = np.max(F_zeta) / median_zeta if median_zeta > 0 else 0

    print(f"  Baseline: {len(peaks_zeta)} peaks, SNR = {snr_zeta:.1f}")
    if len(peaks_zeta) > 0:
        matches = match_peaks_to_zeros(peaks_zeta, KNOWN_ZEROS.get((1, 0), []))
        print(f"  Matched {len(matches)} known zeta zeros:")
        for pg, kz, d in matches:
            print(f"    peak {pg:.3f} <-> zero {kz:.3f}  (delta = {d:.3f})")

    # 4. Survey characters mod q = 3..20
    results = []
    results.append({
        'q': 1, 'chi_index': 0, 'is_primitive': True, 'order': 1,
        'is_principal': True,
        'num_peaks': len(peaks_zeta),
        'first_peak': f'{peaks_zeta[0]:.4f}' if len(peaks_zeta) > 0 else '',
        'snr': f'{snr_zeta:.2f}',
        'max_peak_height': f'{np.max(F_zeta):.4f}',
        'peaks_matched': len(match_peaks_to_zeros(peaks_zeta, KNOWN_ZEROS.get((1, 0), []))),
        'peak_positions': ';'.join(f'{g:.3f}' for g in peaks_zeta[:10]),
    })

    spectroscope_data = {(1, 0): F_zeta}
    total_chars = 0

    for q in range(3, 21):
        print(f"\nProcessing q = {q}...")
        chars = get_all_characters(q)
        phi_q = euler_totient(q)
        print(f"  phi({q}) = {phi_q}, generated {len(chars)} characters")

        chi_idx = 0
        for ci, chi_dict in enumerate(chars):
            if is_principal(chi_dict, q):
                continue
            chi_idx += 1
            total_chars += 1

            prim = is_primitive_character(chi_dict, q)
            order = character_order(chi_dict, q)

            def make_chi(cd, mod):
                def chi_func(p):
                    if p % mod == 0:
                        return 0.0 + 0.0j
                    return cd[p % mod]
                return chi_func

            chi_f = make_chi(chi_dict, q)

            t1 = time.time()
            F_chi = compute_spectroscope(primes, R_vals, gammas, chi_func=chi_f)
            dt = time.time() - t1

            peak_g, peak_h, med = find_spectroscope_peaks(gammas, F_chi, PEAK_PROMINENCE_FACTOR)
            snr = np.max(F_chi) / med if med > 0 else 0

            key = (q, chi_idx)
            known = KNOWN_ZEROS.get(key, [])
            n_matched = len(match_peaks_to_zeros(peak_g, known)) if known else 0

            prim_str = "PRIM" if prim else "ind "
            print(f"  chi_{chi_idx} (ord {order}, {prim_str}): "
                  f"{len(peak_g):2d} peaks, SNR={snr:6.1f}, "
                  f"{dt:.1f}s"
                  + (f"  [{n_matched}/{len(known)} zeros matched]" if known else ""))

            results.append({
                'q': q, 'chi_index': chi_idx, 'is_primitive': prim, 'order': order,
                'is_principal': False,
                'num_peaks': len(peak_g),
                'first_peak': f'{peak_g[0]:.4f}' if len(peak_g) > 0 else '',
                'snr': f'{snr:.2f}',
                'max_peak_height': f'{np.max(F_chi):.4f}',
                'peaks_matched': n_matched,
                'peak_positions': ';'.join(f'{g:.3f}' for g in peak_g[:10]),
            })

            if q in MODULI_FOR_PLOT:
                spectroscope_data[(q, chi_idx)] = F_chi

    # 5. Save results
    save_results_csv(results, OUTPUT_CSV)
    print(f"\nResults saved to {OUTPUT_CSV}")
    print(f"Total non-principal characters surveyed: {total_chars}")

    # Summary stats
    snr_vals = [float(r['snr']) for r in results if not r['is_principal']]
    peak_counts = [r['num_peaks'] for r in results if not r['is_principal']]
    prim_snrs = [float(r['snr']) for r in results if r['is_primitive'] and not r['is_principal']]
    print(f"\nAll non-principal: mean peaks = {np.mean(peak_counts):.1f}, "
          f"mean SNR = {np.mean(snr_vals):.1f}")
    if prim_snrs:
        print(f"Primitive only:    mean SNR = {np.mean(prim_snrs):.1f}, "
              f"max SNR = {np.max(prim_snrs):.1f}")

    # 6. Multi-panel figure
    print("\nGenerating multi-panel figure...")
    fig, axes = plt.subplots(4, 2, figsize=(16, 20))
    fig.suptitle('Farey L-function Spectroscope Survey\n'
                 r'$F_\chi(\gamma) = |\sum \chi(p)\,R(p)\,p^{-1/2-i\gamma}|^2$',
                 fontsize=16, fontweight='bold')

    for ax_idx, q in enumerate(MODULI_FOR_PLOT):
        ax = axes[ax_idx // 2, ax_idx % 2]
        color_cycle = plt.cm.tab10(np.linspace(0, 1, 10))

        chi_keys = sorted([k for k in spectroscope_data if k[0] == q], key=lambda x: x[1])

        if not chi_keys:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                    ha='center', va='center', fontsize=14)
        else:
            for ci, key in enumerate(chi_keys):
                F = spectroscope_data[key]
                label = f'$\\chi_{{{key[1]}}}$'
                ax.plot(gammas, F, alpha=0.8, linewidth=0.7,
                        color=color_cycle[ci % 10], label=label)

        # Known L-function zeros for this modulus (red dashed)
        for key_z in KNOWN_ZEROS:
            if key_z[0] == q:
                for z in KNOWN_ZEROS[key_z]:
                    if GAMMA_MIN <= z <= GAMMA_MAX:
                        ax.axvline(z, color='red', linestyle='--',
                                   alpha=0.6, linewidth=0.8)

        # Zeta zeros for reference (gray dotted)
        for z in KNOWN_ZEROS.get((1, 0), []):
            if GAMMA_MIN <= z <= GAMMA_MAX:
                ax.axvline(z, color='gray', linestyle=':', alpha=0.25, linewidth=0.5)

        ax.set_title(f'mod {q}', fontsize=13, fontweight='bold')
        ax.set_xlabel('$\\gamma$', fontsize=11)
        ax.set_ylabel('$F_\\chi(\\gamma)$', fontsize=11)
        if chi_keys:
            ax.legend(fontsize=8, loc='upper right')
        ax.set_xlim(GAMMA_MIN, GAMMA_MAX)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    os.makedirs(os.path.dirname(OUTPUT_FIG), exist_ok=True)
    fig.savefig(OUTPUT_FIG, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure saved to {OUTPUT_FIG}")

    elapsed = time.time() - t0
    print(f"\nTotal runtime: {elapsed:.1f}s")

    # Summary table
    print("\n" + "=" * 90)
    print("SUMMARY: L-function Spectroscope Survey")
    print("=" * 90)
    print(f"{'q':>3} {'chi':>4} {'prim':>5} {'ord':>4} {'peaks':>6} "
          f"{'1st_peak':>9} {'SNR':>8} {'matched':>8}")
    print("-" * 90)
    for row in results:
        fp = row['first_peak']
        fp_str = f"{float(fp):9.3f}" if fp else "      N/A"
        print(f"{row['q']:3d} {row['chi_index']:4d} "
              f"{'Y' if row['is_primitive'] else 'N':>5} "
              f"{row['order']:4d} "
              f"{row['num_peaks']:6d} "
              f"{fp_str} "
              f"{float(row['snr']):8.1f} "
              f"{row['peaks_matched']:8d}")


if __name__ == '__main__':
    main()
