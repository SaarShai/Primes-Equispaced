"""
Benchmark: PrimeMatchedFilterDetector vs IsolationForest, OneClassSVM,
rolling z-score, Hampel filter.

Synthetic 1D AR(1) background with planted spike-anomalies of varying width,
amplitude, and sign. 100 random seeds. Reports precision @ recall=0.95,
AUC-PR, F1 at recall=0.95, detection latency, false alarm rate.

Run:  python pmf_benchmark.py
"""

from __future__ import annotations

import os
import time
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import average_precision_score, precision_recall_curve

from pmf_detector import PrimeMatchedFilterDetector


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------
def generate_signal(n: int, n_anom: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """AR(1) background + planted anomalies. Returns (x, label_mask)."""
    rng = np.random.default_rng(seed)
    # AR(1): x_t = phi*x_{t-1} + eps_t
    phi = 0.7
    sigma_e = 1.0
    eps = rng.normal(0, sigma_e, size=n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + eps[t]

    # Plant anomalies: structured spikes (varying width 1-7, amp 4-8 sigma, sign +/-)
    bg_std = x.std()
    label = np.zeros(n, dtype=np.int8)
    # Reserve buffer near edges so spikes don't fall off
    buffer = 50
    positions = rng.choice(np.arange(buffer, n - buffer), size=n_anom, replace=False)
    for p in positions:
        width = int(rng.integers(1, 8))
        amp = rng.uniform(4.0, 8.0) * bg_std * rng.choice([-1.0, 1.0])
        # Triangular bump of given half-width
        for k in range(-width, width + 1):
            x[p + k] += amp * (1 - abs(k) / (width + 1))
        # Mark just the centre as ground truth (point-anomaly convention)
        label[p] = 1
    return x, label


# ---------------------------------------------------------------------------
# Detector wrappers: each returns a per-sample score (higher = more anomalous)
# ---------------------------------------------------------------------------
def score_pmf(x: np.ndarray) -> np.ndarray:
    det = PrimeMatchedFilterDetector(n_taps=17, window_size=100, weighting="M_over_sqrt_p")
    z = det.fit(x).score()
    return np.abs(z)


def score_pmf_baseline_Rp(x: np.ndarray) -> np.ndarray:
    """Ablation: same architecture but 1/sqrt(p) weights (no Mertens)."""
    det = PrimeMatchedFilterDetector(n_taps=17, window_size=100, weighting="R_p")
    z = det.fit(x).score()
    return np.abs(z)


def score_isoforest(x: np.ndarray) -> np.ndarray:
    # Use a small temporal context window as features (otherwise IF sees only x)
    W = 11
    X = sliding_window_features(x, W)
    iso = IsolationForest(n_estimators=100, contamination="auto", random_state=0, n_jobs=1)
    iso.fit(X)
    s = -iso.score_samples(X)  # higher = more anomalous
    return pad_to_length(s, x.size, W)


def score_ocsvm(x: np.ndarray) -> np.ndarray:
    W = 11
    X = sliding_window_features(x, W)
    # nu controls the upper bound on outlier fraction; pick a small value
    svm = OneClassSVM(nu=0.05, kernel="rbf", gamma="scale")
    # Subsample for speed: OneClassSVM is O(n^2)
    n = X.shape[0]
    if n > 2000:
        rng = np.random.default_rng(0)
        idx = rng.choice(n, size=2000, replace=False)
        svm.fit(X[idx])
    else:
        svm.fit(X)
    s = -svm.decision_function(X)
    return pad_to_length(s, x.size, W)


def score_zscore(x: np.ndarray, window: int = 100) -> np.ndarray:
    """Vanilla rolling z-score on raw signal."""
    from pmf_detector import _rolling_mean_std
    mu, sigma = _rolling_mean_std(x, window)
    return np.abs((x - mu) / np.maximum(sigma, 1e-12))


def score_hampel(x: np.ndarray, window: int = 11, k: float = 1.4826) -> np.ndarray:
    """Hampel filter score: |x - rolling_median| / (k * rolling_MAD)."""
    n = x.size
    half = window // 2
    med = np.zeros(n)
    mad = np.zeros(n)
    for i in range(n):
        a = max(0, i - half)
        b = min(n, i + half + 1)
        seg = x[a:b]
        m = np.median(seg)
        med[i] = m
        mad[i] = np.median(np.abs(seg - m))
    return np.abs(x - med) / np.maximum(k * mad, 1e-12)


def sliding_window_features(x: np.ndarray, W: int) -> np.ndarray:
    """Stack length-W windows; output shape (n - W + 1, W)."""
    return np.lib.stride_tricks.sliding_window_view(x, W)


def pad_to_length(s: np.ndarray, n: int, W: int) -> np.ndarray:
    """Pad a length-(n-W+1) score back to n by mirroring edges."""
    out = np.zeros(n)
    half = W // 2
    out[half : half + s.size] = s
    if half > 0:
        out[:half] = s[0]
        out[half + s.size :] = s[-1]
    return out


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def metrics_at_recall(scores: np.ndarray, labels: np.ndarray, target_recall: float = 0.95):
    """Return precision, F1, FPR at the threshold giving >= target_recall.

    To handle 'detection within tolerance', we expand labels to a tolerance
    window (any point within +/- TOL of a true anomaly counts as a hit).
    """
    TOL = 5  # samples
    # Expand label mask
    n = labels.size
    expanded = np.zeros(n, dtype=bool)
    true_positions = np.flatnonzero(labels)
    for p in true_positions:
        a = max(0, p - TOL); b = min(n, p + TOL + 1)
        expanded[a:b] = True

    # Per-sample PR using expanded mask vs. score
    precisions, recalls, thresholds = precision_recall_curve(expanded.astype(int), scores)
    auc_pr = average_precision_score(expanded.astype(int), scores)

    # Find first index with recall >= target_recall (PR curve is in decreasing recall)
    valid = np.where(recalls >= target_recall)[0]
    if valid.size == 0:
        return {"precision": 0.0, "f1": 0.0, "fpr": 1.0, "auc_pr": auc_pr,
                "latency": np.nan}
    idx = valid[-1]  # highest precision among those meeting recall
    prec = precisions[idx]
    rec = recalls[idx]
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    # FPR at that threshold
    if idx < thresholds.size:
        thr = thresholds[idx]
    else:
        thr = thresholds[-1]
    pred = scores >= thr
    tn = np.sum((~pred) & (~expanded))
    fp = np.sum(pred & (~expanded))
    fpr = fp / max(1, fp + tn)

    # Latency: for each true anomaly, distance to nearest predicted positive
    latencies = []
    pred_idx = np.flatnonzero(pred)
    if pred_idx.size > 0:
        for p in true_positions:
            d = np.min(np.abs(pred_idx - p))
            latencies.append(d)
    latency = float(np.mean(latencies)) if latencies else np.nan

    return {"precision": float(prec), "f1": float(f1), "fpr": float(fpr),
            "auc_pr": float(auc_pr), "latency": latency}


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main(n_seeds: int = 100, n: int = 10_000, n_anom: int = 10):
    detectors = {
        "PrimeMatchedFilter (M/√p)": score_pmf,
        "PrimeMatchedFilter (1/√p) [ablation]": score_pmf_baseline_Rp,
        "IsolationForest (W=11)": score_isoforest,
        "OneClassSVM (W=11)": score_ocsvm,
        "Rolling z-score (W=100)": score_zscore,
        "Hampel filter (W=11)": score_hampel,
    }
    keys = list(detectors.keys())
    agg = {k: {"precision": [], "f1": [], "fpr": [], "auc_pr": [], "latency": [],
               "time": []} for k in keys}

    t_start = time.time()
    for run in range(n_seeds):
        seed = 42 + run
        x, label = generate_signal(n, n_anom, seed)
        for name, fn in detectors.items():
            t0 = time.time()
            try:
                scores = fn(x)
                m = metrics_at_recall(scores, label, 0.95)
            except Exception as e:
                m = {"precision": 0.0, "f1": 0.0, "fpr": 1.0, "auc_pr": 0.0,
                     "latency": np.nan}
                print(f"  [warn] {name} failed seed {seed}: {e}")
            dt = time.time() - t0
            for k, v in m.items():
                agg[name][k].append(v)
            agg[name]["time"].append(dt)
        if (run + 1) % 10 == 0:
            elapsed = time.time() - t_start
            print(f"  seed {run+1}/{n_seeds}  elapsed {elapsed:.1f}s")

    # Summarise
    print("\n=== Results (mean ± std over {} seeds) ===\n".format(n_seeds))
    header = f"{'Detector':<40s} {'Prec@R=.95':>12s} {'F1@R=.95':>12s} {'AUC-PR':>10s} {'FPR':>10s} {'Latency':>10s} {'Time(s)':>10s}"
    print(header)
    print("-" * len(header))
    rows = []
    for name in keys:
        a = agg[name]
        def ms(k):
            arr = np.array(a[k], dtype=float)
            arr = arr[~np.isnan(arr)]
            if arr.size == 0:
                return "n/a", "n/a"
            return f"{arr.mean():.4f}", f"{arr.std():.4f}"
        prec_m, prec_s = ms("precision")
        f1_m, f1_s = ms("f1")
        auc_m, auc_s = ms("auc_pr")
        fpr_m, _ = ms("fpr")
        lat_m, _ = ms("latency")
        t_m, _ = ms("time")
        line = f"{name:<40s} {prec_m:>12s} {f1_m:>12s} {auc_m:>10s} {fpr_m:>10s} {lat_m:>10s} {t_m:>10s}"
        print(line)
        rows.append((name, prec_m, prec_s, f1_m, f1_s, auc_m, auc_s, fpr_m, lat_m, t_m))

    return agg, rows


def write_report(agg: dict, rows: list, out_path: str, n_seeds: int, n: int, n_anom: int):
    # Determine winner by AUC-PR
    name_to_aucpr = {n_: float(np.nanmean(agg[n_]["auc_pr"])) for n_ in agg}
    sorted_by_aucpr = sorted(name_to_aucpr.items(), key=lambda kv: kv[1], reverse=True)
    winner = sorted_by_aucpr[0][0]
    pmf_name = "PrimeMatchedFilter (M/√p)"

    pmf_aucpr = name_to_aucpr[pmf_name]
    pmf_rank = [i for i, (n_, _) in enumerate(sorted_by_aucpr) if n_ == pmf_name][0] + 1

    # Precision @ R=0.95 winner
    name_to_prec = {n_: float(np.nanmean(agg[n_]["precision"])) for n_ in agg}
    sorted_by_prec = sorted(name_to_prec.items(), key=lambda kv: kv[1], reverse=True)
    pmf_prec_rank = [i for i, (n_, _) in enumerate(sorted_by_prec) if n_ == pmf_name][0] + 1

    lines = []
    lines.append("# PrimeMatchedFilterDetector benchmark\n")
    lines.append(f"- Seeds: {n_seeds}, signal length N={n}, planted anomalies per signal: {n_anom}")
    lines.append(f"- Background: AR(1), φ=0.7, σ_e=1.0")
    lines.append(f"- Anomalies: triangular bumps, width 1–7, amplitude 4–8σ_bg, random sign")
    lines.append(f"- Metrics computed with ±5-sample tolerance window for ground truth\n")

    lines.append("## Bottom line\n")
    if pmf_rank == 1:
        lines.append(f"**The prime-matched-filter detector wins on AUC-PR** "
                     f"(mean {pmf_aucpr:.4f}). Industry-relevance signal: positive.")
    else:
        lines.append(f"**The prime-matched-filter detector ranks #{pmf_rank} of "
                     f"{len(sorted_by_aucpr)} on AUC-PR** "
                     f"(mean {pmf_aucpr:.4f}). Top: {winner} "
                     f"({sorted_by_aucpr[0][1]:.4f}).")
    lines.append(f"On precision @ recall=0.95 it ranks #{pmf_prec_rank}.")
    lines.append("")

    lines.append("## Results table (mean over seeds)\n")
    lines.append("| Detector | Prec@R=0.95 | F1@R=0.95 | AUC-PR | FPR | Latency (samples) | Time/seed (s) |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} ± {r[2]} | {r[3]} ± {r[4]} | {r[5]} ± {r[6]} | {r[7]} | {r[8]} | {r[9]} |")
    lines.append("")

    lines.append("## Honest assessment\n")
    pmf_lat = float(np.nanmean(agg[pmf_name]["latency"]))
    lines.append(f"- PrimeMatchedFilter mean latency: {pmf_lat:.2f} samples; "
                 f"PMF mean precision @ recall=0.95: {name_to_prec[pmf_name]:.4f}.")
    # Wins / losses vs each baseline
    for baseline in [n_ for n_ in agg if n_ != pmf_name]:
        b_aucpr = name_to_aucpr[baseline]
        b_prec = name_to_prec[baseline]
        delta_a = pmf_aucpr - b_aucpr
        delta_p = name_to_prec[pmf_name] - b_prec
        verdict_a = "beats" if delta_a > 0 else ("ties" if abs(delta_a) < 1e-3 else "loses to")
        verdict_p = "beats" if delta_p > 0 else ("ties" if abs(delta_p) < 1e-3 else "loses to")
        lines.append(f"- vs **{baseline}**: PMF {verdict_a} on AUC-PR (Δ={delta_a:+.4f}); "
                     f"{verdict_p} on precision@R=.95 (Δ={delta_p:+.4f}).")

    lines.append("")
    lines.append("## Notes / caveats\n")
    lines.append("- Single-channel synthetic data; structured spikes are exactly the "
                 "regime a matched filter is designed for, so the comparison is somewhat "
                 "favourable to PMF.")
    lines.append("- IsolationForest and OneClassSVM see length-11 sliding-window features; "
                 "they are not given the same kernel structure.")
    lines.append("- PMF kernel size (n_taps=17) and window_size=100 were chosen a priori; "
                 "no per-seed tuning. Hyperparameter sensitivity not explored here.")
    lines.append("- The Mertens-weighted kernel is approximately mean-zero and oscillatory, "
                 "which suppresses the AR(1) low-frequency baseline and accentuates "
                 "transients.")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    n_seeds = int(os.environ.get("N_SEEDS", "100"))
    agg, rows = main(n_seeds=n_seeds)
    write_report(agg, rows,
                 "/Users/saar/Farey 4.7 solutions/pmf_benchmark_results.md",
                 n_seeds=n_seeds, n=10_000, n_anom=10)
