#!/usr/bin/env python3
"""
Rigorous derivation of the factor-of-2 identity.

THEOREM: For prime p, N = p-1, n = |F_N|:
  sum_{k=1}^{p-1} E(k/p)^2 = 2*(p-1)/n * sum_{f in F_N} D(f)^2 + O(p)

where E(k/p) = N_{F_N}(k/p) - n*k/p and D(f) = rank(f) - n*f.

Equivalently: the ratio converges to 2 as p -> infinity.

PROOF STRATEGY:
We work with the exact identity:
  E(k/p) = (p-k)/p - S(k)/p
where S(k) = sum_{m=1}^N c_m * (mk mod p), c_m = M(floor(N/m)).

Then sum_k E(k/p)^2 = (1/p^2) * [P - 2Q + R] where
  P = sum (p-k)^2 = p(p-1)(2p-1)/6
  Q = sum (p-k) S(k) = p^2(p-1)/2 * sum_c - sum_m c_m T(m)
  R = sum S(k)^2 = sum_{r=1}^{p-1} T(r) C(r)

where T(r) = sum_j j*(rj mod p) and C(r) = sum_m c_m c_{mr mod p}.

KEY IDENTITIES:
  T(1) = p(p-1)(2p-1)/6
  sum_r T(r) = (p(p-1)/2)^2
  T_avg(r!=1) = p(p-1)(3p-1)/12

  C(1) = sum c_m^2 = sum M(N/m)^2
  sum_r C(r) = (sum c_m)^2
  sum_c = sum_{m=1}^N M(N/m) = sum_{m=1}^N mu(m) * floor(N/m) (a standard identity)

CONNECTION TO SUM_D^2:
The Franel-Landau theorem gives sum D(f)^2 in terms of the Mertens values c_m.
Specifically, from the exact representation:
  D(f_j) = j - n*f_j and N_{F_N}(x) = 1 + sum_m c_m floor(mx)

The sum of D^2 can be expressed as a quadratic form in c_m, but the explicit
connection to sum c_m^2 requires the Franel identity.

FRANEL'S IDENTITY (simplified):
  sum_{j=0}^{n-1} (f_j - j/n)^2 = (1/n^2) * [n + sum_{m=1}^N c_m^2 * phi_2(m) + cross_terms]

where phi_2(m) involves the second moment of the sawtooth function over Farey points.

Actually, the cleanest connection goes through the integral:

CLAIM 1: integral_0^1 E(x)^2 dx = sum_D^2/n + O(1)
CLAIM 2: sum_{k=1}^{p-1} E(k/p)^2 = 2(p-1) integral_0^1 E(x)^2 dx + O(p)

Claim 1 is a standard equidistribution result (Farey fractions are equidistributed).
Claim 2 is the content of the factor-of-2 identity.

For Claim 2, we use the SPECTRAL APPROACH:

E(x) = sum_h hat_E(h) e(hx) where hat_E(h) = integral E(x) e(-hx) dx.

sum_k E(k/p)^2 = sum_k |sum_h hat_E(h) e(hk/p)|^2
              = sum_{h,h'} hat_E(h) conj(hat_E(h')) * sum_k e((h-h')k/p)
              = (p-1) sum_{h equiv h' mod p} hat_E(h) conj(hat_E(h'))

The diagonal (h=h'): sum |hat_E(h)|^2 * (p-1) = (p-1) * integral E^2. Factor 1.
The off-diagonal (h != h', h equiv h' mod p): these are the "aliasing" terms.

sum_{k=1}^{p-1} e(mk/p) = p-1 if p|m, and -1 if p does not divide m.

So sum_k E(k/p)^2 = p * sum_{h equiv h' mod p} hat_E(h) conj(hat_E(h')) - integral E^2
(approximately, for h,h' ranging over all integers)

The aliasing terms are: for each h, sum over h' = h + jp (j != 0).
The contribution is: for each h, sum_{j!=0} hat_E(h) conj(hat_E(h+jp)).

This is the POISSON SUMMATION formula applied to E^2!

Let me verify numerically that the aliasing accounts for the second factor.
"""

import numpy as np
from fractions import Fraction
from math import gcd

def farey_sequence(N):
    fracs = set()
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

for p in [47, 89, 127]:
    if not is_prime(p): continue
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)

    # Compute E(x) on fine grid for Fourier analysis
    # E(x) is piecewise linear: on (f_j, f_{j+1}], E(x) = (j+1) - n*x
    n_grid = 10000
    x_grid = np.linspace(0, 1, n_grid, endpoint=False) + 0.5/n_grid
    E_grid = np.zeros(n_grid)

    f_vals = np.array([float(f) for f in F_N])
    for i, x in enumerate(x_grid):
        count = np.searchsorted(f_vals, x, side='right')
        E_grid[i] = count - n * x

    # Fourier coefficients of E(x) (approximation via FFT of the grid)
    E_hat = np.fft.fft(E_grid) / n_grid

    # Parseval check
    integral_E2 = np.mean(E_grid**2)
    parseval = np.sum(np.abs(E_hat)**2) * n_grid
    # Hmm, for continuous Fourier: integral |E|^2 = sum |hat_E(h)|^2
    # With our discretization: sum |E_hat(h)|^2 * n_grid = mean(|E|^2)
    # Actually np.fft gives: E_hat[h] = (1/n_grid) sum E(x_j) e(-2pi i h j/n_grid)
    # Parseval: sum |E(x_j)|^2 = n_grid * sum |E_hat[h]|^2

    print(f"\np={p}, N={N}, n={n}")
    print(f"  integral E^2 (grid approx) = {integral_E2:.6f}")
    print(f"  Parseval check: {np.sum(np.abs(E_hat)**2)*n_grid/n_grid:.6f}")

    # E(k/p) values
    E_vals = []
    for k in range(1, p):
        x = Fraction(k, p)
        count = sum(1 for f in F_N if f <= x)
        E_vals.append(float(count - n * x))
    E_arr = np.array(E_vals)
    sum_E2 = np.sum(E_arr**2)

    # Poisson summation: sum_k E(k/p)^2 = sum_{j=-inf}^{inf} integral E(x)^2 e(-2pi i j p x) dx
    # (by Poisson summation of the periodic function E(x)^2)
    # Wait, that's not quite right. Let me be careful.

    # sum_{k=1}^{p-1} f(k/p) = p * sum_{j} hat_f(jp) - f(0)
    # where hat_f(m) = integral_0^1 f(x) e(-2pi i m x) dx
    # This is the standard Poisson summation for sampling.

    # For f(x) = E(x)^2:
    # sum_{k=1}^{p-1} E(k/p)^2 = p * sum_j hat_g(jp) - E(0)^2
    # where g(x) = E(x)^2 and hat_g(m) = integral_0^1 E(x)^2 e(-2pi i m x) dx

    # hat_g(0) = integral E^2 (the average)
    # hat_g(jp) for j != 0: the Fourier coefficients of E^2 at multiples of p

    # j=0 term: p * integral E^2
    # j != 0 terms: p * sum_{j!=0} hat_g(jp)
    # minus: E(0)^2 = (1 - 0)^2 = 1

    # So sum E(k/p)^2 = p * integral E^2 + p * sum_{j!=0} hat_g(jp) - 1
    # The ratio: sum/(p * integral E^2) = 1 + sum_{j!=0} hat_g(jp) / integral E^2 - 1/(p*int)

    # If the aliasing sum equals integral E^2, we get factor 2!

    # Compute hat_g(m) = integral E(x)^2 e(-2pi i m x) dx numerically
    g_hat = np.fft.fft(E_grid**2) / n_grid

    # hat_g(0) should equal integral E^2
    print(f"  hat_g(0) = {g_hat[0].real:.6f} (should be {integral_E2:.6f})")

    # Aliasing sum: sum_{j!=0} hat_g(jp) (only finitely many in our grid)
    # With grid of n_grid points, frequencies are 0, 1, ..., n_grid-1
    # hat_g(jp) corresponds to index jp mod n_grid
    aliasing = 0
    for j in range(1, n_grid // p + 1):
        idx_pos = (j * p) % n_grid
        idx_neg = (n_grid - j * p) % n_grid
        aliasing += g_hat[idx_pos].real
        if idx_pos != idx_neg:
            aliasing += g_hat[idx_neg].real

    # Wait, I need to be more careful. For the standard Poisson:
    # sum_{k=0}^{p-1} f(k/p) = p * sum_{j=-inf}^{inf} hat_f(jp)
    # For our case with k=1,...,p-1 (excluding 0):
    # sum_{k=1}^{p-1} f(k/p) = p * sum_j hat_f(jp) - f(0)

    # In our DFT approximation, hat_f is periodic with period n_grid,
    # so we sum hat_g(jp mod n_grid) for j = 0, +-1, +-2, ...
    # until jp exceeds n_grid/2.

    aliasing_total = 0
    for j in range(-n_grid//(2*p), n_grid//(2*p) + 1):
        if j == 0: continue
        idx = (j * p) % n_grid
        aliasing_total += g_hat[idx].real

    print(f"  Aliasing sum: {aliasing_total:.6f}")
    print(f"  integral E^2: {integral_E2:.6f}")
    print(f"  aliasing / integral: {aliasing_total / integral_E2:.6f}")
    print(f"  p*(integral + aliasing) - E(0)^2 = {p*(integral_E2 + aliasing_total) - 1:.4f}")
    print(f"  Actual sum E^2 = {sum_E2:.4f}")

    # The Poisson prediction
    poisson_pred = p * (integral_E2 + aliasing_total) - 1
    print(f"  Poisson prediction error: {abs(poisson_pred - sum_E2) / sum_E2:.6f}")

    # KEY: What is the aliasing sum physically?
    # hat_g(m) = integral E(x)^2 e(-2pi i m x) dx
    # E(x) has jumps at Farey fractions, so E(x)^2 also has jumps.
    # The Fourier coefficients hat_g(m) for |m| > 0 are O(1/m) due to the jumps.
    # But there are specific RESONANCES at m related to the Farey structure.

    # For the aliasing, we sum hat_g(jp) for j != 0.
    # The dominant term is j = +-1, i.e., hat_g(p) and hat_g(-p).
    # Since g = E^2 is real: hat_g(-p) = conj(hat_g(p)), so the contribution is 2*Re(hat_g(p)).

    print(f"\n  Dominant aliasing terms:")
    for j in range(1, 6):
        idx = (j * p) % n_grid
        neg_idx = (-j * p) % n_grid
        contrib = g_hat[idx].real + g_hat[neg_idx].real
        print(f"    j=+-{j}: hat_g(+-{j}p) contribution = {contrib:.6f}")

    # Alternatively, we can use the CONVOLUTION interpretation:
    # hat_g(m) = sum_h hat_E(h) * conj(hat_E(h-m))
    # (Fourier transform of a product is convolution)
    # hat_g(p) = sum_h hat_E(h) * conj(hat_E(h-p))
    # This is the correlation of E's spectrum with itself, shifted by p.
    #
    # For the aliasing sum: sum_{j!=0} hat_g(jp) = sum_{j!=0} sum_h hat_E(h) conj(hat_E(h-jp))
    # = sum_h |hat_E(h)|^2 * [sum_{j!=0} ... ] -- this is a double sum, not factored.

    # THE SPECTRAL EXPLANATION FOR FACTOR 2:
    # E(x) has significant spectral content at frequencies h ~ n ~ 3p^2/pi^2 >> p.
    # The Fourier coefficients hat_E(h) are approximately:
    # hat_E(h) ~ -(1/(2pi i h)) * sum_{m|h, m<=N} mu(m) * something
    # The ALIASED frequencies h and h+p are BOTH in the "active" range 1..N.
    # So hat_E(h) and hat_E(h+p) are of COMPARABLE magnitude for h ~ N >> p.
    # The aliasing sum is therefore comparable to the direct sum.

    print(f"\n  Spectral energy distribution:")
    E_hat_full = np.fft.fft(E_grid) / n_grid
    power = np.abs(E_hat_full)**2
    total_power = np.sum(power)

    # Energy in bands
    band_size = p
    n_bands = n_grid // (2 * band_size)
    for b in range(min(5, n_bands)):
        lo = b * band_size
        hi = (b+1) * band_size
        band_power = np.sum(power[lo:hi]) + (np.sum(power[n_grid-hi:n_grid-lo]) if lo > 0 else 0)
        print(f"    Band {lo}-{hi}: fraction = {band_power/total_power:.4f}")

print("\n\n=== THEORETICAL DERIVATION ===\n")
print("""
The factor of 2 in the sampling ratio arises from ALIASING in the Poisson summation.

PRECISE STATEMENT:
sum_{k=1}^{p-1} E(k/p)^2 = p * integral_0^1 E(x)^2 dx + p * A(p) - E(0)^2

where A(p) = sum_{j != 0} hat_g(jp) is the aliasing sum.

CLAIM: A(p) ~ integral_0^1 E(x)^2 dx as p -> infinity, giving the factor of 2.

PROOF SKETCH:
1. E(x) has its spectral energy concentrated at frequencies 1 <= h <= N = p-1.
   This is because E(x) = -sum_{m=1}^N c_m {mx} + O(1), and {mx} has
   Fourier coefficients concentrated at h ~ m (multiples of m).

2. For the squared function g(x) = E(x)^2:
   hat_g(m) = sum_h hat_E(h) * conj(hat_E(h-m))  (convolution)

3. hat_g(0) = sum_h |hat_E(h)|^2 = integral E^2.

4. For hat_g(p): the sum runs over h with hat_E(h) and hat_E(h-p) both nonzero.
   Since E's spectrum is supported on [1, N] (roughly), we need both
   1 <= h <= N and 1 <= h-p <= N, i.e., p+1 <= h <= N.
   For N = p-1: there are NO such h! So hat_g(p) ~ 0.

   But wait, E's spectrum extends beyond N due to the higher harmonics of {mx}.
   {mx} = -sum_{l=1}^{infty} sin(2*pi*l*m*x)/(pi*l) has energy at all multiples
   of m. The significant energy is at l*m <= cN for some constant c.

REVISED ANALYSIS:
The Fourier coefficients of E(x) = -sum_m c_m {mx} + const + linear are:
hat_E(h) = sum_{m|h, m<=N} c_m / (2*pi*i*h/m) = (1/(2*pi*i*h)) sum_{m|h,m<=N} m*c_m

Wait, let me be more careful. {mx} has Fourier expansion:
{mx} = 1/2 - sum_{l=1}^{infty} sin(2*pi*l*m*x) / (pi*l)
      = 1/2 + sum_{l != 0} 1/(2*pi*i*l) * e(lmx)

So hat_{{mx}}(h) = { 1/(2*pi*i*l) if h = lm for some integer l != 0
                    { 1/2           if h = 0
                    { 0             otherwise

Therefore hat_E(h) = -(1/(2*pi*i)) * sum_{m|h, 1<=m<=N} c_m * m/h

And hat_g(p) = sum_h hat_E(h) * conj(hat_E(h-p))
The dominant contributions come from h where both hat_E(h) and hat_E(h-p) are large.

For h = m*l and h-p = m'*l' with m,m' <= N:
We need ml - m'l' = p, i.e., the difference of two "smooth numbers" equals p.

The dominant terms are l=1, l'=1: m - m' = p. Since m <= N = p-1, no solution.
l=2, l'=1: 2m - m' = p. Solutions: m' = 2m - p for m >= (p+1)/2.
l=1, l'=2: m - 2m' = p. No solution since m-2m' <= N - 2 < p.

Hmm, the l=2 terms ARE significant. Let me verify.
""")

# Verify the Fourier coefficient structure
for p in [89]:
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)

    from math import floor as fl
    def mertens_values_inner(N):
        mu = [0] * (N + 1)
        mu[1] = 1
        for i in range(1, N + 1):
            for j in range(2*i, N + 1, i):
                mu[j] -= mu[i]
        M = [0] * (N + 1)
        for k in range(1, N + 1):
            M[k] = M[k-1] + mu[k]
        return M, mu

    M, mu = mertens_values_inner(N)
    c = [0]*(N+1)
    for m in range(1,N+1): c[m] = M[N//m]

    # Theoretical hat_E(h) for h != 0:
    # hat_E(h) = -(1/(2*pi*i*h)) * sum_{m|h, 1<=m<=N} c_m * m
    # Wait, let me redo. E(x) = 1 - x + sum_m c_m * (mx - 1/2 - {mx} + 1/2)
    # Hmm this is getting tangled. Let me just check the convolution sum.

    # Compute hat_g(p) from the fine-grid FFT
    n_grid = 20000
    x_grid = np.linspace(0, 1, n_grid, endpoint=False) + 0.5/n_grid
    f_vals = np.array([float(f) for f in F_N])
    E_grid = np.zeros(n_grid)
    for i, x in enumerate(x_grid):
        count = np.searchsorted(f_vals, x, side='right')
        E_grid[i] = count - n * x

    E_hat = np.fft.fft(E_grid) / n_grid
    g_hat = np.fft.fft(E_grid**2) / n_grid

    print(f"\np={p}:")
    # Check convolution formula: hat_g(m) = n_grid * sum_h E_hat(h) * conj(E_hat(h-m))
    for m_test in [0, p, 2*p]:
        conv = 0
        for h in range(n_grid):
            conv += E_hat[h] * np.conj(E_hat[(h - m_test) % n_grid])
        conv *= n_grid
        print(f"  hat_g({m_test}): direct={g_hat[m_test%n_grid]:.6f}, convolution={conv:.6f}")

    # Now: what are the leading contributions to hat_g(p)?
    # From the convolution: sum_h hat_E(h) * conj(hat_E(h-p))
    # The terms where both |hat_E(h)| and |hat_E(h-p)| are large

    power = np.abs(E_hat)**2
    # Top frequencies
    top_h = np.argsort(power)[::-1][:20]
    print(f"\n  Top 20 frequencies by |hat_E(h)|^2:")
    for h in top_h:
        h_eff = h if h < n_grid//2 else h - n_grid
        print(f"    h={h_eff:>6}: |hat_E|^2 = {power[h]:.6f}")

    # The correlation at shift p
    print(f"\n  Correlation at shift p={p}:")
    products = []
    for h in range(n_grid):
        h2 = (h - p) % n_grid
        prod = (E_hat[h] * np.conj(E_hat[h2])).real * n_grid
        if abs(prod) > 0.01:
            h_eff = h if h < n_grid//2 else h - n_grid
            h2_eff = h2 if h2 < n_grid//2 else h2 - n_grid
            products.append((h_eff, h2_eff, prod))

    products.sort(key=lambda x: abs(x[2]), reverse=True)
    print(f"  Top contributions to hat_g(p):")
    for h, h2, prod in products[:15]:
        print(f"    h={h:>6}, h-p={h2:>6}: contribution={prod:.6f}")
