#!/usr/bin/env python3
"""Gold-standard cross-check: my dynamic curve vs the pre-existing,
independently-authored Phase-1 exact data.

Phase-1 (koyama_replication_bundle/) produced pi(x;N,a) at the 9
checkpoints {1e9,1e10,1.3e10,1e11,1.3e11,1e12,1.3e12,1e13,1.3e13} with
TWO independent implementations (out2.tsv = primesieve C++;
indep_full.tsv = hand-rolled C) that agree exactly, on a *different
machine*.  This script asserts my curve reproduces EVERY residue count
at EVERY overlapping checkpoint, for all N and all coprime residues a.

A single mismatch here means my sieve is wrong -- no curve analysis
proceeds until this is clean.

Usage:  xcheck_phase1.py <my_curve_tsv> <phase1_out2.tsv> [indep_full.tsv ...]
"""
import sys, re
from collections import defaultdict

def parse_phase1(path):
    """out2.tsv / indep_full.tsv: per-N 'count_a=' blocks. Return
    {(N,x,a): count} for a in 1..N-1."""
    res = {}
    N = None
    header = None
    with open(path) as f:
        for ln in f:
            ln = ln.rstrip("\n")
            m = re.match(r"## N = (\d+)", ln)
            if m:
                N = int(m.group(1)); header = None; continue
            if ln.startswith("# diffs"):
                N = None; continue        # stop at diff block
            if N is None or not ln or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if parts[0] == "x":
                header = [p for p in parts[1:]]      # count_a=1 ...
                continue
            if header is None:
                continue
            x = int(parts[0])
            for h, v in zip(header, parts[1:]):
                a = int(h.split("=")[1])
                res[(N, x, a)] = int(v)
    return res

def parse_curve(path):
    """mr1 schema: N<TAB>x<TAB>a<TAB>count (+ TOTAL lines)."""
    res = {}
    with open(path) as f:
        for ln in f:
            if ln.startswith("#") or ln.startswith("TOTAL") or not ln.strip():
                continue
            N, x, a, c = ln.split("\t")
            res[(int(N), int(x), int(a))] = int(c)
    return res

def main():
    mine = parse_curve(sys.argv[1])
    refs = {p: parse_phase1(p) for p in sys.argv[2:]}
    if not refs:
        sys.exit("need at least one phase-1 ref file")

    # 1) the phase-1 refs must agree with each other
    rps = list(refs)
    base = refs[rps[0]]
    for p in rps[1:]:
        d = [(k, base[k], refs[p][k]) for k in base
             if k in refs[p] and base[k] != refs[p][k]]
        if d:
            print(f"PHASE-1 REFS DISAGREE {rps[0]} vs {p}: {d[:5]}")
            sys.exit(1)
    print(f"phase-1 refs mutually consistent: "
          f"{', '.join(p.split('/')[-1] for p in rps)}")

    # 2) my curve must match phase-1 at every shared (N,x,a)
    shared_x = sorted({x for (_, x, _) in base} & {x for (_, x, _) in mine})
    n_ok = 0
    fails = []
    for (N, x, a), v in base.items():
        if (N, x, a) in mine:
            if mine[(N, x, a)] != v:
                fails.append(f"N={N} x={x} a={a}: mine={mine[(N,x,a)]} "
                             f"phase1={v}  d={mine[(N,x,a)]-v}")
            else:
                n_ok += 1
    miss = [k for k in base if k[1] in shared_x and k not in mine]
    print(f"shared checkpoints x: {shared_x}")
    print(f"cells compared: {n_ok} exact, {len(fails)} mismatch, "
          f"{len(miss)} missing-in-curve")
    if fails:
        print("MISMATCHES:")
        for s in fails[:40]:
            print("  " + s)
        sys.exit(1)
    if miss:
        print(f"MISSING (curve lacks these phase-1 cells): {miss[:10]}")
        sys.exit(1)
    print(f"GOLD CROSS-CHECK PASS: {n_ok} residue counts identical to "
          f"independently-authored Phase-1 across {len(shared_x)} checkpoints")
    sys.exit(0)

if __name__ == "__main__":
    main()
