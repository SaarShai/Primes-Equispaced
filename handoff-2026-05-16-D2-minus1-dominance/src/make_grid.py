#!/usr/bin/env python3
"""Deterministic snapshot-grid generator for the -1-dominance dynamic curve.

Emits an ascending list of integer x checkpoints (one per line). The grid is:
  * geometric, PTS_PER_DECADE points/decade from 1e6 to 3e14 (fine enough to
    resolve log-x oscillations from low-lying L-zeros: spacing ~0.02 in log10
    resolves "periods" >~0.1, i.e. zero ordinates gamma up to ~60);
  * UNION the 9 exact Phase-1 checkpoints (lets us diff bit-exactly against
    koyama_replication_bundle/out2.tsv & indep_full.tsv);
  * UNION the round pi(x) anchors 1e7..3e14 (absolute pi(x) checks);
  * UNION e^{33.4} ~ 3.19e14 (Koyama's claimed N=23 dominance-onset scale).

Usage:  make_grid.py <out_full> <out_1p3e13>
"""
import sys, math

PTS_PER_DECADE = 50
LO = 10**6
HI = 3 * 10**14

PHASE1 = [1_000_000_000, 10_000_000_000, 13_000_000_000,
          100_000_000_000, 130_000_000_000,
          1_000_000_000_000, 1_300_000_000_000,
          10_000_000_000_000, 13_000_000_000_000]
ANCHORS = [10**k for k in range(7, 15)] + [2*10**14, 3*10**14]
SPECIAL = [round(math.exp(33.4))]            # ~3.19e14, N=23 onset (Koyama)

def main():
    if len(sys.argv) < 3:
        sys.exit("usage: make_grid.py <out_full> <out_1p3e13>")
    n_dec = math.log10(HI) - math.log10(LO)
    npts = int(round(n_dec * PTS_PER_DECADE))
    geo = {int(round(10 ** (math.log10(LO) + i * (n_dec / npts))))
           for i in range(npts + 1)}
    pts = sorted(geo | set(PHASE1) | set(ANCHORS) | set(SPECIAL))
    pts = [p for p in pts if LO <= p <= HI]

    with open(sys.argv[1], "w") as f:
        f.write("\n".join(map(str, pts)) + "\n")
    sub = [p for p in pts if p <= 13_000_000_000_000]
    with open(sys.argv[2], "w") as f:
        f.write("\n".join(map(str, sub)) + "\n")

    print(f"full grid: {len(pts)} pts  [{pts[0]} .. {pts[-1]}]")
    print(f"<=1.3e13 : {len(sub)} pts  [{sub[0]} .. {sub[-1]}]")
    print(f"Phase-1 checkpoints all present: "
          f"{all(c in set(pts) for c in PHASE1)}")

if __name__ == "__main__":
    main()
