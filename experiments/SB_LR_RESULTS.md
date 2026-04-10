# Stern-Brocot / Golden Ratio LR Schedule Experiment Results

## Setup
- **Model**: Simple CNN (~1070986 params)
- **Dataset**: CIFAR-10 (50K train, 10K test)
- **Optimizer**: SGD, momentum=0.9, weight_decay=5e-4
- **Epochs**: 100, batch size 128
- **Seeds**: [42, 123, 777]
- **Device**: mps
- **Total time**: 7467s (124.4 min)

## LR Schedules
| Schedule | Description |
|----------|-------------|
| A. Step Decay | LR=0.1, drop 10x at epochs 30, 60, 80 |
| B. Cosine | Cosine annealing 0.1 -> 0.001 |
| C. Golden Ratio | LR = 0.1 * phi^(-epoch/20), phi=1.6180 |
| D. SB Noble | Fibonacci-timed drops, Fibonacci denominators |

## Test Accuracy at Checkpoints (mean +/- std)

| Schedule | Epoch 25 | Epoch 50 | Epoch 75 | Epoch 100 |
|----------|---------|---------|---------|---------|
| A. Step Decay | 69.25 +/- 0.68 | 78.92 +/- 0.09 | 80.79 +/- 0.27 | 81.35 +/- 0.20 |
| B. Cosine | 66.87 +/- 1.10 | 73.71 +/- 1.16 | 78.95 +/- 0.26 | 82.23 +/- 0.18 |
| C. Golden Ratio | 71.36 +/- 2.56 | 76.22 +/- 0.57 | 78.78 +/- 0.66 | 79.94 +/- 0.22 |
| D. SB Noble | 75.21 +/- 0.26 | 77.54 +/- 0.95 | 79.12 +/- 0.34 | 79.85 +/- 0.12 |

## Best Test Accuracy (any epoch)
| Schedule | Best Acc (mean) | Best Epoch | Final Acc (mean) |
|----------|----------------|------------|-----------------|
| A. Step Decay | 81.35% | 100 | 81.35% |
| B. Cosine | 82.23% | 100 | 82.23% |
| C. Golden Ratio | 80.65% | 90 | 79.94% |
| D. SB Noble | 80.09% | 91 | 79.85% |

## Convergence Smoothness
| Schedule | Mean |dLoss| | Std |dLoss| | Max |dLoss| | Acc Variance (last 20ep) |
|----------|-----------|----------|----------|--------------------------|
| A. Step Decay | 0.01419 | 0.04032 | 0.32541 | 0.049 |
| B. Cosine | 0.01403 | 0.03632 | 0.32776 | 0.088 |
| C. Golden Ratio | 0.01356 | 0.03740 | 0.32975 | 0.553 |
| D. SB Noble | 0.01363 | 0.04120 | 0.32541 | 0.291 |

## Training Time
| Schedule | Avg time/epoch (s) | Total (s) |
|----------|--------------------|-----------|
| A. Step Decay | 7.12 | 712 |
| B. Cosine | 6.15 | 615 |
| C. Golden Ratio | 4.59 | 459 |
| D. SB Noble | 4.53 | 453 |

## Analysis

### Final Accuracy Ranking
1. **B. Cosine**: 82.23% +/- 0.18
2. **A. Step Decay**: 81.35% +/- 0.20
3. **C. Golden Ratio**: 79.94% +/- 0.22
4. **D. SB Noble**: 79.85% +/- 0.12

### Key Question: Do golden ratio / SB schedules achieve comparable or better accuracy with smoother convergence?

**Result**: Standard schedules lead by 2.3% in final accuracy.

### Observations

- **Smoothest convergence**: C. Golden Ratio (mean |dLoss|=0.01356)
- **Roughest convergence**: A. Step Decay (mean |dLoss|=0.01419)
- Golden ratio schedule final: 79.94%, SB noble: 79.85%
- Step decay final: 81.35%, Cosine: 82.23%

### Figures
- `sb_lr_comparison.png` - Main comparison (accuracy, loss, LR curves, final bars)
- `sb_lr_smoothness.png` - Convergence smoothness and stability analysis