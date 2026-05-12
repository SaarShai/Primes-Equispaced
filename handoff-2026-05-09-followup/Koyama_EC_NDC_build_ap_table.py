#!/usr/bin/env python3
"""
Build a complete a_p table for the EC-NDC residual audit.

Curves:
  37a1  : y^2 + y = x^3 - x
  11a1  : y^2 + y = x^3 - x^2 - 10x - 20
  389a1 : y^2 + y = x^3 + x^2 - 2x

For odd p, use the discriminant-in-y formula

  #E(F_p) = p + 1 + sum_x chi(D(x)),
  a_p     = -sum_x chi(D(x)).

This also recovers the multiplicative bad-prime local coefficient for the
three curves; the first 100 primes are checked against the earlier table.
"""

from __future__ import annotations

import argparse
import csv
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = SCRIPT_DIR / "Koyama_EC_NDC_ap_table_100000.csv"
DEFAULT_VERIFY = SCRIPT_DIR / "Koyama_EC_NDC_ap_table.csv"


@dataclass(frozen=True)
class Curve:
    label: str
    ainvs: Sequence[int]
    conductor: int


CURVES = (
    Curve("37a1", (0, 0, 1, -1, 0), 37),
    Curve("11a1", (0, -1, 1, -10, -20), 11),
    Curve("389a1", (0, 1, 1, -2, 0), 389),
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build EC a_p table.")
    parser.add_argument("--max-k", type=int, default=100000)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--verify-prefix",
        type=Path,
        default=DEFAULT_VERIFY,
        help="Existing short table used to verify the generated prefix.",
    )
    parser.add_argument("--no-verify", action="store_true")
    return parser.parse_args(argv)


def sieve_primes(n: int) -> List[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    limit = int(n**0.5)
    for p in range(2, limit + 1):
        if sieve[p]:
            start = p * p
            sieve[start : n + 1 : p] = b"\x00" * len(range(start, n + 1, p))
    return [i for i in range(2, n + 1) if sieve[i]]


def ap_for_prime(curve: Curve, p: int) -> int:
    a1, a2, a3, a4, a6 = curve.ainvs
    if p == 2:
        affine = 0
        for x in range(p):
            rhs = (x**3 + a2 * x * x + a4 * x + a6) % p
            for y in range(p):
                lhs = (y * y + a1 * x * y + a3 * y) % p
                if lhs == rhs:
                    affine += 1
        return p + 1 - (affine + 1)

    xs = np.arange(p, dtype=np.int64)
    rhs = (xs * xs % p * xs + a2 * xs * xs + a4 * xs + a6) % p
    disc = ((a1 * xs + a3) ** 2 + 4 * rhs) % p

    chi = np.full(p, -1, dtype=np.int8)
    residues = (xs * xs) % p
    chi[residues] = 1
    chi[0] = 0
    return -int(chi[disc].sum())


def load_prefix(path: Path) -> Dict[int, Dict[str, int]]:
    out: Dict[int, Dict[str, int]] = {}
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            p = int(row["p"])
            out[p] = {curve.label: int(row[f"a_p({curve.label})"]) for curve in CURVES}
    return out


def reduction_label(curve: Curve, p: int) -> str:
    return "bad" if curve.conductor % p == 0 else "good"


def write_table(path: Path, primes: Iterable[int], ap: Dict[str, Dict[int, int]]) -> None:
    fields = (
        ["p"]
        + [f"a_p({curve.label})" for curve in CURVES]
        + [f"reduction({curve.label})" for curve in CURVES]
    )
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(fields)
        for p in primes:
            writer.writerow(
                [p]
                + [ap[curve.label][p] for curve in CURVES]
                + [reduction_label(curve, p) for curve in CURVES]
            )


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    primes = sieve_primes(args.max_k)
    ap: Dict[str, Dict[int, int]] = {curve.label: {} for curve in CURVES}

    t0 = time.time()
    for curve in CURVES:
        curve_start = time.time()
        for i, p in enumerate(primes, 1):
            ap[curve.label][p] = ap_for_prime(curve, p)
            if i % 2000 == 0:
                print(
                    f"{curve.label}: {i}/{len(primes)} primes, p={p}, "
                    f"{time.time() - curve_start:.1f}s",
                    flush=True,
                )
        print(
            f"{curve.label}: completed {len(primes)} primes in "
            f"{time.time() - curve_start:.1f}s",
            flush=True,
        )

    if not args.no_verify:
        prefix = load_prefix(args.verify_prefix)
        for p, expected in prefix.items():
            got = {curve.label: ap[curve.label][p] for curve in CURVES}
            if got != expected:
                raise SystemExit(f"prefix mismatch at p={p}: got {got}, expected {expected}")
        print(f"verified prefix against {args.verify_prefix} ({len(prefix)} primes)")

    write_table(args.out, primes, ap)
    print(
        f"wrote {args.out} with {len(primes)} primes; "
        f"largest prime {primes[-1] if primes else 'none'}; "
        f"wall {time.time() - t0:.1f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
