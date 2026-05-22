# The finite-x dynamics of the −1-dominance Chebyshev-bias hierarchy: an independent high-resolution measurement

*Saar Shai (Farey Research Lab). Draft — independent
verification/extension. Experimental-Mathematics / specialist tier.
NOT a confirmed joint deliverable; counterparty unverified.*

> Numerical placeholders are written `{{…}}` and are filled only from
> runs that pass every cross-check in §5. Provenance: `MANIFEST.md`,
> `HASHES.sha256`.

## Abstract

For the prime races `D(x;N,a) = π(x;N,a) − π(x;N,1)`,
`N ∈ {7,8,11,19,23}`, we compute the full **dynamic curve in `x`** on a
50-points-per-decade grid from `10⁶` to `{{Xmax}}`, rather than a
handful of endpoints, with two independently-written sieves that agree
bit-for-bit and that reproduce a prior independently-authored
replication exactly at all nine shared checkpoints. We report, as
finite-range observations: for each `N`, the smallest sampled `x` past
which the non-residue class `−1 (mod N)` is sustainedly the largest
(or top-group) among quadratic non-residues; the Littlewood-type sign
changes of `D(x;N,−1)` ("transient reversals"); and the dominant
log-`x` oscillation wavelength, compared against an independently
computed lowest Dirichlet-`L` zero ordinate `γ_min(N)`. We separate
throughout the theoretical bias ordering, the raw observable, the
finite-range evidence, and the (conditional) asymptotic
interpretation. The conjectured strong "dominance of `−1`" is treated
as a hypothesis under test, not an established fact.

## 1. Background and exact scope (verified sources only)

The Chebyshev bias — quadratic non-residue classes tending to contain
more primes than residue classes — is made precise by **Rubinstein &
Sarnak, *Experimental Mathematics* 3 (1994), no. 3, 173–197**: under
GRH and linear independence (LI) of the zero ordinates, the normalised
race has a limiting logarithmic distribution whose mean is governed by
the square-root–counting term, so non-residues lead. **Aoki & Koyama,
*Journal of Number Theory* 245 (2023) 233–262 (arXiv:2203.12266)**
give, under the Deep Riemann Hypothesis, an explicit asymptotic for the
*magnitude* of the deflection and a Frobenius-class criterion — a new
formulation that renders an inter-class ordering ("hierarchy")
explicit.

The specific strong claim that `−1 (mod N)` *dominates* that hierarchy
is stated in an unpublished preprint of Koyama ("A Hidden Hierarchy …
the Dominance of −1 (mod N)"). We have **not** independently verified
that preprint; every statement traceable only to it is flagged and
treated as a conjecture. This note neither assumes nor asserts it; it
measures the finite-`x` behaviour and states plainly where that
behaviour is and is not consistent with the conjecture.

What this note is **not**: a proof; progress on GRH/DRH/RH; or a
confirmed collaborative deliverable. It is a calibrated, reproducible
measurement.

## 2. Layer separation

- **T (theory, read-only):** §1 + `analysis/THEORY_LAYER.md`.
- **O (observable):** `D(x;N,a)`, integer step function, exactly what
  the sieves count — no modelling.
- **F (finite evidence):** §4, the curve and its measured features.
- **I (asymptotic interpretation):** §6, explicitly fenced; the
  limiting statements concern density as `x→∞` and are never claimed
  to be confirmed by any finite range.

## 3. Method

Two independent dependency-free sieves over `[2,{{Xmax}}]`:
`mr1_sieve.c` (serial, odd-only bit-segmented, absolute-index
bookkeeping) and `mr1_par.c` (range-split pthreads with a deterministic
fixed-order prefix combine). Residues for all `N` tallied per prime;
all `φ(N)` classes snapshotted at each of `{{Ngrid}}` grid points. The
curve resolution is free; only the maximum-`x` pass costs. Full
provenance in `MANIFEST.md`.

## 4. Results (finite-range observations) — Layer F

Per-modulus curve features (filled from the verified run):

| N | −1≡ | NR set (k) | sustained strict-max onset | top-⌈k/2⌉ onset | #sign-changes of D(−1) | last reversal x | end rank |
|---|---|---|---|---|---|---|---|
| 7  | 6  | {3,5,6} (3)              | {{}} | {{}} | {{}} | {{}} | {{}} |
| 8  | 7  | {3,5,7} (3)             | {{}} | {{}} | {{}} | {{}} | {{}} |
| 11 | 10 | {2,6,7,8,10} (5)        | {{}} | {{}} | {{}} | {{}} | {{}} |
| 19 | 18 | {2,3,8,10,12,13,14,15,18} (9) | {{}} | {{}} | {{}} | {{}} | {{}} |
| 23 | 22 | {5,7,10,11,14,15,17,19,20,21,22} (11) | {{}} | {{}} | {{}} | {{}} | {{}} |

Headline qualitative readout (to be stated only post-cross-check):
which `N` show sustained `−1` dominance within `[10⁶,{{Xmax}}]`; which
show it only as "top group"; and `N=23`, for which the conjecture
predicts onset only near `x ≈ e^{33.4} ≈ 3·10¹⁴` — tested directly by
the extension run.

Dominant oscillation wavelength vs independent `γ_min(N)`:

| N | measured Δln x wavelength | 2π/γ_min(N) | γ_min(N) (ours) |
|---|---|---|---|
| 7,8,11,19,23 | {{}} | {{}} | {{}} |

## 5. Cross-checks (every headline number is double-verified)

1. Serial `mr1_sieve` vs parallel `mr1_par`: bit-for-bit on the shared
   grid — `{{ser_par}}`.
2. Gold: exact vs the independently-authored, different-machine
   Phase-1 data (`out2.tsv` & `indep_full.tsv`, themselves mutually
   consistent) at all 9 overlapping checkpoints — `{{gold}}`.
3. Identity (3.1) Dirichlet orthogonality at every snapshot, all
   `(N,x,a)` — worst residual `{{resid}}` (numeric only).
4. `π(x)` anchors at every `10^k` vs published table — `{{anchors}}`.
5. Parallel determinism across thread/chunk counts — `{{det}}`.

## 6. Asymptotic interpretation (fenced — Layer I)

The Layer-T limiting statements are about logarithmic density as
`x → ∞` and are conditional (GRH+LI / DRH). A finite-range curve can
be *consistent* or *inconsistent* with them but cannot confirm them.
A single low-lying zero `½+iγ_min` contributes a log-`x` oscillation
of wavelength `2π/γ_min`; an anomalously small `γ_min(N)` lengthens
the transient and can hold the race reversed until `log x` is large.
For `N=23` Koyama's preprint asserts onset near `log x ≈ 33.4`; we
test this against (i) whether `−1` is still sub-dominant at `1.3·10¹³`
yet resolving toward `3·10¹⁴`, and (ii) whether our measured `N=23`
wavelength matches our independently computed `2π/γ_min(23)`. Any
agreement is reported as consistency, not confirmation.

## 7. Honest verdict

{{One paragraph, written last: exactly which conjecture facets the
finite data supports, which it does not, what remains purely
asymptotic/conditional, and the explicit specialist-tier ceiling.}}

## References

- M. Rubinstein, P. Sarnak. *Chebyshev's bias.* Experimental
  Mathematics 3 (1994), no. 3, 173–197.
- M. Aoki, S. Koyama. *Chebyshev's bias against splitting and
  principal primes in global fields.* J. Number Theory 245 (2023)
  233–262. arXiv:2203.12266.
- S. Koyama. *A Hidden Hierarchy of Chebyshev's Bias and the
  Dominance of −1 (mod N).* Unpublished preprint — **cited as a
  conjecture; not independently verified.**
