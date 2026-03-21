#!/usr/bin/env python3
"""
Mertens Function as Wobble Violation Predictor
================================================

KEY INSIGHT: Wobble violations (ΔW(p) > 0) occur at primes p
where M(p)/√p is large and positive.

This script:
1. Computes M(N) via Möbius sieve to N=50,000
2. Identifies "high M" zones where violations should occur
3. Generates predictions for the C wobble computation
4. When C data is available, validates the predictor
"""

import numpy as np
from math import sqrt
import os
import csv


def mobius_sieve(max_N):
    """Compute μ(n), M(n), and primality for all n ≤ max_N."""
    mu = [0] * (max_N + 1)
    mu[1] = 1
    is_p = [True] * (max_N + 1)
    is_p[0] = is_p[1] = False
    primes = []
    for i in range(2, max_N + 1):
        if is_p[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > max_N:
                break
            is_p[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (max_N + 1)
    for k in range(1, max_N + 1):
        M[k] = M[k - 1] + mu[k]
    return mu, M, is_p


def main():
    MAX_N = 50000

    print("=" * 70)
    print("MERTENS FUNCTION AS WOBBLE VIOLATION PREDICTOR")
    print("=" * 70)

    print(f"\nComputing Möbius sieve to N={MAX_N}...")
    mu, M, is_p = mobius_sieve(MAX_N)
    print("Done.")

    # Collect M(p)/√p for all primes p ≥ 11
    primes = [p for p in range(11, MAX_N + 1) if is_p[p]]
    M_norm_at_primes = [(p, M[p] / sqrt(p)) for p in primes]

    print(f"\n  Total primes ≥ 11 up to {MAX_N}: {len(primes)}")

    # ──────────────────────────────────────────────
    # VIOLATION RATE PREDICTION BY WINDOW
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("PREDICTION: Violation rate by M(N)/√N percentile")
    print(f"{'='*70}")

    # The key observation: violations happen when M(p)/√p > threshold
    # From N≤5000 data: all violations had M(p)/√p > 0.175
    # From N=16000-18000: max M(p)/√p = 0.015 → 0 violations
    # Hypothesis: threshold is around 0.10 - 0.20

    thresholds = [0.05, 0.10, 0.15, 0.175, 0.20, 0.25, 0.30]
    print(f"\n  Fraction of primes with M(p)/√p > threshold, by range:")
    print(f"  {'Range':>18}", end="")
    for t in thresholds:
        print(f"  >{t:.3f}", end="")
    print()

    for lo in range(0, MAX_N, 2000):
        hi = lo + 2000
        ps_in_range = [(p, mn) for p, mn in M_norm_at_primes if lo <= p < hi]
        if not ps_in_range:
            continue
        print(f"  [{lo:6d},{hi:6d}):", end="")
        for t in thresholds:
            frac = sum(1 for _, mn in ps_in_range if mn > t) / len(ps_in_range)
            print(f"  {100*frac:5.1f}%", end="")
        print(f"  (n={len(ps_in_range)})")

    # ──────────────────────────────────────────────
    # M(N)/√N TRAJECTORY — KEY EXCURSIONS
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("LARGE EXCURSIONS OF M(N)/√N")
    print(f"{'='*70}")

    # Find all N where M(N)/√N > 0.30 or < -0.40
    pos_peaks = []
    for N in range(2, MAX_N + 1):
        mn = M[N] / sqrt(N)
        if mn > 0.35:
            pos_peaks.append((N, mn))

    print(f"\n  Large positive peaks (M(N)/√N > 0.35):")
    print(f"  {'N':>7}  {'M(N)':>7}  {'M/√N':>8}  {'prime?':>6}")
    # Group into clusters
    if pos_peaks:
        clusters = [[pos_peaks[0]]]
        for item in pos_peaks[1:]:
            if item[0] - clusters[-1][-1][0] < 200:
                clusters[-1].append(item)
            else:
                clusters.append([item])

        for cl in clusters:
            peak = max(cl, key=lambda x: x[1])
            N, mn = peak
            p_str = "PRIME" if is_p[N] else ""
            print(f"  {N:7d}  {M[N]:7d}  {mn:+8.5f}  {p_str:6s}  (cluster of {len(cl)} values)")

    # ──────────────────────────────────────────────
    # PREDICTED VIOLATION CLUSTERS
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("PREDICTED VIOLATION CLUSTERS (primes where M(p)/√p > 0.175)")
    print(f"{'='*70}")

    predicted_violations = [p for p, mn in M_norm_at_primes if mn > 0.175]
    print(f"\n  Total predicted violations: {len(predicted_violations)} / {len(primes)} "
          f"({100*len(predicted_violations)/len(primes):.1f}%)")

    # Group into clusters (gap > 200 = new cluster)
    if predicted_violations:
        clusters = [[predicted_violations[0]]]
        for p in predicted_violations[1:]:
            if p - clusters[-1][-1] > 200:
                clusters.append([p])
            else:
                clusters[-1].append(p)

        print(f"\n  Predicted clusters (gap > 200 = boundary):")
        print(f"  {'#':>3}  {'First':>6}  {'Last':>6}  {'Size':>5}  {'Span':>5}  {'MaxM/√p':>9}  {'Range':>14}")
        for i, cl in enumerate(clusters):
            max_mn = max(M[p]/sqrt(p) for p in cl)
            range_str = f"[{cl[0]:d},{cl[-1]:d}]"
            print(f"  {i+1:3d}  {cl[0]:6d}  {cl[-1]:6d}  {len(cl):5d}  {cl[-1]-cl[0]:5d}  {max_mn:+9.5f}  {range_str:>14}")

    # ──────────────────────────────────────────────
    # VALIDATE AGAINST C DATA IF AVAILABLE
    # ──────────────────────────────────────────────
    csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wobble_c_data.csv')
    if os.path.exists(csv_file):
        print(f"\n{'='*70}")
        print("VALIDATION: Comparing predictions to actual C wobble data")
        print(f"{'='*70}")

        actual_violations = set()
        actual_non_violations = set()
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                N = int(row['N'])
                is_prime = int(row['is_prime'])
                delta_w = float(row['delta_w'])
                if is_prime and N >= 11:
                    if delta_w > 0:
                        actual_violations.add(N)
                    else:
                        actual_non_violations.add(N)

        max_N_data = max(actual_violations | actual_non_violations) if actual_violations else 0
        print(f"\n  C data range: up to N={max_N_data}")
        print(f"  Actual violations: {len(actual_violations)}")
        print(f"  Actual non-violations: {len(actual_non_violations)}")

        # Test different thresholds
        print(f"\n  Threshold optimization (M(p)/√p > θ as violation predictor):")
        print(f"  {'θ':>6}  {'TP':>5}  {'FP':>5}  {'FN':>5}  {'TN':>5}  {'Prec':>6}  {'Recall':>6}  {'F1':>6}")

        all_test_primes = actual_violations | actual_non_violations
        for theta in [0.0, 0.05, 0.10, 0.12, 0.14, 0.15, 0.16, 0.175, 0.20, 0.25]:
            tp = sum(1 for p in actual_violations if M[p]/sqrt(p) > theta)
            fp = sum(1 for p in actual_non_violations if M[p]/sqrt(p) > theta)
            fn = sum(1 for p in actual_violations if M[p]/sqrt(p) <= theta)
            tn = sum(1 for p in actual_non_violations if M[p]/sqrt(p) <= theta)
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
            print(f"  {theta:6.3f}  {tp:5d}  {fp:5d}  {fn:5d}  {tn:5d}  {prec:6.3f}  {rec:6.3f}  {f1:6.3f}")

        # Show actual violations with M(p)/√p
        print(f"\n  Actual violations with lowest M(p)/√p:")
        viol_with_M = [(p, M[p]/sqrt(p)) for p in sorted(actual_violations)]
        viol_with_M.sort(key=lambda x: x[1])
        for p, mn in viol_with_M[:10]:
            print(f"    p={p:6d}  M(p)/√p = {mn:+.6f}")
        print(f"  ...")
        print(f"  Minimum M(p)/√p at a violation: {viol_with_M[0][1]:+.6f} at p={viol_with_M[0][0]}")
        print(f"  Maximum M(p)/√p at a violation: {viol_with_M[-1][1]:+.6f} at p={viol_with_M[-1][0]}")

    else:
        print(f"\n  C data not available yet (looking for {csv_file})")
        print("  Run: ./wobble_largescale 20000")
        print("  Then re-run this script for full validation.")

    # ──────────────────────────────────────────────
    # LONG-RANGE PREDICTION (N=20K to 50K)
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("LONG-RANGE PREDICTIONS: N=20,000 to 50,000")
    print(f"{'='*70}")

    future_predictions = [p for p, mn in M_norm_at_primes if p >= 20000 and mn > 0.175]
    future_primes = [p for p in primes if p >= 20000]

    print(f"\n  Primes ≥ 20000: {len(future_primes)}")
    print(f"  Predicted violations (M(p)/√p > 0.175): {len(future_predictions)} "
          f"({100*len(future_predictions)/len(future_primes):.1f}%)")

    # Cluster the predictions
    if future_predictions:
        clusters = [[future_predictions[0]]]
        for p in future_predictions[1:]:
            if p - clusters[-1][-1] > 200:
                clusters.append([p])
            else:
                clusters[-1].append(p)

        print(f"\n  Predicted violation clusters beyond N=20,000:")
        print(f"  {'#':>3}  {'First':>6}  {'Last':>6}  {'Size':>5}  {'Span':>5}  {'MaxM/√p':>9}")
        for i, cl in enumerate(clusters[:15]):
            max_mn = max(M[p]/sqrt(p) for p in cl)
            print(f"  {i+1:3d}  {cl[0]:6d}  {cl[-1]:6d}  {len(cl):5d}  {cl[-1]-cl[0]:5d}  {max_mn:+9.5f}")

    # Summary statistics
    print(f"\n  Predicted violation rate by 5000-ranges:")
    for lo in range(20000, 50000, 5000):
        hi = lo + 5000
        ps = [p for p in primes if lo <= p < hi]
        vs = [p for p in future_predictions if lo <= p < hi]
        if ps:
            rate = 100 * len(vs) / len(ps)
            max_mn = max(M[p]/sqrt(p) for p in ps)
            print(f"    [{lo:6d},{hi:6d}): {len(ps)} primes, {len(vs)} predicted violations "
                  f"({rate:.1f}%), max M/√p = {max_mn:+.4f}")


if __name__ == '__main__':
    main()
