#!/usr/bin/env python3
"""Correct Dirichlet character table mod N, by CRT prime-power
decomposition, with a built-in orthogonality self-test.

(Z/NZ)* = prod over p^e || N of (Z/p^e)* :
  * p odd        -> cyclic of order phi(p^e); primitive root by search
  * p=2, e=1     -> trivial
  * p=2, e=2     -> C2  (gen 3)
  * p=2, e>=3    -> C2 x C_{2^{e-2}}  (gens -1 and 5)
Each cyclic factor (gen g mod p^e, order d) is CRT-lifted to G mod N
(G == g mod p^e, == 1 mod the rest).  Every unit is uniquely
prod G_i^{x_i}; characters are all prod exp(2πi k_i x_i / d_i).

char_table(N) -> (U, chars) with len(chars)==phi(N); raises unless the
full orthogonality relations hold (so a construction bug cannot pass
silently).
"""
import cmath, math

def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def mult_order(a, m):
    a %= m
    o, v = 1, a
    while v != 1:
        v = (v * a) % m; o += 1
        if o > m:
            raise RuntimeError(f"no order: {a} mod {m}")
    return o

def primitive_root(q):
    """smallest primitive root mod q for q with a cyclic unit group."""
    phi = q // factorize(q).popitem()[0] * (1) if False else euler_phi(q)
    for g in range(2, q):
        if math.gcd(g, q) == 1 and mult_order(g, q) == phi:
            return g
    raise RuntimeError(f"no primitive root mod {q}")

def euler_phi(n):
    r = n
    for p in factorize(n):
        r -= r // p
    return r

def cyclic_factors(p, e):
    """list of (gen mod p^e, order) for (Z/p^e)*."""
    q = p ** e
    if p % 2 == 1:
        return [(primitive_root(q), euler_phi(q))]
    if e == 1:
        return []                       # (Z/2)* trivial
    if e == 2:
        return [(3, 2)]                 # (Z/4)* = {1,3}
    return [(q - 1, 2), (5, 1 << (e - 2))]   # (Z/2^e)*, e>=3

def crt_lift(g, q, N):
    """integer G mod N with G==g (mod q) and G==1 (mod N//q)."""
    m = N // q
    if m == 1:
        return g % N
    inv = pow(m, -1, q)                  # m * inv == 1 (mod q)
    # G = 1 + m * t, choose t so 1 + m t == g (mod q)
    t = ((g - 1) * inv) % q
    G = (1 + m * t) % N
    assert G % q == g % q and G % m == 1 % m, (g, q, N, G)
    return G

def units(N):
    return [a for a in range(1, N) if math.gcd(a, N) == 1]

def char_table(N):
    U = units(N)
    phiN = len(U)
    # global list of cyclic factors lifted to mod N
    facs = []                            # (G mod N, order d)
    for p, e in factorize(N).items():
        q = p ** e
        for g, d in cyclic_factors(p, e):
            facs.append((crt_lift(g, q, N), d))
    # exponent vector of every unit (unique by CRT + cyclicity)
    idx = {}
    r = len(facs)
    dims = [d for _, d in facs]
    def rec(i, val, vec):
        if i == r:
            idx[val] = tuple(vec); return
        G, d = facs[i]
        x = 1
        for ei in range(d):
            rec(i + 1, (val * x) % N, vec + [ei])
            x = (x * G) % N
    rec(0, 1, [])
    if set(idx) != set(U) or len(idx) != phiN:
        raise RuntimeError(f"N={N}: unit parametrisation wrong "
                           f"({len(idx)} vs phi={phiN})")
    # all characters
    chars = []
    def build(i, ks):
        if i == r:
            ch = {}
            for u in U:
                ev = idx[u]
                ph = sum(ks[t] * ev[t] / dims[t] for t in range(r))
                ch[u] = cmath.exp(2j * math.pi * ph)
            chars.append(ch); return
        for k in range(dims[i]):
            build(i + 1, ks + [k])
    build(0, [])
    if len(chars) != phiN:
        raise RuntimeError(f"N={N}: built {len(chars)} chars, phi={phiN}")
    # --- orthogonality self-test (column + row) ---
    for a in U:
        s = sum(ch[a] * ch[1].conjugate() for ch in chars)
        want = phiN if a == 1 else 0
        if abs(s - want) > 1e-7:
            raise RuntimeError(f"N={N}: column orthogonality fail a={a}: {s}")
    for ch in chars:
        s = sum(ch[u] for u in U)
        principal = all(abs(ch[u] - 1) < 1e-9 for u in U)
        if abs(s - (phiN if principal else 0)) > 1e-7:
            raise RuntimeError(f"N={N}: row orthogonality fail")
    return U, chars

if __name__ == "__main__":
    import sys
    for N in ([int(x) for x in sys.argv[1:]] or [7, 8, 11, 19, 23]):
        U, ch = char_table(N)
        print(f"N={N:>3}  units={len(U):>2}  chars={len(ch):>2}  "
              f"phi={euler_phi(N):>2}  orthogonality OK")
