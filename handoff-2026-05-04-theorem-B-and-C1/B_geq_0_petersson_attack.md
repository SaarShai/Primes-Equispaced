---
title: "B ≥ 0 sign problem — Petersson family-averaging attack (Track A → Track B reconnection move #2)"
type: derivation
domain: research
tier: working
confidence: 0.34
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - /Users/saar/Farey 4.7 solutions/PROGRAM_REORIENT.md
  - /Users/saar/Farey 4.7 solutions/B3_unconditional_attempt.md
  - /Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/Bridge_Identity.md
  - /Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/Four_Term_Decomposition.md
  - /Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/B_plus_C.md
  - /Users/saar/NEW Farey 5.5/projects/farey-research/bridge-four-term-franel.md
tags: [farey, four-term, B-sign, petersson, family-average, plancherel, reconnection]
---

# Bottom line

**Attack FAILS in the strong sense (no Petersson family analog of the four-term B exists), but produces a NON-TRIVIAL partial result: a soft "centered family" version ⟨B⟩_F = 0 + small Bessel error, which is *strictly weaker* than B ≥ 0 but is the unique sign-positivity statement the modular machinery can deliver here.**

In short:
1. The Bridge Identity Σ_{f∈F_{p−1}} e^{2πipf} = M(p) + 2 has NO direct Petersson-family analog because the LHS sums over a *Farey set* (rationals in (0,1] with denom ≤ p−1) — there is no second variable to average against modular forms.
2. There is, however, a structurally parallel object: replace e^{2πipf} by a_g(p) for a fixed Hecke newform g, then Petersson-average over g. This produces a "trace formula bridge" that connects to Kloosterman/Bessel rather than to M(p).
3. The four-term decomposition's cross-term B = (2/n'²)Σ D(f)·δ(f) is a *bilinear sawtooth* sum (per the Four_Term_Decomposition wiki). It admits a Dedekind-Rademacher representation, but no Petersson analog because the sawtooth ψ(x) = {x} − 1/2 lives in *abelian* Fourier analysis (one-variable, character sums), not GL(2) automorphic analysis.
4. The closest legitimate cross-pollination move is: **replace the question "B ≥ 0?" by "⟨B⟩_F ≥ 0 for a Petersson-weighted bilinear analog?"** — and for the analog this is **trivially true by orthogonality + Plancherel-Sato-Tate positivity** (sym² L-values are non-negative at s=1). This is publishable ONLY if framed as "structural analog suggests B has a Plancherel-positive shadow"; it does NOT prove B ≥ 0 for the original Farey object.

**Net assessment:** the Petersson tools do NOT directly close the Farey B ≥ 0 problem. The obstruction is structural (one-variable abelian vs two-variable automorphic), not technical. Reconnection move #2 fails as a proof of B ≥ 0; it succeeds as a *suggestive heuristic* that the Plancherel-positive sym²(s=1) input is the right modular shadow of the empirical positivity. 

Confidence the structural obstruction is real: 0.78. Confidence the Plancherel shadow is non-trivial (worth recording): 0.55. Confidence we should pursue posture A in PROGRAM_REORIENT (two-paper plan, not forced unification): 0.85.

---

# 1. Precise statement of the B ≥ 0 sign problem

From `Four_Term_Decomposition.md` (corrected 2026-04-13):

ΔW(p) = A − B − C + 1 − D_term − 1/n'²,

with n = |F_{p−1}|, n' = |F_p| = n + (p−1), and

  **B = (2/n'²) Σ_{f ∈ F_{p−1}} D(f) · δ(f)**       (cross-term)

where:
- D(f) = "rank deviation" = the Möbius-inverted sawtooth sum giving the discrepancy of f relative to the uniform measure
- δ(f) = (f − 1/2) − ψ(pf), with ψ(x) = {x} − 1/2 the centered sawtooth, so δ(f) is the "shift" induced by inserting the new fractions k/p

**The B ≥ 0 sign problem (open):**

  **(B-pos):  B(p) ≥ 0  for all primes p ≥ 11 (or characterize the sign exactly).**

Empirical status (per wiki + Session 14 numerical, 2026-04-14):
- B(p) > 0 for nearly all p ∈ [11, 631] tested.
- B(p) < 0 at exactly p ∈ {11, 17, 97, 223} in the test range. M(11) = M(17) = −2; M(97) = +1; M(223) = +3. **Sign of B is NOT explained by M(p).**
- The fully unconditional bound is "B is a covariance, hence |B| ≤ √(C · D_term) by Cauchy-Schwarz", and empirically (D_term + C + B)/A > 1 at all tested p — but this is a bound on |B|, not a sign result.

Two equivalent reformulations (useful for the attack):

**(B-pos as bilinear sum):**  Σ_{a=1}^{p−1} Σ_{(b, p−1) ranking) D_b(a) · δ(a/b) ≥ 0 (after multiplying by n'²/2).

**(B-pos via Dedekind-Rademacher):** writing T_b(p) := p²[s(b, p) + (p−1)/4] as in the wiki, B = Σ_{b ≤ p−1} (weight) · T_b(p), and the question is whether the weighted sum of generalized Dedekind sums is non-negative.

There is **no known L-function moment** equivalent to B. The wiki explicitly says: "No closed form B = f(M(p), p) exists" and "the four-term decomposition IS the natural endpoint of elementary Farey analysis. Any further compression requires zeros of ζ(s) via explicit formula." The "explicit formula" route is reciprocal-ζ Perron (Track B, classical Landau/Ingham), NOT Petersson family averaging.

---

# 2. Where the Petersson machinery wants to live

Theorem B (B3_unconditional_attempt, §3) sits on:

(a) A **family** F_k = S_k*(N) of holomorphic newforms.  
(b) A **Petersson trace formula**: for fixed (m, n),  
    Σ_{f ∈ F_k} ω_f a_f(m) a_f(n) = δ_{m=n} + (off-diagonal Kloosterman + Bessel).
(c) **Bessel decay** at large weight: J_{k−1}(4π√mn/c) ≪ (4π√mn/(ck))^{k−1} kills the off-diagonal once k > 2T (or k ≫ √(mn)/c).
(d) **Plancherel = Sato-Tate** equidistribution of {a_f(p)/2} as k → ∞, which produces the constant 2/(3π) via integration against the orthogonal symmetry kernel K_{O+}.
(e) **Sym² positivity**: ⟨c_f⟩_F = ⟨L(1, sym²f)/ζ(2)⟩_F ≥ 0 (because L(1, sym²f) is *unconditionally non-negative* — it's a special value of an L-function with non-negative Dirichlet coefficients on Re(s) > 1, and continues to s=1 as a *positive* real number).

To deploy this on B, we'd need:
- A two-parameter object where one parameter is the Farey variable f (or its dual) and the other is a modular form g.
- An identity of the form "⟨B(p; g)⟩_g = something Plancherel-positive."

**This object does not exist in the literature, and its construction is the heart of the question.**

---

# 3. Three candidate constructions, and why they fail (or partially work)

## 3.1 Candidate I — "Fourier-replace e^{2πipf} by a_g(p)" (the naive bridge analog)

**Construction.** The Bridge Identity reads Σ_{f ∈ F_{p−1}} e^{2πipf} = M(p) + 2. Naively, replace the additive character e^{2πipf} by the Hecke eigenvalue a_g(p) of a newform g, and consider the Petersson-weighted sum:

  B^♮(p) := Σ_{g ∈ F_k} ω_g · |Σ_{f ∈ F_{p−1}} a_g(p · f)|² ?

**Why it fails.** The exponent "p · f" in e^{2πipf} is a real number (multiplication in R/Z). It's not an integer, so a_g(p·f) is undefined. The Bridge Identity uses the *additive* group structure of R/Z; the Petersson formula uses *multiplicative* Hecke structure on Z. There is no bilinear structure that aligns them.

A more refined attempt: use the Hecke operator T_p acting on a basis of F_k, and consider a_g(p) summed over Farey rationals f (not p·f). But Σ_f a_g(p) = (p−1) · a_g(p) trivially — the f-sum factors out. No interaction.

**Verdict I: vacuous.** No interaction between the Farey sum and the modular form.

## 3.2 Candidate II — "Replace ψ(pf) by a centered Hecke object" (the four-term cross-term analog)

The cross-term B = (2/n'²) Σ D(f)·δ(f), with δ(f) involving ψ(pf), is the closest candidate. The sawtooth ψ(x) = {x} − 1/2 has the Fourier expansion

  ψ(x) = − (1/π) Σ_{m ≥ 1} sin(2πmx)/m

so

  Σ_f D(f) · ψ(pf) = − (1/π) Σ_{m ≥ 1} (1/m) · Σ_f D(f) sin(2πpmf).

**Construction.** Replace the additive sin(2πpmf) by the symmetric square Hecke eigenvalue λ_g(pm)/2 = (a_g(pm)² − 1)/2 (using λ_g(n) = a_g(n²) − a_g(n)·…; actually for sym² we have λ_{sym²g}(p) = a_g(p)² − 1). Then average over g ∈ F_k:

  B̃(p; F_k) := Σ_g ω_g · Σ_f D(f) · [Σ_m (1/m) · λ_{sym²g}(pm) · weight(f, m)].

**The question:** does ⟨B̃⟩_{F_k} ≥ 0?

**Plancherel-positive part.** By Petersson-Sato-Tate (k → ∞):

  Σ_g ω_g λ_{sym²g}(pm) → δ_{pm = 1} · (2/π) · ∫_{-1}^{1} (1 − x²)^{1/2} (4x² − 1) dx + (off-diagonal Bessel)

Wait — the diagonal of λ_{sym²g}(n) summed over Petersson is *not* δ_{n=1}; it's δ_{n = a square} + lower-order. More precisely:

  Σ_g ω_g a_g(m) a_g(n) → δ_{m,n} (Petersson orthogonality, k → ∞).

For sym² we have λ_{sym²g}(p) = a_g(p²) − 1 (because λ_{sym²g}(n) = Σ_{d² | n} μ(d) a_g(n/d²) for squarefree-friendly n), so Σ_g ω_g λ_{sym²g}(pm) = Σ_g ω_g a_g((pm)²) − δ_{pm = 1}. The diagonal of a_g((pm)²) does NOT vanish — it picks up a_g(pm) · a_g(pm) ~ 1 by Petersson + Hecke, giving a *positive* main term.

So the Plancherel limit gives, schematically,

  Σ_g ω_g λ_{sym²g}(pm) = 1 + (Bessel/Kloosterman, → 0 at k → ∞).

Plug back:

  ⟨B̃(p; F_k)⟩_{k→∞} = Σ_f D(f) · [ Σ_m (1/m) · weight(f, m) · 1 ] + o(1)
                     = Σ_f D(f) · ψ(pf) + o(1)
                     = (n'²/2) · (−B(p)/2) + o(1)            [up to the normalization in B]

**This is a TAUTOLOGY.** The Plancherel limit just *recovers the original Farey-side B(p)*, multiplied by a constant. No new positivity is exposed. The Petersson family-averaging "passes through" without giving sign control.

**Verdict II: tautological.** Plancherel-Sato-Tate at k → ∞ recovers the original B(p), so cannot decide its sign. The reason: Petersson orthogonality is a *delta function* on Hecke indices; convolving it with a Farey-side observable that doesn't itself have intrinsic positivity gives back the observable.

## 3.3 Candidate III — "Embed Σ D·δ as a square via sym² L-values" (the genuine positivity attempt)

**This is the most interesting attempt.** It tries to use the fact that L(1, sym²f) ≥ 0 unconditionally to obtain a Plancherel-positive *family-averaged* analog of Σ D·δ.

**Construction.** Suppose we can find a kernel K_p(f, g) such that:

  Σ_g ω_g K_p(f, g) = D(f) · δ(f) · (k-dependent normalization)

with K_p(f, g) ≥ 0 pointwise, and K_p(f, g) is itself a quadratic form in some Hecke or L-value object. Then summing over f gives ⟨B̃⟩_F ≥ 0.

**Why it almost works, then fails.** A natural candidate for K_p(f, g) is

  K_p(f, g) := |L(1/2 + iγ_g, g) · χ_f(g, p)|²

for some test functional χ_f. But:

(i) δ(f) is *not* obviously positive (it's δ(f) = (f − 1/2) − ψ(pf), oscillates).
(ii) D(f) has both signs.
(iii) Their product D(f)·δ(f) has both signs in general; only the *p-summed* B(p) has a definite sign empirically.

So ANY kernel reproducing D(f)·δ(f) per f cannot be pointwise non-negative. A pointwise-positive kernel can only reproduce a sum-non-negative expression.

The honest construction is then:

  ⟨T(p; F_k)⟩ := Σ_g ω_g · |Λ_g(p)|² · w(g)

where Λ_g(p) is some moment of g at the prime p, and w(g) is positive Petersson weight. Then ⟨T⟩ ≥ 0 trivially (sum of non-negative terms). But to *match* this to B(p), we'd need

  ⟨T(p; F_k)⟩ = B(p) + error.

This is the **identification problem**: which (Λ_g, w(g)) reproduces Σ_f D(f)·δ(f)?

**Closest fit attempted.** The Voronoi-type identity for D(f) (Möbius-inverted sawtooth) suggests

  Σ_f D(f) · ψ(pf) = (constant) · Σ_n μ(n)/n · (sawtooth Fourier mode at pn)

When summed against a_g(pn)·a_g(m) Petersson-orthogonally, the diagonal is δ_{pn = m} which would identify n = m/p and gives a residue. The sym² promotion (n → n²) folds in the L(1, sym²f) factor:

  Σ_g ω_g · |Σ_n μ(n)/n · a_g(pn)|² → (Plancherel) Σ_n (μ(n)/n)² · 1 + (off-diag) = π²/(6·something) + ...

This is **strictly positive** by construction (it's the Petersson norm of the Möbius-twisted Dirichlet series). But it is **NOT equal to B(p)** — it's an analog with extra absolute-value squaring.

**Verdict III:** the natural Plancherel-positive analog corresponds to ⟨|sum|²⟩_F, which is the *modulus squared* of the Möbius-twisted Hecke sum, NOT to the *signed bilinear* B(p). The squaring operation that makes the Petersson average positive is exactly the operation that destroys the cross-term sign question.

The structural obstruction: **Plancherel positivity acts via L² (squaring); B(p) is L¹ (signed bilinear). Hodge/Cauchy-Schwarz inequality has the wrong direction — it gives |B|² ≤ A · C, which the wiki already records as the B+C+D vs A bound, but does NOT force sign(B) ≥ 0.**

---

# 4. The strongest claim the modular machinery DOES support

A non-trivial partial result survives. State it cleanly:

**Claim 4.1 (Structural shadow of B-positivity).** Let

  B^□(p) := Σ_n (μ(n)/n²) · Σ_{m: pn|m, m ≤ X} a_g(m) · w(m, p)

be a Möbius-twisted Hecke moment with squared Möbius (note the **n²**, not n). Then for F_k = S_k*(N) Petersson-weighted, k → ∞,

  ⟨B^□(p)⟩_{F_k} = ζ(2)⁻¹ · L(1, sym²g)-averaged · (constant) + o(1),

and this is **unconditionally ≥ 0** (sym²-positivity, Hoffstein-Lockhart 1994).

**Why this is interesting:** B^□ is not B, but it shares the Möbius-Bridge skeleton (μ summed against a Hecke-promoted "pf" object). The modular family analog of "B is non-negative on average" is "L(1, sym²f) ≥ 0", which is **unconditional and clean**. This is the precise mathematical sense in which the Plancherel-Sato-Tate machinery "explains" the empirical B ≥ 0: not by proving it, but by exhibiting a structurally analogous object that IS positive for hard analytic-NT reasons.

**Why this is NOT enough:** the analog object has μ(n)/n² (squared), which kills the oscillating-cancellation behavior of the actual μ(n)/n that drives the four-term identity. Concretely:
- Bridge Identity LHS = Ramanujan sum c_N(1) = μ(N), which uses μ(n)/n directly.
- Sym² L-value uses μ(n)/n², a different Dirichlet series (it's L(2s)·L(2s, sym²f)⁻¹ at s = 1, roughly).

So the analog is "two-derivatives-too-positive" relative to the original.

---

# 5. Why the Bridge Identity has no Petersson dual at all

A separate diagnostic. The Bridge Identity:

  Σ_{f ∈ F_{p−1}} e^{2πipf} = M(p) + 2 = Σ_{n ≤ p−1, (n,p)=1} μ(n)/(n^0) · (trivial denominator) + 2.

The LHS is a **Ramanujan sum**: c_{p−1}(p) = Σ_{(a, p−1)=1, a ≤ p−1} e^{2πi(p·a/(p−1))}. This sum is over an *additive group* — primitive roots of unity of order p−1, evaluated at p.

Petersson trace formula sums over a *multiplicative family* (newforms, indexed by their Hecke eigenvalues, not by additive characters). There is no known map "Ramanujan sum c_q(n) ↔ Petersson average over F" for any natural family F.

**The closest thing in the literature** is Deshouillers-Iwaniec's "Kloosterman sum trace formula", which expresses sums of *Kloosterman sums* (themselves Ramanujan-sum-like) as spectral averages over Maass forms. But Kloosterman sums S(m, n; c) are bilinear in (m, n), not unary like c_q(n). So Bridge Identity ↛ Petersson.

**Diagnosis:** the Bridge Identity is **abelian** (one-variable Fourier on R/Z). The Petersson family is **non-abelian** (GL(2) automorphic). The two sit in disjoint analytic-NT universes; cross-pollination is structural-skeleton only (both invoke Möbius and primes), not observable-level.

This is the same diagnosis PROGRAM_REORIENT §"Top 3 Reconnection Moves" alludes to but does not state crisply: **the four families share the SKELETON, not a single observable.**

---

# 6. What WOULD close B ≥ 0 (the inputs we'd need but don't have)

For posture B (forced unification) to deliver B ≥ 0:

(a) **A Voronoi-type duality** between Σ_f D(f) · ψ(pf) and a Hecke L-value squared. Voronoi summation does exist for Hecke eigenvalues (Booker-Krishnamurthy-Lee 2014, etc.), but it converts Σ a_f(n) · h(n) into a *similar* sum with a transformed h, not into a positive square.

(b) **A positivity-preserving lift** Σ_f D(f) · ψ(pf) ↦ |M_g(p)|² for some g-indexed moment. The squaring step requires a Cauchy-Schwarz dual of the *original* identity, and the original identity has indefinite sign — so the dual has at best indefinite sign, defeating positivity.

(c) **A new automorphic identity** of the form

  Σ_{(a, b, p) bilinear sawtooth} = ⟨L(1, sym²f) · weighted⟩_F

with explicit weights making sign positive. Not in any literature I can identify.

The honest gap: **B(p) is a height-1 elementary number-theoretic invariant. The Petersson machinery operates at height ≥ 2 (L-functions). Promoting B to a height-2 object loses the sign information; demoting Petersson to height-1 loses the trace-formula structure that gives positivity. There is no "right height" at which both sides are positive AND identifiable.**

---

# 7. Numerical verification (16-curve EC ladder context)

The 16-curve ladder data (from B1 closed-form a_2 work) is not directly applicable here — those curves test the **modular** side (Track A). For the Farey side (Track B), the relevant numerical evidence is already on file:

- B(p) computed exactly for p ∈ [11, 631] (Session 14, exact rational arithmetic).
- B(p) < 0 at exactly p ∈ {11, 17, 97, 223}.
- B(p) > 0 at all other tested primes.

**Cross-pollination check:** does the sym² L-value at the elliptic curves in the 16-EC ladder predict the sign of any Farey object? Test:

For each curve E in the ladder, compute L(1, sym² f_E) (the symmetric square L-value at s=1, where f_E is the modular form attached to E by modularity). All 16 values are ≥ 0 unconditionally (by Hoffstein-Lockhart). For the four primes p ∈ {11, 17, 97, 223} where B(p) < 0, check whether any of the 16 curves has unusual a_E(p). This is a **null test** of the structural-shadow heuristic: if the heuristic were predictive, we'd expect L(1, sym² f_E) to correlate with B(p) at the "exceptional" primes. There is no such mechanism in Candidate III above, so we predict no correlation.

**This null prediction itself is publishable** as a falsifier — it sharpens the claim that the modular tools are *orthogonal* (in the strong sense) to Track B's B-sign question.

I recommend running this null test on M5 overnight: compute (a_E(p), L(1, sym² f_E)) for each (E, p) with E in the 16-EC ladder and p ∈ {11, 17, 97, 223, plus 100 random control primes}, then correlate the residual to sign(B(p)). Predicted r² ≪ 0.05.

**Verification gate per common.md:** Both L(1, sym²f) values and B(p) values must be computed from primary sources (mpmath / PARI exact rationals) — never reuse cached "known" values without recomputation.

---

# 8. Confidence, caveats, and recommendation

## 8.1 Confidence

- Structural obstruction (abelian Bridge ↮ non-abelian Petersson): **0.78** (one would need a Voronoi-type duality that is documented not to exist in the form needed).
- Tautological recovery in Candidate II: **0.82** (this is essentially Petersson orthogonality unfolded; verified at the first-order level).
- Squaring obstruction in Candidate III (L¹ vs L²): **0.85** (this is a generic diagnostic of why the modular methods don't decide signs of sawtooth bilinears).
- Null-prediction on the 16-EC ladder being correct: **0.75** (no mechanism, but small sample, easy to falsify).
- Recommendation for posture A (two-paper plan, not forced unification): **0.85**.

## 8.2 Caveats

1. I have not exhaustively searched the Voronoi-summation / Iwaniec-Sarnak literature for an exotic duality — there's a small but non-zero chance someone has built a non-standard Hecke-promoted sawtooth identity. Recommend a 2-hour Codex-rescue search for "sawtooth Voronoi Hecke" + "Dedekind sum trace formula" + "Petersson + bilinear sawtooth" before fully closing this avenue.

2. The B-sign problem might admit a *non-Petersson* automorphic attack — e.g., GL(3) Voronoi summation (Miller-Schmid 2011) or Eisenstein series (Bump-Diaconu). These were explicitly ruled OUT of scope for this attack but could yield results. Flag for a future reconnection move.

3. The 33000:1 cancellation phenomenon (`Cancellation_33000.md`) and the φ_1 = −1.6933 phase (`Phase_Resolution.md`) are reciprocal-ζ explicit-formula artifacts. They sit on Track B's side and are reachable only via the *smoothed Farey explicit formula* path (PROGRAM_REORIENT reconnection move #1), NOT via Petersson averaging (move #2). This document confirms move #2 fails; move #1 remains the better Track-A → Track-B bridge.

## 8.3 Recommendation

**Drop reconnection move #2 (Petersson family averaging for B ≥ 0). Pivot to reconnection move #1: smoothed Schwartz-cutoff Δw_f explicit formula via the c_W Mellin-shift Lean infrastructure.** Move #1 is structurally compatible (both sides are reciprocal-ζ, abelian, smoothed) and tractable in HIGH (per PROGRAM_REORIENT). Move #2 has been shown here to be structurally incompatible: the modular tools are orthogonal in the strong sense to the four-term sign question.

If the user wants ONE result from today's session that connects today's modular tools to Track B, it should come from move #1 (write `c_W`-shift smoothed Δw_f explicit formula with rigorous tail bound), not from move #2.

The honest summary: **today's modular tools cannot prove B ≥ 0. The structural reason is documented above. The remaining Track-B path to B ≥ 0 is the Dedekind-Rademacher reciprocity route (already noted in the wiki) plus possibly GL(3) Voronoi — neither of which uses today's Petersson/Bessel/sym² machinery.**

---

# 9. Wiki update suggestions

After confirmation:

- Append to `Four_Term_Decomposition.md`: "Petersson family-averaging attack on B ≥ 0 (2026-05-02): structural obstruction documented in `B_geq_0_petersson_attack.md`. The cross-term B is L¹/abelian; Petersson positivity is L²/non-abelian. No known Voronoi-type duality bridges them. Track-B path forward remains Dedekind-Rademacher reciprocity."

- Create new wiki entry `wiki/Research/Tracks-A-and-B-Orthogonality.md` (tier: episodic, confidence: 0.78) recording this orthogonality result. Cross-link from `Farey-C1-W2-Mechanism.md` and `Bridge_Identity.md`.

- Append to `log.md` (JSONL): {date: 2026-05-02, action: "negative reconnection result", topic: "Petersson family averaging cannot decide sign of four-term cross-term B", confidence: 0.78, file: "/Users/saar/Farey 4.7 solutions/B_geq_0_petersson_attack.md"}.

Done. ~2,400 words.
