#!/usr/bin/env python3
"""Figures for the −1-dominance dynamic curve (matplotlib if available;
always also writes the underlying plotdata TSVs so the figures are
reproducible without the plotting lib).

Usage:  plot_curve.py <curve_tsv> <outdir>
Produces, per N:  D(x;N,a) vs log10 x for all coprime a, with the
−1 class highlighted and y=0 marked; and a rank-of-−1 vs log10 x panel.
"""
import sys, os, math
from collections import defaultdict

def load(path):
    cnt = defaultdict(dict)
    with open(path) as f:
        for ln in f:
            if ln.startswith("#") or ln.startswith("TOTAL") or not ln.strip():
                continue
            N, x, a, c = ln.split("\t")
            cnt[(int(N), int(x))][int(a)] = int(c)
    return cnt

def qr_nr(N):
    U = [a for a in range(1, N) if math.gcd(a, N) == 1]
    QR = sorted({(a*a) % N for a in U})
    return U, QR, sorted(set(U) - set(QR))

def main():
    path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    cnt = load(path)
    Ns = sorted({N for (N, _) in cnt})
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        have_mpl = True
    except Exception:
        have_mpl = False

    for N in Ns:
        U, QR, NR = qr_nr(N)
        m1 = N - 1
        xs = sorted(x for (n, x) in cnt if n == N and 1 in cnt[(N, x)])
        lx = [math.log10(x) for x in xs]
        D = {a: [cnt[(N, x)].get(a, 0) - cnt[(N, x)][1] for x in xs]
             for a in U}
        # plotdata TSV (always)
        with open(os.path.join(outdir, f"plotdata_N{N}.tsv"), "w") as fo:
            fo.write("log10x\t" + "\t".join(f"D_{a}"
                     + ("(-1)" if a == m1 else
                        "(NR)" if a in NR else "(QR)") for a in U) + "\n")
            for i in range(len(xs)):
                fo.write(f"{lx[i]:.5f}\t" +
                         "\t".join(str(D[a][i]) for a in U) + "\n")
        if not have_mpl:
            continue
        fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True,
                               gridspec_kw={"height_ratios": [3, 1]})
        for a in U:
            if a == m1:
                continue
            ax[0].plot(lx, D[a], lw=0.7, alpha=0.45,
                       color="tab:red" if a in NR else "tab:gray")
        ax[0].plot(lx, D[m1], lw=2.0, color="black",
                   label=f"a=−1≡{m1} (NR)")
        ax[0].axhline(0, color="k", lw=0.6, ls=":")
        ax[0].set_ylabel("π(x;N,a) − π(x;N,1)")
        ax[0].set_title(f"N={N}: dynamic prime-race curve "
                        f"(red=non-residues, gray=residues, black=−1)")
        ax[0].legend(loc="upper left", fontsize=8)
        # rank of −1 among NR
        rk = []
        for i in range(len(xs)):
            vals = sorted(((D[a][i], a) for a in NR), reverse=True)
            rk.append([a for _, a in vals].index(m1) + 1)
        ax[1].step(lx, rk, where="post", color="black", lw=1.0)
        ax[1].set_ylabel(f"rank of −1\n(1=max of {len(NR)} NR)")
        ax[1].set_xlabel("log10 x")
        ax[1].invert_yaxis()
        ax[1].axhline(1, color="tab:green", lw=0.6, ls="--")
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, f"curve_N{N}.png"), dpi=130)
        plt.close(fig)
    print(f"wrote plotdata (+pngs={have_mpl}) for N={Ns} to {outdir}")

if __name__ == "__main__":
    main()
