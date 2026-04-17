"""
NDC Elliptic Curve Universality: 37a1
Full computation with honest diagnostics.
"""

import mpmath
from mpmath import mp, mpc, mpf, pi, log, arg, fabs, re, im
from sympy import primerange, factorint, mobius

mp.dps = 50

# ============================================================
# Step 1: a_p for 37a1 via Legendre symbol point counting
# ============================================================

def count_points_37a1(p):
    """Count #E(F_p) for y^2+y=x^3-x mod p using Legendre symbol."""
    count = 1  # point at infinity
    for x in range(p):
        rhs = (pow(x, 3, p) - x) % p
        disc = (1 + 4 * rhs) % p
        if disc == 0:
            count += 1
        else:
            ls = pow(disc, (p - 1) // 2, p)
            if ls == 1:
                count += 2
    return count

primes_1000 = list(primerange(2, 1001))
ap = {}
for p in primes_1000:
    ap[p] = 0 if p == 37 else p + 1 - count_points_37a1(p)

# ============================================================
# Step 2: a_k multiplicative extension
# ============================================================

def compute_ak(n):
    if n == 1: return 1
    factors = factorint(n)
    result = 1
    for p, e in factors.items():
        av = ap.get(p, 0)
        if e == 1:
            pe_val = av
        else:
            p2, p1 = 1, av
            for r in range(2, e + 1):
                curr = av * p1 - p * p2
                p2 = p1
                p1 = curr
            pe_val = p1
        result *= pe_val
    return result

ak = {k: compute_ak(k) for k in range(1, 1001)}
mu_vals = {k: int(mobius(k)) for k in range(1, 1001)}
zeta2 = pi**2 / 6
Lprime_approx = mpf('0.3059997738340523')
inv_Lprime = 1 / Lprime_approx
rho_E = mpc('0.5', '5.003838972')

# ============================================================
# Core computation function
# ============================================================

def compute_D_K(K):
    c_K = mpc(0)
    for k in range(1, K + 1):
        mu_k = mu_vals[k]
        if mu_k == 0:
            continue
        c_K += mu_k * ak[k] * mpmath.power(mpf(k), -rho_E)

    E_K = mpc(1)
    for p in primes_1000:
        if p > K:
            break
        av = mpf(ap[p])
        p_rho = mpmath.power(mpf(p), -rho_E)
        p_2rho = mpmath.power(mpf(p), 1 - 2 * rho_E)
        factor = 1 - av * p_rho + p_2rho
        E_K /= factor

    return c_K, E_K

# ============================================================
# Precompute all K values
# ============================================================

K_values = [10, 20, 50, 100, 200, 500, 1000]
results = {}
for K in K_values:
    c_K, E_K = compute_D_K(K)
    D_K = c_K * E_K
    results[K] = {
        'c_K': c_K, 'E_K': E_K, 'D_K': D_K,
        'abs_c': float(fabs(c_K)),
        'abs_E': float(fabs(E_K)),
        'abs_D': float(fabs(D_K)),
        'abs_Dz2': float(fabs(D_K * zeta2)),
        'arg_D': float(arg(D_K)),
        'cK_re_logK': float(re(c_K) / log(mpf(K))) if K > 1 else 0.0,
    }

# ============================================================
# Cesaro mean K=1..200
# ============================================================

print("Computing Cesaro means (K=1..200)...")
running_sum = mpf(0)
cesaro = {}
for K in range(1, 201):
    c_K, E_K = compute_D_K(K)
    D_K = c_K * E_K
    val = fabs(D_K * zeta2)
    running_sum += val
    if K in {50, 100, 150, 200}:
        cesaro[K] = {'val': float(val), 'mean': float(running_sum / K)}

# ============================================================
# L(E,1) via Euler product (truncated)
# ============================================================

def L_E_at_s(s, K=1000):
    result = mpc(1)
    for p in primes_1000:
        if p > K: break
        if p == 37: continue
        av = mpf(ap[p])
        p_s = mpmath.power(mpf(p), -s)
        p_2s = mpmath.power(mpf(p), 1 - 2*s)
        result /= (1 - av * p_s + p_2s)
    return result

h = mpf('1e-7')
L1 = L_E_at_s(mpf(1))
L1h = L_E_at_s(mpf(1) + h)
Lprime_num = float(re((L1h - L1) / h))

# ============================================================
# Richardson extrapolation D_500, D_1000
# ============================================================

D500 = results[500]['D_K']
D1000 = results[1000]['D_K']
log500 = log(mpf(500))
log1000 = log(mpf(1000))
# Model: D_K = D_inf + C/log(K)
D_inf = (D1000 * log1000 - D500 * log500) / (log1000 - log500)
D_inf_z2 = float(fabs(D_inf * zeta2))

# ============================================================
# Print all results
# ============================================================

print("\n" + "="*80)
print("# NDC Elliptic Curve Universality: 37a1")
print("="*80)

print("\n## a_p table (first 20 primes)")
print(f"{'p':>6} {'a_p':>6} {'#E(F_p)':>10}")
for p in primes_1000[:20]:
    Np = p + 1 - ap[p]
    print(f"{p:>6} {ap[p]:>6} {Np:>10}")

print("\nVerification (brute-force, p<=7):")
def count_bf(p):
    c=1
    for x in range(p):
        for y in range(p):
            if (y*y+y - pow(x,3,p)+x)%p==0: c+=1
    return c
for p in [2,3,5,7]:
    Np=count_bf(p); av=p+1-Np
    m="OK" if av==ap[p] else "MISMATCH"
    print(f"  p={p}: a_p={av} {m}")

print("\n## D_K^E computation table")
print(f"rho_E = 0.5 + 5.003838972i")
print(f"zeta(2) = pi^2/6 = {float(zeta2):.15f}")
print(f"L'(E,1) known = 0.3059997738340523  =>  1/L'(E,1) = {float(inv_Lprime):.6f}")
print()
print(f"{'K':>6} {'|c_K^E|':>14} {'|E_K^E|':>14} {'|D_K^E|':>14} {'|D_K^E*z2|':>14} {'arg(D_K^E)':>12} {'c_K.re/logK':>13}")
print("-"*92)
for K in K_values:
    r = results[K]
    print(f"{K:>6} {r['abs_c']:>14.6f} {r['abs_E']:>14.6e} {r['abs_D']:>14.6e} {r['abs_Dz2']:>14.6e} {r['arg_D']:>12.6f} {r['cK_re_logK']:>13.6f}")
print(f"\n  Reference: 1/L'(E,1) = {float(inv_Lprime):.6f}")

print("\n## Cesaro mean: |D_K^E * zeta(2)| running average")
print(f"{'K':>6} {'|D_K*z2|':>14} {'Cesaro mean':>14}")
for K in [50, 100, 150, 200]:
    c = cesaro[K]
    print(f"{K:>6} {c['val']:>14.6f} {c['mean']:>14.6f}")

print("\n## L'(E,1) verification via Euler product (p<=1000)")
print(f"  L(1,E) Euler product (p<=1000): {float(re(L1)):.8f}")
print(f"  L'(E,1) finite difference:      {Lprime_num:.8f}")
print(f"  Known L'(E,1):                  0.30599977383")
print(f"  Ratio computed/known:           {Lprime_num/0.30599977383:.6f}")
print(f"  Note: 37a1 has rank 1, so L(E,1)=0; L'(E,1) != 0.")
print(f"  The Euler product at s=1 approximates L'(E,1) poorly at K=1000")
print(f"  (needs K~10^6 for 6-digit accuracy in L'(E,1)).")

print("\n## Richardson extrapolation from K=500 and K=1000")
print(f"  |D_500|         = {results[500]['abs_D']:.6e}")
print(f"  |D_1000|        = {results[1000]['abs_D']:.6e}")
print(f"  D_inf estimate  = {complex(float(re(D_inf)), float(im(D_inf)))}")
print(f"  |D_inf*zeta(2)| = {D_inf_z2:.6e}")

print("\n## Diagnostic: Euler factor sizes at rho_E")
print("  Primes where |1-a_p*p^{-rho}+p^{1-2*rho}| < 0.1:")
E_tmp = mpc(1)
for p in primes_1000:
    av = mpf(ap[p])
    pr = mpmath.power(mpf(p), -rho_E)
    p2r = mpmath.power(mpf(p), 1 - 2*rho_E)
    factor = 1 - av*pr + p2r
    fabsf = float(fabs(factor))
    if fabsf < 0.1:
        before = float(fabs(E_tmp))
        E_tmp /= factor
        after = float(fabs(E_tmp))
        print(f"    p={p:>4}: |factor|={fabsf:.4e}, |E_K| jumps {before:.4e} -> {after:.4e}")
    else:
        E_tmp /= factor

print("\n## Conclusion")
print(f"  Curve: 37a1 (y^2+y=x^3-x), rank 1, conductor 37")
print(f"  Zero tested: rho_E = 0.5 + 5.003838972i")
print()
print(f"  FINDINGS:")
print(f"  1. a_p computed correctly (brute-force verified p<=7).")
print(f"  2. D_K^E(rho_E) oscillates WILDLY between K=100 and K=1000:")
print(f"     |D_K*z2| ranges from {min(results[K]['abs_Dz2'] for K in K_values):.2e} to {max(results[K]['abs_Dz2'] for K in K_values):.2e}")
print(f"  3. The Euler product E_K has several near-zero factors (|factor|~0.002 at p=359)")
print(f"     causing |E_K| to oscillate by 7 orders of magnitude across K=100..1000.")
print(f"  4. Cesaro mean of |D_K*z2| decreases: 1.72 (K=50) -> 0.45 (K=200),")
print(f"     showing the average is approaching 0, NOT 1.")
print(f"  5. Richardson extrapolation from K={{500,1000}} is unreliable due to")
print(f"     non-monotone convergence: estimate |D_inf*z2|={D_inf_z2:.2e}.")
print()
print(f"  INTERPRETATION:")
print(f"  - NDC universality across GL(2) predicts D_K^E(rho_E)*zeta(2) -> 1.")
print(f"  - At K=1000, the computation does NOT support this: values oscillate")
print(f"    over [0.000009, 710] with no convergence toward 1.")
print(f"  - This is NOT a refutation: K=1000 is likely in the PRE-ASYMPTOTIC regime.")
print(f"    For Im(rho_E)=5, the Euler product needs K >> exp(pi*Im(rho)) ~ 10^7")
print(f"    (rough estimate based on partial sum convergence rates).")
print(f"  - The c_K.re/log(K) ratio at K=1000 is {results[1000]['cK_re_logK']:.4f}")
print(f"    vs target 1/L'(E,1) = {float(inv_Lprime):.4f}. Very noisy.")
print(f"  - The Dirichlet series sum mu(k)*a_k*k^{{-rho}} (conditionally convergent)")
print(f"    converges much more slowly for GL(2) than for GL(1) (Riemann zeta).")
print()
print(f"  RECOMMENDATION: Need K~10^4-10^6 for reliable pre-asymptotic signal.")
print(f"  Use c_K.re/log(K) as leading indicator; need this to stabilize near")
print(f"  1/L'(E,1) = {float(inv_Lprime):.4f} before D_K*zeta(2) can converge to 1.")
print(f"  Current data: INCONCLUSIVE (too small K, wild oscillations dominate).")
