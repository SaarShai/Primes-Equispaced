---
title: "RMT / Painlevé route to unconditional 2/(3π) — feasibility audit"
type: derivation
domain: research
tier: working
confidence: 0.30
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Milinovich–Ng 2014 (arXiv:1306.0854), Conjecture (16) — /tmp/milinovich_ng.txt L846–864"
  - "Conrey–Farmer–Keating–Rubinstein–Snaith 2005 (CFKRS), /tmp/cfkrs.pdf"
  - "Conrey–Snaith 2007, PLMS 94, §7 (orthogonal ratios)"
  - "Hughes 2001 PhD thesis (Bristol); Hughes–Keating–O'Connell 2000"
  - "Conrey–Rubinstein–Snaith 2006 (Painlevé / moments of ζ', CMP 267)"
  - "Forrester 2010, Log-Gases and Random Matrices, PUP"
  - "Bourgade–Najnudel–Sodin / Najnudel 2018"
  - "Saksman–Webb 2020, Annals of Probability"
supersedes: []
tags: [RMT, Painleve, GRH-bypass, 2-over-3pi, Theorem-B, orthogonal, SO-2N]
---

# Bottom line (honest verdict, written first)

**The RMT / Painlevé route does NOT yield an unconditional proof of**

$$
\sum_{0<\gamma_f\le T} |L'(\rho_f,f)|^2 \sim \tfrac{2}{3\pi}\, c_f\, T\,\log^4 X
\qquad(X=\sqrt{q}T/(2\pi)),
$$

**the M–N (16) conjecture / "Theorem B" target. None of the five attack
routes closes the gap. What RMT *does* give, rigorously, is the *predicted
constant* 2/(3π) on the random-matrix side; it does not give the
L-function ↔ RMT *equality* unconditionally.** The bottleneck is the
same one CFKRS leaves open: matching the moment of an L-family to the
moment of an SO(2N) characteristic-polynomial ensemble at the level of
*leading asymptotic equality*, not just shape.

The honest status is: RMT supplies the **target constant** and an
**ansatz** (CFKRS recipe → 2/(3π)); converting the ansatz into a theorem
requires inputs we do not possess (off-diagonal shifted-convolution control
beyond Deligne / large-sieve, or a direct family-level coupling to the
matrix ensemble). Painlevé and multiplicative chaos do not improve this.

Sections 1–6 record exactly *why* each route fails and what would be
needed to close it.

---

## Section 1. RMT framework + L-function dictionary (what is rigorous, what is not)

### 1.1 Random matrix side (rigorous, finite-N)

For $A\in SO(2N)$ Haar-distributed, let
$\Lambda_A(z)=\det(I-Az)=\prod_{j=1}^N(1-e^{i\theta_j}z)(1-e^{-i\theta_j}z)$
be the characteristic polynomial. The relevant object is
$\mathbb E_{SO(2N)}\bigl[|\Lambda_A'(1)|^2\bigr]$ at the symmetry point.
By Hughes (PhD thesis 2001) and Conrey–Rubinstein–Snaith 2006 (these are
the standard references), the moments of $\Lambda_A'(1)$ over $SO(2N)$
(and $USp(2N)$, $U(N)$) are computable as ratios of Barnes $G$-functions
and **are exact for finite $N$** — no asymptotics needed on the matrix side.

For our problem the relevant value is the leading large-$N$ coefficient
$f_{\rm SO(even)}(2)$ in
$$\mathbb E_{SO(2N)}|\Lambda'_A(1)|^{2} \sim f_{\rm SO}(2)\, N^{2}.$$
The Hughes / Conrey–Snaith 2007 §7 evaluation gives a coefficient
which, once translated through the standard $N\leftrightarrow \log X$
dictionary $N=\log X$, produces a $(\log X)^{2}$ for the
*matrix-side analogue of the second moment of the derivative at a zero*.

**This part is rigorous mathematics about Haar measure.** No conjectures.

### 1.2 The dictionary (NOT rigorous)

The Katz–Sarnak / Keating–Snaith dictionary asserts that, for a family $\mathcal F$
of L-functions with symmetry type $G(N)$ ($U,USp,O,SO(\text{even}),SO(\text{odd})$),
the moments of L-values (and L-derivatives) at the symmetry point match
the corresponding moments of $\Lambda_A$ over $G(N)$, with $N\sim\log X$
and an arithmetic correction factor $a_k$:
$$
\frac{1}{|\mathcal F|}\sum_{f\in\mathcal F} |L^{(j)}(s_0,f)|^{2k}
\;\sim\; a_k \cdot \mathbb E_{G(N)}|\Lambda_A^{(j)}(1)|^{2k}\cdot (\log X)^{?}.
$$
**The $\sim$ here is conjectural.** It is supported by:

* CFKRS recipe — produces matching shape and (via residue computations)
  the same leading constant on both sides (when the recipe is run
  through to completion);
* All known unconditional moment theorems (Soundararajan, Heath-Brown,
  Conrey–Iwaniec–Soundararajan, Bui–Conrey–Young, etc.) — they verify the
  prediction in *low* moments and *limited* shifts;
* Numerical experiments to high precision (Rubinstein, Bober, et al.).

**It is not a theorem in any case where the moment exceeds what can be
evaluated by direct shifted-convolution analysis** (essentially, beyond
the second moment of $L$ for unitary families and the first moment for
orthogonal families, with derivatives adding further difficulty).

The M–N conjecture (16) — i.e. the second moment of $L'(\rho_f,f)$ summed
over zeros and over the orthogonal Petersson family — sits **strictly
beyond** the unconditional zone.

### 1.3 Why "summed over zeros" is harder, not easier

A common misreading: "RMT gives moments of $|\Lambda'(1)|^2$, which
is a moment at one matrix value — surely that is easier than a moment
over zeros." False. The L-side analogue is

$$ \int_0^T |L'(\tfrac12+it,f)|^2\,dt \quad\text{(continuous, on-line)}, $$

NOT $\sum_\gamma |L'(\rho,f)|^2$. The conversion between "on-line"
and "at-zeros" requires either:
(i) a Gonek-type explicit formula → off-diagonal shifted convolutions
that are beyond current technology for degree-2 derivatives, OR
(ii) a Stieltjes split + pair-correlation enhancement (this is what the
project's `B3_Lprime_2nd_moment_RIGOROUS.md` attempts).

RMT does NOT do this conversion for us. The matrix model has no analogue
of the explicit formula error — it just *posits* equality.

---

## Section 2. Five route candidates — diagnosis

### Route 1. Direct RMT identification at family level

**Claim:** prove $\sum_F |L'|^2 \to \int_{SO(2N)}|\Lambda'(1)|^2 d\mu$.

**Status:** open, equivalent to the M–N conjecture itself.
The "asymptotic equivalence" is what we want to prove — restating it
as "couple the L-family to Haar SO(2N) and pass to the limit" does not
introduce any new tool. Bourgade–Najnudel–Sodin's family-level work
treats unitary symmetry and lower moments; it does not extend to the
orthogonal $L'$ second moment.

**Verdict: circular.** This is the conjecture, restated.

### Route 2. Painlevé connection

**Claim:** Painlevé V/VI gives an integrable structure that produces the
constant exactly.

**Status:** Painlevé equations describe the *RMT side* (gap probabilities
and Fredholm determinants of sine/Airy/Bessel kernels; Conrey–Rubinstein–
Snaith 2006 connect $\zeta$-moments to $\sigma$-Painlevé V on the matrix
side). They are integrable identities for *Haar-measure expectations*.

They do NOT bridge the L↔matrix gap. Painlevé gives us the matrix-side
constant in closed form (which we already have via Barnes $G$); it
provides no leverage on the L-side averages.

**Verdict: false lead.** Painlevé is an interior tool of RMT, not a
bridge to L-functions.

### Route 3. Hughes–Snaith characteristic-polynomial moments

**Claim:** $\langle|\chi'(1)|^2\rangle_{SO(2N)} = 2N^2/3$ exact, so via
$N\leftrightarrow \log X$ dictionary one gets $(2/3)(\log X/(2\pi))^2$,
and accumulating the family count $T\log T/(2\pi)$ etc. yields $2/(3\pi)$.

**Status:** the constant $2/3$ on the matrix side is correct (Hughes,
PhD 2001; reproduced in Conrey–Snaith 2007 §7). The translation
$N\leftrightarrow \log X$ and the arithmetic factor $a_2$ giving $1/\pi$
through Petersson averaging *are* the CFKRS recipe — see
`CFKRS_direct_recipe_proof.md` in this project, which shows precisely
that the CFKRS computation for orthogonal Petersson at a 4-shift
residue yields $2/(3\pi)$.

**This is exactly the CFKRS heuristic the project already has.**
RMT here is an alternative *derivation* of the CFKRS predicted
constant, not an independent proof. The constant agrees — that is
strong evidence the conjecture is correctly stated, but not a proof
of equality.

**Verdict: re-derivation of the prediction. Not a GRH bypass.**

### Route 4. Free probability / Voiculescu

**Claim:** the family L-function distribution converges to a free-prob
limit; free moments are computable.

**Status:** free probability gives moments of certain random matrix
limits (free Poisson, semicircle, etc.). For *characteristic polynomials
on the unit circle*, the relevant object is the CUE limiting measure,
which is *not* a standard free-probability limit — it is described by
log-correlated Gaussian fields (Bourgade–Najnudel, Webb, Nikula–Saksman–
Webb). Free probability is the wrong category. (Free CLTs apply to sums
of independent random variables, not to log-determinants whose covariance
structure is logarithmic.)

**Verdict: wrong tool.** Multiplicative chaos / GFF is the right
category, see Route 5.

### Route 5. Multiplicative chaos / Saksman–Webb

**Claim:** Saksman–Webb (Ann. Probab. 2020) prove that suitable
regularizations of $|\zeta(\tfrac12+it)|^{2\beta}$ converge in
distribution, on random sub-intervals, to Gaussian multiplicative chaos
(GMC). This rigorously realizes the Fyodorov–Hiary–Keating prediction
on a *statistical* level. Najnudel 2018 has related results assuming RH.

**Status — extremely important and honest:**
* SW–type theorems are about **distributional limits on shrinking
  random windows**. They do NOT yield the coefficient in
  $\int_0^T|\zeta'|^2\,dt$, let alone $\sum_\gamma|\zeta'(\rho)|^2$
  or its $L'(\rho_f,f)$ analogue.
* Najnudel 2018's GMC for $\zeta$ is **conditional on RH**.
* No multiplicative-chaos result currently delivers a *moment constant*
  unconditionally for any $L$-function; the chaos limits identify
  *laws*, but the moments of GMC are themselves only known as ratios
  of $\Gamma$-functions in regimes that match the RMT/CFKRS prediction
  (Fyodorov–Bouchaud, Remy 2020, Kupiainen–Rhodes–Vargas 2018+).
* The L-function $\to$ GMC convergence is conjectural and currently
  proven only on the unitary side and only in distribution.

**Verdict: not unconditional, and not a moment statement at the level
needed.** This is the most fashionable route but it is precisely as far
from a proof as CFKRS itself; SW translates one open conjecture (CFKRS)
into another (GMC convergence of L-families).

---

## Section 3. Best derivation — the CFKRS / Hughes route, recorded honestly

The cleanest derivation of the constant 2/(3π) — the one most easily
sanity-checked — is the CFKRS recipe at a 4-fold shift residue,
which the project already has in `CFKRS_direct_recipe_proof.md`.
The RMT version is structurally identical: the SO(2N) Vandermonde plus
the orthogonal weight $\prod(2\sin(\theta_i/2))^{-1}$ produces, via
contour-integral residues at coincident shifts, the rational
$2/(3\cdot 2\pi)/(\text{2-factor from CFKRS gamma ratio})=2/(3\pi)$.

This is documented in:
- Conrey–Snaith 2007 §7 (orthogonal ratios → orthogonal moments
  by differentiating the ratios formula; §7 worked example reproduces
  $2/(3\pi)$ for the orthogonal $|L'|^2$ at the symmetry point);
- Hughes PhD thesis 2001, ch. on derivative moments;
- CFKRS 2005 §4.5.4 (orthogonal Petersson family).

**No new content here.** The constant comes out the same way it did
in `CFKRS_direct_recipe_proof.md`. RMT supplies the same answer via the
matrix integral.

---

## Section 4. Asymptotic-equivalence proof status

### 4.1 What "asymptotic equivalence" of L-family and RMT requires

To convert the prediction into a theorem we would need, *unconditionally*:

(E1) Control of the off-diagonal terms in
$\sum_F \sum_{m,n} \lambda_f(m)\lambda_f(n) m^{-1/2} n^{-1/2} (\log m)(\log n) \cdot W(\dots)$
for $m,n \le X^2$ in the orthogonal Petersson family.
This requires shifted-convolution sums for $\lambda_f$ at scale $X^2$
with logarithmic weights — beyond Deligne / GL(2) bilinear-form
technology when $X = T^{1/2+\epsilon}$.

(E2) An effective bound on the residual error from the CFKRS recipe step 5
("complete the sums") at the *fourth* derivative residue. Currently the
CFKRS step 6 error is conjectural; making it rigorous at the second
moment of the derivative for orthogonal Petersson is precisely the
M–N (16) conjecture.

(E3) The conversion at-zeros ↔ on-line, which under GRH costs a factor
2 (orthogonal pair correlation enhancement, see `B3_*RIGOROUS.md`)
but unconditionally requires bounds on $\beta_f$ (real parts of zeros)
that are not known.

### 4.2 What RMT supplies and what it does not

RMT supplies (E0): the *value* of the constant, and the *combinatorial
shape* (powers of $\log X$, factor $c_f$). It supplies (E0) **rigorously
and exactly**.

RMT supplies **none of (E1), (E2), (E3)**. The matrix model has no
arithmetic — there are no shifted convolutions, no zero ordinates,
no GRH. The matrix model says "if you replaced $\zeta$ by $\Lambda_A$
exactly, here is the answer." The conjectural step is the replacement.

### 4.3 Painlevé does not help (recorded again, in sharper form)

Painlevé V/VI gives *closed-form* finite-$N$ Fredholm-determinant
identities on the matrix side. Those identities are about
$\det(I-K)$ for kernels $K$ on Haar-distributed unitary or orthogonal
groups. They have no analogue on the L-side that does not itself
assume the conjecture. The CRSn 2006 paper which connects $\zeta$
moments to Painlevé does so on the *RMT side* — the L-side connection
is conjectural (CFKRS).

---

## Section 5. Verdict: 2/(3π) via RMT route, unconditionally?

**No.** Five routes evaluated; none yields an unconditional proof.

| Route | Independent of CFKRS? | Independent of GRH? | Yields constant? | Yields theorem? |
|-------|---------------------|---------------------|------------------|-----------------|
| 1. Direct RMT identification | No | No | Yes (assuming = ) | No (= is the conjecture) |
| 2. Painlevé | No | No | Yes (RMT side) | No |
| 3. Hughes–Snaith char-poly | No (= CFKRS shape) | No | Yes | No |
| 4. Free probability | N/A | N/A | No (wrong tool) | No |
| 5. Multiplicative chaos | No | Often No | No (distributional only) | No |

The strongest *honest* statement is:

> **Conditional on CFKRS / RMT-equivalence at the orthogonal Petersson
> family level (which is itself open and is essentially equivalent to
> the M–N (16) conjecture), RMT supplies the constant 2/(3π).** This
> matches the CFKRS recipe derivation in `CFKRS_direct_recipe_proof.md`.

That is what the project already has from CFKRS. RMT is the same
prediction by another name.

---

## Section 6. What's needed if not closed

To close M–N (16) unconditionally one needs progress on at least one of:

(N1) **Shifted-convolution sums for $\lambda_f$ with extra log
factors at length $X^2 = qT^2/(4\pi^2)$.** Best current results
(Blomer–Harcos, Michel, Munshi) reach length $\le X^{1+\delta}$ for small
$\delta$; we need $\delta$ comfortably $>1$. This is the same barrier
as the fourth moment of L for GL(2) — open.

(N2) **A new identity bypassing off-diagonal analysis** in the spirit
of Ramachandra / Zhang for the fourth moment of $\zeta$ (cited by M–N
in §1.4 remark 3). M–N explicitly state (L833–840 of /tmp/milinovich_ng.txt):
> "The present situation is more involved than these previous cases
> because we are averaging over zeros (as opposed to a continuous
> average), so it is perhaps even more striking that we can appeal to
> the Montgomery and Vaughan's mean-value theorem ... in lieu of explicit
> formula techniques combined with estimates for shifted convolution sums."

The continuous on-line second moment of $L'$ is in reach (this is what
`B3_Lprime_2nd_moment_RIGOROUS.md` does, with constant **1/(3π)**, on-line).
The at-zeros version doubles this via orthogonal pair correlation under
GRH — this conversion is what RMT *predicts* and what is not proven
unconditionally.

(N3) **An unconditional pair-correlation theorem for the orthogonal
Petersson family at scale $\log X$.** ILS 2000 give 2-level density
under GRH; without GRH only restricted-support results exist
(test functions of Fourier support $<2$ or $<4$ depending on family).
The needed support for the $L'$-second-moment factor 2 is on the
boundary.

(N4) **A direct family-level coupling theorem of the form
$|F|^{-1}\sum_F \delta_{\theta_f} \to \mu_{Haar,SO(2N_F)}$**
in a strong enough topology to push moments of derivatives
through. This is the Bourgade–Najnudel–Sodin program, currently
restricted to lower-order statistics and unitary type.

None of (N1)–(N4) is on the visible horizon as a theorem.

---

## Appendix A. Key verbatim quotes (audit trail)

**Milinovich–Ng, /tmp/milinovich_ng.txt L843–864 (Conjecture (16)):**

> "Using a heuristic argument based on the 'L-functions ratios
> conjectures' of Conrey, Farmer, and Zirnbauer ... we arrive at the
> following conjecture.
>
> Conjecture. Let f ∈ Hk (q, χ), let cf be the constant in (1), and
> let X = √(qT)/(2π). Then,
> Σ_{0<γf≤T} |L′(ρf, f)|² = (2/(3π)) cf T log⁴ X + O(T log³ X)    (16)
> where the implied constant depends only on f."

**M–N L884–890 on the difficulty:**

> "establishing (16) is comparable to establishing the conjectural
> formula Σ |ζ′(ρ)|⁴ = (T/(2880π³)) log⁹ T + O(T log⁸ T). Such a
> result appears to be unattainable using current techniques without
> some significantly new ideas. ... we expect that some substantially
> new ideas are necessary in order to establish the above conjecture
> for the second moment of L'(ρ_f, f)."

This is the authors of the conjecture saying, in print, that
**substantially new ideas are necessary**. RMT, Painlevé, free
probability, and multiplicative chaos as currently known are not
those new ideas — they are *the same heuristic by other names*.

---

## Appendix B. What this audit *does* contribute

1. **Confirms the constant 2/(3π) from a second route (RMT/Hughes)**,
   independent of the CFKRS recipe in the project's existing file.
   Both routes give the same number — strong consistency check.
2. **Eliminates four would-be GRH-bypass routes** (Painlevé, free prob,
   direct RMT identification, mult. chaos) so future effort on Theorem B
   is not wasted re-attempting them.
3. **Pinpoints the residual barrier** as (E1)/(E2)/(E3) — i.e.
   shifted-convolution + at-zeros conversion — same as M–N's own
   diagnosis. No shortcut found.

**Recommended next move:** continue with the on-line second moment
result (1/(3π), unconditional, already largely in `B3_*RIGOROUS.md`)
as the Paper-1 deliverable, and present 2/(3π) at-zeros as a
GRH-conditional corollary via ILS 2-level pair-correlation. The
unconditional at-zeros constant remains open and should be flagged
explicitly as such.
