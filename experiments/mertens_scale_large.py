#!/usr/bin/env python3
"""
Large-scale compensated Mertens spectroscope: 10M, 25M, 50M primes.

F_comp(gamma) = gamma^2 * |sum M(p)/p * exp(-i*gamma*log(p))|^2

Uses LOCAL z-scores for zero detection (peak vs background +-8, excluding
+-1.5 around all 20 known zeros).

Double-chunked computation to keep memory under control:
  gamma_chunk=500, prime_chunk=100000 => 500*100K*8 = 400MB per phase matrix.

Author: Saar (with Claude assistance)
"""
import numpy as np
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
import time
import sys
import os
import gc

# ============================================================
# Configuration
# ============================================================
SIZES = [10_000_000, 25_000_000, 50_000_000]
N_GAMMA = 25000
GAMMA_MIN, GAMMA_MAX = 5.0, 85.0
GAMMA_CHUNK = 500       # gammas per chunk
PRIME_CHUNK = 100_000   # primes per chunk

# Local z-score parameters
LOCAL_WINDOW = 8.0      # background window half-width
EXCLUSION_RADIUS = 1.5  # exclude around ALL known zeros

ZEROS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
         37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
         52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
         67.0798, 69.5464, 72.0672, 75.7047, 77.1448]

OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")
FIGURE_DIR = os.path.expanduser("~/Desktop/Farey-Local/figures")
os.makedirs(FIGURE_DIR, exist_ok=True)

gammas = np.linspace(GAMMA_MIN, GAMMA_MAX, N_GAMMA)

# ============================================================
# Linear sieve for Mobius function
# ============================================================
def linear_sieve_mobius(MAX_N):
    """
    Linear sieve: O(N) time, O(N) space.
    Returns mu array (int8) and list of primes.
    Memory: MAX_N bytes for mu + MAX_N bytes for is_composite flag.
    """
    t0 = time.time()
    mu = np.zeros(MAX_N + 1, dtype=np.int8)
    mu[1] = 1
    is_composite = np.zeros(MAX_N + 1, dtype=np.bool_)
    primes_list = []

    for i in range(2, MAX_N + 1):
        if not is_composite[i]:
            primes_list.append(i)
            mu[i] = -1  # prime => mu = -1
        for p in primes_list:
            ip = i * p
            if ip > MAX_N:
                break
            is_composite[ip] = True
            if i % p == 0:
                mu[ip] = 0  # p^2 | ip
                break
            mu[ip] = -mu[i]

    elapsed = time.time() - t0
    print(f"  Linear sieve to {MAX_N:,}: {len(primes_list):,} primes, {elapsed:.1f}s")
    print(f"  Memory: mu={mu.nbytes/1e6:.0f}MB, is_composite={is_composite.nbytes/1e6:.0f}MB")

    del is_composite
    gc.collect()
    return mu, primes_list


def compute_mertens_at_primes(mu, primes_list):
    """Compute M(n) = cumulative sum of mu, extract at prime positions."""
    t0 = time.time()
    M = np.cumsum(mu)
    M_p = np.array([M[p] for p in primes_list], dtype=np.float64)
    elapsed = time.time() - t0
    print(f"  Mertens at primes computed in {elapsed:.1f}s")
    print(f"  M range: [{M_p.min():.0f}, {M_p.max():.0f}]")
    del M
    gc.collect()
    return M_p


# ============================================================
# Double-chunked spectroscope
# ============================================================
def spectroscope_chunked(gammas, log_p, amp, gamma_chunk=GAMMA_CHUNK,
                         prime_chunk=PRIME_CHUNK):
    """
    Compute S(gamma) = sum_j amp_j * exp(-i*gamma*log(p_j))
    then F_comp(gamma) = gamma^2 * |S(gamma)|^2

    Double-chunked: process gamma_chunk gammas x prime_chunk primes at a time.
    Peak memory per chunk: gamma_chunk * prime_chunk * 8 bytes.
    With defaults: 500 * 100K * 8 = 400MB.
    """
    G = len(gammas)
    N = len(log_p)
    S_re = np.zeros(G, dtype=np.float64)
    S_im = np.zeros(G, dtype=np.float64)

    total_chunks = ((G + gamma_chunk - 1) // gamma_chunk) * \
                   ((N + prime_chunk - 1) // prime_chunk)
    chunk_count = 0
    t0 = time.time()

    for g_start in range(0, G, gamma_chunk):
        g_end = min(g_start + gamma_chunk, G)
        g_slice = gammas[g_start:g_end]

        for p_start in range(0, N, prime_chunk):
            p_end = min(p_start + prime_chunk, N)
            lp = log_p[p_start:p_end]
            a = amp[p_start:p_end]

            # phases: (g_end-g_start) x (p_end-p_start)
            phases = np.outer(g_slice, lp)
            S_re[g_start:g_end] += np.cos(phases) @ a
            S_im[g_start:g_end] -= np.sin(phases) @ a  # exp(-i*theta) = cos - i*sin

            del phases
            chunk_count += 1

            # Progress report every 10 chunks
            if chunk_count % 10 == 0 or chunk_count == total_chunks:
                elapsed = time.time() - t0
                pct = chunk_count / total_chunks * 100
                rate = chunk_count / elapsed if elapsed > 0 else 0
                eta = (total_chunks - chunk_count) / rate if rate > 0 else 0
                print(f"    Chunk {chunk_count}/{total_chunks} ({pct:.0f}%), "
                      f"elapsed={elapsed:.0f}s, ETA={eta:.0f}s",
                      flush=True)

    F = (S_re**2 + S_im**2) * gammas**2
    total_time = time.time() - t0
    print(f"  Spectroscope done: {total_time:.1f}s total, "
          f"{G} gammas x {N} primes = {G*N/1e9:.1f}G ops")
    return F


# ============================================================
# Local z-score computation
# ============================================================
def local_zscore(F, gammas, target_gamma, window=LOCAL_WINDOW,
                 exclusion=EXCLUSION_RADIUS, known_zeros=ZEROS):
    """
    Compute local z-score for a peak near target_gamma.
    Background = F values in [target-window, target+window],
    EXCLUDING +-exclusion around ALL known zeros.
    """
    # Find the peak in +-1.2 of target
    peak_mask = (gammas >= target_gamma - 1.2) & (gammas <= target_gamma + 1.2)
    if not peak_mask.any():
        return np.nan, np.nan, np.nan

    peak_indices = np.where(peak_mask)[0]
    best_local = np.argmax(F[peak_indices])
    peak_idx = peak_indices[best_local]
    peak_gamma = gammas[peak_idx]
    peak_val = F[peak_idx]

    # Background: window around target, excluding zero neighborhoods
    bg_mask = (gammas >= target_gamma - window) & (gammas <= target_gamma + window)
    for gz in known_zeros:
        exclude = (gammas >= gz - exclusion) & (gammas <= gz + exclusion)
        bg_mask = bg_mask & ~exclude

    if bg_mask.sum() < 10:
        return peak_gamma, peak_val, np.nan

    bg_vals = F[bg_mask]
    bg_mean = np.mean(bg_vals)
    bg_std = np.std(bg_vals)

    if bg_std < 1e-30:
        return peak_gamma, peak_val, np.nan

    z = (peak_val - bg_mean) / bg_std
    return peak_gamma, peak_val, z


# ============================================================
# Full analysis for one size
# ============================================================
def run_scale(MAX_N, gammas):
    """Run sieve + spectroscope + analysis for one MAX_N."""
    print(f"\n{'='*70}")
    print(f"MAX_N = {MAX_N:,}")
    print(f"{'='*70}")
    wall_t0 = time.time()

    # Step 1: Sieve
    print("\nStep 1: Linear sieve for Mobius function...")
    mu, primes_list = linear_sieve_mobius(MAX_N)

    # Step 2: Mertens at primes
    print("\nStep 2: Compute M(p) at primes...")
    M_p = compute_mertens_at_primes(mu, primes_list)
    del mu
    gc.collect()

    N_primes = len(primes_list)
    primes_arr = np.array(primes_list, dtype=np.float64)
    del primes_list
    gc.collect()

    # Step 3: Compute amplitudes and log-primes
    print(f"\nStep 3: Compute spectroscope ({N_primes:,} primes, {N_GAMMA} gammas)...")
    log_p = np.log(primes_arr)
    amp = M_p / primes_arr  # M(p)/p weight

    F = spectroscope_chunked(gammas, log_p, amp)

    del log_p, amp, primes_arr, M_p
    gc.collect()

    # Step 4: Local z-score analysis
    print(f"\nStep 4: Local z-score analysis (window=+-{LOCAL_WINDOW}, "
          f"excl=+-{EXCLUSION_RADIUS})...")

    results = []
    print(f"  {'#':>3s} {'zero':>8s} {'peak':>8s} {'err%':>8s} {'local_z':>10s}")
    print(f"  {'---':>3s} {'--------':>8s} {'--------':>8s} {'--------':>8s} {'----------':>10s}")

    for i, gz in enumerate(ZEROS):
        peak_gamma, peak_val, z = local_zscore(F, gammas, gz)
        if np.isnan(peak_gamma):
            err = np.nan
        else:
            err = abs(peak_gamma - gz) / gz * 100

        results.append({
            'zero': gz,
            'peak': peak_gamma,
            'err_pct': err,
            'local_z': z,
            'peak_val': peak_val,
        })

        z_str = f"{z:.1f}" if not np.isnan(z) else "N/A"
        err_str = f"{err:.4f}" if not np.isnan(err) else "N/A"
        peak_str = f"{peak_gamma:.4f}" if not np.isnan(peak_gamma) else "N/A"
        print(f"  {i+1:3d} {gz:8.4f} {peak_str:>8s} {err_str:>8s} {z_str:>10s}")

    # Step 5: Summary statistics
    valid = [r for r in results if not np.isnan(r['local_z'])]
    z_vals = [r['local_z'] for r in valid]
    err_vals = [r['err_pct'] for r in valid]

    n_z5 = sum(1 for z in z_vals if z > 5)
    n_z10 = sum(1 for z in z_vals if z > 10)
    n_z20 = sum(1 for z in z_vals if z > 20)
    n_z50 = sum(1 for z in z_vals if z > 50)
    avg_z = np.mean(z_vals) if z_vals else np.nan
    median_z = np.median(z_vals) if z_vals else np.nan
    min_z = np.min(z_vals) if z_vals else np.nan
    avg_err = np.mean(err_vals) if err_vals else np.nan
    max_err = np.max(err_vals) if err_vals else np.nan

    wall_time = time.time() - wall_t0

    summary = {
        'MAX_N': MAX_N,
        'N_primes': N_primes,
        'n_z5': n_z5,
        'n_z10': n_z10,
        'n_z20': n_z20,
        'n_z50': n_z50,
        'avg_z': avg_z,
        'median_z': median_z,
        'min_z': min_z,
        'avg_err': avg_err,
        'max_err': max_err,
        'wall_time': wall_time,
        'results': results,
        'F': F,  # keep for plotting
    }

    print(f"\n  SUMMARY for MAX_N={MAX_N:,}:")
    print(f"    Primes used: {N_primes:,}")
    print(f"    Avg local z-score:    {avg_z:.1f}")
    print(f"    Median local z-score: {median_z:.1f}")
    print(f"    Min local z-score:    {min_z:.1f}")
    print(f"    Zeros with z > 5:     {n_z5}/20")
    print(f"    Zeros with z > 10:    {n_z10}/20")
    print(f"    Zeros with z > 20:    {n_z20}/20")
    print(f"    Zeros with z > 50:    {n_z50}/20")
    print(f"    Avg error:            {avg_err:.4f}%")
    print(f"    Max error:            {max_err:.4f}%")
    print(f"    Wall time:            {wall_time:.0f}s ({wall_time/60:.1f}min)")

    sys.stdout.flush()
    return summary


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("="*70)
    print("COMPENSATED MERTENS SPECTROSCOPE — LARGE SCALE")
    print(f"F_comp(gamma) = gamma^2 * |sum M(p)/p * exp(-i*gamma*log(p))|^2")
    print(f"Sizes: {[f'{s:,}' for s in SIZES]}")
    print(f"Gammas: {N_GAMMA} points in [{GAMMA_MIN}, {GAMMA_MAX}]")
    print(f"Chunks: gamma={GAMMA_CHUNK}, prime={PRIME_CHUNK}")
    print(f"Local z-score: window=+-{LOCAL_WINDOW}, exclusion=+-{EXCLUSION_RADIUS}")
    print("="*70)
    total_t0 = time.time()

    all_summaries = []

    for MAX_N in SIZES:
        summary = run_scale(MAX_N, gammas)
        all_summaries.append(summary)
        sys.stdout.flush()

    # ============================================================
    # Cross-scale comparison
    # ============================================================
    print(f"\n{'='*70}")
    print("CROSS-SCALE COMPARISON")
    print(f"{'='*70}")

    header = f"  {'MAX_N':>12s} {'primes':>10s} {'avg_z':>8s} {'med_z':>8s} " \
             f"{'min_z':>8s} {'z>5':>5s} {'z>10':>5s} {'z>20':>5s} " \
             f"{'z>50':>5s} {'avg_err%':>10s} {'time':>8s}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    for s in all_summaries:
        print(f"  {s['MAX_N']:12,} {s['N_primes']:10,} "
              f"{s['avg_z']:8.1f} {s['median_z']:8.1f} {s['min_z']:8.1f} "
              f"{s['n_z5']:5d} {s['n_z10']:5d} {s['n_z20']:5d} {s['n_z50']:5d} "
              f"{s['avg_err']:10.4f} {s['wall_time']:7.0f}s")

    # Per-zero scaling table
    print(f"\n  Per-zero local z-score scaling:")
    print(f"  {'#':>3s} {'zero':>8s}", end="")
    for s in all_summaries:
        print(f" {'z@'+str(s['MAX_N']//1_000_000)+'M':>10s}", end="")
    print()

    for i, gz in enumerate(ZEROS):
        print(f"  {i+1:3d} {gz:8.4f}", end="")
        for s in all_summaries:
            z = s['results'][i]['local_z']
            if np.isnan(z):
                print(f" {'N/A':>10s}", end="")
            else:
                print(f" {z:10.1f}", end="")
        print()

    total_time = time.time() - total_t0
    print(f"\nTotal wall time: {total_time:.0f}s ({total_time/3600:.1f}h)")

    # ============================================================
    # Save figure
    # ============================================================
    print("\nGenerating figure...")
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(len(all_summaries) + 1, 1,
                                 figsize=(16, 4 * (len(all_summaries) + 1)))

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

        for idx, s in enumerate(all_summaries):
            ax = axes[idx]
            F = s['F']
            label = f"MAX_N={s['MAX_N']:,} ({s['N_primes']:,} primes)"

            ax.plot(gammas, F, linewidth=0.3, color=colors[idx], alpha=0.7)
            ax.set_title(label, fontsize=11)
            ax.set_xlabel('gamma')
            ax.set_ylabel('F_comp(gamma)')

            # Mark zeros
            for gz in ZEROS:
                ax.axvline(x=gz, color='red', alpha=0.3, linewidth=0.5)

            # Mark detected peaks
            for r in s['results']:
                if not np.isnan(r['local_z']) and r['local_z'] > 5:
                    ax.axvline(x=r['peak'], color='green', alpha=0.5,
                               linewidth=0.8, linestyle='--')

            ax.set_xlim(GAMMA_MIN, GAMMA_MAX)

        # Bottom panel: scaling of z-scores
        ax = axes[-1]
        sizes_M = [s['MAX_N'] / 1e6 for s in all_summaries]

        # Plot z-score for each zero across scales
        for i, gz in enumerate(ZEROS):
            z_vals = []
            for s in all_summaries:
                z = s['results'][i]['local_z']
                z_vals.append(z if not np.isnan(z) else 0)
            ax.plot(sizes_M, z_vals, 'o-', markersize=3, alpha=0.5,
                    label=f'gamma={gz:.1f}' if i < 5 else None)

        # Average z-score
        avg_z_vals = [s['avg_z'] for s in all_summaries]
        ax.plot(sizes_M, avg_z_vals, 'k-o', linewidth=2.5, markersize=8,
                label='Average', zorder=10)

        # Median z-score
        med_z_vals = [s['median_z'] for s in all_summaries]
        ax.plot(sizes_M, med_z_vals, 'k--s', linewidth=2, markersize=7,
                label='Median', zorder=10)

        ax.set_xlabel('MAX_N (millions)')
        ax.set_ylabel('Local z-score')
        ax.set_title('Z-score scaling with data size')
        ax.legend(fontsize=8, ncol=4, loc='upper left')
        ax.set_xscale('log')
        ax.axhline(y=5, color='gray', linestyle=':', alpha=0.5, label='z=5')
        ax.axhline(y=10, color='gray', linestyle='--', alpha=0.5, label='z=10')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        fig_path = os.path.join(FIGURE_DIR, "spectroscope_large_scale.png")
        plt.savefig(fig_path, dpi=150, bbox_inches='tight')
        print(f"  Figure saved to {fig_path}")
        plt.close()

    except Exception as e:
        print(f"  Figure generation failed: {e}")

    # ============================================================
    # Save results markdown
    # ============================================================
    print("\nSaving results...")
    md_path = os.path.join(OUTPUT_DIR, "MERTENS_LARGE_SCALE_RESULTS.md")
    with open(md_path, 'w') as f:
        f.write("# Compensated Mertens Spectroscope — Large Scale Results\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Formula\n\n")
        f.write("F_comp(gamma) = gamma^2 * |sum_{p prime <= N} M(p)/p * exp(-i*gamma*log(p))|^2\n\n")
        f.write("## Parameters\n\n")
        f.write(f"- Gamma range: [{GAMMA_MIN}, {GAMMA_MAX}], {N_GAMMA} points\n")
        f.write(f"- Local z-score: window=+-{LOCAL_WINDOW}, exclusion=+-{EXCLUSION_RADIUS}\n")
        f.write(f"- Chunk sizes: gamma={GAMMA_CHUNK}, prime={PRIME_CHUNK}\n\n")

        f.write("## Cross-Scale Summary\n\n")
        f.write("| MAX_N | Primes | Avg z | Median z | Min z | z>5 | z>10 | z>20 | z>50 | Avg err% | Time |\n")
        f.write("|------:|-------:|------:|---------:|------:|----:|-----:|-----:|-----:|---------:|-----:|\n")
        for s in all_summaries:
            f.write(f"| {s['MAX_N']:,} | {s['N_primes']:,} | "
                    f"{s['avg_z']:.1f} | {s['median_z']:.1f} | {s['min_z']:.1f} | "
                    f"{s['n_z5']} | {s['n_z10']} | {s['n_z20']} | {s['n_z50']} | "
                    f"{s['avg_err']:.4f} | {s['wall_time']:.0f}s |\n")

        f.write("\n## Per-Zero Detail\n\n")
        for s in all_summaries:
            f.write(f"\n### MAX_N = {s['MAX_N']:,} ({s['N_primes']:,} primes)\n\n")
            f.write(f"Wall time: {s['wall_time']:.0f}s ({s['wall_time']/60:.1f} min)\n\n")
            f.write("| # | Zero | Peak | Error% | Local z |\n")
            f.write("|--:|-----:|-----:|-------:|--------:|\n")
            for i, r in enumerate(s['results']):
                z_str = f"{r['local_z']:.1f}" if not np.isnan(r['local_z']) else "N/A"
                err_str = f"{r['err_pct']:.4f}" if not np.isnan(r['err_pct']) else "N/A"
                peak_str = f"{r['peak']:.4f}" if not np.isnan(r['peak']) else "N/A"
                f.write(f"| {i+1} | {r['zero']:.4f} | {peak_str} | {err_str} | {z_str} |\n")

        f.write(f"\n## Scaling Analysis\n\n")
        f.write("Per-zero z-score across scales:\n\n")
        f.write(f"| # | Zero |")
        for s in all_summaries:
            f.write(f" z@{s['MAX_N']//1_000_000}M |")
        f.write("\n|--:|-----:|")
        for _ in all_summaries:
            f.write("------:|")
        f.write("\n")
        for i, gz in enumerate(ZEROS):
            f.write(f"| {i+1} | {gz:.4f} |")
            for s in all_summaries:
                z = s['results'][i]['local_z']
                if np.isnan(z):
                    f.write(" N/A |")
                else:
                    f.write(f" {z:.1f} |")
            f.write("\n")

        f.write(f"\nTotal computation time: {total_time:.0f}s ({total_time/3600:.1f}h)\n")

    print(f"  Results saved to {md_path}")
    print(f"\nAll done! Total: {total_time:.0f}s ({total_time/3600:.1f}h)")
