#!/usr/bin/env python3
"""Independent low-lying zeros of Dirichlet L-functions mod N.

The finite-x prime race  D(x;N,a) = π(x;N,a) − π(x;N,1)  is, via the
explicit formula, an almost-periodic function of u = log x whose
lowest Fourier frequency is γ_min(N) = the smallest positive ordinate
of a non-trivial zero ½+iγ over all non-principal χ mod N.  That mode
has log-x wavelength 2π/γ_min and sets the slowest transient: a
reversal can persist over Δ(log x) ~ π/γ_min (a half-period).

We compute γ_min(N) ourselves (mpmath Hurwitz-zeta construction of
L(s,χ)), so the "where does the hierarchy resolve" scale has an
INDEPENDENT theoretical anchor and we do NOT rely on the unverified
preprint's e^{33.4} number.  Modest precision: an anchor, not a
zero-database.

  L(s,χ) = N^{-s} Σ_{r=1}^{N-1} χ(r) ζ(s, r/N)      (Hurwitz ζ)

Usage:  lowzeros.py [Nlist default 7,8,11,19,23]
"""
import sys, os, math
from mpmath import mp, mpf, mpc, zeta, fabs
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chargrp import char_table, units            # correct, self-tested

mp.dps = 15            # γ_min anchor to ~3-4 digits is sufficient

def is_principal(ch, U):
    return all(abs(ch[u] - 1) < 1e-9 for u in U)

def Lval(s, N, U, ch):
    acc = mpc(0)
    for r in U:
        c = ch[r]
        acc += mpc(c.real, c.imag) * zeta(s, mpf(r) / N)
    return acc * mp.power(N, -s)

def lowest_gamma(N, U, ch, tmax=14.0, step=0.05):
    """Coarse scan of |L(1/2+it)| for the first deep min, then refine."""
    half = mpf(1) / 2
    best_t, best_v = None, None
    prev = None
    t = 1e-6
    grid = []
    while t <= tmax:
        v = float(fabs(Lval(mpc(half, t), N, U, ch)))
        grid.append((t, v)); t += step
    # local minima that are small relative to neighbours
    cand = []
    for i in range(1, len(grid) - 1):
        (t0, v0) = grid[i]
        if v0 < grid[i-1][1] and v0 < grid[i+1][1]:
            cand.append((v0, t0, grid[i-1][0], grid[i+1][0]))
    cand.sort()
    for v0, t0, ta, tb in cand[:6]:
        # golden-section refine of |L| on [ta,tb]
        lo, hi = mpf(ta), mpf(tb)
        gr = (mp.sqrt(5) - 1) / 2
        for _ in range(60):
            x1 = hi - gr * (hi - lo)
            x2 = lo + gr * (hi - lo)
            f1 = fabs(Lval(mpc(half, x1), N, U, ch))
            f2 = fabs(Lval(mpc(half, x2), N, U, ch))
            if f1 < f2: hi = x2
            else:       lo = x1
        tm = (lo + hi) / 2
        vm = float(fabs(Lval(mpc(half, tm), N, U, ch)))
        if vm < 1e-4:                      # genuine zero, not just a dip
            return float(tm)
    return None

def main():
    Ns = [int(x) for x in sys.argv[1:]] or [7, 8, 11, 19, 23]
    print(f"{'N':>3} {'#nonprinc χ':>11} {'γ_min(N)':>10} "
          f"{'2π/γ_min':>9} {'e^(π/γ_min)':>14}")
    out = {}
    for N in Ns:
        U, chars = char_table(N)
        gmin = None
        for ch in chars:
            if is_principal(ch, U):
                continue
            g = lowest_gamma(N, U, ch)
            if g is not None and (gmin is None or g < gmin):
                gmin = g
        if gmin:
            wl = 2 * math.pi / gmin
            x_half = math.exp(math.pi / gmin)   # half-period reversal scale
            out[N] = gmin
            print(f"{N:>3} {len(U)-1:>11} {gmin:>10.4f} {wl:>9.3f} "
                  f"{x_half:>14.3e}")
        else:
            print(f"{N:>3} {len(U)-1:>11} {'(none<thr)':>10}")
    print("\nNote: γ_min is the lowest zero ordinate over all "
          "non-principal χ mod N (modest precision; an anchor).")
    print("Reversal persists ~ a half-period in log x: Δlog x ~ π/γ_min.")

if __name__ == "__main__":
    main()
