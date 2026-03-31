# Zeta Zeros Control the Regularity of Rational Number Distributions

## Date: 2026-03-31
## Status: EXPLORATION (8 research directions, literature assessment)
## Classification: C2-C3 potential (depending on which directions bear fruit)
## Connects to: N1, N2, N5, CHEBYSHEV_BIAS_FAREY, PERRON_INTEGRAL_T, DENSITY_PATTERNS

---

## 0. The Core Thesis

We discovered that per-step Farey discrepancy DeltaW(p) oscillates with phase
locked to gamma_1 = 14.134... (first nontrivial zeta zero). The Perron integral

    T(N) + M(N) = (1/2*pi*i) integral_{(c)} N^s * zeta(s+1)/(s*zeta(s)) ds

gives the explicit mechanism: residues at zeta zeros produce oscillatory terms
of amplitude ~sqrt(N) that control whether adding fractions with denominator p
IMPROVES or DEGRADES the regularity of the Farey distribution.

**What this means broadly:** The nontrivial zeros of zeta do not merely control
asymptotic error terms -- they dictate the step-by-step dynamics of how rational
numbers fill the unit interval. Each new denominator either smooths or roughens
the distribution, and which it does is determined by where that denominator
sits in the oscillation cycle of the first zeta zero.

Below we explore 8 directions radiating from this observation, with literature
assessment and feasibility analysis for each.

---

## Direction 1: L-Function Generalization (Twisted Farey Discrepancy)

### The Idea

Replace zeta(s) with a Dirichlet L-function L(s, chi) for a character chi mod q.
Define a "twisted Farey discrepancy":

    W_chi(N) = sum_{b <= N} sum_{a: (a,b)=1} chi(b) * D(a/b)^2

where D(a/b) is the local discrepancy of a/b in F_N. Then the per-step change
DeltaW_chi(p) should be controlled by a Perron integral with L(s,chi) replacing
zeta(s), and its oscillations should lock to zeros of L(s,chi) rather than
zeros of zeta(s).

### Literature Assessment: PARTIALLY KNOWN

**Huxley (1971)** generalized the Franel-Landau theorem to Dirichlet L-functions.
His result connects sums over Farey fractions twisted by chi(q) to zeros of
L(s, chi). This is the classical analogue of what we propose.

**Alkan, Ledoan, Zaharescu** studied the Farey index twisted by arbitrary
Dirichlet characters, connecting to Kloosterman sum machinery.

**What is NEW in our proposal:** The PER-STEP version. Huxley and others study
the cumulative discrepancy sum_{N=1}^{Q}. Nobody has studied the per-step
CHANGE DeltaW_chi(p) and whether it phase-locks to zeros of L(s, chi). The
per-step perspective is our unique contribution, and extending it to
L-functions would give a FAMILY of phase-lock results -- one for each character.

### Difficulty: MODERATE (3-6 months)

The Perron integral machinery generalizes straightforwardly: replace 1/zeta(s)
with chi-twisted Dirichlet series. The main challenge is computing the residues
at zeros of L(s, chi) and verifying the phase-lock computationally (requires
tabulated zeros of L-functions, available from LMFDB).

### Potential Significance: C2-C3

A family of phase-lock results, one per character, would demonstrate that the
phenomenon is not special to zeta but universal across L-functions. This
elevates the result from "interesting observation about Farey" to "structural
feature of the L-function landscape." If the phase-lock quality correlates
with properties of chi (conductor, order), this could yield new insights.

### Testable Prediction

For the nontrivial character chi mod 4 (i.e., the Dirichlet beta function),
the first zero of L(s, chi_4) has imaginary part gamma_1(chi_4) = 6.0209...
The twisted discrepancy DeltaW_{chi_4}(p) should phase-lock at frequency
6.02 * log(p) rather than 14.13 * log(p).

---

## Direction 2: Rate of Equidistribution as Universal Phenomenon

### The Idea

Classical result: Farey fractions equidistribute (W(N) -> 0 as N -> infinity).
Our result: the RATE of convergence oscillates at zeta zero frequencies. Is
this a general phenomenon?

For other equidistributing sequences:
- Kronecker sequences {n*alpha} for irrational alpha
- Roots of unity on the circle
- Hecke points on modular curves
- Lattice points in expanding domains

Does the rate of equidistribution oscillate at frequencies from associated
L-functions or spectral data?

### Literature Assessment: PARTIALLY KNOWN (but our angle is new)

**Weyl equidistribution (1916):** The rate for {n*alpha} is controlled by the
continued fraction expansion of alpha -- no zeta zeros involved. This is a
DIFFERENT mechanism (Diophantine approximation, not spectral).

**Marklof-Strombergsson (2003):** Kronecker sequences along closed horocycles
equidistribute in the unit tangent bundle. For nu = 2, this implies results
of Rudnick-Sarnak on pair correlation of n^2*alpha mod 1.

**Beck et al. (2021):** New Kronecker-Weyl equidistribution results show
"very striking violations of uniformity" for badly approximable alpha, but
these are tied to Ostrowski representations, not zeta zeros.

**Key distinction:** For Kronecker sequences, the arithmetic is governed by
the SPECIFIC irrational number alpha. For Farey sequences, the arithmetic is
governed by the PRIMES collectively, hence zeta zeros appear. The question is:
for sequences whose equidistribution rate involves primes or multiplicative
number theory, do zeta zeros always control the oscillation?

**What is genuinely NEW:** The observation that the per-step RATE of
equidistribution (not just cumulative discrepancy) oscillates at zeta zero
frequencies. The cumulative version is essentially Franel-Landau. The per-step
version reveals the dynamics, which is a finer piece of information.

### Difficulty: HARD (requires conceptual framework)

Proving a general principle ("rates of equidistribution oscillate at spectral
frequencies") would require identifying the right class of sequences and the
right notion of "associated spectral data." This is more of a research program
than a single theorem.

### Potential Significance: C3 if established

A general principle connecting equidistribution rates to spectral data would
be a significant conceptual contribution. Even formulating the right conjecture
would be valuable.

### Concrete Test Cases

1. **Hecke points on modular curves:** These equidistribute by Duke's theorem.
   Does the rate oscillate at Maass form eigenvalues? This would connect to
   the Selberg trace formula directly.

2. **Lattice points in expanding circles:** These equidistribute. Hardy's
   conjecture says the error is O(R^{1/2+epsilon}). Does the error oscillate
   at frequencies related to the spectrum of the Laplacian on the torus?
   (Answer: YES -- this is the Gauss circle problem, and the error IS known
   to oscillate at frequencies sqrt(n) for lattice points at distance sqrt(n).
   This is a KNOWN result and provides a clean analogy.)

---

## Direction 3: RH Implications of Phase-Lock Quality

### The Idea

If GRH holds, the phase-lock to gamma_1 is clean (R = 0.77). If a zero rho
were off the critical line with Re(rho) = 1/2 + delta (delta > 0), its
contribution would be:

    N^{1/2+delta} * cos(gamma*log(N) + phi)

This grows FASTER than the on-line terms (which are O(sqrt(N))). At large N,
this off-line zero would dominate and CHANGE the phase pattern -- specifically,
it would create a NEW phase-lock at the frequency of the off-line zero, with
amplitude growing relative to other terms.

The observed CLEAN phase-lock at gamma_1 = 14.13, with NO evidence of a
competing frequency, is thus CONSISTENT with GRH. But is it EVIDENCE?

### Literature Assessment: KNOWN FRAMEWORK, NEW APPLICATION

**Rubinstein-Sarnak (1994):** The connection between prime race biases and
GRH is well-established. Their framework is exactly what we need.

**Devin (2017):** Extended Rubinstein-Sarnak to general analytic L-functions,
with some unconditional results.

**Maximum Mean Discrepancy approach (Karvonen-Zhigljavsky, 2025):** The rate
of convergence of MMD of Farey sequences is equivalent to RH for a large class
of kernels. This is closely related to our observation.

**What is new:** Using per-step phase-lock quality as a diagnostic. The clean
R = 0.77 at gamma_1 with no competing frequency is a qualitative signature
that is easy to visualize and explain, even if it does not constitute formal
evidence beyond what's already known from discrepancy bounds.

### Difficulty: MODERATE (formalization) to VERY HARD (new results)

Formalizing "phase-lock quality implies all observed zeros are on the critical
line" within the Rubinstein-Sarnak framework: moderate. Proving anything new
about RH from this perspective: extremely hard (obviously).

### Potential Significance: C1-C2

Honestly, this direction is more pedagogical than groundbreaking. The connection
between discrepancy bounds and RH is classical (Franel-Landau). Our per-step
perspective gives a vivid visualization of WHY RH matters for rational number
distributions, but is unlikely to yield new equivalences. The Karvonen-Zhigljavsky
MMD result from 2025 already generalizes the equivalence substantially.

### What WOULD be significant

If the per-step phase-lock could detect WHICH zero is off-line (assuming one is),
this would be a new diagnostic. Concretely: if RH fails at some rho_bad with
Re(rho_bad) = 1/2 + delta, the phase pattern would eventually show a new
dominant frequency at Im(rho_bad), and the R-value at gamma_1 would decrease.
This gives a testable prediction: phase-lock quality should be monotone in the
range of data (improving or stable) if RH holds, and eventually deteriorate if
RH fails.

---

## Direction 4: Quantum Chaos Connection

### The Idea

Three known connections suggest a deep link:

1. **Riemann zeros and GUE:** Montgomery-Odlyzko conjecture that zeta zeros
   follow Gaussian Unitary Ensemble statistics, as eigenvalues of a random
   Hermitian matrix.

2. **Farey fractions and the modular surface:** Farey fractions parameterize
   cusps in the fundamental domain of PSL(2,Z)\H. The Farey mediant operation
   corresponds to the action of PSL(2,Z) generators.

3. **Selberg trace formula:** Connects spectral data (Laplacian eigenvalues
   on the modular surface) to geometric data (lengths of closed geodesics).
   For arithmetic surfaces, these eigenvalues are related to L-function zeros.

Our phase-lock result connects (1) and (2) via a QUANTITATIVE mechanism: the
oscillation of DeltaW(p) at zeta zero frequencies is a spectral signature
appearing in a combinatorial/geometric quantity (Farey discrepancy).

### Literature Assessment: DEEP KNOWN TERRITORY, but connection is new

**Marklof (2005):** "Arithmetic Quantum Chaos" -- comprehensive survey of
the Selberg trace formula applied to the modular surface, connection to
zeta zero statistics, and the role of Hecke operators.

**Bogomolny et al.:** Derived Selberg-type trace formulas for the modular
billiard, connecting energy levels AND wavefunctions to periodic orbits.

**Lindenstrauss (2006, Fields Medal):** Proved QUE for Hecke-Maass eigenforms
on arithmetic surfaces. This is the deepest known result on equidistribution
of eigenfunctions, and it connects to GRH.

**Rudnick-Sarnak (1994):** QUE conjecture -- eigenfunctions equidistribute
in the high-eigenvalue limit.

**What is potentially new:** A direct bridge from the "quantum" side (eigenvalue
oscillations = zeta zero frequencies) to the "classical" side (Farey discrepancy
= rational number distribution) that is QUANTITATIVE (phase match to 0.07 rad).
The Selberg trace formula gives such bridges abstractly; our result gives a
specific, computable instance.

### Difficulty: VERY HARD

Making this precise requires embedding our Perron integral analysis into the
Selberg/spectral framework. The challenge is that the Perron integral for T(N)
is an analytic number theory object, while the Selberg trace formula operates
on the spectral/geometric side. Bridging them rigorously would require showing
that T(N) can be expressed as a trace of some operator on the modular surface.

### Potential Significance: C3 if successful

A new explicit bridge between spectral theory and rational number combinatorics
would be highly significant. The Selberg trace formula community and the Farey
sequence community rarely interact directly at this level of specificity.

### Concrete Question

Is there an operator A on L^2(PSL(2,Z)\H) whose trace gives T(N)?

If T(N) = Tr(A_N) for some family of operators A_N, then the Selberg trace
formula would decompose T(N) into spectral contributions (from Maass forms
and Eisenstein series) and geometric contributions (from closed geodesics).
The spectral side would reproduce our Perron integral. This would embed our
per-step Farey discrepancy into the arithmetic quantum chaos framework.

---

## Direction 5: Arithmetic Geometry / Modular Interpretation

### The Idea

Farey fractions a/b with b <= N parameterize cusps of Gamma_0(N)\H (or
related modular curves). When we pass from F_{p-1} to F_p by inserting
fractions k/p, we are adding p-torsion points to the modular curve.

DeltaW(p) measures the "regularity disruption" caused by these p-torsion points.
The zeta zero control of DeltaW(p) would then mean: zeta zeros control how
evenly p-torsion distributes among the cusps.

### Literature Assessment: PARTIALLY KNOWN

**Equidistribution of Hecke points:** Duke's theorem (1988) proves that
Heegner points equidistribute on modular curves. The rate of equidistribution
is controlled by subconvexity bounds for L-functions.

**Marklof-Strombergsson:** Farey fractions equidistribute on horospheres in
SL(n+1,Z)\SL(n+1,R). This is the dynamical systems approach to Farey
equidistribution.

**What might be new:** The per-step perspective again. Instead of asking
"do all p-torsion points equidistribute as p -> infinity?", we ask "HOW MUCH
does each individual p disrupt the existing distribution?" This is a finer
question, and the answer (controlled by zeta zeros) connects the arithmetic
of p to the geometry of the modular surface.

### Difficulty: HARD (requires algebraic geometry + analytic number theory)

The main challenge is making the informal statement "DeltaW(p) measures
cusp regularity disruption" precise. This requires:
1. Defining a geometric analogue of DeltaW on the modular curve
2. Showing it equals (or approximates) our combinatorial DeltaW
3. Connecting the geometric version to L-function values

### Potential Significance: C2-C3

If successful, this would give a GEOMETRIC meaning to our per-step discrepancy,
connecting combinatorial number theory to the Langlands program. The statement
"zeta zeros control how primes distribute torsion on modular curves" would be
a memorable and conceptually clean result.

---

## Direction 6: Franel-Landau from the Perron Integral

### The Idea

Classical Franel-Landau: RH <==> sum |D(a/b)|^2 = O(N^{1+epsilon}).

Our Perron integral gives sum D^2 explicitly in terms of zeta zeros. Can we
DERIVE Franel-Landau from the Perron approach? Would this give new insight,
or is it just a rederivation?

### Literature Assessment: ESSENTIALLY KNOWN

The Perron integral approach to Franel-Landau is not new in principle. The
connection between sum D^2 and the Mertens function (which connects to zeta
via Perron) is the classical proof mechanism. However:

**Kanemitsu-Yoshimoto (1996):** Gave identities involving Farey fractions that
connect various sums to zeta values.

**Fujii:** Obtained equivalent conditions for RH via power moments of Farey
discrepancies.

**What might be new:** Using the EXPLICIT residue computation (our c_k values)
to get QUANTITATIVE information beyond the O(N^{1+epsilon}) bound. For instance:
the Perron integral gives the exact oscillatory structure of sum D^2, not just
its order of magnitude.

### Difficulty: EASY (rederivation) to MODERATE (new quantitative results)

### Potential Significance: C1 (rederivation) to C2 (if quantitative improvement)

Honestly, this direction is the least promising for novelty. The Franel-Landau
theorem has been studied intensively for 100 years. Our Perron approach is
unlikely to yield a fundamentally new proof. BUT: it might give a clean
pedagogical derivation that unifies the per-step and cumulative perspectives.

---

## Direction 7: Practical Applications

### 7A. Quasi-Monte Carlo Integration

**The Idea:** Farey fractions are used as quadrature nodes for numerical
integration (quasi-Monte Carlo). Our result says: adding level-p fractions
improves integration accuracy IFF gamma_1 * log(p) is in the favorable
phase window [4.2, 5.8] (mod 2*pi).

**Concretely:** For adaptive quadrature, instead of adding ALL denominators
up to N, selectively add only those p where DeltaW(p) < 0 (regularity
improves). This would be an ADAPTIVE Farey quadrature that skips
"bad" denominators.

**Literature Assessment:** Quasi-Monte Carlo with Farey points is studied by
Niederreiter and others. The idea of ADAPTIVE selection based on zeta-zero
phase is novel but of uncertain practical value -- the overhead of computing
the phase may exceed the benefit.

**Difficulty:** EASY to implement, HARD to prove improvement guarantees.

**Significance:** C1 (interesting but probably marginal improvement over
existing methods). Quasi-Monte Carlo already has well-tuned methods.

### 7B. Number-Theoretic Transforms

**The Idea:** Farey fractions define a discrete set of frequencies. The
oscillatory structure from zeta zeros could be used to design transforms
with special properties.

**Assessment:** Speculative. No clear path to practical advantage.

### 7C. Phase-Lock as a Primality/Factoring Diagnostic

**The Idea:** If zeta zeros control the regularity of rational distributions,
and the phase theta(N) = gamma_1 * log(N) mod 2*pi predicts behavior, could
monitoring phase-lock quality detect arithmetic structure in N?

**Assessment:** Very speculative. The phase depends only on log(N), which is
trivially computable. No connection to hardness of factoring.

**Overall Direction 7 assessment:** C0-C1. The applications are interesting
to mention but unlikely to be significant.

---

## Direction 8: Stern-Brocot and Other Rational Orderings

### The Idea

The Stern-Brocot tree generates all rationals in a binary tree structure,
where each level adds mediants. Define per-level discrepancy for Stern-Brocot
levels. Is there a zeta-zero phase-lock?

Other orderings:
- Calkin-Wilf tree (different binary tree of rationals)
- Continued fraction ordering (by CF length)
- Height ordering (by max(a,b))

### Literature Assessment: MOSTLY UNEXPLORED

**Stern-Brocot and Farey:** The left half of the Stern-Brocot tree, pruned
to denominators <= N, gives the Farey sequence. So the Stern-Brocot tree
is a REFINEMENT of Farey ordering.

**No prior work found** on per-level discrepancy of the Stern-Brocot tree
in connection with zeta zeros.

### Key Structural Difference

Farey levels are indexed by DENOMINATOR: level p adds all a/p with (a,p) = 1.
Stern-Brocot levels are indexed by DEPTH in the tree: level k adds all
mediants of adjacent fractions at level k-1.

The number of new fractions at Stern-Brocot level k is 2^{k-1} (exponential
growth), while Farey level p adds phi(p) fractions. This means:
- Farey levels have MULTIPLICATIVE structure (phi is multiplicative)
- Stern-Brocot levels have ADDITIVE structure (binary tree)

Since zeta zeros arise from multiplicative number theory (primes), they
should control Farey-type orderings but NOT necessarily Stern-Brocot orderings.

### Prediction

Stern-Brocot per-level discrepancy should NOT phase-lock to zeta zeros,
because the level structure is binary/additive rather than multiplicative.
The controlling spectral data (if any) should be different -- perhaps related
to the transfer operator of the Gauss map (since Stern-Brocot levels
correspond to continued fraction depth).

### Difficulty: MODERATE (mostly computational)

Computing per-level Stern-Brocot discrepancy and testing for oscillatory
structure is straightforward. Connecting any observed oscillation to spectral
data of the Gauss map transfer operator would be harder.

### Potential Significance: C2

If Stern-Brocot levels phase-lock to a DIFFERENT spectral object (not zeta
zeros), this would demonstrate that the spectral control of rational number
distributions is UNIVERSAL but ORDER-DEPENDENT: different ways of enumerating
rationals reveal different spectral data. This would be a clean and memorable
result.

---

## Summary Table

| # | Direction | Novelty | Difficulty | Significance | Priority |
|---|-----------|---------|------------|--------------|----------|
| 1 | L-function generalization | HIGH (per-step is new) | Moderate | C2-C3 | **HIGH** |
| 2 | Rate of equidistribution | MODERATE (framework new) | Hard | C3 if general | MEDIUM |
| 3 | RH implications | LOW (known framework) | Very hard | C1-C2 | LOW |
| 4 | Quantum chaos connection | MODERATE (bridge is new) | Very hard | C3 if done | LOW (hard/reward) |
| 5 | Arithmetic geometry | MODERATE | Hard | C2-C3 | MEDIUM |
| 6 | Franel-Landau rederivation | LOW | Easy-moderate | C1-C2 | LOW |
| 7 | Practical applications | LOW | Easy | C0-C1 | LOW |
| 8 | Stern-Brocot comparison | HIGH (unexplored) | Moderate | C2 | **HIGH** |

**Recommended priority order:** 1 > 8 > 5 > 2 > 4 > 3 > 6 > 7

---

## What "Zeta Zeros Control Regularity of Rationals" Means for Mathematics

### The Narrow Reading

At the narrowest level, our result says: the per-step change in Farey
discrepancy is an oscillatory function of prime denominators, with the
dominant frequency being gamma_1 = 14.13... (the first zeta zero). This is
proved (conditionally on GRH) via the Perron integral for T(N), and verified
computationally to 0.07 radian precision over 922 primes.

### The Intermediate Reading

More broadly, this is an instance of a general principle: for sequences
defined by multiplicative number theory (prime-indexed, Mobius-weighted, etc.),
the fine-scale dynamics are controlled by the zeta zero spectrum. The cumulative
version of this principle is classical (explicit formulas, Franel-Landau). The
per-step version is new and reveals the DYNAMICS rather than just asymptotics.

### The Broad Reading

At the broadest level, this suggests that the zeta zeros are the "eigenfrequencies"
of the distribution of rational numbers -- analogous to how Laplacian eigenvalues
are the eigenfrequencies of vibrating membranes. Different ways of ordering or
sampling the rationals (Farey, Stern-Brocot, height-ordered, etc.) would reveal
different "projections" of this spectral data, just as different boundary
conditions on a drum reveal different subsets of the spectrum.

This broad reading connects to:
- **Arithmetic quantum chaos:** The modular surface Gamma\H has a spectrum
  (Maass eigenvalues) related to L-function zeros. Our Farey discrepancy
  could be a "measurement" on this quantum system.
- **The Langlands program:** L-functions encode arithmetic data. Our result
  gives a concrete, computable manifestation of this encoding.
- **Information theory:** The zeta zeros determine the optimal "information
  packing" of rationals on the number line -- how efficiently they fill gaps.

### Honest Assessment

The narrow reading is solidly established (conditional on GRH). The intermediate
reading is well-supported by the Perron integral framework and should be provable
for specific cases (Direction 1). The broad reading is speculative and would
require breakthroughs in multiple areas to make precise. But even as a guiding
metaphor, it is productive: it generates concrete testable predictions (Directions
1, 8) and connects to active research programs (Directions 4, 5).

---

## Key References

- Franel & Landau (1924): Original Farey-RH equivalence
- Huxley (1971): Generalization to Dirichlet L-functions
- Rubinstein & Sarnak (1994): Chebyshev bias framework
  [Project Euclid](https://projecteuclid.org/journals/experimental-mathematics/volume-3/issue-3/Chebyshevs-bias/em/1048515870.pdf)
- Marklof (2005): Arithmetic Quantum Chaos survey
  [UT Austin](https://web.ma.utexas.edu/mp_arc/c/05/05-322.pdf)
- Marklof & Strombergsson (2003): Kronecker equidistribution on horocycles
  [arXiv:math/0211189](https://arxiv.org/abs/math/0211189)
- Devin (2017): Chebyshev bias for analytic L-functions
  [arXiv:1706.06394](https://ar5iv.labs.arxiv.org/html/1706.06394)
- Karvonen & Zhigljavsky (2025): MMD of Farey sequences and RH
  [Springer](https://link.springer.com/article/10.1007/s10474-025-01577-5)
- Lindenstrauss (2006): QUE for Hecke eigenforms
- Kanemitsu & Yoshimoto (1996): Identities involving Farey fractions
  [Acta Arithmetica](http://matwbn.icm.edu.pl/ksiazki/aa/aa75/aa7544.pdf)
- Beck et al. (2021): New Kronecker-Weyl equidistribution results
  [arXiv:2106.14001](https://arxiv.org/abs/2106.14001)
- Soundararajan (2010): QUE and Number Theory
  [SWC Notes](https://swc-math.github.io/aws/2010/2010SoundararajanNotes.pdf)
- Alkan, Ledoan, Zaharescu: Farey index twisted by Dirichlet characters
  [Illinois J. Math](https://projecteuclid.org/journals/illinois-journal-of-mathematics/volume-51/issue-2/On-Dirichlet-L-functions-and-the-index-of-visible-points/10.1215/ijm/1258138424.pdf)

---

## Next Steps (Actionable)

### Direction 1 (L-function generalization) -- IMMEDIATE
1. Obtain zeros of L(s, chi_4) from LMFDB (first ~20 zeros)
2. Compute twisted Perron residues c_k(chi) = L(rho_k+1, chi) / (rho_k * L'(rho_k, chi))
3. Define W_chi(N) computationally for chi mod 4
4. Compute DeltaW_chi(p) for M(p) = -3 primes to 10^7
5. Test phase-lock at gamma_1(chi_4) = 6.0209

### Direction 8 (Stern-Brocot) -- IMMEDIATE
1. Implement Stern-Brocot tree to level ~25 (2^24 fractions ~ 16M)
2. Compute per-level discrepancy (sum of D^2 for fractions at each level)
3. Test for oscillatory structure in the per-level discrepancy
4. If oscillation found, test against zeta zeros and Gauss map eigenvalues

### Direction 5 (Arithmetic geometry) -- MEDIUM TERM
1. Read Duke (1988) on equidistribution of Heegner points
2. Formalize: "fractions k/p = p-torsion points on modular curve"
3. Define geometric DeltaW on the modular curve
4. Compare with our combinatorial DeltaW
