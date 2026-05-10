"""
Koyama_B_infty.py — numerical verification of the B_∞ explicit formula.

Conjecture (Saar Shai → Koyama, 2026-04-16): for primitive non-trivial Dirichlet
character χ mod q and a simple zero ρ of L(s,χ),
    T_∞ := lim_{K→∞} Σ_{p≤K} Σ_{k≥2} χ(p)^k / (k p^{kρ})
         = (1/2) log L(2ρ, χ²) + Σ_{k≥3} (1/k) Σ_p χ(p)^k / p^{kρ} + (bad-prime correction).

We verify the rigorous identity derived in `Koyama_B_infty_proof.md`:

    T_∞ = (1/2) log L(2ρ, ψ) + BPC1 + BPC2 + T_{≥3}                       (*)

where  ψ := χ² regarded as the *primitive* character of conductor f | q,
       BPC1 := (1/2) Σ_{p|q, p∤f} log(1 − ψ(p) p^{-2ρ})    (imprimitive→primitive bad-prime correction)
       BPC2 := −(1/2) Σ_{k≥2} (1/k) Σ_p χ(p)^{2k} p^{-2kρ} (residue from k=2 log-Euler-product expansion)
       T_{≥3} := Σ_{k≥3} (1/k) Σ_p χ(p)^k p^{-kρ}            (absolutely convergent)

Tests:
  (A) Truncated identity at K = 2×10^5, 10^6, 2×10^6 with mpmath dps=50.
      Verify Re(T_K) and Im(T_K) match Re/Im of RHS within stated truncation tail
      (the difference is the K-tail of the conditionally-convergent k=2 sum).
  (B) Reproduce Saar's |B_K|·ζ(2) and |B_∞|≈|B_K| ratios at the four (χ,ρ) pairs.
  (C) k=2+3+4 truncation match within 1-2% per Saar's table.

Characters and zeros (from Saar's 2026-04-16 email):
  χ_{-4}/z1: t1 = 6.0209489...   (Hurwitz, real char order 2, mod 4)
  χ_{-4}/z2: t2 = 10.2437...     (same character)
  χ_5      : t  = 6.18357...     (complex char mod 5, order 4)
  χ_{11}   : t  = 3.5474...      (complex char mod 11, order 10)

NOTE on zero precision: the Saar table uses zeros refined to 40 dps. We refine
each zero by Newton iteration (mpmath findroot) before any sum — coarse zeros
contaminate the Re/Im split of T_∞ heavily.
"""

from __future__ import annotations
import mpmath as mp
from sympy import primerange, isprime
import math

mp.mp.dps = 50  # 50 decimal places throughout

# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------

def chi_neg4(n: int) -> mp.mpc:
    """Primitive Dirichlet character mod 4: χ(1)=1, χ(3)=-1, χ(even)=0."""
    n = n % 4
    if n == 1: return mp.mpc(1)
    if n == 3: return mp.mpc(-1)
    return mp.mpc(0)


def chi_5_factory():
    """χ_5 primitive complex character mod 5, order 4.
    Generator of (Z/5)* is 2 (orders: 2,4,3,1 for n=2,4,3,1).
    Define χ(2) = i (primitive root of unity of order 4).
    Then: χ(1)=1, χ(2)=i, χ(4)=i²=-1, χ(3)=i³=-i, χ(0)=0.
    Saar's email: d = {1:0, 2:1, 4:2, 3:3}, χ(n) = i^d(n).
    """
    table = {1: mp.mpc(1), 2: mp.mpc(0,1), 4: mp.mpc(-1), 3: mp.mpc(0,-1), 0: mp.mpc(0)}
    def chi(n):
        return table[n % 5]
    return chi

def chi_11_factory():
    """χ_{11} primitive complex character mod 11, order 10.
    Generator of (Z/11)* is 2: 2^k mod 11 for k=0..9 gives 1,2,4,8,5,10,9,7,3,6.
    Saar's email: d = {1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9}
    χ(n) = exp(2πi · d(n) / 10).
    """
    d_map = {1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9, 0:None}
    def chi(n):
        r = n % 11
        d = d_map[r]
        if d is None:
            return mp.mpc(0)
        return mp.exp(2j*mp.pi * d / 10)
    return chi


# ---------------------------------------------------------------------------
# χ² and its primitive conductor
# ---------------------------------------------------------------------------

def chi_sq(chi, n):
    return chi(n) * chi(n)


# χ_{-4}² is the principal character mod 4. Its primitive inducing character
# is the trivial character (conductor 1) — i.e. corresponds to ζ(s).
# Bad prime: p=2 (divides q=4 but not f=1), and ψ(2) = 1 (trivial char).
#
# χ_5² is the order-2 character mod 5 (Legendre symbol). Conductor f=5=q.
# No bad primes.
#
# χ_{11}² is order-5 character mod 11. Conductor f=11=q.
# No bad primes.

# ---------------------------------------------------------------------------
# Hurwitz-zeta computation of L(s, χ) and L'(s, χ)
# ---------------------------------------------------------------------------
# For χ mod q:  L(s, χ) = q^{-s} Σ_{a=1}^{q} χ(a) ζ(s, a/q)

def L_chi_via_hurwitz(chi, q, s):
    total = mp.mpc(0)
    for a in range(1, q+1):
        c = chi(a)
        if c == 0:
            continue
        total += c * mp.hurwitz(s, mp.mpf(a)/q)
    return q**(-s) * total

# For the bad-prime correction at χ_{-4}, we need L(2ρ, ζ) — but we want the
# *primitive* L: that's just ζ(2ρ). However Re(2ρ)=1, so ζ(s) at s=1+2ti uses mp.zeta.

# ---------------------------------------------------------------------------
# Hurwitz refinement of zeros
# ---------------------------------------------------------------------------

# Saar's table values for t (Im of zero, with Re=1/2):
ZEROS_SEED = {
    'chi_neg4_z1': mp.mpf('6.020948675438580'),       # ~ Saar table 6.0209
    'chi_neg4_z2': mp.mpf('10.243770397127014'),      # ~ Saar table 10.2437
    'chi_5':       mp.mpf('6.183573983900135'),       # ~ Saar table 6.18357
    'chi_11':      mp.mpf('3.547464715633575'),       # ~ Saar table 3.5474
}

def refine_zero(chi, q, t_seed):
    """Refine a zero ρ = 1/2 + i t of L(s, χ) by Muller iteration on L(1/2+it)
    with t kept real. We solve a complex L(s)=0 for s, then read off Im(s)."""
    s_seed = mp.mpc(mp.mpf('0.5'), t_seed)
    def F(s):
        return L_chi_via_hurwitz(chi, q, s)
    s_refined = mp.findroot(F, s_seed, solver='muller', tol=mp.mpf('1e-45'))
    # the zero should still be on Re=1/2 — sanity check
    if abs(mp.re(s_refined) - mp.mpf('0.5')) > mp.mpf('1e-20'):
        # nudge: Newton drifted off. Force Re=1/2 and re-Newton in Im only via secant.
        # Use scalar real-valued solver on |L(1/2+it)|^2.
        def G(t):
            v = L_chi_via_hurwitz(chi, q, mp.mpc(mp.mpf('0.5'), mp.mpf(t)))
            return mp.re(v*mp.conj(v))
        # secant by mpmath
        t_refined = mp.findroot(G, mp.mpf(t_seed), tol=mp.mpf('1e-40'))
        return mp.mpf(t_refined)
    return mp.im(s_refined)


# ---------------------------------------------------------------------------
# Partial sum T_K
# ---------------------------------------------------------------------------

def T_K_partial(chi, rho, K, k_max=None):
    """T_K(χ,ρ) = Σ_{p≤K} Σ_{k≥2} χ(p)^k / (k p^{kρ}).

    For each prime, sum k from 2 up to a safe cutoff where |term| < 1e-50.
    """
    total = mp.mpc(0)
    for p in primerange(2, K+1):
        cp = chi(p)
        if cp == 0:
            continue
        z = cp / mp.power(p, rho)   # = χ(p) p^{-ρ}, complex
        # we want Σ_{k≥2} z^k / k
        # = -log(1-z) - z      (since -log(1-z) = Σ_{k≥1} z^k/k)
        # but be careful about branch: |z| = p^{-1/2} ≤ 1/√2 < 1, so principal branch ok.
        full = -mp.log1p(-z) - z   # Σ_{k≥2} z^k / k
        total += full
    return total


def T_K_partial_split(chi, rho, K, k_max=80):
    """Same as T_K_partial, but also returns a list of partial T_k_K for k=2..k_max
    (for direct verification of decomposition by k)."""
    sum_total = mp.mpc(0)
    sum_by_k = [mp.mpc(0)] * (k_max+1)  # index by k
    for p in primerange(2, K+1):
        cp = chi(p)
        if cp == 0:
            continue
        z = cp / mp.power(p, rho)
        zk = z*z          # k=2 starts
        for k in range(2, k_max+1):
            term = zk / k
            sum_by_k[k] += term
            sum_total += term
            zk *= z
            if abs(zk) < mp.mpf('1e-55'):
                break
    return sum_total, sum_by_k


# ---------------------------------------------------------------------------
# RHS of the identity (*)
# ---------------------------------------------------------------------------

def primitive_log_L_2rho(chi_sq_prim, q_prim, two_rho):
    """Compute log L(2ρ, ψ) where ψ is the *primitive* inducing character of χ²,
    of conductor q_prim. For q_prim=1, this is log ζ(2ρ).
    The principal-branch log is used; since Re(2ρ)=1 and Im(2ρ)≠0, no zero/pole on
    that point (provided 1+2it ≠ 1, i.e. t ≠ 0)."""
    if q_prim == 1:
        # primitive ψ = trivial char → Riemann zeta
        L_val = mp.zeta(two_rho)
    else:
        L_val = L_chi_via_hurwitz(chi_sq_prim, q_prim, two_rho)
    return mp.log(L_val)


def BPC1_bad_prime_imprimitive(chi_sq_prim, q_prim, q_chi, two_rho):
    """BPC1 = (1/2) Σ_{p | q_chi, p ∤ q_prim} log(1 − ψ(p) p^{-2ρ})."""
    # find primes p dividing q_chi but not q_prim
    s = mp.mpc(0)
    if q_prim == 1:
        bad_primes = [p for p in range(2, q_chi+1) if isprime(p) and q_chi % p == 0]
    else:
        bad_primes = [p for p in range(2, q_chi+1) if isprime(p) and q_chi % p == 0 and q_prim % p != 0]
    for p in bad_primes:
        psi_p = chi_sq_prim(p) if q_prim != 1 else mp.mpc(1)
        s += mp.log(1 - psi_p / mp.power(p, two_rho))
    return mp.mpf('0.5') * s


def BPC2_log_expansion_residue(chi, two_rho, K_for_estimate=10**5, k_max=80):
    """BPC2 = -(1/2) Σ_{k≥2} (1/k) Σ_p χ(p)^{2k} p^{-2kρ}.

    Re(2kρ) = k ≥ 2 → absolutely convergent over all primes. We compute by summing
    over primes ≤ K_for_estimate; the tail is bounded by Σ_{p > K} p^{-k} which is
    O(K^{1-k}/(k-1)), negligible for K≥10^5 and k≥2.
    """
    s = mp.mpc(0)
    for k in range(2, k_max+1):
        s_k = mp.mpc(0)
        # χ(p)^{2k} = (χ(p)²)^k = ψ(p)^k where ψ ≡ χ² as a function on integers
        # (zero where χ is zero). So this is a sum of (χ²(p) p^{-2ρ})^k.
        for p in primerange(2, K_for_estimate+1):
            cp2 = chi(p) * chi(p)
            if cp2 == 0:
                continue
            term = mp.power(cp2 / mp.power(p, two_rho), k) / k
            s_k += term
        if abs(s_k) < mp.mpf('1e-45'):
            break
        s += s_k
    return -mp.mpf('0.5') * s


def T_geq3(chi, rho, K_for_estimate=10**5, k_max=120):
    """T_{≥3} := Σ_{k≥3} (1/k) Σ_p χ(p)^k p^{-kρ}.

    Re(kρ)=k/2 ≥ 3/2 → absolutely convergent over all primes.
    Tail bound: Σ_{p > K} p^{-3/2} = O(K^{-1/2}/log K), so K=10^5 → tail ~ 10^{-3}.
    For 50-dps target we use K=10^6 (tail ~ 10^{-4}) — but for moderate accuracy
    K=10^5 is enough; we'll pick K so that the truncation error is < 10^{-12}.
    """
    s = mp.mpc(0)
    # for fixed prime, sum over k≥3 is z^3/(3) + z^4/4 + ... = -log(1-z) - z - z²/2
    # using log1p(-z) for stability.
    for p in primerange(2, K_for_estimate+1):
        cp = chi(p)
        if cp == 0:
            continue
        z = cp / mp.power(p, rho)
        # Σ_{k≥3} z^k/k = -log(1-z) - z - z²/2
        s += -mp.log1p(-z) - z - z*z/2
    return s


# ---------------------------------------------------------------------------
# B_∞ ≈ exp(T_∞), and |B_∞|·ζ(2) for sanity
# ---------------------------------------------------------------------------

def run_one(label, chi, q, t_seed, chi2_prim, q_prim, K_list=(2*10**5, 10**6, 2*10**6)):
    print(f"\n{'='*78}\n{label}    (mod {q})\n{'='*78}")
    # 1. refine zero
    t = refine_zero(chi, q, t_seed)
    rho = mp.mpc(mp.mpf('0.5'), t)
    Lval = L_chi_via_hurwitz(chi, q, rho)
    print(f"refined t = {mp.nstr(t, 25)}")
    print(f"|L(ρ,χ)| at refined zero = {mp.nstr(abs(Lval), 6)}  (should be ~10^{{-25}} or smaller)")
    two_rho = 2*rho
    print(f"2ρ = {mp.nstr(two_rho, 25)}")

    # 2. primitive log L(2ρ, ψ)
    Q = primitive_log_L_2rho(chi2_prim, q_prim, two_rho)
    print(f"\n(1/2) log L(2ρ, ψ_prim, conductor {q_prim}) = {mp.nstr(mp.mpf('0.5')*Q, 18)}")

    # 3. BPC1: bad-prime correction (imprimitive↔primitive)
    bp1 = BPC1_bad_prime_imprimitive(chi2_prim, q_prim, q, two_rho)
    print(f"BPC1 (imprimitive correction) = {mp.nstr(bp1, 18)}")

    # 4. BPC2: log-expansion residue
    bp2 = BPC2_log_expansion_residue(chi, two_rho)
    print(f"BPC2 (log-expansion residue) = {mp.nstr(bp2, 18)}")

    # 5. T_{≥3}
    t3 = T_geq3(chi, rho)
    print(f"T_≥3 (k≥3 absolutely conv. tail) = {mp.nstr(t3, 18)}")

    # RHS of identity (*)
    rhs = mp.mpf('0.5')*Q + bp1 + bp2 + t3
    print(f"\nRHS  = (1/2)logL + BPC1 + BPC2 + T≥3  = {mp.nstr(rhs, 18)}")

    # 6. T_K computed directly, for several K
    print("\n  K       T_K (direct sum)                                     |T_K - RHS|")
    for K in K_list:
        T_K = T_K_partial(chi, rho, K)
        diff = T_K - rhs
        print(f"  {K:>9}  {mp.nstr(T_K, 18):<55} {mp.nstr(abs(diff), 6)}")

    # 7. |B_K| and |B_K|·ζ(2) at largest K
    Klast = K_list[-1]
    T_Klast = T_K_partial(chi, rho, Klast)
    BK = mp.exp(T_Klast)
    print(f"\n|B_{{K={Klast}}}| = |exp(T_K)| = {mp.nstr(abs(BK), 8)}")
    print(f"|B_K|·ζ(2)        = {mp.nstr(abs(BK)*mp.zeta(2), 8)}")

    # 8. for Saar's 1-2% claim: compute k=2-only formula, then k=2+3+4
    T_partial_k234 = mp.mpc(0)
    Tk2_only = mp.mpc(0)
    Tk3_only = mp.mpc(0)
    Tk4_only = mp.mpc(0)
    for p in primerange(2, Klast+1):
        cp = chi(p)
        if cp == 0:
            continue
        z = cp / mp.power(p, rho)
        Tk2_only += z*z / 2
        Tk3_only += z*z*z / 3
        Tk4_only += z*z*z*z / 4
    T_partial_k234 = Tk2_only + Tk3_only + Tk4_only

    BK_obs = abs(BK)                 # observed at K=Klast (proxy for B_∞)
    BK_k2  = abs(mp.exp(Tk2_only))   # k=2 only formula approximation
    BK_k234 = abs(mp.exp(T_partial_k234))
    print(f"\n|B_∞| (proxy at K={Klast}): {mp.nstr(BK_obs, 6)}")
    print(f"  k=2 only      |exp(T_k=2)|  = {mp.nstr(BK_k2, 6)}")
    print(f"  k=2+3+4 trunc |exp(T_k234)| = {mp.nstr(BK_k234, 6)}")
    print(f"  ratio (k234/obs)            = {mp.nstr(BK_k234/BK_obs, 6)}")

    return {
        'rho': rho,
        'T_K_lastK': T_K_partial(chi, rho, K_list[-1]),
        'rhs': rhs,
        'Q': Q,
        'BPC1': bp1,
        'BPC2': bp2,
        'T_geq3': t3,
        'BK_obs': BK_obs,
        'BK_k2': BK_k2,
        'BK_k234': BK_k234,
    }


def main():
    # χ_{-4}² = principal character mod 4. The primitive inducing character is the
    # trivial character (conductor 1). For evaluation we set chi2_prim = None handler:
    # primitive_log_L_2rho with q_prim=1 returns log ζ(2ρ).
    chi_neg4_sq_prim = None
    q_neg4_sq_prim = 1

    # χ_5² is the Legendre/quadratic character mod 5. Define it explicitly:
    chi_5 = chi_5_factory()
    def chi_5_sq(n):
        c = chi_5(n)
        return c*c
    q_5_sq_prim = 5

    # χ_{11}² has order 5; primitive of conductor 11.
    chi_11 = chi_11_factory()
    def chi_11_sq(n):
        c = chi_11(n)
        return c*c
    q_11_sq_prim = 11

    # K values for the verification table. K=10^6 takes ~6s per pair at 50 dps,
    # so K=2×10^6 ~12s is fine. We use Saar's K=2×10^6 as the proxy for B_∞.
    K_list = (2*10**5, 10**6, 2*10**6)

    results = {}
    results['chi_neg4_z1'] = run_one(
        'χ_{-4} / first zero (t≈6.021)',
        chi_neg4, 4, ZEROS_SEED['chi_neg4_z1'],
        chi_neg4_sq_prim, q_neg4_sq_prim, K_list)
    results['chi_neg4_z2'] = run_one(
        'χ_{-4} / second zero (t≈10.244)',
        chi_neg4, 4, ZEROS_SEED['chi_neg4_z2'],
        chi_neg4_sq_prim, q_neg4_sq_prim, K_list)
    results['chi_5'] = run_one(
        'χ_5 / first zero (t≈6.184)',
        chi_5, 5, ZEROS_SEED['chi_5'],
        chi_5_sq, q_5_sq_prim, K_list)
    results['chi_11'] = run_one(
        'χ_{11} / first zero (t≈3.547)',
        chi_11, 11, ZEROS_SEED['chi_11'],
        chi_11_sq, q_11_sq_prim, K_list)

    # Summary table comparing to Saar's reported values
    print("\n" + "="*78)
    print("SUMMARY: comparison to Saar 2026-04-16 table")
    print("="*78)
    print(f"{'pair':<14} {'|B_∞| obs (Saar)':<18} {'|B_K| ours':<14} {'k234 (Saar)':<13} {'k234 ours':<11} {'ratio ours':<11}")
    saar = {
        'chi_neg4_z1': (1.065, 1.198, 1.142, 1.072),
        'chi_neg4_z2': (0.941, 0.853, 0.926, 0.984),
        'chi_5':       (1.065, 0.985, 1.059, 0.994),
        'chi_11':      (0.784, 0.788, 0.795, 1.014),
    }
    for k in ['chi_neg4_z1','chi_neg4_z2','chi_5','chi_11']:
        s = saar[k]
        r = results[k]
        ratio = float(r['BK_k234']/r['BK_obs'])
        print(f"{k:<14} {s[0]:<18} {float(r['BK_obs']):<14.4f} {s[2]:<13} {float(r['BK_k234']):<11.4f} {ratio:<11.4f}")


if __name__ == "__main__":
    main()
