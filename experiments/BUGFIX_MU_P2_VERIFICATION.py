"""
BUGFIX verification: compare old (wrong) vs new (correct) μ_f(p²) coefficients.
Old: μ_E(p²) = a_p² - p (= a_{p²} via Hecke), μ_Δ(p²) = τ(p)² - p^11 (= τ(p²))
New: μ_E(p²) = p (from Euler factor), μ_Δ(p²) = p^11

Run at small K (K=1000) to quickly see C₁ change.
"""
import mpmath as mp, json, subprocess
from pathlib import Path
mp.mp.dps = 30

DATA_DIR = Path.home() / "farey_py_tasks" / "data"

def load_ap(curve):
    f = "ap_37a1_250k.json" if curve=="37a1" else "ap_389a1_250k.json"
    with open(DATA_DIR / f) as fh: return {int(k):v for k,v in json.load(fh).items()}

def load_tau():
    with open(DATA_DIR / "tau_delta_250k.json") as f: return {int(k):v for k,v in json.load(f).items()}

def build_mu_ec(AP, K, N_cond, correct=True):
    """correct=True: μ_E(p²)=p; correct=False: μ_E(p²)=a_p²-p (WRONG)"""
    primes_list = sorted(AP.keys())
    spf = list(range(K+1))
    for p in primes_list:
        if p*p > K: break
        if spf[p] == p:
            for m in range(p*p, K+1, p):
                if spf[m] == m: spf[m] = p
    mu = [mp.mpf(0)]*(K+1); mu[1]=mp.mpf(1)
    for n in range(2, K+1):
        p = spf[n]
        if p not in AP: continue
        m = n; kpow = 0
        while m % p == 0: m //= p; kpow += 1
        a = AP[p]
        bad = N_cond % p == 0
        if kpow == 1: v = -a
        elif bad: v = 0
        elif kpow == 2:
            v = p if correct else (a*a - p)  # KEY DIFFERENCE
        else: v = 0
        mu[n] = mp.mpf(v) * mu[m]
    return mu

def build_mu_delta(TAU, K, correct=True):
    """correct=True: μ_Δ(p²)=p^11; correct=False: μ_Δ(p²)=τ(p)²-p^11 (WRONG)"""
    primes_list = sorted(TAU.keys())
    spf = list(range(K+1))
    for p in primes_list:
        if p*p > K: break
        if spf[p] == p:
            for m in range(p*p, K+1, p):
                if spf[m] == m: spf[m] = p
    mu = [mp.mpf(0)]*(K+1); mu[1]=mp.mpf(1)
    for n in range(2, K+1):
        p = spf[n]
        if p not in TAU: continue
        m = n; kpow = 0
        while m % p == 0: m //= p; kpow += 1
        tp = TAU[p]
        if kpow == 1: v = -tp
        elif kpow == 2:
            v = p**11 if correct else (tp*tp - p**11)  # KEY DIFFERENCE
        else: v = 0
        mu[n] = mp.mpf(v) * mu[m]
    return mu

def compute_c(mu, K, rho):
    exp_rate = mp.mpf(1)/K
    c = mp.mpc(0)
    for n in range(1, K+1):
        if mu[n] != 0:
            c += mu[n] * mp.exp(-mp.mpf(n)*exp_rate) / mp.power(n, rho)
    return c

AP37 = load_ap("37a1")
TAU = load_tau()

# Load L' values for first zero of each
# 37a1 first zero γ_2 = 5.00317... (algebraic norm: ρ=1+5.00317i)
# Δ first zero γ_1 = 9.22237... (algebraic norm: ρ=6+9.22237i)
# L'(ρ,37a1) and L'(ρ,Δ) — load from PARI or use stored values

rho_37a1 = mp.mpc(1, mp.mpf('5.00317001400665869534627315571'))
rho_delta = mp.mpc(6, mp.mpf('9.22237939992110252224376719274'))

# Stored L' magnitudes from our previous computation
# 37a1 γ_2: |L'| stored in L_prime_500.json
try:
    with open(DATA_DIR / "L_prime_500.json") as f:
        LP_data = json.load(f)
    lp_37a1_g2 = mp.mpf(list(LP_data["37a1"].values())[0])  # first zero
    lp_delta_g1 = mp.mpf(list(LP_data["delta"].values())[0])  # first zero
    print(f"Loaded L': 37a1 γ₂ |L'|={float(lp_37a1_g2):.6f}, Δ γ₁ |L'|={float(lp_delta_g1):.6f}")
except Exception as e:
    print(f"Could not load L' data: {e}")
    lp_37a1_g2 = mp.mpf('0.3059')  # approximate fallback
    lp_delta_g1 = mp.mpf('1.0050')  # approximate fallback

print("\n" + "="*60)
print("37a1 COMPARISON: correct vs wrong μ_E(p²)")
print("="*60)
for K in [500, 2000, 10000]:
    mu_c = build_mu_ec(AP37, K, 37, correct=True)
    mu_w = build_mu_ec(AP37, K, 37, correct=False)
    c_c = compute_c(mu_c, K, rho_37a1)
    c_w = compute_c(mu_w, K, rho_37a1)
    C1_c = float(abs(c_c) * lp_37a1_g2 / (mp.log(K) + mp.euler))
    C1_w = float(abs(c_w) * lp_37a1_g2 / (mp.log(K) + mp.euler))
    print(f"  K={K:>6}: C₁(correct)={C1_c:.6f}  C₁(wrong)={C1_w:.6f}  diff={C1_c-C1_w:+.6f}")

print("\n" + "="*60)
print("Δ COMPARISON: correct vs wrong μ_Δ(p²)")
print("="*60)
for K in [500, 2000, 10000]:
    mu_c = build_mu_delta(TAU, K, correct=True)
    mu_w = build_mu_delta(TAU, K, correct=False)
    c_c = compute_c(mu_c, K, rho_delta)
    c_w = compute_c(mu_w, K, rho_delta)
    C1_c = float(abs(c_c) * lp_delta_g1 / (mp.log(K) + mp.euler))
    C1_w = float(abs(c_w) * lp_delta_g1 / (mp.log(K) + mp.euler))
    print(f"  K={K:>6}: C₁(correct)={C1_c:.6f}  C₁(wrong)={C1_w:.6f}  diff={C1_c-C1_w:+.6f}")

print("\nDONE — check how much E[C₁²] shifts between versions")
