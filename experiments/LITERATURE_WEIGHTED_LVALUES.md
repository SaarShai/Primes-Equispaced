# Literature Search: Weighted Mean Values of L-functions

**Date:** 2026-03-29
**Purpose:** Find results that could produce the log p factor in the lower bound for
$$\sum_{\chi \text{ odd mod } p} |L(1,\chi)|^2 \cdot \left|\sum_{a=1}^{p-1} \lambda(a)\chi(a)\right|^2$$
where $\lambda(a) = M(\lfloor(p-1)/a\rfloor)$ are Mertens-weighted coefficients.

---

## 1. UNWEIGHTED SECOND MOMENT OF L(1,chi) -- THE BASELINE

### The pi^2/6 asymptotic (classical)

The fundamental result for prime modulus p:

$$\frac{2}{p-1} \sum_{\substack{\chi \bmod p \\ \chi \text{ odd}}} |L(1,\chi)|^2 \sim \frac{\pi^2}{6} \quad \text{as } p \to \infty$$

Equivalently: $\sum_{\chi \text{ odd}} |L(1,\chi)|^2 \sim \frac{\pi^2}{12}(p-1)$

This is order $\Theta(p)$ -- NO log p factor.

### Key references:
- **Walum (1982):** "An exact formula for an average of L-series," Illinois J. Math. 26, 1-3.
  Exact formula for the mean square.
- **Louboutin (1994):** [Lou94, Theoreme 4] -- explicit formula for prime moduli.
- **Louboutin (1999):** "On the mean value of |L(1,chi)|^2 for odd primitive Dirichlet characters,"
  Proc. Japan Acad. Ser. A Math. Sci. 75(7), 143-145.
  Shows there is NO simple formula for the mean over *primitive* characters only.
- **Louboutin & Munsch (2021):** Proved $M(p,H) = \pi^2/6 + o(1)$ uniformly over subgroups H
  of odd order d <= (log p)/(3 log log p). [Quarterly J. Math. 72(4), 2021]
- **Louboutin & Munsch (2022/2023):** arXiv:2205.01024, Canadian J. Math. 75(5).
  Extension to non-primitive characters: asymptotic $(\pi^2/6)\prod_{q|d_0}(1-1/q^2)$.
- **Louboutin (2024):** arXiv:2406.02802 -- further explicit formulas involving Dedekind sums
  over subgroups.

### CRITICAL OBSERVATION:
The unweighted second moment gives $\Theta(p)$. We NEED $\Theta(p \log p)$. The extra
log p must come from the Mertens weights $\lambda(a)$.

---

## 2. TWISTED SECOND MOMENTS: $\sum_\chi |L(s,\chi)|^2 |A(\chi)|^2$

This is the framework closest to our problem. We need the sum weighted by
$|A(\chi)|^2$ where $A(\chi) = \sum_a \lambda(a)\chi(a)$.

### Iwaniec-Sarnak (classical, s=1/2):
For a Dirichlet polynomial $A(\chi) = \sum_{n \leq N} a_n \chi(n)$,
$$\sum_{\chi \bmod q}^* |L(1/2,\chi)|^2 |A(\chi)|^2$$
has an asymptotic formula when $N < q^{1/2}$. The main term comes from the
diagonal contribution. Off-diagonal terms contribute to the error.

### Bui-Pratt-Robles-Zaharescu (2020): Breaking the 1/2-barrier
- Paper: "Breaking the 1/2-barrier for the twisted second moment of Dirichlet L-functions,"
  Advances in Mathematics 370 (2020), 107234.
- Extended asymptotic evaluation beyond the $q^{1/2}$ barrier.
- As application: upper bound of correct order for the third moment.
- **Key insight for us:** The asymptotic formula for $\sum_\chi |L(1/2,\chi)|^2|A(\chi)|^2$
  at the central point is well-understood when $A$ is a short Dirichlet polynomial.

### For our problem at s=1:
The technology for s=1/2 does not directly transfer to s=1. At s=1, the L-function is
NOT on the critical line, so the problem has a different character. The analogous
twisted moment at s=1 is less studied but related to:
- Dedekind sums and class numbers (Louboutin's work)
- The spectral decomposition via character orthogonality

### HOW THE log p COULD ARISE:
By Parseval/orthogonality:
$$\sum_{\chi \text{ odd}} |L(1,\chi)|^2 |A(\chi)|^2 = \text{(requires expanding both)}$$

If we write $L(1,\chi) = \sum_{n=1}^\infty \chi(n)/n$ (convergent for odd chi at s=1),
then $L(1,\chi) \cdot A(\chi)$ is the character transform of a convolution, and the
sum over chi extracts a diagonal. The log p comes from the CROSS-TERMS in this diagonal
where the Mertens weights correlate with the coefficients 1/n of L(1,chi).

Specifically: $\sum_{n \leq p} 1/n \sim \log p$, and when the Mertens weights $\lambda(a)$
correlate with 1/a over appropriate ranges, they pick up this logarithmic divergence.

---

## 3. THE MOLLIFIER INTERPRETATION

The Mertens weights $\lambda(a) = M(\lfloor(p-1)/a\rfloor)$ can be interpreted as a
MOLLIFIER for L(1,chi). A mollifier is a Dirichlet polynomial designed to approximate
$L(s,\chi)^{-1}$.

### Key mollifier references:
- **Michel & VanderKam:** Mollifier method for nonvanishing of L(1/2,chi). Mollifier of
  length $p^\theta$. Asymptotic evaluation for $\theta < 1/2$.
- **Cech & Matomaki (2025):** arXiv:2501.12526, "On optimality of mollifiers."
  Proves Michel-VanderKam mollifier is optimal in a wide class of balanced two-piece mollifiers.
  Only prior rigorous optimality proof was by Soundararajan.
- **Zacharias:** Mollified fourth moment of Dirichlet L-functions. Uses spectral theory of
  automorphic forms and bounds for bilinear forms in Kloosterman sums.

### CONNECTION:
If $\lambda(a)$ approximates a mollifier, then $L(1,\chi) \cdot A(\chi) \approx 1$ on
average, and the mollified moment gives
$$\sum_\chi |L(1,\chi) A(\chi)|^2 \approx \sum_\chi 1 = (p-1)/2.$$
But we actually want a LOWER bound on $\sum_\chi |L(1,\chi)|^2 |A(\chi)|^2$, which is
harder. The mollifier analogy suggests the weights AMPLIFY rather than dampen, potentially
giving the log p factor through the size of the mollifier coefficients.

---

## 4. FOURTH MOMENT OF DIRICHLET L-FUNCTIONS

### Heath-Brown (1981):
$$\sum_{\chi \bmod q}^* |L(1/2,\chi)|^4 = \frac{1}{2\pi^2}\phi^*(q)\prod_{p|q}\frac{(1-p^{-1})^3}{(1+p^{-1})}(\log q)^4 + O(2^{\omega(q)} q (\log q)^3)$$
For q prime: $\sim \frac{q}{2\pi^2}(\log q)^4$.
Error term issue: $2^{\omega(q)}$ is problematic for highly composite q.

### Soundararajan (2005/2007):
Extended to all q, removing the restriction on $\omega(q)$.

### Young (2011): Annals of Mathematics 173(1), 1-50.
Power-saving error term for q prime. Uses spectral theory of automorphic forms.
Error exponent 5/512, later improved to 1/20 by Blomer-Fouvry-Kowalski-Michel-Milicevic.

### RELEVANCE TO US:
The fourth moment at s=1/2 gives $\Theta(q(\log q)^4)$. By Cauchy-Schwarz:
$$\left(\sum_\chi |L(1/2,\chi)|^2\right)^2 \leq |\{\chi\}| \cdot \sum_\chi |L(1/2,\chi)|^4$$
$$(q \log q)^2 \leq q \cdot q(\log q)^4$$
This is consistent. But at s=1, the fourth moment of |L(1,chi)| is BOUNDED (pi^4/36 times
the number of characters), so higher moments don't help directly.

---

## 5. SELBERG'S CENTRAL LIMIT THEOREM

### Classical result (Selberg, 1946/1992):
As T -> infinity, log L(1/2+it, chi) / sqrt(1/2 log log T) converges to standard Gaussian.

### For L(1,chi):
The distribution of log L(1,chi) as chi varies over characters mod p has been studied by
Granville-Soundararajan using pretentious methods. The key result is that log |L(1,chi)|
has mean $-\sum_\ell \log(1-1/\ell)/\phi(p) \approx 0$ and variance $\sim \log\log p$.

### Key references:
- **Hsu & Wong (2020):** "On Selberg's Central Limit Theorem for Dirichlet L-functions,"
  J. Theorie Nombres Bordeaux 32, 685-710. New proof via Radziwill-Soundararajan method.
- **Radziwill & Soundararajan (2017):** L'Enseignement Math. 63, 1-19.

### RELEVANCE:
The CLT tells us that |L(1,chi)|^2 is typically of order 1, with rare large values
up to (log p)^2 (under GRH). The LOG P in our sum cannot come from concentration of
L-values; it must come from the WEIGHTS.

---

## 6. MONTGOMERY-VAUGHAN AND MULTIPLICATIVE FUNCTIONS

### Key papers:
- **Montgomery & Vaughan (1977):** "Exponential Sums with Multiplicative Coefficients,"
  Inventiones Math. 43, 69-82. Bounding exponential sums twisted by multiplicative coefficients.
- **Montgomery & Vaughan (1979):** "Mean values of character sums," Canadian J. Math. 31, 476-487.
- **Montgomery & Vaughan (2001):** "Mean-values of multiplicative functions," Periodica Math.
  Hungarica 43, 188-214.

### CONNECTION:
The Mertens function M(n) is NOT multiplicative, but our weights $\lambda(a) = M(\lfloor(p-1)/a\rfloor)$
are sums of the Mobius function, which IS multiplicative. The Montgomery-Vaughan large sieve
for multiplicative coefficients could potentially be applied to bound $\sum_a \lambda(a)\chi(a)$
from below (by showing it can't be too small on average).

---

## 7. GRANVILLE-SOUNDARARAJAN: PRETENTIOUS DISTANCE

### The pretentious framework:
The "distance" between two multiplicative functions f, g with |f|, |g| <= 1:
$$D(f,g;x) := \left(\sum_{p \leq x} \frac{1 - \text{Re}(f(p)\bar{g}(p))}{p}\right)^{1/2}$$

### Key papers:
- **Granville & Soundararajan (2001):** "Large Character Sums," JAMS 14, 365-397.
- **Granville & Soundararajan (2003):** arXiv:math/0503113, "Large Character Sums: Pretentious
  Characters and the Polya-Vinogradov Theorem."
- **Granville & Soundararajan (2008):** "Pretentious Multiplicative Functions and an Inequality
  for the Zeta-Function," CRM Proc. Lecture Notes 46, 191-197.
- **Granville & Soundararajan (2001):** "The Spectrum of Multiplicative Functions," Ann. Math.
  153, 407-470.

### RELEVANCE:
A character chi with large character sum $|\sum_a \lambda(a)\chi(a)|$ must be such that
$\lambda(a)$ "pretends to be" $\bar{\chi}(a)$. Since $\lambda(a)$ involves the Mertens
function, this connects to how close M is to a character-like function. The pretentious
distance framework could give LOWER BOUNDS on the average of $|\sum_a \lambda(a)\chi(a)|^2$
by showing the weights can't be chi-pretentious for too many chi simultaneously.

---

## 8. THE LARGE SIEVE AND PARSEVAL

### Large sieve inequality (classical):
$$\sum_{\chi \bmod q} \left|\sum_{n=1}^N a_n \chi(n)\right|^2 \leq (N + q - 1) \sum_{n=1}^N |a_n|^2$$

Applied to our situation with $a_n = \lambda(n)$ for $1 \leq n \leq p-1$:
$$\sum_{\chi \bmod p} \left|\sum_{a=1}^{p-1} \lambda(a)\chi(a)\right|^2 \leq (2p - 2) \sum_{a=1}^{p-1} |\lambda(a)|^2$$

This is an UPPER bound. We need a LOWER bound.

### Parseval / character orthogonality (exact):
$$\sum_{\chi \bmod p} \left|\sum_{a=1}^{p-1} \lambda(a)\chi(a)\right|^2 = (p-1) \sum_{a=1}^{p-1} |\lambda(a)|^2$$

This is EXACT (not just an inequality!) for $\gcd(a,p)=1$, by orthogonality of characters.
So $\sum_\chi |A(\chi)|^2 = (p-1) \|\lambda\|^2$.

### KEY INSIGHT:
Parseval gives us $\sum_{\text{all } \chi} |A(\chi)|^2 = (p-1)\|\lambda\|^2$. But we need
the SUM RESTRICTED TO ODD chi AND weighted by $|L(1,\chi)|^2$. The question is whether
$|L(1,\chi)|^2$ and $|A(\chi)|^2$ are POSITIVELY CORRELATED over odd characters.

If they were independent: $\sum_{\chi \text{ odd}} |L(1,\chi)|^2 |A(\chi)|^2 \approx
\frac{\pi^2}{6} \cdot \frac{p-1}{2} \cdot \frac{1}{(p-1)/2} \cdot (p-1)\|\lambda\|^2 /2
= \frac{\pi^2}{6} \|\lambda\|^2 (p-1)/2$.

And $\|\lambda\|^2 = \sum_a M(\lfloor(p-1)/a\rfloor)^2 \sim C \cdot p \log p$ (heuristically,
since $M(n)^2 \sim n$ on average and summing $\lfloor(p-1)/a\rfloor$ over a gives $p \log p$).

**THIS IS WHERE THE log p COMES FROM.**

---

## 9. FAREY SEQUENCE L2 DISCREPANCY AND SPECTRAL METHODS

### Franel-Landau theorem (1924):
The RH is equivalent to: $\sum_{\nu=1}^{\Phi(Q)} |\delta_\nu| = o(Q^{1/2+\epsilon})$
where $\delta_\nu$ are the Farey discrepancies. The L2 norm $\sum \delta_\nu^2$ connects
to $M(Q)^2$ and the Mertens function.

### Huxley (1971): "The Distribution of Farey Points. I," Acta Arith. 18, 281-287.
Generalized Franel's theorem to Dirichlet L-functions. This is the KEY connection:
Huxley showed that replacing Mobius-function sums by character-weighted sums converts
the Franel identity into statements about zeros of L(s,chi).

### Dress (1999): "Discrepance des suites de Farey," J. Theorie Nombres Bordeaux 11(2), 345-367.
Remarkable result: the absolute discrepancy of the Farey sequence F_Q equals 1/Q exactly.
Uses Mobius function estimates and exponential sums via Ramanujan sums.

### Maximum mean discrepancies (2024): arXiv:2407.10214.
A large class of positive-semidefinite kernels for which polynomial rate of convergence
of MMD of Farey sequences is equivalent to RH. Includes all Matern kernels of order >= 1/2.

### Kanemitsu & Yoshimoto (1996): "Farey series and the Riemann hypothesis,"
Acta Arith. 75(4), 351-374. Connects Farey discrepancy to character sums and Dedekind sums.

### RELEVANCE TO OUR SPECTRAL FORMULA:
The connection Farey discrepancy -> Mertens function -> character sums via Huxley's
generalization is EXACTLY the chain we exploit. The L2 norm of the Farey discrepancy
decomposes spectrally into character contributions weighted by |L(1,chi)|^2.

---

## 10. DEDEKIND SUMS AND CHARACTER TRANSFORMS

### The B_1 connection:
The first Bernoulli function $B_1(x) = ((x)) = \{x\} - 1/2$ (the sawtooth function)
is central. The Dedekind sum $s(h,k) = \sum_{r=1}^{k-1} ((r/k))((hr/k))$.

### Character transform of Dedekind sums:
For a primitive character chi mod q, the Gauss sum gives $\chi(a) = \tau(\bar\chi)^{-1}
\sum_{n} \bar\chi(n) e(an/q)$. The B_1 function has Fourier expansion
$B_1(x) = -\frac{1}{\pi}\sum_{n=1}^\infty \frac{\sin(2\pi nx)}{n}$, so
$\sum_a B_1(a/p) \chi(a) = -\frac{1}{\pi i} \tau(\chi) L(1,\bar\chi)$ (for odd chi).

### Is $\hat{K} = |B_1|^2$ published?
The "Dedekind kernel" $K(a/p) = \sum_b B_1(b/p)B_1((a+b)/p)$ has character transform
$\hat{K}(\chi) = |L(1,\chi)|^2 / p$ (up to constants and Gauss sum factors).

This appears to be IMPLICIT in:
- **Chakraborty, Kanemitsu, Li, Wang (2009):** "Manifestations of the Parseval identity,"
  Proc. Japan Acad. 85(9). They show the mean square formula for L(1,chi) IS the Parseval
  identity with respect to Yamamoto's orthonormal basis.
- **Walum (1982):** The exact formula for $\sum |L(1,chi)|^2$ is essentially Parseval.
- **Louboutin's series of papers:** The exact formulas via Dedekind sums encode this.

### STATUS: The spectral decomposition $\sum_\chi |L(1,\chi)|^2 \chi(a) = \text{(Dedekind kernel)}$
appears to be KNOWN implicitly but not prominently featured as a standalone result.
It follows from standard Gauss sum manipulations + Parseval, and is implicit in the
Chakraborty-Kanemitsu-Li-Wang paper and Walum's identity.

---

## 11. MEAN VALUES WITH ARITHMETIC WEIGHTS (CLOSEST TO OUR NEEDS)

### Choi & Kumchev (2004): arXiv:math/0412227.
Mean values of Dirichlet polynomials with von Mangoldt function coefficients.
New mean-value theorem with $a_n = \Lambda(n)$ (von Mangoldt function).
Application to exponential sums over primes and linear equations with prime variables.

### Goldston & Gonek: Mean values for long Dirichlet polynomials.
When polynomials have more terms than the integration range, off-diagonal contributions
matter. Need correlation functions for the coefficients.

### Ramare: "Arithmetical Aspects of the Large Sieve Inequality" (2009, HRI/Hindustan Book Agency).
Connects large sieve, Selberg sieve, Farey dissection, pseudo-characters, Lambda_Q function.

### WHAT WE NEED BUT DON'T HAVE:
A result of the form
$$\sum_{\chi \text{ odd mod } p} |L(1,\chi)|^2 \left|\sum_{a=1}^{p-1} \lambda(a)\chi(a)\right|^2
\geq c \cdot p \log p$$
where $\lambda(a) = M(\lfloor(p-1)/a\rfloor)$.

This seems to require:
(a) The Parseval-type identity for the character transform of Mertens weights
(b) The correlation between $|L(1,\chi)|^2$ and $|A(\chi)|^2$ over odd characters
(c) Showing that $\|\lambda\|^2 = \sum_a M(\lfloor(p-1)/a\rfloor)^2 \sim C \cdot p \log p$

Step (c) is the most novel and may be provable using standard Mertens function estimates.

---

## 12. STRATEGY ASSESSMENT

### Most promising approach:
1. **Prove $\|\lambda\|^2 \sim Cp\log p$** using Mertens function estimates and hyperbola method.
   This is the source of the log p factor.
2. **Use Parseval** to get $\sum_{\text{all } \chi} |A(\chi)|^2 = (p-1)\|\lambda\|^2 \sim Cp^2\log p$.
3. **Show positive correlation** (or at least non-negative correlation) between $|L(1,\chi)|^2$
   and $|A(\chi)|^2$ over odd characters, or use Cauchy-Schwarz in the other direction.

### Alternative approach via spectral decomposition:
Expand $\sum_{\chi \text{odd}} |L(1,\chi)|^2|A(\chi)|^2$ using the explicit formula for
$L(1,\chi)$ in terms of $B_1$ (sawtooth function). This converts the sum into a sum over
Farey fractions weighted by Mertens values, which is DIRECTLY our Farey discrepancy.

### Papers still to obtain and check:
- Walum (1982) exact formula -- need the explicit form
- Chakraborty et al. (2009) Parseval identity paper -- need details of Yamamoto's basis
- Huxley (1971) -- need the exact form of the generalized Franel identity
- Louboutin (1999) Proc. Japan Acad. -- need the exact formula for prime moduli

---

## SUMMARY TABLE

| Topic | Key Result | Source of log p? | Reference |
|-------|-----------|-----------------|-----------|
| Unweighted $\sum |L(1,\chi)|^2$ | $\sim (\pi^2/6)(p/2)$ | NO | Walum, Louboutin |
| Twisted moment at s=1/2 | Asymptotic for $N < q^{1/2}$ | YES (from $\log q$ in the moment) | Iwaniec-Sarnak, Bui et al. |
| Fourth moment at s=1/2 | $\sim q(\log q)^4/(2\pi^2)$ | YES | Heath-Brown, Young |
| Mollified moments | Controls nonvanishing | Indirectly | Michel-VanderKam |
| Selberg CLT | Gaussian with variance $\log\log p$ | NO | Hsu-Wong |
| Large sieve | Upper bound $(p-1)\|\lambda\|^2$ | From $\|\lambda\|^2$ | Montgomery-Vaughan |
| **Parseval (exact)** | $\sum_\chi |A(\chi)|^2 = (p-1)\|\lambda\|^2$ | **From $\|\lambda\|^2 \sim Cp\log p$** | Standard |
| Franel-Huxley spectral | L2 discrepancy = character sum | Structural | Huxley (1971) |
| Dedekind sum transform | $\hat{K} = |L(1,\chi)|^2/p$ | Implicit | Chakraborty et al. |
| $\|\lambda\|^2$ estimate | $\sum M(\lfloor(p-1)/a\rfloor)^2 \sim Cp\log p$ | **THIS IS THE KEY** | Needs proof |

**BOTTOM LINE:** The log p factor comes from $\|\lambda\|^2 = \sum_{a=1}^{p-1} M(\lfloor(p-1)/a\rfloor)^2$,
which should be $\sim Cp\log p$ by a hyperbola-method computation using $\sum_{n \leq x} M(n)^2 \sim cx$.
The twisted moment technology (Iwaniec-Sarnak, Bui et al.) confirms that weighted second moments
with Dirichlet polynomial twists are computable, but the specific case at s=1 with Mertens weights
appears to be NEW.
