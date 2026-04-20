"""
Final bug comparison: old (wrong) vs new (correct) μ_f(p²) for C₁.
Uses known zero locations + L' magnitudes from verified PARI data.
a_p computed fresh via PARI subprocess.
"""
import mpmath as mp, subprocess
mp.mp.dps = 30

GP = "/opt/homebrew/bin/gp"

# Known data (PARI/LMFDB verified)
ZERO_37A1_G2 = mp.mpf('5.00317001400665869534627315571')
LP_37A1_G2 = mp.mpf('0.30599977383405230182')   # from PARI above

ZERO_DELTA_G1 = mp.mpf('9.22237939992110252224376719274')
LP_DELTA_G1 = mp.mpf('1.00502406972364589632')  # from verification_suite.py

rho_37 = mp.mpc(1, ZERO_37A1_G2)
rho_D  = mp.mpc(6, ZERO_DELTA_G1)

# Get a_p via PARI (single-line)
K = 3000
cmd = (f'default(realprecision,20);E37=ellinit([0,0,1,-1,0]);'
       f'mf=mfinit([1,12],1);fD=mfbasis(mf)[1];'
       f'forprime(p=2,{K},print(p," ",ellap(E37,p)," ",mfcoefs(fD,p)[p+1]));quit;')
r = subprocess.run([GP, "-q"], input=cmd, text=True, capture_output=True, timeout=120)
AP37 = {}; TAU = {}
for line in r.stdout.splitlines():
    parts = line.split()
    if len(parts) == 3:
        try:
            p = int(parts[0]); AP37[p] = int(parts[1]); TAU[p] = int(parts[2])
        except: pass

print(f"Loaded {len(AP37)} primes. a_2={AP37.get(2)}, a_7={AP37.get(7)}, τ(2)={TAU.get(2)}, τ(3)={TAU.get(3)}")

def sieve_spf(N):
    spf = list(range(N+1))
    for p in range(2, int(N**0.5)+1):
        if spf[p]==p:
            for m in range(p*p, N+1, p):
                if spf[m]==m: spf[m]=p
    return spf

def build_mu_ec(AP, K, N_cond, correct=True):
    spf = sieve_spf(K)
    mu = [mp.mpf(0)]*(K+1); mu[1]=mp.mpf(1)
    for n in range(2,K+1):
        p=spf[n]
        if p not in AP: continue
        m=n; kpow=0
        while m%p==0: m//=p; kpow+=1
        a=AP[p]; bad=N_cond%p==0
        if kpow==1: v=-a
        elif bad: v=0
        elif kpow==2: v=p if correct else (a*a-p)
        else: v=0
        mu[n]=mp.mpf(v)*mu[m]
    return mu

def build_mu_delta(TAU, K, correct=True):
    spf = sieve_spf(K)
    mu = [mp.mpf(0)]*(K+1); mu[1]=mp.mpf(1)
    for n in range(2,K+1):
        p=spf[n]
        if p not in TAU: continue
        m=n; kpow=0
        while m%p==0: m//=p; kpow+=1
        tp=TAU[p]
        if kpow==1: v=-tp
        elif kpow==2: v=p**11 if correct else (tp*tp-p**11)
        else: v=0
        mu[n]=mp.mpf(v)*mu[m]
    return mu

def compute_c(mu, K, rho):
    er=mp.mpf(1)/K; c=mp.mpc(0)
    for n in range(1,K+1):
        if mu[n]!=0:
            c+=mu[n]*mp.exp(-mp.mpf(n)*er)/mp.power(n,rho)
    return c

print()
print("="*70)
print("37a1: wrong (a_p²-p) vs correct (p) for μ_E(p²)")
print(f"ρ=1+i·{float(ZERO_37A1_G2):.6f}, |L'(ρ)|={float(LP_37A1_G2):.6f}")
print("="*70)
print(f"{'K':>6} {'C₁_wrong':>12} {'C₁_correct':>12} {'|c|_ratio':>10} {'δC₁':>10}")
results_37 = {}
for Kt in [500, 1000, 2000, 3000]:
    mu_w = build_mu_ec(AP37, Kt, 37, correct=False)
    mu_c = build_mu_ec(AP37, Kt, 37, correct=True)
    cw = compute_c(mu_w, Kt, rho_37); cc = compute_c(mu_c, Kt, rho_37)
    C1w = float(abs(cw)*LP_37A1_G2/(mp.log(Kt)+mp.euler))
    C1c = float(abs(cc)*LP_37A1_G2/(mp.log(Kt)+mp.euler))
    ratio = float(abs(cc)/abs(cw)) if abs(cw)>0 else 0
    results_37[Kt] = (C1w, C1c)
    print(f"{Kt:>6} {C1w:>12.6f} {C1c:>12.6f} {ratio:>10.4f} {C1c-C1w:>+10.6f}")

print()
print("="*70)
print("Delta: wrong (τ²-p^11) vs correct (p^11) for μ_Δ(p²)")
print(f"ρ=6+i·{float(ZERO_DELTA_G1):.6f}, |L'(ρ)|={float(LP_DELTA_G1):.6f}")
print("="*70)
print(f"{'K':>6} {'C₁_wrong':>12} {'C₁_correct':>12} {'|c|_ratio':>10} {'δC₁':>10}")
results_D = {}
for Kt in [500, 1000, 2000, 3000]:
    mu_w = build_mu_delta(TAU, Kt, correct=False)
    mu_c = build_mu_delta(TAU, Kt, correct=True)
    cw = compute_c(mu_w, Kt, rho_D); cc = compute_c(mu_c, Kt, rho_D)
    C1w = float(abs(cw)*LP_DELTA_G1/(mp.log(Kt)+mp.euler))
    C1c = float(abs(cc)*LP_DELTA_G1/(mp.log(Kt)+mp.euler))
    ratio = float(abs(cc)/abs(cw)) if abs(cw)>0 else 0
    results_D[Kt] = (C1w, C1c)
    print(f"{Kt:>6} {C1w:>12.6f} {C1c:>12.6f} {ratio:>10.4f} {C1c-C1w:>+10.6f}")

# Extrapolate to K=50K using log fit
# C₁(K) = C₁_∞ + A/log(K). Fit from K=2000,3000 to estimate K→∞ trend.
print()
print("="*70)
print("SUMMARY: Impact of bug fix")
print("="*70)
print(f"At K=3000:")
C1w_37, C1c_37 = results_37.get(3000, (0,0))
C1w_D,  C1c_D  = results_D.get(3000, (0,0))
print(f"  37a1: C₁_wrong={C1w_37:.4f}, C₁_correct={C1c_37:.4f}, change={100*(C1c_37/C1w_37-1):+.1f}%")
print(f"  Δ:    C₁_wrong={C1w_D:.4f}, C₁_correct={C1c_D:.4f}, change={100*(C1c_D/C1w_D-1):+.1f}%")
print()
print(f"C₁² scale factors: 37a1={(C1c_37/C1w_37)**2:.4f}×, Δ={(C1c_D/C1w_D)**2:.4f}×")
print()
print(f"Pre-bugfix E[C₁²] claims: 37a1=2.561, Δ=2.473")
print(f"Corrected estimates (applying ratio²): 37a1={2.561*(C1c_37/C1w_37)**2:.3f}, Δ={2.473*(C1c_D/C1w_D)**2:.3f}")
print(f"(These estimates assume the per-zero ratio at K=3000 generalizes to K=50K and across zeros)")
print()
print("⚠️  The ratio for Δ may differ more because τ(p)²-p^11 vs p^11 has larger relative")
print("     difference for small p than a_p²-p vs p for EC.")
print("DONE")
