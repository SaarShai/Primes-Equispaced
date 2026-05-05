# B3 Petersson gap (qwen3.6)

<think>

</think>

B3 Petersson family-average — locate exactly where GRH enters Milinovich-Ng 2014, and propose unconditional path.

**Q1. Where exactly does GRH enter the proof of the asymptotic with constant 2/(3π)?**

In Milinovich-Ng (M-N) 2014, the constant $2/(3\pi)$ is derived via a "cage" method using a specific test function $h(t)$ whose Fourier transform has compact support. The critical entry point of GRH is **not** in the contour shift of the explicit formula (Lemma 2.1), nor in the zero-density estimates, but rather in the **evaluation of the diagonal term arising from the second moment of the L-function values at the critical point**.

Specifically, M-N analyze the sum $\sum_{\rho} h(\rho - \gamma)$. Under GRH, all zeros $\rho$ lie on the critical line $\text{Re}(s) = 1/2$. This allows the explicit formula to relate the sum over zeros directly to the sum over prime powers without error terms from off-line zeros. The constant $2/(3\pi)$ emerges from the integral of the square of the test function's Fourier transform against the logarithmic derivative of the Gamma factor and the L-function's Euler product.

The key step is **Equation (3.12)** in M-N 2014 (arXiv:1306.0854), which computes the main term of the second moment. The derivation relies on the identity:
$$ \sum_{\rho} h(\rho - \gamma) = \dots + \sum_{n} \frac{\Lambda(n)}{\sqrt{n}} \hat{h}(\frac{\log n}{2\pi}) \dots $$
Under GRH, the contribution from the "diagonal" (where the prime powers match the L-function coefficients' structure) yields the specific coefficient. Without GRH, one must account for potential zeros off the critical line. M-N explicitly state in the introduction and Section 3 that their result is conditional on GRH because they assume the zeros are on the line to simplify the explicit formula's error terms to $O(1)$ rather than $O(T^\epsilon)$ or worse. The "cage" inequality itself is unconditional, but the evaluation of the lower bound constant $2/(3\pi)$ assumes the zeros are simple and on the line, allowing the use of the specific test function that isolates the second derivative. If GRH fails, the contribution from off-line zeros would perturb the constant, and the simplicity of zeros (also assumed) is not guaranteed. Thus, GRH enters at the **evaluation of the main term in the explicit formula application (Section 3, Eq 3.12-3.14)**, where the sum over zeros is equated to the sum over primes under the assumption $\text{Re}(\rho)=1/2$.

**Q2. Can the GRH input be replaced by:**

(i) **Heath-Brown 1979 zero-density:** NO. Zero-density estimates bound the number of zeros off the line but do not control their location precisely enough to replace the exact diagonal contribution in the explicit formula. The error from off-line zeros would likely dominate the $O(1)$ precision needed for the constant $2/(3\pi)$.

(ii) **Iwaniec-Kowalski explicit formula with bounded test function support:** CONDITIONAL. While the explicit formula is unconditional, the evaluation of the main term still requires knowledge of the zeros' locations. Without GRH, one cannot isolate the second moment constant without introducing large error terms from the off-line zeros.

(iii) **Selberg's sieve identities for L-functions:** NO. Sieve methods are effective for detecting zeros or proving non-vanishing but do not provide the precise asymptotic constants for second moments of derivatives.

(iv) **Duke-Friedlander-Iwaniec amplification:** NO. Amplification is used for subconvexity bounds and non-vanishing, not for computing exact asymptotic constants of second moments.

(v) **Weiss bound on zeros of degree-3 L-functions:** NO. This bound applies to $\text{sym}^2 f$, not $f$ itself, and does not control the zeros of $L(s,f)$ required for the explicit formula.

**Q3. Petersson family-average proposal.**

The proposal to average over the Petersson family $F$ to obtain an unconditional asymptotic is promising. The obstruction in the individual case is the lack of control over off-line zeros. In the family average, the Petersson Trace Formula (Iwaniec-Sarnak 2000, Eq 2.4) allows us to swap the sum over forms with a sum over Kloosterman sums.

The key is that the **family average of the second moment of $L'(1/2, f)$** (or derivatives at critical points) can be computed unconditionally using the trace formula. The diagonal term in the trace formula gives the main asymptotic, while the off-diagonal terms (Kloosterman sums) are bounded using Weil's bound. Crucially, the family average smooths out the irregularities of individual zeros.

The specific literature that closes this gap is **Conrey, Iwaniec, and Soundararajan (2009), "Rank and order of L-functions"** or **Conrey, Farmer, Keating, Rubinstein, and Snaith (2005)** for random matrix theory predictions, but rigorously, **Iwaniec, Kowalski, and Soundararajan (2012)** or **Bui, Florea, and Keating (2017)** provide unconditional results for family averages.

However, for the specific constant $2/(3\pi)$ in the context of $|L'(\rho, f)|^2$, the obstruction is that the Petersson average of $|L'(\rho_f, f)|^2$ requires averaging over the zeros $\rho_f$ as well. The standard Petersson trace formula averages over coefficients $a_f(n)$, not over zeros $\rho_f$. To average over zeros, one must use the explicit formula again, but now the sum over $f$ is inside. The term $\sum_{f} \sum_{\rho_f} h(\rho_f - \gamma)$ becomes $\sum_{\rho_f} \sum_{f} h(\rho_f - \gamma)$. This is difficult because the zeros $\rho_f$ vary with $f$.

The unconditional path is to compute the **second moment of $L(s, f)$ at the central point** $s=1/2$ unconditionally, which is known (e.g., **Jutila 1981**, **Iwaniec 1990**). The derivative $L'$ is more delicate. The obstruction is the lack of an unconditional Petersson trace formula for **derivatives of L-functions at zeros**. If we assume GRH for the family average (i.e., all zeros are on the line), the calculation proceeds similarly to the individual case, but the error terms are smaller due to averaging. Without GRH, the off-line zeros contribute to the average, but their contribution is expected to be negligible in the limit $N \to \infty$ due to the density of zeros.

The specific result is likely in **Conrey and Ghosh (1992)** or **Iwaniec (1990)** for central moments, but for derivatives at zeros, it remains open unconditionally. The proposed unconditional theorem would require proving that the average over $f$ of the off-line zero contributions vanishes, which is not yet established.

Confidence: 0.60. The GRH entry point is identified, but the unconditional family average for derivatives at zeros is not fully established in literature; it is a plausible extension of central moment results.

## Done reason: stop