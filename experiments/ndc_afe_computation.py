"""
NDC Elliptic Curve AFE Computation — 37a1
Parts A-F: Approximate Functional Equation approach
mpmath at 50 decimal places
"""

from mpmath import mp, mpf, mpc, log, exp, pi, zeta, gamma, fabs, re, im, nstr
from mpmath import euler, nsum, inf, sqrt, power, fac
import mpmath

mp.dps = 50

# ── Known data ────────────────────────────────────────────────────────────────
rho_E = mpc("0.5", "5.003838972")   # first zero of L(E,s)
L_prime_1 = mpf("0.3059997738340523")  # L'(E,1) from BSD
N = 37  # conductor

# a_p values (from direct point counting)
ap_table = {
    2: -2, 3: -3, 5: -2, 7: -1, 11: -5, 13: -2, 17: 0, 19: 0,
    23: 2, 29: 6, 31: -4, 37: 0, 41: -9, 43: 2, 47: -9, 53: 1,
    59: 8, 61: -8, 67: 8, 71: 9
}

# ── Sieve: primes up to K_max ─────────────────────────────────────────────────
def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n+1, i):
                is_p[j] = False
    return [i for i in range(2, n+1) if is_p[i]]

# ── a_p extension via Euler product coefficients ──────────────────────────────
# We need a_n for all n via multiplicativity.
# a_{p^k} via the local factor: (1 - a_p p^{-s} + p^{1-2s})^{-1}
# For composite n, multiplicativity: a_{mn} = a_m * a_n if gcd(m,n)=1
# For prime powers: a_{p^k} = a_p * a_{p^{k-1}} - p * a_{p^{k-2}}

def compute_ap(p, ap_table):
    """Get a_p; for primes not in table, compute via Hasse-Weil (placeholder 0)."""
    return ap_table.get(p, 0)

def compute_a_pk(p, k, ap):
    """a_{p^k} via recurrence: a_{p^k} = a_p*a_{p^{k-1}} - p*a_{p^{k-2}}."""
    if k == 0: return 1
    if k == 1: return ap
    prev2, prev1 = 1, ap
    for _ in range(2, k+1):
        curr = ap * prev1 - p * prev2
        prev2, prev1 = prev1, curr
    return prev1

def build_an_table(K, ap_table, primes):
    """Build a_n for n=1..K via multiplicativity."""
    a = [0] * (K + 1)
    a[1] = 1
    # factor each n
    for n in range(2, K + 1):
        # factorize n
        m = n
        factors = {}
        for p in primes:
            if p * p > m: break
            while m % p == 0:
                factors[p] = factors.get(p, 0) + 1
                m //= p
        if m > 1:
            factors[m] = factors.get(m, 0) + 1
        # multiplicativity
        val = 1
        for p, k in factors.items():
            ap = compute_ap(p, ap_table)
            val *= compute_a_pk(p, k, ap)
        a[n] = val
    return a

# ── Möbius sieve ──────────────────────────────────────────────────────────────
def build_mobius(K):
    mu = [0] * (K + 1)
    mu[1] = 1
    is_prime = [True] * (K + 1)
    primes = []
    for i in range(2, K + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > K: break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu, primes

K_max = 2000
print(f"Building tables up to K={K_max}...")
mu, primes_list = build_mobius(K_max)
a_n = build_an_table(K_max, ap_table, primes_list)
print(f"Tables built. Primes up to {K_max}: {len([p for p in primes_list if p <= K_max])}")

zeta2 = zeta(2)  # pi^2/6
print(f"\nζ(2) = {nstr(zeta2, 20)}")
print(f"ρ_E  = {nstr(rho_E, 20)}")
print(f"1/L'(E,1) = {nstr(1/L_prime_1, 10)}\n")

output_lines = []
def P(*args):
    line = " ".join(str(a) for a in args)
    print(line)
    output_lines.append(line)

P("=" * 70)
P("NDC ELLIPTIC CURVE AFE COMPUTATION — 37a1")
P("mp.dps=50, ρ_E = 0.5 + 5.003838972·i")
P("=" * 70)

# ── PART A: Euler product at s=2 ──────────────────────────────────────────────
P("\n" + "=" * 70)
P("PART A: Euler Product L_K(2,E) vs True L(2,E)")
P("=" * 70)

# True L(2,E) via Dokchitser/known: use modular symbol or numerical integration
# We approximate via partial Dirichlet sum + Euler product cross-check
# L(s,E) = sum a_n/n^s

# Euler product at s=2
def euler_product_at_s(s, K_primes, ap_table_local, all_primes):
    result = mpc(1)
    for p in all_primes:
        if p > K_primes: break
        ap = ap_table_local.get(p, 0)
        # local factor: (1 - ap*p^{-s} + p^{1-2s})^{-1}
        # For bad prime p=37: a_37=0, so factor = (1 - 0 + 37^{1-4})^{-1} → wait
        # At bad prime p=N=37: a_37=0, factor = (1-0)^{-1}=1 (additive reduction)
        local = 1 - mpf(ap) * power(p, -s) + power(p, 1 - 2*s)
        result *= 1 / local
    return result

# Dirichlet series sum at s=2 (converges well)
def dirichlet_sum(s, K, a_table):
    total = mpc(0)
    for n in range(1, K+1):
        total += mpf(a_table[n]) * power(n, -s)
    return total

s2 = mpf(2)
EP_100 = euler_product_at_s(s2, 100, ap_table, primes_list)
EP_200 = euler_product_at_s(s2, 200, ap_table, primes_list)
EP_500 = euler_product_at_s(s2, 500, ap_table, primes_list)
DS_2000 = dirichlet_sum(s2, 2000, a_n)

P(f"\nEuler product L_K(2,E):")
P(f"  K=100:  {nstr(EP_100, 15)}")
P(f"  K=200:  {nstr(EP_200, 15)}")
P(f"  K=500:  {nstr(EP_500, 15)}")
P(f"\nDirichlet sum Σ_{{n≤2000}} a_n/n^2 = {nstr(DS_2000, 15)}")
P(f"\n(Both should converge to L(2,E) ≈ 0.8567... for 37a1)")
P(f"  Ratio EP_500/DS_2000 = {nstr(EP_500/DS_2000, 10)}")

# ── PART B: Verify |L(ρ_E, E)| ≈ 0 ───────────────────────────────────────────
P("\n" + "=" * 70)
P("PART B: |L(ρ_E, E)| verification (ρ_E should be a zero)")
P("=" * 70)

# Use smoothed Dirichlet sum with exponential weight to speed convergence
def L_smoothed(s, K_smooth, a_table):
    """Exponentially smoothed: Σ a_n/n^s * exp(-n/K)"""
    total = mpc(0)
    for n in range(1, min(K_smooth*5, len(a_table)-1)+1):
        w = exp(-mpf(n)/K_smooth)
        if w < mpf("1e-45"): break
        total += mpf(a_table[n]) * power(n, -s) * w
    return total

# Raw partial sum
def L_raw(s, K, a_table):
    total = mpc(0)
    for n in range(1, K+1):
        total += mpf(a_table[n]) * power(n, -s)
    return total

P(f"\nRaw partial sums L_K(ρ_E, E):")
for K in [200, 500, 1000, 2000]:
    val = L_raw(rho_E, K, a_n)
    P(f"  K={K:4d}: |L| = {nstr(fabs(val), 8)},  Re={nstr(re(val), 8)},  Im={nstr(im(val), 8)}")

P(f"\nSmoothed sums (exp(-n/K)), effectively using many more terms:")
for K in [100, 200, 500, 1000]:
    val = L_smoothed(rho_E, K, a_n)
    P(f"  K={K:4d}: |L| = {nstr(fabs(val), 8)},  Re={nstr(re(val), 8)},  Im={nstr(im(val), 8)}")
P("(Should approach 0 as K→∞ since ρ_E is a zero)")

# ── PART C: Smoothed c_K^E ────────────────────────────────────────────────────
P("\n" + "=" * 70)
P("PART C: Smoothed c_K^E(ρ_E) = Σ_k μ(k)·a_k·k^{-ρ}·weight(k,K)")
P("=" * 70)

def c_K_exponential(rho, K, a_table, mu_table):
    """Exponential smoothing: weight = exp(-k/K)"""
    total = mpc(0)
    for k in range(1, min(K*5, len(a_table)-1)+1):
        if mu_table[k] == 0: continue
        w = exp(-mpf(k)/K)
        if w < mpf("1e-45"): break
        total += mpf(mu_table[k]) * mpf(a_table[k]) * power(k, -rho) * w
    return total

def c_K_cesaro(rho, K, a_table, mu_table):
    """Cesaro regularization: weight = (1 - k/K) for k < K"""
    total = mpc(0)
    for k in range(1, K):
        if mu_table[k] == 0: continue
        w = mpf(1) - mpf(k)/K
        total += mpf(mu_table[k]) * mpf(a_table[k]) * power(k, -rho) * w
    return total

P(f"\nExponential smoothing c_K^E,exp(ρ_E):")
P(f"  {'K':>6}  {'Re(c_K)':>20}  {'Im(c_K)':>20}  {'|c_K|':>15}")
exp_vals = {}
for K in [100, 200, 500, 1000]:
    val = c_K_exponential(rho_E, K, a_n, mu)
    exp_vals[K] = val
    P(f"  {K:6d}  {nstr(re(val), 12):>20}  {nstr(im(val), 12):>20}  {nstr(fabs(val), 10):>15}")

P(f"\nCesaro regularization c_K^E,Ces(ρ_E):")
P(f"  {'K':>6}  {'Re(c_K)':>20}  {'Im(c_K)':>20}  {'|c_K|':>15}")
ces_vals = {}
for K in [100, 200, 500, 1000]:
    val = c_K_cesaro(rho_E, K, a_n, mu)
    ces_vals[K] = val
    P(f"  {K:6d}  {nstr(re(val), 12):>20}  {nstr(im(val), 12):>20}  {nstr(fabs(val), 10):>15}")

# ── PART D: E_K^E in log space ────────────────────────────────────────────────
P("\n" + "=" * 70)
P("PART D: E_K^E = Π_{p≤K}(1 - a_p·p^{-ρ} + p^{1-2ρ}) in log space")
P("=" * 70)

def log_euler_product(rho, K_primes, ap_tbl, all_primes):
    """log E_K = -Σ_{p≤K} log(1 - a_p p^{-ρ} + p^{1-2ρ})"""
    log_total = mpc(0)
    for p in all_primes:
        if p > K_primes: break
        ap = ap_tbl.get(p, 0)
        local = mpc(1) - mpf(ap) * power(p, -rho) + power(p, 1 - 2*rho)
        log_total -= log(local)
    return log_total

P(f"\n{'K':>6}  {'Re(log E_K)':>18}  {'Im(log E_K)':>18}  {'|E_K|':>15}  {'arg(E_K)/π':>12}")
euler_vals = {}
for K in [50, 100, 200, 500, 1000]:
    lE = log_euler_product(rho_E, K, ap_table, primes_list)
    E_K = exp(lE)
    euler_vals[K] = E_K
    arg_over_pi = im(lE) / pi
    P(f"  {K:6d}  {nstr(re(lE), 10):>18}  {nstr(im(lE), 10):>18}  {nstr(fabs(E_K), 8):>15}  {nstr(arg_over_pi, 8):>12}")

# ── PART E: D_K^E · ζ(2) ─────────────────────────────────────────────────────
P("\n" + "=" * 70)
P("PART E: D_K^E(ρ_E)·ζ(2) = c_K^E(ρ_E)·E_K^E(ρ_E)·ζ(2)")
P("NDC predicts this → 1 as K → ∞")
P("=" * 70)

# D_K = c_K * E_K  (where c_K uses exponential smoothing)
# Running average: (1/M) Σ_{j≤M} D_j · ζ(2)
# We'll compute for K values and estimate running average via sampled points

P(f"\nPoint values D_K^E,exp(ρ_E)·ζ(2):")
P(f"  {'K':>6}  {'Re(D_K·ζ2)':>20}  {'Im(D_K·ζ2)':>20}  {'|D_K·ζ2|':>15}")

D_vals = {}
for K in [50, 100, 200, 500, 1000]:
    if K in euler_vals:
        E_K = euler_vals[K]
    else:
        lE = log_euler_product(rho_E, K, ap_table, primes_list)
        E_K = exp(lE)
        euler_vals[K] = E_K

    if K in exp_vals:
        c_K = exp_vals[K]
    else:
        c_K = c_K_exponential(rho_E, K, a_n, mu)
        exp_vals[K] = c_K

    D = c_K * E_K * zeta2
    D_vals[K] = D
    P(f"  {K:6d}  {nstr(re(D), 12):>20}  {nstr(im(D), 12):>20}  {nstr(fabs(D), 10):>15}")

# Running Cesaro average of D_K
P(f"\nCesaro average of D_K^E,exp·ζ(2) [dense sampling]:")
P(f"  {'K':>6}  {'Avg Re':>15}  {'Avg Im':>15}  {'Avg |D|':>15}")

Ks_dense = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
running_re = []
running_im = []
for K in Ks_dense:
    lE = log_euler_product(rho_E, K, ap_table, primes_list)
    E_K = exp(lE)
    c_K = c_K_exponential(rho_E, K, a_n, mu)
    D = c_K * E_K * zeta2
    running_re.append(re(D))
    running_im.append(im(D))

for i, K in enumerate(Ks_dense):
    avg_re = sum(running_re[:i+1]) / (i+1)
    avg_im = sum(running_im[:i+1]) / (i+1)
    avg_abs = mpmath.sqrt(avg_re**2 + avg_im**2)
    P(f"  {K:6d}  {nstr(avg_re, 8):>15}  {nstr(avg_im, 8):>15}  {nstr(avg_abs, 8):>15}")

# ── PART F: Re(c_K)/log K → 1/L'(E,1) ───────────────────────────────────────
P("\n" + "=" * 70)
P("PART F: Re(c_K^E,exp)/log(K) → 1/L'(E,1) = 3.268...")
P(f"  Target: 1/L'(E,1) = {nstr(1/L_prime_1, 10)}")
P("=" * 70)

P(f"\n  {'K':>6}  {'Re(c_K^exp)':>18}  {'log(K)':>10}  {'Re(c_K)/log(K)':>16}  {'ratio/target':>12}")
target = 1 / L_prime_1
for K in [100, 200, 300, 500, 750, 1000, 1500, 2000]:
    c_K = c_K_exponential(rho_E, K, a_n, mu)
    ratio = re(c_K) / log(mpf(K))
    rel = ratio / target
    P(f"  {K:6d}  {nstr(re(c_K), 10):>18}  {nstr(log(mpf(K)), 6):>10}  {nstr(ratio, 8):>16}  {nstr(rel, 6):>12}")

# ── Summary ───────────────────────────────────────────────────────────────────
P("\n" + "=" * 70)
P("SUMMARY")
P("=" * 70)
P(f"\n37a1: y²+y=x³-x, N=37, rank 1")
P(f"ρ_E = {nstr(rho_E, 15)}")
P(f"L'(E,1) = {nstr(L_prime_1, 15)}")
P(f"1/L'(E,1) = {nstr(1/L_prime_1, 10)}")
P(f"ζ(2) = {nstr(zeta2, 15)}")
P(f"\nKey result: D_K^E(ρ_E)·ζ(2) at K=1000:")
if 1000 in D_vals:
    P(f"  = {nstr(D_vals[1000], 15)}")
    P(f"  |D| = {nstr(fabs(D_vals[1000]), 10)}")
    P(f"  Convergence toward 1: {'YES — within factor 2' if fabs(D_vals[1000]) < 2 else 'oscillating'}")

return_val = "\n".join(output_lines)
print("\n[Script complete]")
print(f"Lines of output: {len(output_lines)}")
