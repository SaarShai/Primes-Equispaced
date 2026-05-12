#!/usr/bin/env python3
"""S1-E numerical zero-frequency diagnostics from existing Agent 3 data.

This script does not recompute elliptic-curve coefficients. It only reads the
saved Agent 3 product CSV, the saved a_p cache, and the local PARI zero file.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


DEFAULT_ALPHA = "0.75"
DEFAULT_MODE = "all"
TWO_PI = 2.0 * math.pi


def default_paths() -> Tuple[Path, Path, Path, Path]:
    here = Path(__file__).resolve().parent
    root = here.parent
    wave = root / "handoff-2026-05-11-gpt55-wave"
    return (
        wave / "AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv",
        wave / "AGENT3_EC_AP_TABLE_1000000.csv",
        root / "koyama-shared" / "data" / "pari_authoritative_zeros.json",
        here,
    )


def parse_args() -> argparse.Namespace:
    raw_csv, ap_csv, zeros_json, out_dir = default_paths()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-csv", type=Path, default=raw_csv)
    parser.add_argument("--ap-csv", type=Path, default=ap_csv)
    parser.add_argument("--zeros-json", type=Path, default=zeros_json)
    parser.add_argument("--out-dir", type=Path, default=out_dir)
    parser.add_argument("--alpha", default=DEFAULT_ALPHA)
    parser.add_argument("--mode", default=DEFAULT_MODE)
    return parser.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(value: float, digits: int = 17) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf" if value > 0.0 else "-inf"
    return f"{value:.{digits}g}"


def smooth_weight(t: float, alpha: float) -> float:
    if alpha <= 0.0:
        return 1.0 - t * t * (3.0 - 2.0 * t) if t < 1.0 else 0.0
    if alpha >= 1.0:
        return 1.0 if t <= 1.0 else 0.0
    if t <= alpha:
        return 1.0
    if t >= 1.0:
        return 0.0
    u = (t - alpha) / (1.0 - alpha)
    return 1.0 - u * u * (3.0 - 2.0 * u)


def read_product_rows(path: Path, alpha: str, mode: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            if row["alpha"] != alpha or row["mode"] != mode:
                continue
            k = int(row["K"])
            rank = int(row["rank"])
            log_k = math.log(k)
            loglog_k = math.log(log_k)
            p_val = float(row["P"])
            rows.append(
                {
                    "curve": row["curve"],
                    "rank": rank,
                    "conductor": int(row["conductor"]),
                    "K": k,
                    "alpha": row["alpha"],
                    "mode": row["mode"],
                    "P": p_val,
                    "logK": log_k,
                    "loglogK": loglog_k,
                    "logP": math.log(p_val),
                    "product_residual": math.log(p_val) + rank * loglog_k,
                }
            )
    rows.sort(key=lambda r: (str(r["curve"]), int(r["K"])))
    return rows


def read_ap_cache(path: Path) -> Tuple[List[int], Dict[str, List[int]], Dict[str, List[str]]]:
    primes: List[int] = []
    ap: Dict[str, List[int]] = {}
    reduction: Dict[str, List[str]] = {}
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError(f"{path} has no header")
        curves = [
            name[len("a_p(") : -1]
            for name in reader.fieldnames
            if name.startswith("a_p(") and name.endswith(")")
        ]
        ap = {curve: [] for curve in curves}
        reduction = {curve: [] for curve in curves}
        for row in reader:
            primes.append(int(row["p"]))
            for curve in curves:
                ap[curve].append(int(row[f"a_p({curve})"]))
                reduction[curve].append(row[f"reduction({curve})"])
    return primes, ap, reduction


def reconstruct_s1(
    product_rows: Sequence[Mapping[str, object]],
    primes: Sequence[int],
    ap: Mapping[str, Sequence[int]],
    reduction: Mapping[str, Sequence[str]],
    alpha: float,
) -> Dict[Tuple[str, int], Dict[str, float]]:
    wanted = {(str(row["curve"]), int(row["K"])) for row in product_rows}
    out: Dict[Tuple[str, int], Dict[str, float]] = {}
    curves = sorted({curve for curve, _ in wanted})
    ks = sorted({k for _, k in wanted})
    for curve in curves:
        if curve not in ap:
            continue
        for k in ks:
            if (curve, k) not in wanted:
                continue
            s1_all = 0.0
            s1_good = 0.0
            harmonic_good = 0.0
            for p, a, red in zip(primes, ap[curve], reduction[curve]):
                if p > k:
                    break
                w = smooth_weight(p / float(k), alpha)
                if w == 0.0:
                    continue
                term = w * a / float(p)
                s1_all += term
                if red == "good":
                    s1_good += term
                    harmonic_good += w / float(p)
            out[(curve, k)] = {
                "s1_all": s1_all,
                "s1_good": s1_good,
                "harmonic_good": harmonic_good,
            }
    return out


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_series_rows(
    product_rows: Sequence[Mapping[str, object]],
    s1_by_curve_k: Mapping[Tuple[str, int], Mapping[str, float]],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in product_rows:
        curve = str(row["curve"])
        k = int(row["K"])
        rank = int(row["rank"])
        s1 = s1_by_curve_k[(curve, k)]
        trace_coeff = 0.5 - rank
        s1_all = float(s1["s1_all"])
        s1_good = float(s1["s1_good"])
        loglog_k = float(row["loglogK"])
        rows.append(
            {
                "curve": curve,
                "rank": rank,
                "conductor": int(row["conductor"]),
                "K": k,
                "alpha": row["alpha"],
                "mode": row["mode"],
                "logK": fmt(float(row["logK"])),
                "loglogK": fmt(loglog_k),
                "P": fmt(float(row["P"])),
                "logP": fmt(float(row["logP"])),
                "product_residual_logP_plus_rank_loglogK": fmt(
                    float(row["product_residual"])
                ),
                "s1_proxy_all_primes": fmt(s1_all),
                "s1_proxy_good_primes": fmt(s1_good),
                "s1_proxy_trace_coeff_0p5_minus_rank": fmt(trace_coeff),
                "s1_proxy_all_adjusted": fmt(s1_all - trace_coeff * loglog_k),
                "s1_proxy_good_adjusted": fmt(s1_good - trace_coeff * loglog_k),
                "harmonic_good": fmt(float(s1["harmonic_good"])),
                "harmonic_good_minus_loglogK": fmt(
                    float(s1["harmonic_good"]) - loglog_k
                ),
            }
        )
    rows.sort(key=lambda r: (str(r["curve"]), int(r["K"])))
    return rows


def read_zeros(path: Path) -> Dict[str, List[float]]:
    with path.open() as fh:
        raw = json.load(fh)
    out: Dict[str, List[float]] = {}
    for curve, payload in raw.items():
        if not isinstance(payload, dict):
            continue
        values = payload.get("complex_zeros_imag") or payload.get("zeros_imag")
        if values:
            out[curve] = [float(x) for x in values]
    return out


def solve_normal_equations(features: Sequence[Sequence[float]], y: Sequence[float]) -> List[float]:
    n = len(y)
    p = len(features[0])
    ata = [[0.0 for _ in range(p)] for _ in range(p)]
    aty = [0.0 for _ in range(p)]
    for row, yi in zip(features, y):
        for i in range(p):
            aty[i] += row[i] * yi
            for j in range(p):
                ata[i][j] += row[i] * row[j]
    aug = [ata[i] + [aty[i]] for i in range(p)]
    for col in range(p):
        pivot = max(range(col, p), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1.0e-12:
            raise ValueError("singular least-squares normal equations")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        for j in range(col, p + 1):
            aug[col][j] /= scale
        for r in range(p):
            if r == col:
                continue
            factor = aug[r][col]
            if factor == 0.0:
                continue
            for j in range(col, p + 1):
                aug[r][j] -= factor * aug[col][j]
    return [aug[i][p] for i in range(p)]


def fit_features(features: Sequence[Sequence[float]], y: Sequence[float]) -> Dict[str, object]:
    beta = solve_normal_equations(features, y)
    fitted = [sum(b * x for b, x in zip(beta, row)) for row in features]
    residuals = [yi - fi for yi, fi in zip(y, fitted)]
    rss = sum(r * r for r in residuals)
    n = len(y)
    p = len(beta)
    return {
        "beta": beta,
        "fitted": fitted,
        "rss": rss,
        "rmse": math.sqrt(rss / n),
        "p": p,
    }


def loo_rmse_for_gamma(u: Sequence[float], y: Sequence[float], gamma: float) -> float:
    errs = []
    n = len(y)
    for held in range(n):
        train_u = [ui for i, ui in enumerate(u) if i != held]
        train_y = [yi for i, yi in enumerate(y) if i != held]
        features = [[1.0, math.cos(gamma * ui), math.sin(gamma * ui)] for ui in train_u]
        beta = solve_normal_equations(features, train_y)
        held_features = [1.0, math.cos(gamma * u[held]), math.sin(gamma * u[held])]
        pred = sum(b * x for b, x in zip(beta, held_features))
        errs.append(y[held] - pred)
    return math.sqrt(sum(e * e for e in errs) / n)


def loo_rmse_constant(y: Sequence[float]) -> float:
    errs = []
    n = len(y)
    for held in range(n):
        train = [yi for i, yi in enumerate(y) if i != held]
        pred = sum(train) / len(train)
        errs.append(y[held] - pred)
    return math.sqrt(sum(e * e for e in errs) / n)


def fit_zero_frequencies(
    series_rows: Sequence[Mapping[str, object]],
    zeros: Mapping[str, Sequence[float]],
    alpha: str,
    mode: str,
) -> List[Dict[str, object]]:
    by_curve: Dict[str, List[Mapping[str, object]]] = {}
    for row in series_rows:
        by_curve.setdefault(str(row["curve"]), []).append(row)

    targets = [
        (
            "product_residual_logP_plus_rank_loglogK",
            "product_residual_logP_plus_rank_loglogK",
        ),
        (
            "s1_proxy_all_adjusted",
            "s1_proxy_all_adjusted",
        ),
    ]
    out: List[Dict[str, object]] = []
    for curve, rows in sorted(by_curve.items()):
        if curve not in zeros:
            continue
        rows = sorted(rows, key=lambda r: int(r["K"]))
        u = [float(r["logK"]) for r in rows]
        rank = int(rows[0]["rank"])
        conductor = int(rows[0]["conductor"])
        for series_name, column in targets:
            y = [float(r[column]) for r in rows]
            n = len(y)
            mean_y = sum(y) / n
            rss0 = sum((yi - mean_y) ** 2 for yi in y)
            const_loo = loo_rmse_constant(y)
            y_range = max(y) - min(y)
            for zero_index, gamma in enumerate(zeros[curve], start=1):
                features = [[1.0, math.cos(gamma * ui), math.sin(gamma * ui)] for ui in u]
                fit = fit_features(features, y)
                rss1 = float(fit["rss"])
                p = int(fit["p"])
                beta = list(fit["beta"])
                r2 = 1.0 - rss1 / rss0 if rss0 > 0.0 else math.nan
                adj_r2 = (
                    1.0 - (rss1 / (n - p)) / (rss0 / (n - 1))
                    if rss0 > 0.0 and n > p
                    else math.nan
                )
                loo = loo_rmse_for_gamma(u, y, gamma)
                loo_skill = (
                    1.0 - (loo * loo) / (const_loo * const_loo)
                    if const_loo > 0.0
                    else math.nan
                )
                phase_steps = [
                    ((gamma * (u[i + 1] - u[i]) + math.pi) % TWO_PI) - math.pi
                    for i in range(len(u) - 1)
                ]
                out.append(
                    {
                        "curve": curve,
                        "rank": rank,
                        "conductor": conductor,
                        "series": series_name,
                        "alpha": alpha,
                        "mode": mode,
                        "n": n,
                        "zero_index": zero_index,
                        "gamma": fmt(gamma),
                        "cycles_over_logK_range": fmt(gamma * (max(u) - min(u)) / TWO_PI),
                        "median_abs_phase_step_rad": fmt(
                            sorted(abs(x) for x in phase_steps)[len(phase_steps) // 2]
                        ),
                        "intercept": fmt(beta[0]),
                        "cos_coef": fmt(beta[1]),
                        "sin_coef": fmt(beta[2]),
                        "amplitude": fmt(math.hypot(beta[1], beta[2])),
                        "phase_rad_for_amp_cos_gamma_u_minus_phase": fmt(
                            math.atan2(beta[2], beta[1])
                        ),
                        "rss_constant": fmt(rss0),
                        "rss_zero_model": fmt(rss1),
                        "rmse_zero_model": fmt(float(fit["rmse"])),
                        "r2_vs_constant": fmt(r2),
                        "adjusted_r2_vs_constant": fmt(adj_r2),
                        "const_loo_rmse": fmt(const_loo),
                        "zero_model_loo_rmse": fmt(loo),
                        "loo_skill_vs_constant": fmt(loo_skill),
                        "series_range": fmt(y_range),
                    }
                )
    out.sort(
        key=lambda r: (
            str(r["curve"]),
            str(r["series"]),
            int(r["zero_index"]),
        )
    )
    return out


def summarize_by_best_fit(fit_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    groups: Dict[Tuple[str, str], List[Mapping[str, object]]] = {}
    for row in fit_rows:
        groups.setdefault((str(row["curve"]), str(row["series"])), []).append(row)
    out: List[Dict[str, object]] = []
    for (curve, series), rows in sorted(groups.items()):
        best_r2 = max(rows, key=lambda r: float(r["r2_vs_constant"]))
        best_loo = max(rows, key=lambda r: float(r["loo_skill_vs_constant"]))
        first = min(rows, key=lambda r: int(r["zero_index"]))
        out.append(
            {
                "curve": curve,
                "rank": first["rank"],
                "series": series,
                "n": first["n"],
                "first_zero_gamma": first["gamma"],
                "first_zero_r2": first["r2_vs_constant"],
                "first_zero_adjusted_r2": first["adjusted_r2_vs_constant"],
                "first_zero_loo_skill": first["loo_skill_vs_constant"],
                "best_in_sample_zero_index": best_r2["zero_index"],
                "best_in_sample_gamma": best_r2["gamma"],
                "best_in_sample_r2": best_r2["r2_vs_constant"],
                "best_in_sample_adjusted_r2": best_r2["adjusted_r2_vs_constant"],
                "best_in_sample_loo_skill": best_r2["loo_skill_vs_constant"],
                "best_loo_zero_index": best_loo["zero_index"],
                "best_loo_gamma": best_loo["gamma"],
                "best_loo_r2": best_loo["r2_vs_constant"],
                "best_loo_adjusted_r2": best_loo["adjusted_r2_vs_constant"],
                "best_loo_skill": best_loo["loo_skill_vs_constant"],
            }
        )
    return out


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    product_rows = read_product_rows(args.raw_csv, args.alpha, args.mode)
    if not product_rows:
        raise SystemExit(f"no product rows for alpha={args.alpha} mode={args.mode}")
    primes, ap, reduction = read_ap_cache(args.ap_csv)
    s1 = reconstruct_s1(product_rows, primes, ap, reduction, float(args.alpha))
    series_rows = build_series_rows(product_rows, s1)
    zeros = read_zeros(args.zeros_json)
    fit_rows = fit_zero_frequencies(series_rows, zeros, args.alpha, args.mode)
    summary_rows = summarize_by_best_fit(fit_rows)

    series_path = args.out_dir / "S1E_residual_series.csv"
    fits_path = args.out_dir / "S1E_zero_frequency_fits.csv"
    summary_path = args.out_dir / "S1E_zero_frequency_summary.csv"
    metadata_path = args.out_dir / "S1E_run_metadata.csv"

    write_csv(series_path, series_rows)
    write_csv(fits_path, fit_rows)
    write_csv(summary_path, summary_rows)
    write_csv(
        metadata_path,
        [
            {
                "python": platform.python_version(),
                "raw_csv": str(args.raw_csv),
                "raw_csv_sha256": sha256(args.raw_csv),
                "ap_csv": str(args.ap_csv),
                "ap_csv_sha256": sha256(args.ap_csv),
                "zeros_json": str(args.zeros_json),
                "zeros_json_sha256": sha256(args.zeros_json),
                "alpha": args.alpha,
                "mode": args.mode,
                "series_rows": len(series_rows),
                "fit_rows": len(fit_rows),
            }
        ],
    )
    print(series_path)
    print(fits_path)
    print(summary_path)
    print(metadata_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
