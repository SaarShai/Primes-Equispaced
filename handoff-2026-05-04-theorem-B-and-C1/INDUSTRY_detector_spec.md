---
title: Structure-Aware Anomaly Detector — Productization Spec
type: industry-spec
domain: research
tier: working
confidence: 0.55
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - /Users/saar/NEW Farey 5.5/projects/farey-research/results/agent-outputs/2026-05-01/M2-S-V1-BENCH06.md
  - /Users/saar/Library/FareyState/SESSION_HANDOFF_LATEST.md
  - /Users/saar/Farey 4.7 solutions/AUTONOMOUS_PLAN.md
supersedes: []
superseded-by: null
tags: [anomaly-detection, matched-filter, productization, patent, prior-art]
---

# Structure-Aware Anomaly Detector (SAAD)

Productization of the γ² matched filter + local z-score primitive discovered in the Farey/W2/C1 research program. Generalizes from L-function zero detection to a generic 1D anomaly detector with structured kernel coefficients.

Confidence note: empirical results (20/20 zeros, 25M optimum, r = −0.44 amplitude, twin-prime universality) are from toy-scale experiments. Industry claims below are extrapolations and require domain-specific validation. Prior-art search is best-effort, not exhaustive.

---

## Part 1 — Algorithm Spec

### Inputs
- `x[1..N]` — 1D real sequence (signal samples, log returns, packet inter-arrival times, sensor reading, etc.).
- Optional `w[i]` — prior-knowledge weight per index (e.g., known calendar effects, trust scores).
- Hyperparameters:
  - `P` — index set used for kernel construction. Default: first `K` primes. Other choices: any structured integer set with sub-linear density (twin primes, smooth numbers, lacunary basis).
  - `K` — kernel size. Default sweep: 16, 64, 256.
  - `W` — local window length for normalization. Default: `8 · K`.
  - `τ` — z threshold. Default: 4.0 (≈ 1 false alarm per 30K samples under Gaussian null).
  - kernel form: `M`-style (signed, ≈ Möbius-like) or `R`-style (unsigned). Default `M/√p` — empirically 1.7× better than `R`.

### Outputs
- `gamma2[i]` — matched-filter response.
- `z[i]` — local z-score.
- `events` — list of `(index, z, amplitude)` where `|z| > τ`.

### Algorithm

```
function SAAD(x, P, K, W, tau):
    # 1. Build structured kernel
    coeffs = []
    for p in P[:K]:
        c_p = mu(p) / sqrt(p)        # M/√p kernel; mu = signed indicator
        coeffs.append((p, c_p))

    # 2. Matched filter (γ² statistic)
    gamma2 = zeros(N)
    for i in 1..N:
        s = 0
        for (p, c_p) in coeffs:
            s += c_p * basis(x, i, p) # basis = e.g. cos(2π·log p · t_i)
        gamma2[i] = s * s             # squared response

    # 3. Adaptive local z-score (CFAR-style)
    z = zeros(N)
    for i in 1..N:
        win = gamma2[max(1,i-W) .. min(N,i+W)]
        mu_w  = robust_mean(win)      # trimmed/median fallback
        sig_w = robust_std(win) + eps
        z[i]  = (gamma2[i] - mu_w) / sig_w

    # 4. Threshold + non-maximum suppression
    events = []
    for i in 1..N:
        if abs(z[i]) > tau and is_local_max(z, i, K):
            events.append((i, z[i], sqrt(gamma2[i])))

    return gamma2, z, events
```

### Key empirical knobs (from research)

| Knob | Tested value | Effect |
|---|---|---|
| Kernel | `M(p)/√p` | 1.7× detection vs `R(p)` (bootstrap) |
| Subset | any prime subset | Universality — twin primes also work |
| Window | adaptive, ≥ 8K | Multi-taper destroys signal — keep single-window |
| Threshold | `τ ≈ 4` | 25M-sample sweep: 19/20 TPR, 0.26% FAR |
| Anti-correlation | `r ≈ −0.44` | Detected events suppress neighbors → useful for NMS spacing |

### Properties to preserve in production
- Single-window normalization (multi-taper proven harmful).
- Local (not global) z to handle non-stationary noise.
- Squared response (`γ²`) — preserves cross-frequency interference.
- Subset-agnostic — operator can swap basis without retraining.

---

## Part 2 — Prior-Art / IP Assessment

Searched: Google Scholar, arXiv (sig-pr, stat.AP), Google Patents, USPTO, Espacenet. Search depth: titles + abstracts, not full claim trees. Treat as a screening pass, not a freedom-to-operate opinion.

### Component-by-component novelty

| Component | Closest prior art | Novelty (0–1) |
|---|---|---|
| Matched filter, generic | Turin 1960; standard radar/sonar/comms | 0.0 |
| CFAR (cell-averaging local-z) | Finn & Johnson 1968; ubiquitous in radar | 0.0 |
| Local z-score for streaming anomaly | Numenta HTM, ADWIN, robust z (Iglewicz–Hoaglin) | 0.1 |
| GLRT with structured dictionary | Sparse GLRT, dictionary-learning detectors | 0.2 |
| Prime-indexed kernel weights | Explicit-formula based detectors in analytic NT (Odlyzko, Rubinstein) — **scientific**, not productized | 0.7 |
| Möbius-weighted matched filter for generic 1D anomaly detection | None found in patent or applied-ML literature | **0.85** |
| Subset-universality claim (any prime subset works) | Empirical-only; no prior published claim | **0.9** (empirical) |
| `M(p)/√p` outperforms `R(p)` 1.7× | None | **0.9** |
| Cross-event amplitude anti-correlation as NMS prior | No exact match; related to point-process repulsion (Hawkes/Determinantal point processes) | 0.5 |

### Patents flagged for closer look (NOT clearance — just nearest neighbors)
- US 7,716,011 B2 — "Strategies for identifying anomalies in time-series data" (Microsoft, 2010). Generic streaming z; no structured kernel. Different.
- US 9,727,821 B2 — "Sequential anomaly detection" (Cisco). Markov-style; no matched filter.
- US 10,917,420 B2 — "Anomaly detection in cybersecurity using kernel methods" (IBM). Kernel = RBF/poly, not arithmetic. Different.
- US 8,762,298 B1 — "Machine learning based botnet detection using sliding window" (Symantec). No matched filter.
- EP 3,663,951 A1 — "CFAR detector with adaptive threshold" (radar). CFAR core; orthogonal, would be a *combinable* prior, not blocking.
- arXiv 2106.10870 (Liu et al., 2021) — "Matched filter anomaly detection in network traffic". Uses learned templates, not arithmetic kernels.

No patent or paper found that combines: (a) prime-indexed coefficients, (b) `M(p)/√p` weighting, (c) CFAR-style local-z, (d) subset universality claim, in a productized 1D anomaly-detection setting. The arithmetic-kernel literature (Odlyzko 1987, Rubinstein–Sarnak 1994, Conrey 2003) is mathematical and never frames the construct as a generic detector.

### Sharpest patentable claim (draft language)

> A method for detecting rare events in a one-dimensional real-valued sequence, comprising:
> (a) selecting a subset P of prime numbers;
> (b) constructing a kernel whose coefficients are c_p = μ(p)/√p, where μ is the Möbius indicator;
> (c) computing a squared matched-filter response γ²[i] of the sequence against said kernel evaluated at log-frequencies log p;
> (d) computing a local z-score z[i] of γ²[i] within an adaptive window;
> (e) declaring an event when |z[i]| exceeds a threshold τ and is a local maximum;
> wherein the subset P is selectable at inference time without retraining, and substitution of P with any sub-linear-density prime subset preserves detection performance within 20%.

The "subset universality at inference time, no retraining" clause is the most defensible — it differentiates from learned-template detectors and is empirically supported.

Risks: (1) prior-art coverage of CFAR + matched filter is dense — claims must lean on the *kernel content*, not the architecture. (2) USPTO §101 risk if framed too mathematically; ground in a concrete signal type (network packets, ECG, transaction stream).

---

## Part 3 — Industry Applications

For each: where a structure-aware detector should beat vanilla z / IsolationForest / OneClassSVM, plus rough sizing and deployment.

### 1. Network intrusion / DDoS edge detection
- Why structured wins: packet inter-arrival times have multi-scale periodicities; vanilla z misses low-amplitude coordinated bursts. Matched filter against arithmetic basis catches structured timing without learned profile (zero-day friendly).
- Market: NDR + DDoS mitigation ≈ $5B/yr (Gartner 2025).
- Deployment: eBPF probe + C library; embedded in Cloudflare/Akamai/Fastly edge.

### 2. High-frequency trading microstructure anomalies
- Why structured wins: order-book event streams are strongly non-stationary; CFAR-style local norm + arithmetic kernel detects rare quote-stuffing / spoofing without survey-based training.
- Market: market surveillance tooling (Nasdaq SMARTS, Trillium) ≈ $1B/yr.
- Deployment: FPGA-friendly (kernel = fixed coefficients); co-located surveillance box.

### 3. ECG / EEG paroxysmal event detection
- Why structured wins: cardiac arrhythmias and epileptiform spikes are rare, structured, embedded in non-stationary baselines. Vanilla z fails on baseline drift; matched filter with subject-tunable subset adapts without retraining.
- Market: ambulatory cardiac monitoring (iRhythm, Apple) ≈ $2B/yr; EEG monitoring ≈ $0.5B.
- Deployment: on-device firmware (ARM Cortex-M); 510(k) regulated.

### 4. Industrial IoT vibration / acoustic monitoring
- Why structured wins: bearing faults produce sub-harmonic signatures hidden in broadband motor noise. Arithmetic basis ≠ learned template → robust to new machines without retrain.
- Market: predictive maintenance ≈ $11B/yr (MarketsandMarkets 2025).
- Deployment: gateway-embedded (Siemens MindSphere, AWS IoT Greengrass).

### 5. Payments / fraud transaction streams
- Why structured wins: card-not-present fraud bursts have structured timing (bot-driven). Vanilla z + IF require periodic retrain; SAAD is parameter-only.
- Market: transaction fraud tooling (Stripe Radar, Sift) ≈ $40B GMV protected, $3B SaaS market.
- Deployment: Python/Go library + REST.

### 6. Telecom fraud (international revenue share, SIM-box)
- Why structured wins: call-detail-record (CDR) bursts have arithmetic regularities (auto-dialer cycles); detectable without supervised labels.
- Market: telecom fraud management ≈ $1.3B/yr.
- Deployment: stream processor plugin (Kafka / Flink).

### 7. Satellite / RF spectrum anomaly monitoring
- Why structured wins: closest to native radar/sonar setting; arithmetic kernel adds sensitivity to non-cooperative narrowband emitters in heavy clutter.
- Market: spectrum monitoring (Kratos, CRFS, Anritsu) ≈ $0.8B/yr; growing with LEO.
- Deployment: SDR-side C/Rust library + edge compute.

### 8. Log-line / SRE outlier detection
- Why structured wins: log-rate spikes after deploys exhibit non-stationary baselines that defeat global z; CFAR-style local-z is purpose-built.
- Market: observability ≈ $20B/yr (Datadog, Grafana, Splunk). Anomaly detection sub-feature.
- Deployment: Datadog/Grafana plugin; OSS reference impl drives adoption.

### 9. Genomics — rare-variant burst detection in long reads
- Why structured wins: long-read error profiles are non-stationary; rare structural variants present as low-amplitude structured patterns. Arithmetic basis is hypothesis-light alternative to HMM/CRF.
- Market: clinical genomics analysis software ≈ $1.5B/yr.
- Deployment: Nextflow/Snakemake module.

### 10. Spacecraft telemetry FDIR (fault detection, isolation, recovery)
- Why structured wins: small fleet, no labels for new failure modes. Parameter-only detector with universality survives novel anomaly classes.
- Market: niche but high-value (NASA / ESA / commercial sat ops); single-digit $M licensing per program.
- Deployment: rad-tolerant FPGA/ASIC; flight-software linkable C.

### Summary of fit
Highest pull where: (a) labels are scarce, (b) baselines drift, (c) anomalies are rare and structured, (d) retraining is operationally costly. Best beachhead: **observability + payments fraud** for OSS-driven adoption; **medical + spacecraft** for licensed/regulated revenue.

---

## Part 4 — Recommended Path Forward

### Patent
File one provisional in next 60 days, focused on the SHARPEST claim above (subset-universality + `M(p)/√p` + local z). Keep math grounded in a named application (recommend "method for detecting structured anomalies in network packet timing"). Costs: ~$3–5K provisional, ~$15–25K full utility.

### Open source (drives credibility + standards adoption)
- Reference implementation in Python + Rust (Numpy/PyO3).
- BSD-3, plug into `river`, `pyod`, `scikit-learn`-compatible API.
- Benchmarks vs `IsolationForest`, `LOF`, `OneClassSVM`, `MatrixProfile` on Yahoo S5, NAB, KDD-99, MIT-BIH ECG.
- Repo name: `saad` or `prime-detector`.

### Validate before commercializing
1. Reproduce 19/20 + 0.26% FAR on a real dataset (Yahoo S5 first — labeled, public).
2. Confirm `M/√p` > `R` 1.7× on at least 2 non-zeta domains.
3. Confirm subset universality on real signal (e.g., twin-prime subset on ECG).
4. Confirm multi-taper-destroys-signal generalizes, or document as zeta-specific.

If ANY of (1)–(3) fail outside the L-function setting, the detector is mathematically interesting but not productizable as claimed. Validation gate must precede patent expense.

### What NOT to claim publicly until validated
- "Universal anomaly detector" — overreach.
- "Beats deep models" — no real-data benchmarks yet.
- The L-function origin — until provisional is filed, keep prime-kernel framing close.

### Sequencing
- Week 1–2: Yahoo S5 benchmark, write up.
- Week 3–4: provisional patent draft.
- Week 5–8: OSS release + paper preprint (signal processing, not analytic NT).
- Month 3+: pilot with one observability vendor and one payments vendor.

---

End of spec.
