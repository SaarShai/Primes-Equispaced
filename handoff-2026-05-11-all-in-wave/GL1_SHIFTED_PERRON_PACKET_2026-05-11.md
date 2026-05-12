---
schema_version: 1
title: "GL1 shifted Perron packet"
date: 2026-05-11
worker: "Worker C"
type: research-packet
tier: claim-safe
status: SHARP_CUTOFF_BLOCKED_SMOOTHED_MODE_CONDITIONAL
confidence: 0.90
scope: "GL(1) sharp shifted Perron and smoothed/filtering fallback"
tags: [gl1, koyama, perron, residue-control, smoothing, finite-filtering]
---

# GL1 Shifted Perron Packet

## Outcome

Sharp cutoff status: `BLOCKED`.

The off-target residue aggregate for

```text
F_K(w) = K^w / (w L(rho+w,chi))
```

is not controlled by the honest standard inputs in the current packet set:
target-zero simplicity, DRH/EDRH, Inoue explicit formulas, Soundararajan-type
Mobius bounds, zero spacing, linear independence, or a Gonek-Hejhal-style
moment heuristic. These either leave the shifted zero sum explicit or give
averaged/coarse information that does not imply the pointwise moving-height
bound.

It can be controlled only by adding a named hypothesis that is essentially the
missing theorem:

```text
GL1-Sharp-OffTarget-Control(chi,rho):
  after extracting the w=0 target residue, all off-target nontrivial-zero
  residues, trivial-zero residues, shifted rectangle integrals, and Perron
  truncation/endpoint errors are o(log K).
```

Equivalently, a split honest package is:

```text
1. GL1-AllCrossedZerosSimple(chi,rho,T_K), or explicit higher-order aggregate
   control for multiple off-target zeros;
2. GL1-Sharp-FixedWeightPV(chi,rho):
     sum_{lambda != rho, |Im(lambda-rho)| <= T_K}
       K^(lambda-rho) / ((lambda-rho)L'(lambda,chi)) = o(log K);
3. GL1-Sharp-Rectangle(chi,rho):
     trivial residues, horizontal/vertical integrals, and Perron truncation
     are o(log K) for the same legal heights T_K.
```

That package proves the sharp theorem, but it is not sourced in the current
notes. It should be presented as a conditional theorem mode, not as closure.

## Sharp Residue Algebra

Let `rho` be a simple noncentral zero of primitive nonprincipal
`L(s,chi)`. The local target residue is closed:

```text
Res_{w=0} K^w/(w L(rho+w,chi))
  = log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2).
```

For an off-target zero `lambda != rho` of multiplicity `m`, put
`w_lambda = lambda-rho` and

```text
L(lambda+z,chi) = a_m z^m + a_{m+1}z^(m+1) + ...
```

Then the residue at `w=w_lambda` has top term

```text
K^(lambda-rho) (log K)^(m-1)
---------------------------------------
(m-1)! (lambda-rho) a_m.
```

Under DRH, `K^(lambda-rho)` has absolute value `1`. Therefore:

```text
m = 1: one bounded oscillatory term, but the moving aggregate is unsourced;
m = 2: an extra log K-scale oscillatory term;
m > 2: a term larger than the target log K scale.
```

So target-zero simplicity alone is formally insufficient. Global simplicity
would remove the higher-order obstruction, but it still leaves the simple-zero
PV sum. Moment or spacing inputs are useful only if upgraded to the actual
uniform fixed-weight PV statement above.

## Conditional Sharp Theorem

Claim-safe statement:

```text
Theorem GL1-sharp-leading-conditional.
Assume rho is simple and noncentral. Assume GL1-Sharp-OffTarget-Control for
the sharp Perron kernel K^w/(wL(rho+w,chi)). Then

  c_K(chi,rho) = log K/L'(rho,chi) + o(log K).

If the Euler-product input also gives

  E_K(chi,rho) log K -> L'(rho,chi)/e^gamma,

then the corrected product limit is

  c_K(chi,rho) E_K(chi,rho) -> e^(-gamma).
```

Do not state this as proved from the current files. Also keep the
noncentral Dirichlet Euler-product citation gap visible for external use:
Agent 2 flags AK as source-closed for its stated DRH formula, but not by itself
as a fully quoted arbitrary noncentral-zero Dirichlet theorem.

## Smoothed/Filtering Mode

This is the polished fallback if sharp remains blocked.

Let

```text
c_{W,K}(chi,rho) = sum_{n>=1} mu(n) chi(n) n^(-rho) W(n/K),
F_{W,K}(w) = K^w W_hat(w) / L(rho+w,chi),
```

with a target-normalized Perron-admissible cutoff:

```text
W_hat(w) = 1/w + kappa_W + O(w) near w=0,
```

and declared vertical decay on the shifted strip. Then a legal finite-box
shift gives the exact profile

```text
c_{W,K}(chi,rho)
  = Res_{w=0} F_{W,K}(w)
    + Z_off,W(K,T)
    + Z_triv,W(K,T)
    + Z_kernel,W(K,T)
    + C_rect,W(K,T).
```

The target residue is closed:

```text
Res_{w=0} F_{W,K}(w)
  = log K/L'(rho,chi)
    + kappa_W/L'(rho,chi)
    - L''(rho,chi)/(2 L'(rho,chi)^2).
```

If `W_hat` vanishes to order `h` at `w_lambda=lambda-rho`, an off-target zero
of multiplicity `m` contributes degree `m-h-1` in `log K`; if `h >= m`, that
residue is killed. Hence finite signed filtering can remove any prescribed
finite set of off-target residues by imposing finite Mellin-moment constraints
on a signed smooth cutoff.

Claim-safe filtered theorem:

```text
For any finite off-target zero set Lambda_0 and prescribed vanishing orders,
there exists a signed target-normalized smooth cutoff W such that the finite
residues in Lambda_0 are killed or degree-lowered as prescribed. The resulting
identity retains an explicit unfiltered tail Z_tail,W,Lambda_0(K).
```

Conditional smoothed leading theorem:

```text
SmoothOffTargetControl(W;chi,rho):
  Z_off,W + Z_triv,W + Z_kernel,W + C_rect,W = o(log K)
  for legal heights T_K.

If rho is simple, W is target-normalized and Perron-admissible, and
SmoothOffTargetControl(W;chi,rho) holds, then

  c_{W,K}(chi,rho) = log K/L'(rho,chi) + o(log K).
```

This is a real theorem mode for the smoothed coefficient. It does not transfer
to the sharp cutoff unless one proves uniform estimates as `W` approaches the
step kernel; those estimates are exactly the missing sharp residue theorem.

## Sources/Paths

Read and used:

```text
../start.md
HANDOFF.md
L0_rules.md
L1_index.md
L2_facts/farey-claim-ledger.md
handoff-2026-05-11-gpt55-wave/GL1_PERRON_CLOSURE_PATH_2026-05-11.md
handoff-2026-05-11-gpt55-extra-high-continuation/GL1_SMOOTHING_BYPASS_2026-05-11.md
handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
handoff-2026-05-11-gpt55-wave/AGENT2_PERRON_CITATION_AUDIT.md
handoff-2026-05-11-gpt55-wave/WAVE_SYNTHESIS_2026-05-11.md
handoff-2026-05-11-gpt55-extra-high-continuation/BIGGEST_CHALLENGES_MATRIX_2026-05-11.md
handoff-2026-05-11-gpt55-extra-high-continuation/LITERATURE_INPUTS_THEOREM_SOURCE_NOTE_2026-05-11.md
handoff-2026-05-09-followup/Koyama_GL1_claimsafe_note_outline_2026-05-10.md
handoff-2026-05-09-followup/Koyama_claimsafe_paper_outline_2026-05-11.md
handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
```

Not edited:

```text
correspondence/KOYAMA.md
projects/farey-research/koyama-correspondence.md
handoff-2026-05-09-followup/Koyama_email_to_Koyama_claimsafe_draft_2026-05-11.md
```

## Confidence

Aggregation rule: minimum of formal local residue obstruction, source-status
audit, and theorem-packaging risk.

```text
Sharp-cutoff non-promotion: 0.94
Statement that standard checked sources do not close the aggregate: 0.92
Smoothed/filtering theorem-mode packaging: 0.86
Overall packet confidence: 0.90
```

Main uncertainty: a specialized external theorem could exist outside the read
set, but no current packet cites one, and the checked Inoue/Soundararajan/AK
routes do not supply it.

## Verification

Local verification only; no code tests apply.

```text
rg/sed source reads completed on requested files and adjacent GL1 packets.
git status --short checked before edits; concurrent changes left untouched.
./te doctor attempted in project root but ./te is absent there.
token-economy.yaml absent in project root; L0_rules.md and L1_index.md read.
git diff --check passed on this packet after write.
```

## Changed Files

```text
handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
```

No correspondence drafts edited. No commit. No push.

## Risks

1. The sharp theorem is easy to overstate: local target residue algebra is not
   global Perron-leading.
2. `All zeros simple` is not enough; it must be paired with the moving
   fixed-weight PV bound and rectangle/truncation control.
3. Finite filtering kills only finitely many residues; it does not control the
   infinite tail.
4. A smoothed theorem for `c_{W,K}` is not the original sharp `c_K` theorem.
5. External use still needs citation closure for the noncentral Dirichlet
   Euler-product input and any newly named sharp/PV hypothesis.
