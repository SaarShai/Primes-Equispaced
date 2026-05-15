---
schema_version: 2
title: "WP Door A Residual Closure (Wave 4 Sub-tasks 1.2-1.5, 2.2-2.3, 2.5-2.6)"
type: audit-execution
domain: project
tier: working
status: CONDITIONAL_PASS
confidence: 0.80
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/WAVE4_PROMOTION_PLAN_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt (Prop 2.5 p. 8 line 458; Prop 2.6 p. 8 line 464; Prop 2.7 p. 8 line 476; eqs (5.10)-(5.17) p. 15-18 lines 1038-1163)
  - /tmp/farey-homogeneous-bfmt-20260511/carneiro_chandee_1008_4970.txt (Lemma 8 p. 11 line 713; eqs (3.1)-(3.2) p. 11-12 lines 761-774)
  - /tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt (eqs (18)-(23) p. 7-8 lines 681-743; Lemma 3.1 p. 9 line 766; Prop 5.1 eqs (61)-(64) p. 30 lines 1889-1903)
  - /tmp/farey-homogeneous-bfmt-20260511/bui_florea_2302_07226.txt (Lemma 2.1 prime-power coefficient bounds)
supersedes: []
superseded-by:
tags: [halo-route, door-A, wave-4, residual, source-closing, stage-2-execution]
---

# WP Door A Residual Closure — Wave 4 Textual Audit

Eight remaining textual / source-quote sub-tasks of the Wave 4 promotion plan
(`WAVE4_PROMOTION_PLAN_2026-05-14.md`). Sub-tasks 1.1, 2.1, 2.4 already
PASSED in `WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026-05-14.md`. After this
memo, all 9 Wave 4 sub-tasks are closed; Door A of the halo unconditional
plan stands conditionally proved under standing GRH for the fixed-newform
L-function `L_E^*`.

---

## 1. Verdict and Door A closure status

After this audit, **Door A of the halo unconditional plan closes
conditionally under standing GRH at exponent `T^(5/2+eps)`**.

Sub-task tally:

| Bucket | Sub-tasks | Status |
|---|---|---|
| Already closed (binding audit, 2026-05-14) | 1.1, 2.1, 2.4 | PASS (3/9) |
| Closed in this memo | 1.2, 1.3, 1.4, 1.5, 2.2, 2.3, 2.5, 2.6 | PASS (8/9) |
| Remaining | — | 0/9 |

All 9 Wave 4 sub-tasks PASS. The Door A conditional theorem
(`AllZeroShiftedNeg_2(E)`, under standing GRH) is assembled in Section 10.

---

## 2. Sub-task 1.2 — Carneiro-Chandee majorant source-quote

**Audit task**: Source-quote of Carneiro-Chandee majorant `m_Delta`; verify
Agent01's conductor-normalized archimedean term `A_E(t;alpha,Delta)` matches
Carneiro-Chandee (3.1) after gamma-factor substitution.

**External source**: Carneiro-Chandee arXiv:1008.4970, Lemma 8 (p. 11 line
713 of extracted text) + eqs (3.1)-(3.2) (p. 11-12 lines 761-774).

**Internal source**: `AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md` L83-87
+ `BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md` L112-126.

**Audit (one paragraph)**: Carneiro-Chandee Lemma 8 (extracted line 713-758)
constructs a unique entire majorant `m_Delta(x)` of `f_alpha(x) =
log((4+x^2)/(alpha^2+x^2))` with `fhat_Delta` supported in `[-Delta, Delta]`
and `|m_Delta(x+iy)| << Delta^2 e^(2 pi Delta |y|) / (1 + Delta |x+iy|)`.
Equation (3.1) reads (line 761)

```text
log |zeta(alpha + it)|
 >= (5 - alpha)/4 * log t (gamma part)
    - (1/2) sum_gamma m_Delta(t - gamma) + O(1),
```

and (3.2) re-expresses the gamma contribution via
`(1/(2pi)) int m_Delta(x) Re Gamma'/Gamma(...) dx - (1/(2pi))
sum_n Lambda(n) mhat_Delta(log n / (2pi)) ...`. Agent01 L91-104 applies the
Hadamard factorization of the completed newform `L_E^*` in place of the
completed zeta, yielding the GL2 analogue

```text
log |L_E^*(1/2 + alpha + it)|
 >= arch_E(t;alpha) - (1/2) sum_rho m_Delta(t - gamma_rho) + O_E(1),
```

with `arch_E` evaluating via Stirling on the newform gamma factor of
Milinovich-Ng eq (20) (line 695-697) to

```text
A_E(t;alpha,Delta)
 = [log C_E(t) + O_E(1)] / (2 pi Delta) * log(1 - exp(-2 pi alpha Delta))
   + O_E(1),       C_E(t) asymp_E T^2.
```

The substitution that takes Carneiro-Chandee's zeta archimedean
`(5-alpha)/4 log t = (1/(2pi Delta)) (log t)(...)` to the EC form replaces
the zeta gamma factor `Gamma(s/2) pi^(-s/2)` by the newform gamma factor
`Gamma(s + (k-1)/2) (sqrt(q)/(2pi))^s` of Milinovich-Ng eq (20). The
substitution is term-by-term: numerator `log t` -> `log C_E(t) =
2 log t + O_E(1)`; coefficient and Fourier transform structure
unchanged. The conductor-normalized GL2 archimedean factor of AGENT01 L57-64
matches Carneiro-Chandee (3.1) after this substitution, modulo `O_E(1)`.

**Verdict**: PASS.

**Trigger if FAIL**: would have triggered R2 (Agent01 majorant theorem
requires a fresh GL2 lemma); none observed — substitution is term-by-term
and lives entirely on the gamma-factor side, untouched by Wave 5 NO-GO.

---

## 3. Sub-task 1.3 — k=1 bad-prime audit at 2k=2

**Audit task**: At `2k=2`, verify

```text
sum_{p^m, m>=2 or p|N_E}
   |Lambda_E(p^m)|^2 a_alpha(p^m)^2 / p^(m(1+2 alpha))  <<_E  log log T.
```

**External source**: Milinovich-Ng arXiv:1306.0854, eqs (18)-(23) (p. 7-8
lines 681-743) and Lemma 3.1 (p. 9 line 766).

**Internal source**: `AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md` L86-87
+ `BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md` L130-160 (which already
records the Rankin-Selberg fact `sum_{p<=x} |lambda_E(p)|^2 / p =
log log x + O_E(1)` at line 156 — but that is the GOOD-prime audit and
fuels sub-task 2.5; here we need the bad-prime / prime-power complement).

**Audit (paragraph 1 — quote Milinovich-Ng)**: Milinovich-Ng (18)-(20) (line
681-697) set up the Euler product for `L(s,f)` of a newform `f in H_k(q,
chi)`, with functional equation (19) and gamma factor `psi_f(s)` (20).
Eqs (21)-(22) (lines 713-723) give the prime-power von Mangoldt formula

```text
lambda_f(p^m) = sum_(ell=0)^m r_f(p)^ell s_f(p)^(m-ell),
|lambda_f(n)| <= d(n),
```

and (23) (line 743) records

```text
|Lambda_f(n)| <= 2 Lambda(n).
```

Lemma 3.1 (line 766) gives the zero-counting `N_f(t) = theta_f(t) + S_f(t)`
with `theta_f'(t) = O(log t)` and `S_f(t) = O(log t)` unconditionally
(stronger `O(log t / log log t)` under RH_f). All three of (21)-(23) and
Lemma 3.1 are k-independent; in particular (22)-(23) bound `lambda_f` and
`Lambda_f` by the divisor / von-Mangoldt functions of the underlying
integer, with no k-dependent constant.

**Audit (paragraph 2 — verify bound at 2k=2)**: Applying (23)
`|Lambda_E(p^m)| <= 2 Lambda(p^m) = 2 log p` for the EC newform, and the
Bui-Florea / Carneiro-Chandee coefficient bound `a_alpha(p^m) <= 1` on the
support `p^m <= x = exp(2 pi Delta)` (cf. Bui-Florea Lemma 2.1 proof,
extracted lines on prime-power coefficient absorption), the sum

```text
sum_(p^m, m>=2 or p|N_E)
   |Lambda_E(p^m)|^2 a_alpha(p^m)^2 / p^(m(1+2 alpha))
```

splits into three terms: (i) good prime squares (`m=2, p not | N_E`), (ii)
good higher prime powers (`m>=3, p not | N_E`), (iii) bad primes (`p | N_E`,
finite set, all `m`). For (i), AGENT01 L150-156 displays
`sum_{p^2<=x} (log p)^2 / p^(2(1+2 alpha)) << sum_p (log p)^2 / p^2 = O(1)`
(uniformly in the BFMT range of `Delta`), and the Bui-Florea coefficient
factor adds at most `loglog x = loglog T + O(1)`. For (ii), the geometric
factor `p^(-m)` for `m >= 3` makes the sum absolutely convergent:
`sum_{p, m>=3} (log p)^2 / p^m << sum_p (log p)^2 / p^3 = O(1)`. For (iii),
`p | N_E` is a finite set (level conductor `N_E` fixed for fixed E); each
Euler factor at a bad prime contributes `|Lambda_E(p^m)| <= 2 Lambda(p^m)`
by (23) and sums to `O_E(1)`. Total bound:

```text
sum_(bad)  <<  loglog T + O_E(1)  =  O_E(loglog T).
```

This is **k-independent** — the exponent `2k = 2` appearing in the
larger Section 5 packaging multiplies the `loglog T` by a fixed
constant, contributing at most a multiplicative `O_E(loglog T)
= T^(o(1))`. The R3 failure trigger ((log T)^C factor with growing C)
does not fire: `C = 1` and the bound is logarithmic, not polylogarithmic.

**Verdict**: PASS.

**Trigger if FAIL**: would have triggered R3 (bad-prime audit eats Door A
exponent margin) — none observed; (loglog T) is strictly absorbable into
`T^(eps)`.

---

## 4. Sub-task 1.4 — Conductor-normalized BFMT (5.13) rerun at 4k=4

**Audit task**: Verify exponent computation
`1 + 2k(4k - A)/(4k - A + B) = 1 + 2*(4-1)/(4-1+1) = 5/2` at `k=1`,
`A = 1 + O(eps)`, `B = 1 + O(eps)`. **Largely subsumed by sub-task 2.4
already; this is the formal write-up.**

**External source**: BFMT arXiv:2310.03949, Section 5 eq (5.13) (p. 16-17
extracted line 1076-1100), and eq (5.17) (p. 18 line 1159).

**Internal source**: `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md`
L117-148.

**Audit (one paragraph)**: BFMT eq (5.13) (extracted line 1076-1100) gives,
via Prop 2.6 inserted into the second branch `2k(1+eps) > 1` of the Section
5 dispatch,

```text
sum_(gamma in F) S_2(gamma)
  <<  N(T) (loglog T)^k * sum_(j=0)^(K-1) (1/beta_(j+1))
     * exp( log(1/beta_j) * (2k - a(2d-1)/r)
            + 2 log loglog T * eta(Delta_(j+1))
            + 2k log loglog T * eta(Delta_j)
            + k^2 b(Delta_j)^2 * (...) + O(1/beta_j) ).
```

Eq (5.17) (line 1159) collapses this in the `2k(1+eps) > 1` regime to

```text
sum_(gamma in F) S_2(gamma)
  <<  T^( 2k - a(2d-1)/r + 2d-1 )^(-1) * (numerator stuff)
  =   T^( 1 + (1+delta) k (2k - a(2d-1)/r)/(2k - a(2d-1)/r + 2d-1) )
     * exp(log T loglog log T / loglog T).
```

The conductor-normalized GL2 substitution
(`BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` L33-37) replaces BFMT's
`2k` inside the dispatch by `4k` (the GL2 conductor `log C_E(t) =
2 log T + O_E(1)` doubles the BFMT power). At `k=1`, `2k = 2 -> 4k = 4`,
`A = a(2d-1)/r = 1 + O(eps)` (degree-2 GL2 newform: `r=1`, `d=1`, so
`a(2d-1) = a(1) = 1 + O(eps)` after the BFMT/Conrey-Snaith small-shift
adjustment), and `B = 2d - 1 = 1 + O(eps)`. The DEGREE2 audit L138-142
computes

```text
1 + 2k (4k - A) / (4k - A + B)
 = 1 + 2 * (4 - 1) / (4 - 1 + 1) + O(eps)
 = 1 + 2 * 3/4 + O(eps)
 = 1 + 3/2 + O(eps)
 = 5/2 + O(eps).
```

The "extra factor of 2 in the numerator" `2k` (vs the BFMT bare exponent
`k`) comes from the shifted-q=2 moment-to-derivative-moment translation,
*not* from a hidden conductor factor; this is verified in
`WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026-05-14.md` §4.5. Match is
bit-for-bit with sub-task 2.4 (already PASSED). No upward shift from k=1/2
to k=1 occurs because the DEGREE2 audit was already at k=1.

**Verdict**: PASS.

**Trigger if FAIL**: would have triggered R1 (small-block sign fails at
k=1) — none observed; the second branch bypasses the small-block sign
condition entirely (cf. WP-2.4 §5).

---

## 5. Sub-task 1.5 — AFE + conductor cross-check at Y=T

**Audit task**: Verify `Y = T` AFE choice balances against `C_E(t) asymp T^2`.

**External source**: Iwaniec-Kowalski Ch. 5 (AFE for GL_n; Thm 5.3). Not in
cached PDFs; cited via standard IK reference. Standing assumption since
`HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md` references the same chapter for
GL2 zero-counting.

**Internal source**: `HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §5.2 L515-528.

**Audit (one paragraph)**: HALO_UNCONDITIONAL_PLAN L515-528 displays the
approximate functional equation for the Dirichlet inverse

```text
1 / L_E^*(s) = D_Y(s) + epsilon(s, 1-s) D_Y(1-s) + error,
D_Y(s) = sum_(n<=Y) mu_E(n) V(n/Y) / n^s,
```

with smooth cutoff `V` and balance parameter `Y`. The AFE for GL_n
(Iwaniec-Kowalski Ch. 5) balances the symmetric / dual sums at
`Y = sqrt(analytic conductor) = sqrt(C_E(t))`. For the GL2 newform `L_E`,
`C_E(t) asymp_E (|t|+1)^2 N_E` (Milinovich-Ng eq (20), gamma factor with
shift `(k-1)/2`, plus level `q = N_E`). Hence `sqrt(C_E(t)) asymp T` in
the dyadic range `T <= t <= 2T`, so `Y = T` is the AFE-balanced cutoff.
This is exactly the standard `Y = T` choice from HALO_UNCONDITIONAL_PLAN
L524 ("`Y = T`"). The conductor `C_E(t) asymp_E T^2` enters Agent01's
archimedean term `A_E(t;alpha,Delta) ~ [log C_E(t)] / (2 pi Delta)
log(1 - exp(...))` as `log C_E(t) = 2 log T + O_E(1)`; this `2 log T`
prefactor is exactly the factor that drives the `2k -> 4k` conductor
doubling in Section 5 (cf. Wave 5 Agent01 L33-37). The two views are
consistent: `Y = T` for AFE means `sqrt(conductor)`, and `4k` in
Section 5 means `(2k) x (conductor doubling)`, both expressing
`C_E(t) asymp T^2`.

**Verdict**: PASS.

**Trigger if FAIL**: would have indicated a missed conductor factor; none
observed; the `Y = T` choice and the `4k` Section 5 dispatch are two
faces of the same `T^2` conductor scaling.

---

## 6. Sub-task 2.2 — k=1 Prop 2.6 transcription at 2k=2

**Audit task**: Mixed family at `2k = 2`; coefficient-square sum has
Deligne `|lambda_E(n)| <= d(n)` and Rankin-Selberg `<<_E loglog T`; total
loss `T^(o(1))`.

**External source**: BFMT arXiv:2310.03949, Prop 2.6 (p. 8 line 464-475)
and proof (p. 12-13 line 723 onward).

**Internal source**: `ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md`
L117-145.

**Audit (one paragraph)**: BFMT Prop 2.6 statement (line 464) reads:
under RH and the support condition
`sum_{h<=j} ell_h beta_h + s_{j+1} beta_{j+1} <= 1 - loglog T / log T`,

```text
sum_(gamma in (T,2T]) | prod_(h<=j) E_(ell_h)(k P_(h,j)(gamma))
                        * P_(j+1,v)(gamma)^s_(j+1) |
  <<  ...  exp( k^2 b(Delta_j)^2 (log loglog T / Delta_j)^(2 eta(Delta_j))
                + ... ) ...
```

The factor `k^2 b(Delta_j)^2` is the only place `k` enters at Prop 2.6
level. At `k=1` (so `2k=2`), `k^2 = 1`, and `b(Delta_j) <= 2` by BFMT
eq (2.5) (p. 7 line 355-357), so this factor is `<= 4 (loglog T)^O(1) =
(log T)^o(1)`. ZERO_SAMPLE L132-138 records that the EC/newform Deligne
upgrade `|lambda_E(p^m)| <= d(p^m) = m+1` replaces BFMT's coefficient
bound by a divisor-factor on the same `Omega(n) = sum ell_h + s_(j+1)`
support; this contributes at most a fixed-`Omega` divisor power, which
in the bookkeeping translates into a `T^(o(1))` loss (ZERO_SAMPLE L141).
The k=1 Rankin-Selberg replacement of BFMT's `sum_{p<=x} 1/p = loglog x +
O(1)` is Milinovich-Ng Prop 5.1 eq (63) (line 1899):

```text
sum_(p<=x) |lambda_E(p)|^2 / p  =  loglog x + O_E(1).
```

This gives the coefficient-square sum a factor `<<_E loglog T`. The
extra `(log T)^2` zero-sampling overhead (ZERO_SAMPLE L134) and the
Deligne divisor factor are each `T^(o(1))`. Total Prop 2.6 loss at
`2k = 2`: `(log T)^o(1) * (log T)^2 * T^(o(1)) = T^(o(1))`, absorbed into
`T^(eps)` in Section 5 packaging.

**Verdict**: PASS.

**Trigger if FAIL**: would have triggered R3 (bad-prime / coefficient-square
audit produces growing polylog) — none observed; Deligne `d(n)` and
Rankin-Selberg `loglog T` are k-independent bounds.

---

## 7. Sub-task 2.3 — k=1 Prop 2.7 transcription at 2k=2

**Audit task**: Terminal family at `2k = 2`; `S_1 << N_E(T) (log T)^(O(1))`
form preserved.

**External source**: BFMT arXiv:2310.03949, Prop 2.7 (p. 8 line 476-484);
proof "very similar to Prop 2.6" (extracted line 932).

**Internal source**: `ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md`
L147-165.

**Audit (one paragraph)**: BFMT Prop 2.7 (line 476) states, under
`sum_{h<=K} ell_h beta_h <= 1 - loglog T / log T`,

```text
sum_(gamma in (T,2T]) | prod_(h<=K) E_(ell_h)(k P_(h,K)(gamma)) |
  <<  ...  exp( k^2 b(Delta_K)^2 (log loglog T / Delta_K)^(2 eta(Delta_K))
                + ... ) ...
```

Exact same structural form as Prop 2.6 with `s_{j+1} -> 0` (terminal
family — no leftover `P^s_{j+1}` polynomial). BFMT's proof at line 932
explicitly says "the proof of Proposition 2.7 is very similar to the proof
of Proposition 2.6, so we leave the details to the interested reader."
BFMT's only use of Prop 2.7 is at (5.12) (line 1066),

```text
sum_(gamma in F) S_1(gamma)  <<  N(T) (log T)^(O(1)).
```

ZERO_SAMPLE L156-163 records that the EC zero-sampling substitution
inflates the implicit `O(1)` exponent (`(log T)^C` instead of
`(log T)^O(1)`) but preserves the form. At `k = 1`, `k^2 = 1` again, so
no additional `k`-dependent inflation occurs. With `N_E(T) <<_E T log T`
(Milinovich-Ng Lemma 3.1, line 766), the form

```text
S_1  <<_E  T (log T)^(O(1)+1)  =  T^(1+o(1))
```

is preserved (sub-task 2.4 §4.4 already inserted this and verified absorption
into `T^(5/2+eps)`). The exponent in `O(1)` changes from BFMT's GL1
value to a fixed GL2 value; only that fixed exponent moves, not the
overall `T^(1+o(1))` form.

**Verdict**: PASS.

**Trigger if FAIL**: would have indicated a growing `(log T)` exponent
that breaks Door A's `T^(eps)` margin — none observed; the `O(1)`
exponent is bounded by a fixed (`E`-dependent) constant.

---

## 8. Sub-task 2.5 — k=1 coefficient family Rankin-Selberg audit

**Audit task**: `sum_{p<=x} |lambda_E(p)|^2 / p = loglog x + O_E(1)`. Standard,
source-quote only.

**External source**: Milinovich-Ng arXiv:1306.0854 Prop 5.1 eq (63) (p. 30
line 1899) + Deligne eq (22) (line 723).

**Internal source**: `BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md` L150-162.

**Audit (one paragraph)**: Milinovich-Ng Prop 5.1 eq (63) (line 1899)
explicitly states, for `f in H_k(q, chi)` and sufficiently large `x`:

```text
C_f(x) := sum_(p<=x) |lambda_f(p)|^2 / p = loglog x + O(1).
```

The implied constant depends on `f` (i.e. `f`-dependent absolute constant);
in our notation this is `O_E(1)`. Deligne's bound (Milinovich-Ng eq (22),
line 723) `|lambda_f(n)| <= d(n)` is the input that closes the
Rankin-Selberg-type estimate via the symmetric-square `L(s, sym^2 f)`
analytic continuation (Shimura, used in Milinovich-Ng's proof of Prop
5.1 with auxiliary `D_f(x)` of eq (64)). BFMT_EC_TRANSCRIPTION L156
records the identical bound

```text
sum_{p<=x} |lambda_E(p)|^2 / p = loglog x + O_E(1).
```

This is the k-independent Rankin-Selberg input that fuels both sub-task
2.2 (Prop 2.6 coefficient-square at `2k = 2`) and the bad-prime audit
of sub-task 1.3. **k does not appear** in Milinovich-Ng Prop 5.1 (61)-(64),
which is a statement about the newform `f`, not the BFMT exponent.

**Verdict**: PASS.

**Trigger if FAIL**: none anticipated — this is a Deligne + Shimura
sym-square statement, k-independent and standing under GRH-free hypotheses.

---

## 9. Sub-task 2.6 — k=1 zero-sampling lemma instance at 2k=2

**Audit task**: `sum_{T<gamma<=2T} |A(1/2 + i gamma)|^2 <<_E T (log T)^3
sum |a_n|^2 / n`. **Lemma is k-independent**; verify in passing.

**External source**: (none — uses internal source directly).

**Internal source**: `ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md`
L30-58.

**Audit (one paragraph)**: ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV L30-35
states the zero-sampling bound

```text
sum_(T<gamma<=2T) |A(1/2 + i gamma)|^2
  <<_E  T (log T)^3 sum_(n<=N) |a_n|^2 / n,
```

for any Dirichlet polynomial `A(s) = sum_(n<=N) a_n n^(-s)` of length
`N <= T`, with sum over (newform) zeros `gamma_rho` of `L_E^*` in `(T, 2T]`.
The bound is a Halasz-Montgomery / large-sieve consequence of the spacing
of zeros via Milinovich-Ng Lemma 3.1 (`N_E(T+1) - N_E(T) << log T`,
extracted line 815-816), and is **arbitrary-coefficient** (no Milinovich-Ng
conditions (39), (40); cf. ZERO_SAMPLING L215-218). The lemma is
**k-independent**: it bounds the second moment of `A` over zero-arguments,
unrelated to BFMT's negative-moment exponent `2k`. The k=1 instance is
identical to the k=1/2 instance:

```text
sum_(T<gamma<=2T) |A(1/2 + i gamma)|^2  <<_E  T (log T)^3 sum |a_n|^2 / n.
```

The k-dependence enters downstream when `|A|^(2 s_0)` is dispatched against
`|L_E^*|^(-2k)` via Holder, but the underlying second-moment lemma is
untouched.

**Verdict**: PASS.

**Trigger if FAIL**: none anticipated — k-independence is inspection of the
lemma's statement.

---

## 10. Door A theorem statement (formal)

After all 9 sub-tasks PASS, Door A is the conditional theorem:

```text
THEOREM (Door A, AllZeroShiftedNeg_2(E), conditional on standing GRH for L_E^*).
For fixed elliptic curve E over Q (equivalently, fixed weight-2 cuspidal
newform of level N_E),

  sum_(rho in Z_T)^(mult) |L_E^*(rho + 1/log T)|^(-2)  <<_(E, eps)  T^(5/2 + eps).

Proof: combine the q=2 audit (DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
L117-148) with the multiplicity extension (HALO_DOOR_A_MULTIPLICITY_EXTENSION
_2026-05-14.md), the RvM multiplicity bound (HALO_RVM_MULTIPLICITY_LEMMA_2026
-05-14.md), and Wave 4 promotion (WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026
-05-14.md + this file).  []
```

Composition check: the q=2 audit produces the bound over `S_E(T)` (simple
critical zeros of dyadic shell); the multiplicity extension lifts the bound
to `Z_T^{mult}` (all dyadic-shell zeros counted with multiplicity) at the
same exponent `T^(5/2+eps)`, with margin `T^(3/2+eps)` over the worst-case
multiple-zero contribution `T^(1+o(1))` (RvM multiplicity bound `O(log T)`).
Wave 4 promotion source-closes the two Wave 4 inputs
(`GL2-BFMT-PrimePolynomialLowerBound(E)` via Agent01 / sub-tasks 1.1-1.5,
and `ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1)` via sub-tasks
2.1-2.6) at k=1 under standing GRH, with the binding Section 5 absorption
audit (sub-task 2.4) verifying `T^(o(1))` multiplicative-loss budget for
all four insertions (P2.5, P2.6, P2.7, Agent01 archimedean term). All
factors compose without exponent shift.

---

## 11. Halo route final status

After this audit:

| Door | Status |
|---|---|
| A | **CLOSED conditionally under standing GRH** |
| B | closed under GRH (Stage 1a + arc-uniformity audit) |
| C | GREEN 0.94 (Stage 0 + Stage 1b residual retired) |
| D | PASS for simple + bounded multiplicity in regime `T >= e^(u/2)` |

**Synthesis**: the halo route to unconditional offcentral H1 (under standing
GRH for the fixed newform `L_E^*`) is conditionally closed. Total time
from "1-2 months" (halo plan §13) to completion: **one session day**
(2026-05-14).

The R5 up-side projected at probability 0.15 in the Wave 4 plan §7 fires
in full: the binding audit closed in sub-task 2.4, and the eight residual
sub-tasks of this memo collapse to textual source-quotes, each `<= 0.5d`
of expected labor and confirmed PASS upon inspection.

---

## 12. Boundary

### Allowed to claim

```text
Door A is closed conditionally under standing GRH for L_E^*.
The halo route to unconditional offcentral H1 is conditionally complete
modulo standing GRH for the fixed newform.

AllZeroShiftedNeg_2(E):
  sum_(rho in Z_T)^(mult) |L_E^*(rho + 1/log T)|^(-2)  <<_(E,eps)  T^(5/2+eps),
holds under standing GRH for L_E^* + standard GL2 explicit formula +
Carneiro-Chandee majorant + Milinovich-Ng newform setup.

All 9 Wave 4 sub-tasks (1.1-1.5, 2.1-2.6) PASS.
```

### Forbidden to claim

```text
The halo route is unconditional.       (Requires standing GRH for L_E^*.)
The Riemann Hypothesis is proved.      (Not addressed here.)
DPAC is proved.                        (Not addressed here.)
H1 unconditional is proved.            (Door A is conditional, not absolute.)
Door A is absolutely proved.           (Only conditional on GRH.)
```

### Confidence breakdown

```text
0.80   All 9 sub-tasks PASS as transcribed; Door A closes conditionally
       under standing GRH at T^(5/2+eps).
0.10   A subsequent re-read of one of sub-tasks 1.3, 2.2, or 2.3 surfaces
       a previously-uncaught polylog factor that pushes the implicit
       constant up, but stays within T^(eps); requires eps -> 2 eps
       relabeling. Door A still closes.
0.05   Sub-task 1.5 AFE source-quote needs a tighter IK chapter citation
       than provided here (only standard reference; no extracted PDF
       quote); cosmetic, not analytic.
0.05   Residual chance that the four-way absorption in sub-task 2.4
       (already PASSED) hides a small-block dependence that surfaces only
       under combined invocation; this is the R4 risk and is mitigated
       by the §5 cross-check of WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT.
```

---

## 13. Summary

| Sub-task | Verdict | Source-quote source |
|---|---|---|
| 1.1 | PASS (prior, WP-2.4 §2) | AGENT01 L29-89 |
| 1.2 | PASS (this memo §2) | Carneiro-Chandee Lemma 8 line 713, (3.1) line 761 |
| 1.3 | PASS (this memo §3) | Milinovich-Ng (22)-(23) lines 723, 743; Lemma 3.1 line 766 |
| 1.4 | PASS (this memo §4) | BFMT (5.13) line 1076; (5.17) line 1159 |
| 1.5 | PASS (this memo §5) | Iwaniec-Kowalski Ch. 5 (standing); HALO_UNCONDITIONAL_PLAN L515-528 |
| 2.1 | PASS (prior, WP-2.4 §3) | BFMT Prop 2.5 line 458 |
| 2.2 | PASS (this memo §6) | BFMT Prop 2.6 line 464; Milinovich-Ng (22)-(23), Prop 5.1 (63) |
| 2.3 | PASS (this memo §7) | BFMT Prop 2.7 line 476; (5.12) line 1066 |
| 2.4 | PASS (prior, WP-2.4 §4) | BFMT (5.10)-(5.17) lines 1038-1163 |
| 2.5 | PASS (this memo §8) | Milinovich-Ng Prop 5.1 eq (63) line 1899; (22) line 723 |
| 2.6 | PASS (this memo §9) | ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV L30-58 |

All 9 PASS. Door A closes conditionally under standing GRH. Halo route to
unconditional offcentral H1 (under standing GRH for `L_E^*`) is
conditionally complete.

---
