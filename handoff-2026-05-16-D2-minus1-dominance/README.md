# D2 — The "Dominance of −1" Chebyshev-bias hierarchy as a dynamic curve

Standalone, reproducible experimental-number-theory study of the
finite-x dynamics of the prime race
`D(x;N,a) = π(x;N,a) − π(x;N,1)` for `N ∈ {7,8,11,19,23}` and all
coprime residues `a`, with the conjectured dominance of the class
`a ≡ −1 (mod N)` among the quadratic non-residues.

**This is the user's own independent verification/extension of
Phase-1.** It is NOT a confirmed joint deliverable. Nothing here is to
be sent to Koyama or pushed to any remote without explicit user
approval (counterparty unverified — see `correspondence/KOYAMA.md`
RISK, `project_koyama_risk.md`). Honest scope ceiling:
Experimental-Mathematics / specialist tier; not a proof, not RH/DRH
progress.

## Layering (kept strictly separate)

| Layer | What | Where |
|---|---|---|
| T theoretical bias ordering | RS 1994 (GRH+LI), Aoki–Koyama 2023 (DRH); −1-dominance = **conjecture** | `analysis/THEORY_LAYER.md` |
| O raw observable | `π(x;N,a) − π(x;N,1)`, integer step fn | sieve TSVs in `data/` |
| F finite-range evidence | onsets, reversals, wavelengths | `analysis/FINDINGS_*.md` |
| I asymptotic interpretation | fenced; limiting-density only | draft `NOTE.md` |

## Reproduce from this directory alone

```bash
# 0. deterministic snapshot grid
python3 src/make_grid.py data/grid_full.txt data/grid_1p3e13.txt

# 1. primary sieve (serial), fine curve to 1.3e13  (~5 h, 1 core)
cc -O3 -std=c99 -Wall -fno-strict-aliasing -o src/mr1_sieve src/mr1_sieve.c -lm
./src/mr1_sieve 13000000000000 data/grid_1p3e13.txt \
      data/curve_1p3e13.tsv data/curve_1p3e13_partial.tsv 2> logs/mr1_1p3e13.log

# 2. independent parallel sieve, extension to 3e14  (~16-18 h, 8 cores)
cc -O3 -std=c99 -Wall -fno-strict-aliasing -pthread -o src/mr1_par src/mr1_par.c -lm
./src/mr1_par 300000000000000 data/grid_full.txt data/curve_3e14.tsv 7 224 2> logs/mr1_3e14.log

# 3. cross-checks (ALL must pass before any analysis is trusted)
python3 src/xcheck_phase1.py data/curve_1p3e13.tsv \
      ../../koyama_replication_bundle/out2.tsv \
      ../../koyama_replication_bundle/indep_full.tsv      # gold: exact vs Phase-1
python3 src/verify_curve.py data/curve_1p3e13.tsv         # (R)+(3.1)+(A)
python3 src/verify_curve.py data/curve_3e14.tsv
#  + serial-vs-parallel exact agreement on the shared grid prefix

# 4. independent theoretical anchor + analysis + figures
python3 src/lowzeros.py | tee logs/lowzeros.out
python3 src/analyze_curve.py data/curve_3e14.tsv --emit-plotdata analysis/plotdata
python3 src/plot_curve.py data/curve_3e14.tsv analysis/figures
```

## Cross-check architecture (why it is trustworthy)

1. **Two independent sieves**, different algorithms/code paths:
   `mr1_sieve.c` (serial, odd-only bit, absolute-index) and
   `mr1_par.c` (range-split pthreads, deterministic prefix-combine).
   They must agree bit-for-bit on the shared grid.
2. **Gold reference**: the pre-existing, *independently authored, run
   on a different machine* Phase-1 data
   (`koyama_replication_bundle/{out2,indep_full}.tsv`, themselves two
   mutually-agreeing implementations). Our curve must reproduce all 9
   overlapping checkpoints exactly.
3. **Identity (3.1)** Dirichlet-orthogonality at every snapshot
   (internal-consistency of the count vector; independent code path).
4. **π(x) anchors** at every 10^k (absolute, vs published table,
   self-confirmed by both sieves).
5. **Parallel determinism**: identical output across thread/chunk
   counts.

`HASHES.sha256` / `MANIFEST.md` record code hashes, machine, runtime.
