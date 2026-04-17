"""
NDC Elliptic Curve Universality: 37a1
Compute D_K^E(rho_E) * zeta(2) for elliptic curve 37a1
y^2 + y = x^3 - x, conductor 37, rank 1
First zero: rho_E = 0.5 + 5.003838972i
"""

import mpmath
from mpmath import mp, mpc, mpf, pi, log, arg, fabs, re, im
from sympy import isprime, primerange, factorint, mobius

mp.dps = 40

# ============================================================
# Step 1: Compute a_p for primes p <= 1000
# ============================================================

def count_points_37a1(p):
    """Count #E(F_p) for y^2 + y = x^3 - x mod p."""
    # Complete the square in y: y^2+y = (y+1/2)^2 - 1/4
    # So (2y+1)^2 = 4(x^3-x) + 1
    # disc_y = 1 + 4*(x^3-x)
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

print("Computing a_p for primes p <= 1000...")
primes_up_to_1000 = list(primerange(2, 1001))
ap = {}
for p in primes_up_to_1000:
    if p == 37:
        ap[p] = 0
    else:
        Np = count_points_37a1(p)
        ap[p] = p + 1 - Np

print("\n## a_p table (first 20 primes)")
print(f"{'p':>6} {'a_p':>6} {'#E(F_p)':>10}")
for p in primes_up_to_1000[:20]:
    Np = p + 1 - ap[p]
    print(f"{p:>6} {ap[p]:>6} {Np:>10}")

# Brute force verification for small primes
print("\nBrute-force verification (p<=13):")
def count_bruteforce(p):
    count = 1
    for x in range(p):
        for y in range(p):
            if (y*y + y - pow(x,3,p) + x) % p == 0:
                count += 1
    return count

for p in [2,3,5,7,11,13]:
    Np_bf = count_bruteforce(p)
    ap_bf = p + 1 - Np_bf
    match = "OK" if ap_bf == ap[p] else f"MISMATCH (legendre got {ap[p]})"
    print(f"  p={p}: brute_force a_p={ap_bf}  {match}")

# ============================================================
# Step 2: Compute a_k for k <= 1000 multiplicatively
# ============================================================

def compute_ak(n, ap_dict):
    if n == 1:
        return 1
    factors = factorint(n)
    result = 1
    for p, e in factors.items():
        ap_val = ap_dict.get(p, 0)
        if e == 1:
            pe_val = ap_val
        else:
            prev2 = 1
            prev1 = ap_val
            for r in range(2, e + 1):
                curr = ap_val * prev1 - p * prev2
                prev2 = prev1
                prev1 = curr
            pe_val = prev1
        result *= pe_val
    return result

print("\nComputing a_k for k <= 1000...")
ak = {}
for k in range(1, 1001):
    ak[k] = compute_ak(k, ap)

# Spot checks: a_4 = a_{2^2} = a_2^2 - 2 = 4-2 = 2
print(f"  a_4 = a_2^2 - 2 = {(-2)**2 - 2} (expected 2), computed: {ak[4]}")
print(f"  a_9 = a_3^2 - 3 = {(-3)**2 - 3} (expected 6), computed: {ak[9]}")
print(f"  a_6 = a_2*a_3 = {(-2)*(-3)} (expected 6), computed: {ak[6]}")

# ============================================================
# Step 3: Compute D_K^E(rho_E) for K = 10, 20, 50, 100, 200, 500, 1000
# ============================================================

rho_E = mpc('0.5', '5.003838972')
zeta2 = pi**2 / 6
Lprime_approx = mpf('0.3059997738340523')
inv_Lprime = 1 / Lprime_approx

print("\n## D_K^E computation table")
print(f"\nrho_E = 0.5 + 5.003838972i")
print(f"zeta(2) = {mpmath.nstr(zeta2, 15)}")
print(f"L'(E,1) = 0.3059997738340523  =>  1/L'(E,1) = {float(inv_Lprime):.6f}")
print()
print(f"{'K':>6} {'|c_K^E|':>14} {'|E_K^E|':>14} {'|D_K^E|':>14} {'|D_K^E*z2|':>14} {'arg(D_K^E)':>12} {'c_K.re/log(K)':>15}")
print("-" * 100)

K_values = [10, 20, 50, 100, 200, 500, 1000]
D_K_values = {}

# Precompute mu(k) for k <= 1000
mu_vals = {k: int(mobius(k)) for k in range(1, 1001)}

def compute_D_K(K):
    # c_K^E(rho) = sum_{k<=K} mu(k)*a_k*k^{-rho}
    c_K = mpc(0)
    for k in range(1, K + 1):
        mu_k = mu_vals[k]
        if mu_k == 0:
            continue
        c_K += mu_k * ak[k] * mpmath.power(mpf(k), -rho_E)

    # E_K^E(rho) = prod_{p<=K} (1 - a_p*p^{-rho} + p^{1-2rho})^{-1}
    E_K = mpc(1)
    for p in primes_up_to_1000:
        if p > K:
            break
        ap_val = mpf(ap[p])
        p_rho = mpmath.power(mpf(p), -rho_E)
        p_2rho = mpmath.power(mpf(p), 1 - 2 * rho_E)
        factor = 1 - ap_val * p_rho + p_2rho
        E_K = E_K / factor

    return c_K, E_K

for K in K_values:
    c_K, E_K = compute_D_K(K)
    D_K = c_K * E_K
    D_K_zeta2 = D_K * zeta2
    D_K_values[K] = D_K

    abs_cK = float(fabs(c_K))
    abs_EK = float(fabs(E_K))
    abs_DK = float(fabs(D_K))
    abs_DKz2 = float(fabs(D_K_zeta2))
    arg_DK = float(arg(D_K))
    cK_re_logK = float(re(c_K) / log(mpf(K))) if K > 1 else 0.0

    print(f"{K:>6} {abs_cK:>14.6f} {abs_EK:>14.6f} {abs_DK:>14.6f} {abs_DKz2:>14.6f} {arg_DK:>12.6f} {cK_re_logK:>15.6f}")

print(f"\n  Reference 1/L'(E,1) = {float(inv_Lprime):.6f}")

# ============================================================
# Step 4: Cesaro mean of |D_K^E * zeta(2)| for K=1..200
# ============================================================

print("\n## Cesaro mean table")
print(f"{'K':>6} {'|D_K*z2|':>14} {'Cesaro mean':>14}")

running_sum = mpf(0)
for K in range(1, 201):
    c_K, E_K = compute_D_K(K)
    D_K = c_K * E_K
    val = fabs(D_K * zeta2)
    running_sum += val
    if K in {50, 100, 150, 200}:
        cesaro_mean = running_sum / K
        print(f"{K:>6} {float(val):>14.6f} {float(cesaro_mean):>14.6f}")

# ============================================================
# Step 5: L'(E,1) verification
# ============================================================

print("\n## L'(E,1) verification")
h = mpf('1e-7')

def L_E_product(s, K=1000):
    result = mpc(1)
    for p in primes_up_to_1000:
        if p > K:
            break
        if p == 37:
            continue
        ap_val = mpf(ap[p])
        p_s = mpmath.power(mpf(p), -s)
        p_2s = mpmath.power(mpf(p), 1 - 2*s)
        result = result / (1 - ap_val * p_s + p_2s)
    return result

L1 = L_E_product(mpf(1))
L1h = L_E_product(mpf(1) + h)
Lprime_numerical = re((L1h - L1) / h)

print(f"  L(1,E) via Euler product (p<=1000):    {float(re(L1)):.8f}")
print(f"  L'(E,1) finite difference (p<=1000):   {float(Lprime_numerical):.8f}")
print(f"  Known L'(E,1):                          0.30599977383")
print(f"  Ratio (computed/known):                 {float(Lprime_numerical)/0.30599977383:.6f}")
print(f"  Note: truncation at p=1000 underestimates L(1,E); need primes to ~10^6 for 6-digit accuracy")

# ============================================================
# Step 6: Richardson extrapolation D_500, D_1000
# ============================================================

print("\n## Richardson extrapolation")
D500 = D_K_values[500]
D1000 = D_K_values[1000]

# Model: D_K = D_inf + C/log(K)
# => D_inf = (D_1000*log(1000) - D_500*log(500)) / (log(1000) - log(500))
log500 = log(mpf(500))
log1000 = log(mpf(1000))
D_inf_rich = (D1000 * log1000 - D500 * log500) / (log1000 - log500)
D_inf_zeta2 = D_inf_rich * zeta2

print(f"  |D_500|  = {float(fabs(D500)):.6f}")
print(f"  |D_1000| = {float(fabs(D1000)):.6f}")
print(f"  D_inf (Richardson) = {complex(float(re(D_inf_rich)), float(im(D_inf_rich)))}")
print(f"  |D_inf * zeta(2)|  = {float(fabs(D_inf_zeta2)):.6f}")
print(f"  arg(D_inf)         = {float(arg(D_inf_rich)):.6f}")
print(f"\n  NDC universality predicts: |D_inf * zeta(2)| -> 1")
print(f"  Richardson estimate:        {float(fabs(D_inf_zeta2)):.6f}")
dev = abs(float(fabs(D_inf_zeta2)) - 1.0)
print(f"  Deviation from 1:           {dev:.6f}")
if dev < 0.5:
    print("  STATUS: Consistent with NDC universality at GL(2) zero")
else:
    print("  STATUS: Large deviation — convergence may require K >> 1000")

print("\n## Conclusion")
print(f"  Curve: 37a1 (y^2+y=x^3-x), rank 1, conductor 37")
print(f"  Zero tested: rho_E = 0.5 + 5.003838972i (first nontrivial zero of L(E,s))")
print(f"  K=1000:  |D_K^E * zeta(2)| = {float(fabs(D_K_values[1000]*zeta2)):.6f}")
print(f"  Richardson: |D_inf^E * zeta(2)| = {float(fabs(D_inf_zeta2)):.6f}")
print(f"  c_K^E.re/log(K) at K=1000 = {float(re(D_K_values[1000]/E_K)):.4f} (target: {float(inv_Lprime):.4f})")
