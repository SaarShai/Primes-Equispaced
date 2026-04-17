#!/usr/bin/env python3
"""
Check the DRH scaling law for partial Euler products against truncated Mobius sums
at the first three nontrivial zeta zeros.

Requirements satisfied:
- mpmath with mp.dps = 30 for all special-function / complex arithmetic
- Mobius function implemented from scratch with a sieve
- Partial Euler products E_P(rho) over the first 25 primes
- Truncated Mobius sums c_P(rho) = sum_{k=2}^P mu(k) k^{-rho}
- Least-squares fits using numpy
- Formatted tables and a final comparison summary
"""

from mpmath import mp
import numpy as np

mp.dps = 30


def linear_sieve_primes_and_mobius(limit):
    """Return all primes <= limit and mobius values mu[0..limit]."""
    primes = []
    lp = [0] * (limit + 1)  # least prime factor
    mu = [0] * (limit + 1)
    mu[1] = 1

    for n in range(2, limit + 1):
        if lp[n] == 0:
            lp[n] = n
            primes.append(n)
            mu[n] = -1

        for p in primes:
            m = n * p
            if m > limit:
                break
            lp[m] = p
            if n % p == 0:
                mu[m] = 0
                break
            mu[m] = -mu[n]

    return primes, mu


def first_three_gammas():
    """
    Use mpmath's zetazero if available, otherwise fall back to standard constants.
    """
    fallback = [
        mp.mpf("14.134725141734693790457251983562"),
        mp.mpf("21.022039638771554992628479593897"),
        mp.mpf("25.010857580145688763213790992563"),
    ]
    try:
        if hasattr(mp, "zetazero"):
            return [mp.im(mp.zetazero(n)) for n in (1, 2, 3)]
    except Exception:
        pass
    return fallback


def partial_euler_product(primes_upto, rho):
    """E_P(rho) = prod_{p<=P} (1 - p^{-rho})^{-1}."""
    prod = mp.mpc(1)
    for p in primes_upto:
        pp = mp.power(mp.mpf(p), -rho)
        prod *= 1 / (1 - pp)
    return prod


def truncated_mobius_sum(P, rho, mu):
    """c_P(rho) = sum_{k=2}^P mu(k) * k^{-rho}."""
    total = mp.mpc(0)
    for k in range(2, P + 1):
        if mu[k] != 0:
            total += mp.mpf(mu[k]) * mp.power(mp.mpf(k), -rho)
    return total


def fit_line(x, y):
    """
    Fit y = slope * x + intercept by least squares.
    Return slope, intercept, R^2.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    X = np.column_stack([x, np.ones_like(x)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    slope, intercept = beta
    y_hat = X @ beta

    ss_tot = np.sum((y - y.mean()) ** 2)
    ss_res = np.sum((y - y_hat) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else float("nan")
    return float(slope), float(intercept), float(r2)


def fmt_mpf(x, digits=12):
    """Format an mp.mpf/mpc-real/numpy-float value as a compact string."""
    return mp.nstr(mp.mpf(x), n=digits)


def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    print("  ".join(headers[i].rjust(widths[i]) for i in range(len(headers))))
    print("  ".join(("-" * widths[i]) for i in range(len(headers))))
    for row in rows:
        print("  ".join(row[i].rjust(widths[i]) for i in range(len(headers))))


def analyze_zero(index, gamma, prime_bounds, mu):
    rho = mp.mpf("0.5") + mp.j * gamma

    E_abs = []
    c_abs = []
    prod_abs = []
    rows = []

    for i, P in enumerate(prime_bounds):
        E = partial_euler_product(prime_bounds[: i + 1], rho)
        c = truncated_mobius_sum(P, rho, mu)

        e_mag = abs(E)
        c_mag = abs(c)
        prod_mag = e_mag * c_mag

        E_abs.append(e_mag)
        c_abs.append(c_mag)
        prod_abs.append(prod_mag)

        rows.append(
            [
                str(P),
                fmt_mpf(e_mag, 12),
                fmt_mpf(c_mag, 12),
                fmt_mpf(prod_mag, 12),
            ]
        )

    # Fit |c_P(rho_1)| to a*log(P) + b
    x_log = np.array([float(mp.log(mp.mpf(P))) for P in prime_bounds], dtype=float)
    y_c = np.array([float(v) for v in c_abs], dtype=float)
    a, b, _ = fit_line(x_log, y_c)

    # Fit |E_P(rho_1)| to c/log(P) + d, i.e. y = c * (1/log(P)) + d
    x_invlog = np.array([1.0 / float(mp.log(mp.mpf(P))) for P in prime_bounds], dtype=float)
    y_E = np.array([float(v) for v in E_abs], dtype=float)
    c_coef, d_intercept, r2 = fit_line(x_invlog, y_E)

    print("\n" + "=" * 88)
    print(f"Zero rho_{index}: rho = 1/2 + i*gamma_{index}")
    print(f"gamma_{index} = {fmt_mpf(gamma, 20)}")
    print("=" * 88)
    print_table(
        ["P", "|E_P|", "|c_P|", "|E_P||c_P|"],
        rows,
    )

    print("\nFit on this zero:")
    print(f"  |c_P(rho_{index})|  ~=  a * log(P) + b")
    print(f"    a = {a:.12f}")
    print(f"    b = {b:.12f}")
    print(f"  |E_P(rho_{index})|  ~=  c / log(P) + d")
    print(f"    c = {c_coef:.12f}")
    print(f"    d = {d_intercept:.12f}")
    print(f"    R^2 = {r2:.12f}")

    return {
        "index": index,
        "gamma": gamma,
        "a": a,
        "b": b,
        "c": c_coef,
        "d": d_intercept,
        "r2": r2,
        "last_product": float(prod_abs[-1]),
        "mean_product": float(np.mean(np.array([float(v) for v in prod_abs]))),
    }


def main():
    # First 25 primes: 2, 3, 5, ..., 97
    primes, mu = linear_sieve_primes_and_mobius(100)
    prime_bounds = primes[:25]
    assert len(prime_bounds) == 25 and prime_bounds[-1] == 97

    gammas = first_three_gammas()

    results = []
    for i, gamma in enumerate(gammas, start=1):
        results.append(analyze_zero(i, gamma, prime_bounds, mu))

    print("\n" + "=" * 88)
    print("Summary across the first three nontrivial zeros")
    print("=" * 88)

    summary_rows = []
    for res in results:
        summary_rows.append(
            [
                f"rho_{res['index']}",
                fmt_mpf(res["gamma"], 18),
                f"{res['a']:.12f}",
                f"{res['c']:.12f}",
                f"{res['r2']:.12f}",
                f"{res['mean_product']:.12f}",
                f"{res['last_product']:.12f}",
            ]
        )

    print_table(
        [
            "zero",
            "gamma",
            "slope a in |c_P| ~= a log(P) + b",
            "coef c in |E_P| ~= c/log(P) + d",
            "R^2 for E fit",
            "mean(|E_P||c_P|)",
            "last |E_P||c_P|",
        ],
        summary_rows,
    )

    a_vals = np.array([r["a"] for r in results], dtype=float)
    a_min = float(np.min(a_vals))
    a_max = float(np.max(a_vals))
    print("\nSlope comparison:")
    for res in results:
        print(f"  rho_{res['index']}: a = {res['a']:.12f}")
    print(f"  spread in a across the three zeros = {a_max - a_min:.12f}")
    print("  reference: the first zero slope is expected to be near 1.15")


if __name__ == "__main__":
    main()
