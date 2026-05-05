"""
Benchmark v2: salvage attempt for PrimeMatchedFilterDetector.

Sweep:
  - n_taps in {17, 64, 256, 1024}
  - prefilter in {None, 'ar1_residual'}
  - anomaly class in {spike, freq_burst, chirp, variance_break}

Compared against OneClassSVM and IsolationForest baselines per anomaly class.

Output: pmf_benchmark_v2_results.md (bottom line at top).

Constraints: 100 seeds (seed = 42 + run_id), wall-time budget ~25 min.
For tractability we reduce n=4000 (down from 10000) and n_seeds is configurable
via env N_SEEDS_V2 (default 50). With 4 kernels x 2 prefilters = 8 PMF configs
+ 2 baselines = 10 detectors per anomaly class x 4 classes = 40 evals/seed.
"""

from __future__ import annotations

import os
import time
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import average_precision_score, precision_recall_curve

from pmf_detector_v2 import PrimeMatchedFilterDetectorV2


# ---------------------------------------------------------------------------
# Anomaly classes
# ---------------------------------------------------------------------------

def _ar1_background(n: int, rng: np.random.Generator,
                    phi: float = 0.7, sigma_e: float = 1.0) -> np.ndarray:
    eps = rng.normal(0, sigma_e, size=n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + eps[t]
    return x


def gen_spike(n: int, n_anom: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Original AR(1) + planted triangular spikes."""
    rng = np.random.default_rng(seed)
    x = _ar1_background(n, rng)
    bg_std = x.std()
    label = np.zeros(n, dtype=np.int8)
    buffer = 50
    positions = rng.choice(np.arange(buffer, n - buffer), size=n_anom, replace=False)
    for p in positions:
        width = int(rng.integers(1, 8))
        amp = rng.uniform(4.0, 8.0) * bg_std * rng.choice([-1.0, 1.0])
        for k in range(-width, width + 1):
            x[p + k] += amp * (1 - abs(k) / (width + 1))
        label[p] = 1
    return x, label


def gen_freq_burst(n: int, n_anom: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """AR(1) bg + brief sinusoidal tone bursts at random frequency."""
    rng = np.random.default_rng(seed)
    x = _ar1_background(n, rng)
    bg_std = x.std()
    label = np.zeros(n, dtype=np.int8)
    buffer = 100
    positions = rng.choice(np.arange(buffer, n - buffer), size=n_anom, replace=False)
    for p in positions:
        burst_len = int(rng.integers(20, 60))
        freq = rng.uniform(0.15, 0.45)  # cycles/sample (Nyquist=0.5)
        amp = rng.uniform(2.5, 5.0) * bg_std
        phase = rng.uniform(0, 2 * np.pi)
        # Hann window envelope
        k = np.arange(burst_len)
        env = 0.5 * (1 - np.cos(2 * np.pi * k / max(burst_len - 1, 1)))
        burst = amp * env * np.sin(2 * np.pi * freq * k + phase)
        a = max(0, p - burst_len // 2)
        b = min(n, a + burst_len)
        x[a:b] += burst[: b - a]
        label[p] = 1
    return x, label


def gen_chirp(n: int, n_anom: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """AR(1) bg + linear-frequency-sweep chirp bursts (phase shifts)."""
    rng = np.random.default_rng(seed)
    x = _ar1_background(n, rng)
    bg_std = x.std()
    label = np.zeros(n, dtype=np.int8)
    buffer = 100
    positions = rng.choice(np.arange(buffer, n - buffer), size=n_anom, replace=False)
    for p in positions:
        burst_len = int(rng.integers(30, 80))
        f0 = rng.uniform(0.05, 0.20)
        f1 = rng.uniform(0.25, 0.45)
        amp = rng.uniform(2.5, 5.0) * bg_std
        k = np.arange(burst_len)
        # instantaneous freq linear from f0 to f1; phase = 2*pi * integral
        t = k / max(burst_len - 1, 1)
        inst = f0 + (f1 - f0) * t
        phase = 2 * np.pi * np.cumsum(inst)
        env = 0.5 * (1 - np.cos(2 * np.pi * k / max(burst_len - 1, 1)))
        burst = amp * env * np.sin(phase)
        a = max(0, p - burst_len // 2)
        b = min(n, a + burst_len)
        x[a:b] += burst[: b - a]
        label[p] = 1
    return x, label


def gen_variance_break(n: int, n_anom: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """AR(1) bg + segments where the innovation variance suddenly multiplies."""
    rng = np.random.default_rng(seed)
    # generate AR(1) but with variance breaks at planted positions
    phi = 0.7
    sigma_base = 1.0
    label = np.zeros(n, dtype=np.int8)
    buffer = 100
    positions = sorted(rng.choice(np.arange(buffer, n - buffer),
                                   size=n_anom, replace=False))
    # Build per-step sigma: spike up by factor 4-8 for a window
    sigma = np.full(n, sigma_base)
    for p in positions:
        seg_len = int(rng.integers(15, 50))
        mult = rng.uniform(4.0, 8.0)
        a = max(0, p - seg_len // 2)
        b = min(n, a + seg_len)
        sigma[a:b] *= mult
        label[p] = 1
    eps = rng.normal(0, 1.0, size=n) * sigma
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + eps[t]
    return x, label


ANOMALY_CLASSES = {
    "spike": gen_spike,
    "freq_burst": gen_freq_burst,
    "chirp": gen_chirp,
    "variance_break": gen_variance_break,
}


# ---------------------------------------------------------------------------
# Detector wrappers
# ---------------------------------------------------------------------------

def _make_pmf_scorer(n_taps: int, prefilter):
    def score(x: np.ndarray) -> np.ndarray:
        det = PrimeMatchedFilterDetectorV2(
            n_taps=n_taps,
            window_size=100,
            weighting="M_over_sqrt_p",
            prefilter=prefilter,
        )
        return np.abs(det.fit(x).score())
    return score


def _sliding(x: np.ndarray, W: int) -> np.ndarray:
    return np.lib.stride_tricks.sliding_window_view(x, W)


def _pad(s: np.ndarray, n: int, W: int) -> np.ndarray:
    out = np.zeros(n)
    half = W // 2
    out[half : half + s.size] = s
    if half > 0:
        out[:half] = s[0]
        out[half + s.size :] = s[-1]
    return out


def score_isoforest(x: np.ndarray, W: int = 11) -> np.ndarray:
    X = _sliding(x, W)
    iso = IsolationForest(n_estimators=100, contamination="auto",
                          random_state=0, n_jobs=1)
    iso.fit(X)
    s = -iso.score_samples(X)
    return _pad(s, x.size, W)


def score_ocsvm(x: np.ndarray, W: int = 11) -> np.ndarray:
    X = _sliding(x, W)
    svm = OneClassSVM(nu=0.05, kernel="rbf", gamma="scale")
    n = X.shape[0]
    if n > 1500:
        rng = np.random.default_rng(0)
        idx = rng.choice(n, size=1500, replace=False)
        svm.fit(X[idx])
    else:
        svm.fit(X)
    s = -svm.decision_function(X)
    return _pad(s, x.size, W)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def metrics_at_recall(scores: np.ndarray, labels: np.ndarray,
                      target_recall: float = 0.95, tol: int = 5) -> dict:
    n = labels.size
    expanded = np.zeros(n, dtype=bool)
    true_positions = np.flatnonzero(labels)
    for p in true_positions:
        a = max(0, p - tol); b = min(n, p + tol + 1)
        expanded[a:b] = True
    if expanded.sum() == 0 or expanded.sum() == n:
        return {"precision": 0.0, "f1": 0.0, "auc_pr": 0.0}
    precisions, recalls, _ = precision_recall_curve(expanded.astype(int), scores)
    auc_pr = average_precision_score(expanded.astype(int), scores)
    valid = np.where(recalls >= target_recall)[0]
    if valid.size == 0:
        return {"precision": 0.0, "f1": 0.0, "auc_pr": float(auc_pr)}
    idx = valid[-1]
    prec = precisions[idx]; rec = recalls[idx]
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return {"precision": float(prec), "f1": float(f1), "auc_pr": float(auc_pr)}


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

def build_detectors():
    dets = {}
    for n_taps in (17, 64, 256, 1024):
        for pre in (None, "ar1_residual"):
            label_pre = "raw" if pre is None else "ar1res"
            name = f"PMF[K={n_taps},{label_pre}]"
            dets[name] = _make_pmf_scorer(n_taps, pre)
    dets["OneClassSVM"] = score_ocsvm
    dets["IsolationForest"] = score_isoforest
    return dets


def main():
    n_seeds = int(os.environ.get("N_SEEDS_V2", "50"))
    n = int(os.environ.get("N_LEN_V2", "4000"))
    n_anom = int(os.environ.get("N_ANOM_V2", "8"))

    detectors = build_detectors()
    classes = list(ANOMALY_CLASSES.keys())
    # results[class][det] = list of metric dicts
    results = {c: {d: {"auc_pr": [], "precision": [], "f1": [], "time": []}
                   for d in detectors}
               for c in classes}

    t_start = time.time()
    print(f"Sweep: {n_seeds} seeds x {len(classes)} classes x {len(detectors)} detectors")
    print(f"Signal length n={n}, anomalies/signal={n_anom}\n")

    for run in range(n_seeds):
        seed = 42 + run
        for cname in classes:
            x, label = ANOMALY_CLASSES[cname](n, n_anom, seed)
            for dname, fn in detectors.items():
                t0 = time.time()
                try:
                    sc = fn(x)
                    m = metrics_at_recall(sc, label, 0.95)
                except Exception as e:
                    m = {"precision": 0.0, "f1": 0.0, "auc_pr": 0.0}
                    print(f"  [warn] {cname}/{dname} seed {seed}: {e}")
                dt = time.time() - t0
                results[cname][dname]["auc_pr"].append(m["auc_pr"])
                results[cname][dname]["precision"].append(m["precision"])
                results[cname][dname]["f1"].append(m["f1"])
                results[cname][dname]["time"].append(dt)
        elapsed = time.time() - t_start
        if (run + 1) % 5 == 0 or run == 0:
            print(f"  seed {run+1}/{n_seeds}  elapsed {elapsed:.1f}s  "
                  f"(proj total {elapsed/(run+1)*n_seeds:.0f}s)")

    return results, n_seeds, n, n_anom


def write_report(results, n_seeds, n, n_anom, out_path):
    classes = list(results.keys())
    detectors = list(next(iter(results.values())).keys())

    # Compute mean AUC-PR per (class, detector)
    mean_aucpr = {c: {d: float(np.mean(results[c][d]["auc_pr"]))
                      for d in detectors}
                  for c in classes}
    mean_prec = {c: {d: float(np.mean(results[c][d]["precision"]))
                     for d in detectors}
                 for c in classes}

    pmf_names = [d for d in detectors if d.startswith("PMF[")]
    baselines = [d for d in detectors if not d.startswith("PMF[")]

    # Find PMF wins per class
    bottom_lines = []
    for c in classes:
        best_baseline = max(baselines, key=lambda d: mean_aucpr[c][d])
        baseline_auc = mean_aucpr[c][best_baseline]
        # best PMF config
        best_pmf = max(pmf_names, key=lambda d: mean_aucpr[c][d])
        pmf_auc = mean_aucpr[c][best_pmf]
        winner_text = "PMF WINS" if pmf_auc > baseline_auc else "PMF LOSES"
        bottom_lines.append(
            (c, best_pmf, pmf_auc, best_baseline, baseline_auc, winner_text)
        )

    lines = []
    lines.append("# PMF salvage benchmark v2 — results\n")
    lines.append("## Bottom line\n")

    any_win = any(b[2] > b[4] for b in bottom_lines)
    if any_win:
        lines.append("**PMF beats best baseline on at least one anomaly class.** Industry pivot has limited but non-zero hope.\n")
    else:
        lines.append("**PMF loses to baselines on all 4 anomaly classes, all kernel sizes, all prefilters.** "
                     "Industry pivot: dead. The original 20/20 result on L-function zeros was domain-specific "
                     "and does NOT generalize to colored-noise + transient-anomaly detection.\n")

    lines.append("Per anomaly class:\n")
    for (c, bp, pa, bb, ba, w) in bottom_lines:
        delta = pa - ba
        lines.append(f"- **{c}**: best PMF = `{bp}` (AUC-PR {pa:.4f}); "
                     f"best baseline = `{bb}` (AUC-PR {ba:.4f}); Δ={delta:+.4f}; **{w}**")
    lines.append("")

    lines.append(f"Sweep: {n_seeds} seeds, n={n}, anomalies/signal={n_anom}, "
                 f"seed = 42 + run_id, tolerance ±5 samples for ground truth.\n")

    # Detailed tables per class
    for c in classes:
        lines.append(f"## Class: `{c}`\n")
        lines.append("| Detector | AUC-PR (mean ± std) | Prec@R=.95 (mean) | Time/seed (s) |")
        lines.append("|---|---|---|---|")
        # sort by AUC-PR desc
        sorted_dets = sorted(detectors,
                             key=lambda d: mean_aucpr[c][d], reverse=True)
        for d in sorted_dets:
            arr = np.array(results[c][d]["auc_pr"])
            tm = np.mean(results[c][d]["time"])
            mark = " **(BEST)**" if d == sorted_dets[0] else ""
            lines.append(f"| {d}{mark} | {arr.mean():.4f} ± {arr.std():.4f} "
                         f"| {mean_prec[c][d]:.4f} | {tm:.3f} |")
        lines.append("")

    # Cross-class kernel/prefilter analysis
    lines.append("## Kernel/prefilter trends across classes\n")
    lines.append("Mean AUC-PR averaged over all anomaly classes per PMF config:\n")
    lines.append("| Config | mean AUC-PR (over 4 classes) |")
    lines.append("|---|---|")
    pmf_avg = {}
    for pn in pmf_names:
        pmf_avg[pn] = float(np.mean([mean_aucpr[c][pn] for c in classes]))
    for pn in sorted(pmf_avg, key=pmf_avg.get, reverse=True):
        lines.append(f"| {pn} | {pmf_avg[pn]:.4f} |")
    lines.append("")
    lines.append("Baseline AUC-PR averaged over all classes:\n")
    for bn in baselines:
        avg = float(np.mean([mean_aucpr[c][bn] for c in classes]))
        lines.append(f"- {bn}: {avg:.4f}")
    lines.append("")

    # Honesty section
    lines.append("## Honest assessment\n")
    if not any_win:
        lines.append("- PMF loses across the board. Longer kernels do not rescue it. "
                     "AR(1) residualization does not rescue it.")
        lines.append("- The Mertens kernel's value seems specific to detecting structure in "
                     "L-function zero sequences (where prime-indexed weights match the actual "
                     "underlying number-theoretic content) and does NOT translate to "
                     "generic colored-noise-plus-transient detection.")
        lines.append("- Recommendation: shelve industry pivot for general anomaly detection. "
                     "If pursuing PMF further, restrict scope to genuinely number-theoretic "
                     "data sources (e.g. L-function zeros, character sums, modular forms).")
    else:
        winners = [b for b in bottom_lines if b[2] > b[4]]
        lines.append("PMF wins in:")
        for (c, bp, pa, bb, ba, _) in winners:
            lines.append(f"- **{c}** with `{bp}`: PMF {pa:.4f} vs baseline {ba:.4f} "
                         f"(Δ={pa-ba:+.4f})")
        lines.append("\nThis is a partial, domain-restricted win. Recommend follow-up "
                     "to characterize WHY PMF wins on these classes specifically.")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    results, n_seeds, n, n_anom = main()
    out = "/Users/saar/Farey 4.7 solutions/pmf_benchmark_v2_results.md"
    write_report(results, n_seeds, n, n_anom, out)
