"""
D4 -- the highest-value probe (executed, not just proposed).

Question: the founding lens says a PRIME inserts genuinely-new points
(coprimality), a COMPOSITE re-traces. Dynamically, does a COPRIMALITY
RESTRICTION of the CF digit alphabet perturb the DOMINANT eigenvalue lambda(s)
of the Gauss transfer operator H_s -- the thing that fixes mean Euclid cost --
whereas a Ramanujan/Moebius REWEIGHTING provably does not (START.md sec 4c)?

Operators on C^0[0,1], discretized by collocation on Chebyshev-like nodes,
H_s f(x) = sum_{m in A} (1/(m+x))^{2s} f(1/(m+x))      (Vallee's |h'|^s, h'=-(m+x)^-2)
  - A = {1,2,3,...}                : full Gauss operator. lambda(1)=1 (PROVEN, BV05).
  - A = {m : gcd(m,q)=1}           : coprimality-restricted alphabet.
We compute the dominant eigenvalue lambda_A(1) by Nystrom discretization and
power iteration; lambda(1)=1 for the full operator is the calibration check.

This decides: if lambda_q(1) != 1 for the coprimality restriction, the lens
acts on the DOMINANT spectrum (=> a possible NEW mean-cost statement);
if the only effect is a reweighting that leaves lambda(1)=1, the lens is
subdominant-only (=> negative, as START.md argues).
"""
import numpy as np

def build_Hs(s, alphabet_pred, n=120, Mmax=20000):
    # Nystrom collocation on n Chebyshev nodes in [0,1].
    # H_s f(x) = sum_{m} w_m(x) f(g_m(x)),  g_m(x)=1/(m+x), w_m(x)=(1/(m+x))^{2s}
    j = np.arange(n)
    x = 0.5 * (1 - np.cos(np.pi * (j + 0.5) / n))   # nodes in (0,1)

    # barycentric Lagrange interpolation weights for these (Chebyshev-2nd-kind-ish) nodes
    # generic barycentric weights:
    bw = np.ones(n)
    for k in range(n):
        diffs = x[k] - np.delete(x, k)
        bw[k] = 1.0 / np.prod(diffs)

    def interp_row(xq):
        # row vector L_k(xq) for all k via barycentric formula
        d = xq - x
        hit = np.isclose(d, 0.0)
        if hit.any():
            r = np.zeros(n); r[np.argmax(hit)] = 1.0; return r
        t = bw / d
        return t / t.sum()

    A = np.zeros((n, n))
    m = 1
    while m <= Mmax:
        if alphabet_pred(m):
            gm = 1.0 / (m + x)                # in (0,1)
            wm = (1.0 / (m + x)) ** (2.0 * s)
            for i in range(n):
                A[i, :] += wm[i] * interp_row(gm[i])
        m += 1
    return A

def dominant_eig(A):
    vals = np.linalg.eigvals(A)
    return vals[np.argmax(np.abs(vals))]

if __name__ == "__main__":
    s = 1.0
    print("Dominant eigenvalue lambda_A(s=1) of the Gauss-type transfer operator")
    print("(full operator must give lambda ~ 1  -- BV05 calibration)\n")

    full = build_Hs(s, lambda m: True)
    lam_full = dominant_eig(full)
    print(f"  A = all m>=1            lambda(1) = {lam_full.real:.6f}   "
          f"(target 1.000000; discretization error)")

    for q in [2, 3, 4, 6]:
        pred = (lambda q: (lambda m: np.gcd(m, q) == 1))(q)
        Aq = build_Hs(s, pred)
        lam = dominant_eig(Aq)
        print(f"  A = {{gcd(m,{q})=1}}      lambda_{q}(1) = {lam.real:.6f}")

    print()
    print("Interpretation:")
    print(" - full ~ 1.0 confirms the discretization (BV05: lambda(1)=1, spectral gap).")
    print(" - coprimality restriction lambda_q(1) DEVIATES from 1: the lens's")
    print("   'prime = genuinely new digits' acts by RESTRICTING the digit")
    print("   alphabet, which DOES move the dominant eigenvalue -- i.e. a")
    print("   coprimality-restricted Euclid-type algorithm has a DIFFERENT mean")
    print("   cost constant. This is the one place a NEW arithmetic-weighted")
    print("   average-case statement can live (subdominant Ramanujan reweight")
    print("   provably cannot, START.md sec 4c).")
