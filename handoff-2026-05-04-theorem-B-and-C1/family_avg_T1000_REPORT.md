# Family-Averaged u_f(T) — 14-Curve Squarefree k=2 Family

**Date:** 2026-05-03  
**Script:** family_avg_T1000.gp  
**Raw output:** family_avg_T1000.out  
**PARI version:** 2.17.3

---

## 0. Formula and conventions

**Exact task formula (M-N convention):**

$$u_f(T) = \frac{\sum_{|\gamma_f| \le T} |L'(\tfrac{1}{2}+i\gamma_f, f)|^2}{c_f \cdot T \cdot \log^4 X}$$

**PARI implementation:**
- σ = k/2 = 1 for k=2 (PARI arithmetic critical line; `lfun(L, 1+I*gamma, 1)`)
- X = √(N·T)/(2π), logX = log(√(NT)/(2π)) = ½log(NT) − log(2π)
- Sum over |γ|≤T = 2 × (sum over 0<γ≤T via `lfunzeros(L, T)`)
- c_f = `lfun(lfunsympow(E,2), 2) / zeta(2)` [task formula]
- Also computed: c_rs = `lfun(lfunsympow(E,2), 1)` [Rankin-Selberg at s=1]

**Note on c_f:** For 11a1, `c_rs(s=1) = 0.5893 ≈ trunc_RS = 0.5886` (Rankin-Selberg constant). But for larger conductors, `c_task(s=2)/zeta(2)` matches the truncated RS better for most curves (12/14). Neither formula agrees to better than 5-40% for all curves — the sym² L-function evaluation has conductor-dependent normalization issues not fully resolved here. Both variants reported.

**Targets:**
- Asymptotic: 2/(3π) ≈ 0.21221
- Cage: [(17−√145)/(12π), (17+√145)/(12π)] ≈ [0.1315, 0.7704]
- Task prediction (inflation-corrected): single-curve u_f(11a1, T=1000) ≈ 0.21 × 1.85 ≈ 0.39

---

## 1. Per-curve u_f at T=400

Source: family_avg_T1000.out (fresh run, independently verified).

| label | N  | c_task   | c_rs     | S_full        | logX    | u_task    | u_rs      | in cage? |
|-------|----|----------|----------|---------------|---------|-----------|-----------|----------|
| 11a1  | 11 | 0.642943 | 0.589365 |  136255.9122  | 2.35680 | 17.172349 | 18.733472 | N        |
| 14a1  | 14 | 0.716539 | 0.835962 |  113415.6800  | 2.47738 | 10.505101 |  9.004373 | N        |
| 15a1  | 15 | 0.569317 | 0.711646 |  105677.9201  | 2.51188 | 11.656671 |  9.325337 | N        |
| 17a1  | 17 | 0.477226 | 0.676071 |  113416.0481  | 2.57446 | 13.525217 |  9.547212 | N        |
| 19a1  | 19 | 0.564097 | 0.893154 |  121777.3960  | 2.63007 | 11.279250 |  7.123737 | N        |
| 21a1  | 21 | 0.627217 | 1.097630 |  120378.7282  | 2.68012 |  9.299445 |  5.313969 | N        |
| 26a1  | 26 | 0.790624 | 1.713018 |  132738.8178  | 2.78690 |  6.957936 |  3.211355 | N        |
| 33a1  | 33 | 0.712264 | 1.958725 |  144800.8886  | 2.90611 |  7.125624 |  2.591136 | N        |
| 35a1  | 35 | 0.507461 | 1.480094 |  126240.7134  | 2.93553 |  8.375127 |  2.871472 | N        |
| 37a1  | 37 | 1.515114 | 4.671600 |  286794.1809  | 2.96331 |  6.136975 |  1.990370 | N        |
| 38a1  | 38 | 0.685658 | 2.171249 |  136475.8309  | 2.97665 |  6.338381 |  2.001594 | N        |
| 43a1  | 43 | 1.324434 | 4.745887 |  256398.6196  | 3.03846 |  5.678245 |  1.584627 | N        |
| 53a1  | 53 | 1.040943 | 4.597500 |  228373.2699  | 3.14300 |  5.620565 |  1.272581 | N        |
| 57a1  | 57 | 1.428345 | 6.784640 |  264024.8335  | 3.17938 |  4.522529 |  0.952111 | N        |

**Family average at T=400:**
- ū_task = 8.870958   (ratio to 2/(3π): 41.80×)
- ū_rs   = 5.394525   (ratio to 2/(3π): 25.42×)

---

## 2. Per-curve u_f at T=1000

Source: T=1000 recomputed from family_avg_finite_T_fix.out S_full values with updated c_task.
Independently confirmed: 11a1 gives identical S_full=617763.2457 in fresh run.

| label | N  | c_task   | c_rs     | S_full         | logX    | u_task    | u_rs      | in cage? |
|-------|----|----------|----------|----------------|---------|-----------|-----------|----------|
| 11a1  | 11 | 0.642943 | 0.589365 |  617763.2457   | 2.81495 | 15.303742 | 16.693844 | N        |
| 14a1  | 14 | 0.716539 | 0.835962 |  508119.5888   | 2.93550 |  9.549884 |  8.185286 | N        |
| 15a1  | 15 | 0.569317 | 0.711646 |  459530.3983   | 2.97000 | 10.373720 |  8.298688 | N        |
| 17a1  | 17 | 0.477226 | 0.676071 |  491535.0844   | 3.03260 | 12.177817 |  8.596026 | N        |
| 19a1  | 19 | 0.564097 | 0.893154 |  560689.3367   | 3.08820 | 10.928149 |  6.901807 | N        |
| 21a1  | 21 | 0.627217 | 1.097630 |  521353.2083   | 3.13830 |  8.569120 |  4.896877 | N        |
| 26a1  | 26 | 0.790624 | 1.713018 |  586019.3483   | 3.24500 |  6.684720 |  3.085070 | N        |
| 33a1  | 33 | 0.712264 | 1.958725 |  623385.6335   | 3.36430 |  6.831829 |  2.484437 | N        |
| 35a1  | 35 | 0.507461 | 1.480094 |  524655.5260   | 3.39370 |  7.794320 |  2.672417 | N        |
| 37a1  | 37 | 1.515114 | 4.671600 | 1304913.2563   | 3.42150 |  6.284492 |  2.038310 | N        |
| 38a1  | 38 | 0.685658 | 2.171249 |  584008.7221   | 3.43480 |  6.119358 |  1.932445 | N        |
| 43a1  | 43 | 1.324434 | 4.745887 | 1205836.7604   | 3.49660 |  6.090801 |  1.699758 | N        |
| 53a1  | 53 | 1.040943 | 4.597500 | 1003518.7241   | 3.60110 |  5.732679 |  1.297898 | N        |
| 57a1  | 57 | 1.428345 | 6.784640 | 1140915.9207   | 3.63750 |  4.562558 |  0.960511 | N        |

**Family average at T=1000:**
- ū_task = 8.357371   (ratio to 2/(3π): 39.38×)
- ū_rs   = 4.981793   (ratio to 2/(3π): 23.48×)

---

## 3. Inflation factor per curve

Inflation factor = u_f(T) / (2/(3π)) = u_f / 0.21221

| label | N  | u_task(T=400) | infl×(400) | u_task(T=1000) | infl×(1000) | trend      |
|-------|----|---------------|------------|----------------|-------------|------------|
| 11a1  | 11 |  17.172349    |  80.9×     |  15.302690     |  72.1×      |  −8.8      |
| 14a1  | 14 |  10.505101    |  49.5×     |   9.549884     |  45.0×      |  −4.5      |
| 15a1  | 15 |  11.656671    |  54.9×     |  10.373720     |  48.9×      |  −6.0      |
| 17a1  | 17 |  13.525217    |  63.7×     |  12.177817     |  57.4×      |  −6.3      |
| 19a1  | 19 |  11.279250    |  53.2×     |  10.928149     |  51.5×      |  −0.4      |
| 21a1  | 21 |   9.299445    |  43.8×     |   8.569120     |  40.4×      |  −0.7      |
| 26a1  | 26 |   6.957936    |  32.8×     |   6.684720     |  31.5×      |  −0.3      |
| 33a1  | 33 |   7.125624    |  33.6×     |   6.831829     |  32.2×      |  −0.3      |
| 35a1  | 35 |   8.375127    |  39.5×     |   7.794320     |  36.7×      |  −0.6      |
| 37a1  | 37 |   6.136975    |  28.9×     |   6.284492     |  29.6×      |  +0.1      |
| 38a1  | 38 |   6.338381    |  29.9×     |   6.119358     |  28.8×      |  −0.2      |
| 43a1  | 43 |   5.678245    |  26.8×     |   6.090801     |  28.7×      |  +1.9      |
| 53a1  | 53 |   5.620565    |  26.5×     |   5.732679     |  27.0×      |  +0.1      |
| 57a1  | 57 |   4.522529    |  21.3×     |   4.562558     |  21.5×      |  +0.0      |

**Family-level inflation factors:**
- T=400:  ū_task = 8.871,  inflation = 41.8×
- T=1000: ū_task = 8.357,  inflation = 39.4×
- Direction: 11 curves moving down, 3 moving up — very slow/inconsistent decrease

---

## 4. Inflation-corrected ū / inflation_factor

Per task spec: after dividing by the inflation factor, the corrected ū should approach 1.

| T    | ū_task | inflation | ū_task / inflation |
|------|--------|-----------|-------------------|
| 400  | 8.871  | 41.8×     | 0.212             |
| 1000 | 8.357  | 39.4×     | 0.212             |

Both ratios give 0.212 ≈ 2/(3π) ✓ — this is tautological (inflation IS defined as u_f/(2/(3π))).

Meaningful inflation-correction would require an a priori formula for the finite-T inflation factor. No such formula is available.

---

## 5. Cage check

Cage = [(17−√145)/(12π), (17+√145)/(12π)] = [0.13153, 0.77035]

- Every single per-curve u_f at both T=400 and T=1000 is **far above the cage upper bound 0.770**.
- u_f values range from 4.5 to 17.2 — 6× to 22× above the cage upper bound.
- Family averages: 8.357 (T=1000) and 8.871 (T=400) — about 11× above cage ceiling.
- **CAGE VIOLATED UNIVERSALLY** at both T values.

---

## 6. Convergence verdict

**Trend T=400 → T=1000:**
- ū_task decreases from 8.871 → 8.357 (−6%)
- Rate of decrease: −0.0075 per unit T (on a log scale: very slow)
- Extrapolating linearly in log T: to reach cage ceiling 0.770 from 8.357 requires ~T = 10^(log(1000) + log(8.357/0.770)) ≈ 10^(3 + 2.35) ≈ 10^5.35 = 220,000

**Comparison to task prediction:**
- Task predicted: single-curve u_f(11a1, T=1000) ≈ 0.39 (inflation 1.85×)
- Actual: u_task(11a1, T=1000) = 15.30 (inflation 72×)
- Discrepancy: 39×
- The predicted inflation factor of 1.85× is **drastically wrong** — actual inflation is ~72× for 11a1.

**Three scenarios:**
1. **Asymptotic correction too slow to observe at T=1000** (most likely): The M-N conjecture is a TRUE asymptotic but the subleading terms completely dominate at T≤1000. The O(T log³X) error is not small relative to the 2/(3π)·T·log⁴X leading term at log X ≈ 2-3.
2. **Formula error in M-N or conventions**: The observed ratio u_f/predicted ≈ 40-80× is stable across all 14 curves, which is suspicious. Could indicate a missing combinatorial factor in the M-N derivation (analogous to the "factor-4" identified in the unitary case).
3. **c_f mismatch**: The task formula `lfun(sym2,2)/zeta(2)` does not closely match the truncated Rankin-Selberg constant for many curves (off by 5-40%). However, even using the better-matching c_rs gives u_rs(T=1000) ≈ 5.0 (family average) — still 23× above prediction.

---

## 7. Summary

| Metric | T=400 | T=1000 |
|--------|-------|--------|
| ū_task (task formula) | 8.8710 | 8.3574 |
| ū_rs (RS c_f) | 5.3945 | 4.9818 |
| Inflation factor ū_task / 0.21221 | 41.8× | 39.4× |
| All curves in cage? | NO (14/14 above) | NO (14/14 above) |
| Trend | — | Decreasing slowly (−6% per 2.5× T) |
| Predicted (task inflation 1.85×) | — | 0.39 |

**Headline:** At T=400 and T=1000, the family-averaged ū_task is 40× above the M-N asymptotic and 11× above the cage upper bound. The inflation factor is ~40×, not the predicted 1.85×. Family averaging does not cancel the inflation — curves disagree in sign of drift. No convergence toward 2/(3π) is visible at these T values.

**c_f convention note (important):** The task formula `c_f = lfun(lfunsympow(E,2), 2)/zeta(2)` gives values differing from the truncated Rankin-Selberg constant by 0-40% depending on curve. For 11a1 it gives 0.643 vs RS=0.589 (9% off). For higher-N curves the discrepancy grows. The formula `lfun(sym2, 1)` matches RS better for 11a1 but worse for most others. The correct formula per Rankin-Selberg theory is `c_f = L(1, sym²f)/ζ(2)` in analytic normalization — but PARI's lfunsympow normalization at various s values doesn't cleanly map to this for all curves.

---

## 8. Log formula note (vs prior G8 scripts)

Two log formulas have appeared in prior scripts:

| Formula | Expression | Value at q=11, T=1000 |
|---------|------------|----------------------|
| **M-N (eq 16) / this script** | log(√(qT)/(2π)) = ½log(qT) − log(2π) | **2.815** |
| G8 v4 (error) | log(√(qT/(2π))) = ½log(qT) − ½log(2π) | 3.734 |

G8 v4 used Y = log(√(qT/(2π))) which is LARGER than M-N logX by log(2π)/2 ≈ 0.919. This means G8 v4's Y⁴ is (3.734/2.815)⁴ = 3.10× larger, producing u_f values 3.10× smaller. G8 v4 u_f(11a1, T=800) = 2.63 in their convention; this corresponds to u_f = 2.63 × 3.10 = 8.15 in M-N convention — consistent with our trend.

**The current script correctly uses the M-N logX formula throughout.**

---

## 9. Verification

- T=400: fresh PARI run (family_avg_T1000.gp, PID 45662)
- T=1000: S_full values confirmed from independent run (family_avg_finite_T_fix.gp, PID 6201) and cross-checked against fresh run (11a1: S_full = 617763.2457, exact match)
- c_task values: independent gp session (cf_check.gp)
- Arithmetic verified: family averages agree to 6 decimal places

---

*Raw PARI output: family_avg_T1000.out*  
*Author: Saar Shai. AI-assisted computation (Claude Sonnet 4.6). No AI authorship.*
