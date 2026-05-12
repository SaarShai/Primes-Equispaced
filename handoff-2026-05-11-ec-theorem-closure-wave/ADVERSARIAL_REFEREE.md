NO_GO

# Adversarial Referee: EC Smoothing Closure Path

Confidence: 0.86 for no theorem promotion; 0.74 that the fixed-curve route remains a coherent rigorous reduction if the dependencies below are stated as hypotheses.

External theorem citations: none. This report cites no external theorem as fact, so no new `curl`/`pdftotext` packet is attached. Internal source audits are treated only as repo-local evidence of non-closure.

## Recommendation

Do not promote an EC smoothing theorem. Keep the current closure path at `RIGOROUS_REDUCTION` / `PROOF_CANDIDATE` only.

The wave improves H2 bookkeeping and gives a plausible S1 branch mechanism, but the actual fixed-curve stabilization theorem still needs a separate H1 reciprocal-pole theorem plus a fully closed H2 package in the same pointwise/oscillatory/averaged mode. Those are not present.

Allowed guarded statement:

```text
For fixed E and fixed W, c_E,W(K)P_E,W(K) stabilizes conditionally if:
H1 proves the reciprocal Perron zero aggregate is o((log K)^r), and
H2 proves log P_E,W(K) = -r log log K + B_E,W + o(1),
with r = ord_{s=1}L(E,s), exact Agent-3 local factors, and rank zero separated.
```

No cross-curve universality, BSD evidence, or `L2^rank` normalization claim follows.

## Fatal Blockers

1. H1 is still open and cannot borrow the H2 branch damping.

`H1_H2_COMPOSITION_AUDIT.md` correctly separates the mechanisms:

```text
H2 offcentral zero: logarithmic branch -> K^(i gamma) W_hat(i gamma)/log K.
H1 offcentral zero: reciprocal pole -> K^(i gamma) W_hat(i gamma)/L'(rho).
```

Thus the S1/H2 branch theorem does not control `1/L(E,1+z)`. For positive analytic rank `r`, final pointwise convergence still needs

```text
Z_c(u)+E_c(u) = o(u^r),   u=log K.
```

For rank zero, even bounded simple offcentral residues are main-scale. For an offcentral zero of multiplicity `m>=r+1`, the H1 residue can survive after H2 multiplication. No file closes reciprocal derivative growth, multiple zeros, or the infinite reciprocal-residue aggregate.

2. H2 pointwise remains conditional.

`H2_POINTWISE_THEOREM_PACKAGE.md` has correct local bookkeeping for Agent 3's `P` factor, but its named dependencies D1-D5 are not closed. In particular:

- `S1_W` branch continuation and zero summability are unproved.
- `Ssym_W` finite part with the same `kappa_sym` is unproved.
- `Mgood_W` weighted prime-Mertens finite part is not source-closed inside the package.
- Offcentral terms must be proved `o(1)`, retained as `Z_H2`, or averaged.

The coefficient calculation

```text
(1/2 + kappa_sym/2 - r) + (1/2)(-kappa_sym) - 1/2 = -r
```

is sound only after all three pieces `S1_W`, `Ssym_W`, and `Mgood_W` are present in the same normalization.

3. S1 branch theorem is not a theorem yet.

`S1_BRANCH_THEOREM_CANDIDATE.md` is useful, but it assumes the hard parts:

- branch-only continuation of `A_E(z)=sum_p a_p p^(-1-z)` in the needed cut strip;
- no surviving offcentral poles on `Re z=0`;
- absolute weighted branch/zero summability plus derivative/local-radius summability;
- valid contour shift past infinitely many cuts with horizontal and left-edge bounds;
- symmetric-square companion finite part and `kappa_sym` convention.

If an offcentral pole survives, S1 gains a persistent term `d_a K^a W_hat(a)`, and the pointwise `C+o(1)` form is false. If the branch sum is only formal/truncated, H2 is not closed.

4. Literature closure is explicitly blocked.

The required context says S1 source closure is blocked and H2 sources do not prove the exact pointwise smoothed theorem. I do not use any external theorem to repair this. A future promotion must include a fresh `curl + pdftotext` packet with quote and page/equation for every outside input, including ordinary Mertens/PNT if used as a cited theorem.

5. Rank and normalization remain dangerous.

The theorem must use

```text
r = ord_{s=1}L(E,s)
```

until BSD/rank equality or direct analytic-rank verification is explicitly added. The reproducer uses script ranks for finite diagnostics and `L2^rank`; those ranks cannot be silently substituted into theorem statements.

The fixed-curve product constant is curve-dependent. The reports repeatedly warn that `L2^rank` is absolutely convergent at `s=2`, numerically non-load-bearing in current ablations, and not the source of the `-r log log K` coefficient.

6. Numerics are audit-only and currently cut against overpromotion.

`DENSE_S1_RESIDUAL_DIAGNOSTICS.md` does not distinguish robustly between persistent zero terms and `1/log K`-damped zero terms. The earlier blocker synthesis records that `cP_only`, `P_only`, and `PL2_only` pass old gates in the finite window. This supports "smoothing suppresses endpoint drift" as a finite-model explanation, not an EC asymptotic theorem.

## Local-Factor And Bad-Prime Audit

No fatal local-factor sign error found in the H2 package. The script uses:

```text
good p: A_p(1)=1-a_p/p+1/p
bad  p: A_p(1)=1-a_p/p
log P_E,W(K)=-sum_p W(p/K) log A_p(1)
```

The package decomposition keeps the required pieces:

```text
log P = S1_W + (1/2)Ssym_W - (1/2)Mgood_W + Rge3_W + Bbad_W.
```

Bad primes are harmless only as constants/o(1) after the exact Agent-3 convention is retained. Replacing `1-a_p/p` by a completed/good-prime factor would change the constant and invalidate the package.

## Ledger Conflicts If Promoted

Promotion now would conflict with the current `HANDOFF.md` and `L2_facts/farey-claim-ledger.md` entries:

- no EC smoothing theorem is promoted;
- naive pointwise H2 is not claim-safe;
- S1 source closure is blocked;
- smoothed full `L2^rank` is not promoted because ablations pass;
- EC smoothing is not BSD, `L(E,2)`, or cross-curve universality evidence.

No conflict exists if the new wave files remain labeled as proof candidates/reductions and the final theorem is withheld.

## Dependencies

To change this verdict, close all of the following in one consistent theorem mode.

1. H1 reciprocal Perron theorem for the same kernel `W`: central polynomial, offcentral Laurent residues, reciprocal derivative growth, multiple-zero powers, contour tails, and `Z_c(u)+E_c(u)=o(u^r)` for positive rank.
2. Rank-zero H1 theorem, explicit oscillatory expansion, or declared averaged theorem.
3. H2 package for exact Agent-3 factors: `S1_W`, `Ssym_W`, `Mgood_W`, `Rge3_W`, and `Bbad_W` all included.
4. S1 branch theorem: branch-only continuation, no offcentral poles, summable zero/branch aggregate, and justified infinite-cut contour shift.
5. Symmetric-square/adjoint finite part with the same `kappa_sym`; no unverified insertion of `kappa_sym=0`.
6. Ordinary weighted prime-Mertens finite part for the same smoothing kernel and good-prime removal.
7. Analytic rank convention, or an explicit rank-equality hypothesis/source packet.
8. External source protocol for every outside theorem: `curl`, `pdftotext`, short quote, page/equation.

## Do Not Promote Unless

- H1 is closed separately as a reciprocal-pole theorem; do not transfer H2's `1/log K` branch damping to `1/L(E,1+z)`.
- H2 is closed with exact Agent-3 good/bad local factors and analytic rank.
- Pointwise, oscillatory, or averaged mode is declared once and used in S1, H2, H1, and the final composition.
- Rank zero is separated.
- Multiple offcentral zeros are ruled out, controlled, retained, or averaged.
- `Ssym_W` and `Mgood_W` are present before claiming the product coefficient `-r`.
- `L2^rank` is not described as load-bearing unless ablations and a theorem justify it.
- No finite-window numerical diagnostic is used as theorem evidence.
- No external theorem is cited without the required source-verification packet.

## Changed File List

```text
handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
```

## Commands Run

```bash
sed -n '1,220p' ../start.md
./te doctor
sed -n '1,220p' token-economy.yaml
test -f L0_rules.md && sed -n '1,220p' L0_rules.md || true
test -f L1_index.md && sed -n '1,220p' L1_index.md || true
test -f skills/plan-first-execute/SKILL.md && sed -n '1,220p' skills/plan-first-execute/SKILL.md || true
pwd; rg --files -g 'HANDOFF.md' -g 'farey-claim-ledger.md' -g 'S1_BRANCH_THEOREM_CANDIDATE.md' -g 'H2_POINTWISE_THEOREM_PACKAGE.md' -g 'H1_H2_COMPOSITION_AUDIT.md' -g 'DENSE_S1_RESIDUAL_DIAGNOSTICS.md' -g 'EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md' -g 'H2_SPRINT_SYNTHESIS_2026-05-11.md' -g 'S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md' -g 'ADVERSARIAL_REFEREE.md'
git status --short
wc -l HANDOFF.md L2_facts/farey-claim-ledger.md handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
find handoff-2026-05-11-ec-theorem-closure-wave -maxdepth 1 -type f -print | sort
rg -n "STATUS|Status|PROOF_CANDIDATE|RIGOROUS_REDUCTION|NO_GO|BLOCK|block|promot|theorem|Theorem|fatal|gap|rank|normal|branch|pole|zero|contour|bad prime|ledger|Mertens|Euler|S1|H2|H1" HANDOFF.md L2_facts/farey-claim-ledger.md handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
sed -n '1,220p' HANDOFF.md
sed -n '1,220p' L2_facts/farey-claim-ledger.md
sed -n '1,360p' handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
sed -n '1,360p' handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
sed -n '1,320p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
sed -n '1,180p' handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md
sed -n '1,170p' handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md
sed -n '1,220p' handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
sed -n '1,190p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
rg -n "def smooth|smoothstep|inv_p1|A_p|log_P|P_only|PL2|L2|bad|good|rank|ap|1 -" handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
sed -n '1,260p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
sed -n '260,430p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
sed -n '131,155p;245,279p' handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
sed -n '1,240p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1F_SYM2_COMPANION_TERM.md
sed -n '240,360p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1F_SYM2_COMPANION_TERM.md
sed -n '1,220p' handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
sed -n '1,260p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1B_SOURCE_AUDIT.md
sed -n '260,360p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1B_SOURCE_AUDIT.md
test -e handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md && sed -n '1,220p' handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md || true
find '/Users/za/Documents/Farey NOW' -path '*ADVERSARIAL_REFEREE.md' -print
find '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave' -maxdepth 2 -type f -print
mv '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md' '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md'
rmdir '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave'
head -n 8 handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md && rg -n "^Confidence:|^## Dependencies|^## Do Not Promote Unless|^## Changed File List|^## Commands Run|^External theorem citations:" handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
perl -ne 'print $. . ":" . $_ if /[^\x00-\x7F]/' handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
find '/Users/za/Documents/Farey NOW' -path '*ADVERSARIAL_REFEREE.md' -print
git diff -- handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
git diff --no-index -- /dev/null handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md || true
git status --short -- handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
```

Bootstrap note: `./te doctor` failed because `./te` is absent in the specified workspace, and `token-economy.yaml` is absent there. I proceeded from `../start.md`, local `L0_rules.md`/`L1_index.md`, and the required handoff files.
