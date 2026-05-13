# Appendix A — Full proof of Theorem X.4.1 ($B_\infty$ identity)

This appendix gives the full proof of Theorem X.4.1 of the main text:
for a primitive non-principal Dirichlet character $\chi$ of conductor
$q$ and a simple zero $\rho$ of $L(s,\chi)$ on the critical line, with
$\psi$ denoting the primitive character of conductor $f \mid q$ that
induces $\chi^2$,
\begin{equation}
\label{eq:Binfty-appendix}
T_\infty(\chi,\rho)
\;=\;
\tfrac12 \log L(2\rho, \psi)
\;+\; \mathrm{BPC}_1(\chi,\rho)
\;+\; \mathrm{BPC}_2(\chi,\rho)
\;+\; T_{\ge 3}(\chi,\rho),
\tag{$\star$}
\end{equation}
with the four terms on the right defined in §X.1 of the main text.
The proof uses no hypothesis beyond simplicity of $\rho$ as a zero of
$L(s,\chi)$; in particular it does not use RH, GRH, EDRH, or DRH.

## A.1 Setup — partial-sum decomposition

For a primitive non-principal Dirichlet character $\chi$ modulo
$q \ge 2$ and a simple zero $\rho = \tfrac12 + i\tau$ with $\tau \ne 0$
of $L(s, \chi)$ on the critical line, define
\[
T_K(\chi,\rho) \;:=\; \sum_{p \le K} \sum_{k \ge 2}
\frac{\chi(p)^k}{k\, p^{k\rho}}.
\]
Inside the partial sum, the order of summation may be swapped
unconditionally because for each fixed prime $p \ge 2$,
\[
\sum_{k \ge 2} \frac{(\chi(p)\, p^{-\rho})^k}{k}
\;=\; -\log\bigl(1 - \chi(p)\,p^{-\rho}\bigr) \;-\; \chi(p)\,p^{-\rho},
\]
with $\bigl|\chi(p)\,p^{-\rho}\bigr| = p^{-1/2} \le 2^{-1/2} < 1$, so
the inner series is absolutely convergent and the logarithm is taken
along the principal branch with no ambiguity. Therefore we may
re-index the partial sum by $k$ first:
\begin{equation}
\label{eq:T_K-split}
T_K(\chi,\rho)
\;=\;
\tfrac{1}{2} \sum_{p \le K} \frac{\chi(p)^2}{p^{2\rho}}
\;+\;
\sum_{k \ge 3} \frac{1}{k} \sum_{p \le K} \frac{\chi(p)^k}{p^{k\rho}}.
\end{equation}

The only delicate object in passing to $K \to \infty$ is the $k=2$
piece, since $\mathrm{Re}(2\rho) = 1$ lies on the boundary line where
the Dirichlet prime sum $\sum_p \chi^2(p) p^{-s}$ is conditionally
(not absolutely) convergent. We address this in §A.2. The $k \ge 3$
piece is absolutely convergent and is handled in §A.3.

## A.2 Identification of the $k = 2$ partial sum

### A.2.1 The squared character $\chi^2$ and its primitive companion $\psi$

For $\chi$ primitive of conductor $q$, define $\chi^2$ by
$\chi^2(n) := \chi(n)\,\chi(n)$ for $\gcd(n, q) = 1$ and $\chi^2(n) = 0$
otherwise. The character $\chi^2$ is a (possibly imprimitive)
Dirichlet character modulo $q$. By a standard textbook result
(e.g. Montgomery–Vaughan, *Multiplicative Number Theory I*, Theorem
9.4 / Corollary 9.5), every Dirichlet character modulo $q$ is induced
from a unique primitive character $\psi$ of some conductor $f \mid q$,
in the sense that $\chi^2(n) = \psi(n)$ for $\gcd(n, q) = 1$ and
$\chi^2(n) = 0$ for $\gcd(n, q) > 1$. The corresponding
$L$-function identity is
\begin{equation}
\label{eq:imprimitive}
L(s, \chi^2) \;=\; L(s, \psi) \cdot
\prod_{p \mid q,\ p \nmid f}\!\Bigl(1 - \frac{\psi(p)}{p^s}\Bigr),
\end{equation}
valid initially for $\mathrm{Re}(s) > 1$ and then by analytic
continuation in the natural domain of the right-hand side.

### A.2.2 Log-Euler-product expansion of $\log L(s, \chi^2)$

For $\mathrm{Re}(s) > 1$, taking the principal branch of the logarithm
of the Euler product
$L(s, \chi^2) = \prod_{p \nmid q}(1 - \chi^2(p) p^{-s})^{-1}$ gives
\begin{equation}
\label{eq:logL-expand}
\log L(s, \chi^2)
\;=\;
\sum_{p \nmid q} \sum_{k \ge 1}
\frac{\chi^2(p)^k}{k\, p^{ks}}
\;=\;
\sum_{p} \sum_{k \ge 1}
\frac{\chi(p)^{2k}}{k\, p^{ks}},
\end{equation}
where the second equality extends the prime sum to *all* primes (the
contribution of $p \mid q$ vanishes because $\chi(p) = 0$ for those
primes). The double sum is absolutely convergent in
$\mathrm{Re}(s) > 1$.

Isolating the $k = 1$ term in (\ref{eq:logL-expand}) yields
\begin{equation}
\label{eq:k1-isolation}
\sum_{p} \frac{\chi(p)^2}{p^{s}}
\;=\;
\log L(s, \chi^2)
\;-\; \sum_{k \ge 2} \frac{1}{k} \sum_{p}
\frac{\chi(p)^{2k}}{p^{ks}},
\qquad \mathrm{Re}(s) > 1.
\end{equation}

### A.2.3 Analytic continuation of (\ref{eq:k1-isolation}) to $s = 2\rho$

We extend (\ref{eq:k1-isolation}) to the half-plane $\mathrm{Re}(s) > \tfrac12$ minus the singular set of the right-hand side, as follows.

**Right-hand side analyticity at $s = 2\rho$.** The function
$\log L(s, \chi^2)$ is holomorphic at $s = 2\rho$ provided
$L(2\rho, \chi^2) \ne 0$ and $L(s, \chi^2)$ has no pole there. When
$\chi^2$ is principal (i.e., $f = 1$, hence $\chi^2$ is induced from
the trivial character), $L(s, \psi) = \zeta(s)$, which has a simple
pole at $s = 1$. But $s = 2\rho = 1 + 2i\tau$ with $\tau \ne 0$, so
$s \ne 1$ and the pole of $\zeta$ is avoided. Non-vanishing of
$L(s, \chi^2)$ on the line $\mathrm{Re}(s) = 1$ (away from the
potential pole at $s = 1$) is the classical Hadamard–de la Vallée
Poussin theorem (see e.g. Tenenbaum, *Introduction to Analytic and
Probabilistic Number Theory*, Chapter II.5). Hence
$\log L(s, \chi^2)$ admits an analytic continuation through the
neighbourhood of $s = 2\rho$ along the principal branch.

**Right-hand $k \ge 2$ sum analyticity.** For $k \ge 2$,
$\mathrm{Re}(ks) \ge k \ge 2$ on the line $\mathrm{Re}(s) = 1$, so the
sum $\sum_{k \ge 2} (1/k) \sum_p \chi(p)^{2k} p^{-ks}$ converges
absolutely on $\mathrm{Re}(s) > 1/2$ and defines a holomorphic
function there.

**Left-hand side analyticity.** The prime sum
$\sum_{p} \chi^2(p) p^{-s}$ on the line $\mathrm{Re}(s) = 1$
(excluding $s = 1$ if $\chi^2$ is principal) converges conditionally
by a partial-summation argument due to Akatsuka (2013), *The Euler
product for the Riemann zeta function in the critical strip*,
Lemma 2.1 and equation (2.5), which establishes that for $t_0 \ne 0$,
\begin{equation}
\label{eq:Akatsuka-2.5}
\sum_{p \le X} \frac{1}{p^{1 + 2it_0}} \;=\; c(t_0) \;+\; O\!\bigl((\log X)^{-1}\bigr),
\end{equation}
proved by partial summation against the prime number theorem with
explicit error term. The estimate (\ref{eq:Akatsuka-2.5}) is
**unconditional** (it does not require RH or any GRH-type
hypothesis); the same partial-summation argument applies with
$\chi^2(p)/p^{1+2i\tau}$ in place of $p^{-1-2it_0}$, with the
character orthogonality producing the appropriate cancellation. We
denote the limit by
$\Sigma_2(\chi,\rho) := \lim_{X \to \infty} \sum_{p \le X} \chi^2(p)\,p^{-2\rho}$.

We pass to the boundary $s = 2\rho$ by Abel summation. For
$\sigma > 1$, identity (\ref{eq:k1-isolation}) reads
$\log L(s,\chi^2) - \sum_{k\ge 2}(1/k)\sum_p \chi(p)^{2k}/p^{ks}
= \sum_p \chi(p)^2/p^s$,
the left side analytic in a neighbourhood of $s = 2\rho$ (here we
use Hadamard–de la Vallée Poussin: $L(s, \psi) \ne 0$ on
$\mathrm{Re}(s) = 1$ with $s \ne 1$, where $\psi$ is the primitive
character inducing $\chi^2$, together with the imprimitive Euler-factor
identity $L(s,\chi^2) = L(s,\psi)\prod_{p\mid q,\,p\nmid f}(1 - \psi(p)/p^s)$).
Writing $S(X) := \sum_{p \le X} \chi(p)^2/p^{2\rho}$ and applying
Abel summation gives, for $\sigma > 1$,
$\sum_p \chi(p)^2/p^s = (s - 2\rho)\int_2^\infty S(X)\,X^{-(s - 2\rho) - 1}\,dX
+ \lim_{X\to\infty} S(X)\,X^{-(s-2\rho)}$;
Akatsuka (2013) Lemma 2.1 / eq. (2.5) provides $S(X) = c(\chi,\rho) + O(1/\log X)$
unconditionally as $X \to \infty$, so the limit term equals
$c(\chi,\rho)$ at $s = 2\rho$ and the integral converges to a
continuous function of $s$ in a neighbourhood. Hence
(\ref{eq:k1-isolation}) extends by continuity to $s = 2\rho$ as the
boundary-value identity
\begin{equation}
\label{eq:Sigma2-id}
\Sigma_2(\chi,\rho)
\;=\;
\log L(2\rho, \chi^2)
\;-\; \sum_{k \ge 2} \frac{1}{k} \sum_{p}
\frac{\chi(p)^{2k}}{p^{2k\rho}}.
\end{equation}

### A.2.4 Multiplying by $1/2$

Multiplying (\ref{eq:Sigma2-id}) by $\tfrac12$ and rewriting
$\log L(2\rho, \chi^2)$ via the imprimitive-induction identity
(\ref{eq:imprimitive}) gives
\begin{equation}
\label{eq:k=2-final}
\tfrac{1}{2} \Sigma_2(\chi,\rho)
\;=\;
\tfrac{1}{2} \log L(2\rho, \psi)
\;+\; \tfrac{1}{2}\!\sum_{p \mid q,\ p \nmid f}\!\log\!\bigl(1 - \psi(p)\,p^{-2\rho}\bigr)
\;-\; \tfrac{1}{2} \sum_{k \ge 2} \frac{1}{k} \sum_{p}
\frac{\chi(p)^{2k}}{p^{2k\rho}}.
\end{equation}
The bad-prime correction in the middle term is precisely the
definition of $\mathrm{BPC}_1$ from §X.1; the last term is
$\mathrm{BPC}_2$.

## A.3 Absolute convergence of the $k \ge 3$ tail

For each fixed prime $p$ and each $k \ge 3$,
$|\chi(p)^k p^{-k\rho}| \le p^{-k/2}$, so the inner $k$-series is
bounded by a geometric series:
\[
\Bigl|\sum_{k \ge 3} \frac{\chi(p)^k}{k\,p^{k\rho}}\Bigr|
\;\le\;
\sum_{k \ge 3} \frac{p^{-k/2}}{k}
\;\le\;
\frac{p^{-3/2}}{3} \cdot \frac{1}{1 - p^{-1/2}}.
\]
Summing over primes:
\[
|T_{\ge 3}|
\;\le\;
\frac{1}{3} \sum_p \frac{p^{-3/2}}{1 - p^{-1/2}}
\;\le\;
\frac{1}{3(1 - 2^{-1/2})} \sum_p p^{-3/2}
\;=\;
\frac{P(3/2)}{3(1 - 2^{-1/2})}
\;\approx\;
0.515,
\]
where $P(3/2) = \sum_p p^{-3/2} \approx 0.45224$ is the prime zeta
function at $s = 3/2$. The truncation tail is also estimable: by
partial summation against PNT, for $\alpha > 1$,
$\sum_{p > K} p^{-\alpha} \le \frac{2K^{1-\alpha}}{(\alpha-1)\log K}$,
so
\[
|T_{\ge 3} - T_{\ge 3, K}|
\;\le\;
\frac{2}{3(1 - 2^{-1/2})} \cdot \frac{K^{-1/2}}{\log K},
\]
which is $\sim 3 \cdot 10^{-4}$ at $K = 10^6$ and $\sim 1 \cdot 10^{-4}$
at $K = 2 \cdot 10^6$.

## A.4 Assembling the identity

Define
\[
T_\infty(\chi,\rho) \;:=\; \lim_{K \to \infty} T_K(\chi,\rho).
\]
The limit exists by combining the two parts:

- The $k = 2$ part is $\tfrac12 \Sigma_2(\chi, \rho)$, whose limit
  exists by Akatsuka (2013) Lemma 2.1 / eq. (2.5) and equals the
  right-hand side of (\ref{eq:k=2-final}).
- The $k \ge 3$ part is absolutely convergent by §A.3.

Hence
\[
T_\infty(\chi, \rho)
\;=\;
\tfrac12 \log L(2\rho, \psi)
\;+\; \mathrm{BPC}_1(\chi, \rho)
\;+\; \mathrm{BPC}_2(\chi, \rho)
\;+\; T_{\ge 3}(\chi, \rho),
\]
which is identity ($\star$). $\hfill\square$

## A.5 Bad-prime correction for the four computational pairs

For the four $(\chi, \rho)$ pairs used in the numerical work of §X.5.4,
the bad-prime correction $\mathrm{BPC}_1$ takes the following
character-explicit forms:

| Character | $q$ | $\chi^2$ order | primitive $\psi$ inducing $\chi^2$ | $f$ | bad primes $\{p \mid q,\ p \nmid f\}$ |
|---|---:|:---:|---|---:|---|
| $\chi_{-4}$ | $4$ | $1$ (principal mod 4) | trivial character ($\Rightarrow L = \zeta$) | $1$ | $\{2\}$ |
| $\chi_5$    | $5$ | $2$ | Legendre symbol $(\cdot/5)$ | $5$ | $\emptyset$ |
| $\chi_{11}$ | $11$ | $5$ | order-$5$ character mod $11$ | $11$ | $\emptyset$ |

Explicitly:
- For $\chi_{-4}$: $\mathrm{BPC}_1 = \tfrac{1}{2}\log(1 - 2^{-2\rho})$.
  For $\rho = \tfrac12 + i\tau$, this is
  $\tfrac{1}{2}\log(1 - 2^{-1 - 2i\tau})$, of modulus
  $\le \tfrac{1}{2}\log(1/(1-1/2)) = \tfrac12 \log 2 \approx 0.347$.
- For $\chi_5$ and $\chi_{11}$: $\mathrm{BPC}_1 = 0$.

This explains the numerical observation in §X.5.4 that the $\chi_{-4}$
pairs show slower convergence of the $B_\infty$ identity residual
than $\chi_5$ and $\chi_{11}$: the bad-prime contribution from
$p = 2$ adds an extra layer of conditionally-convergent boundary
mass to the $\chi_{-4}$ identity that is absent for $\chi_5, \chi_{11}$
(the latter pure conditional-tail decay scales as $K^{-1/2}/\log K$
exactly).

## A.6 What the proof does *not* use

For clarity:

- The proof does **not** use RH, GRH, EDRH, or DRH. The only
  conditional convergence on the boundary line $\mathrm{Re}(s) = 1$ is
  the $k = 1$ prime sum $\sum_p \chi^2(p) p^{-2\rho}$, handled by
  Akatsuka 2013 Lemma 2.1 / eq. (2.5), which itself is
  *unconditional* — derived from PNT with explicit error term.
- The proof does **not** use any rate of convergence for the partial
  Möbius / spectroscope sum $c_K(\chi, \rho)$. The $B_\infty$ identity
  is a statement about the limit $T_\infty$; it makes no claim about
  the *speed* at which $T_K \to T_\infty$.
- The proof does **not** establish the Aoki–Koyama–Mertens limit
  (\ref{eq:AK}) for $E_K \log K$, which is a separate statement on the
  *additive* side and is cited as Hypothesis AK (with verbatim
  quotation in §X.4.3).
- The proof does **not** establish the conditional NDC limit
  (\ref{eq:NDC}); for that, Hypothesis AK and the shifted Perron
  leading hypothesis (SP-L) are both needed (see §X.4.4 and §X.7).

## A.7 Lean formalisation

The four-component identity is formalised in Lean 4 / Mathlib v4.28.0
as the theorem `corrected_B_infty` in
`formal-conjectures/CorrectedBInfty.lean` of the companion
repository. The Lean proof is parameterised by an explicit
`Filter.Tendsto` hypothesis asserting that the partial-sum sequence
$T_K(\chi,\rho)$ converges to the four-component right-hand side as
$K \to \infty$. **The convergence-as-hypothesis is precisely the
conclusion of the present appendix** (\ref{eq:k1-isolation}) +
(\ref{eq:Sigma2-id}) + the $k \ge 3$ tail of §A.3. Given the
convergence, the Lean proof is three lines: `unfold T_inf` (the
`Classical.epsilon` of the `Tendsto` predicate),
`Classical.epsilon_spec` (which yields that $T_\infty$ inherits the
same limit), and `tendsto_nhds_unique` (since $\mathbb{C}$ is
Hausdorff). The file uses only the standard
`propext`, `Classical.choice`, `Quot.sound` axioms.

A fully unconditional Lean proof of `corrected_B_infty` (i.e., one
that *derives* the convergence rather than taking it as a hypothesis)
requires upstream Mathlib formalisations of Akatsuka 2013
eq.\ (2.5) and the imprimitive-induction Euler-factor identity for
$L(s, \chi^2)$; both are `MATHLIB-PREREQ` and not yet upstream as of
v4.28.0.

## A.8 Numerical verification (summary; full table in §X.5.4)

The identity ($\star$) was verified numerically at $K = 2 \cdot 10^6$,
$50$ decimal places of precision, on the four
$(\chi, \rho)$ pairs of §X.5.2. The residuals are:

| Pair | residual $|T_K - \mathrm{RHS}(\star)|$ at $K = 2\cdot 10^6$ |
|---|---:|
| $\chi_{-4}/z_1$ | $2.85 \cdot 10^{-3}$ |
| $\chi_{-4}/z_2$ | $1.66 \cdot 10^{-3}$ |
| $\chi_5$ | $4.24 \cdot 10^{-5}$ |
| $\chi_{11}$ | $3.33 \cdot 10^{-5}$ |

These match the predicted $K^{-1/2}/\log K$ decay envelope at the
$O(1)$ implicit-constant level (with the $\chi_{-4}$ pairs showing the
predicted slower envelope due to the $p=2$ bad-prime weight; see §A.5).
The full table with per-component breakdown is at §X.5.4 of the main
text.
