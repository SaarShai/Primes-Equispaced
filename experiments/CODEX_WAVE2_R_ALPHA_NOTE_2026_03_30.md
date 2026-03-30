# Codex Wave 2 Note: Exact Formula for `e(q)`, `R(N)`, and `alpha`

## Goal
I followed Goal 1 from `CODEX_HANDOFF_WAVE2.md`, but I attacked the `alpha` side first.
The main new output is an exact closed form for the denominator error term
`e(q)`, which gives a much cleaner exact formula for `R(N)` and therefore for
the regression slope `alpha`.

This does not close `B >= 0` by itself, but it sharpens the structure of Part II
and suggests a better route than the current norm-only ratio.

---

## 1. Exact formula for the denominator error `e(q)`

In `ALPHA_POSITIVE_PROOF.md`, the key quantity is

`e(q) = S_2(q)/q^2 - phi(q)/3`,

where

`S_2(q) = sum_{1 <= a <= q-1, gcd(a,q)=1} a^2`.

Using Mobius inversion on the coprimality condition:

`S_2(q) = sum_{d|q} mu(d) d^2 sum_{m <= q/d} m^2`.

Since

`sum_{m <= M} m^2 = M(M+1)(2M+1)/6`,

substituting `M = q/d` and simplifying gives the exact identity

`S_2(q) = q^2 phi(q)/3 + (q/6) sum_{d|q} mu(d) d`.

Therefore:

`e(q) = (1/(6q)) sum_{d|q} mu(d) d`.

Equivalently,

`e(q) = (1/(6q)) prod_{ell|q} (1-ell)`.

So `e(q)` is completely explicit and multiplicative.

Immediate consequences:

- For prime `p`, `e(p) = -(p-1)/(6p)`.
- The sign of `e(q)` is `(-1)^{omega(rad(q))}`.
- Square factors suppress the magnitude because the numerator only sees `rad(q)`.

I independently verified this exact formula numerically for every `2 <= q <= 20`.

---

## 2. Exact formula for `R(N)`

The note `ALPHA_POSITIVE_PROOF.md` defines

`R(N) = sum_{f in F_N} f^2 - n/3 = 1/3 + sum_{q=2}^N e(q)`.

Substituting the exact formula for `e(q)` and swapping the order of summation gives:

`R(N) = 1/6 + (1/6) sum_{d <= N} mu(d) H_{floor(N/d)}`,

where `H_m = sum_{j <= m} 1/j` is the harmonic number.

Swapping the harmonic sum one more time gives an equally useful form:

`R(N) = 1/6 + (1/6) sum_{m <= N} M(floor(N/m))/m`.

This is the cleanest formula I found. It shows that `R(N)` is a weighted
Mertens-harmonic average, not a vague denominator-error remainder.

I also get the Dirichlet series:

`sum_{q >= 1} e(q) q^{-s} = zeta(s+1) / (6 zeta(s))`

for `Re(s) > 1`.

This is a useful structural fact on its own. It means the `R` side of the
argument is directly tied to `1/zeta(s)`, so the same zero structure that shows
up elsewhere in the project is already present in the `alpha` term.

---

## 3. Exact formula for `alpha`

From `ALPHA_POSITIVE_PROOF.md`,

`Cov(D,f) = 1/(12n) - sum D^2/(2n^2) - R/2`.

Also

`sum f = n/2`

and

`sum f^2 = n/3 + R`,

so

`Var(f) = (1/n) sum (f-1/2)^2 = 1/12 + R/n`.

Writing

`C_W(N) = N * old_D_sq / n^2`,

we have

`sum D^2/(2n^2) = C_W(N)/(2N)`.

Therefore the regression slope has the exact form

`alpha(N) = [1/(12n) - C_W(N)/(2N) - R(N)/2] / [1/12 + R(N)/n]`.

Equivalently:

`alpha(N) = [-6 R(N) + 1/n - 6 C_W(N)/N] / [1 + 12 R(N)/n]`.

This is the cleanest exact expression I found for `alpha`.

---

## 4. Consequence: `alpha` is essentially `-6R`

Since `n ~ (3/pi^2) N^2`, the denominator correction `12R/n` is tiny, and the
error term `1/n - 6 C_W(N)/N` is `O(C_W(N)/N)`.

So:

`alpha(N) = -6 R(N) + O(C_W(N)/N)`.

I independently checked this by exact Farey computation for

`N = 12, 18, 42, 70, 106, 198`.

The results are:

| `N` | exact `alpha` | `-6R(N)` | ratio `alpha/(-6R)` |
|-----|---------------|----------|----------------------|
| 12  | 1.4298        | 1.4301   | 0.9998               |
| 18  | 2.3015        | 2.2839   | 1.0077               |
| 42  | 3.8955        | 3.8952   | 1.0001               |
| 70  | 4.5557        | 4.5660   | 0.9977               |
| 106 | 5.7721        | 5.7812   | 0.9984               |
| 198 | 10.0580       | 10.0589  | 0.9999               |

So empirically the approximation is already excellent in the small range.

This is the main conceptual takeaway of the note:

`alpha` is not a mysterious regression artifact; it is essentially a renormalized
weighted Mertens average.

---

## 5. Why this matters for the `B >= 0` proof

The current Wave 2 handoff suggests bounding

`r_CS(p) = 2 ||D_err|| sqrt(C') / (alpha (C'+1))`

by explicit constants.

The exact `alpha` formula changes how I think about this.

### 5.1. The good news

Along the relevant subsequence `p` with `M(p) = -3`, my computation using

`R(N) = 1/6 + (1/6) sum_{m <= N} M(floor(N/m))/m`

shows:

- `R(p-1) < 0` for every tested `M(p) = -3` prime up to `p = 50,000`
- the least-negative case is the first one, `p = 13`, with `R(12) = -0.23835...`

So on this subsequence, `alpha` is not merely positive; it has real margin.

### 5.2. The caution

This exact formula also suggests that the current Part II scaling

`alpha ~ N/log N`

is not the right structural description.

The exact identity says the growth of `alpha` is controlled by `R(N)`, hence by a
weighted Mertens-harmonic sum. That may well grow, but it is a very different object
from the linear-in-`N` lower bound currently asserted in `ELMARRAKI_CORRECTION.md`.

So if the researchers want a fully explicit proof of `r_CS(p) < 1`, I strongly
recommend rewriting the `alpha` side around the exact `R(N)` formula rather than
the present heuristic `N/log N` argument.

---

## 6. A likely obstruction to the pure Cauchy-Schwarz route

This is not yet a theorem, but it is the main strategic warning I would pass on.

We have

`||D_err||^2 = old_D_sq - alpha^2 n Var(f)`.

Now

`old_D_sq = n^2 C_W(N) / N`,

which is of order `N^3 C_W(N)`, while the removed linear component is of order

`alpha^2 n Var(f)`,

which is only order `alpha^2 N^2`.

So unless `alpha` itself is as large as about `sqrt(N C_W(N))`, the regression step
does not shrink `||D_err||` by a full order of magnitude. In other words, the raw
Cauchy-Schwarz envelope is still likely much too large unless one also uses signed
cancellation.

That matches the empirical feel of the current project:

- the signed correction seems to behave much better than its norm envelope
- the real object is the sign of the Abel correction, not the size of the
  Cauchy-Schwarz majorant

So I now think the strongest route is:

1. use the exact `R(N)` formula to clean up `alpha`,
2. but do not expect a pure norm-only proof to finish Part II,
3. instead attack the sign of the Abel correction more directly.

---

## 7. What I would hand the researchers as the usable result

### New exact lemmas

1. `e(q) = (1/(6q)) sum_{d|q} mu(d) d`
2. `R(N) = 1/6 + (1/6) sum_{d <= N} mu(d) H_{floor(N/d)}`
3. `R(N) = 1/6 + (1/6) sum_{m <= N} M(floor(N/m))/m`
4. `alpha(N) = [-6R(N) + 1/n - 6 C_W(N)/N] / [1 + 12 R(N)/n]`

### Strategic consequence

The `alpha` term is now transparent. The remaining difficulty is not positivity
of `alpha`, but the signed control of the residual correction.

### Suggestion for the paper

Even if this does not close `B >= 0` immediately, I think these lemmas are worth
including in the project notes or even in the paper:

- they are clean,
- they connect the regression picture to the Mertens function directly,
- and they give a more honest and more structural account of why `alpha` is positive.

