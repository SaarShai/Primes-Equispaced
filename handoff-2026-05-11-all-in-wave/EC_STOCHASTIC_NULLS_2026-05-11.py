#!/usr/bin/env python3
"""
Staged Sato-Tate null controls for the EC smoothed proxy.

This script is intentionally narrower than the deterministic C2 suite: it tests
the predeclared primary group only,

    real/stochastic, smoothstep, all, alpha=0.75, match=none.

It writes new all-in-wave artifacts and does not overwrite Agent 3 outputs.
Runs with fewer than 512 iid and 128 shared seeds are pilot-only.
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
FOLLOWUP_DIR = PROJECT_DIR / "handoff-2026-05-09-followup"
AGENT3_DIR = PROJECT_DIR / "handoff-2026-05-11-gpt55-wave"
EXTENDED_SWEEP_PATH = FOLLOWUP_DIR / "Koyama_EC_NDC_extended_sweep.py"

DEFAULT_AP_CACHE = AGENT3_DIR / "AGENT3_EC_AP_TABLE_1000000.csv"
DEFAULT_RAW_CSV = SCRIPT_DIR / "EC_STOCHASTIC_NULL_RAW_2026-05-11.csv"
DEFAULT_METRICS_CSV = SCRIPT_DIR / "EC_STOCHASTIC_NULL_METRICS_2026-05-11.csv"
DEFAULT_SUMMARY_CSV = SCRIPT_DIR / "EC_STOCHASTIC_NULL_SUMMARY_2026-05-11.csv"
DEFAULT_REPORT = SCRIPT_DIR / "EC_STOCHASTIC_NULL_REPORT_2026-05-11.md"

OLD_GATE_CROSS_RATIO = 1.42083
OLD_GATE_MAX_WITHIN_CV = 0.08567129
REAL_RATIO = 1.3473754929960748
REAL_MAX_CV = 0.063297427334436704
REAL_SCORE = math.log(REAL_RATIO) + REAL_MAX_CV
PRIMARY_SCORE_SLACK = 0.005

FULL_IID_SEEDS = 512
FULL_SHARED_SEEDS = 128
IID_OLD_PASS_LIMIT = 0.01
IID_PRIMARY_PASS_LIMIT = 0.005
IID_P_LIMIT = 0.01
SHARED_OLD_PASS_LIMIT = 0.02
SHARED_P_LIMIT = 0.02


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
IDENTITY_RANKS = {curve.label: curve.rank for curve in CURVES}


def parse_csv_ints(raw: str) -> Tuple[int, ...]:
    return tuple(int(item.strip()) for item in raw.split(",") if item.strip())


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", choices=("g3", "c2-prime"), default="g3")
    parser.add_argument("--max-k", type=int, default=1_000_000)
    parser.add_argument("--k-grid", type=parse_csv_ints, default=(1000, 3000, 10000, 30000, 100000, 300000, 1000000))
    parser.add_argument("--iid-seeds", type=int, default=16)
    parser.add_argument("--shared-seeds", type=int, default=8)
    parser.add_argument("--iid-seed-start", type=int, default=0)
    parser.add_argument("--shared-seed-start", type=int, default=0)
    parser.add_argument("--ap-cache", type=Path, default=DEFAULT_AP_CACHE)
    parser.add_argument("--raw-csv", type=Path, default=DEFAULT_RAW_CSV)
    parser.add_argument("--metrics-csv", type=Path, default=DEFAULT_METRICS_CSV)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_SUMMARY_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--force", action="store_true", help="allow overwriting outputs")
    return parser.parse_args(argv)


def fmt(value: float, digits: int = 17) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf"
    return f"{value:.{digits}g}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_output_paths(paths: Iterable[Path], force: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if existing and not force:
        joined = "\n".join(f"  {path}" for path in existing)
        raise SystemExit(f"refusing to overwrite existing output(s):\n{joined}\nuse --force")
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def smoothstep_weight(points: np.ndarray, alpha: float = 0.75) -> np.ndarray:
    points = np.asarray(points, dtype=np.float64)
    u = (points - alpha) / (1.0 - alpha)
    return np.where(
        points <= alpha,
        1.0,
        np.where(points < 1.0, 1.0 - u * u * (3.0 - 2.0 * u), 0.0),
    )


def coefficient_of_variation(values: Sequence[float]) -> float:
    if not values:
        return math.nan
    mean = statistics.fmean(values)
    if mean == 0.0:
        return math.inf
    return math.sqrt(statistics.fmean((value - mean) ** 2 for value in values)) / abs(mean)


def old_gate_passes(ratio: float, max_cv: float) -> bool:
    return ratio < OLD_GATE_CROSS_RATIO and max_cv < OLD_GATE_MAX_WITHIN_CV


def primary_gate_passes(ratio: float, max_cv: float) -> bool:
    return old_gate_passes(ratio, max_cv) and math.log(ratio) + max_cv <= REAL_SCORE + PRIMARY_SCORE_SLACK


def read_ap_arrays(path: Path, max_k: int, prime_ints: Sequence[int]) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    ap_arrays = {label: np.zeros(max_k + 1, dtype=np.int64) for label in CURVE_LABELS}
    good_masks = {label: np.zeros(max_k + 1, dtype=bool) for label in CURVE_LABELS}
    seen = {label: set() for label in CURVE_LABELS}
    with path.open(newline="") as fh:
        for raw in csv.DictReader(fh):
            p = int(raw["p"])
            if p > max_k:
                continue
            for label in CURVE_LABELS:
                ap_arrays[label][p] = int(raw[f"a_p({label})"])
                good_masks[label][p] = raw[f"reduction({label})"] == "good"
                seen[label].add(p)
    missing = [p for p in prime_ints if any(p not in seen[label] for label in CURVE_LABELS)]
    if missing:
        raise SystemExit(f"AP cache missing primes at/below max_k, first missing={missing[0]}")
    return ap_arrays, good_masks


def sato_tate_ap(rng: np.random.Generator, p: int) -> int:
    root = math.sqrt(p)
    bound = int(math.floor(2.0 * root))
    while True:
        theta = float(rng.uniform(0.0, math.pi))
        y = float(rng.uniform(0.0, 1.0))
        if y <= math.sin(theta) ** 2:
            return int(max(-bound, min(bound, round(2.0 * root * math.cos(theta)))))


def stochastic_ap_arrays(
    family: str,
    seed: int,
    prime_ints: Sequence[int],
    base_ap: Mapping[str, np.ndarray],
    good_masks: Mapping[str, np.ndarray],
) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    out = {label: base_ap[label].copy() for label in CURVE_LABELS}
    if family == "st_iid":
        for label in CURVE_LABELS:
            arr = out[label]
            mask = good_masks[label]
            for p in prime_ints:
                if mask[p]:
                    arr[p] = sato_tate_ap(rng, p)
        return out
    if family == "st_shared":
        for p in prime_ints:
            value = sato_tate_ap(rng, p)
            for label in CURVE_LABELS:
                if good_masks[label][p]:
                    out[label][p] = value
        return out
    raise ValueError(f"unknown stochastic family {family}")


def mu_local_from_arrays(ap_value: int, is_good: bool, p: int, exponent: int) -> int:
    if exponent == 0:
        return 1
    if is_good:
        if exponent == 1:
            return -ap_value
        if exponent == 2:
            return p
        return 0
    if ap_value == 0:
        return 0
    return (-ap_value) ** exponent


def build_mu_array(ap_arr: np.ndarray, good_mask: np.ndarray, spf: Sequence[int], max_k: int) -> np.ndarray:
    mu = np.zeros(max_k + 1, dtype=np.float64)
    mu[1] = 1.0
    for n in range(2, max_k + 1):
        p = spf[n]
        rest = n
        exponent = 0
        while rest % p == 0:
            rest //= p
            exponent += 1
        local = mu_local_from_arrays(int(ap_arr[p]), bool(good_mask[p]), p, exponent)
        mu[n] = 0.0 if local == 0 else float(local) * mu[rest]
    return mu


def metrics_from_curve_values(values_by_curve: Mapping[str, Sequence[float]]) -> Tuple[float, float, float, Dict[str, float], Dict[str, float]]:
    means = {label: statistics.fmean(values_by_curve[label]) for label in CURVE_LABELS}
    cvs = {label: coefficient_of_variation(values_by_curve[label]) for label in CURVE_LABELS}
    mean_values = list(means.values())
    if any(value <= 0.0 or not math.isfinite(value) for value in mean_values):
        ratio = math.inf
    else:
        ratio = max(mean_values) / min(mean_values)
    cross_cv = coefficient_of_variation(mean_values)
    max_cv = max(cvs.values())
    return ratio, cross_cv, max_cv, means, cvs


def compute_seed_rows(
    family: str,
    seed: int,
    prime_ints: Sequence[int],
    prime_arr: np.ndarray,
    spf: Sequence[int],
    inv_n: np.ndarray,
    k_grid: Sequence[int],
    weights_n: Mapping[int, np.ndarray],
    weights_p: Mapping[int, np.ndarray],
    base_ap: Mapping[str, np.ndarray],
    good_masks: Mapping[str, np.ndarray],
    max_k: int,
) -> Tuple[List[Dict[str, str]], Dict[str, str]]:
    ap_by_label = stochastic_ap_arrays(family, seed, prime_ints, base_ap, good_masks)
    raw_rows: List[Dict[str, str]] = []
    values_by_curve: Dict[str, List[float]] = {label: [] for label in CURVE_LABELS}

    for label in CURVE_LABELS:
        ap_arr = ap_by_label[label]
        good_mask = good_masks[label]
        mu = build_mu_array(ap_arr, good_mask, spf, max_k)
        p_ap = ap_arr[prime_arr.astype(np.int64)].astype(np.float64)
        p_good = good_mask[prime_arr.astype(np.int64)]
        p_float = prime_arr.astype(np.float64)
        inv_p1 = np.where(p_good, 1.0 - p_ap / p_float + 1.0 / p_float, 1.0 - p_ap / p_float)
        inv_p2 = np.where(p_good, 1.0 - p_ap / (p_float * p_float) + 1.0 / (p_float * p_float * p_float), 1.0 - p_ap / (p_float * p_float))
        if np.any(inv_p1 <= 0.0) or np.any(inv_p2 <= 0.0):
            raise ValueError(f"nonpositive local factor in {family} seed {seed} label {label}")
        log_inv_p1 = np.log(inv_p1)
        log_inv_p2 = np.log(inv_p2)

        for k in k_grid:
            p_count = int(np.searchsorted(prime_arr, k, side="right"))
            c_val = float(np.sum(mu[1 : k + 1] * inv_n[1 : k + 1] * weights_n[k]))
            log_p = -float(np.sum(log_inv_p1[:p_count] * weights_p[k]))
            log_l2 = -float(np.sum(log_inv_p2[:p_count] * weights_p[k]))
            p_val = math.exp(log_p)
            l2_val = math.exp(log_l2)
            rank = IDENTITY_RANKS[label]
            l2_rank_power = l2_val ** rank
            d_val = c_val * p_val
            x_val = ZETA2 * d_val / l2_rank_power if l2_rank_power else math.inf
            values_by_curve[label].append(x_val)
            raw_rows.append(
                {
                    "scenario": family,
                    "seed": str(seed),
                    "kernel": "smoothstep",
                    "kernel_param": "none",
                    "match_mode": "none",
                    "mode": "all",
                    "alpha": "0.75",
                    "curve": label,
                    "assigned_rank": str(rank),
                    "K": str(k),
                    "c": fmt(c_val),
                    "P": fmt(p_val),
                    "D": fmt(d_val),
                    "D_zeta2": fmt(ZETA2 * d_val),
                    "L2": fmt(l2_val),
                    "L2_rank_power": fmt(l2_rank_power),
                    "X": fmt(x_val),
                    "p_max": str(int(prime_arr[p_count - 1]) if p_count else 0),
                    "prime_count": str(p_count),
                    "product_complete": "True",
                }
            )

    ratio, cross_cv, max_cv, means, cvs = metrics_from_curve_values(values_by_curve)
    seed_score = math.log(ratio) + max_cv if ratio > 0.0 and math.isfinite(ratio) else math.inf
    metric_row = {
        "scenario": family,
        "seed": str(seed),
        "kernel": "smoothstep",
        "kernel_param": "none",
        "match_mode": "none",
        "mode": "all",
        "alpha": "0.75",
        "cross_curve_ratio": fmt(ratio),
        "cross_curve_cv": fmt(cross_cv),
        "max_within_cv": fmt(max_cv),
        "score": fmt(seed_score),
        "passes_old_gate": str(old_gate_passes(ratio, max_cv)),
        "passes_primary_gate": str(primary_gate_passes(ratio, max_cv)),
        **{f"mean_{label}": fmt(means[label]) for label in CURVE_LABELS},
        **{f"cv_{label}": fmt(cvs[label]) for label in CURVE_LABELS},
    }
    return raw_rows, metric_row


def write_dict_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows to write for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize_family(metrics: Sequence[Mapping[str, str]], family: str, full_count: int) -> Dict[str, str]:
    rows = [row for row in metrics if row["scenario"] == family]
    if not rows:
        return {
            "null_family": family,
            "n_trials": "0",
            "gate_status": "NOT_RUN",
        }
    old_count = sum(1 for row in rows if row["passes_old_gate"] == "True")
    primary_count = sum(1 for row in rows if row["passes_primary_gate"] == "True")
    n = len(rows)
    scores = [float(row["score"]) for row in rows]
    ratios = [float(row["cross_curve_ratio"]) for row in rows]
    max_cvs = [float(row["max_within_cv"]) for row in rows]
    finite_scores = [value for value in scores if math.isfinite(value)]
    finite_ratios = [value for value in ratios if math.isfinite(value)]
    p_score = (1 + sum(1 for value in scores if value <= REAL_SCORE)) / (n + 1)
    p_ratio = (1 + sum(1 for value in ratios if value <= REAL_RATIO)) / (n + 1)
    p_cv = (1 + sum(1 for value in max_cvs if value <= REAL_MAX_CV)) / (n + 1)
    p_pareto = (
        1
        + sum(
            1
            for ratio, max_cv in zip(ratios, max_cvs)
            if ratio <= REAL_RATIO and max_cv <= REAL_MAX_CV
        )
    ) / (n + 1)
    p_old_pareto = (
        1
        + sum(
            1
            for ratio, max_cv in zip(ratios, max_cvs)
            if ratio < OLD_GATE_CROSS_RATIO and max_cv < OLD_GATE_MAX_WITHIN_CV
        )
    ) / (n + 1)
    best_score_row = min(rows, key=lambda row: float(row["score"]))
    best_ratio_row = min(rows, key=lambda row: float(row["cross_curve_ratio"]))
    old_rate = old_count / n
    primary_rate = primary_count / n
    if n < full_count:
        gate_status = "PILOT_ONLY"
    elif family == "st_iid":
        gate_status = "PASS" if (
            old_rate <= IID_OLD_PASS_LIMIT
            and primary_rate <= IID_PRIMARY_PASS_LIMIT
            and p_score <= IID_P_LIMIT
            and p_ratio <= IID_P_LIMIT
        ) else "FAIL"
    else:
        gate_status = "PASS" if (
            old_rate <= SHARED_OLD_PASS_LIMIT
            and p_score <= SHARED_P_LIMIT
        ) else "FAIL"
    return {
        "null_family": family,
        "kernel": "smoothstep",
        "kernel_param": "none",
        "match_mode": "none",
        "mode": "all",
        "alpha": "0.75",
        "n_trials": str(n),
        "full_required_trials": str(full_count),
        "old_pass_count": str(old_count),
        "old_pass_rate": fmt(old_rate),
        "primary_pass_count": str(primary_count),
        "primary_pass_rate": fmt(primary_rate),
        "real_ratio": fmt(REAL_RATIO),
        "real_max_within_cv": fmt(REAL_MAX_CV),
        "real_score": fmt(REAL_SCORE),
        "best_null_ratio": best_ratio_row["cross_curve_ratio"],
        "best_null_ratio_seed": best_ratio_row["seed"],
        "best_null_max_within_cv_for_best_ratio": best_ratio_row["max_within_cv"],
        "best_null_score": best_score_row["score"],
        "best_null_score_seed": best_score_row["seed"],
        "score_min": fmt(min(finite_scores) if finite_scores else math.inf),
        "score_median": fmt(statistics.median(finite_scores) if finite_scores else math.inf),
        "ratio_min": fmt(min(finite_ratios) if finite_ratios else math.inf),
        "ratio_median": fmt(statistics.median(finite_ratios) if finite_ratios else math.inf),
        "p_ratio": fmt(p_ratio),
        "p_score": fmt(p_score),
        "p_cv": fmt(p_cv),
        "p_pareto": fmt(p_pareto),
        "p_old_pareto": fmt(p_old_pareto),
        "gate_status": gate_status,
    }


def apply_gate_status(summary: Dict[str, str], gate: str) -> Dict[str, str]:
    if gate == "g3":
        return summary
    if gate != "c2-prime":
        raise ValueError(f"unknown gate {gate}")
    n = int(summary.get("n_trials", "0"))
    required = int(summary.get("full_required_trials", "0"))
    if n < required:
        summary["gate_status"] = "PILOT_ONLY"
        return summary
    old_rate = float(summary["old_pass_rate"])
    primary_rate = float(summary["primary_pass_rate"])
    p_cv = float(summary["p_cv"])
    p_pareto = float(summary["p_pareto"])
    if summary["null_family"] == "st_iid":
        passed = (
            old_rate <= IID_OLD_PASS_LIMIT
            and primary_rate <= IID_PRIMARY_PASS_LIMIT
            and p_cv <= IID_P_LIMIT
            and p_pareto <= IID_P_LIMIT
        )
    else:
        passed = (
            old_rate <= SHARED_OLD_PASS_LIMIT
            and p_cv <= SHARED_P_LIMIT
            and p_pareto <= SHARED_P_LIMIT
        )
    summary["gate_status"] = "PASS" if passed else "FAIL"
    return summary


def write_report(
    path: Path,
    args: argparse.Namespace,
    summaries: Sequence[Mapping[str, str]],
    metrics: Sequence[Mapping[str, str]],
    hashes: Mapping[str, str],
    elapsed: float,
) -> None:
    overall = "PILOT_ONLY"
    if summaries and all(row.get("gate_status") == "PASS" for row in summaries):
        overall = "FULL_G3_PASS"
    elif any(row.get("gate_status") == "FAIL" for row in summaries):
        overall = "G3_FAIL"

    lines = [
        "---",
        "schema_version: 1",
        'title: "EC stochastic Sato-Tate null controls"',
        "date: 2026-05-11",
        "type: report",
        "tier: working",
        f"status: {overall}",
        "confidence: 0.70",
        "sources:",
        "  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md",
        "  - handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py",
        "tags: [ec-ndc, smoothing, sato-tate, null-controls]",
        "---",
        "",
        "# EC Stochastic Sato-Tate Null Controls",
        "",
        f"status: `{overall}`",
        "",
        "## Verdict",
        "",
        "Do not promote from this run. Runs below `512` iid seeds and `128` shared seeds are pilot-only by the predeclared C2 gate.",
        "",
        "## Exact Run",
        "",
        f"- Command: `{' '.join(sys.argv)}`",
        f"- Gate: `{args.gate}`",
        f"- Python: `{platform.python_version()}`",
        f"- NumPy: `{np.__version__}`",
        f"- Script SHA256: `{hashes['script']}`",
        f"- AP cache: `{args.ap_cache}`",
        f"- AP cache SHA256: `{hashes['ap_cache']}`",
        f"- K grid: `{','.join(map(str, args.k_grid))}`",
        f"- iid seeds: `{args.iid_seed_start}..{args.iid_seed_start + args.iid_seeds - 1}`",
        f"- shared seeds: `{args.shared_seed_start}..{args.shared_seed_start + args.shared_seeds - 1}`",
        f"- Elapsed seconds: `{elapsed:.3f}`",
        "",
        "## Summary",
        "",
        "| family | trials | old pass | primary pass | best ratio | best score | p_ratio | p_score | p_cv | p_pareto | status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            f"| `{row['null_family']}` | {row['n_trials']}/{row['full_required_trials']} | "
            f"{row['old_pass_count']} ({row['old_pass_rate']}) | "
            f"{row['primary_pass_count']} ({row['primary_pass_rate']}) | "
            f"{row['best_null_ratio']} | {row['best_null_score']} | "
            f"{row['p_ratio']} | {row['p_score']} | {row['p_cv']} | {row['p_pareto']} | `{row['gate_status']}` |"
        )

    lines.extend(
        [
            "",
            "## Best Null Rows",
            "",
            "| family | seed | pass old | pass primary | ratio | max CV | score | means (37a1, 11a1, 389a1) |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for family in ("st_iid", "st_shared"):
        rows = [row for row in metrics if row["scenario"] == family]
        for row in sorted(rows, key=lambda r: float(r["score"]))[:8]:
            means = ", ".join(row[f"mean_{label}"] for label in CURVE_LABELS)
            lines.append(
                f"| `{family}` | {row['seed']} | `{row['passes_old_gate']}` | `{row['passes_primary_gate']}` | "
                f"{row['cross_curve_ratio']} | {row['max_within_cv']} | {row['score']} | {means} |"
            )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Full G3 or C2-prime remains open unless this script is run with the predeclared full seed counts and both families satisfy the selected gate.",
            "",
            "## Files",
            "",
            f"- `{args.raw_csv}`",
            f"- `{args.metrics_csv}`",
            f"- `{args.summary_csv}`",
            f"- `{path}`",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main(argv: Sequence[str] | None = None) -> int:
    t0 = time.time()
    args = parse_args(argv)
    args.k_grid = tuple(sorted(k for k in set(args.k_grid) if 2 <= k <= args.max_k))
    ensure_output_paths((args.raw_csv, args.metrics_csv, args.summary_csv, args.report), args.force)

    primes = EXT.sieve_primes(args.max_k)
    prime_ints = [p for p in primes if p <= args.max_k]
    prime_arr = np.asarray(prime_ints, dtype=np.int64)
    spf = EXT.build_spf(args.max_k, prime_ints)
    base_ap, good_masks = read_ap_arrays(args.ap_cache, args.max_k, prime_ints)
    inv_n = np.zeros(args.max_k + 1, dtype=np.float64)
    inv_n[1:] = 1.0 / np.arange(1, args.max_k + 1, dtype=np.float64)
    weights_n = {k: smoothstep_weight(np.arange(1, k + 1, dtype=np.float64) / float(k)) for k in args.k_grid}
    weights_p = {
        k: smoothstep_weight(prime_arr[: int(np.searchsorted(prime_arr, k, side="right"))].astype(np.float64) / float(k))
        for k in args.k_grid
    }

    raw_rows: List[Dict[str, str]] = []
    metric_rows: List[Dict[str, str]] = []
    for family, seed_start, n_seeds in (
        ("st_iid", args.iid_seed_start, args.iid_seeds),
        ("st_shared", args.shared_seed_start, args.shared_seeds),
    ):
        for seed in range(seed_start, seed_start + n_seeds):
            seed_raw, seed_metric = compute_seed_rows(
                family,
                seed,
                prime_ints,
                prime_arr,
                spf,
                inv_n,
                args.k_grid,
                weights_n,
                weights_p,
                base_ap,
                good_masks,
                args.max_k,
            )
            raw_rows.extend(seed_raw)
            metric_rows.append(seed_metric)
            print(
                f"{family} seed={seed} pass_old={seed_metric['passes_old_gate']} "
                f"ratio={seed_metric['cross_curve_ratio']} max_cv={seed_metric['max_within_cv']} score={seed_metric['score']}"
            )

    summaries = [
        apply_gate_status(summarize_family(metric_rows, "st_iid", FULL_IID_SEEDS), args.gate),
        apply_gate_status(summarize_family(metric_rows, "st_shared", FULL_SHARED_SEEDS), args.gate),
    ]
    hashes = {
        "script": sha256_file(Path(__file__)),
        "ap_cache": sha256_file(args.ap_cache),
    }
    write_dict_csv(args.raw_csv, raw_rows)
    write_dict_csv(args.metrics_csv, metric_rows)
    write_dict_csv(args.summary_csv, summaries)
    elapsed = time.time() - t0
    write_report(args.report, args, summaries, metric_rows, hashes, elapsed)

    for row in summaries:
        print(
            f"{row['null_family']} trials={row['n_trials']}/{row['full_required_trials']} "
            f"old_pass={row['old_pass_count']} primary_pass={row['primary_pass_count']} "
            f"p_ratio={row['p_ratio']} p_score={row['p_score']} "
            f"p_cv={row['p_cv']} p_pareto={row['p_pareto']} status={row['gate_status']}"
        )
    print(f"wrote {args.raw_csv}")
    print(f"wrote {args.metrics_csv}")
    print(f"wrote {args.summary_csv}")
    print(f"wrote {args.report}")
    print(f"elapsed={elapsed:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
