#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

N = 500_000
GAMMA1 = 14.13472514
PHI1_APPROX = -1.6933


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def check(condition: bool, message: str) -> None:
    status = "PASS" if condition else "WARN"
    print(f"[{status}] {message}")


def linear_sieve_mu(n: int) -> tuple[np.ndarray, np.ndarray]:
    mu = np.zeros(n + 1, dtype=np.int8)
    mu[1] = 1
    is_composite = np.zeros(n + 1, dtype=np.bool_)
    primes: list[int] = []
    append_prime = primes.append

    for i in range(2, n + 1):
        if not is_composite[i]:
            append_prime(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > n:
                break
            is_composite[ip] = True
            if i % p == 0:
                mu[ip] = 0
                break
            mu[ip] = -mu[i]

    return np.asarray(primes, dtype=np.int32), mu


def build_prime_race_counts(n: int, primes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    prime_mask = np.zeros(n + 1, dtype=np.bool_)
    prime_mask[primes] = True

    x = np.arange(n + 1, dtype=np.int32)
    mod4 = x & 3

    mask_1 = prime_mask & (mod4 == 1)
    mask_3 = prime_mask & (mod4 == 3)

    pi4_1 = np.cumsum(mask_1, dtype=np.int32)
    pi4_3 = np.cumsum(mask_3, dtype=np.int32)
    return pi4_1, pi4_3


def pearson_corr(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    a = a - a.mean()
    b = b - b.mean()
    denom = np.sqrt(np.dot(a, a) * np.dot(b, b))
    if denom == 0.0:
        return float("nan")
    return float(np.dot(a, b) / denom)


def dominant_zero_bias_probability(phi1: float, projection: str = "sine") -> float:
    """
    Approximate/configurable phase-only proxy; this is not a theorem.
    """
    if projection == "sine":
        value = 0.5 * (1.0 + np.sin(-phi1))
    elif projection == "cosine":
        value = 0.5 * (1.0 + np.cos(phi1))
    else:
        raise ValueError(f"unknown projection: {projection}")
    return float(np.clip(value, 0.0, 1.0))


def main() -> None:
    print_section("SIEVE MU AND MERTENS FUNCTION")
    primes, mu = linear_sieve_mu(N)
    M = np.cumsum(mu, dtype=np.int32)
    m_at_primes = M[primes]

    print(f"N = {N:,}")
    print(f"Number of primes up to N: {len(primes):,}")
    print(f"mu(1) = {int(mu[1])}")
    print(f"mu(2) = {int(mu[2])}")
    print(f"M(1) = {int(M[1])}")
    print(f"M(2) = {int(M[2])}")
    print(f"M({N:,}) = {int(M[N])}")
    check(int(mu[1]) == 1, "mu(1) = 1")
    check(int(M[1]) == 1, "M(1) = 1")
    check(int(M[2]) == 0, "M(2) = 0")

    print_section("MERTENS BIAS AT PRIMES")
    negative_fraction = float(np.mean(m_at_primes < 0))
    zero_fraction = float(np.mean(m_at_primes == 0))
    positive_fraction = float(np.mean(m_at_primes > 0))

    m_neg = int(np.count_nonzero(m_at_primes < 0))
    m_zero = int(np.count_nonzero(m_at_primes == 0))
    m_pos = int(np.count_nonzero(m_at_primes > 0))

    print(f"Fraction of primes with M(p) < 0: {negative_fraction:.6f}")
    print(f"Fraction of primes with M(p) = 0: {zero_fraction:.6f}")
    print(f"Fraction of primes with M(p) > 0: {positive_fraction:.6f}")
    print(f"Counts: negative={m_neg:,}, zero={m_zero:,}, positive={m_pos:,}")
    check(negative_fraction > 0.5, "M(p) is negative for most primes in this range")

    print_section("CHEBYSHEV / PRIME-RACE COUNTS")
    pi4_1_all, pi4_3_all = build_prime_race_counts(N, primes)
    diff_all = pi4_3_all - pi4_1_all
    diff_at_primes = diff_all[primes]

    fraction_race_positive_all = float(np.mean(diff_all[2:] > 0))
    fraction_race_positive_primes = float(np.mean(diff_at_primes > 0))

    print(
        f"Fraction of integers x in [2, N] with pi(x;4,3) > pi(x;4,1): "
        f"{fraction_race_positive_all:.6f}"
    )
    print(
        f"Fraction of primes p <= N with pi(p;4,3) > pi(p;4,1): "
        f"{fraction_race_positive_primes:.6f}"
    )
    check(fraction_race_positive_all > 0.5, "Chebyshev bias holds on most x in this sample")

    print_section("SIGN CORRELATION")
    m_sign = np.sign(m_at_primes).astype(np.int8)
    race_sign = np.sign(diff_at_primes).astype(np.int8)

    pearson_r = pearson_corr(m_sign, race_sign)
    same_sign_rate = float(np.mean(m_sign == race_sign))

    nonzero_mask = (m_sign != 0) & (race_sign != 0)
    if np.any(nonzero_mask):
        pearson_r_nonzero = pearson_corr(m_sign[nonzero_mask], race_sign[nonzero_mask])
        same_sign_rate_nonzero = float(np.mean(m_sign[nonzero_mask] == race_sign[nonzero_mask]))
    else:
        pearson_r_nonzero = float("nan")
        same_sign_rate_nonzero = float("nan")

    m_sign_neg = int(np.count_nonzero(m_sign < 0))
    m_sign_zero = int(np.count_nonzero(m_sign == 0))
    m_sign_pos = int(np.count_nonzero(m_sign > 0))
    race_sign_neg = int(np.count_nonzero(race_sign < 0))
    race_sign_zero = int(np.count_nonzero(race_sign == 0))
    race_sign_pos = int(np.count_nonzero(race_sign > 0))

    print(f"Pearson r(sign M(p), sign(pi(p;4,3)-pi(p;4,1))) = {pearson_r:.6f}")
    print(f"Sign agreement rate (including zeros) = {same_sign_rate:.6f}")
    print(f"Pearson r on nonzero sign points = {pearson_r_nonzero:.6f}")
    print(f"Sign agreement rate on nonzero sign points = {same_sign_rate_nonzero:.6f}")
    print(
        f"sign(M(p)) counts: negative={m_sign_neg:,}, zero={m_sign_zero:,}, positive={m_sign_pos:,}"
    )
    print(
        f"sign(race gap) counts: negative={race_sign_neg:,}, zero={race_sign_zero:,}, positive={race_sign_pos:,}"
    )

    if np.isfinite(pearson_r):
        if abs(pearson_r) >= 0.5:
            print(
                "Interpretation: strong association in this sample; consistent with a shared "
                "low-lying-zero driver, not proof."
            )
        elif abs(pearson_r) >= 0.2:
            print(
                "Interpretation: moderate association in this sample; a shared-zero explanation "
                "is plausible but not established."
            )
        else:
            print(
                "Interpretation: weak association in this sample; a shared-zero explanation is "
                "not supported by sign correlation alone."
            )

    print_section("EXTREME NEGATIVE MERTENS VALUES AT PRIMES")
    selected_mask = m_at_primes <= -3
    selected = m_at_primes[selected_mask]

    if selected.size == 0:
        print("No primes with M(p) <= -3 were found.")
    else:
        prev_min = np.empty_like(m_at_primes)
        prev_min[0] = np.iinfo(np.int32).max
        prev_min[1:] = np.minimum.accumulate(m_at_primes[:-1])

        new_min_flags = m_at_primes < prev_min
        selected_new_min = selected_mask & new_min_flags

        selected_count = int(selected.size)
        new_min_count = int(np.count_nonzero(selected_new_min))
        frac_new_min = new_min_count / selected_count

        print(f"Primes with M(p) <= -3: {selected_count:,}")
        print(f"Among them, new record lows in M(p): {new_min_count:,} ({frac_new_min:.6f})")
        print(f"Selected M(p) range: [{int(selected.min())}, {int(selected.max())}]")

        values, counts = np.unique(selected, return_counts=True)
        print("Exact histogram data for selected primes (value -> count):")
        for v, c in zip(values, counts):
            print(f"  {int(v):>4d} -> {int(c):,}")

        hist_path = Path("mertens_prime_histogram.png")
        bins = np.arange(int(selected.min()) - 0.5, int(selected.max()) + 1.5, 1.0)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(selected, bins=bins, color="steelblue", edgecolor="black", alpha=0.85)
        ax.set_title("Histogram of M(p) for primes p with M(p) <= -3")
        ax.set_xlabel("M(p)")
        ax.set_ylabel("Count of primes")
        ax.grid(True, alpha=0.25)

        if len(values) <= 20:
            ax.set_xticks(values)

        fig.tight_layout()
        fig.savefig(hist_path, dpi=160)
        plt.close(fig)
        print(f"Histogram saved to: {hist_path.resolve()}")

    print_section("DOMINANT-ZERO HEURISTIC")
    bias_proxy = dominant_zero_bias_probability(PHI1_APPROX, projection="sine")

    print(f"Dominant zero reference: rho1 = 1/2 + i*{GAMMA1:.8f}...")
    print(f"Approximate phase parameter: phi1 = {PHI1_APPROX:.4f} (approx/configurable)")
    print("Heuristic formula used: bias_proxy = 0.5 * (1 + sin(-phi1))")
    print("Note: this is a phase-only proxy, not a proved bias theorem.")
    print(f"Heuristic dominant-zero bias proxy: {bias_proxy:.6f}")
    print(f"Empirical Mertens bias P(M(p) < 0): {negative_fraction:.6f}")
    print(f"Proxy minus empirical Mertens bias: {bias_proxy - negative_fraction:+.6f}")
    print(f"Proxy minus empirical Chebyshev bias on all x: {bias_proxy - fraction_race_positive_all:+.6f}")

    print_section("SANITY CHECK SUMMARY")
    check(int(M[1]) == 1 and int(M[2]) == 0, "M(1)=1 and M(2)=0")
    check(negative_fraction > 0.5, "Known Mertens bias: M(p) < 0 for most primes in this range")
    check(
        fraction_race_positive_all > 0.5,
        "Known Chebyshev bias: pi(x;4,3) > pi(x;4,1) for most x in this range",
    )
    print("Done.")


if __name__ == "__main__":
    main()
