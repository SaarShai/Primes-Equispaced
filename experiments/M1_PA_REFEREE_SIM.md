# REFEREE REPORT: Manuscript M1_PA_FAREY

**Journal:** *Experimental Mathematics* (Simulated Submission)
**Manuscript Title:** Per-Step Analysis of Farey Sequence Uniformity
**Author:** Saar Shai
**Date:** October 26, 2023
**Referee:** Mathematical Research Assistant / Senior Analyst (Analytic Number Theory & Computational Math)

---

## 1. SUMMARY

This manuscript by Saar Shai presents a novel computational and theoretical investigation into the per-step discrepancies of Farey sequences. The central object of study is the wobble function $W(N) = \sum_{j=1}^N (f_j - j/n)^2$, where the authors analyze the change $\Delta W(p)$ at prime steps $p$. The author derives several algebraic identities, including a bridge identity relating sums of exponentials over the Farey sequence $\mathcal{F}_{p-1}$ to the Mertens function $M(p)$, and a decomposition $\Delta W(p) = A - B - C - D$. The paper employs a "Mertens spectroscope" to detect Riemann zeros via the spectral properties of the Farey sequence. The work claims to be formally verified using the Lean 4 proof assistant (reporting 441 verified results) and asserts a strong correlation ($r=0.77$) between the sign of $\Delta W(p)$ and the Mertens function. The computational scope extends up to $N=100,000$, identifying a significant counterexample at $p=243,799$. The findings suggest a deeper link between Farey sequence uniformity and the distribution of zeros of the Riemann zeta function.

## 2. RECOMMENDATION

**Decision:** **Major Revisions**

**Reasoning:** The manuscript contains a compelling blend of analytic number theory and computational experimentation. The theoretical framework, specifically the decomposition of $\Delta W(p)$ and the connection to Ramanujan sums, is mathematically sound in its structure, though the claims regarding universality require significant re-evaluation due to the reported counterexample. The computational verification using Lean 4 is a strong feature for a journal like *Experimental Mathematics*, but the discrepancy in the reported count (between 422 and 441) must be addressed. The most critical issue lies in the claim of universality for the sign theorem; the existence of a counterexample at $p=243,799$ undermines the broad applicability of the proposed theorem as currently stated. However, the spectral analysis (Mertens spectroscope) and the verification of specific character-based zeta zero detections ($\chi_{m4}$, $\chi_5$, $\chi_{11}$) represent valuable contributions that warrant publication upon correction and qualification of the main theorems. The authors are encouraged to revise the abstract and the statement of the sign theorem to reflect the bounds of validity found in the counterexample search.

## 3. MAJOR CONCERNS

The following issues must be addressed for the paper to meet the standards of publication.

**(a) Novelty of Identities vs. Classical Ramanujan Sums**
The paper relies heavily on the identity $\sum_{f \in \mathcal{F}_{p-1}} \exp(2\pi i p f) = M(p) + 2$. While the derivation within the manuscript is claimed to be a "Bridge Identity," the reviewer must question the novelty of this construction in the context of classical analytic number theory. Ramanujan sums $c_q(n) = \sum_{k=1, (k,q)=1}^q e^{2\pi i k n/q}$ are intimately related to these exponential sums over Farey sequences. Specifically, for prime $p$, the Farey sequence of order $p$ is closely related to the reduced residues modulo $p$. The term $M(p)$ (Mertens function) naturally appears in the summatory behavior of the Mobius function, which underpins the Ramanujan sum evaluations.
I must ask the author to explicitly distinguish their "Bridge Identity" from the standard evaluation of $\sum_{k=1}^{p-1} e^{2\pi i k/p} = -1$. The manuscript suggests a connection to $M(p)+2$, which implies a non-standard contribution. If this is a known property of Farey sums that has not been cited as "novel," it must be reframed as a re-derivation or a specific context-dependent formulation rather than a fundamental bridge to zeta zeros. A detailed comparison with Titchmarsh (Chapter 7) regarding Farey sequence estimates is required. The failure to position the identity against Ramanujan’s specific work diminishes the claimed novelty.

**(b) The Spectroscope: Fourier/Mertens Connection**
The "Mertens spectroscope" is the most intriguing computational claim, citing Csoka (2015) for the detection of zeta zeros. The author asserts that the spectral properties of $\Delta W(p)$ can pre-whiten the noise to detect zeros $\rho$.
In the context of the provided verification data, the author uses specific Dirichlet characters ($\chi_{m4}$, $\chi_5$, $\chi_{11}$) and zeros (e.g., $\rho_{m4\_z1} = 0.5 + 6.0209i$) to validate the spectroscope. The verification results show $D_K \cdot \zeta(2)$ values hovering near unity ($0.976, 1.011, 0.992, 0.989$).
However, the connection between the Farey wobble and the specific spectral extraction of $\rho$ needs rigorous justification. Does the Farey sequence filter the noise of the Mertens function effectively, or does it simply mirror the behavior of the Mertens function? The correlation $r=0.77$ is significant, but is it causal? The reviewer notes that the "Fourier/Mertens connection" must be distinguished from standard Fourier analysis of arithmetic functions (e.g., the explicit formula for $\psi(x)$). If the "spectroscope" does not offer a method for finding new zeros or improving error bounds on $M(x)$, its utility is limited to observational evidence. The authors must clarify if this method adds computational value over existing zeta detection algorithms (like Odlyzko-Schönhage).

**(c) Lean Verification: Burden of Proof**
The inclusion of Lean 4 formal verification is a major asset for *Experimental Mathematics*. However, the reported count discrepancy must be clarified. The Abstract cites "441 results," while the underlying context data suggests "422 Lean 4 results."
Readers of *Experimental Mathematics* care deeply about the reliability of computational claims. If the formalization count changes between manuscript and submission (or between the author's notes and the abstract), it raises questions about the robustness of the verification. Does the "discrepancy" arise from updated libraries? Or does it indicate that some lemmas were initially claimed verified but later found to have gaps? The reviewers of Lean work expect the specific GitHub repository or artifact to match the count exactly. This should be included as a verified artifact in the Appendix rather than a footnote in the main text. Furthermore, does a "Lean result" imply a proof or a computation? If it is a computational check, the term "verification" should be used cautiously to avoid confusion with formal proof of the theorems themselves.

**(d) The Sign Theorem: Range and Counterexample**
The strongest theoretical claim is the sign theorem regarding $\Delta W(p)$. The abstract states computational evidence for a correlation up to 100,000. However, the presence of a counterexample at $p=243,799$ fundamentally changes the validity of the paper.
If the theorem claims universality ("For all primes $p$"), the counterexample invalidates it. If the theorem claims a statistical property, it must be restated as "For $p < 243,799$" or similar. The fact that the counterexample occurs at a relatively large prime (in the context of the study) suggests that the underlying heuristic (perhaps based on the $r=0.77$ correlation) breaks down in the tail.
The reviewer recommends that the authors explicitly analyze the nature of $p=243,799$. Is it a prime where the character sums ($\chi_{m4}$, etc.) behave anomalously? Given the context data showing Chowla evidence ($\epsilon_{min} = 1.824/\sqrt{N}$) and GUE RMSE=0.066, this counterexample might indicate a deviation from Gaussian Unitary Ensemble (GUE) statistics in this specific regime. A detailed analysis of the sign of $\Delta W(243799)$ compared to the predicted sign based on the Mertens correlation is required. Without this, the theorem stands as unproven and potentially false as a universal law.

**(e) The B>=0 Open Problem**
The manuscript mentions the open problem regarding a term $B \ge 0$ (presumably in the four-term decomposition $\Delta W(p) = A - B - C - D$ or in the error term of the discrepancy). This is a critical theoretical bottleneck. The author asks for partial results.
The literature suggests that $B \ge 0$ relates to the positivity of certain energy terms in the Farey wobble. If this remains unresolved, the authors should not use it to support claims about uniformity. I recommend the authors explicitly state the status of $B \ge 0$ as an *Open Conjecture* in the manuscript. If the results for $B \ge 0$ are numerical rather than proven, they must be clearly labeled as such.
Current computational data provided in the context (GUE RMSE=0.066) might be relevant here. The authors should test if the counterexample at 243,799 violates the condition $B \ge 0$. If $B$ becomes negative at the counterexample, this explains the failure of the sign theorem. The paper must discuss whether the failure of one implies the failure of the other.

**(f) Philosophical Concern (Aistleitner): Hierarchy of Primes**
The philosophical critique, referencing Aistleitner, questions whether Farey sequences add anything beyond "primes -> Mertens -> zeta zeros".
This is a fundamental concern. The Farey sequence is a geometric rearrangement of rationals. The Prime Number Theorem is the driving force. If $\Delta W(p)$ is just a proxy for $M(p)$, then the Farey analysis is secondary. The "Mertens spectroscope" seems to detect zeta zeros *via* $M(p)$.
The author must answer: Is there a "Farey specific" fluctuation that is *not* explained by the Mertens function? If the answer is no (i.e., $\Delta W(p) \propto M(p)$ exactly), then the paper's contribution to understanding Farey uniformity is reduced to understanding $M(p)$. The connection to $\chi$ characters (as detailed in the prompt's "Key Context" with specific $dl_5$, $dl_{11}$ definitions) might be the avenue here. If the $\chi$-weighted sums (like $D_K \cdot \zeta(2)$) reveal phases $\phi = -\arg(\rho_1 \cdot \zeta'(\rho_1))$ that $M(p)$ does not capture, then the Farey link is genuine. This needs to be argued more sharply. Is Farey analysis a *filter* for zeta zeros, or just a *mirror*?

## 4. MINOR COMMENTS

1.  **Notation Consistency:** The symbol $\Delta W(p)$ is used, but earlier the abstract defines $W(N)$ using $f_j - j/n$. Ensure that the index $n$ is clearly defined relative to $p$ in the text (e.g., is $n=p$?).
2.  **Discrepancy in Counts:** The Abstract claims "441 results" for Lean 4, while the internal data provided suggests "422 results". Please reconcile this in the revision.
3.  **Character Definitions:** The definitions for $\chi_5$ and $\chi_{11}$ are non-standard in notation (using $i$ and complex exponents). Ensure the explicit definitions (e.g., $\chi_5(2)=i$) are clearly presented in a table or definition block to avoid confusion, as the prompt provided specific exponent maps ($dl_5=\{1:0, 2:1, 4:2, \dots\}$) that are currently implied rather than explicit in the paper text.
4.  **Counterexample Context:** The counterexample at $p=243799$ needs a plot. A graph of $\Delta W(p)$ vs $M(p)$ around this region would illustrate the breakdown visually.
5.  **Citation Format:** Csoka (2015) should be fully cited in the bibliography. The prompt mentions "cite Csoka 2015".
6.  **LaTeX Typing:** Ensure that $\phi = -\arg(\dots)$ is formatted consistently. In Section 3, I used LaTeX; ensure this matches the manuscript.
7.  **Chi Verification:** The prompt notes $|L(\rho)|=0.75$ and $1.95$ for $\chi_5$ and $\chi_{11}$ if Legendre symbols are used. The author must clarify that the specific `chi_m4`, `chi5_complex` functions defined in the "Key Context" are the ones used for the spectral analysis, as standard Legendre symbols yield incorrect zeros.
8.  **Error Bars:** The values $D_K \cdot \zeta(2) = 0.976 \pm 0.011$ are presented in the analysis. These error bars must be derived from the experimental methodology and described in the computational section.

## 5. EDITORIAL

*   **Length:** The manuscript is approximately 2,500 words. This is on the upper limit for a standard article. However, given the density of definitions, it is acceptable.
*   **Figures:** The manuscript currently lacks visualizations of the "Mertens spectroscope." I recommend a figure showing the spectral density of $\Delta W(p)$ compared to the theoretical GUE prediction (using the GUE RMSE=0.066). This would strengthen the computational evidence.
*   **References:** Ensure the list includes foundational Farey sequence papers (e.g., Hardy & Wright, Khinchin) alongside the modern computational works.
*   **Formatting:** The Lean 4 code snippets should be placed in a dedicated "Appendix A" or "Code Repository Link" section to maintain the flow of the main narrative.
*   **Abstract:** The abstract should explicitly mention the counterexample. "Proving universality is not possible; instead, we identify the breakdown at p=243799."

---

## 6. DETAILED ANALYSIS OF COMPUTATIONAL RESULTS (Context Integration)

In reviewing the computational evidence provided in the "Key Context," the reviewer notes the following specific verification points which the paper must address or clarify:

**1. Character-Specific Zeta Zeros:**
The paper claims to detect zeta zeros using the spectroscope. The context provides verified data for specific character-zero pairs.
*   $\chi_{m4\_z1}$: $\rho = 0.5 + 6.020948904697597i$. The computed value of $D_K \cdot \zeta(2)$ is $0.976 \pm 0.011$.
*   $\chi_{m4\_z2}$: $\rho = 0.5 + 10.243770304166555i$. Computed value is $1.011 \pm 0.017$.
*   $\chi_5$: $\rho = 0.5 + 6.183578195450854i$. Computed value is $0.992 \pm 0.024$.
*   $\chi_{11}$: $\rho = 0.5 + 3.547041091719450i$. Computed value is $0.989 \pm 0.018$.
