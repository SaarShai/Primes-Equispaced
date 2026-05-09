# P1b / T2 — Orthogonal Barnes-G Coefficient `1/12` via O(2N) Monte Carlo

**Target model:** Opus 4.7, **extra-high** reasoning mode.
**Repo root context:** `/Users/za/Documents/Farey NOW/primes-equispaced/` (this repo).
**Deliverable file:** `handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md`

---

## Goal (single sentence)

Monte-Carlo verify that the **second moment of `|Z'(1)|²` for orthogonal random matrices `O(2N)` in the bulk-scaling limit converges to `1/12 + O(1/N)`** (the Hughes-Mezzadri Barnes-G coefficient claimed in [`Reverse_engineer_constant.md`](../handoff-2026-05-04-theorem-B-and-C1/Reverse_engineer_constant.md)). This is the C2 RMT match — if it passes, the `2/(3π) = (1/(2π)) · (1/12) · 16` decomposition jumps in confidence to 0.85, and combined with P1a (T1 PARI Mellin) closes Theorem B-exact unconditional.

If the orthogonal coefficient is anything other than `1/12 + O(1/N)`, the decomposition is wrong and the route to unconditional Theorem B-exact via C2 fails — state precisely why.

---

## Mandatory protocol (read before starting; embedded in deliverable)

1. **NO fabrication.** Every cited theorem must be verified by `curl + pdftotext` on the actual paper. Quote verbatim with page or equation number. If you cannot retrieve, mark `UNVERIFIED` and do not depend on it.
2. **Single confidence aggregation rule** stated at start of deliverable, never switched mid-document.
3. **Honest verdict.** State precisely what passes, what fails, and what is inconclusive.
4. **Cross-reference prior failures and prior partial work in the bundle**:
   - [`B2_R_neigh_v3_polished.md`](../handoff-2026-05-04-theorem-B-and-C1/B2_R_neigh_v3_polished.md) — the unitary case (R_neigh α_ratio = 1 forced by Soshnikov 2000a)
   - [`SESSION_SYNTHESIS_extra_high_round.md`](../handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md) — the 5-of-5 inflation pattern; do NOT repeat it
   - [`G7_CS_2007_verification.md`](../handoff-2026-05-04-theorem-B-and-C1/G7_CS_2007_verification.md) — caught CS 2007 §7 was unitary not orthogonal; you are testing the **orthogonal** case
   - [`RMT_Painleve_GRH_bypass.md`](../handoff-2026-05-04-theorem-B-and-C1/RMT_Painleve_GRH_bypass.md) — RMT route history
5. **Don't switch families.** Theorem B context is weight-aspect Petersson family — the orthogonal symmetry type is the SO(even) lift of holomorphic newforms (verify via Katz-Sarnak symmetry-type assignment, citing verbatim).

---

## Inputs and references

### Existing scripts and partial results in the bundle (READ FIRST)

These already exist. Verify what they computed before doing fresh work:

- [`C2_orthogonal_MC.py`](../handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC.py) and [`C2_orthogonal_MC.out`](../handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC.out)
- [`C2_orthogonal_MC_check.md`](../handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC_check.md)
- [`C2_cue_control_MC.py`](../handoff-2026-05-04-theorem-B-and-C1/C2_cue_control_MC.py) and `.out` — CUE control (you compare against this)
- [`C2_robust_stats.py`](../handoff-2026-05-04-theorem-B-and-C1/C2_robust_stats.py) and `.out`
- [`C2_symbolic_residue.py`](../handoff-2026-05-04-theorem-B-and-C1/C2_symbolic_residue.py) and `.out`
- [`B2_cue_mc_K10k.py`](../handoff-2026-05-04-theorem-B-and-C1/B2_cue_mc_K10k.py) — CUE Monte Carlo at K=10000, the unitary baseline
- [`B2_R_neigh_v3_polished.md`](../handoff-2026-05-04-theorem-B-and-C1/B2_R_neigh_v3_polished.md) — the Soshnikov 2000a closure for unitary `α_ratio = 1`

### Required reading

- [`THEOREM_B_HANDOFF.md`](../handoff-2026-05-04-theorem-B-and-C1/THEOREM_B_HANDOFF.md) §4 — the `2/(3π) = (1/(2π))(1/12)(16)` decomposition
- [`Reverse_engineer_constant.md`](../handoff-2026-05-04-theorem-B-and-C1/Reverse_engineer_constant.md) — the orthogonal Barnes-G `1/12` claim full statement
- [`MK3_Bridge_Selberg_VERIFIED.md`](../handoff-2026-05-04-theorem-B-and-C1/MK3_Bridge_Selberg_VERIFIED.md) — universal kernel for context
- [`theorem-b-five-routes.md`](../handoff-2026-05-04-theorem-B-and-C1/theorem-b-five-routes.md) — T2 entry
- [`AUTONOMOUS_PLAN.md`](../handoff-2026-05-04-theorem-B-and-C1/AUTONOMOUS_PLAN.md) — T2 spec

### Source papers to retrieve

- Hughes-Mezzadri 2008 — *On the second moment of the derivative of the Riemann zeta function*. Try `arXiv:0708.2922` or the published version. Save `/tmp/hughes_mezzadri.pdf`, `pdftotext`. Quote the Barnes-G `G(3)²/G(5) = 1/12` result verbatim with equation number.
- Conrey-Snaith 2007 — *Applications of the L-functions ratios conjectures*. Verify via `arXiv:math/0610495`. Note from G7 audit: §7 of CS 2007 is **unitary**, not orthogonal — do NOT cite §7 for orthogonal.
- Conrey-Farmer-Mezzadri 2008 — *Random matrix theory and the Riemann zeta function* — for the orthogonal Painlevé framing if applicable. `arXiv:0710.3017`.
- Katz-Sarnak 1999 — *Random matrices, Frobenius eigenvalues, and monodromy* — for the symmetry-type assignment of holomorphic newforms (SO(even)). Quote the assignment with chapter or theorem number.

---

## Plan (step-by-step)

### Step 1 — read existing C2 work

Open the existing `C2_orthogonal_MC*` files. Report:
- What samples were taken (N values, sample counts)
- What statistic was computed
- What value was reported
- Why the prior round did not reach a verdict (if it didn't)

State explicitly: "this task **extends/verifies/replaces** the prior C2 work because [reason]."

### Step 2 — define the statistic precisely

The target is the second moment of `|Z'(1)|²` averaged over the **orthogonal ensemble O(2N)** with Haar measure, in the bulk-scaling limit. State:
- Bulk-scaling limit definition (cite Soshnikov 2000a verbatim, or the analogous orthogonal CLT — Wieand 2002 / Diaconis-Evans 2001 / Hughes-Rudnick 2003)
- The kernel `K_O(y, y')` for the orthogonal sine-kernel Palm extension (analogous to Bourgade-Nikeghbali for unitary)
- The exact predicted leading constant `1/12` — quote verbatim from Hughes-Mezzadri

### Step 3 — Monte Carlo design

Sample N ∈ {50, 100, 200, 400, 800} from O(2N) Haar. For each:
- Sample size ≥ 10⁴ matrices per N (more if N≤200; budget per Cerebras / Mistral / OpenRouter availability)
- Compute `|Z'(1)|²` per sample by extracting eigenangles, evaluating the secular polynomial derivative, normalizing by `Λ_K = log K · 2π/N`
- Report mean ± standard error and finite-N correction `c_∞ + a/N + b/N² + ...` fit

### Step 4 — falsifier at κ=0

Per [`B2_R_neigh_v3_polished.md`](../handoff-2026-05-04-theorem-B-and-C1/B2_R_neigh_v3_polished.md), there is a κ=0 falsifier that gives a different prediction than κ matched to physical L. Run this falsifier in the orthogonal case:
- κ=0: predicts `Var(S; κ=0) ≠ 1/12`
- κ matched (κ ≈ (2π)² ≈ 39.5): predicts `1/12`
Two-orders-of-magnitude separation — only `1/12` should match the matched-κ regime.

If both regimes give `1/12`, the test is degenerate and the result tells us nothing — flag as **DEGENERATE** and propose a sharper falsifier.

### Step 5 — alternative-α candidate comparison

Per the unitary precedent (B2 v3), tabulate residual against alternative candidates:
- `1/12 = 0.0833...` (Hughes-Mezzadri orthogonal Barnes-G)
- `1/(2π²) ≈ 0.0507`
- `1/π² ≈ 0.1013`
- `2/π² ≈ 0.2026`
- `1/(4π) ≈ 0.0796`
- `1/24 ≈ 0.0417` (off by factor 2 — sanity check)

Only `1/12` should match within statistical error. Reject any other candidate.

### Step 6 — symbolic / theoretical cross-check

Independently compute the Barnes-G prediction symbolically via mpmath at 50 dps:
- `G(3) = 1`, `G(5) = 12`, so `G(3)²/G(5) = 1/12` exactly
- Verify this matches Hughes-Mezzadri's published value to ≥30 digits
- If mpmath disagrees with Hughes-Mezzadri, **STOP** and report the discrepancy — do not assume the published value is right

### Step 7 — agreement statement

Cross MC vs symbolic. The MC mean at largest N must agree with `1/12` within Monte Carlo standard error (typically `O(1/√samples)`).

If `|MC_mean - 1/12| > 3·SE`, the route fails. State this clearly.

---

## Deliverable specification

Single Markdown file at `handoff-2026-05-09-followup/C2_orthogonal_MC_extended.md` with sections:

1. **Confidence aggregation rule** — state once
2. **What the prior `C2_orthogonal_MC*` files computed** — verbatim summary, what's missing
3. **Statistic definition** — bulk-scaling, kernel, predicted constant with verbatim Hughes-Mezzadri citation
4. **MC results table** — N ∈ {50, 100, 200, 400, 800}, mean ± SE, finite-N fit
5. **κ=0 falsifier** — pass / degenerate / fail
6. **Alternative-α residual table** — `1/12` vs other candidates
7. **Symbolic mpmath cross-check** — `G(3)²/G(5)` to 30+ digits
8. **MC vs symbolic agreement** — final residual, in standard-error units
9. **Verdict** — exactly one of: `PASS (decomposition jumps to 0.85; combined with P1a closes Theorem B-exact unconditional)`, `FAIL (orthogonal Barnes-G coefficient is X ≠ 1/12 by Y standard errors)`, `DEGENERATE (test cannot distinguish; sharper falsifier required)`
10. **Companion files** — embed the actual `.py` source. Save `C2_orthogonal_MC_extended.py`, `.out`, raw samples per N if storage permits.

---

## Done when

- File exists at the specified path
- All 10 sections present
- Hughes-Mezzadri verbatim quote with equation number
- MC at N=800 has SE small enough to resolve `1/12` vs `1/24` vs `1/(2π²)` (typically need ≥10⁵ samples at N=800)
- κ=0 falsifier reported
- Verdict is one of the three exact strings
- All Python scripts saved as companion files

## Stop and report immediately if

- Hughes-Mezzadri PDF cannot be retrieved (do not invent the constant)
- Symbolic mpmath disagrees with Hughes-Mezzadri's published value
- O(2N) Haar sampling library unavailable (use scipy.stats.ortho_group; if not, report)
- κ=0 falsifier returns `1/12` (degenerate; flag and stop)
- ANY citation cannot be `pdftotext`-verified

Do **not** publish a "PASS" if any of the above triggered.
