#!/usr/bin/env python3
"""
Post-ceiling phase probe for the failed (MERTENS-LB) inequality.

The earlier SP-2/R1 empirical ceiling was N = 99,991.  This script pins down
the first positive T(N) after that ceiling and summarizes the first large
positive cluster without doing a full dense scan to 1e6.
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from MERTENS_LB_sweep import cumsum_int32, mobius_sieve, verify_mertens_table


def harmonic_prefix(nmax: int) -> np.ndarray:
    h = np.empty(nmax + 1, dtype=np.float64)
    h[0] = 0.0
    h[1:] = np.cumsum(1.0 / np.arange(1, nmax + 1, dtype=np.float64))
    return h


def t_value(n: int, mertens: np.ndarray, h: np.ndarray) -> float:
    total = 0.0
    k = 1
    while k <= n:
        q = n // k
        k1 = n // q
        total += int(mertens[q]) * (h[k1] - h[k - 1])
        k = k1 + 1
    return 1.0 + total


def q_band_contributions(n: int, mertens: np.ndarray, h: np.ndarray) -> list[tuple[str, float]]:
    bands = [
        ("q<=10", 1, 10),
        ("11-100", 11, 100),
        ("101-1k", 101, 1000),
        ("1k-10k", 1001, 10000),
        ("10k-100k", 10001, 100000),
        (">100k", 100001, n),
    ]
    values = {name: 0.0 for name, _, _ in bands}
    k = 1
    while k <= n:
        q = n // k
        k1 = n // q
        contrib = int(mertens[q]) * (h[k1] - h[k - 1])
        for name, lo, hi in bands:
            if lo <= q <= hi:
                values[name] += contrib
                break
        k = k1 + 1
    return [(name, values[name]) for name, _, _ in bands]


def small_k_terms(n: int, mertens: np.ndarray, kmax: int = 10) -> list[tuple[int, int, int, float]]:
    rows = []
    for k in range(1, kmax + 1):
        q = n // k
        mq = int(mertens[q])
        rows.append((k, q, mq, mq / k))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=99_992)
    parser.add_argument("--end", type=int, default=350_000)
    parser.add_argument("--threshold", type=float, action="append", default=[0.0, 10.0, 50.0, 100.0])
    parser.add_argument("--key", type=int, action="append", default=[
        99_991, 108_004, 116_845, 121_618, 200_000,
        286_899, 300_296, 320_058, 342_767,
    ])
    args = parser.parse_args()

    nmax = max(args.end, *(args.key or []))
    t0 = time.time()
    mu = mobius_sieve(nmax)
    mertens = cumsum_int32(mu)
    ok, mismatches = verify_mertens_table(mertens, nmax)
    h = harmonic_prefix(nmax)

    print(f"# MERTENS-LB phase probe")
    print(f"nmax: {nmax}")
    print(f"mertens_anchor_check: {ok}")
    if mismatches:
        print(f"mismatches: {mismatches}")
    print(f"sieve_and_prefix_seconds: {time.time() - t0:.3f}")
    print()

    print("## Key values")
    print("N\tT(N)\tM(N)\tT(N)/logN")
    for n in args.key:
        val = t_value(n, mertens, h)
        print(f"{n}\t{val:.12f}\t{int(mertens[n])}\t{val / math.log(n):.12f}")

    first = {thr: None for thr in args.threshold}
    clusters: list[tuple[int, int, int, float, int]] = []
    in_pos = False
    cluster_start = 0
    peak_n = 0
    peak_t = float("-inf")

    scan_t0 = time.time()
    for n in range(args.start, args.end + 1):
        val = t_value(n, mertens, h)
        for thr in args.threshold:
            if first[thr] is None and val > thr:
                first[thr] = (n, val, int(mertens[n]))
        if val > 0:
            if not in_pos:
                in_pos = True
                cluster_start = n
                peak_n = n
                peak_t = val
            if val > peak_t:
                peak_n = n
                peak_t = val
        elif in_pos:
            clusters.append((cluster_start, n - 1, peak_n, peak_t, n - cluster_start))
            in_pos = False
    if in_pos:
        clusters.append((cluster_start, args.end, peak_n, peak_t, args.end - cluster_start + 1))

    print()
    print("## First threshold crossings")
    print("threshold\tN\tT(N)\tM(N)")
    for thr in args.threshold:
        row = first[thr]
        if row is None:
            print(f"{thr:g}\tNA\tNA\tNA")
        else:
            n, val, mn = row
            print(f"{thr:g}\t{n}\t{val:.12f}\t{mn}")

    print()
    print("## Positive clusters")
    print(f"scan_range: [{args.start}, {args.end}]")
    print(f"scan_seconds: {time.time() - scan_t0:.3f}")
    print(f"cluster_count: {len(clusters)}")
    print("start\tend\tpeak_N\tpeak_T\twidth")
    for row in clusters[:12]:
        start, end, pn, pv, width = row
        print(f"{start}\t{end}\t{pn}\t{pv:.12f}\t{width}")
    if clusters:
        widest = max(clusters, key=lambda row: row[4])
        highest = max(clusters, key=lambda row: row[3])
        print()
        print(f"widest_cluster: {widest[0]}-{widest[1]}, peak {widest[2]} with T={widest[3]:.12f}, width={widest[4]}")
        print(f"highest_cluster: {highest[0]}-{highest[1]}, peak {highest[2]} with T={highest[3]:.12f}, width={highest[4]}")

    print()
    print("## q-band decomposition")
    for n in args.key:
        val = t_value(n, mertens, h)
        print(f"N={n}, T={val:.12f}, M(N)={int(mertens[n])}")
        for name, contrib in q_band_contributions(n, mertens, h):
            print(f"  {name}\t{contrib:.12f}")

    print()
    print("## Small-k terms")
    for n in [99_991, 108_004, 116_845, 300_296, 342_767]:
        print(f"N={n}, M(N)={int(mertens[n])}")
        subtotal = 1.0
        for k, q, mq, contrib in small_k_terms(n, mertens):
            subtotal += contrib
            print(f"  k={k}\tq={q}\tM(q)={mq}\tM(q)/k={contrib:.12f}")
        print(f"  1+sum_k<=10 = {subtotal:.12f}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
