#!/usr/bin/env python3
"""Agent 4 reproducibility probe for MERTENS-LB small-k/tail splits."""
from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FOLLOWUP = ROOT / "handoff-2026-05-09-followup"
sys.path.insert(0, str(FOLLOWUP))

from MERTENS_LB_sweep import cumsum_int32, mobius_sieve, verify_mertens_table  # noqa: E402


ANCHORS = [
    99_991, 108_004, 111_812, 116_845, 121_618, 200_000,
    286_899, 297_331, 300_296, 320_058, 342_767, 1_000_000,
]


def parse_k_list(raw: str) -> list[int]:
    return [int(x) for x in raw.split(",") if x.strip()]


def h_prefix(mu: np.ndarray, nmax: int) -> np.ndarray:
    h = np.zeros(nmax + 1, dtype=np.int64)
    for d in range(1, nmax + 1):
        md = int(mu[d])
        if md:
            h[d::d] += md * d
    return 1.0 + np.cumsum(h[1:].astype(np.float64) / np.arange(1, nmax + 1, dtype=np.float64))


def small_head(nvals: np.ndarray, mertens: np.ndarray, k: int) -> np.ndarray:
    out = np.ones(len(nvals), dtype=np.float64)
    for j in range(1, k + 1):
        out += mertens[nvals // j] / j
    return out


def clusters(t_values: np.ndarray, lo: int) -> list[tuple[int, int, int, float, int]]:
    pos = t_values > 0
    out: list[tuple[int, int, int, float, int]] = []
    i = 0
    while i < len(pos):
        if not pos[i]:
            i += 1
            continue
        j = i
        peak = i
        while j + 1 < len(pos) and pos[j + 1]:
            j += 1
            if t_values[j] > t_values[peak]:
                peak = j
        out.append((lo + i, lo + j, lo + peak, float(t_values[peak]), j - i + 1))
        i = j + 1
    return out


def print_dense(dense_max: int, ks: list[int]) -> tuple[np.ndarray, np.ndarray]:
    t0 = time.time()
    mu = mobius_sieve(dense_max)
    mertens = cumsum_int32(mu)
    ok, mismatches = verify_mertens_table(mertens, dense_max)
    t_values = h_prefix(mu, dense_max)
    print(f"dense_max\t{dense_max}")
    print(f"dense_build_seconds\t{time.time() - t0:.3f}")
    print(f"mertens_anchor_check\t{ok}\t{mismatches}")
    print("anchor_N\tT(N)\tM(N)")
    for n in ANCHORS:
        if n <= dense_max:
            print(f"{n}\t{t_values[n - 1]:.12f}\t{int(mertens[n])}")
    print("threshold\tfirst_N\tT(N)\tM(N)")
    arr = t_values[99_991:dense_max] if dense_max >= 99_992 else np.array([], dtype=np.float64)
    for thr in [0.0, 10.0, 50.0, 100.0, 150.0, 200.0]:
        if len(arr):
            idx = int(np.argmax(arr > thr))
            if arr[idx] > thr:
                n = 99_992 + idx
                print(f"{thr:g}\t{n}\t{t_values[n - 1]:.12f}\t{int(mertens[n])}")
                continue
        print(f"{thr:g}\tNA\tNA\tNA")
    if dense_max >= 350_000:
        cl = clusters(t_values[99_991:350_000], 99_992)
        widest = max(cl, key=lambda row: row[4])
        highest = max(cl, key=lambda row: row[3])
        print(f"clusters_99992_350000\t{len(cl)}")
        print(f"widest_cluster\t{widest}")
        print(f"highest_cluster\t{highest}")
    for lo, hi in [(99_992, min(350_000, dense_max)), (99_992, dense_max)]:
        if lo > hi:
            continue
        nvals = np.arange(lo, hi + 1, dtype=np.int64)
        print(f"tail_range\t{lo}\t{hi}")
        for k in ks:
            head = small_head(nvals, mertens, k)
            tail = t_values[lo - 1:hi] - head
            imn = int(np.argmin(tail))
            imx = int(np.argmax(tail))
            corr = float(np.corrcoef(head, t_values[lo - 1:hi])[0, 1])
            sign_acc = float(np.mean((head > 0) == (t_values[lo - 1:hi] > 0)))
            print(
                f"K\t{k}\tmin\t{lo + imn}\t{tail[imn]:.6f}"
                f"\tmax\t{lo + imx}\t{tail[imx]:.6f}"
                f"\tcorr\t{corr:.6f}\tsign_acc\t{sign_acc:.6f}"
            )
    return mu, mertens


def print_sample(tsv: Path, sample_max: int, ks: list[int]) -> None:
    rows: list[tuple[int, float]] = []
    with tsv.open() as f:
        for row in csv.DictReader(f, delimiter="\t"):
            n = int(row["N"])
            if 99_992 <= n <= sample_max:
                rows.append((n, float(row["T(N)"])))
    if not rows:
        return
    nmax = max(n for n, _ in rows)
    t0 = time.time()
    mu = mobius_sieve(nmax)
    mertens = cumsum_int32(mu)
    ok, mismatches = verify_mertens_table(mertens, nmax)
    print(f"sample_tsv\t{tsv}")
    print(f"sample_count\t{len(rows)}")
    print(f"sample_mertens_max\t{nmax}")
    print(f"sample_build_seconds\t{time.time() - t0:.3f}")
    print(f"sample_mertens_anchor_check\t{ok}\t{mismatches}")
    for k in ks:
        vals = []
        for n, t_val in rows:
            head = 1.0 + sum(int(mertens[n // j]) / j for j in range(1, k + 1))
            vals.append((n, t_val, head, t_val - head, int(mertens[n])))
        mn = min(vals, key=lambda row: row[3])
        mx = max(vals, key=lambda row: row[3])
        pos = [row for row in vals if row[3] > 0]
        first = pos[0] if pos else None
        first_text = "NA" if first is None else f"{first[0]}\t{first[3]:.6f}"
        print(
            f"sample_K\t{k}\tmin\t{mn[0]}\t{mn[3]:.6f}"
            f"\tmax\t{mx[0]}\t{mx[3]:.6f}\tpos_count\t{len(pos)}"
            f"\tfirst_pos\t{first_text}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dense-max", type=int, default=1_000_000)
    parser.add_argument("--ks", default="10,20,50,100,200")
    parser.add_argument("--asymptotic-tsv", type=Path, default=FOLLOWUP / "MERTENS_LB_asymptotic_scan.tsv")
    parser.add_argument("--sample-max", type=int, default=0)
    args = parser.parse_args()
    ks = parse_k_list(args.ks)
    print_dense(args.dense_max, ks)
    if args.sample_max:
        print_sample(args.asymptotic_tsv, args.sample_max, ks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
