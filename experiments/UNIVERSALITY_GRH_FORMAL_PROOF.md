# Universality under GRH+LI: formalization, conditional proof, and gap analysis

> Status: the target universality claim is not proved by GRH+LI alone. The explicit-formula reduction is standard, but the off-resonance and peak-location steps require additional quantitative hypotheses on the subset of primes.

## 1. Target statement

Let $S$ be an infinite subset of primes and, for $X \ge 2$, write

$$
S_X := \{p \in S : p \le X\}.
$$

Define the truncated spectroscope

$$
A_X(\gamma) := \sum_{p \in S_X} \frac{M(p)}{p} e^{-i\gamma \log p},
 \qquad
F_X(\gamma) := \gamma^2 |A_X(\gamma)|^2.
$$

Let $\rho_j = \tfrac12 + i\gamma_j$ be a nontrivial zero of $\zeta(s)$.

The target claim from the sketch is:

> For each fixed $j$, there is a constant $C_j$ such that, for all sufficiently large $X$, the function $F_X$ has a local maximum $\tilde\gamma_{j,X}$ with
> $$
> |\tilde\gamma_{j,X} - \gamma_j| \le \frac{C_j}{\log X}.
> $$

This note does **not** prove that claim from GRH+LI alone. What it does prove is the standard explicit-formula reduction, then a conditional peak-stability theorem showing exactly what extra estimate is missing.

## 2. Hypotheses and conventions

We separate the hypotheses precisely.

- **GRH**: every nontrivial zero of $\zeta(s)$ has real part $1/2$.
- **LI**: the positive ordinates $\gamma_1,\gamma_2,\dots$ of the nontrivial zeros are linearly independent over $\mathbb Q$.
- **Simple zeros**: under the standard LI convention used in prime number races, repeated ordinates are excluded, so the zeros are simple and the residues $1/\zeta'(\rho)$ are well-defined.
- **Truncation convention**: every zero sum is interpreted symmetrically, first with height cutoff $|\Im \rho| \le T$, and only then with $T \to \infty$ or with a smooth cutoff.

The argument below uses the standard explicit formula for the Mertens summatory function

$$
M(x) := \sum_{n \le x} \mu(n),
$$

as obtained by Perron inversion of $1/\zeta(s)$; see Iwaniec-Kowalski, *Analytic Number Theory*, Section 5.5, and Montgomery-Vaughan, *Multiplicative Number Theory I: Classical Theory*, Chapter 12.

## 3. Normalization correction

The proof sketch in the prompt writes the resonant main term as

$$
c_j \sum_{p \in S_X} \frac{1}{p}.
$$

That is not the correct normalization for the standard Mertens explicit formula.

Under GRH and simple zeros, the residue at a zero $\rho$ is

$$
\operatorname{Res}_{s=\rho} \frac{x^s}{s \zeta(s)} = \frac{x^\rho}{\rho \zeta'(\rho)}.
$$

Therefore, after dividing by $p$ and inserting the phase $e^{-i\gamma_j \log p}$, the $\rho_k = \tfrac12 + i\gamma_k$ contribution is

$$
\frac{p^{\rho_k}}{p} e^{-i\gamma_j \log p}
= p^{-1/2 + i(\gamma_k - \gamma_j)}.
$$

So the resonant term at $k=j$ is

$$
c_j \sum_{p \in S_X} p^{-1/2},
 \qquad
c_j := \frac{1}{\rho_j \zeta'(\rho_j)}.
$$

This is the correct analogue of the sketch. The growth rate is different from the displayed $\sum 1/p$, but the logical issue is the same: one needs a quantitative bound showing that the off-resonant terms are small compared with the resonant one.

If one really wants a coefficient $1/p$ rather than $p^{-1/2}$, then one must change the observable, not just the proof.

## 4. Step 1: explicit formula with truncation

### Statement

Assume GRH and simple zeros. For each $x \ge 2$ and each truncation height $T \ge 2$, the standard explicit formula gives

$$
M(x)
=
-2
+
\sum_{|\gamma| \le T} \frac{x^\rho}{\rho \zeta'(\rho)}
+
E_M(x;T),
$$

where $\rho = \tfrac12 + i\gamma$ runs over the nontrivial zeros of $\zeta(s)$.

The remainder $E_M(x;T)$ is the usual truncation error coming from Perron inversion and contour shifting. Its exact shape depends on the smoothing convention, but in every standard version it can be made lower order by choosing the cutoff smoothly and taking $T$ sufficiently large.

### Proof sketch

Start from Perron's formula

$$
M(x)
=
\frac{1}{2\pi i}
\int_{c-iT}^{c+iT} \frac{x^s}{s\zeta(s)} \, ds
 + \text{(Perron error)},
 \qquad c>1.
$$

Shift the contour left. The poles encountered are:

- the pole at $s=0$ coming from the factor $1/s$;
- the poles at the nontrivial zeros $\rho$ of $\zeta(s)$;
- the trivial-zero contribution from $s=-2,-4,\dots$.

The residue at $s=0$ is $1/\zeta(0) = -2$, which gives the constant term $-2$.
The residue at each simple zero $\rho$ is $x^\rho / (\rho \zeta'(\rho))$.
The trivial-zero residues and the truncated vertical integral are absorbed into $E_M(x;T)$.

This is the standard explicit formula. The sum over zeros is not absolutely convergent, so the truncation or smoothing is essential.

### Logical status

- **GRH**: used to place all nontrivial zeros on the critical line.
- **LI**: not needed for the residue computation itself, but it implies simplicity in the standard prime-race convention.
- **Unconditional**: the Perron setup and residue calculation are standard once one accepts the explicit formula framework.

## 5. Step 2: substitute into the spectroscope

Fix $X$ and write

$$
A_X(\gamma_j)
=
\sum_{p \in S_X} \frac{M(p)}{p} e^{-i\gamma_j \log p}.
$$

Insert the truncated explicit formula for $M(p)$:

$$
A_X(\gamma_j)
=
-2 \sum_{p \in S_X} p^{-1} e^{-i\gamma_j \log p}
+
\sum_{|\gamma_k| \le T} c_k
 \sum_{p \in S_X} p^{-1/2 + i(\gamma_k - \gamma_j)}
+
\mathcal E_{X,T}(\gamma_j),
$$

where

$$
c_k := \frac{1}{\rho_k \zeta'(\rho_k)}
$$

and $\mathcal E_{X,T}(\gamma_j)$ denotes the accumulated truncation error after summing over $p \in S_X$.

The constant term $-2 \sum p^{-1} e^{-i\gamma_j \log p}$ is lower order compared with the resonant $p^{-1/2}$ contribution and can be absorbed into the error once the truncation is fixed.

Separating the resonant zero $k=j$ gives

$$
A_X(\gamma_j)
=
 c_j \sum_{p \in S_X} p^{-1/2}
+
\sum_{k \ne j} c_k \sum_{p \in S_X} p^{-1/2 + i(\gamma_k - \gamma_j)}
+
\text{(lower-order terms)}.
$$

This is the corrected version of Step 2 in the sketch.

### Logical status

- **GRH**: used in the form of the explicit formula.
- **Simple zeros**: used to write the residues as $1/(\rho \zeta'(\rho))$.
- **Unconditional algebra**: the separation into resonant and off-resonant pieces is purely formal once the explicit formula is accepted.

## 6. Step 3: on-resonance growth

The resonant term is

$$
c_j \sum_{p \in S_X} p^{-1/2}.
$$

Because $p^{-1/2} \ge p^{-1}$, the assumption

$$
\sum_{p \in S} \frac{1}{p} = \infty
$$

implies

$$
\sum_{p \in S_X} p^{-1/2} \to \infty.
$$

So the resonant contribution diverges for every infinite $S$ satisfying the hypothesis in the prompt.

If one takes $S$ to be all primes up to $X$, then the prime number theorem gives the sharper asymptotic

$$
\sum_{p \le X} p^{-1/2} \sim \frac{2\sqrt X}{\log X},
$$

but the theorem as stated does not require a density assumption on $S$, so divergence is the only safe universal claim.

### Logical status

- **Unconditional** once Step 2 is accepted.
- The specific $\log\log X$ growth in the sketch is not the correct growth for the standard Mertens observable.

## 7. Step 4: off-resonance terms

This is the first serious gap.

The sketch asserts that for $k \ne j$ the terms

$$
\sum_{p \in S_X} p^{-1/2 + i(\gamma_k - \gamma_j)}
$$

are $o\!\left(\sum_{p \in S_X} p^{-1/2}\right)$ because the phases are equidistributed.

That conclusion does not follow from LI alone.

### Why LI is not enough

LI is a statement about the ordinates $\gamma_k$ themselves. It does **not** give a quantitative estimate for prime sums over an arbitrary subset $S$.

To make Step 4 rigorous one would need an additional hypothesis of the form

$$
\tag{QD}
\max_{k \ne j}
\left|
\sum_{p \in S_X} p^{-1/2 + i(\gamma_k - \gamma_j)}
\right|
=
o\!\left(\sum_{p \in S_X} p^{-1/2}\right),
 \qquad X \to \infty.
$$

This is a genuine quantitative phase-cancellation hypothesis. It is not a consequence of GRH+LI as stated.

### Where Weyl and Erdos-Turan actually enter

Weyl's criterion and the Erdos-Turan inequality are useful only after one has an exponential-sum bound. They convert such a bound into discrepancy control. They do **not** create the bound.

So the logic

1. LI,
2. therefore equidistribution,
3. therefore cancellation over arbitrary $S$

is not valid.

### Logical status

- **Gap**.
- **LI** is insufficient by itself.
- To close Step 4, one needs an additional distribution hypothesis on $S$ or a separate exponential-sum estimate for the particular prime subset under consideration.

## 8. Step 5: signal/noise ratio

Under the additional hypothesis (QD),

$$
A_X(\gamma_j)
=
 c_j \sum_{p \in S_X} p^{-1/2} \, (1 + o(1)),
$$

and therefore

$$
\frac{\text{signal}}{\text{noise}} \to \infty.
$$

This is the point where the sketch wants to conclude that the resonant zero dominates.

But note carefully:

- the conclusion is **conditional on (QD)**;
- the proof is not valid if one only assumes GRH+LI;
- and the ratio depends on the actual subset $S$, not just on the zero ordinates.

### Logical status

- **Conditional** on Step 4.
- Not proved from GRH+LI alone.

## 9. Step 6: local maxima near zeros

The last step is also nontrivial.

Pointwise divergence at $\gamma_j$ does not by itself imply that $F_X$ has a local maximum within the claimed distance.

### What is actually needed

Let

$$
B_X(\delta)
:=
\sum_{p \in S_X} a_p e^{-i\delta \log p},
 \qquad a_p > 0,
$$

denote the resonant main term after factoring out the phase $e^{-i\gamma_j\log p}$ and the coefficient $c_j$.
Then:

1. $|B_X(\delta)| \le B_X(0)$ by the triangle inequality.
2. The maximum at $\delta=0$ is strict as soon as the support contains at least two distinct frequencies.
3. If the perturbation from the off-resonant terms and truncation is small in a $C^2$ sense, then the strict maximum persists under perturbation.

Thus a local maximum near $\gamma_j$ follows from a standard stability argument **provided** one has a quantitative $C^2$ control on the error.

### Why the scale $O(1/\log X)$ is not automatic

The $O(1/\log X)$ localization scale is only natural if the logarithmic spread of the support of $S_X$ is comparable to $\log X$.
For an arbitrary subset $S$, that need not be true. If $S_X$ is concentrated in a narrow log-window, the peak can be much broader.

So the claimed scale is not a formal consequence of GRH+LI; it requires an additional spread hypothesis on $S_X$.

### Effect of the $\gamma^2$ factor

The factor $\gamma^2$ is smooth and positive on any neighborhood of a fixed zero $\gamma_j > 0$.
It does not destroy a local maximum once one exists, but it is not literally "uniform" in $j$:

- near a fixed zero, its logarithmic variation is lower order;
- uniformly as $j \to \infty$, it contributes a nontrivial drift and must be controlled explicitly.

So the $\gamma^2$ compensation is harmless for a fixed-zero perturbation argument, but it is not a free pass for a uniform-in-$j$ theorem.

### Logical status

- **Conditional** on a quantitative $C^2$ dominance estimate and on a support-spread hypothesis.
- **Gap** for the exact $O(1/\log X)$ statement as written in the prompt.

## 10. What can actually be proved

The clean, rigorous statement is the following.

> **Proposition (conditional peak stability).**  
> Assume GRH, LI, the standard truncated explicit formula for $M(x)$, and the quantitative off-resonance estimate (QD) together with a log-spread hypothesis for $S_X$. Then, for each fixed zero $\gamma_j$, the truncated spectroscope $F_X(\gamma)$ has a local maximum at distance $O(1/\log X)$ from $\gamma_j$.

The proof is the combination of:

- the explicit-formula decomposition in Steps 1-2;
- the dominance of the resonant term in Step 3;
- the smallness of the off-resonant terms in Step 4;
- the perturbative peak-stability argument in Step 6.

This proposition is the strongest rigorous form of the sketch.

## 11. Why the original theorem is still open

The original theorem in the prompt would require all of the following to be true from GRH+LI alone:

1. a fully justified zero-sum truncation that can be swapped with the prime sum;
2. a quantitative equidistribution/cancellation statement for arbitrary subsets $S$ of primes;
3. a $C^2$-level perturbation argument with a uniform $O(1/\log X)$ location bound;
4. a uniform control of the $\gamma^2$ factor across all zeros.

Items 2 and 3 are genuine missing inputs.

So the correct mathematical status is:

- the explicit formula part is standard;
- the resonance decomposition is formal and correct after normalization;
- the universal local-maxima conclusion is not proved from GRH+LI alone.

## 12. Gap analysis

### a) The explicit formula for $M(p)$ involves truncation and error terms

Handled as follows:

- use Perron inversion for $1/\zeta(s)$;
- shift the contour past the poles;
- keep a symmetric truncation at height $T$;
- absorb the tail, trivial zeros, and the vertical integral into $E_M(x;T)$.

This is standard, but it must be stated explicitly because the zero sum is not absolutely convergent.

### b) The equidistribution argument needs quantitative bounds

Correct. The step

$$
\sum_{p \in S_X} p^{-1/2 + i\alpha} = o\!\left(\sum_{p \in S_X} p^{-1/2}\right)
$$

for arbitrary $S$ is not a consequence of LI. One needs a separate exponential-sum estimate or a specific pseudorandomness property of $S$.

### c) Pointwise divergence does not by itself produce local maxima

Correct. A local maximum requires a neighborhood comparison, not just a large value at one point.
The rigorous route is a $C^2$-stability argument for strict maxima.

### d) Convergence of the sum over zeros needs justification

Correct. The zero sum must be interpreted through truncation or smoothing. Under GRH and simple zeros, the residues are well-defined, but one cannot naively interchange the zero sum with the prime sum without a convergence argument.

### e) The role of the simple-zeros assumption

If LI is adopted in the standard form used in prime number races, then simple zeros are automatic.
Without simple zeros, the explicit formula acquires higher-order residue terms and the coefficient $1/(\\rho \\zeta'(\\rho))$ is no longer the whole story.

### f) The normalization mismatch in the sketch

The sketch uses $\\sum 1/p$ where the standard Mertens explicit formula gives $\\sum p^{-1/2}$ after dividing by $p$.
That mismatch must be fixed before any fully rigorous writeup can be claimed.

### g) The $O(1/\\log X)$ localization scale needs support spread

The exact window size depends on the log-diameter of the chosen prime subset $S_X$.
For arbitrary $S$, the claimed scale is not automatic.

## 13. References

- H. Iwaniec and E. Kowalski, *Analytic Number Theory*, Section 5.5.
- H. L. Montgomery and R. C. Vaughan, *Multiplicative Number Theory I: Classical Theory*, Chapter 12.
- J. Kuipers and H. Niederreiter, *Uniform Distribution of Sequences*.
- P. Garrett, "Riemann's Explicit/Exact Formula" (public lecture notes).

## 14. Summary table

| Major step | Logical status | Hypotheses used | Notes |
|---|---|---|---|
| Target theorem statement | Open / not proved | GRH + LI were requested | As stated, the theorem is stronger than what the standard explicit formula yields |
| Step 1: explicit formula | Proved conditionally | GRH, simple zeros, standard Perron truncation | Standard residue computation for $1/\\zeta(s)$ |
| Step 2: resonance decomposition | Proved conditionally | Step 1, GRH | Correct normalization gives $p^{-1/2}$, not $1/p$ |
| Step 3: on-resonance growth | Proved (with normalization correction) | Infinite $S$ with $\\sum_{p \\in S} 1/p = \\infty$ | Divergence is clear; the sketch's $\\log\\log X$ rate is not the standard one |
| Step 4: off-resonant cancellation | Gap | Would need (QD) or similar | LI alone does not imply the needed bound |
| Step 5: signal/noise ratio | Conditional | Step 4 | Follows once the off-resonant terms are $o$ of the resonant term |
| Step 6: local maxima | Conditional / gap | Step 5 plus a $C^2$ stability estimate and log-spread | The $O(1/\\log X)$ window is not automatic for arbitrary $S$ |
| $\\gamma^2$ compensation | Proved as a smooth perturbation | Fixed zero $\\gamma_j > 0$ | Harmless locally, but not uniform in $j$ |
