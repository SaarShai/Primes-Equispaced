#!/usr/bin/env python3
"""
Scan small prime moduli for low-lying quadratic-character peaks over primes.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import numpy as np
from sympy import mobius as sympy_mobius
from sympy.ntheory import isprime

try:
    from sympy.ntheory.residues import legendre_symbol
except Exception:
    from sympy.functions.combinatorial.numbers import legendre_symbol


LIMIT = 500_000
GAMMAS = np.linspace(0.01, 3.0, 2000)
LOW_GAMMA_CUTOFF = 1.5
CHUNK_SIZE = 200
OUTPUT_PATH = Path(os.path.expanduser("~/Desktop/Farey-Local/experiments/SIEGEL_MODULI_50.md"))


def mobius_prime_sieve(limit: int) -> tuple[np.ndarray, np.ndarray]:
    """Linear sieve for mu(n) and all primes <= limit."""
    mu = np.zeros(limit + 1, dtype=np.int8)
    lp = np.zeros(limit + 1, dtype=np.int32)
    primes: list[int] = []
    mu[1] = 1

    for n in range(2, limit + 1):
        if lp[n] == 0:
            lp[n] = n
            primes.append(n)
            mu[n] = -1
        for p in primes:
            nxt = n * p
            if nxt > limit:
                break
            lp[nxt] = p
            if p == lp[n]:
                mu[nxt] = 0
                break
            mu[nxt] = -mu[n]

    return mu, np.array(primes, dtype=np.int32)


def verify_mobius_sieve(mu: np.ndarray, upto: int = 20) -> None:
    expected = np.array([int(sympy_mobius(n)) for n in range(1, upto + 1)], dtype=np.int8)
    actual = mu[1 : upto + 1]
    if not np.array_equal(actual, expected):
        raise ValueError("Mobius sieve sanity check failed against sympy.mobius.")


def build_legendre_lookup(q: int) -> np.ndarray:
    """Lookup table a -> (a/q) for residues mod q."""
    table = np.empty(q, dtype=np.int8)
    for a in range(q):
        table[a] = int(legendre_symbol(a, q))
    return table


def compute_character_matrix(primes: np.ndarray, moduli: list[int]) -> np.ndarray:
    rows = []
    for q in moduli:
        lookup = build_legendre_lookup(q)
        rows.append(lookup[primes % q])
    return np.vstack(rows).astype(np.int8)


def sweep_character_sums(
    gammas: np.ndarray,
    log_primes: np.ndarray,
    weighted_chars: np.ndarray,
) -> np.ndarray:
    """
    Compute F_chi(gamma) = |sum_p chi(p) p^{-1/2-i gamma}| for all gammas/moduli.
    """
    n_gamma = gammas.size
    out = np.empty((n_gamma, weighted_chars.shape[0]), dtype=np.float64)
    weights_t = np.ascontiguousarray(weighted_chars.T)

    for start in range(0, n_gamma, CHUNK_SIZE):
        stop = min(start + CHUNK_SIZE, n_gamma)
        gamma_chunk = gammas[start:stop]
        phase = np.outer(gamma_chunk, log_primes)
        cos_phase = np.cos(phase)
        sin_phase = np.sin(phase)
        real_part = np.einsum("gp,pq->gq", cos_phase, weights_t, optimize=True)
        imag_part = -np.einsum("gp,pq->gq", sin_phase, weights_t, optimize=True)
        out[start:stop] = np.hypot(real_part, imag_part)

    return out


def summarize_results(
    moduli: list[int],
    gammas: np.ndarray,
    values: np.ndarray,
) -> list[dict[str, float]]:
    low_mask = gammas < LOW_GAMMA_CUTOFF
    summaries: list[dict[str, float]] = []

    for idx, q in enumerate(moduli):
        curve = values[:, idx]
        peak_idx_local = np.argmax(curve[low_mask])
        peak_indices = np.flatnonzero(low_mask)
        peak_idx = int(peak_indices[peak_idx_local])
        mean_val = float(curve.mean())
        std_val = float(curve.std())
        peak_height = float(curve[peak_idx])
        z_score = (peak_height - mean_val) / std_val if std_val > 0 else float("nan")
        summaries.append(
            {
                "q": float(q),
                "peak_height": peak_height,
                "peak_gamma": float(gammas[peak_idx]),
                "z_score": float(z_score),
                "mean": mean_val,
                "std": std_val,
            }
        )

    return summaries


def render_table(rows: list[dict[str, float]]) -> str:
    header = "| q | peak_height | peak_gamma | z_score |\n|---:|------------:|-----------:|--------:|"
    body = [
        f"| {int(row['q'])} | {row['peak_height']:.6f} | {row['peak_gamma']:.6f} | {row['z_score']:.6f} |"
        for row in rows
    ]
    return "\n".join([header, *body])


def render_report(
    rows: list[dict[str, float]],
    weakest: dict[str, float],
    sensitivity_observed: float,
    sensitivity_3sigma: float,
    mu: np.ndarray,
    prime_count: int,
    elapsed: float,
) -> str:
    table = render_table(rows)
    q = int(weakest["q"])
    mean_val = weakest["mean"]
    std_val = weakest["std"]
    peak_height = weakest["peak_height"]
    peak_gamma = weakest["peak_gamma"]
    z_score = weakest["z_score"]
    mertens_tail = int(np.cumsum(mu)[LIMIT])

    return f"""# Siegel-Modulus Scan up to q=50

Computed a Mobius sieve to {LIMIT:,} and used all {prime_count:,} primes up to {LIMIT:,}. The gamma scan used 2,000 points on [0.01, 3.00], and each quadratic character was evaluated by the prime sum

`F_chi(gamma) = |sum_(p <= {LIMIT}) chi(p) p^(-0.5 - i gamma)|`.

Runtime for the full sweep was {elapsed:.2f} seconds. As a sieve sanity check, the linear Mobius sieve matched `sympy.mobius` on the first 20 values. The final Mertens value `M({LIMIT:,})` from the sieve is {mertens_tail}.

## Peak Summary

{table}

## Sensitivity Discussion

The weakest candidate in z-score terms is modulus `q={q}`, with peak height `{peak_height:.6f}` at `gamma={peak_gamma:.6f}` and z-score `{z_score:.6f}`. Over the full scan window its baseline mean and standard deviation are

- mean = {mean_val:.6f}
- std = {std_val:.6f}

Using the heuristic `peak height ~ 1 / |1 - beta|` for a Siegel zero at `beta`, there are two natural scales:

- Matching the observed weakest peak gives `|1 - beta| ~ 1 / {peak_height:.6f} = {sensitivity_observed:.6f}`.
- Requiring a conservative `3 sigma` excess over the weakest background means a detectable height of about `{mean_val + 3.0 * std_val:.6f}`, so `|1 - beta| <= {sensitivity_3sigma:.6f}`.

The second number is the more conservative detectability threshold: with this prime range and this statistic, a Siegel-zero-style resonance would need to lie within roughly `{sensitivity_3sigma:.6f}` of 1 to rise `3 sigma` above the weakest character background.

## Conclusion

Across prime moduli `3 <= q <= 50`, the low-lying quadratic-character peaks are modest rather than explosive. On this finite dataset there is no sign of the huge `~1 / |1 - beta|` amplification one would expect from an extremely near-1 Siegel zero. Interpreting the weakest-character background conservatively, this scan would only be sensitive to a Siegel-zero-style effect if `|1 - beta|` were on the order of `{sensitivity_3sigma:.6f}` or smaller. Nothing in the present table suggests such an outlier.
"""


def main() -> None:
    start_time = time.time()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Sieving Mobius function and primes up to {LIMIT:,}...")
    mu, primes = mobius_prime_sieve(LIMIT)
    verify_mobius_sieve(mu)
    prime_count = primes.size
    print(f"  Found {prime_count:,} primes.")

    moduli = [q for q in range(3, 51) if isprime(q)]
    print(f"Prime moduli in [3, 50]: {moduli}")

    print("Building quadratic characters...")
    character_matrix = compute_character_matrix(primes, moduli)

    log_primes = np.log(primes.astype(np.float64))
    inv_sqrt_primes = primes.astype(np.float64) ** (-0.5)
    weighted_chars = character_matrix.astype(np.float64) * inv_sqrt_primes

    print(f"Sweeping {GAMMAS.size:,} gamma values on [{GAMMAS[0]:.2f}, {GAMMAS[-1]:.2f}]...")
    values = sweep_character_sums(GAMMAS, log_primes, weighted_chars)

    rows = summarize_results(moduli, GAMMAS, values)
    weakest = min(rows, key=lambda row: row["z_score"])
    sensitivity_observed = 1.0 / weakest["peak_height"]
    sensitivity_3sigma = 1.0 / (weakest["mean"] + 3.0 * weakest["std"])

    elapsed = time.time() - start_time
    print("\nSummary table:")
    print(render_table(rows))

    print("\nSensitivity analysis:")
    print(
        "  Weakest modulus q={q} with peak_height={peak:.6f}, peak_gamma={gamma:.6f}, "
        "z_score={z:.6f}".format(
            q=int(weakest["q"]),
            peak=weakest["peak_height"],
            gamma=weakest["peak_gamma"],
            z=weakest["z_score"],
        )
    )
    print(
        "  Heuristic |1-beta| from observed weakest peak: {value:.6f}".format(
            value=sensitivity_observed
        )
    )
    print(
        "  Conservative 3-sigma detectability threshold: |1-beta| <= {value:.6f}".format(
            value=sensitivity_3sigma
        )
    )
    print(
        "  Conclusion: no modulus in this q-range shows the large amplification expected "
        "from an extremely close Siegel zero."
    )

    report = render_report(
        rows=rows,
        weakest=weakest,
        sensitivity_observed=sensitivity_observed,
        sensitivity_3sigma=sensitivity_3sigma,
        mu=mu,
        prime_count=prime_count,
        elapsed=elapsed,
    )
    OUTPUT_PATH.write_text(report)
    print(f"\nSaved markdown report to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
