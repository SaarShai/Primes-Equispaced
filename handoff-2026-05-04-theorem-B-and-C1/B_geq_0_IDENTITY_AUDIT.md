---
title: "B ≥ 0 — Identity Audit: the Bern/Saw decomposition is WRONG, B(p) ≥ 0 was never a universal conjecture"
type: audit
domain: research
tier: working
confidence: 0.97
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - /Users/saar/NEW Farey 5.5/projects/farey-research/results/aristotle-W2-V2-LEMMA-2026-05-01/RequestProject_aristotle_aristotle/CrossTermPositive.lean (PRIMARY)
  - /Users/saar/NEW Farey 5.5/projects/farey-research/results/aristotle-W2-V2-LEMMA-2026-05-01/RequestProject_aristotle_aristotle/DisplacementShift.lean
  - /Users/saar/NEW Farey 5.5/projects/farey-research/results/aristotle-W2-V2-LEMMA-2026-05-01/RequestProject_aristotle_aristotle/SignTheorem.lean
  - /Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/Four_Term_Decomposition.md
  - /Users/saar/Farey 4.7 solutions/B_geq_0_extra_high_attempt.md (SUPERSEDED — decomposition wrong)
  - /Users/saar/Farey 4.7 solutions/B_geq_0_v3_honest.md (correct refutation, partial)
  - /Users/saar/Farey 4.7 solutions/B_geq_0_dedekind_attack.md
  - /Users/saar/Farey 4.7 solutions/B_identity_audit_3299.py (this audit's verifier)
supersedes:
  - /Users/saar/Farey 4.7 solutions/B_geq_0_extra_high_attempt.md
  - /Users/saar/Farey 4.7 solutions/B_geq_0_FULL_CLOSURE.md
superseded-by: null
tags: [farey, B-sign, audit, paper-killing-question, decomposition-error]
---

# Bottom line (TL;DR)

The "paper-killing question" resolves on the **identity-wrong** side, not the
counterexample side:

1. **The identity `B(p)·n'²/2 = Bern(p) − Saw(p)` from `B_geq_0_extra_high_attempt.md`
   §2 is WRONG.** It does not hold at any tested prime. At p = 11 the LHS is
   −1412.43 while the RHS is +0.0222; they disagree by orders of magnitude AND
   in sign.

2. **`B(p) ≥ 0` was never a universal theorem or even a universal conjecture in
   the program.** The primary Lean source explicitly states "The cross term B
   is NOT nonneg for all primes (e.g., B(5) = −2/9, B(11) = −55/36)" and only
   conjectures `B > 0` for primes with `M(p) ≤ −3` (the Mertens-relevant subset).

3. The extra_high.md "Bern/Saw" object is **not a decomposition of the primary
   B(p)**; it is a different Farey bilinear sum that uses a different
   normalization of the displacement (`i/(n−1) − f` vs the Lean
   `rank − n·f = (i+1) − n·f`) and a different δ split. Its sign behavior is
   genuinely an unrelated bilinear question.

4. **Paper B Spectroscope positivity is NOT killed by this audit.** The
   load-bearing claim is `B > 0` on the *Mertens-restricted* subset
   `{p : M(p) ≤ −3}`, exactly as encoded in
   `aristotle-W2-V2-LEMMA-2026-05-01/SignTheorem.lean` and confirmed
   numerically up to p = 99,991 in `Four_Term_Decomposition.md` Session 14.
   None of the {1399, 3299, …} numerical "failures" of the Bern/Saw inequality
   are statements about the primary B(p), so they cannot refute the
   conditional positivity claim.

5. The `extra_high` document and its descendants — `B_geq_0_FULL_CLOSURE.md`
   and any "Bern/Saw closes B ≥ 0" framing — are **retracted**. The
   `B_geq_0_v3_honest.md` partial refutation stands and is upgraded: its Open
   Q1 is now answered (scenario B — "the identity is wrong").

Confidence values:
- The Bern/Saw identity is wrong: **0.99** (numerical disagreement at exact
  rational precision on 4 primes, magnitude and sign).
- B(p) ≥ 0 universally is FALSE: **0.99** (Lean `native_decide` proof of
  `crossTerm_neg_5 : crossTerm 5 < 0`, exact value `B(11) = −55/36`).
- B(p) > 0 for all primes with M(p) ≤ −3 (Paper B's actual claim): **0.85**
  (verified numerically up to p = 99,991, no theorem yet).

# 1. Original B(p) definition — verbatim from primary source

The primary, Lean-verified source is
`aristotle-W2-V2-LEMMA-2026-05-01/RequestProject_aristotle_aristotle/CrossTermPositive.lean`
(file from W2 Lean formalization, 2026-05-01). The file's docstring states
verbatim (lines 7–18):

> Cross Term Positivity: B = 2 Σ D(f) · δ(f) ≥ 0
>
> For prime p ≥ 11 with M(p) ≤ −3, the cross term
>   B = 2 · Σ_{f ∈ F_{p-1}} D(f) · δ(f) > 0,
> where D(f) = rank(f, F_{p-1}) − |F_{p-1}| · f is the displacement and
> δ(f) = f − {pf} is the shift function.

The Lean definition (lines 41–45):

```
def crossTerm (p : ℕ) : ℚ :=
  2 * ∑ ab ∈ fareySet (p - 1),
    displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)
```

with (`DisplacementShift.lean` lines 30–36):

```
def displacement (N : ℕ) (f : ℚ) : ℚ :=
  (fareyRank N f : ℚ) - (fareySet N).card * f

def shiftFun (p : ℕ) (f : ℚ) : ℚ :=
  f - Int.fract ((p : ℚ) * f)
```

So the **primary** definition is:

> **B(p) := 2 · Σ_{f ∈ F_{p−1}} D(f) · δ(f),  D(f) = rank(f) − n·f,  δ(f) = f − {pf}**, n = |F_{p−1}|.

**The same file documents** (lines 21–24, verbatim):

> The cross term B is NOT nonneg for all primes (e.g., B(5) = −2/9, B(11) =
> −55/36). However, B IS strictly positive for every prime p with M(p) ≤ −3
> (the primes relevant to the Mertens conjecture analysis): p = 13, 19, 31, 43, 47, …

And the file proves with `native_decide` (line 79):
```
theorem crossTerm_neg_5 : crossTerm 5 < 0
```

This is a Lean theorem. **B(5) < 0 is a Lean-verified fact.** Therefore the
proposition "B(p) ≥ 0 for all primes p" is **decisively false** and was
**never** part of the program's claims.

The wiki page `Four_Term_Decomposition.md` (line 24) corroborates:

> B = (2/n'²) Σ D(f)·δ(f) — cross-term, sign unknown (can be negative)

and (lines 66–67):
> B < 0 at p = 11 (M=−2), p = 17 (M=−2), p = 97 (M=1), p = 223 (M=3).

(Note the wiki page reports B with a 1/n'² scaling — the "wobble-normalized"
form W(p−1) − W(p) ≡ A − B − C + 1 − D_term − 1/n'². The Lean `crossTerm` is
the un-normalized 2 Σ D·δ; multiplying by 1/n'² gives the wiki's B. Either
way, the SIGN of B is the SIGN of Σ D·δ, and Σ D·δ < 0 at the four primes
above. This is what the program calls "B(p) sign anomaly" and is the topic
the Sign Theorem is restricted to avoid.)

# 2. Step-by-step re-derivation: what would Bern − Saw actually equal?

Set up using the primary definitions (n = |F_{p−1}|, rank = i+1 for f at
0-indexed position i):

  D(f_i) = (i+1) − n · f_i.

  δ(f) = f − {pf} = f − ((pa) mod b)/b   (for f = a/b, b > 0, gcd(a,b)=1).

For non-integer pf, ψ(pf) = {pf} − 1/2, so

  δ(f) = (f − 1/2) − ψ(pf).

(For integer pf we set ψ = 0 by convention; then δ = f − 0 ≠ (f − 1/2) − 0 in
general — δ = f, not f − 1/2. But this only happens at f = 0/1 and f = 1/1 if
relevant; for all interior Farey fractions f = a/b with b > 1 it's fine.)

Carrying through the rearrangement, **using the primary D**:

  Σ_f D(f) · δ(f) = Σ_f [(i+1) − n·f] · [(f − 1/2) − ψ(pf)]
                  = T1 − T2 − T3 + T4

where
  T1 = Σ_i (i+1)·(f_i − 1/2)         [rank × value]
  T2 = Σ_i (i+1)·ψ(pf_i)              [rank × sawtooth]
  T3 = n · Σ_i f_i·(f_i − 1/2)        [value × value]
  T4 = n · Σ_i f_i·ψ(pf_i)            [value × sawtooth]

So
  B(p)/2 = (T1 − T3) − (T2 − T4).

The extra_high.md "Bern, Saw" objects are defined with a DIFFERENT
displacement D_extra = i/(n−1) − f (note: divisor n−1, not n; index i, not
i+1; sign convention flipped):

  Bern(p)  = Σ D_extra · (f − 1/2) = (1/(n−1)) · T1 − Σ f·(f − 1/2) − [boundary i=0 piece, since here i goes 0..n−1]
                                  = (1/(n−1))·(T1 − Σ_i 1·(f_i − 1/2))     [shifting (i+1) → i drops a row]
                                  = (1/(n−1))·T1 − (1/(n−1))·Σ (f_i − 1/2) − Σ f(f − 1/2)

Using Σ (f − 1/2) = Σ f − n/2 = 0 (since Σ f = n/2 by reflection), the middle
term vanishes:

  Bern(p) = (1/(n−1))·T1 − (1/n)·T3.   ※

Similarly Saw(p) = (1/(n−1))·T2 − (1/n)·T4.

Therefore:

  Bern(p) − Saw(p) = (1/(n−1))·(T1 − T2) − (1/n)·(T3 − T4).

**This is NOT proportional to B(p)/2 = (T1 − T3) − (T2 − T4).** The
coefficients of T1, T2, T3, T4 in B and in (Bern − Saw) are completely
different. They cannot match up to a single scalar multiplier.

The extra_high.md §2 claim "Σ D(f)·δ(f) = Bern(p) − Saw(p), exactly" is a
**confusion of two different D's**. The doc's own §0 defines D(f) =
i/(n−1) − f, while pretending it's the same D as in the four-term
decomposition. The four-term D is `rank − n·f`. These differ by a factor of
≈ (n−1)·(−1)·(some shift) — not a clean rescaling.

# 3. Where Σ f² = n/4 vs n/3 enters

This is the v3_honest §5 error and it is **a separate, additional bug** on
top of the D-mismatch above.

The §7 of `extra_high_attempt.md` claimed:

> Bern(p) reduces to (1/(n−1))·Σ (i − (n−1)/2)·(f_i − 1/2)
>  = (1/(n−1))·Σ i·(f_i − 1/2)   [Σ(f−1/2) = 0]
> hence Bern > 0 by Chebyshev.

Computing both sides directly:

  Bern(p)        = (1/(n−1))·T1 − (1/n)·T3      (per ※ above)
  ChebForm(p)    = (1/(n−1))·T1               (the term §7 says equals Bern)

So Bern − ChebForm = −(1/n)·T3 = −Σ f(f−1/2) = −[Σ f² − (1/2)·Σ f]
                  = −Σ f² + n/4.

The §7 deduction "Bern = ChebForm" requires Σ f² = n/4. But by f ↔ 1−f
reflection: Σ (1−f)² = Σ (1 − 2f + f²) = n − 2·(n/2) + Σ f² = Σ f². This is a
**tautology**, not a constraint, so it does NOT prove Σ f² = n/4. The actual
Σ f² over F_{p−1} is approximately the integral ∫₀¹ x² dx · n = n/3, with a
discrepancy correction of order O(log p).

Numerical confirmation (this audit, exact rationals, primary verifier):

| p | n | Σ f² (exact) | n/3 (heuristic) | n/4 (claim §7) |
|---|---|---|---|---|
| 11 | 33 | 10.8854 | 11.0 | 8.25 |
| 17 | 81 | 26.7577 | 27.0 | 20.25 |
| 97 | 2807 | 935.1751 | 935.667 | 701.75 |
| 223 | 14991 | 4996.4938 | 4997.0 | 3747.75 |

Σ f² agrees with n/3 to ~0.1% and is **substantially different** from n/4. So
T3/n = Σ f(f−1/2) ≈ n/3 − n/4 = n/12, growing linearly in n — completely
dominating any positive Chebyshev contribution at large n. This is what makes
"Bern" go negative at p ≥ 3299.

**Two errors stacked:** (a) the "decomposition" identity B·n'²/2 = Bern − Saw
itself is wrong (uses the wrong D, mismatched normalization, drops T3 and T4
asymmetrically); (b) within Bern's *own* arithmetic, the §7 "proof" that
Bern > 0 via Chebyshev silently used Σ f² = n/4. Either error alone refutes
the closure; both together explain why downstream numerical checks (in
v3_honest.md) found Bern itself going negative.

# 4. Numerical comparison at p = 3299 (and 11, 17, 97, 223)

Using `B_identity_audit_3299.py` (exact `fractions.Fraction` arithmetic, no
floating point in the computation; floats only printed for display):

| p   | n=\|F_{p−1}\| | n'=\|F_p\| | B(p) [primary] | Bern−Saw [extra_high] | B·n'²/2 (claimed eq Bern−Saw) |
|-----|---|---|---|---|---|
| 11  | 33    | 43    | **−1.5278** (= −55/36, matches Lean comment exactly) | +0.02224 | −1412.43 |
| 17  | 81    | 97    | **−2.6099** | +0.04252 | −12278.18 |
| 97  | 2807  | 2903  | **−95.13** | +0.06344 | −4.008 × 10⁸ |
| 223 | 14991 | 15213 | **−751.52** | +0.05425 | −8.696 × 10¹⁰ |

The "identity" Bern − Saw = B · n'²/2 fails by **many orders of magnitude
AND by sign** at every tested prime. It is not an off-by-constant error or a
sign error; it is a wholly different object.

(The p = 1399 and p = 3299 cases are running; preliminary smaller-prime data
already settles the question. Update will follow if anything diverges from
the pattern.)

The match `B(11) = −55/36 = −1.52778…` between this audit's Python verifier
and the Lean theorem's docstring (verbatim "B(11) = −55/36") confirms the
primary verifier is correct.

# 5. Verdict

## 5.1 Identity status

**The Bern/Saw decomposition `B(p)·n'²/2 = Bern(p) − Saw(p)` is FALSE.** Not a
sign error, not a normalization error — the two sides are different bilinear
sums on F_{p−1} with different displacement normalizations. The doc that
introduced it (`B_geq_0_extra_high_attempt.md`) silently substituted a
modified `D(f) = i/(n−1) − f` for the primary `D(f) = rank − n·f`, then
claimed "trivial rearrangement" without checking.

## 5.2 B ≥ 0 conjecture status

**The proposition "B(p) ≥ 0 for all primes p" is FALSE and was already known
to be false in the program.** Counterexamples:
- B(5) = −2/9      [Lean `native_decide` theorem `crossTerm_neg_5`]
- B(11) = −55/36   [Lean docstring; reproduced this audit]
- B(17) ≈ −2.61    [this audit]
- B(97) ≈ −95.13   [this audit, matches `Four_Term_Decomposition.md` Session 14 list]
- B(223) ≈ −751.52 [this audit]

The relevant question is "B(p) > 0 for primes with M(p) ≤ −3", and that
question is open but well-supported (verified for all 4,617 such primes up to
p = 99,991 per `SignTheorem.lean` docstring).

The 42 numerical "failures of |Saw| ≤ Bern" at p ∈ {1399, 1409, …, 4937}
documented in `bern_saw_extend.tsv` are real failures of a real bilinear
inequality on F_{p−1}, but that bilinear inequality is **not** equivalent to
B ≥ 0. They are not counterexamples to anything in Paper B.

## 5.3 What the 42 "failure primes" actually mean

They mean: the bilinear form Σ_f (i/(n−1) − f)·ψ(pf) on F_{p−1} can exceed in
absolute value the related bilinear form Σ_f (i/(n−1) − f)·(f − 1/2). Both
are interesting Farey×sawtooth correlations in their own right but neither is
the B(p) of the Spectroscope program. Whether either has a positive sign for
all p is a clean (and apparently false) bilinear question for a separate
investigation; it is not a "paper-killing" finding.

# 6. Implications for Paper B (Spectroscope)

1. **No retraction needed.** Paper B's positivity argument depends on the
   four-term decomposition's actual B (with `crossTerm` Lean definition) and
   on `B > 0` *only on the Mertens-restricted subset* `{p : M(p) ≤ −3}`. That
   restricted claim is intact, well-tested, and not touched by anything in
   `extra_high_attempt.md` or `v3_honest.md`.

2. **Retract the `extra_high_attempt.md` Bern/Saw framing.** The four-term
   reformulation it proposes is not the four-term decomposition of B(p); it
   is a different (and broken) gadget. Update `extra_high_attempt.md`'s
   frontmatter `superseded-by: B_geq_0_IDENTITY_AUDIT.md` and lower
   confidence to 0.0.

3. **Retract `B_geq_0_FULL_CLOSURE.md`** (already partially done by v3_honest;
   make it explicit). The "closure" was via the same broken decomposition.

4. **Promote `v3_honest.md` Open Q1 to "resolved (identity wrong)".** The
   v3_honest analysis was correct in spirit; this audit completes it by
   identifying *which* algebraic step is wrong (the wholesale substitution of
   D's, not just §7).

5. **The genuine open question that remains** for the Mertens-restricted
   positivity is the one already in
   `aristotle-W2-V2-LEMMA-2026-05-01/SignTheorem.lean`'s "ratio test":
   `D + B + C − 1 > dilution`. That is the claim that needs theoretical
   support. The Bern/Saw route is **not** the route to that support; the
   Dedekind-Rademacher route in `B_geq_0_dedekind_attack.md` (confidence 0.58
   at last assessment) remains the most promising line of attack.

6. **Action items**
   - Update `B_geq_0_extra_high_attempt.md` and `B_geq_0_FULL_CLOSURE.md`
     frontmatter to mark them superseded by this audit.
   - Update `bern_saw_extend.tsv` README/comments: this is data on a real
     bilinear sum, but it is *not* B(p). Rename to `bern_saw_extra_high_decomp.tsv`
     to prevent future confusion.
   - In the wiki, link `Four_Term_Decomposition.md` ↔ this audit so the
     "B(p) ≥ 0 for all primes" misconception cannot reappear.
   - The Sign Theorem Lean proof and its conditional positivity for
     M(p) ≤ −3 remain the canonical claim.

# 7. Files

- This audit's verifier: `/Users/saar/Farey 4.7 solutions/B_identity_audit_3299.py`
- Primary Lean source for B(p): `/Users/saar/NEW Farey 5.5/projects/farey-research/results/aristotle-W2-V2-LEMMA-2026-05-01/RequestProject_aristotle_aristotle/CrossTermPositive.lean`
- Wiki anchor: `/Users/saar/Documents/Spark Obsidian Beast/Farey Research/wiki/Four_Term_Decomposition.md`
- Failed framework: `/Users/saar/Farey 4.7 solutions/B_geq_0_extra_high_attempt.md` (retract)
- Prior partial refutation: `/Users/saar/Farey 4.7 solutions/B_geq_0_v3_honest.md` (correct, now superseded by this fuller analysis)

End of audit. The "paper-killing" question is RESOLVED in the
identity-is-wrong scenario. Paper B is intact; the extra_high decomposition
is retracted.
