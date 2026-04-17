#!/usr/bin/env python3
from __future__ import annotations

import math
from mpmath import mp
import numpy as np

mp.dps = 15

N = 50000
TABLE_LIMIT = N + 1  # needed for mu(n+1) in the shifted Möbius product
GRID_START = 1.0
GRID_STOP = 50.0
GRID_STEP = 0.1
MATCH_TOL = 0.3

KNOWN_ZETA_ZEROS = [
    14.134,
    21.022,
    25.011,
    30.425,
    32.935,
    37.586,
    40.919,
    43.327,
]

KNOWN_L_ZEROS = [
    6.021,
    10.244,
    12.589,
    16.311,
]


def build_spf(limit: int) -> np.ndarray:
    spf = np.arange(limit + 1, dtype=np.int32)
    spf[0] = 0
    spf[1] = 1
    root = math.isqrt(limit)
    for p in range(2, root + 1):
        if spf[p] == p:
            start = p * p
            for m in range(start, limit + 1, p):
                if spf[m] == m:
                    spf[m] = p
    return spf


def build_number_theory_tables(limit: int):
    spf = build_spf(limit)

    mu = np.zeros(limit + 1, dtype=np.int8)
    omega = np.zeros(limit + 1, dtype=np.int16)
    divisor = np.zeros(limit + 1, dtype=np.int32)
    mangoldt = np.zeros(limit + 1, dtype=np.float64)

    mu[1] = 1
    omega[1] = 0
    divisor[1] = 1
    mangoldt[1] = 0.0

    for n in range(2, limit + 1):
        p = int(spf[n])
        m = n // p
        exp = 1
        while m % p == 0:
            m //= p
            exp += 1

        mu[n] = 0 if exp > 1 else -mu[m]
        omega[n] = omega[m] + exp
        divisor[n] = divisor[m] * (exp + 1)
        if m == 1:
            mangoldt[n] = math.log(p)

    return spf, mu, omega, divisor, mangoldt


def prepare_kernel(n_max: int):
    n = np.arange(1, n_max + 1, dtype=np.float64)
    logn = np.log(n)

    gamma_grid = np.linspace(GRID_START, GRID_STOP, int(round((GRID_STOP - GRID_START) / GRID_STEP)) + 1, dtype=np.float64)
    gamma_step = float(gamma_grid[1] - gamma_grid[0])

    base_phase = np.exp(-1j * gamma_grid[0] * logn)
    step_phase = np.exp(-1j * gamma_step * logn)

    return n, logn, gamma_grid, base_phase, step_phase


def spectroscope(weights: np.ndarray, gamma_grid: np.ndarray, base_phase: np.ndarray, step_phase: np.ndarray):
    weights = np.asarray(weights, dtype=np.float64)
    if weights.shape[0] != base_phase.shape[0]:
        raise ValueError("weights and kernel length mismatch")

    phase = weights * base_phase
    values = np.empty(gamma_grid.shape[0], dtype=np.float64)

    for idx, gamma in enumerate(gamma_grid):
        total = phase.sum(dtype=np.complex128)
        values[idx] = (gamma * gamma) * (total.real * total.real + total.imag * total.imag)
        phase *= step_phase

    mean = float(values.mean())
    std = float(values.std())
    if std == 0.0:
        zscores = np.zeros_like(values)
    else:
        zscores = (values - mean) / std

    return values, zscores


def match_labels(gamma: float):
    gamma = round(float(gamma), 10)
    labels = []

    for z in KNOWN_ZETA_ZEROS:
        if abs(gamma - z) <= MATCH_TOL:
            labels.append(f"zeta {z:.3f}")

    for z in KNOWN_L_ZEROS:
        if abs(gamma - z) <= MATCH_TOL:
            labels.append(f"L(chi_-1) {z:.3f}")

    return labels


def collect_unique_matches(top_indices: np.ndarray, gamma_grid: np.ndarray):
    seen = {}
    for idx in top_indices:
        gamma = float(gamma_grid[idx])
        for label in match_labels(gamma):
            seen.setdefault(label, None)
    return list(seen.keys())


def build_top3_summary(top3_indices: np.ndarray, gamma_grid: np.ndarray, zscores: np.ndarray) -> str:
    parts = []
    for idx in top3_indices:
        gamma = float(gamma_grid[idx])
        z = float(zscores[idx])
        labels = match_labels(gamma)
        if labels:
            parts.append(f"{gamma:.1f} (z={z:.3f}; {', '.join(labels)})")
        else:
            parts.append(f"{gamma:.1f} (z={z:.3f})")
    return " | ".join(parts)


def infer_verdict(expected_kind: str, matched_labels: list[str]) -> str:
    has_zeta = any(label.startswith("zeta ") for label in matched_labels)
    has_l = any(label.startswith("L(chi_-1) ") for label in matched_labels)

    if expected_kind == "noise":
        return "NOISE" if not matched_labels else "UNKNOWN"

    if expected_kind == "l":
        return "DETECTS_L" if has_l and not has_zeta else "UNKNOWN"

    if expected_kind == "zeta":
        return "DETECTS_ZETA" if has_zeta and not has_l else "UNKNOWN"

    if has_l and not has_zeta:
        return "DETECTS_L"
    if has_zeta and not has_l:
        return "DETECTS_ZETA"
    if not has_zeta and not has_l:
        return "UNKNOWN"
    return "UNKNOWN"


def print_peaks(label: str, top5_indices: np.ndarray, gamma_grid: np.ndarray, zscores: np.ndarray):
    print("  Top 5 peaks by z-score:", flush=True)
    for rank, idx in enumerate(top5_indices, start=1):
        gamma = float(gamma_grid[idx])
        z = float(zscores[idx])
        labels = match_labels(gamma)
        match_text = ", ".join(labels) if labels else "-"
        print(
            f"    {rank}. gamma={gamma:5.1f}  z={z:8.3f}  matches={match_text}",
            flush=True,
        )


def print_summary_table(rows):
    headers = [
        "Function",
        "Top 3 peaks (gamma / z / matches)",
        "Matched known zeros",
        "Verdict",
    ]
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    print()
    print("=" * (sum(widths) + 3 * (len(widths) - 1)))
    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt(row))
    print("=" * (sum(widths) + 3 * (len(widths) - 1)))


def process_function(label: str, weights: np.ndarray, expected_kind: str, gamma_grid: np.ndarray, base_phase: np.ndarray, step_phase: np.ndarray):
    values, zscores = spectroscope(weights, gamma_grid, base_phase, step_phase)
    top5_indices = np.argsort(zscores)[::-1][:5]
    top3_indices = top5_indices[:3]
    matched_labels = collect_unique_matches(top5_indices, gamma_grid)
    verdict = infer_verdict(expected_kind, matched_labels)

    print_peaks(label, top5_indices, gamma_grid, zscores)
    print(f"  Verdict: {verdict}", flush=True)

    top3_summary = build_top3_summary(top3_indices, gamma_grid, zscores)
    matched_summary = ", ".join(matched_labels) if matched_labels else "-"

    return {
        "function": label,
        "top3": top3_summary,
        "matches": matched_summary,
        "verdict": verdict,
    }


def main():
    print("Farey spectroscope conjecture tester", flush=True)

    _, mu, omega, divisor, mangoldt = build_number_theory_tables(TABLE_LIMIT)

    # Sanity checks on the sieves and recursive arithmetic tables.
    assert mu[1] == 1
    assert mu[4] == 0
    assert mu[6] == 1
    assert omega[12] == 3
    assert divisor[12] == 6
    assert abs(mangoldt[4] - math.log(2.0)) < 1e-12

    n, logn, gamma_grid, base_phase, step_phase = prepare_kernel(N)

    mu_slice = mu[1 : N + 1].astype(np.float64)
    omega_slice = omega[1 : N + 1]
    divisor_slice = divisor[1 : N + 1].astype(np.float64)
    mangoldt_slice = mangoldt[1 : N + 1]
    n_inv = 1.0 / n

    liouville = 1.0 - 2.0 * (omega_slice & 1).astype(np.float64)
    alt_sign = 1.0 - 2.0 * (np.arange(1, N + 1, dtype=np.int32) & 1).astype(np.float64)
    mu_shift = (mu[1 : N + 1].astype(np.int16) * mu[2 : N + 2].astype(np.int16)).astype(np.float64)
    squarefree_density = float(6.0 / (mp.pi ** 2))

    function_specs = [
        ("mu(n)", mu_slice * n_inv, "zeta"),
        ("lambda(n)=(-1)^Omega(n)", liouville * n_inv, "zeta"),
        ("mu(n)^2 - 6/pi^2", (mu_slice * mu_slice - squarefree_density) * n_inv, "zeta"),
        ("Lambda(n) - 1", (mangoldt_slice - 1.0) * n_inv, "zeta"),
        ("d(n) - log(n)", (divisor_slice - logn) * n_inv, "zeta"),
        ("(-1)^n * mu(n)", alt_sign * mu_slice * n_inv, "l"),
        ("mu(n) * mu(n+1)", mu_shift * n_inv, "noise"),
    ]

    summary_rows = []
    for idx, (label, weights, expected_kind) in enumerate(function_specs, start=1):
        print(f"\nProcessing {idx}/7: {label}", flush=True)
        result = process_function(label, weights, expected_kind, gamma_grid, base_phase, step_phase)
        summary_rows.append(
            [
                result["function"],
                result["top3"],
                result["matches"],
                result["verdict"],
            ]
        )

    print_summary_table(summary_rows)


if __name__ == "__main__":
    main()
