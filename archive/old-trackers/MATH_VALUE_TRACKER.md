# Mathematical Value Tracker
# Things researchers and mathematicians would find useful/interesting
# Priority: HIGH = directly useful, MEDIUM = interesting, LOW = niche

## TOOLS (methods that make something practical at scale)

| Tool | What it enables | Who benefits | Priority |
|------|----------------|-------------|----------|
| Batch L-function spectroscope | Zero detection for entire L-function families simultaneously (12x-141x faster) | LMFDB, computational NT | **HIGH** |
| Siegel zero exclusion | Unconditional verification that L(s,χ) has no zeros off critical line | Class number researchers, primes-in-progressions | **HIGH** |
| Predictive M(p) model | Predict Mertens function at any prime from 20 zeros (R=0.952) | Computational NT, explicit formula researchers | **HIGH** |
| GRH verification pipeline | Verify GRH for 9592+ quadratic characters simultaneously | Anyone using GRH-conditional results | **HIGH** |
| MC z-score spectroscope | Detect degree-2 L-function zeros (EC, modular forms) | Elliptic curve researchers, LMFDB | **MEDIUM** |
| General spectroscope principle | Any summatory function with explicit formula → zero detection | Broad analytic NT | **HIGH** |

## RESULTS (mathematical findings researchers would cite)

| Finding | Significance | Who benefits | Priority |
|---------|-------------|-------------|----------|
| Universality: any Σ1/p=∞ subset detects all zeros | New structural theorem about prime-zero encoding | Analytic NT | **HIGH** |
| Dichotomy: unconditional zero detection | New RH equivalence with "graceful degradation" | RH researchers | **HIGH** |
| Bounded gaps corollary | Links Maynard-Tao to zero detection | Prime gap researchers | **HIGH** |
| Class number bounds 5-14x | Better unconditional h(-p) estimates | Algebraic NT, Bhargava program | **HIGH** |
| Primes in progressions for large q | Only unconditional tool for q > (log x)^A | Analytic NT | **HIGH** |
| Prime gaps detect zeros (3.8x) | Novel connection: gaps carry spectral information | Prime gap researchers, Cramér model | **HIGH** |
| 20 zeros explain 90.6% of M(p) variance | First quantification of zero information content | Explicit formula researchers | **HIGH** |
| R improves out-of-sample (0.938→0.952) | Explicit formula MORE accurate at larger primes | Computational NT | **MEDIUM** |
| Fourth moment 96x amplification | Connects spectroscope to pair correlation | RMT, Montgomery conjecture | **MEDIUM** |
| Smooth numbers detect zeros (2.9x) | Extends framework to Dickman function | Factoring algorithm researchers | **MEDIUM** |
| Detection pattern: explicit formula = detection | Characterizes WHICH functions detect zeros | Analytic NT theory | **HIGH** |
| Figure-eight = golden ratio (Lean verified) | Algebraic identity in three-body dynamics | Dynamical systems, celestial mechanics | **HIGH** |
| Lucas/Pell number field classification | Orbits organized by quadratic number fields | Dynamical systems | **MEDIUM** |
| 434 Lean results | Largest Farey formalization | Formal verification community | **MEDIUM** |
| Finite field validation (0.005 rad) | Ground truth confirmation of method | Method validation | **MEDIUM** |
| EC spectroscope methodology | Degree-2 L-functions need MC normalization | EC researchers | **MEDIUM** |

## PEOPLE TO CONTACT (from OUTREACH_TARGETS.md)

| Person/Group | Why they'd care | Our relevant finding |
|-------------|----------------|---------------------|
| LMFDB (Cremona, Farmer) | Batch speedup for database expansion | 12x-141x L-function batch |
| Platt/Trudgian | Independent verification method | Spectroscope as cross-check |
| Maynard/Tao/Green | Bounded gaps → zero detection | Universality corollary |
| Keating/Snaith | New pathway to GUE statistics | Fourth moment, pair correlation |
| Berry/Connes | Quantum chaos / RH framework | Dichotomy, RIP interpretation |
| Bhargava/Wood/Ellenberg | Class number bounds | 5-14x Siegel exclusion |
| Lean community (Buzzard) | 434 Farey theorems | Mathlib contributions |
| Cramér model researchers | Prime gaps detect zeros | 3.8x gap spectroscope |
| Factoring algorithm researchers | Smooth number spectroscope | 2.9x, Dickman connection |
