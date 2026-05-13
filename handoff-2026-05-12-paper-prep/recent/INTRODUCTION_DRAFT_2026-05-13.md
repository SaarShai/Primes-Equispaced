# Introduction — first prose draft (discussion document)

A first prose draft of the Introduction, against the bullet outline
in `INTRO_AND_ABSTRACT_OUTLINE_2026-05-13.md`. Frame: discussion
document, intended as a drop-in starting point that can be edited,
tightened, or substantially restructured. The Introduction sits at
whole-paper level; the §X-specific material below is from our
analytic contribution, with explicit "your-section-here" cues where
the Dominance-of-$-1$ framework material would join.

---

## 1. Introduction

### 1.1 Motivation

The study of Chebyshev's bias and its refinement to weighted
prime-counting functions $\pi_w(x; N, a)$ has been a central thread
in analytic number theory since the work of Rubinstein and Sarnak
[RS] and the more recent re-weighted formulation of Aoki and
Koyama [AK]. The choice of weight $w = 1/2$ stabilises the bias to
$\sim \log\log x$ growth between non-residues and residues
modulo $N$ [AK, Theorem 1.4], and Shimada–Koyama [SK] establish that
no weight $w < 1/2$ stabilises the sign of the difference at all.
At $w = 1/2$ the bias *among* quadratic non-residues — invisible at
the classical Rubinstein–Sarnak resolution — emerges as a finer
structure controlled by the values $\log L(1, \chi_{a, 1})$. The
\emph{Dominance-of-$-1$} framework of Koyama [§\textit{your section
on nontriv.pdf here}] formulates this fine bias precisely:
$\log L(1, \chi_{-1, 1})$ is conjecturally the smallest of all such
values, manifesting as a numerical signal in the residue-count
tables of $\pi(x; N, a) - \pi(x; N, 1)$ at $x \approx 10^{13}$ across
moduli $N \in \{7, 8, 11, 19, 23\}$.

### 1.2 The analytic dual and the corrected normalisation

The framework's analytic dual is supplied by the partial Euler
product $E_K(\chi, \rho) := \prod_{p \le K}(1 - \chi(p) p^{-\rho})^{-1}$
and the partial Möbius sum
$c_K(\chi, \rho) := \sum_{n \le K} \mu(n) \chi(n) n^{-\rho}$
at a simple noncentral zero $\rho$ of $L(s, \chi)$. The
Aoki–Koyama Deep-Riemann-Hypothesis statement [AK, eq.~(1.4)]
asserts, for $m = \mathrm{ord}_{s = 1/2} L(s, \chi)$,
$$
\lim_{x \to \infty}\Bigl((\log x)^{m} \prod_{p \le x}(1 - \chi(p)/p^s)^{-1}\Bigr)
\;=\;
\frac{L^{(m)}(s, \chi)}{e^{m\gamma}\,m!}
\quad \text{(simple-zero, noncentral case).}
$$
Specialised to $m = 1$ and a critical-line zero
$\rho \ne \tfrac12$, this says $E_K(\chi, \rho) \log K \to
L'(\rho, \chi) / e^\gamma$ — the **corrected Mertens constant
$e^{-\gamma}$** in place of the earlier $\zeta(2)^{-1}$ target that
appeared in the first phase of this collaboration. The dual
statistic $D_K = c_K E_K$ has corrected asymptotic target
$e^{-\gamma}$, accurate to better than $0.02$ at $K = 10^{7}$ and
incompatible with $\zeta(2)^{-1}$ at the $1/\log K$ finite-size
scale.

### 1.3 Contributions of this paper

We make four contributions.

(i) An **unconditional four-component identity** for the prime-power
tail $T_\infty(\chi, \rho)$ (Theorem~X.4.1), isolating the primitive
$L$-factor $\tfrac12 \log L(2\rho, \psi)$, a finite bad-prime
correction $\mathrm{BPC}_1$, the residual $\mathrm{BPC}_2$, and the
absolutely-convergent $k \ge 3$ tail; the only analytic input is
Akatsuka 2013 eq.~(2.5), itself unconditional.

(ii) A **local Perron double-pole residue identity** (Lemma~X.3.1)
giving the subleading constant $C_1(\chi, \rho) = -L''(\rho, \chi) /
(2 L'(\rho, \chi)^2)$, together with the partial-Möbius asymptotic
$c_K(\chi, \rho) = \log K / L'(\rho, \chi) + C_1 + o(1)$ as
$K \to \infty$ (Theorem~X.4.2), conditional only on simplicity of
the off-target zeros at the truncation height of Inoue's explicit
formula.

(iii) **Precisely-stated open challenges** — the shifted Perron
leading remainder (SP-L), the Dirichlet Polynomial Avoidance
Conjecture (DPAC), and the GL(2) reciprocal-derivative control —
each with the input theorem that would close it; (SP-L) and DPAC
are the two analytic obstructions that block the conditional limit
$D_K \to e^{-\gamma}$ and the general-$K$ avoidance statement,
respectively.

(iv) Rigorous **independent replication of the Phase-1
Dominance-of-$-1$ tables** at $x = 1.3 \cdot 10^{13}$ across two
independent prime-enumeration implementations
($\pi(1.3 \cdot 10^{13}) = 445{,}831{,}610{,}611$; identity~(3.1)
of the Dominance-of-$-1$ framework verified across $495$ cells), and
a Lean 4 / Mathlib v4.28.0 accompaniment in which seven of the nine
files in the formalisation inventory are fully proved.

### 1.4 Open challenges and outlook

The shifted Perron leading remainder (SP-L) is the load-bearing
analytic obstruction: it is the input that, combined with the
Aoki–Koyama statement, would close the corrected duality limit
$D_K(\chi, \rho) \to e^{-\gamma}$. The Dirichlet Polynomial Avoidance
Conjecture is a related open problem at the LI-Hypothesis level for
$\zeta$-zero ordinates; it would also follow from a sufficient
phase-avoidance hypothesis at $\zeta$-zero ordinates, which the
present paper records as an explicit reduction. On the
elliptic-curve side, an analogous GL(2) reciprocal-derivative
control remains the gating analytic input. We state each precisely
in §X.7.

### 1.5 Paper structure

§2 [\textit{your Dominance-of-$-1$ section title}] reviews the
Aoki–Koyama framework and presents the Dominance-of-$-1$ conjectures
in detail. §3 [\textit{...}] develops the further theoretical
consequences. §X (the present technical/computational section)
treats the analytic dual, the Lean 4 formalisation inventory, and
the open challenges. Appendix A gives the full proof of
Theorem~X.4.1; Appendix B gives the full proof of Theorem~X.4.2 and
the local Perron residue computation. The Lean 4 lake project and
all numerical artefacts are in the reproducibility bundle
(Supplementary Materials S1).

---

## Notes for the integration pass

- **Author-voice.** Collective "we" throughout, consistent with §X.
- **What you (Shin-ya) will likely want to add / replace.** §1.1
  needs your authoritative framing of the
  Dominance-of-$-1$ result — what is being claimed, how it builds on
  AK and SK, and (for instance) the role of $\chi_{a, 1}$ vs
  $\chi_{1, a}$. §1.5 needs your section titles for §2, §3.
- **What's optional.** §1.4 could be folded into §1.3(iii) for a
  tighter paper. §1.2 could be shorter if the Abstract already names
  $e^{-\gamma}$ vs $\zeta(2)^{-1}$.
- **Citation keys.** All bibliographic references use placeholder
  keys ([RS], [AK], [SK], [Aka], [Ino], [Sou]) until we fix the
  BibTeX names; the actual `references.bib` already defines them.
- **References still to be added.** Stark (1971), Littlewood (1914),
  Hardy–Littlewood (1918), and possibly Ingham (1942) for the
  classical Chebyshev-bias context.
