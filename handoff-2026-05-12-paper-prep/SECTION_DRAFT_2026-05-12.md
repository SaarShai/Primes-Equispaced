# §X. Methodology, formalization, and numerical evidence

This section records the technical and computational content of the
paper: the algebraic identities at the heart of the corrected
$B_\infty$ framework (§X.3–§X.4), the open challenges that organise
the program forward (§X.4.4, §X.7), the numerical evidence at the
two scales on which our verification operates (§X.5), and the Lean 4
formalisation inventory (§X.6).

The numerical evidence has **two distinct verified scales**, which
we keep rigorously separate throughout. The **replication scale**
is $x = 1.3 \cdot 10^{13}$, at which two independent prime-counting
implementations agree on Koyama's Dominance-of-$-1$ residue tables
(§X.5.1). The **analytic-identity scale** is $K \le 10^{7}$, at
which the corrected $B_\infty$ identity, the subleading constant
$C_1$, and the Aoki–Koyama–Mertens drift toward $e^{-\gamma}$ are
verified across three numerical stacks (§X.5.2–§X.5.4). Numbers
from one scale are not transferred to the other.

---

## X.1 Notation

Fix a primitive non-principal Dirichlet character $\chi$ modulo
$q \ge 2$, and let $\rho = \tfrac12 + i\tau$ with $\tau \neq 0$ be a
simple non-trivial zero of $L(s,\chi)$. We use:

- $E_K(\chi,\rho) := \prod_{p \le K} (1 - \chi(p)\,p^{-\rho})^{-1}$
  (truncated partial Euler product);
- $c_K(\chi,\rho) := \sum_{n \le K} \mu(n)\,\chi(n)\,n^{-\rho}$
  (truncated Möbius sum);
- $D_K(\chi,\rho) := c_K(\chi,\rho)\,E_K(\chi,\rho)$
  (Dirichlet $D_K$ statistic);
- $T_K(\chi,\rho) := \sum_{p \le K}\sum_{k \ge 2} \chi(p)^k / (k\,p^{k\rho})$
  and its limit $T_\infty$ with $B_\infty := \exp(T_\infty)$;
- $C_1(\chi,\rho) := -L''(\rho,\chi) / (2\,L'(\rho,\chi)^2)$
  (subleading constant);
- $\psi$ for the primitive character of conductor $f \mid q$ inducing
  $\chi^2$.

The branch of $\log L(2\rho,\psi)$ is fixed by analytic continuation
from $\mathrm{Re}(s) > 1$, where the absolutely convergent log-Euler
expansion applies, to the boundary line $\mathrm{Re}(s) = 1$ via
Hadamard–de la Vallée Poussin non-vanishing.

For elliptic-curve work we use the arithmetic normalisation
$\rho_E = 1 + i\gamma_E$, $\rho_\Delta = 6 + i\gamma_\Delta$.

---

## X.2 Methodology of double verification

Every numerical claim of §X.5 is computed by **two independent
implementations in two languages with independent algorithms**.

- **L1 (primary).** `mpmath` 1.4 (Python 3.13), 50 decimal places.
  Direct partial-Möbius and partial-Euler evaluation; each zero $\rho$
  refined by Muller's method to $|L(\rho,\chi)| < 10^{-50}$.
- **L1b (in-language cross-check).** Same library, independent
  algorithm: Hurwitz-zeta expansion
  $L(s,\chi) = q^{-s}\sum_{a=1}^{q}\chi(a)\,\zeta(s, a/q)$ in place
  of `mpmath.dirichlet`, central-difference numerical derivatives at
  three step sizes, and an independent linear sieve for $\mu(n)$.
- **L2 (cross-language).** PARI/GP 2.17.3 (C), 57 dps default; with
  python-flint 0.8.0 / Arb (FLINT 3.3) at 250 bits as a third stack
  on the worst-case pair.

Acceptance gates: agreement to $\ge 12$ significant digits on $\rho$
and to $\ge 8$ digits on $L'$, $L''$, $C_1$; for residual quantities
where cancellation occurs (the $B_\infty$ residual), agreement to
$10^{-12}$ on each of the four component sums separately. Branch
choices and external citation provenance are recorded independently
in L1 and L2.

For the Phase-1 prime-residue replication of §X.5.1, "L1" is a
`primesieve` 12.13 segmented wheel sieve and "L2" is a hand-rolled
plain-C segmented Eratosthenes sieve with no external dependency.

---

## X.3 The local Perron double-pole residue

**Lemma X.3.1.** *Let $\chi$ be a primitive non-principal Dirichlet
character and let $\rho$ be a simple zero of $L(s,\chi)$. Then for
any $K > 1$,*
\begin{equation}
\label{eq:res}
\mathop{\mathrm{Res}}_{w = 0}\!\left[\,\frac{K^{w}}{w\,L(w + \rho,\chi)}\,\right]
\;=\;
\frac{\log K}{L'(\rho,\chi)} \;+\; C_1(\chi,\rho).
\end{equation}

*Proof.* Taylor-expand $L(w + \rho,\chi)$ at $w = 0$; invert to get
$1/L(w+\rho,\chi) = (L'(\rho,\chi)\,w)^{-1} - L''(\rho,\chi)/(2\,L'(\rho,\chi)^2) + O(w)$.
Multiply by $K^w/w = w^{-1} + \log K + O(w)$ and read off the
coefficient of $w^{-1}$. $\square$

Lemma X.3.1 is unconditional given simplicity of $\rho$. The full
algebraic derivation is in Appendix B §B.2.

---

## X.4 Identities

### X.4.1 Corrected $B_\infty$ identity (unconditional)

**Theorem X.4.1.** *Let $\chi$ be a primitive non-principal Dirichlet
character of conductor $q$, let $\rho$ be a simple zero of
$L(s,\chi)$ on the critical line, and let $\psi$ be the primitive
character of conductor $f \mid q$ inducing $\chi^2$. Then*
\begin{equation}
\label{eq:Binfty}
T_\infty(\chi,\rho)
\;=\;
\tfrac12 \log L(2\rho,\psi)
\;+\; \mathrm{BPC}_1(\chi,\rho)
\;+\; \mathrm{BPC}_2(\chi,\rho)
\;+\; T_{\ge 3}(\chi,\rho),
\end{equation}
*where*
$$
\mathrm{BPC}_1 = \tfrac12 \sum_{p \mid q,\, p \nmid f}
\log\bigl(1 - \psi(p)\,p^{-2\rho}\bigr),
$$
$$
\mathrm{BPC}_2 = -\tfrac12 \sum_{k \ge 2}\frac1k \sum_p \frac{\chi(p)^{2k}}{p^{2k\rho}},
\qquad
T_{\ge 3} = \sum_{k \ge 3}\frac1k \sum_p \frac{\chi(p)^k}{p^{k\rho}}.
$$
*The four right-hand-side terms are individually finite. The identity
is unconditional given simplicity of $\rho$.*

The $k = 1$ prime sum $\sum_p \chi^2(p) / p^{2\rho}$ is only
conditionally convergent on $\mathrm{Re}(s) = 1$; its convergence is
supplied by Akatsuka (2013, Lemma 2.1 / eq. (2.5)), which is itself
unconditional (derived from PNT with explicit error term). $\mathrm{BPC}_2$
and $T_{\ge 3}$ are absolutely convergent (minimum exponents
$\mathrm{Re}(2k\rho) = 2$ and $\mathrm{Re}(k\rho) = \tfrac32$). The
full proof is given in Appendix A.

### X.4.2 Subleading constant $C_1$ and the partial Möbius identity

**Theorem X.4.2.** *Under the hypotheses of Theorem X.4.1,*
\begin{equation}
\label{eq:cK}
c_K(\chi,\rho) \;=\; \frac{\log K}{L'(\rho,\chi)} \;+\; C_1(\chi,\rho) \;+\; o(1)
\qquad (K \to \infty).
\end{equation}
*The identity is unconditional. The rate $o(1) = O(K^{-1/2+\epsilon})$
is RH-conditional; the unconditional Soundararajan (2009) bound
gives $o(1) = O(K^{-1/2}\exp((\log K)^{1/2}(\log\log K)^{14}))$.*

The proof combines Inoue (2021, Theorem 1)'s truncated explicit
formula for $M^*(K,\chi)$ with Lemma X.3.1 to extract the double-pole
residue at $\rho$; off-target zero contributions are bounded by
Soundararajan's argument. See Appendix B for the full proof.

### X.4.3 The Aoki–Koyama–Mertens constant (Hypothesis AK)

Aoki–Koyama (2023, *J. Number Theory* **245**, eq. (1.4), p. 235)
states for a non-principal Dirichlet $\chi$ that, under DRH,
$$
\lim_{x \to \infty}\Bigl((\log x)^{m}\!\!\prod_{p \le x}(1 - \chi(p)/p^s)^{-1}\Bigr)
\;=\;
\frac{L^{(m)}(s,\chi)}{e^{m\gamma}\,m!} \cdot
\begin{cases}\sqrt 2, & \chi^2 = 1,\ s = \tfrac12,\\ 1, & \text{otherwise,}\end{cases}
$$
with $m = m_\chi = \mathrm{ord}_{s = 1/2}\,L(s,\chi)$. Specialised to
the regime of this paper ($m = 1$, $\rho \ne \tfrac12$, branch
multiplier $1$), this reads:
\begin{equation}
\label{eq:AK}
\lim_{K \to \infty} E_K(\chi,\rho)\,\log K \;=\; \frac{L'(\rho,\chi)}{e^{\gamma}}.
\tag*{(AK)}
\end{equation}
This **corrects** the earlier target $L'(\rho,\chi) / \zeta(2)$: the
ratio is $\zeta(2)/e^\gamma \approx 1.0828$. (AK) is DRH-conditional
in the form stated by Aoki–Koyama.

### X.4.4 The conditional NDC limit (open)

Composing (\ref{eq:cK}) with (AK) formally gives
\begin{equation}
\label{eq:NDC}
D_K(\chi,\rho) = c_K(\chi,\rho)\,E_K(\chi,\rho)
\;\longrightarrow\; e^{-\gamma}
\qquad (K \to \infty),
\tag*{(NDC)}
\end{equation}
the corrected Numerical Duality Constant. The composition is
mechanical provided (\ref{eq:cK}) is strengthened to the **shifted
Perron leading theorem**:
\begin{equation}
\label{eq:Perron-leading}
c_K(\chi,\rho) \;=\; \frac{\log K}{L'(\rho,\chi)} \;+\; o(\log K)
\qquad (K \to \infty).
\tag*{(SP-L)}
\end{equation}
The obstruction is the off-target nontrivial-zero residue aggregate:
even under DRH, an off-target zero $\lambda$ of multiplicity $m \ge 2$
contributes
$$
K^{\lambda - \rho}\,(\log K)^{m-1}\big/\bigl((m-1)!\,(\lambda - \rho)\,a_m(\lambda)\bigr),
$$
and the $(\log K)^{m-1}$ factor is not absorbed by simplicity of
$\rho$. We have searched the relevant literature (Inoue 2021,
Soundararajan 2009, Ng 2004, Akatsuka 2013) and have not found a
theorem that closes (SP-L); we state (NDC) as **conditional on (AK)
and (SP-L)** (Question Q:Perron, §X.7).

---

## X.5 Numerical findings

### X.5.1 Phase-1 Dominance-of-$-1$ replication, $x = 1.3 \cdot 10^{13}$

We independently replicate the prime-residue counts $\pi(x; N, a)$
of Koyama's *nontriv.pdf* for $N \in \{7, 8, 11, 19, 23\}$ and
$x \in \{10^{12}, 1.3\cdot 10^{12}, 10^{13}, 1.3\cdot 10^{13}\}$ via
two independent prime-enumeration implementations (`primesieve` 12.13
and a hand-rolled segmented C sieve). Headline numbers:

- $\pi(1.3 \cdot 10^{13}) = 445{,}831{,}610{,}611$, cross-checked
  against `primesieve --count` standalone.
- Library-independence: at every one of the four checkpoints, the
  `primesieve` counts and the hand-rolled C-sieve counts agree on
  every residue class for every $N$.
- Hardware-independence: a second M1-class machine agrees through
  $x = 1.3 \cdot 10^{12}$ on every residue class for every $N$.
- Koyama's identity (3.1), a Dirichlet-orthogonality cross-check on
  the residue-count vector, is verified directly at all $495$
  $(N, x, a)$-cells (worst real residual $1.4 \cdot 10^{-4}$).

Cell-by-cell comparison with Koyama's Tables 3–7 at all four
checkpoints, all moduli:

| Table | $N$ | cells | exact | substantive disagreement (at $x = 1.3 \cdot 10^{13}$) |
|---|---:|---:|---:|---|
| 3 | 7 | 12 | 11 | 1 cell ($\Delta = 50$, clean digit-shift profile) |
| 4 | 8 | 12 | 1 | 11 (small-$x$ rows; possible $x$-label error in Table 4 draft) |
| 5 | 11 | 20 | 19 | 1 cell ($a = 10$: our $11{,}503$ vs Koyama $71{,}711$) |
| 6 | 19 | 18 | 15 | 3 (2 substantive at $a = 13, 18$; 1 sign flip at small $x$) |
| 7 | 23 | 30 | 29 | 1 cell ($\Delta = 100$, clean transposition profile) |
| **Total** | | **92** | **75** | **17** (74/83 = 89% excluding the Table-4 small-$x$ rows) |

The qualitative dominance-of-$-1$ signal at $x = 1.3 \cdot 10^{13}$
is reproduced for $N \in \{7, 8, 19\}$. For $N = 11$ the dominance
ranking turns on the single substantive cell $a = 10$ above and is
**not reproduced** at this checkpoint pending Koyama's reconciliation;
at the smaller $x = 10^{12}$ checkpoint, $-1$ ranks first for both
$N = 11$ and $N = 19$, consistent with the Littlewood-style sign
flips Koyama attributes to low-lying $L$-zeros. For $N = 23$ the
dominance regime sets in around $e^{33.4} \approx 3 \cdot 10^{14}$,
beyond our checkpoint.

Replication bundle (delivered 2026-05-04): `koyama_replication_bundle/`
with source, build hashes, TSV outputs, and `MANIFEST.txt`.

### X.5.2 Numerical values of the four Dirichlet pairs

The four pairs $(\chi, \rho)$ used throughout §X.5.2–§X.5.4 (all
values computed at 50 dps via `Koyama_C1.py`):

| Pair | $\chi$ (conductor) | $\rho = \tfrac12 + i\tau$ | $L'(\rho,\chi)$ | $L''(\rho,\chi)$ |
|---|---|---|---|---|
| $\chi_{-4}/z_1$ | $\chi_{-4}$ ($q = 4$) | $\tfrac12 + 6.020949 i$ | $\phantom{-}1.296500 + 0.182765 i$ | $-1.697050 - 0.554017 i$ |
| $\chi_{-4}/z_2$ | $\chi_{-4}$ | $\tfrac12 + 10.243770 i$ | $\phantom{-}1.788467 - 0.296776 i$ | $-3.319767 + 0.755548 i$ |
| $\chi_5$ | $\chi_5$ ($q = 5$) | $\tfrac12 + 6.183578 i$ | $\phantom{-}1.112930 - 0.448830 i$ | $-1.642973 + 1.035107 i$ |
| $\chi_{11}$ | $\chi_{11}$ ($q = 11$) | $\tfrac12 + 3.547041 i$ | $\phantom{-}1.696582 - 0.250988 i$ | $-3.121598 + 0.261219 i$ |

L1b in-language cross-check (Hurwitz expansion, independent sieve)
agrees with L1 to $|\Delta L'|, |\Delta L''| \lesssim 6 \cdot 10^{-12}$
and $|\Delta C_1| \lesssim 5 \cdot 10^{-13}$. L2 cross-language (PARI/GP
2.17.3) agrees with L1 to $\ge 11$ decimal digits on every real and
imaginary component. An Arb spot-check at 250 bits on the worst pair
gives interval agreement on $|L'|$ within $3 \cdot 10^{-43}$.

### X.5.3 The Aoki–Koyama drift: $e^{-\gamma}$ vs $\zeta(2)^{-1}$

The modulus $|D_K|$ statistic at $K = 2 \cdot 10^{6}$ and $K = 10^{7}$
(40 dps, mean over the four pairs):

| Quantity | $K = 2 \cdot 10^{6}$ | $K = 10^{7}$ | $\zeta(2)^{-1}$ target | $e^{-\gamma}$ target |
|---|---:|---:|---:|---:|
| Mean $|D_K| \cdot \zeta(2)$ | $0.992$ | $0.974$ | $1.000$ | $\zeta(2)\,e^{-\gamma} \approx 0.9237$ |
| Mean $|E_K \log K|\,e^{\gamma}/|L'|$ | --- | $0.942$ | --- | $1.000$ |

The drift from $0.992$ to $0.974$ between $K = 2 \cdot 10^{6}$ and
$K = 10^{7}$ is consistent with the AK normalisation $e^{-\gamma}$
at the natural $1/\log K$ finite-size scale and **incompatible with
the $\zeta(2)^{-1}$ target** at the same scale. We do not claim
convergence of the complex $D_K(\chi,\rho)$ from a modulus statistic
alone — that depends on (SP-L), which is open.

### X.5.4 The $B_\infty$ identity at the four pairs

Identity residual $|T_K - \mathrm{RHS}|$ for (\ref{eq:Binfty}) at
$K = 2 \cdot 10^{6}$ (mpmath, 50 dps) and $K = 10^{7}$ (PARI/GP
2.17.3, closed-form component evaluation):

| Pair | $K = 2 \cdot 10^{6}$ (L1) | $K = 2 \cdot 10^{6}$ (L2) | $K = 10^{7}$ (L2) |
|---|---:|---:|---:|
| $\chi_{-4}/z_1$ | $2.85 \cdot 10^{-3}$ | $2.85 \cdot 10^{-3}$ | $2.58 \cdot 10^{-3}$ |
| $\chi_{-4}/z_2$ | $1.66 \cdot 10^{-3}$ | $1.66 \cdot 10^{-3}$ | $1.52 \cdot 10^{-3}$ |
| $\chi_5$        | $4.24 \cdot 10^{-5}$ | $4.24 \cdot 10^{-5}$ | $1.22 \cdot 10^{-5}$ |
| $\chi_{11}$     | $3.33 \cdot 10^{-5}$ | $3.34 \cdot 10^{-5}$ | $1.75 \cdot 10^{-5}$ |

L1 and L2 agree to all displayed digits at $K = 2 \cdot 10^{6}$
(stack difference $\le 10^{-8}$). For the clean-character pairs
$\chi_5$, $\chi_{11}$ (where $\chi(2) \ne 0$ and there is no bad-prime
contribution to $\mathrm{BPC}_1$), the residual decays by a factor
$1.9$–$3.5$ from $K = 2 \cdot 10^{6}$ to $K = 10^{7}$, bracketing
the $\sqrt{5} \approx 2.24$ predicted by the $K^{-1/2} / \log K$ rate
of the boundary-line conditional tail (Akatsuka 2013 eq. (2.5)). The
$\chi_{-4}$ pairs show systematically larger residuals consistent
with the bad-prime $p = 2$ contribution to $\mathrm{BPC}_1$.

### X.5.5 Conductor-confounded rank trend

A multivariate OLS regression of $E[C_1^2]$ on $(\mathrm{rank},\log N)$
across 19 weight-2 elliptic curves (data in
`koyama-shared/data/PATH_B_20FORMS.csv`) returns
\begin{equation}
\label{eq:W2}
E[C_1^2] \;=\; -0.1811 \;+\; (-0.6773)\,\mathrm{rank} \;+\; 0.7345\,\log N,
\qquad R^2 = 0.8144.
\end{equation}
The $\log N$ coefficient is statistically significant and stable
under resampling; **the rank coefficient is not**. Leaving the
rank-3 anchor ($5077a_1$) out shifts the rank coefficient from
$-0.6773$ to $-0.2533$ (a 63% relative change). The bootstrap 95%
CI for the rank coefficient is $[-1.222,\,+0.104]$, *includes zero*,
and the sign-flip rate is $4.7\%$. We therefore describe
(\ref{eq:W2}) as a **conductor-confounded trend**, not a clean rank
law, and pose its resolution as Question Q:conductor (§X.7).

The raw $\mathrm{Sym}^2 / \langle f, f \rangle$ proportionality
across $\{37a_1, 389a_1, \Delta\}$ ranges over seven orders of
magnitude (ratios $6.70$, $0.638$, $610{,}456$); the raw form is
**empirically falsified**. A completed / archimedean-corrected
normalisation may survive; we pose its identification as
Question Q:Sym2 (§X.7).

---

## X.6 Lean 4 / Mathlib4 formalisation

We accompany the paper with a Lean 4 / Mathlib4 lake project in the
companion repository at
`primes-equispaced/formal-conjectures/`. The toolchain is
`leanprover/lean4:v4.28.0`; Mathlib is pinned at commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`. The Lean inventory fixes
the **statements** of every identity of §X.4, ensures normalisations
and branch conventions are syntactically explicit, and records each
statement's proof status against a public audit trail.

**Build status.** `lake build FormalConjectures` succeeds on all
**8 files** in `formal-conjectures/` with 11 `sorry` warnings, each
annotated in-source as `MATHLIB-PREREQ:` (an upstream Mathlib lemma
not yet available) or `RESEARCH-OPEN:` (an open mathematical
conjecture or pending formalisation). No `axiom` is introduced
anywhere in the project. The full per-`sorry` inventory is in
`LEAN_SORRY_STATUS.md` of the reproducibility bundle.

| Paper object | Lean file | Status |
|---|---|---|
| Boundary residue $R_0 = -2$ for the smoothed $\Delta w_f$ explicit formula (Schwartz cutoff) and 25+ algebraic-glue theorems | `SmoothedDwfFormula_full.lean` | **THEOREM (chain).** All algebraic-glue lemmas closed without `sorry`. Two remaining `sorry`s are named analytic prerequisites: `mellin_decay` (Stirling on $\Gamma$ vertical strips) and `inv_zeta_polynomial_growth` (Titchmarsh §3.11) — Mathlib v4.28.0 has only the qualitative versions. |
| Lemma X.3.1 (local Perron residue) | `LocalPerronResidue.lean` | **STATEMENT-CLOSED, PROOF research-open.** Auxiliary `perronResidue_eq` closed by `ring`; main theorem stated as a `Tendsto` limit with 1 `sorry` awaiting `AnalyticAt.hasFPowerSeriesAt`. |
| Theorem X.4.1 ($B_\infty$ identity) | `CorrectedBInfty.lean` | **STATEMENT-CLOSED, PROOF research-open.** Four-component identity stated against `noncomputable def`s of $T_\infty$, $T_{\ge 3}$, $\mathrm{BPC}_1$, $\mathrm{BPC}_2$, $L$. The single `sorry` is the proof, awaiting Akatsuka (2013) eq. (2.5). |
| Farey bridge identity | `FareyBridgeIdentity.lean` | **SCAFFOLD.** Identity stated against a local `FareySet`; 1 `sorry`. `MATHLIB-PREREQ: Mathlib.NumberTheory.RamanujanSum`. |
| Mertens spectroscope universality | `MertensSpectroscopeUniversality.lean` | **SCAFFOLD.** Stated as `Tendsto … atTop atTop` against an inline RH-for-$\zeta$ predicate; 1 `sorry`. |
| Farey sign pattern | `FareySignPattern.lean` | **NEGATIVE.** The pointwise version is falsified at $p = 237{,}733$ and $p = 243{,}799$ (recorded as theorems, not axioms — the project's "no `axiom`" convention is preserved). The density-one surviving version is stated as a `Tendsto`. 3 `sorry`s. |
| Dirichlet Polynomial Avoidance (DPAC) statement + four phase-avoidance bridge layers | `DirichletPolynomialAvoidance.lean`, `DPAC_full.lean` | **OPEN (the headline conjecture).** The earlier LI-to-DPAC bridge is tombstoned; four explicit phase-avoidance bridges (`dpac_of_logPrimePhaseAvoidance`, …, `dpac_of_certifiedZetaZeroSample`) are **closed without `sorry`**. The remaining `sorry` is DPAC itself, diagnostically comparable to the Linear Independence Hypothesis. Submitted as `google-deepmind/formal-conjectures` PR #3716. |

The role of the Lean artifact is to fix the statements and provide
a publicly inspectable audit trail of the proof obligations
remaining.

---

## X.7 Open challenges

The following structure the next phase of the program.

> **Q:Perron (Shifted Perron leading theorem).** Prove (SP-L)
> (\ref{eq:Perron-leading}) for primitive non-principal $\chi$ and
> simple non-central $\rho$.

Sufficient packages: (a) all crossed off-target zeros simple and
$Z_\mathrm{simple}(K, T_K) := \sum_{\rho' \ne \rho,\,|\gamma'| \le T_K} K^{\rho'-\rho}/[(\rho'-\rho)\,L'(\rho',\chi)] = o(\log K)$
at a zero-avoiding height $T_K \asymp K(\log K)^{-B}$; (b) a
Dirichlet shifted second moment
$\sum_{\rho'}^\mathrm{mult} |L(\rho' + \alpha,\chi)|^{-2} \ll_\chi (\log K)^{O(1)}$.
The total-Möbius bounds of Soundararajan type are too coarse to
isolate the pointwise cancellation at the $\log K$ scale.

We note a *structural* development that does not close (SP-L) but
identifies the right pivot: the GL(2) **halo-route reduction**
(divided-difference cluster residues + signed contour cancellation
over a halo region) gives $|R_\Phi(T)| \ll M_T \cdot T^{7/4+\varepsilon}$
in the elliptic-curve setting, with three of four "doors" closed and
the remaining one a Dirichlet shifted second moment. Its naïve
GL(1) transfer yields only $K^{1/2+\varepsilon}$, still far above
$o(\log K)$ — so the halo route in its present form **does not close
(SP-L)**, but the cluster-summed-residue pivot replaces the rooted
Palm wall that obstructs the termwise estimate. The full GL(2)
plan is in the supplementary repository
([`HALO_UNCONDITIONAL_PLAN_2026-05-12.md`](../handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md));
the GL(1) accounting is in
[`HALO_GL1_SKETCH_2026-05-12.md`](HALO_GL1_SKETCH_2026-05-12.md).

> **Q:EC-recip (GL(2) reciprocal-derivative control).** Prove a
> fixed-curve theorem for
> $\sum_\gamma \widehat W(i\gamma)\,e^{i\gamma u} / L'(E, 1 + i\gamma)$
> giving cancellation $o(u^r)$, or a minimum-modulus estimate
> on a vertical line with explicit exponent $< 2$.

Without a GL(2) analogue of Aoki–Koyama, the EC side remains at the
level of quantitative ensemble evidence.

> **Q:conductor (rank vs $\log N$).** Replicate (\ref{eq:W2}) on a
> curve set in which rank and $\log N$ are not collinear.

> **Q:Sym2 (corrected Sym$^2$ normalisation).** Identify a completed
> / archimedean-corrected Sym$^2$ normalisation replacing the
> empirically falsified raw $\mathrm{Sym}^2 / \langle f,f\rangle$
> proportionality.

> **Q:DPAC (Dirichlet Polynomial Avoidance).** Prove DPAC (the
> phase-avoidance bridges are formalised in Lean; the headline
> conjecture is open).

> **Q:EC-NDC (EC NDC normalisation).** Find a normalisation of
> $D_K^E$ for which the universal limit exists and survives a
> null-control gate. The simple sharp-cutoff form
> $D_K^E \cdot \zeta(2) \to 1$ is **falsified** through $K = 10^{6}$;
> smoothed variants pass empirically but also pass a null-control
> gate against predeclared null transformations, so the gate is not
> load-bearing.

---

## X.8 Code, data, and certificate availability

All scripts, refined zero data, numerical-table CSVs, convergence
logs, the Lean 4 lake project, and the reproducibility manifest will
be deposited as a single self-contained reproducibility bundle
(Supplementary material S1), mirrored at a Zenodo DOI at acceptance.
The bundle pins all software versions: Lean toolchain
`leanprover/lean4:v4.28.0`, Mathlib commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`, `mpmath` 1.4,
PARI/GP 2.17.3, FLINT 3.3 / python-flint 0.8.0. The Phase-1
Dominance-of-$-1$ replication bundle (`koyama_replication_bundle.zip`)
is the version supplied to S. Koyama on 2026-05-04. Each numerical
table in §X.5 cites the L1 script and L2 reproducer; each external
theorem cited in §X.4 has its PDF retrieval recipe, page/equation,
and verbatim quote recorded in the citation audit
(Supplementary S2 / Appendix C).
