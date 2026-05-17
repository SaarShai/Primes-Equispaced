"""
D4 -- DUAL numeric confirmation, CORRECTED restricted-algorithm object.

The transfer operator  H_{s,q} f(x) = sum_{gcd(m,q)=1} (m+x)^{-2s} f(1/(m+x))
is, exactly, the generating operator of the RESTRICTED-DIGIT continued
fraction: its quasi-inverse (I - H_{s,q})^{-1} sums  prod |h_w'|^s  over all
finite words  w = (m_1,...,m_P)  with every m_i in A_q = {m: gcd(m,q)=1}.
The corresponding algorithm is the Euclidean / Gauss algorithm run on the
rationals whose COMPLETE CF expansion uses only admissible digits, ordered
by continuant (denominator) size N -- precisely Vallee's "Euclidean algorithm
with restricted digits" (Fast Class, infinite admissible alphabet A_q).

This is the lens-faithful object: "a prime step inserts only genuinely-new
(coprime-to-q) digits" => the algorithm's digit alphabet IS A_q, and the
inputs it acts on are exactly the continuants built from A_q.

We confirm  mu_q = 2/|lambda_q'(1)|  two independent ways:
 (A) SPECTRAL  : lambda_q'(1) by finite difference of dominant eigenvalue.
 (B) COMBINATORIC SIMULATION : enumerate every reduced p/k, k<=N, whose CF
     digits all lie in A_q (exact integer recursion on continuants), record
     the number of CF steps P_q, regress E_N[P_q] on log N. Slope = mu_q.
Exact integer arithmetic throughout (B): continuants via the standard
p_i = a_i p_{i-1} + p_{i-2} recursion, no floating point.
"""
import numpy as np
from math import gcd, log


# ---------- (A) spectral (vectorized barycentric Nystrom) ----------
def _nodes_weights(n):
    j = np.arange(n)
    x = 0.5 * (1.0 - np.cos(np.pi * (j + 0.5) / n))
    bw = np.ones(n)
    for k in range(n):
        bw[k] = 1.0 / np.prod(x[k] - np.delete(x, k))
    return x, bw


def _interp_matrix(xq, x, bw):
    """Rows = barycentric Lagrange evaluation of each xq[i] at nodes x."""
    D = xq[:, None] - x[None, :]            # (Q, n)
    T = bw[None, :] / D
    # exact-node hits (D==0) -> unit row
    hit = np.isclose(D, 0.0)
    if hit.any():
        rows_hit = hit.any(axis=1)
        T[rows_hit] = 0.0
        T[hit] = 1.0
    return T / T.sum(axis=1, keepdims=True)


def build_Hs_q(s, q, n=160, Mmax=6000):
    """
    H_{s,q} matrix.  Tail branches m>Mmax contribute O(sum_{m>Mmax} m^{-2s})
    ~ Mmax^{1-2s}/(2s-1) < 1e-4 at s~1, Mmax=6000 -- negligible vs the
    discretization error, and the DUAL simulation is the real cross-check.
    """
    x, bw = _nodes_weights(n)
    ms = np.array([m for m in range(1, Mmax + 1) if gcd(m, q) == 1], dtype=float)
    A = np.zeros((n, n))
    # process branches in chunks to bound memory
    CH = 2000
    for c0 in range(0, len(ms), CH):
        mc = ms[c0:c0 + CH]                          # (B,)
        # for each branch m and node x_i: g = 1/(m+x_i), w = (1/(m+x_i))^{2s}
        MX = mc[:, None] + x[None, :]                # (B, n)
        G = 1.0 / MX                                 # (B, n) images
        W = G ** (2.0 * s)                           # (B, n) weights
        for bi in range(mc.shape[0]):
            P = _interp_matrix(G[bi], x, bw)         # (n, n)
            A += W[bi][:, None] * P
    return A


def dom(A):
    v = np.linalg.eigvals(A)
    return v[np.argmax(np.abs(v))].real


def spectral_mu_q(q, h=1e-3, n=160):
    lp = dom(build_Hs_q(1.0 + h, q, n))
    lm = dom(build_Hs_q(1.0 - h, q, n))
    l0 = dom(build_Hs_q(1.0, q, n))
    d = (lp - lm) / (2.0 * h)
    return l0, d, 2.0 / abs(d)


# ---------- (B) exact enumeration of restricted continuants ----------
def restricted_stats(q, N):
    """
    Enumerate every restricted-CF rational x = [0; a_1, ..., a_P] in (0,1]
    with all a_i in A_q = {gcd(m,q)=1} and continuant denominator Q_P <= N.

    Continued-fraction UNIQUENESS convention (standard): a finite CF is made
    canonical by requiring the last partial quotient a_P >= 2 (the only
    ambiguity is [..., a_P] = [..., a_P - 1, 1]).  With that convention the
    map  word -> reduced rational  is a BIJECTION, so NO dedup is needed and
    each admissible word contributes exactly one distinct rational of (0,1].

    We must therefore require the LAST digit a_P in A_q AND a_P >= 2 (when
    P >= 1; the single word of length 1, namely a_1 with a_1 in A_q,
    a_1 >= 2, gives 1/a_1; the empty/■ word is excluded).  Interior digits
    a_i in A_q with a_i >= 1.  (Note 1 in A_q always; it may appear only in
    interior positions under the canonical convention.)

    Continuant recursion (denominator only suffices for the size filtration):
        Q_{-1}=0, Q_0=1,  Q_i = a_i Q_{i-1} + Q_{i-2};  denominator = Q_P.
    Returns (count, sum_of_P).
    """
    adm = [m for m in range(1, N + 1) if gcd(m, q) == 1]   # ascending
    cnt = 0
    sumP = 0
    # DFS over words.  State: (Q_{i-1}, Q_i, depth_so_far).
    # At each node we may (a) CLOSE the word here by having the current last
    # digit be >=2 admissible -> counted when we *appended* a >=2 digit; or
    # (b) extend.  Cleanest: enumerate by appending digits; a word is counted
    # iff its last appended digit is >=2 (canonical) -- but interior digits
    # may be 1.  So: every time we append an admissible digit a, the word
    # ending there is canonical iff a >= 2; count it then.
    stack = [(0, 1, 0)]      # (Q_prev, Q_cur, depth)
    while stack:
        Qp, Qc, d = stack.pop()
        for a in adm:
            Qn = a * Qc + Qp
            if Qn > N:
                break        # adm ascending -> all larger a exceed N too
            # word of length d+1 ending in digit a:
            if a >= 2:       # canonical (last digit >= 2) -> a valid rational
                cnt += 1
                sumP += d + 1
            stack.append((Qc, Qn, d + 1))
    return cnt, sumP


def simulate_mu_q(q, Ns):
    logN, meanP = [], []
    rows = []
    for N in Ns:
        c, s = restricted_stats(q, N)
        if c == 0:
            continue
        logN.append(log(N)); meanP.append(s / c)
        rows.append((N, c, s / c))
    logN = np.array(logN); meanP = np.array(meanP)
    A = np.vstack([logN, np.ones_like(logN)]).T
    slope, intc = np.linalg.lstsq(A, meanP, rcond=None)[0]
    # also tail slope (last 4 points) -- asymptotic regime
    if len(logN) >= 4:
        At = np.vstack([logN[-4:], np.ones(4)]).T
        tslope = np.linalg.lstsq(At, meanP[-4:], rcond=None)[0][0]
    else:
        tslope = slope
    return slope, tslope, intc, rows


if __name__ == "__main__":
    print("=" * 72)
    print("DUAL confirmation  mu_q = 2/|lambda_q'(1)|  (restricted-digit CF)")
    print("=" * 72)
    # enumeration is exact over ALL restricted continuants <= N; the count
    # grows ~ N^2 so N up to ~3e4 is fine and fast.
    # q=1 (full Gauss) word count ~ 0.3 N^2 -> cap N for tractable runtime;
    # the slope is asymptotically stable and the tail slope is the estimator.
    Ns = [200, 400, 800, 1600, 3200, 6400]
    for q in [1, 2, 3, 4, 6]:
        print(f"\n--- q = {q}   alphabet A_q = {{m>=1 : gcd(m,{q})=1}} ---", flush=True)
        l0, d, mu_s = spectral_mu_q(q, n=140)
        print(f"  [A] lambda_q(1)={l0:.6f}  lambda_q'(1)={d:.6f}  "
              f"mu_q^spec=2/|.|={mu_s:.5f}", flush=True)
        slope, tslope, intc, rows = simulate_mu_q(q, Ns)
        for (N, c, mp) in rows:
            print(f"      N={N:6d}  #restricted-fracs={c:9d}  E[P_q]={mp:8.4f}")
        print(f"  [B] full-range slope={slope:.5f}  tail slope={tslope:.5f}  "
              f"(intercept {intc:.3f})")
        rel = abs(mu_s - tslope) / mu_s * 100.0
        print(f"  >>> mu_q  spectral={mu_s:.4f}  vs  simulation(tail)={tslope:.4f}"
              f"   rel diff {rel:.1f}%")
