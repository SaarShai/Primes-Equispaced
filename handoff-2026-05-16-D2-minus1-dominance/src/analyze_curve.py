#!/usr/bin/env python3
"""Layer-F analysis of the −1-dominance dynamic curve.

Pure post-processing of a curve TSV (works on the streaming *partial*
file too, for previews).  Produces ONLY observed facts; all asymptotic
interpretation is fenced to THEORY_LAYER.md / the draft.

For each N in the file:
  * classify units mod N into quadratic residues (QR={t² mod N}) and
    non-residues (NR); locate −1 ≡ N−1;
  * D(x;N,a) = π(x;N,a) − π(x;N,1);
  * rank of −1 among the NR classes by D (1 = largest), for every x;
  * VISIBILITY ONSET: smallest grid x past which −1 is (i) the strict
    max NR and (ii) in the top ⌈k/2⌉ of the k NR classes, AND stays so
    for every sampled x ≥ it ("sustained"); report "not sustained in
    range" otherwise;
  * TRANSIENT REVERSALS: sign changes of D(x;N,−1) (−1 vs principal)
    and rank-1 losses, with the x at which each occurs; the last such
    x is the empirical end-of-transient;
  * dominant oscillation wavelength of the normalised
    E(u)=D·√? -> we use E(u)=D(x)/ (√x/ln x) on a uniform u=ln x grid
    (linear interp from the geometric sample), via rFFT; compare to
    2π/γ_min(N) read from logs/lowzeros.out if present.

Usage:  analyze_curve.py <curve_tsv> [--emit-plotdata DIR]
"""
import sys, os, math, re
from collections import defaultdict
import numpy as np

def load(path):
    cnt = defaultdict(dict); tot = {}
    with open(path) as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip():
                continue
            p = ln.rstrip("\n").split("\t")
            if p[0] == "TOTAL":
                tot[(int(p[1]), int(p[2]))] = int(p[3])
            else:
                cnt[(int(p[0]), int(p[1]))][int(p[2])] = int(p[3])
    return cnt, tot

def qr_nr(N):
    U = [a for a in range(1, N) if math.gcd(a, N) == 1]
    QR = sorted({(a * a) % N for a in U})
    NR = sorted(set(U) - set(QR))
    return U, QR, NR

def read_gmin(path):
    g = {}
    if not os.path.exists(path):
        return g
    for ln in open(path):
        m = re.match(r"\s*(\d+)\s+\d+\s+([\d.]+)\s", ln)
        if m:
            g[int(m.group(1))] = float(m.group(2))
    return g

def main():
    path = sys.argv[1]
    emit = None
    if "--emit-plotdata" in sys.argv:
        emit = sys.argv[sys.argv.index("--emit-plotdata") + 1]
        os.makedirs(emit, exist_ok=True)
    cnt, tot = load(path)
    gmin = read_gmin(os.path.join(os.path.dirname(os.path.dirname(path)),
                                  "logs", "lowzeros.out"))
    Ns = sorted({N for (N, _) in cnt})
    xs_all = sorted({x for (_, x) in cnt})
    print(f"# curve: {path}")
    print(f"# {len(xs_all)} x-samples  [{xs_all[0]:.3e} .. {xs_all[-1]:.3e}]"
          .replace("e+", "e"))
    print(f"# moduli: {Ns}\n")

    summary = []
    for N in Ns:
        U, QR, NR = qr_nr(N)
        m1 = N - 1                                  # −1 mod N
        xs = [x for x in xs_all if (N, x) in cnt and 1 in cnt[(N, x)]]
        D = {a: np.array([cnt[(N, x)].get(a, 0) - cnt[(N, x)][1]
                          for x in xs], dtype=float) for a in U}
        xa = np.array(xs, dtype=float)

        # rank of −1 among NR by D (1 = largest)
        NRm = NR
        ranks = []
        for i in range(len(xs)):
            vals = sorted(((D[a][i], a) for a in NRm), reverse=True)
            order = [a for _, a in vals]
            ranks.append(order.index(m1) + 1)
        ranks = np.array(ranks)
        k = len(NRm)
        topg = math.ceil(k / 2)

        def sustained(pred):
            ok = np.array([pred(i) for i in range(len(xs))])
            for i in range(len(xs)):
                if ok[i] and ok[i:].all():
                    return xs[i]
            return None

        x_strict = sustained(lambda i: ranks[i] == 1)
        x_top    = sustained(lambda i: ranks[i] <= topg)

        # transient reversals: sign changes of D(−1) (−1 vs principal)
        d1 = D[m1]
        sgn = np.sign(d1)
        flips = [xs[i] for i in range(1, len(xs))
                 if sgn[i] != 0 and sgn[i-1] != 0 and sgn[i] != sgn[i-1]]
        # rank-1 losses (was top, then not)
        rank_losses = [xs[i] for i in range(1, len(xs))
                       if ranks[i-1] == 1 and ranks[i] != 1]
        last_rev = max(flips + rank_losses) if (flips or rank_losses) else None

        # dominant wavelength of normalised E(u), u=ln x, uniform grid
        u = np.log(xa)
        E = d1 / (np.sqrt(xa) / np.log(xa))
        wl = None
        if len(u) > 16 and u[-1] > u[0]:
            uu = np.linspace(u[0], u[-1], 1024)
            EE = np.interp(uu, u, E)
            EE = EE - EE.mean()
            sp = np.abs(np.fft.rfft(EE * np.hanning(len(EE))))
            fr = np.fft.rfftfreq(len(EE), d=(uu[1] - uu[0]))
            j = 1 + int(np.argmax(sp[1:]))
            if fr[j] > 0:
                wl = 1.0 / fr[j]                     # period in u=ln x

        gm = gmin.get(N)
        wl_pred = (2 * math.pi / gm) if gm else None

        last_i = len(xs) - 1
        print(f"## N={N}   −1≡{m1}∈{'NR' if m1 in NR else 'QR'}   "
              f"NR={NR} (k={k})")
        print(f"   D(−1) over range: "
              f"[{d1.min():+.0f} .. {d1.max():+.0f}], "
              f"end x={xs[last_i]:.3e} D(−1)={d1[last_i]:+.0f} "
              f"rank={ranks[last_i]}/{k}".replace("e+", "e"))
        print(f"   sustained STRICT-max(−1) onset: "
              f"{'x=%.3e' % x_strict if x_strict else 'NOT in sampled range'}"
              .replace("e+", "e"))
        print(f"   sustained TOP-⌈k/2⌉ onset      : "
              f"{'x=%.3e' % x_top if x_top else 'NOT in sampled range'}"
              .replace("e+", "e"))
        print(f"   sign changes of D(−1): {len(flips)}"
              + (f"  last at x={last_rev:.3e}".replace("e+", "e")
                 if last_rev else ""))
        if wl is not None:
            msg = f"   dominant Δln x wavelength (measured): {wl:.2f}"
            if wl_pred:
                msg += (f"   |  2π/γ_min(N={N}) = {wl_pred:.2f} "
                        f"(γ_min={gm:.4f})")
            print(msg)
        print()
        summary.append((N, m1, x_strict, x_top, len(flips), last_rev,
                        ranks[last_i], k, wl, wl_pred))

        if emit:
            with open(os.path.join(emit, f"N{N}.tsv"), "w") as fo:
                fo.write("x\tlnx\tD_m1\trank_m1\t" +
                         "\t".join(f"D_{a}" for a in U) + "\n")
                for i, x in enumerate(xs):
                    fo.write(f"{x}\t{u[i]:.6f}\t{d1[i]:.0f}\t{ranks[i]}\t" +
                             "\t".join(f"{D[a][i]:.0f}" for a in U) + "\n")

    print("# SUMMARY  (onsets are 'sustained over all sampled x>=onset')")
    print(f"# {'N':>3} {'-1':>3} {'strict_onset':>13} {'topgrp_onset':>13} "
          f"{'#signflip':>9} {'last_rev':>10} {'end_rank':>8} "
          f"{'wl_meas':>8} {'wl_pred':>8}")
    for (N, m1, xs_, xt, nf, lr, er, k, wl, wp) in summary:
        print(f"  {N:>3} {m1:>3} "
              f"{('%.2e'%xs_) if xs_ else 'none':>13} "
              f"{('%.2e'%xt) if xt else 'none':>13} "
              f"{nf:>9} {('%.2e'%lr) if lr else '-':>10} "
              f"{('%d/%d'%(er,k)):>8} "
              f"{('%.2f'%wl) if wl else '-':>8} "
              f"{('%.2f'%wp) if wp else '-':>8}")

if __name__ == "__main__":
    main()
