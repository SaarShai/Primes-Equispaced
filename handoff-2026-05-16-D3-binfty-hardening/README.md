# D3 B∞ / C₁ / e^{−γ} numerical hardening (2026-05-16)

The user's own independent verification work. Nothing here is sent to
Koyama; nothing is pushed without explicit user approval (counterparty
unverified — see `project_koyama_risk`).

## Contents

| File | What |
|---|---|
| `binfty_hardened.py` | Hardened two-engine verifier (supersedes `../handoff-2026-05-09-followup/Koyama_B_infty*.py`, `Koyama_C1.py`, `Koyama_AK*.py`). |
| `run_full.out` | Captured output of the full run (7 (χ,ρ) pairs, K≤2·10⁶). |
| `AUDIT_MEMO_2026-05-16.md` | Citation lock, the five-loci re-audit, conditional/unconditional boundary, defects fixed, residual action items. **Read this first.** |
| `extract_pdf.py` (in `../handoff-2026-05-16-D3-functionfield/`) | Citation-verification helper: text-window extraction from the published Akatsuka 2017 / Aoki–Koyama 2023 PDFs (used to primary-verify eq.(2.5) unconditionality and eq.(1.4) DRH-conditionality). |

## Reproducible build

```
python3 -m pip install --user python-flint        # Arb engine (one-time)
python3 binfty_hardened.py                         # full audit, ~10–30 min
```

Dependencies: Python 3.9, `mpmath` 1.3.0, `numpy` 2.0.2, `sympy` 1.14.0,
`python-flint` 0.6.0 (FLINT/Arb). No `gp`/PARI and no native-Arb binary
are required (and none is available in this environment — see the
Reproducibility note in §X.5.2).

## What the verifier establishes (and at what strength)

* **Two independent engines** — mpmath (dps **50 and 80**,
  precision-doubling) and python-flint/**Arb** (rigorous ball
  arithmetic, proven radii). Agreement on the K-independent base
  `½logL(2ρ,ψ)+BPC₁+BPC₂` is `0` at displayed precision; Arb radius
  ~1e-65. ρ refined to `|L(ρ,χ)|<1e-67` in both engines.
* **Genuine analytic object isolated.** `R2(K)=½∑_{p≤K}χ²(p)p^{−2ρ}
  −[½logL(2ρ,ψ)+BPC₁+BPC₂]` — the only conditionally-convergent /
  boundary-line content of Appendix A. The full (★) residual differs
  from `R2` only by an absolutely-convergent k≥3 remainder with an
  explicit rigorous bound. (Prior scripts truncated `T_{≥3}` at a
  *different* K than `T_K`, conflating the two.)
* **Conditional/unconditional labels on every line.** B∞ identity =
  UNCONDITIONAL (simple ρ). k=2 rate: χ²-principal UNCOND O(1/lnK)
  [Akatsuka 2017 eq.(2.5)]; χ²-non-principal UNCOND O(exp(−c√lnK))
  floor, observed ~K^{−1/2} = RH(ψ)-CONDITIONAL. C₁ (†): identity
  UNCOND given simplicity, o(1) rate RH(χ)-CONDITIONAL [Soundararajan
  2009]. e^{−γ} (Hyp. AK): DRH-CONDITIONAL [Aoki–Koyama 2023].
* **Cross-checks the paper.** Reproduces §X.5.2 `L′,L″,C₁` and the
  Aoki–Koyama `|D_K|·ζ(2)` / `/Cak` / `/Cs` drift table to displayed
  digits.

Honest scope ceiling: this is **calibrated numerical evidence + an
audited pen-and-paper identity**, specialist tier — not a theorem,
not RH/DRH progress. Conditional results are labelled conditional
everywhere.
