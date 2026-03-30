# Effective (Explicit Constant) Bounds on the Mertens Function M(x)

## Survey compiled 2026-03-29

This document surveys all known EFFECTIVE (explicit constant) upper bounds on
|M(x)| = |sum_{n<=x} mu(n)|, focusing on unconditional results with fully explicit
constants and ranges of validity.

---

## 1. THE KEY QUESTION FOR OUR PROOF

We need: |M(x)| < c_0 * x / log(x) for all x >= P_0, with EXPLICIT c_0 and P_0.

**ANSWER: YES, this is known.** Multiple published results give this.

### Best available results of the form |M(x)| <= c * x / log(x):

| Source | Bound | Valid for | Notes |
|--------|-------|-----------|-------|
| El Marraki (1995) | \|M(x)\| <= 0.6437752 x / log(x) | ALL x > 1 | Optimal constant for universal validity (tight at x=5) |
| El Marraki (1995) | \|M(x)\| <= 0.002969 x / (log x)^{1/2} | x >= 142,194 | Stronger: decays as 1/sqrt(log x) |
| Ramare (2013) | \|M(x)\| <= 0.0130 x / log(x) - 0.118 x/(log x)^2 | x >= 1,078,853 | Much better constant than El Marraki |
| Ramare-Zuniga-Alterman (2024) | \|M(x)\| <= 0.006688 x / log(x) | x >= ~1,798,118 | Best current result, factor ~2 improvement over 2013 |

### CRITICAL FOR OUR PROOF:

If we need |M(x)|/x < c_0/log(x) with c_0 ~ 0.8, then:

- **El Marraki (1995) suffices immediately**: |M(x)| <= 0.6437752 x/log(x) for ALL x > 1.
  This gives c_0 = 0.6437752 < 0.8. Valid universally.

- **Even stronger**: Ramare (2013) gives c_0 = 0.0130 for x >= 1,078,853.

- **Strongest**: Ramare-Zuniga-Alterman (2024) gives c_0 = 0.006688 for x >= 1,798,118.

**Conclusion: Our proof closes unconditionally using El Marraki (1995) or any later result.**

---

## 2. BOUNDS OF THE FORM |M(x)| <= C * x (constant ratio)

| Source | Bound | Valid for |
|--------|-------|-----------|
| Dress & El Marraki (1993) | \|M(x)\| <= x/2360 | x >= 617,973 |
| Cohen, Dress & El Marraki (2007) | \|M(x)\| <= x/4345 | x >= 2,160,535 |

These are weaker (don't tend to 0) but provide simple finite verification ranges.

---

## 3. BOUNDS WITH EXPONENTIAL SAVINGS (Vinogradov-Korobov type)

### Lee & Leong (2022, updated 2024) — arXiv:2208.06141

**Theorem 1.1 (Classical zero-free region):**
For x >= x_0 >= exp(363.11):
  |M(x)| < c_1(x_0) * x * exp(-c_2(x_0) * sqrt(log x))

Sample values from their Table 1:
  - log(x_0) = 10^5: c_1 = 0.1154, c_2 = 0.3876
  - log(x_0) = 10^6: c_1 = 0.1035, c_2 = 0.4102

**Theorem 1.2 (Vinogradov-Korobov zero-free region):**
For x >= x_0:
  |M(x)| < c_3(x_0) * x * exp(-c_4(x_0) * (log x)^{3/5} * (log log x)^{-1/5})

Sample values:
  - log(x_0) = 10^5: c_3 = 5.6144, c_4 = 0.0031

**Corollary 1.3 (piecewise, valid for all x >= 1):**
For x > exp(exp(36.821)):
  |M(x)| <= 5.09591 * x * exp(-0.02196 * (log x)^{3/5} * (log log x)^{-1/5})

**This is the FIRST explicit Vinogradov-Korobov type bound for M(x).**

---

## 4. COMPUTATIONAL VERIFICATIONS

| Source | Range verified | Key finding |
|--------|---------------|-------------|
| Dress (1993) | x <= 10^{12} | \|M(x)\| <= 0.570591 sqrt(x) |
| Kotnik & te Riele (2006) | Zeros of zeta to high precision | Mertens conjecture false, counterexample < exp(1.59 * 10^{40}) |
| Hurst (2018) | ALL x <= 10^{16}, plus powers of 2 up to 2^{73} | Max \|M(x)/sqrt(x)\| < 0.585... in range |
| Kim & Nguyen (2025) | Lattice methods | Counterexample to Mertens conjecture < exp(1.96 * 10^{19}) |

### Implication for our proof:
Hurst verified M(x) for all x <= 10^{16}. In this range, |M(x)/sqrt(x)| < 0.586.
For x <= 10^{16}, this means |M(x)| < 0.586 * x^{1/2} << x/log(x).
So any bound we need is trivially satisfied computationally up to 10^{16}.

---

## 5. COMPLETE REFERENCE LIST

### Primary sources (explicit bounds on M(x)):

1. **El Marraki, M.** (1995). "Fonction sommatoire de la fonction de Mobius, 3.
   Majorations asymptotiques effectives fortes."
   *J. Theorie Nombres Bordeaux* 7(2), 407-433.
   KEY RESULT: |M(x)| <= 0.6437752 x/log(x) for all x > 1.

2. **Dress, F. & El Marraki, M.** (1993). "Fonction sommatoire de la fonction de
   Mobius. 2. Majorations asymptotiques elementaires."
   *Experimental Mathematics* 2(2), 99-112.
   KEY RESULT: |M(x)| <= x/2360 for x >= 617,973.

3. **Cohen, H., Dress, F. & El Marraki, M.** (2007). "Explicit estimates for
   summatory functions linked to the Mobius mu-function."
   *Funct. Approx. Comment. Math.* 37(1), 51-63.
   KEY RESULT: |M(x)| <= x/4345 for x >= 2,160,535.

4. **Ramare, O.** (2013). "From explicit estimates for primes to explicit estimates
   for the Mobius function."
   *Acta Arith.* 157(4), 365-379.
   KEY RESULT: |M(x)| <= 0.0130 x/log(x) for x >= 1,078,853.

5. **Ramare, O.** (2015). "Explicit estimates on several summatory functions
   involving the Moebius function."
   *Math. Comp.* 84(293), 1359-1387.
   Derives bounds on sum mu(d)/d with coprimality conditions from M(x) bounds.

6. **Ramare, O.** (2018). "On the Missing Log Factor."
   In: *Ergodic Theory and Dynamical Systems in their Interactions with
   Arithmetics and Combinatorics*, Springer, Lecture Notes in Mathematics 2213.

7. **Ramare, O. & Zuniga-Alterman** (2024). "From explicit estimates for the
   primes to explicit estimates for the Mobius function -- II."
   arXiv:2408.05969.
   KEY RESULT: |M(x)| <= 0.006688 x/log(x) for x >= 1,798,118.
   (Improves Ramare 2013 by factor ~2.)

8. **Lee, E. S. & Leong, N.** (2022, updated 2024). "New explicit bounds for
   Mertens function and the reciprocal of the Riemann zeta-function."
   arXiv:2208.06141.
   KEY RESULT: First explicit Vinogradov-Korobov type bound.
   |M(x)| <= 5.09591 x exp(-0.02196 (log x)^{3/5} (log log x)^{-1/5})
   for x > exp(exp(36.821)).

9. **Leong, N.** (2024). PhD Thesis, UNSW. Supervised by T. Trudgian.
   Comprehensive collection of explicit results linking zeta bounds to M(x).

### Zero-free regions (feeding into M(x) bounds):

10. **Mossinghoff, M. J., Trudgian, T. S. & Yang, A.** (2024). "Explicit
    zero-free regions for the Riemann zeta-function."
    *Research in Number Theory*.
    KEY: sigma >= 1 - 1/(5.558691 log|t|) for |t| >= 2 (classical).
    KEY: sigma >= 1 - 1/(55.241 (log|t|)^{2/3} (log log|t|)^{1/3}) for |t| >= 3 (VK type).

### Computational verifications:

11. **Hurst, G.** (2018). "Computations of the Mertens Function and Improved
    Bounds on the Mertens Conjecture."
    *Math. Comp.* 87(310), 1013-1028.
    Computed M(x) for all x <= 10^{16}.

12. **Kotnik, T. & te Riele, H.** (2006). "The Mertens Conjecture Revisited."
    *ANTS VII*, Springer LNCS 4076, 156-167.

### Coprimality-restricted sums:

13. **Ramare, O.** (2014). "Explicit estimates on the summatory functions of the
    Mobius function with coprimality restrictions."
    *Acta Arith.* 165(1), 1-10.
    KEY: |sum_{d<=x,(d,q)=1} mu(d)/d| <= 2.4 (q/phi(q)) / log(x/q) for x > q >= 1.

---

## 6. WHAT THIS MEANS FOR OUR PROOF

### The bound we need:
|M(x)| / x < c_0 / log(x) for all x >= P_0

### Available options (in order of strength):

**Option A (simplest, universally valid):**
Use El Marraki (1995): |M(x)| <= 0.6437752 x / log(x) for ALL x > 1.
- Gives c_0 = 0.6437752
- P_0 = 2 (or any x > 1)
- No finite verification needed

**Option B (better constant, requires finite check):**
Use Ramare (2013): |M(x)| <= 0.0130 x / log(x) for x >= 1,078,853.
- Gives c_0 = 0.0130
- P_0 = 1,078,853
- For x < P_0, verify computationally or use El Marraki

**Option C (best current, requires finite check):**
Use Ramare-Zuniga-Alterman (2024): |M(x)| <= 0.006688 x / log(x) for x >= 1,798,118.
- Gives c_0 = 0.006688
- P_0 = 1,798,118
- For x < P_0, use El Marraki or compute directly

**Option D (exponential savings, for asymptotic arguments):**
Use Lee-Leong (2024): |M(x)| <= 5.09591 x exp(-0.02196 (log x)^{3/5} (log log x)^{-1/5})
- This decays MUCH faster than x/log(x)
- Valid for x > exp(exp(36.821)) ~ 10^{10^{16}} (impractically large threshold)
- For practical ranges, use Options A-C

### RECOMMENDATION:
**Use Option A (El Marraki 1995) for the cleanest proof.**
It gives |M(x)| <= 0.644 x / log(x) for ALL x > 1, which is well within our
c_0 ~ 0.8 requirement. No finite verification needed. Single citation.

If the proof needs a SMALLER constant, use Option B or C and handle the
finite range separately (trivial given Hurst's computation to 10^{16}).

---

## 7. IMPORTANT CAVEATS

1. The bound |M(x)| = o(x) (equivalently, |M(x)| <= cx/log(x) for any c) is
   EQUIVALENT to the Prime Number Theorem. So these bounds, while effective,
   are consequences of deep results about zeta zeros.

2. The Walfisz (1963) bound |M(x)| <= x exp(-c sqrt(log x)) has INEFFECTIVE
   constant c (depends on Siegel's theorem). Do NOT use this for explicit work.

3. The EFFECTIVE bounds listed above avoid Siegel's theorem by using explicit
   zero-free regions and numerical verification of the Riemann Hypothesis
   up to large height.

4. All bounds in this document are UNCONDITIONAL (do not assume RH).

5. The Vinogradov-Korobov type bound (Lee-Leong) has a very large threshold
   x_0 ~ exp(exp(36.821)). For practical use, the x/log(x) bounds are better.
