#!/usr/bin/env python3
"""H2-D slope diagnostics for the Agent 3 EC smoothed product CSV.

The H2 target is

    log P_E,W(K) = -rank(E) log log K + B_E,W + o(1).

This script does not recompute elliptic-curve data. It only reads the existing
Agent 3 CSV/metrics/summary files and writes H2-D-local diagnostics.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import platform
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


MODE_ORDER = [
    "sharp",
    "c_only",
    "P_only",
    "L2_only",
    "cP_only",
    "cL2_only",
    "PL2_only",
    "all",
]

CURVE_ORDER = ["11a1", "37a1", "389a1"]
WINDOWS = [("all", None), ("tail_ge_100000", 100000)]


def default_paths() -> Tuple[Path, Path, Path, Path]:
    here = Path(__file__).resolve().parent
    root = here.parent
    wave = root / "handoff-2026-05-11-gpt55-wave"
    return (
        wave / "AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv",
        wave / "AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv",
        wave / "AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md",
        here,
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(x: float, digits: int = 12) -> str:
    if math.isnan(x):
        return "nan"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    return f"{x:.{digits}g}"


def alpha_key(alpha: str) -> Tuple[float, str]:
    return (float(alpha), alpha)


def mode_key(mode: str) -> Tuple[int, str]:
    try:
        return (MODE_ORDER.index(mode), mode)
    except ValueError:
        return (len(MODE_ORDER), mode)


def curve_key(curve: str) -> Tuple[int, str]:
    try:
        return (CURVE_ORDER.index(curve), curve)
    except ValueError:
        return (len(CURVE_ORDER), curve)


def read_raw(path: Path) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            K = int(row["K"])
            rank = int(row["rank"])
            P = float(row["P"])
            if K <= 1:
                raise ValueError(f"K must exceed 1, got {K}")
            if P <= 0:
                raise ValueError(f"P must be positive, got {P} for {row}")
            loglogK = math.log(math.log(K))
            logP = math.log(P)
            rows.append(
                {
                    **row,
                    "rank_i": rank,
                    "conductor_i": int(row["conductor"]),
                    "K_i": K,
                    "alpha_f": float(row["alpha"]),
                    "P_f": P,
                    "loglogK": loglogK,
                    "logP": logP,
                    "h2_adjusted": logP + rank * loglogK,
                    "expected_slope": -float(rank),
                }
            )
    return rows


def read_metrics(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def ols(xs: Sequence[float], ys: Sequence[float]) -> Dict[str, float]:
    n = len(xs)
    if n < 2:
        raise ValueError("OLS needs at least two points")
    xbar = sum(xs) / n
    ybar = sum(ys) / n
    sxx = sum((x - xbar) ** 2 for x in xs)
    if sxx == 0:
        raise ValueError("OLS x values are constant")
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    rss = sum(r * r for r in residuals)
    tss = sum((y - ybar) ** 2 for y in ys)
    r2 = float("nan") if tss == 0 else 1.0 - rss / tss
    rmse = math.sqrt(rss / n)
    return {"slope": slope, "intercept": intercept, "r2": r2, "rmse": rmse}


def stdev_pop(values: Sequence[float]) -> float:
    if not values:
        return float("nan")
    m = sum(values) / len(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / len(values))


def compute_adjusted_rows(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for r in rows:
        out.append(
            {
                "curve": r["curve"],
                "rank": r["rank"],
                "conductor": r["conductor"],
                "K": r["K"],
                "alpha": r["alpha"],
                "mode": r["mode"],
                "P": fmt(float(r["P_f"]), 17),
                "loglogK": fmt(float(r["loglogK"]), 17),
                "logP": fmt(float(r["logP"]), 17),
                "h2_adjusted_logP_plus_rank_loglogK": fmt(
                    float(r["h2_adjusted"]), 17
                ),
            }
        )
    return out


def compute_fits(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    groups: Dict[Tuple[str, str, str], List[Dict[str, object]]] = defaultdict(list)
    for r in rows:
        groups[(str(r["mode"]), str(r["alpha"]), str(r["curve"]))].append(r)

    fits: List[Dict[str, object]] = []
    for (mode, alpha, curve), group in groups.items():
        group = sorted(group, key=lambda r: int(r["K_i"]))
        rank = int(group[0]["rank_i"])
        conductor = int(group[0]["conductor_i"])
        for window, min_k in WINDOWS:
            sub = [r for r in group if min_k is None or int(r["K_i"]) >= min_k]
            xs = [float(r["loglogK"]) for r in sub]
            ys = [float(r["logP"]) for r in sub]
            adjusted = [float(r["h2_adjusted"]) for r in sub]
            fit = ols(xs, ys)
            slope_error = fit["slope"] + rank
            last_step = adjusted[-1] - adjusted[-2] if len(adjusted) >= 2 else float("nan")
            fits.append(
                {
                    "mode": mode,
                    "alpha": alpha,
                    "curve": curve,
                    "rank": rank,
                    "conductor": conductor,
                    "window": window,
                    "n": len(sub),
                    "K_min": min(int(r["K_i"]) for r in sub),
                    "K_max": max(int(r["K_i"]) for r in sub),
                    "slope_logP_vs_loglogK": fit["slope"],
                    "expected_slope": -float(rank),
                    "slope_error_vs_minus_rank": slope_error,
                    "intercept": fit["intercept"],
                    "r2": fit["r2"],
                    "rmse_logP": fit["rmse"],
                    "adjusted_mean": sum(adjusted) / len(adjusted),
                    "adjusted_sd_pop": stdev_pop(adjusted),
                    "adjusted_min": min(adjusted),
                    "adjusted_max": max(adjusted),
                    "adjusted_range": max(adjusted) - min(adjusted),
                    "adjusted_first": adjusted[0],
                    "adjusted_last": adjusted[-1],
                    "adjusted_endpoint_drift": adjusted[-1] - adjusted[0],
                    "adjusted_last_step": last_step,
                    "P_first": float(sub[0]["P_f"]),
                    "P_last": float(sub[-1]["P_f"]),
                }
            )
    fits.sort(
        key=lambda r: (
            str(r["window"]),
            mode_key(str(r["mode"])),
            alpha_key(str(r["alpha"])),
            curve_key(str(r["curve"])),
        )
    )
    return fits


def compute_mode_summary(fits: List[Dict[str, object]]) -> List[Dict[str, object]]:
    groups: Dict[Tuple[str, str, str], List[Dict[str, object]]] = defaultdict(list)
    for r in fits:
        groups[(str(r["mode"]), str(r["alpha"]), str(r["window"]))].append(r)

    out: List[Dict[str, object]] = []
    for (mode, alpha, window), group in groups.items():
        errors = [float(r["slope_error_vs_minus_rank"]) for r in group]
        ranges = [float(r["adjusted_range"]) for r in group]
        last_steps = [float(r["adjusted_last_step"]) for r in group]
        endpoint = [float(r["adjusted_endpoint_drift"]) for r in group]
        worst_slope = max(group, key=lambda r: abs(float(r["slope_error_vs_minus_rank"])))
        worst_range = max(group, key=lambda r: float(r["adjusted_range"]))
        out.append(
            {
                "mode": mode,
                "alpha": alpha,
                "window": window,
                "n_curves": len(group),
                "max_abs_slope_error": max(abs(e) for e in errors),
                "rms_slope_error": math.sqrt(sum(e * e for e in errors) / len(errors)),
                "mean_abs_slope_error": sum(abs(e) for e in errors) / len(errors),
                "max_adjusted_range": max(ranges),
                "mean_adjusted_range": sum(ranges) / len(ranges),
                "max_abs_adjusted_last_step": max(abs(x) for x in last_steps),
                "max_abs_adjusted_endpoint_drift": max(abs(x) for x in endpoint),
                "worst_slope_curve": worst_slope["curve"],
                "worst_slope_error": worst_slope["slope_error_vs_minus_rank"],
                "worst_range_curve": worst_range["curve"],
                "worst_range": worst_range["adjusted_range"],
            }
        )
    out.sort(
        key=lambda r: (
            str(r["window"]),
            mode_key(str(r["mode"])),
            alpha_key(str(r["alpha"])),
        )
    )
    return out


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def table(rows: Iterable[Sequence[object]], headers: Sequence[str]) -> str:
    rows = list(rows)
    all_rows = [list(map(str, headers))] + [list(map(str, row)) for row in rows]
    widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]
    lines = []
    lines.append("| " + " | ".join(all_rows[0][i].ljust(widths[i]) for i in range(len(headers))) + " |")
    lines.append("| " + " | ".join("-" * widths[i] for i in range(len(headers))) + " |")
    for row in all_rows[1:]:
        lines.append("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    return "\n".join(lines)


def find_fit(
    fits: List[Dict[str, object]], mode: str, alpha: float, curve: str, window: str
) -> Dict[str, object]:
    for r in fits:
        if (
            r["mode"] == mode
            and abs(float(r["alpha"]) - alpha) < 1e-12
            and r["curve"] == curve
            and r["window"] == window
        ):
            return r
    raise KeyError((mode, alpha, curve, window))


def find_summary(
    summary: List[Dict[str, object]], mode: str, alpha: float, window: str
) -> Dict[str, object]:
    for r in summary:
        if (
            r["mode"] == mode
            and abs(float(r["alpha"]) - alpha) < 1e-12
            and r["window"] == window
        ):
            return r
    raise KeyError((mode, alpha, window))


def metric_row(metrics: List[Dict[str, str]], mode: str, alpha: float) -> Dict[str, str]:
    for r in metrics:
        if r["mode"] == mode and abs(float(r["alpha"]) - alpha) < 1e-12:
            return r
    raise KeyError((mode, alpha))


def write_report(
    path: Path,
    *,
    raw_path: Path,
    metrics_path: Path,
    summary_path: Path,
    adjusted_path: Path,
    fits_path: Path,
    mode_summary_path: Path,
    rows: List[Dict[str, object]],
    metrics: List[Dict[str, str]],
    fits: List[Dict[str, object]],
    mode_summary: List[Dict[str, object]],
    command: str,
) -> None:
    raw_sha = sha256(raw_path)
    metrics_sha = sha256(metrics_path)
    summary_sha = sha256(summary_path)
    pass_count = sum(1 for r in metrics if r.get("passes_old_gate") == "True")

    key_fit_rows = []
    for curve in CURVE_ORDER:
        all_fit = find_fit(fits, "all", 0.75, curve, "all")
        tail_fit = find_fit(fits, "all", 0.75, curve, "tail_ge_100000")
        key_fit_rows.append(
            [
                curve,
                str(all_fit["rank"]),
                fmt(float(all_fit["slope_logP_vs_loglogK"])),
                fmt(float(all_fit["slope_error_vs_minus_rank"])),
                fmt(float(all_fit["adjusted_range"])),
                fmt(float(tail_fit["slope_logP_vs_loglogK"])),
                fmt(float(tail_fit["slope_error_vs_minus_rank"])),
                fmt(float(tail_fit["adjusted_range"])),
                fmt(float(tail_fit["adjusted_last_step"])),
            ]
        )

    alpha_rows = []
    for alpha in sorted({float(r["alpha"]) for r in rows}):
        all_sum = find_summary(mode_summary, "P_only", alpha, "all")
        tail_sum = find_summary(mode_summary, "P_only", alpha, "tail_ge_100000")
        alpha_rows.append(
            [
                fmt(alpha, 4),
                fmt(float(all_sum["max_abs_slope_error"])),
                fmt(float(all_sum["rms_slope_error"])),
                fmt(float(tail_sum["max_abs_slope_error"])),
                fmt(float(tail_sum["rms_slope_error"])),
                fmt(float(tail_sum["max_adjusted_range"])),
            ]
        )

    gate_rows = []
    for mode in ["all", "cP_only", "P_only"]:
        r = metric_row(metrics, mode, 0.75)
        gate_rows.append(
            [
                mode,
                r["passes_old_gate"],
                fmt(float(r["cross_curve_ratio"])),
                fmt(float(r["max_within_cv"])),
            ]
        )

    family_rows = []
    for family, representative, modes in [
        ("P-smoothed", "all", "all, cP_only, P_only, PL2_only"),
        ("unsmoothed P", "sharp", "sharp, c_only, L2_only, cL2_only"),
    ]:
        all_sum = find_summary(mode_summary, representative, 0.75, "all")
        tail_sum = find_summary(mode_summary, representative, 0.75, "tail_ge_100000")
        family_rows.append(
            [
                family,
                modes,
                representative,
                fmt(float(all_sum["max_abs_slope_error"])),
                fmt(float(tail_sum["max_abs_slope_error"])),
                fmt(float(tail_sum["max_adjusted_range"])),
            ]
        )

    tail_value_rows = []
    for curve in CURVE_ORDER:
        sub = [
            r
            for r in rows
            if r["mode"] == "all"
            and abs(float(r["alpha"]) - 0.75) < 1e-12
            and r["curve"] == curve
            and int(r["K_i"]) >= 100000
        ]
        sub = sorted(sub, key=lambda r: int(r["K_i"]))
        tail_value_rows.append(
            [
                curve,
                str(sub[0]["rank"]),
                fmt(float(sub[0]["h2_adjusted"])),
                fmt(float(sub[1]["h2_adjusted"])),
                fmt(float(sub[2]["h2_adjusted"])),
                fmt(float(sub[2]["h2_adjusted"]) - float(sub[1]["h2_adjusted"])),
            ]
        )

    all_075 = find_summary(mode_summary, "P_only", 0.75, "all")
    tail_075 = find_summary(mode_summary, "P_only", 0.75, "tail_ge_100000")

    md = f"""---
schema_version: 1
title: "H2-D numerical slope diagnostics"
date: 2026-05-11
type: report
tier: working
status: AUDIT_ONLY
confidence: 0.62
sources:
  - {raw_path.as_posix()}
  - {metrics_path.as_posix()}
  - {summary_path.as_posix()}
  - {Path(__file__).resolve().as_posix()}
tags: [ec-ndc, smoothing, h2, mertens, diagnostics]
---

# H2-D Numerical Slope Diagnostics

status: `AUDIT_ONLY`

## Verdict

Do not promote. The existing seven-point grid gives a decent all-grid slope
match for the P-smoothed `alpha=0.75` product, but the three-point tail fit does
not show settled stabilization.

For `all/cP_only/P_only, alpha=0.75`, the H2 product diagnostics are exactly the
same, because H2 uses only `P` and all three modes have the same smoothed `P`
column. This numerical check therefore cannot distinguish the full `all`
normalization from the `cP_only` or `P_only` ablations.

## Target

H2 predicts

```text
log P_E,W(K) = -rank(E) log log K + B_E,W + o(1).
```

I fit `log P` against `log log K`. A matching slope has
`slope_logP_vs_loglogK = -rank`. Equivalently,
`log P + rank log log K` should have slope `0` and should stabilize.

Windows:

- all grid: `K=1000,3000,10000,30000,100000,300000,1000000`
- tail grid: `K>=100000`, i.e. `100000,300000,1000000`

## Mode Collapse For H2

H2 only tests the `P` column. The eight Agent 3 modes therefore collapse into
two product families.

{table(family_rows, ["family", "modes", "representative", "all max abs err", "tail max abs err", "tail max adj range"])}

The full per-mode/per-alpha fits are in `{fits_path.as_posix()}` and the
per-mode summaries are in `{mode_summary_path.as_posix()}`.

## Key Fits: `all`, `alpha=0.75`

{table(key_fit_rows, ["curve", "rank", "all slope", "all slope error", "all adj range", "tail slope", "tail slope error", "tail adj range", "tail last step"])}

Read:

- all-grid slopes are close to `-rank`: max absolute slope error
  `{fmt(float(all_075["max_abs_slope_error"]))}`.
- tail-grid slopes are not close: max absolute slope error
  `{fmt(float(tail_075["max_abs_slope_error"]))}`.
- the rank-2 curve `389a1` has tail adjusted last step
  `{fmt(float(find_fit(fits, "all", 0.75, "389a1", "tail_ge_100000")["adjusted_last_step"]))}`,
  so the last endpoint is still moving visibly.

## Tail Adjusted Values: `all`, `alpha=0.75`

Values are `log P + rank log log K`.

{table(tail_value_rows, ["curve", "rank", "K=100000", "K=300000", "K=1000000", "last step"])}

## Alpha Sweep For P-Smoothed Modes

The table uses `P_only`, but the same H2 product rows apply to `all`,
`cP_only`, and `PL2_only` for the same alpha.

{table(alpha_rows, ["alpha", "all max abs err", "all RMS err", "tail max abs err", "tail RMS err", "tail max adj range"])}

The all-grid optimum by max slope error is `alpha=0.75`. Tail diagnostics do
not select the same story cleanly: every tested alpha has tail max absolute
slope error at least about `0.18`, and the tail has only three points.

## Agent 3 Gate Reference

Read from the existing metrics CSV. These are old `X` gate values, not H2 slope
tests.

{table(gate_rows, ["mode", "old gate", "ratio", "max CV"])}

The old gate pass for `all, alpha=0.75` remains numerically real. The H2 product
test shows that the product part alone is identical for the `all/cP_only/P_only`
comparison, so that old pass is not evidence that the `L2^rank` denominator is
load-bearing.

## Caveats

- The tail fit has only three K values. It can flag instability, but it cannot
  falsify an asymptotic statement.
- The largest endpoint, `K=1000000`, has high leverage on the tail slope.
- The current data are three curves only: ranks `0,1,2`, one curve each.
- No new EC products, `a_p` values, holdout curves, or dense K grids were
  computed here.

## Exact Command

```bash
{command}
```

## Source Hashes

- raw CSV SHA256: `{raw_sha}`
- metrics CSV SHA256: `{metrics_sha}`
- summary markdown SHA256: `{summary_sha}`
- Python: `{platform.python_version()}`

## Outputs

- `{adjusted_path.as_posix()}`
- `{fits_path.as_posix()}`
- `{mode_summary_path.as_posix()}`
- `{path.as_posix()}`

## Status Decision

`AUDIT_ONLY`: this is a numerical audit of existing reproduction data. It gives
supporting all-grid diagnostics for `alpha=0.75`, but tail-grid diagnostics are
too sparse and too unsettled to promote H2 or to declare a numerical no-go.

"""
    path.write_text(md)


def main() -> int:
    default_raw, default_metrics, default_summary, default_out = default_paths()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-csv", type=Path, default=default_raw)
    parser.add_argument("--metrics-csv", type=Path, default=default_metrics)
    parser.add_argument("--summary-md", type=Path, default=default_summary)
    parser.add_argument("--out-dir", type=Path, default=default_out)
    args = parser.parse_args()

    raw_path = args.raw_csv.resolve()
    metrics_path = args.metrics_csv.resolve()
    summary_path = args.summary_md.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = read_raw(raw_path)
    metrics = read_metrics(metrics_path)
    fits = compute_fits(rows)
    mode_summary = compute_mode_summary(fits)
    adjusted_rows = compute_adjusted_rows(rows)

    adjusted_path = out_dir / "H2D_adjusted_values.csv"
    fits_path = out_dir / "H2D_slope_fits.csv"
    mode_summary_path = out_dir / "H2D_slope_mode_summary.csv"
    report_path = out_dir / "H2D_NUMERICAL_DIAGNOSTICS.md"

    write_csv(adjusted_path, adjusted_rows)
    write_csv(fits_path, fits)
    write_csv(mode_summary_path, mode_summary)

    command = (
        "python3 handoff-2026-05-11-ec-h2-mertens-sprint/"
        "H2D_slope_diagnostics.py "
        "--raw-csv handoff-2026-05-11-gpt55-wave/"
        "AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv "
        "--metrics-csv handoff-2026-05-11-gpt55-wave/"
        "AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv "
        "--summary-md handoff-2026-05-11-gpt55-wave/"
        "AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md "
        "--out-dir handoff-2026-05-11-ec-h2-mertens-sprint"
    )
    write_report(
        report_path,
        raw_path=raw_path,
        metrics_path=metrics_path,
        summary_path=summary_path,
        adjusted_path=adjusted_path,
        fits_path=fits_path,
        mode_summary_path=mode_summary_path,
        rows=rows,
        metrics=metrics,
        fits=fits,
        mode_summary=mode_summary,
        command=command,
    )

    print(f"wrote {adjusted_path}")
    print(f"wrote {fits_path}")
    print(f"wrote {mode_summary_path}")
    print(f"wrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
