#!/usr/bin/env python3
r"""
binfty_hardened.py  --  hardened numerical verification of the corrected
B_infty identity, the local-Perron C_1 subleading identity, and the
Aoki-Koyama e^{-gamma} normalisation.   (D3 numerical hardening, 2026-05-16)

The user's OWN independent verification work.  Supersedes Koyama_B_infty.py /
Koyama_C1.py / Koyama_AK*.py with a genuine high-precision, two-engine audit.

WHAT IS HARDENED
----------------
1. TRUE multi-precision.  rho is refined to 80 dps and carried as an
   arbitrary-precision complex; every Dirichlet-character value is the
   EXACT root of unity e^{2 pi i a/m} evaluated at the engine's working
   precision (NOT a double via cmath).  The prior helper that funnelled
   rho and chi through python `complex` capped the whole computation at
   ~1e-16 -- a hollow "50-dps" claim; that is fixed here.

2. TWO independent engines:
     - mpmath 1.3.0  (pure python, run at dps 50 AND 80: precision-doubling)
     - python-flint / Arb 0.6.0  (FLINT C core, RIGOROUS ball arithmetic;
       every value carries a proven radius)
   Engine cross-check spans different codebases AND different number
   models (heuristic vs rigorous-interval).  HONEST SCOPE: PARI/GP 2.17.3
   and a separate native 250-bit Arb run quoted in the prior handoff are
   NOT reproducible in this environment (no `gp`; Arb here is
   python-flint).  The multi-engine claim is made at exactly this strength
   and no stronger.

3. The genuine analytic object isolated.  The only conditionally
   convergent / boundary-line content of Appendix A is the k=2 identity
        1/2 sum_{p<=K} chi^2(p) p^{-2 rho}  -->  1/2 logL(2rho,psi)+BPC1+BPC2 .
   We report R2(K) = LHS_K - RHS directly with its convergence envelope.
   The full (*) residual differs from R2 only by an ABSOLUTELY convergent
   k>=3 remainder carrying an explicit rigorous bound.  The prior scripts
   truncated T_{>=3} at a *different* K than T_K, conflating the two.

4. P(3/2) FIX.  Appendix A 5A.3 and Koyama_B_infty_proof.md 55 state
   "P(3/2)=sum_p p^{-3/2} ~= 0.45224"; that is the prime zeta at s=2.
   Correct: P(3/2)=0.849562683..., so crude |T_{>=3}|<=0.9669, not 0.515.

CONDITIONAL / UNCONDITIONAL BOUNDARY (printed on every relevant line)
   * (*) B_infty identity            : UNCONDITIONAL given simple rho.
   * k=2 rate, chi^2 principal       : UNCONDITIONAL O(1/logK)
                                       [Akatsuka, Kodai 40 (2017) eq.(2.5);
                                        proved from PNT-with-error; there
                                        is NO Akatsuka 2013 paper].
   * k=2 rate, chi^2 non-principal   : unconditional o(1) via PNT-for-psi;
                                       observed ~K^{-1/2} is RH(L(.,psi))-COND.
   * C_1 leading+subleading identity : identity UNCONDITIONAL given
                                       simplicity; o(1) RATE is
                                       RH(L(.,chi))-CONDITIONAL
                                       [Soundararajan, Crelle 631 (2009)].
   * Aoki-Koyama e^{-gamma} limit    : DRH-CONDITIONAL in char 0
                                       [Aoki-Koyama, JNT 245 (2023)].

Run:  python3 binfty_hardened.py
"""
from __future__ import annotations
import sys, time, math
import numpy as np
import mpmath as mp
from flint import acb, arb, ctx

# ---------------------------------------------------------------------------
# 0. sieves
# ---------------------------------------------------------------------------
def primes_upto(N: int) -> np.ndarray:
    s = np.ones(N + 1, dtype=bool); s[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0].astype(np.int64)

# ---------------------------------------------------------------------------
# 1. EXACT Dirichlet characters.
#    chi(n) -> None  (means 0)  or integer a with chi(n)=exp(2 pi i a / chi.m)
# ---------------------------------------------------------------------------
def _primitive_root(q):
    from sympy import is_primitive_root
    for g in range(2, q):
        if is_primitive_root(g, q): return g
    raise RuntimeError(f"no primitive root mod {q}")

class Char:
    def __init__(self, q, m, table, name):
        self.q, self.m, self._t, self.name = q, m, table, name
    def a(self, n):                       # exponent a (value = e^{2 pi i a/m}) or None
        return self._t[n % self.q]

def char_prime_full(q, name=None):
    """Primitive char mod prime q of full order m=q-1."""
    g = _primitive_root(q); m = q - 1
    dlog = {}; x = 1
    for k in range(m):
        dlog[x] = k; x = (x * g) % q
    table = [None] * q
    for r in range(1, q):
        table[r] = dlog[r] % m
    return Char(q, m, table, name or f"chi_{q}")

def char_neg4():
    # m=2: chi(1)=e^0=1, chi(3)=e^{i pi}=-1
    return Char(4, 2, [None, 0, None, 1], "chi_-4")

def char_8():
    # primitive real char mod 8, chi(1)=chi(7)=1, chi(3)=chi(5)=-1
    return Char(8, 2, [None, 0, None, 1, None, 1, None, 0], "chi_8")

def squared_primitive(chi: Char):
    """Primitive character psi inducing chi^2, its conductor f, bad primes,
    and a flag if psi is trivial (=> L(.,psi)=zeta).  chi^2 value exponent
    is 2*a mod m."""
    q, m = chi.q, chi.m
    def chi2a(n):
        a = chi.a(n)
        return None if a is None else (2 * a) % m
    def induced_mod(d):
        for n in range(q):
            if math.gcd(n, q) == 1:
                for mm in range(n % d, q, d):
                    if math.gcd(mm, q) == 1 and chi2a(mm) != chi2a(n):
                        return False
        return True
    f = q
    for d in range(1, q + 1):
        if q % d == 0 and induced_mod(d): f = d; break
    psi_triv = (f == 1)
    if psi_triv:
        psi = None
    else:
        tab = [None] * f
        for n in range(q):
            if math.gcd(n, q) == 1:
                tab[n % f] = chi2a(n)
        psi = Char(f, m, tab, f"psi[{chi.name}^2]")
    bad = [p for p in (2, 3, 5, 7, 11, 13) if q % p == 0 and f % p != 0]
    return psi, f, bad, psi_triv

# ---------------------------------------------------------------------------
# 2. engines.  Each builds its own arbitrary-precision complex from STRINGS
#    (rho carried as 80-digit decimal strings) and exact roots of unity.
# ---------------------------------------------------------------------------
class Mp:
    name = "mpmath"
    def __init__(self, dps): self.dps = dps
    def set(self): mp.mp.dps = self.dps
    def C(self, re_s, im_s): return mp.mpc(mp.mpf(re_s), mp.mpf(im_s))
    def one(self): return mp.mpc(1)
    def zero(self): return mp.mpc(0)
    def half(self): return mp.mpf('0.5')
    def root(self, a, m):                       # e^{2 pi i a/m}
        return mp.expjpi(mp.mpf(2 * a) / m)
    def cpow(self, base, s): return mp.power(int(base), s)
    def neg(self, s): return -s
    def log1pm(self, z): return mp.log1p(-z)
    def log(self, z): return mp.log(z)
    def hurwitz(self, s, a_num, a_den): return mp.zeta(s, mp.mpf(a_num) / a_den)
    def zeta(self, s): return mp.zeta(s)
    def cx(self, z): return complex(mp.re(z), mp.im(z))
    def rad(self, z): return 0.0

class Arb:
    name = "arb"
    def __init__(self, bits): self.bits = bits
    def set(self): ctx.prec = self.bits
    def C(self, re_s, im_s): return acb(arb(re_s), arb(im_s))
    def one(self): return acb(1)
    def zero(self): return acb(0)
    def half(self): return arb('0.5')
    def root(self, a, m):
        return (acb(0, 1) * acb.pi() * acb(2 * a) / acb(m)).exp()
    def cpow(self, base, s): return acb(int(base)) ** s
    def neg(self, s): return -s
    def log1pm(self, z): return (acb(1) - z).log()
    def log(self, z): return z.log()
    def hurwitz(self, s, a_num, a_den): return acb.zeta(s, acb(a_num) / acb(a_den))
    def zeta(self, s): return acb.zeta(s)
    def cx(self, z): return complex(float(z.real), float(z.imag))
    def rad(self, z):
        try: return max(float(arb(z.real).rad()), float(arb(z.imag).rad()))
        except Exception: return float('nan')

# ---------------------------------------------------------------------------
# 3. rho refinement (mpmath, dps 80) -> 78-digit decimal strings
# ---------------------------------------------------------------------------
def char_complex_mp(chi: Char, n):
    a = chi.a(n)
    return None if a is None else mp.expjpi(mp.mpf(2 * a) / chi.m)

def L_hurwitz_mp(chi: Char, s):
    tot = mp.mpc(0)
    for r in range(1, chi.q + 1):
        cv = char_complex_mp(chi, r)
        if cv is None: continue
        tot += cv * mp.zeta(s, mp.mpf(r) / chi.q)
    return mp.power(chi.q, -s) * tot

def refine_zero(chi: Char, t_seed):
    mp.mp.dps = 80
    s_ref = mp.findroot(lambda s: L_hurwitz_mp(chi, s),
                        mp.mpc(mp.mpf('0.5'), mp.mpf(str(t_seed))),
                        solver='muller', tol=mp.mpf('1e-55'), maxsteps=300)
    if abs(mp.re(s_ref) - mp.mpf('0.5')) > mp.mpf('1e-10'):
        g = lambda tt: mp.re(L_hurwitz_mp(chi, mp.mpc(mp.mpf('0.5'), tt)) *
                             mp.conj(L_hurwitz_mp(chi, mp.mpc(mp.mpf('0.5'), tt))))
        tt = mp.findroot(g, mp.mpf(str(t_seed)), tol=mp.mpf('1e-45'))
        re_s, im_s = mp.mpf('0.5'), mp.mpf(tt)
    else:
        re_s, im_s = mp.re(s_ref), mp.im(s_ref)
    qual = float(abs(L_hurwitz_mp(chi, mp.mpc(re_s, im_s))))
    return mp.nstr(re_s, 78), mp.nstr(im_s, 78), qual

# ---------------------------------------------------------------------------
# 4. engine-generic building blocks
# ---------------------------------------------------------------------------
def L_hurwitz(E, chi: Char, s):
    tot = E.zero()
    for r in range(1, chi.q + 1):
        a = chi.a(r)
        if a is None: continue
        tot = tot + E.root(a, chi.m) * E.hurwitz(s, r, chi.q)
    return E.cpow(chi.q, E.neg(s)) * tot

def L_psi(E, psi, psi_triv, s):
    return E.zeta(s) if psi_triv else L_hurwitz(E, psi, s)

def half_logL_psi(E, psi, psi_triv, two_rho):
    return E.C('0.5', '0') * E.log(L_psi(E, psi, psi_triv, two_rho))

def BPC1(E, psi, psi_triv, bad, two_rho):
    s = E.zero()
    for p in bad:
        if psi_triv:
            psip = E.one()
        else:
            a = psi.a(p)
            if a is None: continue
            psip = E.root(a, psi.m)
        s = s + E.log(E.one() - psip * E.cpow(p, E.neg(two_rho)))
    return E.C('0.5', '0') * s

def accumulate(E, chi: Char, rho, two_rho, primes, mode):
    """One pass: per prime add
       's2'   : chi^2(p) p^{-2rho}
       'bpc2w': -log(1-w)-w           (w = chi^2(p) p^{-2rho})
       'kge2' : -log(1-z)-z           (z = chi(p)  p^{-rho})   [= T_K term]
       'kge3' : -log(1-z)-z-z^2/2
       'logE' : -log(1-z)             [log E_K Euler-product]"""
    nrho = E.neg(rho); n2rho = E.neg(two_rho)
    tot = E.zero(); half = E.C('0.5', '0')
    for p in primes:
        a = chi.a(int(p))
        if a is None: continue
        cp = E.root(a, chi.m)
        if mode in ('s2', 'bpc2w'):
            w = cp * cp * E.cpow(p, n2rho)
            tot = tot + (w if mode == 's2' else (E.neg(E.log1pm(w)) - w))
        else:
            z = cp * E.cpow(p, nrho)
            if mode == 'kge2':   tot = tot + (E.neg(E.log1pm(z)) - z)
            elif mode == 'kge3': tot = tot + (E.neg(E.log1pm(z)) - z - half * z * z)
            else:                tot = tot + E.neg(E.log1pm(z))   # logE
    return tot

# rigorous absolute-convergence tails (proven, not heuristic)
def tail_Tge3(K3):  return 1.1380712 * 2.0 / math.sqrt(K3)   # 1/(3(1-2^-1/2)) * 2/sqrt
def tail_BPC2(K3):  return 1.0 / K3

# L', L'' via analytic Hurwitz derivatives (mpmath, dps 60)
def L_derivs(chi: Char, re_s, im_s):
    mp.mp.dps = 60
    s = mp.mpc(mp.mpf(re_s), mp.mpf(im_s))
    L = Lp = Lpp = mp.mpc(0); logq = mp.log(chi.q)
    for r in range(1, chi.q + 1):
        cv = char_complex_mp(chi, r)
        if cv is None: continue
        ar = mp.mpf(r) / chi.q
        L   += cv * mp.zeta(s, ar)
        Lp  += cv * mp.zeta(s, ar, derivative=1)
        Lpp += cv * mp.zeta(s, ar, derivative=2)
    qp = mp.power(chi.q, -s)
    Lf   = qp * L
    Lpf  = qp * (Lp - logq * L)
    Lppf = qp * (Lpp - 2*logq*Lp + logq*logq*L)
    return complex(Lpf), complex(Lppf), complex(Lf)

# ---------------------------------------------------------------------------
# 5. one pair
# ---------------------------------------------------------------------------
def audit_pair(label, chi, t_seed, K_list, primes_all, K3, engines):
    print("\n" + "=" * 94)
    print(f"{label}   ({chi.name}, mod {chi.q})")
    print("=" * 94)
    re_s, im_s, qual_mp = refine_zero(chi, t_seed)
    print(f"refined rho = {re_s[:24]}... + {im_s[:24]}... i   |L(rho,chi)|_mp = {qual_mp:.2e}")
    psi, f, bad, psi_triv = squared_primitive(chi)
    print(f"chi^2 -> primitive psi conductor f={f}"
          f"{'  (psi trivial: L=zeta, chi^2 PRINCIPAL)' if psi_triv else '  (chi^2 NON-principal)'}"
          f"; bad primes {bad or 'none'}")

    # rho / 2rho per engine, full precision
    def rho_of(E):  return E.C(re_s, im_s)
    def two_of(E):  return E.C(re_s, im_s) + E.C(re_s, im_s)

    # zero quality cross-engine (Arb, rigorous)
    Ea = engines['arb']; Ea.set()
    qa = abs(L_hurwitz(Ea, chi, rho_of(Ea)))
    print(f"|L(rho,chi)|_arb = {float(qa):.2e}   (independent-engine zero check)")

    # base = 1/2 logL(2rho,psi) + BPC1 + BPC2, at K3 (rigorous abs-conv tails)
    pK3 = primes_all[primes_all <= K3]
    base = {}
    for ek in ('mp50', 'mp80', 'arb'):
        E = engines[ek]; E.set()
        tr = two_of(E)
        hl = half_logL_psi(E, psi, psi_triv, tr)
        b1 = BPC1(E, psi, psi_triv, bad, tr)
        b2 = E.C('-0.5', '0') * accumulate(E, chi, rho_of(E), tr, pK3, 'bpc2w')
        base[ek] = E.cx(hl + b1 + b2)
    d_eng = abs(base['mp50'] - base['arb'])
    d_prec = abs(base['mp50'] - base['mp80'])
    base_ref = base['mp80']
    print(f"base=1/2logL+BPC1+BPC2 :  mp50={base['mp50']:.10g}")
    print(f"  engine agree |mp50-arb|={d_eng:.2e}   precision-double |mp50-mp80|={d_prec:.2e}"
          f"   rig.tails: BPC2<= {tail_BPC2(K3):.1e}, T>=3<= {tail_Tge3(K3):.1e}")

    # ---- genuine analytic object: R2(K) = 1/2 S2(K) - base ----
    env = ("UNCOND O(1/lnK) [Akatsuka 2017 (2.5)]" if psi_triv
           else "uncond o(1); ~K^-1/2 = RH(psi)-COND")
    print(f"\n  k=2 boundary identity   R2(K)=1/2 sum_{{p<=K}} chi^2(p)p^(-2rho) - base"
          f"     [{env}]")
    print(f"  {'K':>9} | {'|R2| arb':>11} {'|R2| mp50':>11} | {'eng|Δ|':>8} "
          f"{'arb rad':>9} {'C/lnK fit':>10}")
    Ea = engines['arb']; Em = engines['mp50']
    for K in K_list:
        pK = primes_all[primes_all <= K]
        Ea.set(); s2a = Ea.C('0.5','0') * accumulate(Ea, chi, rho_of(Ea), two_of(Ea), pK, 's2')
        Em.set(); s2m = Em.C('0.5','0') * accumulate(Em, chi, rho_of(Em), two_of(Em), pK, 's2')
        R2a = Ea.cx(s2a) - base_ref
        R2m = Em.cx(s2m) - base_ref
        rad = Ea.rad(s2a)
        cfit = abs(R2a) * math.log(K)
        print(f"  {K:>9} | {abs(R2a):>11.4e} {abs(R2m):>11.4e} | {abs(R2a-R2m):>8.1e} "
              f"{rad:>9.1e} {cfit:>10.4f}")

    # ---- full (*) residual, matched cutoff K3'=K (continuity w/ prior table) ----
    print(f"\n  full (*) residual  Rfull(K)=T_K-[base+T>=3,->K];"
          f"  R2(K) plus rigorously-bounded abs-conv tail")
    print(f"  {'K':>9} | {'|Rfull| arb':>12} {'|Rfull| mp50':>12} | {'rig tail<=':>10}")
    for K in K_list:
        pK = primes_all[primes_all <= K]
        Ea.set()
        TKa = Ea.cx(accumulate(Ea, chi, rho_of(Ea), two_of(Ea), pK, 'kge2'))
        t3a = Ea.cx(accumulate(Ea, chi, rho_of(Ea), two_of(Ea), pK, 'kge3'))
        Em.set()
        TKm = Em.cx(accumulate(Em, chi, rho_of(Em), two_of(Em), pK, 'kge2'))
        t3m = Em.cx(accumulate(Em, chi, rho_of(Em), two_of(Em), pK, 'kge3'))
        Rfa = TKa - (base_ref + t3a)
        Rfm = TKm - (base_ref + t3m)
        print(f"  {K:>9} | {abs(Rfa):>12.4e} {abs(Rfm):>12.4e} | {tail_Tge3(int(K)):>10.2e}")

    # ---- C_1 subleading identity (Appendix B Lemma X.3.1) ----
    Lp, Lpp, Lval = L_derivs(chi, re_s, im_s)
    C1 = -Lpp / (2 * Lp * Lp)
    print(f"\n  C_1 = -L''/(2 L'^2) = {C1:.8g}   "
          f"[identity UNCONDITIONAL given simple rho]")
    print(f"  L'(rho,chi)={Lp:.8g}  L''(rho,chi)={Lpp:.8g}  (|L|={abs(Lval):.1e})")

    # ---- Aoki-Koyama e^{-gamma} drift (DRH-CONDITIONAL) ----
    mp.mp.dps = 50
    Kak = int(K_list[-1]); pK = primes_all[primes_all <= Kak]
    logE = accumulate(engines['mp50'], chi,
                      engines['mp50'].C(re_s, im_s),
                      engines['mp50'].C(re_s, im_s) + engines['mp50'].C(re_s, im_s),
                      pK, 'logE')
    ElogK = mp.e ** logE * mp.log(Kak)
    eg = float(mp.e ** mp.euler); z2 = float(mp.zeta(2))
    rAK = float(abs(ElogK)) / (abs(Lp) / eg)
    rS  = float(abs(ElogK)) / (abs(Lp) / z2)
    print(f"  AK drift @K={Kak:.0e}: |E_K logK|/|L'/e^gamma|={rAK:.4f} (->1 DRH)"
          f"   /|L'/zeta2|={rS:.4f} (->e^g/z2=0.9237)   [DRH-CONDITIONAL, AK 2023]")

    return dict(label=label, im=im_s[:20], psi_triv=psi_triv, f=f,
                qual_mp=qual_mp, qual_ar=float(qa),
                d_eng=d_eng, d_prec=d_prec, C1=C1, Lp=Lp)

# ---------------------------------------------------------------------------
# 6. main
# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("HARDENED B_infty / C_1 / e^{-gamma} verification  (2026-05-16, D3)")
    print("engines: mpmath 1.3.0 (dps 50 & 80) + python-flint/Arb 0.6.0 (rigorous balls)")
    mp.mp.dps = 40
    print(f"\n[P(3/2) AUDIT]  P(3/2) = {mp.nstr(mp.primezeta(1.5),14)}    "
          f"P(2) = {mp.nstr(mp.primezeta(2.0),14)}")
    c = 1 / (3 * (1 - 2 ** mp.mpf('-0.5')))
    print(f"  crude |T_>=3| <= P(3/2)/(3(1-2^-1/2)) = {mp.nstr(c*mp.primezeta(1.5),8)}"
          f"   <-- Appendix A 5A.3 / Koyama_B_infty_proof 55 wrongly print 0.515 (used P(2))")

    Kmax = 2_000_000; K3 = 2_000_000
    print(f"\nsieving to {Kmax:,} ...", flush=True)
    primes_all = primes_upto(Kmax)
    print(f"  pi({Kmax:,}) = {len(primes_all):,}  ({time.time()-t0:.1f}s)")

    engines = {'mp50': Mp(50), 'mp80': Mp(80), 'arb': Arb(230)}  # 230 bits ~ 69 dps
    K_list = [10_000, 100_000, 1_000_000, 2_000_000]
    pairs = [
        ("chi_-4/z1", char_neg4(),          6.020949),
        ("chi_-4/z2", char_neg4(),          10.243770),
        ("chi_8 /z1", char_8(),             4.0),
        ("chi_5 /z1", char_prime_full(5),   6.183578),
        ("chi_7 /z1", char_prime_full(7),   4.0),
        ("chi_11/z1", char_prime_full(11),  3.547041),
        ("chi_13/z1", char_prime_full(13),  3.0),
    ]
    res = []
    for (lab, chi, seed) in pairs:
        try:
            res.append(audit_pair(lab, chi, seed, K_list, primes_all, K3, engines))
        except Exception as e:
            import traceback; print(f"  !! {lab}: {e}"); traceback.print_exc()

    print("\n" + "=" * 94)
    print("ERROR-BUDGET SUMMARY  (base = 1/2 logL(2rho,psi)+BPC1+BPC2)")
    print("=" * 94)
    print(f"{'pair':<12}{'chi^2':<8}{'f':<4}{'|L(rho)|mp':<12}{'|L(rho)|arb':<12}"
          f"{'eng|Δ|base':<12}{'precdbl':<10}")
    for r in res:
        print(f"{r['label']:<12}{'princ' if r['psi_triv'] else 'nonpr':<8}{r['f']:<4}"
              f"{r['qual_mp']:<12.1e}{r['qual_ar']:<12.1e}{r['d_eng']:<12.1e}{r['d_prec']:<10.1e}")
    print(f"\nwall {time.time()-t0:.1f}s. Conditional/unconditional labels are on each line above.")

if __name__ == "__main__":
    main()
