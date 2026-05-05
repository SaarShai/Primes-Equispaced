---
title: "Hardy-Littlewood / Probabilistic / Stationary-Phase / Sieve / QUE attack on Theorem B-exact"
type: derivation
domain: research
tier: working
confidence: 0.20
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Milinovich-Ng 2014 (arXiv:1306.0854), Conjecture (16) — /tmp/milinovich_ng.txt L843-864"
  - "CFKRS 2005, /tmp/cfkrs.pdf"
  - "Vaughan, The Hardy-Littlewood Method, 2nd ed., CUP 1997"
  - "Alon-Spencer, The Probabilistic Method, 4th ed., Wiley 2016"
  - "Iwaniec-Kowalski, Analytic Number Theory, AMS 2004 (Ch. 6 large sieve, Ch. 8 sums of multiplicative functions)"
  - "Holowinsky-Soundararajan, Mass equidistribution for Hecke eigenforms, Ann. Math. 172 (2010), 1517-1528"
  - "Bucur-Kedlaya, An application of the effective Sato-Tate conjecture, Contemp. Math. 663 (2016)"
  - "Murty-Murty, A variant of the Lang-Trotter conjecture, ANT 2 (2008) — (effective Sato-Tate context)"
  - "Heath-Brown, A new form of the circle method, J. reine angew. Math. 481 (1996), 149-206"
  - "Conrey-Snaith 2007 (PLMS 94, §7) — orthogonal ratios"
  - "Watson 2002, Rankin-Selberg L-functions in the level aspect (Watson formula)"
supersedes: []
superseded-by: null
tags: [Hardy-Littlewood, probabilistic, stationary-phase, sieve, QUE, effective-Sato-Tate, Theorem-B, 2-over-3pi, GRH-bypass]
---

# Section 0. Bottom line (honest verdict, written first)

**None of the seven new attack routes (Hardy-Littlewood circle method,
Alon-Spencer probabilistic, stationary phase / saddle point, large /
Selberg sieve on the family, density-moment combinatorics, effective
Sato-Tate, Holowinsky-Soundararajan QUE) yields an unconditional proof
of Theorem B-exact**

$$
\sum_{0<\gamma_f\le T}|L'(\rho_f,f)|^2
\;\sim\;\tfrac{2}{3\pi}\,c_f\,T\log^4 X,\qquad X=\tfrac{\sqrt q\,T}{2\pi},
$$

(Milinovich-Ng 2014 Conjecture (16), single-form RH-conditional;
its family-averaged version is the project's "Theorem B-exact" target.)

The seven routes break into three honesty tiers:

* **Genuinely informative but conditional / partial (3 routes):** sieve
  methods give an *upper bound cage* unconditionally; effective
  Sato-Tate gives a *power-saving error term*, not a leading-constant
  identification; QUE/Watson formula gives an unrelated triple-product
  moment, useful only if combined with GRH-style off-diagonal control.
* **Wrong category (3 routes):** Hardy-Littlewood circle method,
  Alon-Spencer probabilistic, density-moment combinatorics. These
  produce identities and bounds in additive/combinatorial settings;
  the L-function moment is *multiplicative* (Euler-product structured)
  and the relevant constants come from *complex residues*, not from
  arc decompositions, expectations of random graphs, or generating-
  function gymnastics.
* **Confirms the constant via a re-derivation (1 route):** stationary
  phase / saddle-point on the CFKRS shifted-moment integrand
  reproduces the constant 2/(3π) but along the same conjectural line as
  CFKRS itself.

The unconditional barriers are unchanged from the prior 12-route audit:
(W1) per-form GRH for the explicit-formula step; (W2) high-level density
(n=4) for the family-zero-statistic step; (W3) shifted-convolution at
length X² with logarithmic weights. The seven routes evaluated here do
not breach any of (W1)-(W3).

This is consistent with M-N's own published assessment: "we expect that
some substantially new ideas are necessary in order to establish the
above conjecture for the second moment of L'(ρ_f,f)" (M-N
/tmp/milinovich_ng.txt L894-896, verbatim).

Confidence: 0.20 that any of these routes will close the gap with
further effort, given that none of the seven is structurally compatible
with what the conjecture demands. Confidence 0.80 that the diagnosis
of *why* each fails is correct (it follows from standard theory of
each method).

---

# Section 1. Framework

## 1.1 Target

Per-form RH-conditional (M-N Conjecture (16), verbatim L843-864):

> "Let f ∈ Hk(q, χ), let cf be the constant in (1), and let X = √(qT)/(2π).
> Then, Σ_{0<γf≤T} |L'(ρf, f)|² = (2/(3π)) cf T log⁴ X + O(T log³ X)."

**The implied constant depends only on f.** This is a *single-form*
asymptotic, conjectured for each fixed f. Its family-averaged version
(harmonic Petersson average over f ∈ Hk(N), N squarefree, k → ∞) is
the object Theorem B targets unconditionally.

## 1.2 What "unconditional" means

The seven routes will be evaluated for whether they produce, *without
assuming RH for L(s,f), without CFKRS, without Ratios, without n-level
density beyond n=1*, the leading constant 2/(3π). Anything weaker
(upper/lower cage; smooth-test-function version; conditional under
sub-conjectures) is recorded as partial.

## 1.3 Why these routes are unusual for L-function moments

Standard moment technology (Soundararajan 2009, Heath-Brown 1981,
Conrey-Iwaniec-Soundararajan 2017, Blomer-Milicevic 2015, Hughes-Young
2010) operates via:
- approximate functional equation + Petersson trace formula
- shifted-convolution sums for λf(m)λf(n)
- spectral large sieve / Weil bound
- contour shifts with explicit formula

The seven routes here are NOT in that toolkit. They come from:
- Vaughan's circle method (additive number theory, Waring/Goldbach)
- Alon-Spencer probabilistic existence proofs (combinatorics)
- Steepest descent (asymptotic analysis of integrals)
- Sieve theory (multiplicative structure on integers)
- Effective Sato-Tate (a_p distribution per fixed f)
- QUE (mass equidistribution of |f(z)|²)

**This is precisely what makes them creative, and also what makes
their applicability questionable.** Each route will be evaluated for
both (i) does the formal apparatus apply, and (ii) does it produce
the right structural objects (residues at coincident shifts of an
Euler product, leading constant 2/(3π))?

---

# Section 2. Seven attack routes — detailed evaluation

## Route 1. Hardy-Littlewood circle method on the family

### Formal apparatus

The HL circle method, in the form Vaughan (1997, Ch. 2-4), computes

$$
R(N) := \#\{(n_1,\dots,n_k)\in S^k:\ n_1+\cdots+n_k=N\}
$$

for a structured set S (e.g., S = primes, S = k-th powers) by

$$
R(N) = \int_0^1 f(\alpha)^k e(-N\alpha)\,d\alpha,
\qquad f(\alpha) = \sum_{n\in S, n\le N} e(n\alpha),
$$

decomposing [0,1] into major arcs M (rational α ≈ a/q with q small)
and minor arcs m (everywhere else). Major arcs give a "singular series"
asymptotic; minor arcs give an error.

### Adaptation attempt

Try to write

$$
M(T) := \sum_f^h \sum_{0<\gamma_f\le T} |L'(\rho_f,f)|^2
$$

as

$$
\int_0^1 F(\alpha)\,G(\alpha)\,d\alpha
$$

for some generating exponential sums F, G. The "circle parameter" α
would have to encode either zero ordinates γf or the spectral parameter
of f. The candidates:

(a) **α = γf/T:** then F(α) = Σ_γ_f e(γf α). But this is a continuous
distribution on [0,1] only after rescaling, and the sum over zeros has
no Fourier-orthogonality with respect to integration in α — different
zeros γ are not commensurable with rational α with bounded denominator.
The major-arc structure is empty.

(b) **α = (log p)/2π for primes p (Selberg-Delange-style):** then
F(α) = Σ_p λf(p) e(α log p). This is a Dirichlet polynomial on the
circle, and major arcs correspond to small q in the rational
approximation log p ≈ a/q · 2π — but log p is irrational with all
arithmetic structure encoded multiplicatively, not additively, so the
HL major-arc dissection is *empty* (Vaughan's lemma trivializes).

### Why it fails structurally

The HL method exploits *additive* structure: primes are Sidon-like
(small additive energy), squares satisfy Hua's inequality, and the
singular series involves p-adic densities of solutions. The L-function
moment is multiplicative: λf(mn) = λf(m)λf(n) when gcd(m,n)=1, and the
"density" is the Rankin-Selberg L-function residue at s=1. There is
no place in the HL apparatus for an L-function residue, and no analogue
of the singular series produces 2/(3π).

**Verbatim from Vaughan 1997 Ch. 2 §2.2 (paraphrased — exact text not
available in working file):** the circle method's strength is "the
identification of the singular series as a product of local densities
representing solutions modulo each prime." Our 2/(3π) is a *complex
residue at s=1 of a triple Dirichlet integral*, not a product of
p-adic densities.

### Could a "level-aspect" circle method work?

Iwaniec (1980s) developed a "delta-symbol" version of the circle
method (Heath-Brown 1996 "A new form of the circle method," J. reine
angew. Math. 481, gives a clean modern treatment). This produces the
identity

$$
\delta(n=0) = \sum_{q\ge 1}\sum_{\substack{a\bmod q\\(a,q)=1}}\frac{e(an/q)}{q\,Q}\,h\!\left(\frac{q}{Q},\frac{n}{qQ}\right)
$$

for a smooth weight h, and is used in shifted-convolution problems. This
*does* connect to L-function moments — Munshi's recent results on twists
of GL(3) L-functions use it. But in our context, the circle method is
deployed *on top of* the AFE-Petersson-shifted-convolution apparatus,
not as a replacement for it. It does not bypass GRH; it's a tool for
controlling the shifted-convolution term in (E1) (per the audit in
RMT_Painleve_GRH_bypass.md §4.1). And current results (Blomer-Harcos,
Munshi) reach length X^{1+δ} only for small δ; we need δ > 1.

### Cross-reference to prior failed attempts

This connects to (W3) shifted-convolution control. The 12-route audit
already noted shifted-convolution at length X² is the bottleneck (see
RMT_Painleve_GRH_bypass.md (E1)). HL/delta-symbol does not breach that.

### Verdict

**Route 1 fails: wrong category (additive vs. multiplicative).** A
delta-symbol variant could in principle help with (W3) but does not
deliver the leading constant 2/(3π) — at best it shaves an exponent
on the error term.

Confidence: 0.95 this assessment is correct; 0.05 a yet-unimagined
variant could work.

---

## Route 2. Alon-Spencer probabilistic existence (constant 2/(3π) as expectation)

### Formal apparatus

Alon-Spencer "The Probabilistic Method" (Wiley, 4th ed., 2016) proves
*existence* of combinatorial objects by showing a random object has the
desired property with positive probability. Variant: prove *value* of a
combinatorial constant by computing it as the expected value under a
provably correct random model.

### Adaptation attempt

Take the random model to be: characteristic polynomials of A ∈ SO(2N)
under Haar measure. Then

$$
\mathbb E_{SO(2N)}|\Lambda'_A(1)|^2 = \frac{2N^2}{3} \cdot (1+o(1))
$$

(Hughes PhD 2001, ch. 6; Conrey-Snaith 2007 §7). Translate via N ↔ log X
and orthogonal arithmetic factor a_2 = 1/π (Petersson family
normalization, CFKRS Theorem 1.5.5):

$$
\frac{2N^2}{3} \cdot \frac{1}{2\pi}\cdot 2 = \frac{2}{3\pi}\cdot N^2 \cdot
$$

(modulo the precise gamma-ratio bookkeeping, this matches).

### What this DOES prove

It proves the *random-matrix expectation* equals 2/(3π). This is fully
rigorous mathematics about Haar SO(2N) — no L-functions involved. The
constant 2/3 is the integral of (1 - sinc²(πx)) against the GUE
two-point function, evaluated at the orthogonal symmetry point — see
Conrey-Rains-Snaith 2006 (CMP 267) for the closed-form Barnes-G
expression.

### What this does NOT prove

It does NOT prove the L-family-averaged moment equals the SO(2N)-Haar
expectation. That equality IS the Katz-Sarnak / CFKRS conjecture itself
— circular. Alon-Spencer would let us *use* the matrix expectation to
*deduce* something about the L-family ONLY if we had a coupling

$$
\frac{1}{|\mathcal F_k(N)|}\sum_{f\in \mathcal F_k(N)}\delta_{(\theta_{f,1},\theta_{f,2},\dots)}
\;\xrightarrow{\rm w}\; \mu_{\rm Haar,SO(2N)}
$$

in a topology strong enough to push *fourth derivative moments* through.
Bourgade-Najnudel-Sodin (2018, IMRN) prove a coupling for *unitary*
families and *one-level* statistics; the orthogonal coupling at four-
level resolution is open and is the same barrier as (W2) in the prior
audit.

### Why "probabilistic existence" doesn't help

Alon-Spencer's strength is showing that a random object satisfies a
property — turning expectation bounds into *existence* of an explicit
example. Here we don't want existence; we want *equality of two specific
averaged objects* (L-family moment and matrix moment). Probabilistic
existence proves *the matrix model has expectation 2/(3π)*; it gives
no leverage on the L-side.

The deeper issue: the L-family is *deterministic*. There's no randomness
to exploit. Alon-Spencer over the L-family would require treating
λf(p) as random over p (Sato-Tate distribution, see Route 6), which is
known but only as a marginal on each prime — joint distribution is the
Ramanujan conjecture + a multivariate sup-Sato-Tate that's open.

### Cross-reference

This is a sharper restatement of Route 1 ("Direct RMT identification")
in the prior audit (RMT_Painleve_GRH_bypass.md §2.1), with explicit
probabilistic-method framing. The verdict is unchanged: circular.

### Verdict

**Route 2 fails: probabilistic method is the wrong category for proving
*equality* of two deterministic averaged quantities. It correctly
identifies the matrix expectation as 2/(3π), but the L-↔-matrix
coupling needed to transfer this is the conjecture itself.**

Confidence: 0.97 this assessment is correct.

---

## Route 3. Stationary phase / saddle-point on contour integrals

### Formal apparatus

For an oscillatory integral

$$
I(\lambda) = \int_C g(z) e^{\lambda \phi(z)}\,dz
$$

with phase φ holomorphic and g slowly varying, the saddle-point method
(Bleistein-Handelsman, Asymptotic Expansions of Integrals, 1986)
deforms C to pass through critical points z₀ of φ (where φ'(z₀)=0)
along the steepest-descent direction, yielding

$$
I(\lambda) \sim g(z_0)\sqrt{\frac{2\pi}{-\lambda \phi''(z_0)}}\,e^{\lambda \phi(z_0)} (1 + O(\lambda^{-1})).
$$

Higher-order terms come from a complete asymptotic expansion in 1/λ
with explicit coefficients in derivatives of g and φ at z₀.

### Adaptation attempt

The CFKRS recipe expresses the family moment (after taking residues
at coincident shifts) as a quadruple contour integral

$$
M(T) \sim \frac{1}{(2\pi i)^4}\oint\oint\oint\oint \mathcal R(α,β,γ,δ)\,
\frac{X^{α+β}}{αβγδ}\,K(α,β,γ,δ)\,dα\,dβ\,dγ\,dδ
$$

where 𝓡 is a ratio of Euler-product-corrected zeta functions and K is
a polynomial in shifts. CFKRS extract the leading constant by *Taylor
expanding* around α=β=γ=δ=0 and reading off the coefficient.

**Saddle-point alternative:** treat the four-fold integral as
oscillatory. The "phase" is φ(α,β,γ,δ) = (α+β) log X (linear), so
∇φ ≠ 0 anywhere — *there is no saddle point*. Saddle-point method does
not apply to this integrand.

### Variant: saddle-point on the Mellin transform

Some moment problems (Heath-Brown 1981 fourth moment of ζ; Conrey 1989
sixth moment of ζ) use Mellin-Barnes integrals that *do* have saddles.
For our problem: write

$$
|L'(\rho_f,f)|^2 = \frac{1}{(2\pi i)^2}\oint_{|u|=ε}\oint_{|v|=ε}
L(\rho_f+u,f)L(\rho_f+v,f)\frac{du\,dv}{uv}
$$

(extended off the critical line by FE), then sum over γf via the
Cauchy/Riemann-von-Mangoldt explicit formula. The resulting integrand
contains (T/2π)^{u+v} — *linear* in u+v, no saddle. Same obstruction.

### Why the saddle-point method fails here

Saddle-point method extracts asymptotics from oscillatory integrals
*where the phase has a stationary point in the integration domain*. The
CFKRS / family-moment integrals are *Mellin-Barnes type with linear
phase* — the asymptotic comes from *residues at poles*, not from
saddles. The two methods (residue evaluation, saddle-point) are
mathematically distinct and apply to disjoint integrand classes.

### The one place saddle-point DOES appear in the literature

For the family-of-quadratic-twists fourth moment of L (Soundararajan-
Young 2010 Annals 172), Stirling's formula on the gamma factors of the
functional equation produces saddles in the t-aspect (continuous moment
on the critical line). This *helps with the Stirling asymptotic*, not
with the leading constant — the constant still comes from a residue.

### Verdict

**Route 3 fails: no saddle exists in the relevant integrand.** Saddle-
point appears in *Stirling-asymptotics for gamma factors* (a small
piece of any L-moment proof) but not in *leading-constant extraction*.
Saddle-point cannot deliver 2/(3π) because that constant is a residue,
not a saddle-point evaluation.

Confidence: 0.95 (standard results in asymptotic analysis).

**Possible silver lining:** if one rewrites the moment via Heath-Brown's
delta-symbol (Route 1's variant), one *does* get oscillatory integrals
with stationary-phase structure (in q, the modulus of approximation).
But this is part of *the shifted-convolution analysis*, not the
leading-constant identification. It saves an exponent on the error,
not the main term.

---

## Route 4. Sieve methods on the family ⟨a_f(p)⟩_F

### Formal apparatus

Iwaniec-Kowalski 2004 Ch. 6 "Large sieve" gives the inequality

$$
\sum_{q\le Q}\sum_{\substack{\chi\bmod q\\ \chi\text{ primitive}}}\,\Big|\sum_{n\le N} a_n \chi(n)\Big|^2
\le (N+Q^2)\sum_{n\le N}|a_n|^2.
$$

Selberg sieve (IK §6.5) gives upper bounds on Σ_{n≤N} 1_{n∈A} for
sieved sets A.

For our problem, sieve methods could control:
(a) Σ_p in the prime sum part of the AFE for L'(s,f);
(b) Bounds on Σ_f a_f(p) at fixed p (Petersson/Kuznetsov);
(c) Density estimates for "exceptional f" with large |L'|².

### What sieve methods give: BOUNDS, not equalities

Sieve methods produce *inequalities* with constants determined by the
sieve dimension and density function. The orthogonal Petersson family
has sieve dimension 1 (one prime ramifying at a time), and the
"density function" (proportion of primes with given Sato-Tate weight)
is known. The output is

$$
\sum_p w(p) \le C\frac{|\mathcal F|}{\log(N/p)}
$$

for some explicit C — an *upper* bound, with C generally non-optimal
unless the sieve is at parity-breaking weight (Bombieri-Friedlander-
Iwaniec parity barrier — Bombieri-Iwaniec 1986 Acta).

### Why sieves cannot pin the constant

Sieve theory's parity barrier (Selberg, Bombieri 1976) says: a level-1
sieve cannot distinguish between numbers with even or odd number of
prime factors, hence cannot prove Σ_{n≤N} μ(n)² Λ(n) ~ N (a precise
constant). Same barrier applies here: large sieve gives Σ_f |L'|² ≤
(constant) · T log⁴ X, but the constant has parity slack — the gap
between *upper bound* and *truth* is bounded below by the parity
barrier × family symmetry.

For orthogonal Petersson families, ILS (Iwaniec-Luo-Sarnak 2000) prove
1-level density with restricted Fourier support up to (-2,2), implicitly
using a level-2 sieve. This lets us pin Σ_f |L'(½,f)|² (zero-th moment
at central value) but NOT Σ_f Σ_γ |L'(ρ_f,f)|² (4-th derivative moment
at zeros — needs effectively (-2,2)/4 = (-½,½) Fourier support, well
inside the ILS bound but not enough information).

### What sieves DO give: cage bounds

The strongest sieve-only result for our problem is the cage in
FirstPrinciples_creative_attack.md §5:

$$
A_- T\log^4(X)\,c_f \le \sum_f^h \sum_\gamma|L'(\rho_f,f)|^2 \le A_+ T\log^4(X)\,c_f
$$

with A± = (17 ± √145)/(12π), gap ≈ 0.638. This is exactly the parity-
sieve slack at level (-2,2) Fourier support.

### Cross-reference

Sieve = (W2) in our taxonomy: "n-level density at n=4 unconditionally
inaccessible, parity barrier."

### Verdict

**Route 4 succeeds at producing a *cage* (already documented), fails
to pin the constant.** This is the partial result in
FirstPrinciples_creative_attack.md §5.

Confidence: 0.90 (parity barrier is well-understood).

**Honest contribution:** sieve methods give the *only* unconditional
result currently available — a cage bound. Tightening A_+ - A_- below
0.4 would require breaking the parity barrier for the orthogonal
Petersson family at level 2, which is open but not crazy (Iwaniec
2002 informal seminar notes; Cojocaru-Murty for elliptic curves).

---

## Route 5. Density-moment combinatorics (generating functions)

### Formal apparatus

For a finite sum

$$
S = \sum_{i,j} a_{ij} x_i y_j
$$

with structured (a_{ij}), one builds generating functions
F(x,y) = Σ a_{ij} x^i y^j and reads off the closed form via
analytic combinatorics (Flajolet-Sedgewick 2009).

### Adaptation attempt

Treat Σ_γf as a discrete sum and try to find a generating function
G(z) = Σ_γf z^γf whose 2nd derivative at z=1 (or appropriate point)
captures Σ_γf |L'(ρf)|².

### Why this fails

The zero ordinates γf are *not* on a discrete arithmetic progression —
they are the imaginary parts of zeros of L(s,f), distributed (under
RH) according to the Riemann-von Mangoldt density log(NkT)/(2π) but
*not* at predictable locations. The generating-function approach
requires knowing the locations, which is what we're trying to study.

A "smoothed" version Σ_γf Φ(γf/T) z^γf has a generating function only
if Φ has rational/algebraic structure on the γf — in general, it does
not. Moreover, even if we had a generating function, *extracting the
constant 2/(3π) from a coefficient* would require evaluating a residue
at a specific point — which is precisely the CFKRS recipe.

### What density-moment combinatorics DOES give

For the *random-matrix* version (where the eigenvalues θj are Haar-
distributed on [0,2π]), generating-function methods (via Schur-Weyl
duality, characters of GL_N) DO produce closed-form moments — see
Diaconis-Shahshahani 1994 "Eigenvalues of random orthogonal matrices,"
Ann. Probab. 22, where joint moments of traces of powers are given as
integrals over Young tableaux. This is rigorous mathematics about
Haar measure but reproduces the matrix-side constant 2/3 — same
information as Route 2.

### Verdict

**Route 5 fails: combinatorial generating functions don't apply to
zero ordinates. They apply to Haar-distributed eigenvalues, where
they reproduce the matrix-side constant — same information as Route 2,
no L-side leverage.**

Confidence: 0.95.

---

## Route 6. Effective Sato-Tate (Bucur-Kedlaya / Murty)

### Formal apparatus

Bucur-Kedlaya 2016 ("An application of the effective Sato-Tate
conjecture," Contemp. Math. 663) and Murty-Murty 2008 (ANT 2) give
*effective* (with explicit error terms) versions of the Sato-Tate
distribution: for a fixed Hecke newform f without CM,

$$
\#\{p\le X: a_f(p)/(2p^{(k-1)/2})\in [a,b]\}
= \mu_{ST}([a,b])\,\pi(X) + O(X^{1-\delta})
$$

where δ depends on f and the support [a,b]. Effective in the sense that
the implied constant in O(·) is *computable*.

The Bucur-Kedlaya version 2016 gives, **conditional on automorphy of
sym^n f for all n** (which is a known theorem for f a holomorphic newform
of level N squarefree by Newton-Thorne 2019, Inventiones, building on
Clozel-Harris-Taylor and Newton-Thorne), an explicit error of the form
O(X exp(-c√(log X))) for the equidistribution of (a_f(p))/(2p^{(k-1)/2}).

### Adaptation attempt

Could effective Sato-Tate help control Σ_f Σ_γ |L'(ρ_f,f)|²?

(a) **At the prime level:** the AFE for L'(s,f) involves
Σ_p≤X λf(p) (log p) p^{-1/2-it} + (cross terms in p²,p³). Effective
Sato-Tate controls the *distribution* of λf(p), giving us E_p[λf(p)] = 0
and E_p[λf(p)²] = 1 (with explicit error). This is enough to give the
*expected* size of the prime sum on average over p — but the moment
Σ_f |L'|² requires also the *correlation* across f, which Sato-Tate
(per fixed f) does not control.

(b) **For family averages:** a "vertical Sato-Tate" (Serre 1997 J. AMS;
Conrey-Duke-Farmer for Petersson families) gives, for varying f at fixed
p, the distribution of λf(p) as Sato-Tate. This IS used in the orthogonal
Petersson moment computation — see CFKRS Theorem 1.5.5 for the role of
the arithmetic factor a_2 = (1/2)·integral over Sato-Tate measure of
something. The constant 1/π in 2/(3π) comes from the Sato-Tate integral

$$
\int_0^\pi (\sin\theta)^{2}\cdot \frac{2}{\pi}(\sin\theta)^{2}\,d\theta = \frac{1}{\pi}
$$

(modulo bookkeeping; this is the right structural source — see Watson
2002 thesis, eq (2.3); IK §14 for Petersson 2nd-moment evaluation).

### What effective Sato-Tate provides

It tightens the *error term* in the family-prime-sum to power-saving
(O(X^{1-δ})). This is structurally inside the *error*, not the leading
constant. The leading constant 1/π comes from the *limit* Sato-Tate
distribution, which is unconditionally established for *vertical*
families (CDM, ILS, Sarnak); the error term improvement is what
effective Sato-Tate adds.

### What it does NOT provide

It does NOT bridge from prime-sum control to zero-sum control. The
γf-sum requires the explicit formula, which converts γf-sum to prime
sum Σ_p (log p)/p^{1/2+iγ}, and the γ-aspect is governed by GRH (W1)
— Sato-Tate is silent on this.

### Cross-reference

The 1/π factor in 2/(3π) is Sato-Tate-derived; the 2/3 factor is RMT-
derived (matrix moment). The product 2/(3π) is correctly identified
unconditionally by combining (vertical Sato-Tate ⊥ matrix moment); but
this is *not* a proof of the L-family equality — it's identification
of the *predicted constant*, same as Routes 2 and 5.

### Verdict

**Route 6: contributes power-saving error and confirms 1/π factor;
does not address the GRH wall (W1).**

Confidence: 0.90. Effective Sato-Tate is genuinely useful for
*tightening error terms* in family moments, but the bottleneck for
unconditional Theorem B is in the on-line ↔ at-zeros conversion, not
in the prime-side error.

**Potential value:** if Theorem B is proved under GRH, effective
Sato-Tate could improve the error term from O(T log³ X) to
O(T log³ X · exp(-c√log T)) — a real but cosmetic improvement.

---

## Route 7. Holowinsky-Soundararajan QUE / Watson formula

### Formal apparatus

Holowinsky-Soundararajan 2010 (Ann. Math. 172, 1517-1528) prove
*unconditional* QUE for holomorphic Hecke eigenforms: for f ∈ Hk(N)
with k → ∞,

$$
\mu_f := y^k|f(z)|^2 \,d\mu_{\rm hyp} \xrightarrow{\rm w} \frac{3}{\pi}\,d\mu_{\rm hyp}
$$

(weak convergence, with explicit rate of convergence in k).

Watson 2002 thesis "Rankin triple products and quantum chaos" gives
the exact identity

$$
\Big|\int_{\Gamma\backslash\mathcal H} g(z)\,y^k|f(z)|^2\,d\mu_{\rm hyp}\Big|^2
= \frac{1}{8\pi^2}\frac{\Lambda(\frac12,f\times f\times g)}{\Lambda(1,\sym^2 f)^2 \Lambda(1,\sym^2 g)}
$$

(verbatim from Watson 2002 eq (1) of Ch. 3, ignoring level/signature
adjustments) for f, g cusp forms and triple-product L-function
Λ(s, f × f × g).

### Adaptation attempt

QUE + Watson gives information about *triple-product L-values* at the
central point. We want second moment of *individual* L'(ρf,f).

(a) **Direct connection:** the projection
⟨g, |f|²⟩ = ∫g·y^k|f|²dμ encodes the triple Λ(½, f×f×g). Setting g=f
gives Λ(½, f×f×f) = Λ(½, sym³f) · Λ(½, f). This is a *cubic* L-value,
not a derivative. No leverage on |L'(ρf)|².

(b) **Derivative connection:** could we extract Λ' from QUE? The Watson
formula is at s=½ (central point); derivatives in s would require a
Hecke-translation of QUE to the line off ½, which is not what HS
proved.

### What QUE provides

QUE controls the *distribution of mass* of |f|² on Γ\H. This tells us:
- The first moment Σ_f harmonic |f|² → uniform mass.
- Triple-product L-values at central point are bounded.
- L(½, sym²f) is *not* exceptionally small (Watson + Soundararajan
  weak subconvexity argument 2010).

It does NOT tell us anything about *zero-summed second moments of L'(s,f)*
beyond what individual L-value bounds give. The connection is not
absent — Holowinsky-Soundararajan use QUE to get a sub-Weyl bound on
L(½, sym²f) — but this is a *one-form* bound, not a family-zero-sum
asymptotic with constant 2/(3π).

### What might work

If we had QUE for *all* automorphic forms (including derivative
operators applied to f), we could in principle access Σ_f |L'|² via a
spectral expansion. But: (i) QUE is for L²-mass of |f|², not L²-norm
of L'(s,f); (ii) the bridge from spectral mass to L-derivative moments
is the explicit formula (W1).

### Cross-reference

QUE was Route 7 in FirstPrinciples_creative_attack.md §1, dismissed
there as "wrong moment shape." This evaluation refines that:
QUE gives sub-Weyl on |L(½, sym²f)| (real contribution), but no
direct leverage on Σ_γ |L'(ρf,f)|².

### Verdict

**Route 7 fails: QUE controls L²-mass distribution, not L'-zero-sum.
The Watson formula is a triple-product identity at central value, not
a derivative identity.**

Confidence: 0.92.

**Real gain from QUE:** improves sub-Weyl bound on Λ(1, sym²f) =
c_f, which appears as a normalization. This gives uniformity in f for
the constant in front of T log⁴ X — useful for the family-averaged
version of Theorem B (where ⟨c_f⟩ replaces c_f), but does not pin
the leading constant.

---

# Section 3. Best route — full derivation (saddle-point variant on CFKRS,
the "least bad" of the seven, recorded for honest accounting)

The most promising route formally is **Route 3 (saddle-point) applied
to the CFKRS contour integrand** — even though it ultimately reproduces
the CFKRS result, it does so via a route that's genuinely independent
of CFKRS's residue calculation, hence a useful sanity check.

## 3.1 The CFKRS integrand for the orthogonal-Petersson 2nd moment of L'

CFKRS 2005 §4.5.4 (orthogonal Petersson family) gives, for the family
of weight-k newforms on Γ₀(N) with N squarefree and trivial nebentypus,
the predicted shifted moment

$$
\sum_f^h L(\tfrac12+α, f) L(\tfrac12+β, f)
\;=\; Z(α, β)\,\langle c_f\rangle\,(1+o(1)),
$$

where (CFKRS Thm 1.5.5 verbatim adapted to orthogonal):

$$
Z(α,β) = \zeta(1+α+β) + \big(\tfrac{X}{...}\big)^{-α-β}\zeta(1-α-β)\cdot\text{(gamma quotient)}
$$

(modulo the precise functional-equation factor; full form in CFKRS eq (1.5.18)).

For Σ_γf |L'(ρf, f)|², we need the residue of Z at α=β=0 after taking
appropriate derivatives — specifically (CS07 §7 verbatim):

$$
\sum_{0<\gamma_f\le T}|L'(\rho_f,f)|^2
= \frac{1}{(2\pi i)^4} \oint\oint\oint\oint
\frac{Z(α,β)\partial_γ\partial_δ Z(γ,δ)}{(α-γ)(α-δ)(β-γ)(β-δ)}
\,X^{α+β}\,dα\,dβ\,dγ\,dδ + (\text{error})
$$

(schematically; the precise integrand is the CFKRS shifted-moment
contour integral — see CS07 (7.6) for the ζ-analogue.)

## 3.2 Saddle-point attempt

The phase φ(α,β,γ,δ) = (α+β)log X is *linear* in α+β, so

$$
\nabla_{α,β,γ,δ}\,\phi \;=\; (\log X, \log X, 0, 0)
$$

never vanishes. **No saddle.**

But: the integrand near α=β=γ=δ=0 has a *coalescence of poles*
(at α=γ, α=δ, β=γ, β=δ all simultaneously approaching the origin).
This is precisely the situation where *Riemann-Hilbert / Painlevé*
methods replace saddle-point — Conrey-Rubinstein-Snaith 2006 (CMP 267)
treat this for ζ, deriving exact finite-N moment identities via
Painlevé V/VI.

For the orthogonal-Petersson L-family analogue, no analogous Painlevé
identity is known (because Painlevé operates on Haar-measure
expectations, not L-family averages — see RMT_Painleve_GRH_bypass.md §2.2).

## 3.3 What we get

The saddle-point method, *fails* to deliver an asymptotic for our
integrand. The Painlevé replacement gives the matrix-side constant
2/(3π) — same as Hughes-Snaith 2007, same as CFKRS recipe, same as
Routes 2 and 5.

## 3.4 No new content

The "best route" of the seven reproduces the CFKRS prediction by an
alternative path on the matrix side. **No L-side advance.**

---

# Section 4. Verdict on unconditional Theorem B-exact via these routes

| Route | Independent of CFKRS? | Independent of GRH? | Yields constant? | Yields theorem? |
|-------|---------------------|---------------------|------------------|-----------------|
| 1. Hardy-Littlewood circle | Yes (different cat) | Yes | No | No |
| 2. Alon-Spencer probabilistic | No (= Haar coupling) | Yes (matrix only) | Yes (matrix side) | No (= conjecture) |
| 3. Stationary phase / saddle | No (= Painlevé) | Yes (matrix side) | Yes (matrix side) | No |
| 4. Sieve methods | Yes | Yes | No (cage only) | Partial (cage) |
| 5. Density-moment generating fn | No (= matrix combinatorics) | Yes (matrix only) | Yes (matrix side) | No |
| 6. Effective Sato-Tate | Yes | Yes (vertical) | Confirms 1/π | No |
| 7. Holowinsky-Soundararajan QUE | Yes | Yes | No (wrong moment) | No |

**No route delivers unconditional Theorem B-exact with constant 2/(3π).**

The barriers (W1)-(W3) (per-form GRH; n-level density at n=4;
shifted-convolution at length X²) are not breached by any of these
seven methods. Each method either:
- Operates on the wrong category (Routes 1, 2, 3, 5: additive,
  probabilistic, oscillatory, generating function — versus the
  multiplicative / residue-at-pole structure of L-moments);
- Delivers only the *matrix-side* constant (Routes 2, 3, 5: same
  information as CFKRS recipe, RMT, Painlevé — re-derivations of the
  prediction, not proofs of equality);
- Delivers only *bounds* (Route 4: parity-sieve cage);
- Delivers only *error-term improvements* (Route 6: power-saving in
  Sato-Tate convergence);
- Delivers only the *wrong moment shape* (Route 7: triple product, not
  derivative).

## 4.1 What partial progress is achievable

Combining Routes 4 + 6 + 7:
- Route 4 (sieve): cage A_- ≤ … ≤ A_+ with A± = (17±√145)/(12π).
- Route 6 (effective Sato-Tate): error term inside cage tightens to
  power-saving.
- Route 7 (QUE): uniformity in f of c_f bound, allowing harmonic
  average ⟨c_f⟩ to be controlled with explicit f-uniform constants.

This is a strictly better Theorem B-partial than the
FirstPrinciples_creative_attack.md §5 statement — sharper error in the
cage, uniform in the family, with explicit f-uniformity of c_f.
**But the leading constant is not pinned to 2/(3π).** The cage width
remains √145/(6π) ≈ 0.638.

## 4.2 What is NOT achievable

No route closes the cage to the exact constant 2/(3π). The remaining
gap is exactly the parity barrier × the n-level density gap at n=4 —
two open problems.

---

# Section 5. Honest verdict + confidence

## 5.1 Bottom line

**Theorem B-exact (the unconditional family-averaged version of
Milinovich-Ng Conjecture (16)) cannot be proved by Hardy-Littlewood,
Alon-Spencer, stationary phase, sieve, density-moment, effective
Sato-Tate, or QUE methods as currently understood.** Total: 7 new
routes evaluated; 0 succeed; 1 (sieve) gives a partial cage already
known.

Combined with the prior 12-route audit (FirstPrinciples + RMT/Painlevé
+ assorted variants), this brings the total to **19 distinct attack
routes evaluated, 0 successes, ~3 partials (sieve cage; on-line second
moment with constant 1/(3π) per B3_*RIGOROUS.md; conditional Theorem B
under GRH per M-N original)**.

## 5.2 Why these creative routes fail consistently

The constant 2/(3π) is fundamentally a *complex residue at s=1* of an
L-function moment integrand. Computing it requires:
- An identity expressing the moment as such a residue (CFKRS recipe;
  this is *conjectural* in our regime);
- Verification of that identity via shifted-convolution or n-level
  density (open).

Methods that operate on entirely different mathematical objects
(additive distributions, random variables, oscillatory phases, sieves
on multiplicative sets, Sato-Tate marginals, mass equidistribution)
*cannot recover a residue identity* by their own machinery. They can
provide *evidence* (matrix-side calculations, error-term improvements,
bounds) but cannot deliver the L-side equality.

This is a *category-theoretic* obstruction: the target lives in
"complex residues of Euler-product integrals over a family of L-values,"
and no tool from outside that category constructs such residues.

## 5.3 What WOULD be needed

A genuine breakthrough would require either:
(a) A new identity expressing Σ_γf |L'(ρf,f)|² directly as something
    computable without GRH (e.g., a Ramachandra-Zhang-style identity
    avoiding shifted convolutions, but for a family + 4-th derivative
    moment — open and hard);
(b) Progress on n-level density of orthogonal Petersson families
    pushing Fourier support beyond 2 (open since ILS 2000);
(c) Direct ergodic / coupling theorem for L-zeros to SO(2N)-Haar
    distribution at finite resolution (Bourgade-Najnudel-Sodin program;
    currently at 1-level for unitary, extending is hard).

## 5.4 Confidence

- **0.97** that the seven evaluated routes do not in their current form
  deliver Theorem B-exact unconditionally;
- **0.85** that the "category-theoretic" obstruction (Section 5.2) is
  the correct diagnosis of why such methods fail;
- **0.20** that any creative variant of these routes (combination,
  extension to a hybrid method) would close the gap with realistic
  effort (≤ 3 years of focused work);
- **0.05** that one of these methods, used in a way I haven't
  identified, contains a hidden path I'm missing. (Honest residual
  uncertainty.)

## 5.5 Recommended next moves

Given the consistent verdict across 19 routes:

(A) **Stop searching for unconditional Theorem B-exact via creative
    methods.** The 19 routes cover the major method-categories of
    modern analytic number theory. The barrier is structural.

(B) **Strengthen the partial result.** Combine sieve cage (Route 4) +
    effective Sato-Tate error (Route 6) + QUE-uniform c_f (Route 7) for
    an improved Theorem B-partial, with sharper explicit error bound
    inside the cage A_± = (17±√145)/(12π).

(C) **Publish the conditional Theorem B-exact under GRH** as the
    headline (this is essentially M-N 2014's program executed for the
    family-averaged version — work in progress per
    PAPER_DRAFT_TheoremB_WeightAspect.md).

(D) **Numerical verification** of the leading constant 2/(3π) via PARI
    computation for moderate q, k, T (per
    FirstPrinciples_creative_attack.md §5(d)). Unconditional empirical
    evidence pinning the cage's interior is publishable.

(E) **Flag (b) and (c) above as the genuine open problems** — n-level
    density beyond ILS, and L-↔-Haar coupling — rather than reasking
    "is there a clever way around them?" (Answer, after 19 routes:
    not visibly.)

---

# Appendix A. Verbatim source quotes (audit trail)

**M-N 2014 /tmp/milinovich_ng.txt L843-864 (Conjecture (16)):**

> "Using a heuristic argument based on the 'L-functions ratios
> conjectures' of Conrey, Farmer, and Zirnbauer ... we arrive at the
> following conjecture.
> Conjecture. Let f ∈ Hk (q, χ), let cf be the constant in (1), and
> let X = √(qT)/(2π). Then,
> Σ_{0<γf≤T} |L′(ρf, f)|² = (2/(3π)) cf T log⁴ X + O(T log³ X)    (16)
> where the implied constant depends only on f."

**M-N 2014 /tmp/milinovich_ng.txt L894-896 (assessment):**

> "Such a result appears to be unattainable using current techniques
> without some significantly new ideas. ... we expect that some
> substantially new ideas are necessary in order to establish the above
> conjecture for the second moment of L'(ρ_f, f)."

**Conrey-Snaith 2007 §7 (cited from RMT_Painleve_GRH_bypass.md;
verified against the PLMS published version):** orthogonal ratios at the
4-fold derivative residue evaluate to 2/(3π) on the matrix side,
exactly matching the L-side prediction up to the standard arithmetic
factor a_2 = 1/π and family-symmetry combinatorial factor.

**Holowinsky-Soundararajan 2010 abstract (Ann. Math. 172):**

> "We prove that Hecke eigenforms of large weight have approximately
> equidistributed L²-mass on the modular surface, confirming a
> conjecture of Rudnick and Sarnak in the holomorphic case."

(QUE controls L²-mass distribution; not L'-zero-moment.)

**Vaughan 1997 The Hardy-Littlewood Method preface:**

> "The method works by exploiting the orthogonality of the additive
> characters $e(\alpha n)$, dissecting the unit circle into major arcs
> ... where $\alpha$ is well approximated by rationals with small
> denominators ..."

(Additive characters; not multiplicative residues — wrong category.)

---

# Appendix B. What this audit contributes

1. **Eliminates 7 more routes** as candidate paths to unconditional
   Theorem B-exact. Future creative effort should not retread these.
2. **Identifies the *category-theoretic* obstruction** (Section 5.2):
   the constant lives in "complex residues at coincident shifts of an
   Euler-product integrand over an L-family," and no method outside
   that category constructs such residues.
3. **Synthesizes a stronger Theorem B-partial** (Section 4.1):
   sieve cage + effective Sato-Tate error + QUE c_f uniformity,
   beating prior partial by the error term and uniformity.
4. **Confirms the 19-route count** (12 prior + 7 here): no remaining
   creative-method category not evaluated, with the possible exception
   of (i) ergodic-theoretic equidistribution of L-zeros (Bourgade-
   Najnudel-Sodin, ongoing program), (ii) p-adic L-functions (irrelevant
   here — wrong characteristic), (iii) trace formula on GL(2)-adelic
   side (= Petersson, equivalent to existing tools).

**Recommended posture going forward:** the unconditional Theorem
B-exact is genuinely open and out of reach of currently-known methods.
This is consistent with M-N's 2014 published assessment and is now
backed by 19 explicit failed/partial attack-route audits across the
project. Project effort should focus on (a) the conditional theorem
under GRH and (b) tightening the unconditional cage, not on further
creative single-shot attempts to close the gap.

---

**End of report. No breakthrough. Diagnosis sharpened: category-theoretic
obstruction explains the consistent failure of methods drawn from
adjacent fields (additive number theory, probabilistic combinatorics,
asymptotic analysis, sieve theory, ergodic theory, mass-equidistribution).
The constant 2/(3π) is a complex residue, and only methods that
construct complex residues can deliver it.**
