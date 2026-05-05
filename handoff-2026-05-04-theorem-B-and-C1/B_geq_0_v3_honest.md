---
title: "B ≥ 0 — v3 honest assessment: prior closure attempts FAIL, conjecture itself in doubt"
type: derivation
domain: research
tier: working
confidence: 0.05
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - /Users/saar/Farey 4.7 solutions/B_geq_0_FULL_CLOSURE.md (prior — has gaps)
  - /Users/saar/Farey 4.7 solutions/B_geq_0_extra_high_attempt.md (prior — algebra error in §7)
  - /Users/saar/Farey 4.7 solutions/bern_saw_extend.tsv (this session, p ≤ 4999)
  - /Users/saar/Farey 4.7 solutions/bern_saw_verify_failures.py (exact-rational check)
  - /Users/saar/Farey 4.7 solutions/bern_verify_3299.py (exact-rational check)
supersedes:
  - /Users/saar/Farey 4.7 solutions/B_geq_0_FULL_CLOSURE.md
  - /Users/saar/Farey 4.7 solutions/B_geq_0_extra_high_attempt.md
superseded-by: null
tags: [farey, B-sign, bern-saw, refutation, numerical-counterexamples]
---

# Bottom line

**The Bern/Saw closure route is REFUTED in its current form.** Numerical
verification at exact-rational precision shows that the conjectured inequality
`|Saw(p)| ≤ Bern(p)` (which is equivalent, up to a positive constant, to
`B(p) ≥ 0` under the decomposition stated in the prior document) **fails for
42 out of 665 primes in the range 11 ≤ p ≤ 4999**.

Worse: the algebraic claim `Bern(p) > 0 unconditionally` from §7 of
`B_geq_0_extra_high_attempt.md` is wrong. The proof there reduces Bern to a
"Chebyshev sum form" but the reduction silently assumes
`Σ_{f ∈ F_{p−1}} f·(f − 1/2) = 0`, which is false in general (it equals
`Σ f² − (1/2)·Σ f` and only the second term simplifies under reflection
symmetry). Exact-rational computation at p = 3299 gives `Bern(3299) =
−0.1192…` — i.e. `Bern` itself is sometimes **negative**.

So this session does NOT deliver an unconditional `|Saw| ≤ (1−ε)·Bern` bound.
Instead it delivers something more important: a refutation of the prior
session's optimistic confidence, together with a list of explicit primes that
witness the failure. If the original `B(p) ≥ 0` conjecture (from the source
paper) is in fact correct, then the Bern/Saw decomposition cannot be the right
bookkeeping for it; if the decomposition IS the right bookkeeping, then the
conjecture is false at p ∈ {1399, 1409, 1423, 1427, 1429, 2633, 2647, 2657,
2659, 2663, 3163, …, 4937}.

**Confidence the Bern/Saw split closes B ≥ 0 unconditionally:**
prior 0.45 → **0.02**.

# 1. What is verified vs what is open (table)

| Statement | Status | Evidence |
|---|---|---|
| `Σ_{f ∈ F_{p−1}} f = n/2` | **Verified** algebraically (reflection f↔1−f and 0,1 ∈ F) | trivial |
| `Σ_{f ∈ F_{p−1}} f² = n/4` | **FALSE in general** | Σ(1−f)² = Σf² is a tautology, not a constraint |
| `Σ_{f ∈ F_{p−1}} f(f − 1/2) = 0` | **FALSE in general** (claimed in prior §7) | computational, see below |
| `Bern(p) = Σ D(f)(f−1/2)` reduces to `(1/(n−1)) Σ (i − (n−1)/2)(f_i − 1/2)` | **FALSE in general** | exact-rational diff at p=3299 is ≈ 275521 |
| `Bern(p) > 0` for all primes p | **FALSE** | exact-rational `Bern(3299) = −0.1192…`, also p ∈ {3301, 3307, 3319} |
| Identity `B(p) · n′²/2 = Bern(p) − Saw(p)` | **Not re-verified this session** — prior algebra not audited; see Open Q1 |
| `|Saw(p)| ≤ Bern(p)` | **FALSE** for 42/665 primes p ≤ 4999 | float `bern_saw_extend.tsv`, exact-verified for cluster {1399…1429, 3299} |
| `B(p) ≥ 0` for all p | **OPEN, possibly false** — depends on Open Q1 | see §3 |
| `T_h(p) := Σ D(f) e(hpf)` bound `Σ_h |T_h|/h = O((log p)^{1−ε})` | **OPEN, untouched this session** | not attacked rigorously by anyone |

# 2. Numerical evidence (exact rationals where flagged)

Code: `bern_saw_extend_5k.py` (float64) over primes 11 ≤ p ≤ 4999, plus
exact-rational `bern_saw_verify_failures.py` and `bern_verify_3299.py`.

* Total primes computed: **665**
* `B_raw := Bern − Saw > 0` count: **623 / 665** (= 93.7%)
* Counterexamples (`B_raw ≤ 0`): **42** primes
  * Smallest: p = 1399 (B_raw ≈ −5.3·10⁻⁴, ratio 1.0017)
  * Most extreme finite ratio: p = 4889 (|Saw|/Bern ≈ 7.05)
  * Bern itself negative: p ∈ {3299, 3301, 3307, 3319}
  * Most negative B_raw: p = 3299 (B_raw ≈ −0.4351)
* All failure primes (B_raw ≤ 0):
  ```
  1399 1409 1423 1427 1429
  2633 2647 2657 2659 2663
  3163 3251 3253 3257 3259 3271 3299 3301 3307 3313 3319 3323 3329 3331 3343 3359
  3433 3449 3457 3461 3463 3467
  4861 4871 4877 4889 4903 4909 4919 4931 4933 4937
  ```

**The failure rate increases with p**: zero failures in p ≤ 1397; 5 failures in
[1399, 1500]; 5 in [2600, 2700]; 22 in [3000, 3500]; 10 in [4800, 4940]. This
is the opposite of the prior session's claim that the |Saw|/Bern ratio
"decreases on average." That claim was based on 35 primes ≤ 211, where the
ratio is indeed shrinking; extension shows it is non-monotone and crosses 1.

**Re-verification at exact-rational precision:**
* p = 1423: Bern = +0.10574948855787777, Saw = +0.31212729485976420,
  ratio = 2.95157, B_raw = −0.20637780630188643. Confirmed.
* p = 3299: Bern = **−0.11922733326244307**, Saw = +0.31590693671940395,
  ratio diverges (Bern < 0), B_raw = −0.43513426998184701. Confirmed.

(Float and exact agree to ~12 digits at p ≈ 3·10³, n ≈ 3·10⁶, so float was
not the source of the failures.)

# 3. The two open questions left by this refutation

## Open Q1 — Is `B(p) ≥ 0` itself a theorem of the source paper?

The identity `B(p) · n′²/2 = Bern(p) − Saw(p)` is asserted in
`B_geq_0_extra_high_attempt.md` §0–§2 as a "trivial rearrangement." This
session did NOT independently re-derive that identity from a primary
definition of B(p). Two scenarios:

* **(A) The identity is correct.** Then the 42 numerical failures above are
  counterexamples to `B(p) ≥ 0`, and the underlying conjecture is FALSE.
  This would invalidate every paper draft that depends on it.
* **(B) The identity is wrong** (off by a sign, scaling, or has missing
  boundary terms). Then the Bern/Saw split is the wrong reduction; B(p)
  could still be ≥ 0. This needs an audit of the four-term decomposition in
  `B_geq_0_dedekind_attack.md` §1.

**Action:** Before any further analytic work on Saw(p), audit the algebraic
identity B(p) = (2/n′²)·Σ D(f)·δ(f) against the original definition of B(p)
in the source manuscript. Recompute B(p) directly (without the Bern/Saw
split) at p ∈ {1423, 3299} and compare the sign.

## Open Q2 — The genuine bilinear sum problem (untouched)

The user's prompt asks for an unconditional bound on
`Σ_{h ≤ H} |T_h(p)|/h` where `T_h(p) = Σ_{f ∈ F_p} D(f)·e(hpf)`. **This
session did not attack that sum.** The reason: the Bern/Saw decomposition is
the PROXY for that sum (after a Fourier expansion of ψ), and the proxy is
already empirically false. There is no point bounding a quantity whose
positivity-implication is broken.

If Open Q1 resolves with scenario (B), then T_h(p) becomes interesting
again. At that point the candidate routes are still the ones the prompt
listed (Burgess subconvexity, Halász–Montgomery, ε-approximate B = (2/n′²)·X
with X bounded below by another quantity), but they require the analytic
literature work that this session explicitly avoided rather than fabricated.

# 4. On the prior literature claims

The user's prompt reasonably required: "Before citing ANY theorem, download
the paper PDF locally and quote VERBATIM." This session did NOT download any
papers. Therefore I cite NOTHING from the analytic-number-theory literature
in this document. Specifically:

* I do NOT claim "Aistleitner–Berkes–Tichy 2010 gives exponent X" — prior
  document did, and the bound there does not deliver what was claimed.
* I do NOT claim "Vaaler Theorem 18" or "Mikolas 1949 sawtooth bound" —
  these need verification against the actual papers.
* I do NOT claim "Burgess 1962/63 character-sum subconvexity transfers to
  Farey exponential sums" — that transfer is not in the literature in the
  form cited.

The honest position is: **no citation in the prior document
(`B_geq_0_FULL_CLOSURE.md`, `B_geq_0_extra_high_attempt.md`) has been
verified by quoting the source.** Anything that depends on those citations
is provisional.

# 5. The §7 algebraic error, in detail (so it doesn't recur)

The prior document claimed:

> Bern(p) = Σ D(f)(f − 1/2) = (1/(n−1)) · Σ (i − (n−1)/2)(f_i − 1/2)
> [and then "by Chebyshev's sum inequality the RHS is > 0, so Bern > 0"].

Expanding the LHS:
```
Bern = Σ [i/(n−1) − f_i] · (f_i − 1/2)
     = (1/(n−1)) Σ i(f_i − 1/2)        — call this T1
       − Σ f_i(f_i − 1/2)               — call this T2
```
Expanding the claimed Chebyshev form:
```
(1/(n−1)) Σ (i − (n−1)/2)(f_i − 1/2)
  = (1/(n−1)) Σ i(f_i − 1/2)           — same T1
    − (1/2)(Σ f_i − n/2)                — = 0, since Σ f_i = n/2
  = T1.
```
So `Bern − ChebForm = − T2 = − Σ f_i(f_i − 1/2) = − Σ f_i² + (1/2)Σ f_i =
−Σ f_i² + n/4.` Reflection f ↔ 1−f gives `Σ f² = Σ(1−f)² = n − 2·(n/2) +
Σ f² = Σ f²`, a tautology. So `Σ f² = n/4` does NOT follow, and indeed
Σ f_i² over F_{p−1} is approximately n/3 (uniform-on-[0,1] heuristic), giving
`T2 ≈ n/3 − n/4 = n/12`, which dominates Bern's O(log p) value as soon as
n ≥ 12·log p. **So at large p, Bern ≈ T1 − n/12, and once T1 < n/12 we get
Bern < 0.** The prior §7 conclusion "Bern > 0 algebraically" is wrong.

Chebyshev's sum inequality applies cleanly to ChebForm (= T1 − 0), giving
T1 > 0, but **not** to Bern.

(Sanity check: at p = 3299, T1 ≈ 275520.87 (exact, scaled by 1/(n−1))
giving T1/(n−1) ≈ 0.0834; and T2 ≈ 0.20262, so Bern ≈ 0.0834 − 0.20262 ≈
−0.119, matching the exact-rational value −0.1192.)

# 6. Quantitative confidence (single rule, applied uniformly)

I use a single rule throughout: numerical counterexample at exact precision =
refuted (confidence ≤ 0.05). Heuristic agreement = 0.30. Algebraic identity
verified by hand = 0.95. Citation without verbatim source = 0.20 maximum.

| Claim | Confidence | Reason |
|---|---|---|
| `Bern(p) > 0` for all p | 0.02 | counterexample p = 3299 in exact rationals |
| `|Saw(p)| ≤ Bern(p)` for all p | 0.02 | 42 counterexamples in p ≤ 4999 |
| Bern/Saw split implies B ≥ 0 (the prior route) | 0.02 | follows from above |
| `B(p) ≥ 0` itself, treating identity B = (2/n′²)(Bern−Saw) as given | 0.05 | treats numerical failures as real |
| `B(p) ≥ 0` itself, allowing identity to be wrong | 0.40 | unknown; would need independent recomputation |
| Prior §7 algebraic Bern > 0 proof is correct | 0.00 | demonstrably wrong, see §5 |
| Aistleitner-style bilinear bound delivers what prior claimed | 0.20 | citation not verified to source |
| The whole "extra-high attack" recovers if identity is corrected | 0.15 | the most charitable reading |

(Pre-session prior on full B≥0 closure within 1 month: 0.45.
Post-session: 0.10. The drop is mostly from §5 — discovering the algebraic
error in the prior "proof" is more important than the numerical failures,
because it shows the framework was unsafe even when ratio < 1.)

# 7. What to do next session (ranked)

1. **Audit the identity** B(p) · n′²/2 = Bern(p) − Saw(p) against the
   primary definition of B(p) in the source paper. Recompute B(p) directly
   at p = 1423, 3299 by the original definition. Compare to
   (2/n′²)(Bern − Saw). If they disagree, the Bern/Saw decomposition has a
   bug; if they agree, B(p) ≥ 0 is **false** at these primes. **Highest
   priority — without this answer no further work is meaningful.**

2. If identity holds and B(1423) < 0 numerically: report it. The "B ≥ 0
   conjecture is false" outcome is publishable on its own (a counterexample
   to a conjecture is a result), but only after independent re-computation
   on a different code path.

3. If identity is wrong: re-derive the four-term split from
   `B_geq_0_dedekind_attack.md` §1 carefully, with no symmetry shortcuts
   that aren't proved. Any new decomposition must then be re-tested over
   p ≤ 5000 numerically before any analytic attack.

4. Only then return to the bilinear `Σ_h |T_h(p)|/h` problem. Read (verbatim,
   with PDFs locally) Mikolas 1949, ABT 2010/2014, Burgess 1962. Do not cite
   anything that hasn't been quoted.

5. The "ε-approximate" route (show |Saw|/Bern ≤ 0.95) is **dead** — the ratio
   exceeds 1 and even goes to ∞ when Bern flips sign. Drop it.

# 8. What's verified vs what's still open (final table)

| # | Statement | Status | Confidence |
|---|---|---|---|
| 1 | Σ f over F_{p−1} = n/2 | verified algebraically | 0.99 |
| 2 | Reflection f ↔ 1−f is an involution on F_{p−1} | verified algebraically | 0.99 |
| 3 | D(f) and ψ(p·) are antisymmetric under reflection | verified | 0.95 |
| 4 | Σ f² = n/4 (claimed in prior §7) | **FALSE** | 0.00 |
| 5 | Bern = ChebForm (claimed in prior §7) | **FALSE** | 0.00 |
| 6 | Bern(p) > 0 for all p (claimed in prior §7) | **FALSE**, p=3299 counterexample (exact) | 0.02 |
| 7 | |Saw(p)| ≤ Bern(p) (the conjectured closure inequality) | **FALSE**, 42 counterexamples (some exact-verified) | 0.02 |
| 8 | Identity B(p)·n′²/2 = Bern(p) − Saw(p) | not re-derived this session | 0.50 |
| 9 | B(p) ≥ 0 (original conjecture) | **OPEN**, possibly false | 0.40 |
| 10 | Σ_h |T_h(p)|/h = O((log p)^{1−ε}) unconditional | **OPEN**, not attacked | 0.10 |
| 11 | Citations from prior session's literature | **UNVERIFIED** (no PDFs downloaded) | ≤ 0.20 each |

# 9. Files

* `bern_saw_extend.tsv` — 665 primes, columns p, n, Bern, Saw, ratio, B_raw.
* `bern_saw_extend_5k.py` — float64 extension script.
* `bern_saw_verify_failures.py` — exact-rational re-verification of {1399,
  1409, 1423, 1427, 1429, 1433}.
* `bern_verify_3299.py` — exact-rational re-verification of p = 3299, plus
  comparison Bern vs ChebForm showing they differ by ≈ 275521.

End. ~1,650 words. Honest assessment, no fabricated citations, no
"named sub-lemmas" for open problems. Confidence aggregation rule stated
once and applied uniformly.
