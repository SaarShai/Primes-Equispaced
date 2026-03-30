# Codex Wave 2: Suggested Next Directions After the `R/alpha` Calculation

## Main conclusion from this pass
I do not think the best path is to keep pushing the current norm-only Part II
argument exactly as written.

The new exact formulas

- `R(N) = 1/6 + (1/6) sum_{m <= N} M(floor(N/m))/m`
- `alpha(N) = [-6R(N) + 1/n - 6 C_W(N)/N] / [1 + 12R(N)/n]`

make the `alpha` side much cleaner, but they also suggest that the real difficulty
is the signed Abel correction, not the positivity of `alpha`.

So my recommendations split into one near-term proof route and several secondary
research directions.

---

## 1. Best proof route now: attack the sign of the Abel correction directly

For `M(p) = -3`, the exact identity is

`B = C - 2 Term2`,

so `B > 0` follows immediately from `Term2 < C/2`, and even more strongly from
`Term2 < 0`.

The data in `CORRECTION_BOUND_M3.md` says:

- `Term2/C > 0` only at `p = 13, 19`
- `Term2/C < 0` for every tested `M(p) = -3` prime from `p = 43` onward

That is a much sharper target than the Cauchy-Schwarz envelope.

### Concrete next step

Define the Abel-step kernels

`K_m(p) = sum_{f in F_{p-1}} S(f,m) delta(f)`.

Then rewrite `Term2` entirely in terms of the signed increments of `K_m(p)` as
`m = floor(N/k)` changes.

What I would try next:

1. compute exact formulas for `K_1(p), K_2(p), K_3(p)`
2. prove their signs
3. show the early negative kernels dominate the later tail

This is the most promising way I can see to turn the observed `Term2 < 0` into
an actual proof.

---

## 2. Cleaner `alpha` route: prove a lower bound on `R(N)` on the `M(p) = -3` subsequence

The new formula

`R(N) = 1/6 + (1/6) sum_{m <= N} M(floor(N/m))/m`

suggests a more targeted subproblem:

prove that for `N = p-1` with `M(p) = -3`, one has

`R(N) <= -c_0`

for some explicit `c_0 > 0`.

Numerically, up to `p = 50,000`, the worst case is the first one:

- `p = 13`, `R(12) = -0.23835...`

So the conjectural statement is very plausible:

`R(p-1) <= R(12) < -0.23`

for every prime `p` with `M(p) = -3`.

If true, this would immediately give a clean positive lower bound for `alpha`
through the exact formula.

### How I would attack it

Use the first few terms of

`sum_{m <= N} M(floor(N/m))/m`

explicitly:

- `m = 1` contributes `-2`
- `m = 2, 3, 4, ...` can be studied on the `M(p) = -3` subsequence

This feels much more concrete than the present broad asymptotic argument.

---

## 3. Finite verification plus explicit tail

If the direct-sign route produces any explicit asymptotic inequality at all, the
remaining finish should be a hybrid proof:

1. prove `Term2 < 0` or `Term2/C <= eta < 1/2` for all `p >= P_0`
2. compute the finitely many `M(p) = -3` primes below `P_0`

This is the right style for the current project. It does not need a perfectly
sharp asymptotic constant, only an explicit one.

I would not aim first for a proof valid from `p = 43` analytically. A moderate
explicit threshold plus finite verification is enough.

---

## 4. New structural direction: add the `R`-Dirichlet series to the project

The exact Dirichlet series

`sum_{q >= 1} e(q) q^{-s} = zeta(s+1)/(6 zeta(s))`

is valuable beyond the immediate `B >= 0` problem.

Why it matters:

- it ties the regression slope `alpha` to the same zeta-structure driving the
  rest of the project,
- it gives a clean, publication-worthy standalone lemma,
- it may explain oscillations in `alpha` and `R` by the zeros of `zeta(s)`.

This could improve the paper even if the main proof still needs one more ingredient.

---

## 5. A concrete computational-mathematical direction

The researchers already have strong data for `correction/C` on the `M(p) = -3`
subsequence. The next computational question I would ask is more structured:

for each such prime, record not just `Term2/C`, but the first few Abel-step
contributions separately.

Suggested table:

- `k = 1` block contribution
- `k = 2` block contribution
- `k = 3` block contribution
- remaining tail contribution

If the sign transition at `p = 43` comes from one or two specific low-step blocks,
that is exactly the kind of pattern that often becomes provable.

---

## 6. How this could improve the paper even before the full proof closes

I would add a short note or appendix-level result around the `R` term:

1. exact denominator formula for `e(q)`
2. harmonic-Mertens representation of `R(N)`
3. exact formula for `alpha`

This gives the paper a cleaner internal story:

- `B` is hard because of a signed residual,
- `alpha` itself is not mysterious,
- the obstruction is localized in the Abel correction

That is a stronger and more honest narrative than treating `alpha` as a black-box
positive quantity with a heuristic `N/log N` growth law.

---

## 7. My ranking of next steps

### Highest priority

1. Rewrite Part II around the exact `R/alpha` formulas.
2. Study the sign of the Abel-step kernels `K_m(p)`.
3. Aim for `Term2 < 0` for all `M(p) = -3` primes beyond an explicit threshold.

### Medium priority

4. Prove a uniform negative bound on `R(p-1)` on the `M(p) = -3` subsequence.
5. Add the `e(q)` / `R(N)` lemmas to the paper or core notes.

### Longer-range

6. Study the Dirichlet-series / zero-structure of `R(N)` and `alpha(N)`.
7. Look for a spectral interpretation of the Abel correction itself.

