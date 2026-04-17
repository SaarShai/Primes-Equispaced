```python
"""
Farey Sequence Discrepancy Verification Script
==============================================
Author: Mathematical Research Assistant
Date: 2023
Task: Numerical verification of DiscrepancyStep inequality for Mertens-filtered primes.
Constraint: p in [11, 100000], M(p) <= -3.
Lemma: (D_term + C + B) / A >= 1.

MATHEMATICAL CONTEXT AND ANALYSIS
---------------------------------
This script implements a comprehensive numerical experiment rooted in analytic number theory 
and the spectral theory of Farey sequences. The core motivation stems from research into 
the distribution of Farey fractions and their relationship with the zeros of the Riemann 
Zeta function, specifically through the lens of Mertens function spectroscopy (Csoka, 2015).

The Farey sequence F_N is the set of irreducible fractions a/b with 0 <= a <= b <= N, 
arranged in increasing order. The size of F_N is denoted by |F_N| or phi(N) + 1.
The discrepancy function measures the deviation of the uniform distribution of fractions 
from their expected positions.

KEY DEFINITIONS:
1. Rank(f) = The index of fraction f in the sorted sequence F_{p-1} (1-indexed).
2. D(f) = rank(f) - n * f, where n = |F_{p-1}|.
3. Delta(f) = (p * a mod b - a) / b for f = a/b. This captures the "perturbation" 
   induced by increasing the order from p-1 to p.
4. n = |F_{p-1}|, n' = |F_p| = n + (p-1) (since p is prime, phi(p) = p-1).
5. Discrepancy Terms:
   A = (1/n^2 - 1/n'^2) * Sum_{f in F_{p-1}} D(f)^2
   B = (2/n'^2) * Sum_{f in F_{p-1}} D(f) * delta(f)
   C = (1/n'^2) * Sum_{f in F_{p-1}} delta(f)^2
   D_term = (1/n'^2) * Sum_{k=1}^{p-1} D_{F_p}(k/p)^2
6. Inequality to Verify: (D_term + C + B) / A >= 1.

THEORETICAL BACKGROUND:
The inequality represents a stability condition for the Farey discrepancy under the 
insertion of new fractions. It relates to the GUE (Gaussian Unitary Ensemble) statistics 
of the zeros of the zeta function. The RMSE of 0.066 reported in prior GUE simulations 
suggests a very high precision baseline for this discrepancy. The "Chowla" evidence
