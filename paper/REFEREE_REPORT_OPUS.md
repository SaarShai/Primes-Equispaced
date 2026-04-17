# Referee Report: "The Geometric Signature of Primes in Farey Sequences"

**Reviewer:** Hostile Referee (Opus 4.6)
**Date:** 2026-04-04
**Manuscript length:** ~2,345 lines LaTeX, ~25 pages estimated
**Venue assessment:** arXiv preprint / journal submission

---

## Overall Assessment

This paper introduces the per-step Farey discrepancy Delta W(N) = W(N-1) - W(N), studies its sign as a function of the Mertens function M(N), proves several exact identities connecting Farey exponential sums to the Mobius function, and proposes a "Farey spectroscope" that detects zeta zeros from discrepancy data. The paper contains genuine mathematical content (the Bridge Identity and its generalizations, the Injection Principle, the four-term decomposition) alongside extensive computational observations. The formal verification in Lean 4 is a significant strength.

However, the paper has serious structural and mathematical issues that must be addressed before journal submission. The central difficulty is a persistent conflation of computational observations with proved results, a "Sign Theorem" that is not actually a theorem, and a spectroscope whose theoretical justification is a heuristic dressed up in conjecture notation. I detail these below.

---

## 1. MATHEMATICAL CORRECTNESS

### 1.1 Bridge Identity (Theorem 3.1) -- CORRECT

The proof is sound. Decomposing by denominator, using c_b(p) = mu(b) for gcd(p,b)=1 (which holds since b < p), and summing gives 2 + sum_{b=2}^{p-1} mu(b) = 2 + M(p-1) - 1 = M(p) + 2, using M(p-1) = M(p) - mu(p) = M(p) + 1 (since mu(p) = -1). This is correct.

**Minor issue:** The step "M(p-1) = M(p) + 1" in the proof sketch uses mu(p) = -1, hence M(p) = M(p-1) + mu(p) = M(p-1) - 1, so M(p-1) = M(p) + 1. Correct, but the paper should note this uses the fact that p is prime (so mu(p) = -1), not just that M is being evaluated at consecutive integers.

### 1.2 Universal Farey Exponential Sum (Theorem 3.3) -- CORRECT with caveat

The proof sketch exchanges summation order via c_b(m) = sum_{d | gcd(b,m)} d mu(b/d). This is the standard Ramanujan sum identity and the exchange is valid for finite sums. The claim that d=1 terms give M(N)-1 and boundary gives 2, totaling M(N)+1, is correct.

**Caveat:** The paper says "verified computationally for all m <= 40 and N <= 30." This is a very small verification grid for a result claimed to hold universally. Since the proof is a sketch, a full proof should be provided or cited. The identity itself follows from completely standard manipulations of Ramanujan sums, so this is a matter of exposition rather than correctness.

### 1.3 Displacement--Cosine Identity (Theorem 3.4) -- INCOMPLETE PROOF

The "proof" says "Since cos(2 pi p f) is symmetric under f -> 1-f, apply Theorem 3.1." This is not a proof. The theorem states sum D(f) cos(2 pi p f) = -1 - M(p)/2. The Bridge Identity gives sum e^{2 pi i p f} = M(p) + 2, hence sum cos(2 pi p f) = M(p) + 2 (imaginary part vanishes by symmetry).

But D(f) cos(2 pi p f) is NOT the same as cos(2 pi p f). The displacement D(f) = j - n f is not constant. The "proof sketch" does not explain how D(f) enters the picture. There must be an intermediate identity -- perhaps using the pairing D(f) + D(1-f) = -1 and cos(2 pi p f) + cos(2 pi p(1-f)) = 2 cos(2 pi p f) (which is wrong for the interior) -- but the paper omits this entirely.

**This is a genuine gap.** The identity may well be true (it is computationally verified), but the proof as presented does not work.

### 1.4 Cross-Term Formula (Theorem 3.5) -- PROOF NEEDS MORE DETAIL

The proof invokes a "Master Involution Principle" that is never formally stated in the paper. The boundary computation D(0) delta(0)^2 + D(1) delta(1)^2 = 0 + (-1)(1) = -1 needs verification: D(0) = 0 - n*0 = 0 (correct since f_0 = 0 has rank 0), delta(0) = 0 - {p*0} = 0 (correct), so D(0) delta(0)^2 = 0. D(1) = (n-1) - n*1 = -1 (correct), delta(1) = 1 - {p} = 1 - 0 = 1 (correct since p is integer), so D(1) delta(1)^2 = -1. The boundary gives -1, and the "involution principle predicts -1/2 for this pair" -- this is unclear. What exactly is being paired?

**The proof is sketchy to the point of being uncheckable.** A referee for Mathematics of Computation would require a full proof.

### 1.5 Injection Principle (Theorem 5.1) -- CORRECT

The proof for interior gaps is clean: the interval (pa/b, pc/d) has length p/(bd), and since b+d >= p (adjacency condition), bd >= (b+d)^2/4 >= p^2/4... wait, that's not what the paper says. The paper says bd >= p-1 from b+d >= p with b,d >= 2. Actually, for b,d >= 2, b+d >= p implies bd >= p-1 only when b+d = p and {b,d} = {2, p-2}, giving bd = 2(p-2) = 2p-4 >= p-1 for p >= 3. For other cases bd is larger. So p/(bd) <= p/(p-1) < 2, hence at most one integer in the interval. Correct.

The boundary cases are handled correctly.

**However:** The paper claims b+d >= p follows from adjacency and b+d < p would allow the mediant to appear. This is correct -- the mediant (a+c)/(b+d) enters F_N when b+d <= N, and since the fractions are adjacent in F_{p-1}, the mediant is NOT in F_{p-1}, so b+d >= p. This is the correct argument but it deserves explicit statement.

### 1.6 Generalized Injection (Theorem 5.3) -- CORRECT

This is the standard mediant property of Farey sequences. The proof is correct and well-known.

### 1.7 Displacement-Shift Identity (Proposition 5.5) -- CORRECT with reservation

The computation D_{F_p}(f) = old rank + floor(pf) - n' * f = D_{F_{p-1}}(f) + floor(pf) - (p-1)f = D_{F_{p-1}}(f) + (f - {pf}) = D_{F_{p-1}}(f) + delta(f) is correct for interior fractions f != 1.

**Reservation:** The step "new rank of f = old rank + number of new fractions k/p less than f" is correct ONLY if no new fraction k/p equals any old fraction a/b. Since p is prime and b < p, gcd(k,p) = 1 for all k/p, and k/p = a/b would require bp = kb, impossible for b < p unless k/p is already in F_{p-1}. But k/p has denominator p which is not in F_{p-1}. So this is fine -- but the paper should note this.

### 1.8 Deficit Minimality (Theorem 6.1) -- PROOF NEEDS VERIFICATION

The reduction to Dedekind sums is stated without proof. The claim that D_q(r) >= D_q(2) is equivalent to s(r,q) <= s(2,q) needs justification. The proof sketch then uses Dedekind reciprocity for small r and antisymmetry for large r. The final reduction to 2(r-2)(r-(q+1)/2) <= 0 for 2 <= r <= (q-1)/2 is algebraically clean if the preceding steps are correct.

**Issue:** The proof relies on the "permutation bound" s(a,b) <= s(1,b), which is stated without reference. This bound is not standard -- Dedekind sums can be negative, and s(1,b) = (b-1)(b-2)/(12b) > 0 for b >= 3. The bound s(a,b) <= s(1,b) does NOT hold in general (for example, s(1,5) = 1/5, but Dedekind sums can be larger). This needs a reference or proof.

### 1.9 Spectral Positivity (Corollary 6.3) -- CORRECT for stated claims

The spectral factorization and the connection to L-functions via the functional equation are standard. The vanishing for even characters and positivity for odd characters follow from the factorization.

### 1.10 Total Shift-Squared Asymptotic (Theorem 6.4) -- CONDITIONAL, correctly flagged

The paper honestly flags that this result is conditional on a Kloosterman estimate. The main term N^2/(2 pi^2) comes from standard Euler product asymptotics. The fluctuation bound using Kloosterman sums is plausible but the constant is not made explicit. This is correctly labeled as requiring verification.

### 1.11 C_W(N) >= N/28 (Theorem 6.6) -- PROOF NEEDS TIGHTENING

The proof sketch uses n >= 0.3 N^2 from |F_N| = 3N^2/pi^2 + O(N log N). For N >= 10, 3*100/pi^2 ~ 30.4, so n ~ 30.4 + O(10*2.3) ~ 30.4 + 23 = 53.4, while 0.3 * 100 = 30. So n >= 0.3 N^2 needs the lower bound from the asymptotic to be tight, which it is for N >= 10 but only barely. The proof should provide an explicit verification for N in [10, C] for some C beyond which the asymptotic kicks in.

The chain of inequalities leading to C_W >= N/28 involves several approximate constants (0.05N, 0.01N^3, 0.36N^2) that need to be made rigorous. A referee would want explicit bounds, not "~" estimates in a proof.

### 1.12 The "Sign Theorem" (Observation 7.1) -- THIS IS NOT A THEOREM

This is the paper's most serious terminological issue. Observation 7.1 is labeled "Computational Sign Pattern" and states that for all primes 11 <= p <= 100,000 with M(p) <= -3, Delta W(p) < 0. The paper refers to this as the "Sign Theorem" throughout.

**This is a computational observation, not a theorem.** A theorem requires a proof. The paper even acknowledges (Remark 7.2) that the pattern FAILS at p = 243,799. Calling it a "Sign Theorem" in multiple places is misleading. It should be called "Sign Pattern" or "Sign Observation" throughout.

Moreover, the "proof" of Observation 7.1 (starting at line 1739) is simply: "Direct computation in C verifies..." followed by analytical ingredients that "support the geometry." This is not a proof. It is a computational verification for a finite range, combined with heuristic arguments for why the pattern should hold.

**The paper must not call this a theorem.** It is a computational observation for p <= 100,000 that is known to fail beyond that range.

---

## 2. OVERSTATEMENTS

### 2.1 "Novel object not previously studied"

The claim that Delta W(N) = W(N-1) - W(N) has "not previously been studied" (abstract, line 56) is a strong novelty claim. The per-step change of discrepancy measures is a natural object, and while I am not aware of a specific prior study, the claim should be softened to "appears not to have been studied" (which the body text does in places but the abstract does not).

### 2.2 "Both signs occur infinitely often (unconditional, via Ingham's theorem)"

The abstract (line 66) states this as unconditional. But the argument requires showing that the sign of Delta W(p) is determined by M(p)/sqrt(p) via the sigmoid relationship -- and the sigmoid is an empirical observation, not a proved result. If the sigmoid is assumed, then Ingham's theorem (which gives infinitely many sign changes of M) would indeed give infinitely many sign changes of Delta W. But the paper has not proved the sigmoid connection, so calling this "unconditional" is an overstatement.

**What IS unconditional:** That W(N) -> 0 and W(N) oscillates (so Delta W changes sign). But connecting this to specific prime behavior requires more.

### 2.3 "The density of negative steps tends to 1/2 under GRH+LI"

This claim (abstract, line 68) relies on the Rubinstein-Sarnak framework applied to the Mertens function. The connection is heuristic -- the paper has not proved that the density of negative Delta W(p) among primes equals the density of negative M(p) values. The sigmoid relationship is empirical and the Rubinstein-Sarnak framework applies to the Mertens function, not directly to Delta W(p).

### 2.4 "258 results across fifteen Lean 4 files"

While impressive, many of these 258 "results" appear to be definitions, lemmas of the form "mu(p) = -1", and computational verifications by native_decide. The count conflates trivial facts with substantial theorems. The paper should distinguish between definitions, computational verifications, and genuine proof contributions.

### 2.5 Magnitude scaling exponent

The claim that |Delta W(p)| scales as p^{-1.77} (line 701) is stated without error bars or confidence intervals. For an empirical power law fit over the range p <= 100,000, the uncertainty should be reported. The claim that the exponent "should approach -2 under RH" is a heuristic, not a proved implication.

### 2.6 "Composites account for 96% of positive-Delta W events"

The abstract says "composites account for 96% of positive-Delta W events" and then Section 4.1 gives tables only for p <= 200. The 96% figure needs clarification: is it for N <= 200, N <= 100,000, or all N? The paper switches between these ranges without flagging it.

### 2.7 Information compression remark

Remark 7.3 claims a "2,807:1 reduction at N=96" and "mutual information ~ 0.79 bits." These are interesting observations but "information compression" is a strong framing. The Bridge Identity is a mathematical identity, not a compression algorithm. The mutual information between M(p) and sgn(Delta W(p)) being 0.79 bits simply says these are highly correlated, which is the paper's main observation. Calling it "compression" adds nothing mathematically.

---

## 3. INTERNAL CONSISTENCY

### 3.1 Definition of Delta W

Delta W(N) = W(N-1) - W(N) is defined at equation (3) and used consistently thereafter. **Consistent.**

### 3.2 Definition of R(p)

R(p) is defined as "2 sum D delta / sum delta^2" in the abstract (line 69) and as "the correlation ratio" in Remark 7.5 (line 1781). The factor of 2 in the numerator is present in both definitions. **Consistent.**

However, the abstract says "R(p) = 2 sum D delta / sum delta^2" while the four-term decomposition has B = (2/n'^2) sum D delta and C = (1/n'^2) sum delta^2. So B + C = (1/n'^2)(2 sum D delta + sum delta^2) = (sum delta^2/n'^2)(1 + 2R) where R = sum D delta / (sum delta^2 / 2)... no, wait. Let me recheck.

From line 1780: "B + C = 2 sum D delta + sum delta^2 = sum delta^2 (1 + 2R) where R(p) = 2 sum D delta / sum delta^2." This gives B + C = sum delta^2 (1 + 2R) = sum delta^2 + 4 sum D delta * sum delta^2 / sum delta^2... no, that's B + C = sum delta^2 (1 + R') where R' = 2 sum D delta / sum delta^2 = R. So B + C = sum delta^2 (1 + R). Wait -- line 1780 says "B + C = sum delta^2 (1 + 2R)". With R = 2 sum D delta / sum delta^2, this gives B + C = sum delta^2 + 2 * 2 sum D delta = sum delta^2 + 4 sum D delta. But B = (2/n'^2) sum D delta and C = (1/n'^2) sum delta^2 give (unnormalized) B' + C' = 2 sum D delta + sum delta^2. So sum delta^2 (1 + 2R) = sum delta^2 (1 + 2 * 2 sum D delta / sum delta^2) = sum delta^2 + 4 sum D delta != 2 sum D delta + sum delta^2.

**INCONSISTENCY FOUND.** If R = 2 sum D delta / sum delta^2, then sum delta^2 (1 + R) = sum delta^2 + 2 sum D delta = C' + B' (unnormalized). But the paper writes B + C = sum delta^2 (1 + 2R), which gives sum delta^2 + 4 sum D delta. This is wrong unless R = sum D delta / sum delta^2 (without the factor of 2).

Let me recheck: from line 69, R(p) = 2 sum D delta / sum delta^2. From line 1780-1781: "B + C = 2 sum D delta + sum delta^2 = sum delta^2 (1 + 2R)". Substituting R: sum delta^2 (1 + 2 * 2 sum D delta / sum delta^2) = sum delta^2 + 4 sum D delta. But B + C = 2 sum D delta + sum delta^2. These are equal only if 4 sum D delta = 2 sum D delta, i.e., sum D delta = 0.

**This is a real error.** Either R is defined with or without the factor of 2, but the two uses are inconsistent. If R = sum D delta / sum delta^2 (no factor of 2), then B + C = sum delta^2 (1 + 2R) works. If R = 2 sum D delta / sum delta^2 (with factor of 2 as in the abstract), then B + C = sum delta^2 (1 + R). The paper uses both conventions.

Looking more carefully: the abstract says "R(p) = 2 sum D delta / sum delta^2" but this may be a notational condensation of the cross-term ratio. Then Remark 7.5 defines R(p) = 2 sum D delta / sum delta^2 AND says B + C = sum delta^2 (1 + 2R). This is algebraically incorrect as shown above.

**Most likely:** The correct definition is R = sum D delta / sum delta^2, the factor of 2 in the abstract is an error, and line 1781 should read R(p) = sum D delta / sum delta^2. Then B + C = 2 sum D delta + sum delta^2 = sum delta^2 (1 + 2R). This is consistent.

**Resolution needed:** Fix the abstract definition of R(p) to remove the factor of 2, OR fix line 1781 to read B + C = sum delta^2 (1 + R).

### 3.3 Prime counts

- Abstract: "4,617 qualifying primes p <= 100,000" -- this is the count of primes with M(p) <= -3 up to 100,000.
- Observation 7.1 (line 1650): "4,617" -- consistent.
- Abstract: "3,829 qualifying primes" for the spectroscope -- this is a different count (primes with M(p) <= -3 up to p = 83,773). Consistent with Definition 8.1 using a different upper bound.
- Table in Section 4.1: "9,588" primes p >= 11 up to 100,000. This is the total count of primes >= 11 up to 100,000, which is pi(100000) - 4 = 9592 - 4 = 9588. **Consistent.**

### 3.4 R minimum value

Abstract says "minimum R = 0.0068 at p = 64,781." Remark 7.5 says "minimum R = 0.0068 at p = 64,781." **Consistent.**

### 3.5 Observation vs. Theorem numbering

Observation 7.1 is referred to as "thm:sign" in the LaTeX (line 1649). The paper calls it a "Computational Sign Pattern" but uses \begin{observation} environment. This is technically fine but the \label{thm:sign} prefix "thm" is misleading -- it is not a theorem.

---

## 4. THE SPECTROSCOPE (Section 8)

### 4.1 Is the conjecture honestly labeled?

Conjecture 8.1 is labeled as a conjecture and assumes GRH with simple zeros. This is honest.

### 4.2 Is the heuristic argument sound?

The heuristic says: under GRH, E(N) ~ sum_rho N^rho / (rho zeta'(rho)), so R_2(p) p^{-1/2} ~ sum_k a_k p^{i gamma_k}. At gamma = gamma_j, the k=j term sums constructively while cross-terms cancel.

**Problems:**
1. The paper does not define what R_2(p) is precisely in the spectroscope section. Definition 8.1 uses "the insertion-deviation correlation ratio (the insertion-deviation ratio from Section 2)." But Section 2 defines delta(f) = f - {pf} as the "shift," and R_2 appears first in Observation 7.4 as the "response ratio" (summing over old fractions). The connection between R_2 and the explicit formula is not established.

2. The step "R_2(p) p^{-1/2} ~ sum_k a_k p^{i gamma_k}" is the core heuristic leap. The explicit formula gives the *counting error* E(N) in terms of zeta zeros. But R_2(p) is a ratio of sums of D * delta over sums of delta^2. The paper does not show how R_2(p) relates to E(p) or to the explicit formula. This is the weakest link in the entire spectroscope argument.

3. The "constructive summing" argument assumes that |sum_p p^{i(gamma_k - gamma_j)}| is small for k != j. This is essentially the pair correlation conjecture, which is not proved unconditionally. The paper acknowledges this (line 1949) but then immediately says the heuristic is "strongly supported by computation."

### 4.3 Could a skeptic dismiss it?

**Yes, easily.** A skeptic would say: "The Farey discrepancy is known to be controlled by zeta zeros via the Franel-Landau theorem. Any function derived from Farey data that correlates with the Mertens function will, when run through a periodogram, produce peaks at zeta zero locations. This is just the explicit formula applied to a periodogram -- it would be surprising if it did NOT work."

The paper does not adequately address this criticism. The spectroscope is computationally interesting but does not provide new information about zeta zeros that could not be obtained more efficiently by other methods. The paper acknowledges this (line 1993: "the Riemann-Siegel formula converges exponentially faster") but frames them as "complementary."

### 4.4 The correlation r = 0.997

The paper reports r = 0.997 with p < 10^{-8} for n=10 zeros, then honestly notes (line 1954) that "the monotonic decrease of both sequences inflates the correlation." This is correct and important. With n=10 points that are both monotonically decreasing, a high correlation is expected even for unrelated sequences. The effective degrees of freedom are much less than 8. **The paper should provide a more honest statistical assessment.** For instance, what is the correlation after removing the monotonic trend (e.g., using successive ratios)?

---

## 5. THE D(1/p) PROOF (Proposition 7.6)

### 5.1 Is rank(1/p, F_p) really 2?

The claim is that only 0/1 and 1/p itself are <= 1/p in F_p. Is this true? We need: for all a/b in F_p with a/b <= 1/p and b <= p, either a/b = 0/1 or a/b = 1/p.

If a/b <= 1/p with b <= p and gcd(a,b) = 1, then ap <= b. If a = 0, done. If a >= 1, then b >= p, so b = p and a = 1. If b < p, then a >= 1 gives a/b >= 1/b >= 1/(p-1) > 1/p for p >= 3. **Correct.**

Wait: 1/(p-1) > 1/p? Yes, for p >= 3: 1/(p-1) = p/(p(p-1)) > 1/p = (p-1)/(p(p-1)). So any fraction a/b with a >= 1 and b <= p-1 satisfies a/b >= 1/(p-1) > 1/p. Hence rank(1/p, F_p) = 2 (counting 0/1 and 1/p). **Correct.**

### 5.2 Is the formula exact?

D(1/p) = 2 - |F_p|/p. With |F_p| = |F_{p-1}| + (p-1):
D(1/p) = 2 - (|F_{p-1}| + p - 1)/p = 2 - |F_{p-1}|/p - 1 + 1/p = 1 + 1/p - |F_{p-1}|/p.

The paper writes this as "= 2 - (|F_{p-1}| + p - 1)/p = 1 + 1/p - |F_{p-1}|/p." **Correct.**

### 5.3 Does the asymptotic follow from Mertens?

|F_{p-1}| = 1 + sum_{k=1}^{p-1} phi(k) ~ 3(p-1)^2/pi^2 ~ 3p^2/pi^2.

D(1/p) ~ 1 - 3p/pi^2 ~ -3p/pi^2. **Correct.**

The product D(1/p) * delta(1/p): we need delta(1/p) = 1/p - {p/p} = 1/p - 0 = 1/p. So D(1/p) * delta(1/p) ~ (-3p/pi^2)(1/p) = -3/pi^2. **Correct.**

### 5.4 The "65-73% dominance" claim

This is stated for p <= 199 and is a computational observation, appropriately qualified. The fraction decreasing with p would be expected as more fractions contribute to the sum.

---

## 6. DAMAGE/RESPONSE DECOMPOSITION (Observation 7.4)

### 6.1 Definition clarity

R_1 and R_2 are defined informally: R_1 sums "D * delta_1 over new fractions" and R_2 sums "D * delta_2 over existing fractions." But delta_1 and delta_2 are new notation introduced only in this observation. delta_1 = f - f_prev "in F_p" is the gap between the new fraction and its predecessor, while delta_2(a/b) = (a - pa mod b)/b.

**Problem:** delta_2 is the same as delta(f) = f - {pf} from the main definitions. So R_2 should just use the existing notation. The introduction of delta_1 and delta_2 is confusing and unnecessary.

### 6.2 Do they sum to something meaningful?

The paper says R_1 < 0 always and R_2 > 0 always (for qualifying primes), with R_2 dominating. But R_1 + R_2 is NOT stated to equal R (the correlation ratio). The damage-response decomposition appears to be a different decomposition from the B + C framework. The paper should clarify the relationship.

### 6.3 "Response overcompensates damage"

This is justified by the data: R_2 > |R_1| in all tested cases. But the observation also notes that the sign alignment is "weak" (59% at p=31), with magnitude doing the work. This is honest reporting.

---

## 7. MISSING MATH / WHAT WOULD MAKE SECTIONS STRONGER

### 7.1 Bridge Identity (Section 3)

**Almost within reach:** A full proof of the Displacement-Cosine Identity (Theorem 3.4). The proof sketch is currently a gap. If the pairing D(f) + D(1-f) = -1 is used together with cos(2 pi p f) = cos(2 pi p(1-f)), then sum D(f) cos(2 pi pf) = sum_{pairs} [D(f) + D(1-f)] cos(2 pi pf) = -sum_{pairs} cos(2 pi pf) + boundary. This should give -1/2 * sum cos(2 pi pf) + boundary correction = -1/2 * (M(p) + 2) + correction. Working this out properly would fill the gap.

### 7.2 The four-term decomposition (Section 4.4)

**Decisive computation:** Verify the four-term decomposition to p = 1,000,000 using MPFR arithmetic, with particular attention to the D/A ratio near 1. If D/A deviates significantly from 1 for large p, the "near-cancellation" narrative weakens. If it stays within [0.97, 1.12], this strengthens the picture substantially.

### 7.3 Sign Theorem

**Most important missing proof:** Show R(p) > -1/2 for all primes p >= 11. The paper identifies this as the frontier and notes a 44x gap in Cauchy-Schwarz. The Kloosterman/Weil bound approach (Open Question 11) is the right direction but is not even partially executed. **Even a conditional result** (e.g., R(p) > -1/2 under GRH, or for p in a density-one set) would dramatically strengthen the paper.

### 7.4 Spectroscope (Section 8)

**Needed:** A rigorous error analysis. The paper claims 0.4% accuracy for gamma_1 with 3,829 primes. But what is the expected accuracy from random Dirichlet series? A null model (random coefficients with the same magnitude distribution as R_2(p)) would establish whether the spectroscope genuinely detects zeros or merely picks up the largest peak in noise.

### 7.5 Total Shift-Squared Asymptotic

**Within reach:** Make the Kloosterman constant explicit. The Weil bound gives |S(m,n;c)| <= d(c) c^{1/2} (m,n,c)^{1/2}. For the specific sums here, the constant can likely be made explicit, promoting this from a conditional to an unconditional result.

### 7.6 The C_W >= N/28 bound

**Within reach:** Replace the approximate constants (0.05N, 0.01N^3, etc.) with rigorous lower bounds. This is an exercise in careful estimation, not a conceptual difficulty.

---

## 8. VERDICT

### For arXiv: CONDITIONALLY YES

The paper has enough genuine mathematical content (Bridge Identity, Universal Formula, Injection Principle, four-term decomposition, extensive Lean verification) to be a legitimate arXiv preprint. However, the following must be fixed first:

1. **Stop calling Observation 7.1 the "Sign Theorem."** It is a computational observation that is KNOWN TO FAIL beyond the computed range (Remark 7.2). Call it the "Sign Pattern" or "Computational Sign Observation."

2. **Fix the R(p) definition inconsistency** between the abstract (R = 2 sum D delta / sum delta^2) and the body (B + C = sum delta^2 (1 + 2R)), which are algebraically incompatible.

3. **Provide a complete proof of the Displacement-Cosine Identity** (Theorem 3.4), or downgrade it to a computationally verified observation.

4. **Add honest error bars** to the spectroscope correlation (r = 0.997 with n=10 monotonically decreasing quantities is not impressive).

5. **State clearly in the abstract** that the "both signs occur infinitely often" claim depends on the empirical sigmoid, which is not proved.

### For Mathematics of Computation: NOT YET

The paper would need, in addition to the above:

- Full proofs (not sketches) of ALL theorems. "Proof sketch" is not acceptable for a journal submission.
- The "Master Involution Principle" must be stated and proved.
- A genuine analytical result beyond the computational range (e.g., R(p) > -1/2 for a density-one set, or an unconditional spectroscope convergence theorem).
- Significant tightening of the writing: the paper is too long for its proved content. Much of the computational observation could go to supplementary material.
- Remove or drastically shorten the "Applications and Connections" section, which currently contains only the RH restatement (which is trivially equivalent to the classical Mertens characterization).
- The Lean verification, while impressive as engineering, should not be presented as if it adds mathematical content. Verifying "mu(p) = -1" in Lean 4 is not a mathematical contribution.

### For a top journal (Annals, Inventiones, etc.): NO

The paper's main contributions are: (1) a well-executed computational study of a natural quantity, (2) elementary but clean identities connecting Farey sums to Mertens, and (3) an interesting spectroscopic visualization. None of these reach the depth required for a top journal. The fundamental difficulty is that the per-step Farey discrepancy, while novel as a specific object of study, is entirely controlled by the Mertens function via classical mechanisms (Ramanujan sums, explicit formula). The paper discovers this connection computationally and verifies it extensively, but does not prove a deep new theorem. The spectroscope is an application of the explicit formula, not a new method for studying zeta zeros.

### Summary of Required Changes (ranked by importance)

1. Fix the R(p) definition inconsistency (mathematical error)
2. Provide a real proof of the Displacement-Cosine Identity (gap)
3. Rename "Sign Theorem" to "Sign Pattern" throughout (overstatement)
4. Qualify the "unconditional" claim about both signs occurring infinitely often (overstatement)
5. Add null model comparison for spectroscope (missing validation)
6. Convert all proof sketches to full proofs (incomplete)
7. State the "Master Involution Principle" explicitly (undefined term)
8. Report error bars on power law exponents (missing statistics)
9. Reduce paper length by moving computational details to supplement (structure)
10. Tighten the abstract to separate proved results from computational observations (clarity)

---

## Appendix: Minor Issues

- Line 321: "M(p-1) = M(p) + 1" -- add "(since mu(p) = -1 for prime p)"
- Line 406: "sum = 0 (vectors cancel)" -- for p=11, M(11) = -2, so bridge gives M+2 = 0. Correct.
- Line 592: "Verified by exact computation for all primes p <= 500" -- a proof sketch should not rely on computation.
- Line 966: "a/b = (p-2)/(p-1)" -- this is the fraction just below 1 in F_{p-1}. Is this correct? For F_6, the fraction just below 1 is 5/6. For general p, the fraction just below 1 in F_{p-1} is (p-2)/(p-1). This is correct.
- Line 1088: "Conjecture 5.8 (Composite Healing Rate)" is labeled with \label{thm:healing} but referenced as Conjecture~\ref{conj:healing} at line 1098. The cross-reference appears broken.
- Line 1128: "sum_old D_{F_p} = -n/2" -- this needs justification. The total displacement sum for F_p is -|F_p|/2, and the new fractions contribute sum D(k/p). The claim that old fractions contribute -n/2 where n = |F_{p-1}| is not obvious.
- Line 1140: Proposition 5.10 says sum D(k/p) = 1 for primes p >= 3. But line 1128 says sum D(k/p) = -(p-1)/2. These are contradictory. The first sums over k=1..p-1, the second also. One of them must be wrong, or they are measuring different quantities (rank in F_p vs. something else).
- Line 1463: "D_q(2) = q(q^2-1)/24" but the Remark then says "Delta W(q) = D_q(2)/q = (q^2-1)/24 for prime q." This implies Delta W is directly the deficit divided by q, which needs justification from the four-term decomposition.
- Reference [Garcia2025] is cited in the bibliography but never referenced in the text.
- Reference [Niederreiter1992] is cited but never referenced in the text.
- Reference [IwaniecKowalski2004] is cited but never referenced in the text.
- Reference [AthreyaCheung2014] is cited but never referenced in the text.
- Reference [ElMarraki1995] is cited but never referenced in the text.
- Reference [ErdosTuran1948] is cited but never referenced in the text (the Erdos-Turan section was cut).
- Reference [ParksBurrus2020] is cited but never referenced in the text (the CZT section was cut).
- Reference [Montgomery1973] is cited but never referenced in the text (pair correlation is mentioned but not cited inline).
- Reference [Walfisz1963] is cited but never referenced in the text.

**Multiple unused references suggest aggressive cutting without updating the bibliography.** Clean up the reference list.

---

*End of report.*
