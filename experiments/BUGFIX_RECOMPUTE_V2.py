"""
Recompute C₁ comparison (wrong vs correct μ_f(p²)) using PARI for a_p via stdin.
"""
import mpmath as mp, subprocess, sys
mp.mp.dps = 30

GP = "/opt/homebrew/bin/gp"

def gp_run(cmd, timeout=120):
    r = subprocess.run([GP, "-q"], input=cmd, text=True, capture_output=True, timeout=timeout)
    return r.stdout, r.stderr

# Get a_p for 37a1 and tau(p) for Delta up to K=5000
K = 5000
print(f"Fetching a_p (37a1, 389a1) and τ(p) (Δ) for p≤{K} via PARI...")

cmd = (
    "default(realprecision,20);"
    "E37=ellinit([0,0,1,-1,0]);"
    "E389=ellinit([0,1,1,-2,0]);"
    "mf=mfinit([1,12],1);fD=mfbasis(mf)[1];"
    f"forprime(p=2,{K},"
    'printf("AP %d %d %d %d\\n",p,ellap(E37,p),ellap(E389,p),mfcoefs(fD,p)[p+1]));'
    "quit;"
)
out, err = gp_run(cmd, timeout=300)
if err.strip():
    print(f"PARI errors: {err[:500]}")

AP37 = {}; AP389 = {}; TAU = {}
for line in out.splitlines():
    parts = line.split()
    if len(parts) == 5 and parts[0] == "AP":
        p = int(parts[1])
        AP37[p] = int(parts[2])
        AP389[p] = int(parts[3])
        TAU[p] = int(parts[4])
print(f"Got {len(AP37)} primes")

# Spot check
print(f"  a_2(37a1)={AP37.get(2)}, a_3={AP37.get(3)}, a_7={AP37.get(7)}")
print(f"  τ(2)={TAU.get(2)}, τ(3)={TAU.get(3)}")

# Fetch first zero and |L'| for each curve
print("\nFetching zeros and L' values via PARI...")
cmd2 = (
    "default(realprecision,25);"
    "default(parisizemax,2*10^9);"
    "E37=ellinit([0,0,1,-1,0]);L37=lfuninit(E37,[1,60]);"
    "z37=lfunzeros(L37,60);"
    "for(i=1,min(5,#z37),rho=1+I*z37[i];lp=lfun(L37,rho,1);"
    'printf("Z37 %.20f %.20f\\n",real(z37[i]),abs(lp)));'
    "mf=mfinit([1,12],1);fD=mfbasis(mf)[1];LD=lfuninit(lfunmf(mf,fD),[6,60]);"
    "zD=lfunzeros(LD,60);"
    "for(i=1,min(5,#zD),rho=6+I*zD[i];lp=lfun(LD,rho,1);"
    'printf("ZD %.20f %.20f\\n",real(zD[i]),abs(lp)));'
    "quit;"
)
out2, err2 = gp_run(cmd2, timeout=120)
if err2.strip(): print(f"PARI err2: {err2[:300]}")

zeros_37 = []; LP_37 = []; zeros_D = []; LP_D = []
for line in out2.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[0] == "Z37":
        zeros_37.append(mp.mpf(parts[1])); LP_37.append(mp.mpf(parts[2]))
    elif len(parts) == 3 and parts[0] == "ZD":
        zeros_D.append(mp.mpf(parts[1])); LP_D.append(mp.mpf(parts[2]))

print(f"Got {len(zeros_37)} 37a1 zeros, {len(zeros_D)} Delta zeros")
if zeros_37: print(f"  37a1 first zero: γ={float(zeros_37[0]):.6f}, |L'|={float(LP_37[0]):.6f}")
if zeros_D: print(f"  Delta first zero: γ={float(zeros_D[0]):.6f}, |L'|={float(LP_D[0]):.6f}")

if not zeros_37 or not zeros_D:
    print("ERROR: No zeros. Aborting.")
    sys.exit(1)

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

# ---- 37a1 comparison ----
print("\n" + "="*70)
print("37a1: correct vs wrong μ_E(p²)")
print("="*70)
rho37 = mp.mpc(1, zeros_37[0]); lp37 = LP_37[0]
print(f"γ={float(zeros_37[0]):.6f}, |L'|={float(lp37):.6f}")
print(f"{'K':>6} {'C₁_wrong':>12} {'C₁_correct':>12} {'ratio':>8}")
for Kt in [200, 500, 1000, 2000, 5000]:
    mu_w = build_mu_ec(AP37, Kt, 37, correct=False)
    mu_c = build_mu_ec(AP37, Kt, 37, correct=True)
    cw = compute_c(mu_w, Kt, rho37); cc = compute_c(mu_c, Kt, rho37)
    C1w = float(abs(cw)*lp37/(mp.log(Kt)+mp.euler))
    C1c = float(abs(cc)*lp37/(mp.log(Kt)+mp.euler))
    ratio = float(abs(cc)/abs(cw)) if abs(cw)>0 else 0
    print(f"{Kt:>6} {C1w:>12.6f} {C1c:>12.6f} {ratio:>8.4f}")

# ---- Delta comparison ----
print("\n" + "="*70)
print("Delta: correct vs wrong μ_Δ(p²)")
print("="*70)
rhoD = mp.mpc(6, zeros_D[0]); lpD = LP_D[0]
print(f"γ={float(zeros_D[0]):.6f}, |L'|={float(lpD):.6f}")
print(f"{'K':>6} {'C₁_wrong':>12} {'C₁_correct':>12} {'ratio':>8}")
for Kt in [200, 500, 1000, 2000]:
    mu_w = build_mu_delta(TAU, Kt, correct=False)
    mu_c = build_mu_delta(TAU, Kt, correct=True)
    cw = compute_c(mu_w, Kt, rhoD); cc = compute_c(mu_c, Kt, rhoD)
    C1w = float(abs(cw)*lpD/(mp.log(Kt)+mp.euler))
    C1c = float(abs(cc)*lpD/(mp.log(Kt)+mp.euler))
    ratio = float(abs(cc)/abs(cw)) if abs(cw)>0 else 0
    print(f"{Kt:>6} {C1w:>12.6f} {C1c:>12.6f} {ratio:>8.4f}")

print("\nDONE — C₁ values at these K tell us how wrong the pre-bugfix results were.")
print("Save as BUGFIX_MU_P2_RECOMPUTE.md")
