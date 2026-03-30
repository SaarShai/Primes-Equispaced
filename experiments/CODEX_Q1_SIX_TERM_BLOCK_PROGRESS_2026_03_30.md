# Codex Note: Six-Term Mod-6 Block Progress in the `q=1` Range

## Target

For a prime `p` and a block start `m = 2,8,14,...`, define the actual reduced
`q=1` six-term block

`B_{p,m} := sum_{t=0}^5 Delta_{m+t}(p-(m+t))`,

where

`Delta_r(b) := sum_{b/3 < u <= b/2, gcd(u,b)=1} ([ru]_b - u)`.

I do **not** yet have a full analytic proof that `B_{p,m} > 0` for every
admissible pair `(p,m)`. What I do now have is:

- a clean exact reduction of the block to unrestricted floor sums
- an exact continuous six-term main term with a strict positive lower bound
- a rigorous partial theorem in a genuine subrange of `q=1`
- a much sharper exact conjectural surrogate for the full problem

This note is the current best handoff on that route.

---

## 1. Exact Reduction to Unrestricted Window Sums

Define the unrestricted window sum

`E_r(n) := sum_{n/3 < v <= n/2} ([rv]_n - v)`.

Then Möbius inversion gives the exact identity

`Delta_r(b) = sum_{d|b} mu(d) d E_r(b/d)`.

Proof sketch:

- insert `1_{gcd(u,b)=1} = sum_{d|(u,b)} mu(d)`
- write `u = d v`
- use `[r d v]_{d n} = d [r v]_n` with `n = b/d`

So the six-term block is exactly

`B_{p,m} = sum_{t=0}^5 sum_{d|(p-m-t)} mu(d) d E_{m+t}((p-m-t)/d)`.

This isolates the true obstruction: we do not need a vague transport heuristic,
we need control of a six-term combination of explicit unrestricted sums.

---

## 2. Exact Floor-Sum Form and Termwise Bound

Let

- `F_{r,n}(X) := sum_{1 <= v <= X} floor(r v / n)`
- `A(n) := sum_{n/3 < v <= n/2} v`

Then

`E_r(n) = (r-1) A(n) - n ( F_{r,n}(floor(n/2)) - F_{r,n}(floor(n/3)) )`.

This is the exact floor-sum form.

Now define

`I_r := int_(1/3)^(1/2) ({r x} - x) dx`.

Using the Bernoulli-polynomial calculation from the earlier `q=1` note, we have

`I_r = 1/72 + ( B_2({r/2}) - B_2({r/3}) ) / (2r)`,

with `B_2(t) = t^2 - t + 1/6`.

Applying Koksma to

`g_r(x) = 1_(1/3,1/2](x) ({r x} - x)`

gives the rigorous bound

`|E_r(n) - n^2 I_r| <= ((r/3) + 3) n`.

This is not strong enough to close the full problem by itself, but it is a real
theorem and it gives a clean bridge from exact arithmetic to the continuous main
term.

---

## 3. Exact Continuous Six-Term Main Term

For `m = 6k+2`, the six-term continuous block is

`S_I(k) := sum_{t=0}^5 I_{6k+2+t}`.

I simplified this exactly to

`S_I(k) = 1/12 + (180 k^4 + 576 k^3 + 661 k^2 + 329 k + 62) / (24 (2k+1)(3k+1)(3k+2)(6k+5)(6k+7))`.

Hence

`S_I(k) > 1/12`

for every `k >= 0`.

This is the strongest exact analytic fact I have on the block structure itself:
the full mod-`6` continuous block is not barely positive, it is uniformly above
`1/12`.

---

## 4. A Rigorous Partial Theorem in the Actual `q=1` Range

Define the unrestricted actual `q=1` block

`U_{p,m} := sum_{t=0}^5 E_{m+t}(p-(m+t))`.

Write `n := p-m`, so the six denominators are `n,n-1,...,n-5`.

For `m >= 14`, every `I_{m+t}` in the block is nonnegative, so from the exact
continuous lower bound and the termwise Koksma bound we get

`U_{p,m} >= (n-5)^2 S_I((m-2)/6) - sum_{t=0}^5 ( ((m+t)/3)+3 ) (n-t)`.

Using `S_I > 1/12` and simplifying the error sum exactly,

`sum_{t=0}^5 ( ((m+t)/3)+3 ) (n-t) = 2mn - 5m + 23n - 190/3`,

we obtain the explicit bound

`U_{p,m} > (n-5)^2 / 12 - ( 2mn - 5m + 23n - 190/3 )`.

Equivalently,

`12 U_{p,m} > n^2 - (24m + 286) n + 60m + 785`.

So we get a genuine theorem:

### Theorem

If `m = 6k+2 >= 14` and

`n = p-m > (24m + 286 + sqrt((24m+286)^2 - 4(60m+785))) / 2`,

then `U_{p,m} > 0`.

In particular, the simple sufficient condition

`p > 25m + 286`

implies `U_{p,m} > 0`.

This does **not** close the full six-term block problem, but it is a genuine
analytic lower bound on actual `q=1` blocks in a nonempty subrange.

---

## 5. What the Numerics Say About the Full Reduced Block

I rechecked the six-term reduced block numerically and the picture is now much
sharper.

### Global scan facts

From the exact scan:

- up to `p <= 10000`, every one of the `477116` reduced six-term `q=1` blocks
  was strictly positive
- up to `p <= 20000`, every one of the `1762576` reduced six-term `q=1` blocks
  was strictly positive
- the minimum raw block value up to `20000` stayed
  `min B_{p,m} = 7` at `(p,m) = (17,2)`
- the minimum normalized value up to `20000` occurred at `(p,m) = (10631,3542)`
  with
  `B_{p,m} / p^2 ~= 1.58157e-3`

So the block positivity is very robust computationally, but the margin can be
small enough that crude `cp^2` arguments are not the right tool.

### Early `q=1` regime is much cleaner

If `p > 3(m+5)`, then every denominator in the block satisfies `b > 2r`.
In that regime I found:

- every reduced six-term block up to `p <= 10000` was positive
- among those early-regime blocks, the minimum raw value was `25` at `(41,8)`
- the minimum `B_{p,m}/p^2` in that regime was about `6.49e-3` at `(401,128)`

So the hard part is **not** the clean early `q=1` zone. The genuinely small
margins come from the late `q=1` tail.

---

## 6. A Stronger Exact Surrogate: the Unrestricted Block

For the unrestricted actual block

`U_{p,m} := sum_{t=0}^5 E_{m+t}(p-(m+t))`,

I found a striking new pattern:

- up to `p <= 5000`, every unrestricted six-term block was positive
- in fact, every tested block satisfied
  `U_{p,m} >= p - 2`
- equality occurred only at `(p,m) = (17,2)` and `(29,8)` in that scan

This is not yet proved analytically, but it is the sharpest exact surrogate I
have found. If the researchers can prove

`U_{p,m} >= p - 2`

or any comparable linear lower bound, then the remaining work is to control the
Möbius correction from the non-coprime part.

I currently think this unrestricted theorem is one of the best targets on the
table.

---

## 7. Best Next Directions

I would prioritize the following in order.

### Direction A: Prove a six-term cancellation lemma before absolute values

The real missing step is not another termwise estimate. It is a block estimate
of the form

`sum_{t=0}^5 ( E_{m+t}(n) - n^2 I_{m+t} ) = O(n)`

uniformly in `m`.

If that is proved, the continuous block lower bound `> 1/12` becomes strong
enough to force positivity for large blocks after Möbius inversion.

### Direction B: Prove the unrestricted lower bound

The exact scan strongly suggests the theorem

`U_{p,m} >= p - 2`.

That would give a robust linear buffer before the Möbius correction is even
considered.

### Direction C: Focus on the late `q=1` tail

The small margins are not coming from the early `b > 2r` zone. They come from
the late part of `q=1`, where the complementary parameter

`s = b-r = p-2r`

is small. So an exact `s`-side decomposition may be more promising there than
another `r`-side Koksma argument.

---

## Bottom Line

I do not yet have a full proof that every reduced six-term `q=1` block is
positive.

I do now have:

- an exact Möbius reduction to unrestricted window sums
- an exact floor-sum formula
- a rigorous termwise Koksma bound
- an exact six-term continuous block formula with strict lower bound `> 1/12`
- a rigorous positivity theorem in an explicit early subrange of actual `q=1`
- very strong computational evidence for the full reduced block up to `20000`
- a new sharp surrogate conjecture `U_{p,m} >= p - 2`

So the six-term mod-`6` block route is still very much alive. The remaining gap
has become narrower and more explicit: the real target is now a blockwise
cancellation theorem, not another single-term estimate.
