# What Our Discoveries Say About the Riemann Hypothesis

**Date:** 2026-03-30
**Purpose:** Honest assessment of what our per-step Farey discrepancy framework reveals (and does not reveal) about RH.

---

## 0. What We Actually Have

Before connecting to RH, let us be precise about what is established:

| Result | Status | What It Says |
|--------|--------|--------------|
| Sign Theorem: DeltaW(p) < 0 for M(p) <= -3 | Proved analytically for large p + computed for p <= 100K | Primes with sufficiently negative Mertens decrease Farey discrepancy |
| Spectral identity: L_1(N) = M(N) + 1 | Proved (classical) | First Fourier coefficient of Farey points on circle = Mertens function |
| Permutation square-sum: Sigma delta^2 = N^2/(2pi^2) + o(N^2) | Proved (elementary) | Per-step shift variance matches random permutation prediction |
| Four-term decomposition DeltaW = A - B - C - D | Proved (algebraic identity) | Per-step change has four interpretable components |
| B+C > 0 for all primes 11 <= p <= 200K | Computed, not proved | Cross-correlation plus shift always beats zero in range |
| C_W(N) = N * W(N) bounded near 0.67 | Computed to N = 100K; proved only C_W <= log N | The Franel L2 sum grows slowly |

The explicit formula for DeltaW involving zeta zeros, the pair correlation connection, and the triangular distribution for delta are **observed/conjectured structures**, not proved theorems in our framework. They come from combining our decomposition with classical explicit formulas (von Mangoldt, Guinand-Weil).

---

## A. Per-Step Behavior and the Total W(N): Does Knowing DeltaW Constrain W?

### The Classical Franel-Landau Equivalence

RH is equivalent to: W(N) = O(N^{-1+epsilon}) for every epsilon > 0.

Equivalently, in our notation: C_W(N) = N * W(N) = O(N^epsilon).

The strongest unconditional bound is C_W(N) = O(log N) from the Walfisz bound on M(N), and empirically C_W stays near 0.67.

### What Our Per-Step Results Add

We have W(N) = W(1) + sum_{k=2}^{N} DeltaW(k). Our Sign Theorem says DeltaW(p) < 0 when M(p) <= -3, meaning those primes INCREASE W (our convention: DeltaW = W(N-1) - W(N), so DeltaW < 0 means W goes up).

**The honest answer:** Knowing the sign of individual DeltaW(p) does NOT constrain the rate of growth of W(N). Here is why:

1. The Sign Theorem only covers primes with M(p) <= -3. Primes with M(p) > -3 (including the counterexample at p = 92,173 where DeltaW > 0) go the other direction. The BALANCE between positive-M and negative-M primes determines the cumulative behavior.

2. Composites contribute the overwhelming majority of steps (they heal -- 96% decrease discrepancy). The prime contributions are perturbations on a composite-dominated trend.

3. W(N) is a telescoping sum. Even with perfect sign control at primes, the MAGNITUDES matter for the growth rate. RH is about the growth rate of the cumulative sum, not the sign of individual terms.

**What would help:** If we could prove |DeltaW(p)| <= C * p^{-3/2+epsilon} (a bound on magnitude, not just sign), that would constrain the cumulative sum. But our current results give no such bound -- magnitude control requires bounding B_raw, which involves the very Mertens/zeta-zero structure that RH governs.

### Verdict on Question A

**The per-step sign information is orthogonal to the RH growth rate question.** Knowing that negative-M primes increase W tells us about the local dynamics but not the global trajectory. The cumulative W(N) depends on cancellations between all steps (prime and composite, positive and negative M), and controlling these cancellations IS the Riemann Hypothesis. We have not circumvented this.

---

## B. The Spectral Formula K_hat = (p/pi^2)|L(1,chi)|^2 and Zeros of L-functions

### What This Formula Says

The Fourier transform of the Farey "kernel" (the per-denominator contribution to delta^2) at character chi is proportional to |L(1,chi)|^2. This is a restatement of the classical identity connecting Farey fractions to L-values.

### Could We Detect Zeros of L(1,chi)?

For Dirichlet L-functions with real characters (Kronecker symbols), L(1,chi) > 0 by Dirichlet's class number formula -- there ARE no zeros at s=1 for real characters. For complex characters, L(1,chi) is nonzero by the same theorem (extended). So L(1,chi) = 0 is impossible, and this is a classical theorem, not something our framework discovers.

**However**, the formula does encode L-VALUES. If |L(1,chi)|^2 is unusually small for some character chi, the corresponding Fourier mode of the Farey kernel is suppressed. This happens when chi corresponds to a quadratic field with large class number (Siegel zeros territory). A hypothetical Siegel zero (L(sigma,chi) = 0 with sigma close to 1) would make |L(1,chi)| very small, which WOULD be visible in the Farey spectral data as an anomalously weak mode.

### Could We Detect This?

In principle, scanning the Farey kernel spectrum for anomalously weak modes at specific characters could flag potential near-zeros of L(1,chi). But:

1. Siegel's theorem already guarantees L(1,chi) > c(epsilon) * q^{-epsilon} for conductor q. The smallness is bounded.
2. Computing the Farey kernel to the precision needed to detect Siegel-zero-scale suppression would require working with conductors q where we already know L(1,chi) directly.
3. This is a REFORMULATION of the Siegel zero problem, not a new attack on it.

### Verdict on Question B

**The spectral formula encodes L(1,chi) values faithfully, but provides no new leverage on Siegel zeros or the nonvanishing of L-functions.** The information is already present in the L-functions themselves; the Farey representation is a different packaging of the same data.

---

## C. The Explicit Formula and RH: Simplification Under Re(rho) = 1/2?

### The Structure

The classical explicit formula gives:

    M(x) = sum_rho x^rho / (rho * zeta'(rho)) + corrections

Since DeltaW(p) is controlled by M(p) (our central finding N2), the per-step discrepancy change implicitly involves ALL zeta zeros through this sum.

More precisely, through the four-term decomposition, B_raw involves correlations of D(f) with delta(f), and D(f) can be expressed via the Moebius function and hence via zeta zeros.

### What RH Simplifies

Under RH, every rho has Re(rho) = 1/2, so x^rho = x^{1/2} * x^{i*gamma}. The bilinear form over zero pairs (rho, rho') that appears in the L2 discrepancy becomes:

    sum_{rho,rho'} c(rho,rho') * p^{(rho+rho')/2} * [phase factors]

Under RH, rho + rho' has real part 1 for all pairs, so p^{Re(rho+rho')/2} = p^{1/2} uniformly. The phase factors x^{i(gamma+gamma')/2} oscillate and create cancellation.

### Could a Zero Off the Line Be Detected?

If some rho_0 has Re(rho_0) = 1/2 + alpha with alpha > 0, then:

1. **In M(p):** The term p^{rho_0}/rho_0 contributes p^{1/2+alpha} * e^{i*gamma_0*log(p)}, which grows FASTER than the p^{1/2} contributions from on-line zeros. For large p, this term dominates.

2. **In DeltaW(p):** Since DeltaW is controlled by M(p), the anomalous zero would eventually produce anomalously large |DeltaW(p)| values at primes where the phase e^{i*gamma_0*log(p)} aligns constructively.

3. **The signature:** Primes p where gamma_0 * log(p) is near 0 (mod 2pi) would show DeltaW(p) anomalously negative (if the zero is in the upper half-plane). This would be a PERIODIC pattern in log(p) with period 2pi/gamma_0.

**But this is exactly what the classical zero-detection methods already do.** Detecting zeros of zeta via their effect on M(x) (or equivalently on pi(x) via Chebyshev psi) is the STANDARD approach. Our DeltaW adds nothing to this -- it is a filtered version of M(p) at prime arguments, which carries LESS information than M(x) at all integers.

### The Real Question: Does the Bilinear Form Simplify Usefully?

The bilinear form sum_{rho,rho'} K(rho,rho') over zero pairs could potentially be diagonalized or bounded under RH. Specifically:

- Under RH: K(rho,rho') = f(gamma-gamma') for some kernel f (since Re(rho) = Re(rho') = 1/2).
- Off RH: K(rho,rho') depends on both Re(rho)-Re(rho') AND gamma-gamma', breaking the translation invariance.

So RH gives TRANSLATION INVARIANCE in the imaginary parts. This is precisely the Montgomery pair correlation setting. But exploiting this requires understanding the distribution of gamma-gamma' differences, which is Montgomery's conjecture territory.

### Verdict on Question C

**Under RH, the bilinear form over zero pairs becomes translation-invariant in imaginary parts, which is a genuine structural simplification. A zero off the line would break this symmetry. But detecting such a break through DeltaW is strictly HARDER than detecting it through M(x) directly, because DeltaW is a lossy derivative of M at prime arguments only. The explicit formula connection is real but does not give our framework any advantage over classical methods.**

---

## D. Pair Correlation and Montgomery's Conjecture

### The Connection

Our W_tilde(s) = sum_p DeltaW(p) * p^{-s} is a Dirichlet series whose analytic properties encode the statistics of DeltaW. If this series has poles at s = 1 + i(gamma - gamma'), that would connect Farey discrepancy statistics to the pair correlation of zeta zeros.

### What Montgomery's Conjecture Says

Montgomery (1973) conjectured that the pair correlation of normalized zero spacings follows R_2(alpha) = 1 - (sin(pi*alpha)/(pi*alpha))^2 for 0 < alpha < 1 (proved) and for all alpha (conjectured). This matches the GUE (Gaussian Unitary Ensemble) prediction from random matrix theory.

### If Proved Through Farey Statistics

This is deeply speculative, but suppose one could:
1. Compute the pair correlation of the poles of W_tilde(s)
2. Show it matches the GUE form
3. Relate this to the pair correlation of zeta zeros

What would this imply for RH?

**Almost nothing directly.** Montgomery's pair correlation conjecture is INDEPENDENT of RH in the logical sense. Montgomery proved the correlation for 0 < alpha < 1 assuming RH, but the conjecture for all alpha is additional. Moreover:

- Pair correlation is a STATISTICAL property of zeros. It says how zeros are DISTRIBUTED relative to each other.
- RH is a POINTWISE property of zeros. It says where each zero IS.
- GUE statistics are consistent with RH but do not imply it. Random matrices have all eigenvalues on the critical line (by definition of the GUE), but proving real zeta zeros obey GUE statistics does not force them onto Re(s) = 1/2.

### The Deeper Issue

The pair correlation approach would at best show that zeta zeros BEHAVE AS IF they were on the critical line (in a statistical sense). This is evidence for RH but not a proof. It is analogous to how the observed distribution of prime gaps matches random models -- this is strong evidence for the Hardy-Littlewood conjectures but does not prove them.

### What About Our Specific Data?

Our pink noise investigation (experiments/pink_noise_findings.md) found:
- DeltaW spectral slope: f^{-1.67} (between pink and brown noise)
- ACF does NOT match Montgomery's pair correlation form
- No discrete peaks at individual zeta zero frequencies
- The signal is a superposition of ALL zeros, consistent with the explicit formula

**This means our DeltaW data does NOT reproduce Montgomery's pair correlation.** The Farey per-step signal is too "averaged" to resolve individual zero pairs.

### Verdict on Question D

**Even in the most optimistic scenario (proving Montgomery via Farey statistics), the implication for RH would be indirect and statistical, not a logical implication. Our actual data shows DeltaW does NOT resolve pair correlations -- the signal is a broadband superposition of all zeros. This direction is a dead end for RH.**

---

## E. The "Primes Are Random" Result and RH

### What We Proved

Sigma delta^2 = N^2/(2pi^2) + o(N^2), meaning the total squared shift when inserting p new fractions matches what a random permutation of residues would produce.

### The Error Term and RH

Write Sigma delta^2 = N^2/(2pi^2) + E(N). What does E(N) encode?

The error E(N) comes from the NON-randomness of multiplication-by-p acting on residue classes. Specifically, it arises from the deviation of the actual residue distribution from the uniform permutation model. This deviation is controlled by:

1. **Character sums:** For each denominator b, the squared shift involves sum_{a coprime b} (a - pa mod b)^2 / b^2. The deviation from the random expectation involves Ramanujan sums and ultimately Dirichlet characters.

2. **RH connection:** Under RH, the error in prime-counting functions (and hence in the distribution of residues) is O(x^{1/2+epsilon}). For our sum over denominators b <= N = p-1, this would give E(N) = O(N^{3/2+epsilon}).

3. **Unconditional bound:** Without RH, the best bound is E(N) = O(N^2 / exp(c * (log N)^{3/5} / (log log N)^{1/5})), which is o(N^2) but barely.

### Is The Error Term Detectable?

The ratio E(N)/N^2 measures the departure from random-permutation behavior. Under RH, this should be O(N^{-1/2+epsilon}). Without RH, it decays like 1/exp(c*(log N)^{3/5}...) -- much slower.

**In principle:** If we could compute E(N)/N^2 to sufficient precision and show it decays faster than any polynomial of 1/log(N), that would be evidence for (but not proof of) RH. But:

1. Computing Sigma delta^2 to the needed precision requires exact arithmetic over all denominators b <= N, which scales as O(N^2/log N) operations.
2. The signal-to-noise ratio is terrible: E(N) is swamped by the N^2/(2pi^2) main term.
3. This is equivalent to studying the distribution of residues pa mod b across all b, which IS the study of prime residue distribution -- i.e., the same problem RH addresses.

### Verdict on Question E

**The error term E(N) in Sigma delta^2 does encode RH information, in the same way that every error term in prime number theory does. The random-permutation main term is the "expected" behavior; the deviation from it is controlled by zeta zeros. But measuring this deviation through our framework is neither easier nor more informative than measuring it through classical means (explicit formulas for psi(x), pi(x), or M(x)). The "primes are random" result confirms a known heuristic; its error term is a repackaging of the RH question, not a new angle on it.**

---

## F. The Minimal New Result Needed

### What Would Make Our Framework RH-Relevant?

After honest assessment, here are the possible bridges from our work to RH, ranked by plausibility:

### F1. An Unconditional Sign Theorem for ALL Primes (Not Just M(p) <= -3)

**What:** Prove DeltaW(p) < 0 for all primes p >= P_0 (with no condition on M(p)).

**Why it matters:** The counterexample at p = 92,173 (M(p) > 0, DeltaW > 0) shows this is FALSE as stated. But a weaker version -- DeltaW(p) < 0 for "most" primes in a density sense -- combined with magnitude bounds could give:

    W(N) = W(1) + sum DeltaW(k) <= C * (some rate)

If this rate were O(N^{-1+epsilon}), we would have an RH equivalence.

**Gap:** The magnitude of DeltaW(p) when it IS positive is uncontrolled. And the counterexamples exist.

**Plausibility: LOW.** The counterexamples at positive M(p) are genuine, not artifacts. An unconditional sign theorem for all primes is false.

### F2. An L2 Bound on DeltaW Magnitudes

**What:** Prove sum_{p <= N} DeltaW(p)^2 = O(f(N)) for some explicit f.

**Why it matters:** This would bound the mean squared per-step change, which via telescoping bounds W(N). Specifically, if sum DeltaW(p)^2 = O(N^{-1+epsilon}), we could argue W(N) decreases fast enough to satisfy the Franel-Landau criterion.

**Gap:** DeltaW(p) involves B_raw, which involves M(p), so bounding sum DeltaW(p)^2 requires bounding sum M(p)^2 / p^4 (roughly), which is a known sum related to the mean-square of M(x). The mean-square of M(x) is:

    (1/X) integral_1^X M(x)^2 dx ~ c * X / (zeta zero structure)

This is a deep result (Titchmarsh, Ng 2004) that is itself RH-sensitive.

**Plausibility: VERY LOW.** Bounding sum DeltaW(p)^2 is as hard as bounding the mean square of M(x), which is an RH-adjacent problem.

### F3. A New Monotone Functional of Farey Sequences

**What:** Find a quantity Q(N) that is STRICTLY MONOTONE at every step (not just at primes with M(p) <= -3) and whose rate of growth/decay encodes RH.

**Why it matters:** Monotonicity eliminates the cancellation problem. If Q(N) is strictly increasing and we can bound its rate, we get one-sided information.

**Current candidates:**
- Fisher information sum 1/g^2 (proved monotone, but rate is unclear)
- Voronoi entropy (conjectured monotone, not proved, and entropy rate does not obviously connect to RH)
- C_W(N) = N * W(N) (NOT monotone)

**Gap:** None of our known monotone quantities have established connections to zeta zeros. The Fisher information grows because every insertion adds a new small gap, but the growth rate reflects the gap structure, not the zero structure.

**Plausibility: MODERATE but speculative.** This is the most genuinely novel direction -- finding a Farey monotone functional whose rate is RH-sensitive. But we have no concrete candidate.

### F4. Proving C_W(N) = O(1)

**What:** Prove that N * W(N) is bounded by an absolute constant.

**Why it matters:** This is WEAKER than RH (which gives N * W(N) = O(N^epsilon)) but STRONGER than what is currently proved (C_W <= log N). It would be a genuine advance in unconditional number theory.

**Connection to our work:** Our per-step framework gives W(N) as a telescoping sum. If we could show that the positive steps (DeltaW < 0, W increases) are on average cancelled by the negative steps (composites healing), and the net effect is bounded, we would get C_W = O(1).

**Gap:** The cancellation between prime damage and composite healing is precisely the arithmetic that encodes zeta zeros. We know 96% of composites heal, and our Sign Theorem covers M(p) <= -3 primes. But the positive-M primes and the MAGNITUDES are uncontrolled.

**Plausibility: LOW-MODERATE.** This is a meaningful intermediate goal between what we have and RH. It is likely true (C_W appears to converge to about 0.67) but proving it seems to require understanding the prime-composite balance at a level that current methods do not reach.

### F5. Connecting the R-Cancellation (N13) to Zeta Zero Structure

**What:** Our discovery N13 shows |R| = |sum D*delta / sum delta^2| uses only 10% of its Cauchy-Schwarz budget, and the actual R is below ALL random permutation trials. Formalizing WHY multiplication-by-p creates more cancellation than random would require understanding the arithmetic of residues at a deep level.

**Why it matters:** If the reason is traceable to the distribution of zeta zeros (through the explicit formula for M(p)), this would be a genuine new perspective.

**Gap:** The cancellation comes in two stages (within-denominator 63%, cross-denominator 30%). The within-denominator part is a Weyl-sum phenomenon (smooth function paired against scrambled permutation). The cross-denominator part involves Moebius cancellation. Both are controlled by the SAME zero structure that RH addresses.

**Plausibility: LOW.** The R-cancellation is a beautiful observation, but explaining it rigorously requires the very zeta-zero control that we are trying to derive from it.

---

## G. Summary: What Connects and What Does Not

### What Genuinely Connects

1. **The Franel-Landau framework:** Our W(N) IS the L2 Farey discrepancy, and bounding it IS equivalent to RH. This is not our discovery -- it is Franel (1924) and Landau (1924).

2. **M(p) controls DeltaW(p):** This is our genuine contribution (N2). It says the Mertens function, which encodes ALL zeta zeros through the explicit formula, governs the per-step discrepancy change. This is a new PERSPECTIVE on the Franel-Landau sum, decomposing it into per-step contributions.

3. **The spectral identity L_1 = M(N) + 1:** This connects the Fourier structure of Farey points to the Mertens function, confirming that spectral and arithmetic views are equivalent.

### What Does NOT Connect (Despite Appearances)

1. **The Sign Theorem does not constrain W(N) growth.** Sign information without magnitude bounds does not help with the cumulative sum.

2. **The pair correlation "connection" is not realized in our data.** DeltaW is too coarse to resolve individual zero pairs.

3. **The spectral formula K_hat = (p/pi^2)|L(1,chi)|^2 is a repackaging.** It encodes L-values faithfully but provides no new computational or theoretical leverage.

4. **The random-permutation match is expected.** The main term of sum delta^2 follows from equidistribution; the error term is controlled by the same zeta-zero structure as all prime distribution questions.

### The Honest Bottom Line

Our framework provides a NEW DECOMPOSITION of a KNOWN RH-equivalent quantity (the Franel L2 sum) into per-step contributions controlled by the Mertens function. This decomposition is mathematically valid, computationally revealing, and produces genuine theorems (Sign Theorem, Bypass Theorem, N11 identity). But it does not provide a new ROUTE to RH because:

1. **Every path from DeltaW back to W(N) requires magnitude control, which requires understanding zeta zeros.** The per-step view gives local information; RH is a global statement.

2. **The Mertens function that controls DeltaW is itself an explicit sum over zeta zeros.** So our central connection M(p) -> DeltaW(p) is, at its core, the statement that zeta zeros -> Farey discrepancy. This is the Franel-Landau theorem, which has been known for a century.

3. **No unconditional bound we have proved goes beyond what Franel-Landau + PNT already gives.** Our analytical proofs use PNT (for Mertens bounds) and elementary estimates. The per-step packaging is new; the final bounds are not.

### What Our Work IS Good For

- **A new perspective** on Farey equidistribution: the prime/composite damage/healing dichotomy
- **Publishable theorems** (Sign Theorem for M(p) <= -3, Bypass Theorem, permutation identity N11)
- **Computational evidence** for the extraordinary regularity of Farey sequences
- **A pedagogical bridge** between multiplicative number theory (Moebius, Mertens) and equidistribution (Farey, discrepancy)
- **Motivation for proving C_W = O(1)**, which is an interesting open problem in its own right

It is NOT a new approach to RH. Claiming otherwise would be overselling.

---

## H. If We Had to Write One Sentence for a Paper

"The per-step Farey discrepancy DeltaW(p), which we prove is negative for all primes with M(p) <= -3, provides a new dynamical decomposition of the Franel-Landau L2 sum into arithmetically interpretable components, but does not yield unconditional bounds beyond those obtainable from the prime number theorem."

This is honest, publishable, and correctly scoped.
