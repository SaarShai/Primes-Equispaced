#!/usr/bin/env python3
"""Test for chi_{11} (order-10 complex character mod 11) at first zero t~=3.547.
Generator of (Z/11)* is 2 of order 10. chi_{11}(2) = exp(2*pi*i/10).
"""
import mpmath as mp
mp.mp.dps = 30

# d-table: power-of-2 index for n=1..10 mod 11
# 2^0=1, 2^1=2, 2^2=4, 2^3=8, 2^4=5, 2^5=10, 2^6=9, 2^7=7, 2^8=3, 2^9=6
DLOG_2_MOD11 = {1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9}

def chi11(n):
    nn = n % 11
    if nn == 0: return mp.mpc(0)
    d = DLOG_2_MOD11[nn]
    return mp.expj(2*mp.pi*d/10)

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

def L_chi11(s):
    s = mp.mpc(s)
    out = mp.mpc(0)
    for a in range(1, 11):
        out += chi11(a) * mp.zeta(s, mp.mpf(a)/11)
    return mp.power(11, -s) * out

def Lp_chi11(s, eps=mp.mpf('1e-10')):
    return (L_chi11(s+eps)-L_chi11(s-eps))/(2*eps)

def find_zero_chi11(t):
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(t))
    for _ in range(50):
        f = L_chi11(s); fp = Lp_chi11(s)
        s = s - f/fp
    return s

def main():
    N = int(2e6)
    print(f'mp.mp.dps={mp.mp.dps}, N={N}')
    rho = find_zero_chi11(mp.mpf('3.547'))
    print(f'rho_chi11 = {mp.nstr(rho, 25)}')
    print(f'L(rho, chi11) = {mp.nstr(L_chi11(rho), 12)} (should be ~0)')
    Lp = Lp_chi11(rho); aLp = abs(Lp)
    print(f"|L'(rho, chi11)| = {mp.nstr(aLp, 18)}")
    egam = mp.exp(mp.euler); z2 = mp.zeta(2)
    Cak = aLp/egam; Cs = aLp/z2
    print(f"AK pred  |E_K log K| -> |L'/e^gamma| = {mp.nstr(Cak, 10)}")
    print(f"Saar pred|E_K log K| -> |L'/zeta(2)| = {mp.nstr(Cs, 10)}")

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
        cn = chi11(n)
        if abs(cn) > 0:
            mu = mu_of(n, spf)
            if mu != 0:
                cK = cK + mp.mpc(mu) * cn * mp.power(n, -rho)
        if Kix < len(Ks) and n == Ks[Kix]:
            while p_idx < len(pr) and pr[p_idx] <= n:
                p = pr[p_idx]; p_idx += 1
                cp = chi11(p)
                if abs(cp) > 0:
                    Ek = Ek / (mp.mpc(1) - cp * mp.power(p, -rho))
            DK = cK * Ek
            ElK = Ek * mp.log(n)
            print(f'{n:>9} {mp.nstr(abs(DK),8):>10} {mp.nstr(abs(ElK),10):>12} {mp.nstr(abs(ElK)/Cak,7):>10} {mp.nstr(abs(ElK)/Cs,7):>10}')
            Kix += 1

if __name__=='__main__':
    main()
