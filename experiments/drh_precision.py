#!/usr/bin/env python3
"""
High-precision DRH verification computation.

Requirements implemented:
- mp.dps = 50 throughout
- Möbius function via a linear sieve up to max K = 1000
- First 10 zeta zeros from mp.zetazero(j)
- c_K(s) = sum_{k<=K} mu(k) * k^{-s}
- zeta'(rho_j) via mp.zeta(rho_j, derivative=1), with numerical fallback
- Least-squares fit of |c_K| against log(K)
- Euler product E_P(s) over primes p <= P
- Clean publication-style output and timing info
"""

from mpmath import mp
from time import perf_counter


# ---------------------------------------------------------------------------
# Global precision
# ---------------------------------------------------------------------------

mp.dps = 50

DIGITS = 18
ZERO_COUNT = 10
MAX_K = 1000
FIT_KS = [10, 20, 50, 100, 200, 500]
GROWTH_KS = [2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 700, 1000]
EULER_P_VALUES = [10, 50, 100, 500]


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_mpf(x, digits=DIGITS):
    return mp.nstr(x, digits)


def fmt_complex(z, digits=DIGITS):
    re = mp.nstr(mp.re(z), digits)
    im = mp.nstr(mp.im(z), digits)
    if im.startswith("-"):
        return f"{re} - {im[1:]}j"
    return f"{re} + {im}j"


def print_section(title):
    print()
    print("=" * 92)
    print(title)
    print("=" * 92)


def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    fmt = "  ".join("{:<" + str(w) + "}" for w in widths)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * w for w in widths]))
    for row in rows:
        print(fmt.format(*row))


# ---------------------------------------------------------------------------
# Sieve: primes and Möbius function
# ---------------------------------------------------------------------------

def sieve_moebius_and_primes(limit):
    """
    Linear sieve that returns:
      mu[n] for 0 <= n <= limit
      primes list up to limit

    Correctly handles:
      mu(1) = 1
      mu(p) = -1 for prime p
      mu(p^2) = 0
    """
    mu = [0] * (limit + 1)
    lp = [0] * (limit + 1)
    primes = []

    if limit >= 1:
        mu[1] = 1

    for i in range(2, limit + 1):
        if lp[i] == 0:
            lp[i] = i
            primes.append(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > limit:
                break
            lp[ip] = p
            if p == lp[i]:
                mu[ip] = 0
                break
            mu[ip] = -mu[i]

    if limit >= 6:
        assert mu[1] == 1
        assert mu[2] == -1
        assert mu[4] == 0
        assert mu[6] == 1

    return mu, primes


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------

def zeta_prime_at(rho):
    """
    First derivative of zeta at rho.
    Uses mp.zeta(rho, derivative=1) if available; falls back to mp.diff.
    """
    try:
        return mp.zeta(rho, derivative=1)
    except TypeError:
        return mp.diff(lambda s: mp.zeta(s), rho)


def c_prefix_values(rho, mu, max_k):
    """
    Compute prefix sums:
      c_K(rho) = sum_{k=1}^K mu(k) * k^{-rho}
    for K = 1..max_k.

    Returns a list c_prefix where c_prefix[K] is c_K(rho), and c_prefix[0] = 0.
    """
    prefix = [mp.mpc(0)] * (max_k + 1)
    running = mp.mpc(0)
    for k in range(1, max_k + 1):
        running += mu[k] * mp.power(mp.mpf(k), -rho)
        prefix[k] = running
    return prefix


def ordinary_least_squares(xs, ys):
    """
    Fit y = a*x + b using ordinary least squares via normal equations.

    xs, ys are lists of mp numbers.
    """
    n = mp.mpf(len(xs))
    sx = mp.fsum(xs)
    sy = mp.fsum(ys)
    sxx = mp.fsum([x * x for x in xs])
    sxy = mp.fsum([x * y for x, y in zip(xs, ys)])
    denom = n * sxx - sx * sx
    if denom == 0:
        raise ZeroDivisionError("degenerate least-squares system")
    a = (n * sxy - sx * sy) / denom
    b = (sy - a * sx) / n
    return a, b


def euler_product(s, primes, P):
    """
    E_P(s) = prod_{p <= P} (1 - p^{-s})^{-1}.
    """
    prod = mp.mpc(1)
    for p in primes:
        if p > P:
            break
        prod *= 1 / (1 - mp.power(mp.mpf(p), -s))
    return prod


def mean_and_std(values):
    n = mp.mpf(len(values))
    mean = mp.fsum(values) / n
    var = mp.fsum([(x - mean) ** 2 for x in values]) / n
    return mean, mp.sqrt(var)


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def main():
    t_global = perf_counter()

    mu, primes = sieve_moebius_and_primes(MAX_K)

    print_section("DRH verification computation with mpmath")
    print(f"mp.dps = {mp.dps}")
    print(f"Zero count        : {ZERO_COUNT}")
    print(f"Max K             : {MAX_K}")
    print(f"Fit K values      : {FIT_KS}")
    print(f"Growth curve K's  : {GROWTH_KS}")
    print(f"Euler P values    : {EULER_P_VALUES}")
    print(f"Primes generated  : {len(primes)} up to {MAX_K}")
    print(f"Timing start      : {t_global:.6f} (perf_counter seconds)")

    # -----------------------------------------------------------------------
    # 1) First 10 zeros: fit |c_K| ~ a_j log(K) + b_j
    # -----------------------------------------------------------------------
    print_section("1) First 10 zeta zeros: |c_K(rho_j)| fits against log(K)")

    fit_xs = [mp.log(mp.mpf(k)) for k in FIT_KS]
    zero_rows = []
    zero_results = []

    t_zeros = perf_counter()
    for j in range(1, ZERO_COUNT + 1):
        t_j = perf_counter()

        rho = mp.zetazero(j)
        gamma = mp.im(rho)
        zeta_prime = zeta_prime_at(rho)
        zeta_prime_abs = abs(zeta_prime)
        residue_inverse_abs = 1 / zeta_prime_abs

        prefix = c_prefix_values(rho, mu, MAX_K)
        fit_ys = [abs(prefix[k]) for k in FIT_KS]
        slope, intercept = ordinary_least_squares(fit_xs, fit_ys)

        ratio = slope / residue_inverse_abs  # equals slope * |zeta'(rho_j)|
        elapsed_j = perf_counter() - t_j

        zero_rows.append([
            str(j),
            fmt_mpf(gamma),
            fmt_mpf(zeta_prime_abs),
            fmt_mpf(slope),
            fmt_mpf(residue_inverse_abs),
            fmt_mpf(ratio),
            f"{elapsed_j:.4f}",
        ])
        zero_results.append({
            "j": j,
            "rho": rho,
            "gamma": gamma,
            "zeta_prime_abs": zeta_prime_abs,
            "residue_inverse_abs": residue_inverse_abs,
            "slope": slope,
            "intercept": intercept,
            "ratio": ratio,
            "prefix": prefix,
        })

    total_zeros_elapsed = perf_counter() - t_zeros

    print(
        "Fit model: |c_K(rho_j)| ≈ a_j * log(K) + b_j, with K in "
        f"{FIT_KS}"
    )
    print(
        "Note: the residue comparison uses |zeta'(rho_j)| because zeta(rho_j)=0 "
        "at a nontrivial zero."
    )
    print_table(
        [
            "j",
            "gamma_j",
            "|zeta'(rho_j)|",
            "a_j",
            "1/|zeta'|",
            "ratio = a_j / (1/|zeta'|)",
            "time_s",
        ],
        zero_rows,
    )
    print(f"Elapsed for zero loop: {total_zeros_elapsed:.4f} s")

    # -----------------------------------------------------------------------
    # 2) Growth curve for rho_1 over selected K values
    # -----------------------------------------------------------------------
    print_section("2) Full growth curve for rho_1: |c_K(rho_1)|")

    rho1 = zero_results[0]["rho"]
    prefix1 = zero_results[0]["prefix"]

    growth_rows = []
    for k in GROWTH_KS:
        growth_rows.append([str(k), fmt_mpf(abs(prefix1[k]))])

    print("Growth curve data for the first zero (rho_1):")
    print_table(["K", "|c_K(rho_1)|"], growth_rows)

    # -----------------------------------------------------------------------
    # 3) Universality check: a_j * |zeta'(rho_j)|
    # -----------------------------------------------------------------------
    print_section("3) Universality check: a_j * |zeta'(rho_j)|")

    ratio_rows = []
    ratios = []
    for res in zero_results:
        ratio = res["ratio"]
        ratios.append(ratio)
        ratio_rows.append([
            str(res["j"]),
            fmt_mpf(ratio),
            fmt_mpf(res["slope"]),
            fmt_mpf(res["zeta_prime_abs"]),
        ])

    print("Ratio definition: ratio_j = a_j * |zeta'(rho_j)|")
    print_table(
        ["j", "ratio_j", "a_j", "|zeta'(rho_j)|"],
        ratio_rows,
    )

    ratio_mean, ratio_std = mean_and_std(ratios)
    ratio_min = min(ratios)
    ratio_max = max(ratios)
    ratio_rel_std = ratio_std / abs(ratio_mean) if ratio_mean != 0 else mp.nan
    ratio_rel_range = (ratio_max - ratio_min) / abs(ratio_mean) if ratio_mean != 0 else mp.nan

    print()
    print(f"Mean ratio            : {fmt_mpf(ratio_mean)}")
    print(f"Std. dev.             : {fmt_mpf(ratio_std)}")
    print(f"Relative std. dev.    : {fmt_mpf(ratio_rel_std)}")
    print(f"Relative range        : {fmt_mpf(ratio_rel_range)}")
    print(
        "Assessment           : "
        "the first 10 sampled ratios provide only a finite-range diagnostic; "
        "use the spread above as the convergence check for any universal constant C."
    )

    # -----------------------------------------------------------------------
    # 4) E_P * c_500 product at rho_1
    # -----------------------------------------------------------------------
    print_section("4) Euler product experiment: E_P(rho_1) * c_500(rho_1)")

    c500_rho1 = prefix1[500]
    print(f"c_500(rho_1) = {fmt_complex(c500_rho1)}")

    euler_rows = []
    products = []

    for P in EULER_P_VALUES:
        E_P = euler_product(rho1, primes, P)
        product = E_P * c500_rho1
        products.append((P, E_P, product))
        euler_rows.append([
            str(P),
            fmt_complex(E_P),
            fmt_complex(product),
            fmt_mpf(abs(product)),
        ])

    print("E_P is the partial Euler product over primes p <= P.")
    print_table(
        ["P", "E_P(rho_1)", "E_P(rho_1) * c_500(rho_1)", "|product|"],
        euler_rows,
    )

    if len(products) >= 2:
        last_change = abs(products[-1][2] - products[-2][2])
        last_rel_change = last_change / abs(products[-1][2]) if products[-1][2] != 0 else mp.nan
        first_to_last = abs(products[-1][2] - products[0][2])
        first_to_last_rel = first_to_last / abs(products[-1][2]) if products[-1][2] != 0 else mp.nan

        print()
        print(f"Change from P={products[-2][0]} to P={products[-1][0]} : {fmt_mpf(last_change)}")
        print(f"Relative change last step          : {fmt_mpf(last_rel_change)}")
        print(f"Change from P={products[0][0]} to P={products[-1][0]}  : {fmt_mpf(first_to_last)}")
        print(f"Relative change first to last      : {fmt_mpf(first_to_last_rel)}")
        print(
            "Assessment                           : "
            "use the P=500 product as the best finite-P estimate from this run; "
            "the deltas above quantify whether the sequence appears numerically stabilized."
        )

    total_elapsed = perf_counter() - t_global
    print()
    print(f"Total elapsed time: {total_elapsed:.4f} s")


if __name__ == "__main__":
    main()
