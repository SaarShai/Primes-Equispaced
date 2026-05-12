#!/usr/bin/env python3
"""
Reproduce and adversarially test the finite smoothed EC-NDC proxy.

This script intentionally treats the proxy as a numerical lead only.  It writes
the full a_p cache used by the run, raw proxy rows, summary metrics, and a short
Markdown report with command/runtime/hash metadata.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import math
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
SOURCE_DIR = PROJECT_DIR / "handoff-2026-05-09-followup"
EXTENDED_SWEEP_PATH = SOURCE_DIR / "Koyama_EC_NDC_extended_sweep.py"
SOURCE_AP_CACHE = SOURCE_DIR / "Koyama_EC_NDC_ap_table_100000.csv"

DEFAULT_RAW_CSV = SCRIPT_DIR / "AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv"
DEFAULT_METRICS_CSV = SCRIPT_DIR / "AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv"
DEFAULT_REPORT = SCRIPT_DIR / "AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md"
DEFAULT_AP_CACHE_OUT = SCRIPT_DIR / "AGENT3_EC_AP_TABLE_1000000.csv"

DEFAULT_K_GRID = (1000, 3000, 10000, 30000, 100000, 300000, 1000000)
DEFAULT_ALPHAS = (0.0, 0.25, 0.50, 0.65, 0.75, 0.85, 0.92)
GATE_CROSS_RATIO = 1.42083
GATE_MAX_WITHIN_CV = 0.08567129

MODE_FLAGS: Mapping[str, Tuple[bool, bool, bool]] = {
    "sharp": (False, False, False),
    "c_only": (True, False, False),
    "P_only": (False, True, False),
    "L2_only": (False, False, True),
    "cP_only": (True, True, False),
    "cL2_only": (True, False, True),
    "PL2_only": (False, True, True),
    "all": (True, True, True),
}


def load_extended_module():
    spec = importlib.util.spec_from_file_location("ec_ndc_extended_sweep", EXTENDED_SWEEP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {EXTENDED_SWEEP_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


EXT = load_extended_module()
CURVES = EXT.CURVES
CURVE_LABELS = EXT.CURVE_LABELS
CURVE_BY_LABEL = EXT.CURVE_BY_LABEL
ZETA2 = EXT.ZETA2


def parse_csv_floats(raw: str) -> Tuple[float, ...]:
    out = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            out.append(float(item))
    return tuple(out)


def parse_csv_ints(raw: str) -> Tuple[int, ...]:
    out = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            out.append(int(item))
    return tuple(out)


def parse_modes(raw: str) -> Tuple[str, ...]:
    modes = tuple(item.strip() for item in raw.split(",") if item.strip())
    unknown = [mode for mode in modes if mode not in MODE_FLAGS]
    if unknown:
        raise SystemExit(f"unknown mode(s): {', '.join(unknown)}")
    return modes


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-k", type=int, default=1_000_000)
    parser.add_argument("--k-grid", type=parse_csv_ints, default=DEFAULT_K_GRID)
    parser.add_argument("--alphas", type=parse_csv_floats, default=DEFAULT_ALPHAS)
    parser.add_argument("--modes", type=parse_modes, default=tuple(MODE_FLAGS))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--ap-cache", type=Path, default=SOURCE_AP_CACHE)
    parser.add_argument("--ap-cache-out", type=Path, default=DEFAULT_AP_CACHE_OUT)
    parser.add_argument("--raw-csv", type=Path, default=DEFAULT_RAW_CSV)
    parser.add_argument("--metrics-csv", type=Path, default=DEFAULT_METRICS_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args(argv)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def choose_ap_cache(args: argparse.Namespace, max_prime_needed: int) -> Path:
    if args.ap_cache != SOURCE_AP_CACHE or not args.ap_cache_out.exists():
        return args.ap_cache
    try:
        _, _, cache_max = EXT.read_ap_cache(args.ap_cache_out)
    except Exception:
        return args.ap_cache
    return args.ap_cache_out if cache_max >= max_prime_needed else args.ap_cache


def smooth_weight(t: np.ndarray, alpha: float) -> np.ndarray:
    t = np.asarray(t, dtype=np.float64)
    if alpha <= 0.0:
        u = t
        return np.where(t < 1.0, 1.0 - u * u * (3.0 - 2.0 * u), 0.0)
    if alpha >= 1.0:
        return np.where(t <= 1.0, 1.0, 0.0)
    u = (t - alpha) / (1.0 - alpha)
    return np.where(t <= alpha, 1.0, np.where(t < 1.0, 1.0 - u * u * (3.0 - 2.0 * u), 0.0))


def local_inverse_factors(curve, p: int, ap: Mapping[str, Mapping[int, int]], reduction: Mapping[str, Mapping[int, str]]) -> Tuple[float, float]:
    a = ap[curve.label][p]
    if reduction[curve.label][p] == "good":
        inv_p1 = 1.0 - a / p + 1.0 / p
        inv_p2 = 1.0 - a / (p * p) + 1.0 / (p * p * p)
    else:
        inv_p1 = 1.0 - a / p
        inv_p2 = 1.0 - a / (p * p)
    if inv_p1 <= 0.0 or inv_p2 <= 0.0:
        raise ValueError(f"non-positive local factor for {curve.label} at p={p}")
    return inv_p1, inv_p2


def build_mu_array(
    curve,
    spf: Sequence[int],
    ap: Mapping[str, Mapping[int, int]],
    reduction: Mapping[str, Mapping[int, str]],
    max_k: int,
) -> np.ndarray:
    mu = np.zeros(max_k + 1, dtype=np.float64)
    mu[1] = 1.0
    for n in range(2, max_k + 1):
        m = n
        prod = 1
        while m > 1:
            p = spf[m]
            exponent = 0
            while m % p == 0:
                m //= p
                exponent += 1
            prod *= EXT.mu_local(curve.label, p, exponent, ap, reduction)
            if prod == 0:
                break
        mu[n] = float(prod)
    return mu


def coefficient_of_variation(values: Sequence[float]) -> float:
    if not values:
        return math.nan
    mean = statistics.fmean(values)
    if mean == 0.0:
        return math.inf
    variance = statistics.fmean((value - mean) ** 2 for value in values)
    return math.sqrt(variance) / abs(mean)


def fmt(value: float, digits: int = 17) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf"
    return f"{value:.{digits}g}"


def write_ap_cache(
    path: Path,
    primes: Sequence[int],
    ap: Mapping[str, Mapping[int, int]],
    reduction: Mapping[str, Mapping[int, str]],
    max_k: int,
) -> None:
    fields = ["p"]
    fields.extend(f"a_p({label})" for label in CURVE_LABELS)
    fields.extend(f"reduction({label})" for label in CURVE_LABELS)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for p in primes:
            if p > max_k:
                break
            writer.writerow(
                {
                    "p": p,
                    **{f"a_p({label})": ap[label][p] for label in CURVE_LABELS},
                    **{f"reduction({label})": reduction[label][p] for label in CURVE_LABELS},
                }
            )


def compute_raw_rows(
    args: argparse.Namespace,
    primes: Sequence[int],
    spf: Sequence[int],
    ap: Mapping[str, Mapping[int, int]],
    reduction: Mapping[str, Mapping[int, str]],
    ap_cache_in: Path,
    ap_cache_max: int,
    ap_extended_count: int,
) -> List[Dict[str, str]]:
    k_grid = tuple(k for k in args.k_grid if 2 <= k <= args.max_k)
    if args.max_k not in k_grid:
        k_grid = tuple(sorted((*k_grid, args.max_k)))

    n_all = np.arange(args.max_k + 1, dtype=np.float64)
    inv_n = np.zeros(args.max_k + 1, dtype=np.float64)
    inv_n[1:] = 1.0 / n_all[1:]
    prime_arr = np.asarray([p for p in primes if p <= args.max_k], dtype=np.float64)
    prime_ints = [p for p in primes if p <= args.max_k]

    raw_rows: List[Dict[str, str]] = []
    for curve in CURVES:
        mu = build_mu_array(curve, spf, ap, reduction, args.max_k)
        log_inv_p1 = []
        log_inv_p2 = []
        for p in prime_ints:
            inv_p1, inv_p2 = local_inverse_factors(curve, p, ap, reduction)
            log_inv_p1.append(math.log(inv_p1))
            log_inv_p2.append(math.log(inv_p2))
        log_inv_p1_arr = np.asarray(log_inv_p1, dtype=np.float64)
        log_inv_p2_arr = np.asarray(log_inv_p2, dtype=np.float64)

        for K in k_grid:
            n_slice = n_all[1 : K + 1]
            mu_over_n = mu[1 : K + 1] * inv_n[1 : K + 1]
            p_count = int(np.searchsorted(prime_arr, K, side="right"))
            p_slice = prime_arr[:p_count]
            p_max = int(p_slice[-1]) if p_count else 0
            for alpha in args.alphas:
                weight_n_smooth = smooth_weight(n_slice / float(K), alpha)
                weight_p_smooth = smooth_weight(p_slice / float(K), alpha)
                for mode in args.modes:
                    smooth_c, smooth_P, smooth_L2 = MODE_FLAGS[mode]
                    weight_n = weight_n_smooth if smooth_c else 1.0
                    weight_P = weight_p_smooth if smooth_P else 1.0
                    weight_L2 = weight_p_smooth if smooth_L2 else 1.0

                    c_val = float(np.sum(mu_over_n * weight_n))
                    log_P = -float(np.sum(log_inv_p1_arr[:p_count] * weight_P))
                    log_L2 = -float(np.sum(log_inv_p2_arr[:p_count] * weight_L2))
                    P_val = math.exp(log_P)
                    L2_val = math.exp(log_L2)
                    L2_rank_power = L2_val ** curve.rank
                    D_val = c_val * P_val
                    X_val = ZETA2 * D_val / L2_rank_power if L2_rank_power else math.inf
                    raw_rows.append(
                        {
                            "curve": curve.label,
                            "rank": str(curve.rank),
                            "conductor": str(curve.conductor),
                            "K": str(K),
                            "alpha": fmt(alpha, 12),
                            "mode": mode,
                            "smooth_c": str(smooth_c),
                            "smooth_P": str(smooth_P),
                            "smooth_L2": str(smooth_L2),
                            "c": fmt(c_val),
                            "P": fmt(P_val),
                            "D": fmt(D_val),
                            "D_zeta2": fmt(ZETA2 * D_val),
                            "L2": fmt(L2_val),
                            "L2_rank_power": fmt(L2_rank_power),
                            "X": fmt(X_val),
                            "p_max": str(p_max),
                            "prime_count": str(p_count),
                            "ap_cache_in": str(ap_cache_in),
                            "ap_cache_max_in": str(ap_cache_max),
                            "ap_extended_count": str(ap_extended_count),
                            "product_complete": "True",
                        }
                    )
    return raw_rows


def compute_metrics(raw_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, str]]:
    by_group: Dict[Tuple[str, str], Dict[str, List[float]]] = {}
    for row in raw_rows:
        key = (row["mode"], row["alpha"])
        by_group.setdefault(key, {label: [] for label in CURVE_LABELS})
        by_group[key][row["curve"]].append(float(row["X"]))

    metric_rows: List[Dict[str, str]] = []
    for (mode, alpha), by_curve in by_group.items():
        curve_means = {
            label: statistics.fmean(values)
            for label, values in by_curve.items()
            if values
        }
        within = {
            label: coefficient_of_variation(values)
            for label, values in by_curve.items()
            if values
        }
        means = list(curve_means.values())
        cross_ratio = max(means) / min(means) if means and min(means) > 0 else math.inf
        max_within_cv = max(within.values()) if within else math.nan
        promoted = cross_ratio < GATE_CROSS_RATIO and max_within_cv < GATE_MAX_WITHIN_CV
        metric_rows.append(
            {
                "mode": mode,
                "alpha": alpha,
                "passes_old_gate": str(promoted),
                "max_within_cv": fmt(max_within_cv),
                "cross_curve_cv": fmt(coefficient_of_variation(means)),
                "cross_curve_ratio": fmt(cross_ratio),
                **{f"mean_{label}": fmt(curve_means.get(label, math.nan)) for label in CURVE_LABELS},
                **{f"cv_{label}": fmt(within.get(label, math.nan)) for label in CURVE_LABELS},
            }
        )
    metric_rows.sort(
        key=lambda row: (
            row["mode"] != "all",
            row["passes_old_gate"] != "True",
            float(row["cross_curve_ratio"]),
            float(row["max_within_cv"]),
            row["mode"],
            float(row["alpha"]),
        )
    )
    return metric_rows


def write_dict_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows to write for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    args: argparse.Namespace,
    raw_rows: Sequence[Mapping[str, str]],
    metrics: Sequence[Mapping[str, str]],
    timings: Mapping[str, float],
    ap_cache_in: Path,
    hashes: Mapping[str, str],
) -> None:
    all_rows = [row for row in metrics if row["mode"] == "all"]
    passing_all = [row for row in all_rows if row["passes_old_gate"] == "True"]
    passing_any = [row for row in metrics if row["passes_old_gate"] == "True"]
    passing_non_all = [row for row in passing_any if row["mode"] != "all"]
    best_all = min(all_rows, key=lambda row: (float(row["cross_curve_ratio"]), float(row["max_within_cv"])))
    best_passing_non_all = min(
        passing_non_all,
        key=lambda row: (float(row["cross_curve_ratio"]), float(row["max_within_cv"])),
    ) if passing_non_all else None
    lowest_ratio_any = min(metrics, key=lambda row: (float(row["cross_curve_ratio"]), float(row["max_within_cv"])))

    lines = [
        "---",
        "schema_version: 1",
        'title: "Agent 3 EC smoothed proxy reproduction"',
        "date: 2026-05-11",
        "type: report",
        "tier: working",
        "status: NUMERICAL_LEAD_ONLY",
        "confidence: 0.42",
        "sources:",
        "  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py",
        "  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv",
        "  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv",
        "  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv",
        "tags: [ec-ndc, smoothing, reproduction, claim-safe]",
        "---",
        "",
        "# Agent 3 EC Smoothed Proxy Reproduction",
        "",
        "status: `NUMERICAL_LEAD_ONLY`",
        "confidence: 0.42 for finite-pattern reproduction; 0.10 for asymptotic universality",
        "",
        "## Verdict",
        "",
        "Do not promote. The smoothed proxy is now reproducible as a finite numerical pattern, but component ablations show the old gate is not specific to the full `L2^rank` normalization.",
        "",
        "## Exact Run",
        "",
        f"- Command: `{' '.join(sys.argv)}`",
        f"- Python: `{platform.python_version()}`",
        f"- NumPy: `{np.__version__}`",
        f"- Script SHA256: `{hashes['script']}`",
        f"- Input AP cache: `{ap_cache_in}`",
        f"- Input AP cache SHA256: `{hashes['ap_cache_in']}`",
        f"- Output AP cache: `{args.ap_cache_out}`",
        f"- Output AP cache SHA256: `{hashes['ap_cache_out']}`",
        f"- Raw CSV: `{args.raw_csv}`",
        f"- Metrics CSV: `{args.metrics_csv}`",
        f"- K grid: `{','.join(str(k) for k in args.k_grid)}`",
        f"- Alpha grid: `{','.join(fmt(a, 12) for a in args.alphas)}`",
        f"- Modes: `{','.join(args.modes)}`",
        "",
        "## Timings",
        "",
        "| phase | seconds |",
        "|---|---:|",
    ]
    for name in ("load", "extend_ap", "write_ap_cache", "compute_raw", "write_csv", "total"):
        lines.append(f"| `{name}` | {timings.get(name, 0.0):.3f} |")

    lines.extend(
        [
            "",
            "## Old Gate Results",
            "",
            f"Old gate: cross-curve ratio `< {GATE_CROSS_RATIO}` and max within-curve CV `< {GATE_MAX_WITHIN_CV}`.",
            "",
            f"- Full all-component smoothing passes old gate for {len(passing_all)} alpha values.",
            f"- Any mode passes old gate for {len(passing_any)} mode/alpha values.",
            f"- Best full smoothing: alpha `{best_all['alpha']}`, ratio `{best_all['cross_curve_ratio']}`, max CV `{best_all['max_within_cv']}`.",
            (
                f"- Best passing non-all ablation: mode `{best_passing_non_all['mode']}`, alpha `{best_passing_non_all['alpha']}`, "
                f"ratio `{best_passing_non_all['cross_curve_ratio']}`, max CV `{best_passing_non_all['max_within_cv']}`."
                if best_passing_non_all
                else "- No non-all ablation passes the old gate."
            ),
            (
                f"- Lowest ratio any mode, not necessarily passing: mode `{lowest_ratio_any['mode']}`, alpha `{lowest_ratio_any['alpha']}`, "
                f"ratio `{lowest_ratio_any['cross_curve_ratio']}`, max CV `{lowest_ratio_any['max_within_cv']}`."
            ),
            "",
            "| mode | alpha | passes | ratio | max CV | means (37a1, 11a1, 389a1) |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in metrics[:24]:
        means = ", ".join(row[f"mean_{label}"] for label in CURVE_LABELS)
        lines.append(
            f"| `{row['mode']}` | {row['alpha']} | {row['passes_old_gate']} | {row['cross_curve_ratio']} | {row['max_within_cv']} | {means} |"
        )

    lines.extend(
        [
            "",
            "## Raw Full-Smoothing Rows At Max K",
            "",
            "| curve | alpha | X | c | P | L2 |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    max_k = max(int(row["K"]) for row in raw_rows)
    for row in raw_rows:
        if row["mode"] == "all" and int(row["K"]) == max_k:
            lines.append(f"| {row['curve']} | {row['alpha']} | {row['X']} | {row['c']} | {row['P']} | {row['L2']} |")

    lines.extend(
        [
            "",
            "## Do Not Promote Unless",
            "",
            "- A predeclared alpha, preferably `0.75`, survives holdout curves across ranks/conductors.",
            "- The signal survives a denser K grid and larger K, with tail-only drift controlled.",
            "- Component ablation shows the proposed normalization is load-bearing, not merely endpoint smoothing.",
            "- A theorem explains the smoothing kernel and normalization from an explicit Euler/Perron transform.",
            "",
            "## Files",
            "",
            f"- `{args.ap_cache_out}`",
            f"- `{args.raw_csv}`",
            f"- `{args.metrics_csv}`",
            f"- `{path}`",
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
    args.k_grid = tuple(sorted(set(k for k in args.k_grid if 2 <= k <= args.max_k)))
    if not args.k_grid:
        raise SystemExit("--k-grid has no entries at or below --max-k")

    timings: Dict[str, float] = {}

    t0 = time.time()
    primes = EXT.sieve_primes(args.max_k)
    max_prime_needed = primes[-1] if primes else 0
    ap_cache_in = choose_ap_cache(args, max_prime_needed)
    spf = EXT.build_spf(args.max_k, primes)
    ap, reduction, ap_cache_max = EXT.read_ap_cache(ap_cache_in)
    EXT.validate_cache(primes, ap, min(ap_cache_max, args.max_k))
    timings["load"] = time.time() - t0

    ap_extended_count, ap_elapsed = EXT.extend_ap(primes, ap, reduction, args.max_k, args.workers)
    timings["extend_ap"] = ap_elapsed

    t0 = time.time()
    write_ap_cache(args.ap_cache_out, primes, ap, reduction, args.max_k)
    timings["write_ap_cache"] = time.time() - t0

    t0 = time.time()
    raw_rows = compute_raw_rows(args, primes, spf, ap, reduction, ap_cache_in, ap_cache_max, ap_extended_count)
    metrics = compute_metrics(raw_rows)
    timings["compute_raw"] = time.time() - t0

    t0 = time.time()
    write_dict_csv(args.raw_csv, raw_rows)
    write_dict_csv(args.metrics_csv, metrics)
    timings["write_csv"] = time.time() - t0

    hashes = {
        "script": sha256_file(Path(__file__)),
        "ap_cache_in": sha256_file(ap_cache_in),
        "ap_cache_out": sha256_file(args.ap_cache_out),
    }
    timings["total"] = time.time() - t_total
    write_report(args.report, args, raw_rows, metrics, timings, ap_cache_in, hashes)

    print(f"wrote {args.ap_cache_out}")
    print(f"wrote {args.raw_csv}")
    print(f"wrote {args.metrics_csv}")
    print(f"wrote {args.report}")
    print(f"rows={len(raw_rows)} metrics={len(metrics)} total={timings['total']:.3f}s")
    for row in metrics[:12]:
        print(
            f"{row['mode']} alpha={row['alpha']} pass={row['passes_old_gate']} "
            f"ratio={row['cross_curve_ratio']} max_cv={row['max_within_cv']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
