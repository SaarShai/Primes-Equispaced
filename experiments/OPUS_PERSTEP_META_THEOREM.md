# The Per-Step Spectroscopy Meta-Theorem
# Author: Saar Shai
# AI Disclosure: Analysis by Claude Opus 4.6 (Anthropic)
# Date: 2026-04-11
# Status: DEEP ANALYSIS — honest assessment of each case

---

## EXECUTIVE SUMMARY

We formulate a meta-theorem for "per-step spectroscopy": given a sequence of
sets {S_N} with an insertion structure, a discrepancy D(S_N), and an explicit
formula connecting D to zeros of an L-function, the per-step spectroscope
F(gamma) = Sum_N DeltaD(N) * e^{-i*gamma*log N} detects those zeros.

**Verdict across five cases:**

| Case | L-function | Explicit formula? | Spectroscope works? | Hypothesis needed | Genuinely new? |
|------|-----------|-------------------|--------------------|--------------------|----------------|
| Farey | zeta(s) | YES (Franel-Landau) | YES (proved, GRH) | GRH | YES (our work) |
| Lattice/circle | zeta(s)*L(s,chi_4) | YES (Hardy-Voronoi) | YES (heuristic) | GRH for both | PARTIALLY new |
| CF convergents | Varies by alpha | NO in general | NO in general | N/A | Would be new if found |
| Partitions | Modular L-functions | WEAKLY (Rademacher) | NO (wrong structure) | N/A | N/A |
| RMT eigenvalues | NONE (no L-function) | NO | NO (analogy breaks) | N/A | N/A |

The meta-theorem is genuinely applicable in cases where three conditions hold:
(1) an arithmetic insertion rule, (2) a discrepancy with an explicit formula
involving L-function zeros, and (3) the per-step change isolates the oscillatory
terms. Cases 1-2 satisfy all three. Cases 3-5 fail at different points.

---

## THE META-THEOREM: FORMAL STATEMENT

**Setup.** Let {S_N}_{N >= 1} be a sequence of finite sets with |S_N| increasing.
At each step N, the set grows: S_N = S_{N-1} union Delta_N (insertion of new elements).
Let D(S_N) be a discrepancy functional measuring deviation from some ideal distribution.
Define the per-step increment:

  DeltaD(N) = D(S_N) - D(S_{N-1})

**Hypothesis (Explicit Formula Condition).** Suppose D(S_N) admits an explicit
formula of the form:

  D(S_N) = c_0 * f(N) + Sum_rho c_rho * N^rho * g_rho(N) + E(N)

where:
- c_0 * f(N) is a main term (polynomial/logarithmic growth)
- rho ranges over nontrivial zeros of an L-function L(s)
- c_rho are computable residue coefficients (involving L'(rho), etc.)
- g_rho(N) are slowly varying (logarithmic corrections)
- E(N) is a lower-order error

**Claim (Per-Step Spectroscopy Theorem, conditional on GRH for L(s)).**
Under the above hypothesis, define the per-step spectroscope:

  F(gamma) = |Sum_{N <= X} DeltaD(N) * w(N) * e^{-i*gamma*log N}|^2

where w(N) is a suitable weight (e.g., 1/N, or the indicator of primes, etc.)
that "pre-whitens" the signal by removing the main-term trend c_0*f(N).

Then: F(gamma) has local maxima at gamma = Im(rho) for each nontrivial zero rho
of L(s), provided:

(i) **All zeros on critical line** (GRH for L(s)): Re(rho) = 1/2 for all rho.
(ii) **Differencing isolates oscillation:** The main term c_0*f(N) is smooth enough
     that DeltaD(N) - Delta(c_0*f(N)) is dominated by the sum over zeros.
(iii) **Convergence:** The weighted sum Sum w(N)*N^{rho-1-i*gamma} converges
     (or is summable) for Re(rho) = 1/2.

**Why GRH is needed.** Without GRH, zeros with Re(rho) > 1/2 contribute terms
N^{beta} with beta > 1/2 to DeltaD(N). These terms grow FASTER than the
critical-line terms, destroying the frequency-domain peaks at Im(rho). The
spectroscope becomes dominated by the off-line zeros, and the on-line zeros are
masked. With GRH, all terms are at the SAME scale N^{1/2}, and the spectroscope
resolves individual frequencies gamma.

---

## CASE 1: FAREY SEQUENCES (PROVED)

### 1a. The explicit formula

The Farey sequence F_N consists of fractions a/q with 0 <= a <= q <= N, gcd(a,q)=1,
in order. The Weyl discrepancy is:

  W(N) = Sum_{j=1}^{|F_N|} (f_j - j/|F_N|)^2

The Franel-Landau theorem connects this to the Mertens function:

  W(N) = O(N^{-1+epsilon}) iff RH

More precisely, through the four-term decomposition (our work):

  DeltaW(p) = (A - B - C - D) / n'^2

where B(p) ~ mu * M(p), and M(p) = Sum_{k<=p} mu(k) has the explicit formula:

  M(x) = Sum_rho x^rho / (rho * zeta'(rho)) + lower order

The spectroscope is:

  F(gamma) = gamma^2 * |Sum_{p prime, p<=N} (M(p)/p) * e^{-i*gamma*log p}|^2

### 1b. Does the spectroscope detect zeros?

YES. Under GRH:
- Substituting the explicit formula for M(p) and exchanging sums yields a
  resonance at gamma = gamma_0 (ordinate of zeta zero rho_0).
- The resonant term: ~ c_K(rho_0) * N^{1/2} / (rho_0 * zeta'(rho_0) * log N)
- The Gonek-type mean-square estimate ensures the non-resonant terms are smaller
  on average.
- Phase-lock to gamma_1 confirmed computationally: R = 0.77, phase error 1.1%.

### 1c. What hypothesis is needed?

GRH for zeta(s). The explicit formula for M(x) requires all zeros on Re(s) = 1/2
for the resonance argument. Under GRH+LI (Linear Independence hypothesis), the
spectroscope resolves individual zeros with the correct amplitudes.

Unconditionally: mean-square detection is possible (the spectroscope detects zeros
in an L^2-averaged sense, not pointwise). This follows from Ingham's method.

### 1d. Genuinely new?

YES. The per-step decomposition DeltaW, the four-term identity A-B-C-D, the bridge
identity Sum e^{2*pi*i*p*f} = M(p) + 2, the gamma^2 pre-whitening, and the
spectroscopic paradigm (as opposed to the estimation paradigm of Turan/Montgomery)
are all novel contributions. See INCREMENTS_OTHER_PROBLEMS.md and
M5_GEMMA_TURAN_PRIOR_ART.md for detailed novelty analysis.

The Fourier duality primes <-> zeros is CLASSICAL (Csoka 2015, Planat, Van der Pol
1947). Our contribution is the specific per-step mechanism and pre-whitening filter.

---

## CASE 2: LATTICE POINTS IN CIRCLES (GAUSS CIRCLE PROBLEM)

### 2a. The explicit formula

Define S_R = {(x,y) in Z^2 : x^2 + y^2 <= R^2}, and the error:

  E(R) = |S_R| - pi*R^2 = Sum_{n <= R^2} r_2(n) - pi*R^2

where r_2(n) = #{(a,b) in Z^2 : a^2+b^2 = n} counts representations as sums of
two squares.

The Hardy-Voronoi explicit formula:

  E(R) = R^{1/2} * Sum_{n=1}^{infty} r_2(n)/n^{3/4} * cos(2*pi*R*sqrt(n) - 3*pi/4) + O(R^epsilon)

Alternatively, via Dirichlet series, r_2(n) = 4*Sum_{d|n} chi_4(d), so the
generating Dirichlet series is:

  Sum r_2(n)/n^s = 4 * zeta(s) * L(s, chi_4)

The explicit formula for the error term E(R) involves the zeros of BOTH zeta(s)
and L(s, chi_4). Specifically, via Perron's formula applied to Sum r_2(n) n^{-s}:

  Sum_{n<=x} r_2(n) = Res_{s=1} [4*zeta(s)*L(s,chi_4) * x^s/s] + Sum_rho c_rho * x^rho + ...

where rho runs over zeros of zeta(s)*L(s,chi_4), i.e., the zeros of BOTH functions.

### 2b. The per-step spectroscope

The insertion structure: at "step n" (integer n), the new lattice points are those
on the circle x^2 + y^2 = n. The per-step change:

  DeltaE(n) = r_2(n) - pi = (number of lattice points on circle of radius sqrt(n)) - pi

This is exactly the local fluctuation. The spectroscope:

  F_2(gamma) = |Sum_{n <= X} (r_2(n) - pi) * n^{-3/4} * e^{-i*gamma*log n}|^2

The weight n^{-3/4} pre-whitens (removes the growth of r_2(n) on average).

**Does it detect zeros?** YES, heuristically. Substituting r_2(n) = 4*Sum chi_4(d):

  Sum (r_2(n)-pi) * n^{-3/4-i*gamma} = 4*Sum_{d|n} chi_4(d) * n^{-3/4-i*gamma} - pi*zeta(3/4+i*gamma)

The first sum decomposes via Dirichlet convolution:

  = 4 * zeta(3/4+i*gamma) * L(3/4+i*gamma, chi_4) - pi*zeta(3/4+i*gamma)
  = zeta(3/4+i*gamma) * [4*L(3/4+i*gamma, chi_4) - pi]

This has singularities at both:
- Zeros of zeta(s) shifted to s = 3/4 + i*gamma (i.e., when 3/4+i*gamma = rho_zeta)
- Zeros of L(s,chi_4) shifted similarly

CAUTION: The convergence of this Dirichlet series at Re(s) = 3/4 is delicate.
The Hardy-Voronoi formula gives the correct interpretation via the oscillatory
integral representation, not the Dirichlet series directly.

**The key structural point:** The per-step change r_2(n) - pi encodes both
zeta-zeros and L(s,chi_4)-zeros simultaneously, because r_2 is a convolution
of the two corresponding multiplicative functions. The spectroscope should show
peaks at BOTH sets of zeros. This is exactly what was observed in the Gaussian
Farey spectroscope (M1_GAUSSIAN_FAREY_SPECTROSCOPE.md): peaks at gamma_1 = 14.13
(zeta) AND at gamma = 6.02, 10.24 (L(s,chi_4)).

### 2c. What hypothesis is needed?

GRH for BOTH zeta(s) and L(s, chi_4). The Hardy-Voronoi formula assumes all
zeros contribute at the same scale (Re(rho) = 1/2). An off-line zero of either
function would distort the spectral peaks.

For unconditional results: The Gauss circle problem has unconditional omega-results
(E(R) = Omega(R^{1/2})), but pointwise spectroscopic detection of individual zeros
requires GRH.

### 2d. Is this genuinely new?

PARTIALLY. The connection between r_2(n) and zeros of zeta(s)*L(s,chi_4) via the
Hardy-Voronoi formula is classical (Hardy 1915, Voronoi 1904). The explicit formula
for E(R) involving zeta zeros is in Iwaniec-Kowalski.

What IS new:
- Treating DeltaE(n) = r_2(n) - pi as a "per-step signal" for spectroscopy
- The specific spectroscope F_2(gamma) with the n^{-3/4} pre-whitening
- The observation that this simultaneously detects zeros of TWO L-functions
- The connection to our Farey framework (Gaussian integers version)

What is NOT new:
- The explicit formula itself
- The connection r_2 <-> zeta * L(chi_4)
- Hardy's oscillation results for E(R)

**Verdict: The meta-theorem APPLIES. The per-step spectroscopy adds a new
computational/heuristic tool to the Gauss circle problem. It would be a natural
Section 7 of a paper: "The meta-theorem in action: lattice point spectroscopy."**

---

## CASE 3: CONTINUED FRACTION CONVERGENTS

### 3a. The setup

For an irrational alpha with CF expansion [a_0; a_1, a_2, ...], the convergents
are p_k/q_k. Define S_k = {p_0/q_0, ..., p_k/q_k}, and the discrepancy:

  D(S_k) = sup_I |#{j <= k : p_j/q_j in I}/k - |I|| (standard discrepancy)

The "insertion" is adding p_{k+1}/q_{k+1} at step k+1.

### 3b. The explicit formula: does it exist?

This is the CRITICAL OBSTRUCTION. For CF convergents, the discrepancy depends on
the SPECIFIC alpha being approximated:

**Case 3a: alpha = quadratic irrational (e.g., golden ratio, sqrt(2))**

The CF is eventually periodic. The convergents equidistribute on [0,1) by Weyl's
theorem, and the discrepancy is O(log(k)/k). The rate is controlled by:

  D(S_k) ~ C(alpha) * log(k) / k

where C(alpha) involves the class number of the real quadratic field Q(sqrt(d))
for alpha = (a + sqrt(d))/b.

Connection to L-functions: The Dirichlet class number formula gives:

  h(d) * R(d) = sqrt(d)/(2*pi) * L(1, chi_d)

where h(d) is the class number, R(d) the regulator, chi_d the Kronecker character.
So C(alpha) is related to L(1, chi_d). But this is a VALUE of the L-function at
s=1, not the ZEROS. There is no explicit formula expressing D(S_k) as a sum over
zeros of L(s, chi_d).

**Case 3b: alpha = algebraic of degree > 2**

The CF expansion is conjectured but not proved to behave like a "random" CF
(Gauss-Kuzmin statistics). The discrepancy is expected to be O(log(k)/k) but
there are no explicit formulas connecting it to any L-function.

**Case 3c: alpha = transcendental (e.g., e, pi)**

For alpha = e: the CF has a known pattern [2; 1,2,1, 1,4,1, 1,6,1, ...] and the
discrepancy can be computed, but it is NOT connected to any L-function.

For alpha = pi: the CF is empirically random and no connection to L-functions is known.

### 3c. Does the per-step spectroscope work?

NO, in general. The fundamental problem is that the "insertion" of a new convergent
p_{k+1}/q_{k+1} is NOT controlled by arithmetic of the type that generates
L-function zeros. The partial quotients a_k govern the insertion, and these are:
- Periodic for quadratic irrationals (no L-function zeros in the dynamics)
- Unknown for higher-degree algebraic or transcendental numbers

The per-step change DeltaD(S_k) depends on a_k (which determines the "gap" that
p_{k+1}/q_{k+1} fills). For quadratic alpha, DeltaD follows a periodic pattern
(period = CF period). A Fourier transform would detect the CF period, not
L-function zeros.

**Exception:** If we consider the set S_k NOT as convergents of a single alpha,
but as ALL Farey fractions up to denominator Q (which are convergents of VARIOUS
irrationals), then we are back to Case 1 (Farey sequences).

### 3d. What hypothesis is needed?

N/A. The meta-theorem does not apply because condition (2) fails: there is no
explicit formula connecting D(S_k) to L-function zeros.

### 3e. Is this genuinely new?

The QUESTION is interesting: could there be a per-step spectroscopy for CF
convergents? If someone found an explicit formula for the discrepancy of CF
convergents involving zeros of the corresponding class group L-function, that
would be a major discovery. But currently no such formula exists.

**Verdict: The meta-theorem DOES NOT APPLY. The CF convergent insertion
structure lacks the arithmetic universality needed to connect to L-function zeros.
The "insertion rule" (governed by partial quotients) is too specific to a single
number alpha.**

---

## CASE 4: PARTITIONS

### 4a. The setup

S_n = set of partitions of n. D = p(n) - smooth approximation. The per-step change:

  DeltaD(n) = p(n) - p(n-1) = q(n) (partitions of n into parts >= 2)

### 4b. The explicit formula

The Rademacher formula gives an EXACT expression:

  p(n) = (1/(pi*sqrt(2))) * Sum_{k=1}^{infty} A_k(n) * sqrt(k) *
         d/dn [sinh(pi*sqrt(2(n-1/24)/3) / k) / sqrt(n - 1/24)]

where A_k(n) = Sum_{0<=h<k, gcd(h,k)=1} omega(h,k) * exp(-2*pi*i*h*n/k)
are Kloosterman-type sums, and omega involves Dedekind sums.

The connection to L-functions: The generating function is 1/eta(tau) where
eta(tau) = q^{1/24} * prod(1-q^n) is the Dedekind eta function, a modular form
of weight 1/2. But 1/eta is NOT an L-function in the standard sense. The zeros
of eta(tau) are not "nontrivial zeros of an L-function."

The Kloosterman sums A_k(n) involve exponential sums related to roots of unity,
not to zeros of an L-function on a critical line. There IS a connection to
L-functions through the theory of modular forms (the Petersson trace formula
relates Kloosterman sums to Fourier coefficients of automorphic forms), but this
connection is several levels of abstraction removed.

### 4c. Does the per-step spectroscope work?

NO, for structural reasons:

1. **No oscillatory main term:** Unlike M(x) which oscillates due to mu(n) being
   {-1, 0, +1}, the partition function p(n) is ALWAYS POSITIVE and grows
   exponentially. The per-step change q(n) = p(n) - p(n-1) is also always positive.
   There is no sign change to create interference/cancellation.

2. **No natural frequency variable:** In the Farey case, log(p) provides a natural
   frequency for prime p. For partitions, what plays this role? The index n itself
   is not naturally "logarithmic" in a way that connects to L-function zeros.

3. **Wrong asymptotic structure:** DeltaD(n) = q(n) ~ p(n)*pi/(2*sqrt(6n)), which
   is monotonically increasing (exponential growth with slowly decreasing ratio).
   This is the OPPOSITE of the oscillatory structure needed for spectroscopy.

4. **Rademacher terms are NOT indexed by L-function zeros:** The sum in the
   Rademacher formula is over k = 1, 2, 3, ... (moduli of Kloosterman sums),
   not over zeros rho. Each term contributes an oscillatory correction, but the
   "frequencies" are 2*pi*sqrt(n)/k, not gamma*log(n).

**One possible rescue:** The partition function modulo a prime p satisfies
congruences (Ramanujan). The Hecke operators connect these to L-functions of
modular forms. If we defined D(n) = p(n) mod p for a fixed prime p, then the
"explicit formula" might involve zeros of the L-function attached to the
corresponding modular form. But this is speculative and the per-step change
would be p(n) mod p - p(n-1) mod p, which oscillates, and MIGHT be amenable to
spectroscopy. This would require the full machinery of Ono's partition congruences.

### 4d. What hypothesis is needed?

N/A for the standard partition function. For the mod-p variant, GRH for the
associated modular L-function.

### 4e. Is this genuinely new?

The meta-theorem does NOT apply to standard partitions. The mod-p variant is
speculative but potentially interesting -- it would connect partition congruences
to L-function zeros via spectroscopy. I am not aware of this being proposed.

**Verdict: The meta-theorem DOES NOT APPLY to standard partitions. The partition
function grows too smoothly, has no sign changes, and its "explicit formula"
(Rademacher) is not indexed by L-function zeros. The mod-p variant deserves a
separate investigation (5-10 page computation to test feasibility).**

---

## CASE 5: RANDOM MATRIX EIGENVALUES

### 5a. The setup

S_N = spectrum of an N x N Hermitian matrix from GUE/GOE. "Insertion" via rank-1
perturbation: S_{N+1} = eigenvalues of (A_N + v*v^*) for random v. Discrepancy:

  D(S_N) = integral |rho_N(x) - rho_{sc}(x)| dx

where rho_N is the empirical spectral measure and rho_{sc} the Wigner semicircle.

### 5b. The explicit formula: does it exist?

The characteristic polynomial det(xI - A_N) satisfies:

  E[prod_{j=1}^N (x - lambda_j)] relates to Hermite polynomials (GUE)

The individual eigenvalue fluctuations around their expected positions are:

  lambda_j - E[lambda_j] ~ (1/N) * Sum_k c_{jk} * sin(k*theta_j)

where theta_j are the semicircle-law positions. But these fluctuations are NOT
governed by zeros of an L-function. The "explicit formula" in RMT is the
determinantal structure (sine kernel, Airy kernel), not a Dirichlet series.

**The Keating-Snaith connection:** The moments of the Riemann zeta function on
the critical line are modeled by moments of characteristic polynomials:

  E[|det(I - U)|^{2s}] = product formula involving Gamma functions

This connects RMT to zeta(s), but in the REVERSE direction: RMT models zeta,
not the other way around. There is no L-function whose zeros govern the spectrum
of a random matrix. The eigenvalues ARE the analog of the zeros.

### 5c. Does the per-step spectroscope work?

NO. The fundamental issue is categorical:

1. **No L-function:** Random matrices do not have an associated L-function. The
   eigenvalues are the objects analogous to L-function zeros, not to the arithmetic
   data (primes, Farey fractions) that generates L-function zeros.

2. **Wrong direction of analogy:** In the Farey case, we have:
   arithmetic data (Farey fractions) --[explicit formula]--> L-function zeros
   In RMT, the eigenvalues ARE the "zeros." There is no deeper layer of
   "arithmetic data" whose spectroscopy reveals the eigenvalues.

3. **Rank-1 perturbation is not arithmetic:** Adding a rank-1 perturbation to a
   random matrix changes eigenvalues by amounts governed by the Cauchy interlacing
   theorem and the resolvent. The per-step change in eigenvalues is:
   Delta_lambda_j ~ |<v, u_j>|^2 / (lambda_j - mu)
   where u_j are eigenvectors and mu is the new eigenvalue. This has Cauchy/Poisson
   structure, not Dirichlet series structure.

4. **The Montgomery-Odlyzko connection is NOT a "spectroscope":** The famous
   observation that zeta zero spacings match GUE eigenvalue spacings is a
   STATISTICAL match, not a spectroscopic detection. It says the zeros of zeta
   BEHAVE LIKE eigenvalues, not that eigenvalues are DETECTED BY a spectroscope
   applied to some arithmetic sequence.

### 5d. What hypothesis is needed?

N/A. There is no meaningful statement to make.

### 5e. Is this genuinely new?

The observation that the meta-theorem FAILS for RMT eigenvalues is itself
informative: it clarifies that the per-step spectroscopy phenomenon is intrinsically
ARITHMETIC, not just any "spectral" phenomenon. The three-way connection:

  Arithmetic data <--explicit formula--> L-function zeros <--statistics--> RMT eigenvalues

shows that spectroscopy lives in the LEFT arrow, while RMT lives in the RIGHT arrow.
The meta-theorem governs the left arrow. The right arrow is a separate phenomenon
(universality of eigenvalue statistics).

**Verdict: The meta-theorem DOES NOT APPLY. Random matrix eigenvalues are the
ANALOGUE of L-function zeros, not of the arithmetic data that generates them.
Applying spectroscopy to eigenvalues would be looking for "zeros of zeros" --
a category error.**

---

## SYNTHESIS: WHEN DOES THE META-THEOREM APPLY?

### The Three Necessary Conditions

The meta-theorem applies when:

**(C1) Arithmetic insertion rule.** The set S_N grows via an insertion determined
by arithmetic structure (primality, divisibility, lattice membership, etc.).
Crucially, the insertion rule must be multiplicative or additive in nature, so
that the generating Dirichlet series has an Euler product or modular structure.

- Farey: insertion at primes (Euler product for 1/zeta). CHECK.
- Lattice: r_2(n) = 4*Sum chi_4(d|n) (Euler product for zeta*L). CHECK.
- CF convergents: insertion governed by partial quotients (no Euler product). FAIL.
- Partitions: insertion at every n (generating function is eta, not Euler product). FAIL.
- RMT: insertion is random perturbation (no arithmetic). FAIL.

**(C2) Explicit formula with L-function zeros.** The discrepancy D(S_N) must have
an explicit formula expressing it as a sum over nontrivial zeros of an L-function.

- Farey: M(x) = Sum_rho x^rho/(rho*zeta'(rho)) + .... CHECK.
- Lattice: E(R) involves Sum_rho (Hardy-Voronoi type). CHECK.
- CF convergents: No such formula exists. FAIL.
- Partitions: Rademacher series over k, not over zeros. FAIL.
- RMT: No L-function. FAIL.

**(C3) Per-step change isolates oscillation.** The per-step change DeltaD(N) must
be dominated by the oscillatory (zero-dependent) terms, with the smooth main term
differenced away or pre-whitened.

- Farey: DeltaW(p) ~ -B(p)/n'^2, and B(p) ~ mu*M(p), which oscillates. CHECK.
- Lattice: Delta E(n) = r_2(n) - pi, which oscillates (r_2 is 0 for most n). CHECK.
- CF convergents: DeltaD periodic for quadratic alpha, no oscillation. FAIL.
- Partitions: q(n) = p(n)-p(n-1) > 0 always, monotone increasing. FAIL.
- RMT: N/A. FAIL.

### Score:

| Case | C1 | C2 | C3 | Meta-theorem applies? |
|------|----|----|----|-----------------------|
| Farey | Y | Y | Y | YES |
| Lattice | Y | Y | Y | YES |
| CF convergents | N | N | N | NO |
| Partitions | N | N | N | NO |
| RMT | N | N | N | NO |

### Broader Applicability

Beyond the five cases analyzed, the meta-theorem should apply to:

1. **Stern-Brocot tree insertions:** Same as Farey (different enumeration order).
   L-function: zeta(s). Should detect the same zeros.

2. **Gaussian/Eisenstein integer Farey sequences:** Already explored in our
   Gaussian spectroscope work. L-functions: Dedekind zeta of Q(i) and Q(omega).
   Detects zeros of zeta(s)*L(s,chi_4) and zeta(s)*L(s,chi_3) respectively.

3. **Lattice points in ellipses:** a*x^2 + b*y^2 <= R^2 for positive-definite
   binary quadratic form. L-function: L(s, chi_D) for discriminant D of the form.
   The per-step spectroscope should detect zeros of the corresponding Hecke L-function.

4. **Divisor sum fluctuations:** D(x) = Sum_{n<=x} d(n) - x*log(x) - (2*gamma-1)*x.
   Dirichlet divisor problem. Explicit formula involves zeta zeros (Voronoi formula).
   Per-step: Delta D(n) = d(n) - log(n) - 2*gamma + 1. The spectroscope
   F(gamma) = |Sum d(n)*n^{-s}|^2 ~ |zeta(s)|^4 detects zeros of zeta^2(s), i.e.,
   the same zeros with doubled multiplicity. This IS known (Voronoi/Atkinson).

5. **Prime-counting function:** pi(x) - Li(x). Explicit formula involves zeta zeros.
   Per-step: Delta = 1 if x is prime, -1/log(x) correction. The spectroscope is
   essentially the prime zeta function, which DOES detect zeta zeros (this is
   classical via the explicit formula for psi(x)). NOT new.

---

## THE GENUINELY NEW CONTRIBUTION

The meta-theorem as stated is new in the following sense:

**WHAT IS CLASSICAL:** The explicit formula (Riemann, von Mangoldt, Hardy, Voronoi)
connects various counting functions to L-function zeros. The Fourier duality
between primes and zeros is classical. The estimation paradigm (Turan, Montgomery,
Selberg) uses these formulas to bound error terms.

**WHAT IS NEW (our work):**

1. **The per-step paradigm.** Studying DeltaD instead of D. This is not standard in
   analytic number theory. The four-term decomposition of DeltaW is entirely new.

2. **The spectroscopic paradigm.** Treating DeltaD as a TIME SERIES and applying
   signal-processing techniques (pre-whitening, periodogram, local z-score) to
   DETECT individual zeros, rather than BOUNDING the error term. This is a
   paradigm shift from estimation to detection.

3. **The gamma^2 pre-whitening.** The specific weight gamma^2 that removes the
   1/gamma^2 decay of the spectral power (from the 1/rho factor in the explicit
   formula). This is a signal-processing insight, not a number-theory insight.

4. **The meta-theorem itself.** The recognition that conditions C1-C3 delineate
   a CLASS of problems where per-step spectroscopy works, and the systematic
   analysis of which classical problems fit.

5. **The Gaussian extension.** Demonstrating that the spectroscope extends to
   Dedekind zeta functions of number fields, simultaneously detecting zeros of
   multiple L-functions (Section 2 above and M1_GAUSSIAN_FAREY_SPECTROSCOPE.md).

---

## WHAT SHOULD BE DONE NEXT

### Immediate (computation, 1-2 hours each):

1. **Lattice point spectroscope:** Implement F_2(gamma) for r_2(n) up to n = 10^6.
   Verify peaks at both zeta zeros (14.13, 21.02, ...) and L(s,chi_4) zeros
   (6.02, 10.24, ...). Compare with the Gaussian Farey spectroscope -- they should
   match because r_2(n) and the Gaussian Mertens function encode the same L-functions.

2. **Divisor spectroscope:** Implement F_d(gamma) for d(n) - log(n). Verify it
   detects zeta zeros. Compare SNR with the Farey spectroscope. The divisor
   spectroscope should be NOISIER because d(n) is not multiplicative in the same
   sign-changing way as mu(n).

3. **Partition mod 5 spectroscope:** Implement p(n) mod 5 for n up to 10^5 and
   compute the spectroscope. Check whether any peaks appear at zeros of the
   modular L-function associated to the eta-quotient eta(5*tau)/eta(tau).

### Medium-term (theory, weeks):

4. **Rigorous proof for the lattice case (Case 2).** The Hardy-Voronoi formula
   is well-established. Proving that the per-step spectroscope detects zeros
   should be a straightforward (if technical) exercise paralleling the Farey proof.
   This would give a second instance of the meta-theorem.

5. **Write the meta-theorem section for the paper.** This should be Section 7 or 8:
   "Universality of per-step spectroscopy." State the meta-theorem, give Farey and
   lattice as examples, explain why partitions and RMT fail.

### Long-term (open problems):

6. **Can the meta-theorem be made unconditional?** Currently requires GRH. Is there
   a weaker statement (e.g., "the spectroscope detects at least one zero in any
   interval [T, T+1]") that can be proved unconditionally? The Ingham-type
   mean-square results suggest this is possible.

7. **Does the meta-theorem extend to automorphic L-functions?** For GL(3) or higher,
   the counting problems involve lattice points in higher-dimensional regions
   (e.g., number of ways to write n as a sum of three squares involves L-functions
   of weight 3/2 modular forms). The per-step spectroscope for r_3(n) should detect
   zeros of these higher L-functions. But the octahedral symmetry obstruction
   (found in SPHERE_EXTENSION_ANALYSIS.md) may complicate this.

---

## REFERENCES

Classical explicit formulas:
- Riemann (1859): Explicit formula for pi(x) involving zeta zeros
- von Mangoldt (1895): Explicit formula for psi(x)
- Hardy (1915): Lattice point explicit formula (Voronoi summation)
- Rademacher (1937): Exact formula for p(n) via circle method

Per-step spectroscopy (our work):
- Farey spectroscope: farey_spectroscope.py, DEEP_DELTAW_EXPLICIT_FORMULA.md
- Gaussian extension: gaussian_spectroscope.py, M1_GAUSSIAN_FAREY_SPECTROSCOPE.md
- Chebyshev bias: SESSION10_HANDOFF.md (DeltaW phase-lock to gamma_1)
- Other increments: INCREMENTS_OTHER_PROBLEMS.md
- Prior art: M5_GEMMA_TURAN_PRIOR_ART.md, LOCAL_G4_SPECTROSCOPE_PRIOR_ART_DEEP.md

Spectroscopy vs estimation paradigm:
- OPUS_SPECTROSCOPE_DIRECT_AND_POLE_AVOIDANCE.md (obstruction analysis)
- OPUS_RH_PATH_VIA_CANCELLATION.md (what the cancellation proves)
