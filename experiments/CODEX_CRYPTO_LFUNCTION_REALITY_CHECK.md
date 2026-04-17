# Reality Check: Is Batch Dirichlet L-Function Evaluation Actually Useful for Cryptography?

**Date:** 2026-04-16
**Claim under investigation:**
> "Large-scale L-function evaluation is a bottleneck in some lattice and isogeny cryptosystem parameter searches. A 12-141x batch speedup for families of characters cuts real compute time."

**Verdict (up front):** The claim as written is **overstated and should be removed or heavily qualified** in any applications section aimed at practitioners. Dirichlet L-function evaluation is *not* a hot path in production lattice or isogeny cryptosystems. However, there is **one narrow, honest, defensible niche** — analytic class-number computation for imaginary quadratic fields in the CSIDH / CSI-FiSh / SCALLOP family of research-grade isogeny schemes, and in LMFDB-style computational number theory. That niche is academic, not commercial. Details below, angle by angle.

---

## Angle 1: Lattice-based PQC (Kyber / ML-KEM, Dilithium / ML-DSA, NTRU, Falcon)

**Is Dirichlet L evaluation on the hot path?** No. Not in keygen, not in encapsulation, not in signing, not in parameter generation, not in the security proofs that practitioners actually run.

Kyber's parameters are `n=256, q=3329` chosen for NTT-friendliness. Dilithium's parameters are similarly chosen for efficient polynomial arithmetic in `Z_q[x]/(x^n+1)`. NTRU uses `Z_q[x]/(x^n-1)`. Nowhere in the specs (pq-crystals.org, NIST FIPS 203/204/205) is a Dirichlet L-function evaluated. The hardness reductions go through Module-LWE / Module-SIS / NTRU assumption and lattice estimators (lattice-estimator / LWE-estimator tools), which measure BKZ block-size cost curves, not L-values.

The only places Dirichlet characters appear tangentially:
- Decomposing cyclotomic `Z[ζ_n]` into CRT slots uses characters of `(Z/nZ)*`, but evaluates them, not `L(s,χ)`.
- Some ring-LWE hardness proofs (Regev, Lyubashevsky-Peikert-Regev) reference the behavior of Dedekind zeta functions in worst-case-to-average-case reductions. These appear in proofs, not in parameter selection software.

**Hot-path evaluations/sec:** zero (no production pipeline evaluates `L(s,χ)` at all).
**Impact of a 12-141x batch speedup:** zero for lattice PQC.
**Who would pay:** nobody in this subfield.

## Angle 2: Isogeny-based cryptography (CSIDH, SQIsign, SIDH)

This is where the claim has its strongest (but still narrow) footing.

**SIDH / SIKE** — broken in 2022 by Castryck-Decru. Irrelevant.

**SQIsign** — based on the quaternion-isogeny problem and the Deuring correspondence. The NIST Round-1 spec (2023) does not evaluate Dirichlet L-functions. Key generation does endomorphism-ring computations, KLPT, Eichler orders. No Dirichlet `L`.

**SEA (Schoof-Elkies-Atkin) point counting** — The "L-function" that matters here is the Hasse-Weil `L(s,E)` of an elliptic curve, with Dirichlet coefficients `a_p = p+1-#E(F_p)`. SEA computes those `a_p` via modular polynomials and Elkies/Atkin prime splitting, **not** by evaluating `L(s,E)`. Dirichlet L-functions of Dirichlet characters (Q(i), Q(√-d), cyclotomic L-functions) do **not** appear in the SEA hot path. Batch Dirichlet L would not help SEA.

**CSIDH / CSI-FiSh / SCALLOP / PEGASIS** — This is the one real use case.
  - CSIDH's parameter is `p = 4·ℓ_1···ℓ_n - 1`. The class group `Cl(Z[π])` is an order in an imaginary quadratic field `Q(√-p)`.
  - **CSI-FiSh (Beullens-Kleinjung-Vercauteren, Asiacrypt 2019)** performed a record class-group computation for CSIDH-512: a 154-digit discriminant. They used Hafner-McCurley / Buchmann-style subexponential methods. These algorithms **do** use analytic-class-number estimates `h ≈ (√|d|/π)·L(1,χ_d)` as a stopping criterion / verifier for the relation lattice.
  - **SCALLOP (2023)** and **PEGASIS (2025)** scaled this up; they need to compute class groups of orders in larger discriminant fields `Q(√-d)` with `|d|` up to hundreds or thousands of digits.

Here the pattern: one big class-group computation *per parameter set*, happening at research / standardization time — not during keygen, sign, or verify. Order of magnitude: a handful of `L(1,χ_d)` computations per *year* across the whole community, each at a discriminant so large that individual eval might take minutes to hours in PARI or Magma, regardless of batching.

**Would a 12-141x batch speedup move the needle?** Only if your batch is over a *family of characters of the same conductor*. In the CSIDH context you typically have one `χ_d` per discriminant, not a family sharing conductor. The batch speedup structure you have (same conductor, family of χ's) maps more naturally to **genus-theory computations** for class groups of non-fundamental discriminants or to **Dedekind zeta factorizations** `ζ_K(s) = ∏ L(s, χ)` over characters of `Gal(K/Q)`. That factorization *is* used inside PARI's `lfuninit` and is exactly a same-conductor family — so a 12-141x speedup here would genuinely help a researcher evaluating `ζ_K(1)` for abelian number fields.

**Hot-path evaluations/sec (in active research):** tens to thousands per paper, not per second.
**Impact:** a class-group computation that takes 3 weeks instead of 1 year is genuinely useful for one paper per year. Not a commercial bottleneck.
**Who pays:** Steven Galbraith, Luca De Feo, Ward Beullens-style research groups; possibly NIST PQC reviewers evaluating CSIDH parameter claims.

## Angle 3: Class numbers / imaginary quadratic fields in cryptanalysis

Class numbers `h(-d)` appear in:
- **Cohen-Lenstra heuristics** — predicting the distribution of `Cl(Q(√-d))`. Mostly theoretical; computations use analytic class number formula at scale up to `|d| < 10^11` (Jacobson-Ramachandran-Williams, Mosunov-Jacobson). This is a legitimate batch Dirichlet-L workload: for each fundamental discriminant `d` in a range, compute `L(1,χ_d)` then recover `h(-d)`. Batch speedups **genuinely help** here.
- **CM method for pairing-friendly curves** (BN, BLS) — solves `DV² = 4p-t²` for small `D`. The `D` values used in practice are tiny (`D=3` for BN, `D=1,2,3` for common BLS variants). Class number `h(-D) = 1`. No batch Dirichlet L workload.
- **Cryptanalysis of RSA via class groups** (Schnorr, Buchmann-Williams class-group-based cryptosystems, NICE cryptosystem attacks by Jaulmes-Joux 2000, Castagnos-Laguillaumie). These systems are historical / broken; modern cryptanalysis does not run at a rate where batch L-evaluation is the bottleneck.

**Verdict:** batch `L(1,χ_d)` over ranges of `d` is a real workload in *analytic number theory* (Cohen-Lenstra, Littlewood-bound verification) but essentially not in active cryptanalysis.

## Angle 4: PARI/GP, Sage, Magma, FLINT/Arb benchmarks

Checked pari-dev and the FLINT/Arb documentation:

- **PARI/GP** (Molin-Belabas `lfun` framework): explicitly exploits that "conjugate characters are evaluated simultaneously" and uses `lfuninit` to factor abelian Dedekind zeta functions as products of Dirichlet L's over a shared conductor. This is literally the family-of-characters same-conductor batch structure your C code accelerates. Molin's 2015 Bordeaux talk flags this as a practical optimization. If your C implementation beats PARI's `lfun` by 12-141x on such batches at cryptographic precision (say 100-300 digits), that's a real, publishable win for the PARI ecosystem.
- **FLINT/Arb** (`acb_dirichlet_l`, Fredrik Johansson): competitive; has reduced-complexity rational-point evaluators (`acb_dirichlet_l_fmpq_afe`). Johansson's blog posts benchmark single-character evaluations but do not emphasize family-batching. A batch speedup would be welcomed upstream.
- **Magma, Sage**: Sage calls PARI; Magma has its own implementation. No public batch-Dirichlet benchmark suite exists.
- **LMFDB** (Cremona et al.): hosts hundreds of millions of precomputed L-function data points. Their bottleneck historically has been *modular form coefficient computation* and *rigorous zero verification*, not batch Dirichlet L-eval. A 12-141x speedup on same-conductor batches would help populate Dirichlet L tables faster, but Dirichlet L-functions are already a "solved" corner of LMFDB relative to GL(n) automorphic L-functions.

**Hot-path evaluations/sec (LMFDB/PARI/Arb users):** extreme niche. Maybe 10-100 researchers worldwide regularly push these libraries. For them, a 12-141x speedup is genuinely meaningful.

## Angle 5: Cryptanalysis using L-function properties

- **Attacks via analytic rank** — Heuristic rank estimates for elliptic curve L-functions are used in the BSD side of cryptanalysis, but this is `L(s,E)`, not Dirichlet L.
- **Jacobi-sum primality proofs** (APR-CL, used in PARI `isprime`) — evaluate character sums, not `L(s,χ)`.
- **Number-field sieve (NFS) for DLP on pairing-friendly curves** — exTNFS (Kim-Barbulescu 2016). Does not use Dirichlet L evaluation on the hot path; uses polynomial selection heuristics.

No hot path here.

## Angle 6: LMFDB

Covered in Angle 4. The LMFDB population pipeline for Dirichlet L's is largely complete; incremental batch speedups move the needle modestly for future extensions (higher conductors, higher precision for RH-verification efforts).

**Impact:** real but small. Publishable note for LMFDB team, not a funded deliverable.

## Angle 7: Quantum algorithms (Shor, Kuperberg, CSIDH attacks)

- **Shor** — factors and computes discrete logs. No L-function evaluation.
- **Kuperberg / CSIDH dihedral-hidden-shift attack** — uses phase vectors indexed by characters of an abelian group. The algorithm evaluates the *group action* (an isogeny) on superpositions; it does **not** evaluate `L(s,χ)`. The characters are objects of the algorithm, not analytic targets.
- **Quantum class-group computation** (Biasse-Song, Eisenträger-Hallgren-Kitaev-Song) — solves the PIP / class-group DLP in polynomial quantum time. Uses HSP machinery, not `L(s,χ)` evaluation.

No hot path. Zero impact.

---

## Quantitative bottom line

| Angle | L-eval a hot path? | Evals/sec realistic | 12-141x speedup impact | Who cares |
|---|---|---|---|---|
| 1. Kyber/Dilithium/NTRU | No | 0 | None | Nobody |
| 2a. SQIsign/SEA | No | 0 | None | Nobody |
| 2b. CSIDH/CSI-FiSh class group | Indirect, once per param set | ~1e2 per paper | Modest (weeks→days, once per param) | ~20 researchers |
| 3. Cohen-Lenstra / class number tables | **Yes** | 1e4-1e6 per campaign | **Real** (months→days) | ~10 analytic number theorists |
| 4. PARI/FLINT/Arb users | **Yes, exactly this shape** | varies | **Publishable** | ~50-100 library users |
| 5. L-based cryptanalysis | No | 0 | None | Nobody |
| 6. LMFDB | Yes, but already mostly done | batch-1e6 per year | Small | LMFDB team (~10 people) |
| 7. Quantum / Kuperberg | No | 0 | None | Nobody |

## Honest recommendation for your applications list

**Remove:** "lattice cryptosystem parameter searches" — false, there is no Dirichlet L in the lattice PQC pipeline.

**Remove:** "isogeny cryptosystem parameter searches" — overstated. SEA and SQIsign don't use it. CSIDH class-group computation uses it only as an indirect verification quantity, once per parameter set, and your same-conductor-family batch shape doesn't match the usual CSIDH workload (one discriminant at a time).

**Keep, but reframe honestly:**

> "Same-conductor batch Dirichlet L evaluation accelerates Dedekind zeta factorization `ζ_K(s) = ∏_{χ ∈ Ĝ} L(s,χ)` for abelian number fields `K`, which is a primitive used inside PARI/GP's `lfuninit` and in analytic class-number computations (Cohen-Lenstra range scans, Littlewood-bound verification). A 12-141x speedup on this primitive would be of direct interest to computational number theory groups (LMFDB, PARI, Arb/FLINT) and has secondary value in class-group precomputations for research-grade isogeny schemes (CSI-FiSh, SCALLOP). It is not a bottleneck in production lattice or isogeny cryptography."

This is defensible, citable, and won't get laughed off by a competent crypto reviewer.

## Blunt summary

- The claim as written is puffery.
- There is one real, narrow, academically useful application: same-conductor Dirichlet L batches inside Dedekind-zeta factorizations and class-number table computations.
- Market size: tens, maybe low hundreds, of researchers worldwide. Zero commercial crypto revenue.
- If this is positioned as "our C library plugs into PARI's `lfun` and gives 12-141x on abelian Dedekind-zeta decompositions", you have a real contribution worth a short paper or a PARI patch.
- If it is positioned as "accelerates crypto parameter search", you will get (rightly) dismissed.

**Action item:** rewrite that bullet. Drop "lattice". Drop "isogeny" (or qualify heavily as class-group precompute for CSIDH-family research). Add "abelian Dedekind-zeta factorization" and "class-number table computation". Cite Molin's PARI `lfuninit` talk and FLINT/Arb `acb_dirichlet` as the concrete libraries that would consume this.

## Sources consulted

- pq-crystals.org Kyber/Dilithium specifications (round-3)
- NIST FIPS 203 / 204 (ML-KEM, ML-DSA)
- Beullens-Kleinjung-Vercauteren, CSI-FiSh, Asiacrypt 2019 (eprint 2019/498)
- SCALLOP (2023), PEGASIS (2025)
- SQIsign round-1 spec, NIST PQC additional signatures
- Castryck-Lange-Martindale-Panny-Renes, CSIDH, Asiacrypt 2018
- Schoof-Elkies-Atkin literature (Wikipedia + Gaski survey)
- Hafner-McCurley subexponential class group algorithm
- Buchmann-Jacobson class-group computation
- Jacobson-Ramachandran-Williams, class numbers of imaginary quadratic fields |Δ|<10^11
- PARI/GP `lfun` catalogue; Molin Bordeaux 2015 talk
- FLINT `acb_dirichlet.h` documentation; Fredrik Johansson 2016 blog on Dirichlet L in Arb
- LMFDB project paper (Cremona et al., FoCM 2021)
- Kim-Barbulescu, exTNFS, Crypto 2016
- Kuperberg HSP algorithms; Peikert C-sieves; Childs-Jao-Soukharev CSIDH quantum attack

Word count: ~2050.
