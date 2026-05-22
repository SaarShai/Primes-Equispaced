#!/usr/bin/env python3
"""Layer-2/3 verification harness for the -1-dominance dynamic curve.

Input: a curve TSV (schema:  N<TAB>x<TAB>a<TAB>count  and
TOTAL<TAB>N<TAB>x<TAB>pi_x), as emitted by mr1_sieve / mr1_par.

Three orthogonal checks (kept conceptually separate, as the project's
honesty norm requires -- each detects a different failure mode):

  (R) Residue-sum identity.  sum_a count(N,x,a) == pi_x(N,x), and pi_x is
      the SAME across all five N at a given x.  Detects mis-binning /
      lost or double-counted primes.  Internal-consistency only.

  (3.1) Dirichlet-character orthogonality (Koyama identity (3.1)):
      pi(x;N,a)-pi(x;N,1) == (1/phi(N)) * sum_chi (conj chi(a) - 1)*S(chi),
      S(chi) = sum_{r in (Z/N)*} c[r]*chi(r),
      computed via an INDEPENDENT character-sum code path (general
      finite-abelian (Z/N)*, so N=8's Klein-four group is handled too).
      Algebraically this is an identity for ANY integer vector c, so a
      large residual flags numeric corruption / a parser-level bug, not
      prime correctness.  Weak but independent.

  (A) pi(x) anchors.  At x = 10^k the total pi(x) is compared with the
      published value (hardcoded, each tagged [PUBLISHED]); these are
      the only ABSOLUTE check on the prime enumeration here.

Usage:  verify_curve.py <curve_tsv> [--max-resid 1e-3]
Exit 0 iff every check passes within tolerance.
"""
import sys, os, cmath, math
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chargrp import char_table, units            # correct, self-tested

# pi(10^k): primary public reference values.  [PUBLISHED] -- these are
# standard, widely tabulated (e.g. OEIS A006880) and additionally
# self-confirmed here by both independent sieves reproducing them.
PI_ANCHORS = {
    10**7:  664579,
    10**8:  5761455,
    10**9:  50847534,
    10**10: 455052511,
    10**11: 4118054813,
    10**12: 37607912018,
    10**13: 346065536839,
    10**14: 3204941750802,
}

def main():
    path = sys.argv[1]
    max_resid = 1e-3
    if "--max-resid" in sys.argv:
        max_resid = float(sys.argv[sys.argv.index("--max-resid") + 1])

    count = defaultdict(dict)          # count[(N,x)][a] = c
    tot   = {}                         # tot[(N,x)] = pi_x
    with open(path) as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip():
                continue
            p = ln.rstrip("\n").split("\t")
            if p[0] == "TOTAL":
                tot[(int(p[1]), int(p[2]))] = int(p[3])
            else:
                count[(int(p[0]), int(p[1]))][int(p[2])] = int(p[3])

    Ns = sorted({N for (N, _) in count})
    xs = sorted({x for (_, x) in count})
    ctab = {N: char_table(N) for N in Ns}

    n_R = n_31 = n_A = 0
    worst_31 = 0.0
    fail = []

    # (R) cross-N pi(x) agreement
    for x in xs:
        vals = {tot.get((N, x)) for N in Ns if (N, x) in tot}
        if len(vals) != 1:
            fail.append(f"[R] pi(x={x}) disagrees across N: {vals}")
        else:
            n_R += 1

    for N in Ns:
        U, chars = ctab[N]
        for x in xs:
            if (N, x) not in count:
                continue
            c = count[(N, x)]
            # (R) residue sum == pi_x
            s = sum(c.values())
            if (N, x) in tot and s != tot[(N, x)]:
                fail.append(f"[R] N={N} x={x}: sum={s} != pi_x={tot[(N,x)]}")
            # (3.1) identity for every coprime a
            cu = {r: c.get(r, 0) for r in U}
            Sl = [sum(cu[r] * ch[r] for r in U) for ch in chars]
            for a in U:
                direct = cu[a] - cu[1]
                rhs = sum((chars[k][a].conjugate() - 1) * Sl[k]
                          for k in range(len(chars))) / len(U)
                r = abs(rhs.real - direct) + abs(rhs.imag)
                worst_31 = max(worst_31, r)
                if r > max_resid:
                    fail.append(f"[3.1] N={N} x={x} a={a}: "
                                f"direct={direct} rhs={rhs:.4f} resid={r:.2e}")
                else:
                    n_31 += 1
            # (A) anchor
            if x in PI_ANCHORS and (N, x) in tot:
                if tot[(N, x)] != PI_ANCHORS[x]:
                    fail.append(f"[A] x={x}: pi_x={tot[(N,x)]} != "
                                f"published {PI_ANCHORS[x]}")
                else:
                    n_A += 1

    print(f"checks: (R) cross-N pi agree x-pts={n_R}/{len(xs)}")
    print(f"        (3.1) identity cells PASS={n_31}  worst residual={worst_31:.3e}")
    print(f"        (A) pi(x) anchors PASS={n_A}")
    if fail:
        print(f"FAIL ({len(fail)}):")
        for m in fail[:40]:
            print("  " + m)
        sys.exit(1)
    print("ALL CHECKS PASS")
    sys.exit(0)

if __name__ == "__main__":
    main()
