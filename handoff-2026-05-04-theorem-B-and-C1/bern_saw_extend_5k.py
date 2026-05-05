#!/usr/bin/env python3
"""
Extend Bern/Saw verification to p <= 5000 using float64.
Margin at p<=1019 is ~0.55; float precision is ample.
Append-only to bern_saw_extend.tsv (skip already-computed primes).
"""
import os, time
from sympy import primerange

def farey_seq_floats(N):
    a, b = 0, 1
    c, d = 1, N
    out = [(a, b)]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        out.append((a, b))
    return out

def bern_saw_float(p: int):
    F = farey_seq_floats(p - 1)
    n = len(F)
    nm1 = n - 1
    Bern = 0.0
    Saw = 0.0
    for i, (a, b) in enumerate(F):
        f = a / b
        D = i / nm1 - f
        Bern += D * (f - 0.5)
        # psi(p*f) = {p*a/b} - 1/2  (p not multiple of b for b>1; for b=1, f=0 or 1, psi=0)
        if b == 1:
            psi = 0.0
        else:
            r = (p * a) % b
            psi = r / b - 0.5
        Saw += D * psi
    return n, Bern, Saw

def existing_primes(path):
    s = set()
    if not os.path.exists(path): return s
    with open(path) as fh:
        next(fh, None)
        for line in fh:
            try: s.add(int(line.split("\t")[0]))
            except: pass
    return s

def main():
    out_path = "/Users/saar/Farey 4.7 solutions/bern_saw_extend.tsv"
    done = existing_primes(out_path)
    primes = [p for p in primerange(11, 5001) if p not in done]
    print(f"# remaining primes: {len(primes)}, first {primes[0] if primes else None}, last {primes[-1] if primes else None}")
    t0 = time.time()
    with open(out_path, "a") as fh:
        for p in primes:
            n, Bern, Saw = bern_saw_float(p)
            B_raw = Bern - Saw
            ratio = abs(Saw) / Bern if Bern > 0 else float('inf')
            fh.write(f"{p}\t{n}\t{Bern:.15g}\t{Saw:.15g}\t{ratio:.10g}\t{B_raw:.15g}\n")
            fh.flush()
            if p % 100 < 5 or p in (1021, 2003, 3001, 4001, 5000):
                print(f"  p={p:5d}  n={n:8d}  Bern={Bern:.6f}  Saw={Saw:.6f}  ratio={ratio:.6f}  B_raw>0? {B_raw>0}  t={time.time()-t0:.1f}s")
    # Summary
    ratios = []; margins = []; pos = 0; tot = 0
    with open(out_path) as fh:
        next(fh)
        for line in fh:
            parts = line.strip().split("\t")
            r = float(parts[4]); br = float(parts[5])
            ratios.append(r); margins.append(1-r)
            if br > 0: pos += 1
            tot += 1
    print(f"\nFINAL: {tot} primes, B_raw>0 count = {pos}/{tot}")
    print(f"max ratio = {max(ratios):.6f}, min ratio = {min(ratios):.6f}")
    print(f"min margin (1 - max_ratio) = {min(margins):.6f}")

if __name__ == "__main__":
    main()
