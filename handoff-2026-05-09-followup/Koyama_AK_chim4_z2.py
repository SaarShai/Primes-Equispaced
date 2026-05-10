#!/usr/bin/env python3
"""Test for chi_{-4} at the SECOND zero, t ~= 10.244."""
import mpmath as mp
mp.mp.dps = 30

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
                if spf[j]==0: spf[j]=i
    return spf

def L_chi_m4(s):
    s = mp.mpc(s)
    return mp.power(4,-s) * (mp.zeta(s, mp.mpf(1)/4) - mp.zeta(s, mp.mpf(3)/4))

def Lp_chi_m4(s, eps=mp.mpf('1e-10')):
    return (L_chi_m4(s+eps)-L_chi_m4(s-eps))/(2*eps)

def find_zero(t):
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(t))
    for _ in range(50):
        f = L_chi_m4(s); fp = Lp_chi_m4(s)
        s = s - f/fp
    return s

def main():
    N = int(2e6)
    rho = find_zero(mp.mpf('10.243770'))
    print(f'rho_chi_-4_z2 = {mp.nstr(rho, 25)}')
    print(f'L(rho) = {mp.nstr(L_chi_m4(rho), 12)}')
    Lp = Lp_chi_m4(rho); aLp = abs(Lp)
    print(f"|L'(rho)| = {mp.nstr(aLp, 18)}")
    egam = mp.exp(mp.euler); z2 = mp.zeta(2)
    Cak = aLp/egam; Cs = aLp/z2

    spf = smallest_prime_factor(N)
    pr = primes_up_to(N)
    def mu_of(n, spf):
        if n==1: return 1
        s=1
        while n>1:
            p=spf[n]; n//=p
            if n%p==0: return 0
            s=-s
        return s

    cK = mp.mpc(0); Ek = mp.mpc(1)
    p_idx = 0
    Ks = [int(K) for K in [1e4,1e5,1e6,2e6]]
    Kix = 0
    print(f"{'K':>9} {'|D_K|':>10} {'|EK*logK|':>12} {'/Cak (AK)':>10} {'/Cs (Saar)':>10}")
    for n in range(1, N+1):
        cn = chi_m4(n)
        if cn != 0:
            mu = mu_of(n, spf)
            if mu != 0:
                cK = cK + mp.mpc(mu) * mp.mpc(cn) * mp.power(n, -rho)
        if Kix < len(Ks) and n == Ks[Kix]:
            while p_idx < len(pr) and pr[p_idx] <= n:
                p = pr[p_idx]; p_idx += 1
                cp = chi_m4(p)
                if cp != 0:
                    Ek = Ek / (mp.mpc(1) - mp.mpc(cp) * mp.power(p, -rho))
            DK = cK * Ek
            ElK = Ek * mp.log(n)
            print(f'{n:>9} {mp.nstr(abs(DK),8):>10} {mp.nstr(abs(ElK),10):>12} {mp.nstr(abs(ElK)/Cak,7):>10} {mp.nstr(abs(ElK)/Cs,7):>10}')
            Kix += 1

if __name__=='__main__':
    main()
