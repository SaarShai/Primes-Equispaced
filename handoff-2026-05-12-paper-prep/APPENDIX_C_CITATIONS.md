<!--
title: "Appendix C — Citation appendix with verbatim quotations"
date: 2026-05-12
type: appendix
target: companion to SECTION_DRAFT_2026-05-12.md
-->

# Appendix C — Citation appendix (verbatim quotations)

This appendix records the verbatim quotations of every external result
cited in the main text and in Appendices A and B. Each entry gives the
exact source (paper, journal, page or equation number), the verbatim
text, and the role the result plays in the present manuscript.

## C.1 Aoki–Koyama (2023), equation (1.4), p. 235

**Source.** M. Aoki and S. Koyama, *Chebyshev's bias against splitting
and principal primes in global fields*, Journal of Number Theory
**245** (2023), 233–262. DOI: `10.1016/j.jnt.2022.10.005`.
Received 26 June 2022, available online 23 November 2022,
communicated by S. J. Miller. Page 235, equation (1.4).

**Verbatim quotation.**

> *"In case of Dirichlet $L$-functions $L(s,\chi)$ for non-principal
> Dirichlet characters $\chi$, DRH states that it holds on
> $\mathrm{Re}(s) = 1/2$ that*
> \[
> \lim_{x \to \infty}\Bigl((\log x)^m \prod_{p \le x}(1 - \chi(p)/p^s)^{-1}\Bigr)
> \;=\; \frac{L^{(m)}(s, \chi)}{e^{m\gamma}\,m!} \times
> \begin{cases}\sqrt{2}, & \chi^2 = 1,\,s = 1/2,\\ 1, & \text{otherwise,}\end{cases}
> \tag{1.4}
> \]
> *with $\gamma$ being the Euler constant and
> $m = m_\chi = \mathrm{ord}_{s = 1/2}\,L(s, \chi)$."*

**Role in the manuscript.** Specialized to a simple noncentral zero
($m = 1$, $\rho \ne \tfrac12$) it gives Hypothesis AK of §X.4.3.

## C.2 Akatsuka (2013), Lemma 2.1 and equation (2.5)

**Source.** H. Akatsuka, *The Euler product for the Riemann
zeta-function in the critical strip*, preprint, dated February 14,
2013; published in Journal of Number Theory (date as in the project's
internal record). Project copy: `akatsukaDRH3.pdf`.

**Role of Lemma 2.1 / equation (2.5).** Mertens-type estimate for
the prime sum on the boundary line:
\[
\sum_{p \le X}\frac{1}{p^{1 + 2it_0}}
\;=\; c(t_0) \;+\; O\bigl((\log X)^{-1}\bigr),
\qquad t_0 \ne 0.
\]
Proved by partial summation against the prime number theorem with
explicit error term. **Unconditional**: the result does not require
RH or any GRH-type hypothesis.

**Verbatim quotation.** *(To be inserted from the PDF before
submission. The internal proof packets `Koyama_B_infty_proof.md`
§4.4 and `Koyama_C1_subleading_proof.md` §6 reproduce the
character analogue and use this result; the literal quote of
Lemma 2.1 and eq. (2.5) is in the PDF at
`~/Downloads/akatsukaDRH3.pdf`.)*

**Role in the manuscript.** Establishes the analytic continuation of
the $k = 1$ Dirichlet prime sum
$\sum_p \chi^2(p)\,p^{-2\rho}$ to the boundary line, underwriting
Theorem X.4.1 (Appendix A §A.2.3 and A.6).

## C.3 Inoue (2021), Theorem 1, p. 3

**Source.** S. Inoue, *Some explicit formulas for partial sums of
Möbius functions*, Journal de Théorie des Nombres de Bordeaux
**33** (2021), 273–315. Preprint arXiv:1805.05015v1. URL:
`https://www.numdam.org/item/JTNB_2021__33_2_273_0.pdf`. Page 3.

**Verbatim quotation.**

> *"Theorem 1. Let $x > 0$, $q \ge 2$,
> $T \ge \max\{T_0, \exp(q^{1/3}), 2/x\}$, … Then, uniformly for all
> primitive Dirichlet characters $\chi$ modulo $d$ with $d \le q$,
> there exists $T_\nu \in [T, 2T]$ satisfying*
> \[
> M^*(x, \chi)
> \;=\; \sum_{|\gamma| < T_\nu} \frac{1}{(m(\rho) - 1)!}\,
>       \lim_{s \to \rho} \frac{d^{m(\rho)-1}}{ds^{m(\rho)-1}}
>       \Bigl((s - \rho)^{m(\rho)}\,\frac{x^s}{L(s, \chi)\,s}\Bigr)
>       \;+\; \mathop{\mathrm{Res}}_{s=0}\Bigl(\frac{x^s}{L(s, \chi)\,s}\Bigr) \;+\; \cdots\,$*

**Role in the manuscript.** Used in Appendix B §B.1.3 to obtain the
truncated Perron formula for $c_K$ (after the change of variable
$w = s - \rho$), and to give the $J_1, J_2, J_3$ truncation-error
bounds (Inoue 2021 §4).

## C.4 Soundararajan (2009), Theorem 1, p. 1

**Source.** K. Soundararajan, *Partial sums of the Möbius function*,
Annals of Mathematics **170** (2009), 981–993. Preprint
arXiv:0705.0723v2. URL: `https://arxiv.org/pdf/0705.0723`. Page 1.

**Verbatim quotation.**

> *"Theorem 1. Assume the Riemann Hypothesis. Then*
> \[
> M(x) \;\ll\; \sqrt{x}\,\exp\!\bigl((\log x)^{1/2}(\log\log x)^{14}\bigr).
> \]
> *"*

**Role in the manuscript.** Provides the RH-conditional rate for the
off-target zero aggregate in Theorem X.4.2 / Appendix B §B.3 and §B.4.

## C.5 Montgomery–Vaughan, *Multiplicative Number Theory I*, Theorem 9.4 / Corollary 9.5

**Source.** H. L. Montgomery and R. C. Vaughan, *Multiplicative
Number Theory I: Classical Theory*, Cambridge Studies in Advanced
Mathematics **97**, Cambridge University Press, 2007.
Theorem 9.4 / Corollary 9.5.

**Role in the manuscript.** The textbook statement that every
Dirichlet character $\chi$ modulo $q$ is induced from a unique
primitive character $\psi$ of some conductor $f \mid q$, and the
corresponding imprimitive Euler-factor identity
\[
L(s, \chi) \;=\; L(s, \psi) \cdot \prod_{p \mid q,\ p \nmid f}\Bigl(1 - \frac{\psi(p)}{p^s}\Bigr).
\]
Applied with $\chi \mapsto \chi^2$ in Appendix A §A.2.1 to obtain
(\ref{eq:imprimitive}).

**Verbatim quotation.** *(Page reference to be confirmed from the
physical reference before submission.)*

## C.6 Hadamard–de la Vallée Poussin non-vanishing

**Source.** Classical 1896 theorem; modern textbook reference:
G. Tenenbaum, *Introduction to Analytic and Probabilistic Number
Theory*, Third Edition, Graduate Studies in Mathematics **163**,
American Mathematical Society, 2015. Chapter II.5.

**Statement (textbook form).** For every Dirichlet character $\chi$
modulo $q \ge 2$, $L(s, \chi) \ne 0$ on the line $\mathrm{Re}(s) = 1$.

**Role in the manuscript.** Used in Appendix A §A.2.3 to justify
that $\log L(s, \chi^2)$ admits an analytic continuation along the
principal branch through a neighborhood of $s = 2\rho$ (because the
only potential pole of $\zeta$ at $s = 1$ is avoided).

## C.7 Ng (2004), Möbius partial-sum bound

**Source.** N. Ng, *The distribution of the summatory function of the
Möbius function*, Proceedings of the London Mathematical Society
**89** (2004), 361–389.

**Role in the manuscript.** Cited in Appendix B §B.4 for the
stronger conditional rate
$M(x) \ll x^{1/2}(\log x)^{5/4}$ under RH plus a Gonek–Hejhal-type
bound. Not load-bearing for the manuscript's main statement
(Theorem X.4.2 holds under Soundararajan 2009 alone); included for
the rate-envelope discussion only.

## C.8 Bartz (1991), explicit formulas for the Möbius function

**Source.** K. Bartz, *On some complex explicit formulas connected
with the Möbius function*, Acta Arithmetica **57** (1991), 283–293.

**Role in the manuscript.** Background reference for the
Möbius-side Laurent expansion at a simple zero. Used implicitly via
Inoue (2021), who builds on Bartz's framework.

## C.9 Primesieve (used in §X.5.1)

**Source.** K. Walisch, *primesieve* (a fast prime number generator).
Version 12.13. URL: `https://github.com/kimwalisch/primesieve`.

**Role in the manuscript.** Library used by the primary
implementation `replicate.cpp` in the Phase-1 Dominance-of-$-1$
replication (§X.5.1). Library-independence is established by the
hand-rolled C segmented Eratosthenes sieve `independent_sieve.c`,
which uses no external dependency.

## C.10 PARI/GP, FLINT/Arb, mpmath (used throughout §X.5)

- **PARI/GP** version 2.17.3 (released; arm64 darwin, GMP kernel,
  compiled 2026-03-10). URL: `https://pari.math.u-bordeaux.fr/`.
  Used for the cross-language L2 lane (§X.2, §X.5.2,
  Appendix B §B.1.3; via the `lfun` interface for Dirichlet
  $L$-functions and the `chareval` interface for character
  evaluation).
- **FLINT/Arb** via python-flint 0.8.0 (bundling libflint 3.3 and
  Arb). URL: `https://flintlib.org/`. Used for the 250-bit
  interval-arithmetic spot check (§X.5.2; verification report
  `ARB_L2_SPOT_2026-05-12.md` and `ARB_L2_SPOT_CHI5_CHI11_2026-05-12.md`).
- **mpmath** 1.4.1 (Python 3.9/3.13). URL: `https://mpmath.org/`.
  Used for the primary L1 lane and the L1b in-language cross-check
  (§X.2, §X.5.2; verifier script `mpmath_L2_crosscheck.py`).
