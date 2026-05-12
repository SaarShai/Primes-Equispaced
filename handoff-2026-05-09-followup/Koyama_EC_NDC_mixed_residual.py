#!/usr/bin/env python3
"""
Koyama EC-NDC mixed residual audit.

Default mode is intentionally conservative: read the existing EC sweep CSV and
the existing a_p table, then compute the mixed residuals only from primes that
are actually present in that table.  The bundled table stops at p=541, so every
current K checkpoint is reported as a truncated residual product.

Conventions:
  good p EC inverse factor: 1 - a_p/p + 1/p, so mu_E(p^2)=p.
  C_mix(K) = (e^gamma log K)^(1/2)
             * prod_good exp(-a_p/p) * (1 - a_p/p + 1/p)^(-1)
  D_mix(K) = D_K^E * zeta(2) / C_mix(K)
  C_2(K)   = (e^gamma log K)^(1/2)
             * exp(sum_good (a_p^2 - 2p)/(2p^2))
  D_2(K)   = D_K^E * zeta(2) / C_2(K)

Bad-prime finite factors are not guessed in the default audit; C_bad(E)=1.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SWEEP = SCRIPT_DIR / "Koyama_EC_NDC.csv"
DEFAULT_AP_TABLE = SCRIPT_DIR / "Koyama_EC_NDC_ap_table.csv"
DEFAULT_REPORT = SCRIPT_DIR / "Koyama_EC_NDC_mixed_residual_2026-05-10.md"
REPORT_DATE = "2026-05-11"

CURVES = ("37a1", "11a1", "389a1")
ZETA2 = math.pi * math.pi / 6.0
EULER_GAMMA = 0.577215664901532860606512090082402431

BEST_PRIOR_CROSS_CURVE_RATIO = 1.42083
BEST_PRIOR_MAX_WITHIN_CV = 0.08567129


@dataclass(frozen=True)
class SweepRow:
    curve: str
    K: int
    c_K: float
    E_K: float
    D_K: float
    D_K_zeta2: float
    scale_label: str
    scale_value: float


@dataclass(frozen=True)
class APRow:
    p: int
    ap: Dict[str, int]
    reduction: Dict[str, str]


@dataclass(frozen=True)
class ResidualRow:
    curve: str
    K: int
    D_K_zeta2: float
    p_product_max: int
    p_table_max: int
    product_complete: bool
    good_prime_count: int
    log_R_mix_good: float
    R_mix_good: float
    C_mix_good: float
    D_mix_good: float
    C_2_good: float
    D_2_good: float


@dataclass(frozen=True)
class MetricRow:
    name: str
    max_within_cv: float
    cross_curve_cv: float
    cross_curve_ratio: float
    score: float
    promoted: bool
    curve_means: Dict[str, float]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute EC-NDC mixed residuals from existing sweep outputs."
    )
    parser.add_argument("--sweep", type=Path, default=DEFAULT_SWEEP)
    parser.add_argument("--ap-table", type=Path, default=DEFAULT_AP_TABLE)
    parser.add_argument("--max-k", type=int, default=100000)
    parser.add_argument("--curves", nargs="+", default=list(CURVES), choices=CURVES)
    parser.add_argument(
        "--write-report",
        type=Path,
        default=None,
        help="Write markdown report to this path. If omitted, print report to stdout.",
    )
    parser.add_argument(
        "--emit-csv",
        action="store_true",
        help="Print residual rows as CSV to stdout instead of markdown.",
    )
    return parser.parse_args(argv)


def read_sweep(path: Path, curves: Iterable[str], max_k: int) -> List[SweepRow]:
    wanted = set(curves)
    rows: List[SweepRow] = []
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            curve = raw["curve"]
            K = int(raw["K"])
            if curve not in wanted or K > max_k:
                continue
            rows.append(
                SweepRow(
                    curve=curve,
                    K=K,
                    c_K=float(raw["c_K"]),
                    E_K=float(raw["E_K"]),
                    D_K=float(raw["D_K"]),
                    D_K_zeta2=float(raw["D_K_times_zeta2"]),
                    scale_label=raw["scale_label"],
                    scale_value=float(raw["scale_value"]),
                )
            )
    rows.sort(key=lambda r: (CURVES.index(r.curve), r.K))
    return rows


def read_ap_table(path: Path) -> List[APRow]:
    rows: List[APRow] = []
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            p = int(raw["p"])
            rows.append(
                APRow(
                    p=p,
                    ap={curve: int(raw[f"a_p({curve})"]) for curve in CURVES},
                    reduction={curve: raw[f"reduction({curve})"] for curve in CURVES},
                )
            )
    rows.sort(key=lambda r: r.p)
    return rows


def primes_upto(n: int) -> List[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : n + 1 : p] = b"\x00" * len(range(start, n + 1, p))
    return [i for i in range(2, n + 1) if sieve[i]]


def table_complete_for_k(table_primes: Set[int], k: int) -> bool:
    return all(p in table_primes for p in primes_upto(k))


def residual_for_row(row: SweepRow, ap_rows: Sequence[APRow]) -> ResidualRow:
    p_table_max = ap_rows[-1].p if ap_rows else 0
    p_product_max = min(row.K, p_table_max)
    table_primes = {ap_row.p for ap_row in ap_rows}
    product_complete = table_complete_for_k(table_primes, row.K)

    log_R_mix = 0.0
    log_C2_tail = 0.0
    good_count = 0
    for ap_row in ap_rows:
        p = ap_row.p
        if p > row.K:
            break
        if ap_row.reduction[row.curve] != "good":
            continue
        ap = ap_row.ap[row.curve]
        inv_local = 1.0 - ap / p + 1.0 / p
        if inv_local <= 0.0:
            raise ValueError(f"non-positive good local factor for {row.curve} p={p}")
        log_R_mix += -ap / p - math.log(inv_local)
        log_C2_tail += (ap * ap - 2.0 * p) / (2.0 * p * p)
        good_count += 1

    mertens_half = 0.5 * (EULER_GAMMA + math.log(math.log(row.K)))
    log_C_mix = mertens_half + log_R_mix
    log_C2 = mertens_half + log_C2_tail

    R_mix = math.exp(log_R_mix)
    C_mix = math.exp(log_C_mix)
    C2 = math.exp(log_C2)
    return ResidualRow(
        curve=row.curve,
        K=row.K,
        D_K_zeta2=row.D_K_zeta2,
        p_product_max=p_product_max,
        p_table_max=p_table_max,
        product_complete=product_complete,
        good_prime_count=good_count,
        log_R_mix_good=log_R_mix,
        R_mix_good=R_mix,
        C_mix_good=C_mix,
        D_mix_good=row.D_K_zeta2 / C_mix,
        C_2_good=C2,
        D_2_good=row.D_K_zeta2 / C2,
    )


def coefficient_of_variation(values: Sequence[float]) -> float:
    if not values:
        return math.nan
    mean = statistics.fmean(values)
    if mean == 0.0:
        return math.inf
    if len(values) == 1:
        return 0.0
    variance = statistics.fmean((x - mean) ** 2 for x in values)
    return math.sqrt(variance) / abs(mean)


def metrics(rows: Sequence[ResidualRow]) -> List[MetricRow]:
    suffix = "" if rows and all(row.product_complete for row in rows) else "_truncated"
    candidates = {
        f"D_mix_good{suffix}": lambda r: r.D_mix_good,
        f"D_2_good{suffix}": lambda r: r.D_2_good,
    }
    out: List[MetricRow] = []
    for name, getter in candidates.items():
        by_curve: Dict[str, List[float]] = {curve: [] for curve in CURVES}
        for row in rows:
            by_curve[row.curve].append(getter(row))

        curve_means = {
            curve: statistics.fmean(vals)
            for curve, vals in by_curve.items()
            if vals
        }
        within_cvs = [
            coefficient_of_variation(vals) for vals in by_curve.values() if vals
        ]
        means = list(curve_means.values())
        cross_curve_cv = coefficient_of_variation(means)
        cross_curve_ratio = max(means) / min(means) if means and min(means) > 0 else math.inf
        max_within_cv = max(within_cvs) if within_cvs else math.nan
        score = max_within_cv + cross_curve_cv
        promoted = (
            cross_curve_ratio < BEST_PRIOR_CROSS_CURVE_RATIO
            and max_within_cv < BEST_PRIOR_MAX_WITHIN_CV
        )
        out.append(
            MetricRow(
                name=name,
                max_within_cv=max_within_cv,
                cross_curve_cv=cross_curve_cv,
                cross_curve_ratio=cross_curve_ratio,
                score=score,
                promoted=promoted,
                curve_means=curve_means,
            )
        )
    out.sort(key=lambda r: (r.promoted is False, r.score))
    return out


def format_float(x: float, digits: int = 10) -> str:
    if math.isnan(x):
        return "nan"
    if math.isinf(x):
        return "inf"
    return f"{x:.{digits}g}"


def csv_output(rows: Sequence[ResidualRow]) -> str:
    fields = [
        "curve",
        "K",
        "D_K_zeta2",
        "p_product_max",
        "p_table_max",
        "product_complete",
        "good_prime_count",
        "R_mix_good",
        "C_mix_good",
        "D_mix_good",
        "C_2_good",
        "D_2_good",
    ]
    lines = [",".join(fields)]
    for row in rows:
        lines.append(
            ",".join(
                [
                    row.curve,
                    str(row.K),
                    format_float(row.D_K_zeta2, 16),
                    str(row.p_product_max),
                    str(row.p_table_max),
                    str(row.product_complete),
                    str(row.good_prime_count),
                    format_float(row.R_mix_good, 16),
                    format_float(row.C_mix_good, 16),
                    format_float(row.D_mix_good, 16),
                    format_float(row.C_2_good, 16),
                    format_float(row.D_2_good, 16),
                ]
            )
        )
    return "\n".join(lines) + "\n"


def markdown_report(
    rows: Sequence[ResidualRow],
    metric_rows: Sequence[MetricRow],
    sweep_path: Path,
    ap_table_path: Path,
    elapsed: float,
    max_k: int,
    report_path: Optional[Path] = None,
) -> str:
    complete = all(row.product_complete for row in rows)
    max_table_prime = max((row.p_table_max for row in rows), default=0)
    max_seen_k = max((row.K for row in rows), default=0)
    report_target = report_path if report_path is not None else DEFAULT_REPORT
    promotion = [m for m in metric_rows if m.promoted]
    outcome = "no normalization promoted"
    if promotion:
        outcome = "promotion candidate found: " + ", ".join(m.name for m in promotion)

    lines: List[str] = [
        "# Koyama EC-NDC mixed residual audit",
        "",
        f"Date: {REPORT_DATE}",
        f"Outcome: **{outcome}**.",
        "",
        "## Method",
        "",
        f"- Sweep source: `{sweep_path}`.",
        f"- a_p source: `{ap_table_path}`.",
        f"- Requested max K: `{max_k}`; rows available through K=`{max_seen_k}`.",
        f"- Product table max prime: `{max_table_prime}`.",
        "- Convention: inverse EC local factor with `mu_E(p^2)=p`.",
        "- `C_bad(E)` not guessed; all reported residual products are good-prime only.",
        "- Promotion rule: require cross-curve ratio below `1.42083` and max within-curve CV below `0.08567129`.",
        "",
        "## Limitation",
        "",
    ]
    if complete:
        lines.append("All reported products are complete for their K checkpoints.")
    else:
        lines.append(
            "The existing `a_p` table stops at p=541, so these are **truncated diagnostics**, "
            "not real K=100000 Euler products. No K=300000 product was attempted because the "
            "K=100000 product is not complete from the available table."
        )

    lines.extend(
        [
            "",
            "## Stability",
            "",
            "| normalization | promoted | max within-K CV | cross-curve CV | cross-curve ratio | score | curve means (37a1, 11a1, 389a1) |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in metric_rows:
        means = ", ".join(format_float(row.curve_means.get(curve, math.nan), 8) for curve in CURVES)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.name}`",
                    str(row.promoted),
                    format_float(row.max_within_cv, 8),
                    format_float(row.cross_curve_cv, 8),
                    format_float(row.cross_curve_ratio, 8),
                    format_float(row.score, 8),
                    means,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## K=100000 Rows",
            "",
            "| curve | K | D*zeta(2) | p max | complete | good p count | C_mix | D_mix | C_2 | D_2 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        if row.K != 100000:
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    row.curve,
                    str(row.K),
                    format_float(row.D_K_zeta2, 10),
                    str(row.p_product_max),
                    str(row.product_complete),
                    str(row.good_prime_count),
                    format_float(row.C_mix_good, 10),
                    format_float(row.D_mix_good, 10),
                    format_float(row.C_2_good, 10),
                    format_float(row.D_2_good, 10),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Verification",
            "",
            f"- Command: `python3 {Path(__file__).name} --max-k {max_k} --ap-table {ap_table_path} --write-report {report_target}`.",
            f"- Wall time: `{elapsed:.3f}s`.",
            f"- Rows computed: `{len(rows)}`.",
        ]
    )
    if complete:
        lines.extend(
            [
                "- K=300000 command not run in this report: `python3 Koyama_EC_NDC_mixed_residual.py --max-k 300000 --ap-table <complete-ap-table> --write-report <report.md>`.",
                f"- Reason: source sweep rows are available only through K=`{max_seen_k}`; K=300000 needs recomputing `D_K*zeta(2)` as well as extending the `a_p` table.",
            ]
        )
    else:
        lines.extend(
            [
                "- K=300000 command not run: `python3 Koyama_EC_NDC_mixed_residual.py --max-k 300000 --write-report Koyama_EC_NDC_mixed_residual_2026-05-10.md`.",
                f"- Reason: no complete K={max_k} mixed product from available `a_p` source; K=300000 would be table-truncated to p={max_table_prime}.",
            ]
        )
    lines.extend(
        [
            "",
            "## Residual Rows",
            "",
            "| curve | K | D*zeta(2) | p max | complete | C_mix | D_mix | C_2 | D_2 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.curve,
                    str(row.K),
                    format_float(row.D_K_zeta2, 10),
                    str(row.p_product_max),
                    str(row.product_complete),
                    format_float(row.C_mix_good, 10),
                    format_float(row.D_mix_good, 10),
                    format_float(row.C_2_good, 10),
                    format_float(row.D_2_good, 10),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Confidence",
            "",
        ]
    )
    if complete:
        lines.append(
            "Medium for normalization decisions: formulas were implemented directly from the sprint theory note, "
            "and the residual products are complete for the source sweep checkpoints through K=100000. "
            "High for the negative promotion decision at this checkpoint."
        )
    else:
        lines.append(
            "Low-to-medium for normalization decisions: formulas were implemented directly from the sprint theory note, "
            f"but the product is truncated at p={max_table_prime} for at least one checkpoint. High for the negative "
            "promotion decision on this truncated diagnostic."
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    t0 = time.time()
    sweep_rows = read_sweep(args.sweep, args.curves, args.max_k)
    if not sweep_rows:
        raise SystemExit(f"no sweep rows found in {args.sweep} for max K {args.max_k}")
    ap_rows = read_ap_table(args.ap_table)
    if not ap_rows:
        raise SystemExit(f"no a_p rows found in {args.ap_table}")
    residual_rows = [residual_for_row(row, ap_rows) for row in sweep_rows]
    metric_rows = metrics(residual_rows)
    elapsed = time.time() - t0

    if args.emit_csv:
        sys.stdout.write(csv_output(residual_rows))
        return 0

    report = markdown_report(
        residual_rows,
        metric_rows,
        args.sweep,
        args.ap_table,
        elapsed,
        args.max_k,
        args.write_report,
    )
    if args.write_report:
        args.write_report.write_text(report + "\n")
    else:
        sys.stdout.write(report + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
