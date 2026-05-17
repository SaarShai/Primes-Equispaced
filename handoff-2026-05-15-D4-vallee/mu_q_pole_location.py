"""
D4 -- DIAGNOSIS of the dual-numeric DISAGREEMENT (q>=2).

Finding (mu_q_restricted_cf.py): for q=1 the dual estimates agree and match
the classical 12 ln2/pi^2.  For q>=2 the spectral  2/|lambda_q'(1)|  does
NOT match the simulation slope.  HYPOTHESIS: because lambda_q(1) < 1, the
dominant singularity of the size-Dirichlet series is NOT at s=1 but at the
s = s_q solving  lambda_q(s_q) = 1  (with s_q < 1 here, since lambda_q is
decreasing and lambda_q(1)<1 means the root is at s_q<1 ... check sign).

Vallee/BV05 mean-cost  mu = 2/|lambda'(1)|  is derived UNDER the normalization
lambda(1)=1 (full Gauss): the size-Dirichlet pole sits at s=1 exactly because
the dominant eigenvalue equals 1 there.  For a restricted system the pole
sits at s_q (the parameter where the spectral radius hits 1).  The Tauberian
leading constant is then governed by s_q and lambda_q'(s_q), giving the
candidate  mu_q^* = 1 / ( s_q * |lambda_q'(s_q)| / lambda_q(s_q) )  forms.
We test several closed forms against the SIMULATION slope (the ground truth,
since it directly counts restricted CF steps with exact arithmetic).

Recall: continuant denominators ~ size, and the Dirichlet variable carries
N^{-2s} (Vallee S(2s)); so the pole in the s-plane that matters solves
lambda_q(2*sigma)=1 in one convention or lambda_q(sigma)=1 in the |h'|^s one.
We just locate s_q with lambda_q(s_q)=1 and report 1/s_q and 2/s_q etc.,
and compare to the measured slopes.
"""
import numpy as np
from math import gcd
from mu_q_restricted_cf import build_Hs_q, dom

SIM_SLOPE = {1: 0.84257, 2: 0.67646, 3: 0.80445, 4: 0.67646, 6: 0.54651}


def lam(q, s, n=140):
    return dom(build_Hs_q(s, q, n))


def find_sq(q, lo=0.30, hi=1.60, n=140, tol=1e-5):
    """Solve lambda_q(s_q) = 1 by bisection (lambda decreasing in s)."""
    flo = lam(q, lo, n) - 1.0
    fhi = lam(q, hi, n) - 1.0
    if flo * fhi > 0:
        # widen
        lo, hi = 0.10, 3.0
        flo = lam(q, lo, n) - 1.0
        fhi = lam(q, hi, n) - 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        fm = lam(q, mid, n) - 1.0
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


if __name__ == "__main__":
    print("Diagnosis: pole location s_q (lambda_q(s_q)=1) vs simulation slope")
    print("=" * 70)
    h = 1e-3
    for q in [1, 2, 3, 4, 6]:
        sq = find_sq(q)
        lp = lam(q, sq + h)
        lm = lam(q, sq - h)
        dlam_sq = (lp - lm) / (2 * h)            # lambda_q'(s_q)
        l1 = lam(q, 1.0)
        lp1 = lam(q, 1.0 + h); lm1 = lam(q, 1.0 - h)
        dlam_1 = (lp1 - lm1) / (2 * h)           # lambda_q'(1)
        sim = SIM_SLOPE[q]
        # candidate closed forms for the mean-cost slope:
        c_BV_at1 = 2.0 / abs(dlam_1)                       # the (wrong) BV form
        c_pole_1 = 1.0 / (sq * abs(dlam_sq))              # 1/(s_q|lam'(s_q)|)
        c_pole_2 = 2.0 / (sq * abs(dlam_sq))              # 2/(s_q|lam'(s_q)|)
        c_invsq = 1.0 / sq
        c_2invsq = 2.0 / sq
        print(f"\nq={q}:  lambda_q(1)={l1:.5f}  s_q={sq:.5f}  "
              f"lambda_q'(s_q)={dlam_sq:.5f}  lambda_q'(1)={dlam_1:.5f}")
        print(f"   SIM slope (ground truth)            = {sim:.5f}")
        print(f"   2/|lambda_q'(1)|   (BV, mis-normed) = {c_BV_at1:.5f}   "
              f"[rel {abs(c_BV_at1-sim)/sim*100:5.1f}%]")
        print(f"   1/(s_q|lambda_q'(s_q)|)            = {c_pole_1:.5f}   "
              f"[rel {abs(c_pole_1-sim)/sim*100:5.1f}%]")
        print(f"   2/(s_q|lambda_q'(s_q)|)            = {c_pole_2:.5f}   "
              f"[rel {abs(c_pole_2-sim)/sim*100:5.1f}%]")
        print(f"   1/s_q                              = {c_invsq:.5f}   "
              f"[rel {abs(c_invsq-sim)/sim*100:5.1f}%]")
        print(f"   2/s_q                              = {c_2invsq:.5f}   "
              f"[rel {abs(c_2invsq-sim)/sim*100:5.1f}%]")
