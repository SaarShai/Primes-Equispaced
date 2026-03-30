# Algebraic Derivation: B'/C' = alpha + rho

## Date: 2026-03-30
## Status: Complete algebraic derivation from first principles
## Dependencies: Permutation identity (PERMUTATION_IDENTITY.md)

---

## 0. Definitions

Fix a prime p >= 5 and set N = p - 1. Let F = {f_1, ..., f_n} be the Farey fractions in F_N with denominator b > 1, listed in increasing order. For each f = a/b in F:

- **Rank discrepancy:** D(f_j) = j - n f_j
- **Shift residual:** delta(f) = (a - pa mod b) / b, where f = a/b
- **B' = 2 Sigma D(f) delta(f)**, summed over f in F
- **C' = Sigma delta(f)^2**, summed over f in F

Statistics over the n fractions in F:

- **f-bar = (1/n) Sigma f = 1/2** (by the Farey symmetry f <-> 1-f)
- **D-bar = (1/n) Sigma D(f) = -1/2** (since Sigma D = Sigma j - n Sigma f = n(n+1)/2 - n^2/2 = n/2 - n^2 f-bar... see derivation in Section 1)
- **alpha = Cov(D, f) / Var(f)**, the slope of the linear regression of D on f
- **D_err(f) = D(f) - D-bar - alpha (f - 1/2)**, the residual after removing the linear trend
- **rho = 2 Sigma D_err(f) delta(f) / C'**

**Goal:** Derive B'/C' = alpha + rho purely algebraically.

---

## 1. Preliminary: Compute D-bar

By definition, D(f_j) = j - n f_j, so:

    Sigma_{j=1}^{n} D(f_j) = Sigma j - n Sigma f_j = n(n+1)/2 - n Sigma f_j

Now Sigma f_j = n f-bar = n/2 (by Farey symmetry). Therefore:

    Sigma D = n(n+1)/2 - n(n/2) = n(n+1)/2 - n^2/2 = n/2

Hence:

    D-bar = (1/n) Sigma D = 1/2

**Wait -- let me recheck this.** The sum Sigma j from j=1 to n is n(n+1)/2. And Sigma f = n/2. So:

    Sigma D = n(n+1)/2 - n * (n/2) = n(n+1)/2 - n^2/2 = n/2

So D-bar = (Sigma D)/n = 1/2.

**Note:** The problem statement says D-bar = -1/2. Let me check: the Farey fractions with b > 1 do NOT include 0/1 and 1/1. The symmetry f <-> 1-f still holds for interior fractions (if a/b is in F_N with 1 < b, then (b-a)/b is also in F_N with the same denominator). So f-bar = 1/2 is correct.

But we need to be careful: the index j runs from 1 to n where the fractions are ordered. If f-bar = 1/2, then Sigma D = n/2, and D-bar = 1/2. However, if we were summing over ALL Farey fractions including 0/1 and 1/1, let n_full = n + 2 fractions, Sigma f_full = n/2 + 0 + 1 = n/2 + 1, and D_full-bar = (n_full + 1)/2 - n_full * (n/2 + 1)/n_full... this gets complicated.

**For this derivation, we work exclusively with the n interior fractions (b > 1) as stated, and we have D-bar = 1/2.**

*Correction to problem statement:* The sign of D-bar depends on the convention. With D(f_j) = j - n f_j and interior fractions only, D-bar = 1/2. If D-bar were defined as D(f_j) = j - (n+1) f_j or similar, the sign could differ. We proceed with D-bar = 1/2; the derivation works for any constant value of D-bar, as this term will vanish anyway (see Step 2).

---

## 2. Key Lemma: Sigma delta(f) = 0 (per-denominator vanishing)

**Lemma.** For each fixed denominator b in {2, ..., N} with gcd(p, b) = 1:

    Sigma_{a: gcd(a,b)=1, 1<=a<b} delta(a/b) = 0

**Proof.** Since gcd(p, b) = 1, the map a -> (pa mod b) is a permutation of the coprime residues {a : gcd(a,b) = 1, 1 <= a < b}. Therefore:

    Sigma_{a} delta(a/b) = Sigma_{a} (a - pa mod b) / b
                         = (1/b) [Sigma a - Sigma (pa mod b)]
                         = (1/b) [Sigma a - Sigma a]     (by permutation)
                         = 0.    QED

**Corollary.** Summing over all denominators:

    Sigma_{f in F} delta(f) = Sigma_{b=2}^{N} Sigma_{a: gcd(a,b)=1} delta(a/b) = 0

Note: For p prime and N = p-1, every b in {2, ..., N} satisfies gcd(p, b) = 1 since b < p. So the permutation property applies to every denominator class, and the global sum vanishes.

---

## 3. Key Lemma: The Permutation Square-Sum Identity

**Lemma (PERMUTATION_IDENTITY.md).** For prime p and N = p-1:

    Sigma_{f in F} f * delta(f) = (1/2) C'

where C' = Sigma delta(f)^2.

**Proof.** Write delta(f) = f - {pf} where {pf} = (pa mod b)/b for f = a/b. Then:

    f * delta = f^2 - f * {pf}
    delta^2 = f^2 - 2f * {pf} + {pf}^2

Compute f * delta - delta^2 / 2:

    f * delta - delta^2/2 = (f^2 - f{pf}) - (f^2 - 2f{pf} + {pf}^2)/2
                          = f^2 - f{pf} - f^2/2 + f{pf} - {pf}^2/2
                          = f^2/2 - {pf}^2/2
                          = (f^2 - {pf}^2) / 2

For fixed b, summing over coprime a: since a -> pa mod b is a permutation,

    Sigma_a (a/b)^2 = Sigma_a (pa mod b / b)^2

so Sigma_a (f^2 - {pf}^2) = 0 for each b. Summing over all b:

    Sigma_f [f * delta - delta^2/2] = 0

Therefore: **Sigma f * delta = C'/2**.    QED

---

## 4. Corollary: Sigma (f - 1/2) * delta(f) = C'/2

From the two lemmas:

    Sigma (f - 1/2) * delta = Sigma f * delta - (1/2) * Sigma delta
                             = C'/2 - (1/2) * 0
                             = C'/2

This is the crucial bridge identity.

---

## 5. The Decomposition of D(f)

Define the linear regression decomposition:

    D(f) = D-bar + alpha * (f - f-bar) + D_err(f)
         = D-bar + alpha * (f - 1/2) + D_err(f)

where:
- alpha = Cov(D, f) / Var(f) is the OLS slope
- D_err(f) is the residual, satisfying by construction:
  - Sigma D_err(f) = 0 (residuals sum to zero)
  - Sigma D_err(f) * (f - 1/2) = 0 (residuals are orthogonal to the regressor)

This is just the standard OLS decomposition. The three components (constant, linear, residual) are mutually orthogonal in the sense that Sigma D_err = 0 and Sigma D_err * f = 0.

---

## 6. Main Derivation: Substituting into B'

Start with:

    B' = 2 Sigma D(f) * delta(f)

Substitute the decomposition D(f) = D-bar + alpha(f - 1/2) + D_err(f):

    B' = 2 Sigma [D-bar + alpha(f - 1/2) + D_err(f)] * delta(f)

Distribute the sum:

    B' = 2 D-bar * Sigma delta(f)
       + 2 alpha * Sigma (f - 1/2) * delta(f)
       + 2 Sigma D_err(f) * delta(f)

Now evaluate each term:

### Term 1: 2 D-bar * Sigma delta

By Lemma (Section 2): Sigma delta(f) = 0.

Therefore: **Term 1 = 0.**

(This holds regardless of the value of D-bar.)

### Term 2: 2 alpha * Sigma (f - 1/2) * delta

By the Corollary (Section 4): Sigma (f - 1/2) * delta = C'/2.

Therefore: **Term 2 = 2 alpha * C'/2 = alpha * C'.**

### Term 3: 2 Sigma D_err * delta

This is, by definition: **Term 3 = rho * C'**

since rho = 2 Sigma D_err(f) delta(f) / C'.

### Combining:

    B' = 0 + alpha * C' + rho * C' = (alpha + rho) * C'

Dividing both sides by C' (which is strictly positive since not all delta(f) are zero for p >= 5):

    **B'/C' = alpha + rho**    QED

---

## 7. Summary of What Was Used

The derivation requires exactly three ingredients:

1. **Sigma delta = 0** (Section 2): follows from the permutation property of multiplication mod b when gcd(p, b) = 1. Holds for all b < p when p is prime.

2. **Sigma f * delta = C'/2** (Section 3): the permutation square-sum identity. Also follows from the permutation property, via the algebraic identity f*delta - delta^2/2 = (f^2 - {pf}^2)/2.

3. **Standard OLS decomposition** (Section 5): D = constant + linear + residual, with residuals orthogonal to the constant and linear terms.

The identity B'/C' = alpha + rho is then a direct algebraic consequence. No approximations, no asymptotics, no number-theoretic estimates are needed. It holds exactly for every prime p >= 5.

---

## 8. Boundary Terms from b = 1 Exclusion

The exclusion of b = 1 fractions (0/1 and 1/1) does NOT affect the derivation:

- For b = 1, the only fractions are 0/1 and 1/1. Their delta values are delta(0/1) = (0 - 0)/1 = 0 and delta(1/1) = (1 - p mod 1)/1 = (1 - 0)/1 = 1. But 0/1 has delta = 0 and 1/1 has delta = 1.
- However, we defined F to exclude b = 1 from the start, so all sums are over b >= 2 only.
- The permutation property Sigma delta = 0 holds per-b for each b >= 2 (since gcd(p, b) = 1 for all b < p). There is no "boundary correction" from excluding b = 1.
- The square-sum identity Sigma f delta = C'/2 was also proved per-b and holds for the same range b >= 2.
- The OLS decomposition is defined intrinsically over the set F.

**Conclusion:** There are no boundary terms. The identity holds cleanly over the interior fractions.

---

## 9. Interpretation

The identity B'/C' = alpha + rho decomposes the normalized cross-correlation B'/C' into:

- **alpha = Cov(D, f) / Var(f)**: the "linear" part, measuring how much of D's variation is explained by the linear trend in f. This grows like log(N) and dominates for large p.

- **rho = 2 Sigma D_err delta / C'**: the "nonlinear" part, measuring the residual correlation between the non-linear fluctuations of D and the shift residual delta. This is bounded and oscillatory.

The Correction Negativity Theorem (Term2 < 0) is equivalent to alpha + rho > 1, which for M(p) <= -3 primes follows from alpha growing to infinity while |rho| remains bounded.
