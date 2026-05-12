#!/usr/bin/env python3
"""Construct a signed log-Gaussian kernel with prescribed Mellin zeros.

In log variables t = exp(x),

    W_hat(z) = int_0^infty W(t) t^(z-1) dt
             = int_R Phi(x) exp(z x) dx,  Phi(x)=W(exp(x)).

This diagnostic chooses real coefficients c_j and centers a_j for
Phi(x)=sum_j c_j exp(-(x-a_j)^2/(2 sigma^2)), imposing

    W_hat(0)=1,  W_hat(i gamma_k)=0.

It is a signed Schwartz-kernel diagnostic, not a positivity or compact-support
theorem.
"""

from __future__ import annotations

import argparse
import cmath
import math
from typing import Iterable, List


def gaussian_mellin(z: complex, center: float, sigma: float) -> complex:
    return math.sqrt(2.0 * math.pi) * sigma * cmath.exp(z * center + 0.5 * sigma * sigma * z * z)


def solve_linear(a: List[List[float]], b: List[float]) -> List[float]:
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-14:
            raise ValueError("singular moment system; adjust centers or sigma")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [x / div for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor:
                aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    return [aug[i][-1] for i in range(n)]


def make_centers(n: int, width: float) -> List[float]:
    if n == 1:
        return [0.0]
    return [-width + 2.0 * width * j / (n - 1) for j in range(n)]


def build_system(gammas: Iterable[float], centers: List[float], sigma: float):
    rows: List[List[float]] = []
    rhs: List[float] = []

    rows.append([gaussian_mellin(0.0, c, sigma).real for c in centers])
    rhs.append(1.0)

    for gamma in gammas:
        vals = [gaussian_mellin(1j * gamma, c, sigma) for c in centers]
        rows.append([v.real for v in vals])
        rhs.append(0.0)
        rows.append([v.imag for v in vals])
        rhs.append(0.0)

    return rows, rhs


def moment(z: complex, coeffs: List[float], centers: List[float], sigma: float) -> complex:
    return sum(c * gaussian_mellin(z, a, sigma) for c, a in zip(coeffs, centers))


def parse_gammas(text: str) -> List[float]:
    out = []
    for part in text.replace(";", ",").split(","):
        part = part.strip()
        if part:
            out.append(float(part))
    if not out:
        raise ValueError("provide at least one gamma")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gammas", default="1.5,3.25,5.75", help="comma-separated positive ordinates")
    parser.add_argument("--sigma", type=float, default=0.35, help="log-Gaussian width")
    parser.add_argument("--width", type=float, default=2.0, help="center range [-width,width]")
    args = parser.parse_args()

    gammas = parse_gammas(args.gammas)
    n = 1 + 2 * len(gammas)
    centers = make_centers(n, args.width)
    rows, rhs = build_system(gammas, centers, args.sigma)
    coeffs = solve_linear(rows, rhs)

    print("# signed log-Gaussian Mellin filter")
    print(f"gammas={gammas}")
    print(f"sigma={args.sigma}")
    print(f"centers={centers}")
    print(f"coefficients={coeffs}")
    print(f"W_hat(0)={moment(0.0, coeffs, centers, args.sigma):.16g}")
    for gamma in gammas:
        val = moment(1j * gamma, coeffs, centers, args.sigma)
        print(f"W_hat(i*{gamma})={val.real:.3e}{val.imag:+.3e}j abs={abs(val):.3e}")
    l1_proxy = sum(abs(c) * gaussian_mellin(0.0, a, args.sigma).real for c, a in zip(coeffs, centers))
    print(f"signed_L1_log_proxy={l1_proxy:.12g}")
    print("note=diagnostic signed Schwartz kernel; not positive and not compactly supported")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
