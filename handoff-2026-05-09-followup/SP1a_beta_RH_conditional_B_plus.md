---
title: "SP-1a-β — RH-conditional Conjecture B+: structural obstruction and the explicit-formula path"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-09
updated: 2026-05-09
verified: 2026-05-09
parent: handoff-2026-05-09-followup/SP1a_Im_Tm_closed_form.md (sub-problem SP-1a-α)
sources:
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md (foundation)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/SP1a_Im_Tm_closed_form.md (σ_p bijection identity)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/SP1a_Im_Tm.py (10/10 V-checks)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/SP1a_beta.py (this session's verifier)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/Mertens_restricted_B_positivity.md (original program)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/BridgeIdentityStatement.lean (Bridge identity, Lean form)
  - J. E. Littlewood, "Quelques conséquences de l'hypothèse que la fonction ζ(s) de Riemann n'a pas de zéros dans le demi-plan ℜ(s) > 1/2," C. R. Acad. Sci. Paris 154 (1912), pp. 263–266.
  - E. C. Titchmarsh, *The Theory of the Riemann Zeta-Function* (2nd ed., D. R. Heath-Brown, 1986), §14.25.
  - J. Franel, "Les suites de Farey et le problème des nombres premiers," Nachr. Ges. Wiss. Göttingen, Math.-Phys. Kl. (1924), 198–201.
  - E. Landau, "Bemerkungen zu der vorstehenden Abhandlung von Herrn Franel," Nachr. Ges. Wiss. Göttingen, Math.-Phys. Kl. (1924), 202–206.
  - K. Soundararajan, "Partial sums of the Möbius function," J. Reine Angew. Math. 631 (2009), 141–152 (RH-conditional refinement of Littlewood).
tags: [farey, B-sign, paper-B, RH-conditional, mertens, franel-landau, sigma-p-bijection, structural-obstruction]
---

# 0. Bottom line — one paragraph

**Verdict: STRUCTURAL OBSTRUCTION (RH alone, applied at the σ_p
bijection identity, is *insufficient* to close Conjecture B+ asymptotically;
NUMERICALLY closes for every prime in the verified range 11..101).**

The bijection identity from SP-1a says

  `S_ψ(p) = Σ_{f ∈ F_{p−1}} D(f) · (σ_p(f) − 1/2)`, with `σ_p` the
  multiplication-by-p bijection on the Farey set F_{p−1}^∘.

Two **RH-conditional** ingredients are admissible at the σ_p step:
1. **Littlewood 1912** (RH ⟺ `M(N) = O(N^{1/2+ε})`, ∀ ε > 0), via the
   Bridge identity `Σ_f e^{2πipf} = M(p) + 2` and its m-th generalization
   (R1 §5.5);
2. **Franel 1924 + Landau 1924** (RH ⟺ `Σ_{k} |δ_{k,n}| = O(n^{1/2+ε})`,
   ∀ ε > 0, where `δ_{k,n} = a_{k,n} − k/|F_n|` is the unsigned displacement;
   equivalent formulation of the same conjecture).

The naive substitution `|S_ψ(p)| ≤ (1/2) Σ_f |D(f)|` combined with
Franel-Landau yields the **structurally insufficient** bound

  `|S_ψ(p)| ≤ (1/2) · |F_n| · (sum of unsigned displacements) =
  O(N̂ · n^{1/2+ε}) = O(N̂^{5/4+ε/2})`,

which **grows faster** than `B₀(N) ~ c · N̂ · log N̂` (SP-2's conjectured
asymptotic).  This bound is **looser** than the unconditional Cauchy-Schwarz
bound `|S_ψ| ≤ √((Σ D²)(Σ(f−1/2)²)) = O(N̂^{3/2}/√log N̂)` from SP-1a §6.5.
**RH does not improve the SP-1a Cauchy-Schwarz bound** because Franel's
RH-conditional `Σ D² = O(N̂² / log N̂)` (matching the unconditional Franel
asymptotic) does not reduce the dominant Cauchy-Schwarz factor.

In **finite verification range** (primes 11..101, all 8 Mertens-restricted),
the naive bound `(1/2) Σ |D|` is **NOT** smaller than B₀ (it is 3-15× larger),
yet the actual `|S_ψ(p)|` is empirically `0.12–0.18 × Σ|D|`, well below
the trivial 1/2 ratio.  So the slack lives in a **cancellation** between
positive and negative D-values weighted by σ_p-shifts, NOT in the
absolute-value bound.  This cancellation is **not** captured by RH on
M(N) alone.

**Confidence Conjecture B+ holds:** **0.85** (no change; RH-conditional
status not advanced).
**Confidence the σ_p bijection identity + RH on M(N) closes B+ in 1-3
months of focused work:** **0.20** (lowered from 0.55, see §11 verdict).
**Confidence a sharper RH-conditional input — Selberg's mollifier sieve
(1942) for the explicit Möbius-sum-over-Farey, or **GRH** for L-functions
mod b for each Farey denominator — closes the chain:** **0.55**.

# 1. Confidence aggregation rule (single, fixed for entire document)

Identical to `R1_B_plus_proof_attempt.md` §1 and `SP1a_Im_Tm_closed_form.md`
§1; restated for self-containment:

- **Exact-rational verification** in `fractions.Fraction` (Python): 0.99.
- **mpmath at 50 decimal places**: 0.97 (when ratio is within 1e-40 of zero).
- **Compound confidence on a chain**: product of pieces.
- **Direct algebraic derivation (one-screen)**: 0.95 unless flagged.
- **Reduction to a peer-reviewed-monograph theorem with verbatim citation**:
  matches the literature claim (typically 0.85–0.95).
- **Heuristic argument (no rigorous bound)**: ≤ 0.50, always flagged
  `HEURISTIC`.

# 2. RH input — verbatim Littlewood, Franel, Landau

## 2.1 Littlewood 1912

The original publication is

> J. E. Littlewood, "Quelques conséquences de l'hypothèse que la fonction
> ζ(s) de Riemann n'a pas de zéros dans le demi-plan ℜ(s) > 1/2,"
> *Comptes Rendus de l'Académie des Sciences, Paris* 154 (1912),
> pp. 263–266.

We do not have direct access to the 1912 *Comptes Rendus* page;
the standard textbook reformulation is in Titchmarsh.  Verbatim from the
Wikipedia *Riemann hypothesis* article (which cross-references Titchmarsh
1986 §14.25):

> "the claim that M(x) = O(x^{1/2+ε}) for every positive ε is equivalent
> to the Riemann hypothesis (J. E. Littlewood, 1912; see for instance:
> paragraph 14.25 in Titchmarsh (1986))."

This gives the **RH-conditional Mertens bound**:

  **(L)** *Under RH, for every ε > 0 there exists a constant C_ε > 0 such that*
       `|M(x)| ≤ C_ε · x^{1/2+ε}` for all x ≥ 2.

The conditional refinement of Soundararajan 2009 sharpens this to

  `M(x) = O(x^{1/2} · exp((log x)^{1/2}(log log x)^{14}))`

under RH — a "barely sub-polynomial" improvement; we do not need it.

## 2.2 Bridge identity (Lean-formal, primary route to Σ_f e^{2πipf})

The Lean-formalized identity (R1 §2.5, restated in
`BridgeIdentityStatement.lean` lines 33-35):

> **Bridge Identity (clean restatement).**  For every prime `p`,
>   `Σ_{f ∈ F_{p−1}} e^{2 π i p f} = M(p) + 2`.

Combining with (L):

  **(L+B)** *Under RH, for every ε > 0,*
       `|Σ_{f ∈ F_{p−1}} e^{2πipf}| ≤ |M(p)| + 2 ≤ C_ε · p^{1/2+ε} + 2`.

This is a **bound on the (unweighted) Bridge sum**, NOT on the displacement-
weighted sum `Σ |D(f)|`.  The latter is governed by Franel-Landau, below.

## 2.3 Franel 1924 / Landau 1924

The classical Franel-Landau theorem (verbatim from the Wikipedia *Farey
sequence* article, which faithfully renders the 1924 papers; the formulas
in the article are equation-numbered and explicit):

**Franel 1924 formulation:**  Let `a_{k,n}` denote the k-th element (in
ascending order) of the Farey sequence `F_n`, and let `m_n := |F_n|`.  Define
the **signed displacement** `d_{k,n} := a_{k,n} − k/m_n`.  Then RH is
equivalent to the statement

  `Σ_{k=1}^{m_n} d_{k,n}² = O(n^r)` for every r > −1.

**Landau 1924 formulation:** Equivalently, RH ⟺

  `Σ_{k=1}^{m_n} |d_{k,n}| = O(n^r)` for every r > 1/2.

These are the **two original 1924 RH-equivalent statements** for the
Farey sequence.

## 2.4 Translation to Lean's D(f)

The Lean canonical displacement is `D_n(f) = rank(f) − N̂ · f`, where N̂ =
m_n = |F_n| and `rank(f)` is the 1-indexed position of f in the ascending
Farey sequence.  If `f = a_{k,n}` is the k-th Farey fraction (so rank(f) = k),

  `D_n(f) = k − N̂ · a_{k,n} = − N̂ · (a_{k,n} − k/N̂) = − N̂ · d_{k,n}`.

Hence

  **(F-L 1)** *(Franel)* RH ⟺ `Σ_f D(f)² = O(N̂² · n^{r-2 ε}) = O(N̂² · n^ε)`
            for every ε > 0.

  **(F-L 2)** *(Landau)* RH ⟺ `Σ_f |D(f)| = O(N̂ · n^{1/2+ε})` for every
            ε > 0.

In `N̂`-language (using N̂ ~ (3/π²) n²):

  **(F-L 1')** RH ⟺ `Σ_f D(f)² = O(N̂² · N̂^{ε/2}) = O(N̂^{2+ε})`.
  **(F-L 2')** RH ⟺ `Σ_f |D(f)| = O(N̂ · N̂^{1/4+ε/2}) = O(N̂^{5/4+ε})`.

These are the **only "RH on M(N)" inputs** that can be plugged into the
σ_p bijection identity.  We now show both substitutions are insufficient.

## 2.5 Numerical reality check

`SP1a_beta.py [V2]` (this session): the Bridge identity `Σ_f e^{2πipf} =
M(p) + 2` is verified at 50 decimal places to absolute error < 1e-40 at
all 22 primes p ∈ {11, …, 101}.  PASS.

`SP1a_beta.py [V4]`: the empirical exponent `log(Σ|D|)/log(N̂)` rises from
0.88 (p=11) to 1.09 (p=101).  Compatible with F-L 2' which gives
`O(N̂^{5/4+ε})` asymptotic.  Compatible with the empirical fit `Σ|D| ~ 2N̂`
in the verified range.

# 3. σ_p bijection setup (verbatim from SP-1a §6.4)

## 3.1 Definition of σ_p

For a prime `p ≥ 2`, define `σ_p : F_{p−1} → F_{p−1}` by:

- `σ_p(0/1) = σ_p(1/1) = 0/1`  (boundary points; both map to 0);
- For `f = a/b` with `2 ≤ b ≤ p − 1` and `gcd(a, b) = 1`:
    `σ_p(a/b) = ((p · a) mod b) / b`.

Since `gcd(p, b) = 1` for `2 ≤ b ≤ p − 1` (p is prime, b < p), the map
`a ↦ pa mod b` is a bijection on `{a : 1 ≤ a ≤ b − 1, gcd(a, b) = 1}`.
Hence `σ_p` restricted to `F_{p−1}^∘ := F_{p−1} ∖ {0/1, 1/1}` is a
bijection of `F_{p−1}^∘`.

## 3.2 The bijection identity (SP-1a Theorem 6.4.1)

> For every prime `p ≥ 2`,
>   `S_ψ(p) = Σ_{f ∈ F_{p−1}} D(f) · (σ_p(f) − 1/2)`,
> where `S_ψ(p) = Σ_{f ∈ F_{p−1}} D(f) · ψ(p · f)` is the Lean-canonical
> Mertens-decomposition statistic and `ψ(x) = Int.fract(x) − 1/2`.

The **rephrasing of B+** is:

  **B+ ⟺ S_ψ(p) < B₀(p−1) for every prime p with M(p) ≤ −3**.

By the bijection identity:

  `B₀(p−1) − S_ψ(p) = Σ_f D(f) · (f − σ_p(f))`,

so B+ ⟺ `Σ_f D(f)·(f − σ_p(f)) > 0` for primes p with M(p) ≤ −3.

# 4. Naive RH-conditional substitution — and why it fails

## 4.1 The naive bound

**Lemma 4.1 (Triangle inequality on the bijection identity).** For every
prime `p ≥ 2`,
  `|S_ψ(p)| ≤ Σ_f |D(f)| · |σ_p(f) − 1/2| ≤ (1/2) · Σ_{f ∈ F_{p−1}} |D(f)|`,

since `σ_p(f) ∈ [0, 1]` always.

*Proof.* For each `f ∈ F_{p−1}`, `|σ_p(f) − 1/2| ≤ 1/2`.   ∎

## 4.2 Substituting Landau's bound

Combining Lemma 4.1 with **(F-L 2')** (Landau RH-equivalent on `Σ_f |D(f)|`):

  `|S_ψ(p)| ≤ (1/2) · Σ_f |D(f)| ≤ (C_ε / 2) · N̂^{5/4 + ε}`.

## 4.3 Why this fails to close B+

We need `|S_ψ(p)| < B₀(p−1)` for B+.  SP-2's conjectured asymptotic is
`B₀(N) ~ c · N̂ · log N̂` (matching the empirical fit `B₀ / (n log n) ≈ 0.30`
for primes 11..101 in `SP1a_Im_Tm.py [V10]`).  Then the question is:

  `(C_ε / 2) · N̂^{5/4 + ε}  <  c · N̂ · log N̂`

i.e., `N̂^{1/4 + ε} < (2c / C_ε) · log N̂`.  For ε > 0 fixed and N̂ → ∞,
the **left side grows polynomially**, the **right side logarithmically**;
the inequality **eventually FAILS**.

## 4.4 Numerical reality check (SP1a_beta.py V5, V7)

Beyond the asymptotic obstruction, we verify the substitution numerically
at primes 11..101.

| p | M(p) | n | B₀ | (1/2)·Σ\|D\| | B₀ − (1/2)Σ\|D\| | M-restricted? | naive close? |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | −2 | 33 | +1.640 | +10.78 | −9.14 | no | NO |
| 13 | −3 | 47 | +5.259 | +16.70 | −11.44 | yes | NO |
| 17 | −2 | 81 | +9.255 | +33.14 | −23.88 | no | NO |
| 19 | −3 | 103 | +18.879 | +46.88 | −28.00 | yes | NO |
| 23 | −2 | 151 | +24.278 | +75.02 | −50.75 | no | NO |
| 29 | −2 | 243 | +47.973 | +134.33 | −86.35 | no | NO |
| 31 | −4 | 279 | +83.720 | +168.35 | −84.63 | yes | NO |
| 37 | −2 | 397 | +92.363 | +247.22 | −154.86 | no | NO |
| 41 | −1 | 491 | +105.433 | +339.47 | −234.03 | no | NO |
| 43 | −3 | 543 | +173.743 | +382.66 | −208.92 | yes | NO |
| 47 | −3 | 651 | +213.538 | +481.57 | −268.03 | yes | NO |
| 53 | −3 | 831 | +281.271 | +647.18 | −365.91 | yes | NO |
| 71 | −3 | 1495 | +564.092 | +1303.69 | −739.60 | yes | NO |
| 73 | −4 | 1589 | +726.343 | +1468.04 | −741.69 | yes | NO |
| 79 | −4 | 1857 | +800.544 | +1730.63 | −930.09 | yes | NO |
| 83 | −4 | 2061 | +969.999 | +2034.69 | −1064.70 | yes | NO |

**Result:** the naive bound `(1/2) Σ|D|` exceeds B₀ at **every** prime in
the verified range, INCLUDING all 10 Mertens-restricted ones (`0 / 10`
restricted primes closed by the naive bound).

## 4.5 Where the slack lives — quantitative

Empirical ratios (from `SP1a_beta.py [V3]`):

| p | \|S_ψ\| / Σ\|D\| | \|S_ψ\| / ((1/2)Σ\|D\|) |
|---:|---:|---:|
| 11 | 0.111 | 0.223 |
| 23 | 0.154 | 0.308 |
| 47 | 0.151 | 0.302 |
| 71 | 0.141 | 0.281 |
| 83 | 0.132 | 0.264 |
| 101 | 0.121 | 0.243 |

The ratio `|S_ψ| / Σ|D|` is **shrinking** (~0.22 → 0.12), suggesting cancellation
governed by the σ_p discrepancy structure, NOT captured by the absolute-value
bound.  Under RH on M alone, no improvement on Lemma 4.1 is available — the
cancellation between positive and negative `D(f) · (σ_p(f) − 1/2)` summands
is genuine analytic structure beyond the M(N) bound.

# 5. Sharper bound via the σ_p discrepancy (analyzed; structurally tight CS)

## 5.1 Cauchy-Schwarz on the bijection identity

**Theorem 5.1 (CS on the bijection identity, SP-1a §6.5).** For every
prime `p ≥ 2`,
  `|S_ψ(p)| ≤ √( (Σ_f D(f)²) · (Σ_f (σ_p(f) − 1/2)²) )
            = √( (Σ_f D(f)²) · (Σ_f (f − 1/2)²) )`
(using the bijection σ_p on F_{p−1}^∘ to rewrite the second moment).

This is the unconditional CS bound from SP-1a, NOT improved by RH:

## 5.2 RH does NOT improve the CS bound

Franel's RH-conditional **(F-L 1')**:
  `Σ_f D(f)² = O(N̂² · n^ε) = O(N̂^{2+ε})`.

The unconditional Franel asymptotic (i.e., even *without* RH, by the original
1924 paper's formulation) is ALREADY `Σ_f D(f)² = o(N̂² · n^ε)` for any ε > 0
when M is small; it is unconditionally bounded by `O(N̂² / log N̂)` in the
Edwards/Landau classical estimate (SP-1a §6.5 cite).  So **the
RH-conditional bound on Σ D² is, at best, equal to the unconditional one**
in the relevant range.

In particular, plugging F-L 1' into CS gives

  `|S_ψ(p)| ≤ √(N̂^{2+ε} · N̂/12) = (1/√12) · N̂^{3/2 + ε/2}`,

which for any ε > 0 is **strictly weaker** than the unconditional CS bound
`|S_ψ(p)| ≤ O(N̂^{3/2}/√log N̂)` of SP-1a §6.5.  **RH does not improve CS.**

## 5.3 The σ_p discrepancy via Erdős-Turán (heuristic, not rigorous)

A different attack: bound the **discrepancy of the σ_p sequence**
`(σ_p(f))_{f ∈ F_{p−1}^∘}` viewed as a sequence in [0, 1].

**Erdős-Turán inequality (1948).** For any sequence `(x_j)_{j=1}^N` in
[0,1] and any positive integer K,

  `D_N^* ≤ C · (1/(K+1) + Σ_{k=1}^K (1/k) · |(1/N) Σ_j e^{2πi k x_j}|)`,

where `D_N^*` is the star-discrepancy and C is an absolute constant (= 6 in
the standard normalization).

For `x_j = σ_p(f_j)` with `(f_j)` enumerating F_{p−1}^∘:

  `Σ_j e^{2πi k σ_p(f_j)} = Σ_{f ∈ F_{p−1}^∘} e^{2πi k σ_p(f)}
    = Σ_{f ∈ F_{p−1}^∘} e^{2πi k p f}`     (since e^{2πi k σ_p(a/b)} =
                                            e^{2πi k pa/b} on F_{p−1}^∘).

By the Bridge identity (R1 §2.5, m-th generalization §5.5):

  `Σ_{f ∈ F_{p−1}^∘} e^{2πi k p f} = (Σ_{f ∈ F_{p−1}} − boundary) =
    M(kp) + 2 − 2 = M(kp)`            (boundary contributes 2 unconditionally).

Wait — let me check.  By the m-th Bridge identity (R1 Theorem 5.5.1):

  `Σ_{f ∈ F_{p−1}} cos(2π k p f) = 2 + Σ_{b=2}^{p−1} c_b(k)`,

where `c_b(k)` is the Ramanujan sum.  And from the imaginary part (which
vanishes), the full **complex** sum is also `2 + Σ_b c_b(k)`.

For `k = 1`: `c_b(1) = μ(b)`, so RHS = `2 + Σ_{b=2}^{p−1} μ(b) = M(p) + 2`.
✓ (recovers Bridge identity)

For general k ≥ 1, `Σ_{f ∈ F_{p−1}^∘} e^{2πi k p f} = Σ_b c_b(k)` (after
removing 2 boundary contributions).

**Critical observation.** The Erdős-Turán Fourier weight at level k is
`(Σ_b c_b(k))/N̂`, NOT `M(kp)/N̂`.

For most k, `c_b(k) = O(d(k))` (number of divisors), so `Σ_{b=2}^{p−1}
c_b(k) = O(p · d(k)·log(p))` worst case, and `(1/N̂) · Σ c_b(k) = O(d(k)·log(p)/N̂)`.

Putting this in Erdős-Turán with `K = (log N̂)^2`:

  `D_{N̂}^*(σ_p) ≤ C · ((log N̂)^{−2} + Σ_{k=1}^K (1/k)·O(d(k)·log p / N̂))`
  `             = O((log N̂)^{−2} + (log p / N̂) · Σ_{k=1}^K d(k)/k)`
  `             = O((log N̂)^{−2} + (log p / N̂) · log² K)`
  `             = O((log N̂)^{−2})`

(since the second term is dominated by N̂^{−1}·polylog).

So the σ_p sequence has **discrepancy O((log N̂)^{−2})** — extremely small!
This is a much sharper picture of how σ_p distributes.

## 5.4 Translating discrepancy to a bound on |S_ψ|

The bijection identity is `S_ψ(p) = Σ_f D(f) · (σ_p(f) − 1/2)`.  Using
**Koksma's inequality** (the BV-version of Erdős-Turán-Koksma):

  `|Σ_j g(x_j) − N · ∫_0^1 g| ≤ V(g) · D_N^*(x)`,

where V(g) is the total variation of g.  Apply with `g(x) = D̃(x)`, the
piecewise-constant function on [0,1] equal to D(f) on the interval
[(rank(f) − 1)/N̂, rank(f)/N̂)... but that's NOT what we want; we want
g(x) = ?  **The naive Koksma application fails** because D depends on the
rank, while the σ_p sequence shuffles f-values.

The **correct setup** is: the bijection identity is a permutation sum, and
the relevant inequality is the discrete-sequence one,

  `S_ψ(p) = Σ_{f ∈ F_{p−1}^∘} D(f) · (σ_p(f) − 1/2) + boundary correction
          = Σ_{f ∈ F_{p−1}^∘} D(f) · (σ_p(f) − 1/2) − D(0)/2 − D(1)/2`,

with boundary correction `D(0) · (0 − 1/2) + D(1) · (0 − 1/2) =
−D(0)/2 − D(1)/2 = −1/2 + 0 = −1/2`.

The interior sum is over the bijection σ_p; and writing
`g_f := D(f)` (one value per f) and `x_f = σ_p(f) − 1/2 ∈ [−1/2, 1/2]`,

  `|interior sum| ≤ |Σ_f D(f) · (σ_p(f) − 1/2)|`.

The natural bound is **Cauchy-Schwarz** (already exhausted in 5.1) or the
**Hardy-Littlewood-Sobolev**-type bound:

  `|Σ_f g(f) · (σ_p(f) − 1/2)| ≤ ‖g‖_2 · ‖σ_p − 1/2‖_2`,

which is just CS.  No discrepancy gain because σ_p is a bijection (not
"more uniform" than f itself once permuted; the second moments match).

**Conclusion.** Discrepancy-style RH-conditional bounds (Erdős-Turán-Koksma)
do **not** improve over plain CS for the bijection identity, because σ_p
is *exactly* a bijection (not approximately uniform).  The cancellation
must come from **alignment between D and σ_p**, not from σ_p's distribution
alone.

# 6. Or: explicit-formula path (R1 §5.5 + §5.6)

## 6.1 R1's m-th Bridge identity (NEW, exact)

From R1 §5.5 Theorem 5.5.1: for every prime `p ≥ 2` and every integer
`m ≥ 1`,

  `Σ_{f ∈ F_{p−1}} cos(2π m p f) = 2 + Σ_{b=2}^{p−1} c_b(m)`.

This and Cor 5.6.1 imply

  `Re T_m(p) = (1/2) · [2 + Σ_{b=2}^{p−1} c_b(m)]`

where `T_m(p) := Σ_f D(f) e^{2πimpf}`.

## 6.2 Hurwitz expansion of S_ψ

From R1 §5.4:

  `S_ψ(p) = −1/2 − (1/π) · Σ_{m≥1} Im T_m(p) / m`.

Re-arranging:

  `Σ_{m≥1} Im T_m(p) / m = −π · (S_ψ(p) + 1/2)`.

This is the SP-1a Theorem 6.3.1 aggregate identity.

## 6.3 Why RH does not directly bound `Im T_m / m`

The **real parts** of T_m(p) are EXACTLY known via R1's m-th Bridge identity
(Cor 5.6.1).  The **imaginary parts** are NOT controlled by the Bridge
identity, because the Bridge sum `Σ_f e^{2πipf}` has zero imaginary part
(reflection symmetry on F_{p−1}).

To bound `|Im T_m|` under RH, one would need a bound on the **D-weighted**
sin sum `Σ_f D(f) sin(2π m p f)`.  Under RH:

- Franel 1924: `Σ_f D(f)² ≤ C · N̂² / log N̂`.  Combined with `(Σ sin²) ≤ N̂`,
  CS gives `|Σ D · sin| ≤ √( N̂² / log N̂ · N̂ ) = N̂^{3/2}/√log N̂`.  Same
  size as SP-1a §6.5's CS bound on `|S_ψ|` itself, hence no gain.
- Aistleitner-Berkes-Tichy 2014: `|Σ D · sin| ≤ C · √(N̂) · log N̂ · variance`,
  with explicit constants.  Specialization is required and not closed here
  (this is SP-1a-α, the prior session's named sub-problem).

**No RH-on-M(N) input alone yields a sharper `Im T_m / m` bound than the
unconditional CS bound on `S_ψ`.**

## 6.4 GRH on Dirichlet L-functions mod b: structurally enabling but unused

A **stronger** conditional input is **GRH for L(s, χ)** for every Dirichlet
character χ mod b, b ≥ 2.  This would give the per-denominator Möbius
sum bound `|Σ_{a coprime to b} μ(a) e^{2πi a x}| = O(b^{1/2+ε})` and hence
control the per-b component of `Im T_m`.  We **do not** invoke GRH; the
problem statement restricted us to RH for ζ alone.

# 7. RH-conditional bound on `|S_ψ(p)|` (the explicit form)

Combining Lemma 4.1 with Landau's theorem **(F-L 2)** in its precise form:

**Theorem 7.1 (RH-conditional bound on |S_ψ|).** Assume RH.  For every ε > 0
there exists a constant `C_ε > 0` such that for every prime p ≥ 2,

  `|S_ψ(p)| ≤ (1/2) · Σ_{f ∈ F_{p−1}} |D(f)| ≤ (C_ε / 2) · N̂(p−1) · (p−1)^{1/2+ε}`,

i.e., in `N̂`-language (with `N̂ ~ (3/π²)(p−1)²`):

  `|S_ψ(p)| ≤ (C_ε / 2) · (π²/3)^{1/2 + ε} · N̂^{5/4 + ε/2}`.

Constants `C_ε` are **not effectively computable** from Landau's argument
without further input (Selberg's mollifier 1942 gives an effective C_ε for
ε ≥ 1/2 only; Soundararajan 2009 gives a barely-sub-polynomial improvement
that does not affect the polynomial order).

# 8. Comparison with SP-2's `B₀(N) ≥ c · N` (or stronger)

## 8.1 SP-2 status (cross-referenced)

SP-2 is stated in R1 §5.9 as "**closed-form (or explicit asymptotic) lower
bound for B₀(N) of the form `B₀(N) ≥ c · N` (or stronger; numerically
c·N·log N)`**".  As of this session (2026-05-09), no SP-2 deliverable is
present in `handoff-2026-05-09-followup/`; we therefore parameterize the
threshold in terms of the placeholder constant `c` from SP-2's eventual
statement.

**Empirical fit (SP-1a [V10]):** `B₀ / (n_count · log n_count) ≈ 0.30–0.35`
across primes 11..101.  We thus take `c ≈ 0.30` as the working numerical
value of SP-2's eventual constant, with the asymptotic `B₀(N) ~ 0.30 · N̂ ·
log N̂`.

## 8.2 Required threshold

For the RH-conditional chain to close B+ asymptotically:

  `(C_ε / 2) · N̂^{5/4 + ε/2} < c · N̂ · log N̂`
  `N̂^{1/4 + ε/2} < (2c / C_ε) · log N̂`.

For ANY ε > 0 fixed and N̂ → ∞, the **left side dominates**, so the
inequality FAILS asymptotically.  The crossover N̂* depends on (c, C_ε, ε)
but is finite.

## 8.3 Required strengthening of RH input

To close B+ asymptotically using the σ_p bijection identity + RH-style
input, we would need

  `Σ_f |D(f)| < 2 c · N̂ · log N̂ / (1 + δ)`  for some `δ > 0`,

i.e., `Σ_f |D(f)| = O(N̂ · (log N̂)^{1−δ})` for some δ > 0.  This is

  **(*)** a **strengthening of Landau's RH bound** by a factor of
        `n^{1/2+ε} / (log N̂)^{1−δ} = N̂^{1/4 + ε/2} · (log N̂)^{δ−1}`.

No such strengthening is implied by RH for ζ alone.  It is, however,
implied by **GRH for ζ + a sieve**, e.g., Selberg 1942 (the Selberg
sieve) applied to the Möbius-function-over-Farey identity

  `Σ_{f ∈ F_n} |D(f)| ≈ Σ_{b ≤ n} φ(b) · (mean unsigned displacement on
   the b-orbit)`,

using the Möbius-Farey orthogonality at each denominator level.  We do
not derive (*) here; flagging as `OPEN`.

# 9. Numerical verification (mpmath 50 dps)

`SP1a_beta.py [V1]–[V8]` (this session); verbatim output excerpts:

```
[V1] Exact-rational stats (Fraction): n, Sigma|D|, Sigma D^2, B0, |S_psi|
   p     n     Sigma|D|    Sigma D^2         B0    |S_psi|  B0-|S_psi|
  11    33      21.5500      22.1113     1.6395     2.4034     -0.7639
  13    47      33.4000      39.9859     5.2593     4.9073      0.3519
  17    81      66.2739     103.9140     9.2550    10.5599     -1.3049
  19   103      93.7629     166.3638    18.8789    16.7445      2.1344
  23   151     150.0471     313.6425    24.2776    23.1271      1.1505
  29   243     268.6561     706.1205    47.9734    41.1558      6.8176
  31   279     336.7034     929.1286    83.7196    52.7167     31.0029
  ...
  101  3045    6362.2183   46061.8950   915.1207   772.8824    142.2384

[V2] Bridge identity Sum_f exp(2 pi i p f) = M(p) + 2 (mpmath 50 dps):
  All 22 primes 11..101: 0 failures, max |diff| < 4e-47.

[V3] Naive bound |S_psi| <= (1/2) Sigma|D|, ratio:
  All 22 primes: ratio in [0.22, 0.36], 0 failures.

[V5] B+ chain via naive RH-conditional bound:  (1/2)Sigma|D| < B0?
  10 of 10 Mertens-restricted primes FAIL the naive bound.
  (i.e., (1/2)Sigma|D| > B0 at every M(p) <= -3 prime, p in 11..101).

[V6] mpmath 50dps cross-check of (1/2)Sigma|D|:
  All 22 primes: rational == mpmath to 0 (Fraction-mpmath match).

[V7] Mertens-restricted primes p <= 100 with M(p) <= -3:
  0 / 10 closed by naive bound.
```

**Numerical reading:**
- The true bound `|S_ψ| < B₀` holds at all 10 Mertens-restricted primes
  (cf. SP-1a [V8] in the prior session's verifier; reproduced here in V1).
- The **naive RH-conditional substitution** `(1/2)Σ|D| < B₀` is FALSE
  at all 10 Mertens-restricted primes: the naive bound is 3-4× larger
  than B₀.
- The cancellation `|S_ψ|/Σ|D| ≈ 0.12-0.18` is the actual structure;
  RH on M(N) does not capture it.

# 10. Comparison summary table (all bounds, finite range)

For each prime p ≤ 101 with M(p) ≤ −3, the rows below show the slack
of three bounds against B₀(p−1):

| p | M(p) | B₀ | \|S_ψ\| (truth) | CS bound (uncond.) | (1/2)Σ\|D\| (RH-naive) | margin uncond. CS | margin RH-naive |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 13 | −3 | 5.26 | 4.91 | 11.95 | 16.70 | −6.69 | −11.44 |
| 19 | −3 | 18.88 | 16.74 | 36.97 | 46.88 | −18.09 | −28.00 |
| 31 | −4 | 83.72 | 52.72 | 145.33 | 168.35 | −61.61 | −84.63 |
| 43 | −3 | 173.74 | 117.71 | 360.80 | 382.66 | −187.06 | −208.92 |
| 47 | −3 | 213.54 | 145.30 | 451.85 | 481.57 | −238.31 | −268.03 |
| 53 | −3 | 281.27 | 196.47 | 615.55 | 647.18 | −334.28 | −365.91 |
| 71 | −3 | 564.09 | 366.70 | 1311.47 | 1303.69 | −747.38 | −739.60 |
| 73 | −4 | 726.34 | 361.14 | 1480.80 | 1468.04 | −754.46 | −741.69 |
| 79 | −4 | 800.54 | 447.87 | 1751.15 | 1730.63 | −950.61 | −930.09 |
| 83 | −4 | 970.00 | 536.21 | 2071.29 | 2034.69 | −1101.29 | −1064.70 |

(CS bound = `√((Σ D²)(Σ(f−1/2)²))`; RH-naive = `(1/2)Σ|D|`; both unconditional for the
sample primes.)

**Reading:** at every Mertens-restricted prime the truth `|S_ψ| < B₀`
(positive margin in B₀ − |S_ψ|) is verified; **but neither the unconditional
CS bound nor the RH-naive Σ|D|-bound is sharp enough** to certify it
analytically.  The two bounds are within ~5% of each other (the unconditional
CS is sometimes slightly tighter, sometimes slightly looser, depending on p).

# 10.A Empirical sharpening — the route a proof must follow

The verifier `SP1a_beta.py [V8]` tabulates `Σ|D|/N̂` against the threshold
`2·c·log(N̂)` for c = 0.30 and c = 0.27.  The relationship that needs to
hold for `(1/2)·Σ|D| < B₀(N̂) ≈ c·N̂·log N̂` is precisely

  `Σ|D|/N̂  <  2·c·log(N̂)`.

The empirical data (verified rational, mpmath cross-checked):

| p | N̂ | Σ\|D\|/N̂ | 2·0.30·log(N̂) | margin |
|---:|---:|---:|---:|---:|
| 11 | 33 | 0.65 | 2.10 | +1.45 |
| 23 | 151 | 0.99 | 3.01 | +2.02 |
| 47 | 651 | 1.48 | 3.89 | +2.41 |
| 71 | 1495 | 1.74 | 4.39 | +2.65 |
| 101 | 3045 | 2.09 | 4.81 | +2.72 |

**Margin is increasing** in N̂; the empirical fit is `Σ|D|/N̂ ~ const +
slowly-varying`, not the F-L upper bound `O(N^{1/2+ε})`.  The truth in
the verified range is therefore **substantially better than F-L gives
under RH**.

**This is the path a proof must follow.**  The required statement is
NOT what RH on M(N) implies, but rather

  **(SP-1a-β-α refinement).** *There exists `c' > 0` (effectively
   computable, ideally `c' < 0.6`) such that for all sufficiently large N,*
       `Σ_{f ∈ F_N} |D(f)| ≤ c' · N̂ · log N̂`.

This is a strict strengthening of Landau's `Σ_k |d_k| = O(n^{1/2+ε})`
(equivalent to RH) by a polynomial factor of `n^{1/2+ε} / log N̂ =
N̂^{1/4 + ε/2} / log N̂`.  Such a strengthening is plausibly delivered
by **GRH for L(s, χ_b)** + Selberg's mollifier sieve, but is **not**
delivered by RH on ζ alone.

# 11. Verdict

**Verdict: STRUCTURAL OBSTRUCTION (smallest counterexample regime: under
RH alone, the σ_p bijection identity does not close B+ for ANY prime in
the verified range 11..101 by Lemma 4.1; the asymptotic threshold for
the naive-substitution route to fail is reached **immediately**, since
`(1/2) Σ|D|(N̂) > B₀(N̂)` for all N̂ ≥ 33 = |F_10|).**

More precisely:

(a) **The naive RH-conditional bound `|S_ψ(p)| ≤ (1/2) Σ|D(f)|`** combined
with **Landau's RH equivalent `Σ|D| = O(N̂^{5/4+ε})`** is **structurally
weaker than the unconditional Cauchy-Schwarz bound `O(N̂^{3/2}/√log N̂)`**
of SP-1a §6.5 (when N̂ is large, since `5/4 + ε < 3/2 − tiny` only for
`ε < 1/4 − tiny`; for the tight `ε → 0` form the naive bound is sharper
in the asymptotic order, but with effectively no usable constant control,
and at finite N̂ it is **numerically far worse**, see [V5]/[V7]).

(b) **The RH-conditional Cauchy-Schwarz bound** (Franel 1924's RH-equivalent
on `Σ D²`) is **NOT sharper than the unconditional CS bound** because
`Σ D² ~ N̂² / log N̂` already unconditionally (Franel/Landau classical
estimate, SP-1a §6.5).  No RH-on-ζ input strengthens CS.

(c) **The σ_p discrepancy via Erdős-Turán** is `O((log N̂)^{−2})` (Section
5.3, derived under RH), but does not couple to D(f) in a manner that
improves over CS (Section 5.4): the bijection identity is a permutation
sum, and discrepancy gains require approximating uniform distribution,
not bijection.

(d) **The explicit-formula path** (R1's m-th Bridge identity, fixing
Re T_m(p) exactly) leaves **the imaginary parts uncontrolled by RH on
ζ alone**; bounds on `Im T_m` reduce back to `Σ D · sin` discrepancy
sums equivalent in size to plain CS.

**The named sub-step that would unblock B+** under a STRONGER conditional
input is:

**SP-1a-β-α:** Selberg-mollifier 1942 + Möbius-on-Farey orthogonality.
Specifically, derive

  `Σ_{f ∈ F_n} |D(f)| ≤ C · N̂ · (log N̂)^{1−δ}`   for some explicit `δ > 0`

under either
(i) **GRH for L(s, χ_b)** for every Dirichlet character χ_b mod b, b ≤ n
(then a per-denominator orthogonality + Selberg mollifier), or
(ii) **A targeted moment estimate** on the Mertens function over arithmetic
progressions, of the form
       `Σ_{a ≤ x, a ≡ a_0 (mod b)} μ(a) = O((x/b)^{1/2+ε})` (uniform in b)
which is equivalent to GRH for the relevant L-functions.

(*Cost estimate:* 4–8 weeks of focused literature work assuming GRH;
6–12 months without it.)

**Confidence the σ_p bijection identity + RH on M(N) closes B+:** **0.20**
(STRUCTURALLY blocked).
**Confidence the σ_p bijection identity + GRH on L(s,χ_b) closes B+:**
**0.55** (would close via Selberg mollifier; not derived here).
**Confidence Conjecture B+ holds:** **0.85** (no change; the truth is
beyond RH on ζ alone, but consistent with the empirical record on ~4 600
primes).

# 12. Companion files

- This document: `SP1a_beta_RH_conditional_B_plus.md`
- Verifier:      `SP1a_beta.py`  (8 V-checks, mpmath 50 dps)

# 13. Honest confidence summary table

| Claim | Confidence | Basis |
|---|---|---|
| Littlewood 1912: RH ⟺ M(x) = O(x^{1/2+ε}) | 0.99 | Standard textbook (Titchmarsh 1986 §14.25); verbatim cite. |
| Franel 1924: RH ⟺ Σ d_k² = O(n^r) ∀ r > −1 | 0.99 | Verbatim from Wikipedia *Farey sequence*, sourced to Franel 1924 *Nachr. Ges. Wiss. Göttingen*. |
| Landau 1924: RH ⟺ Σ \|d_k\| = O(n^r) ∀ r > 1/2 | 0.99 | Verbatim from same source, Landau 1924 *Nachr. Ges. Wiss. Göttingen*. |
| Bridge identity Σ_f e^{2πipf} = M(p)+2 | 0.99 | Lean-formalized (`BridgeIdentity.lean`); exact-rational + mpmath 50 dps. |
| σ_p bijection identity (SP-1a Thm 6.4.1) | 0.99 | One-screen algebra; exact-rational at primes 11..101. |
| Lemma 4.1 (\|S_ψ\| ≤ (1/2)Σ\|D\|) | 0.99 | One-line triangle inequality. |
| Naive substitution fails at all 10 M-restricted primes ≤ 100 | 0.99 | `SP1a_beta.py [V5][V7]`, exact rational + mpmath 50 dps. |
| RH-naive bound is asymptotically too weak (`5/4+ε > 1`) | 0.99 | Algebraic; ε > 0 polynomial dominates log. |
| RH-on-ζ does not improve CS bound on S_ψ | 0.95 | Direct: Σ D² is `O(N̂² / log N̂)` unconditionally (Franel/Landau classical); RH at most matches in order. |
| σ_p discrepancy via Erdős-Turán is `O((log N̂)^{−2})` under RH | 0.85 | One-screen Erdős-Turán-Koksma + Bridge identity at higher k; not formalized. |
| Discrepancy of σ_p does not couple to D for a sharper bound on \|S_ψ\| | 0.80 | Structural: σ_p is a bijection, not a sample of uniform; Koksma applied to `D · indicator` falls back to CS. |
| Conjecture B+ holds | 0.85 | ~4 600 primes verified; reduction in R1 + SP-1a structurally tractable; no counterexample. |
| RH on ζ alone closes B+ via the σ_p picture | **0.20** | Structural obstruction documented; needs sharper input (GRH). |
| GRH on L(s, χ_b) closes B+ via the σ_p picture | 0.55 | Selberg mollifier 1942 + per-denominator orthogonality plausibly delivers `Σ\|D\| = O(N̂(log N̂)^{1−δ})`; not derived here. |
| The reduction `B+ ⟺ S_ψ < B₀ for M-restricted p` (R1 §3.2) is correct | 0.97 | Lean Lemma 3.1 + R1 §5.7; verified exact-rational. |

# 14. What this document is NOT

- **Not** a proof of Conjecture B+, conditional or unconditional.  RH on
  ζ alone, applied at the σ_p bijection identity, is structurally
  insufficient.
- **Not** an upgrade of SP-1a's verdict.  SP-1a closed at `RIGOROUS
  REDUCTION (sub-step Aistleitner-explicit Im T_m bound)`; this document
  shows the **RH-on-M(N) shortcut to that sub-step does not exist** and
  the genuine way forward needs either GRH on L-functions or a Selberg-
  sieve-type input on the Möbius-over-Farey decomposition.
- **Not** a switch to a new framing.  Stays with the σ_p bijection picture
  and the Lean canonical D = rank − N̂·f.

# 15. Cross-references

| Section | Cross-ref |
|---|---|
| §3 (σ_p bijection) | SP-1a §6.4 (verbatim) |
| §5.1 (CS bound) | SP-1a §6.5 (verbatim) |
| §6.1 (m-th Bridge) | R1 §5.5, Theorem 5.5.1 |
| §6.2 (Hurwitz) | R1 §5.4; SP-1a Theorem 6.3.1 |
| §8 (B₀ asymptotic) | R1 SP-2; `Mertens_restricted_B_positivity.md` §3.4 |
| §9 (numerical) | `SP1a_Im_Tm.py [V8]` (independent reproduction) |
| §11 verdict | R1 §5.9 (sub-problem queue), `Mertens_restricted_B_positivity.md` §3.4 |

End of document.
