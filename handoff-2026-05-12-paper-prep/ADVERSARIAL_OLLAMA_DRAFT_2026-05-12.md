8. The $B_\corrected{Binfty}$ identity (Theorem X.4.1) is unconditional.
   The $C_1$ partial-Möbius identity (Thecorrected{C1}}) is unconditional. [K
The AK normalization $e^{-\changeable{gamma}}$ is conditional on Hypothesis[10D[K
Hypothesis AK and (SP-L). The EC NDC sweep is a diagnostic, not a command. [K
The EC rank-trend (\ref{editable_W2}) is a conductor-confounded trend,

<think>

</think>

1. **Laurent Expansion of $1/L(w+\rho, \chi)$**
   $$ \frac{1}{L(w+\rho,\chi)} = \frac{1}{L'(\rho,\chi)w} - \frac{L''(\rho,[15D[K
\frac{L''(\rho,\chi)}{2L'(\rho,\chi)^2} + O(w) $$
   **Status:** CONFIRMED. Elementary Taylor inversion of $L(w+\rho) \approx[7D[K
\approx w L' + \frac{w^2}{2} L''$.

2. **Product Rule for Residue Coefficient**
   $$ \text{Coeff of } w^{-1} \text{ in } \left( \frac{K^w}{w} \right) \lef[4D[K
\left( \frac{1}{L(w+\rho)} \right) = \frac{\log K}{L'} - \frac{L''}{2(L')^2[18D[K
\frac{L''}{2(L')^2} $$
   **Status:** CONFIRMED. Follows from multiplying $\frac{1}{w} + \log K + [K
\dots$ by the Laurent series above.

3. **Corrected $B_\infty$ Identity**
   $$ T_\infty(\chi,\rho) = \tfrac12 \log L(2\rho,\psi) + \mathrm{BPC}_1 + [K
\mathrm{BPC}_2 + T_{\ge 3} $$
   **Status:** NOT CHECKED. Requires verifying the specific splitting of th[2D[K
the Euler product log into "k=1" (conditional) and "k>=2" (absolute) compon[6D[K
components and the handling of imprimitive characters.

4. **Aoki–Koyama–Mertens Limit**
   $$ \lim_{K\to\infty} E_K(\chi,\rho) \log K = \frac{L'(\rho,\chi)}{e^\gam[27D[K
\frac{L'(\rho,\chi)}{e^\gamma} $$
   **Status:** REJECTED (as unconditional). The draft explicitly labels thi[3D[K
this **Hypothesis AK** and states it is DRH-conditional. While the formula [K
itself is a known conjectural limit under RH/DRH, the draft correctly ident[5D[K
identifies it as unproved.

5. **Numerical Duality Constant Limit**
   $$ D_K(\chi,\rho) \to e^{-\gamma} $$
   **Status:** REJECTED (as proven). The draft explicitly states this is co[2D[K
conditional on Hypothesis AK and the open (SP-L) hypothesis.

6. **Elliptic Curve Normalization**
   $$ \rho_E = 1 + i\gamma_E, \quad \rho_\Delta = 6 + i\gamma_\Delta $$
   **Status:** NOT CHECKED. This is a definition choice for the "arithmetic[11D[K
"arithmetic normalization" in the context of GL(2) forms, distinct from the[3D[K
the analytic critical line.

**Normalization/Branch Ambiguity Flags:**

*   **Log Branch ($s=2\rho$):** The draft fixes the branch via analytic con[3D[K
continuation from $\mathrm{Re}(s)>1$. This is standard and unambiguous for [K
$L(2\rho, \psi)$ since $2\rho$ is on the critical line $\mathrm{Re}(s)=1$ b[1D[K
but not at a pole (assuming $\psi$ is non-principal or $2\rho \neq 1$). How[3D[K
However, if $\psi$ is principal (e.g., $\chi^2=1$), $L(s,\psi)$ has a pole [K
at $s=1$. If $2\rho$ is close to 1, numerical stability is a concern, thoug[5D[K
though $\mathrm{Re}(2\rho)=1$ generally keeps it away from the pole at $s=1[4D[K
$s=1$ unless $\rho=1/2$ and $\tau=0$ (excluded).
*   **Arithmetic vs. Analytic Normalization:** The draft explicitly separat[7D[K
separates the analytic Dirichlet L-function normalization ($\rho = 1/2 + i\[2D[K
i\tau$) from the arithmetic elliptic curve normalization ($\rho_E = 1 + i\g[3D[K
i\gamma_E$). This is a critical distinction. The draft acknowledges the "bu[3D[K
"bug class" of mixing them. The notation $\rho$ is overloaded: in §X.1 it d[1D[K
denotes a zero of $L(s,\chi)$, while in the EC subsections it denotes a poi[3D[K
point on the critical line of an L-function associated with a form (normali[8D[K
(normalized to $s=1$). This is potentially confusing but technically distin[6D[K
distinct contexts.
*   **Imprimitive Character $\psi$:** The definition $\chi(n)^2 = \psi(n)$ [K
for $\gcd(n,q)=1$ is standard for inducing the square of a character to a p[1D[K
primitive one. The factor $\mathrm{BPC}_1$ handles the Euler factors at $p|[3D[K
$p|q, p\nmid f$. This is consistent with standard Euler product identities [K
$L(s, \chi^2) = L(s, \psi) \prod_{p|q, p\nmid f} (1 - \psi(p)p^{-s})$. The [K
log of this product yields the $\mathrm{BPC}_1$ term. This part of the $B_\[4D[K
$B_\infty$ identity is likely correct, but the convergence of the $\log L(2[3D[K
L(2\rho, \psi)$ term on the critical line is delicate and relies on the spe[3D[K
specific summation method (Akatsuka).<|endoftext|><|im_start|><|im_start|>u[49D[K
(Akatsuka).<|endoftext|><|im_start|><|im_start|>user
You are an independent mathematical reviewer. The following is a draft of a[1D[K
a Technical/Computational section in analytic number theory. Read it and pr[2D[K
produce *only* the following:

1. List every load-bearing algebraic identity in the draft (state the ident[5D[K
identity name + the LaTeX form).
2. For each, mark it CONFIRMED, REJECTED, or NOT CHECKED based on whether y[1D[K
you can verify it on the spot from elementary Laurent expansions and Euler-[6D[K
Euler-product log identities.
3. Flag any normalization/branch ambiguity you spot.

Be terse. No introduction, no conclusion, no thanks. Cap response at 600 wo[2D[K
words.

DRAFT FOLLOWS:
===
<!--
schema_version: 1
title: "Saar–Koyama paper — Technical & Computational section, first draft"[6D[K
draft"
date: 2026-05-12
type: eq:res
tier: working
status: DRAFT_INTERNAL_NOT_SENT
target: "first complete draft for internal review; Koyama 2026-05-12 ask"
authorship: "left as placeholders; user has not yet fixed author order"
sources:
  - handoff-2026-05-12-paper-prep/TECHNICAL_COMPUTATIONAL_SECTION_PLAN_2026handoff-2026-05-12-paper-prep/TECHNICAL_COMPUTATIONAL_SECTION_PLAN_2026-05-12.md
  - handoff-2026-05-12-paper-prep/SCOPE_AUDIT_10E13_2026-05-12.md
  - handoff-2026-05-12-paper-repair/ADVERSARIAL_AUDIT_RESPONSE_2026-05-12.mhandoff-2026-05-12-paper-repair/ADVERSARIAL_AUDIT_RESPONSE_2026-05-12.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-0handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - handoff-202X-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
  - HANDOFF.md
tags: [koyama, draft, technical-section, computational-section, lean4]
-->

# §X. Methodology, formalization, and numerical evidence

> *Internal draft, 2026-05-12. Author order and journal target are open
> placeholders. The draft is written so that statements, forms, and
> normalizations can be transferred to LaTeX with minimal rework.
> Cross-references such as `(\thmref{B-infty})` use placeholder
> labels.*

This section gathers the computational and formal content of the
present paper. We describe (i) the precise normalizations used in
every Dirichlet-side and Euler-product computation; (ii) the
three-layer double-verification protocol applied to every numerical
claim; (iii) the partial Lean 4 / Mathlib4 formalization that
accompanies the corrected Aoki–Koyama–Mertens identity and the
$B_\infty$ identity; (iv) the current numerical findings, including
the Phase-1 Dominance-of-$-1$ replication at $x = 1.3 \cdot 10^{13}$
and the analytic identities verified at $K \le 10^7$; and (v) the
open challenges that should, in
2026-05-12 ask"
authorship: "left as placeholders; user has not yet fixed author order"
sources:
  - handoff-2026-05-12-paper-prep/TECHNICAL_COMPUTATIONAL_SECTION_PLAN_2026handoff-2026-05-12-paper-prep/TECHNICAL_COMPUTATIONAL_SECTION_PLAN_2026-05-12.md
  - handoff-2026-05-12-paper-prep/SCOPE_AUDIT_10E13_2026-05-12.md
  - handoff-2026-05-12-paper-repair/ADVERSARIAL_AUDIT_RESPONSE_20226-05-12.handoff-2026-05-12-paper-repair/ADVERSARIAL_AUDIT_RESPONSE_20226-05-12.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-0handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
  - HANDOFF.md
tags: [koyama, draft, technical-section, computational-section, lean4]
-->

# §X. §X. Methodology, formalization, and numerical evidence

> *Internal draft, 2026-05-12. Author order and journal target are open
> placeholders. The draft is written so that statements, forms, and
> normalizations can be transferred to LaTeX with minimal rework.
> Cross-references such as `(\thmref{B-infty})` use placeholder
> labels.*

This section gathers the computational and formal content of the
present paper. We describe (i) the precise normalizations used in
every Dirichlet-side and Euler-product computation; (ii) the
three-layer double-verification protocol applied to every numerical
claim; (iii) the partial Lean 4 / Mathlib4 formalization that
accompanies the corrected Aoki–Koyama–Mertens identity and the
$B_\infty$ identity; (iv) the current numerical findings, including
the Phase-1 Dominance-of-$-1$ replication at $x = 1.1.3 \cdot 10^{13}$
and the analytic identities verified at $K \le 10^7$; and (v) the
open challenges that should, in the authors' view, structure the next
phase of the program.

---

## X.1 Notation and normalizations

Fix a primitive non-principal Dirichlet character $\chi$ modulo
$q \ge 2$, and let $\rho = \tfrac12 + i\tau$ with $\tau \neq 0$ be a
**simple** non-trivial zero of $L(s,\chi)$ on the critical line. We
work throughout with the following objects:

- **Truncated partial Euler product:**
  $$
  E_K(\chi,\rho) \;:=\; \prod_{p\le K} \Bigl(1 - \chi(p)\,p^{-\rho}\Bigr)^{[26D[K
\chi(p)\,p^{-\rho}\Bigr)^{-1}.
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
  T_K(\chi,\rho) \;:=\; \sum_{p\le K}\,\sum_{k\ge 2}\frac{\chi(p)^k}{k\,p^{[25D[K
2}\frac{\chi(p)^k}{k\,p^{k\rho}},
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
claim. This three-layer stack is not a substitute for human refereeing; it [K
is a
mechanical check that the prose and the load-bearing algebra survive
an adversarial reading. Two pilot dispatches were run on
2026-05-12. The Ollama `qwen3.6:35b-a3b-a3b-q4km` model, asked in
isolation, **independently reproduced** the simple-zero Laurent expansion
$$
\frac{1}{L(w+\rho,\chi)}
\;=\;\frac{1}{L'(\rho,\chi)\,w} \;-\; \frac{L''(\rho,\chi)}{2\,L'(\rho,\chi[37D[K
\frac{L''(\rho,\chi)}{2\,L'(\rho,\chi)^2} \;+\; O(w)
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
\mathop{\mathrm{Res}}_{w=0}\!\left[\,\frac{K^{w}}{w\,L(w+\rho,\chi)}\,\righ\mathop{\mathrm{Res}}_{w=0}\!\left[\,\frac{K^{w}}{w\,L(w+\rho,\chi)}\,\right]
\;=\;
\frac{\log K}{L'(\rho,\chi)} \;-\; \frac{L''(\rho,\chi)}{2\,L'(\rho,\chi)^{[40D[K
\frac{L''(\rho,\chi)}{2\,L'(\rho,\chi)^{2}}
\;=\;
\frac{\log K}{L'(\rho,\chi)} + C_1(\chi,\rho).
\end{equation}

*Proof.* The Taylor expansion of $L(w+\rho,\chi)$ at $w = 0$ is
$L(w+\rho,\chi) = w\,L'(\rho,\chi) + \tfrac{w^2}{2}\,L''(\rho,\chi) + O(w^3[5D[K
O(w^3)$,
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
let $\rho$ is a simple zero of $L(s,\chi)$ on the critical line.
Let $\psi$ is the primitive character of conductor $f\mid q$ inducing
$\chi^2$. Then*
\begin{equation}
\label{eq:Binfty}
T_\infty(\chi,\rho)
\;=\;
\tfrac12 \log L(2\rho,\psi)
\;+\; \mathrm{BPC}_1(\chi,\rho)
\;+\; \mathrm{BPC}_2(\chi,\rho)
\;+\; Theorem X.4.1 (corrected $B_\infty$ identity). Then* *Let $\chi$ be a[1D[K
a
primitive non-principal Dirichlet character of conductor $q$, and
let $\rho$ is a simple zero of $L(s,\chi)$ on the critical line.
Let $\psi$ is the primitive character of conductor $f\mid q$ inducing
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
\tfrac12 \sum_{p\mid q,\ p\nmid f} \log\!\bigl(1 - \psi(p)\,p^{-2\rho}\bigr[24D[K
\psi(p)\,p^{-2\rho}\bigr),
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
of $\rho$ as a zero of $L(s,\chi)$ is used. The proof is given in
Appendix \appref{A:Binfty} (full audit), based on the partial-Euler
log-Taylor expansion and the classical Hadamard–de la Vallée Poussin
non-vanishing of $L$ on $\mathrm{Re}(s) = 1$.

A convergence-regime table:

| Term | Convergence | Hypothesis used |
|---|---|---|
| $\tfrac12 \log L(2\rho, \psi)$ | conditional at $\mathrm{Re}(s) = 1$; abs[3D[K
absolute at $\mathrm{Re}(s) > 1$ | Akatsuka 2013 Lemma 2.1 |
| $\mathrm{BPC}_1$ | finite sum over bad primes | textbook (Montgomery–Vaug[16D[K
(Montgomery–Vaughan Thm 9.4) |
| $\mathrm{BPC}_2$ | absolute, $\mathrm{Re}(2k\rho) \ge 2$ | geometric-seri[14D[K
geometric-series + prime-zeta tail |
| $T_{\ge 3}$ | absolute, $\text{Re}(k\rho) \ge \tfrac32$ | geometric-serie[15D[K
geometric-series + prime-zeta tail |

### X.4.2 Subleading constant $C_1$ and the partial Möbius identity

**Theorem X.4.2 (Möbius-side leading + subleading).** *Under the
hypotheses of Theorem X.4.1,*
\begin{

