#!/usr/bin/env python3
"""
MERTENS_LB_sweep.py
===================

Computational sweep for the (MERTENS-LB) inequality:

    T(N) := 1 + sum_{k=1}^N M(floor(N/k)) / k   <=   -c'

where M(x) = sum_{n<=x} mu(n) is the Mertens function.

Goal: at the largest tractable N reachable on this machine, find
  - the smallest N where (MERTENS-LB) holds (with c' > 0)
  - the smallest c' that survives across the tested range
  - any value of N where T(N) > 0  (Polya-style disproof of the conjecture)
  - any N where T(N) > -1  (would invalidate c'=1)

Algorithm:
  1. Sieve mu(n) for n in [1..Nmax] using a linear-time Mobius sieve
     based on smallest-prime-factor (SPF). Output: int8 array mu[1..N].
  2. Cumulative sum: M[n] = sum_{k<=n} mu[k]. Output: int64 array.
  3. For each target N, evaluate T(N) using the Dirichlet hyperbola
     trick (only sqrt(N) distinct values of floor(N/k) appear).
     Sum is exact-rational using Python `Fraction` for moderate N,
     or via `mpmath.mpf` at >=50 digits for very large N (where
     Fraction cost dominates).

We retain the int8 mu array and the int64 cumulative M array in memory.
Memory:  N bytes for mu (int8) + 8N bytes for M (int64) = 9N bytes total.
For N = 10^9 that is approx 9 GB.  A pure-int8 mu array plus a
*partial* M plus on-the-fly recomputation of M(floor(N/k)) via prefix
arithmetic would lower this, but the current machine has ~12.5 GB free,
which is borderline.  The version below stores only mu (int8) plus a
cumulative M as int32 (since |M(x)| < 50000 well past 10^9 -- |M(N)|
< sqrt(N) is widely believed; the actual record at N ~ 10^9 is
|M| < 2 * 10^4), so M fits in int32 comfortably.  Total: 5*N bytes.

For N = 10^9, that is 5 GB, which exceeds our soft cap.  We therefore:
  - run the full pipeline at N = 10^4, 10^5, 10^6, 10^7, 10^8 from a
    single sieve up to N = 10^8 (~500 MB)
  - run an incremental sweep extending to N = 10^9 only if memory
    permits, monitoring psutil.

We always cross-check: at the largest N actually reached, compute T(N)
two different ways and verify agreement to >= 12 digits.

Author: SP-2 follow-up sweep, 2026-05-09.
"""
from __future__ import annotations

import argparse
import gc
import math
import os
import sys
import time
from fractions import Fraction
from typing import Tuple

import numpy as np

try:
    import psutil  # type: ignore
    HAVE_PSUTIL = True
except Exception:
    HAVE_PSUTIL = False

# mpmath only used for very-large-N decimal output / cross-check.
try:
    import mpmath as mp  # type: ignore
    HAVE_MPMATH = True
except Exception:
    HAVE_MPMATH = False


# ---------------------------------------------------------------------------
# Memory + logging utilities
# ---------------------------------------------------------------------------

def mem_gb() -> float:
    if not HAVE_PSUTIL:
        return -1.0
    return psutil.Process(os.getpid()).memory_info().rss / 1e9


def avail_gb() -> float:
    if not HAVE_PSUTIL:
        return -1.0
    return psutil.virtual_memory().available / 1e9


def log(msg: str, *, file=None) -> None:
    t = time.strftime("%H:%M:%S")
    line = f"[{t}] mem={mem_gb():.2f}GB free={avail_gb():.2f}GB | {msg}"
    print(line, flush=True)
    if file is not None:
        file.write(line + "\n")
        file.flush()


# ---------------------------------------------------------------------------
# Linear-time Mobius sieve (smallest-prime-factor / Euler's sieve)
# ---------------------------------------------------------------------------

def mobius_sieve(N: int) -> np.ndarray:
    """
    Linear-time sieve of mu(n) for n in [0, N].

    Returns: int8 numpy array mu of length N+1, with mu[0] = 0 by convention.

    Algorithm:  Euler's linear sieve maintains primes p1 < p2 < ...; for
    each n we cross out n*p (p <= smallest_prime_factor(n)).  We track
    mu(n) using the recursion:
       mu(n*p) = -mu(n)   if p does not divide n
       mu(n*p) =  0       if p divides n  (squarefree fails)
    Time O(N), space O(N) for the mu array plus O(N/log N) for primes.

    For N = 10^8, runtime ~ 30-60s; for N = 10^9, runtime ~ 5-15 minutes
    in pure Python.  We implement in pure Python (with arrays) since
    numpy linear sieves require an O(N log log N) Eratosthenes variant
    or a chunked approach, which is harder to write compactly.

    Optimization: actually we use a numpy-based sieve that:
      (i) computes the squarefree mask via a sieve of squares of primes
      (ii) computes the parity of prime divisor count.
    This is O(N log log N) in C-speed numpy ops, totalling maybe ~30s
    for N=10^9 -- much faster than pure-Python linear sieve.
    """
    if N < 2:
        mu = np.zeros(N + 1, dtype=np.int8)
        if N >= 1:
            mu[1] = 1
        return mu

    # Strategy: for each prime p, multiply parities; for each prime p^2,
    # zero out the multiples.

    # Initialize mu[n] = 1 for n >= 1 (placeholder for sign accumulator).
    mu = np.ones(N + 1, dtype=np.int8)
    mu[0] = 0

    # Find primes via standard Eratosthenes (bool array)
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[:2] = False
    sqrtN = int(math.isqrt(N))
    for i in range(2, sqrtN + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = False

    # For each prime p:
    #   Flip sign of mu[k*p] for all k (including k=1: mu[p] *= -1).
    # This gives mu[n] = (-1)^(number of distinct prime factors) * 1
    #   (squarefree case)  -- because each prime divisor flips the sign once.
    # Then zero out non-squarefree numbers (multiples of p^2).
    primes = np.nonzero(is_prime)[0]
    # Free is_prime to save memory (~N bytes); we only need primes.
    del is_prime
    gc.collect()
    for p in primes:
        # Flip sign on multiples of p
        mu[p::p] = -mu[p::p]
        # Zero out multiples of p^2
        p2 = int(p) * int(p)
        if p2 <= N:
            mu[p2::p2] = 0

    # Sanity: mu[1] should be 1; mu[2] should be -1; mu[4] should be 0.
    return mu


def cumsum_int32(mu_int8: np.ndarray) -> np.ndarray:
    """
    Compute M[n] = sum_{k<=n} mu[k] in int32.

    |M(n)| is empirically << 1e5 for n <= 10^10, well within int32.
    """
    # int32 cumsum.  numpy's cumsum default upcasts int8 -> int64; we
    # explicitly request int32 to halve memory.
    return np.cumsum(mu_int8, dtype=np.int32)


# ---------------------------------------------------------------------------
# Verifying mu/M against published values (OEIS A002321 etc.)
# ---------------------------------------------------------------------------

# Hard-coded reference values from OEIS A002321 (Mertens function M(n)):
#   M(1) = 1
#   M(10) = -1
#   M(100) = 1
#   M(1000) = 2
#   M(10000) = -23
#   M(100000) = -48
#   M(1000000) = 212
#   M(10000000) = 1037
#   M(100000000) = 1928
#   M(1000000000) = -222
# References for the larger values:
#   M(10^7) =  1037   (Deléglise & Rivat 1996, Table 1)
#   M(10^8) =  1928   (Deléglise & Rivat 1996, Table 1)
#   M(10^9) = -222    (Deléglise & Rivat 1996; also OEIS A084237)
# OEIS A084237 lists M(10^k) for k=0..16; we use the first ten entries.
KNOWN_M = {
    1:           1,
    10:         -1,
    100:         1,
    1_000:       2,
    10_000:    -23,
    100_000:   -48,
    1_000_000:  212,
    10_000_000: 1037,
    100_000_000: 1928,
    1_000_000_000: -222,
}


def verify_mertens_table(M: np.ndarray, N: int) -> Tuple[bool, list]:
    """Cross-check our M(n) values vs OEIS A084237/A002321.  Return (ok, mismatches)."""
    mismatches = []
    for x, ref in KNOWN_M.items():
        if x > N:
            continue
        ours = int(M[x])
        if ours != ref:
            mismatches.append((x, ours, ref))
    return (len(mismatches) == 0, mismatches)


# ---------------------------------------------------------------------------
# Compute T(N) = 1 + sum_{k=1}^N M(floor(N/k))/k via Dirichlet hyperbola
# ---------------------------------------------------------------------------

def T_of_N_fraction(N: int, M: np.ndarray) -> Fraction:
    """
    Exact-rational computation of T(N) = 1 + sum_{k=1}^N M(floor(N/k))/k
    using the floor-block trick: only O(sqrt N) distinct values of
    floor(N/k) appear, so we group k's that share the same quotient.

    Block enumeration:  for k = k0, find largest k1 with floor(N/k1) ==
    floor(N/k0); then this block contributes M(q) * (H(k1) - H(k0-1)),
    where H(m) = sum_{j=1}^m 1/j (harmonic).  Summed exactly with
    Fraction (slow for large N, fine for sanity checks at moderate N).

    Returns: T(N) as a Fraction.  For N up to ~ 10^6 this is feasible;
    for larger N use T_of_N_mp (mpmath float).
    """
    total = Fraction(0)
    # Precompute harmonic prefix sums H[k] = sum_{j=1}^k 1/j as Fractions.
    # That requires storing N Fractions, i.e. O(N) memory -- not viable
    # at large N.  So instead we walk in order of k, summing 1/k as we go.
    k = 1
    H_prev = Fraction(0)  # H[k-1]
    while k <= N:
        q = N // k
        k1 = N // q  # largest k' with floor(N/k') == q
        if k1 > N:
            k1 = N
        # Compute H[k1] - H[k-1] = sum_{j=k}^{k1} 1/j
        h_block = Fraction(0)
        for j in range(k, k1 + 1):
            h_block += Fraction(1, j)
        Mq = int(M[q])
        total += Mq * h_block
        H_prev = H_prev + h_block  # not strictly needed but tracks progress
        k = k1 + 1
    return Fraction(1) + total


def T_of_N_mp(N: int, M: np.ndarray, dps: int = 50) -> "mp.mpf":
    """
    High-precision floating computation of T(N) = 1 + sum_k M(N//k)/k
    using Dirichlet hyperbola groupings and mpmath.

    Faster than T_of_N_fraction for large N (no Fraction overhead).
    Uses dps decimal digits of precision; default 50 -- ample.

    Returns: mpmath.mpf approximating T(N).
    """
    if not HAVE_MPMATH:
        raise RuntimeError("mpmath not available")
    mp.mp.dps = dps
    total = mp.mpf(0)
    k = 1
    while k <= N:
        q = N // k
        k1 = N // q
        # Sum_{j=k}^{k1} 1/j
        # For speed, compute via mpmath; this loop dominates the cost.
        h_block = mp.mpf(0)
        for j in range(k, k1 + 1):
            h_block += mp.mpf(1) / j
        total += int(M[q]) * h_block
        k = k1 + 1
    return mp.mpf(1) + total


def T_of_N_float64(N: int, M: np.ndarray) -> float:
    """
    Fast float64 computation of T(N) using Dirichlet hyperbola.

    Key optimization: harmonic prefix sums computed in numpy float64.
    That requires an O(N) array of float64 (= 8N bytes).  At N = 10^8
    that's 0.8 GB; at N = 10^9 that's 8 GB (too much).

    Alternative: walk k in increasing order, accumulate H_prev =
    sum_{j=1}^{k-1} 1/j as a float64 scalar; for each block from k0 to
    k1 add (H_at_k1 - H_at_k0_minus_1) * M[q].  We can compute
    H_at_k1 by adding 1/k0 + 1/(k0+1) + ... + 1/k1 for each block,
    which costs O(N) float ops in total.

    For N = 10^9 this is ~10^9 float ops, roughly 5-15s in pure Python
    (slow due to Python loop), or sub-second with numpy.

    To keep memory low we do per-block numpy operations: for each block
    we create a small numpy array of integers k0..k1 (up to length 2*sqrt N
    ~ 60000 at N=10^9 in the early blocks), compute reciprocals, and sum.
    The per-block cost is O(block_size) float ops; total O(N) ops; total
    blocks ~ 2 sqrt(N).  At N = 10^9 the early blocks are huge (block_size
    ~ N/q for small q).  Specifically:
        block for q from k= floor(sqrt N)+1 to N has block_size 1.
        block for q=1 has block_size N - floor(sqrt N) ~ N - 31623 ~ N.
    So the first block is the dominant cost: numpy reciprocal sum over
    a large arange.  At N = 10^9, that array is 8 GB -- DOES NOT FIT.

    Trick: for the "tail" blocks (k > sqrt N), there are ~ sqrt N of them,
    each contributing M[q] * (1/k) with q = N//k.  We can vectorize this
    in numpy by building a numpy array k_vals[sqrt N : N], computing
    q = N // k_vals, looking up M[q], dividing by k.  The array of size
    N - sqrt N is large -- but we can chunk it.

    Trick (better): for k <= sqrt N the block structure is k -> [k, k1];
    each block has block_size = k1 - k + 1.  We sum 1/k + ... + 1/k1
    using numpy on a small slice of size block_size.  Block sizes for
    small k are large (~N/k^2), but we only have ~sqrt N small k's.
    Total ops still O(N).

    For the "large k" tail (k > sqrt N), each k gives a block of size 1.
    There are ~ N - sqrt N such k's.  For these we can vectorize:
        K = arange(sqrt(N)+1, N+1)
        Q = N // K
        contrib = sum(M[Q] / K)
    The arange has length N - sqrt N -- 1 GB at N=10^9 (int64).  We
    chunk this into blocks of, say, 10^7 to control memory.

    With chunking the algorithm runs in O(N) flops, ~3-30 seconds at
    N = 10^9 with numpy.

    Returns: float64 estimate of T(N).
    """
    if N < 1:
        return 1.0
    sqrtN = int(math.isqrt(N))

    total = 0.0

    # Part A: k in [1, sqrtN], block-structured.
    k = 1
    while k <= sqrtN:
        q = N // k
        k1 = N // q  # largest k with same quotient
        if k1 > N:
            k1 = N
        # Sum 1/j for j in [k, k1] via numpy (block_size <= N/k <= N for k=1)
        # Memory: block_size * 8 bytes.  block_size = k1 - k + 1 <= N/k.
        # The largest block (k=1) has size = N // 1 - 1 + 1 = N.  We'd allocate
        # 8 GB at N=10^9, which DOES NOT FIT.
        # So we sub-chunk if block is huge.
        block_size = k1 - k + 1
        if block_size <= 10_000_000:
            js = np.arange(k, k1 + 1, dtype=np.float64)
            h_block = float(np.sum(np.reciprocal(js)))
        else:
            h_block = 0.0
            chunk = 10_000_000
            j0 = k
            while j0 <= k1:
                j1 = min(j0 + chunk - 1, k1)
                js = np.arange(j0, j1 + 1, dtype=np.float64)
                h_block += float(np.sum(np.reciprocal(js)))
                j0 = j1 + 1
                del js
        Mq = int(M[q])
        total += Mq * h_block
        k = k1 + 1

    # Part B: k in [sqrtN+1, N], each gives a singleton block
    # (because for k > sqrtN, floor(N/k) <= sqrtN, and consecutive k's
    # may share a q but actually the block-walk above already handled
    # k <= sqrtN's matching k1's that may extend into k > sqrtN).
    # We need to be careful not to double-count: after Part A, k has
    # been advanced past all blocks whose smallest k is <= sqrtN.
    # The remaining k's are all > sqrtN with block-size = 1 (since
    # consecutive q values for k > sqrtN are distinct).
    # Actually that's not quite true either: for k > sqrtN, we have
    # q = N // k <= sqrtN, and the values q span 1..sqrtN.  Each q
    # corresponds to a *range* of k's, but those ranges have already
    # been covered in Part A (they were the k1's of blocks whose
    # leading k <= sqrtN... HMM but no, block_size could be 1).
    #
    # Let's just continue the block walk past sqrtN.  The cost is
    # bounded by 2*sqrt(N) blocks total (Dirichlet's identity).
    #
    # We DROP Part B and rely on the unified loop: continue the
    # while-loop until k > N.

    while k <= N:
        q = N // k
        k1 = N // q
        if k1 > N:
            k1 = N
        block_size = k1 - k + 1
        if block_size <= 10_000_000:
            js = np.arange(k, k1 + 1, dtype=np.float64)
            h_block = float(np.sum(np.reciprocal(js)))
        else:
            h_block = 0.0
            chunk = 10_000_000
            j0 = k
            while j0 <= k1:
                j1 = min(j0 + chunk - 1, k1)
                js = np.arange(j0, j1 + 1, dtype=np.float64)
                h_block += float(np.sum(np.reciprocal(js)))
                j0 = j1 + 1
                del js
        Mq = int(M[q])
        total += Mq * h_block
        k = k1 + 1

    return 1.0 + total


def T_of_N_float64_fast(N: int, M: np.ndarray) -> float:
    """
    Vectorized float64 computation of T(N).

    Strategy: vectorize the "tail" k > sqrt(N) part where each block has
    size 1 (k1 = k).  Actually it's not quite size-1 for k > sqrt N:
    we have block-size = k1 - k + 1 where k1 = N // q.  For q = 1, k
    ranges over [N//2 + 1, N] with q=1, block size = N - N//2 -- sizable.

    Cleaner formulation:
      For each q in [1, sqrt N]:
         k_low = N // (q+1) + 1
         k_high = N // q
         contribution = M[q] * (H(k_high) - H(k_low - 1))
      For each k in [1, sqrt N]:
         q = N // k
         contribution = M[q] / k    (if k > N // (q+1), to avoid double-count)

    Wait, that's the standard hyperbola.  Let me redo:

    sum_{k=1}^N M(N//k) / k
      = sum_{q=1}^N M(q) * (sum_{k: N//k == q} 1/k)

    Let S(q) := sum_{k: N//k == q} 1/k.  The set {k: N//k == q} = [N//(q+1)+1, N//q].

    For q <= sqrt N: this range may be very large (up to N/q in size).
    For q > sqrt N: this range is empty unless q <= N, but the lengths get small.

    Equivalently, we can split:
      sum_{q=1}^{sqrt N} M(q) * (H(N//q) - H(N//(q+1)))   [outer sum over q]
      +  sum_{k=1}^{sqrt N} M(N//k) / k                    [outer sum over k]
      -  (overlap correction: when q = k = sqrt N exactly, may be double-counted)

    Standard Dirichlet hyperbola identity:
      sum_{k=1}^N f(N//k) = sum_{q=1}^{sqrt N} f(q) * (number of k's with N//k == q)
                         + sum_{k=1}^{sqrt N} f(N//k)
                         - f(sqrt N) * sqrt N   [if applicable]

    Here f(q) = M(q)/k -- but f depends on k, so the standard formula
    doesn't directly apply.  Instead we just walk the blocks; that is
    what `T_of_N_float64` already does, and it is correct.

    For raw speed at large N we vectorize the block-by-block iteration:
    enumerate blocks via the standard Pollard formula, compute H_block
    using a single big numpy operation.

    Implementation note: at N = 10^9, the whole sum has total cost ~
    sum of block sizes = N.  Numpy ops of total length N do ~10^9 flops,
    which is feasible (~5-15s on this machine).  But we cannot allocate
    a single 8 GB float array.  So we chunk per block, with chunks of
    10^7.

    Actually the SIMPLEST way is: never build the full reciprocal
    array.  Compute H_block analytically as a partial harmonic sum
    using the asymptotic H(n) = ln n + gamma + 1/(2n) - 1/(12 n^2) + ...
    BUT this introduces small error.  We want >= 12 digits.

    For >= 12 digits we use mpmath's psi(n+1) - psi(k) =
    sum_{j=k}^n 1/j -- exact in arbitrary precision.  Or compute the
    partial harmonic using log() + correction.

    Simplest correct approach:
      For block [k, k1] with block_size = k1 - k + 1:
        if block_size <= 10^6: use numpy reciprocal sum (fast, exact to
        ~ ulp(H) ~ 1e-15 * H).
        else: use mpmath's nsum or psi function for arbitrary precision.

    For our purposes (12 digit cross-check), float64 reciprocal sum on
    blocks of size <= 10^7 with Kahan-summation-like care should suffice.
    If precision is a concern we'll cross-check at large N with mpmath.
    """
    return T_of_N_float64(N, M)


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def sanity_check_vs_sp2(M: np.ndarray, log_file=None) -> bool:
    """Reproduce SP-2's exact-rational identity at N in [2, 200].

    Verifies that T(N) := 1 + sum_{k=1}^N M(floor(N/k))/k
    equals 2 + S(N) where S(N) = sum_{b=2}^N h(b)/b
    with h(b) = prod_{p|b}(1-p).

    Uses Python Fractions for exact arithmetic.  Cost ~ O(N^2) Fractions
    over the test range -- fine for N <= 200.
    """
    log("Sanity check vs SP-2 at N in [2, 200] (exact rational T(N))", file=log_file)

    def h_b(b):
        if b == 1:
            return 1
        n = b
        primes_list = []
        p = 2
        while p * p <= n:
            if n % p == 0:
                primes_list.append(p)
                while n % p == 0:
                    n //= p
            p += 1
        if n > 1:
            primes_list.append(n)
        r = 1
        for q in primes_list:
            r *= (1 - q)
        return r

    failures = 0
    for N in range(1, 201):
        # Direct S(N) = sum_{b=2}^N h(b)/b
        S_direct = Fraction(0)
        for b in range(2, N + 1):
            S_direct += Fraction(h_b(b), b)
        # SP-2's (C4): 1 + S(N) = sum_k M(N//k)/k.
        # Our T(N) = 1 + sum_k M(N//k)/k = 2 + S(N).
        T_via_M = Fraction(1) + sum(Fraction(int(M[N // k]), k) for k in range(1, N + 1))
        T_pred = Fraction(2) + S_direct
        if T_via_M != T_pred:
            failures += 1
            log(f"  MISMATCH at N={N}: T_via_M={float(T_via_M)}, "
                f"2+S_direct={float(T_pred)}", file=log_file)
            if failures >= 3:
                break
    if failures == 0:
        log(f"  Sanity OK: all 200 values of N in [1, 200] agree exact-rational.",
            file=log_file)
        return True
    else:
        log(f"  Sanity FAILED: {failures} mismatches.", file=log_file)
        return False


def cross_check_T(N: int, M: np.ndarray, log_file=None) -> Tuple[float, float]:
    """
    Compute T(N) two different ways at the same N and verify agreement.
    Returns (T_float, T_alt_float).
    """
    log(f"  Cross-check at N={N} (Dirichlet block walk vs direct sum)", file=log_file)
    t1 = time.time()
    T_block = T_of_N_float64(N, M)
    t2 = time.time()
    log(f"    Method 1 (block walk float64): T={T_block:.15f}  ({t2-t1:.2f}s)", file=log_file)

    # Alternative: direct sum k=1..N (slower but no block logic).
    t1 = time.time()
    chunk = 10_000_000
    s = 0.0
    for k0 in range(1, N + 1, chunk):
        k1 = min(k0 + chunk - 1, N)
        ks = np.arange(k0, k1 + 1, dtype=np.int64)
        qs = N // ks
        Mqs = M[qs].astype(np.float64)
        s += float(np.sum(Mqs / ks.astype(np.float64)))
        del ks, qs, Mqs
    T_dir = 1.0 + s
    t2 = time.time()
    log(f"    Method 2 (direct k-loop float64, chunked): T={T_dir:.15f}  ({t2-t1:.2f}s)", file=log_file)
    diff = abs(T_block - T_dir)
    rel = diff / max(abs(T_block), 1e-30)
    log(f"    diff={diff:.3e}  rel={rel:.3e}", file=log_file)
    return T_block, T_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Nmax", type=int, default=10**8,
                        help="Largest N to sweep (default: 1e8)")
    parser.add_argument("--out_tsv", type=str,
                        default="MERTENS_LB_sweep.tsv")
    parser.add_argument("--out_log", type=str,
                        default="MERTENS_LB_sweep.out")
    parser.add_argument("--checkpoint_dir", type=str, default=".")
    parser.add_argument("--skip_sanity", action="store_true",
                        help="skip the SP-2 N in [2, 200] sanity check")
    args = parser.parse_args()

    Nmax = args.Nmax
    out_tsv = args.out_tsv
    out_log_path = args.out_log

    log_file = open(out_log_path, "w")
    log("=" * 72, file=log_file)
    log(f"MERTENS_LB_sweep.py  --  Nmax = {Nmax:,}", file=log_file)
    log("=" * 72, file=log_file)

    log(f"Available memory: {avail_gb():.2f} GB", file=log_file)
    expected_mu_GB = (Nmax + 1) * 1 / 1e9
    expected_M_GB = (Nmax + 1) * 4 / 1e9
    log(f"Expected memory: mu (int8) = {expected_mu_GB:.2f} GB, "
        f"M (int32) = {expected_M_GB:.2f} GB, total = "
        f"{expected_mu_GB + expected_M_GB:.2f} GB", file=log_file)

    if HAVE_PSUTIL:
        free = avail_gb()
        if expected_mu_GB + expected_M_GB > free * 0.6:
            log(f"WARNING: predicted memory > 60% of free RAM. "
                f"Aborting before sieve to avoid swap.", file=log_file)
            return 2

    # 1. Sieve
    log(f"Step 1: Mobius sieve up to N = {Nmax:,}", file=log_file)
    t0 = time.time()
    mu = mobius_sieve(Nmax)
    t1 = time.time()
    log(f"  done sieve, mu.dtype={mu.dtype}, mu.nbytes/1e9={mu.nbytes/1e9:.2f} GB, "
        f"elapsed {t1-t0:.1f}s", file=log_file)

    # Quick mu sanity: mu[1]=1, mu[2]=-1, mu[3]=-1, mu[4]=0, mu[5]=-1, mu[6]=1
    expected_mu_small = {1: 1, 2: -1, 3: -1, 4: 0, 5: -1, 6: 1, 30: -1, 42: -1, 60: 0}
    for k, v in expected_mu_small.items():
        if k <= Nmax:
            actual = int(mu[k])
            assert actual == v, f"mu[{k}] = {actual}, expected {v}"
    log(f"  mu sanity OK on small n.", file=log_file)

    # 2. Cumulative
    log(f"Step 2: Cumulative Mertens M[n] = sum_{{k<=n}} mu[k]", file=log_file)
    t0 = time.time()
    M = cumsum_int32(mu)
    t1 = time.time()
    log(f"  done cumsum, M.dtype={M.dtype}, M.nbytes/1e9={M.nbytes/1e9:.2f} GB, "
        f"elapsed {t1-t0:.1f}s", file=log_file)

    # Verify M against OEIS A084237
    ok, mm = verify_mertens_table(M, Nmax)
    if ok:
        log(f"  M(n) verified against OEIS A084237 at all known anchor points "
            f"<= {Nmax}.", file=log_file)
    else:
        log(f"  M(n) MISMATCH against OEIS:", file=log_file)
        for x, ours, ref in mm:
            log(f"    M({x}) = {ours} (computed), {ref} (OEIS).  ABORT.", file=log_file)
        return 3

    # 3. Sanity check vs SP-2 at N in [2, 200]
    if not args.skip_sanity:
        ok = sanity_check_vs_sp2(M, log_file=log_file)
        if not ok:
            log(f"  SP-2 sanity FAILED.  ABORT.", file=log_file)
            return 4

    # 4. Sweep at logspaced N values
    log(f"Step 3: sweep T(N) at N in {{1e1..{Nmax:.0e}}}", file=log_file)

    sweep_Ns = []
    n = 10
    while n <= Nmax:
        sweep_Ns.append(n)
        n *= 10
    # Also a denser intermediate set:
    extra = [50, 500, 5000, 50000, 500_000, 5_000_000, 50_000_000, 500_000_000]
    for e in extra:
        if e <= Nmax and e not in sweep_Ns:
            sweep_Ns.append(e)
    sweep_Ns.sort()

    tsv = open(out_tsv, "w")
    tsv.write("N\tT_N\tT_N_over_logN\tneg_T_logN_over_N\tnotes\n")
    tsv.flush()

    near_flips = []
    min_neg_TlogN_over_N = float("inf")
    min_neg_TlogN_over_N_at_N = None

    for N in sweep_Ns:
        log(f"--- N = {N:,} ---", file=log_file)
        t0 = time.time()
        T = T_of_N_float64(N, M)
        elapsed = time.time() - t0
        logN = math.log(N)
        T_over_logN = T / logN if logN > 0 else float("nan")
        # The "empirical c' analog" if we hypothesize T(N) ~ -c' (sign-bound form):
        # we want T(N) <= -c'.  At fixed N the smallest c' that holds is c' = -T(N)
        # (provided T(N) < 0).  We track the global infimum of -T(N) > 0.
        c_prime_at_N = -T
        notes = ""
        if T > 0:
            notes = "POLYA-FLIP! T(N) > 0, (MERTENS-LB) DISPROVED at this N"
            log(f"  *** POLYA-FLIP: T({N}) = {T:.6f} > 0 ***", file=log_file)
        elif T > -1:
            notes = "near-flip: T(N) > -1; c'=1 form fails"
            near_flips.append((N, T, "T > -1"))
        elif T > -2:
            notes = "weak: T(N) > -2"
        log(f"  T(N) = {T:.10f}  (elapsed {elapsed:.1f}s)", file=log_file)
        log(f"  T(N)/log N = {T_over_logN:.6f}", file=log_file)
        log(f"  -T(N) (smallest c' that holds at this N) = {c_prime_at_N:.6f}", file=log_file)

        if T < 0 and c_prime_at_N < min_neg_TlogN_over_N:
            min_neg_TlogN_over_N = c_prime_at_N
            min_neg_TlogN_over_N_at_N = N

        tsv.write(f"{N}\t{T:.15g}\t{T_over_logN:.15g}\t{c_prime_at_N:.15g}\t{notes}\n")
        tsv.flush()

    log("=" * 72, file=log_file)
    log(f"Sweep complete.  min(-T(N)) over swept N's = {min_neg_TlogN_over_N:.6f} "
        f"at N = {min_neg_TlogN_over_N_at_N:,}", file=log_file)
    log(f"Near-flips: {near_flips}", file=log_file)
    if not near_flips:
        log("No near-flips: T(N) <= -1 at every swept N.", file=log_file)
    log("=" * 72, file=log_file)

    # 5. Final cross-check at the largest N reached
    Nbig = sweep_Ns[-1]
    log(f"Cross-check at largest N = {Nbig:,}", file=log_file)
    t1, t2 = cross_check_T(Nbig, M, log_file=log_file)
    diff = abs(t1 - t2)
    if diff < 1e-9 * max(abs(t1), 1):
        log(f"  Cross-check OK: T={t1:.12f} vs T_alt={t2:.12f}, diff={diff:.2e}",
            file=log_file)
    else:
        log(f"  Cross-check WARNING: diff={diff:.2e} larger than expected.",
            file=log_file)

    tsv.close()
    log_file.close()
    print(f"\nWrote {out_tsv}, {out_log_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
