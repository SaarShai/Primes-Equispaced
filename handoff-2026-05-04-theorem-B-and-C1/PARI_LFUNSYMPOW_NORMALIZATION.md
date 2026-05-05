# PARI/GP lfunsympow Normalization & Convention

**Source:** Pascal Molin, "L functions computations using Pari/GP" (Université Paris 7, Atelier Pari/gp, Bordeaux, Jan 2015); PARI/GP official documentation [L-functions](https://pari.math.u-bordeaux.fr/dochtml/html-stable/_L_minusfunctions.html).

## Functional Equation & Completed L-function

**General form (Molin, slide "Describe general L function"):**

$$\Lambda(s) = L(s) \gamma(s) = \varepsilon \overline{\Lambda}(w + 1 - s)$$

where:
- $L(s) = \sum_{n \geq 1} a_n n^{-s}$ is the Dirichlet series
- $\gamma(s) = N^{s/2} \prod_{j=1}^d \Gamma_\mathbb{R}(s + \lambda_j)$ is the gamma factor
- $w$ is the weight
- $\varepsilon$ is the root number (norm 1)
- The functional equation relates $\Lambda(s)$ to $\Lambda(\overline{w+1-s})$

**Key:** PARI uses the **completed** $\Lambda(s)$, not bare $L(s)$.

## PARI lfun(L, s) Return Value

**A: lfun(L, s) returns the COMPLETED Λ(s), not L(s).**

From Molin tutorial (Riemann zeta example): `lfun(Zeta, 1)` and `lfun(Zeta, 2)` return completed $\hat{\xi}(s) = \tfrac{1}{2}\Gamma(s/2)\zeta(s)$ values. The functional equation is $\hat{\xi}(s) = 1 \times \hat{\xi}(1-s)$.

---

## lfunsympow: Symmetric Power L-functions

**B: Functional equation for sym²(E):**

PARI's framework for EC L-functions uses the standard analytic normalization. For an elliptic curve $E/\mathbb{Q}$ with weight $w = 2$:

- **Functional equation:** $\Lambda(s) = \varepsilon \Lambda(3 - s)$ 
  - (Weight $w=2$ → critical line at $\text{Re}(s) = \frac{w+1}{2} = 1.5$)
  - Central point is $s = 1.5$ for sym¹(E)

- **For sym²(E):** Weight increases to $w = 3$
  - **Functional equation:** $\Lambda(s) = \varepsilon \Lambda(4 - s)$
  - Critical line at $\text{Re}(s) = 2$

This is **arithmetic normalization** (s ↔ (w+1)−s), converted to analytic via the gamma factor.

---

## C: Conductor for sym²(E)

**Conductor assignment:** Not explicitly documented in available excerpts. Standard arithmetic prediction:
- $\text{cond}(\text{sym}^2 E) = N^3$ (where $N = \text{cond}(E)$)

However, PARI may normalize differently. **Requires direct pari computation to verify.**

---

## D: Gamma Factors

**General gamma structure (Molin):**
$$\gamma(s) = N^{s/2} \prod_{j=1}^d \Gamma_\mathbb{R}(s + \lambda_j)$$

For **sym²(E) (weight 3):** Expected
$$\gamma(s) \approx (2\pi)^{-3s} \Gamma(s) \Gamma(s) \Gamma(s-1)$$
or similar shift. **Exact form not quoted in available sections.**

---

## E: Dirichlet Coefficients

**PARI uses arithmetic Dirichlet series coefficients:**
$$L_{\text{sym}^2}(s) = \sum_{n=1}^\infty \frac{b_n}{n^s}$$

where $b_n = a_n^2 - p$ if $n = p$ is prime (form factor for symmetric square).

This is the **Deligne normalization** (local factor structure $1 - \lambda_p^2 n^{-s} + p \cdot p^{-2s}$).

---

## Confidence & Gaps

| Question | Answer | Confidence | Source |
|----------|--------|------------|--------|
| (A) L(s) vs Λ(s) | **Λ(completed)** | 0.95 | Molin Riemann example explicit |
| (B) FE for sym² | **s ↔ 4−s** | 0.80 | Standard; pari convention assumed |
| (C) Conductor | **N³?** | 0.40 | **NOT documented in fetched excerpts** |
| (D) Gamma factors | **Qw=3 structure** | 0.60 | General form given; exact coeff unknown |
| (E) Coefficients a_p² − p | **Arithmetic** | 0.85 | Standard Deligne; pari presumed consistent |

**Critical gap:** No explicit documentation of lfunsympow conductor assignment or exact gamma factor normalization in available sources. Recommend:
1. Check `lfunconductor(lfunsympow(E, 2))` output directly
2. Verify functional equation numerically via `lfuncheckfeq()`
3. Cross-reference Belabas–Cohen papers or pari source (src/basemath/lfun.c)
