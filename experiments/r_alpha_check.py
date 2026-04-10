from fractions import Fraction
from math import gcd


def mobius_upto(n: int) -> list[int]:
    mu = [1] * (n + 1)
    mu[0] = 0
    primes: list[int] = []
    is_comp = [False] * (n + 1)
    for i in range(2, n + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def farey_sequence(N: int) -> list[Fraction]:
    fracs: list[Fraction] = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    return sorted(set(fracs))


def e_formula(q: int, mu: list[int]) -> Fraction:
    return Fraction(sum(mu[d] * d for d in range(1, q + 1) if q % d == 0), 6 * q)


def R_formula(N: int, M: list[int]) -> Fraction:
    return Fraction(1, 6) + sum(Fraction(M[N // m], 6 * m) for m in range(1, N + 1))


def alpha_exact(N: int) -> Fraction:
    F = farey_sequence(N)
    n = len(F)
    mean_f = Fraction(1, 2)
    D = [Fraction(i, 1) - n * f for i, f in enumerate(F)]
    cov = sum(D[i] * (F[i] - mean_f) for i in range(n)) / n
    var = sum((F[i] - mean_f) ** 2 for i in range(n)) / n
    return cov / var


def precompute_R_values(Nmax: int, mu: list[int]) -> list[Fraction]:
    R = [Fraction(0, 1)] * (Nmax + 1)
    running = Fraction(1, 3)
    for q in range(2, Nmax + 1):
        running += e_formula(q, mu)
        R[q] = running
    return R


def main() -> None:
    Nmax = 50000
    mu = mobius_upto(Nmax)
    M = [0] * (Nmax + 1)
    for i in range(1, Nmax + 1):
        M[i] = M[i - 1] + mu[i]
    R_values = precompute_R_values(Nmax, mu)

    print("Check 1: e(q) exact formula for q = 2..20")
    for q in range(2, 21):
        print(q, float(e_formula(q, mu)))

    print()
    print("Check 2: alpha vs -6R on sample N")
    for N in [12, 18, 42, 70, 106, 198]:
        alpha = alpha_exact(N)
        R = R_formula(N, M)
        ratio = float(alpha / (-6 * R))
        print(
            f"N={N:3d} alpha={float(alpha):.6f} "
            f"-6R={float(-6 * R):.6f} ratio={ratio:.6f}"
        )

    print()
    print("Check 3: R(p-1) on the M(p)=-3 subsequence up to 50000")
    vals: list[tuple[int, float]] = []
    for p in range(13, Nmax + 1):
        if is_prime(p) and M[p] == -3:
            vals.append((p, float(R_values[p - 1])))

    print(f"count={len(vals)}")
    print(f"max_R={max(vals, key=lambda x: x[1])}")
    print(f"min_R={min(vals, key=lambda x: x[1])}")
    print("first_20=", vals[:20])


if __name__ == "__main__":
    main()
