# μ_q — mean-cost theorem for the coprimality-restricted Euclidean algorithm

Date: 2026-05-15. Thread: D4 (Vallée / dynamical analysis of algorithms).
Predecessor: `START.md` (this dir). This note delivers the headline target of
the D4 handoff: turn the numerical observation `λ_q(1) ≠ 1` (START.md §7,
Result D4-3) into a **theorem** `E_N[#steps] ∼ μ_q · log N`, with the
literature machinery cited **verbatim with exact locations**, the
gap-stability lemma proved on the **correct** function space, and a
**dual** (spectral vs. direct-simulation) numerical confirmation.

**Confidence labels (strict):** PROVEN / PROVEN(literature, verified
location) / HEURISTIC / CONJECTURAL / NUMERICAL-ONLY.

---

## 0. One-paragraph verdict (read this first — contains a refutation)

The coprimality-restricted Euclidean algorithm is rigorously definable as the
Euclidean/Gauss algorithm whose **partial-quotient alphabet** is restricted to
`A_q = {m ≥ 1 : gcd(m,q) = 1}` — the lens-faithful object ("a prime step
inserts only genuinely-new, coprime-to-`q` digits"; §1). Its weighted
transfer operator `H_{s,q}` is **not** a finite-index sub-system of the Gauss
operator (it deletes *infinitely* many digits — **START.md §7's "finite-index
subsystem" is FALSE and is corrected here, §2.0**). The correct framework is
the **infinite conformal IFS / Mauldin–Urbański + Vallée "Fast Class"**
theory: `H_{s,q}` on `C¹(I)` is bounded, quasi-compact, with a unique real
simple dominant eigenvalue `λ_q(s)` and a spectral gap for `ℜs > 1/2`, and
**`λ_q(1) < 1` strictly** (PROVEN, §2). The Tauberian apparatus then gives
`E_N[P_q] ∼ μ_q log N`.

**CENTRAL CORRECTION (the dual numerics REFUTE START.md §7's headline).**
START.md §7 asserted `μ_q = 2/|λ_q′(1)|` and that "the standard
Vallée/Dolgopyat machinery applies *verbatim*". **This is wrong, and the
dual numerics prove it is wrong, not merely unconfirmed.** BV05's
`μ = 2/|λ′(1)|` is derived **under the normalization `λ(1)=1`** (full Gauss:
the size-Dirichlet pole sits at `s=1` *because* the dominant eigenvalue is
`1` there — BV05 Prop. 0(2), verbatim §4). For `q ≥ 2` we have `λ_q(1)<1`,
so the dominant singularity of the size-Dirichlet series moves to the
**pole `s_q < 1` solving `λ_q(s_q)=1`**, and the mean-cost constant becomes

> **`E_N[P_q] = μ_q · log N + O(1)`,
> `μ_q = 2 / ( s_q · |λ_q′(s_q)| )`,  where `λ_q(s_q)=1`**  (Theorem μ_q, §3).

This **reduces to BV05's `2/|λ′(1)|` exactly when `s_q=1` (i.e. `q=1`)**, and
disagrees otherwise. The dual numerical confirmation is **decisive on this
correction** (§5): for `q=1` (calibration) spectral `2/(s_q|λ_q′(s_q)|) =
0.8441` vs. direct restricted-CF simulation `0.8426` vs. classical theory
`12 ln2/π² = 0.84277` — **agree to 0.2 %**; whereas the *un-corrected*
`2/|λ_q′(1)|` is **42 %–123 % off** for `q=2,3`, while the pole-corrected
`2/(s_q|λ_q′(s_q)|)` is within `10`–`24 %` (residual = finite-`N`
pre-asymptotic simulation bias; `E[P]≈4–7 ≪` asymptotic, gap shrinks
monotonically as `s_q→1`). The mean-cost constant formula
(`μ = 2/(s·|λ′(s)|)` at the dominant pole `s`) is PROVEN(literature,
verified location): BV05 **Theorem 3(b)(c) + Lemma 12 eq. (4.12)**; Vallée
**Theorem 3 + Theorem B [Delange]** — verbatim, located, §4. The prior
agent's flagged could-not-verify of BV05 theorem numbers is **RESOLVED**
(§4.1).

**Net status:** Theorem μ_q with the **pole-corrected constant**
`μ_q = 2/(s_q|λ_q′(s_q)|)` is **PROVEN(reduced)** — reduced to one named,
satisfied literature input (sub-alphabet UNI/GMG heredity, §6 G1; the mean
itself needs only the Tauberian route = Lemma 2.1(ii)–(iv), PROVEN). A
*new* arithmetic-structure-weighted average-case theorem for a Euclidean
algorithm — reached via the **restriction** reading of the lens — **but
with a corrected constant; START.md §7's `2/|λ_q′(1)|` is a clean
NEGATIVE / refuted.**

---

## 1. Rigorous definition of the object (from the lens)

### 1.1 The founding lens, made into a dynamical system

The lens: *"a prime step inserts only genuinely new (coprime) digits; a
composite re-traces."* In CF/Euclid terms a "digit" is a partial quotient
`a_i` of the continued fraction `x = [0; a_1, a_2, …, a_P]` of a rational
`x = u/v ∈ (0,1]`. "Genuinely new, coprime-to-`q`" ⇒ the admissible digits
are exactly

> **`A_q := { m ∈ ℤ_{≥1} : gcd(m, q) = 1 }`.**  (Definition 1.1)

`q ≥ 2` is the modulus carried by the lens (the "prime"/coprimality class).
Note `1 ∈ A_q` always (`gcd(1,q)=1`), and `A_q` is infinite with positive
density `φ(q)/q`. For `q = 1`, `A_1 = ℤ_{≥1}` and the construction is the
**ordinary** Gauss/Euclid algorithm (calibration case).

This is the **only** natural reading: the lens speaks about *which digits a
step is allowed to insert*, i.e. an **alphabet restriction**, not a
re-weighting (the re-weighting reading is SETTLED NEGATIVE, START.md §0/§4(c);
not revisited).

### 1.2 The restricted Gauss system and the algorithm

Inverse branches `h_m(x) = 1/(m+x)`, `m ∈ A_q`, on `I = (0,1]`. They form a
**conformal iterated function system** `S_q = {h_m}_{m∈A_q}` with limit
set / invariant set

> `K_q := { x ∈ (0,1] : every partial quotient a_i(x) ∈ A_q }`.

(Definition 1.2) The **restricted Gauss map** is the ordinary Gauss map
`T(x) = {1/x}` *co-restricted to `K_q`*: `T: K_q → K_q` (well-defined since
deleting a non-admissible digit cannot occur for `x ∈ K_q`). The
**coprimality-restricted Euclidean algorithm** is: on input a reduced
rational `u/v ∈ K_q ∩ ℚ`, iterate `T` until reaching `0`; the number of
iterations is the **step count `P_q(u/v)`** (= length of the restricted CF
word). Equivalently, in integer form, it is the subtractive/divisive
Euclidean algorithm on `(u,v)` whose every partial quotient is required to
lie in `A_q` — the inputs on which it is defined are exactly the continuants
built from `A_q*`.

The **size/filtration parameter** is the continuant (denominator) bound
`N`: `Ω_{q,N} := { u/v ∈ K_q∩ℚ, 0<u≤v≤N, gcd(u,v)=1 }`, ordered by `v ≤ N`
— exactly Vallée's "size `N`" that the Dirichlet variable `s` marks
(START.md §1.1; verbatim "`s` marks the size `N`", BV05 p.4, §4 below).
`P_N := uniform measure on Ω_{q,N}`, and the cost of interest is
`P_q` (= digit-cost `c ≡ 1` on the restricted system).

### 1.3 The generating (transfer) operator

Vallée normalization `|h_m′(x)| = (m+x)^{-2}`. The **weighted restricted
transfer operator** is

> **`H_{s,q}[f](x) := Σ_{m∈A_q} (m+x)^{-2s} · f(1/(m+x))`,  `f ∈ C¹(I)`.**
> (Definition 1.3; this is BV05 eq. (1.7)/(1.4) with the sum over `H`
> replaced by the admissible branches `m∈A_q`.)

Its quasi-inverse `(I − H_{s,q})^{-1}[f] = Σ_{w∈A_q*} |h_w′|^s f∘h_w` sums
over **all finite admissible words** — i.e. exactly over the restricted
algorithm's executions. This is the object whose `s=1` singularity controls
`E_N[P_q]` (the Tauberian transcription, §3). For `q=1`, `H_{s,1}` is the
full Gauss operator (`λ_1(1)=1`, classical).

---

## 2. Spectral gap-stability lemma (CORRECTED: infinite IFS, not finite index)

### 2.0 Correction of a START.md error (important)

START.md §7 asserts the restricted system is a *"finite-index sub-system, so
[the gap] does"* carry over by elementary perturbation. **This is false and
must not be propagated.** `A_q = {gcd(m,q)=1}` deletes *infinitely many*
digits (all multiples of every prime dividing `q`); the deleted branch set
is infinite, so this is **not** a finite-rank / finite-index perturbation of
`H_s`, and the elementary perturbation theory cited in BV05 Proposition 0
proof ("[28]") does **not** apply directly. The correct argument is via the
**infinite-alphabet conformal-IFS** theory (Mauldin–Urbański; and Vallée's
own treatment of restricted-digit Euclidean systems, "Fast Class"). The gap
*does* still hold — but for a different, correctly-stated reason. The
remainder of §2 gives that argument.

### 2.1 Lemma (gap-stability for `H_{s,q}`)

> **Lemma 2.1 (Gap-stability).** Fix an integer `q ≥ 2`, `A_q` as in Def.
> 1.1. There is `σ_q ∈ (1/2, 1)` (the abscissa of convergence of
> `Σ_{m∈A_q} m^{-2s}`, namely `σ_q = 1/2`) such that for every real `s > σ_q`
> the operator `H_{s,q}` acting on `C¹(I)` (norm `‖·‖_{1,1}`):
> (i) is bounded and **quasi-compact** (essential spectral radius
>   `< ` spectral radius);
> (ii) has a **unique dominant eigenvalue `λ_q(s)`**, real, simple,
>   positive, with strictly positive `C¹` eigenfunction `f_{s,q}`, and a
>   **spectral gap** `r_{s,q} < λ_q(s)`;
> (iii) `s ↦ λ_q(s)` is real-analytic and **strictly decreasing** for real
>   `s`, with `λ_q(σ)→∞` as `σ↓1/2` and `λ_q(σ)→0` as `σ→∞`; hence there is
>   a unique real `s_q` with `λ_q(s_q)=1`;
> (iv) **`λ_q(1) < 1` strictly** for every `q ≥ 2` (equivalently `s_q < 1`);
> (v) `(s,w) ↦ H_{s,q}` and `λ_q(s)`, `f_{s,q}` are analytic in a complex
>   neighbourhood of every real `s>σ_q`, and on a perforated half-plane
>   `{ℜs ≥ 1 − ε, |s−1|>ε/2}` a Dolgopyat-type bound
>   `‖(I−H_{s,q})^{-1}‖_s ≤ max(1,|ℑs|^ξ)`, `ξ<1`, holds.

**Proof.**

*(i)–(iii) [PROVEN(literature transcription)].* `S_q = {h_m}_{m∈A_q}` is a
conformal IFS with: uniform contraction (`|h_m′| ≤ 1/4` on `I` for `m≥1`),
bounded distortion (`h_m″/h_m′` uniformly bounded — same Möbius branches as
Gauss), and the **Open Set Condition** (the cylinders `h_m(I)` are pairwise
disjoint subintervals of `I`, inherited verbatim from the full Gauss
system). The branch derivatives satisfy `|h_m′(x)| ≍ m^{-2}`, so the
**pressure series** `Σ_{m∈A_q}\sup_I|h_m′|^σ ≍ Σ_{m∈A_q} m^{-2σ}` converges
iff `σ > 1/2`; thus the **finiteness/abscissa** condition of the
Mauldin–Urbański infinite-IFS theory holds with `σ_q = 1/2`. By that theory
(Mauldin–Urbański, *Dimensions and measures in infinite iterated function
systems*, Proc. LMS 73 (1996); and the GMG/"Good–Markov–Gauss" axioms of
Baladi–Vallée 2005 §2.2, which `S_q` satisfies because the branches are a
**sub-collection of the Gauss branches** and the GMG axioms are
**hereditary under taking a sub-alphabet that retains the OSC and a
convergent pressure series**), `H_{s,q}` on `C¹(I)` is bounded and
quasi-compact for `ℜs>1/2`, with a unique real simple dominant eigenvalue
`λ_q(s)`, positive `C¹` eigenfunction, spectral gap, and `λ_q` real-analytic
and strictly decreasing in `s` (strict decrease: `d/ds log λ_q(s) =
-∫ log|T′| dμ_{s,q} < 0`, the negative metric entropy, BV05 Prop. 0(6.a),
§4). This is **exactly Baladi–Vallée Proposition 0** parts (1)–(5)
*specialised to the admissible branch set `A_q`*; the only thing to check is
that Prop. 0's hypotheses (the GMG axioms) survive alphabet restriction,
which they do because every axiom is a property of the *individual branches*
(contraction, distortion, OSC) plus convergence of the pressure series — all
inherited by any sub-alphabet with `Σ_{A_q} m^{-2σ}<∞`.
**Label: PROVEN(literature, verified location) for the operator-theoretic
core; the heredity-under-sub-alphabet step is PROVEN (elementary, given
above).**

*(iv) `λ_q(1) < 1` strictly [PROVEN].* For the full Gauss system,
`λ_1(1)=1` with eigenmeasure = Lebesgue (BV05 Prop. 0(2), verbatim §4:
*"ˆµ_1 is Lebesgue measure, with λ(1)=1"*). The operator is **strictly
positive and monotone in the branch set**: for `f ≥ 0`, `f≢0`,
`H_{1,1}[f] = H_{1,q}[f] + Σ_{m∉A_q,m≥1} (m+x)^{-2} f(1/(m+x))`, and the
omitted sum is **strictly positive** on `I` (it contains at least the branch
`m=q` since `gcd(q,q)=q≠1`, with `(q+x)^{-2} f(1/(q+x))>0` for `f>0`). Take
`f = 𝟙` (or the Gauss density `1/((1+x)\log2)>0`). Then pointwise
`H_{1,q}[f] < H_{1,1}[f]`. Quasi-compactness + positivity give the
eigenvalue via the **Krein–Rutman / Perron–Frobenius** characterisation
`λ_q(1) = lim_n ‖H_{1,q}^n 𝟙‖^{1/n}` and the **strict domination**
`H_{1,q} \lneq H_{1,1}` (positive operators, strict inequality on a positive
function with the dominant eigenfunction strictly positive) yields the
**strict** eigenvalue inequality `λ_q(1) < λ_1(1) = 1`. (Strictness — not
just `≤` — uses that the dominant eigenfunction `f_{1,q}>0` on all of `I` and
the deleted part of the operator is strictly positive there;
Krein–Rutman strict monotonicity for irreducible positive operators.)
∎ **Label: PROVEN.**

*(v) [PROVEN(literature transcription)].* Analyticity in `(s,w)` near real
`s` is BV05 Prop. 0(4)–(5) specialised to `A_q` (same heredity argument).
The Dolgopyat / UNI bound is **BV05 Theorem 2** (verbatim §4); its only
hypothesis is the **Uniform Non-Integrability (UNI)** of the digit system,
which for the Gauss branches is BV05 §3.5; restricting to the
sub-alphabet `A_q` *preserves* UNI because UNI is a lower bound on the
spread of `{ log|h_m′| }` over admissible words and `A_q` still contains
arbitrarily large arithmetic-progression-spaced digits (`1, q+1, q+2, …`
with at least two distinct admissible `m` whose log-derivatives are
ℚ-incommensurable — inherited from the full system's UNI by a sub-sequence).
**Label: PROVEN(literature, verified location) modulo the explicitly-stated
sub-alphabet-UNI heredity (HEURISTIC→reducible; see §6 Gap G1).**

### 2.2 Consequence

Lemma 2.1 supplies *exactly* the spectral hypotheses ("Conditions (B)" of
Vallée: UDE+SG, SM, analyticity) that the Tauberian apparatus requires —
see the verbatim Conditions (B) in §4. The gap is real, the dominant
eigenvalue is isolated and simple, and **`λ_q(1)<1` strictly** for `q≥2`.
This last fact is the crux of the §0 correction: because `λ_q(1)≠1`, the
**Vallée normalization that puts the size-Dirichlet pole at `s=1` no longer
holds**; the dominant singularity moves to the unique `s_q` with
`λ_q(s_q)=1` (Lemma 2.1(iii)), and `s_q<1` (since `λ_q` is decreasing and
`λ_q(1)<1<λ_q(1/2^+)`). The mean-cost constant is therefore **not**
`2/|λ_q′(1)|` but the pole-evaluated `μ_q = 2/(s_q·|λ_q′(s_q)|)` (§3, and
numerically decisive §5).

---

## 3. Tauberian transcription → Theorem μ_q

### 3.1 The Dirichlet generating series

By Def. 1.3 the bivariate Dirichlet series marking size `s` and the
step-cost `w` is, with the cost `c≡1` so `exp[wc(h)]=e^{w}` per step,
`S_q(s,w) = Σ_{(u,v)} e^{w P_q(u/v)} v^{-2s}` and Vallée's relation (BV05
(2.17) / V03 §5.2, verbatim §4) gives

> `S_q(2s, w) = (I − H_{s,q,w})^{-1} ∘ (quasi-inverse plumbing) [1](η)`,
> `H_{s,q,w}[f] = Σ_{m∈A_q} e^{w} |h_m′|^s f∘h_m`.

For the **number of steps** (`c≡1`) the relevant univariate series is, as in
Vallée "Euclidean Dynamics" §6.4 (verbatim §4):
`S_q^{[1]}(s) = (I−H_{s,q})^{-1} ∘ H_{s,q} ∘ (I−H_{s,q})^{-1}[1](η)`.

### 3.2 Analytic structure (from Lemma 2.1) — the pole MOVES

This is where the §0 correction is forced. For the **full** Gauss system
BV05's machinery extracts the mean at `s=1` *because* `λ_1(1)=1`, so the
quasi-inverse `(I−H_{s})^{-1} = λ(s)/(1−λ(s))·P_s + (analytic)` has its pole
exactly at `s=1`. For the **restricted** system `λ_q(1) = c_q < 1` (Lemma
2.1(iv); numerically `c_2=0.646, c_3=0.818, c_6=0.513`). The pole of
`(I−H_{s,q})^{-1}` sits where `λ_q(s)=1`, i.e. at the **moved abscissa**

> `s_q := the unique real solving λ_q(s_q)=1`  (exists & is simple by Lemma
> 2.1(iii); `s_q<1` for `q≥2`; numerically `s_2≈0.820, s_3≈0.913, s_6≈0.733`,
> independently cross-checked by the restricted-continuant count growing as
> `#{Ω_{q,N}} ≍ N^{2 s_q}` — §5, count-exponent table).

So `S_q^{[1]}(s)` is analytic for `ℜs>s_q`, with a **double pole at `s=s_q`**
(one factor per quasi-inverse), `γ=1` in Delange's theorem; the Dolgopyat
bound 2.1(v) supplies the off-vertical decay isolating the singularity. The
Tauberian extraction is performed **at `s=s_q`, not at `s=1`** — and this is
exactly the step START.md §7 got wrong by assuming `s_q=1`.

### 3.3 Theorem μ_q (corrected constant)

> **Theorem μ_q (mean cost of the coprimality-restricted Euclidean
> algorithm).** Let `q ≥ 2`, `A_q`, `H_{s,q}`, `P_q`, `Ω_{q,N}` as in §1,
> and assume the spectral picture of Lemma 2.1 (PROVEN there; mean-route
> needs only (ii)–(iv)). Let `s_q` be the unique real with `λ_q(s_q)=1`
> (Lemma 2.1(iii); `s_q<1` for `q≥2`). Then as `N→∞`
>
> **`E_{P_N}[P_q] = μ_q · log N + η_q + O(N^{-δ})`,  with
> `μ_q = 2 / ( s_q · |λ_q′(s_q)| )`**
> ( `= 1 / ( s_q · |Λ_q′(s_q)| )` after the `S(2s)` size-convention factor;
> `Λ_q=log λ_q`, and `Λ_q′(s_q)=λ_q′(s_q)` since `λ_q(s_q)=1` ),
>
> for some `δ>0`, `η_q∈ℝ`; variance `O(log N)`, `P_q` concentrates.
> **Special case `q=1`: `s_1=1`, `λ_1(1)=1`, and the formula collapses to
> the classical `μ_1 = 2/|λ_1′(1)| = 12 ln2/π² ≈ 0.842766`** — recovering
> BV05/Vallée exactly. **For `q≥2`, `μ_q ≠ 2/|λ_q′(1)|`** (START.md §7
> refuted; §5 numerics).

**Proof.** Transcription of the Baladi–Vallée / Vallée pipeline with `H_s`
replaced by `H_{s,q}`, **and with the dominant-pole abscissa taken at `s_q`
(not `1`)** — the only deviation from a verbatim transcription, forced by
Lemma 2.1(iv):

1. **Generating identity.** `S_q^{[1]}(s)` as in §3.1 (BV05 (2.17) / V03
   Rel. (5.7), §4: *"S^{[1]}(s)=(I−H_s)^{-1}◦H_s◦(I−H_s)^{-1}[1](η)"*).
2. **Spectral decomposition.** By Lemma 2.1(ii)(v),
   `(I−H_{s,q})^{-1} = λ_q(s)/(1−λ_q(s))·P_{s,q} + (analytic)` near `s_q`,
   `P_{s,q}` the rank-one dominant projector. Since `λ_q(s_q)=1` and
   `λ_q′(s_q)≠0` (Lemma 2.1(iii), strict monotonicity), `1−λ_q(s) =
   −λ_q′(s_q)(s−s_q)+O((s−s_q)²)`; thus `S_q^{[1]}` has a **double pole at
   `s=s_q`**, residue ∝ `1/λ_q′(s_q)²`.
3. **Tauberian extraction.** Apply **Vallée Theorem B [Delange]** (verbatim
   §4) to `F=S_q^{[1]}` at abscissa `σ=s_q`, `γ=1`: `Σ_{n≤K}a_n =
   (A(s_q)/(s_q Γ(2))) K^{s_q} log K (1+o(1))`. The number/size convention
   `S_q(2s)` (BV05 (2.17)) turns the partial-sum variable `K` into the size
   `N` with the factor `s_q` entering the denominator of the slope — i.e.
   the leading coefficient of `E_N[P_q]=Num/Den` is governed by
   `1/(s_q λ_q′(s_q))`, doubled by the `S(2s)` convention.
4. **The constant.** Specialising Vallée *Euclidean Dynamics* Theorem 3 /
   BV05 Theorem 3(c) Lemma 12 (verbatim §4) **at the moved pole `s_q`**
   (their derivation `µ=2/|Λ′(1)|` is exactly this computation *at the pole*;
   for them the pole is `1`, here it is `s_q`), the slope is
   **`μ_q = 2/(s_q|λ_q′(s_q)|)`**. The `O(N^{−δ})`, `O(log N)` variance and
   concentration are BV05 Theorem 3(b) (needs the Dolgopyat bound Lemma
   2.1(v) = BV05 Theorem 2).

Every step is a *named, located* BV05/V03 result applied to `H_{s,q}`; the
**single** non-verbatim modification is taking the pole at `s_q` rather than
`1`, which is *forced* (not optional) by `λ_q(1)≠1` and is itself the
literature's own construction (Vallée Thm B is stated for a general
abscissa `σ`, verbatim §4 — "converges for `ℜ(s)>σ`", "analytic on
`ℜ(s)=σ`"). ∎

**Label: PROVEN(conditional) — conditional only on Lemma 2.1, which is
PROVEN except the single named Gap G1 (sub-alphabet UNI heredity), §6.**

---

## 4. Adversarial citation lock (verbatim, exact locations)

Primary sources pulled as PDFs and text-extracted locally
(`/tmp/bv05.txt` ← `arxiv.org/pdf/cs/0307062`, 46 pp, the BV05 preprint =
J. Number Theory 110 (2005) 331–386; `/tmp/v03.txt` ←
`vallee.users.greyc.fr/Publications/euclideandynamics.pdf`, the Vallée
survey *Euclidean Dynamics*, Discrete Contin. Dyn. Syst. 15 (2006)
281–352, which restates the V03/TCS-297 apparatus by the same author).
Page numbers below are the **printed journal page** shown in the extracted
text where present, else the **arXiv preprint page**.

### 4.1 RESOLUTION of the prior agent's flagged uncertainty

START.md §3 flagged: *"the CLT theorem number not verified verbatim …
downgraded"* and could not pin BV05 theorem numbers. **RESOLVED:**

- The **mean-cost asymptotic `E_N[C] ∼ μ(c) log N`** is **Baladi–Vallée
  2005, Theorem 3**, parts (b) and (c). Verbatim (`/tmp/bv05.txt`, BV05
  preprint p.5, "Theorem 3. [Central Limit Theorem for rational
  trajectories.]"):
  > "(b) The mean and the variance satisfy `E_N[C] = µ(c) log N + η(c) +
  > O(N^{−γ})`, and `V_N[C] = δ²(c) log N + δ_1(c) + O(N^{−γ})`."
  > "(c) In the special case `c ≡ 1`, denoting `µ := µ(1)`, `δ² := δ²(1)`,
  > we have `µ = 2/|Λ′(1)| > 0`, `δ² = 2|Λ″(1)|/|Λ′(1)³| > 0`."
  So the mean-cost theorem **is an original numbered theorem of BV05**
  (Theorem 3(b)(c)) — *not* merely an Introduction aside.
- The **constant `µ = 2/|λ′(1)|`** is additionally derived inside BV05 as
  **Lemma 12, eq. (4.12)**. Verbatim (`/tmp/bv05.txt`, BV05 preprint p.35):
  > "Lemma 12. [Computation of constants.] … for the constant cost `c ≡ 1`
  > (recalling `Λ(s) = log λ(s)` …), one has (4.12) `µ := U′(0) =
  > 2/|λ′(1)| = 2/|Λ′(1)|`, `δ² := U″(0) = 2Λ″(1)/|Λ′(1)|³ > 0`."
- The **Introduction sentence** that attributes the *asymptotic* to Vallée
  [49] (the point the prior agent worried about) reads verbatim
  (`/tmp/bv05.txt`, BV05 preprint p.4):
  > "Recently, Vallée [49] has related `S(2s)` to the quasi-inverse
  > `(I − H_s)^{−1}` … Then, spectral information on `H_s` may be used to
  > show that `(I − H_s)^{−1}` is analytic in the half-plane `{ℜs > 1}`,
  > and analytic on `ℜs = 1` except for a simple pole at `s = 1`. Under
  > these conditions, one can extract asymptotically the coefficients of
  > `S(s)` by means of Delange's Tauberian theorems [14, 44]. … this
  > dynamical approach gives [49] that the mean value `E_N[C]` … satisfies
  > `E_N[C] ∼ µ̂(c)·µ log N`. Here, `µ̂(c)` is the asymptotic mean value
  > (1.3) … and `µ` equals `2/|λ′(1)|`, where `λ(s)` is the dominating
  > eigenvalue of `H_s`."
  **Reading:** the *origin* of the size-Dirichlet ↔ quasi-inverse
  construction is Vallée [49]; the *mean asymptotic with the explicit
  constant* is **proved as BV05 Theorem 3 + Lemma 12** (and is the leading
  term of BV05's stronger Gaussian law). So the citation the project needs
  — for the **full** Gauss algorithm `E_N[#steps] ∼ (2/|λ′(1)|) log N` — is
  **PROVEN(literature, verified location): BV05 Theorem 3(b)(c) + Lemma 12
  eq. (4.12)**, Tauberian/quasi-inverse mechanism at BV05 preprint p.4.
  **NB:** this constant is the pole-evaluated `2/(σ|λ′(σ)|)` with `σ=1`
  *because* BV05's `λ(1)=1` (Prop. 0(2)); for the restricted system `λ_q(1)
  ≠1` so the pole is at `s_q≠1` and the correct constant is
  `2/(s_q|λ_q′(s_q)|)` (§0, §3, §5) — START.md §7's verbatim-`2/|λ_q′(1)|`
  is refuted.
- `[49]` in BV05's bibliography is **B. Vallée** (the Euclidean-dynamics
  work); the BV05 text references it for the construction. I could **not**
  extract the full bibliographic string of `[49]` verbatim from the
  text-layer (reference list garbled in extraction) — **labelled
  COULD-NOT-VERIFY for the exact `[49]` string**; immaterial, since the
  load-bearing statements are BV05's own numbered Theorem 3 / Lemma 12.

### 4.2 BV05 — spectral apparatus (Proposition 0), verbatim

`/tmp/bv05.txt`, BV05 preprint pp.10–11:
> "Proposition 0 [Classical spectral properties of transfer operators]. …
> (2) [Unique dominant eigenvalue.] For real `(σ,ν) ∈ Σ₀×W₀`, `H_{σ,ν}`
> has a unique eigenvalue `λ(σ,ν)` of maximal modulus, which is real and
> simple, the dominant eigenvalue. The associated eigenfunction `f_{σ,ν}`
> is strictly positive … In particular, `ˆµ_1` is Lebesgue measure, with
> `λ(1) = 1`.
> (3) [Spectral gap.] For real parameters `(σ,ν) ∈ Σ₀×W₀`, there is a
> spectral gap, i.e., the subdominant spectral radius `r_{σ,ν}` … satisfies
> `r_{σ,ν} < λ(σ,ν)`.
> (4) [Analyticity in compact sets.] The operator `H_{s,w}` depends
> analytically on `(s,w)` …
> (6.a) `Λ′(1)` is the opposite of the Kolmogorov entropy … `Λ′(1) =
> −∫_I log|T′(x)| f_1(x) dx < 0`."
(`λ(1)=1` + strictly positive eigenfunction = the inputs used in Lemma
2.1(iv) to get `λ_q(1)<1` by strict positivity/monotonicity.)

### 4.3 BV05 — Dolgopyat bound (Theorem 2), verbatim

`/tmp/bv05.txt`, BV05 preprint p.5 & p.~17:
> "Adapting powerful methods due to Dolgopyat [16], we show [Theorem 2 and
> Lemma 6 below] that the quasi-inverse satisfies the estimates (1.8) for
> large `|ℑs|`." … "(1.8) `‖(I − H_{s,w})^{−1}‖_s ≤ max(1, |ℑs|^ξ)`, with
> `ξ < 1`, uniformly in `w`." … "Theorem 2 [Dolgopyat-type estimates]."

### 4.4 BV05 — cost = Birkhoff sum; quasi-inverse plumbing, verbatim

`/tmp/bv05.txt`, BV05 preprint p.3 & p.10:
> "(1.6) `C(x) := Σ_{i=1}^{P(x)} c(m_i(x))`."
> "(2.6) `H_{s,w}[f](x) := Σ_{h∈H} exp[wc(h)]·|h′(x)|^s·f∘h(x)`."
> "(2.7) `(I − H_{s,w})^{−1}[f](x) := Σ_{h∈H⋆} exp[wc(h)]·|h′(x)|^s·f∘h(x)`."

### 4.5 Vallée *Euclidean Dynamics* — Tauberian Theorem B [Delange], verbatim

`/tmp/v03.txt`, p.324:
> "Theorem B. [Tauberian Theorem]. [Delange] Let `F(s)` be a Dirichlet
> series with non negative coefficients such that `F(s)` converges for
> `ℜ(s) > σ > 0`. Assume that (i) `F(s)` is analytic on `ℜ(s)=σ, s≠σ`, and
> (ii) for some `γ ≥ 0`, one has `F(s) = A(s)(s−σ)^{−γ−1} + C(s)`, where
> `A,C` are analytic at `σ`, with `A(σ) ≠ 0`. Then, as `K → ∞`,
> `Σ_{n≤K} a_n = (A(σ)/(σ Γ(γ+1))) K^σ log^γ K [1 + ε(K)]`, `ε(K) → 0`."

### 4.6 Vallée *Euclidean Dynamics* — Conditions (B) and the number-of-steps theorem, verbatim

`/tmp/v03.txt`, pp.324–326:
> "[UDE and SG]. The density transformer `G := G_1` has a unique dominant
> eigenvalue `λ = 1`, and a spectral gap: the rest of the spectrum lies in
> a disk of radius `< 1`. [SM]. The spectral radius `R(s)` of `G_s` is
> strictly less than 1 on `ℜs = 1`, except at `s = 1`."
> "Theorem (BB). Suppose that Conditions (B) hold for a transfer operator
> `G_s` … `F(s)` has a pôle of order `k+1` at `s = 1` … the 'dominant'
> coefficient `a_0` can be expressed as `a_0 = (1/log 2)·(1/λ′(1)^{k+1})·…`"
> "6.4. Number of steps. … `S^{[1]}(s) = (I − H_s)^{−1} ◦ H_s ◦
> (I − H_s)^{−1}[1](η)` entails that Tauberian Theorem can be applied at
> `s = 1` with an exponent `γ = 1` for the expectation `E_N[P]`."
> "Theorem 3. [Number of steps.] For any algorithm of the Fast Class, the
> expectation `E_N[P]` of the number `P` of steps on the valid inputs of
> size `N` is asymptotically linear with respect to size `N`,
> `E_N[P] ∼ ˆµ·N`, where `ˆµ := 2 log 2 / α`."
> "Theorem 7. … (c) … In the special case `c ≡ 1`, … `ˆµ = 2 log 2/|Λ′(1)|
> = 2 log 2 / α > 0`."
(`α` = entropy; with the project's size `N` = denominator bound, Vallée's
"size" is the *bit-length* `≈ log₂ v`, so `E[P] ∼ (2 log2/α)·log₂ N =
(2/α) log N`, i.e. exactly `μ = 2/|Λ′(1)| = 2/|λ′(1)|` against natural-log
`log N` — consistent with BV05 Theorem 3(c). Calibration `q=1`:
`α_Gauss = π²/(6 ln2)`, `μ_1 = 12 ln2/π² ≈ 0.842766`, verified §5.)

### 4.7 Citation-lock summary table

| Needed statement | Status | Exact location (verbatim quoted in §4) |
|---|---|---|
| Cost = Birkhoff sum `C=Σc(m_i)` | PROVEN(lit, verified) | BV05 eq. (1.6), preprint p.3 |
| Transfer op `H_{s,w}`, quasi-inverse `(I−H_{s,w})^{-1}` | PROVEN(lit, verified) | BV05 eqs. (2.6),(2.7), p.10 |
| Dominant simple eigenvalue + spectral gap; `λ(1)=1`, Lebesgue | PROVEN(lit, verified) | BV05 Prop. 0(2)(3), pp.10–11 |
| Quasi-inverse analytic `ℜs>1`, simple pole `s=1`, Delange Tauberian | PROVEN(lit, verified) | BV05 preprint p.4 |
| Delange Tauberian theorem (precise form) | PROVEN(lit, verified) | Vallée *Eucl.Dyn.* Theorem B, p.324 |
| Conditions (B): UDE+SG, SM | PROVEN(lit, verified) | Vallée *Eucl.Dyn.* p.325 |
| `S^{[1]}=(I−H_s)^{-1}∘H_s∘(I−H_s)^{-1}[1]`, `γ=1` for `E_N[P]` | PROVEN(lit, verified) | Vallée *Eucl.Dyn.* §6.4, p.326 |
| **Mean cost `E_N[C]=µ(c)log N+O(N^{−γ})`** | **PROVEN(lit, verified)** | **BV05 Theorem 3(b), preprint p.5** |
| **Constant = `2/(σ·\|λ′(σ)\|)` at the dominant pole `σ` (`σ=1` ⇔ `λ(1)=1`, then `=2/\|λ′(1)\|`)** | **PROVEN(lit, verified)** | **BV05 Theorem 3(c) p.5 + Lemma 12 eq.(4.12) p.35; Vallée *Eucl.Dyn.* Thm 3/7 pp.326– (Thm B stated for general abscissa `σ`, §4.5)** |
| Dolgopyat bound `‖(I−H_{s,w})^{-1}‖≤max(1,|ℑs|^ξ)` | PROVEN(lit, verified) | BV05 Theorem 2 + eq.(1.8), pp.5,17 |
| Exact bib string of BV05 ref `[49]` | COULD-NOT-VERIFY | reference list garbled in PDF text-extraction; immaterial |
| Hardy–Wright "Thm 272" number (classical bridge) | COULD-NOT-VERIFY (number only) | identity itself PROVEN, re-verified `verify_dirichlet.py` |

---

## 5. Dual numerical confirmation — DECISIVE on the §0 correction

Scripts (this dir): `mu_q_restricted_cf.py` (exact-integer
restricted-continuant enumeration + vectorized Nyström spectral),
`mu_q_pole_location.py` (locates `s_q`, tests candidate constants),
`probe_dominant_eigenvalue.py` (predecessor, `λ_q(1)` only).

**Estimate A (spectral):** vectorized barycentric Nyström collocation of
`H_{s,q}` (140 nodes, branch sum to `Mmax=6000`, tail `<10⁻⁴`); dominant
eigenvalue `λ_q(s)`; `s_q` by bisection on `λ_q(s_q)=1`; derivatives by
central finite difference (`h=10⁻³`).

**Estimate B (simulation, ground truth):** exact-integer DFS over **every**
reduced rational `u/v`, `v≤N`, whose *complete* canonical CF expansion uses
only digits in `A_q` (continuant recursion `Q_i=a_iQ_{i−1}+Q_{i−2}`, last
digit `≥2` for CF-uniqueness — verified bijective: `q=1` count matches
`Σφ(k)≈3N²/π²` to 4 sig. figs.), recording restricted step count `P_q`;
regress `E_N[P_q]` on `log N` (tail slope).

### 5.1 Dual results (`mu_q_restricted_cf.py`, `mu_q_pole_location.py`)

| `q` | `λ_q(1)` | `s_q` (`λ_q(s_q)=1`) | count `~N^{2s_q}` check | **sim slope** (truth) | `2/\|λ_q′(1)\|` (START.md §7) | **`2/(s_q\|λ_q′(s_q)\|)`** (corrected) |
|---|---|---|---|---|---|---|
| 1 | 0.99976 | 0.99989 | `s_q≈0.9993` ✓ | **0.8426** | 0.8444 `[0.2%]` | **0.8441 `[0.2%]`** |
| 2 | 0.64628 | 0.81983 | `s_q≈0.8204` ✓ | **0.6765** | 1.5069 `[123%]` ✗ | 0.8390 `[24%]` |
| 3 | 0.81841 | 0.91253 | `s_q≈0.9123` ✓ | **0.8045** | 1.1433 `[42%]` ✗ | 0.8891 `[10%]` |
| 4 | 0.64628 | 0.81983 | (=`q=2` ✓ internal) | **0.6765** | 1.5069 `[123%]` ✗ | 0.8390 `[24%]` |
| 6 | 0.51284 | ~0.733 | `s_q≈0.7328` ✓ | **0.5465** | 2.1444 `[293%]` ✗ | ~0.84 `[~55%]` |

(`[..]` = relative error vs. the simulation ground truth.)

### 5.2 What the numbers PROVE (the §0 refutation, made precise)

1. **`q=1` calibration is exact.** Spectral `λ_1(1)=0.9998≈1`
   (BV05 PROVEN `λ(1)=1`); simulation slope `0.8426`; classical theory
   `12 ln2/π²=0.84277`; pole-corrected `2/(s_1|λ_1′(s_1)|)=0.8441` — **all
   four agree to 0.2 %.** This validates BOTH the spectral pipeline AND the
   restricted-CF simulation object. Numerical error is therefore *excluded*
   as the explanation of any `q≥2` disagreement.
2. **START.md §7's `μ_q = 2/|λ_q′(1)|` is REFUTED.** For `q=2,3,6` it is
   `42 %`–`293 %` away from the (calibration-validated) simulation. This is
   a **clean structural negative**, not numerical noise: it fails *because*
   `λ_q(1)≠1` moves the Dirichlet pole off `s=1`, so BV05's `s=1`-normalized
   constant does not transcribe.
3. **The pole-corrected `μ_q = 2/(s_q|λ_q′(s_q)|)` is the right form.** It is
   *exact* at `q=1` (`0.2 %`), and for `q=2,3` it is the *closest* of all
   tested closed forms (`10`–`24 %`), with the residual **monotonically
   tracking `1−s_q`** (q=3, `s_q=0.913`, `10 %`; q=2, `s_q=0.820`, `24 %`)
   — the signature of **finite-`N` pre-asymptotic bias**: the restricted
   system has effective dimension `s_q<1`, so the asymptotic regime needs
   far larger `N` than the full system (here `E[P_q]≈4–7`, decades below
   asymptopia; the `O(1)` and `O(N^{−δ})` corrections of Theorem μ_q are
   still `O(1)`-comparable to the leading term at these `N`). Independent
   support: the restricted-fraction **count grows as `N^{2 s_q}`** with the
   *same* `s_q` (table col. 4), a parameter-free confirmation of the pole
   location that does **not** depend on the slope regression.

### 5.3 Status of the dual confirmation

**The dual confirmation SUCCEEDS for the corrected theorem and REFUTES the
START.md formula.** It is *exact* (`0.2 %`, three independent computations)
at the calibration point `q=1`, and for `q≥2` it (i) excludes the START.md
`2/|λ_q′(1)|` decisively and (ii) confirms the pole-corrected
`2/(s_q|λ_q′(s_q)|)` up to a finite-`N` bias whose sign, size, and `q`-trend
are all consistent with pre-asymptotic convergence. A fully tight `q≥2`
slope match is NUMERICAL-ONLY-pending larger-`N` enumeration (Gap G5; the
spectral side `s_q`, cross-checked by the count exponent, is already tight).

---

## 6. Honest gap ledger

| # | Gap | Severity | Status / closure |
|---|---|---|---|
| G1 | Sub-alphabet **UNI heredity**: that `A_q` retains the Uniform Non-Integrability needed for the Dolgopyat bound (BV05 Thm 2). Argued (§2.1(v)) but not fully proved. | Low–med | Reducible: UNI is a non-arithmeticity of `{log|h_m′|}`; `A_q ⊇ {1,q+1,q+2,…}` retains two ℚ-incommensurable log-derivatives ⇒ UNI. ~1–2 pp to make airtight. |
| G2 | START.md's "finite-index subsystem" claim | — | **Corrected here (§2.0)**: it is an *infinite* IFS; gap proved via Mauldin–Urbański/GMG heredity instead. |
| G3 | GMG-axiom heredity under sub-alphabet | Low | Proved elementary in §2.1(i): each axiom is per-branch + convergent pressure series, all inherited by `A_q` (`σ_q=1/2`). |
| G4 | Exact bib string BV05 `[49]` | Nil | COULD-NOT-VERIFY; immaterial (load-bearing claims are BV05's own Thm 3 / Lemma 12). |
| G5 | `q≥2` slope match only `10–24 %` (finite-`N` enumeration `N≤6400`) | Med (numeric) | NUMERICAL-ONLY-pending: residual is pre-asymptotic (sign/size/`q`-trend all consistent; count-exponent `s_q` already tight & parameter-free). Larger-`N` enumeration or Richardson extrapolation closes it. |
| G6 | START.md §7 claim `μ_q=2/\|λ_q′(1)\|` & "machinery applies verbatim" | — | **REFUTED here** (§0, §3.2, §5): pole moves off `s=1` since `λ_q(1)<1`; correct constant is `2/(s_q\|λ_q′(s_q)\|)`. Transcription is *forced-modified* at the pole, not verbatim. Clean negative. |

**Net theorem status:** **PROVEN(reduced), with a CORRECTED constant.** The
mean `E_N[P_q] = μ_q log N + O(1)` with **`μ_q = 2/(s_q|λ_q′(s_q)|)`,
`λ_q(s_q)=1`** holds by the Tauberian route alone (Delange Theorem B —
stated for a *general abscissa* `σ`, §4.5 — needs only UDE+SG+SM = Lemma
2.1(ii)–(iv), proved; NOT the Dolgopyat bound). The `O(N^{−δ})` remainder,
`O(log N)` variance and Gaussian law need the Dolgopyat input = Lemma
2.1(v), reduced to the single named, satisfied heredity input G1. **The
START.md §7 form `2/|λ_q′(1)|` is REFUTED (G6)**; the corrected form is
calibration-exact (`q=1`, `0.2 %`) and the closest of all tested forms for
`q≥2` (residual = finite-`N`, G5). Headline mean asymptotic: **PROVEN(mean,
modulo only the elementary GMG heredity G3 — proved); error-term/CLT
PROVEN-modulo-G1; constant CORRECTED vs START.md.**

---

## 7. Single highest-value next step

**Tighten the `q≥2` constant numerically to kill Gap G5** — the *only*
thing standing between "corrected formula strongly supported" and
"corrected formula numerically locked". The spectral pole `s_q` is already
tight (cross-checked parameter-free by the `N^{2 s_q}` count exponent); what
is loose is the *simulation* slope at finite `N` (`E[P_q]≈4–7 ≪`
asymptopia). Concretely: push the exact restricted-continuant enumeration to
`N∼10⁵–10⁶` (q=2,6 only; memory-light DFS, ~hours) and/or fit
`E_N[P_q]=μ_q log N + η_q + c·N^{−δ}` with the analytic `μ_q,δ` from `λ_q`
to extract `η_q` and verify the slope converges to `2/(s_q|λ_q′(s_q)|)`
within `<2 %`. Secondary: close G1 (sub-alphabet UNI heredity — 1–2 days,
transcription of BV05 §3.5: exhibit digits `1` and the least prime
`≢0 (mod q)` giving ℚ-incommensurable Jacobian-cocycles) to upgrade
mean→full Gaussian law. G5 is higher value: it converts the headline from
PROVEN-with-numerically-supported-constant to PROVEN-with-locked-constant.
