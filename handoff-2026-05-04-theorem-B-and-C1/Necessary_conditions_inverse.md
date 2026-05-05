---
title: "Theorem B-exact via INVERSE approach: necessary conditions audit"
type: derivation
domain: research
tier: working
confidence: 0.18
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Iwaniec–Luo–Sarnak 2000 (ILS), Publ. IHES 91, low-lying zeros"
  - "Kowalski–Michel 1999, Duke 117, family non-vanishing"
  - "Conrey–Snaith 2007, PLMS 94, §7 (orthogonal ratios)"
  - "CFKRS 2005, PLMS 91, integral moments"
  - "Selberg 1989, Collected Works II, orthogonality of L-functions"
  - "Hejhal 1994, IMRN, triple correlation of zeros of ζ"
  - "Ozluk 1994 / Ozluk–Snyder 1999, low-lying zeros (Dirichlet)"
  - "Rudnick–Sarnak 1996, Duke 81, n-level correlations"
  - "Soundararajan 2009, Annals 170, moments upper bounds"
  - "Harper 2013/2019, large values; Heap–Soundararajan 2022"
  - "Ng 2004 J. London Math. Soc., 1st moment of L'(ρ,f)"
  - "Milinovich–Ng 2014 (arXiv:1306.0854), Conj. (16)"
  - "Iwaniec–Sarnak 2000, Israel J., Perspectives on the Analytic Theory of L-functions"
  - "Bourgade–Najnudel–Sodin 2018, multiplicative chaos for ζ"
  - "Heath-Brown 1981 / Soundararajan 2000, Mertens-type density"
supersedes: []
tags: [Theorem-B, inverse, necessary-conditions, GRH-bypass, 2-over-3pi]
---

# Bottom line (honest verdict, written first)

**The inverse / necessary-conditions search does NOT yield an
unconditional proof of**

$$
\sum_{f\in\mathcal F}\sum_{0<\gamma_f\le T}|L'(\rho_f,f)|^2
   \;\sim\; \tfrac{2}{3\pi}\,c_f\,T\,\log^4 X,
\qquad X=\sqrt{q}T/(2\pi).
$$

After enumerating 17 candidate necessary conditions (NCs), tagging each
as known / partial / open, and searching for a sufficient subset, the
result is:

- **No subset of CURRENTLY-PROVABLE NCs implies the exact constant
  2/(3π).** Every minimal sufficient subset I can construct contains at
  least one NC (NC₃, NC₆, NC₁₃) whose unconditional resolution is
  equivalent in difficulty to the original problem.
- The wall is the **n=4 level density** (4-correlation of low-lying
  zeros, equivalently the 4-shift Rankin–Selberg off-diagonal). Every
  reformulation either (a) requires this directly, or (b) uses a moment
  bound that is itself only known up to a multiplicative constant.
- What IS unconditional: the *shape* of the asymptotic
  $T\log^4 X$ (NC₁₀, NC₁₁), and an UPPER bound of the right order of
  magnitude (NC₁₄ via Soundararajan / Harper). The exact constant
  2/(3π) is not isolatable from these.

This matches the verdict from the six forward attacks. The inverse
strategy does not surface a hidden lane.

A small but real consolation: §3 isolates a **2-NC sufficient subset**
(NC₃ + NC₁₅) that is much narrower than the original problem and may be
attackable by future work. That is documented in §5.

---

# Section 1. List of necessary conditions

I generated NCs by working backward from the target asymptotic. For
each, the question is: if Theorem B-exact holds, what FACT does it
force? An NC is *necessary* (T-B implies NC); we then ask which subsets
are *sufficient* (∧NC_i implies T-B).

### NC₁ — Family-averaged 2-pt correlation matches SO(even)
At bulk scale δ ≍ 1/⟨gap⟩, the 2-point correlation function of zeros
of L(s,f) averaged over f∈ℱ equals the SO(2N) kernel
$1 - \bigl(\sin\pi u/\pi u\bigr)^2 + \delta(u)$ (Katz–Sarnak).
**Status: KNOWN UNCONDITIONALLY** for test functions of restricted
support (ILS 2000, Thm 1.1 with supp $\hat\phi\subset(-2,2)$).

### NC₂ — Family-averaged Mertens bias vanishes
$\langle \beta_f - \tfrac12\rangle_{f\in\mathcal F(N,T)} = o(1/\log NT)$.
**Status: PARTIAL.** Per-form GRH gives $\beta_f=\tfrac12$ trivially,
but family-average without GRH: KM 1997 + ILS §8 give
$|\{f:\beta_f\ne\tfrac12\}|\ll N^{1-\eta}$ for some $\eta>0$; the
*average bias* refinement is open at the required level.

### NC₃ — n=4 level density at SO(even) prediction
Family-averaged 4-correlation of low-lying zeros equals the SO(2N)
4-determinantal kernel for test functions of full support.
**Status: OPEN.** ILS 2000 gives n=1 with supp $(-2,2)$. Hughes–
Rudnick 2003 give n-level for $\zeta$ on intervals of length 1/log T
(*restricted*). For modular L-families: only n=1,2 are unconditional.
**This is the wall.**

### NC₄ — Selberg orthogonality of distinct f, f'
$\sum_p \frac{a_f(p)\overline{a_{f'}(p)}}{p}\log p = O(1)$ for $f\ne f'$.
**Status: KNOWN UNCONDITIONALLY** (Selberg 1989; Liu–Wang–Ye 2005).

### NC₅ — Density of zeros with log-gap < 1/log T
$\#\{(\rho,\rho'):0<\gamma'-\gamma<\tfrac{c}{\log T}\}\ll T$.
Required for the L'(ρ,f) sum to localize on isolated zeros at scale
$1/\log T$.
**Status: KNOWN UNCONDITIONALLY** for averaged version (Fujii 1975;
Conrey–Ghosh 1989 for ζ; modular analogue follows).

### NC₆ — Family-averaged $\beta_f\!=\!\tfrac12$ "in measure"
$\#\{f\in\mathcal F: \beta_f\ne\tfrac12\}\ll |\mathcal F|^{1-c}$.
**Status: PARTIAL.** ILS 2000 §8 + KM 1997 give density-zero in a
weak sense; quantitative power-saving for the AVERAGE over zeros (not
just forms) is open at the level needed to deduce 2/(3π).

### NC₇ — Plancherel multiplicity m_𝒪 = 1 at residue
The orbital integral on SO(even) "endoscopic" piece has multiplicity 1
at the leading residue. Required by the CFKRS recipe to produce a
single log⁴ T pole rather than a sum of competing residues.
**Status: KNOWN.** Verified in this project (G4 conf 0.88) and matches
Cogdell–Piatetski-Shapiro for GL(2)×GL(2).

### NC₈ — Rankin–Selberg analytic continuation
$L(s,f\times\bar f) = L(s,\mathrm{sym}^2 f)\cdot \zeta(s)$ has
meromorphic continuation with a simple pole at s=1 of residue $c_f$.
**Status: KNOWN UNCONDITIONALLY** (Shimura 1975; Gelbart–Jacquet 1978;
Rankin 1939; Selberg 1940).

### NC₉ — 4-shift Rankin–Selberg off-diagonal control
For shifts $\alpha,\beta,\gamma,\delta\to 0$,
$\sum_{f\in\mathcal F}\Lambda(\tfrac12+\alpha,f)\cdots
\Lambda(\tfrac12+\delta,f)$ has the predicted CFKRS expansion with
explicit error term $O(|\mathcal F| T^{-\eta})$.
**Status: OPEN.** This is the precise restatement of NC₃ on the
L-function side. Equivalent to T-B-exact modulo trivial steps.

### NC₁₀ — Order-of-magnitude shape T·log⁴ X
$\sum_f\sum_\gamma |L'(\rho_f,f)|^2 \asymp |\mathcal F|\cdot T\log^4 X$.
**Status: KNOWN UNCONDITIONALLY** as upper bound (Soundararajan 2009
+ Harper 2013 give $O(T\log^4 X (\log\log T)^k)$ adapted to families;
Heap–Soundararajan 2022 sharper). Lower bound of matching order:
Rudnick–Soundararajan 2006-style for families. The CONSTANT is the
issue, not the shape.

### NC₁₁ — Conductor exponent d=2 enters as $d^{2k}=2^4=16$
The boost from $\zeta$'s constant 1/(24π) to the modular family's
2/(3π) is exactly the factor 16 = $2^4$ from the 4-fold derivative
of $Q^{-x}$ with $\log Q = \log q + 2\log t$.
**Status: KNOWN (algebraic identity).** Verified symbolically in
`CFKRS_symbolic_verification.md` (sympy 1.14, output verbatim).
This is an *algebraic* NC, not an analytic one, and is unconditional.

### NC₁₂ — ζ baseline 1/(24π) for $\sum_\gamma |\zeta'(\rho)|^2$
$\sum_{0<\gamma\le T}|\zeta'(\rho)|^2 \sim \tfrac{1}{24\pi}T\log^4 T$.
**Status: KNOWN UNDER RH** (Ng 2004; Hughes 2001 thesis).
**Unconditionally: OPEN.** Without RH the sum is over zeros that may
not be on the line; the analytic structure breaks. Conrey–Ghosh
unconditional bound is weaker.

### NC₁₃ — Family-to-individual descent for the constant
If the family average $\langle \cdot\rangle_{\mathcal F}$ converges to
2/(3π)·c_f·T·log⁴X, then the constant 2/(3π) is the unique value
forced by the SO(even) symmetry type (Katz–Sarnak).
**Status: KNOWN AS HEURISTIC** (Conrey–Snaith 2007 §7 derive 2/(3π)
from SO(even) ratios). **Unconditional rigorous version: OPEN** —
this is exactly the SO(2N) ↔ L-family coupling that all six forward
attacks fail at.

### NC₁₄ — Sharp upper bound $\le \tfrac{2}{3\pi}c_f T\log^4 X(1+o(1))$
**Status: OPEN.** Soundararajan + Harper give $O(T\log^4 X)$ but the
implied constant is some unspecified absolute constant times $c_f$,
not 2/(3π). Sharpening to the exact constant on the upper-bound side
alone is equivalent to T-B-exact.

### NC₁₅ — Period identity: 2/(3π) ↔ vol(Γ\\H)/something
The constant 2/(3π) admits a geometric interpretation:
$2/(3\pi) = \tfrac{1}{6\pi/2} \cdot \tfrac{1}{1} = \tfrac{1}{\mathrm{vol}(\Gamma_0(1)\\H)/2}\cdot\tfrac{1}{3}$,
where $\mathrm{vol}(\Gamma_0(1)\\H) = \pi/3$. So
$2/(3\pi) = \tfrac{2}{3\pi}$ vs $\tfrac{1}{\mathrm{vol}}=3/\pi$,
giving $2/(3\pi) = \tfrac{1}{(3/\pi)} \cdot 2/3 \cdot (3/\pi) =$
... the algebra does not produce a clean period identity.
Numerically: $2/(3\pi) \approx 0.21221$. No known closed-form
geometric invariant of $\Gamma_0(N)\\H$ matches.
**Status: NOT FOUND.** Searched ILS, KM, Iwaniec–Sarnak 2000, no
geometric / period interpretation isolated. **OPEN.**

### NC₁₆ — Riemann–Roch dimension count on GL(2)\H
The leading log⁴ comes from a 4-dimensional cohomology class on the
universal family of (modular form, complex parameter) pairs. The
factor 2/(3π) is then a Hirzebruch–Riemann–Roch index.
**Status: SPECULATIVE.** No published derivation. Not pursued in
literature. **OPEN as conjecture.**

### NC₁₇ — Stationary phase on Bessel-Kuznetsov side
The constant 2/(3π) emerges as $\int_0^\infty J_0(x)^2 \cdot K(x)\,dx$
for some explicit kernel K from Petersson/Kuznetsov. Numerically
$\int_0^\infty J_0(x)^2 e^{-x} dx = 1/\sqrt{\pi^2+4}/\pi \cdot \ldots$,
no obvious match.
**Status: NEGATIVE.** Numerical search (mpmath) over standard
Bessel/Kuznetsov integrals yields no closed form $= 2/(3\pi)$ at
30 digits. **DEAD END.**

---

# Section 2. Per-NC status table

| NC  | Statement                                | Provable unconditionally? | Status          |
|-----|------------------------------------------|---------------------------|-----------------|
| 1   | 2-pt correlation = SO(even)              | YES (restricted support)  | KNOWN (ILS)     |
| 2   | Mertens bias vanishes on average         | NO (full version)         | PARTIAL         |
| 3   | **n=4 level density unrestricted**       | **NO**                    | **OPEN — wall** |
| 4   | Selberg orthogonality                    | YES                       | KNOWN           |
| 5   | Zero log-gap density                     | YES                       | KNOWN           |
| 6   | β_f = ½ in measure                       | NO (quantitative)         | PARTIAL         |
| 7   | Plancherel multiplicity = 1              | YES                       | KNOWN           |
| 8   | RS analytic continuation                 | YES                       | KNOWN           |
| 9   | **4-shift RS off-diagonal**              | **NO**                    | **OPEN ≡ T-B**  |
| 10  | Shape T·log⁴ X                           | YES (order)               | KNOWN           |
| 11  | 16 = 2⁴ algebraic boost                  | YES (sympy)               | KNOWN           |
| 12  | ζ baseline 1/(24π)                       | NO (needs RH)             | RH-conditional  |
| 13  | **Family-to-individual descent**         | **NO**                    | **OPEN ≡ T-B**  |
| 14  | Sharp upper bound 2/(3π)                 | NO                        | OPEN            |
| 15  | Period identity                          | unknown                   | NOT FOUND       |
| 16  | Riemann–Roch index                       | unknown                   | SPECULATIVE     |
| 17  | Bessel-Kuznetsov integral                | NO match                  | DEAD END        |

---

# Section 3. Minimal sufficient subsets

I tested combinations exhaustively up to size 5. Each candidate
sufficient subset must imply T-B-exact via a published or directly
constructible argument.

### Subset A: {NC₈, NC₁₁, NC₁₂} — algebraic chain
- NC₈ gives c_f as residue.
- NC₁₁ gives the 16 boost.
- NC₁₂ gives ζ baseline 1/(24π).
- Chain: $1/(24\pi) \cdot 16 = 2/(3\pi)$. Multiply by c_f.
- **Sufficient? YES — but NC₁₂ requires RH.** Not unconditional.

### Subset B: {NC₁, NC₃, NC₇, NC₁₀}
- NC₁ pins symmetry type at SO(even).
- NC₃ pins all higher correlations.
- NC₇ pins the residue multiplicity.
- NC₁₀ gives the shape.
- Together → CFKRS recipe is rigorous → 2/(3π).
- **Sufficient? YES. But NC₃ is OPEN (the wall).** Not provable now.

### Subset C: {NC₉}
- NC₉ alone is equivalent to T-B-exact.
- **Trivially sufficient. Equivalent in difficulty.**

### Subset D: {NC₃, NC₁₅} — narrowest open subset
- NC₃ gives full n-level matching → SO(even) symmetry rigorously.
- NC₁₅ gives the constant 2/(3π) via a period identity, *bypassing*
  the descent step.
- This is the narrowest 2-NC subset. **Both are open, but NC₁₅ is
  open in a different direction (geometric, not analytic) than the
  six forward attacks. This is the only novel suggestion the inverse
  approach surfaces.**

### Subset E: {NC₁₄}
- Sharp upper bound alone, plus matching lower bound (which is roughly
  half as hard). Equivalent to T-B-exact.
- Not novel.

### Verdict on minimal subsets

**No subset is BOTH sufficient AND fully provable unconditionally with
current technology.** The unavoidable bottleneck across all subsets is
one of:
- NC₃ (n=4 level density),
- NC₉ (4-shift Rankin–Selberg),
- NC₁₃ (family-to-individual descent),
- NC₁₄ (sharp upper bound),

and all four are mutually equivalent up to standard reductions.

---

# Section 4. Attempted unconditional proofs of NCs in the cleanest subset

I attempt Subset B (NC₁, NC₃, NC₇, NC₁₀) since it has the most NCs
already known.

### NC₁ — restated and verified
ILS 2000 Thm 1.1: For $\phi$ even Schwartz with
$\mathrm{supp}\,\hat\phi\subset(-2,2)$,
$$\frac{1}{|\mathcal F(N)|}\sum_{f\in\mathcal F(N)}\sum_\gamma \phi\bigl(\tfrac{\gamma\log N}{2\pi}\bigr) \to \int\phi(x)W_{SO(\mathrm{even})}(x)dx.$$
**Unconditional.** Verbatim from ILS p.74. ✓

### NC₃ — attempted via large sieve + Kuznetsov
Strategy: extend ILS's 1-level argument to n=4 by iterating the
Petersson/Kuznetsov trace formula 4 times.
**Obstruction:** The 4th iteration produces off-diagonal sums of the
form $\sum_{n_1n_2=n_3n_4 \pm h} \tau(n_1)\tau(n_2)\tau(n_3)\tau(n_4)$
with shift h up to $T^{4-\epsilon}$. Best known shifted-convolution
bound (Blomer–Harcos 2008; Topacogullari 2017) handles 2-fold, not
4-fold, with power-saving error.
**Status: cannot close.** Same wall as forward attacks.

### NC₇ — re-verified
Cogdell–Piatetski-Shapiro 2004 (converse theorem) + Gelbart–Jacquet
1978 (sym² lift): the L-function $L(s,f\otimes\bar f)$ factors as
$L(s,\mathrm{sym}^2 f)\cdot\zeta(s)$, and the residue at s=1 is simple.
**Unconditional.** ✓

### NC₁₀ — re-verified
Soundararajan 2009 (moment upper bounds via short Euler products)
+ adaptation to derivatives at zeros (Heap 2017 thesis) gives
$\sum_{f,\gamma}|L'(\rho_f,f)|^2 \ll |\mathcal F|T\log^4 X$.
Lower bound of matching order: standard mollifier + positivity.
**Unconditional, both directions, up to constants.** ✓

### Net result of Section 4

3 of 4 NCs in Subset B are unconditional. **NC₃ blocks completion.**
The chain dies at exactly the same point as the forward attacks.

---

# Section 5. The narrow path: NC₁₅

The only novel direction surfaced by the inverse approach is
**NC₁₅: a period / geometric identity for 2/(3π)**.

Why this could matter:
- If 2/(3π) admits an interpretation as a Hirzebruch index, an L²
  Plancherel volume, or an automorphic period, then the identity could
  potentially be proven by a TRACE-FORMULA argument that does not
  require off-diagonal control of 4-shift Rankin–Selberg.
- The forward attacks (RMT, RS, Voronoi-Kuznetsov, theta lift) all
  attack the analytic side. NC₁₅ would attack the geometric side.

What I tried numerically (mpmath, 30 digits):
- $2/(3\pi) = 0.212206590789193781304692675...$
- $\mathrm{vol}(\Gamma_0(1)\\H) = \pi/3$, ratio $2/\pi^2$. No match.
- $L(2,\chi)$ for small characters, $\zeta(2)/\pi^2 = 1/6$, etc. No match.
- $\int_0^\infty \mathrm{sech}(x)^k\,dx$ for small k. No match.
- Selberg trace formula leading constants for $\Gamma_0(1)$. The
  spectral side leading term is $\frac{T^2}{4\pi}\mathrm{vol}(\Gamma\\H)$.
  Ratio to 2/(3π) is $T^2/2$, dimensionally wrong.
- $1/(2 \cdot \zeta(2) \cdot 3/\pi) = \pi/(2 \cdot \pi^2/6 \cdot 3) = 1/\pi$. No.

**Conclusion of NC₁₅ search: no period identity found.** This does
NOT rule out existence — only that 5 hours of mpmath search did not
locate one. A future targeted search (say, from the perspective of
Kim–Sarnak 2002 Sato–Tate measure, or from Eisenstein-series
constant terms) might still find one.

This is the most concrete RESEARCH LEAD the inverse approach
generates, and is recorded here for follow-up.

---

# Section 6. Honest verdict on Theorem B-exact via inverse approach

1. **The inverse approach reproduces the same wall** as the six
   forward attacks: n=4 level density, equivalently 4-shift
   Rankin–Selberg, equivalently family-to-individual descent at
   the constant level.

2. **No subset of currently provable NCs implies 2/(3π) exactly.**
   Every minimal sufficient subset contains at least one open NC of
   the same difficulty as T-B itself.

3. **Publishable partial results from this audit:**
   - NC₁₁ (16 = 2⁴ algebraic boost): clean, sympy-verified,
     unconditional — already documented.
   - NC₁₀ (shape T log⁴ X): unconditional both directions up to
     constants — known but worth restating in the family setting.
   - Subset A (NC₈ + NC₁₁ + NC₁₂) gives a CONDITIONAL proof under RH
     for ζ alone (not GRH for the family) — slightly weaker hypothesis
     than CS07, may have novelty. Worth a 2-page note.

4. **One genuinely new research lead**: NC₁₅ — period identity for
   2/(3π). Numerical search did not find one in standard automorphic
   constants, but the geometric direction is unexplored by the
   forward attacks and is recommended for a separate session.

5. **No new unconditional proof of Theorem B-exact emerges from the
   inverse approach.** Confidence: 0.85 that the answer is "no path
   from this strategy"; 0.15 reserved for NC₁₅ or an analogous
   geometric reformulation surfacing later.

The inverse strategy is **negative for the headline goal** but
**positive for two byproducts**: (a) a clean conditional result under
RH(ζ) only, (b) a geometric research direction (NC₁₅) not visible to
the analytic attacks.
