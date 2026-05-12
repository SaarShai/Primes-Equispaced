1. **L2 "independent re-implementation" is mpmath-only; PARI/GP not installed.**
   (a) §X.2 table lists PARI/GP 2.15 and Arb/FLINT 3.x as the L2 stack, but §X.5.2 admits "PARI is not installed on the current host." The actual L2 cross-check is a second mpmath script using a different prime sieve and Hurwitz-zeta path — same library, same arbitrary-precision backend. This is L1-with-variants, not an independent second-language verification.
   (b) Either install PARI and run the check, or relabel the current L2 as "L1b" and reserve "L2" for the PARI/Arb lane once completed. The three-layer table must match what was actually executed.
   (c) **Fatal.**

2. **Lean tags PROVED-UP-TO-MATHLIB-PREREQ for Lemma X.3.1 and Theorem X.4.1 are prospective, not actual.**
   (a) Both Lean files are described as "*(to be added)*." No Lean declaration currently exists. Tagging a not-yet-written file as PROVED-UP-TO-MATHLIB-PREREQ implies the algebraic content is closed in Lean modulo named Mathlib gaps; in fact nothing has been compiled. A reasonable referee would expect the file to exist and `lake build` to pass (modulo the annotated prerequisites) before that tag is used.
   (b) Either write and compile the files before submission, or downgrade both to SCAFFOLD with a note that the Lean formalization is planned.
   (c) **Serious.**

3. **Hypothesis (AK) is presented as a direct specialization of Aoki–Koyama (1.4), but the specialization itself is not proved.**
   (a) The verbatim quote from Aoki–Koyama (1.4) involves a limit with $(\log x)^m$ and a $\sqrt{2}$ factor for $\chi^2=1, s=\tfrac12$. The paper specializes to simple $\rho \ne \tfrac12$ and drops the $\sqrt{2}$, obtaining $E_K \log K \to L'/e^\gamma$. The passage from the general formula to this specialization requires an argument (the $m=1$ case, the exclusion of the $\sqrt{2}$ branch, the identification of $e^\gamma$ with the Mertens constant in the Euler product). This argument is not given; the reader is told to "specialize" without proof.
   (b) Add a short lemma showing the specialization explicitly, or cite a worked-out corollary in Aoki–Koyama or a follow-up.
   (c) **Serious.**

4. **(SP-L) is stated as an open challenge but is silently used to reach (NDC).**
   (a) §X.4.4 composes (SP-L) with (AK) to derive (NDC). The composition is presented as a formal derivation, yet (SP-L) is explicitly open. The result (NDC) is tagged as conditional, but the *mechanism* of composition — what exactly fails when (SP-L) is false — is not spelled out. A referee cannot assess whether the conditional framing is tight or whether additional hidden hypotheses are needed.
   (b) Add a one-sentence statement: "If (SP-L) fails, the product $c_K E_K$ may not converge to $e^{-\gamma}$; the drift evidence of §X.5.2 is consistent with convergence but does not exclude slow divergence."
   (c) **Cosmetic.**

5. **The $D_K$ drift table (§X.5.2) conflates $|D_K|$ with $D_K$.**
   (a) The table reports "Mean $|D_K|\cdot\zeta(2)$" — the absolute value — not $D_K$ itself. Since $D_K$ is complex-valued, $|D_K|$ can converge to $e^{-\gamma}$ even if $\arg D_K$ drifts. The table does not report the argument or the real/imaginary parts separately. The claim that the drift "distinguishes $e^{-\gamma}$ from $\zeta(2)^{-1}$" is weaker than it appears: $|D_K|$ converging to a constant does not imply $D_K$ converges.
   (b) Report $D_K$ (complex) at both scales, or explicitly state that only the modulus is being tracked and that phase convergence is not claimed.
   (c) **Serious.**

6. **The EC NDC sweep is "demoted to diagnostic" but still occupies §X.5.6 and generates Question Q:EC-NDC.**
   (a) The section reports G3_FAIL, null-control gate failure at $\alpha=0.75$, and falsification of the sharp-cutoff form. Despite this, it retains a full subsection and an open question. A referee may reasonably ask: if the signal is falsified, why is it in the paper at all? The framing "diagnostic" is not standard; it reads as a way to keep a negative result in the narrative.
   (b) Either collapse §X.5.6 into a single paragraph in §X.7 (open challenges) or reframe it explicitly as a negative result with a clear statement of what was tested and what failed.
   (c) **Cosmetic.**

7. **The L3 adversarial layer is described as "independent generative models" but the models are co-authoring the paper.**
   (a) §X.2 states L3 models "have no co-authorship interest in the manuscript," yet the MiMo model is listed as producing the adversarial pass *and* is the system generating this very referee report. The Ollama models are run by one of the authors on local hardware. Independence requires that the auditor has no access to the authors' draft; in practice, the models are prompted with the draft text. This is internal review, not independent verification.
   (b) Remove the claim of independence or rephrase as "internal adversarial pass" without implying external independence.
   (c) **Cosmetic.**

8. **The replication scale ($1.3\times10^{13}$) and the analytic scale ($K\le10^7$) are correctly separated, but the prose risks conflation.**
   (a) §X.5 opens with a bold warning not to conflate the two scales, yet the section's abstract/intro (§X opening paragraph) lists "Phase-1 Dominance-of-$-1$ replication at $x=1.3\cdot10^{13}$" and "analytic identities verified at $K\le10^7$" in the same sentence as if they jointly support the paper's claims. A skimming reader could easily inherit the wrong impression.
   (b) Move the replication-scale summary to an appendix or a separate section, and keep §X focused on the analytic identities.
   (c) **Cosmetic.**

9. **Theorem X.4.1 claims unconditional status but relies on Akatsuka (2013) Lemma 2.1 for conditional convergence of $\sum_p \chi^2(p)/p^{2\rho}$ at $\operatorname{Re}(s)=1$.**
   (a) The convergence-regime table says $\tfrac12\log L(2\rho,\psi)$ is "conditional at $\operatorname{Re}(s)=1$; absolute at $\operatorname{Re}(s)>1$." Since $2\rho = 1+2i\tau$ lies exactly on $\operatorname{Re}(s)=1$, the convergence is conditional. The theorem header says "unconditional." These two statements are in tension: the identity is unconditional *given* that the conditional convergence is handled by Akatsuka, but Akatsuka's result itself may depend on hypotheses (e.g., non-vanishing on $\operatorname{Re}(s)=1$). The paper should state explicitly whether Akatsuka (2013) Lemma 2.1 is unconditional or GRH-conditional.
   (b) Add a sentence: "Akatsuka (2013) Lemma 2.1 is unconditional [or: conditional on ...]; therefore Theorem X.4.1 is unconditional [or: conditional on ...]."
   (c) **Serious.**

10. **The open-challenges list is internally consistent but omits the most immediate blocker.**
    (a) Q:Perron and Q:Z-simple correctly identify the analytic blockers for (SP-L). But the most immediate practical blocker — the missing PARI L2 verification — is not listed as an open challenge. A referee who reads §X.7 will think the only gaps are analytic; the computational gap (no second-language verification) is buried in a TODO.
    (b) Add a computational open challenge: "Complete the PARI/GP L2 verification at $K=10^7$ on all four Dirichlet pairs."
    (c) **Cosmetic.**
