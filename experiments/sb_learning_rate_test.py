#!/usr/bin/env python3
"""
Stern-Brocot / Golden Ratio Learning Rate Schedules vs Standard Schedules on CIFAR-10.

Motivated by Matsubara & Yaguchi (AAAI 2025) showing 2-7x improvement for PINNs
using number-theoretic methods. The hypothesis: LR values at "noble" points
(related to golden ratio / Fibonacci) avoid destructive resonances with periodic
loss landscape structures.

Schedules tested:
  A. Step decay: LR=0.1, drop 10x at epochs 30, 60, 80
  B. Cosine annealing: 0.1 -> 0.001
  C. Golden ratio decay: LR = 0.1 * phi^(-epoch/20)
  D. Stern-Brocot noble: Fibonacci-timed LR drops with Fibonacci denominators
"""

import multiprocessing
multiprocessing.set_start_method('fork', force=True)

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import numpy as np
import time
import json
import os
import sys
import math
from collections import defaultdict

# ─── Config ───
TOTAL_EPOCHS = 100
BATCH_SIZE = 128
SEEDS = [42, 123, 777]
CHECKPOINT_EPOCHS = [25, 50, 75, 100]
DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
RESULTS_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")
PHI = (1 + math.sqrt(5)) / 2  # golden ratio ~1.618

print(f"Device: {DEVICE}")
print(f"PyTorch: {torch.__version__}")


# ─── Simple CNN (~100K params) ───
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(256, 10),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# ─── Data ───
def get_dataloaders():
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
    ])
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True, persistent_workers=True)
    testloader = torch.utils.data.DataLoader(testset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True, persistent_workers=True)
    return trainloader, testloader


# ─── LR Schedules ───

# Fibonacci numbers for SB schedule
FIBS = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
# Corresponding LR = 0.1 / fib_denom
FIB_DENOMS = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
# So LR sequence: 0.1, 0.1, 0.05, 0.0333, 0.02, 0.0125, 0.00769, 0.00476, 0.00294, 0.00182


def get_lr_step_decay(epoch):
    """Standard step decay: 0.1, drop 10x at 30, 60, 80."""
    lr = 0.1
    if epoch >= 80:
        lr *= 0.001
    elif epoch >= 60:
        lr *= 0.01
    elif epoch >= 30:
        lr *= 0.1
    return lr


def get_lr_cosine(epoch):
    """Cosine annealing from 0.1 to 0.001 over 100 epochs."""
    lr_min, lr_max = 0.001, 0.1
    return lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * epoch / TOTAL_EPOCHS))


def get_lr_golden(epoch):
    """Golden ratio exponential decay: 0.1 * phi^(-epoch/20)."""
    return 0.1 * PHI ** (-epoch / 20.0)


def get_lr_sb_noble(epoch):
    """Stern-Brocot noble schedule: switch LR at Fibonacci epoch boundaries."""
    # Find which Fibonacci interval we're in
    lr = 0.1  # initial
    for i, fib_epoch in enumerate(FIBS):
        if epoch >= fib_epoch and i < len(FIB_DENOMS):
            lr = 0.1 / FIB_DENOMS[i]
    # After last Fibonacci epoch (89), keep the last LR
    if epoch >= FIBS[-1]:
        lr = 0.1 / FIB_DENOMS[-1]
    return lr


SCHEDULES = {
    "A_step_decay": get_lr_step_decay,
    "B_cosine": get_lr_cosine,
    "C_golden_ratio": get_lr_golden,
    "D_sb_noble": get_lr_sb_noble,
}


# ─── Training ───
def train_one_epoch(model, trainloader, optimizer, criterion):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in trainloader:
        inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
    return total_loss / total, 100.0 * correct / total


def evaluate(model, testloader, criterion):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in testloader:
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            total_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    return total_loss / total, 100.0 * correct / total


def run_experiment(schedule_name, lr_fn, seed, trainloader, testloader):
    """Run a single training experiment."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    if DEVICE.type == "mps":
        torch.mps.manual_seed(seed)

    model = SimpleCNN().to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4)

    history = {
        "train_loss": [],
        "train_acc": [],
        "test_loss": [],
        "test_acc": [],
        "lr": [],
        "epoch_time": [],
    }

    for epoch in range(TOTAL_EPOCHS):
        # Set LR
        lr = lr_fn(epoch)
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr

        t0 = time.time()
        train_loss, train_acc = train_one_epoch(model, trainloader, optimizer, criterion)
        epoch_time = time.time() - t0

        test_loss, test_acc = evaluate(model, testloader, criterion)

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_loss"].append(test_loss)
        history["test_acc"].append(test_acc)
        history["lr"].append(lr)
        history["epoch_time"].append(epoch_time)

        if (epoch + 1) in CHECKPOINT_EPOCHS or (epoch + 1) % 25 == 0:
            print(f"  [{schedule_name}] seed={seed} epoch={epoch+1:3d}  "
                  f"lr={lr:.6f}  train_loss={train_loss:.4f}  "
                  f"test_acc={test_acc:.2f}%  ({epoch_time:.1f}s)")

    return history


# ─── Plotting ───
def plot_results(all_results):
    """Generate comparison plots."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    colors = {
        "A_step_decay": "#1f77b4",
        "B_cosine": "#ff7f0e",
        "C_golden_ratio": "#2ca02c",
        "D_sb_noble": "#d62728",
    }
    labels = {
        "A_step_decay": "Step Decay",
        "B_cosine": "Cosine Annealing",
        "C_golden_ratio": "Golden Ratio",
        "D_sb_noble": "SB Noble (Fibonacci)",
    }

    epochs = np.arange(1, TOTAL_EPOCHS + 1)

    # --- Figure 1: Test Accuracy ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Test accuracy curves (mean +/- std)
    ax = axes[0, 0]
    for sched in SCHEDULES:
        accs = np.array([all_results[sched][s]["test_acc"] for s in SEEDS])
        mean = accs.mean(axis=0)
        std = accs.std(axis=0)
        ax.plot(epochs, mean, color=colors[sched], label=labels[sched], linewidth=1.5)
        ax.fill_between(epochs, mean - std, mean + std, color=colors[sched], alpha=0.15)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Test Accuracy (%)")
    ax.set_title("Test Accuracy (mean +/- std over 3 seeds)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Training loss curves
    ax = axes[0, 1]
    for sched in SCHEDULES:
        losses = np.array([all_results[sched][s]["train_loss"] for s in SEEDS])
        mean = losses.mean(axis=0)
        std = losses.std(axis=0)
        ax.plot(epochs, mean, color=colors[sched], label=labels[sched], linewidth=1.5)
        ax.fill_between(epochs, mean - std, mean + std, color=colors[sched], alpha=0.15)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Training Loss")
    ax.set_title("Training Loss (mean +/- std)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # LR schedules
    ax = axes[1, 0]
    for sched in SCHEDULES:
        lrs = [SCHEDULES[sched](e) for e in range(TOTAL_EPOCHS)]
        ax.plot(epochs, lrs, color=colors[sched], label=labels[sched], linewidth=2)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Learning Rate")
    ax.set_title("Learning Rate Schedules")
    ax.set_yscale("log")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Bar chart: final test accuracy comparison
    ax = axes[1, 1]
    x_pos = np.arange(len(SCHEDULES))
    means = []
    stds = []
    sched_list = list(SCHEDULES.keys())
    for sched in sched_list:
        final_accs = [all_results[sched][s]["test_acc"][-1] for s in SEEDS]
        means.append(np.mean(final_accs))
        stds.append(np.std(final_accs))
    bars = ax.bar(x_pos, means, yerr=stds, capsize=5,
                  color=[colors[s] for s in sched_list], alpha=0.8)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([labels[s] for s in sched_list], rotation=15, fontsize=9)
    ax.set_ylabel("Final Test Accuracy (%)")
    ax.set_title("Final Accuracy (epoch 100)")
    ax.grid(True, alpha=0.3, axis='y')
    # Add value labels on bars
    for bar, m, s in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + s + 0.2,
                f'{m:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.suptitle("Stern-Brocot / Golden Ratio LR Schedules vs Standard (CIFAR-10, Simple CNN)",
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "sb_lr_comparison.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved sb_lr_comparison.png")

    # --- Figure 2: Convergence smoothness analysis ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Loss gradient magnitude (smoothness proxy)
    ax = axes[0]
    for sched in SCHEDULES:
        losses = np.array([all_results[sched][s]["train_loss"] for s in SEEDS]).mean(axis=0)
        diffs = np.abs(np.diff(losses))
        ax.plot(epochs[1:], diffs, color=colors[sched], label=labels[sched], linewidth=1.2, alpha=0.8)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("|dLoss/dEpoch|")
    ax.set_title("Loss Change Magnitude (smoothness proxy)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_yscale("log")

    # Test accuracy variance across seeds
    ax = axes[1]
    for sched in SCHEDULES:
        accs = np.array([all_results[sched][s]["test_acc"] for s in SEEDS])
        var = accs.var(axis=0)
        ax.plot(epochs, var, color=colors[sched], label=labels[sched], linewidth=1.2)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Variance across seeds")
    ax.set_title("Test Accuracy Variance (stability)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.suptitle("Convergence Smoothness & Stability Analysis",
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "sb_lr_smoothness.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved sb_lr_smoothness.png")


# ─── Results Report ───
def generate_report(all_results, total_time):
    """Generate markdown report."""
    lines = []
    lines.append("# Stern-Brocot / Golden Ratio LR Schedule Experiment Results")
    lines.append("")
    lines.append("## Setup")
    lines.append(f"- **Model**: Simple CNN (~{count_params(SimpleCNN())} params)")
    lines.append(f"- **Dataset**: CIFAR-10 (50K train, 10K test)")
    lines.append(f"- **Optimizer**: SGD, momentum=0.9, weight_decay=5e-4")
    lines.append(f"- **Epochs**: {TOTAL_EPOCHS}, batch size {BATCH_SIZE}")
    lines.append(f"- **Seeds**: {SEEDS}")
    lines.append(f"- **Device**: {DEVICE}")
    lines.append(f"- **Total time**: {total_time:.0f}s ({total_time/60:.1f} min)")
    lines.append("")

    lines.append("## LR Schedules")
    lines.append("| Schedule | Description |")
    lines.append("|----------|-------------|")
    lines.append("| A. Step Decay | LR=0.1, drop 10x at epochs 30, 60, 80 |")
    lines.append("| B. Cosine | Cosine annealing 0.1 -> 0.001 |")
    lines.append(f"| C. Golden Ratio | LR = 0.1 * phi^(-epoch/20), phi={PHI:.4f} |")
    lines.append("| D. SB Noble | Fibonacci-timed drops, Fibonacci denominators |")
    lines.append("")

    # Checkpoint table
    lines.append("## Test Accuracy at Checkpoints (mean +/- std)")
    lines.append("")
    header = "| Schedule |"
    sep = "|----------|"
    for ep in CHECKPOINT_EPOCHS:
        header += f" Epoch {ep} |"
        sep += "---------|"
    lines.append(header)
    lines.append(sep)

    sched_labels = {
        "A_step_decay": "A. Step Decay",
        "B_cosine": "B. Cosine",
        "C_golden_ratio": "C. Golden Ratio",
        "D_sb_noble": "D. SB Noble",
    }

    for sched in SCHEDULES:
        row = f"| {sched_labels[sched]} |"
        for ep in CHECKPOINT_EPOCHS:
            accs = [all_results[sched][s]["test_acc"][ep - 1] for s in SEEDS]
            mean = np.mean(accs)
            std = np.std(accs)
            row += f" {mean:.2f} +/- {std:.2f} |"
        lines.append(row)
    lines.append("")

    # Best accuracy
    lines.append("## Best Test Accuracy (any epoch)")
    lines.append("| Schedule | Best Acc (mean) | Best Epoch | Final Acc (mean) |")
    lines.append("|----------|----------------|------------|-----------------|")
    for sched in SCHEDULES:
        # Mean curve
        accs = np.array([all_results[sched][s]["test_acc"] for s in SEEDS])
        mean_curve = accs.mean(axis=0)
        best_epoch = np.argmax(mean_curve) + 1
        best_acc = mean_curve.max()
        final_acc = mean_curve[-1]
        lines.append(f"| {sched_labels[sched]} | {best_acc:.2f}% | {best_epoch} | {final_acc:.2f}% |")
    lines.append("")

    # Smoothness metrics
    lines.append("## Convergence Smoothness")
    lines.append("| Schedule | Mean |dLoss| | Std |dLoss| | Max |dLoss| | Acc Variance (last 20ep) |")
    lines.append("|----------|-----------|----------|----------|--------------------------|")
    for sched in SCHEDULES:
        losses = np.array([all_results[sched][s]["train_loss"] for s in SEEDS]).mean(axis=0)
        diffs = np.abs(np.diff(losses))
        accs = np.array([all_results[sched][s]["test_acc"] for s in SEEDS])
        late_var = accs[:, -20:].var(axis=0).mean()
        lines.append(f"| {sched_labels[sched]} | {diffs.mean():.5f} | {diffs.std():.5f} | {diffs.max():.5f} | {late_var:.3f} |")
    lines.append("")

    # Timing
    lines.append("## Training Time")
    lines.append("| Schedule | Avg time/epoch (s) | Total (s) |")
    lines.append("|----------|--------------------|-----------|")
    for sched in SCHEDULES:
        times = []
        for s in SEEDS:
            times.extend(all_results[sched][s]["epoch_time"])
        avg = np.mean(times)
        total = np.sum(times) / len(SEEDS)
        lines.append(f"| {sched_labels[sched]} | {avg:.2f} | {total:.0f} |")
    lines.append("")

    # Analysis
    lines.append("## Analysis")
    lines.append("")

    # Determine winner
    final_accs = {}
    for sched in SCHEDULES:
        accs = [all_results[sched][s]["test_acc"][-1] for s in SEEDS]
        final_accs[sched] = (np.mean(accs), np.std(accs))

    ranked = sorted(final_accs.items(), key=lambda x: -x[1][0])
    lines.append("### Final Accuracy Ranking")
    for i, (sched, (m, s)) in enumerate(ranked):
        lines.append(f"{i+1}. **{sched_labels[sched]}**: {m:.2f}% +/- {s:.2f}")
    lines.append("")

    # Key question
    lines.append("### Key Question: Do golden ratio / SB schedules achieve comparable or better accuracy with smoother convergence?")
    lines.append("")

    golden_acc = final_accs["C_golden_ratio"][0]
    sb_acc = final_accs["D_sb_noble"][0]
    step_acc = final_accs["A_step_decay"][0]
    cos_acc = final_accs["B_cosine"][0]
    best_standard = max(step_acc, cos_acc)
    best_novel = max(golden_acc, sb_acc)

    if best_novel >= best_standard - 0.5:
        lines.append("**Result**: The number-theoretic schedules achieve **comparable** accuracy to standard schedules.")
    elif best_novel > best_standard:
        lines.append("**Result**: The number-theoretic schedules **outperform** standard schedules!")
    else:
        gap = best_standard - best_novel
        lines.append(f"**Result**: Standard schedules lead by {gap:.1f}% in final accuracy.")

    lines.append("")
    lines.append("### Observations")
    lines.append("")

    # Auto-generate observations based on data
    losses_smoothness = {}
    for sched in SCHEDULES:
        losses = np.array([all_results[sched][s]["train_loss"] for s in SEEDS]).mean(axis=0)
        diffs = np.abs(np.diff(losses))
        losses_smoothness[sched] = diffs.mean()

    smoothest = min(losses_smoothness, key=losses_smoothness.get)
    roughest = max(losses_smoothness, key=losses_smoothness.get)
    lines.append(f"- **Smoothest convergence**: {sched_labels[smoothest]} (mean |dLoss|={losses_smoothness[smoothest]:.5f})")
    lines.append(f"- **Roughest convergence**: {sched_labels[roughest]} (mean |dLoss|={losses_smoothness[roughest]:.5f})")
    lines.append(f"- Golden ratio schedule final: {golden_acc:.2f}%, SB noble: {sb_acc:.2f}%")
    lines.append(f"- Step decay final: {step_acc:.2f}%, Cosine: {cos_acc:.2f}%")
    lines.append("")
    lines.append("### Figures")
    lines.append("- `sb_lr_comparison.png` - Main comparison (accuracy, loss, LR curves, final bars)")
    lines.append("- `sb_lr_smoothness.png` - Convergence smoothness and stability analysis")

    report = "\n".join(lines)
    report_path = os.path.join(RESULTS_DIR, "SB_LR_RESULTS.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Report saved to {report_path}")
    return report


# ─── Main ───
def main():
    print("=" * 70)
    print("Stern-Brocot / Golden Ratio LR Schedule Experiment")
    print("=" * 70)

    # Print LR schedule preview
    print("\nLR Schedule Preview (first 10 epochs + key epochs):")
    preview_epochs = list(range(10)) + [25, 30, 50, 60, 75, 80, 89, 99]
    print(f"{'Epoch':>6} {'Step':>10} {'Cosine':>10} {'Golden':>10} {'SB Noble':>10}")
    for e in preview_epochs:
        print(f"{e:>6d} {get_lr_step_decay(e):>10.6f} {get_lr_cosine(e):>10.6f} "
              f"{get_lr_golden(e):>10.6f} {get_lr_sb_noble(e):>10.6f}")

    # Count params
    m = SimpleCNN()
    print(f"\nModel params: {count_params(m):,}")

    # Load data
    print("\nLoading CIFAR-10...")
    trainloader, testloader = get_dataloaders()

    # Run all experiments
    all_results = defaultdict(dict)
    t_total = time.time()

    total_runs = len(SCHEDULES) * len(SEEDS)
    run_idx = 0

    for sched_name, lr_fn in SCHEDULES.items():
        for seed in SEEDS:
            run_idx += 1
            print(f"\n--- Run {run_idx}/{total_runs}: {sched_name}, seed={seed} ---")
            t_run = time.time()
            history = run_experiment(sched_name, lr_fn, seed, trainloader, testloader)
            elapsed = time.time() - t_run
            all_results[sched_name][seed] = history
            print(f"  Done in {elapsed:.1f}s. Final test acc: {history['test_acc'][-1]:.2f}%")

    total_time = time.time() - t_total
    print(f"\n{'=' * 70}")
    print(f"All {total_runs} runs completed in {total_time:.0f}s ({total_time/60:.1f} min)")

    # Save raw results as JSON (convert numpy to native Python types)
    raw_path = os.path.join(RESULTS_DIR, "sb_lr_raw_results.json")
    json_results = {}
    for sched in all_results:
        json_results[sched] = {}
        for seed in all_results[sched]:
            json_results[sched][str(seed)] = {
                k: [float(v) for v in vals] for k, vals in all_results[sched][seed].items()
            }
    with open(raw_path, "w") as f:
        json.dump(json_results, f, indent=2)
    print(f"Raw results saved to {raw_path}")

    # Plots
    print("\nGenerating plots...")
    plot_results(all_results)

    # Report
    print("\nGenerating report...")
    report = generate_report(all_results, total_time)
    print("\n" + report)


if __name__ == "__main__":
    main()
