#!/usr/bin/env python3
"""
Extended EC-NDC sweep.

Reads the existing K=100000 sweep/a_p cache, extends a_p as needed, and writes
only the requested extended CSV/report.  No bad-prime correction is introduced
beyond the actual EC local factors already present in D_K and L(E,2).
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_AP_CACHE = SCRIPT_DIR / "Koyama_EC_NDC_ap_table_100000.csv"
DEFAULT_BASE_SWEEP = SCRIPT_DIR / "Koyama_EC_NDC.csv"
DEFAULT_CSV = SCRIPT_DIR / "Koyama_EC_NDC_extended_sweep_2026-05-11.csv"
DEFAULT_REPORT = SCRIPT_DIR / "Koyama_EC_NDC_extended_sweep_2026-05-11.md"

ZETA2 = math.pi * math.pi / 6.0
EULER_GAMMA = 0.577215664901532860606512090082402431
REPORT_DATE = "2026-05-11"

BEST_PRIOR_CROSS_CURVE_RATIO = 1.42083
BEST_PRIOR_MAX_WITHIN_CV = 0.08567129


@dataclass(frozen=True)
class Curve:
    label: str
    ainvs: Tuple[int, int, int, int, int]
    conductor: int
    rank: int


CURVES: Tuple[Curve, ...] = (
    Curve("37a1", (0, 0, 1, -1, 0), 37, 1),
    Curve("11a1", (0, -1, 1, -10, -20), 11, 0),
    Curve("389a1", (0, 1, 1, -2, 0), 389, 2),
)
CURVE_LABELS = tuple(curve.label for curve in CURVES)
CURVE_BY_LABEL = {curve.label: curve for curve in CURVES}


@dataclass(frozen=True)
class SweepRow:
    curve: str
    K: int
    rank: int
    c_K: float
    E_K: float
    D_K: float
    D_K_zeta2: float
    L2E_partial: float
    L2E_rank_power: float
    D_zeta2_over_L2E_rank: float
    C_mix_good: float
    D_mix_good: float
    C_2_good: float
    D_2_good: float
    p_max: int
    good_prime_count: int
    ap_cache_max: int
    ap_extended_count: int
    product_complete: bool


@dataclass(frozen=True)
class MetricRow:
    normalization: str
    promoted: bool
    max_within_cv: float
    cross_curve_cv: float
    cross_curve_ratio: float
    curve_means: Dict[str, float]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extend the EC-NDC sweep.")
    parser.add_argument("--max-k", type=int, default=300000)
    parser.add_argument("--ap-cache", type=Path, default=DEFAULT_AP_CACHE)
    parser.add_argument("--base-sweep", type=Path, default=DEFAULT_BASE_SWEEP)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--out-report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--workers",
        type=int,
        default=min(4, os.cpu_count() or 1),
        help="Worker processes for missing a_p computation.",
    )
    parser.add_argument(
        "--checkpoints",
        type=int,
        nargs="*",
        default=[1000, 3000, 10000, 30000, 100000, 300000, 1000000],
    )
    return parser.parse_args(argv)


def sieve_primes(n: int) -> List[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : n + 1 : p] = b"\x00" * len(range(start, n + 1, p))
    return [i for i in range(2, n + 1) if sieve[i]]


def build_spf(n: int, primes: Sequence[int]) -> List[int]:
    spf = list(range(n + 1))
    if n >= 1:
        spf[1] = 1
    for p in primes:
        p2 = p * p
        if p2 > n:
            break
        if spf[p] == p:
            for m in range(p2, n + 1, p):
                if spf[m] == m:
                    spf[m] = p
    return spf


def read_ap_cache(path: Path) -> Tuple[Dict[str, Dict[int, int]], Dict[str, Dict[int, str]], int]:
    ap: Dict[str, Dict[int, int]] = {label: {} for label in CURVE_LABELS}
    reduction: Dict[str, Dict[int, str]] = {label: {} for label in CURVE_LABELS}
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            p = int(raw["p"])
            for label in CURVE_LABELS:
                ap[label][p] = int(raw[f"a_p({label})"])
                reduction[label][p] = raw[f"reduction({label})"]
    cache_max = max((p for values in ap.values() for p in values), default=0)
    return ap, reduction, cache_max


def read_base_sweep(path: Path) -> Dict[Tuple[str, int], float]:
    out: Dict[Tuple[str, int], float] = {}
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            out[(raw["curve"], int(raw["K"]))] = float(raw["D_K_times_zeta2"])
    return out


def validate_cache(primes: Sequence[int], ap: Mapping[str, Mapping[int, int]], max_k: int) -> None:
    missing = [p for p in primes if p <= max_k and any(p not in ap[label] for label in CURVE_LABELS)]
    if missing:
        preview = ", ".join(map(str, missing[:5]))
        raise SystemExit(f"a_p cache has gaps at/before cache max: {preview}")


def ap_all_curves_for_prime(p: int) -> Tuple[int, int, int]:
    if p == 2:
        vals: List[int] = []
        for curve in CURVES:
            a1, a2, a3, a4, a6 = curve.ainvs
            affine = 0
            for x in range(p):
                rhs = (x**3 + a2 * x * x + a4 * x + a6) % p
                for y in range(p):
                    lhs = (y * y + a1 * x * y + a3 * y) % p
                    if lhs == rhs:
                        affine += 1
            vals.append(p + 1 - (affine + 1))
        return vals[0], vals[1], vals[2]

    xs = np.arange(p, dtype=np.int64)
    x2 = xs * xs % p
    x3 = x2 * xs % p
    chi = np.full(p, -1, dtype=np.int8)
    chi[x2] = 1
    chi[0] = 0

    vals = []
    for curve in CURVES:
        a1, a2, a3, a4, a6 = curve.ainvs
        rhs = (x3 + a2 * x2 + a4 * xs + a6) % p
        disc = ((a1 * xs + a3) ** 2 + 4 * rhs) % p
        vals.append(-int(chi[disc].sum()))
    return vals[0], vals[1], vals[2]


def chunk_by_prime_weight(primes: Sequence[int], chunks: int) -> List[List[int]]:
    if not primes:
        return []
    chunks = max(1, min(chunks, len(primes)))
    target = sum(primes) / chunks
    out: List[List[int]] = []
    cur: List[int] = []
    cur_sum = 0
    for p in primes:
        if cur and cur_sum >= target and len(out) < chunks - 1:
            out.append(cur)
            cur = []
            cur_sum = 0
        cur.append(p)
        cur_sum += p
    if cur:
        out.append(cur)
    return out


def compute_ap_chunk(prime_chunk: Sequence[int]) -> List[Tuple[int, int, int, int]]:
    rows = []
    for p in prime_chunk:
        a37, a11, a389 = ap_all_curves_for_prime(p)
        rows.append((p, a37, a11, a389))
    return rows


def extend_ap(
    primes: Sequence[int],
    ap: Dict[str, Dict[int, int]],
    reduction: Dict[str, Dict[int, str]],
    max_k: int,
    workers: int,
) -> Tuple[int, float]:
    missing = [p for p in primes if p <= max_k and any(p not in ap[label] for label in CURVE_LABELS)]
    if not missing:
        return 0, 0.0

    t0 = time.time()
    chunks = chunk_by_prime_weight(missing, max(workers * 3, 1))
    if workers <= 1:
        chunk_results = [compute_ap_chunk(chunk) for chunk in chunks]
    else:
        chunk_results = []
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(compute_ap_chunk, chunk) for chunk in chunks]
            for future in as_completed(futures):
                chunk_results.append(future.result())

    for chunk in chunk_results:
        for p, a37, a11, a389 in chunk:
            for label, value in zip(CURVE_LABELS, (a37, a11, a389)):
                curve = CURVE_BY_LABEL[label]
                ap[label][p] = value
                reduction[label][p] = "bad" if curve.conductor % p == 0 else "good"
    return len(missing), time.time() - t0


def mu_local(label: str, p: int, exponent: int, ap: Mapping[str, Mapping[int, int]], reduction: Mapping[str, Mapping[int, str]]) -> int:
    if exponent == 0:
        return 1
    a = ap[label][p]
    if reduction[label][p] == "good":
        if exponent == 1:
            return -a
        if exponent == 2:
            return p
        return 0
    if a == 0:
        return 0
    return (-a) ** exponent


def compute_curve_rows(
    curve: Curve,
    primes: Sequence[int],
    spf: Sequence[int],
    checkpoints: Sequence[int],
    ap: Mapping[str, Mapping[int, int]],
    reduction: Mapping[str, Mapping[int, str]],
    ap_cache_max: int,
    ap_extended_count: int,
    max_k: int,
) -> List[SweepRow]:
    label = curve.label
    mu = [0] * (max_k + 1)
    mu[1] = 1
    for n in range(2, max_k + 1):
        m = n
        prod = 1
        while m > 1:
            p = spf[m]
            exponent = 0
            while m % p == 0:
                m //= p
                exponent += 1
            prod *= mu_local(label, p, exponent, ap, reduction)
            if prod == 0:
                break
        mu[n] = prod

    rows: List[SweepRow] = []
    wanted = set(checkpoints)
    c_sum = 0.0
    prime_idx = 0
    log_E = 0.0
    log_L2E = 0.0
    log_R_mix = 0.0
    log_C2_tail = 0.0
    good_count = 0

    for n in range(1, max_k + 1):
        if mu[n]:
            c_sum += mu[n] / n
        while prime_idx < len(primes) and primes[prime_idx] == n:
            p = primes[prime_idx]
            a = ap[label][p]
            if reduction[label][p] == "good":
                inv_local = 1.0 - a / p + 1.0 / p
                inv_l2 = 1.0 - a / (p * p) + 1.0 / (p * p * p)
                log_R_mix += -a / p - math.log(inv_local)
                log_C2_tail += (a * a - 2.0 * p) / (2.0 * p * p)
                good_count += 1
            else:
                inv_local = 1.0 - a / p
                inv_l2 = 1.0 - a / (p * p)
            if inv_local <= 0.0:
                raise ValueError(f"non-positive EC local factor for {label} p={p}")
            if inv_l2 <= 0.0:
                raise ValueError(f"non-positive L2E local factor for {label} p={p}")
            log_E += -math.log(inv_local)
            log_L2E += -math.log(inv_l2)
            prime_idx += 1

        if n in wanted:
            E_K = math.exp(log_E)
            D_K = c_sum * E_K
            D_K_zeta2 = D_K * ZETA2
            L2E_partial = math.exp(log_L2E)
            L2E_rank_power = L2E_partial ** curve.rank
            D_over_L2E = D_K_zeta2 / L2E_rank_power if L2E_rank_power else math.inf
            mertens_half = 0.5 * (EULER_GAMMA + math.log(math.log(n)))
            C_mix = math.exp(mertens_half + log_R_mix)
            C2 = math.exp(mertens_half + log_C2_tail)
            rows.append(
                SweepRow(
                    curve=label,
                    K=n,
                    rank=curve.rank,
                    c_K=c_sum,
                    E_K=E_K,
                    D_K=D_K,
                    D_K_zeta2=D_K_zeta2,
                    L2E_partial=L2E_partial,
                    L2E_rank_power=L2E_rank_power,
                    D_zeta2_over_L2E_rank=D_over_L2E,
                    C_mix_good=C_mix,
                    D_mix_good=D_K_zeta2 / C_mix,
                    C_2_good=C2,
                    D_2_good=D_K_zeta2 / C2,
                    p_max=primes[prime_idx - 1] if prime_idx else 0,
                    good_prime_count=good_count,
                    ap_cache_max=ap_cache_max,
                    ap_extended_count=ap_extended_count,
                    product_complete=True,
                )
            )
    return rows


def coefficient_of_variation(values: Sequence[float]) -> float:
    if not values:
        return math.nan
    mean = statistics.fmean(values)
    if mean == 0.0:
        return math.inf
    if len(values) == 1:
        return 0.0
    variance = statistics.fmean((value - mean) ** 2 for value in values)
    return math.sqrt(variance) / abs(mean)


def metric_rows(rows: Sequence[SweepRow]) -> List[MetricRow]:
    getters = {
        "D_zeta2": lambda row: row.D_K_zeta2,
        "D_zeta2_over_L2E_rank": lambda row: row.D_zeta2_over_L2E_rank,
        "D_mix_good": lambda row: row.D_mix_good,
        "D_2_good": lambda row: row.D_2_good,
    }
    out: List[MetricRow] = []
    for name, getter in getters.items():
        by_curve: Dict[str, List[float]] = {label: [] for label in CURVE_LABELS}
        for row in rows:
            by_curve[row.curve].append(getter(row))
        curve_means = {label: statistics.fmean(vals) for label, vals in by_curve.items() if vals}
        within = [coefficient_of_variation(vals) for vals in by_curve.values() if vals]
        means = list(curve_means.values())
        cross_ratio = max(means) / min(means) if means and min(means) > 0 else math.inf
        promoted = (
            cross_ratio < BEST_PRIOR_CROSS_CURVE_RATIO
            and max(within, default=math.inf) < BEST_PRIOR_MAX_WITHIN_CV
        )
        out.append(
            MetricRow(
                normalization=name,
                promoted=promoted,
                max_within_cv=max(within, default=math.nan),
                cross_curve_cv=coefficient_of_variation(means),
                cross_curve_ratio=cross_ratio,
                curve_means=curve_means,
            )
        )
    out.sort(key=lambda row: (not row.promoted, row.cross_curve_ratio, row.max_within_cv))
    return out


def format_float(value: float, digits: int = 12) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf"
    return f"{value:.{digits}g}"


def write_csv(path: Path, rows: Sequence[SweepRow]) -> None:
    fields = [
        "curve",
        "K",
        "rank",
        "c_K",
        "E_K",
        "D_K",
        "D_K_zeta2",
        "L2E_partial",
        "L2E_rank_power",
        "D_zeta2_over_L2E_rank",
        "C_mix_good",
        "D_mix_good",
        "C_2_good",
        "D_2_good",
        "p_max",
        "good_prime_count",
        "ap_cache_max",
        "ap_extended_count",
        "product_complete",
    ]
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "curve": row.curve,
                    "K": row.K,
                    "rank": row.rank,
                    "c_K": format_float(row.c_K, 17),
                    "E_K": format_float(row.E_K, 17),
                    "D_K": format_float(row.D_K, 17),
                    "D_K_zeta2": format_float(row.D_K_zeta2, 17),
                    "L2E_partial": format_float(row.L2E_partial, 17),
                    "L2E_rank_power": format_float(row.L2E_rank_power, 17),
                    "D_zeta2_over_L2E_rank": format_float(row.D_zeta2_over_L2E_rank, 17),
                    "C_mix_good": format_float(row.C_mix_good, 17),
                    "D_mix_good": format_float(row.D_mix_good, 17),
                    "C_2_good": format_float(row.C_2_good, 17),
                    "D_2_good": format_float(row.D_2_good, 17),
                    "p_max": row.p_max,
                    "good_prime_count": row.good_prime_count,
                    "ap_cache_max": row.ap_cache_max,
                    "ap_extended_count": row.ap_extended_count,
                    "product_complete": str(row.product_complete),
                }
            )


def write_report(
    path: Path,
    rows: Sequence[SweepRow],
    metrics: Sequence[MetricRow],
    args: argparse.Namespace,
    phase_times: Mapping[str, float],
    base_diffs: Mapping[Tuple[str, int], float],
) -> None:
    max_k = max(row.K for row in rows)
    max_prime = max(row.p_max for row in rows)
    promotions = [row.normalization for row in metrics if row.promoted]
    status = "NUMERICAL; complete through K={}".format(max_k)
    claim = "No normalization promoted."
    if promotions:
        claim = "Promotion candidate(s): {}.".format(", ".join(promotions))

    lines = [
        "# Koyama EC-NDC Extended Sweep",
        "",
        f"Date: {REPORT_DATE}",
        "",
        "## Status",
        "",
        f"`{status}`",
        "",
        "## Claim",
        "",
        claim,
        "",
        "Promotion rule: cross-curve ratio `< 1.42083` and max within-curve CV `< 0.08567129`.",
        "",
        "## Evidence",
        "",
        "| normalization | promoted | max within-K CV | cross-curve CV | cross-curve ratio | curve means (37a1, 11a1, 389a1) |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in metrics:
        means = ", ".join(format_float(row.curve_means.get(label, math.nan), 10) for label in CURVE_LABELS)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.normalization}`",
                    str(row.promoted),
                    format_float(row.max_within_cv, 10),
                    format_float(row.cross_curve_cv, 10),
                    format_float(row.cross_curve_ratio, 10),
                    means,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            f"Complete products: all CSV rows have `product_complete=True`; largest prime used is `{max_prime}`.",
            "",
            f"At K={max_k}:",
            "",
            "| curve | D*zeta2 | D*zeta2/L2E^rank | D_mix_good | D_2_good | L2E_partial |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        if row.K == max_k:
            lines.append(
                "| "
                + " | ".join(
                    [
                        row.curve,
                        format_float(row.D_K_zeta2, 12),
                        format_float(row.D_zeta2_over_L2E_rank, 12),
                        format_float(row.D_mix_good, 12),
                        format_float(row.D_2_good, 12),
                        format_float(row.L2E_partial, 12),
                    ]
                )
                + " |"
            )

    cmd = (
        "python3 handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py "
        f"--max-k {args.max_k} --workers {args.workers}"
    )
    lines.extend(
        [
            "",
            "## Commands/Timings",
            "",
            f"- Command: `{cmd}`",
            f"- load_inputs: `{phase_times.get('load_inputs', 0.0):.3f}s`",
            f"- extend_ap: `{phase_times.get('extend_ap', 0.0):.3f}s`",
            f"- compute_rows: `{phase_times.get('compute_rows', 0.0):.3f}s`",
            f"- write_outputs: `{phase_times.get('write_outputs', 0.0):.3f}s`",
            f"- total_self_reported: `{phase_times.get('total', 0.0):.3f}s`",
            "",
            "K=1000000 attempt: not run by this command.",
        ]
    )
    if args.max_k >= 1000000:
        lines[-1] = "K=1000000 attempt: included in this run."

    lines.extend(
        [
            "",
            "## CSV Schema",
            "",
            "`curve,K,rank,c_K,E_K,D_K,D_K_zeta2,L2E_partial,L2E_rank_power,D_zeta2_over_L2E_rank,C_mix_good,D_mix_good,C_2_good,D_2_good,p_max,good_prime_count,ap_cache_max,ap_extended_count,product_complete`",
            "",
            "Definitions: `D_K_zeta2` is raw `D*zeta(2)`; `D_zeta2_over_L2E_rank` uses the complete partial `L(E,2)^rank`; `D_mix_good` and `D_2_good` use complete good-prime products only.",
            "",
            "## Verification",
            "",
            f"- Existing cache: `{args.ap_cache}`.",
            f"- Existing base sweep: `{args.base_sweep}`.",
            f"- Output CSV rows: `{len(rows)}`.",
            f"- Output max K: `{max_k}`.",
            f"- Product max prime: `{max_prime}`.",
            "- 100k raw-D cross-checks vs existing `Koyama_EC_NDC.csv`:",
        ]
    )
    for key in sorted(base_diffs):
        lines.append(f"  - `{key[0]}` K=`{key[1]}` abs diff `{base_diffs[key]:.3e}`")

    lines.extend(
        [
            "",
            "## Changed Files",
            "",
            "- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py`",
            "- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.csv`",
            "- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md`",
            "",
            "## Risks",
            "",
            "- Float arithmetic replaces the original mpmath output; 100k raw cross-checks are included.",
            "- No bad-prime-adjusted `D_mix`/`D_2` variant is reported; no finite bad-prime residual was derived here.",
            "- This is a sharp cutoff computation at `rho=1`; it does not test smoothed or complex-zero variants.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main(argv: Sequence[str] | None = None) -> int:
    t_total = time.time()
    args = parse_args(argv)
    args.max_k = int(args.max_k)
    if args.max_k < 2:
        raise SystemExit("--max-k must be at least 2")
    checkpoints = sorted({k for k in args.checkpoints if 2 <= k <= args.max_k} | {args.max_k})

    phase_times: Dict[str, float] = {}
    t0 = time.time()
    primes = sieve_primes(args.max_k)
    ap, reduction, ap_cache_max = read_ap_cache(args.ap_cache)
    base_sweep = read_base_sweep(args.base_sweep)
    validate_cache(primes, ap, min(ap_cache_max, args.max_k))
    spf = build_spf(args.max_k, primes)
    phase_times["load_inputs"] = time.time() - t0

    ap_extended_count, ap_elapsed = extend_ap(primes, ap, reduction, args.max_k, args.workers)
    phase_times["extend_ap"] = ap_elapsed

    t0 = time.time()
    rows: List[SweepRow] = []
    for curve in CURVES:
        rows.extend(
            compute_curve_rows(
                curve,
                primes,
                spf,
                checkpoints,
                ap,
                reduction,
                ap_cache_max,
                ap_extended_count,
                args.max_k,
            )
        )
    rows.sort(key=lambda row: (CURVE_LABELS.index(row.curve), row.K))
    metrics = metric_rows(rows)
    phase_times["compute_rows"] = time.time() - t0

    base_diffs = {}
    for row in rows:
        key = (row.curve, row.K)
        if key in base_sweep:
            base_diffs[key] = abs(row.D_K_zeta2 - base_sweep[key])

    t0 = time.time()
    write_csv(args.out_csv, rows)
    phase_times["write_outputs"] = time.time() - t0
    phase_times["total"] = time.time() - t_total
    write_report(args.out_report, rows, metrics, args, phase_times, base_diffs)

    print(f"wrote {args.out_csv}")
    print(f"wrote {args.out_report}")
    print(f"rows={len(rows)} max_k={args.max_k} ap_extended={ap_extended_count} total={phase_times['total']:.3f}s")
    for row in metrics:
        print(
            f"{row.normalization}: promoted={row.promoted} "
            f"ratio={format_float(row.cross_curve_ratio, 10)} "
            f"max_within_cv={format_float(row.max_within_cv, 10)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
