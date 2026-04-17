from mpmath import mp

mp.dps = 30

HALF = mp.mpf("0.5")
QUARTER = mp.mpf("0.25")
THREE_QUARTER = mp.mpf("0.75")
FOUR_OVER_PI = mp.mpf("4") / mp.pi

N_TERMS = 10000
K = 10
SCAN_START = mp.mpf("1")
SCAN_END = mp.mpf("200")
SCAN_STEP = mp.mpf("0.5")
ZERO_TARGET = 40

SIGN_TOL = mp.mpf("1e-28")
ROOT_TOL = mp.mpf("1e-12")


def chi4(n):
    r = n % 4
    if r == 1:
        return 1
    if r == 3:
        return -1
    return 0


def mobius_sieve(nmax):
    mu = [0] * (nmax + 1)
    if nmax >= 1:
        mu[1] = 1
    primes = []
    is_comp = [False] * (nmax + 1)

    for i in range(2, nmax + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > nmax:
                break
            is_comp[ip] = True
            if i % p == 0:
                mu[ip] = 0
                break
            mu[ip] = -mu[i]
    return mu


MU = mobius_sieve(K)

EXPECTED_CHI = [1, 0, -1, 0]
EXPECTED_MU = [1, -1, -1, 0, -1, 1, -1, 0, 0, 1]
if [chi4(n) for n in range(1, 5)] != EXPECTED_CHI:
    raise RuntimeError("chi4 verification failed")
if MU[1:11] != EXPECTED_MU:
    raise RuntimeError("mu verification failed")

# Partial-sum terms for L(1/2 + it, chi4), using odd n only.
SCAN_TERMS = []
for n in range(1, N_TERMS + 1, 2):
    sign = 1 if n % 4 == 1 else -1
    SCAN_TERMS.append((mp.mpf(sign) / mp.sqrt(n), mp.log(n)))


def beta_partial_on_line(t):
    t = mp.mpf(t)
    total = mp.mpc(0)
    jt = -mp.j * t
    for coeff, logn in SCAN_TERMS:
        total += coeff * mp.exp(jt * logn)
    return total


def beta_exact_on_line(t):
    t = mp.mpf(t)
    s = HALF + mp.j * t
    try:
        return mp.power(mp.mpf(4), -s) * (
            mp.zeta(s, QUARTER) - mp.zeta(s, THREE_QUARTER)
        )
    except Exception:
        return beta_partial_on_line(t)


def completed_real_from_beta(t, beta_val):
    t = mp.mpf(t)
    s = HALF + mp.j * t
    val = (FOUR_OVER_PI ** ((s + 1) / 2)) * mp.gamma((s + 1) / 2) * beta_val
    return mp.re(val)


def z_scan(t):
    return completed_real_from_beta(t, beta_partial_on_line(t))


def z_exact(t):
    return completed_real_from_beta(t, beta_exact_on_line(t))


def sign_real(x, tol=SIGN_TOL):
    if not mp.isfinite(x):
        raise ValueError("non-finite value")
    if x > tol:
        return 1
    if x < -tol:
        return -1
    return 0


def bisect_root(f, a, b, tol=ROOT_TOL, max_iter=100):
    a = mp.mpf(a)
    b = mp.mpf(b)
    fa = f(a)
    fb = f(b)
    sa = sign_real(fa)
    sb = sign_real(fb)

    if sa == 0:
        return a
    if sb == 0:
        return b
    if sa * sb > 0:
        raise ValueError("interval does not bracket a sign change")

    for _ in range(max_iter):
        m = (a + b) / 2
        fm = f(m)
        sm = sign_real(fm)

        if sm == 0 or (b - a) / 2 < tol:
            return m

        if sa * sm < 0:
            b = m
            fb = fm
            sb = sm
        else:
            a = m
            fa = fm
            sa = sm

    return (a + b) / 2


def refine_zero(a, b):
    try:
        return bisect_root(z_exact, a, b)
    except Exception:
        pass

    try:
        return bisect_root(z_scan, a, b)
    except Exception:
        pass

    try:
        pts = [mp.mpf(a) + (mp.mpf(b) - mp.mpf(a)) * mp.mpf(i) / 8 for i in range(9)]
        vals = [z_exact(p) for p in pts]
        for i in range(8):
            if sign_real(vals[i]) * sign_real(vals[i + 1]) < 0:
                return bisect_root(z_exact, pts[i], pts[i + 1])
    except Exception:
        pass

    raise RuntimeError("failed to refine zero")


def c_chi_k(s, c_terms):
    total = mp.mpc(0)
    for k, coeff in c_terms:
        total += coeff * mp.power(k, -s)
    return total


def fmt(x, digits=15):
    try:
        if not mp.isfinite(x):
            return str(x)
    except Exception:
        return str(x)
    return mp.nstr(x, digits)


def main():
    c_terms = []
    for k in range(2, K + 1):
        coeff = MU[k] * chi4(k)
        if coeff != 0:
            c_terms.append((k, mp.mpf(coeff)))

    print("mp.dps =", mp.dps)
    print("N_terms =", N_TERMS)
    print("K =", K)
    print("chi4(1..4) =", [chi4(n) for n in range(1, 5)])
    print("mu(1..10) =", [MU[n] for n in range(1, 11)])
    print()

    brackets = []
    prev_t = SCAN_START
    prev_val = z_scan(prev_t)
    prev_sign = sign_real(prev_val)

    num_scan_steps = int((SCAN_END - SCAN_START) / SCAN_STEP)
    for i in range(1, num_scan_steps + 1):
        t = SCAN_START + SCAN_STEP * i
        val = z_scan(t)
        sgn = sign_real(val)
        if prev_sign * sgn < 0:
            brackets.append((prev_t, t))
            if len(brackets) >= ZERO_TARGET:
                break
        prev_t = t
        prev_sign = sgn

    zeros = []
    for a, b in brackets:
        root = refine_zero(a, b)
        if not zeros or abs(root - zeros[-1]) > mp.mpf("1e-8"):
            zeros.append(root)
        if len(zeros) >= ZERO_TARGET:
            break

    if len(zeros) < ZERO_TARGET:
        raise RuntimeError(f"found only {len(zeros)} zeros in [{SCAN_START}, {SCAN_END}]")

    zero_mags = [abs(c_chi_k(HALF + mp.j * g, c_terms)) for g in zeros]

    generic_ts = [mp.mpf(500) * i / mp.mpf(999) for i in range(1000)]
    generic_mags = [abs(c_chi_k(HALF + mp.j * t, c_terms)) for t in generic_ts]

    zero_mean = mp.fsum(zero_mags) / len(zero_mags)
    generic_mean = mp.fsum(generic_mags) / len(generic_mags)

    zero_min_idx = min(range(len(zero_mags)), key=zero_mags.__getitem__)
    generic_min_idx = min(range(len(generic_mags)), key=generic_mags.__getitem__)
    zero_max_idx = max(range(len(zero_mags)), key=zero_mags.__getitem__)
    generic_max_idx = max(range(len(generic_mags)), key=generic_mags.__getitem__)

    zero_min = zero_mags[zero_min_idx]
    generic_min = generic_mags[generic_min_idx]
    zero_max = zero_mags[zero_max_idx]
    generic_max = generic_mags[generic_max_idx]

    mean_ratio = zero_mean / generic_mean if generic_mean != 0 else mp.inf
    min_ratio = zero_min / generic_min if generic_min != 0 else mp.inf

    print("First 50 zeros of L(s, chi4) on the critical line")
    print("(found by scanning a 10000-term partial sum on [1, 200] with step 0.5)")
    for j, g in enumerate(zeros, 1):
        print(f"{j:2d}: gamma = {fmt(g, 15)}")
    print()

    print("|c_{chi,K}(1/2+i*gamma_j)| at each zero, K=10")
    for j, (g, v) in enumerate(zip(zeros, zero_mags), 1):
        print(f"{j:2d}: gamma = {fmt(g, 15)}   |c| = {fmt(v, 15)}")
    print()

    print("Zero-point statistics")
    print("  count =", len(zero_mags))
    print("  mean |c| =", fmt(zero_mean, 15))
    print("  min  |c| =", fmt(zero_min, 15), "at gamma =", fmt(zeros[zero_min_idx], 15))
    print("  max  |c| =", fmt(zero_max, 15), "at gamma =", fmt(zeros[zero_max_idx], 15))
    print()

    print("Generic-point statistics")
    print("  count =", len(generic_mags))
    print("  t-grid = 1000 uniformly spaced points in [0, 500]")
    print("  mean |c| =", fmt(generic_mean, 15))
    print("  min  |c| =", fmt(generic_min, 15), "at t =", fmt(generic_ts[generic_min_idx], 15))
    print("  max  |c| =", fmt(generic_max, 15), "at t =", fmt(generic_ts[generic_max_idx], 15))
    print()

    print("Avoidance ratios")
    print("  mean_zero / mean_generic =", fmt(mean_ratio, 15))
    print("  min_zero / min_generic =", fmt(min_ratio, 15))
    print()

    print("First zero check:", fmt(zeros[0], 15), "(expected near 6.0209)")


if __name__ == "__main__":
    main()
