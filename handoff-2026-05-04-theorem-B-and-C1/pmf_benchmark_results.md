# PrimeMatchedFilterDetector benchmark

- Seeds: 100, signal length N=10000, planted anomalies per signal: 10
- Background: AR(1), φ=0.7, σ_e=1.0
- Anomalies: triangular bumps, width 1–7, amplitude 4–8σ_bg, random sign
- Metrics computed with ±5-sample tolerance window for ground truth

## Bottom line

**The prime-matched-filter detector ranks #4 of 6 on AUC-PR** (mean 0.1094). Top: OneClassSVM (W=11) (0.8997).
On precision @ recall=0.95 it ranks #3.

## Results table (mean over seeds)

| Detector | Prec@R=0.95 | F1@R=0.95 | AUC-PR | FPR | Latency (samples) | Time/seed (s) |
|---|---|---|---|---|---|---|
| PrimeMatchedFilter (M/√p) | 0.0128 ± 0.0028 | 0.0252 ± 0.0054 | 0.1094 ± 0.0301 | 0.8412 | 0.0350 | 0.0029 |
| PrimeMatchedFilter (1/√p) [ablation] | 0.0111 ± 0.0004 | 0.0220 ± 0.0008 | 0.0381 ± 0.0096 | 0.9399 | 0.0440 | 0.0025 |
| IsolationForest (W=11) | 0.2369 ± 0.1303 | 0.3622 ± 0.1597 | 0.7671 ± 0.0909 | 0.0532 | 0.0250 | 0.0990 |
| OneClassSVM (W=11) | 0.6299 ± 0.2438 | 0.7262 ± 0.2154 | 0.8997 ± 0.0499 | 0.0137 | 0.0270 | 0.0556 |
| Rolling z-score (W=100) | 0.0119 ± 0.0009 | 0.0235 ± 0.0017 | 0.2345 ± 0.0381 | 0.8813 | 0.0010 | 0.0023 |
| Hampel filter (W=11) | 0.0110 ± 0.0002 | 0.0217 ± 0.0003 | 0.0123 ± 0.0051 | 1.0000 | 0.0000 | 0.1632 |

## Honest assessment

- PrimeMatchedFilter mean latency: 0.04 samples; PMF mean precision @ recall=0.95: 0.0128.
- vs **PrimeMatchedFilter (1/√p) [ablation]**: PMF beats on AUC-PR (Δ=+0.0713); beats on precision@R=.95 (Δ=+0.0016).
- vs **IsolationForest (W=11)**: PMF loses to on AUC-PR (Δ=-0.6577); loses to on precision@R=.95 (Δ=-0.2241).
- vs **OneClassSVM (W=11)**: PMF loses to on AUC-PR (Δ=-0.7903); loses to on precision@R=.95 (Δ=-0.6171).
- vs **Rolling z-score (W=100)**: PMF loses to on AUC-PR (Δ=-0.1250); beats on precision@R=.95 (Δ=+0.0008).
- vs **Hampel filter (W=11)**: PMF beats on AUC-PR (Δ=+0.0972); beats on precision@R=.95 (Δ=+0.0018).

## Notes / caveats

- Single-channel synthetic data; structured spikes are exactly the regime a matched filter is designed for, so the comparison is somewhat favourable to PMF.
- IsolationForest and OneClassSVM see length-11 sliding-window features; they are not given the same kernel structure.
- PMF kernel size (n_taps=17) and window_size=100 were chosen a priori; no per-seed tuning. Hyperparameter sensitivity not explored here.
- The Mertens-weighted kernel is approximately mean-zero and oscillatory, which suppresses the AR(1) low-frequency baseline and accentuates transients.