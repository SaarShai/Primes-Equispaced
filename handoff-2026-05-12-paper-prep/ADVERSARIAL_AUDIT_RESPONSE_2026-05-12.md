---
schema_version: 1
title: "Authors' response to adversarial pilot (Mimo + Ollama, 2026-05-12)"
date: 2026-05-12
type: audit-response
tier: working
status: WORKING_RESPONSE_NO_THEOREM_PROMOTION
sources:
  - handoff-2026-05-12-paper-prep/ADVERSARIAL_MIMO_2026-05-12.md
  - handoff-2026-05-12-paper-prep/ADVERSARIAL_OLLAMA_C1_2026-05-12.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
tags: [adversarial, mimo, ollama, audit-response, section-prep]
---

# Authors' response to the 2026-05-12 adversarial pilot

This file is the structured response to the two pilot adversarial-referee
dispatches launched on 2026-05-12 against the manuscript's headline claims.
Inputs:

* [`ADVERSARIAL_MIMO_2026-05-12.md`](ADVERSARIAL_MIMO_2026-05-12.md)
  (`mimo-v2.5-pro`, six numbered objections).
* [`ADVERSARIAL_OLLAMA_C1_2026-05-12.md`](ADVERSARIAL_OLLAMA_C1_2026-05-12.md)
  (`qwen3.6:35b-a3b-q4km`, symbolic re-derivation of the local Perron
  residue).

## Ollama symbolic re-derivation — verdict

**INDEPENDENTLY CONFIRMED.** The local model derives, step by step:

```
L(w+ρ,χ) = w·L'(ρ,χ) + (w²/2)·L''(ρ,χ) + O(w³)

1/L(w+ρ,χ) = 1/(L'(ρ,χ)·w) − L''(ρ,χ)/(2·L'(ρ,χ)²) + O(w)

[K^w / w] · [1/L(w+ρ,χ)]  has  1/w-coefficient
   = log K / L'(ρ,χ) − L''(ρ,χ) / (2·L'(ρ,χ)²)
```

This is exactly the manuscript's local Perron residue identity (N-3 in
the plan; `Koyama_C1_subleading_proof.md §4`). The derivation is by a
model on a non-Anthropic stack, run locally, with no shared context with
the Python verifier. Lane L3-Ollama acceptance gate ✓.

## Mimo objections — point-by-point response

### Objection 1 (Mimo: "Fatal — Claim 1 unconditional tag is fraudulent")

**Mimo's argument:** The k=2 sum `Σ_p χ(p)^{2·2} p^{-2·2ρ}` is on the
boundary `Re(s) = 1` and needs a zero-free region or GRH-type input.

**Authors' response: REJECTED with explanation.** Mimo is misreading the
component breakdown.

The `B_∞` identity has four pieces:

```
T_∞ = (1/2) log L(2ρ, ψ)  +  BPC_1  +  BPC_2  +  T_{≥3}.
```

`BPC_2` is `−(1/2) Σ_{k≥2} (1/k) Σ_p χ(p)^{2k} / p^{2k·ρ}`. The minimum
exponent is `Re(2k·ρ) = 2 · 2 · (1/2) = 2`, i.e. *absolute* convergence
in `Re(s) > 1`. Same for `T_{≥3}` (minimum `Re(k·ρ) = 3/2`). No
boundary issue.

The *only* place a boundary-line conditional convergence appears is the
single Dirichlet prime sum `Σ_p χ²(p)/p^{2ρ}` which gets absorbed into
the leading `(1/2) log L(2ρ, ψ)` term. That step uses Akatsuka 2013
Lemma 2.1 / equation (2.5), which is itself unconditional (derived from
PNT with explicit error term).

The "unconditional given simple zero" tag is therefore correct *as
stated*. However, the paper must make this breakdown **explicit** — call
out which pieces are absolutely convergent and which one rides on
Akatsuka 2013 (2.5) — to prevent exactly the misread Mimo demonstrates.

**Action in §:** Add an inline "convergence regime per piece" table
right beneath the `T_∞` definition.

**Severity reclassification:** Mimo "fatal" → authors "presentation
clarity" (still important, still actioned).

### Objection 2 (Mimo: "Serious — Claim 2's `o(1)` hides the off-target zero aggregate")

**Authors' response: PARTIALLY ACCEPTED.**

Mimo is correct that the `o(1)` in `c_K = log K/L'(ρ) + C_1 + o(1)`
absorbs the sum over off-target nontrivial zeros. Specifically, Inoue
2021 Theorem 1's other-zero residues
`Σ_{ρ'≠ρ, |γ'|≤T} K^{ρ'−ρ}/[(ρ'−ρ) L'(ρ', χ)]` is what the `o(1)` is
*explicitly* covering, plus the trivial-zero / contour pieces.

What we have:

* `o(1)` is `unconditional` *only* in the sense that Inoue 2021 Theorem
  1 is unconditional and Soundararajan 2009 gives an unconditional
  `M(x) ≪ x^{1/2} exp((log x)^{1/2}(log log x)^{14})` *under RH for*
  `L(s, χ)`.
* The faster rate `O(K^{-1/2+ε})` requires RH for `L(s, χ)`.
* The `O(log K / √K)` heuristic requires RH + Gonek–Hejhal-type bound.

This was already explicit in `Koyama_C1_subleading_proof.md §6`. The
manuscript must mirror that explicitness; the brief Mimo audited
compressed it incorrectly. Update the brief and the section.

**Action in §:** Promote the existing §6 rate breakdown (unconditional
identity, RH-conditional rate) into the manuscript prose verbatim; do
not abbreviate.

### Objection 3 (Mimo: "Serious — `e^{-γ}` vs `1/ζ(2)` is likely a normalization artifact")

**Authors' response: REJECTED with embedded-quote action.**

Mimo's hypothesis is that the two constants are the same up to a
normalization swap of `E_K`. The `Koyama_AK_constant_proof.md §2`
embedded verbatim quote from **Aoki–Koyama 2023, J. Number Theory 245,
equation (1.4), p. 235** uses the *same* definition

```
E_K = ∏_{p ≤ x} (1 − χ(p) p^{-s})^{-1}
```

and concludes

```
lim_{x→∞} (log x)^m · E_K(s, χ) = L^{(m)}(s, χ) / (e^{m γ} m!)
```

(×√2 only at the central value `s = 1/2` when `χ² = 1`, hence the ×1
case at our noncentral simple zeros). At `m = 1`: the constant is
`L'(ρ,χ)/e^γ`, full stop. `1/ζ(2) ≈ 0.608` and `1/e^γ ≈ 0.561` differ
by ≈ 7.6%; the numerical drift at `K = 10^7` (mean `|D_K|·ζ(2)` falling
from 0.992 to 0.974 toward `ζ(2)/e^γ ≈ 0.911`) is *also* what
distinguishes them. Not a normalization swap.

**Action in §:** Embed the verbatim AK (1.4) quote on page 235 as a
displayed quotation in the section, exactly as
`Koyama_AK_constant_proof.md §2` reproduces it. Add a paragraph showing
the `E_K` definition is the same as Aoki–Koyama's `E_K`.

### Objection 4 (Mimo: "Serious — shifted Perron DEFER is a gap masquerading as a theorem")

**Authors' response: ACCEPTED in spirit, REJECTED in wording.**

Mimo argues that "DEFER" reads as a theorem-grade impossibility while
the truth is just "unproven". This is precisely the audit point
`KOYAMA_CLAIM_AUDIT_2026-05-11.md` already flagged. Our DEFER is *not*
an impossibility claim. The exact wording we will use in the section:

> The shifted Perron leading theorem
> `c_K(ρ,χ) = log K/L'(ρ,χ) + o(log K)`
> is **not closed** at the level of dependency-closed proof. The local
> double-pole residue is proved (algebraically). The remaining
> obstruction is the off-target nontrivial zero residue aggregate: if
> any off-target zero has multiplicity `m ≥ 2`, the shifted kernel
> contributes a residue of order `(log K)^{m−1}`, so target-zero
> simplicity plus DRH/EDRH alone do not suffice to give `o(log K)`. We
> state this as an open challenge, not an impossibility.

Note Mimo's separate claim that "shifted Perron with a smooth weight
plus DRH gives `O(K^{-1/2+ε})`" is itself imprecise — that holds for
the *smooth* kernel, not the *sharp-cutoff* `c_K`. We compute and
report both. The smoothing route gives a separate conditional theorem
mode but does *not* close the sharp-cutoff target — this is the
`GL1-Sharp-OffTarget-Control` blocker recorded in `HANDOFF.md`.

**Action in §:** Use exactly the wording above. Add a separate
paragraph distinguishing the smooth-kernel rate (where DRH does
suffice for the smooth analogue) from the sharp-cutoff target
(where it does not).

### Objection 5 (Mimo: "Cosmetic — no support for `verified at 10^{13}`")

**Authors' response: ACCEPTED.** No such computation exists in our
internal record. Plan §7 already routes this through Koyama
reconciliation. Until clarified, the manuscript prints `K = 10^7`
(Dirichlet) and `K = 10^6` (EC) as the verified scales.

**Action in §:** Reply to Koyama with the question: "By 'rigorous
verification at `10^{13}`' do you mean a specific Dirichlet or zeta
computation? Our internal verified scales are `K = 10^7` for Dirichlet
pairs and `K = 10^6` for the EC sweep. We will list whichever scale we
can independently re-verify before submission." (Draft only — not sent
without explicit user approval.)

### Objection 6 (Mimo: "Cosmetic — convergence rate is fitted, not proved")

**Authors' response: ACCEPTED.** Replace "demonstrates" with "is
consistent with" wherever the `K^{-1/2}/log K` rate is described from
the four-pair table; mark the rate as *evidence-grade*, not theorem-grade.

**Action in §:** Editorial.

## Summary table for the manuscript

| Mimo objection | Authors' verdict | Action |
|---|---|---|
| O1 — Unconditional fraudulent | Misread of component breakdown; presentation must be sharper | Add convergence-regime table |
| O2 — `o(1)` hides off-target aggregate | Partially accepted; the existing breakdown must not be abbreviated | Promote §6 rate analysis verbatim |
| O3 — `e^{-γ}` vs `1/ζ(2)` normalization | Rejected; same `E_K`, distinct constants, drift is observed | Embed AK (1.4) quote |
| O4 — DEFER reads as theorem | Accepted in spirit; reword as "open challenge" | Use prescribed wording |
| O5 — No `10^{13}` support | Accepted | Restrict verified scales / ask Koyama |
| O6 — Rate is fitted | Accepted | Editorial — "consistent with" |

## L3-Mimo and L3-Ollama gate status after pilot

* **L3-Ollama (qwen3.6:35b-a3b-q4km), Laurent re-derivation:** PASS ✓.
* **L3-Mimo (mimo-v2.5-pro), prose adversarial pass:** PASS with
  actionable findings (6 objections, all addressed above). No fatal
  issue survives. Section text must adopt the wording / table changes
  to clear the gate cleanly.

This pilot demonstrates that the adversarial-referee lane is operational
and produces actionable signal. The full L3 sweep (planned in §8 of the
section plan) will reuse these prompts at higher temperature, against
the fully written section text once available.
