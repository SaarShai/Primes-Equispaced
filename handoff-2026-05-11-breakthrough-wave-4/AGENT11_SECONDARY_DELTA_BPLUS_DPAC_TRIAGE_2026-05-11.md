---
title: "Agent 11 - Secondary Delta/B+/DPAC Triage"
date: 2026-05-11
status: RIGOROUS_REDUCTION
tags: [breakthrough-wave-4, secondary-frontier, delta-machine, b-plus, dpac]
---

# Verdict

Pick `Delta-2.5b`.

Among Delta-2.5b, B+ sign-cluster classification, and DPAC phase bridge, the only next task that is both theorem-shaped and immediately executable is the Delta local ramified correction divisor / axis-pole multiplicity registry execution. It is a local finite-algebra proposition after the ramified polynomials `P_p` are known. It has no Theorem B impact.

B+ is real but compute-only: it can produce a certified finite MR-prime sign-cluster atlas, not a positivity theorem. DPAC is useful proof hygiene: it can make the Lean bridge claim-safe, but it still depends on finite phase nonvanishing and does not prove pointwise zeta-zero DPAC.

# Source Anchors

- `primes-equispaced/L2_facts/farey-current-state.md`: Delta normalization anchor is arithmetic `rho = 6 + i gamma`; confirmed Delta `E[C1^2] = 0.950231842` over 683 zeros at `K = 10^4`.
- `primes-equispaced/L2_facts/farey-claim-ledger.md`: B+ positivity is dead; B+ is sign-cluster classification; DPAC/Delta only gain formal/registry reductions; top-10 secondary update selects Delta-2.5b.
- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT10_SECONDARY_FRONTIER_TRIAGE_2026-05-11.md`: prior direct comparison selects Delta registry execution over B+ and DPAC.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md`: exact Proposition 2.5b statement and registry/draft patch plan.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md`: B+ tier-1B bridge is specified but unrun.
- `primes-equispaced/formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md` and `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT09_DPAC_LEAN_BRIDGE_PATCH_PLAN_2026-05-11.md`: DPAC bridge is claim-safe scaffolding with remaining Lean/proof obligations.

# Ranked Secondary Directions

1. `Delta-2.5b` registry execution - highest breakthrough probability. The proposition is local: factor finite `P_p(z)`, solve `p^{-s}=alpha`, classify axis roots by `|alpha|=1`, and add divisor orders with cancellation by `A(s)M_W(s)`. Output can be a clean theorem-registry proposition plus draft patch.

2. B+ sign-cluster classification - medium deliverability, lower theorem value. Tier `1B` over `237733 <= p <= 243799` has `468` expected MR rows and about `9.94` core-hours. It can certify finite `B(p)` sign clusters, but cannot revive B+ positivity and cannot use `T(p-1)` as a sign proxy.

3. DPAC phase bridge - low-to-medium deliverability, lowest breakthrough value now. The useful task is to close Lean normalization/bridge obligations such as `moebiusDirichletPoly_eq_gammaExponentialPoly`; even success gives conditional same-`K`, same-`rho` finite phase avoidance, not pointwise DPAC at zeta zeros.

# Next Executable Task

Execute `Delta-2.5b` as a registry/draft patch, using only the existing patch plan.

Target files for the next worker:

```text
primes-equispaced/paper/Delta_machine_paper_theorem_registry.md
primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
```

Required insertion:

```text
Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities):
for E_ram(s)=prod_p P_p(p^{-s})^{-1}, roots alpha of P_p generate local
solutions s=-log|alpha|/log p - i(arg alpha + 2*pi*k)/log p. Axis poles are
exactly |alpha|=1 roots. Full multiplicity is the divisor order of
A(s)M_W(s) minus the summed local root multiplicities; zeros may cancel poles.
```

Acceptance check:

```bash
rg -n "Open 7\\.2|Open 10\\.2|12% mismatch|19% mismatch|N = 10\\^6|10\\^6|slope mismatch" \
  primes-equispaced/paper/Delta_machine_paper_theorem_registry.md \
  primes-equispaced/paper/Delta_machine_paper_compositio_draft.md

rg -n "Proposition 2\\.5b|Ramified correction divisor|axis-pole|P_3\\(z\\)=1-z\\^2" \
  primes-equispaced/paper/Delta_machine_paper_theorem_registry.md \
  primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
```

Pass only if stale `N=10^6` / old mismatch-open language is removed or explicitly historical, and the `zeta x L(s, chi_3)` regression is present with `E_ram(s)=(1-3^{-2s})^{-1}`, `P_3(z)=1-z^2`, roots `+-1`, and axis lattice `s=i*pi*k/log 3`.

# Overclaim Guardrails

- Do not claim any Theorem B consequence from Delta-2.5b.
- Do not claim BCL transfer, support-4 density, fixed-level de-averaging, or at-zeros `L'` second moments.
- Do not claim broad higher-rank Cross-Selberg global continuation from the local divisor proposition.
- Do not revive B+ positivity. The only B+ target is finite sign-cluster classification.
- Do not infer `B(p)` sign from `T(p-1)`.
- Do not state DPAC from LI. DPAC needs explicit finite phase avoidance, a certified sample bridge, or an external all-zero phase theorem.

# Dependency Impact

Delta-2.5b improves secondary theorem hygiene only. It converts the resolved `zeta x L(s, chi_3)` ramified-axis diagnosis into a local theorem-registry proposition and removes stale Open 7.2 / Open 10.2 language.

Main-theorem dependency impact: none. Theorem B, H1/H2 EC smoothing, GL1 sharp cutoff, B+ positivity, and pointwise zeta-zero DPAC remain unchanged. If Delta-2.5b cannot be executed cleanly, archive this lane as secondary-only rather than promoting any main theorem claim.
