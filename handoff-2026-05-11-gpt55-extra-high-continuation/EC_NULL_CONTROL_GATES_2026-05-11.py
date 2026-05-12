#!/usr/bin/env python3
"""
Read-only null-control gate audit for AGENT3 EC smoothed proxy outputs.

This is a narrow successor to AGENT3_ec_smoothed_reproducer.py.  It does not
recompute a_p, change kernels, or edit the original AGENT3 CSVs.  It consumes a
raw CSV and metrics CSV, applies predeclared null/ablation gates, and writes new
audit artifacts only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import platform
import shlex
import statistics
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
AGENT3_DIR = PROJECT_DIR / "handoff-2026-05-11-gpt55-wave"

DEFAULT_RAW_CSV = AGENT3_DIR / "AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv"
DEFAULT_METRICS_CSV = AGENT3_DIR / "AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv"
DEFAULT_SUMMARY_CSV = SCRIPT_DIR / "EC_NULL_CONTROL_ABLATION_SUMMARY_2026-05-11.csv"
DEFAULT_REPORT = SCRIPT_DIR / "EC_NULL_CONTROL_GATES_2026-05-11.md"

PRIMARY_MODE = "all"
PRIMARY_ALPHA = 0.75
PRIMARY_KERNEL = "smoothstep"
PREDECLARED_NULL_MODES = ("cP_only", "P_only", "PL2_only")
SUPPORTING_ABLATION_MODES = ("sharp", "c_only", "L2_only", "cL2_only")
CURVE_LABELS = ("37a1", "11a1", "389a1")

OLD_GATE_CROSS_RATIO = 1.42083
OLD_GATE_MAX_WITHIN_CV = 0.08567129
ANCHOR_RATIO = 1.3473754929960748
ANCHOR_MAX_CV = 0.063297427334436704
ANCHOR_TOL = 5e-13
MATERIAL_SCORE_MARGIN = 0.01


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-csv", type=Path, default=DEFAULT_RAW_CSV)
    parser.add_argument("--metrics-csv", type=Path, default=DEFAULT_METRICS_CSV)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_SUMMARY_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--force", action="store_true", help="allow overwriting audit outputs")
    return parser.parse_args(argv)


def read_dict_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(value: float, digits: int = 17) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf"
    return f"{value:.{digits}g}"


def alpha_matches(row: Mapping[str, str], alpha: float) -> bool:
    return abs(float(row["alpha"]) - alpha) <= 1e-12


def old_gate_passes(ratio: float, max_within_cv: float) -> bool:
    return ratio < OLD_GATE_CROSS_RATIO and max_within_cv < OLD_GATE_MAX_WITHIN_CV


def row_passes_old_gate(row: Mapping[str, str]) -> bool:
    return old_gate_passes(float(row["cross_curve_ratio"]), float(row["max_within_cv"]))


def score(ratio: float, max_within_cv: float) -> float:
    return math.log(ratio) + max_within_cv


def metric_score(row: Mapping[str, str]) -> float:
    return score(float(row["cross_curve_ratio"]), float(row["max_within_cv"]))


def coefficient_of_variation(values: Sequence[float]) -> float:
    mean = statistics.fmean(values)
    if mean == 0.0:
        return math.inf
    return math.sqrt(statistics.fmean((value - mean) ** 2 for value in values)) / abs(mean)


def metrics_from_raw(rows: Sequence[Mapping[str, str]]) -> Dict[str, object]:
    by_curve: Dict[str, List[float]] = {label: [] for label in CURVE_LABELS}
    for row in rows:
        by_curve[row["curve"]].append(float(row["X"]))
    missing = [label for label, values in by_curve.items() if not values]
    if missing:
        raise ValueError(f"raw rows missing curve(s): {', '.join(missing)}")

    means = {label: statistics.fmean(values) for label, values in by_curve.items()}
    cvs = {label: coefficient_of_variation(values) for label, values in by_curve.items()}
    mean_values = list(means.values())
    ratio = max(mean_values) / min(mean_values)
    max_cv = max(cvs.values())
    return {
        "cross_curve_ratio": ratio,
        "cross_curve_cv": coefficient_of_variation(mean_values),
        "max_within_cv": max_cv,
        "score": score(ratio, max_cv),
        "means": means,
        "cvs": cvs,
        "passes_old_gate": old_gate_passes(ratio, max_cv),
    }


def find_metric(
    metrics: Sequence[Mapping[str, str]],
    mode: str,
    alpha: float,
) -> Mapping[str, str]:
    matches = [row for row in metrics if row["mode"] == mode and alpha_matches(row, alpha)]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one metrics row for mode={mode}, alpha={alpha}; found {len(matches)}")
    return matches[0]


def best_row_for_mode(metrics: Sequence[Mapping[str, str]], mode: str) -> Mapping[str, str]:
    rows = [row for row in metrics if row["mode"] == mode]
    if not rows:
        raise ValueError(f"no metrics rows for mode={mode}")
    return min(rows, key=lambda row: (metric_score(row), float(row["cross_curve_ratio"]), float(row["max_within_cv"])))


def primary_raw_rows(raw_rows: Sequence[Mapping[str, str]]) -> List[Mapping[str, str]]:
    rows = [row for row in raw_rows if row["mode"] == PRIMARY_MODE and alpha_matches(row, PRIMARY_ALPHA)]
    if not rows:
        raise ValueError(f"no raw rows for mode={PRIMARY_MODE}, alpha={PRIMARY_ALPHA}")
    return rows


def leave_one_k_diagnostics(primary_rows: Sequence[Mapping[str, str]]) -> Dict[str, object]:
    k_values = sorted({int(row["K"]) for row in primary_rows})
    rows = []
    for k in k_values:
        metric = metrics_from_raw([row for row in primary_rows if int(row["K"]) != k])
        rows.append(
            {
                "held_out_K": k,
                "cross_curve_ratio": float(metric["cross_curve_ratio"]),
                "max_within_cv": float(metric["max_within_cv"]),
                "passes_old_gate": bool(metric["passes_old_gate"]),
            }
        )
    return {
        "rows": rows,
        "pass_count": sum(1 for row in rows if row["passes_old_gate"]),
        "ratio_min": min(row["cross_curve_ratio"] for row in rows),
        "ratio_max": max(row["cross_curve_ratio"] for row in rows),
        "maxcv_min": min(row["max_within_cv"] for row in rows),
        "maxcv_max": max(row["max_within_cv"] for row in rows),
    }


def leave_one_curve_diagnostics(primary_metric: Mapping[str, object]) -> List[Dict[str, object]]:
    means = primary_metric["means"]
    cvs = primary_metric["cvs"]
    assert isinstance(means, dict)
    assert isinstance(cvs, dict)
    rows = []
    for held in CURVE_LABELS:
        train = [float(means[label]) for label in CURVE_LABELS if label != held]
        train_geo_mean = math.exp(statistics.fmean(math.log(value) for value in train))
        held_mean = float(means[held])
        holdout_ratio = max(held_mean, train_geo_mean) / min(held_mean, train_geo_mean)
        holdout_cv = float(cvs[held])
        rows.append(
            {
                "held_out_curve": held,
                "train_geo_mean": train_geo_mean,
                "held_mean": held_mean,
                "holdout_ratio": holdout_ratio,
                "holdout_cv": holdout_cv,
                "passes_old_gate": old_gate_passes(holdout_ratio, holdout_cv),
            }
        )
    return rows


def make_ablation_rows(metrics: Sequence[Mapping[str, str]], primary: Mapping[str, str]) -> List[Dict[str, str]]:
    primary_ratio = float(primary["cross_curve_ratio"])
    primary_max_cv = float(primary["max_within_cv"])
    primary_score = metric_score(primary)
    modes = (PRIMARY_MODE,) + PREDECLARED_NULL_MODES + SUPPORTING_ABLATION_MODES
    rows = []
    for mode in modes:
        for row in sorted((r for r in metrics if r["mode"] == mode), key=lambda r: float(r["alpha"])):
            ratio = float(row["cross_curve_ratio"])
            max_cv = float(row["max_within_cv"])
            row_score = score(ratio, max_cv)
            rows.append(
                {
                    "classification": (
                        "primary"
                        if mode == PRIMARY_MODE
                        else "predeclared_null"
                        if mode in PREDECLARED_NULL_MODES
                        else "supporting_ablation"
                    ),
                    "mode": mode,
                    "alpha": row["alpha"],
                    "passes_old_gate": str(row_passes_old_gate(row)),
                    "cross_curve_ratio": fmt(ratio),
                    "max_within_cv": fmt(max_cv),
                    "score": fmt(row_score),
                    "ratio_delta_vs_primary": fmt(ratio - primary_ratio),
                    "maxcv_delta_vs_primary": fmt(max_cv - primary_max_cv),
                    "score_delta_vs_primary": fmt(row_score - primary_score),
                }
            )
    return rows


def gate_row(name: str, status: bool, detail: str) -> Dict[str, str]:
    return {"gate": name, "status": "PASS" if status else "FAIL", "detail": detail}


def write_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows to write for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def ensure_output_paths(paths: Iterable[Path], force: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if existing and not force:
        joined = "\n".join(f"  {path}" for path in existing)
        raise SystemExit(f"refusing to overwrite existing audit output(s):\n{joined}\nuse --force or choose new paths")
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def clean_rerun_command() -> str:
    rerun_dir = SCRIPT_DIR / "ec-null-control-rerun"
    repro_cmd = [
        "python3",
        str(AGENT3_DIR / "AGENT3_ec_smoothed_reproducer.py"),
        "--workers",
        "8",
        "--ap-cache",
        str(AGENT3_DIR / "AGENT3_EC_AP_TABLE_1000000.csv"),
        "--ap-cache-out",
        str(rerun_dir / "AGENT3_EC_AP_TABLE_1000000.csv"),
        "--raw-csv",
        str(rerun_dir / "AGENT3_EC_SMOOTHED_PROXY.csv"),
        "--metrics-csv",
        str(rerun_dir / "AGENT3_EC_SMOOTHED_PROXY_METRICS.csv"),
        "--report",
        str(rerun_dir / "AGENT3_EC_SMOOTHED_PROXY_SUMMARY.md"),
    ]
    audit_cmd = [
        "python3",
        str(SCRIPT_DIR / "EC_NULL_CONTROL_GATES_2026-05-11.py"),
        "--raw-csv",
        str(rerun_dir / "AGENT3_EC_SMOOTHED_PROXY.csv"),
        "--metrics-csv",
        str(rerun_dir / "AGENT3_EC_SMOOTHED_PROXY_METRICS.csv"),
        "--summary-csv",
        str(rerun_dir / "EC_NULL_CONTROL_ABLATION_SUMMARY.csv"),
        "--report",
        str(rerun_dir / "EC_NULL_CONTROL_GATES.md"),
    ]
    return "\n".join(
        [
            f"mkdir -p {shlex.quote(str(rerun_dir))}",
            " ".join(shlex.quote(part) for part in repro_cmd),
            " ".join(shlex.quote(part) for part in audit_cmd),
        ]
    )


def write_report(
    path: Path,
    args: argparse.Namespace,
    gate_rows: Sequence[Mapping[str, str]],
    ablation_rows: Sequence[Mapping[str, str]],
    primary: Mapping[str, str],
    best_null: Mapping[str, str],
    loo: Mapping[str, object],
    loc: Sequence[Mapping[str, object]],
    hashes: Mapping[str, str],
) -> None:
    raw_source = args.raw_csv.resolve()
    metrics_source = args.metrics_csv.resolve()
    script_source = Path(__file__).resolve()
    first_failure = next((row["gate"] for row in gate_rows if row["status"] == "FAIL"), "none")
    overall_status = "NO_GO" if first_failure != "none" else "PROOF_CANDIDATE"
    primary_score = metric_score(primary)
    best_null_score = metric_score(best_null)
    passing_nulls = [
        row
        for row in ablation_rows
        if row["classification"] == "predeclared_null" and row["passes_old_gate"] == "True"
    ]
    primary_alpha_nulls = [
        row
        for row in ablation_rows
        if row["classification"] == "predeclared_null"
        and abs(float(row["alpha"]) - PRIMARY_ALPHA) <= 1e-12
    ]

    lines = [
        "---",
        "schema_version: 1",
        'title: "EC null-control gates for AGENT3 smoothed proxy"',
        "date: 2026-05-11",
        "type: report",
        "tier: working",
        f"status: {overall_status}",
        "confidence: 0.76",
        "sources:",
        f"  - {raw_source.relative_to(PROJECT_DIR) if raw_source.is_relative_to(PROJECT_DIR) else raw_source}",
        f"  - {metrics_source.relative_to(PROJECT_DIR) if metrics_source.is_relative_to(PROJECT_DIR) else metrics_source}",
        f"  - {script_source.relative_to(PROJECT_DIR)}",
        "tags: [ec-ndc, smoothing, null-controls, ablation, no-promotion]",
        "---",
        "",
        "# EC Null-Control Gates",
        "",
        f"status: `{overall_status}`",
        f"first failing gate: `{first_failure}`",
        "",
        "## Scope",
        "",
        f"This audit is read-only over the saved `{PRIMARY_KERNEL}` AGENT3 CSVs. It does not implement new kernel families or stochastic null simulations.",
        f"Primary case is predeclared as `{PRIMARY_MODE}, alpha={PRIMARY_ALPHA}`.",
        f"Predeclared null modes are `{', '.join(PREDECLARED_NULL_MODES)}`.",
        "",
        "## Exact Command",
        "",
        f"- Command: `{' '.join(shlex.quote(arg) for arg in sys.argv)}`",
        f"- Python: `{platform.python_version()}`",
        f"- Script SHA256: `{hashes['script']}`",
        f"- Raw CSV SHA256: `{hashes['raw_csv']}`",
        f"- Metrics CSV SHA256: `{hashes['metrics_csv']}`",
        f"- Summary CSV: `{args.summary_csv}`",
        "",
        "## Gate Results",
        "",
        "| gate | status | detail |",
        "|---|---:|---|",
    ]
    for row in gate_rows:
        lines.append(f"| `{row['gate']}` | `{row['status']}` | {row['detail']} |")

    lines.extend(
        [
            "",
            "## Load-Bearing Ablation Summary",
            "",
            f"Primary score `log(ratio)+max_cv`: `{fmt(primary_score)}`.",
            f"Best predeclared null: `{best_null['mode']}, alpha={best_null['alpha']}`, score `{fmt(best_null_score)}`.",
            f"Best-null score delta versus primary: `{fmt(best_null_score - primary_score)}`.",
            f"Material margin required for load-bearing promotion: `{MATERIAL_SCORE_MARGIN}`.",
            "",
            "| class | mode | alpha | old gate | ratio | max CV | score | score delta vs primary |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    headline_modes = [
        row
        for row in ablation_rows
        if row["mode"] == PRIMARY_MODE
        or row in primary_alpha_nulls
        or (row["classification"] == "predeclared_null" and row["mode"] == best_null["mode"] and row["alpha"] == best_null["alpha"])
    ]
    seen = set()
    for row in headline_modes:
        key = (row["classification"], row["mode"], row["alpha"])
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            f"| `{row['classification']}` | `{row['mode']}` | {row['alpha']} | {row['passes_old_gate']} | "
            f"{row['cross_curve_ratio']} | {row['max_within_cv']} | {row['score']} | {row['score_delta_vs_primary']} |"
        )

    lines.extend(
        [
            "",
            "Passing predeclared null rows:",
            "",
            "| mode | alpha | ratio | max CV | score |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in passing_nulls:
        lines.append(
            f"| `{row['mode']}` | {row['alpha']} | {row['cross_curve_ratio']} | {row['max_within_cv']} | {row['score']} |"
        )

    lines.extend(
        [
            "",
            "## Leave-One-K Diagnostics",
            "",
            f"Pass count: `{loo['pass_count']}/7`.",
            f"Ratio range: `{fmt(float(loo['ratio_min']))}` to `{fmt(float(loo['ratio_max']))}`.",
            f"Max-CV range: `{fmt(float(loo['maxcv_min']))}` to `{fmt(float(loo['maxcv_max']))}`.",
            "",
            "| held-out K | old gate | ratio | max CV |",
            "|---:|---:|---:|---:|",
        ]
    )
    for row in loo["rows"]:
        lines.append(
            f"| {row['held_out_K']} | {row['passes_old_gate']} | "
            f"{fmt(float(row['cross_curve_ratio']))} | {fmt(float(row['max_within_cv']))} |"
        )

    lines.extend(
        [
            "",
            "## Leave-One-Curve Diagnostics",
            "",
            "| held-out curve | old gate | holdout ratio | holdout CV |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in loc:
        lines.append(
            f"| `{row['held_out_curve']}` | {row['passes_old_gate']} | "
            f"{fmt(float(row['holdout_ratio']))} | {fmt(float(row['holdout_cv']))} |"
        )

    lines.extend(
        [
            "",
            "## Clean Rerun Command",
            "",
            "Writes to a fresh rerun directory under this handoff folder and leaves original AGENT3 outputs untouched.",
            "",
            "```bash",
            clean_rerun_command(),
            "```",
            "",
            "## Do Not Promote Unless",
            "",
            "- A predeclared alpha, preferably `0.75`, survives holdout curves across ranks/conductors.",
            "- The signal survives a denser K grid and larger K, with tail-only drift controlled.",
            "- Component ablation shows the proposed normalization is load-bearing, not merely endpoint smoothing.",
            "- A theorem explains the smoothing kernel and normalization from an explicit Euler/Perron transform.",
            "",
            "## Next Controls",
            "",
            "- Implement the C2 primary kernel suite: smoothstep, hann, riesz, exponential, gaussian.",
            "- Run stochastic nulls: Sato-Tate iid/shared, prime-order permutation, sign-randomization.",
            "- Add rank and curve-label permutation controls for the `L2^rank` denominator.",
            "- Extend to holdout curves and a denser/larger K grid before any promotion.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_output_paths((args.summary_csv, args.report), args.force)

    raw_rows = read_dict_csv(args.raw_csv)
    metrics = read_dict_csv(args.metrics_csv)
    primary = find_metric(metrics, PRIMARY_MODE, PRIMARY_ALPHA)
    primary_metric_from_raw = metrics_from_raw(primary_raw_rows(raw_rows))
    loo = leave_one_k_diagnostics(primary_raw_rows(raw_rows))
    loc = leave_one_curve_diagnostics(primary_metric_from_raw)
    ablation_rows = make_ablation_rows(metrics, primary)

    primary_ratio = float(primary["cross_curve_ratio"])
    primary_max_cv = float(primary["max_within_cv"])
    primary_score = metric_score(primary)
    best_null = min(
        (row for row in metrics if row["mode"] in PREDECLARED_NULL_MODES),
        key=lambda row: (metric_score(row), float(row["cross_curve_ratio"]), float(row["max_within_cv"])),
    )
    best_null_score = metric_score(best_null)

    primary_anchor_ok = (
        row_passes_old_gate(primary)
        and abs(primary_ratio - ANCHOR_RATIO) <= ANCHOR_TOL
        and abs(primary_max_cv - ANCHOR_MAX_CV) <= ANCHOR_TOL
    )
    primary_survival_ok = (
        bool(primary_metric_from_raw["passes_old_gate"])
        and int(loo["pass_count"]) == len(loo["rows"])
        and all(bool(row["passes_old_gate"]) for row in loc)
    )

    primary_alpha_nulls = [
        row for row in metrics if row["mode"] in PREDECLARED_NULL_MODES and alpha_matches(row, PRIMARY_ALPHA)
    ]
    primary_alpha_null_passes = [row for row in primary_alpha_nulls if row_passes_old_gate(row)]
    sweep_null_passes = [row for row in metrics if row["mode"] in PREDECLARED_NULL_MODES and row_passes_old_gate(row)]
    load_bearing_score_ok = best_null_score - primary_score >= MATERIAL_SCORE_MARGIN
    cP_primary = find_metric(metrics, "cP_only", PRIMARY_ALPHA)
    cP_delta = metric_score(cP_primary) - primary_score
    l2_material_ok = cP_delta >= MATERIAL_SCORE_MARGIN

    gate_rows = [
        gate_row(
            "G0_primary_anchor",
            primary_anchor_ok,
            (
                f"`{PRIMARY_MODE}, alpha={PRIMARY_ALPHA}` ratio `{fmt(primary_ratio)}`, max CV `{fmt(primary_max_cv)}`; "
                f"anchor tolerance `{ANCHOR_TOL}`"
            ),
        ),
        gate_row(
            "G1_primary_survival",
            primary_survival_ok,
            (
                f"primary old gate `{row_passes_old_gate(primary)}`, leave-one-K `{loo['pass_count']}/7`, "
                f"leave-one-curve `{sum(1 for row in loc if row['passes_old_gate'])}/3`"
            ),
        ),
        gate_row(
            "G2_primary_alpha_null_rejection",
            not primary_alpha_null_passes,
            (
                "passing primary-alpha nulls: "
                + (
                    ", ".join(f"`{row['mode']}`" for row in primary_alpha_null_passes)
                    if primary_alpha_null_passes
                    else "none"
                )
            ),
        ),
        gate_row(
            "G3_alpha_sweep_null_rejection",
            not sweep_null_passes,
            (
                f"passing null mode/alpha rows `{len(sweep_null_passes)}` across modes "
                f"`{', '.join(PREDECLARED_NULL_MODES)}`"
            ),
        ),
        gate_row(
            "G4_best_null_margin",
            load_bearing_score_ok,
            (
                f"best null `{best_null['mode']}, alpha={best_null['alpha']}` score delta "
                f"`{fmt(best_null_score - primary_score)}` versus required `{MATERIAL_SCORE_MARGIN}`"
            ),
        ),
        gate_row(
            "G5_L2_smoothing_load_bearing",
            l2_material_ok,
            (
                f"`all` vs `cP_only` at alpha `{PRIMARY_ALPHA}` score delta `{fmt(cP_delta)}` "
                f"versus required `{MATERIAL_SCORE_MARGIN}`"
            ),
        ),
    ]

    write_csv(args.summary_csv, ablation_rows)
    hashes = {
        "script": sha256_file(Path(__file__).resolve()),
        "raw_csv": sha256_file(args.raw_csv),
        "metrics_csv": sha256_file(args.metrics_csv),
    }
    write_report(args.report, args, gate_rows, ablation_rows, primary, best_null, loo, loc, hashes)

    first_failure = next((row["gate"] for row in gate_rows if row["status"] == "FAIL"), "none")
    status = "NO_GO" if first_failure != "none" else "PROOF_CANDIDATE"
    print(f"status={status}")
    print(f"first_failing_gate={first_failure}")
    print(f"primary ratio={fmt(primary_ratio)} max_cv={fmt(primary_max_cv)} score={fmt(primary_score)}")
    print(
        f"best_null={best_null['mode']} alpha={best_null['alpha']} "
        f"score_delta={fmt(best_null_score - primary_score)}"
    )
    print(f"primary_alpha_null_passes={','.join(row['mode'] for row in primary_alpha_null_passes) or 'none'}")
    print(f"sweep_null_pass_count={len(sweep_null_passes)}")
    print(f"wrote {args.summary_csv}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
