# Predictive Maintenance MVP: f² Spectral Compensation

## Setup
- 30 healthy + 30 faulty (BPFO @ 89.2 Hz)
- Amps: [0.005, 0.01, 0.02, 0.05, 0.1], 6/amp
- 50000 samples, ~10000Hz, 5.0% dropout
- Pink σ=0.5, White σ=0.05
- 10000 freq bins, resolution ~5.0 mHz

## Methods
| Method | Description |
|--------|-------------|
| A: Raw Standard | Peak power at BPFO from standard LS |
| B: Raw f²-comp | Peak power at BPFO from f²·LS |
| C: Ratio Standard | Peak/baseline ratio from standard LS |
| D: Ratio f²-comp | Peak/baseline ratio from f²·LS |

## ROC Results

| Method | AUC | Threshold | TPR | FPR |
|--------|-----|-----------|-----|-----|
| A: Raw Standard | 0.7500 | 0.000318 | 0.57 | 0.07 |
| B: Raw f²-comp | 0.7483 | 2.529626 | 0.57 | 0.07 |
| C: Ratio Standard | 0.7478 | 9.441698 | 0.53 | 0.03 |
| D: Ratio f²-comp | 0.7500 | 9.821001 | 0.53 | 0.03 |

**Raw power: f² improvement = -0.2%**
**Ratio: f² improvement = +0.3%**

### A: Raw Standard
```
              Faulty  Healthy
Act. Faulty     17      13
Act. Healthy     2      28
```
TPR=0.567 FPR=0.067 Prec=0.895 F1=0.694

| Amp | Det | Rate |
|-----|-----|------|
| 0.5% | 2/6 | 33% |
| 1.0% | 0/6 | 0% |
| 2.0% | 3/6 | 50% |
| 5.0% | 6/6 | 100% |
| 10.0% | 6/6 | 100% |

### B: Raw f²-comp
```
              Faulty  Healthy
Act. Faulty     17      13
Act. Healthy     2      28
```
TPR=0.567 FPR=0.067 Prec=0.895 F1=0.694

| Amp | Det | Rate |
|-----|-----|------|
| 0.5% | 2/6 | 33% |
| 1.0% | 0/6 | 0% |
| 2.0% | 3/6 | 50% |
| 5.0% | 6/6 | 100% |
| 10.0% | 6/6 | 100% |

### C: Ratio Standard
```
              Faulty  Healthy
Act. Faulty     16      14
Act. Healthy     1      29
```
TPR=0.533 FPR=0.033 Prec=0.941 F1=0.681

| Amp | Det | Rate |
|-----|-----|------|
| 0.5% | 1/6 | 17% |
| 1.0% | 0/6 | 0% |
| 2.0% | 3/6 | 50% |
| 5.0% | 6/6 | 100% |
| 10.0% | 6/6 | 100% |

### D: Ratio f²-comp
```
              Faulty  Healthy
Act. Faulty     16      14
Act. Healthy     1      29
```
TPR=0.533 FPR=0.033 Prec=0.941 F1=0.681

| Amp | Det | Rate |
|-----|-----|------|
| 0.5% | 1/6 | 17% |
| 1.0% | 0/6 | 0% |
| 2.0% | 3/6 | 50% |
| 5.0% | 6/6 | 100% |
| 10.0% | 6/6 | 100% |

## VERDICT

**Best method: A: Raw Standard** (AUC=0.750)

- f² does not improve raw detection (-0.2%)
- f² has no effect on ratio-based detection (as expected)

**f² compensation shows no significant advantage** in this scenario. Both raw and ratio-based detection perform similarly with and without f². The 1/f noise floor at BPFO frequency (89.2 Hz) is not steep enough in this band to create meaningful bias.

**Product recommendation**: f² adds negligible complexity and may help in more extreme 1/f environments. Include as optional preprocessing.

### Technical Notes
- f² multiplies LS power by f², counteracting 1/f spectral slope
- Analog of Farey γ² filter: both flatten spectral bias to reveal weak signals
- Ratio-based detection already handles slope → f² redundant there
- f² most useful for simple threshold detectors, not adaptive methods
- For production: adaptive f^α, envelope demod, multi-sensor fusion, trending

![Results](predictive_maintenance_roc.png)
---
*predictive_maintenance_mvp.py*