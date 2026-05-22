# mr1_sieve benchmark + decision-gate compute estimate (2026-05-16)

Machine: Apple M1 Max, 10-core (8 perf), macOS Darwin 25.4.0.
Toolchain: Apple `cc` (clang), `-O3 -std=c99 -fno-strict-aliasing -lm`.
No primesieve / primecount / brew on this machine (Phase-1 was a
different machine). `mr1_sieve.c` = dependency-free odd-only bit
segmented sieve, absolute-index bookkeeping, hardcoded moduli.

## Correctness anchors (PASS — matched against published pi(10^k))

| x      | mr1 total pi(x) | published pi(x)   | match |
|--------|-----------------|-------------------|-------|
| 1e9    | 50,847,534      | 50,847,534        | YES   |
| 1e10   | 455,052,511     | 455,052,511       | YES   |
| 1e11   | 4,118,054,813   | 4,118,054,813     | YES   |

Residue counts at 1e10 (N=8) exactly match the independently-authored
Phase-1 `koyama_replication_bundle/independent_sieve.c`
(a1=113,758,759 a3=113,763,027 a5=113,764,516 a7=113,766,208).

## Single-thread wall-clock (measured)

| x    | wall (s) | per-decade |
|------|----------|------------|
| 1e9  | 1.14     | -          |
| 1e10 | 12.89    | 11.3x      |
| 1e11 | 126.42   | 9.8x       |

Model cost = O + k * x * lnln(x), fit on the two asymptotic points
(1e10, 1e11):  k = 3.890e-10 s,  O = 0.69 s.

## Extrapolated single-thread wall-clock (decision gate)

| x       | est. wall (1 core) |
|---------|--------------------|
| 1.3e13  | ~4.8 h             |
| 1e14    | ~37 h (1.6 d)      |
| 3e14    | ~113 h (4.7 d)     |

(Independently corroborated: the same model applied to the Phase-1
`independent_sieve.c` two measured points reproduces that tool's
reported "~3.7 h to 1.3e13", so the extrapolation is sound.)

A wheelless C segmented sieve tops out ~35M primes/s here; primesieve
(wheel-210, not installed) would be ~3x faster but adds an external
dependency contrary to the single-artefact-dir reproducibility goal.

## Lever: range-split parallelism

8 perf cores -> ~6-7x: 1e14 ~6 h, 3e14 ~16-18 h. Adds correctness
surface; fully mitigated by the mandated cross-checks (independent
single-thread sieve at sub-scale + identity (3.1) + pi(x) anchors at
every snapshot + serial-vs-parallel agreement at 1e13).
