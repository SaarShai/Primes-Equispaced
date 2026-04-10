"""
Extended computation: K[N] - K[N/2] for more primes.
Also compute the analytical decomposition more carefully.

Key identity: K_diff = sum_f [sum_{j=N/2+1}^N {jf}] * delta(f)
            = sum_f [half_sum(f) - N/4] * delta(f)   [since sum delta = 0]

This is a CORRELATION between the half-sum fluctuations and delta.

For f = a/b with gcd(a,b)=1, the sum sum_{j=1}^m {ja/b} has an exact formula:
  sum_{j=1}^m {ja/b} = (m - floor(m/b)*b)(b-1)/2/b + ...
Actually, the Dedekind-type sum: sum_{j=1}^m {ja/b} = m(b-1)/(2b) + error terms.

Let's just compute the ratio for more primes and understand the asymptotics.
"""

from fractions import Fraction
import math

def farey_interior(N):
    fracs = set()
    for b in range(2, N+1):
        for a in range(1, b):
            if math.gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def delta_p(f, p):
    a, b = f.numerator, f.denominator
    bma = b - a
    res = (p * bma) % b
    if res == 0:
        res = b
    return Fraction(res - bma, b)

def mertens(n):
    """Compute M(n) = sum_{k=1}^n mu(k)."""
    if n <= 0:
        return 0
    # Sieve mu
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (n + 1)
    for i in range(1, n + 1):
        M[i] = M[i-1] + mu[i]
    return M[n]

def compute_q1_block(p):
    N = p - 1
    N2 = N // 2
    fracs = farey_interior(N)

    deltas = {f: delta_p(f, p) for f in fracs}
    Cprime = sum(d*d for d in deltas.values())

    K_diff = Fraction(0)
    for f in fracs:
        d = deltas[f]
        half_sum = Fraction(0)
        for j in range(N2 + 1, N + 1):
            jf = j * f
            fp = jf - int(jf)
            if fp < 0:
                fp += 1
            half_sum += fp
        K_diff += half_sum * d

    return float(K_diff), float(Cprime), float(K_diff / Cprime)

# Find M(p)=-3 primes
def get_mp3_primes(limit):
    """Find primes p where M(p) = -3."""
    # Sieve
    n = limit
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime_arr = [True] * (n + 1)
    primes_list = []
    for i in range(2, n + 1):
        if is_prime_arr[i]:
            primes_list.append(i)
            mu[i] = -1
        for pr in primes_list:
            if i * pr > n:
                break
            is_prime_arr[i * pr] = False
            if i % pr == 0:
                mu[i * pr] = 0
                break
            else:
                mu[i * pr] = -mu[i]

    M = [0] * (n + 1)
    for i in range(1, n + 1):
        M[i] = M[i-1] + mu[i]

    result = []
    for p in primes_list:
        if M[p] == -3:
            result.append(p)
    return result

primes = get_mp3_primes(300)
print(f"M(p)=-3 primes up to 300: {primes}")
print()

print(f"{'p':>5} {'N':>5} {'K_diff':>12} {'Cprime':>12} {'ratio':>10}")
for p in primes:
    kd, cp, ratio = compute_q1_block(p)
    print(f"{p:>5} {p-1:>5} {kd:>12.4f} {cp:>12.4f} {ratio:>10.6f}")
