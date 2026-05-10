#!/usr/bin/env python3
"""Cross-check: directly compute c_K (Mobius) and D_K = c_K * E_K and
compare |D_K * zeta(2)| vs Saar's empirical claim ~= 1, and
|D_K * e^gamma| vs the Aoki-Koyama prediction ~= 1."""
import mpmath as mp
mp.mp.dps = 40

def chi_m4(n):
    return {1: mp.mpf(1), 3: mp.mpf(-1)}.get(n%4, mp.mpf(0))

def primes_up_to(N):
    sv = bytearray([1])*(N+1); sv[0]=sv[1]=0
    for i in range(2, int(N**0.5)+1):
        if sv[i]:
            for j in range(i*i,N+1,i): sv[j]=0
    return [i for i,v in enumerate(sv) if v]

def L_chi_m4(s):
    s = mp.mpc(s)
    return mp.power(4,-s)*(mp.zeta(s, mp.mpf(1)/4) - mp.zeta(s, mp.mpf(3)/4))

def Lp_chi_m4(s, eps=mp.mpf('1e-12')):
    return (L_chi_m4(s+eps)-L_chi_m4(s-eps))/(2*eps)

def find_zero(t):
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(t))
    for _ in range(50):
        f = L_chi_m4(s); fp = Lp_chi_m4(s)
        s = s - f/fp
    return s

def mobius_chi_sieve(N, chi):
    """Compute mu(n)*chi(n)*n^{-rho} sum incrementally; needs full mu values."""
    # Standard Mobius sieve:
    mu = [1]*(N+1)
    pr = primes_up_to(N)
    for p in pr:
        for j in range(p, N+1, p):
            mu[j] = -mu[j]
        for j in range(p*p, N+1, p*p):
            mu[j] = 0
    return mu

def main():
    N = 2_000_000
    print(f'mp.mp.dps={mp.mp.dps}, N={N}')
    rho = find_zero(mp.mpf('6.020948668'))
    print(f'rho = {mp.nstr(rho,30)}')
    Lp = Lp_chi_m4(rho)
    print(f"L'(rho) = {mp.nstr(Lp,18)}")
    # Mobius sieve
    print('Sieving Mobius...')
    mu = mobius_chi_sieve(N, chi_m4)
    # primes
    print('Sieving primes...')
    pr = primes_up_to(N)

    Ks = [int(K) for K in [1e4,3e4,1e5,3e5,1e6,2e6]]
    egam = mp.exp(mp.euler)
    z2 = mp.zeta(2)
    Cak = abs(Lp/egam); Cs = abs(Lp/z2)

    # Incremental c_K and E_K
    cK = mp.mpc(0)
    Ek = mp.mpc(1)
    n_idx = 1
    p_idx = 0
    print()
    h7 = "|EK*logK|/(L_p/eg)"
    h8 = "|EK*logK|/(L_p/z2)"
    hdr = f"{'K':>9} {'|c_K|':>14} {'|E_K|':>14} {'|D_K|':>10} {'|DK|*zeta(2)':>13} {'|DK|*e^gam':>11} {h7:>20} {h8:>20}"
    print(hdr)
    for K in Ks:
        # update c_K up to K
        while n_idx <= K:
            cn = chi_m4(n_idx)
            if cn != 0 and mu[n_idx] != 0:
                cK = cK + mp.mpc(mu[n_idx]) * cn * mp.power(n_idx, -rho)
            n_idx += 1
        # update E_K up to primes <=K
        while p_idx < len(pr) and pr[p_idx] <= K:
            p = pr[p_idx]; p_idx += 1
            cp = chi_m4(p)
            if cp != 0:
                Ek = Ek / (mp.mpc(1) - cp*mp.power(p, -rho))
        DK = cK * Ek
        ElK = Ek * mp.log(K)
        print(f'{K:>9} {mp.nstr(abs(cK),10):>14} {mp.nstr(abs(Ek),10):>14} {mp.nstr(abs(DK),8):>10} {mp.nstr(abs(DK)*z2,8):>13} {mp.nstr(abs(DK)*egam,8):>11} {mp.nstr(abs(ElK)/Cak,8):>20} {mp.nstr(abs(ElK)/Cs,8):>20}')

if __name__=='__main__':
    main()
