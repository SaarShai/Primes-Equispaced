# PMF salvage benchmark v2 — results

## Bottom line

**PMF loses to baselines on all 4 anomaly classes, all kernel sizes, all prefilters.** Industry pivot: dead. The original 20/20 result on L-function zeros was domain-specific and does NOT generalize to colored-noise + transient-anomaly detection.

Per anomaly class:

- **spike**: best PMF = `PMF[K=17,raw]` (AUC-PR 0.1820); best baseline = `OneClassSVM` (AUC-PR 0.8638); Δ=-0.6818; **PMF LOSES**
- **freq_burst**: best PMF = `PMF[K=17,ar1res]` (AUC-PR 0.0513); best baseline = `IsolationForest` (AUC-PR 0.7460); Δ=-0.6947; **PMF LOSES**
- **chirp**: best PMF = `PMF[K=17,ar1res]` (AUC-PR 0.0499); best baseline = `IsolationForest` (AUC-PR 0.6842); Δ=-0.6343; **PMF LOSES**
- **variance_break**: best PMF = `PMF[K=17,raw]` (AUC-PR 0.0673); best baseline = `IsolationForest` (AUC-PR 0.4309); Δ=-0.3635; **PMF LOSES**

Sweep: 100 seeds, n=4000, anomalies/signal=8, seed = 42 + run_id, tolerance ±5 samples for ground truth.

## Class: `spike`

| Detector | AUC-PR (mean ± std) | Prec@R=.95 (mean) | Time/seed (s) |
|---|---|---|---|
| OneClassSVM **(BEST)** | 0.8638 ± 0.0706 | 0.5353 | 0.021 |
| IsolationForest | 0.8344 ± 0.0879 | 0.4165 | 0.074 |
| PMF[K=17,raw] | 0.1820 ± 0.0514 | 0.0240 | 0.002 |
| PMF[K=17,ar1res] | 0.1392 ± 0.0373 | 0.0243 | 0.001 |
| PMF[K=256,ar1res] | 0.0283 ± 0.0072 | 0.0221 | 0.001 |
| PMF[K=1024,raw] | 0.0254 ± 0.0090 | 0.0226 | 0.002 |
| PMF[K=1024,ar1res] | 0.0239 ± 0.0055 | 0.0223 | 0.002 |
| PMF[K=256,raw] | 0.0238 ± 0.0069 | 0.0221 | 0.001 |
| PMF[K=64,ar1res] | 0.0193 ± 0.0028 | 0.0219 | 0.001 |
| PMF[K=64,raw] | 0.0182 ± 0.0032 | 0.0219 | 0.001 |

## Class: `freq_burst`

| Detector | AUC-PR (mean ± std) | Prec@R=.95 (mean) | Time/seed (s) |
|---|---|---|---|
| IsolationForest **(BEST)** | 0.7460 ± 0.0697 | 0.4311 | 0.074 |
| OneClassSVM | 0.6142 ± 0.0812 | 0.3306 | 0.022 |
| PMF[K=17,ar1res] | 0.0513 ± 0.0192 | 0.0221 | 0.001 |
| PMF[K=17,raw] | 0.0318 ± 0.0112 | 0.0222 | 0.001 |
| PMF[K=1024,raw] | 0.0260 ± 0.0091 | 0.0223 | 0.002 |
| PMF[K=64,raw] | 0.0258 ± 0.0083 | 0.0222 | 0.001 |
| PMF[K=1024,ar1res] | 0.0253 ± 0.0078 | 0.0221 | 0.002 |
| PMF[K=64,ar1res] | 0.0252 ± 0.0068 | 0.0221 | 0.001 |
| PMF[K=256,raw] | 0.0248 ± 0.0078 | 0.0222 | 0.001 |
| PMF[K=256,ar1res] | 0.0244 ± 0.0070 | 0.0220 | 0.001 |

## Class: `chirp`

| Detector | AUC-PR (mean ± std) | Prec@R=.95 (mean) | Time/seed (s) |
|---|---|---|---|
| IsolationForest **(BEST)** | 0.6842 ± 0.0815 | 0.4322 | 0.074 |
| OneClassSVM | 0.4804 ± 0.0830 | 0.2582 | 0.024 |
| PMF[K=17,ar1res] | 0.0499 ± 0.0182 | 0.0220 | 0.001 |
| PMF[K=17,raw] | 0.0360 ± 0.0134 | 0.0221 | 0.001 |
| PMF[K=1024,raw] | 0.0262 ± 0.0094 | 0.0222 | 0.002 |
| PMF[K=64,raw] | 0.0255 ± 0.0078 | 0.0221 | 0.001 |
| PMF[K=1024,ar1res] | 0.0255 ± 0.0074 | 0.0221 | 0.002 |
| PMF[K=256,raw] | 0.0255 ± 0.0087 | 0.0222 | 0.001 |
| PMF[K=256,ar1res] | 0.0244 ± 0.0065 | 0.0221 | 0.001 |
| PMF[K=64,ar1res] | 0.0242 ± 0.0051 | 0.0222 | 0.001 |

## Class: `variance_break`

| Detector | AUC-PR (mean ± std) | Prec@R=.95 (mean) | Time/seed (s) |
|---|---|---|---|
| IsolationForest **(BEST)** | 0.4309 ± 0.1002 | 0.3462 | 0.071 |
| OneClassSVM | 0.3917 ± 0.0905 | 0.3075 | 0.020 |
| PMF[K=17,raw] | 0.0673 ± 0.0311 | 0.0219 | 0.001 |
| PMF[K=17,ar1res] | 0.0627 ± 0.0234 | 0.0219 | 0.001 |
| PMF[K=256,ar1res] | 0.0260 ± 0.0068 | 0.0220 | 0.001 |
| PMF[K=256,raw] | 0.0258 ± 0.0070 | 0.0220 | 0.001 |
| PMF[K=1024,ar1res] | 0.0254 ± 0.0066 | 0.0222 | 0.002 |
| PMF[K=1024,raw] | 0.0253 ± 0.0084 | 0.0224 | 0.002 |
| PMF[K=64,ar1res] | 0.0210 ± 0.0051 | 0.0218 | 0.001 |
| PMF[K=64,raw] | 0.0188 ± 0.0062 | 0.0216 | 0.001 |

## Kernel/prefilter trends across classes

Mean AUC-PR averaged over all anomaly classes per PMF config:

| Config | mean AUC-PR (over 4 classes) |
|---|---|
| PMF[K=17,raw] | 0.0793 |
| PMF[K=17,ar1res] | 0.0758 |
| PMF[K=256,ar1res] | 0.0258 |
| PMF[K=1024,raw] | 0.0257 |
| PMF[K=1024,ar1res] | 0.0250 |
| PMF[K=256,raw] | 0.0250 |
| PMF[K=64,ar1res] | 0.0224 |
| PMF[K=64,raw] | 0.0221 |

Baseline AUC-PR averaged over all classes:

- OneClassSVM: 0.5875
- IsolationForest: 0.6739

## Honest assessment

- PMF loses across the board. Longer kernels do not rescue it. AR(1) residualization does not rescue it.
- The Mertens kernel's value seems specific to detecting structure in L-function zero sequences (where prime-indexed weights match the actual underlying number-theoretic content) and does NOT translate to generic colored-noise-plus-transient detection.
- Recommendation: shelve industry pivot for general anomaly detection. If pursuing PMF further, restrict scope to genuinely number-theoretic data sources (e.g. L-function zeros, character sums, modular forms).