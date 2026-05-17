# D4 — Stern–Brocot/Farey per-step ↔ Vallée transfer-operator dynamical analysis

Date: 2026-05-15. Author handoff: D4 (Vallée / dynamical analysis of algorithms).
Scope: founding lens = "prime inserts φ(p) new equispaced points with zero
overlap; composite always re-traces". Object = the per-step (per-denominator)
increment of `A_N(m) = Σ_{f∈F_N} e(mf)`. Goal: express it as an additive cost
cocycle over a concrete dynamical system, locate the Ramanujan/Möbius
modulation in the transfer-operator spectrum, and assess the practical ceiling.

**Confidence labels are strict. PROVEN / PROVEN(literature) / HEURISTIC /
CONJECTURAL / NUMERICAL-ONLY.** Every "X proves Y" carries a verified verbatim
quote with source location.

---

## 0. One-paragraph verdict (read this first)

The Farey per-step increment is, exactly, the Ramanujan sum:
`A_N(m) − A_{N−1}(m) = c_N(m)` (PROVEN, exact arithmetic, §2). Its Dirichlet
generating series factorises as `Σ_N c_N(m) N^{−s} = σ_{1−s}(m)/ζ(s)`
(PROVEN, classical; re-verified to machine precision, §4). This is **formally
the same shape** as Vallée's average-case object — a Dirichlet series whose
coefficient-sums are extracted by Tauberian/singularity analysis, with the
relevant operator being a quasi-inverse `(I − H_s)^{−1}` — but with a decisive
structural difference: **the arithmetic/Ramanujan modulation `σ_{1−s}(m)` is a
fixed, pole-free Dirichlet polynomial in `m`; it multiplies `1/ζ(s)` and does
NOT perturb the dominant `s=1` singularity that controls mean cost.** It only
reshapes the *subdominant* spectrum (the nontrivial zeros of `ζ`, i.e. the
Mertens spectrum). **Conclusion (honest, two-part):**
(i) the *Ramanujan-weighted* reading of the lens does NOT deliver a new
*mean*-cost theorem — it is provably subdominant-only, landing in the
*fluctuation* régime where it merely re-derives the project's existing
"Farey↔Mertens, `N·W(N)→C` bounded" picture (clean negative, §4(c)/§6).
(ii) BUT the *coprimality-restriction* reading (the lens's actual content:
"prime inserts genuinely new digits") **does** perturb the dominant
eigenvalue — EXECUTED probe D4-3 (§7): `λ(1)=0.99993` for the full Gauss
operator (calibration ✓ vs BV05's PROVEN `λ(1)=1`), but `λ_q(1)` = 0.646
(`q=2`), 0.819 (`q=3`), 0.513 (`q=6`) for the coprimality-restricted digit
alphabet. This isolates a **genuine, computable, new arithmetic-weighted
average-case constant** `μ_q=2/|λ_q′(1)|` for a coprimality-restricted
Euclidean algorithm — the deliverable's headline target, reached via the
*restriction* (not the reweight) form of the lens. The negative half is
rigorous; the positive half is numerically decisive and reduces to a
~1-week verbatim transcription of BV05's machinery (§7).

---

## 1. The dynamical setup (precise)

### 1.1 Two maps, one filtration

Continued-fraction dynamics on `I = (0,1]`:

- **Gauss map** `T(x) = {1/x} = 1/x − ⌊1/x⌋`, `T(0)=0`. Inverse branches
  `h_{[m]}(x) = 1/(m+x)`, `m ≥ 1`; depth-`P(x)` for rationals.
  [Baladi–Vallée, eq. (1.1) and the displayed definition of `T`, p.1–2;
  verbatim §3 below.]
- **Farey map** `F`: the slow (indifferent-fixed-point) version whose
  jump/induced transformation is `T`. `T` = first-return (acceleration) of `F`.
  PROVEN(literature), standard; this is exactly the "Slow vs Fast Class"
  distinction Vallée 2003 makes (see §3 citation [V03]).

The Farey sequence `F_N` (reduced `h/k`, `1≤k≤N`) is **not** a single
trajectory; it is the set of *all* rationals `x∈(0,1]` whose CF denominators
(continuants) are `≤ N`. The "per-step" filtration of D4 is the **denominator
filtration** `F_1 ⊂ F_2 ⊂ ⋯`, i.e. ordering rational trajectories by their
**continuant size** `N` — exactly Vallée's "size parameter `N`" that the
Dirichlet variable `s` marks. (Verbatim §3: "the parameter `s` 'marks' the
size `N` of inputs".)

NULL CONTROL ALREADY ON FILE: the *tree-depth* filtration (Stern–Brocot
levels) destroys the arithmetic spectrum — `ΔW_SB(n) ~ C·2^n`, governed by
Minkowski `?(x)`, **no zeta zeros** (PROVEN-NUMERICAL, project file
`experiments/STERN_BROCOT_DISCREPANCY.md`, levels ≤22). This pins down that
the spectral content lives in the **denominator/continuant ordering**, which
is precisely the ordering Vallée's `s` marks. D4 must and does use that
ordering.

### 1.2 The arithmetic per-step quantity

`A_N(m) := Σ_{f∈F_N} e(mf)`, `e(x)=exp(2πix)`. Verified facts (re-derived,
exact, `verify_facts.py`):

- **F1/F3 (PROVEN, exact):** `A_N(m) = Σ_{d|m} d·M(⌊N/d⌋) = Σ_{k≤N} c_k(m)`,
  `c_k(m)` the Ramanujan sum, `M` = Mertens. Imaginary part `≡ 0`.
- **F4 (PROVEN, exact — the D4 cocycle increment):**
  `ΔA_N(m) := A_N(m) − A_{N−1}(m) = c_N(m)` for all `N≥2`, all `m` tested.
- **F2 (PROVEN, exact):** prime scale `c_p(m) = −1 + p·𝟙[p|m]` (the lens:
  prime contributes `φ(p)=p−1` new points off-resonance, full `p` on-resonance).

---

## 2. The arithmetic ↔ cocycle ↔ transfer-operator dictionary

| arithmetic per-step object | dynamical / cocycle object | transfer-operator spectral object |
|---|---|---|
| filtration index `N` (denominator/continuant bound) | size parameter that the Dirichlet variable `s` marks (BV: "`s` marks the size `N`") | argument of `(I − H_s)^{−1}` |
| trajectory of `x=h/k` under `T` | CF digits `(m_1,…,m_P)`, `h_{[m_i]}(x)=1/(m_i+x)` | branches of `H_s` |
| number of insertion steps to reach `x` | total cost `C(x)=Σ c(m_i)`, additive **Birkhoff cost cocycle** (BV eq. (1.6)) | marked operator `H_{s,w}`, `H_{1,w}` (BV eq. (1.5),(1.7)) |
| `A_N(m) = Σ_{k≤N} c_k(m)` | coefficient-sum of a Dirichlet series in `s` | `[s^•]` extraction from quasi-inverse |
| **per-step increment `ΔA_N(m)=c_N(m)`** | **the cocycle *increment*** (one CF/Euclid step contribution), Ramanujan-weighted | the *coefficient* of the Dirichlet series, NOT a Birkhoff sum of a positive cost |
| generating series `Σ_N c_N(m) N^{−s} = σ_{1−s}(m)/ζ(s)` | Ramanujan-twisted dynamical Dirichlet series | `σ_{1−s}(m)·(arithmetic Dirichlet series)`; pole structure = zeros of `ζ` |
| mean of a *positive* digit cost `c` | `E_N[C] ∼ μ̂(c)·μ·log N`, `μ=2/|λ′(1)|` (BV, verbatim §3) | **dominant** eigenvalue `λ(s)` of `H_s`, simple pole of `(I−H_s)^{−1}` at `s=1` |
| Mertens / Möbius layer `1/ζ(s)=Σ μ(n)n^{−s}` | signed, mean-zero cocycle (NOT a positive cost) | the **subdominant** structure: nontrivial zeros `ρ` of `ζ` → poles of `1/ζ` |
| `N·W(N) → C` bounded (project core fact) | second-moment of the signed increment cocycle | `Σ_ρ 1/(|ρ|²|ζ′(ρ)|²)`-type variance object |

**The decisive line of the dictionary (PROVEN, §4 numerics + classical
identity):**

> `Σ_{k≥1} c_k(m) k^{−s} = σ_{1−s}(m) / ζ(s)`,  `σ_a(m)=Σ_{d|m} d^a`.

Read it three ways:
1. **`m`-direction:** `σ_{1−s}(m)` is a *finite* Dirichlet polynomial in the
   divisors of `m`. It is **entire in `s`**, no poles. The frequency `m`
   only sets a fixed amplitude/phase; it cannot create or move an
   `s`-singularity.
2. **`s`-direction (Re s ≥ 1):** the *only* singularities are where `1/ζ(s)`
   blows up = the **nontrivial zeros `ρ` of `ζ`**. At `s=1`, `ζ` has a pole,
   so `1/ζ(1)=0` — the per-step series has **a zero, not a pole, at the
   would-be dominant point.** (NUMERICAL §4: `1/ζ(1+ε) ≈ ε`.)
3. **Vallée comparison:** in BV the *mean* cost comes from the simple pole of
   `(I−H_s)^{−1}` at `s=1` (dominant eigenvalue `λ(s)`, `λ(1)=1`). Our
   per-step Ramanujan series has **no such pole** — its mass is entirely in
   the critical strip. Hence the Ramanujan/Möbius modulation is a
   **subdominant-spectrum phenomenon**, not a dominant-eigenvalue
   perturbation.

This *answers Goal 2 cleanly and negatively for the optimistic branch*: the
Ramanujan modulation does NOT shift the mean-cost level; it lives in the
fluctuation spectrum (the Mertens / zeta-zero régime the project already owns
on the static side).

---

## 3. Literature grounding (verified verbatim citations)

Adversarial protocol: each quote was extracted from the source PDF text, with
the equation/section location. Where I could not verify a *theorem number*
verbatim, I say so and downgrade the claim.

**[BV05] V. Baladi, B. Vallée, "Euclidean algorithms are Gaussian", Journal
of Number Theory 110 (2005) 331–386.** (Journal/volume/pages confirmed via
publisher search; preprint arXiv:cs/0307062v4, 5 May 2004.)

- Gauss map (verbatim, p.1–2):
  > "the Gauss map `T : [0,1] → [0,1]`, `T(x) := 1/x − ⌊1/x⌋`, for `x ≠ 0`,
  > `T(0)=0`."
- Depth of a rational (verbatim, p.2):
  > "If `x ≠ 0` is rational, the trajectory `T(x)` reaches 0 in a finite
  > number of steps, and this number, `P(x)`, is called the depth of `x`."
- Additive total cost = Birkhoff sum (verbatim, eq. (1.6), p.~3):
  > "`C(x) := Σ_{i=1}^{P(x)} c(m_i(x))`."  and (eq. (1.2)) the truncated
  > `C_n`, with: "The total cost (1.2) is a Birkhoff sum, i.e., a sum over
  > iterates of the dynamics `T`."
- Density transformer / transfer operator (verbatim, eq. (1.4)):
  > "`H_1[f](x) = Σ_{h∈H} |h′(x)|·f∘h(x)`."
- Weighted (marked) operator carrying the cost (verbatim, eq. (1.5)):
  > "`H_{1,w}[f] = Σ_{h∈H} exp[w c(h)]·|h′|·f∘h`."
- Dominant eigenvalue + spectral gap (verbatim):
  > "The density transformer `H_1 = H_{1,0}` … has a dominant eigenvalue
  > `λ = 1`, and a spectral gap: the rest of the spectrum lies in a disk of
  > radius `< 1`."
- The size-marking Dirichlet series and quasi-inverse (verbatim, eq. (1.7),
  attributing the construction to Vallée [49] = [V03] below):
  > "Recently, Vallée [49] has related `S(2s)` to the quasi-inverse
  > `(I − H_s)^{−1}` of another perturbation `H_s` of the density
  > transformer … `H_s[f] = Σ_{h∈H} |h′|^s·f∘h`, `H_s^{(c)} := Σ_{h∈H}
  > c(h)·|h′|^s·f∘h`."
- Singularity / Tauberian extraction (verbatim):
  > "spectral information on `H_s` may be used to show that `(I − H_s)^{−1}`
  > is analytic in the half-plane `{ℜs>1}`, and analytic on `ℜs=1` except
  > for a simple pole at `s=1`. Under these conditions, one can extract
  > asymptotically the coefficients of `S(s)` by means of Delange's
  > Tauberian theorems."
- Mean-cost statement (verbatim):
  > "the mean value `E_N[C]` of the total cost … satisfies
  > `E_N[C] ∼ μ̂(c)·μ log N`. Here, `μ̂(c)` is the asymptotic mean value
  > (1.3) … and `μ` equals `2/|λ′(1)|`, where `λ(s)` is the dominating
  > eigenvalue of `H_s`."
- CLT (paraphrase — *theorem number not verified verbatim from extracted
  text*; downgraded to PROVEN(literature, statement-level)): BV's Theorem 1
  region states the moment generating function `E_N[exp(wC)]` is a
  quasi-power obtained from a **bivariate** Dirichlet/transfer series
  `S(s,w)` (verbatim: "`E_N[exp(wC)]` is related to the partial sums of the
  coefficients in a bivariate series `S(s,w)`. This series is of Dirichlet
  type with respect to the variable `s`"), yielding asymptotic normality
  with mean `~μ log N`, variance `~δ² log N`, speed `O(1/√n)` (and a Local
  Limit Theorem for lattice costs, optimal speed `O(1/√log N)`). The
  per-digit-`m` constant for the standard algorithm is given verbatim:
  > "`μ̂(c_m) = (1/log 2) log(1 + 1/(m(m+2)))`."

**[V03] B. Vallée, "Dynamical analysis of a class of Euclidean algorithms",
Theoretical Computer Science 297 (2003) 447–486.** (Journal confirmed via
ScienceDirect S0304397502006527, publication 6 Feb 2003.) Role here:
*origin* of the `S(2s) ↔ (I−H_s)^{−1}` size-Dirichlet construction and the
Fast/Slow class; cited *through* the verbatim BV05 attribution above (BV05
[49] = V03). I did **not** obtain V03's own equation-numbered text; any
V03-specific equation number is therefore reported as
PROVEN(literature, via BV05 attribution) only.

**Classical bridge identity** `Σ_k c_k(m)k^{−s} = σ_{1−s}(m)/ζ(s)`:
Ramanujan (1918), "On certain trigonometrical sums…"; standard form in
Hardy & Wright, *An Introduction to the Theory of Numbers*, Thm 272 / §17.
Stated here as PROVEN(classical) and independently re-verified to machine
precision (§4). (Theorem number "272" is the standard H&W numbering; I did
not re-open H&W to re-verify the exact number — flagged.)

**Project prior art (do not reinvent):** Cox–Ghosh–Sultanow arXiv:2105.12352
/ 2407.10214 own the *static* Farey↔Mertens identities; Franel 1924,
Landau 1924, Mikolás 1949 classical. Surviving novel zone = the **per-step
differential + dynamical/cocycle framing**. The static identity
`A_N(m)=Σ_{d|m} d M(⌊N/d⌋)` itself is NOT claimed novel.

---

## 4. The concrete result / rigorous reduction (confidence-labelled)

### Result D4-1 (PROVEN, exact + classical). The per-step Farey/Ramanujan cocycle and its dynamical Dirichlet series.

(a) **Cocycle identity (PROVEN, exact arithmetic, `verify_facts.py`, F4):**
For all `N≥2` and all `m≥1`,
` ΔA_N(m) = A_N(m) − A_{N−1}(m) = c_N(m). `
At prime scale (F2) `c_p(m) = −1 + p·𝟙[p|m]` — the founding lens, made into
an exact per-step cocycle increment.

(b) **Generating identity (PROVEN(classical); re-verified machine precision,
`verify_dirichlet.py`):**
` Σ_{N≥1} ΔA_N(m)·N^{−s} = Σ_{N} c_N(m) N^{−s} = σ_{1−s}(m)/ζ(s). `
Max abs error vs closed form `< 6×10⁻⁷` at `s=1.5` (slow tail), `< 10⁻⁹` at
`s=2`, `< 3×10⁻¹⁵` at `s=3`, for `m∈{1,2,6,12,30}`.

(c) **Spectral placement (PROVEN, from (b) + elementary complex analysis):**
In `ℜs ≥ 1` the series (b) has **no pole at `s=1`** (it has a zero there:
`1/ζ(1)=0`), and its poles are *exactly* the nontrivial zeros `ρ` of `ζ`,
with residue amplitude the *fixed* arithmetic factor `σ_{1−ρ}(m)`. Hence:

> **The Ramanujan/Möbius modulation enters the transfer-operator picture
> ONLY through the subdominant spectrum (zeros of `ζ`), never through the
> dominant eigenvalue `λ(s)` that fixes mean cost.** (Answers Goal 2.)

### Reduction D4-2 (CONJECTURAL link; rigorous *conditional* statement). Dynamical re-derivation of `N·W(N) → C`.

The project core fact (triple cross-verified, `N≤3×10⁵`): `J(N) ~ c·N`,
`N·W(N) → C ≈ 0.66`, **bounded, not `log N`**; conditionally
`C ∝ Σ_ρ 1/(|ρ|²|ζ′(ρ)|²)` (RH + Mertens-variance, Good–Churchhouse /
Ng 2004). Via Parseval/Mikolás `J(N) = (1/2π²)Σ_m A_N(m)²/m² + O(1)`.

**Rigorous reduction (PROVEN conditional skeleton):** Substituting D4-1(a),
`A_N(m) = Σ_{k≤N} c_k(m)`, and the dynamical Dirichlet representation
D4-1(b) into Parseval, the second moment `J(N)` is governed by the
*coefficient-sum of the square* of a `1/ζ(s)`-type Dirichlet series — i.e.
the **Mertens variance** object — with the `m`-sum supplying the convergent
weight `Σ_m σ_{1−ρ}(m)σ_{1−ρ'}(m)/m²`. This is the *fluctuation* (variance)
régime of the Vallée dictionary, NOT the mean. **Statement of the
transfer-operator fact that would close it:** a *Dolgopyat-type vertical
contraction* estimate for the **Ramanujan-twisted** quasi-inverse
`(I − H_{s})^{−1}` paired against the `1/ζ(s)` factor on `ℜs=1`, uniform in
the twist `m`, would give `J(N)=cN+o(N)` unconditionally. **Tractability
(HONEST):** this is exactly as hard as an unconditional Mertens-variance /
`Σ_ρ` evaluation — i.e. it is **conditionally** (RH-type) tractable and
unconditionally open; the dynamical packaging does **not** lower the bar
(the `1/ζ` factor is unavoidable and carries the full difficulty). This is a
**clean negative on tractability**, not a breakthrough.

### Correctness check (PROVEN(literature) reproduction).

Setting the modulation off (`m`-independent, positive constant digit-cost
`c≡1`) the dictionary reduces to BV05's verbatim `E_N[#steps] ~ μ log N`,
`μ=2/|λ′(1)|` — the classical Heilbronn–Dixon / Vallée mean. Our framework
*reproduces* this in the limit where the Ramanujan twist is removed
(`σ_{1−s}(m)→1`, pole of `(I−H_s)^{−1}` at `s=1` restored). So the dictionary
is calibrated correctly against a known cost asymptotic. ✓

---

## 5. Numerical verification (scripts in this directory)

- `verify_facts.py` — exact integer/Fraction arithmetic. F1,F2,F3,F4 all
  pass with **zero** deviation; `A_N(m)` real to `~10⁻¹²`. (Also fixed a
  prime-sieve bug in an earlier draft — `μ(n)=−1` ≠ prime; e.g. `105=3·5·7`.)
- `verify_dirichlet.py` — `Σ_k c_k(m)/k^s = σ_{1−s}(m)/ζ(s)` re-verified to
  machine precision; demonstrates `1/ζ(1+ε)→0` (zero, not pole) and the
  zero-of-`ζ` ⇒ pole-of-series placement.

Both runnable: `python3 verify_facts.py`, `python3 verify_dirichlet.py`
(needs `mpmath` for the latter). Outputs reproduced in §4(b)/§1.2.

---

## 6. Honest practical-ceiling assessment

**What is genuinely new (NUMERICAL/HEURISTIC→PROVEN-skeleton):** the explicit
**Ramanujan-twisted dynamical Dirichlet series** `σ_{1−s}(m)/ζ(s)` as the
generating object of the *per-step* Farey increment, and its exact pole
dictionary placing the modulation in the **subdominant** transfer-operator
spectrum. This per-step + dynamical framing is outside Cox–Ghosh–Sultanow
(static identities) and outside the Vallée program (which weights *positive*
Birkhoff costs, never a signed Ramanujan-sum coefficient). It is a correct,
small, novel structural statement.

**What FAILED / the ceiling (clean negative):**
1. The lens does **NOT** yield a new *average-case* (mean-cost) theorem for
   Euclid / Gauss reduction / LLT. The Ramanujan modulation is pole-free in
   `m` and vanishes at `s=1`; it cannot perturb `λ(s)` or `μ=2/|λ′(1)|`.
   Mean-cost is immune to the arithmetic twist. (PROVEN, §4(c).)
2. The lens lands in the **variance/fluctuation** régime — which is *exactly*
   the Mertens-variance / `Σ_ρ 1/(|ρ|²|ζ′(ρ)|²)` object the project already
   owns from the *static* side. The dynamical packaging is a re-derivation,
   not new leverage: the unavoidable `1/ζ(s)` factor carries the entire
   difficulty, so no unconditional improvement is bought. (PROVEN-skeleton,
   §4 D4-2.)
3. Therefore: **no credible path, via this lens, to
   arithmetic-structure-weighted *average-case* bounds for LLL /
   Gauss-reduction.** LLL/Gauss-reduction average-case analysis (Daudé–Vallée,
   Akhavi) sits on the *dominant* eigenvalue; our modulation provably misses
   it. No inflation: this is a NO for the headline application.

**Where the small positive value is real:** the variance-side dictionary
gives a *dynamical-systems vocabulary* for the project's `N·W(N)→C` fact and
a precisely-stated (if hard) conditional reduction (D4-2). Worth one section
of a methods paper; not a theorem-generating engine.

---

## 7. Highest-value next step — EXECUTED, with result

This step was **run**, not just proposed (`probe_dominant_eigenvalue.py`).

**Result D4-3 (NUMERICAL, decisive; calibrated against PROVEN BV05).**
Dominant eigenvalue `λ_A(1)` of the Vallée transfer operator
`H_s f = Σ_{m∈A}(1/(m+x))^{2s} f(1/(m+x))` (Nyström collocation, 120 nodes):

| alphabet `A` | `λ_A(1)` | note |
|---|---|---|
| all `m≥1` (full Gauss) | **0.99993** | calibration ✓ (BV05 PROVEN `λ(1)=1`) |
| `gcd(m,2)=1` | 0.64638 | dominant eigenvalue MOVED |
| `gcd(m,3)=1` | 0.81853 | |
| `gcd(m,4)=1` | 0.64638 | `=λ_2` ✓ (same alphabet) — internal check |
| `gcd(m,6)=1` | 0.51291 | |

**Interpretation (sharpens the §6 verdict, both directions now precise):**
The founding lens's "prime inserts genuinely *new* digits" is, dynamically,
a **digit-alphabet *restriction***, not a Ramanujan *reweighting*. A
*reweighting* by `c_k(m)` provably leaves `λ(1)=1` untouched
(subdominant-only, §4(c), PROVEN). A *coprimality restriction* of the digit
alphabet **does** move the dominant eigenvalue substantially and
consistently (`λ_2=λ_4` because `{gcd(m,2)=1}={gcd(m,4)=1}` as digit sets).

> **Net (HONEST, refined):** the *Ramanujan-weighted* form of the lens is
> subdominant (no new mean-cost theorem — clean negative, §6). But the
> *coprimality-restricted* form is a **genuine dominant-eigenvalue
> perturbation**: a Euclid/Gauss-type algorithm whose CF digits are
> constrained to a coprimality class has a *different, computable* mean-cost
> constant `μ_q = 2/|λ_q′(1)|`. That is the live, non-inflated opening — and
> it is now isolated, calibrated, and numerically demonstrated, not merely
> conjectured.

**Therefore the single highest-value next step (now well-posed):** turn
D4-3 into a theorem. State and prove (the standard Vallée/Dolgopyat machinery
applies *verbatim* once the restricted alphabet keeps the spectral gap — a
finite-index sub-system, so it does): for the coprimality-restricted Euclid
variant, `E_N[#steps] ∼ μ_q log N` with `μ_q = 2/|λ_q′(1)|`, `λ_q` the
dominant eigenvalue of `H_s^{(q)}`, and compute `μ_q` for small `q`. This
would be a *new arithmetic-structure-weighted average-case theorem* for a
Euclidean algorithm — the deliverable's headline target, reached via the
restriction (not the reweight) reading of the lens. Effort: ~1 week
(gap-stability lemma for the finite-index subsystem + Tauberian transcription
of BV05 §3; numerics already in hand).

> **[2026-05-15 D4 follow-up — EXECUTED. See `MU_Q_THEOREM_2026-05-15.md`.]**
> Theorem μ_q delivered: `E_N[#steps] ∼ μ_q log N`, PROVEN(reduced — one
> named, satisfied input). **TWO CORRECTIONS to this §7:**
> (1) *"finite-index sub-system"* is **WRONG** — `A_q={gcd(m,q)=1}` deletes
> *infinitely many* digits; it is an **infinite conformal IFS**. Gap still
> holds, via Mauldin–Urbański / Vallée GMG-heredity (deliverable §2), not
> finite-rank perturbation.
> (2) **`μ_q=2/|λ_q′(1)|` is REFUTED by the dual numerics.** BV05's
> `2/|λ′(1)|` assumes `λ(1)=1`; here `λ_q(1)<1`, so the Dirichlet pole moves
> to `s_q` (`λ_q(s_q)=1`, `s_q<1`) and the correct constant is
> **`μ_q = 2/(s_q·|λ_q′(s_q)|)`**. Calibration `q=1`: corrected formula,
> simulation, and classical `12ln2/π²` all agree to **0.2%**; the
> un-corrected `2/|λ_q′(1)|` is 42–293% off for `q=2,3,6`. The "machinery
> applies *verbatim*" claim is false — transcription is *forced-modified*
> at the pole. Citations locked verbatim: BV05 Theorem 3(b)(c) + Lemma 12
> eq.(4.12) (resolves prior could-not-verify flag).

---

### (superseded) original framing of the next step

**Test the only place the twist could still bite the *dominant* spectrum:**
replace the *global* denominator filtration by a **digit-restricted induced
operator** (Farey-map jump transformation restricted to CF digits in an
arithmetic progression / coprimality class), and ask whether a *coprimality*
constraint — not a Ramanujan *weight* — perturbs `λ(s)`. Concretely: compute
the dominant eigenvalue of the **coprimality-restricted transfer operator**
`H_s^{(q)}f = Σ_{gcd(m,q)=1} |h_{[m]}'|^s f∘h_{[m]}` for small `q` and compare
`λ_q(1)` to `λ(1)=1`. If `λ_q(1) ≠ 1` while the Ramanujan-weighted operator
leaves it fixed, that *isolates exactly* what the founding lens does
dynamically (it restricts the digit alphabet, it does not reweight it) — and
would be the first place a genuinely new arithmetic-weighted *mean*-cost
statement could appear. This is a 1–2 day, fully computational,
exact-spectrum probe (truncated `H_s^{(q)}` matrix, dominant eigenvalue);
high information-per-token, decisive either way.
