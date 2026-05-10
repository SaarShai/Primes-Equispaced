#!/usr/bin/env python3
"""
Push K to 1e7 to discriminate L'/e^gamma vs L'/zeta(2) for the AK constant.
At K=1e7, log K ~ 16.12, so subleading C_1/log K ~ 0.03 — should be enough to
discriminate the 7.6% gap if the limits are stable.

To save memory we don't store mu[1..N]; instead we sieve mu only at chi-supported
n and accumulate c_K incrementally.
"""
import mpmath as mp
import sys, time
mp.mp.dps = 30  # 30 digits is enough at this scale; saves time

def chi_m4(n):
    return {1: 1, 3: -1}.get(n%4, 0)

def primes_up_to(N):
    sv = bytearray([1])*(N+1); sv[0]=sv[1]=0
    for i in range(2, int(N**0.5)+1):
        if sv[i]:
            sv[i*i::i] = bytearray(len(sv[i*i::i]))
    return [i for i,v in enumerate(sv) if v]

def smallest_prime_factor(N):
    spf = [0]*(N+1)
    for i in range(2, N+1):
        if spf[i]==0:
            for j in range(i, N+1, i):
                if spf[j]==0:
                    spf[j]=i
    return spf

def L_chi_m4(s):
    s = mp.mpc(s)
    return mp.power(4,-s) * (mp.zeta(s, mp.mpf(1)/4) - mp.zeta(s, mp.mpf(3)/4))

def Lp_chi_m4(s, eps=mp.mpf('1e-10')):
    return (L_chi_m4(s+eps)-L_chi_m4(s-eps))/(2*eps)

def find_zero(t):
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(t))
    for _ in range(40):
        f = L_chi_m4(s); fp = Lp_chi_m4(s)
        s = s - f/fp
    return s

def main():
    N = int(1e7)
    print(f'mp.mp.dps={mp.mp.dps}, N={N}', flush=True)
    rho = find_zero(mp.mpf('6.020948668'))
    print(f'rho = {mp.nstr(rho,25)}', flush=True)
    Lp = Lp_chi_m4(rho); aLp = abs(Lp)
    print(f"|L'(rho)| = {mp.nstr(aLp,18)}", flush=True)

    egam = mp.exp(mp.euler); z2 = mp.zeta(2)
    Cak = aLp/egam; Cs = aLp/z2
    pred_DK_eg = 1/egam   # AK
    pred_DK_z2 = 1/z2     # Saar
    print(f"Predict |D_K| -> 1/e^gamma = {float(pred_DK_eg):.6f} (AK)")
    print(f"Predict |D_K| -> 1/zeta(2) = {float(pred_DK_z2):.6f} (Saar)")
    print(flush=True)

    print('Building smallest-prime-factor sieve...', flush=True)
    t0 = time.time()
    spf = smallest_prime_factor(N)
    print(f'  done in {time.time()-t0:.1f}s', flush=True)

    # Compute mu(n) on the fly: factor n by spf, mu = 0 if any p^2 | n, else (-1)^{omega(n)}.
    def mu_of(n, spf):
        if n == 1: return 1
        s = 1
        while n > 1:
            p = spf[n]; n //= p
            if n % p == 0: return 0
            s = -s
        return s

    # primes
    print('Sieving primes...', flush=True)
    t0 = time.time()
    pr = primes_up_to(N)
    print(f'  {len(pr)} primes, {time.time()-t0:.1f}s', flush=True)

    # Iterate K through breakpoints, computing c_K and E_K incrementally.
    breakpts = [int(K) for K in [1e4,3e4,1e5,3e5,1e6,2e6,5e6,1e7]]
    cK = mp.mpc(0); Ek = mp.mpc(1)
    n_idx = 1; p_idx = 0

    print(f"{'K':>9} {'|c_K|':>14} {'|E_K|':>14} {'|D_K|':>10} {'|EK*logK|':>12} {'/Cak (AK)':>10} {'/Cs (Saar)':>10}", flush=True)
    t_walk = time.time()
    next_break = 0
    Ks = sorted(set(breakpts))
    Kix = 0
    last_print_t = time.time()
    for n in range(1, N+1):
        cn = chi_m4(n)
        if cn != 0:
            mu = mu_of(n, spf)
            if mu != 0:
                cK = cK + mp.mpc(mu) * mp.mpc(cn) * mp.power(n, -rho)
        # also handle prime n
        # We do prime-product separately by walking pr.
        if Kix < len(Ks) and n == Ks[Kix]:
            # advance prime product to Kx
            while p_idx < len(pr) and pr[p_idx] <= n:
                p = pr[p_idx]; p_idx += 1
                cp = chi_m4(p)
                if cp != 0:
                    Ek = Ek / (mp.mpc(1) - mp.mpc(cp) * mp.power(p, -rho))
            DK = cK * Ek
            ElK = Ek * mp.log(n)
            print(f'{n:>9} {mp.nstr(abs(cK),10):>14} {mp.nstr(abs(Ek),10):>14} {mp.nstr(abs(DK),8):>10} {mp.nstr(abs(ElK),10):>12} {mp.nstr(abs(ElK)/Cak,7):>10} {mp.nstr(abs(ElK)/Cs,7):>10}', flush=True)
            Kix += 1
        # progress
        if time.time()-last_print_t > 30:
            print(f'  ... at n={n}, t={time.time()-t_walk:.0f}s', flush=True, file=sys.stderr)
            last_print_t = time.time()

    print()
    print('Conclusion criterion:')
    print('  At K=1e7 the C_1/log K subleading is ~0.03; if |D_K| is centered around')
    print('  0.5615 +- 0.03  -> AK 2023 (1.4) confirmed: C(rho,chi) = L\'(rho)/e^gamma.')
    print('  If |D_K| is centered around 0.6079 +- 0.03  -> Saar conjecture confirmed.')

if __name__ == '__main__':
    main()
