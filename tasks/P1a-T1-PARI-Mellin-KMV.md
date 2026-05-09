# P1a / T1 — Verify KMV §5 Leading Constant via PARI/GP Mellin

**Target model:** Opus 4.7, **extra-high** reasoning mode.
**Repo root context:** `/Users/za/Documents/Farey NOW/primes-equispaced/` (this repo).
**Deliverable file:** `handoff-2026-05-09-followup/S4_KMV_Mellin_verify.md`

---

## Goal (single sentence)

Compute the leading constant `c₁` of the Mellin transform of the Kowalski-Michel-Vanderkam (KMV) §5 variance integrand for the Petersson weight-aspect family `F_k = S_k*(N)` (squarefree N, k = T^a, 1 < a < 2). If `c₁ = 4/(3π) ≈ 0.4244` to ≥10 digits, S4 sufficient conditions in [`handoff-2026-05-04-theorem-B-and-C1/Weakest_sufficient_conditions.md`](../handoff-2026-05-04-theorem-B-and-C1/Weakest_sufficient_conditions.md) deliver **Theorem B-exact unconditional** (Annals headline `2/(3π)`).

If `c₁` is anything else, the S4 route fails and you must say precisely why.

---

## Mandatory protocol (read before starting; embedded in deliverable)

1. **NO fabrication.** Every cited theorem must be verified by `curl + pdftotext` on the actual paper. Quote verbatim with page or equation number. If you cannot retrieve the source, mark the citation `UNVERIFIED` and proceed without it.
2. **Single confidence aggregation rule** stated at the start of the deliverable, never switched mid-document.
3. **Honest verdict.** If the route fails, state precisely why; if it succeeds, identify gaps.
4. **Cross-reference prior failures** in the bundle:
   - [`RMT_Painleve_GRH_bypass.md`](../handoff-2026-05-04-theorem-B-and-C1/RMT_Painleve_GRH_bypass.md)
   - [`RankinSelberg_trace_attack.md`](../handoff-2026-05-04-theorem-B-and-C1/RankinSelberg_trace_attack.md)
   - [`Voronoi_Kuznetsov_GRH_bypass.md`](../handoff-2026-05-04-theorem-B-and-C1/Voronoi_Kuznetsov_GRH_bypass.md)
   - [`E1_E2_E3_barrier_attack.md`](../handoff-2026-05-04-theorem-B-and-C1/E1_E2_E3_barrier_attack.md)
   - [`Necessary_conditions_inverse.md`](../handoff-2026-05-04-theorem-B-and-C1/Necessary_conditions_inverse.md)
   - [`SESSION_SYNTHESIS_extra_high_round.md`](../handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md) — note the 5-of-5 inflation pattern; you must NOT repeat it
5. **Don't switch families.** Stay on weight-aspect Petersson family `F_k = S_k*(N)`, squarefree N fixed, k → ∞ along k = T^a with 1 < a < 2, threshold k > 4eT/√N.

---

## Inputs and references

### Required reading before computing

- [`handoff-2026-05-04-theorem-B-and-C1/Weakest_sufficient_conditions.md`](../handoff-2026-05-04-theorem-B-and-C1/Weakest_sufficient_conditions.md) — defines S4 sufficient conditions; says KMV §5 variance + KMV §4 mean + ILS §3 sign all UC; identifies the Mellin verification as the load-bearing 10-min PARI step. Read in full.
- [`handoff-2026-05-04-theorem-B-and-C1/THEOREM_B_HANDOFF.md`](../handoff-2026-05-04-theorem-B-and-C1/THEOREM_B_HANDOFF.md) §4 (constant decomposition) and §10 (three-paper plan). Read.
- [`handoff-2026-05-04-theorem-B-and-C1/Reverse_engineer_constant.md`](../handoff-2026-05-04-theorem-B-and-C1/Reverse_engineer_constant.md) — Plancherel / unitary Barnes-G / family-lift decomposition. Read.
- [`handoff-2026-05-04-theorem-B-and-C1/CFKRS_symbolic_verification.md`](../handoff-2026-05-04-theorem-B-and-C1/CFKRS_symbolic_verification.md) and [`CFKRS_FAPC2_regime_check.md`](../handoff-2026-05-04-theorem-B-and-C1/CFKRS_FAPC2_regime_check.md). Read.
- [`handoff-2026-05-04-theorem-B-and-C1/theorem-b-five-routes.md`](../handoff-2026-05-04-theorem-B-and-C1/theorem-b-five-routes.md) — task scoreboard. Read T1 entry.

### Source papers to retrieve

- KMV 2002 — Kowalski-Michel-Vanderkam *Mollification of the fourth moment of automorphic L-functions and arithmetic applications*, Invent. Math. **142** (2000) 95-151. Try `arXiv:math/9909085` or `https://link.springer.com/article/10.1007/PL00005828`. Save as `/tmp/kmv2002.pdf`, run `pdftotext -layout /tmp/kmv2002.pdf /tmp/kmv2002.txt`. Quote §4 and §5 verbatim with page numbers.
- ILS 2000 — Iwaniec-Luo-Sarnak *Low lying zeros of families of L-functions*, Publ. IHES **91**. Already at `/tmp/ils.txt` per AUTONOMOUS_PLAN; if absent, retrieve.
- M-N 2014 — Milinovich-Ng `arXiv:1306.0854 v1`, eq. (16). Already at `/tmp/milinovich_ng.txt`; if absent, retrieve.
- CFKRS 2005 — Conrey-Farmer-Keating-Rubinstein-Snaith *Integral moments of L-functions*, Proc. LMS **91**. Already at `/tmp/cfkrs.pdf`; if absent, retrieve.

### Existing scripts in the bundle (do NOT redo)

- [`G8_pari_reanchor_v4.gp`](../handoff-2026-05-04-theorem-B-and-C1/G8_pari_reanchor_v4.gp) and `.out` — PARI reanchor at σ=1/2, current best version. Read both.
- [`G8_reanchor_sigma_half.gp`](../handoff-2026-05-04-theorem-B-and-C1/G8_reanchor_sigma_half.gp), `.out` — σ=1/2 anchor.
- [`family_avg_finite_T_fix.gp`](../handoff-2026-05-04-theorem-B-and-C1/family_avg_finite_T_fix.gp), `.out` — 14-curve T=400, 1000.
- [`G7_CS_2007_verification.md`](../handoff-2026-05-04-theorem-B-and-C1/G7_CS_2007_verification.md) — caught the CS 2007 §7 unitary-not-orthogonal miscitation; read so you don't redo.

---

## Plan (step-by-step)

### Step 1 — fix conventions

State the convention block at top of deliverable:
- Family: `F_k = S_k*(N)` squarefree N=11 (default; also test N=14, 37 for ladder consistency)
- Weight: k = T^a, take a = 1.5 for verification, k = T^{1.5}
- Sample T-values: T ∈ {400, 1000, 5000, 10000}
- σ-line: σ = 1/2 (critical line) for the Mellin contour anchor
- Normalization: `c_f = L(1, sym²f)` harmonic-Petersson averaged via `c_task = lfun(lfunsympow(E,2), 2)/zeta(2)` AND `c_rs = lfun(lfunsympow(E,2), 1)` (cross-check both per [`Convention_reconciliation_INDEPENDENT_VERIFY.md`](../handoff-2026-05-04-theorem-B-and-C1/Convention_reconciliation_INDEPENDENT_VERIFY.md))

### Step 2 — extract the integrand

From KMV §5 verbatim, write the variance integrand `V(s)` as a function of the Mellin variable. Quote the equation number and page. Give the integrand both symbolically and as a PARI expression.

### Step 3 — compute the Mellin transform leading constant

`c₁ = lim_{T→∞} M_V(s)|_{leading} / (T · log⁴ X)` where X = √(NkT)/(2π).

Compute via PARI/GP at increasing T and extrapolate. Show convergence table.

### Step 4 — compare against `4/(3π)`

`4/(3π) = 0.42441318...` (12 digits via mpmath). Compute residual `|c₁ - 4/(3π)|`.

If `|residual| < 10^{-10}`: **PASS**. The S4 route delivers Theorem B-exact unconditional.
If `|residual| > 10^{-3}`: **FAIL**. State exactly which step of the S4 chain breaks.
In between: report the residual, conjecture a slow-convergence regime, and request more compute.

### Step 5 — adversarial cross-check

Same computation in two independent ways:
- (a) Direct PARI Mellin via `intnum` + `lfun` + Voronoi summation
- (b) Symbolic via sympy: build `V(s)` symbolically, take residue at the relevant pole

Both must agree to ≥10 digits. If they disagree, **STOP** and report the discrepancy — do NOT proceed with overclaim.

### Step 6 — sanity-check on ζ' calibration

Re-run the ζ' calibration table from [`zeta_prime_calibration_REPORT.md`](../handoff-2026-05-04-theorem-B-and-C1/zeta_prime_calibration_REPORT.md) at T=10000 to confirm convergence to `1/(24π) = 0.013263...`. This is the sanity baseline; if it doesn't reproduce, your PARI setup is wrong and step 4 verdict is invalid.

---

## Deliverable specification

Single Markdown file at `handoff-2026-05-09-followup/S4_KMV_Mellin_verify.md` with sections:

1. **Convention block** — exact normalization, conventions, family choice
2. **KMV §5 verbatim quote** — equation + page number (`pdftotext` output included)
3. **Integrand `V(s)` — symbolic and PARI form**
4. **Computation table** — `c₁` at T = 400, 1000, 5000, 10000 with extrapolation
5. **Residual against `4/(3π)`** — to 12 digits
6. **Adversarial cross-check** — sympy symbolic vs PARI numerical, agreement statement
7. **ζ' calibration sanity check** — T=10000 result vs `1/(24π)`
8. **Verdict** — exactly one of: `PASS (S4 closes Theorem B-exact unconditional)`, `FAIL (S4 breaks at step X for reason Y)`, `INCONCLUSIVE (residual ~10^{-N}, request more compute or longer-T run)`
9. **Confidence aggregation** — single rule stated, applied uniformly
10. **PARI/GP scripts** — embed the actual `.gp` source you ran. Save companion files `S4_KMV_Mellin_verify.gp` and `.out` next to the markdown.

---

## Done when

- File exists at the specified path
- All 10 sections present
- Verbatim KMV §5 quote with page number
- Two independent computations agree (or discrepancy is clearly reported)
- Verdict is one of the three exact strings
- Confidence aggregation rule stated once, applied uniformly
- PARI scripts saved as companion files

## Stop and report immediately if

- KMV 2002 PDF cannot be retrieved (cite the URL attempted; do not invent the integrand)
- PARI Mellin diverges or returns NaN
- The σ=1/2 anchor cannot be reproduced for ζ'
- ANY citation cannot be verified by `pdftotext` quote — flag as `UNVERIFIED`
- Adversarial cross-check (sympy vs PARI) disagrees by > 10⁻⁵

Do **not** publish a "PASS" verdict if any of the above triggers fired and was not resolved.
