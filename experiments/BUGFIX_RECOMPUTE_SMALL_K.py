"""
Recompute C₁ comparison (correct vs wrong μ_f(p²)) using PARI for a_p.
Small K for speed. Enough to verify ratio and see if universality survives.
"""
import mpmath as mp, subprocess, json
from pathlib import Path
mp.mp.dps = 30

GP = "/opt/homebrew/bin/gp"

def run_gp(script, timeout=120):
    r = subprocess.run([GP, "-q"], input=script, text=True, capture_output=True, timeout=timeout)
    return r.stdout

# Get a_p for 37a1 up to K=5000 via PARI
K = 5000
print(f"Computing a_p for 37a1 and tau for Delta up to p≤sqrt({K})+1 = {int(K**0.5)+1} via PARI...")

# We need a_p for all primes up to K (for building mu table)
gp_script = f"""
\\p 20
E37 = ellinit([0,0,1,-1,0]);
mf = mfinit([1,12],1); fD = mfbasis(mf)[1];
for(p=2, {K},
    if(isprime(p),
        a37 = ellap(E37, p);
        td = mfcoefs(fD, p)[p+1];
        print("AP ", p, " ", a37, " ", td)
    )
);
quit;
"""
print("Running PARI...")
out = run_gp(gp_script, timeout=300)

AP37 = {}; TAU = {}
for line in out.splitlines():
    parts = line.split()
    if len(parts) == 4 and parts[0] == "AP":
        p = int(parts[1]); AP37[p] = int(parts[2]); TAU[p] = int(parts[3])
print(f"Got {len(AP37)} primes")

def sieve_spf(N):
    spf = list(range(N+1))
    for p in range(2, int(N**0.5)+1):
        if spf[p] == p:
            for m in range(p*p, N+1, p):
                if spf[m] == m: spf[m] = p
    return spf

def build_mu_ec(AP, K, N_cond, correct=True):
    spf = sieve_spf(K)
    mu = [mp.mpf(0)]*(K+1); mu[1]=mp.mpf(1)
    for n in range(2, K+1):
        p = spf[n]
        if p not in AP: continue
        m = n; kpow = 0
        while m % p == 0: m //= p; kpow += 1
        a = AP[p]; bad = N_cond % p == 0
        if kpow == 1: v = -a
        elif bad: v = 0
        elif kpow == 2: v = p if correct else (a*a - p)
        else: v = 0
        mu[n] = mp.mpf(v) * mu[m]
    return mu

def build_mu_delta(TAU, K, correct=True):
    spf = sieve_spf(K)
    mu = [mp.mpf(0)]*(K+1); mu[1]=mp.mpf(1)
    for n in range(2, K+1):
        p = spf[n]
        if p not in TAU: continue
        m = n; kpow = 0
        while m % p == 0: m //= p; kpow += 1
        tp = TAU[p]
        if kpow == 1: v = -tp
        elif kpow == 2: v = p**11 if correct else (tp*tp - p**11)
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

# Zeros and L' via PARI
print("\nFetching zeros and L' via PARI...")
gp_zero = f"""
\\p 25
default(parisizemax, 1*10^9);
E37 = ellinit([0,0,1,-1,0]);
L37 = lfuninit(E37, [1, 60]);
z37 = lfunzeros(L37, 60);
print("NZ37 ", #z37);
for(i=1, min(5, #z37), rho = 1 + I*z37[i]; lp = lfun(L37, rho, 1); print("Z37 ", z37[i], " ", abs(lp)));

mf = mfinit([1,12],1); fD = mfbasis(mf)[1];
LD = lfuninit(lfunmf(mf, fD), [6, 60]);
zD = lfunzeros(LD, 60);
print("NZD ", #zD);
for(i=1, min(5, #zD), rho = 6 + I*zD[i]; lp = lfun(LD, rho, 1); print("ZD ", zD[i], " ", abs(lp)));

quit;
"""
out2 = run_gp(gp_zero, timeout=120)
print(out2[:2000])

zeros_37 = []; LP_37 = []; zeros_D = []; LP_D = []
for line in out2.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[0] == "Z37":
        zeros_37.append(mp.mpf(parts[1])); LP_37.append(mp.mpf(parts[2]))
    elif len(parts) == 3 and parts[0] == "ZD":
        zeros_D.append(mp.mpf(parts[1])); LP_D.append(mp.mpf(parts[2]))

print(f"\nGot {len(zeros_37)} 37a1 zeros, {len(zeros_D)} Delta zeros")

if not zeros_37 or not zeros_D:
    print("ERROR: No zeros found. Check PARI output above.")
    exit(1)

# Use first 3 zeros for comparison
print("\n" + "="*70)
print("37a1: correct vs wrong μ_E(p²) at first zero")
print("="*70)
rho37_1 = mp.mpc(1, zeros_37[0])
lp37_1 = LP_37[0]
print(f"γ = {float(zeros_37[0]):.6f}, |L'(ρ)| = {float(lp37_1):.6f}")

for K_test in [500, 1000, 2000, 5000]:
    mu_w = build_mu_ec(AP37, K_test, 37, correct=False)
    mu_c = build_mu_ec(AP37, K_test, 37, correct=True)
    c_w = compute_c(mu_w, K_test, rho37_1)
    c_c = compute_c(mu_c, K_test, rho37_1)
    C1_w = float(abs(c_w)*lp37_1/(mp.log(K_test)+mp.euler))
    C1_c = float(abs(c_c)*lp37_1/(mp.log(K_test)+mp.euler))
    ratio = float(abs(c_c)/abs(c_w)) if abs(c_w)>0 else 999
    print(f"  K={K_test:>5}: C₁_wrong={C1_w:.6f}  C₁_correct={C1_c:.6f}  ratio={ratio:.4f}")

print("\n" + "="*70)
print("Delta: correct vs wrong μ_Δ(p²) at first zero")
print("="*70)
rhoD_1 = mp.mpc(6, zeros_D[0])
lpD_1 = LP_D[0]
print(f"γ = {float(zeros_D[0]):.6f}, |L'(ρ)| = {float(lpD_1):.6f}")

for K_test in [200, 500, 1000, 2000]:
    mu_w = build_mu_delta(TAU, K_test, correct=False)
    mu_c = build_mu_delta(TAU, K_test, correct=True)
    c_w = compute_c(mu_w, K_test, rhoD_1)
    c_c = compute_c(mu_c, K_test, rhoD_1)
    C1_w = float(abs(c_w)*lpD_1/(mp.log(K_test)+mp.euler))
    C1_c = float(abs(c_c)*lpD_1/(mp.log(K_test)+mp.euler))
    ratio = float(abs(c_c)/abs(c_w)) if abs(c_w)>0 else 999
    print(f"  K={K_test:>5}: C₁_wrong={C1_w:.6f}  C₁_correct={C1_c:.6f}  ratio={ratio:.4f}")

print("\n" + "="*70)
print("Are 37a1 and Delta E[C₁²] still similar after fix?")
print("Need full 500-zero ensemble to say definitively. Above shows per-zero impact.")
print("DONE")
