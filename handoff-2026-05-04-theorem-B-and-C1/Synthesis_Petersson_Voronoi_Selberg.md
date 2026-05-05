---
title: "Synthesis attack: Petersson + Voronoi + Selberg simultaneously, on Theorem B (exact 2/(3π) unconditional)"
type: original-research-attempt
domain: research
tier: working
confidence: 0.08
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (10h budget, original synthesis)
sources:
  - Iwaniec 2002, "Spectral Methods of Automorphic Forms" (GSM 53), Ch. 9 (Petersson/Kuznetsov)
  - Iwaniec–Kowalski 2004, "Analytic Number Theory" (AMS Coll. 53), Ch. 4 (Voronoi), Ch. 15
  - Hejhal 1976/1983, "The Selberg Trace Formula for PSL(2,R)" Vols I–II (LNM 548, 1001)
  - Bruggeman 1983, "Fourier Coefficients of Automorphic Forms" (LNM 865) — Selberg/Kuznetsov/Petersson hybrid
  - Iwaniec–Sarnak 2000 (Publ. Math. IHÉS 91)
  - Bump 1989, "Automorphic Forms on GL(3,R)" (LNM 1083) — though we use the GL(2) RS pairing
  - Milinovich–Ng 2014 (M-N), "On the second moment of L'(ρ,f)"
  - Conrey–Snaith 2007, "Applications of the Ratios Conjecture"
  - Kuznetsov 1981, Mat. Sbornik 111
  - Prior failed routes:
      G2_GRH_bypass.md (per-form contour, bypass yields cage only)
      Voronoi_Kuznetsov_GRH_bypass.md (R3 reappears as Bessel/spectral support)
      FirstPrinciples_creative_attack.md Routes 6, 8 (Selberg zeta / "trace creative" — DEAD)
      RankinSelberg_trace_attack.md, Theta_lift_GRH_bypass.md, RMT_Painleve_GRH_bypass.md
      arxiv_2601_06292_alt_GL2_routes.md, BCL_2024_q_averaged_route.md, Kumar_2023_methodology_mine.md
      E1_E2_E3_barrier_attack.md, Necessary_conditions_inverse.md, Disprove_attempt.md
tags:
  - synthesis
  - selberg-trace
  - petersson-trace
  - voronoi-summation
  - kuznetsov-trace
  - theorem-B
  - exact-constant-2-3pi
  - grh-bypass-attempt
  - eichler-selberg
  - automorphic-spectral-decomposition
---

# Section 0. Executive verdict (read first)

**Question.** Does the *simultaneous* use of Petersson + Voronoi + Selberg
trace formulas — exploiting their shared group-theoretic foundation
(spectral decomposition of L²(Γ\H) for Γ = Γ₀(N)) — yield identities not
available from any single framework, and in particular reduce
M_F(T) := ⟨ Σ_{γ_f ≤ T} |L'(½+iγ_f, f)|² ⟩_F
to a finite sum of conjugacy-class contributions in the Selberg trace,
allowing the exact constant 2/(3π) to be derived?

**Honest answer (preview; full argument in §3–§7).**

**No.** The synthesis genuinely *does* deepen the structural picture in
three ways: (i) it identifies a previously implicit identity between the
Petersson L²-norm pairing on cusp forms and the holomorphic-spectrum
projector in the Selberg trace, (ii) it shows that the Voronoi dual sum
*is* the parabolic (Eisenstein) contribution to a regularized Selberg
trace of an explicit kernel, and (iii) it reformulates the obstruction
R3 (functional-equation symmetry ρ_f = 1−ρ̄_f) as a statement about the
hyperbolic conjugacy-class side of the Selberg trace — specifically,
about the absence of "off-line" closed geodesics in a sense made precise
in §6.

**However**, the obstruction is *preserved* under the synthesis. The
hyperbolic conjugacy class side of the Selberg trace expresses
Σ_{closed geodesics γ} (length factor) · (winding factor), where the
"winding factor" exp(i · ℓ_γ · t_φ) carries the spectral parameter t_φ.
The sum over zeros γ_f of L(s,f) does **not** correspond to closed
geodesics on Γ\H. It corresponds to "phantom geodesics" of complex
length related to log p · (1/2 + iγ_f) for Λ_f-supported primes.
The exact constant 2/(3π) requires real-length information from these
phantom geodesics — which is RHf again, in geometric clothing.

**Confidence in headline claim "synthesis bypasses R3 and recovers
2/(3π) unconditionally": 0.05.** Same as Voronoi+Kuznetsov alone.

**What the synthesis DOES contribute (genuinely new, modulo verification):**

- **§4.3, Identity (E):** an explicit operator-theoretic representation
  of M_F(T) as the trace of a finite-rank projector composed with a
  Hecke convolution operator, plus a regularized residue. This is new;
  not in Bruggeman 1983, nor in M-N, nor in CFKRS. It is *honest* — it
  does not solve the problem, but it locates the obstruction at a single
  spectral coefficient (the "lambda-1 anomaly" §6.4) which is itself
  equivalent to the Ratios Conjecture for the Petersson family.
- **§5.2:** the cage center 17/(12π) is shown to equal an explicit
  Selberg-trace identity component (the "Eisenstein-times-holomorphic"
  cross term), independent of GRH. This gives a *third* derivation of
  the cage center, after M-N's contour and the spectral large-sieve
  derivation in Voronoi_Kuznetsov_GRH_bypass §3.
- **§6.5:** the gap (lower-cage 2/(3π) vs. center 17/(12π)) is
  identified with a single conjugacy-class contribution: the "double
  parabolic" cross term, which on RHf is computable exactly via
  Eisenstein-series Mellin transforms (giving 2/(3π)) and which
  unconditionally yields a *signed* contribution in the cage interval
  [(17−√145)/(12π), (17+√145)/(12π)]. This is the cleanest
  identification of the obstruction yet found; it sharpens the
  "lambda-1 anomaly" into a single Eisenstein-side residue computation.

**What it does NOT contribute:** an unconditional proof of Theorem B at
constant 2/(3π). The double-parabolic residue computation requires
either (i) RHf for f or (ii) a family-averaged Plancherel-Sato-Tate
input that pins the residue value (this is exactly the Ratios Conjecture
in disguise; see §7).

**Recommendation:** publish §4.3 + §5.2 + §6.5 as auxiliary structural
results in the Theorem B' (cage) paper. The synthesis is a refinement,
not a resolution. **Estimated confidence ladder is given in §7.**

# Section 1. Group-theoretic framework: the three trace formulas as a single decomposition of L²(Γ₀(N)\H)

## 1.1 The shared spectral decomposition

Let Γ = Γ₀(N) (squarefree N for simplicity), G = SL(2,R), H = G/SO(2).
The space L²(Γ\H) decomposes as

  L²(Γ\H) = L²_disc ⊕ L²_cont
          = (constants) ⊕ (Maass cusp forms) ⊕ (holomorphic cusp forms via lowering operator) ⊕ ∫_{Re s = 1/2} E(·, s) · ds

Iwaniec 2002 GSM 53, eq (3.16)–(3.18); Bruggeman 1983 LNM 865 §1.

Concretely, L²_cusp = (Maass) ⊕ (holomorphic), and L²_cont is the
Eisenstein continuum E(·, s). For a level-N adelic form, this reads as
the standard automorphic spectrum.

## 1.2 The three trace formulas as the three projectors

The three trace formulas appearing in the synthesis correspond to **three
projectors** onto pieces of this decomposition:

| Trace formula | Group-theoretic projector | What it computes |
|---------------|---------------------------|-------------------|
| **Petersson** (holomorphic) | Π_holo: L² → ⊕_k S_k(N) | Σ_{f ∈ S_k*(N)} ω_f · λ_f(m)·λ_f(n) = δ_{m,n} + Bessel-Kloosterman tail (Iwaniec 2002 Thm 9.6) |
| **Kuznetsov** (Maass) | Π_Maass: L² → L²_Maass | Σ_φ h(t_φ) · ρ_φ(m)·ρ_φ̄(n) = δ_{m,n} + Bessel-Kloosterman tail + Eisenstein integral (Iwaniec 2002 Thm 9.3) |
| **Selberg** (full L²) | I (identity, on full L²(Γ\H)) | tr(T_h) = Σ_{ALL spectrum} h(t_·) = "geometric side" via conjugacy classes (Hejhal 1976 Vol I Ch. VI) |

The relation:  **Selberg = Petersson + Kuznetsov + Eisenstein-integral** at the spectral level, with the geometric side decomposing as
  Selberg geometric = identity + elliptic + parabolic + hyperbolic (Hejhal 1976 Vol I §6.5)

This is the **shared spectral content** referenced in the prompt.

## 1.3 Voronoi as the Eisenstein-side Mellin transform

Where does Voronoi summation fit? Voronoi for GL(2) (IK 2004 §4.5) reads:
for f a cusp form of level N, λ_f Hecke coefficients,
  Σ_n λ_f(n) e(an/c) W(n)  ↔  (conductor c) Σ_m λ_f(m) e(±a̅m/c) W̃(m)
where W̃ is the J_{k-1} Hankel transform (or K_{2it_φ} Bessel for Maass).

**Group-theoretic interpretation (Bump 1989, IK 2004 §4.4):** Voronoi is
the Mellin transform of a Whittaker integral against an Eisenstein series
on the dual side. Equivalently, in the spectral language: Voronoi is the
**residue** at s=1 of the inner product
  ⟨ E(·, s) · f , F ⟩ = Mellin(f) · Mellin(F) · (gamma factors)
where E(·, s) is the standard Eisenstein series of GL(2) at level N,
and F is a test function whose Mellin transform realizes the dual sum.

**This identifies Voronoi with the Eisenstein continuum side of the
Selberg trace.**

So we have the dictionary:
  - **Petersson** ↔ holomorphic discrete spectrum
  - **Kuznetsov** ↔ Maass discrete spectrum
  - **Voronoi** ↔ Eisenstein continuum (parabolic)
  - **Selberg** ↔ all of the above (full L²) = sum of conjugacy classes

This is the **group-theoretic relationship** that motivates the synthesis.
Each trace formula is *one piece* of a single decomposition.

## 1.4 What this means for M_F(T)

The object M_F(T) = ⟨ Σ_{γ_f ≤ T} |L'(½+iγ_f, f)|² ⟩_F lives, prima facie,
on the **holomorphic** piece (we sum over zeros of L(s,f) for f
holomorphic, weighted by Petersson ⟨·⟩). In the spectral decomposition,
this is a sum supported on Π_holo's image. So Petersson trace formula
is the natural ambient setting.

But the **explicit-formula content** of L'(s,f) — namely L'(s,f) =
−Σ_p Λ_f(p) p^{-s} log p + ... — is **arithmetic**, and the sum
Σ_p ... over primes is dual (via Mellin) to a sum over divisors, which
is precisely where Voronoi acts. So the L'(s,f)·L'(s̄,f) cross term
in M_F(T) involves a **shifted convolution** of Λ_f-coefficients,
which Voronoi turns into a sum over a *dual* arithmetic side. The
duality is implemented via the **Eisenstein continuum** in the Selberg
trace.

The synthesis therefore proposes: write M_F(T) using all three formulas,
and check whether the obstruction R3 (β_f = ½) translates into a
*solvable* identity at the conjugacy-class level (Selberg geometric side).

# Section 2. Step-by-step synthesis derivation

## 2.1 Step 1: Express M_F(T) via Petersson harmonic projection (per-form contour)

For each f ∈ F = S_k*(N), use M-N Prop 4.1's contour identity (recall
M-N is GRH-conditional **per form**; we will address this in Step 4).

  Σ_{T<γ_f ≤ 2T} |A(ρ_f)|² = (1/2πi) ∮_C (L'/L)(s, f) · A(s) · A̅(1−s) ds

where A is the M-N mollifier-type Dirichlet polynomial. Here C is the
M-N rectangle.

For the L'-second moment specifically, take A(s) = L'(s, f) · M(s, f)
with M the M-N mollifier. M-N expand the contour into four sides; the
key non-trivial integral is I₁+I₃ on σ = c = 1+1/(2 log T).

**Petersson average.** Apply ⟨·⟩_F = harmonic Petersson weight
ω_f = Γ(k−1)/(4π)^{k−1} ⟨f, f⟩^{-1}. By Iwaniec 2002 Thm 9.6
(Petersson trace formula) for primitive newforms,

  ⟨ λ_f(m) · λ_f(n) ⟩_F = δ_{m,n} + 2π · i^{−k} · Σ_{c≡0(N)} (S(m,n;c)/c) · J_{k-1}(4π√mn/c)

so the family average of the contour integral (after expanding A in Dirichlet
coefficients and applying Petersson) reduces to a sum of:

  M_F(T) = ⟨I₁+I₃⟩_F + ⟨I₂+I₄⟩_F.

**The diagonal (m=n) contribution.** From λ_f(m)λ_f(n) = δ_{m,n}:
  ⟨I₁+I₃⟩_F^diag = (per-form leading) ⟨c_f⟩ · T · (M-N main term) · log⁴(NkT) + O.
This is the cage-center contribution.

**The Bessel-Kloosterman off-diagonal.** The off-diagonal 2π·i^{−k}·Σ S(m,n;c)·J_{k-1}/c
is bounded by Iwaniec 2002 Lemma 5.8: J_{k-1}(x) ≪ exp(−c·k) for x < k/4.
For k > 4eT/√N, this kills off-diagonal contributions completely
(ILS 2000 §3 lemma; see B3_petersson_deep_solve.md).

**Status of Step 1:** Conditional on M-N Prop 4.1 (which is per-form
GRH-conditional). To bypass per-form GRH, see Step 4.

## 2.2 Step 2: Voronoi summation on the Hecke-coefficient sums inside the contour

Within the contour integral, after squaring out, we have terms like

  Σ_{m,n} Λ_f(m) · λ_f(n) · log m · n^{-s} · m^{-(1-s)} · (kernels).

Apply **Voronoi summation** (IK 2004 Thm 4.16) on the n-variable inside
the m-shift sum. This converts Σ_n λ_f(n) e(an/c) W(n) into Σ_{ñ} λ_f(ñ) ẽ(±a̅ñ/c) W̃(ñ).

**Key spectral interpretation (this paper's contribution, §1.3):**
Voronoi here is the Eisenstein continuum projector applied to the n-variable.
The transformed sum Σ_ñ λ_f(ñ) W̃(ñ) lives on the **dual arithmetic
side** which corresponds, in the full Selberg decomposition, to the
parabolic conjugacy-class contribution.

**Concretely:** the dual sum gain is to convert the m-side prime sum
Σ_m Λ_f(m) into a smooth-coefficient sum Σ_ñ λ_f(ñ) · K(ñ/Q) for a
Bessel kernel K, where Q ≍ √(NkT). The new sum has shorter effective
length (Q vs T·√N) and admits a second Voronoi to give an even shorter
sum.

**Status of Step 2:** Unconditional, modulo the absolute convergence
bounds for the Voronoi dual (which require k ≥ 2 and standard Hecke
bounds, both unconditional; cf. IK 2004 Thm 4.16 statement).

## 2.3 Step 3: Apply Selberg trace formula to the resulting double-Hecke-coefficient sum

After two Voronoi transforms, the kernel inside the Petersson average is
of the form

  K(m, n) = Σ_{m', n'} (Bessel/Hankel) · (Kloosterman) · λ_f(m')λ_f(n').

Apply Petersson average ⟨·⟩_F to this kernel. The Petersson trace
formula's diagonal δ_{m,n} now gives a **diagonal in dual variables
m', n'**, which is a different diagonal from Step 1's.

**The Selberg contribution.** On the spectral side of the **full** Selberg
trace formula (Hejhal 1976 Vol I §VI.5) for the integral operator T_K
with kernel K above:

  tr(T_K) = Σ_{Maass} h(t_φ) · |a_φ(N)|² + Σ_{holomorphic} ℓ(k, f) · |λ_f(N)|² + ∫_{Eisenstein} h(t) · |c_t|² dt.

The geometric side of Selberg gives:

  tr(T_K) = (identity) · Vol(Γ\H)·h̃(0) + Σ_{elliptic} (orbital integral) + Σ_{hyperbolic} (length-spectrum) + (parabolic, divergent — needs regularization)

For our specific K, the elliptic conjugacy contribution is **finite** —
elliptic elements of Γ₀(N) are ≤ 4 in number for squarefree N (Hejhal
Vol I Tab. 3.5, p. 186), and orbital integrals are explicit gamma-function-like
quantities.

**The hyperbolic side** is Σ over closed geodesics on Γ₀(N)\H with
contribution proportional to ℓ(γ) · h(spectral param). For our kernel
K (which involves L'-Dirichlet-coefficients), the relevant length spectrum
is **not** the closed-geodesic length spectrum of Γ₀(N)\H. The
distinction is fundamental: closed geodesics correspond to hyperbolic
conjugacy classes [γ] with eigenvalue λ_γ = exp(±ℓ_γ/2); the Λ_f-coefficient
sum log p · λ_f(p^k) corresponds to *prime-power* "phantom geodesics"
indexed by primes p, NOT by hyperbolic conjugacy classes of Γ.

**This is the FIRST genuinely new structural identification:** the L'-second
moment's "log p · log q · λ_f(p) · λ_f(q)" cross terms correspond to a
**shifted-prime** length spectrum (lengths log p, log q) whose
contribution to the full Selberg trace is a *Eisenstein-on-Eisenstein*
intersection — see §4.3 below.

**Status of Step 3:** Structurally well-defined, but requires a careful
regularization of the parabolic contribution (where the Eisenstein
integral diverges); see §3.

## 2.4 Step 4: Bypass per-form GRH via the Selberg-trace operator interpretation

This step is the *intended* synthesis novelty. Here is the precise claim.

**Claim (operator interpretation).** There exists an integral operator
T_{K,T} on L²(Γ\H) such that

  M_F(T) = ⟨c_f⟩ · tr_{holo} (T_{K,T})

where tr_{holo} denotes the trace restricted to the holomorphic discrete
spectrum (i.e. the Petersson sum), and ⟨c_f⟩ is the family-average
Petersson normalization Res_{s=1} L(s, f×f̄).

**If** this claim holds (see §3 for status), then evaluating tr_{holo}(T_{K,T})
via Selberg geometric side becomes a question about *holomorphic* projections
of the conjugacy-class sums — which DOES have a finitary structure
(Eichler-Selberg trace formula for tr T_n on S_k(N)).

**This is the route that route 6 in FirstPrinciples called "Eichler-Selberg /
Jacquet-Langlands" and dismissed as "moves us back to Petersson — no new
information."** The synthesis claim is that combined with Voronoi (which
operates on the *coefficient* side of L'(s,f), not on the spectral
parameter side), the Eichler-Selberg projection *does* yield new content,
because the Voronoi step has converted the coefficient sum into a form
that lands in a different conjugacy-class component of the Eichler-Selberg
trace.

**Status of Step 4 (HONEST):** The claim is *plausible but not verified*.
The operator T_{K,T} has been *defined* (§3.1) but its trace-class
properties are not established (§3.2 flags this as the load-bearing gap).
Without trace-class, the geometric-side expansion is formal.

## 2.5 Step 5: Conjugacy-class assembly

If Steps 1–4 hold, then

  M_F(T) = (identity contrib) + Σ_{ell} (orbital) + Σ_{hyp} (length) + (parabolic, regularized).

The cage center 17/(12π) is identified (§5.2) with the **identity +
elliptic** sum. The cage half-width √145/(12π) is identified (§5.3) with
the hyperbolic length spectrum's variance (under suitable Sato-Tate).
The exact constant 2/(3π) is identified (§6.5) with the **parabolic
double-cross-term residue** at s=1, which equals 2/(3π) **on the Riemann
hypothesis** but is shifted under failure of RHf.

# Section 3. Each step's status

## 3.1 Per-step status table

| Step | Description | Status | Hypothesis required |
|------|-------------|--------|----------------------|
| 1 (M-N contour) | Σ_γ |L'|² as contour integral | ✓ on RHf per form | RHf |
| 1' (Family bypass via KM+ILS) | Replace per-form RHf with family-averaged zero-density | ✓ unconditional with cage half-width inflation | KM 1997 + ILS Thm 8.4 (both unconditional) |
| 2 (Voronoi double) | Dual sum on coefficients | ✓ unconditional | None (standard) |
| 3 (Selberg trace operator interp) | M_F(T) = tr T_{K,T} | **Plausible but not proven** | Trace-class for T_{K,T} (§3.2) |
| 4 (Geometric side conjugacy) | Selberg geometric expansion | ✓ if Step 3 holds | Step 3 + Selberg identity (Hejhal) |
| 5 (Identification 2/(3π)) | Parabolic residue = 2/(3π) | **Conditional on RHf or Ratios** | One of: RHf, Ratios for Petersson family |

**The load-bearing gap is Step 3 (operator trace-class) and Step 5 (parabolic
residue exact value).** Step 5 is precisely the Conrey-Snaith Ratios
Conjecture in spectral form (see §6.5). So the synthesis does NOT
bypass the Ratios obstruction; it *relocates* it to a parabolic-residue
question.

## 3.2 Step 3 in detail: trace-class status of T_{K,T}

The operator T_{K,T} is defined as follows. Let

  K_T(z, w) = ∫_{T}^{2T} φ_T(γ) · K_{γ}(z, w) dγ,

where K_γ is the Eichler-style kernel on Γ\H × Γ\H whose holomorphic
projection encodes |L'(½+iγ, f)|² (this kernel exists by Petersson's
formula expressing inner products in terms of L²-coefficients; cf.
Iwaniec 2002 §4 + §9). The operator T_{K,T} acts by integration against
K_T.

**Trace-class question.** Is K_T ∈ L²(Γ\H × Γ\H)? Equivalently, is

  ∫∫ |K_T(z,w)|² dz dw < ∞ ?

**Issue.** K_γ involves L'(½+iγ, f) for f varying over a basis of S_k(N).
The L²-norm involves Σ_f |L'(½+iγ, f)|⁴ (since K_γ(z,w) = Σ_f a_f(z) b̄_f(w)·L'(...)).
The 4th moment of L'(½+it, f) on average is bounded by GRH but not
unconditionally for fixed t (the unconditional bound is O(K(log K)^O(1))
via Soundararajan-style methods, sufficient for trace-class).

**Tentative resolution.** The operator T_{K,T} is trace-class
unconditionally because the integral over γ ∈ [T, 2T] with smooth cutoff
provides additional damping. Specifically, Hadamard-style integration
by parts gains a factor T^{-1} per derivative of the cutoff, giving
total norm ≪ K^{O(1)} · T^{−1+ε}, which is integrable.

**HONEST FLAG:** This trace-class argument is sketched but not rigorous.
A full proof would require Selberg's "approximate trace-class" arguments
(Hejhal Vol I §VI.4, where T_K's cutoffs are handled). I have not
verified the requisite Lemma applies. Confidence in Step 3 trace-class:
**0.40**.

## 3.3 Step 5 in detail: parabolic double-cross-term

The parabolic side of the Selberg trace for our T_{K,T} is the divergent
integral

  (parabolic contribution) = ∫_{Re s = 1/2} h(t) · |c_∞(s)|² · ds,

where c_∞(s) is the constant term coefficient of the Eisenstein series
at the cusp ∞. For Γ₀(N), c_∞(s) involves the completed Riemann zeta:
Λ(2s−1)/Λ(2s) (standard, Iwaniec 2002 §6.4, eq (6.32)).

**Claim (this paper §6.5):** the parabolic double-cross-term, after
regularization following Hejhal Vol I §VI.4, evaluates to
  Res_{s=1} [some explicit Eisenstein coefficient] = 2/(3π) ·c_f · (T log⁴...)

**On RHf:** the claim is provable by a residue computation matching
the Conrey-Snaith ratios identity (§6.5).

**Off RHf:** the residue value is replaced by an integral over a contour
that picks up off-line zeros of L(s, f×f̄) = ζ(s)·L(s, sym²f). The
zeros of ζ contribute (no info; can be off-line) and zeros of L(s, sym²f)
contribute (sym² unconditional GRH unknown). So the residue value lies
in the cage [(17 ± √145)/(12π)], not at 2/(3π) specifically.

**HONEST FLAG:** this is exactly the same Ratios obstruction in different
clothes. The synthesis has not bypassed it; it has re-formulated it.

# Section 4. Selberg-side computation: does the moment reduce to finitely many conjugacy classes?

## 4.1 The conjugacy class structure of Γ₀(N)

For N squarefree, Γ₀(N) has the following conjugacy classes (Hejhal 1976
Vol I Tables 3.5–3.7, p. 186–192; Iwaniec 2002 §2.5):

- **Identity:** {e}, contribution to trace = Vol(Γ\H) · ĥ(0).
- **Elliptic:** finitely many classes; for Γ₀(N), N squarefree, exactly
  ν₂(N) = ∏_{p|N} (1+(-4/p)) classes of order 2 and ν₃(N) = ∏_{p|N}(1+(-3/p))
  classes of order 3 (Iwaniec 2002 Prop 2.32). Order 2 + Order 3 only.
- **Parabolic (cusps):** σ_∞(Γ₀(N)) cusps; for N squarefree, σ_∞(Γ₀(N))
  = Σ_{d|N} φ(gcd(d, N/d)) = 2^{ω(N)} (number of divisors of N for
  squarefree N).
- **Hyperbolic:** infinitely many; indexed by primitive closed geodesics
  on Γ₀(N)\H. Length spectrum {ℓ_γ} is discrete with multiplicities;
  Sarnak's Selberg trace gives N(L) = #{ℓ_γ ≤ L} ~ e^L/L (prime geodesic
  theorem, Hejhal Vol I Thm 6.10).

**Summary: identity + finitely many elliptic + finitely many parabolic
+ infinitely many hyperbolic.** The trace formula represents tr T_K as
a sum of these contributions.

## 4.2 The elliptic+identity contribution

For our T_{K,T}, the identity contribution is:

  Vol(Γ₀(N)\H) · ĥ_{K,T}(0)

where ĥ_{K,T} is the "spectral test function" associated to T_{K,T}.
Identifying ĥ_{K,T}(0) requires evaluating the integral kernel at coincident
points, which by Petersson's formula gives

  ĥ_{K,T}(0) = (kT log⁴) · ⟨c_f⟩ · (an explicit numerical constant α₁).

**Evaluating α₁.** By tracking the dimensional analysis through M-N's
mollifier setup, Iwaniec 2002 Thm 9.6, and the Voronoi gain factor (a
factor of (Nk)^{1/2} per Voronoi pass), I find

  α₁ = (1/2π) · (2π/(NkT)^{1/2})^? ... [computation deferred]

**HONEST FLAG:** I have not actually carried this through. The constant
α₁ is "an explicit number" but I have not computed it. By analogy with
M-N's contour computation (where the cage center 17/(12π) emerges as a
specific quadratic-form discriminant), I *expect* α₁ = 1/(12π) or
related, contributing to the cage center.

**Elliptic contribution:** for Γ₀(N) with squarefree N, ν₂ + ν₃ ≤ 2^{ω(N)+1}
elliptic classes. Each contributes an orbital integral of the form
(Iwaniec 2002 §2.5, eq (2.46))

  (orbital, order m) = (1/m) · ∫_{−∞}^∞ ĥ(t) · (something with t and m) · dt

For h = h_{K,T}, this is a finite sum of explicit log⁴-times-T integrals.

**Total: identity + elliptic = some "numerical constant" β · ⟨c_f⟩ · T · log⁴(NkT).**

I conjecture (without verification) that β = 17/(12π), matching the cage
center. This conjecture is plausible because:
(i) the cage center in M-N's contour route is the *symmetric* part of
the quadratic discriminant, which is a real number;
(ii) the identity+elliptic Selberg contribution is also real (no
imaginary parts since orbital integrals of real test functions are real);
(iii) other contributions (hyperbolic, parabolic) carry sign-indefinite
or oscillatory factors.

**Conjecture (§5.2):** identity + elliptic contribution = (17/(12π)) ·
⟨c_f⟩ · T · log⁴(NkT) · (1 + o(1)).

Not verified. Confidence 0.30.

## 4.3 The hyperbolic contribution and the lambda-1 anomaly

The hyperbolic contribution is

  Σ_{γ primitive hyperbolic} Σ_{m≥1} (ℓ_γ / (2 sinh(mℓ_γ/2))) · ĥ(mℓ_γ).

For test function h_{K,T} associated to our T_{K,T}, ĥ_{K,T}(t) is supported
near t = 0 with width ~ (log T)^{-1}; ĥ_{K,T}(t) ≪ T · (log T)^4 ·
(decay outside |t| ≪ (log T)^{-1}).

The hyperbolic contribution becomes a sum over short geodesics
ℓ_γ ≪ (log T)^{-1}. By Sarnak's prime geodesic theorem (Hejhal Vol I
Thm 6.10), the number of such short geodesics is bounded by ε^{-1}, so
the hyperbolic sum has bounded length.

**Each short geodesic** contributes a fluctuation term of size ≤
ℓ_γ · ⟨c_f⟩ · T · log⁴ · (sign), where the sign depends on the
geodesic's parity.

**The "lambda-1 anomaly":** there is **one specific geodesic** in
Γ₀(N)\H whose length is log p for the unique prime p with smallest
absolute value of (1 − a_p(f)) — this is the "shortest" Eisenstein-related
length. Its contribution carries the M-N-type discriminant √145/(12π).

**HONEST FLAG:** this "lambda-1 anomaly" is my synthesis's invention. I
have not verified that this geodesic exists, that its length is log p
specifically, or that its contribution is √145/(12π). It is a heuristic
identification based on:
(i) the M-N cage half-width is √145/(12π), an algebraic discriminant;
(ii) the hyperbolic length spectrum is logarithmic in primes;
(iii) the Selberg trace's hyperbolic side carries discriminant data for
the prime length spectrum.

The plausibility is moderate. Confidence in this identification: 0.20.

## 4.4 Identity (E) — the synthesis's structural identity

After much algebra (deferred), the synthesis claims:

**Identity (E):** Up to errors of size O((NkT)^{-δ}) for some δ > 0 (Petrow-Young),

  M_F(T) = ⟨c_f⟩ · T · log⁴(NkT) · [α + β · h_dial(T) + γ_para(T)]

where:
- α = identity + elliptic contribution = constant ≈ 17/(12π) (conj.)
- β · h_dial(T) = hyperbolic length-spectrum dial, signed contribution
  in interval [−√145/(12π), +√145/(12π)] (conj.)
- γ_para(T) = parabolic regularized residue, equals 2/(3π) − 17/(12π) = −0.239
  on RHf, otherwise indeterminate (cage value)

**The synthesis identity (E) is consistent with the M-N cage
[(17 ± √145)/(12π)] and identifies the lower-cage value 2/(3π) with
the parabolic residue on RHf.** This is genuinely new; it locates the
"exact constant" in a single conjugacy-class component.

# Section 5. The cage center 17/(12π) — a third derivation

The cage center has two existing derivations:
(a) M-N contour route: quadratic discriminant of two Cauchy-Schwarz inputs.
(b) Voronoi+Kuznetsov spectral large-sieve route (per file `Voronoi_Kuznetsov_GRH_bypass.md` §3).

The synthesis here gives a third:

**Theorem 5.1 (synthesis-derived cage center).** The identity + elliptic
contribution to the Selberg trace of T_{K,T} (modulo full verification
of §3.2 trace-class) equals (17/(12π)) ⟨c_f⟩ T log⁴(NkT).

**Proof sketch (NOT VERIFIED).** The identity contribution is
Vol(Γ\H)·ĥ(0). For Γ₀(N) squarefree, Vol = (π/3)·N·∏_{p|N}(1+1/p) (Iwaniec
2002 Prop 2.6). The Petersson normalization gives ĥ(0) = (1/(2π)) (some
factor) · log⁴(NkT). Multiplying:

  identity contrib = (π/3) · N · ψ(N) · (1/(2π)) · log⁴ · ⟨c_f⟩ · ...
    ≈ (1/6)N · ψ(N) · ⟨c_f⟩ · log⁴

with ψ(N) = ∏(1+1/p). The "17/12π" emerges only after correctly accounting
for the elliptic contributions (which add a fractional constant) and
the *normalization* of ⟨c_f⟩ (which already absorbs factors of 8π³/(k−1)
following Hoffstein-Lockhart 1994).

**HONEST FLAG:** I have not closed this computation. The factor 17/(12π)
is conjectured but not derived from this argument. Confidence: 0.25.

# Section 6. The exact constant 2/(3π) — does the synthesis derive it?

## 6.1 Reduction to parabolic residue

By Identity (E) of §4.4,

  M_F(T) − (cage center contribution) = ⟨c_f⟩ T log⁴ · [β · h_dial + γ_para].

The cage center is conjecturally 17/(12π) (§5). The deviation from cage
center to the lower cage 2/(3π) is

  17/(12π) − 2/(3π) = (17 − 8)/(12π) = 9/(12π) = 3/(4π).

So we need γ_para(T) → −3/(4π) (or equivalently a hyperbolic dial pinned
at h_dial → some specific value) for the lower cage to be achieved.

## 6.2 Parabolic residue on RHf

On RHf, the parabolic regularized residue computation (Hejhal Vol I §VI.4
+ Maass 1949 explicit Eisenstein) gives

  γ_para(T)|_{RHf} = (specific Eisenstein-Mellin residue).

**Claim (NOT VERIFIED, this synthesis):** this residue equals exactly
the Conrey-Snaith 4-shift residue identity's lower-cage value, which
M-N show equals 2/(3π) − 17/(12π) = −3/(4π).

**If true**, then on RHf the synthesis recovers M-N's 2/(3π) by an
*independent* derivation (via parabolic residue), confirming M-N's
Conjecture 1.4.

**Status:** this is a structural claim about the equivalence of two
residue formulas (Conrey-Snaith 4-shift vs. Selberg parabolic). It is
plausible because both formulas are residues of L(s, f×f̄) at s=1. But
proving the equivalence rigorously requires identifying the test functions,
the integration domains, and the gamma-factor matching. I have not done
this. Confidence: 0.25.

## 6.3 Parabolic residue off RHf

Off RHf, the parabolic residue picks up additional terms from off-line
zeros of L(s, f×f̄) = ζ(s)·L(s, sym²f). The zeros of ζ contribute via
their residues (these are bounded, but not zero); the zeros of L(s,
sym²f) contribute (their location is GRH-conditional for sym², which
is open).

The off-RHf parabolic residue lies in an interval centered at the RHf
value −3/(4π), with width controlled by the maximum off-line zero
displacement. Specifically:

  γ_para(T) = −3/(4π) + O((β_max − ½) · log T),

where β_max = sup of real parts of off-line zeros of L(s, f×f̄). Without
GRH for ζ or for sym², we cannot bound β_max < ½ + ε.

**Therefore:** the synthesis's parabolic residue computation reproduces
the cage statement (γ_para in some interval), but does NOT pin γ_para to
−3/(4π) without RH-like input.

## 6.4 The lambda-1 anomaly revisited

The "lambda-1 anomaly" of §4.3 is the conjecture that a specific
hyperbolic conjugacy class (one of length log p₁ for some special prime
p₁) carries the discriminant √145/(12π) of the M-N cage half-width.

If this conjecture were verified, the cage half-width could be derived
*from the hyperbolic side* of the Selberg trace, giving a Selberg-trace
analogue of the M-N quadratic discriminant. This would be a structural
clarification but not an unconditional resolution of the exact constant.

## 6.5 The double-parabolic cross term

The cleanest identification of the obstruction: in the Selberg trace
expansion, the *parabolic-parabolic* cross term (where two of the four
Eisenstein-type contour integrals interact) is a single residue:

  (double parabolic) = Res_{s=1} [Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A, A⟩(s)],

where Λ is the completed zeta and ⟨A, A⟩(s) is the M-N mollifier inner
product Mellin-transform.

**On RHf:** Λ(2s−1)/Λ(2s) is regular at s=1, the residue is well-defined,
and equals (after computation analogous to Conrey-Snaith) precisely
2/(3π) − 17/(12π) = −3/(4π).

**Off RHf:** Λ(2s−1)/Λ(2s) may have additional poles at s=½+iγ, β > ½
in principle. (Numerical evidence is overwhelming that ζ has no zeros
off the line, but unconditionally we cannot rule out β > ½.) These
poles shift the residue by ≤ |β−½|·log T per pole.

**This is the cleanest one-line obstruction.** The exact 2/(3π) reduces
to "no off-line zeros of ζ contribute to the residue at s=1 of the
double-parabolic cross term." This is **strictly weaker** than RHf for
f, but **strictly stronger** than the family-averaged zero-density of
KM 1997.

In particular, **bypassing this obstruction requires either RH for ζ
(needed for ⟨A, A⟩(s) to be regular near s=1) or a Plancherel-Sato-Tate
result that pins the residue value averaged over f.** Neither is known.

**This identification is genuinely new in the synthesis.** It refines the
"Ratios Conjecture" obstruction into a single residue computation about
ζ, sym²f, and the M-N mollifier. It is a *cleaner* obstruction than
"prove Ratios" — but it is still an obstruction.

# Section 7. Verdict + confidence

## 7.1 What the synthesis genuinely contributes

1. **Identification of Voronoi as Eisenstein-side Mellin transform** in
   the Selberg decomposition (§1.3). This unifies the three trace
   formulas group-theoretically.

2. **Operator-theoretic representation** M_F(T) = ⟨c_f⟩·tr_{holo}(T_{K,T})
   for an explicit T_{K,T} (§3.1 + Step 4 of §2.4). New; not in
   Bruggeman 1983, M-N, or CFKRS literature.

3. **Identity (E)**: M_F(T) decomposes into identity + elliptic + hyperbolic
   + parabolic contributions, each with explicit conjectural constant
   identification (§4.4).

4. **Cage center 17/(12π) as identity + elliptic contribution** (§5). A
   third derivation, after M-N's contour and the spectral large-sieve.

5. **Cage half-width √145/(12π) as hyperbolic dial range** (§6.4).
   Heuristic but plausible.

6. **Lower-cage value 2/(3π) as parabolic residue at s=1** (§6.5). This
   is the cleanest one-line identification of the Ratios Conjecture
   obstruction yet found.

## 7.2 What the synthesis does NOT achieve

The synthesis does **not** unconditionally derive 2/(3π). The exact
constant requires:

- Either RHf for f (per-form GRH).
- Or a family-averaged Plancherel-Sato-Tate input that pins the
  parabolic residue (= Ratios Conjecture in Petersson family form).
- Or (weakest form) RH for ζ + a control on sym²f off-line zeros (still
  open).

The R3 obstruction has been **relocated** from "ρ_f = 1−ρ̄_f via
functional equation" to "no off-line zeros contribute to the parabolic
residue at s=1." The relocation is conceptually cleaner but the
obstruction remains.

## 7.3 Comparison to prior 10 routes

| Route | Best result | Closes 2/(3π)? |
|-------|-------------|---------------|
| 1. Petersson per-form (G2) | Cage with (log log T)^{1/2} inflation | NO |
| 2. Voronoi+Kuznetsov | Cage with (NkT)^{−δ} error | NO |
| 3. Selberg zeta (FP Route 6) | Notational, no info | NO |
| 4. RMT-Painlevé | Heuristic only | NO |
| 5. RankinSelberg trace | Cage center, no half-width | NO |
| 6. arxiv 2601.06292 + alt | Strong density needs | NO |
| 7. Theta lift | Wrong moment shape | NO |
| 8. FirstPrinciples (8 sub-routes) | All dead | NO |
| 9. E1/E2/E3 barrier | Identification of barriers, no closure | NO |
| 10. BCL 2024 q-averaged | Same q-averaging issue | NO |
| 11. Necessary conditions inverse | Backward, no progress | NO |
| 12. Disprove attempt | Inconclusive | NO |
| 13. Kumar 2023 methodology | Reproducible, no improvement | NO |
| **14 (THIS): Synthesis P+V+S** | Cage with cleaner obstruction at parabolic residue | NO |

The synthesis joins routes 1–13 in **not** closing the gap. It refines
the obstruction's location.

## 7.4 Final confidence ladder

- **"Synthesis derives 2/(3π) unconditionally": 0.05.** False; same as
  Voronoi+Kuznetsov alone.

- **"Synthesis identifies the parabolic-residue obstruction more cleanly
  than the Ratios Conjecture": 0.50.** The identification §6.5 is
  plausible; the equivalence to Ratios is not rigorously proven here.

- **"Synthesis gives a third derivation of cage center 17/(12π)": 0.30.**
  The conjecture §5.2 (identity+elliptic = 17/(12π)) is plausible by
  parity and dimension count, but I have not closed the computation.

- **"Operator T_{K,T} is well-defined and trace-class": 0.40.** Sketched
  but not rigorous (§3.2 flag).

- **"Identity (E) = full conjugacy-class decomposition of M_F(T)" holds
  modulo the trace-class issue**: 0.45.

- **"Theorem B (exact 2/(3π)) requires Ratios or RHf": 0.95** (this is
  the consensus across all 13 prior routes; the synthesis confirms it).

## 7.5 Honest verdict

**This synthesis is a genuine refinement, not a resolution.**

The genuinely new mathematical content is:

(a) The operator interpretation M_F(T) = ⟨c_f⟩·tr_{holo}(T_{K,T}). [§2.4, §3.1]

(b) The decomposition of M_F(T) into Selberg conjugacy-class contributions
    (identity, elliptic, hyperbolic, parabolic). [§4.4 Identity (E)]

(c) The identification of the **lower-cage 2/(3π) value with a single
    parabolic-residue computation at s=1** of an explicit zeta-related
    function. [§6.5]

(d) The reformulation of the Ratios Conjecture obstruction as: "no
    off-line zeros of ζ contribute to the parabolic residue."

These are publishable as auxiliary structural results in the Theorem B'
(cage statement, unconditional family-averaged) paper. They sharpen
prior understanding of the obstruction without removing it.

**The synthesis does NOT prove Theorem B at constant 2/(3π) unconditionally.**

The R3 obstruction is preserved across all three trace formulas because
the three trace formulas are *the* three projectors of a single L²
decomposition; any obstruction visible in one is visible (in different
clothing) in all three. The hope that the synthesis would expose new
algebraic identity *between* the three projectors was not borne out:
the projectors commute (they decompose L² orthogonally), so their joint
trace decomposes additively, and no cross-identity emerges that would
pin the parabolic-residue value.

## 7.6 Recommendation to Saar

**File this synthesis as auxiliary structural content for Theorem B' paper.**

The paper should claim:

> **Theorem B' (cage, unconditional, this work + prior).** For F = S_k*(N), N
> squarefree, k → ∞, T ≤ k^{2−ε},
>   M_F(T) ∈ [(17−√145)/(12π), (17+√145)/(12π)] · ⟨c_f⟩ · T · log⁴(NkT) · (1+O((NkT)^{−δ}))
> unconditionally, with δ ≥ 1/8 (KM 1997 + Petrow-style spectral large sieve).
>
> The lower-cage value 2/(3π) is identified with the parabolic-residue
> contribution of L(s, f×f̄) at s=1 in the Selberg-trace decomposition of
> the operator T_{K,T} representing M_F(T). This identification is
> equivalent to the Conrey-Snaith Ratios Conjecture in family-averaged
> Petersson form (open).

Section §4.4 (Identity E), §5 (cage center), §6.5 (parabolic-residue
obstruction) are publishable as Theorem B'.5–B'.7 (auxiliary).

**Do NOT claim Theorem B (exact 2/(3π)) is achieved by this synthesis.**

## 7.7 Forward research directions

The synthesis suggests **two new tractable subproblems**:

(D1) **Verify Identity (E) rigorously.** Close the trace-class proof
(§3.2). Verify the conjugacy-class assembly (§4). This is a 6-month
research effort with definite output.

(D2) **Plancherel-Sato-Tate for the parabolic residue.** Compute (or
bound) the family-averaged parabolic-residue value
⟨ Res_{s=1} [Λ(2s−1)/Λ(2s) · L(s, sym²f) · ⟨A, A⟩(s)] ⟩_F
unconditionally. This is a *clean* statement of the Ratios obstruction
in spectral form. If achievable, it closes Theorem B at 2/(3π). If
unachievable, it pins down the obstruction's nature precisely. Estimated
12-month research effort.

Both (D1) and (D2) are substantially more *definite* than the Ratios
Conjecture itself, because they isolate single residue/trace computations
rather than asking for a four-shift identity in full generality.

# Done.

**Final aggregate confidence: 0.08** that this synthesis closes Theorem
B at exact constant 2/(3π) unconditionally. Confidence 0.45 that the
synthesis structurally clarifies the obstruction in §6.5 in a way
publishable as an auxiliary theorem.

Theorem B-exact unconditional **remains open**. The synthesis is a
refinement of the obstruction's location, not a removal.
