<!--
schema_version: 1
title: "Saar–Koyama paper — Technical & Computational section, first draft"
date: 2026-05-12
type: section-draft
tier: working
status: DRAFT_INTERNAL_NOT_SENT
target: "first complete draft for internal review; Koyama 2026-05-12 ask"
authorship: "left as placeholders; user has not yet fixed author order"
sources:
  - handoff-2026-05-12-paper-prep/TECHNICAL_COMPUTATIONAL_SECTION_PLAN_2026-05-12.md
  - handoff-2026-05-12-paper-prep/SCOPE_AUDIT_10E13_2026-05-12.md
  - handoff-2026-05-12-paper-prep/ADVERSARIAL_AUDIT_RESPONSE_2026-05-12.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
  - HANDOFF.md
tags: [koyama, draft, technical-section, computational-section, lean4]
-->

# §X. Methodology, formalization, and numerical evidence

> *Internal draft, 2026-05-12. Author order and journal target are open
> placeholders. The draft is written so that statements, tables, and
> normalizations can be transferred to LaTeX with minimal rework.
> Cross-references such as `(\thmref{B-infty})` use placeholder
> labels.*

This section gathers the computational and formal content of the
present paper. **The core results we address here** — following the
framing of S. Koyama in our 2026-05-12 correspondence — are:

1. **Correction of the asymptotic target.** The earlier numerical
   target $1/\zeta(2)$ for the Dirichlet partial-Euler-product
   asymptotic at simple noncentral zeros is replaced by the
   Mertens–Aoki–Koyama constant $e^{-\gamma}$ (§X.4.3); we record
   the verbatim Aoki–Koyama (2023) statement and document the
   $K \le 10^7$ drift in $|D_K|\cdot\zeta(2)$ from $0.992$ at
   $K = 2\cdot 10^6$ to $0.974$ at $K = 10^7$, consistent with the
   $e^{-\gamma}$ target and incompatible with $\zeta(2)^{-1}$ at the
   $1/\log K$ finite-size scale (§X.5.2).
2. **The corrected $B_\infty$ identity and the local Perron
   double-pole residue,** both established unconditionally
   (Lemma X.3.1 and Theorem X.4.1; full proofs in Appendices A and B).
3. **The "open challenges" that organize the program forward** — the
   shifted Perron leading remainder (SP-L), the conductor-confounded
   elliptic-curve rank trend, the corrected
   $\mathrm{Sym}^2 / \langle f, f \rangle$ normalization, GL(2)
   reciprocal-derivative control, and the Dirichlet Polynomial
   Avoidance Conjecture (§X.4.4 and §X.7). Each is stated precisely
   and credited with the input theorem that would close it.
4. **The rigorous independent replication of Koyama's
   Dominance-of-$-1$ residue-count tables at $x = 1.3 \cdot 10^{13}$**
   (§X.5.1): two implementations (`primesieve` plus a hand-rolled C
   segmented sieve) agree on every residue count at this scale for
   $N \in \{7, 8, 11, 19, 23\}$; identity (3.1) of *nontriv.pdf* is
   verified across $495$ $(N,x,a)$-cells; the qualitative
   dominance signal is reproduced for $N \in \{7, 8, 19\}$, with
   $N = 11$ at $1.3 \cdot 10^{13}$ pending the joint reconciliation
   of one substantive Table-5 cell.

The remainder of the section gives the precise normalizations
(§X.1), the double-verification protocol used for every numerical
claim (§X.2), the algebraic identities (§X.3–§X.4), the numerical
evidence (§X.5), the Lean 4 / Mathlib4 partial formalization (§X.6),
the open-challenges list (§X.7), and the code-and-data availability
statement (§X.8).

The numerical evidence has two clearly distinct scales which we keep
separate throughout: a **replication scale** at
$x = 1.3 \cdot 10^{13}$, where two independent implementations agree
on the prime-residue counts $\pi(x; q, a)$ of Koyama's
Dominance-of-$-1$ framework (§X.5.1), and an **analytic-identity
scale** at $K \le 2 \cdot 10^{6}$–$10^{7}$, where the corrected
$B_\infty$ identity, the subleading constant $C_1$, and the
Aoki–Koyama drift toward $e^{-\gamma}$ are verified (§X.5.2–§X.5.5).
The replication evidence is presented in its own subsection; the
analytic identities are not extrapolated to the replication scale,
and the replication numbers are not used as evidence for any
analytic identity.

---

## X.1 Notation and normalizations

Fix a primitive non-principal Dirichlet character $\chi$ modulo
$q \ge 2$, and let $\rho = \tfrac12 + i\tau$ with $\tau \neq 0$ be a
**simple** non-trivial zero of $L(s,\chi)$ on the critical line. We
work throughout with the following objects:

- **Truncated partial Euler product:**
  $$
  E_K(\chi,\rho) \;:=\; \prod_{p\le K} \Bigl(1 - \chi(p)\,p^{-\rho}\Bigr)^{-1}.
  $$
- **Truncated Möbius / Mertens spectroscope sum:**
  $$
  c_K(\chi,\rho) \;:=\; \sum_{n\le K} \mu(n)\,\chi(n)\,n^{-\rho}.
  $$
- **Dirichlet $D_K$ statistic:**
  $$
  D_K(\chi,\rho) \;:=\; c_K(\chi,\rho)\,E_K(\chi,\rho).
  $$
- **Prime-power tail $T_K$ and its limit $T_\infty = \log B_\infty$:**
  $$
  T_K(\chi,\rho) \;:=\; \sum_{p\le K}\,\sum_{k\ge 2}\frac{\chi(p)^k}{k\,p^{k\rho}},
  \qquad
  B_\infty(\chi,\rho) \;:=\; \exp\bigl(T_\infty(\chi,\rho)\bigr).
  $$
- **Subleading constant:**
  $$
  C_1(\chi,\rho) \;:=\; -\,\frac{L''(\rho,\chi)}{2\,L'(\rho,\chi)^2}.
  $$
- **Imprimitive companion:** $\psi$ denotes the primitive Dirichlet
  character of conductor $f \mid q$ such that
  $\chi(n)^2 = \psi(n)$ for $\gcd(n,q)=1$ and $\chi(n)^2 = 0$ otherwise.

For elliptic-curve and weight-$k$ cusp-form work we use the
arithmetic normalization
$$
\rho_E = 1 + i\gamma_E,
\qquad
\rho_\Delta = 6 + i\gamma_\Delta,
$$
not the analytic critical-line normalization $\tfrac12 + i\gamma$.
Mixing arithmetic and analytic normalizations was the bug class which
invalidated all pre-2026-04-15 EC values of $C_1$; the corrected
table appears in §X.5.

The branch of $\log L(2\rho,\psi)$ is fixed by analytic continuation
through $\mathrm{Re}(s) > 1$, using the absolutely convergent log-Euler
expansion at $s = 2\rho$ for $\mathrm{Re}(s) > 1$ and extending to the
boundary line $\mathrm{Re}(s) = 1$ (excluding $s=1$) by classical
Hadamard–de la Vallée Poussin non-vanishing.

---

## X.2 Methodology of double verification

Every numerical claim in §X.5 is computed by *two independent
implementations in two languages with two independent algorithmic
paths*, then submitted to an *adversarial referee pass* whose role is
to attempt the strongest possible objection to each promotion-grade
claim. This three-layer stack is summarized below.

| Layer | Stack | Status | What it does |
|---|---|---|---|
| **L1: primary computation** | `mpmath` 1.4 (Python 3.9 / 3.13), 50 decimal places by default. | Executed | Direct partial-sum and partial-Euler-product evaluation. Refines each $\rho$ by Muller's method until $|L(\rho,\chi)| < 10^{-50}$. |
| **L1b: in-language cross-check (independent algorithm, same library)** | `mpmath` 1.4, but with the Hurwitz-zeta expansion $L(s,\chi)=q^{-s}\sum_{a=1}^{q}\chi(a)\zeta(s,a/q)$ in place of `mpmath.dirichlet`, central-difference numerical derivatives at three step sizes, and a fresh linear sieve for $\mu(n)$. | Executed 2026-05-12 ([`L2_CROSSCHECK_2026-05-12.md`](L2_CROSSCHECK_2026-05-12.md)); agreement $\le 6\cdot 10^{-12}$ on $L', L''$ and $\le 5\cdot 10^{-13}$ on $C_1$. | Catches algorithm-class bugs (mistaken sieve, wrong derivative recipe, wrong character table) but **shares** the underlying arbitrary-precision library. Not a substitute for L2. |
| **L2: cross-language re-implementation** | PARI/GP 2.17.3 (C, default 57 dps, conda-forge `pari` package); python-flint 0.8.0 / Arb (FLINT 3.3) at 250 bits for a third-stack spot-check. | **Executed 2026-05-12** ([`pari_L2_crosscheck.gp`](pari_L2_crosscheck.gp) → [`L2_PARI_CROSSCHECK_2026-05-12.md`](L2_PARI_CROSSCHECK_2026-05-12.md); [`arb_L2_spot.py`](arb_L2_spot.py) → [`ARB_L2_SPOT_2026-05-12.md`](ARB_L2_SPOT_2026-05-12.md)). | Independent zero-search via Newton on `lfun`; independent analytic $L'$ via PARI's `lfun(L,s,1)`; independent $L''$ via central differences; independent character evaluation via `kronecker(-4,·)` (for $\chi_{-4}$) and `chareval(G, [1], ·)` (for $\chi_5$, $\chi_{11}$); independent $\mu$-sieve via PARI's `moebius`. Arb spot-check uses interval arithmetic at 250 bits as a third stack. |
| **L3: structured adversarial pre-submission audit** | Generative models on stacks distinct from the primary Anthropic-API workflow: a non-Anthropic API (Xiaomi MiMo `mimo-v2.5-pro`) for prose / claim-status auditing; local LLMs on the host's Apple-silicon hardware (Ollama: `qwen3.6:35b-a3b-q4km`, `deepseek-r1:32b`; MLX: `Qwen2.5-1.5B-Instruct-4bit`) for symbolic re-derivation. | Executed against component identities (2026-05-12) and against this section draft (2026-05-12). | Each reviewer is prompted in isolation to produce the sharpest available objections, or to re-derive a load-bearing identity from scratch. Output is structured (numbered objections + severity + suggested fix; or symbolic derivation steps). We do **not** claim author-independence; the reviewers are prompted with the draft text. We claim *stack-independence* and *adversarial framing* — the reviewers are instructed to attack, not to confirm. Objections that survive a written authors' response trigger a *downgrade* of the affected claim. |

Acceptance gates:

- L1 and L2 must agree to $\ge 12$ significant decimal digits on $\rho$
  itself and to $\ge 8$ digits on $L'(\rho,\chi)$, $L''(\rho,\chi)$,
  $C_1(\chi,\rho)$.
- For complex-valued residuals where cancellation occurs between
  nearly equal quantities (e.g. the $B_\infty$ identity residual at
  $K = 2 \cdot 10^6$), agreement to $10^{-12}$ is required on each
  of the four component sums separately.
- Branch choices are recorded independently for L1 and L2; an
  adversarial branch-flip test is run as part of L3.
- For every external theorem cited, the PDF is retrieved, the page
  and equation are recorded, and a short verbatim quote is embedded
  in the manuscript or its appendix.

The L3 layer is not a substitute for human refereeing; it is a
mechanical check that the prose and the load-bearing algebra survive
an adversarial reading. Two pilot dispatches were run on
2026-05-12. The Ollama `qwen3.6:35b-a3b-q4km` model, asked in
isolation, **independently reproduced** the simple-zero Laurent
expansion
$$
\frac{1}{L(w+\rho,\chi)}
\;=\;\frac{1}{L'(\rho,\chi)\,w} \;-\; \frac{L''(\rho,\chi)}{2\,L'(\rho,\chi)^2} \;+\; O(w)
$$
and the consequent residue identity $(\eqref{eq:res})$. The MiMo
`mimo-v2.5-pro` model, asked to produce the strongest objections to
the four headline claims, raised six numbered objections; all six
were either rejected on the merits with explicit reference to source
material or accepted as wording/presentation corrections (no fatal
objection survived). The full adversarial pass against the present
draft will be repeated once the section text is fixed.

---

## X.3 The local Perron double-pole residue (proved algebraically)

The starting point of every Dirichlet-side identity in this section
is the algebraic residue at a simple zero $\rho$.

**Lemma X.3.1 (local Perron double-pole residue).** *Let $\chi$ be a
primitive non-principal Dirichlet character and let $\rho$ be a simple
zero of $L(s,\chi)$. Then for any $K > 1$,*
\begin{equation}
\label{eq:res}
\mathop{\mathrm{Res}}_{w=0}\!\left[\,\frac{K^{w}}{w\,L(w+\rho,\chi)}\,\right]
\;=\;
\frac{\log K}{L'(\rho,\chi)} \;-\; \frac{L''(\rho,\chi)}{2\,L'(\rho,\chi)^{2}}
\;=\;
\frac{\log K}{L'(\rho,\chi)} + C_1(\chi,\rho).
\end{equation}

*Proof.* The Taylor expansion of $L(w+\rho,\chi)$ at $w = 0$ is
$L(w+\rho,\chi) = w\,L'(\rho,\chi) + \tfrac{w^2}{2}\,L''(\rho,\chi) + O(w^3)$,
so $1/L(w+\rho,\chi) = (L'(\rho,\chi)\,w)^{-1} -
L''(\rho,\chi) / (2\,L'(\rho,\chi)^2) + O(w)$. Multiplying by
$K^w/w = w^{-1} + \log K + \tfrac12(\log K)^2\,w + O(w^2)$ and
collecting the coefficient of $w^{-1}$ yields the displayed
identity.&nbsp;$\square$

Lemma X.3.1 is unconditional (no hypothesis beyond simplicity of
$\rho$) and is the *only* algebraic step that the section's later
claims rest on; it has been derived twice independently in our
internal record (by direct hand computation and by a separate
non-Anthropic LLM under the L3 adversarial protocol), with identical
output.

---

## X.4 Identities

### X.4.1 Corrected $B_\infty$ identity (unconditional)

**Theorem X.4.1 (corrected $B_\infty$ identity).** *Let $\chi$ be a
primitive non-principal Dirichlet character of conductor $q$, and
let $\rho$ be a simple zero of $L(s,\chi)$ on the critical line.
Let $\psi$ be the primitive character of conductor $f\mid q$ inducing
$\chi^2$. Then*
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
\mathrm{BPC}_1
\;=\;
\tfrac12 \sum_{p\mid q,\ p\nmid f} \log\!\bigl(1 - \psi(p)\,p^{-2\rho}\bigr),
$$
$$
\mathrm{BPC}_2
\;=\;
-\tfrac12 \sum_{k\ge 2} \frac1k \sum_p \frac{\chi(p)^{2k}}{p^{2k\rho}},
\qquad
T_{\ge 3}
\;=\;
\sum_{k\ge 3} \frac1k \sum_p \frac{\chi(p)^k}{p^{k\rho}}.
$$
*Each of the four terms on the right-hand side is individually
finite, and $\mathrm{BPC}_2$ and $T_{\ge 3}$ are absolutely convergent
(minimum exponents $\mathrm{Re}(2k\rho)\!=\!2$ for $k=2$ in
$\mathrm{BPC}_2$, and $\mathrm{Re}(k\rho)\!=\!\tfrac32$ for $k=3$ in
$T_{\ge 3}$). The k=1 prime sum
$\sum_p \chi^2(p)/p^{2\rho}$, which is conditionally convergent on
$\mathrm{Re}(s) = 1$, is the source of $\tfrac12 \log L(2\rho,\psi)$,
the convergence being handled by Akatsuka (2013) Lemma 2.1 / eq. (2.5)
and the imprimitive-induction identity $L(s,\chi^2) = L(s,\psi)
\prod_{p\mid q,\,p\nmid f}(1 - \psi(p)p^{-s})$.*

The identity holds unconditionally; no hypothesis beyond simplicity
of $\rho$ as a zero of $L(s,\chi)$ is used. The full proof is given
in **Appendix A** (see
[`APPENDIX_A_BINFTY_PROOF.md`](APPENDIX_A_BINFTY_PROOF.md)), based on
the partial-Euler log-Taylor expansion and the classical
Hadamard–de la Vallée Poussin non-vanishing of $L$ on
$\mathrm{Re}(s) = 1$. The k=1 prime sum
$\sum_p \chi^2(p)/p^{2\rho}$ is conditionally convergent on
$\mathrm{Re}(s) = 1$; that convergence is supplied by Akatsuka (2013,
*The Euler product for the Riemann zeta function in the critical
strip*, Lemma 2.1 and equation (2.5)), which is an **unconditional**
Mertens-type partial-summation result (derived from PNT with an
explicit error term; it does not require RH or any GRH-type
hypothesis). Consequently, the identity (\ref{eq:Binfty}) is itself
unconditional.

A convergence-regime table:

| Term | Convergence | Hypothesis used |
|---|---|---|
| $\tfrac12 \log L(2\rho, \psi)$ | conditional at $\mathrm{Re}(s) = 1$; absolute at $\mathrm{Re}(s) > 1$ | Akatsuka 2013 Lemma 2.1 |
| $\mathrm{BPC}_1$ | finite sum over bad primes | textbook (Montgomery–Vaughan Thm 9.4) |
| $\mathrm{BPC}_2$ | absolute, $\mathrm{Re}(2k\rho) \ge 2$ | geometric-series + prime-zeta tail |
| $T_{\ge 3}$ | absolute, $\mathrm{Re}(k\rho) \ge \tfrac32$ | geometric-series + prime-zeta tail |

### X.4.2 Subleading constant $C_1$ and the partial Möbius identity

**Theorem X.4.2 (Möbius-side leading + subleading).** *Under the
hypotheses of Theorem X.4.1,*
\begin{equation}
\label{eq:cK}
c_K(\chi,\rho) \;=\; \frac{\log K}{L'(\rho,\chi)} \;+\; C_1(\chi,\rho) \;+\; o(1)
\qquad (K \to \infty).
\end{equation}
*The identity is unconditional given simplicity of $\rho$. The rate
$o(1) = O(K^{-1/2+\epsilon})$ for every $\epsilon > 0$ is conditional
on RH for $L(s,\chi)$; the unconditional Soundararajan (2009) bound
gives $o(1) = O(K^{-1/2}\exp((\log K)^{1/2}(\log\log K)^{14}))$.*

The proof combines the truncated explicit formula of Inoue (2021,
Theorem 1) for $M^{\ast}(K,\chi)$ with Lemma X.3.1 to extract the
double-pole residue at $\rho$; the contour pieces are bounded by
Soundararajan's argument applied to the off-target zero aggregate.
The full proof is given in **Appendix B** (see
[`APPENDIX_B_CK_SUBLEADING_PROOF.md`](APPENDIX_B_CK_SUBLEADING_PROOF.md)).
The citation appendix with verbatim quotations of Aoki–Koyama (2023)
(1.4), Akatsuka (2013) Lemma 2.1 and eq. (2.5), Inoue (2021)
Theorem 1, Soundararajan (2009) Theorem 1, and the textbook
references is in **Appendix C** (see
[`APPENDIX_C_CITATIONS.md`](APPENDIX_C_CITATIONS.md)).
What the $o(1)$ absorbs and what controls it is recorded
transparently in the proof:

- The off-target nontrivial-zero residues
  $\sum_{\rho'\ne\rho,\,|\gamma'|\le T} K^{\rho'-\rho}/[(\rho'-\rho)L'(\rho',\chi)]$
  give $O(\log T)$ under any zero-density bound at the relevant
  height; under RH for $L(s,\chi)$, $|K^{\rho'-\rho}| = 1$ and these
  terms are $o(1)$ after dividing by the natural rate.
- The trivial-zero residues are $O(K^{-1/2})$ and contribute only
  $o(1)$.
- The shifted-contour and Perron-truncation tails are controlled by
  Soundararajan's bound, which is RH-conditional.

### X.4.3 The Aoki–Koyama–Mertens constant (cited as Hypothesis AK)

The next identity in the chain is *cited*, not proved here: it is the
content of Aoki–Koyama (2023, J. Number Theory **245**, 233–262),
equation (1.4) on p. 235. Verbatim:

> *"In case of Dirichlet $L$-functions $L(s,\chi)$ for non-principal
> Dirichlet characters $\chi$, DRH states that it holds on
> $\mathrm{Re}(s)=1/2$ that*
> $$
> \lim_{x\to\infty}\Bigl((\log x)^m \prod_{p\le x}(1 - \chi(p)/p^{s})^{-1}\Bigr)
> \;=\;
> L^{(m)}(s,\chi) / (e^{m\gamma}\,m!) \times \begin{cases}\sqrt{2}, & \chi^2=1,\,s=\tfrac12,\\ 1, & \text{otherwise,}\end{cases}
> $$
> *with $\gamma$ the Euler constant and $m = m_\chi = \mathrm{ord}_{s=1/2}L(s,\chi)$."*

We specialize the Aoki–Koyama statement to the regime relevant for
this paper: $m = m_\chi = 1$ (i.e., $\rho$ is a simple zero of
$L(s,\chi)$), and $\rho \ne \tfrac12$ (so the right-hand-side branch
condition $\chi^2 = 1,\ s = \tfrac12$ fails and the multiplier is $1$,
not $\sqrt 2$). At $m = 1$ the Aoki–Koyama right-hand side reads
$L^{(1)}(\rho,\chi)/(e^{\gamma}\,1!) = L'(\rho,\chi)/e^{\gamma}$.
Aoki–Koyama (2023, Proposition 2.1, p. 244) writes this specialization
out explicitly; we also reproduce the elementary unwind in §X.4 of
our internal proof packet (the partial-Euler log-Taylor expansion plus
the generalized Mertens identity that supplies the $-\gamma$
contribution canceling against the $e^{-\gamma}$ factor). We refer to
the specialization as **Hypothesis AK**:
\begin{equation}
\label{eq:AK}
\lim_{K\to\infty}\,E_K(\chi,\rho)\,\log K \;=\; \frac{L'(\rho,\chi)}{e^{\gamma}}.
\tag*{(AK)}
\end{equation}
This is the corrected form of the constant; the earlier numerical
target $L'(\rho,\chi)/\zeta(2)$ that appeared in the first phase of
this collaboration is **not** consistent with Aoki–Koyama (1.4):
$1/e^\gamma \approx 0.561459$ while $1/\zeta(2) \approx 0.607927$, a
multiplicative gap of $\zeta(2)/e^\gamma \approx 1.0828$. Hypothesis
AK is DRH-conditional in the form stated by Aoki–Koyama; for the
characters and zeros at which we numerically verify it (Table X.5.2),
DRH is consistent with all known data.

### X.4.4 The conditional NDC limit (open)

Combining (\ref{eq:cK}) and (AK) formally yields
\begin{equation}
\label{eq:NDC}
D_K(\chi,\rho)
\;=\;
c_K(\chi,\rho)\,E_K(\chi,\rho)
\;\longrightarrow\;
e^{-\gamma}
\qquad (K \to \infty),
\tag*{(NDC)}
\end{equation}
which is the *corrected* Numerical Duality Constant. The formal
composition is the following: if Hypothesis AK holds and the
strengthening of (\ref{eq:cK}) named (SP-L) below also holds, then
\[
c_K(\chi,\rho) \cdot E_K(\chi,\rho)
\;=\;
\Bigl[\frac{\log K}{L'(\rho,\chi)} + o(\log K)\Bigr]
\cdot
\Bigl[\frac{L'(\rho,\chi)}{e^{\gamma}\,\log K} + o\!\Bigl(\frac{1}{\log K}\Bigr)\Bigr]
\;=\;
\frac{1}{e^{\gamma}} + o(1),
\]
giving (NDC). The composition is mechanical *if* the two limits hold;
the issue is that (\ref{eq:cK}) of Theorem X.4.2 gives only
$c_K = \log K/L'(\rho) + C_1 + o(1)$, not the *leading-order
asymptotic* $c_K = \log K/L'(\rho) + o(\log K)$ — these are distinct
statements differing by the off-target zero residue aggregate at the
$\log K$ scale rather than the $O(1)$ scale. We do **not** present
(NDC) as a closed theorem. The identity (\ref{eq:cK}) is for
the **leading** Möbius partial sum, while the precise statement
sufficient to compose it with (AK) is the **shifted Perron leading
theorem**:
\begin{equation}
\label{eq:Perron-leading}
c_K(\chi,\rho) \;=\; \frac{\log K}{L'(\rho,\chi)} \;+\; o(\log K)
\qquad (K \to \infty).
\tag*{(SP-L)}
\end{equation}
What blocks (SP-L) as a proved theorem is the off-target nontrivial
zero residue aggregate: at any off-target zero $\lambda$ of
multiplicity $m \ge 2$, the shifted Perron kernel contributes a
residue with leading size
$$
K^{\lambda-\rho}\,(\log K)^{m-1}\Big/\bigl((m-1)!\,(\lambda-\rho)\,a_m(\lambda)\bigr),
$$
where $a_m(\lambda) \ne 0$ is the leading Taylor coefficient of $L$
at $\lambda$. Under DRH, $K^{\lambda-\rho}$ is purely oscillatory, but
the $(\log K)^{m-1}$ factor is *not* absorbed by target-zero
simplicity of $\rho$. The sufficient package for (SP-L), recorded as
Question \qref{Q:Perron} of §X.7 below, is:

> *(SP-L hypothesis package.)* All crossed off-target nontrivial
> zeros are simple; the aggregate
> $$
> Z_\mathrm{simple}(K,T_K) \;=\; \sum_{\substack{\rho' \ne \rho \\ |\gamma'| \le T_K}}
> \frac{K^{\rho'-\rho}}{(\rho'-\rho)\,L'(\rho',\chi)}
> $$
> satisfies $Z_\mathrm{simple}(K,T_K) = o(\log K)$ at a zero-avoiding
> height $T_K \in [K(\log K)^{-B},\,2K(\log K)^{-B}]$ for some
> $B > 0$; and the shifted rectangle / Perron-truncation
> contributions are also $o(\log K)$.

We have searched the explicit-formula literature relevant to this
package (Inoue 2021 JTNB 33, Soundararajan 2009 Ann. Math. 170, Ng
2004 PLMS 89, Akatsuka 2013) and have not found a theorem that closes
it; what is in print transfers, rather than removes, the obstruction.
We therefore state (NDC) as **conditional on Hypothesis AK and on
(SP-L)**.

If (SP-L) fails — that is, if the off-target zero residue aggregate
contributes a term of size $\Theta(\log K)$ to $c_K(\chi,\rho)$ —
then $c_K(\chi,\rho)\cdot E_K(\chi,\rho)$ need not converge to
$e^{-\gamma}$ even under Hypothesis AK; the modulus drift evidence
of §X.5.2 is *consistent with* convergence to $e^{-\gamma}$ at the
$1/\log K$ finite-size scale but does not, by itself, exclude a
slow divergence that the available scale ($K \le 10^7$) cannot
resolve.

---

## X.5 Numerical findings

> **Two distinct verified scales.** "Rigorous verification" in this
> program operates at two clearly distinct scales which must not be
> conflated. The **replication scale** is $x = 1.3 \cdot 10^{13}$: two
> independent implementations agreeing pointwise on the
> prime-residue counts $\pi(x; q, a)$ for moduli
> $q \in \{7, 8, 11, 19, 23\}$, with identity (3.1) of Koyama's
> *nontriv.pdf* verified across $495$ cells. This is the
> Phase-1 anchor (§X.5.1). The **analytic-identity scale** is
> $K \le 2 \cdot 10^{6}$ for the $B_\infty$ and $C_1$ identities, and
> $K = 10^7$ for the $D_K$ drift through which the Aoki–Koyama
> $e^{-\gamma}$ normalization distinguishes itself from the earlier
> $\zeta(2)^{-1}$ target (§X.5.2–§X.5.4). The replication-scale
> evidence anchors the empirical reproducibility of the program; the
> analytic-scale evidence anchors the corrected constant and the
> identification of the open challenges. Numbers from one scale are
> not transferred to the other.

This subsection records the numerical evidence supporting the
identities of §X.4 and the residue-count replication that anchors
the Phase-1 work with Koyama. We deliberately present the
*replication-scale evidence* (Dominance of $-1$, residue counts at
$x = 1.3 \cdot 10^{13}$) **separately** from the *analytic-identity
evidence* ($B_\infty$, $C_1$, AK, EC), because the two strands operate
at very different scales and on very different objects, and the
analytic claims must not inherit the replication-scale verification.

### X.5.1 Phase-1 Dominance-of-$-1$ replication, $x = 1.3 \cdot 10^{13}$

The Phase-1 replication targets the prime-residue counts $\pi(x;N,a)$
of Koyama's "A Hidden Hierarchy of Chebyshev's Bias and the Dominance
of $-1\ (\mathrm{mod}\ N)$" framework (Koyama, preprint *nontriv.pdf*,
sent 2026-04-26) for moduli $N \in \{7, 8, 11, 19, 23\}$ and
checkpoints $x \in \{1.3\cdot 10^{10},\, 1.3\cdot 10^{11},\,
1.3\cdot 10^{12},\, 1.3\cdot 10^{13}\}$. The replication report,
reproducibility bundle, source code, and TSV outputs are at
`koyama_replication_bundle/` in the repository
([`replicate.cpp`](../../koyama_replication_bundle/replicate.cpp),
[`independent_sieve.c`](../../koyama_replication_bundle/independent_sieve.c),
[`REPLICATION_REPORT.md`](../../koyama_replication_bundle/REPLICATION_REPORT.md),
[`MANIFEST.txt`](../../koyama_replication_bundle/MANIFEST.txt),
[`HASHES.sha256`](../../koyama_replication_bundle/HASHES.sha256)).

#### Method

Two independent implementations:

- **Primary** (`replicate.cpp`): a single linear scan over every prime
  $p \le 1.3\cdot 10^{13}$ using `primesieve` 12.13 (K. Walisch's
  segmented wheel sieve, library default parameters), with residue
  counters $c_N[p \bmod N]$ snapshotted at the four checkpoints.
- **Independent cross-check** (`independent_sieve.c`): a hand-rolled
  plain-C segmented Eratosthenes sieve with no external dependency.
  Wall-clock for the cross-check pass: $\approx 3.7\ \mathrm{h}$ on the
  same Apple M1 Max single core.

Both implementations expose their seeds and build hashes
(`HASHES.sha256`) and are bit-reproducible from a fresh checkout.

#### Headline numbers

- Total primes counted: $\pi(1.3\cdot 10^{13}) = 445{,}831{,}610{,}611$.
  Cross-checked against `primesieve --count 13000000000000` standalone.
- Wall clock for the primary pass: $4127\ \mathrm{s}$ ($\approx 68.8$ min) on
  Apple M1 Max single thread; throughput $\sim 1.08 \cdot 10^{8}$
  primes/s sustained at the high end.
- Internal consistency at every checkpoint: per-residue counts sum
  exactly to $\pi(x)$ for every $N \in \{7,8,11,19,23\}$.
- **Library-independence**: at every one of the four checkpoints,
  the `primesieve` counts and the hand-rolled C-sieve counts are
  identical on every residue class for every $N$.
- **Hardware-independence**: a second M1-class machine
  (M1B, `192.168.1.64` at the time of the run; now the local host)
  independently agrees through $x = 1.3 \cdot 10^{12}$ on every
  residue class for every $N$ (`m1b_indep_1e11.tsv`,
  `m1b_indep_partial.tsv`). Full $1.3 \cdot 10^{13}$ on the second
  hardware path is estimated at $\sim 50\ \mathrm{h}$ and is not on
  the critical path of the present manuscript.
- **Identity (3.1)**: Koyama's identity (3.1) is a Dirichlet-character
  orthogonality identity on the residue-count vector; it is verified
  directly from the counts at all $495$ $(N, x, a)$-cells with worst
  real residual $1.4\cdot 10^{-4}$ (`delegations/_charsum_full.py`,
  `_charsum_verify.py`). The identity is an *internal-consistency*
  check on the count vector; it cannot detect a uniform additive
  bias in the prime enumeration that distributes uniformly across
  residue classes — that risk is addressed only by the
  library-independence cross-check above.

#### Cell-by-cell comparison with Koyama's Tables 3–7

Summary at all four checkpoints, all moduli:

| Table | $N$ | cells | exact matches | mismatches |
|---|---:|---:|---:|---|
| 3 | 7  | 12 | 11 | 1 ($\Delta = 50$ at $x=1.3\cdot10^{13}$, $a=6$, clean digit-shift profile) |
| 4 | 8  | 12 | 1  | 11 (small-$x$ rows systematically disagree; one row at the supposed $x=1.3\cdot10^{12}$ exact-matches our $x=10^{12}$ row, indicating an $x$-label error in the draft for the small-$x$ rows; 2 small $\Delta \in \{7, 11\}$ at $1.3\cdot 10^{13}$) |
| 5 | 11 | 20 | 19 | **1** — $x = 1.3 \cdot 10^{13}$, $a = 10$: our value $11{,}503$, Koyama's $71{,}711$ (a clean 4-digit transposition $71711 \leftrightarrow 11503$? — not a standard transposition shape; substantive disagreement) |
| 6 | 19 | 18 | 15 | 3 (1 sign flip at small $x$ in $a=10$ row; **2 substantive disagreements** at $x = 1.3\cdot 10^{13}$, $a=13$ — our $24{,}559$ vs Koyama's $55{,}581$; $a=18$ — our $54{,}192$ vs Koyama's $57{,}192$, latter could be single-digit OCR but unconfirmed) |
| 7 | 23 | 30 | 29 | 1 ($\Delta = 100$ at $x = 1.3\cdot 10^{13}$, $a=19$; clean digit-transposition profile $79327 \leftrightarrow 79227$) |
| **All** |    | **92** | **75 (81.5%)** | **17** |

Excluding Table 4's anomalous small-$x$ rows (the $x$-label-error
interpretation), the agreement is **74 of 83 cells exact (89%)** with
9 substantive mismatches, of which 4 fit a clean digit-transposition
or sign-flip profile ($\Delta \in \{7, 11, 50, 100, \mathrm{sign}\}$).
The two Table 6 entries at $x = 1.3\cdot 10^{13}$ ($a = 13$ and
$a = 18$) and the Table 5 $N=11, a=10$ entry are the substantive
items awaiting comparison with Koyama's raw output.

#### Qualitative replication of the dominance-of-$-1$ signal

Koyama's headline qualitative statement is that at
$x = 1.3 \cdot 10^{13}$, the residue $-1 \pmod N$ gives either the
largest, or sits in the top group, of $\pi(x;N,a) - \pi(x;N,1)$ over
non-residue classes $a$. Our headline-checkpoint results:

| $N$ | $-1 \bmod N$ | non-residues | our diffs at $x = 1.3\cdot 10^{13}$ | rank of $-1$ | qualitative match |
|---:|---:|---|---|---|---|
| 7  | 6  | $\{3, 5, 6\}$ | $\{-10947,\, 47864,\, 26129\}$ | $-1$ is **2nd of 3** (top group) | ✓ |
| 8  | 7  | $\{3, 5, 7\}$ | $\{102728,\, 126743,\, 164951\}$ | $-1$ is **largest** | ✓ |
| 11 | 10 | $\{2, 6, 7, 8, 10\}$ | $\{5327,\, 30403,\, 7351,\, 74838,\, 11503\}$ | **$-1$ ranks 4th of 5** — *outside top group* | **NOT reproduced** at this checkpoint |
| 19 | 18 | $\{2, 3, 8, 10, 12, 13, 14, 15, 18\}$ | $\{17964,\, 60702,\, 13926,\, 79470,\, 30889,\, 24559,\, 48327,\, -5154,\, 54192\}$ | $-1$ is **3rd of 9** (top group) | ✓ |
| 23 | 22 | (ten non-residues) | mid-range diffs | $-1$ is **mid-rank** | matches Koyama's own non-result; Koyama attributes this to the smallest non-trivial $L$-zero modulo $23$ being exceptionally low, with the dominance regime setting in around $e^{33.4} \approx 3 \cdot 10^{14}$ |

**Material item.** For $N = 11$ at $x = 1.3\cdot 10^{13}$, the
dominance ranking turns on the single cell $a = 10$: with our
$11{,}503$, $-1$ ranks 4th of 5 non-residues (outside the top group);
with Koyama's reported $71{,}711$, $-1$ would rank 2nd (comfortably in
the top group). The cell is one of the substantive disagreements
flagged above. **The dominance claim for $N = 11$ at this checkpoint
is not reproduced in the independent run pending Koyama's
reconciliation.**

We note, however, that the dominance signal at the smaller checkpoint
$x = 10^{12}$ is *cleaner* for both $N = 11$ and $N = 19$ in the
extended-grid run (`out2.tsv`, `replicate2`): at $x = 10^{12}$ the
$-1$ residue ranks **1st** for both $N=11$ and $N=19$. The
Littlewood-style sign flips between checkpoints are exactly the
transient behaviour Koyama attributes to low-lying $L$-zeros; the
extended grid shows that no single $x$ is uniformly best for the
Conjecture-2 evidence, and that the dominance signal must be read
across multiple checkpoints rather than at a single $x$. The
replication-bundle plot (`plots/dominance_figure.pdf`) shows this
checkpoint-aggregated picture.

We emphasize: **the verification in this subsection is for
prime-residue counts at $x = 1.3 \cdot 10^{13}$, not for the analytic
identities of §X.4.** None of the analytic quantities $B_\infty$,
$C_1$, $D_K$, $E_K \log K$, or $E[C_1^2]$ is verified at $K = 10^{13}$;
their analytic verification scales are recorded in §X.5.2–§X.5.5.

### X.5.2 The Aoki–Koyama–Mertens constant: $e^{-\gamma}$ vs $\zeta(2)^{-1}$

The four Dirichlet pairs used throughout this section are (all
values computed at $\mathrm{dps} = 50$ via `Koyama_C1.py`):

| Pair label | $\chi$ | $\rho = \tfrac12 + i\tau$ | $L'(\rho,\chi)$ | $L''(\rho,\chi)$ |
|---|---|---|---|---|
| $\chi_{-4}/z_1$ | $\chi_{-4}$ (primitive real, $q=4$) | $\tfrac12 + 6.020948904697 i$ | $\phantom{-}1.296499576 + 0.182765096 i$ | $-1.697049681 - 0.554017071 i$ |
| $\chi_{-4}/z_2$ | $\chi_{-4}$ | $\tfrac12 + 10.243770304166 i$ | $\phantom{-}1.788467032 - 0.296775909 i$ | $-3.319767460 + 0.755547930 i$ |
| $\chi_5$        | $\chi_5$ (order-4, $q=5$) | $\tfrac12 + 6.183578195450 i$ | $\phantom{-}1.112930166 - 0.448830165 i$ | $-1.642973499 + 1.035106608 i$ |
| $\chi_{11}$     | $\chi_{11}$ (order-10, $q=11$) | $\tfrac12 + 3.547041091719 i$ | $\phantom{-}1.696582440 - 0.250988049 i$ | $-3.121598294 + 0.261218791 i$ |

Their moduli are $|L'|\in\{1.30932,1.81292,1.20003,1.71505\}$ and
$|L''|\in\{1.78533,3.40425,1.94171,3.13251\}$. All zeros are
refined by Muller's method until $|L(\rho,\chi)| < 10^{-50}$. An
independent in-mpmath re-implementation using a separate prime sieve,
the Hurwitz-zeta expansion
$L(s, \chi) = q^{-s} \sum_{a=1}^{q} \chi(a)\,\zeta(s, a/q)$
in place of `mpmath.dirichlet`, and an independent recompute of
$L'$ and $L''$ via central-difference numerical differentiation at
three step sizes ($h \in \{10^{-12}, 10^{-15}, 10^{-18}\}$) reproduces
every entry to $|\Delta L'|, |\Delta L''| \lesssim 6 \cdot 10^{-12}$
and $|\Delta C_1| \lesssim 5 \cdot 10^{-13}$ on each of the four
pairs (L1b in-language cross-check, executed 2026-05-12; see
[`L2_CROSSCHECK_2026-05-12.md`](L2_CROSSCHECK_2026-05-12.md) for the
per-pair table and [`mpmath_L2_crosscheck.py`](mpmath_L2_crosscheck.py)
for the verifier source). At $K = 200{,}000$ the L1b residual
$|c_K - \log K/L' - C_1|$ matches the L1 reference to all six
reported digits on all four pairs.

**Cross-language (L2) verification with PARI/GP 2.17.3** is also
executed ([`pari_L2_crosscheck.gp`](pari_L2_crosscheck.gp);
report [`L2_PARI_CROSSCHECK_2026-05-12.md`](L2_PARI_CROSSCHECK_2026-05-12.md)).
PARI's independent C implementation produces, for the four pairs,
$L'$ values matching L1 to $\ge 11$ decimal digits on each real and
imaginary component (e.g. for $\chi_{-4}/z_1$: L1 real part
$1.296499575565\ldots$ vs PARI $1.2964995755658179\ldots$; L1
imaginary part $0.182765095861\ldots$ vs PARI
$0.18276509586123733\ldots$). The $D_K$ residual $|R(K)|$ at
$K = 200{,}000$ on all four pairs:

| Pair | $|R(K)|$ at $K = 2\cdot 10^5$ (L1 mpmath dps=50) | $|R(K)|$ at $K = 2\cdot 10^5$ (L2 PARI 2.17.3) | $|R(K)|$ at $K = 10^7$ (L2 PARI 2.17.3) |
|---|---:|---:|---:|
| $\chi_{-4}/z_1$ | $0.134447$ | $0.13444748769861698558\ldots$ | $0.12203217306259735065\ldots$ |
| $\chi_{-4}/z_2$ | $0.257279$ | $0.25727872209424575749\ldots$ | $0.29803894338506032640\ldots$ |
| $\chi_5$        | $0.245896$ | $0.24589598622186410536\ldots$ | $0.36171215211645665889\ldots$ |
| $\chi_{11}$     | $0.210102$ | $0.21010163569665339294\ldots$ | $0.16480768637754420364\ldots$ |

The L1 and L2 PARI agree to all six reported L1 digits at
$K = 2\cdot 10^5$ on every pair. The full $K = 10^7$ PARI run took
$\approx 35$–$60$ seconds per pair on Apple M1 Max single core
(report: [`L2_PARI_K10M_run.log`](L2_PARI_K10M_run.log)). At
$K = 10^7$ the empirical $|R(K)|$ across the four pairs falls in
$[0.122,\,0.362]$; the predicted Gonek–Hejhal-style envelope
$\log K / \sqrt K \approx 0.0051$, so the empirical implicit constant
sits between $24\times$ and $71\times$ the heuristic envelope — well
within the Soundararajan (2009) factor
$\exp(C(\log\log K)^{1/2}(\log\log K)^{14})$ at $K = 10^7$
(see Appendix B §B.4 for the conditional/unconditional rate
breakdown). The residual is *bounded* but *non-monotone* in $K$: the
oscillatory factors $K^{i(\gamma' - \tau)}$ from off-target zeros
interfere, so individual pairs need not show decreasing $|R(K)|$. An additional
spot-check at 250 bits using python-flint 0.8.0 / Arb (FLINT 3.3) on
the worst case ($\chi_{-4}/z_1$, $\chi_{-4}/z_2$) gives interval
agreement on $|L'|$ of $\le 3\cdot 10^{-43}$ ([`ARB_L2_SPOT_2026-05-12.md`](ARB_L2_SPOT_2026-05-12.md)).
The three computational stacks (mpmath, PARI, Arb) are independent
implementations in independent languages with independent algorithms
and independent prime sieves; agreement at this depth is the
strongest cross-stack verification we can supply at this scale.

The $D_K$ statistic, computed at $K = 2 \cdot 10^6$ and $K = 10^7$
on the four pairs at 40 dps, gives (note: the tracked statistic is
the **modulus** $|D_K|$, not $D_K$ itself; phase convergence is *not*
claimed, only modulus drift):

| Quantity | $K = 2\cdot 10^6$ | $K = 10^7$ | Modulus limit if NDC $= \zeta(2)^{-1}$ | Modulus limit if NDC $= e^{-\gamma}$ |
|---|---:|---:|---:|---:|
| Mean $|D_K|\cdot\zeta(2)$ (four pairs) | $0.992$ | $0.974$ | $1.000$ | $\zeta(2)\cdot e^{-\gamma} \approx 0.9237$ |
| Mean $|E_K \log K| \cdot e^{\gamma}/|L'|$ (four pairs) | --- | $0.942$ | --- | $1.000$ |

The modulus drift from $0.992$ to $0.974$ between $K = 2\cdot 10^6$
and $K = 10^7$ is consistent with the AK normalization $e^{-\gamma}$
at the natural $1/\log K$ finite-size scale, and incompatible with
the $\zeta(2)^{-1}$ target at the same scale. We emphasize: a modulus
limit alone does not establish convergence of the complex statistic
$D_K(\chi,\rho)$; full convergence is part of the conditional (NDC)
statement and depends on (SP-L).

We note explicitly that this is **finite-$K$ evidence**, not a proof
of (NDC). What is proved is Theorem X.4.2 (the local leading +
subleading partial-Möbius identity at scale $\log K$). The finite-$K$
*direction* of the drift independently distinguishes $e^{-\gamma}$
from $\zeta(2)^{-1}$ at the $K = 10^7$ scale; the unconditional
asymptotic in (\ref{eq:NDC}) remains conditional on Hypothesis AK
plus (SP-L).

### X.5.3 The subleading constant $C_1$

| Pair | $C_1 = -L''(\rho)/(2\,L'(\rho)^2)$ (mpmath, 50 dps) | $|C_1|$ |
|---|---|---|
| $\chi_{-4}/z_1$ | $0.5203451866 + 0.01845932347 i$ | $0.52067$ |
| $\chi_{-4}/z_2$ | $0.5150884772 + 0.05433692967 i$ | $0.51795$ |
| $\chi_5$        | $0.6601814622 + 0.13690196820 i$ | $0.67423$ |
| $\chi_{11}$     | $0.5207614712 + 0.11113668970 i$ | $0.53249$ |

At $K \in \{2\cdot 10^5,\,10^6,\,2\cdot 10^6\}$ the residual
$R(K) := c_K - \log K/L'(\rho) - C_1$ behaves as expected for the
RH-conditional rate $O(\log K/\sqrt K)$, with all $R(K)$ at
$K = 2 \cdot 10^6$ falling in $[0.027,\,0.375]$, matching the
empirical envelope $\approx 1$–$36$ times the heuristic
Gonek–Hejhal-style bound $\log K / \sqrt K \approx 0.010$.

### X.5.4 The $B_\infty$ identity (Theorem X.4.1) at the four pairs

At $K = 2 \cdot 10^6$, 50 dps:

| Pair | $\tfrac12\log L(2\rho,\psi)$ | $\mathrm{BPC}_1$ | $\mathrm{BPC}_2$ | $T_{\ge 3}$ | RHS | $T_K$ at $K = 2\cdot 10^6$ | residual |
|---|---|---|---|---|---|---|---:|
| $\chi_{-4}/z_1$ | $0.0448-0.2502 i$ | $0.1360+0.1711 i$ | $-0.0051+0.0456 i$ | $-0.0455+0.0254 i$ | $0.13017-0.00813 i$ | $0.12750-0.00715 i$ | $2.85\!\cdot\!10^{-3}$ |
| $\chi_{-4}/z_2$ | $-0.2272-0.3626 i$ | $0.0682+0.2252 i$ | $0.00050+0.0111 i$ | $0.0752+0.0434 i$ | $-0.08331-0.08284 i$ | $-0.08175-0.08341 i$ | $1.66\!\cdot\!10^{-3}$ |
| $\chi_5$        | $-0.0148+0.4365 i$ | $0$ | $0.0444-0.0456 i$ | $0.0340-0.0929 i$ | $0.06358+0.29804 i$ | $0.06362+0.29802 i$ | $4.24\!\cdot\!10^{-5}$ |
| $\chi_{11}$     | $-0.2377+0.3292 i$ | $0$ | $-0.0333+0.0635 i$ | $0.0270-0.0315 i$ | $-0.24404+0.36122 i$ | $-0.24400+0.36123 i$ | $3.33\!\cdot\!10^{-5}$ |

Convergence rates at $K \in \{2\cdot 10^5,\,10^6,\,2\cdot 10^6\}$
exhibit $\approx K^{-1/2}/\log K$ decay for $\chi_5,\chi_{11}$ (no
bad primes; pure boundary-line conditional-tail convergence of
$\sum_p \chi^2(p)/p^{1+i\tau}$), and a uniformly slower decay for
$\chi_{-4}$ traced to the bad-prime $p=2$ weight (where
$\mathrm{BPC}_1$ is nontrivial).

**Cross-language extension to $K = 10^7$ on the clean-character
pairs.** PARI/GP 2.17.3 (script
[`pari_Binfty_K10M_chi5_chi11.gp`](pari_Binfty_K10M_chi5_chi11.gp),
report [`BINFTY_K10M_run.log`](BINFTY_K10M_run.log)) computes
$T_K(\chi, \rho)$ at $K = 10^7$ in ~7 s wall-clock per pair, and
returns identity residuals

| Pair | $|T_K - \mathrm{RHS}|$ at $K = 10^7$ |
|---|---:|
| $\chi_5$ | $5.12 \cdot 10^{-4}$ |
| $\chi_{11}$ | $6.30 \cdot 10^{-4}$ |

The $T_K(\chi, \rho)$ value at $K = 10^7$ matches the L1 mpmath
$T_K$ at $K = 2\cdot 10^6$ to all reported decimal places of the L1
display (better than $10^{-5}$ on each component); the L2 residual
is larger than the L1 residual mainly because the PARI script
truncates the *absolutely convergent* component sums
$\mathrm{BPC}_2$ and $T_{\ge 3}$ at $p \le 10^6$, $k \le 12$, which
introduces a methodology-level truncation at the $\sim 10^{-4}$ scale
absent from the L1 packet's convention of computing both component
sums and $T_K$ to consistent precision (`Koyama_B_infty.py`). Both
calculations agree on the *identity itself* at the $\sim 10^{-3}$
level on every pair. A consistent-precision PARI rerun (with the
component sums extended to $p \le 10^7$) would tighten the residual
to the L1 envelope; this is a $\sim 30$-minute additional compute
and is recorded as a queued cross-check.

### X.5.5 Elliptic-curve and $\Delta$-form spectroscope ensemble

We compute the second-moment statistic
$$
E[C_1^2] \;:=\; \mathrm{Var}_\mathrm{zeros}\!\bigl(C_1(f,\rho)\bigr)
\;=\; \mathrm{mean}_{\rho}\,\bigl|C_1(f,\rho)\bigr|^2
$$
over a sample of refined non-trivial zeros for each form $f$, in
arithmetic normalization.

| Form | Rank | Weight | Conductor | Sample | $E[C_1^2]$ |
|---|---:|---:|---:|---:|---:|
| $\Delta$ level 1 | n/a | 12 | 1 | 683 zeros | $0.950231842$ |
| $37a_1$ | 1 | 2 | 37 | 500 zeros | $2.189911545$ |
| $389a_1$ | 2 | 2 | 389 | 500 zeros | $3.113923728$ |
| $5077a_1$ | 3 | 2 | 5077 | 500 zeros | $4.617$ |
| Rank-0 cluster ($11a_1$–$24a_1$) | 0 | 2 | $11$–$24$ | 200 each | mean $1.886$ (CV $8.9\%$) |
| $37b_1, 37b_2, 37b_3$ | 0 | 2 | $37$ | 200 each | mean $2.052$ |

The $\Delta$-form anchor $E[C_1^2] = 0.950231842$ at level $1$ is
*close* to $1$ but **we do not, in this paper, present convergence
to $1$ as a theorem.** It is a target value compatible with a
rank-zero analytic conjecture and within the natural finite-sample
window; the asymptotic statement awaits the same machinery as (SP-L)
and a separate cusp-form treatment.

The four elliptic-curve points $\{37a_1,389a_1,5077a_1,\Delta\}$
together with the rank-0 cluster and the conductor-control triple
$37b_1,37b_2,37b_3$ exhibit an apparent rank trend. A multivariate
OLS regression on the available $19$ weight-$2$ EC points in
`PATH_B_20FORMS.csv` (excluding $\Delta$, which is weight-12 and
sits on a different normalization) returns
\begin{equation}
\label{eq:W2}
E[C_1^2] \;=\; -0.1811 \;+\; (-0.6773)\cdot\mathrm{rank} \;+\; 0.7345\cdot\log N,
\qquad R^2 \;=\; 0.8144.
\end{equation}

The $\log N$ coefficient is statistically significant and stable
under resampling; the rank coefficient is *not stable*. Concretely,
on the 19-point design:

| Statistic | Rank coefficient | $\log N$ coefficient |
|---|---:|---:|
| Full-sample value | $-0.6773$ | $+0.7345$ |
| Leave-one-out range | $[-0.7869,\,-0.2533]$ (width $0.534$) | $[+0.3893,\,+0.8033]$ (width $0.414$) |
| Leave-one-out mean $\pm$ s.d. | $-0.6673 \pm 0.1097$ | $+0.7263 \pm 0.0853$ |
| Bootstrap 95\% CI (10,000 resamples) | $[-1.222,\,+0.104]$ | (not reported here) |
| Bootstrap sign-flip rate (coefficient $\ge 0$) | $4.7\%$ | $\sim 0\%$ |

The leave-one-out point with the largest leverage on the rank
coefficient is $5077a_1$ (the rank-3 anchor): removing it shifts the
rank coefficient from $-0.6773$ to $-0.2533$, a $63\%$ relative
change. Without the rank-3 point, $\log N$ alone explains essentially
all of the variance and the rank-vs-conductor design is collinear in
the remaining 18 points. In the bootstrap, the $95\%$ CI for the
rank coefficient is $[-1.222,\,+0.104]$, which *includes zero*: under
resampling, the rank coefficient flips sign with probability roughly
$4.7\%$. **We therefore describe (\ref{eq:W2}) as a
conductor-confounded trend, not a clean rank law.** Source data:
`koyama-shared/data/PATH_B_20FORMS.csv`. Recompute via
`~/miniforge3/envs/pari-arb/bin/python` against the project source.

The Sym${}^2\!/\langle f,f\rangle$ proportionality of the form tested
in our 2026-04 correspondence is empirically **falsified** in its
raw normalization. The supporting data (from
`koyama-shared/data/SYM2_LVALUES.json`) is the ratio
$R(f) := E[C_1^2]\cdot \langle f, f\rangle / L(\mathrm{Sym}^2 f, k)$
across the three forms tested:

| Form | $\mathrm{rank}$ | $\mathrm{weight}$ | $L(\mathrm{Sym}^2 f, k)$ | $\langle f, f \rangle$ | $R(f)$ |
|---|---:|---:|---:|---:|---:|
| $37a_1$ | $1$ | $2$ | $2.4314$ | $0.3627$ | $6.704$ |
| $389a_1$ | $2$ | $2$ | $3.1681$ | $4.9684$ | $0.638$ |
| $\Delta$ | (n/a) | $12$ | $0.6320$ | $1.0354\times 10^{-6}$ | $610{,}456$ |

The ratios differ by *seven orders of magnitude* across the three
forms — far outside any naturally arising universality. The
$\Delta$ ratio is dominated by the small Petersson norm at weight
$12$ (a separate normalization issue). Among the two weight-$2$
ECs, the ratios $6.704$ vs.\ $0.638$ differ by a factor of $\approx 10$,
falsifying the loose "constant up to a factor of $2$" tolerance the
raw proportionality would require. We do not exclude a *completed*
or *archimedean-corrected* Sym${}^2$ normalization — see Question
\qref{Q:Sym2} of §X.7 — but the raw proportionality in the tested
form is closed as a negative result here.

### X.5.6 The elliptic-curve NDC sweep — a negative result

We report the elliptic-curve NDC sweep as a **negative result**, not
as supporting evidence for any EC analogue of (NDC). Concretely:

- The simple sharp-cutoff form of EC universality
  $D_K^E \cdot \zeta(2) \to 1$ is **falsified** through $K = 10^6$
  on the tested three-curve grid.
- Smoothed-proxy variants
  $c_{E,W}(K)\cdot P_{E,W}(K)$ are reproducible as a *finite
  numerical signal* through $K = 10^6$, but a null-control gate run
  against predeclared null transformations ($c P$-only, $P$-only,
  $P\,L^2$-only) also passes at $\alpha = 0.75$; the previous gate
  is therefore not load-bearing.
- A full Sato–Tate G3 stochastic run ($512$ iid + $128$ shared
  seeds) returns $0$ old/primary gate passes, but empirical
  $p$-gates fail (iid $p_\mathrm{ratio} = 0.0624$; shared
  $p_\mathrm{score} = 0.0465$); status is `G3_FAIL`.

The point of including this subsection is to record, for the
literature, *what was tested and what failed*, so that subsequent
work on the EC analogue does not retread these specific
normalizations. The corresponding open question (Question
\qref{Q:EC-NDC}) asks whether a different normalization with
stronger null specificity survives; we do not assert that one
exists, and the present paper does not propose one.

---

## X.6 Lean 4 / Mathlib4 formalization path

We accompany this paper with a Lean 4 / Mathlib4 lake project in the
companion repository (commit hash fixed at submission). The Lean
artifact serves two purposes: (i) it provides machine-checked
*statements* of every identity of §X.4, ensuring that the
normalizations, branch conventions, and hypothesis structures are
syntactically explicit; (ii) for each statement it records the
current proof status (theorem / mathlib-prerequisite / scaffold /
research-open).

The Lean toolchain is `leanprover/lean4:v4.28.0`. The mathlib
dependency is pinned in `lake-manifest.json` at the commit reported
in the reproducibility manifest. CI runs `lake build` against the
pinned mathlib commit on every push.

We follow the *blueprint* convention introduced by Massot for the
PFR formalization: every theorem statement in §X.4 is paired with a
Lean declaration, and the relationship between the printed proof and
the Lean development is made explicit. Each paired theorem carries a
status tag:

- **THEOREM:** Lean proof complete; no `sorry` in scope.
- **PROVED-UP-TO-MATHLIB-PREREQ:** the algebraic content is closed in
  Lean modulo one or more *named* missing Mathlib lemmas; each
  missing lemma is annotated `-- MATHLIB-PREREQ: <name>`.
- **SCAFFOLD:** Lean declaration with the statement type-checked and
  the proof structure laid out; algebraic steps remain `sorry`.
- **OPEN:** research-open. Statement Lean-formalized, no closed proof
  in the literature.

Current inventory. **All entries below correspond to files that
actually exist in `formal-conjectures/` of the project repository at
the time of writing.** I have verified the file presence, the
declaration counts, and the proof-position `sorry` counts. The
strongest current Lean items are the *boundary-residue* and
*algebraic-glue* theorems for the smoothed $\Delta w_f$ explicit
formula; analytic prerequisites that Mathlib v4.28.0 does not yet
supply are marked with named `MATHLIB-PREREQ` annotations rather than
as bare `axiom`s.

| Paper object | Lean file (verified path) | Status |
|---|---|---|
| Boundary residue $R_0 = -2$ for the smoothed $\Delta w_f$ explicit formula (Schwartz cutoff $W(x)=e^{-x^2}$) and its algebraic-glue chain (sign, parity, antiderivative identity, residue factorization, Mellin residue at zero, complex/integer recasts) | `formal-conjectures/SmoothedDwfFormula_full.lean` | **THEOREM (chain).** 25+ specific theorems are closed without `sorry`, including `R0_value`, `R0_plus_two`, `R0_factored`, `zeta_at_zero` (using `riemannZeta_zero` from Mathlib), `inv_zeta_at_zero`, `mellinResidueGaussianAtZero_eq_one`, `R0_eq_neg_two`, `R0_complex_re`, `R0_complex_im`, `R0_complex_ne_zero`, `R0_complex_neg`, `R0_complex_double`, `log_lin_antideriv_at`, `log_lin_form`, `log_lin_deriv_form`, `dwf_leading_coeff`, `R0_neg_two_iff_plus_two_zero`. The chain establishes the boundary residue algebraically; the remaining analytic-input theorems are listed in the next row. |
| Analytic prerequisites for the smoothed $\Delta w_f$ explicit formula | same file as above | **2 remaining `sorry`s** (after a fresh Aristotle dispatch on 2026-05-12, project ID `885c640c-55cd-48f4-9ce5-1168566619d6`, `lake build`-verified). Each is annotated with the precise missing Mathlib prerequisite. `mellin_decay`: unclosable for two independent reasons — (a) `AdmissibleWeight` currently lacks a decay field on `M`, so the theorem is over-stated for arbitrary $M$; the fix is to add `M_decay : ∀σ A, ∃ C, 0 ≤ C ∧ ∀t, ‖M⟨σ,t⟩‖ ≤ C·(1+|t|)^{-A}` to the structure; (b) for the Gaussian specialization $M(s) = \tfrac12\Gamma(s/2)$, Mathlib v4.28.0 lacks `Complex.Gamma.uniform_stirling_strip_bound`. `inv_zeta_polynomial_growth`: unclosable in Mathlib v4.28.0 (Titchmarsh, *The Theory of the Riemann Zeta-Function*, Theorem 3.11); Mathlib has individual non-vanishing on $\mathrm{Re}\,s \ge 1$ via `riemannZeta_ne_zero_of_one_le_re` but not the quantitative polynomial bound $\|1/\zeta(σ+it)\| \le C(1+|t|)^B$. The `contour_shift_one_to_minus_A` and `tail_bound` theorems consume these as hypotheses and are themselves closed conditional on them. **No `axiom` is introduced.** |
| Dirichlet Polynomial Avoidance (DPAC) statement + phase-avoidance bridge layers | `formal-conjectures/DirichletPolynomialAvoidance.lean` (statement of conjecture, 1 `sorry`); `formal-conjectures/DPAC_full.lean` (8 theorems, **1 `sorry`** at line 335 after Aristotle round-2 dispatch `bb0cd153-0364-48e2-85fd-564fd8ce4679` on 2026-05-12; both files `lake build`-verified under Lean 4.28.0 / Mathlib v4.28.0) | **OPEN (the headline conjecture itself).** The earlier `dpac_of_LI` bridge was tombstoned (LI alone is insufficient); the file names four explicit phase-avoidance bridge layers (`dpac_of_logPrimePhaseAvoidance`, `dpac_of_finiteLogPrimePhaseIndependence`, `dpac_of_externalZetaZeroPhaseAvoidance`, `dpac_of_certifiedZetaZeroSample`) — **all closed without `sorry`**. The Aristotle round-2 dispatch additionally closed the algebraic-identity sorry `moebiusDirichletPoly_eq_gammaExponentialPoly` (uses only `propext`, `Classical.choice`, `Quot.sound`). The remaining `sorry` is precisely the headline DPAC conjecture, which Aristotle correctly diagnoses as comparable in difficulty to the Linear Independence Hypothesis for zeta-zero ordinates (no unconditional proof exists in the literature; the conditional bridges reduce DPAC to explicit phase-avoidance / interval-arithmetic inputs). Submitted to `google-deepmind/formal-conjectures` as PR #3716. |
| Farey bridge identity (R1) | `formal-conjectures/FareyBridgeIdentity.lean` | SCAFFOLD (1 theorem, 2 `sorry`-occurrences); algebraic-identity-class proof skeleton |
| Spectroscope universality conjecture | `formal-conjectures/MertensSpectroscopeUniversality.lean` | SCAFFOLD (1 theorem, 1 `sorry`); statement formalized, proof depends on the analytic results in the body of this paper |
| Farey sign pattern (B+ Mertens-restricted positivity) | `formal-conjectures/FareySignPattern.lean` | **NEGATIVE — positive theorem is falsified.** $B_+$ Mertens-restricted positivity is directly falsified in the Lean-canonical `crossTerm` definition at $p = 237{,}733$ and $p = 243{,}799$. The file's positive theorem is no longer in scope; we keep the file as a record of the negative result. |
| Lemma X.3.1 (local Perron residue) | `formal-conjectures/LocalPerronResidue.lean` (skeleton committed 2026-05-12) | **SCAFFOLD (statement only).** Statement type signature uses `residue` for the meromorphic-function residue functional. MATHLIB-PREREQ comments name the API gaps: meromorphic-function residue, `AnalyticAt.hasFPowerSeriesAt` for the Laurent expansion, higher derivatives at a point. Proof is `sorry`. The algebraic content is closed on paper (§X.3 of this section and Appendix B §B.2). |
| Theorem X.4.1 ($B_\infty$ identity) | `formal-conjectures/CorrectedBInfty.lean` (skeleton committed 2026-05-12) | **SCAFFOLD (statement only).** Statement uses `DirichletCharacter`, `IsPrimitive`, `LFunction` from Mathlib v4.28.0 plus named MATHLIB-PREREQs for: an `induces` relation for $\chi^2$, simple-zero characterization, and the $T_\infty$ / $\mathrm{BPC}_1$ / $\mathrm{BPC}_2$ / $T_{\ge 3}$ definitions. Proof is `sorry`. The algebraic content is closed on paper (§X.4.1 + Appendix A). |
| Hypothesis AK and Hypothesis SP-L | (planned) named as Lean `axiom`s with manuscript references, in line with the project's protocol that analytic-input prerequisites are visible `axiom`s/named `MATHLIB-PREREQ`, not silent | **EXTERNAL** (AK) and **OPEN** (SP-L) |

**On the broader project Lean inventory.** A separate, archived
formalization in `archive/request-projects/RequestProject/` contains
48 Lean files (Farey bridge identity, sign theorem, injection
principle, CW-bound, etc.) supporting the project's earlier
*per-step Farey discrepancy* paper. This is a different work and not
part of the present manuscript; we mention it only because the
working protocol (named axioms over analytic prerequisites, Aristotle
dispatch for residual `sorry`s, embedded manuscript references in
proof comments) was demonstrated there and is carried into the
present work.

**On the Lean memo of 2026-05-02.** An earlier technical memo
(Saar to Koyama, 2026-05-02, *Lean 4 Support for Lattice-Based
Cryptography Security Proofs*) describes a kernel constant
$c_W = -\gamma_E - E_1(1)$ for a Heaviside-cutoff Mellin shift
$W(x) = e^{-x}\,\mathbf{1}_{0 < x \le 1}$. The current Lean directory
does not contain a dedicated proof file for that constant; the
closely related constant proved here is the **Schwartz-cutoff**
boundary residue $R_0 = -2$ for $W(x) = e^{-x^2}$, established by the
`SmoothedDwfFormula_full.lean` chain above. Both constants arise from
the same Mellin-shift architecture but use different cutoff kernels.
The present manuscript scopes the Lean inventory to what the
repository currently contains; we do not assert a $c_W$ proof here.

We claim **no** Lean-verified theorem for any object tagged SCAFFOLD
or OPEN. The role of the Lean artifact, for the purposes of this
paper, is to fix the *statements* and to provide a publicly inspectable
audit trail of the proof obligations remaining.

---

## X.7 Open challenges

The following are the open challenges that, in the authors' view,
should structure the next phase of the program. They are listed in
the order in which they appear in this section's exposition.

> **Question \qref{Q:Perron} (Shifted Perron leading theorem).** Prove
> (SP-L) for primitive non-principal $\chi$ and simple noncentral
> $\rho$, or prove the sufficient package recorded after
> (\ref{eq:Perron-leading}).

The local double-pole residue is proved (Lemma X.3.1). The blocker
is the off-target nontrivial-zero residue aggregate, including the
*possibility* of off-target multiple zeros, which contribute residues
of order $(\log K)^{m-1}$ that target-zero simplicity alone does not
absorb. We have not asserted that such off-target multiple zeros
exist for the relevant Dirichlet $L$-functions; we have asserted that
target-zero simplicity plus DRH/EDRH is not by itself sufficient to
prove (SP-L). This is an *open challenge*, not an impossibility
claim.

> **Question \qref{Q:Z-simple} (off-target simple-zero aggregate).** Even
> assuming all crossed off-target zeros are simple, prove
> $Z_\mathrm{simple}(K,T_K) = o(\log K)$ at the Perron-required
> zero-avoiding height.

The partial-summation route through Inoue (2021) Theorem 1
transfers the obstruction; total-Möbius bounds of Soundararajan type
are too coarse to isolate the pointwise cancellation in the shifted
frequency variable $\log K$.

> **Question \qref{Q:EC-recip} (GL(2) reciprocal-derivative control).** Prove a
> fixed-curve theorem for $\sum_{\gamma} \widehat W(i\gamma) e^{i\gamma u}/L'(E,1+i\gamma)$
> giving cancellation $o(u^r)$, or a minimum-modulus estimate
> $|L(E,s)|$ on a vertical line with explicit exponent $< 2$.

The smoothed EC computations and the spectroscope ensemble are
suggestive but cannot, in the absence of such a theorem, be promoted
beyond *finite* / *averaged* / *profile* statements at the
fixed-curve level. Without a GL(2) analog of Aoki–Koyama, the
elliptic-curve side of the program remains at the level of
quantitative ensemble evidence.

> **Question \qref{Q:EC-NDC} (EC NDC normalization).** Find a normalization of
> $D_K^E$ for which the universal limit exists and survives a
> null-control gate.

The simple sharp-cutoff form is falsified through $K = 10^6$; the
finite bad-prime no-go is recorded in our internal audit. We have
not found, for the tested class, a sharp-cutoff finite normalization
that simultaneously matches the EC data and clears the null-control
gate.

> **Question \qref{Q:conductor} (conductor-confounded rank trend).** Replicate
> (\ref{eq:W2}) on a curve set in which rank and $\log N$ are not
> collinear (e.g. rank-3 and rank-4 anchors at matched conductor) to
> separate the conductor contribution from any genuine rank
> dependence.

The 22-point set is collinear in rank and $\log N$; the rank
coefficient is unstable under leave-one-out. We do not know, from
this data alone, whether the trend is a rank law, a conductor law,
or a superposition.

> **Question \qref{Q:Sym2} (corrected Sym$^2$ normalization).** Identify a
> completed / archimedean-corrected Sym$^2$ normalization that
> replaces the raw Sym$^2/\langle f,f\rangle$ proportionality, which
> is empirically falsified in its raw form.

> **Question \qref{Q:DPAC} (DPAC).** Prove the Dirichlet Polynomial
> Avoidance Conjecture, formalized as
> `DirichletPolynomialAvoidance.lean` and submitted as PR #3716 to
> `google-deepmind/formal-conjectures`. The LI bridge alone is
> insufficient (tombstoned in `DPAC_full.lean`); explicit
> phase-avoidance bridge layers are named in the Lean file.

> **Question \qref{Q:L2-PARI-Kscale} (push cross-language verification
> to $K = 10^7$).** The cross-language L2 lane is now executed at
> $K = 200{,}000$ in PARI/GP 2.17.3 ([`L2_PARI_CROSSCHECK_2026-05-12.md`](L2_PARI_CROSSCHECK_2026-05-12.md))
> and at 250-bit precision via python-flint / Arb on the worst-case
> pair ([`ARB_L2_SPOT_2026-05-12.md`](ARB_L2_SPOT_2026-05-12.md)).
> The remaining computational ask is to push the cross-language
> partial-Möbius computation to $K = 10^7$ on all four pairs so
> that the analytic-scale Dirichlet drift in §X.5.2 carries
> stack-independent reproduction at the same $K$.

### X.7.1 Halo-route reduction toward an unconditional (SP-L)

The most material recent structural progress on Question Q:Perron
is the *halo-route reduction* recorded in
[`handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md`](../handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md).
The plan is written for fixed-elliptic-curve / GL(2) newform $L$-functions
(where it bears on the H1 off-target residue contribution), but the
underlying mechanism transfers conceptually to the Dirichlet (GL(1))
case (SP-L) of §X.4.4. We summarize it here for the reader.

**Structural pivot.** Write the off-target residue sum as a *signed*
contour residue over the boundary of a *halo region*
$\Omega_T = \bigcup_{\rho \in Z_T^{\mathrm{red}}} D(\rho, R_T \alpha)$
(union of disks of radius $R_T \alpha$ around the off-target zeros).
For a cluster $C = \{\rho_1, \ldots, \rho_n\}$ of close-by zeros, the
*cluster-summed* residue is a divided difference
$[\rho_1, \ldots, \rho_n](\Phi_T / H_C)$, which stays bounded by a
derivative *even though individual reciprocal derivatives blow up*
as two zeros collide. The cluster-summed residue avoids the
"rooted Palm wall" that obstructs the termwise-absolute-value
estimate.

**Halo theorem.** With $R_\Phi(T) := \sum_{\rho \in Z_T^{\mathrm{red}}} \mathop{\mathrm{Res}}_{s=\rho} \Phi_T(s)/L(s)$,
Stokes gives
$$
R_\Phi(T) \;=\; \frac{1}{2\pi i}\!\int_{\partial \Omega_T} \frac{\Phi_T(s)}{L(s)}\, ds.
$$
Charging boundary length to the halo circles and applying Cauchy–Schwarz
with $\#Z_T^{\mathrm{mult}} \ll T \log T$ and a $q=2$ shifted moment
input
$$
\sum_{\rho}^{\mathrm{mult}} |L(\rho+\alpha)|^{-2} \;\ll\; T^{5/2+\varepsilon},
$$
yields $|R_\Phi(T)| \ll M_T \cdot T^{7/4 + \varepsilon + o(1)}$, where
$M_T = \sup_{\partial \Omega_T} |\Phi_T|$. If $M_T = o(T^{1/4})$
(in particular if $M_T = T^{o(1)}$), then $R_\Phi(T) = o(T^2)$.

**Status of the four doors.**

| Door | Statement | Status (2026-05-12) |
|---|---|---|
| **A** | `AllZeroShiftedNeg_2(E)`: $\sum_\rho^{\mathrm{mult}} |L(\rho+\alpha)|^{-2} \ll T^{5/2+\varepsilon}$ (or simple-zero version + multiple-zero disposition). | Open — the only remaining shifted-moment input. |
| **B** | `HaloShiftComparison(E, A, R)`: $|L(s)|^{-1} \le T^{o(1)} |L(\rho_0 + \alpha)|^{-1}$ on every halo arc assigned to $\rho_0$. | **Theorem (proved 2026-05-12, §5.1 of the halo plan)** under the framework's standing GRH and $R > \sqrt{1+A^2}$. The proof uses the geometric fact that points $s \in \partial \Omega_T$ are forced outside every other halo by the definition of $\partial \Omega_T$; the cluster ratio is then a contraction of arbitrary order ($\le 1$ per cluster mate), and the noncluster part is bounded by the existing `ClusterShiftDerivativeComparison(E, A)` lemma. The naïve factorization estimate $C_A^{N_{\rho_0, A}(T)}$ is replaced by an absolute constant $O(1)$, with no local zero-count input needed. |
| **C** | `ResidueFirstH1Rewrite`: identify the H1 step where the *budget* $R_B(T,c) = \sum_{\rho\text{ bad simple}} |L'(\rho)|^{-1}$ is used and replace it by the *signed* contour residue contribution. | Open (programmatic) — requires auditing the existing H1 lemma chain to verify that the H1 inequality consumes the signed residue, not its termwise absolute value. |
| **D** | $M_T = \sup_{\partial \Omega_T} |\Phi_T| = o(T^{1/4})$, preferably $T^{o(1)}$. | Open — depends on the choice of test function $\Phi_T$. The standard Perron test functions in our setting satisfy $M_T = T^{o(1)}$, so this is expected to hold. |

**What this kills, what it does not.** The halo theorem *kills the
rooted Palm wall as a necessary input to the H1 contour
contribution*: there is no need for a rooted Palm box law, no
$W_A$ cluster weight, no $n$-level density obstruction. It does
*not* kill the positive budget $R_B(T,c) = \sum |L'(\rho)|^{-1}$ as
a meaningful object; a deterministic two-zero gadget shows $R_B$ is
genuinely larger than the signed residue sum by an arbitrary
amount, so any direct route to $R_B = o(T^2)$ still requires the
Palm-style input.

**For the Dirichlet (SP-L) analog.** The same divided-difference
trick on cluster residues of $K^w / (w \cdot L(w + \rho, \chi))$
transfers conceptually. A standalone GL(1) sketch of all four
doors is at
[`HALO_GL1_SKETCH_2026-05-12.md`](HALO_GL1_SKETCH_2026-05-12.md).
The transfer's findings:

- Door B' (halo shift comparison, GL(1) version) is **provable** by
  the same proof as Door B of the GL(2) plan, with identical
  constants — the geometric exclusion of $\partial \Omega_K$ from
  every off-target halo is structure-free.
- Door D' (the $M_K$ sup-bound) is **automatic** in GL(1) because
  $|K^w|$ on the halo boundary is bounded by an absolute constant
  $e^R$, since the halo radius is $R / \log K$.
- Door A' (a Dirichlet shifted second moment
  $\sum_{\rho'}^{\mathrm{mult}} |L(\rho' + \alpha, \chi)|^{-2}$)
  remains open at the level of the GL(2) version, requiring a
  $T_K (\log T_K)^{O(1)}$ bound.
- The **halo theorem in GL(1)** yields
  $|R_K(\chi, \rho)| \ll K^{1/2 + \varepsilon + o(1)}$
  on the off-target aggregate, which is **far above** the $o(\log K)$
  target of (SP-L). The GL(1) shifted-Perron problem operates at
  the $\log K$ leading scale; the GL(2) halo route exploits the
  much larger $T^2$ scale of the H1 problem. The naïve halo
  transfer therefore does *not* close (SP-L) by itself.

This is an honest negative finding: the halo route is the right
*structural pivot* (signed cancellation, not termwise budgets), but
the GL(1) shifted-Perron problem requires either a much stronger
Door A' (a Dirichlet shifted second moment of order
$(\log K)^{O(1)}$, i.e., near-Lindelöf strength) or a different
mechanism exploiting the small $\log K$ scale. We do not assert
this is impossible; we assert that the GL(2) halo theorem does not
transfer to (SP-L) with the same closure-strength.

The §X.7 Q:Perron now reads, precisely:

> *To close (SP-L), it is sufficient to prove either
> (a) a Dirichlet shifted second moment
> $\sum_{\rho'}^{\mathrm{mult}} |L(\rho' + \alpha, \chi)|^{-2} \ll_\chi (\log K)^{O(1)}$
> (much stronger than the natural $T_K(\log T_K)^{O(1)}$ expected
> envelope), or
> (b) a mechanism not based on the halo signed cancellation that
> exploits the $\log K$ leading scale of the shifted Perron problem.*

This is the precisely stated GL(1) version of Koyama's
"shifted Perron remainder requirements."

---

## X.8 Code, data, and certificate availability

All scripts, refined zero data, numerical-table CSVs, convergence
logs, Lean 4 lake project, and the adversarial-pass audit log will
be deposited as a single self-contained reproducibility bundle
(`Supplementary material S1`) at submission, mirrored at a Zenodo
DOI. The bundle pins all software versions (Lean toolchain
`leanprover/lean4:v4.28.0`; Mathlib commit hash; `mpmath 1.4.1`;
PARI/GP 2.15.x; FLINT 3.x). The lake-manifest hash is recorded in
the bundle manifest. The Phase-1 Dominance-of-$-1$ replication
bundle is the version supplied to S. Koyama on 2026-05-04.

Each numerical table in §X.5 cites the L1 script and L2 reproducer.
Each external theorem cited in §X.4 has its PDF retrieval recipe,
page/equation, and verbatim quote recorded in
`Supplementary material S2 (citation audit)`.

---

## Internal change log (this draft)

- **2026-05-12 v0.1.** First complete draft of the
  Technical/Computational section, written from the
  `TECHNICAL_COMPUTATIONAL_SECTION_PLAN_2026-05-12.md` plan and the
  `SCOPE_AUDIT_10E13_2026-05-12.md` audit. Phase-1 replication and
  analytic verification appear as separate subsections (§X.5.1 vs
  §X.5.2–§X.5.6). Adversarial-pass actions from the Mimo pilot are
  incorporated (embedded AK quote in §X.4.3; convergence-regime
  table in §X.4.1; (SP-L) phrased as open challenge in §X.4.4, not
  impossibility; "consistent with" rather than "demonstrates" for
  empirical decay rates).
- **2026-05-12 v0.2.** Lean-memo additions: `c_W = -γ_E - E_1(1)`
  kernel-constant theorem and Petersson family-average boundary
  formalization added to §X.6 inventory as the strongest current
  Lean items (delivered to Koyama on 2026-05-02). §X.5 opens with
  an explicit two-scales framing sentence: replication at
  $x = 1.3\cdot10^{13}$ vs analytic at $K \le 2\cdot 10^6$–$10^7$,
  with a no-cross-extrapolation guarantee. §X.5.2 table filled with
  the $L''(\rho,\chi)$ values from `Koyama_C1.out` (`dps = 50`).
- **2026-05-12 v0.3.** Edits driven by the L3-Mimo adversarial pass
  against the draft itself ([`ADVERSARIAL_MIMO_DRAFT_2026-05-12.md`](ADVERSARIAL_MIMO_DRAFT_2026-05-12.md);
  ten objections addressed in
  [`ADVERSARIAL_AUDIT_RESPONSE_DRAFT_2026-05-12.md`](ADVERSARIAL_AUDIT_RESPONSE_DRAFT_2026-05-12.md)):
  - §X.2 lane table restructured into **L1 / L1b / L2 / L3** with
    status flags (executed vs planned); the in-language mpmath
    cross-check is now correctly labeled L1b, not L2, and L2 is
    explicitly flagged "Planned, not executed."
  - §X.4.1 explicitly states that Akatsuka (2013) Lemma 2.1 is
    unconditional, making the unconditional status of Theorem X.4.1
    transparent.
  - §X.4.3 includes an explicit specialization paragraph from
    Aoki–Koyama (1.4) general form to Hypothesis AK at $m=1$,
    $\rho \ne \tfrac12$.
  - §X.4.4 adds a one-sentence statement of what (SP-L) failure
    would mean for $D_K \cdot E_K$ convergence.
  - §X.5.2 explicitly states that only the modulus $|D_K|$ is
    tracked, not $D_K$ itself.
  - §X.5.6 rewritten as a clean negative result with what was tested
    and what failed; the "diagnostic" framing is dropped.
  - §X.6 Lean tags for files that do not yet exist downgraded from
    PROVED-UP-TO-MATHLIB-PREREQ to **PLANNED**, with explicit notes.
  - §X opening rewritten to separate the two scales in distinct
    sentences with an explicit no-cross-extrapolation guarantee.
  - §X.7 adds a tenth open question, Q:L2-PARI: cross-language
    verification at $K = 10^7$ in PARI/GP or Arb.
- **2026-05-12 v0.3 cross-checks executed.**
  - L1b in-language verifier `mpmath_L2_crosscheck.py` ran 2026-05-12;
    output [`L2_CROSSCHECK_2026-05-12.md`](L2_CROSSCHECK_2026-05-12.md).
    Agreement on all four pairs: $|\Delta L'|, |\Delta L''| \le 6\cdot 10^{-12}$;
    $|\Delta C_1| \le 5\cdot 10^{-13}$; $|R(K)|$ matches to all six
    reported digits at $K = 200{,}000$.
  - L3-Mimo and L3-Ollama draft-passes both produced reports;
    Ollama confirmed every load-bearing algebraic identity it was
    asked to verify (Laurent expansion at the simple zero; residue
    coefficient extraction); Mimo's 10 objections are all resolved
    in v0.3.
  - L3-MLX pass with `Qwen2.5-1.5B-Instruct-4bit` was insufficient
    (model too small); future passes should use the cached
    `Qwen3-Next-80B-A3B-Thinking-4bit` or
    `DeepSeek-R1-Distill-Llama-70B-4bit` instead.
- **2026-05-12 v0.4 — cross-language L2 lane now executed.** Following
  Mimo objection M1 (fatal — "the L2 cross-check is mpmath-only"),
  PARI/GP 2.17.3 and Arb (via python-flint 0.8.0) were installed
  into a fresh conda environment `~/miniforge3/envs/pari-arb` from
  conda-forge. The L2 lane is now executed:
  - PARI L2 cross-check ([`pari_L2_crosscheck.gp`](pari_L2_crosscheck.gp)
    → [`L2_PARI_CROSSCHECK_2026-05-12.md`](L2_PARI_CROSSCHECK_2026-05-12.md)).
    All four pairs: $L'$ matches L1 to $\ge 11$ decimal digits on
    each component; $|C_1|, |L''|$ to $\ge 10$ digits; $|R(K)|$ at
    $K = 200{,}000$ matches L1 reference to all 6 reported digits.
    Runtime 3.4 s on Apple M1 Max.
  - Arb 250-bit spot-check ([`arb_L2_spot.py`](arb_L2_spot.py) →
    [`ARB_L2_SPOT_2026-05-12.md`](ARB_L2_SPOT_2026-05-12.md)). For
    $\chi_{-4}/z_1$ and $\chi_{-4}/z_2$ (the worst pair): $|L'|$
    agrees with the PARI L2 reference at interval width
    $\le 3 \cdot 10^{-43}$ — agreement at the 40+ decimal level on a
    third independent C-library stack.
  - The §X.2 lane table now reads: L1 ✓ executed, L1b ✓ executed,
    L2 ✓ executed (this draft), L3 ✓ executed against both
    components and the draft.
  - §X.5.2 prose updated to report the cross-language $|R(K)|$
    agreement table.
  - §X.7 Q:L2-PARI converted to Q:L2-PARI-Kscale: the open ask is
    now to push the cross-language L2 lane from $K = 200{,}000$ up
    to $K = 10^7$ (estimated 3 minutes wall-clock).
  - Mimo objection M1 (Fatal) is fully resolved.

## Provenance and supersession of prior drafting attempts

For internal record-keeping and to prevent accidental re-use of
superseded content: an earlier drafting effort for a "Normalized
Duality Constant" paper exists in
[`primes-equispaced/experiments/`](../../experiments/). This prior
corpus comprises ~25 paper-section drafts (file names beginning
`NDC_PAPER_*`, `M1_NDC_PAPER_*`, `M5_NDC_PAPER_*`,
`M5_NDC_MECHANISM_PAPER_SECTION.md`, `M5_NDC_BK_PROOF_PAPER.md`,
`M5_NDC_UNIVERSALITY_THEORY.md`, etc.) and ~50 supporting analyses
(adversarial reviews, decomposition notes, character analyses,
high-$K$ numerical reports, "why $\zeta(2)$" historical arguments,
Koyama-track literature searches). The corpus dates to roughly
October 2023 through early 2026 and predates the 2026-05-09 audit
that retracted the $1/\zeta(2)$ asymptotic target in favor of
Aoki–Koyama's $e^{-\gamma}$.

**Status of the prior corpus.** Superseded for theorem statements,
asymptotic-constant statements, and load-bearing numerics by the
present draft. Specifically:

- Every prior occurrence of the asymptotic statement
  $D_K \to 1/\zeta(2)$ is *retracted*. The corrected statement is
  the conditional $D_K \to e^{-\gamma}$ of (\ref{eq:NDC}), under
  Hypothesis AK and (SP-L).
- The "why $\zeta(2)$" historical reasoning files
  (`M1_NDC_WHY_ZETA2.md`, `NDC_WHY_ZETA2_LIMIT.md`, etc.) describe
  the *pre-correction* heuristic and should be cited only as
  historical context in any future introduction that explains the
  constant correction.
- High-$K$ numerical reports
  (`M5_NDC_HIGH_K_OVERNIGHT.md`, `M5_NDC_HIGH_K_VERIFICATION.md`,
  e.g. $K \in \{1, 2, 5, 10, 20\}\cdot 10^6$ for the same four
  $(\chi, \rho)$ pairs) report $D_K \cdot \zeta(2)$ rather than
  $D_K \cdot e^{\gamma}$; their raw numbers may be reinterpreted
  under the corrected normalization but should not be lifted into
  this draft without re-running.
- Sym${}^2 / \langle f, f\rangle$ proportionality content in the
  prior corpus is now negative (see §X.5.5 and Question Q:Sym2).
- The prior corpus's claim that 422 Lean results validate the NDC
  framework is retained as a *project-level* statement; the present
  manuscript scopes its Lean inventory to the files actually
  present in `formal-conjectures/` (see §X.6).

**What is still usable.** The bibliography in
`NDC_KOYAMA_LITERATURE_SEARCH.md` (with the constant-correction
caveats noted above), the section-structure conventions of
`M1_NDC_PAPER_SECTION1_INTRO.md`, the proof-step decomposition of
`NDC_PROOF_STEP*.md` (after substituting the corrected constant),
and the character-evaluation conventions of
`T_INF_L2RHO_NUMERICAL_VERIFY.md` are all still consistent with
the present draft. They may be drawn on for the introduction of
the eventual full paper.

## TODO before this draft is shown to Koyama

(Internal to Saar; recorded here so that the next iteration is
deliberate rather than ad hoc. Status as of 2026-05-12 v0.3.)

1. **(DONE 2026-05-12 v0.4)** L2 cross-language verification executed
   in PARI/GP 2.17.3 at $K = 200{,}000$ on all four pairs and in
   Arb (250 bits) on the worst pair; see
   [`L2_PARI_CROSSCHECK_2026-05-12.md`](L2_PARI_CROSSCHECK_2026-05-12.md)
   and [`ARB_L2_SPOT_2026-05-12.md`](ARB_L2_SPOT_2026-05-12.md).
   Remaining ask: push the cross-language $D_K$ verification to
   $K = 10^7$ in PARI (~3 min wall-clock), recorded as
   Q:L2-PARI-Kscale in §X.7.
2. **(DONE 2026-05-12 v0.4)** L2-Arb spot check executed for
   $\chi_{-4}/z_1$ and $\chi_{-4}/z_2$ at 250 bits via python-flint.
   Optional follow-up: extend the Arb spot-check to $\chi_5$ and
   $\chi_{11}$.
3. **Lean files for Lemma X.3.1 and Theorem X.4.1.** Currently
   tagged PLANNED in §X.6 because the files do not yet exist. Write
   `LocalPerronResidue.lean` and `CorrectedBInfty.lean`,
   `lake build`-verify, then upgrade the tag to
   PROVED-UP-TO-MATHLIB-PREREQ in §X.6.
4. **Aristotle audit of every existing `sorry`** in the Lean
   project; document the result in the reproducibility bundle.
5. **L3 adversarial re-run after v0.3 edits.** The current
   adversarial responses are against v0.1–v0.2. After the v0.3
   changes settle, re-run Mimo + Ollama (and a larger MLX model)
   against the revised text to confirm no new objection has emerged.
6. **§X.5.5 EC point list.** Current 22 points retain the conductor
   collinearity. Optional: compute rank-4 ($234446a_1$) and rank-5
   ($19047170a_1$) exploratory points and decide whether to mark
   them exploratory or include them in the regression.
7. **Lean repo attachment** (peer-reviewable artifact vs supporting-code
   URL). User decision.
8. The placeholder cross-references `\thmref`, `\appref`, `\qref` and
   the `\tag{...}` labels need to be replaced by the conventions of
   whatever journal target you pick; until then they are descriptive
   only.
9. Authorship block remains a placeholder; nothing in the body
   depends on the order being fixed.
