# Reproducibility manifest — D2 −1-dominance dynamic curve

## Machine / toolchain (this study)

- Hardware: Apple M1 Max, 10-core (8 performance), 32 GB RAM
  (note: a *different* machine from Phase-1's M1 Max/192 GB — the
  Phase-1 cross-check is therefore also a hardware-independence check).
- OS: macOS 26.4.1 (build 25E253), Darwin 25.4.0.
- Compiler: Apple clang 21.0.0 (clang-2100.0.123.102), invoked as `cc`.
- Python: 3.9.6; mpmath 1.3.0; numpy 2.0.2.
- No primesieve / primecount / Homebrew present — both sieves are
  dependency-free C99 by design (single-artefact-dir reproducibility).

## Build flags

```
cc -O3 -std=c99 -Wall -fno-strict-aliasing            -o src/mr1_sieve src/mr1_sieve.c -lm
cc -O3 -std=c99 -Wall -fno-strict-aliasing -pthread   -o src/mr1_par   src/mr1_par.c   -lm
```
`-fno-strict-aliasing`: the segment bitset is marked as bytes and
scanned as `uint64_t` words; this flag makes that type-pun defined.

## Source SHA-256 (frozen at run time)

```
mr1_sieve.c     324a32c839e3934a05bc22653c1eedaabddf8dbc0ed69bb4c266e705adc5623a
mr1_par.c       5b8d96d2bbd89292d07a4c0b078b26e598a446f0866883b14460827bb28b8147
make_grid.py    1a2c540a98d2eadd28331a5fa95b1bd9a856ae44690b638b0fc91f0869b8ba0d
verify_curve.py 68f2e9f356d2ac2d18c70a0cb5c9d8efa5e1a98177421012d64c738010d39ccf
xcheck_phase1.py e18c30232c245c0b07521654a93570bc0b438f77ca3d56103b96d709cd1cc9b3
lowzeros.py     f242b8781b58d369ebc7908ff345967223f82bc1938526859eb2d8d412bd74a4
analyze_curve.py e886716920ebd93ddca343003f7be08d8fb478b92b79df95e84e3c1722624248
plot_curve.py   bcac248f9b797ec439985878c84d875f2d1b4e98bbde686507ee9b32f8e5147d
grid_full.txt   e4265e5f2fc8e7387e06dec152fb321a9a1e8079cd358c5b56e29ba6d886a6de
grid_1p3e13.txt f779e316d931d8d1a04c205da50bc3c2871d9d27f0fa1a402ec5e92af8369ba7
```
(`HASHES.sha256` is regenerated over code+data at finalisation.)

## Grid

`make_grid.py`: 50 pts/decade geometric on `[10⁶, 3·10¹⁴]` ∪ the 9
Phase-1 checkpoints ∪ `10^k` anchors ∪ `round(e^{33.4})`.
Full grid = 438 pts; `≤1.3·10¹³` subset = 367 pts.

## Runs (filled at completion)

| run | binary | Xmax | grid | cores | wall | total π(Xmax) | out |
|---|---|---|---|---|---|---|---|
| serial fine curve | mr1_sieve | 1.3·10¹³ | grid_1p3e13 | 1 | {{}} | {{}} | data/curve_1p3e13.tsv |
| parallel extension | mr1_par | 3·10¹⁴ | grid_full | 7 | {{}} | {{}} | data/curve_3e14.tsv |

## Verification ledger (filled at completion)

| check | tool | result |
|---|---|---|
| serial vs parallel bit-identical (shared grid) | cmp | {{}} |
| gold: exact vs Phase-1 (9 checkpoints) | xcheck_phase1.py | {{}} |
| identity (3.1) all snapshots | verify_curve.py | {{}} |
| π(x) anchors vs published | verify_curve.py | {{}} |
| parallel determinism (T,NCHUNK variants) | cmp | {{}} |
| independent γ_min(N) | lowzeros.py | {{}} |
