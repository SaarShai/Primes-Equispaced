#!/usr/bin/env python3
"""Test the AK constant identification for the complex Dirichlet character chi_5 of
order 4 mod 5, at the zero of L(s, chi_5) at t ~= 6.184.
chi_5(n) = i^d(n) where d(1)=0, d(2)=1, d(4)=2, d(3)=3 (mod 5).
"""
import mpmath as mp
mp.mp.dps = 30

# Construct chi_5 (order-4 complex character mod 5)
# Generator: 2 mod 5 has order 4. chi_5(2) = i.
# chi_5(1)=1, chi_5(2)=i, chi_5(3)=chi(2^3)=i^3=-i, chi_5(4)=chi(2^2)=-1.
def chi5(n):
    nn = n % 5
    return {1: mp.mpc(1,0), 2: mp.mpc(0,1), 3: mp.mpc(0,-1), 4: mp.mpc(-1,0)}.get(nn, mp.mpc(0))

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

def L_chi5(s):
    s = mp.mpc(s)
    # L(s, chi5) = 5^{-s} sum_{a=1}^{4} chi5(a) zeta(s, a/5)
    return mp.power(5,-s) * (
        chi5(1)*mp.zeta(s, mp.mpf(1)/5) +
        chi5(2)*mp.zeta(s, mp.mpf(2)/5) +
        chi5(3)*mp.zeta(s, mp.mpf(3)/5) +
        chi5(4)*mp.zeta(s, mp.mpf(4)/5))

def Lp_chi5(s, eps=mp.mpf('1e-10')):
    return (L_chi5(s+eps)-L_chi5(s-eps))/(2*eps)

def find_zero_chi5(t):
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(t))
    for _ in range(40):
        f = L_chi5(s); fp = Lp_chi5(s)
        s = s - f/fp
    return s

def main():
    N = int(2e6)
    print(f'mp.mp.dps={mp.mp.dps}, N={N}')
    rho = find_zero_chi5(mp.mpf('6.184'))
    print(f'rho_chi5 = {mp.nstr(rho, 25)}')
    print(f'L(rho, chi5) = {mp.nstr(L_chi5(rho), 12)} (should be ~0)')
    Lp = Lp_chi5(rho); aLp = abs(Lp)
    print(f'|L\'(rho, chi5)| = {mp.nstr(aLp, 18)}')
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
    print(f"{'K':>9} {'|c_K|':>13} {'|E_K|':>13} {'|D_K|':>10} {'|D_K|*eg':>10} {'|D_K|*z2':>10} {'/Cak (AK)':>10} {'/Cs (Saar)':>10}")
    for n in range(1, N+1):
        cn = chi5(n)
        if cn != 0:
            mu = mu_of(n, spf)
            if mu != 0:
                cK = cK + mp.mpc(mu) * cn * mp.power(n, -rho)
        if Kix < len(Ks) and n == Ks[Kix]:
            while p_idx < len(pr) and pr[p_idx] <= n:
                p = pr[p_idx]; p_idx += 1
                cp = chi5(p)
                if cp != 0:
                    Ek = Ek / (mp.mpc(1) - cp * mp.power(p, -rho))
            DK = cK * Ek
            ElK = Ek * mp.log(n)
            print(f'{n:>9} {mp.nstr(abs(cK),10):>13} {mp.nstr(abs(Ek),10):>13} {mp.nstr(abs(DK),8):>10} {mp.nstr(abs(DK)*egam,8):>10} {mp.nstr(abs(DK)*z2,8):>10} {mp.nstr(abs(ElK)/Cak,7):>10} {mp.nstr(abs(ElK)/Cs,7):>10}')
            Kix += 1

if __name__=='__main__':
    main()
