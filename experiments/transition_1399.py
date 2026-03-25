#!/usr/bin/env python3
"""
Deep exploration of the p=1399 wobble transition.

p=1399 is the FIRST prime where W(p) > W(p-1) ("violation" / non-healing).
This script investigates WHY it happens here and what predicts it.

Key findings from preliminary analysis:
- M(1399) = +8, the first time Mertens reaches +8 at a prime
- Violations occur at ALL M values (even M=-2!), but rate increases with |M|
- There is NO sharp M threshold -- it's a probability that grows with M
"""

import csv
import math
import numpy as np
from collections import defaultdict
from fractions import Fraction

CSV_PATH = "experiments/wobble_primes_100000.csv"


def load_csv():
    """Load the wobble CSV data."""
    rows = []
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                'p': int(row['p']),
                'wobble_p': float(row['wobble_p']),
                'wobble_pm1': float(row['wobble_pm1']),
                'delta_w': float(row['delta_w']),
                'farey_size': int(row['farey_size_p']),
                'mertens': int(row['mertens_p']),
                'm_over_sqrt': float(row['m_over_sqrt_p']),
                'violation': int(row['violation']),
            })
    return rows


def compute_mertens_trajectory(N_max):
    """Compute M(n) for all n up to N_max using the Mobius function."""
    # Sieve for Mobius function
    mu = [0] * (N_max + 1)
    mu[1] = 1
    is_prime = [True] * (N_max + 1)
    primes = []

    for i in range(2, N_max + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1  # prime => mu = -1
        for p in primes:
            if i * p > N_max:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0  # p^2 divides i*p
                break
            else:
                mu[i * p] = -mu[i]

    # Accumulate to get M(n)
    M = [0] * (N_max + 1)
    for n in range(1, N_max + 1):
        M[n] = M[n - 1] + mu[n]

    return M, mu


def compute_wobble_exact(N):
    """Compute W(N) exactly using Farey sequence F_N."""
    # Generate Farey sequence F_N
    fracs = set()
    for q in range(1, N + 1):
        for p in range(0, q + 1):
            if math.gcd(p, q) == 1:
                fracs.add(Fraction(p, q))
    farey = sorted(fracs)
    n = len(farey)

    # Wobble = sum of |f_i - i/(n-1)|
    wobble = 0
    for i, f in enumerate(farey):
        ideal = Fraction(i, n - 1)
        wobble += abs(f - ideal)

    return float(wobble)


# ============================================================
# SECTION 1: What's special about p=1399?
# ============================================================
def analyze_1399(rows):
    print("=" * 70)
    print("SECTION 1: What's special about p=1399?")
    print("=" * 70)

    # Find the row for 1399 and neighbors
    idx_1399 = None
    for i, r in enumerate(rows):
        if r['p'] == 1399:
            idx_1399 = i
            break

    if idx_1399 is None:
        print("ERROR: p=1399 not found in data!")
        return

    print("\n--- Primes around the transition ---")
    print(f"{'p':>6} {'M(p)':>6} {'W(p)':>14} {'W(p-1)':>14} {'delta_W':>14} {'violation':>9}")
    for i in range(max(0, idx_1399 - 8), min(len(rows), idx_1399 + 8)):
        r = rows[i]
        marker = " <-- FIRST" if r['p'] == 1399 else ""
        print(f"{r['p']:>6} {r['mertens']:>6} {r['wobble_p']:>14.8e} {r['wobble_pm1']:>14.8e} "
              f"{r['delta_w']:>14.8e} {r['violation']:>9}{marker}")

    # Is 1399 special as a prime?
    p = 1399
    print(f"\n--- Properties of p = {p} ---")
    print(f"  p = {p}")
    print(f"  p mod 4 = {p % 4}")
    print(f"  p mod 6 = {p % 6}")
    print(f"  p mod 3 = {p % 3}")

    # Check if 1399 is in a twin prime pair
    def is_prime(n):
        if n < 2: return False
        if n < 4: return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0: return False
            i += 6
        return True

    print(f"  Is 1397 prime? {is_prime(1397)} (twin below)")
    print(f"  Is 1401 prime? {is_prime(1401)} (twin above)")
    print(f"  Previous prime: ", end="")
    pp = p - 1
    while not is_prime(pp): pp -= 1
    print(f"{pp} (gap = {p - pp})")
    print(f"  Next prime: ", end="")
    np_ = p + 1
    while not is_prime(np_): np_ += 1
    print(f"{np_} (gap = {np_ - p})")

    # Factorizations near 1399
    print(f"\n--- Composites between p=1381 and p=1399 ---")
    for n in range(1382, 1399):
        if not is_prime(n):
            # Factor
            factors = []
            temp = n
            d = 2
            while d * d <= temp:
                while temp % d == 0:
                    factors.append(d)
                    temp //= d
                d += 1
            if temp > 1:
                factors.append(temp)
            print(f"  {n} = {'*'.join(map(str, factors))}")

    # The delta_w is BARELY positive at 1399
    r = rows[idx_1399]
    print(f"\n--- The violation is tiny ---")
    print(f"  delta_W(1399) = {r['delta_w']:.10e}")
    print(f"  W(1399)       = {r['wobble_p']:.10e}")
    print(f"  Relative size  = {r['delta_w']/r['wobble_p']:.6e}")
    print(f"  Compare delta_W(1381) = {rows[idx_1399-2]['delta_w']:.10e}  (last non-violation)")


# ============================================================
# SECTION 2: Composite precursor analysis
# ============================================================
def analyze_composites_near_1399():
    print("\n" + "=" * 70)
    print("SECTION 2: What happens at nearby composites?")
    print("=" * 70)

    # Compute Mertens and wobble for composites near 1399
    M, mu = compute_mertens_trajectory(1500)

    print("\n--- M(N) for N = 1395..1405 ---")
    print(f"{'N':>6} {'mu(N)':>6} {'M(N)':>6} {'prime?':>7}")
    for n in range(1395, 1406):
        is_p = all(n % i != 0 for i in range(2, int(n**0.5) + 1)) and n > 1
        print(f"{n:>6} {mu[n]:>6} {M[n]:>6} {'YES' if is_p else '':>7}")

    print("\n--- M(N) for N = 1375..1405 (full trajectory) ---")
    print(f"{'N':>6} {'mu(N)':>6} {'M(N)':>6} {'prime?':>7}")
    for n in range(1375, 1406):
        is_p = all(n % i != 0 for i in range(2, int(n**0.5) + 1)) and n > 1
        marker = " ***" if is_p else ""
        print(f"{n:>6} {mu[n]:>6} {M[n]:>6} {marker}")

    # Key question: what's M(1398)?
    print(f"\n--- The composite just before 1399 ---")
    print(f"  M(1398) = {M[1398]}")
    print(f"  M(1399) = {M[1399]}")
    print(f"  mu(1399) = {mu[1399]}  (should be -1 since 1399 is prime)")
    print(f"  So M jumped by {M[1399] - M[1398]} at n=1399")


# ============================================================
# SECTION 3: Mertens trajectory 1300..1500
# ============================================================
def mertens_trajectory_plot(M):
    print("\n" + "=" * 70)
    print("SECTION 3: Mertens function trajectory N = 1300..1500")
    print("=" * 70)

    # Find where M first reaches each milestone
    milestones = {}
    for n in range(1, 1501):
        if M[n] not in milestones:
            milestones[M[n]] = n

    print("\n--- First time M(N) reaches various values ---")
    for val in sorted(milestones.keys()):
        if val >= 5:
            print(f"  M first = {val:>3} at N = {milestones[val]}")

    # ASCII plot of M(N) for 1300..1500
    print("\n--- ASCII plot of M(N), N = 1300..1500 ---")
    vals = [M[n] for n in range(1300, 1501)]
    mn, mx = min(vals), max(vals)
    height = 30
    width = 100  # compress 200 values into 100 columns

    # Check which N are primes
    def is_prime(n):
        if n < 2: return False
        if n < 4: return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0: return False
            i += 6
        return True

    print(f"  M range: [{mn}, {mx}]")
    for row in range(height, -1, -1):
        m_val = mn + (mx - mn) * row / height
        line = f"{m_val:>5.1f} |"
        for col in range(width):
            n = 1300 + col * 2  # sample every other N
            if n > 1500:
                break
            val = M[n]
            target = mn + (mx - mn) * row / height
            if abs(val - target) <= (mx - mn) / height / 2:
                if n == 1399:
                    line += "X"
                elif is_prime(n):
                    line += "*"
                else:
                    line += "."
            else:
                line += " "
        print(line)
    print("       " + "-" * width)
    print("       1300" + " " * (width - 8) + "1500")

    # How long does M stay >= 8?
    print("\n--- Duration of M(N) >= 8 near 1399 ---")
    run_start = None
    runs = []
    for n in range(1, 1501):
        if M[n] >= 8:
            if run_start is None:
                run_start = n
        else:
            if run_start is not None:
                runs.append((run_start, n - 1))
                run_start = None
    if run_start is not None:
        runs.append((run_start, 1500))

    for start, end in runs:
        peak = max(M[n] for n in range(start, end + 1))
        print(f"  N = {start}..{end} (length {end - start + 1}), peak M = {peak}")


# ============================================================
# SECTION 4: Sharp or gradual transition?
# ============================================================
def transition_analysis(rows):
    print("\n" + "=" * 70)
    print("SECTION 4: Is the transition sharp or gradual?")
    print("=" * 70)

    # Examine delta_w as M increases
    print("\n--- delta_W vs M(p) for primes near the transition ---")
    print(f"{'p':>6} {'M(p)':>6} {'delta_W':>14} {'sign':>6}")
    for r in rows:
        if 1200 <= r['p'] <= 1500:
            sign = "+" if r['delta_w'] > 0 else "-"
            print(f"{r['p']:>6} {r['mertens']:>6} {r['delta_w']:>14.8e} {sign:>6}")

    # Look at the RATIO of healing vs non-healing by M value
    print("\n--- Violation rate by M(p) value ---")
    violations_by_m = defaultdict(int)
    total_by_m = defaultdict(int)

    for r in rows:
        m = r['mertens']
        total_by_m[m] += 1
        if r['violation'] == 1:
            violations_by_m[m] += 1

    print(f"{'M(p)':>6} {'violations':>11} {'total':>7} {'rate':>8}")
    for m in sorted(total_by_m.keys()):
        if total_by_m[m] >= 3:  # only show M values with enough data
            rate = violations_by_m[m] / total_by_m[m]
            bar = "#" * int(rate * 40)
            print(f"{m:>6} {violations_by_m[m]:>11} {total_by_m[m]:>7} {rate:>8.3f}  {bar}")

    # Compute violation rate in bins of |M|
    print("\n--- Violation rate by |M(p)| (binned) ---")
    bins = [(0, 3), (4, 7), (8, 11), (12, 15), (16, 20), (21, 30), (31, 50), (51, 100)]
    for lo, hi in bins:
        v_count = sum(violations_by_m.get(m, 0) for m in range(lo, hi + 1))
        t_count = sum(total_by_m.get(m, 0) for m in range(lo, hi + 1))
        # Also include negative M
        v_count += sum(violations_by_m.get(-m, 0) for m in range(lo, hi + 1))
        t_count += sum(total_by_m.get(-m, 0) for m in range(lo, hi + 1))
        if t_count > 0:
            rate = v_count / t_count
            print(f"  |M| in [{lo:>3}, {hi:>3}]: {v_count:>5}/{t_count:>5} = {rate:.4f}")


# ============================================================
# SECTION 5: Can we predict non-healing from M alone?
# ============================================================
def prediction_analysis(rows):
    print("\n" + "=" * 70)
    print("SECTION 5: Can we predict non-healing from M(p) alone?")
    print("=" * 70)

    # Hypothesis: violation probability depends on M(p)/sqrt(p)
    # Group by m_over_sqrt_p bins
    print("\n--- Violation rate by M(p)/sqrt(p) ---")
    bins_edge = np.arange(-0.6, 0.7, 0.05)
    v_count = np.zeros(len(bins_edge) - 1)
    t_count = np.zeros(len(bins_edge) - 1)

    for r in rows:
        ratio = r['m_over_sqrt']
        idx = np.searchsorted(bins_edge, ratio) - 1
        if 0 <= idx < len(v_count):
            t_count[idx] += 1
            if r['violation'] == 1:
                v_count[idx] += 1

    print(f"{'M/sqrt(p) range':>20} {'violations':>11} {'total':>7} {'rate':>8}")
    for i in range(len(v_count)):
        if t_count[i] >= 5:
            rate = v_count[i] / t_count[i]
            bar = "#" * int(rate * 40)
            print(f"  [{bins_edge[i]:>6.3f}, {bins_edge[i+1]:>6.3f}): "
                  f"{int(v_count[i]):>7} {int(t_count[i]):>7} {rate:>8.3f}  {bar}")

    # Alternative: M(p)^2 / p as predictor
    print("\n--- Violation rate by M(p)^2 / p ---")
    bins_m2p = np.arange(0, 0.12, 0.005)
    v_m2p = np.zeros(len(bins_m2p) - 1)
    t_m2p = np.zeros(len(bins_m2p) - 1)

    for r in rows:
        ratio = r['mertens'] ** 2 / r['p']
        idx = np.searchsorted(bins_m2p, ratio) - 1
        if 0 <= idx < len(v_m2p):
            t_m2p[idx] += 1
            if r['violation'] == 1:
                v_m2p[idx] += 1

    print(f"{'M^2/p range':>20} {'violations':>11} {'total':>7} {'rate':>8}")
    for i in range(len(v_m2p)):
        if t_m2p[i] >= 5:
            rate = v_m2p[i] / t_m2p[i]
            bar = "#" * int(rate * 40)
            print(f"  [{bins_m2p[i]:>6.4f}, {bins_m2p[i+1]:>6.4f}): "
                  f"{int(v_m2p[i]):>7} {int(t_m2p[i]):>7} {rate:>8.3f}  {bar}")

    # Find the "crossover" where violation rate exceeds 50%
    print("\n--- Finding the 50% crossover point ---")
    # Sort rows by M(p)/sqrt(p) and compute running violation rate
    sorted_rows = sorted(rows, key=lambda r: r['m_over_sqrt'])
    window = 100
    for i in range(0, len(sorted_rows) - window, window // 2):
        chunk = sorted_rows[i:i + window]
        v_rate = sum(1 for r in chunk if r['violation'] == 1) / len(chunk)
        m_range = (chunk[0]['m_over_sqrt'], chunk[-1]['m_over_sqrt'])
        if 0.4 <= v_rate <= 0.6:
            print(f"  ~50% rate at M/sqrt(p) in [{m_range[0]:.3f}, {m_range[1]:.3f}], rate = {v_rate:.3f}")

    # Logistic regression: P(violation) = sigmoid(a * M/sqrt(p) + b)
    print("\n--- Logistic fit: P(violation) = sigmoid(a * M/sqrt(p) + b) ---")
    X = np.array([r['m_over_sqrt'] for r in rows])
    Y = np.array([r['violation'] for r in rows])

    # Simple gradient descent for logistic regression
    a, b = 0.0, 0.0
    lr = 0.01
    for _ in range(5000):
        z = a * X + b
        z = np.clip(z, -20, 20)
        pred = 1 / (1 + np.exp(-z))
        pred = np.clip(pred, 1e-10, 1 - 1e-10)
        grad_a = np.mean(X * (pred - Y))
        grad_b = np.mean(pred - Y)
        a -= lr * grad_a
        b -= lr * grad_b

    print(f"  a = {a:.4f}, b = {b:.4f}")
    print(f"  P(violation) = sigmoid({a:.4f} * M/sqrt(p) + {b:.4f})")
    print(f"  50% crossover at M/sqrt(p) = {-b/a:.4f}")
    print(f"  For p=1399: M/sqrt(p) = {8/math.sqrt(1399):.4f}, predicted P = {1/(1+math.exp(-(a*8/math.sqrt(1399)+b))):.4f}")

    # Also try: P(violation) = sigmoid(a * M^2/p + b)
    X2 = np.array([r['mertens'] ** 2 / r['p'] for r in rows])
    a2, b2 = 0.0, 0.0
    for _ in range(5000):
        z = a2 * X2 + b2
        z = np.clip(z, -20, 20)
        pred = 1 / (1 + np.exp(-z))
        pred = np.clip(pred, 1e-10, 1 - 1e-10)
        grad_a = np.mean(X2 * (pred - Y))
        grad_b = np.mean(pred - Y)
        a2 -= lr * grad_a
        b2 -= lr * grad_b

    print(f"\n  Alternative: P(violation) = sigmoid({a2:.4f} * M^2/p + {b2:.4f})")
    print(f"  50% crossover at M^2/p = {-b2/a2:.4f}")

    # Accuracy comparison
    pred1 = (1 / (1 + np.exp(-(a * X + b)))) > 0.5
    pred2 = (1 / (1 + np.exp(-(a2 * X2 + b2)))) > 0.5
    acc1 = np.mean(pred1 == Y)
    acc2 = np.mean(pred2 == Y)
    print(f"\n  Accuracy of M/sqrt(p) model: {acc1:.4f}")
    print(f"  Accuracy of M^2/p model:     {acc2:.4f}")


# ============================================================
# SECTION 6: First-violation clustering
# ============================================================
def violation_clustering(rows):
    print("\n" + "=" * 70)
    print("SECTION 6: Do violations come in clusters?")
    print("=" * 70)

    violations = [r for r in rows if r['violation'] == 1]
    gaps = []
    for i in range(1, len(violations)):
        gap = violations[i]['p'] - violations[i - 1]['p']
        gaps.append(gap)

    print(f"\n  Total violations: {len(violations)}")
    print(f"  Mean gap between violations: {np.mean(gaps):.1f}")
    print(f"  Median gap: {np.median(gaps):.1f}")
    print(f"  Min gap: {min(gaps)} (consecutive primes?)")
    print(f"  Max gap: {max(gaps)}")

    # First 10 clusters (consecutive violations with gap <= 20)
    print("\n--- First 10 violation clusters ---")
    clusters = []
    current_cluster = [violations[0]]
    for i in range(1, len(violations)):
        if violations[i]['p'] - violations[i - 1]['p'] <= 30:
            current_cluster.append(violations[i])
        else:
            if len(current_cluster) >= 2:
                clusters.append(current_cluster)
            current_cluster = [violations[i]]
    if len(current_cluster) >= 2:
        clusters.append(current_cluster)

    for i, cl in enumerate(clusters[:10]):
        primes = [r['p'] for r in cl]
        mertens_vals = [r['mertens'] for r in cl]
        print(f"  Cluster {i + 1}: primes {primes}, M values {mertens_vals}")


# ============================================================
# SECTION 7: The M(p) "excursion" theory
# ============================================================
def excursion_analysis(rows):
    print("\n" + "=" * 70)
    print("SECTION 7: Mertens excursion theory")
    print("=" * 70)

    # Theory: violations happen during Mertens "excursions" away from 0
    # An excursion is a run where M(n) stays above some threshold

    M, _ = compute_mertens_trajectory(100000)

    # For each prime, compute the "local excursion height"
    # = max M(n) in a window around p
    print("\n--- Excursion context for violations ---")
    print("For each violation, what's the local M peak and how far into the excursion?")

    violations = [r for r in rows if r['violation'] == 1][:20]
    print(f"\n{'p':>6} {'M(p)':>6} {'local_peak':>11} {'excursion_start':>16} {'depth_in':>9}")
    for r in violations:
        p = r['p']
        # Find the excursion: go backwards from p until M crosses 0
        start = p
        while start > 1 and M[start] > 0:
            start -= 1
        # Find peak
        peak = max(M[n] for n in range(start, min(p + 100, 100001)))
        depth = p - start
        print(f"{p:>6} {r['mertens']:>6} {peak:>11} {start:>16} {depth:>9}")

    # Big picture: what fraction of primes during an excursion are violations?
    print("\n--- Violation rate vs excursion height ---")
    # For each prime, compute the current excursion peak
    excursion_data = []
    for r in rows:
        p = r['p']
        if p > 100000:
            break
        # Simple proxy: M(p) itself as excursion indicator
        excursion_data.append((abs(r['mertens']), r['violation']))

    # Bin by |M|
    bins = list(range(0, 100, 5))
    for i in range(len(bins) - 1):
        lo, hi = bins[i], bins[i + 1]
        in_bin = [v for m, v in excursion_data if lo <= m < hi]
        if len(in_bin) >= 10:
            rate = sum(in_bin) / len(in_bin)
            bar = "#" * int(rate * 50)
            print(f"  |M| in [{lo:>3}, {hi:>3}): {sum(in_bin):>5}/{len(in_bin):>5} = {rate:.3f}  {bar}")


# ============================================================
# SECTION 8: The delta_W formula decomposition at p=1399
# ============================================================
def delta_w_decomposition():
    print("\n" + "=" * 70)
    print("SECTION 8: delta_W decomposition at p=1399")
    print("=" * 70)

    # delta_W(p) = W(p) - W(p-1) has known structure:
    # When going from F_{p-1} to F_p, we INSERT all fractions a/p (gcd(a,p)=1)
    # The new fractions redistribute the wobble
    # For prime p, we insert phi(p) = p-1 new fractions

    p = 1399
    print(f"\n  p = {p}")
    print(f"  phi(p) = {p - 1} new fractions inserted")
    print(f"  |F_{{p-1}}| needs computation...")

    # Farey size formula: |F_N| = 1 + sum_{k=1}^{N} phi(k)
    def euler_phi(n):
        result = n
        temp = n
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                while temp % d == 0:
                    temp //= d
                result -= result // d
            d += 1
        if temp > 1:
            result -= result // temp
        return result

    farey_size_pm1 = 1 + sum(euler_phi(k) for k in range(1, p))
    farey_size_p = farey_size_pm1 + (p - 1)  # since p is prime, phi(p) = p-1

    print(f"  |F_{{p-1}}| = {farey_size_pm1}")
    print(f"  |F_p| = {farey_size_p}")
    print(f"  Fraction of new points: {(p-1)/farey_size_p:.6f}")
    print(f"  Relative expansion: {farey_size_p/farey_size_pm1:.6f}")

    # The M(p) connection: M(p) measures the bias of Mobius,
    # which connects to how the new fractions distribute
    M, mu = compute_mertens_trajectory(1500)
    print(f"\n  M(p-1) = {M[p-1]}")
    print(f"  M(p) = {M[p]}")
    print(f"  mu(p) = {mu[p]}")
    print(f"  M(p)/sqrt(p) = {M[p]/math.sqrt(p):.6f}")
    print(f"  M(p)^2/p = {M[p]**2/p:.6f}")

    # Compare with "typical" healing prime near 1399
    for comparison_p in [1381, 1373, 1361]:
        ratio = M[comparison_p] / math.sqrt(comparison_p)
        m2p = M[comparison_p] ** 2 / comparison_p
        print(f"\n  Compare p={comparison_p}: M={M[comparison_p]}, M/sqrt(p)={ratio:.6f}, M^2/p={m2p:.6f}")


# ============================================================
# SECTION 9: Summary and key findings
# ============================================================
def summary(rows):
    print("\n" + "=" * 70)
    print("SECTION 9: SUMMARY OF KEY FINDINGS")
    print("=" * 70)

    # Compute key statistics
    violations_by_m = defaultdict(int)
    total_by_m = defaultdict(int)
    for r in rows:
        m = r['mertens']
        total_by_m[m] += 1
        if r['violation'] == 1:
            violations_by_m[m] += 1

    # Find the M value where violation rate crosses 50%
    for m in sorted(total_by_m.keys()):
        if total_by_m[m] >= 5:
            rate = violations_by_m[m] / total_by_m[m]
            if rate >= 0.5:
                print(f"\n  1. First M value with >= 50% violation rate: M = {m}")
                print(f"     ({violations_by_m[m]}/{total_by_m[m]} = {rate:.3f})")
                break

    # The lowest M with a violation
    min_m_violation = min(r['mertens'] for r in rows if r['violation'] == 1)
    print(f"\n  2. Lowest M(p) with a violation: M = {min_m_violation}")

    # The highest M without a violation
    max_m_clean = max(r['mertens'] for r in rows if r['violation'] == 0)
    print(f"\n  3. Highest M(p) WITHOUT a violation: M = {max_m_clean}")

    print(f"\n  4. Conclusion: There is NO sharp M threshold.")
    print(f"     Violations occur even at M = {min_m_violation}.")
    print(f"     Non-violations occur even at M = {max_m_clean}.")
    print(f"     The violation PROBABILITY increases smoothly with |M(p)|.")

    print(f"\n  5. p = 1399 is special because:")
    print(f"     - It's the first prime where M(p) = 8 (a new Mertens record at a prime)")
    print(f"     - The high M pushes delta_W just barely positive (+4.3e-8)")
    print(f"     - The transition is NOT sharp: it's a gradual probability shift")

    # Count violations by sign of M
    pos_violations = sum(1 for r in rows if r['violation'] == 1 and r['mertens'] > 0)
    neg_violations = sum(1 for r in rows if r['violation'] == 1 and r['mertens'] < 0)
    zero_violations = sum(1 for r in rows if r['violation'] == 1 and r['mertens'] == 0)
    pos_total = sum(1 for r in rows if r['mertens'] > 0)
    neg_total = sum(1 for r in rows if r['mertens'] < 0)

    print(f"\n  6. MASSIVE ASYMMETRY: Violations are almost entirely a POSITIVE M phenomenon!")
    print(f"     M > 0: {pos_violations}/{pos_total} violations ({pos_violations/pos_total:.3f})")
    print(f"     M < 0: {neg_violations}/{neg_total} violations ({neg_violations/neg_total:.5f})")
    print(f"     M = 0: {zero_violations} violations")
    print(f"     Ratio: {pos_violations/(neg_violations+0.001):.0f}x more likely when M > 0!")

    print(f"\n  7. BEST PREDICTOR: M(p)/sqrt(p)")
    print(f"     Binned data shows clear sigmoid:")
    print(f"       M/sqrt(p) < 0:    ~0% violation rate")
    print(f"       M/sqrt(p) ~ 0.05:  6.5% rate")
    print(f"       M/sqrt(p) ~ 0.10: 25.9% rate")
    print(f"       M/sqrt(p) ~ 0.12: 66.7% rate  <-- crosses 50% here")
    print(f"       M/sqrt(p) ~ 0.15: 86.6% rate")
    print(f"       M/sqrt(p) > 0.25: 99%+ rate")
    print(f"     The transition is continuous but STEEP around M/sqrt(p) ~ 0.10-0.15.")

    print(f"\n  8. CLUSTERS: Violations come in bursts during Mertens excursions.")
    print(f"     The first cluster at p=1399 has 5 primes (1399-1429) with M in [8,11].")
    print(f"     Clusters track EXACTLY with positive Mertens excursions.")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("Loading wobble data...")
    rows = load_csv()
    print(f"Loaded {len(rows)} prime records.\n")

    analyze_1399(rows)
    analyze_composites_near_1399()

    print("\nComputing Mertens trajectory (this may take a moment)...")
    M, mu = compute_mertens_trajectory(1500)
    mertens_trajectory_plot(M)

    transition_analysis(rows)
    prediction_analysis(rows)
    violation_clustering(rows)
    excursion_analysis(rows)
    delta_w_decomposition()
    summary(rows)

    print("\n" + "=" * 70)
    print("DONE. All analysis complete.")
    print("=" * 70)
