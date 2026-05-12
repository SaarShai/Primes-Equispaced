#!/usr/bin/env python3
"""Dense S1 residual diagnostics for the EC smoothing theorem closure wave.

This uses only saved a_p and zero data. It tests a narrow model comparison:
whether the first few zero-frequency residual modes are better represented as
persistent oscillations or as oscillations damped by 1/log(K).
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
AP_CSV = ROOT / "handoff-2026-05-11-gpt55-wave" / "AGENT3_EC_AP_TABLE_1000000.csv"
PRODUCT_CSV = ROOT / "handoff-2026-05-11-gpt55-wave" / "AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv"
ZEROS_JSON = ROOT / "koyama-shared" / "data" / "pari_authoritative_zeros.json"


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
    if t <= alpha:
        return 1.0
    if t >= 1.0:
        return 0.0
    u = (t - alpha) / (1.0 - alpha)
    return 1.0 - u * u * (3.0 - 2.0 * u)


def log_grid(k_min: int = 1000, k_max: int = 1_000_000, n: int = 121) -> List[int]:
    lo = math.log(k_min)
    hi = math.log(k_max)
    vals = []
    seen = set()
    for i in range(n):
        k = int(round(math.exp(lo + (hi - lo) * i / (n - 1))))
        k = max(k_min, min(k_max, k))
        if k not in seen:
            seen.add(k)
            vals.append(k)
    return vals


def read_ranks(path: Path) -> Dict[str, int]:
    ranks: Dict[str, int] = {}
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            ranks.setdefault(row["curve"], int(row["rank"]))
    return ranks


def read_ap_cache(path: Path) -> Tuple[List[int], Dict[str, List[int]]]:
    primes: List[int] = []
    ap: Dict[str, List[int]] = {}
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
        for row in reader:
            primes.append(int(row["p"]))
            for curve in curves:
                ap[curve].append(int(row[f"a_p({curve})"]))
    return primes, ap


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


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def solve_least_squares(features: Sequence[Sequence[float]], y: Sequence[float]) -> List[float]:
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


def predict(beta: Sequence[float], features: Sequence[Sequence[float]]) -> List[float]:
    return [sum(b * x for b, x in zip(beta, row)) for row in features]


def rmse(y: Sequence[float], yhat: Sequence[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(y, yhat)) / len(y))


def kfold_rmse(features: Sequence[Sequence[float]], y: Sequence[float], folds: int = 5) -> float:
    errs: List[float] = []
    n = len(y)
    for fold in range(folds):
        test_idx = [i for i in range(n) if i % folds == fold]
        train_idx = [i for i in range(n) if i % folds != fold]
        beta = solve_least_squares([features[i] for i in train_idx], [y[i] for i in train_idx])
        for i in test_idx:
            pred = sum(b * x for b, x in zip(beta, features[i]))
            errs.append(y[i] - pred)
    return math.sqrt(sum(e * e for e in errs) / len(errs))


def bic(rss: float, n: int, p: int) -> float:
    return n * math.log(max(rss / n, 1.0e-300)) + p * math.log(n)


def make_features(model: str, u: Sequence[float], gamma: float) -> List[List[float]]:
    rows: List[List[float]] = []
    for ui in u:
        c = math.cos(gamma * ui)
        s = math.sin(gamma * ui)
        if model == "constant":
            rows.append([1.0])
        elif model == "persistent_zero":
            rows.append([1.0, c, s])
        elif model == "damped_zero":
            rows.append([1.0, c / ui, s / ui])
        elif model == "damped_zero_plus_1_over_logK":
            rows.append([1.0, 1.0 / ui, c / ui, s / ui])
        else:
            raise ValueError(model)
    return rows


def reconstruct_rows(alpha: float = 0.75) -> List[Dict[str, object]]:
    ranks = read_ranks(PRODUCT_CSV)
    primes, ap = read_ap_cache(AP_CSV)
    ks = log_grid()
    rows: List[Dict[str, object]] = []
    for curve in sorted(ap):
        rank = ranks[curve]
        coeff = 0.5 - rank
        values = ap[curve]
        for k in ks:
            s1 = 0.0
            for p, a in zip(primes, values):
                if p > k:
                    break
                w = smooth_weight(p / float(k), alpha)
                if w:
                    s1 += w * a / float(p)
            log_k = math.log(k)
            loglog_k = math.log(log_k)
            adjusted = s1 - coeff * loglog_k
            rows.append(
                {
                    "curve": curve,
                    "rank": rank,
                    "K": k,
                    "alpha": fmt(alpha),
                    "logK": fmt(log_k),
                    "loglogK": fmt(loglog_k),
                    "s1_all": fmt(s1),
                    "central_coeff_0p5_minus_rank": fmt(coeff),
                    "s1_adjusted": fmt(adjusted),
                }
            )
    return rows


def compare_models(series_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    zeros = read_zeros(ZEROS_JSON)
    by_curve: Dict[str, List[Mapping[str, object]]] = {}
    for row in series_rows:
        by_curve.setdefault(str(row["curve"]), []).append(row)

    out: List[Dict[str, object]] = []
    models = [
        "constant",
        "persistent_zero",
        "damped_zero",
        "damped_zero_plus_1_over_logK",
    ]
    for curve, rows in sorted(by_curve.items()):
        if curve not in zeros:
            continue
        rows = sorted(rows, key=lambda r: int(r["K"]))
        u = [float(r["logK"]) for r in rows]
        y = [float(r["s1_adjusted"]) for r in rows]
        n = len(y)
        for zero_index, gamma in enumerate(zeros[curve][:3], start=1):
            constant_bic = None
            constant_cv = None
            for model in models:
                features = make_features(model, u, gamma)
                beta = solve_least_squares(features, y)
                yhat = predict(beta, features)
                rss = sum((a - b) ** 2 for a, b in zip(y, yhat))
                cv = kfold_rmse(features, y)
                this_bic = bic(rss, n, len(beta))
                if model == "constant":
                    constant_bic = this_bic
                    constant_cv = cv
                osc_amp = 0.0
                if model == "persistent_zero":
                    osc_amp = math.hypot(beta[1], beta[2])
                    amp_at_k_min = osc_amp
                    amp_at_k_max = osc_amp
                elif model == "damped_zero":
                    osc_amp = math.hypot(beta[1], beta[2])
                    amp_at_k_min = osc_amp / min(u)
                    amp_at_k_max = osc_amp / max(u)
                elif model == "damped_zero_plus_1_over_logK":
                    osc_amp = math.hypot(beta[2], beta[3])
                    amp_at_k_min = osc_amp / min(u)
                    amp_at_k_max = osc_amp / max(u)
                else:
                    amp_at_k_min = 0.0
                    amp_at_k_max = 0.0
                out.append(
                    {
                        "curve": curve,
                        "rank": rows[0]["rank"],
                        "n": n,
                        "zero_index": zero_index,
                        "gamma": fmt(gamma),
                        "model": model,
                        "parameters": len(beta),
                        "rmse": fmt(rmse(y, yhat)),
                        "cv_rmse_mod5": fmt(cv),
                        "bic": fmt(this_bic),
                        "delta_bic_vs_constant": fmt(this_bic - constant_bic if constant_bic is not None else 0.0),
                        "cv_skill_vs_constant": fmt(1.0 - (cv * cv) / (constant_cv * constant_cv) if constant_cv else 0.0),
                        "oscillator_coefficient_amplitude": fmt(osc_amp),
                        "implied_amp_at_K_min": fmt(amp_at_k_min),
                        "implied_amp_at_K_max": fmt(amp_at_k_max),
                        "amp_Kmax_over_Kmin": fmt(amp_at_k_max / amp_at_k_min if amp_at_k_min else 0.0),
                    }
                )
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    series_rows = reconstruct_rows()
    comparison_rows = compare_models(series_rows)
    write_csv(OUT / "DENSE_S1_residual_grid.csv", series_rows)
    write_csv(OUT / "DENSE_S1_model_comparison.csv", comparison_rows)
    write_csv(
        OUT / "DENSE_S1_metadata.csv",
        [
            {
                "python": platform.python_version(),
                "ap_csv": str(AP_CSV),
                "ap_csv_sha256": sha256(AP_CSV),
                "product_csv": str(PRODUCT_CSV),
                "product_csv_sha256": sha256(PRODUCT_CSV),
                "zeros_json": str(ZEROS_JSON),
                "zeros_json_sha256": sha256(ZEROS_JSON),
                "script_sha256_note": "hash after write available via shasum -a 256",
                "grid_points_per_curve": len({row["K"] for row in series_rows}),
                "series_rows": len(series_rows),
                "comparison_rows": len(comparison_rows),
            }
        ],
    )
    print(OUT / "DENSE_S1_residual_grid.csv")
    print(OUT / "DENSE_S1_model_comparison.csv")
    print(OUT / "DENSE_S1_metadata.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
