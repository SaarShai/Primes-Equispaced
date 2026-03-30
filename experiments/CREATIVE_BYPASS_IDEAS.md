# Creative Bypass Ideas: Proving the Sign Theorem Without Sigma E^2 >= c*p^2*log(p)

## Date: 2026-03-29
## Status: Assessment of 8 alternative proof strategies

---

## Background

**Sign Theorem (target):** For every prime p >= 11, Delta W(p) < 0.

**Current approach:** Four-term decomposition Delta W = A' - B' - C' + 1 - D'. For M(p) <= -3 primes, B' >= 0, so we need C' + D' > A' + 1. This reduces to showing D' ~ A' (near-cancellation) and C' = Sigma delta^2 is large enough to absorb the deficit. The sticking point is making the C' lower bound rigorous for ALL primes, including those with large positive M(p) where B' + C' can be negative (R(p) < -1/2 observed at p=1399, 1409, 1423).

**Key obstacle:** The decomposition approach splits naturally into M(p) <= -3 (where it nearly works) and M(p) > -3 (where B+C can be negative, requiring a fundamentally different argument). A unified proof would be more satisfying.

**Question:** Can we find a COMPLETELY DIFFERENT proof strategy that avoids the Sigma E^2 lower bound entirely?

---

## Idea 1: Direct Monotonicity of W(N)

### Approach
W(p) = (1/n') Sigma D^2_{F_p}. Show W(p) < W(p-1) directly by analyzing how inserting p-1 new fractions (those with denominator p) changes the displacement function.

When we go from F_{p-1} to F_p:
- n' = n + (p-1) new fractions
- Each old fraction f has displacement D'(f) = D(f) + delta(f) where delta accounts for the shift in rank
- Each new fraction k/p has a new displacement D_new(k/p)

Delta W = W(p) - W(p-1) = [Sigma D'^2 + Sigma D_new^2]/n' - Sigma D^2/n

### Key Lemma Needed
Show that the dilution effect (dividing by n' > n) outweighs the contribution from new fractions and cross-terms.

### Feasibility: 2/5

**Pros:**
- Conceptually clean: directly tracks what happens during insertion
- The dilution factor n'/n = 1 + (p-1)/n ~ 1 + pi^2/(3p) provides a "discount"
- This is essentially the four-term decomposition rephrased, so it inherits all partial results

**Cons:**
- This IS the current approach, just restated. The four-term decomposition is exactly this direct analysis.
- The same difficulties re-emerge: bounding cross-terms B', showing D' ~ A', etc.
- No genuine bypass of the Sigma E^2 issue

**Verdict:** Not a new strategy. The four-term decomposition already IS the direct monotonicity analysis. Rephrasing it does not help.

---

## Idea 2: Combinatorial Gap Structure

### Approach
F_p has p-1 more fractions than F_{p-1}. Each new fraction k/p sits in a specific Farey gap between consecutive fractions a/b and c/d (where b+d > p-1 but b, d < p). The displacement change at each old fraction depends on how many new fractions land to its left.

Define delta(f) = (number of new fractions k/p with k/p < f). Then the rank shift of f is exactly delta(f), and the new displacement is D'(f) = D(f) + delta(f) - n'*f + n*f = D(f) + delta(f) - (p-1)*f.

### Key Lemma Needed
Show that Sum_{f in F_{p-1}} [2*D(f)*(delta(f) - (p-1)*f) + (delta(f) - (p-1)*f)^2] + Sum_{new} D_new^2 can be controlled through the gap structure.

The gap structure is well-understood: consecutive Farey fractions a/b, c/d satisfy bc - ad = 1, and the new fraction inserted is (a+c)/(b+d) = mediant. For F_{p-1} -> F_p, the new fractions are exactly the k/p, and each sits in the unique gap where floor(bp/(some formula)) works out.

### Feasibility: 2/5

**Pros:**
- Rich combinatorial structure of Farey mediant insertion
- The mediant property bc - ad = 1 is powerful
- Gap sizes are well-controlled: max gap ~ 1/N, and the gap distribution is known (BCZ pair correlation)

**Cons:**
- Counting how many new k/p land to the left of each f requires understanding the distribution of {kp^{-1} mod 1}, which is the same multiplicative structure that makes the cross-term hard
- The gap-level analysis doesn't simplify the sum; it just reorganizes it
- The key difficulty (bounding sum of D*delta) remains, now expressed in terms of gap sizes

**Verdict:** The gap structure provides an alternative bookkeeping but doesn't avoid the fundamental difficulty. The combinatorial structure of mediant insertion doesn't directly control the cross-correlation between position-based (D) and arithmetic (delta) quantities.

---

## Idea 3: Entropy / Information Theory Bridge

### Approach
Fisher information I(N) = Sigma 1/g_j^2 is PROVED strictly increasing (via the gap-splitting lemma: 1/a^2 + 1/b^2 > 1/(a+b)^2). Shannon entropy H(N) = -Sigma g_j log(g_j) is also proved monotone increasing. Can we find a functional inequality connecting W(N) to I(N) or H(N)?

If there existed a function phi such that W(N) >= phi(I(N)) with phi increasing, then W would inherit monotonicity from I.

### Key Lemma Needed
An inequality of the form: W(N) >= f(I(N), n) where f is increasing in I.

Or: W(N) * I(N) is monotone (stronger, but not necessary).

### Analysis
W(N) = (1/n) Sigma (j - n*f_j)^2 relates to how the Farey fractions deviate from uniform spacing.
I(N) = Sigma 1/g_j^2 measures how far the gaps are from being equal.

By Cauchy-Schwarz: (Sigma 1)^2 <= (Sigma g_j^2)(Sigma 1/g_j^2), so n^2 <= L2 * I where L2 = Sigma g_j^2.

Also Sigma g_j = 1, so by Jensen: I(N) >= n^2 (since 1/x^2 is convex).

The L2 norm of gaps relates to W: Sigma g_j^2 = 1/n + (something involving W). More precisely, if f_j are the Farey fractions, gaps g_j = f_{j+1} - f_j, then Sigma g_j^2 measures non-uniformity of gaps. Meanwhile W measures non-uniformity of point positions relative to uniform. These are related but not identical measures.

### Feasibility: 2/5

**Pros:**
- I(N) monotonicity is cleanly proved (gap-splitting lemma is elegant)
- H(N) monotonicity is also proved
- If such a bridge existed, it would be a beautiful structural result

**Cons:**
- W and I measure different things. W cares about position deviations from rank/n; I cares about gap non-uniformity. These are correlated but not functionally linked by any known inequality.
- Empirically checked (monotone_functional.py): W(N)*I(N) is NOT monotone. W(N)/I(N) is NOT monotone. No simple combination phi(W,I) was found to be monotone.
- The gap-splitting trick works because it's purely local (each split contributes positively). W is a global quantity -- each insertion changes ALL displacements.
- There is no obvious convexity or variational principle connecting W to gap-based functionals.

**Verdict:** Elegant idea but almost certainly a dead end. The gap-splitting monotonicity of I is fundamentally local, while W is fundamentally global. No functional bridge is known or expected.

---

## Idea 4: Inductive Approach (Prove for ALL N, Not Just Primes)

### Approach
Instead of proving Delta W(p) < 0 only at primes, prove W(N+1) < W(N) for ALL N >= some threshold. Then the Sign Theorem for primes follows as a special case.

### Key Observation
When N+1 is composite, it adds FEWER new fractions (only phi(N+1) < N, since N+1 has a nontrivial factor). Fewer new fractions means the dilution effect A' is almost the same but the injection D' and cross-terms B', C' are smaller. So composite steps should be EASIER to prove.

### Key Lemma Needed
W(N+1) < W(N) for all N >= N_0, where N_0 is small enough to verify computationally.

### Analysis
The four-term decomposition generalizes: going from F_N to F_{N+1}, we add phi(N+1) new fractions (those k/(N+1) with gcd(k, N+1) = 1).

For N+1 = p (prime): phi(p) = p-1 fractions added. Maximum disruption.
For N+1 = p^2: phi(p^2) = p^2 - p fractions added, but p^2 is large so the ratio phi(p^2)/n is still ~pi^2/(3p^2) * (p^2-p) ~ pi^2/3 * (1 - 1/p), similar to prime case.
For N+1 = 2p: phi(2p) = p-1, same as for p but at a different N.

### Feasibility: 3/5

**Pros:**
- Composites add fewer fractions relative to |F_N|, so the "dilution beats injection" argument should be easier per step
- If proved for all N, the Sign Theorem follows trivially
- The inductive structure (W(N+1) < W(N) using information about W(N)) could leverage the known growth rate W(N) ~ log(N)/(2*pi^2*N)
- This shifts from a "pointwise at primes" statement to a "monotone in N" statement, which might connect better to asymptotic tools

**Cons:**
- The empirical evidence needs checking: IS W(N+1) < W(N) for ALL N? This is known for prime steps but I'm not certain about every composite step.
- Even if true, the same analytical difficulties arise for each step. The cross-term bounding problem doesn't vanish.
- The inductive hypothesis "W(N) <= f(N)" for some explicit f could help, but we'd need to know f precisely. The asymptotic W(N) ~ log(N)/(2*pi^2*N) gives a candidate, but making this effective requires the Nyman-Beurling theory which is conditional on RH.

**Critical check needed:** Verify computationally that W(N+1) < W(N) for ALL N in [10, 10000], not just prime N. If this FAILS for some composite N, the approach dies immediately.

**Verdict:** Worth investigating. The shift to "monotone for all N" is a genuine reframing. If W is indeed monotone decreasing for all N >= 10, this is actually a STRONGER result that should be stated as the main theorem. The proof challenge remains, but the inductive structure provides additional leverage.

---

## Idea 5: Coupling / Transport

### Approach
Construct an explicit measure-preserving (or measure-contracting) coupling between F_p and F_{p-1} that shows the L2 discrepancy decreases.

The Farey sequence F_N defines an empirical measure mu_N = (1/n) Sigma delta_{f_j}. The wobble W(N) is related to the L2 discrepancy of mu_N from the uniform measure.

Idea: define a transport map T: F_{p-1} -> F_p that maps each old fraction to a "nearby" fraction in the new sequence. Show that the transported measure is closer to uniform in L2.

### The Natural Coupling
The identity map embeds F_{p-1} into F_p (all old fractions are kept). The new fractions k/p provide the additional mass. Under this embedding:
- Old fractions shift in rank (displacement changes by delta)
- New fractions fill gaps

The displacement shift delta(f) = f - {pf} mod appropriate terms provides the coupling.

### Key Lemma Needed
Under the natural embedding, the L2 norm of the centered empirical process decreases:
||F_p - uniform||_2 < ||F_{p-1} - uniform||_2

### Feasibility: 2/5

**Pros:**
- Optimal transport / coupling arguments are powerful in probability
- The natural embedding (inclusion) provides an obvious coupling
- Transport theory gives inequalities like Wasserstein contraction

**Cons:**
- Tried already (see PROOF_STATUS: "Coupling approach - DEAD, found Dedekind connection but that's dead")
- The L2 discrepancy is not a Wasserstein distance, so optimal transport theory doesn't directly apply
- The coupling map (identity on old fractions + new k/p points) doesn't have a contraction property because the new points are NOT uniformly distributed -- they cluster near rationals with small denominator
- The Dedekind sum connection (delta ~ sawtooth function) was explored and the error term is as large as the main term

**Verdict:** Already explored and found dead. The natural coupling doesn't contract because the arithmetic structure of the new fractions (k/p for k = 1..p-1) introduces correlations that prevent clean contraction bounds.

---

## Idea 6: Variational / Convexity

### Approach
W(N) is a quadratic functional on the empirical Farey measure. Inserting new points changes the measure. If W has a convexity property (or concavity in the right variable), the insertion could be shown to decrease W using Jensen's inequality or a variational principle.

### Setup
Let mu_N = (1/|F_N|) Sigma delta_{f_j}. Define W(mu) = integral (F_mu(x) - x)^2 dx where F_mu is the CDF of mu.

Going from mu_{N-1} to mu_N, we add mass at new points. This is a convex combination:
mu_N = (n/(n+phi(N))) * mu_{N-1,shifted} + (phi(N)/(n+phi(N))) * nu_N

where nu_N is the empirical measure of the new fractions and mu_{N-1,shifted} accounts for the rank changes.

### Key Lemma Needed
W(alpha*mu + (1-alpha)*nu) <= alpha*W(mu) + (1-alpha)*W(nu) - (correction) < W(mu) when nu is "more uniform" than mu.

### Analysis
W(mu) = ||F_mu - id||_2^2 where F_mu is the CDF. This is a CONVEX functional in mu (it's a squared L2 norm of a linear function of mu). So:

W(alpha*mu + (1-alpha)*nu) <= alpha*W(mu) + (1-alpha)*W(nu)

This gives: W(mu_N) <= (n/n')*W(mu_{N-1,shifted}) + (phi(N)/n')*W(nu_N)

For this to give W(mu_N) < W(mu_{N-1}), we need:
(n/n')*W(shifted) + (phi(N)/n')*W(nu_N) < W(mu_{N-1})

The shifted version W(shifted) ~ W(mu_{N-1}) (small perturbation). The new measure nu_N (p-1 equally spaced points k/p) has W(nu_N) = D^2 discrepancy of the p-grid.

For the p-grid: W(nu_N) = (1/(p-1)) Sigma_{k=1}^{p-1} (k/(p-1) - k/p)^2 = (1/(p-1)) Sigma (k/[p(p-1)])^2 ~ 1/(3p^2). This is TINY compared to W(mu_{N-1}) ~ log(p)/(2*pi^2*p).

So: W(mu_N) <= (n/n')*W_old + (phi(N)/n')*W_new ~ (1 - phi/n')*W_old + tiny

The dilution factor 1 - phi/n' = n/n' ~ 1 - pi^2/(3p) means:
W(mu_N) <~ W_old * (1 - pi^2/(3p)) + O(1/p^2)

Since W_old ~ log(p)/p, the decrease is ~ log(p)*pi^2/(3p^2), which dominates the O(1/p^2) new contribution.

### WAIT -- This Might Actually Work!

The convexity of the L2 norm gives a clean bound. The key steps are:

1. W is convex in the measure (TRUE -- it's a squared norm of a linear map)
2. mu_N is a convex combination of (shifted old measure) and (new fractions measure)
3. W(new fractions) << W(old fractions) because the p-grid is nearly uniform
4. The convex combination decreases W

The subtlety is step 2: mu_N is NOT a simple convex combination of mu_{N-1} and nu_N because inserting new fractions CHANGES THE RANKS of old fractions. The CDF is affected at every point. So F_{mu_N}(x) is not a convex combination of F_{mu_{N-1}} and F_{nu_N} at each x.

Actually, it IS: F_{mu_N}(x) = (n/n')*F_{mu_{N-1}}(x) + (phi(N)/n')*F_{nu_N}(x).

This is because the fraction of points in F_N that are <= x equals (number of old points <= x + number of new points <= x)/(total). So:

F_{mu_N}(x) = (n * F_{mu_{N-1}}(x) + phi(N) * F_{nu_N}(x)) / n'

Then: F_{mu_N}(x) - x = (n/n')(F_{mu_{N-1}}(x) - x) + (phi(N)/n')(F_{nu_N}(x) - x)

Let h = F_{mu_{N-1}} - id and g = F_{nu_N} - id. Then:

F_{mu_N} - id = (n/n')*h + (phi/n')*g

W(N) = ||F_{mu_N} - id||_2^2 = (n/n')^2 ||h||^2 + 2*(n/n')*(phi/n')<h,g> + (phi/n')^2 ||g||^2

Since (n/n')^2 < n/n' (because n/n' < 1), we have:

W(N) = (n/n')^2 * W(N-1) + cross + (phi/n')^2 * W_new

And (n/n')^2 * W(N-1) < (n/n') * W(N-1) < W(N-1)

So: W(N) < W(N-1) iff (n/n')^2 * W(N-1) + cross + (phi/n')^2 * W_new < W(N-1)

i.e., cross + (phi/n')^2 * W_new < [1 - (n/n')^2] * W(N-1)

The RHS is ~ (2*phi/n') * W(N-1) ~ 2*pi^2/(3p) * log(p)/(2*pi^2*p) = log(p)/(3p^2).

The cross term 2*(n/n')*(phi/n')*<h,g> is the problematic part. This is exactly the B' cross-term in disguise!

So the variational approach reduces to bounding the cross-term <h,g>, which is the inner product between the centered CDF of the old Farey measure and the centered CDF of the p-grid. This is exactly the same difficulty as bounding B' = 2*Sigma D*delta.

### Feasibility: 3/5

**Pros:**
- The CDF decomposition F_{mu_N} = (n/n')*F_{mu_{N-1}} + (phi/n')*F_{nu_N} is EXACT and clean
- The squared norm gives a transparent decomposition
- The dilution term (n/n')^2 < 1 is automatic
- The new-fraction discrepancy W_new is extremely small (p-grid is nearly uniform)
- This gives the clearest possible framing of what needs to be proved

**Cons:**
- The cross-term <h,g> is the same beast as B'/2
- Convexity alone is insufficient because the cross-term can be negative (and for M(p) > 0, IS negative enough to threaten)
- This doesn't bypass the cross-term problem, it just reformulates it in L2 function space

**Verdict:** This is THE cleanest formulation of the problem, and worth writing up as the framework for a proof. But it does NOT bypass the cross-term bound. The insight is: the Sign Theorem is equivalent to showing that the L2 inner product between the Farey discrepancy function and the p-grid discrepancy function is not too negative. This is a nice reformulation but not a bypass.

**NEW INSIGHT:** The L2 inner product <h,g> where h = F_{mu_{N-1}} - id and g = F_{nu_N} - id can be analyzed via Fourier series. h has the expansion h(x) = Sigma_m a_m * e(mx) where the Fourier coefficients involve Ramanujan sums. g has the expansion g(x) = Sigma_m b_m * e(mx) where b_m = (1/p)*Sigma_{k=1}^{p-1} e(mk/p) - delta_{m=0}. These are geometric sums! b_m = -1/p if p|m, (p-1)/p - 1 = -1/p if p does not divide m. Wait, more carefully: the CDF of the p-grid at x is #{k: k/p <= x}/(p-1) ~ floor(px)/(p-1). Its Fourier coefficients are known. This connects to Idea 7 (spectral).

---

## Idea 7: Spectral / Bridge Identity Direct Approach

### Approach
Express W(p) - W(p-1) as a spectral sum involving Ramanujan sums and the modular sigma function, then show positivity using K-hat >= 0 from the bridge identity.

### Setup (from the bridge identity work)
The bridge identity connects:
Delta W(p) = (spectral terms involving Ramanujan sums c_q(p)) * (displacement Fourier coefficients)

The Ramanujan sum c_q(p) = mu(q/gcd(q,p)) * phi(q)/phi(q/gcd(q,p)).

For q coprime to p (which is most q when p is prime): c_q(p) = mu(q)*phi(q)/phi(q) = mu(q).

So the spectral sum becomes a Mobius-weighted sum of displacement Fourier coefficients. This is precisely the reformulation in BREAKTHROUGH_REFORMULATION.md:

B + C = -2 * Sigma R(x)*delta(x) = -2 * Sigma_d mu(d) * Sigma_m T(m)

### Key Insight from Bridge Identity
The kernel K(f,g) = Sigma_q c_q(f)*c_q(g)/phi(q)^2 has non-negative Fourier transform (K-hat >= 0). This means:

Sigma_{f,g} K(f,g) * alpha(f) * alpha(g) >= 0 for any sequence alpha.

If we can express B+C as such a quadratic form with the right alpha, positivity follows.

### Key Lemma Needed
Express B + C = Sigma_{f,g} K(f,g) * alpha(f) * alpha(g) for some explicit alpha related to delta.

### Analysis
B = 2*Sigma D*delta. D(f) = rank(f) - n*f. delta(f) = f - {pf}/p (approximately).

The bridge identity gives: Sigma D(a/q)*c_q(m)/phi(q) = (related to M(m)). So D has a spectral decomposition in terms of Ramanujan sums. But delta also has a spectral decomposition: delta is determined by the multiplication-by-p permutation on each residue class.

The inner product <D, delta> in the Ramanujan basis becomes:
<D, delta> = Sigma_q (D-hat_q * delta-hat_q) / phi(q)^2

If D-hat and delta-hat have opposite signs in most terms (orthogonality), the sum is small. This is the "D and delta live in orthogonal arithmetic worlds" observation from PROOF_STATUS.

### Feasibility: 3/5

**Pros:**
- K-hat >= 0 is a powerful positivity result
- The Ramanujan sum expansion is the natural basis for both D and delta
- The bridge identity already connects D's Fourier coefficients to Mertens-family sums
- delta's Fourier coefficients are clean (character sums related to multiplication by p)
- This approach directly uses the arithmetic structure rather than fighting it

**Cons:**
- Expressing B+C as a POSITIVE-DEFINITE quadratic form requires choosing the right alpha, which isn't obvious
- The Ramanujan expansion of D converges slowly (D has a "rough" component from small denominators)
- Even with K-hat >= 0, the quadratic form Sigma K*alpha*beta is NOT necessarily non-negative when alpha and beta are different sequences
- The spectral approach was assessed as "AMBITIOUS" in PROOF_STATUS and spectral methods generally give asymptotic/average results, not pointwise results (confirmed in MAYER_SPECTRAL_PROOF.md)

**Verdict:** The most mathematically natural approach, but also the hardest to make rigorous. The K-hat >= 0 positivity doesn't directly give B+C > 0 because B is a bilinear form <D, delta>, not a quadratic form <alpha, K*alpha>. Would need to find a way to "square" the problem -- e.g., show that (B+C)^2 is bounded below using spectral positivity. This is deep but not obviously feasible.

---

## Idea 8: Probabilistic / CLT

### Approach
Model Farey fractions as a random process. The CLT for Farey fractions (Boca-Cobeli-Zaharescu 2001) gives:

The pair correlation of Farey fractions converges to a specific limit distribution. The counting function A(k) = #{f in F_N: f <= k/p} satisfies a CLT-like limit theorem.

If E(k) = A(k) - nk/p has variance ~ c*p*log(p), then by concentration (Chebyshev or better), the sum Sigma E(k)^2 concentrates around its mean ~ c*p^2*log(p).

### Key Lemma Needed
A concentration inequality for Sigma E(k)^2 around its expected value under the BCZ pair correlation model.

### Analysis
The BCZ pair correlation result says: for generic test functions phi,
(1/n) Sigma_{consecutive (f,g)} phi(n*g) -> integral phi(t) * P(t) dt
where P(t) is the BCZ limiting density.

This gives information about GAP statistics. For counting statistics (how many Farey fractions fall in an interval), the variance of A(k) = #{f <= k/p} is related to the L2 discrepancy.

The key probabilistic insight: E(k) for different k are NOT independent, but they are WEAKLY correlated because the Farey fractions exhibit "short-range dependence" (BCZ pair correlation decays). This means:

Var(Sigma E(k)^2) << (E[Sigma E(k)^2])^2

So Sigma E(k)^2 concentrates around its mean. If we can compute the mean (which involves the pair correlation), we get the desired lower bound.

### Feasibility: 2/5

**Pros:**
- Leverages deep results (BCZ pair correlation) that encode the arithmetic structure
- Concentration inequalities are well-developed tools
- The variance / weak dependence structure of Farey statistics is partially understood
- This would give a "soft" proof that avoids explicit constant tracking

**Cons:**
- BCZ pair correlation is an ASYMPTOTIC result (N -> infinity). It doesn't give effective bounds for specific N.
- The CLT-type results for Farey fractions are for gap statistics, not directly for the counting function E(k) at prime grids k/p
- "Concentration around mean" requires computing the mean first, which is the Sigma E^2 lower bound we're trying to prove!
- The probabilistic model treats Farey fractions as "approximately random" but the very deviations from randomness (captured by Mobius/Mertens) are what control the sign. A probabilistic argument might wash out the sign information.
- The weakest link: BCZ is proved using the theory of horocycle flows on the modular surface, and making it effective would require Selberg's eigenvalue bounds -- this is conditional or at least very technical.

**Verdict:** Circular at its core. To use concentration, you need to know the mean of Sigma E^2, which IS the quantity we're trying to bound. The probabilistic perspective is valuable for intuition (explaining WHY Delta W < 0 with high probability) but not for a rigorous proof.

---

## Summary and Rankings

| # | Idea | Feasibility | Genuine Bypass? | Key Obstacle | Priority |
|---|------|------------|----------------|--------------|----------|
| 1 | Direct Monotonicity | 2/5 | NO | IS the current approach | LOW |
| 2 | Combinatorial Gaps | 2/5 | NO | Same cross-term problem | LOW |
| 3 | Entropy/Information | 2/5 | NO | No functional bridge | LOW |
| **4** | **Inductive (all N)** | **3/5** | **PARTIAL** | **Need to verify W monotone for composites** | **HIGH** |
| 5 | Coupling/Transport | 2/5 | NO | Already tried, dead | LOW |
| **6** | **Variational/Convexity** | **3/5** | **NO but cleanest formulation** | **Cross-term in L2 function space** | **MEDIUM** |
| **7** | **Spectral/Bridge** | **3/5** | **PARTIAL** | **Bilinear != quadratic form** | **MEDIUM** |
| 8 | Probabilistic/CLT | 2/5 | NO | Circular (need mean to concentrate) | LOW |

---

## Recommendation: Three Paths Forward

### Path A (Recommended): Inductive + Variational Combined
1. First, VERIFY computationally: is W(N+1) < W(N) for ALL N in [10, 50000]? If yes, this is the real theorem.
2. Use the variational (L2 CDF) formulation: W(N) = ||(n/n')h + (phi/n')g||^2 where h = old discrepancy, g = new fraction discrepancy.
3. The key is: ||(n/n')h + (phi/n')g||^2 = (n/n')^2 ||h||^2 + 2(n*phi/n'^2)<h,g> + (phi/n')^2 ||g||^2 < ||h||^2.
4. Sufficient condition: <h,g> < [(1-(n/n')^2)*||h||^2 - (phi/n')^2*||g||^2] / [2*n*phi/n'^2].
5. RHS ~ (2phi/n') * ||h||^2 / (2*n*phi/n'^2) = n' * ||h||^2 / n ~ ||h||^2 = W(N-1).
6. So we need <h,g> < W(N-1), i.e., the L2 inner product between old discrepancy and new-fraction discrepancy is less than the full L2 norm. This is MUCH weaker than bounding <h,g> tightly.
7. By Cauchy-Schwarz: |<h,g>| <= ||h|| * ||g||. Since ||g|| ~ 1/(p*sqrt(3)) and ||h|| ~ sqrt(log(p)/p), we get |<h,g>| <= sqrt(log(p))/(p*sqrt(3p)) which is MUCH less than W(N-1) ~ log(p)/p.
8. WAIT -- this might actually close the proof!

### Path A Critical Check
Let me be more careful. We have:
- h = F_{mu_{N-1}} - id, so ||h||^2 = integral_0^1 (F_{mu_{N-1}}(x) - x)^2 dx = W_{L2}(N-1).
- g = F_{nu_N} - id where nu_N is the empirical measure of the phi(N) new fractions.

Is ||g||^2 small? The new fractions for N = p are k/p for k = 1..p-1. Their CDF is F_{nu}(x) = #{k <= px}/(p-1) = floor(px)/(p-1). So g(x) = floor(px)/(p-1) - x. For x in [k/p, (k+1)/p): g(x) = k/(p-1) - x. At x = k/p: g = k/(p-1) - k/p = k/[p(p-1)]. So ||g||^2 ~ integral of (k/[p(p-1)])^2, summed over intervals of length 1/p. This gives ~ (1/p) * (1/p^2(p-1)^2) * Sigma k^2 ~ (1/p) * p^3/(3p^2(p-1)^2) ~ 1/(3p^2). Very small.

And |<h,g>| <= ||h|| * ||g|| ~ sqrt(W_{L2}) * 1/(p*sqrt(3)).

Now W_{L2}(N) = integral (F_N(x) - x)^2 dx. This is the INTEGRATED squared discrepancy, not our W(N) which is the DISCRETE sum (1/n)*Sigma D_j^2. They're related but different. Our W = (1/n)*Sigma (j - n*f_j)^2 = n * integral (F_n(x) - x)^2 dx (approximately, by Riemann sum). So W_{L2} ~ W/n ~ log(N)/(2*pi^2*N*n) ~ log(N)/(2*pi^2*N*(3N^2/pi^2)) ~ pi^2*log(N)/(6N^3). Hmm, this is getting small.

Actually, let me reconsider. The correct relationship: our W(N) = (1/n) Sigma D_j^2 where D_j = j - n*f_j. This is n times the L2 discrepancy of the empirical CDF evaluated at the sample points. The continuous L2 discrepancy is integral (F(x) - x)^2 dx which differs by interpolation effects. For our purposes, the key question is whether the Cauchy-Schwarz bound |<h,g>| is sufficient.

### Path B: Spectral Decomposition of <h,g>
Expand both h and g in Fourier series: h(x) = Sigma a_m e(mx), g(x) = Sigma b_m e(mx).
Then <h,g> = Sigma a_m * conj(b_m).
For the p-grid: b_m = (1/(p-1)) * Sigma_{k=1}^{p-1} e(mk/p) * (integration correction). The sum Sigma e(mk/p) = -1 if p does not divide m, and = p-1 if p|m. So the p-grid CDF has Fourier coefficients concentrated at multiples of p. Meanwhile, the Farey discrepancy h has Fourier coefficients a_m ~ c_m(N)/m where c_m involves Ramanujan sums. For m = multiple of p, these are special. The inner product <h,g> picks out the Fourier coefficients of h at multiples of p, weighted by 1/p. This might be tractable!

### Path C: Two-Class Proof
Accept two separate arguments:
1. For M(p) <= -3: use the bypass (C' > deficit + 1, nearly proved in UNCONDITIONAL_PROOF_SKETCH.md)
2. For M(p) > -3: use dilution dominance. When M(p) > -3, the prime is in a region where the Farey sequence is already close to equidistributed. Show that the dilution effect A' alone exceeds D' + B' + C'.

The advantage: argument 2 doesn't need B+C > 0 at all. It works directly with the four-term decomposition in the regime where the dilution benefit is large.

---

## Action Items

1. **VERIFY W(N+1) < W(N) for all N in [10, 50000]** -- critical test for Idea 4 / Path A
2. **Compute Path A Cauchy-Schwarz explicitly** -- check if |<h,g>| << W(N-1) with actual constants
3. **Investigate Path B spectral inner product** -- Fourier coefficients of Farey discrepancy at multiples of p
4. **Formalize Path C two-class proof** -- nearly complete for M(p) <= -3, needs the M(p) > -3 case

---

## Key Takeaway

Most "creative bypass" ideas reduce to the SAME cross-term bounding problem, just reformulated. The genuine new insight is the **variational/L2 CDF formulation** (Idea 6 / Path A), which shows that the Sign Theorem is equivalent to a Cauchy-Schwarz-type bound in L2 function space. This might be tractable because the p-grid discrepancy function g has very small L2 norm (~1/p), while the Farey discrepancy function h has larger norm (~sqrt(log(p)/p^3)), and their inner product is bounded by the product of norms. The question is whether this Cauchy-Schwarz bound, combined with the explicit dilution factor (n/n')^2 < 1, is TIGHT ENOUGH to close the proof.

The second genuinely new direction is **Path C (two-class proof)**: accept that M(p) <= -3 and M(p) > -3 require different arguments, and close each separately. This is less elegant but potentially achievable.
