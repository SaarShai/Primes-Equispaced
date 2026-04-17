# NDC Elliptic Curve Universality: 37a1
**Date:** 2026-04-16  
**Curve:** y² + y = x³ − x, conductor 37, rank 1  
**Zero tested:** ρ_E = 0.5 + 5.003838972i (first nontrivial zero of L(E,s))  
**Precision:** mpmath dps=50  
**Script:** `ndc_ec_universality_final.py`

---

## a_p table (first 20 primes)

Point counting via Legendre symbol: for each x ∈ F_p, discriminant = 1+4(x³−x) is tested as QR.  
Brute-force verified correct for p ≤ 7.

```
     p    a_p    #E(F_p)
     2     -2          5
     3     -3          7
     5     -2          8
     7     -1          9
    11     -5         17
    13     -2         16
    17      0         18
    19      0         20
    23      2         22
    29      6         24
    31     -4         36
    37      0         38   (bad reduction, a_37=0)
    41     -9         51
    43      2         42
    47     -9         57
    53      1         53
    59      8         52
    61     -8         70
    67      8         60
    71      9         63
```

**NOTE:** Reference values sometimes cited (a_7=−2, a_11=0, a_13=6) are WRONG.  
Correct values from brute-force: a_7=−1, a_11=−5, a_13=−2.

---

## D_K^E computation table

ρ_E = 0.5 + 5.003838972i  
ζ(2) = π²/6 = 1.644934066848226  
L'(E,1) = 0.3059997738340523 → 1/L'(E,1) = 3.267976  

```
     K        |c_K^E|        |E_K^E|        |D_K^E|     |D_K^E·ζ(2)|  arg(D_K^E)  c_K.re/log(K)
--------------------------------------------------------------------------------------------------
    10       1.526428   8.715e-01   1.330e+00   2.188e+00    -2.170995     -0.526644
    20       1.879873   1.230e+00   2.312e+00   3.804e+00    -1.191424      0.627487
    50       5.749650   1.966e-02   1.131e-01   1.860e-01    -1.363925      0.765641
   100       4.080952   1.070e-03   4.366e-03   7.182e-03     0.234382     -0.552807
   200       7.038357   3.171e-03   2.232e-02   3.671e-02     2.578517      0.074226
   500       7.846968   5.506e+01   4.320e+02   7.107e+02    -1.221300     -0.905359
  1000      22.462117   2.434e-07   5.468e-06   8.995e-06     0.457330      3.183227
```

**Reference:** 1/L'(E,1) = 3.267976

---

## Cesaro mean table

Running mean of |D_K^E · ζ(2)| for K=1..200:

```
     K       |D_K·ζ(2)|    Cesaro mean
    50         0.185974        1.715844
   100         0.007182        0.897537
   150         0.000117        0.598933
   200         0.036710        0.450738
```

---

## c_K^E/log(K) vs 1/L'(E,1)

```
  K=1000: c_K.re/log(K) = 3.1832
  Target 1/L'(E,1)      = 3.2680
  Ratio:                  0.974  (within 2.6% at K=1000 — surprisingly close)
```

However, the ratio is noisy (ranges from −0.91 at K=500 to 3.18 at K=1000).  
The K=1000 value agreeing with 1/L'(E,1) at the 2.6% level may be coincidental.

---

## L'(E,1) verification

```
  L(1,E) via Euler product (p≤1000):    0.02188917  (should be 0 for rank-1 curve)
  L'(E,1) finite difference (p≤1000):   0.20893261
  Known L'(E,1):                         0.30599977383
  Ratio computed/known:                  0.683
```

The Euler product at K=1000 only recovers 68% of L'(E,1). Needs K~10^6 for full convergence.  
Note: 37a1 has rank 1, so L(E,1)=0 exactly; L'(E,1)≈0.306 is the leading term in BSD.

---

## Richardson extrapolation

Model D_K = D_∞ + C/log(K), solve from K=500 and K=1000:

```
  |D_500|          = 4.320e+02
  |D_1000|         = 5.468e-06
  D_inf (estimate) = −1326.4 + 3639.4i
  |D_inf · ζ(2)|   = 6.372e+03
```

**Richardson extrapolation is UNRELIABLE here** due to non-monotone behavior.  
D_K jumps 8 orders of magnitude from K=500 to K=1000, violating the model assumption.

---

## Diagnostic: Euler factor near-zeros

Primes where |1 − a_p·p^{−ρ} + p^{1−2ρ}| < 0.1 at ρ_E:

```
  p=  17: |factor|=7.95e-02   (causes |E_K| jump × 12.6)
  p= 179: |factor|=1.30e-02   (causes |E_K| jump × 76.6)
  p= 271: |factor|=5.85e-02   (causes |E_K| jump × 17.1)
  p= 337: |factor|=3.95e-02   (causes |E_K| jump × 25.3)
  p= 359: |factor|=1.92e-03   (causes |E_K| jump × 521 — DOMINANT)
  p= 461: |factor|=9.92e-02   (causes |E_K| jump × 10.1)
  p= 683: |factor|=4.22e-02   (causes |E_K| jump × 23.7)
  p= 919: |factor|=8.29e-02   (causes |E_K| jump × 12.1)
```

The near-zero at p=359 (|factor|=0.00192) drives the wild oscillation.  
These are accidental near-zeros of the local L-factor at the specific ρ_E — not related to zeros of L(E,s).

---

## Conclusion: does D_K^E · ζ(2) → 1?

**Current data: INCONCLUSIVE.**

| Metric | Value | Judgment |
|--------|-------|----------|
| Range of |D_K·ζ(2)| for K≤1000 | [9e-6, 711] | Wild oscillation |
| Cesaro mean at K=200 | 0.45 | Trending toward 0, not 1 |
| Richardson estimate | 6372 | Unreliable (non-monotone) |
| c_K.re/log(K) at K=1000 | 3.18 | Within 2.6% of target 3.27 |

**Key physics:**
- The Dirichlet series c_K(ρ) = Σ μ(k)a_k k^{−ρ} is conditionally convergent on Re(ρ)=1/2 for GL(2). It converges far more slowly than the GL(1) (Riemann zeta) case because |a_k| = O(k^{1/2+ε}) vs O(k^ε) for the Möbius function.
- The Euler product E_K(ρ_E) is a finite product with near-zero factors that dominate individual steps. The product itself oscillates 7 orders of magnitude across K=100..1000.
- NDC universality across GL(2) requires K >> exp(π·Im(ρ)) ≈ exp(15.7) ≈ 6×10^6 for this zero. We are at K=1000.

**Recommendation for follow-up:**
1. Extend to K=10^4..10^6 using M1 Max (queue task for qwen3.5:35b to analyze precomputed tables).
2. Use the **Approximate Functional Equation** instead of raw Dirichlet series — avoids conditional convergence issues and requires only K~100 for Im(ρ)=5.
3. Cross-check: compute D_K^ζ(ρ_zeta) at a zeta zero (GL(1) case) to verify the machinery works before claiming GL(2) behavior.

---

*Computation: Python/mpmath (dps=50), a_p by Legendre symbol point counting, a_k by multiplicative extension, c_K by Möbius sum, E_K by Euler product. Runtime ~10 min on M5 Max.*
