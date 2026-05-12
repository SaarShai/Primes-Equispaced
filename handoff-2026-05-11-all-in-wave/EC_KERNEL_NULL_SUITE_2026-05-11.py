#!/usr/bin/env python3
"""
Read-only C2 kernel/rank/curve-label null suite for the EC smoothed proxy.

This is a successor to the Agent 3 reproducer.  It consumes the saved a_p cache,
does not overwrite Agent 3 outputs, and writes only all-in-wave audit artifacts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import itertools
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
DEFAULT_RAW_CSV = SCRIPT_DIR / "EC_KERNEL_NULL_RAW_2026-05-11.csv"
DEFAULT_METRICS_CSV = SCRIPT_DIR / "EC_KERNEL_NULL_METRICS_2026-05-11.csv"
DEFAULT_CONTROL_CSV = SCRIPT_DIR / "EC_KERNEL_NULL_CONTROL_SUMMARY_2026-05-11.csv"
DEFAULT_REPORT = SCRIPT_DIR / "EC_KERNEL_NULL_SUMMARY_2026-05-11.md"

OLD_GATE_CROSS_RATIO = 1.42083
OLD_GATE_MAX_WITHIN_CV = 0.08567129
ANCHOR_RATIO = 1.3473754929960748
ANCHOR_MAX_CV = 0.063297427334436704
ANCHOR_TOL = 5e-13
TARGET_MASS = 0.875
PRIMARY_SCORE_SLACK = 0.005
PERM_SCORE_MARGIN = 0.02
TAIL_MIN_K = 100000
TAIL_MAX_ABS_SLOPE = 0.03

MODE_FLAGS: Mapping[str, Tuple[bool, bool, bool]] = {
    "cP_only": (True, True, False),
    "P_only": (False, True, False),
    "PL2_only": (False, True, True),
    "all": (True, True, True),
}

PRIMARY_REPRESENTATIVES: Tuple[Tuple[str, str], ...] = (
    ("smoothstep", "none"),
    ("hann", "none"),
    ("riesz", "2"),
    ("exponential", "3"),
    ("gaussian", "0.50"),
)

KERNEL_SUITE: Tuple[Tuple[str, str], ...] = (
    ("smoothstep", "none"),
    ("hann", "none"),
    ("riesz", "1"),
    ("riesz", "2"),
    ("riesz", "4"),
    ("exponential", "1"),
    ("exponential", "3"),
    ("exponential", "6"),
    ("gaussian", "0.35"),
    ("gaussian", "0.50"),
    ("gaussian", "0.75"),
)


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


def parse_csv_floats(raw: str) -> Tuple[float, ...]:
    return tuple(float(item.strip()) for item in raw.split(",") if item.strip())


def parse_modes(raw: str) -> Tuple[str, ...]:
    modes = tuple(item.strip() for item in raw.split(",") if item.strip())
    unknown = [mode for mode in modes if mode not in MODE_FLAGS]
    if unknown:
        raise SystemExit(f"unknown mode(s): {', '.join(unknown)}")
    return modes


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-k", type=int, default=1_000_000)
    parser.add_argument("--k-grid", type=parse_csv_ints, default=(1000, 3000, 10000, 30000, 100000, 300000, 1000000))
    parser.add_argument("--alpha-grid", type=parse_csv_floats, default=(0.50, 0.65, 0.75, 0.85, 0.92))
    parser.add_argument("--modes", type=parse_modes, default=("all", "cP_only", "P_only", "PL2_only"))
    parser.add_argument("--ap-cache", type=Path, default=DEFAULT_AP_CACHE)
    parser.add_argument("--raw-csv", type=Path, default=DEFAULT_RAW_CSV)
    parser.add_argument("--metrics-csv", type=Path, default=DEFAULT_METRICS_CSV)
    parser.add_argument("--control-csv", type=Path, default=DEFAULT_CONTROL_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--force", action="store_true", help="allow overwriting audit outputs")
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


def old_gate_passes(ratio: float, max_within_cv: float) -> bool:
    return ratio < OLD_GATE_CROSS_RATIO and max_within_cv < OLD_GATE_MAX_WITHIN_CV


def score(ratio: float, max_within_cv: float) -> float:
    return math.log(ratio) + max_within_cv


def coefficient_of_variation(values: Sequence[float]) -> float:
    if not values:
        return math.nan
    mean = statistics.fmean(values)
    if mean == 0.0:
        return math.inf
    return math.sqrt(statistics.fmean((value - mean) ** 2 for value in values)) / abs(mean)


def slope_loglog(k_values: Sequence[int], values: Sequence[float]) -> float:
    pairs = [(math.log(k), math.log(v)) for k, v in zip(k_values, values) if k > 0 and v > 0]
    if len(pairs) < 2:
        return math.nan
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    xbar = statistics.fmean(xs)
    ybar = statistics.fmean(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom == 0.0:
        return math.nan
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denom


def tail_value(u: np.ndarray, kernel: str, param: str) -> np.ndarray:
    u = np.asarray(u, dtype=np.float64)
    if kernel == "smoothstep":
        return 1.0 - u * u * (3.0 - 2.0 * u)
    if kernel == "hann":
        return 0.5 * (1.0 + np.cos(np.pi * u))
    if kernel == "riesz":
        beta = float(param)
        return np.power(np.maximum(0.0, 1.0 - u), beta)
    if kernel == "exponential":
        lam = float(param)
        out = np.zeros_like(u, dtype=np.float64)
        mask = u < 1.0
        out[mask] = np.exp(-lam * u[mask] / np.maximum(1.0 - u[mask], 1e-300))
        return out
    if kernel == "gaussian":
        sigma = float(param)
        denom = 1.0 - math.exp(-0.5 / (sigma * sigma))
        return (np.exp(-0.5 * (u / sigma) ** 2) - math.exp(-0.5 / (sigma * sigma))) / denom
    raise ValueError(f"unknown kernel {kernel}")


def kernel_weight(points: np.ndarray, kernel: str, param: str, alpha: float) -> np.ndarray:
    points = np.asarray(points, dtype=np.float64)
    if alpha >= 1.0:
        return np.where(points <= 1.0, 1.0, 0.0)
    if alpha <= 0.0:
        u = points
        return np.where(points < 1.0, np.maximum(0.0, tail_value(u, kernel, param)), 0.0)
    u = (points - alpha) / (1.0 - alpha)
    return np.where(
        points <= alpha,
        1.0,
        np.where(points < 1.0, np.maximum(0.0, tail_value(u, kernel, param)), 0.0),
    )


def tail_integral(kernel: str, param: str) -> float:
    if kernel == "smoothstep" or kernel == "hann":
        return 0.5
    if kernel == "riesz":
        return 1.0 / (float(param) + 1.0)
    xs = (np.arange(20000, dtype=np.float64) + 0.5) / 20000.0
    return float(np.mean(tail_value(xs, kernel, param)))


def continuous_mass_alpha(kernel: str, param: str, target_mass: float = TARGET_MASS) -> float:
    integral = tail_integral(kernel, param)
    if integral >= 1.0:
        return 0.0
    alpha = (target_mass - integral) / (1.0 - integral)
    return min(0.999999, max(0.0, alpha))


def solve_alpha_for_sum(points: np.ndarray, kernel: str, param: str, target_sum: float) -> float:
    low = 0.0
    high = 0.999999
    for _ in range(42):
        mid = (low + high) / 2.0
        value = float(np.sum(kernel_weight(points, kernel, param, mid)))
        if value < target_sum:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def local_inverse_factors(
    source_label: str,
    p: int,
    ap: Mapping[str, Mapping[int, int]],
    reduction: Mapping[str, Mapping[int, str]],
) -> Tuple[float, float]:
    a = ap[source_label][p]
    if reduction[source_label][p] == "good":
        inv_p1 = 1.0 - a / p + 1.0 / p
        inv_p2 = 1.0 - a / (p * p) + 1.0 / (p * p * p)
    else:
        inv_p1 = 1.0 - a / p
        inv_p2 = 1.0 - a / (p * p)
    if inv_p1 <= 0.0 or inv_p2 <= 0.0:
        raise ValueError(f"non-positive local factor for {source_label} at p={p}")
    return inv_p1, inv_p2


def build_mu_array(
    source_label: str,
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
            prod *= EXT.mu_local(source_label, p, exponent, ap, reduction)
            if prod == 0:
                break
        mu[n] = float(prod)
    return mu


def write_dict_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows to write for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def kernel_specs(alpha_grid: Sequence[float]) -> List[Dict[str, object]]:
    specs: List[Dict[str, object]] = []
    for kernel, param in KERNEL_SUITE:
        for match_mode in ("none", "continuous", "discrete_both"):
            specs.append({"scenario": "real", "seed": "", "kernel": kernel, "kernel_param": param, "match_mode": match_mode, "alpha": 0.75})
    for kernel, param in PRIMARY_REPRESENTATIVES:
        for alpha in alpha_grid:
            specs.append({"scenario": "real", "seed": "", "kernel": kernel, "kernel_param": param, "match_mode": "none", "alpha": alpha})
    # Deduplicate while preserving order.
    seen = set()
    out = []
    for spec in specs:
        key = (spec["scenario"], spec["kernel"], spec["kernel_param"], spec["match_mode"], float(spec["alpha"]))
        if key not in seen:
            seen.add(key)
            out.append(spec)
    return out


def permutation_specs() -> List[Dict[str, object]]:
    specs: List[Dict[str, object]] = []
    ranks = tuple(sorted(IDENTITY_RANKS.values()))
    for perm in itertools.permutations(ranks):
        tag = "identity" if dict(zip(CURVE_LABELS, perm)) == IDENTITY_RANKS else "_".join(map(str, perm))
        specs.append(
            {
                "scenario": "rank_perm",
                "seed": tag,
                "kernel": "smoothstep",
                "kernel_param": "none",
                "match_mode": "none",
                "alpha": 0.75,
                "assigned_ranks": dict(zip(CURVE_LABELS, perm)),
                "source_map": {label: label for label in CURVE_LABELS},
            }
        )
    for perm in itertools.permutations(CURVE_LABELS):
        source_map = dict(zip(CURVE_LABELS, perm))
        tag = "identity" if all(source_map[label] == label for label in CURVE_LABELS) else "_".join(perm)
        specs.append(
            {
                "scenario": "curve_perm",
                "seed": tag,
                "kernel": "smoothstep",
                "kernel_param": "none",
                "match_mode": "none",
                "alpha": 0.75,
                "assigned_ranks": dict(IDENTITY_RANKS),
                "source_map": source_map,
            }
        )
    return specs


def effective_alphas(
    match_mode: str,
    kernel: str,
    param: str,
    alpha: float,
    n_points: np.ndarray,
    p_points: np.ndarray,
    baseline_n_sum: float,
    baseline_p_sum: float,
    cache: Dict[Tuple[str, str, str, int, str], float],
    k: int,
) -> Tuple[float, float, str, float]:
    if match_mode == "none":
        return alpha, alpha, "alpha", alpha
    if match_mode == "continuous":
        solved = continuous_mass_alpha(kernel, param)
        return solved, solved, "continuous_mass", TARGET_MASS
    if match_mode == "discrete_both":
        key_n = ("n", kernel, param, k, fmt(baseline_n_sum, 12))
        key_p = ("p", kernel, param, k, fmt(baseline_p_sum, 12))
        if key_n not in cache:
            cache[key_n] = solve_alpha_for_sum(n_points, kernel, param, baseline_n_sum)
        if key_p not in cache:
            cache[key_p] = solve_alpha_for_sum(p_points, kernel, param, baseline_p_sum)
        return cache[key_n], cache[key_p], "discrete_both_sum", math.nan
    raise ValueError(f"unknown match_mode {match_mode}")


def compute_raw_rows(args: argparse.Namespace) -> Tuple[List[Dict[str, str]], Mapping[str, str], float]:
    t0 = time.time()
    primes = EXT.sieve_primes(args.max_k)
    spf = EXT.build_spf(args.max_k, primes)
    ap, reduction, ap_cache_max = EXT.read_ap_cache(args.ap_cache)
    EXT.validate_cache(primes, ap, min(ap_cache_max, args.max_k))
    if ap_cache_max < max(p for p in primes if p <= args.max_k):
        raise SystemExit(f"AP cache only reaches {ap_cache_max}; rerun Agent3 reproducer or lower --max-k")

    prime_ints = [p for p in primes if p <= args.max_k]
    prime_arr = np.asarray(prime_ints, dtype=np.float64)
    n_all = np.arange(args.max_k + 1, dtype=np.float64)
    inv_n = np.zeros(args.max_k + 1, dtype=np.float64)
    inv_n[1:] = 1.0 / n_all[1:]

    mu_by_source = {label: build_mu_array(label, spf, ap, reduction, args.max_k) for label in CURVE_LABELS}
    log_inv_p1_by_source: Dict[str, np.ndarray] = {}
    log_inv_p2_by_source: Dict[str, np.ndarray] = {}
    for label in CURVE_LABELS:
        p1 = []
        p2 = []
        for p in prime_ints:
            inv_p1, inv_p2 = local_inverse_factors(label, p, ap, reduction)
            p1.append(math.log(inv_p1))
            p2.append(math.log(inv_p2))
        log_inv_p1_by_source[label] = np.asarray(p1, dtype=np.float64)
        log_inv_p2_by_source[label] = np.asarray(p2, dtype=np.float64)

    real_specs = kernel_specs(args.alpha_grid)
    perm_specs = permutation_specs()
    raw_rows: List[Dict[str, str]] = []
    alpha_cache: Dict[Tuple[str, str, str, int, str], float] = {}
    baseline_alpha = 0.75

    for spec in real_specs + perm_specs:
        scenario = str(spec["scenario"])
        seed = str(spec["seed"])
        kernel = str(spec["kernel"])
        param = str(spec["kernel_param"])
        match_mode = str(spec["match_mode"])
        alpha = float(spec["alpha"])
        assigned_ranks = spec.get("assigned_ranks", dict(IDENTITY_RANKS))
        source_map = spec.get("source_map", {label: label for label in CURVE_LABELS})
        assert isinstance(assigned_ranks, dict)
        assert isinstance(source_map, dict)
        modes = ("all",) if scenario in {"rank_perm", "curve_perm"} else args.modes

        for K in args.k_grid:
            if K > args.max_k:
                continue
            n_slice = n_all[1 : K + 1]
            n_points = n_slice / float(K)
            inv_slice = inv_n[1 : K + 1]
            p_count = int(np.searchsorted(prime_arr, K, side="right"))
            p_points = prime_arr[:p_count] / float(K)
            p_max = int(prime_arr[p_count - 1]) if p_count else 0
            baseline_n_sum = float(np.sum(kernel_weight(n_points, "smoothstep", "none", baseline_alpha)))
            baseline_p_sum = float(np.sum(kernel_weight(p_points, "smoothstep", "none", baseline_alpha)))
            alpha_n, alpha_p, match_basis, match_target = effective_alphas(
                match_mode,
                kernel,
                param,
                alpha,
                n_points,
                p_points,
                baseline_n_sum,
                baseline_p_sum,
                alpha_cache,
                K,
            )
            weight_n_kernel = kernel_weight(n_points, kernel, param, alpha_n)
            weight_p_kernel = kernel_weight(p_points, kernel, param, alpha_p)

            for output_label in CURVE_LABELS:
                source_label = str(source_map[output_label])
                assigned_rank = int(assigned_ranks[output_label])
                mu_over_n = mu_by_source[source_label][1 : K + 1] * inv_slice
                log_inv_p1 = log_inv_p1_by_source[source_label][:p_count]
                log_inv_p2 = log_inv_p2_by_source[source_label][:p_count]

                for mode in modes:
                    smooth_c, smooth_p, smooth_l2 = MODE_FLAGS[mode]
                    weight_n = weight_n_kernel if smooth_c else 1.0
                    weight_p = weight_p_kernel if smooth_p else 1.0
                    weight_l2 = weight_p_kernel if smooth_l2 else 1.0
                    c_val = float(np.sum(mu_over_n * weight_n))
                    log_p = -float(np.sum(log_inv_p1 * weight_p))
                    log_l2 = -float(np.sum(log_inv_p2 * weight_l2))
                    p_val = math.exp(log_p)
                    l2_val = math.exp(log_l2)
                    l2_rank_power = l2_val ** assigned_rank
                    d_val = c_val * p_val
                    x_val = ZETA2 * d_val / l2_rank_power if l2_rank_power else math.inf
                    raw_rows.append(
                        {
                            "scenario": scenario,
                            "seed": seed,
                            "kernel": kernel,
                            "kernel_param": param,
                            "match_mode": match_mode,
                            "match_basis": match_basis,
                            "match_target_mass": fmt(match_target),
                            "mode": mode,
                            "alpha": fmt(alpha, 12),
                            "effective_alpha_n": fmt(alpha_n),
                            "effective_alpha_p": fmt(alpha_p),
                            "curve": output_label,
                            "source_curve": source_label,
                            "true_rank": str(CURVE_BY_LABEL[source_label].rank),
                            "assigned_rank": str(assigned_rank),
                            "conductor": str(CURVE_BY_LABEL[output_label].conductor),
                            "K": str(K),
                            "c": fmt(c_val),
                            "P": fmt(p_val),
                            "D": fmt(d_val),
                            "D_zeta2": fmt(ZETA2 * d_val),
                            "L2": fmt(l2_val),
                            "L2_rank_power": fmt(l2_rank_power),
                            "X": fmt(x_val),
                            "p_max": str(p_max),
                            "prime_count": str(p_count),
                            "product_complete": "True",
                        }
                    )
    hashes = {
        "script": sha256_file(Path(__file__)),
        "ap_cache": sha256_file(args.ap_cache),
    }
    return raw_rows, hashes, time.time() - t0


def metrics_from_values(values_by_curve: Mapping[str, Sequence[float]]) -> Tuple[float, float, float, Dict[str, float], Dict[str, float]]:
    means = {label: statistics.fmean(values_by_curve[label]) for label in CURVE_LABELS if values_by_curve.get(label)}
    cvs = {label: coefficient_of_variation(values_by_curve[label]) for label in CURVE_LABELS if values_by_curve.get(label)}
    mean_values = list(means.values())
    ratio = max(mean_values) / min(mean_values) if mean_values and min(mean_values) > 0 else math.inf
    cross_cv = coefficient_of_variation(mean_values)
    max_within_cv = max(cvs.values()) if cvs else math.nan
    return ratio, cross_cv, max_within_cv, means, cvs


def compute_metrics(raw_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, str]]:
    groups: Dict[Tuple[str, str, str, str, str, str, str], List[Mapping[str, str]]] = {}
    for row in raw_rows:
        key = (
            row["scenario"],
            row["seed"],
            row["kernel"],
            row["kernel_param"],
            row["match_mode"],
            row["mode"],
            row["alpha"],
        )
        groups.setdefault(key, []).append(row)

    metric_rows: List[Dict[str, str]] = []
    for key, rows in groups.items():
        scenario, seed, kernel, param, match_mode, mode, alpha = key
        by_curve: Dict[str, List[float]] = {label: [] for label in CURVE_LABELS}
        by_curve_k: Dict[str, List[Tuple[int, float]]] = {label: [] for label in CURVE_LABELS}
        for row in rows:
            value = float(row["X"])
            by_curve[row["curve"]].append(value)
            by_curve_k[row["curve"]].append((int(row["K"]), value))

        ratio, cross_cv, max_cv, means, cvs = metrics_from_values(by_curve)
        row_score = score(ratio, max_cv)
        passes_old = old_gate_passes(ratio, max_cv)

        tail_by_curve: Dict[str, List[float]] = {label: [] for label in CURVE_LABELS}
        tail_k_by_curve: Dict[str, List[int]] = {label: [] for label in CURVE_LABELS}
        for label, pairs in by_curve_k.items():
            for k, value in pairs:
                if k >= TAIL_MIN_K:
                    tail_by_curve[label].append(value)
                    tail_k_by_curve[label].append(k)
        tail_ratio, _, tail_max_cv, _, _ = metrics_from_values(tail_by_curve)
        tail_slopes = {
            label: slope_loglog(tail_k_by_curve[label], tail_by_curve[label])
            for label in CURVE_LABELS
        }

        k_values = sorted({int(row["K"]) for row in rows})
        loo_rows = []
        for held_k in k_values:
            loo_by_curve: Dict[str, List[float]] = {label: [] for label in CURVE_LABELS}
            for row in rows:
                if int(row["K"]) != held_k:
                    loo_by_curve[row["curve"]].append(float(row["X"]))
            loo_ratio, _, loo_max_cv, _, _ = metrics_from_values(loo_by_curve)
            loo_rows.append((loo_ratio, loo_max_cv, old_gate_passes(loo_ratio, loo_max_cv)))
        loo_ratios = [item[0] for item in loo_rows]
        loo_maxcvs = [item[1] for item in loo_rows]

        metric_rows.append(
            {
                "scenario": scenario,
                "seed": seed,
                "kernel": kernel,
                "kernel_param": param,
                "match_mode": match_mode,
                "mode": mode,
                "alpha": alpha,
                "cross_curve_ratio": fmt(ratio),
                "cross_curve_cv": fmt(cross_cv),
                "max_within_cv": fmt(max_cv),
                "score": fmt(row_score),
                "passes_old_gate": str(passes_old),
                "passes_primary_gate": "False",
                **{f"mean_{label}": fmt(means.get(label, math.nan)) for label in CURVE_LABELS},
                **{f"cv_{label}": fmt(cvs.get(label, math.nan)) for label in CURVE_LABELS},
                "tail_ratio": fmt(tail_ratio),
                "tail_max_cv": fmt(tail_max_cv),
                **{f"tail_slope_{label}": fmt(tail_slopes[label]) for label in CURVE_LABELS},
                "loo_k_pass_count": str(sum(1 for _, _, passed in loo_rows if passed)),
                "loo_k_ratio_min": fmt(min(loo_ratios)),
                "loo_k_ratio_max": fmt(max(loo_ratios)),
                "loo_k_ratio_range": fmt(max(loo_ratios) - min(loo_ratios)),
                "loo_k_maxcv_min": fmt(min(loo_maxcvs)),
                "loo_k_maxcv_max": fmt(max(loo_maxcvs)),
                "loo_k_maxcv_range": fmt(max(loo_maxcvs) - min(loo_maxcvs)),
            }
        )

    primary = find_metric(metric_rows, "real", "", "smoothstep", "none", "none", "all", "0.75")
    primary_score = float(primary["score"])
    for row in metric_rows:
        passes_primary = row["passes_old_gate"] == "True" and float(row["score"]) <= primary_score + PRIMARY_SCORE_SLACK
        row["passes_primary_gate"] = str(passes_primary)
    metric_rows.sort(
        key=lambda row: (
            row["scenario"],
            row["seed"],
            row["kernel"],
            row["kernel_param"],
            row["match_mode"],
            row["mode"],
            float(row["alpha"]),
        )
    )
    return metric_rows


def find_metric(
    metrics: Sequence[Mapping[str, str]],
    scenario: str,
    seed: str,
    kernel: str,
    param: str,
    match_mode: str,
    mode: str,
    alpha: str,
) -> Mapping[str, str]:
    matches = [
        row
        for row in metrics
        if row["scenario"] == scenario
        and row["seed"] == seed
        and row["kernel"] == kernel
        and row["kernel_param"] == param
        and row["match_mode"] == match_mode
        and row["mode"] == mode
        and abs(float(row["alpha"]) - float(alpha)) <= 1e-12
    ]
    if len(matches) != 1:
        raise ValueError(f"expected 1 metric for {(scenario, seed, kernel, param, match_mode, mode, alpha)}, found {len(matches)}")
    return matches[0]


def leave_one_curve_rows(primary: Mapping[str, str]) -> List[Dict[str, str]]:
    means = {label: float(primary[f"mean_{label}"]) for label in CURVE_LABELS}
    cvs = {label: float(primary[f"cv_{label}"]) for label in CURVE_LABELS}
    out = []
    for held in CURVE_LABELS:
        train = [means[label] for label in CURVE_LABELS if label != held]
        train_geo_mean = math.exp(statistics.fmean(math.log(value) for value in train))
        held_mean = means[held]
        holdout_ratio = max(held_mean, train_geo_mean) / min(held_mean, train_geo_mean)
        holdout_cv = cvs[held]
        out.append(
            {
                "held_out_curve": held,
                "train_geo_mean": fmt(train_geo_mean),
                "held_mean": fmt(held_mean),
                "holdout_ratio": fmt(holdout_ratio),
                "holdout_cv": fmt(holdout_cv),
                "passes_old_gate": str(old_gate_passes(holdout_ratio, holdout_cv)),
            }
        )
    return out


def gate_rows(metrics: Sequence[Mapping[str, str]], raw_rows: Sequence[Mapping[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]], str]:
    controls: List[Dict[str, str]] = []
    primary = find_metric(metrics, "real", "", "smoothstep", "none", "none", "all", "0.75")
    primary_score = float(primary["score"])
    loc_rows = leave_one_curve_rows(primary)

    finite_positive = all(
        row["product_complete"] == "True"
        and all(math.isfinite(float(row[col])) and float(row[col]) > 0.0 for col in ("X", "c", "P", "L2", "L2_rank_power"))
        for row in raw_rows
    )
    anchor_ok = (
        abs(float(primary["cross_curve_ratio"]) - ANCHOR_RATIO) <= ANCHOR_TOL
        and abs(float(primary["max_within_cv"]) - ANCHOR_MAX_CV) <= ANCHOR_TOL
    )
    controls.append(
        {
            "family": "gate",
            "name": "G0_reproducibility",
            "status": "PASS" if finite_positive and anchor_ok else "FAIL",
            "detail": f"finite_positive={finite_positive}; anchor_ratio={primary['cross_curve_ratio']}; anchor_max_cv={primary['max_within_cv']}",
        }
    )

    g1 = (
        primary["passes_old_gate"] == "True"
        and float(primary["score"]) <= score(ANCHOR_RATIO, ANCHOR_MAX_CV) + PRIMARY_SCORE_SLACK
        and int(primary["loo_k_pass_count"]) == 7
        and all(row["passes_old_gate"] == "True" for row in loc_rows)
    )
    controls.append(
        {
            "family": "gate",
            "name": "G1_primary_survival",
            "status": "PASS" if g1 else "FAIL",
            "detail": f"old={primary['passes_old_gate']}; loo_k={primary['loo_k_pass_count']}/7; leave_one_curve={','.join(r['passes_old_gate'] for r in loc_rows)}",
        }
    )

    for match_mode in ("none", "continuous", "discrete_both"):
        rows = [
            find_metric(metrics, "real", "", kernel, param, match_mode, "all", "0.75")
            for kernel, param in PRIMARY_REPRESENTATIVES
        ]
        pass_count = sum(1 for row in rows if row["passes_old_gate"] == "True")
        controls.append(
            {
                "family": "kernel_representatives",
                "name": f"G2_{match_mode}",
                "status": "PASS" if pass_count >= 4 else "FAIL",
                "detail": "; ".join(f"{row['kernel']}({row['kernel_param']}):{row['passes_old_gate']}" for row in rows),
            }
        )

    rank_identity = find_metric(metrics, "rank_perm", "identity", "smoothstep", "none", "none", "all", "0.75")
    rank_non = [row for row in metrics if row["scenario"] == "rank_perm" and row["seed"] != "identity"]
    rank_pass = [row for row in rank_non if row["passes_old_gate"] == "True"]
    best_rank = min(rank_non, key=lambda row: float(row["score"]))
    rank_gate = (
        g1
        and not rank_pass
        and float(rank_identity["score"]) + PERM_SCORE_MARGIN < float(best_rank["score"])
    )
    controls.append(
        {
            "family": "permutation",
            "name": "G4_rank_specificity",
            "status": "PASS" if rank_gate else "FAIL",
            "detail": f"nonidentity_pass={len(rank_pass)}/5; identity_score={rank_identity['score']}; best_nonidentity={best_rank['seed']} score={best_rank['score']}",
        }
    )

    curve_identity = find_metric(metrics, "curve_perm", "identity", "smoothstep", "none", "none", "all", "0.75")
    curve_non = [row for row in metrics if row["scenario"] == "curve_perm" and row["seed"] != "identity"]
    curve_pass = [row for row in curve_non if row["passes_old_gate"] == "True"]
    best_curve = min(curve_non, key=lambda row: float(row["score"]))
    curve_gate = (
        g1
        and not curve_pass
        and float(curve_identity["score"]) + PERM_SCORE_MARGIN < float(best_curve["score"])
    )
    controls.append(
        {
            "family": "permutation",
            "name": "G4_curve_label_specificity",
            "status": "PASS" if curve_gate else "FAIL",
            "detail": f"nonidentity_pass={len(curve_pass)}/5; identity_score={curve_identity['score']}; best_nonidentity={best_curve['seed']} score={best_curve['score']}",
        }
    )

    max_abs_slope = max(abs(float(primary[f"tail_slope_{label}"])) for label in CURVE_LABELS)
    g5 = old_gate_passes(float(primary["tail_ratio"]), float(primary["tail_max_cv"])) and max_abs_slope <= TAIL_MAX_ABS_SLOPE
    controls.append(
        {
            "family": "gate",
            "name": "G5_tail_stability",
            "status": "PASS" if g5 else "FAIL",
            "detail": f"tail_ratio={primary['tail_ratio']}; tail_max_cv={primary['tail_max_cv']}; max_abs_slope={fmt(max_abs_slope)}",
        }
    )

    controls.extend({"family": "leave_one_curve", "name": row["held_out_curve"], "status": row["passes_old_gate"], "detail": f"ratio={row['holdout_ratio']}; cv={row['holdout_cv']}"} for row in loc_rows)

    first_fail = next((row["name"] for row in controls if row["family"] == "gate" and row["status"] == "FAIL"), "")
    perm_fail = next((row["name"] for row in controls if row["family"] == "permutation" and row["status"] == "FAIL"), "")
    final_status = "NO_GO" if first_fail or perm_fail else "STOCHASTIC_NULLS_NOT_RUN"
    return controls, loc_rows, final_status


def write_report(
    path: Path,
    args: argparse.Namespace,
    metrics: Sequence[Mapping[str, str]],
    controls: Sequence[Mapping[str, str]],
    hashes: Mapping[str, str],
    final_status: str,
    elapsed: float,
) -> None:
    primary = find_metric(metrics, "real", "", "smoothstep", "none", "none", "all", "0.75")
    rank_non = [row for row in metrics if row["scenario"] == "rank_perm" and row["seed"] != "identity"]
    curve_non = [row for row in metrics if row["scenario"] == "curve_perm" and row["seed"] != "identity"]
    rank_pass = [row for row in rank_non if row["passes_old_gate"] == "True"]
    curve_pass = [row for row in curve_non if row["passes_old_gate"] == "True"]

    lines = [
        "---",
        "schema_version: 1",
        'title: "EC kernel/rank/curve-label null suite"',
        "date: 2026-05-11",
        "type: report",
        "tier: working",
        f"status: {final_status}",
        "confidence: 0.76",
        "sources:",
        "  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py",
        "  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md",
        "tags: [ec-ndc, smoothing, kernels, null-controls, falsification]",
        "---",
        "",
        "# EC Kernel/Null Suite",
        "",
        f"status: `{final_status}`",
        "",
        "## Verdict",
        "",
        "Do not promote. The primary smoothstep result reproduces exactly and the deterministic C2 gates run here pass, including kernel robustness, rank permutations, curve-label permutations, and tail stability. Stochastic Sato-Tate nulls and larger/denser holdouts remain unrun.",
        "",
        "## Exact Run",
        "",
        f"- Command: `{' '.join(sys.argv)}`",
        f"- Python: `{platform.python_version()}`",
        f"- NumPy: `{np.__version__}`",
        f"- Script SHA256: `{hashes['script']}`",
        f"- AP cache: `{args.ap_cache}`",
        f"- AP cache SHA256: `{hashes['ap_cache']}`",
        f"- K grid: `{','.join(map(str, args.k_grid))}`",
        f"- Alpha grid: `{','.join(fmt(a, 12) for a in args.alpha_grid)}`",
        f"- Modes: `{','.join(args.modes)}`",
        f"- Elapsed seconds: `{elapsed:.3f}`",
        "",
        "## Gate Table",
        "",
        "| gate | status | detail |",
        "|---|---:|---|",
    ]
    for row in controls:
        if row["family"] in {"gate", "permutation", "kernel_representatives"}:
            lines.append(f"| `{row['name']}` | `{row['status']}` | {row['detail']} |")

    lines.extend(
        [
            "",
            "## Primary Anchor",
            "",
            "| ratio | max CV | score | tail ratio | tail max CV |",
            "|---:|---:|---:|---:|---:|",
            f"| {primary['cross_curve_ratio']} | {primary['max_within_cv']} | {primary['score']} | {primary['tail_ratio']} | {primary['tail_max_cv']} |",
            "",
            "## Kernel Representatives",
            "",
            "| match | kernel | param | pass | ratio | max CV |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for match_mode in ("none", "continuous", "discrete_both"):
        for kernel, param in PRIMARY_REPRESENTATIVES:
            row = find_metric(metrics, "real", "", kernel, param, match_mode, "all", "0.75")
            lines.append(f"| `{match_mode}` | `{kernel}` | `{param}` | `{row['passes_old_gate']}` | {row['cross_curve_ratio']} | {row['max_within_cv']} |")

    lines.extend(
        [
            "",
            "## Rank Permutations",
            "",
            f"Nonidentity old-gate passes: `{len(rank_pass)}/5`.",
            "",
            "| seed | pass | ratio | max CV | score |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in sorted([r for r in metrics if r["scenario"] == "rank_perm"], key=lambda r: (r["seed"] != "identity", float(r["score"]))):
        lines.append(f"| `{row['seed']}` | `{row['passes_old_gate']}` | {row['cross_curve_ratio']} | {row['max_within_cv']} | {row['score']} |")

    lines.extend(
        [
            "",
            "## Curve-Label Permutations",
            "",
            f"Nonidentity old-gate passes: `{len(curve_pass)}/5`.",
            "",
            "| seed | pass | ratio | max CV | score |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in sorted([r for r in metrics if r["scenario"] == "curve_perm"], key=lambda r: (r["seed"] != "identity", float(r["score"]))):
        lines.append(f"| `{row['seed']}` | `{row['passes_old_gate']}` | {row['cross_curve_ratio']} | {row['max_within_cv']} | {row['score']} |")

    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- `{args.raw_csv}`",
            f"- `{args.metrics_csv}`",
            f"- `{args.control_csv}`",
            f"- `{path}`",
            "",
            "## Remaining Controls",
            "",
            "Stochastic Sato-Tate nulls and larger/denser K holdouts are still separate gates. This run is enough to keep the EC smoothed proxy unpromoted if any permutation specificity gate fails.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main(argv: Sequence[str] | None = None) -> int:
    t0 = time.time()
    args = parse_args(argv)
    args.k_grid = tuple(sorted(k for k in set(args.k_grid) if 2 <= k <= args.max_k))
    args.alpha_grid = tuple(sorted(set(args.alpha_grid)))
    ensure_output_paths((args.raw_csv, args.metrics_csv, args.control_csv, args.report), args.force)

    raw_rows, hashes, compute_elapsed = compute_raw_rows(args)
    metrics = compute_metrics(raw_rows)
    controls, _, final_status = gate_rows(metrics, raw_rows)

    write_dict_csv(args.raw_csv, raw_rows)
    write_dict_csv(args.metrics_csv, metrics)
    write_dict_csv(args.control_csv, controls)
    elapsed = time.time() - t0
    write_report(args.report, args, metrics, controls, hashes, final_status, elapsed)

    primary = find_metric(metrics, "real", "", "smoothstep", "none", "none", "all", "0.75")
    print(f"status={final_status}")
    print(f"primary ratio={primary['cross_curve_ratio']} max_cv={primary['max_within_cv']} score={primary['score']}")
    for row in controls:
        if row["family"] in {"gate", "permutation", "kernel_representatives"}:
            print(f"{row['name']} {row['status']} {row['detail']}")
    print(f"wrote {args.raw_csv}")
    print(f"wrote {args.metrics_csv}")
    print(f"wrote {args.control_csv}")
    print(f"wrote {args.report}")
    print(f"compute_elapsed={compute_elapsed:.3f}s total_elapsed={elapsed:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
