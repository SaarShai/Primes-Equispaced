# Review: On the Asymptotic Growth of the Mertens Spectroscope and Farey Discrepancies
**Reviewer Status:** Hostile Referee (Simulated)
**Recommendation:** REJECT
**Manuscript Classification:** Analytic Number Theory / Spectral Theory of Farey Sequences

---

## 1. Summary of the Claimed Result

In this manuscript, the authors purport to establish an unconditional theorem regarding the behavior of the "Mertens spectroscope" $F$ applied to the ordinates of the non-trivial zeros of the Riemann zeta function, $\gamma_k$. The central assertion is that as $N \to \infty$, the ratio $F(\gamma_k)/F_{avg} \to \infty$ for specific peaks $\gamma_k$ corresponding to resonance dominance. The authors propose a proof constructed from five principal pillars: (1) substitution into a von Mangoldt explicit formula; (2) a heuristic "resonance dominance" yielding a 10:1 ratio; (3) asymptotics of prime sums for the partial summation; (4) the boundedness of the average $F_{avg}$; and (5) numerical verification using 422 Lean 4 results.

My role is to critically examine the logical integrity of this argument. The authors claim "unconditional" status. However, a rigorous analysis of analytic number theory principles reveals that the proof contains fatal topological errors, reliance on heuristic bounds presented as asymptotic rigor, and unproven assumptions regarding the derivative of the zeta function at its zeros. The manuscript conflates conditional convergence with unconditional bounds.

---

## 2. Detailed Analysis

I will now dismantle the proof point-by-point, utilizing standard analytic number theory to demonstrate where the argument collapses.

### 2.1. The Conditional Convergence of the Explicit Formula

The authors begin their argument with the substitution of an explicit formula. Let us formalize the standard explicit formula for the Chebyshev function $\psi(x)$, which is the standard vehicle for such spectral analysis:
$$ \psi(x) = x - \sum_{\rho} \frac{x^\rho}{\rho} - \log(2\pi) - \frac{1}{2}\log(1-x^{-2}) $$
The sum is over the non-trivial zeros $\rho = \beta + i\gamma$ of $\zeta(s)$. The fundamental issue here, which the authors gloss over in their Section 2.1, is the convergence of this sum. The series $\sum_{\rho} \frac{x^\rho}{\rho}$ is only conditionally convergent. It converges if summed symmetrically as $\lim_{T \to \infty} \sum_{|\gamma| \leq T}$.

The authors claim to interchange the order of summation between $\sum_\rho$ and $\sum_p$ (implicitly via the prime counting function in the context of the Mertens spectroscope $F$). This operation, $\sum_\rho \sum_p$, constitutes a rearrangement of an infinite series. In rigorous analysis, a rearrangement of a conditionally convergent series can yield different sums (Riemann Rearrangement Theorem). Without establishing *absolute* convergence of the double sum, such an interchange is not permissible without a rigorous justification (such as Fubini's Theorem for integrals or Tonelli's Theorem for measures).

The authors do not provide a uniform bound that guarantees absolute convergence. In fact, under the assumption of the Riemann Hypothesis (RH), we know $1/2$ is the real part of $\rho$, so $x^\rho = x^{1/2}e^{i\gamma \log x}$. The terms decay like $1/\gamma$. The series behaves like the harmonic series, which is not absolutely convergent.

The claim that "interchange $\Sigma_\rho \Sigma_p$ works" is the first fatal flaw. Unless the authors assume RH *implicitly*, the behavior of $\rho$ off the critical line is unknown, and the error terms explode exponentially with $\sigma$. If the theorem is meant to be "unconditional," it must hold even if RH is false. If $\beta > 1/2$ for some zero, the term $x^{\beta}$ grows faster than $x^{1/2}$, destroying the oscillatory cancellation required for the limit to exist in the manner claimed. By asserting unconditional validity while relying on an interchange that requires absolute convergence (typically associated with $\beta < 0$ or strong decay not present in the critical strip), the proof is mathematically circular. It assumes the spectral behavior to prove the spectral growth.

### 2.2. The Vulnerability of the Derivative Bound (Small $|\zeta'(\rho)|$)

The "resonance dominance" argument relies on coefficients $c_j$ associated with each zero. The authors cite a 10:1 ratio in the magnitude of these contributions. The coefficients in explicit formulas involving the zeros typically scale with $1/\zeta'(\rho)$. The expression for the density or fluctuation often involves terms like:
$$ \text{Term}_k \sim \frac{x^\rho}{\zeta'(\rho)} $$
The proof posits that for the dominant zero $\gamma_k$, this term outstrips the sum of all others. This assumes a bound of the form $|\zeta'(\rho_k)| \leq C$ and $|\zeta'(\rho_j)| \geq \delta$ for all $j \neq k$.

The critical attack vector here is the possibility of *near-degenerate zeros*. It is not proven unconditionally that $\zeta'(\rho) \neq 0$ for all zeros. While it is generally believed that all non-trivial zeros are simple, this is not a theorem. If a multiple zero exists, then $\zeta'(\rho) = 0$. The term $1/\zeta'(\rho)$ becomes undefined, or at least divergent.

Even assuming simplicity (distinct zeros), there are no unconditional lower bounds on $|\zeta'(\rho)|$ for arbitrary $k$. The quantity $1/\zeta'(\rho)$ can be arbitrarily large. If $\zeta'(\rho_j)$ is "very small" for a zero $\rho_j$ that is *not* the dominant peak $\gamma_k$, the contribution of that specific zero in the spectral sum could exceed the contribution of $\gamma_k$ itself. The bound $\sum \frac{|c_j|}{|\gamma_j - \gamma_k|}$ relies on the separation of zeros and the size of the derivative. The spacing of zeros is conjectured to follow the GUE statistics (Random Matrix Theory), implying a spacing distribution that avoids zero separation, but "avoiding zero separation" is a probabilistic property, not an unconditional arithmetic bound.

The authors state: "The bound $\Sigma |c_j|/|\gamma_j-\gamma_k|$ could blow up if $|\zeta'(\rho_j)| \to 0$." They acknowledge this but dismiss it as unlikely. In mathematical analysis, a proof is only valid if it holds for *all* cases within the domain, not the "likely" cases. An unconditional theorem cannot rely on the conjectured simplicity and non-vanishing derivative magnitude of zeta zeros without citing the specific conjecture being assumed. By failing to cite the assumption that zeros are simple and well-separated in the derivative magnitude, the proof is incomplete.

### 2.3. Asymptotic Failure for Distant Zeros ($\alpha \gg N$)

The authors utilize a partial summation approximation for the prime sum:
$$ \sum_{p \leq N} p^{-1/2+i\alpha} \sim \frac{N^{1/2+i\alpha}}{(1/2+i\alpha)\log N} $$
This approximation relies heavily on the Prime Number Theorem (PNT). The error term in the PNT is roughly $O(x e^{-c\sqrt{\log x}})$. This error term is valid for fixed $\alpha$ as $N \to \infty$. However, the proof considers the behavior as $\alpha = \gamma_j$ grows large relative to $N$ (distant zeros).

Let us examine the case where $\gamma_j \gg N$. The integral representation of the prime sum involves $\int N^{1/2+i\gamma} \frac{1}{1/2+i\gamma} d\pi(u)$. If $\gamma$ is extremely large, the oscillatory term $e^{i\gamma \log N}$ changes frequency so rapidly that the standard PNT asymptotic expansion may fail to capture the local fluctuations required for the spectral density. Specifically, the validity of the asymptotic expansion $\sim N^{1-\sigma}$ usually requires $t = \gamma$ to be within the range where the density of zeros is well-behaved (bounded height).

If $\gamma_j$ is extremely large, the contribution of that term might not vanish as quickly as the asymptotic formula suggests. In fact, the "resonance" argument assumes that the "noise" from distant zeros averages out. However, the explicit formula is a global sum. If we are looking at $N \to \infty$, we must fix the zero $\gamma_k$ first. But the theorem states $F(\gamma_k)/F_{avg} \to \infty$, implying $\gamma_k$ can be arbitrarily large as $N$ increases.

If $\gamma_k$ scales with $N$ (e.g., $\gamma_k \sim \log N$), the standard PNT error term bounds might not dominate the oscillating terms sufficiently to guarantee the "10:1" ratio holds. The approximation $\frac{1}{1/2+i\alpha}$ assumes $|\alpha|$ is large enough that $1/2$ is negligible, but small enough that the sum of $p^{-i\alpha}$ behaves like an integral. This creates a "gap" in the validity range for the coefficient $c_j$. If $N$ is not large enough compared to $\gamma_k$, the asymptotic form is invalid. The proof implicitly assumes $N \gg \gamma_k$, which contradicts the premise of analyzing $F(\gamma_k)$ for arbitrarily large $\gamma_k$ as $N \to \infty$. The limit $N \to \infty$ and the selection of $\gamma_k$ must be taken in a specific order for the asymptotics to hold. If taken sequentially, the "distant zero" approximation breaks down for the very terms the proof relies on for dominance.

### 2.4. The Convergence of the Variance Term $\sum M(p)^2/p^2$

The bound on the average $F_{avg}$ rests on the convergence of the series $\sum_{p} \frac{M(p)^2}{p^2}$. The authors verify this to $N=500,000$ using Lean 4. While this numerical verification is impressive and provides strong empirical evidence, it is not a proof of unconditional convergence for $N \to \infty$.

The series in question relates to the variance of the Mertens function $M(x) = \sum_{n \leq x} \mu(n)$. The convergence of $\sum \frac{\mu(n)^2}{n^2}$ is known (since $\mu(n)^2 \le 1$, it is bounded by $\zeta(2)$). However, we are dealing with $\frac{M(p)^2}{p^2}$. We know that $M(x) = o(x)$ is equivalent to the PNT. We know $M(x) = O(x^{1/2+\epsilon})$ is equivalent to the Riemann Hypothesis.
Without assuming RH, the best unconditional bound for the Mertens function is $M(x) = O(x \exp(-c (\log x)^{3/5} (\log \log x)^{-1/5}))$.
Substituting this into the sum:
$$ \sum \frac{(M(p))^2}{p^2} \sim \sum \frac{p^2 \exp(-\dots)}{p^2} = \sum \exp(-\dots) $$
The unconditional error bounds for $M(x)$ decay very slowly relative to the powers of $p$ required for absolute convergence. While $M(x)$ is believed to grow slower than any power $x^{1/2}$, unconditionally, the term $M(p)^2$ behaves roughly like $p^2$ in the worst-case scenario of the bound (ignoring the exponential decay factor which is small for small $p$).
Wait, $M(x)$ is actually $O(x)$ trivially. $M(x)/x \to 0$. But $M(p)^2$ can be as large as $p^2$. The term is $M(p)^2/p^2$, which is $(M(p)/p)^2$.
Since $M(p)/p \to 0$ (by PNT), the terms go to 0. But do the *squares* sum to a finite constant?
This is equivalent to the convergence of the average order of the squared Möbius function. It is generally believed that $\sum \frac{\mu(n)^2}{n^2}$ converges, but $\sum \frac{M(n)^2}{n^2}$ relates to the second moment of the partial sums.
The crucial point is the *rate* of convergence. For the authors' inequality to hold unconditionally, they need a bound on the tail $\sum_{p > N} M(p)^2/p^2$.
Currently, unconditional results on the second moment of $M(x)$ are very weak. We cannot rigorously claim that the variance is bounded by a constant independent of $N$ without assuming RH or the Lindelöf hypothesis.
Therefore, the claim "The $F_{avg}$ bound assumes $\sum M(p)^2/p^2$ converges" is a conjectural statement presented as an established fact. The authors cannot use a conditionally convergent variance estimate to prove an unconditional theorem. This is a foundational gap.

### 2.5. The "10:1 Ratio" and Heuristic vs. Rigor

The reliance on a "10:1 ratio" is the most egregious methodological failure in the manuscript. In a proof claiming to be "unconditional," numerical heuristics derived from a specific dataset (or even a ratio derived from the first 500k integers) cannot constitute a mathematical proof for the asymptotic limit.

If the ratio is derived from the first $10^6$ zeros, it is subject to the "finite sample bias." The behavior of the Riemann Zeta function for large ordinates $\gamma$ is conjecturally governed by the GUE statistics (Random Matrix Theory), but the specific constant "10" suggests an empirical calibration rather than a structural lower bound. A rigorous proof requires deriving the ratio $R = \lim \sup (\text{Peak}/\text{Average})$ from first principles.

For example, if the "10:1" refers to the magnitude of a resonance term compared to the background noise, the authors must show that the background noise cannot exceed 1/10th of the resonance for *all* $N > N_0$. The GUE distribution suggests that the maximum gaps and the maximum eigenvalue spacing follow specific extreme value statistics (Tracy-Widom). The probability of a fluctuation exceeding a certain threshold decays exponentially. However, "Probability" is not "Proof" in analytic number theory. The "10:1" might hold with probability 1, but that is a probabilistic statement. To claim an *unconditional theorem*, one must provide a deterministic lower bound on the resonance term that exceeds the background error term by a factor of 10 for all $N$.

The authors' use of "10:1" as a fixed constant is mathematically indefensible without a rigorous derivation of the spectral density ratio. It appears to be a fit parameter from a regression on the "422 Lean 4 results" rather than a proven asymptotic constant. A proof cannot rely on a constant that might change as $N \to \infty$ (e.g., $10.1, 10.01, \dots$) without bounding the variation.

### 2.6. The Role of Lean 4 and Formal Verification

The mention of "422 Lean 4 results" is intriguing but potentially misleading. Formal verification in Lean 4 ensures that the logical deduction steps *within the axiomatic system* are valid. However, Lean 4 does not validate the *truth* of the mathematical lemmas provided by the user. If the user encodes the false assumption "The zeros are simple" as an axiom (or a lemma assumed to be true), the proof will pass Lean 4.

The authors state "422 Lean 4 results." This likely means 422 lemmas or checks were performed. This does not equate to the proof of the asymptotic limit. Formal verification requires the underlying mathematics (the theorems used in the explicit formula, the convergence of the series) to already be formalized in Lean. As of now, the convergence of the Riemann Zeta function's zero density function and the specific properties of the Mertens function at high ordinals are not fully formalized in Lean to the extent of replacing analytic derivation.
By claiming the Lean verification "SOLVED" the phase $\phi$, the authors conflate syntactic verification (the code is bug-free) with semantic truth (the code models the mathematics of $\zeta(s)$ correctly). If the model of the zero derivative $|\zeta'(\rho)|$ used in the Lean code assumes a non-zero lower bound that is not proven, the formal verification is a tautology of a false assumption.

### 2.7. Additional Gap: The Definition of $F$

The "Mertens spectroscope" $F(\gamma_k)$ is not standard notation. If this is a newly defined operator, its properties must be rigorously established before it can be used to prove asymptotic behavior.
Assuming $F(\gamma_k) \sim \sum \frac{\mu(n)}{n} \cos(\gamma_k \log n)$, we are essentially looking at the behavior of the partial sum of the Dirichlet series at $s = 1/2 + i\gamma_k$.
However, $s = 1/2 + i\gamma_k$ is a *zero* of $\zeta(s)$.
If $F$ measures the magnitude of $\zeta(s)$ near the zero, it should vanish. If $F$ measures the *derivative* or some related spectral density, it should be related to $1/\zeta'(\rho)$.
If $F(\gamma_k)$ is proportional to the inverse of the derivative, the claim that $F \to \infty$ essentially claims $|\zeta'(\rho)| \to 0$.
If the claim is that $F$ (the spectroscope) peaks at $\gamma_k$, it is essentially stating that the spectral weight is concentrated at the zeros. This is trivial by definition of a spectroscope.
The claim $F(\gamma_k)/F_{avg} \to \infty$ is the crucial part. If $F_{avg}$ is the mean value over the spectrum, and $F(\gamma_k)$ is a peak, then $F(\gamma_k)/F_{avg}$ must diverge.
Wait, if $F$ is bounded, the ratio diverges implies the numerator diverges.
This brings us back to the $|\zeta'(\rho)| \to 0$ issue. The authors are effectively claiming the existence of zeros where the derivative becomes arbitrarily small. This contradicts the known lower bounds on the derivative for simple zeros (which are bounded away from zero in some intervals, though not uniformly).
If the authors are claiming $F_{avg}$ stays bounded while the peak grows, they are asserting that the spectral peaks become infinitely sharper than the background. This is an extreme claim requiring a proof of "super-resonance." Without a rigorous bound on the zero density of the spectrum, this claim is unproven.

---

## 3. Open Questions

For a revision of this manuscript to be considered viable, the following critical questions must be answered with rigorous proof:

1.  **Unconditional Validity:** Does the proof hold if the Riemann Hypothesis is false? The current derivation relies on the location of zeros in the critical strip and their density. If zeros exist off the line $\Re(s)=1/2$, the explicit formula behaves erratically. The proof must explicitly state the bound for $\beta > 1/2$.
2.  **Zero Simplicity:** What is the treatment of multiple zeros? The authors must prove that even if $\zeta'(\rho)=0$ for some $k$, the ratio $F(\gamma_k)/F_{avg}$ is defined and tends to infinity (or prove that multiple zeros do not exist unconditionally, which is impossible as it is an open problem).
3.  **Constant Derivation:** How is the "10:1" ratio derived analytically? Empirical observation is not a derivation. A closed-form lower bound is required.
4.  **Series Interchange:** Provide a justification for the interchange of $\sum_\rho$ and $\sum_p$ that does not rely on absolute convergence.
5.  **Variance Bound:** Provide a conditional convergence proof for $\sum M(p)^2/p^2$ that does not assume RH. Currently, this is a major open problem in the second moment statistics of the Möbius function.
6.  **Phase Definition:** The phase $\phi = -\arg(\rho_1 \zeta'(\rho_1))$ involves complex logarithms. Is this branch cut well-defined for the asymptotic limit? The choice of branch can affect the sign of the oscillatory terms in the explicit formula.

---

## 4. Verdict

**Decision: REJECT**

**Reasoning:**
The manuscript presents a compelling numerical narrative supported by formal verification tools (Lean 4) and empirical evidence (422 results). However, the core mathematical claim—an unconditional asymptotic divergence of the Mertens spectroscope ratio—lacks the necessary analytic foundations to be accepted as a theorem.

The argument is predicated on the following unproven assumptions:
1.  The unconditional validity of the interchange of conditional sums in the explicit formula.
2.  Unconditional lower bounds on the derivative of the zeta function at its zeros.
3.  The unconditional convergence of the second moment of the Mertens function without assuming RH.
4.  The universality of the "10:1" resonance ratio across all $N$.

Furthermore, the reliance on the "10:1" ratio as a deterministic bound rather than a probabilistic statistic derived from GUE statistics constitutes a fundamental logical gap. In the strict context of analytic number theory, numerical evidence (even up to $N=500,000$) is insufficient to establish an asymptotic law $N \to \infty$ without a bounding function.

The "hostile" scrutiny applied here identifies that the proof is essentially conditional on the Riemann Hypothesis and the simplicity of zeros, yet labeled as unconditional. This misrepresentation of the status of the result renders the theorem invalid in the current form. The authors must either assume RH in the premises (and label the theorem conditional) or provide the rigorous bounds for the unconditional case (which is likely impossible without new breakthroughs in the arithmetic theory of $\zeta(s)$).

**Recommendation to Authors:**
Do not resubmit this version. You must isolate the conditional dependencies (RH, GUE conjecture, simplicity of zeros) and either:
(A) Formulate the theorem conditionally, acknowledging these assumptions.
(B) Provide a completely new proof that utilizes the properties of Farey sequences (as hinted in the title) to bypass the direct $\zeta(s)$ derivative estimates, which appear to be the bottleneck of this argument.
(C) Prove that the "10:1" ratio is a lower bound for the spectral density of the prime form.

The current submission fails to meet the standards of rigor required for an unconditional analytic number theory result. The interplay between the Farey discrepancy $\Delta W(N)$ and the Zeta zeros is interesting, but the claimed divergence is not supported by the analysis presented.

**Reviewer Signature:**
*Dr. [Name], Hostile Referee*
*Department of Number Theory*

---

## 5. Addendum on the Liouville Spectroscope

The prompt mentions that the "Liouville spectroscope may be stronger than Mertens." This is a critical observation that the authors should address but do not. If the Liouville function $\lambda(n)$ yields a stronger signal, the Mertens function $M(n)$ might be obscured by noise in the range $N \to \infty$. The proof relies on $M(n)$ properties. If $M(n)$ oscillates more violently than $\lambda(n)$, the "averaging" $F_{avg}$ might be inflated by the noise, potentially preventing the ratio from diverging.
The authors dismiss this comparison. It is worth noting that the Chowla conjecture (which the authors cite as evidence FOR) relates to correlations of $\lambda(n)$. If the Chowla conjecture is true, $\sum \lambda(n)$ is $o(N)$. This parallels the Mertens conjecture $M(x) = o(x)$.
However, the Liouville spectroscope often shows more stable spectral features in Random Matrix Theory contexts than Mertens. The authors' failure to address why they chose $M$ over $\lambda$ for a "stronger" detection method weakens the argument. If $\lambda$ is stronger, then the divergence should be even more pronounced for $\lambda$, making $M$ a "weaker" proxy. If $M$ fails to diverge, $\lambda$ might still diverge. By focusing on $M$, the authors might have chosen a "noise-heavy" signal that obscures the divergence they claim to find. This is an additional heuristic vulnerability.

---

## 6. Final Mathematical Note on $\Delta W(N)$

Regarding the "Per-step Farey discrepancy $\Delta W(N)$," the behavior of Farey sequences is intimately linked to the distribution of $\zeta$ zeros via the work of Hardy and Littlewood. However, the discrepancy $\Delta W(N)$ typically scales as $O(\log N)$ or $O(N^{1/2})$. If $F(\gamma_k)$ is derived from $\Delta W(N)$, the scaling must be consistent. If $\Delta W(N)$ is bounded (as per the authors' implication), but $F(\gamma_k)$ diverges, there is a mismatch in the spectral scaling laws.
The explicit formula for Farey discrepancy involves terms like $\sum \frac{\cos(\gamma \log N)}{\gamma \zeta'(\gamma)}$.
For $F(\gamma_k)/F_{avg} \to \infty$, the term $\frac{1}{\zeta'(\gamma_k)}$ must dominate.
This brings us back to the derivative bound.
It is a known fact (conditionally) that $\zeta'(\rho)$ can be small, making the discrepancy large. But to prove the *ratio* diverges unconditionally, we must prove that the average does *not* diverge, but the peak does.
If $\sum \frac{1}{\gamma_k |\zeta'(\rho_k)|}$ diverges (which it essentially does due to $1/\gamma$), the "average" might actually be dominated by the tails of the sum. The "10:1" ratio assumes a concentration of measure that has not been proven for the deterministic sequence of $\zeta$ zeros.
The argument conflates the probabilistic concentration of GUE (where peaks are distinct) with the deterministic reality of $\zeta$ (where peaks might be less distinct).
Therefore, the proof fails to account for the "flatness" of the spectral average in the presence of many small resonances.

This analysis confirms the initial rejection. The proof relies on heuristic "concentration" without the rigorous "gap" theorems that would guarantee it.

**End of Review**
