# mr1_par validation record (2026-05-16)

## Bug found & fixed (pre-launch gate working as intended)

`mr1_par.c` word-extraction loop `while(bits){…}` was missing
`bits &= bits - 1;` — it spun forever re-counting one prime (observed:
29 min @539% CPU on a 2 s 10¹⁰ job). Reproduced at 10⁷, root-caused by
inspection, fixed, re-validated. The serial `mr1_sieve.c` already had
the clear and was unaffected. A separate bug in the *verification*
harness (`char_table` over-generated characters: 18 for N=7, φ=6) was
also found and replaced by `chargrp.py` (CRT prime-power decomposition
with a built-in orthogonality self-test; passes for N∈{7,8,11,19,23},
including the non-cyclic (ℤ/8)*).

## Validation results (all PASS) — mr1_par @ x≤10¹⁰

| check | scope | result |
|---|---|---|
| terminates | 10⁷ | yes (was: infinite loop) |
| π(10⁷) | parallel | 664,579 = published |
| determinism across (T,NCHUNK) | (7,224)(4,9)(8,1)(1,50) | byte-identical |
| serial == parallel | 10⁹,10¹⁰ all N,a | byte-identical |
| gold vs Phase-1 (out2+indep_full) | 10⁹,10¹⁰ | 126 cells exact, 0 mismatch |
| identity (3.1) | corrected chargrp | 120 cells, worst resid 1.98e-7 |
| π(x) anchors | 10⁹,10¹⁰ ×5 N | 10/10 = published |

π anchors independently confirmed by the sieves at 10⁹ 10¹⁰ 10¹¹ 10¹²
(serial), all matching the published table.

Conclusion: `mr1_par` is trustworthy for the 3·10¹⁴ extension. The
serial `mr1_sieve` 1.3·10¹³ run is unaffected (different code path,
already-correct loop) and continues.
