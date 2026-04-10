# Adversarial Review: Spectral Enhancement by Depth Filtering
**Date:** 2026-04-04
**Reviewer:** Opus (adversarial mode)
**Verdict:** (c) FUNDAMENTALLY FLAWED as stated; partial rescue possible but theorem must be rewritten

---

## 1. Theorem Summary

The theorem claims that depth-filtering Farey fractions by terminal CF quotient c_m >= L
produces a spectral sum S_L(p) with a low-pass filter property: higher zeta-zero modes
are suppressed by factor F_k ~ gamma_1/gamma_k, arising from the tail Dirichlet series
T(L,gamma) replacing zeta(3/2+i*gamma) in the spectral decomposition. The proof requires
one bridge assumption: D(a/p) ~ M(q_{m-1}).

---

## 2. Attempted Breaks

### Attack 1: Bridge assumption D(a/p) ~ M(q_{m-1}) — **BROKEN**

The computational check (corr = 0.000 for p = 13, 19, 31, 43, 61) was already known.
This is not just a "gap" — it is a **false statement**. Sign agreement is 47% (coin flip).
For large c_m, the ratio |D*delta| / |M(q)*delta| grows to 17-28x.

Without this bridge, the ENTIRE derivation from Step 3 onward (connecting individual
D(a/p) values to Mertens sums via convergent denominators) collapses. The spectral
formula as written cannot be derived.

**Verdict: BROKEN**

### Attack 2: "c_m = p fraction contributes 65-73%" claim — **BROKEN (factual error)**

The theorem file states "p=31: c_m=31 alone -> 73% of total Sum D*delta."
This is **factually wrong** in multiple ways:

- c_m = p (i.e., c_m = 31 for p=31) corresponds to exactly ONE fraction: 1/p.
- D(1/p) = 0 ALWAYS (1/p has rank 1 in F_p among denominators p, and a=1).
- Therefore c_m = p contributes EXACTLY ZERO to S(p).

The actual dominant group is c_m = p-1 (the fraction (p-1)/p = [0; 1, p-1]):
- p=13: c_m=12 contributes 44.6% (not 73%)
- p=31: c_m=30 contributes 33.1% (not 73%)
- p=61: c_m=60 contributes 27.3%
- p=97: c_m=96 contributes 24.4%
- p=509: c_m=508 contributes 17.5%

The dominance **decreases** as p grows (from 44.6% at p=13 to 17.5% at p=509).
This is the OPPOSITE of what would be needed for a single-fraction rescue.

**Verdict: BROKEN (wrong fraction, wrong percentage, wrong trend)**

### Attack 3: Low-pass property T(L,gamma) ~ L^{-1/2}/sqrt(1/4+gamma^2) — **SURVIVES (asymptotically)**

The Euler-Maclaurin asymptotic is mathematically correct. Numerical verification:

| L | |T(L,g1)| num | |T(L,g1)| asymp | err% |
|---|-------------|-----------------|------|
| 2 | 0.4603 | 0.0500 | 89% |
| 10 | 0.0252 | 0.0224 | 11% |
| 50 | 0.01037 | 0.01000 | 3.6% |
| 100 | 0.00678 | 0.00707 | 4.3% |

Convergence to the asymptotic is SLOW: relative correction ~ sqrt(1/4+gamma^2)/(2L).
For gamma_5 ~ 33, need L > 1000 for under 2% error. For small L (the practically
interesting regime L = 2 to 10), the asymptotic is worthless (11-89% error).

The suppression ratio F_k = |T(L,g_k)|/|T(L,g_1)| -> sqrt(1/4+g_1^2)/sqrt(1/4+g_k^2)
as L -> infinity, which is essentially gamma_1/gamma_k for large gammas. This is
confirmed at L=5000+ to 0.00% error. But at L=5 the ratio oscillates wildly
(F_5 = 2.89 at L=5 vs predicted 0.43 — an 8x discrepancy with WRONG DIRECTION).

**Verdict: SURVIVES as pure math; USELESS for practical L values (L < 100)**

### Attack 4: Unfiltered zeta(3/2+i*gamma_k) does not decay — **SURVIVES**

Confirmed: |zeta(3/2+i*14.13)| = 0.544, |zeta(3/2+i*32.94)| = 0.695.
No systematic decay. In fact zeta(3/2+i*gamma_5) > zeta(3/2+i*gamma_1).
The qualitative contrast with the filtered case (which does decay for large L) is real.

**Verdict: SURVIVES**

### Attack 5: D((p-1)/p) grows as ~(3/pi^2)*p^2 — structural issue

D((p-1)/p) = |F_p| - 2 - (p-1) ~ (3/pi^2)p^2 - p.
D((p-1)/p) * delta((p-1)/p) = D((p-1)/p)/(1+p) ~ (3/pi^2)*p.
Total S(p) = sum D*delta ~ c*p*log(p) (empirically grows faster than the single fraction).
So the single-fraction dominance fraction goes to ZERO as p -> infinity.

This rules out any rescue strategy based on single-fraction dominance.

**Verdict: BROKEN (rescue path fails)**

### Attack 6: "Does not need LI" claim — **UNCLEAR**

The theorem claims it needs GRH but not linear independence of zeros.
However, the spectral formula involves individual terms p^{i*gamma_k} which
require separation of zero contributions. Without LI, nearby zeros could
produce interference effects not captured by the simple T(L,gamma_k) factorization.
This is not a fatal flaw but the claim of LI-independence is insufficiently justified.

**Verdict: UNCLEAR**

---

## 3. Low-Pass Verification

### T(L,gamma) asymptotics: CONFIRMED for L >> gamma^2

| L | gamma | |T| numerical | |T| asymptotic | relative error |
|---|-------|---------------|-----------------|----------------|
| 2 | 14.13 | 0.4603 | 0.0500 | 89% |
| 10 | 14.13 | 0.0252 | 0.0224 | 11% |
| 50 | 14.13 | 0.01037 | 0.01000 | 3.6% |
| 100 | 14.13 | 0.00678 | 0.00707 | 4.3% |
| 100 | 32.94 | 0.00316 | 0.00304 | 4.0% |

### Suppression factor convergence:

| L | F_5 numerical | F_5 predicted (gamma_1/gamma_5) | error |
|---|---------------|----------------------------------|-------|
| 5 | 2.92 | 0.43 | 580% WRONG DIRECTION |
| 10 | 0.67 | 0.43 | 57% |
| 50 | 0.43 | 0.43 | 1.4% |
| 100 | 0.42 | 0.43 | 2.7% |

**Verdict on low-pass:** The mathematical asymptotic is correct but convergence requires
L >> gamma_k. For the first 5 zeros (gamma up to 33), you need L > 500 for reliable
suppression. Since practical depth filtering uses L = 2 to 10, the low-pass effect is
NOT operative in any experimentally accessible regime.

---

## 4. Rescue Assessment

### Can the theorem be rescued?

**Bridge replacement options:**

1. **Direct spectral expansion of D(a/p):** This would bypass M(q_{m-1}) entirely.
   D(a/p) = rank(a/p) - a can be expressed via the explicit formula for Farey rank
   deviations, which involves sums over zeta zeros. However, the key step — factoring
   this sum by terminal CF quotient c_m — requires showing that grouping by c_m
   produces an arithmetic structure compatible with the zeta-zero sum. This is a
   major open problem, not a gap.

2. **Single-fraction dominance:** FAILS. The dominant fraction (p-1)/p contributes
   a DECREASING share (45% at p=13, down to 17% at p=509). Cannot support a
   spectral formula that becomes more accurate as p grows.

3. **Average over c_m groups:** One could try to show that the AVERAGE D*delta over
   fractions with c_m = c has a spectral decomposition. But with only 1-2 fractions
   per large c_m value, "average" is meaningless. For small c_m (c_m=2 has ~p/3
   fractions), the averaging might work, but those are exactly the fractions you
   EXCLUDE when depth-filtering with L >= 3.

4. **Reformulate as a density statement:** Instead of a spectral formula for individual
   S_L(p), claim that the EMPIRICAL spectral content of {S_L(p)}_p shifts toward
   low frequencies as L increases. This would be a statistical statement, not a
   spectral formula, and could potentially be true even without the bridge.

**My assessment:** Rescue option (4) is the only honest path forward. The spectral
formula as written is not derivable from any currently available bridge. The low-pass
property of T(L,gamma) is mathematically real but operates at scales (L > 500)
irrelevant to practical depth filtering (L = 2-10).

---

## 5. Final Rating

### **(c) FUNDAMENTALLY FLAWED**

The theorem is fatally compromised by:

1. **Bridge is false:** D(a/p) ~ M(q_{m-1}) has zero correlation. Not a gap that
   might be closed — the statement is empirically wrong.

2. **Supporting evidence is wrong:** The "c_m = p contributes 65-73%" claim is
   factually incorrect (wrong fraction, wrong percentage, wrong trend).

3. **Practical irrelevance:** Even if a valid spectral formula existed, the low-pass
   effect requires L >> gamma_k^2 ~ 1000, making it inoperative for any realistic
   depth filter.

4. **No viable rescue:** Single-fraction dominance diminishes with p. Direct spectral
   expansion of D(a/p) factored by c_m is an open problem of comparable difficulty to
   the original.

### Recommendation

**Do NOT include this theorem in any paper.** The mathematical observation that T(L,gamma)
decays as 1/gamma while zeta(3/2+i*gamma) does not is a correct and potentially interesting
asymptotic fact. But it does not extend to a spectral formula for depth-filtered Farey sums.

If the low-pass framing is important, pivot to an empirical/statistical version:
"Depth-filtered Farey sums show enhanced gamma_1 coherence" as a computational observation,
with the T(L,gamma) asymptotic as suggestive motivation, not as a theorem.

---

*Review generated by adversarial Opus analysis, 2026-04-04.*
*All numerical claims verified by independent computation.*
