#!/usr/bin/env python3
"""
Farey vs QMC sampling for Monte Carlo integration — ray tracing relevance test.
Compares convergence rates of: Random, Halton, Sobol, Van der Corput, Farey sequences.
"""

import numpy as np
import json
import time
from fractions import Fraction
from math import gcd

# ─── Sequence generators ───

def random_uniform(n, seed=42):
    rng = np.random.default_rng(seed)
    return rng.random(n)

def van_der_corput(n, base=2):
    """Van der Corput sequence in given base."""
    pts = []
    for i in range(1, n + 1):
        x, denom = 0.0, 1.0
        num = i
        while num > 0:
            denom *= base
            x += (num % base) / denom
            num //= base
        pts.append(x)
    return np.array(pts)

def halton_1d(n, base=2):
    return van_der_corput(n, base)

def halton_2d(n):
    """Halton sequence in bases 2,3."""
    return np.column_stack([van_der_corput(n, 2), van_der_corput(n, 3)])

def sobol_1d(n):
    """Sobol sequence via scipy if available, else fallback to VdC base 2."""
    try:
        from scipy.stats import qmc
        sampler = qmc.Sobol(d=1, scramble=False)
        # Sobol needs power-of-2; take first n from next power of 2
        m = 1
        while m < n + 1:
            m *= 2
        pts = sampler.random(m)[1:n+1, 0]  # skip 0
        return pts
    except ImportError:
        # Fallback: use a different VdC base as approximation
        return van_der_corput(n, 3)

def sobol_2d(n):
    try:
        from scipy.stats import qmc
        sampler = qmc.Sobol(d=2, scramble=False)
        m = 1
        while m < n + 1:
            m *= 2
        pts = sampler.random(m)[1:n+1]
        return pts
    except ImportError:
        return np.column_stack([van_der_corput(n, 2), van_der_corput(n, 5)])

def farey_sequence(order):
    """Generate Farey sequence F_N (all fractions p/q with 0 < p/q < 1, q <= order)."""
    fracs = set()
    for q in range(1, order + 1):
        for p in range(1, q):
            if gcd(p, q) == 1:
                fracs.add(p / q)
    return sorted(fracs)

def farey_samples(n):
    """Get ~n Farey samples: find the smallest order giving >= n fractions, take first n."""
    order = 2
    while True:
        fs = farey_sequence(order)
        if len(fs) >= n:
            return np.array(fs[:n])
        order += 1

def hammersley_2d(n):
    """Hammersley set: (i/n, VdC(i))."""
    return np.column_stack([np.arange(1, n+1) / (n+1), van_der_corput(n, 2)])

def farey_2d(n):
    """Farey x Farey tensor product: take sqrt(n) from each axis."""
    k = max(int(np.sqrt(n)) + 1, 3)
    fx = farey_samples(k)
    fy = farey_samples(k)
    xx, yy = np.meshgrid(fx, fy)
    pts = np.column_stack([xx.ravel(), yy.ravel()])
    # Take first n points
    if len(pts) > n:
        pts = pts[:n]
    return pts

# ─── Test functions (1D) ───

def f_smooth(x):
    return np.sin(np.pi * x) ** 2

def f_discontinuous(x):
    return np.where(x > 0.3, 1.0, 0.0)

def f_highfreq(x):
    return np.sin(50 * np.pi * x)

def f_mixed(x):
    base = np.sin(np.pi * x) ** 2
    # 3 narrow Gaussian spikes
    spikes = (2.0 * np.exp(-((x - 0.2)**2) / (2 * 0.01**2)) +
              3.0 * np.exp(-((x - 0.55)**2) / (2 * 0.008**2)) +
              1.5 * np.exp(-((x - 0.85)**2) / (2 * 0.012**2)))
    return base + spikes

# Exact integrals (computed analytically or with high-precision quadrature)
from scipy import integrate
EXACT_1D = {}
for name, fn in [("smooth", f_smooth), ("discontinuous", f_discontinuous),
                  ("highfreq", f_highfreq), ("mixed", f_mixed)]:
    val, _ = integrate.quad(fn, 0, 1)
    EXACT_1D[name] = val

# ─── Test function (2D): indicator of circle ───

def f_circle(xy):
    """Soft shadow: indicator of circle centered at (0.5, 0.5) with radius 0.3."""
    x, y = xy[:, 0], xy[:, 1]
    return np.where((x - 0.5)**2 + (y - 0.5)**2 < 0.3**2, 1.0, 0.0)

EXACT_2D_CIRCLE = np.pi * 0.3**2  # area of circle

# ─── Star discrepancy approximation (1D) ───

def star_discrepancy_1d(pts):
    """Compute D*_N for 1D points in [0,1]."""
    pts_sorted = np.sort(pts)
    n = len(pts_sorted)
    indices = np.arange(1, n + 1)
    # D* = max(max_i |i/n - x_i|, max_i |x_i - (i-1)/n|)
    d_plus = np.max(indices / n - pts_sorted)
    d_minus = np.max(pts_sorted - (indices - 1) / n)
    return max(d_plus, d_minus)

# ─── Main experiment ───

def run_1d_experiment():
    Ns = [10, 20, 50, 100, 200, 500, 1000]
    functions = {
        "smooth": f_smooth,
        "discontinuous": f_discontinuous,
        "highfreq": f_highfreq,
        "mixed": f_mixed
    }
    methods_1d = {
        "random": random_uniform,
        "halton": lambda n: halton_1d(n, 2),
        "sobol": sobol_1d,
        "van_der_corput": lambda n: van_der_corput(n, 2),
        "farey": farey_samples
    }

    results = {}

    for fname, fn in functions.items():
        exact = EXACT_1D[fname]
        results[fname] = {}
        for mname, gen in methods_1d.items():
            errors = []
            for n in Ns:
                pts = gen(n)
                estimate = np.mean(fn(pts))
                error = abs(estimate - exact)
                errors.append(error)
            results[fname][mname] = {
                "Ns": Ns,
                "errors": errors
            }

    return results

def run_discrepancy_test():
    Ns = [10, 20, 50, 100, 200, 500, 1000]
    methods = {
        "random": random_uniform,
        "halton": lambda n: halton_1d(n, 2),
        "sobol": sobol_1d,
        "van_der_corput": lambda n: van_der_corput(n, 2),
        "farey": farey_samples
    }

    disc_results = {}
    for mname, gen in methods.items():
        discs = []
        for n in Ns:
            pts = gen(n)
            d = star_discrepancy_1d(pts)
            discs.append(d)
        disc_results[mname] = {"Ns": Ns, "discrepancies": discs}

    return disc_results

def run_2d_experiment():
    Ns = [25, 50, 100, 200, 500, 1000]
    methods_2d = {
        "random": lambda n: np.random.default_rng(42).random((n, 2)),
        "halton": halton_2d,
        "sobol": sobol_2d,
        "hammersley": hammersley_2d,
        "farey_tensor": farey_2d
    }
    exact = EXACT_2D_CIRCLE

    results = {}
    for mname, gen in methods_2d.items():
        errors = []
        for n in Ns:
            pts = gen(n)
            estimate = np.mean(f_circle(pts))
            error = abs(estimate - exact)
            errors.append(error)
        results[mname] = {"Ns": Ns, "errors": errors}

    return results

def fit_convergence_rate(Ns, errors):
    """Fit error ~ C * N^(-alpha), return alpha."""
    # Filter out zeros
    valid = [(n, e) for n, e in zip(Ns, errors) if e > 1e-16]
    if len(valid) < 3:
        return float('nan')
    ns, es = zip(*valid)
    log_n = np.log(np.array(ns, dtype=float))
    log_e = np.log(np.array(es, dtype=float))
    # Linear regression: log_e = -alpha * log_n + c
    coeffs = np.polyfit(log_n, log_e, 1)
    return -coeffs[0]  # alpha

def main():
    print("=" * 70)
    print("FAREY vs QMC SAMPLING — RAY TRACING INTEGRATION TEST")
    print("=" * 70)

    t0 = time.time()

    # 1D tests
    print("\n--- 1D Integration Tests ---")
    results_1d = run_1d_experiment()

    for fname in results_1d:
        print(f"\nFunction: {fname} (exact = {EXACT_1D[fname]:.8f})")
        print(f"  {'Method':<16} {'N=10':>10} {'N=100':>10} {'N=1000':>10} {'Rate':>8}")
        print(f"  {'-'*54}")
        for mname in results_1d[fname]:
            data = results_1d[fname][mname]
            errs = data["errors"]
            rate = fit_convergence_rate(data["Ns"], errs)
            # indices for N=10,100,1000
            print(f"  {mname:<16} {errs[0]:10.6f} {errs[3]:10.6f} {errs[6]:10.6f} {rate:8.2f}")

    # Discrepancy
    print("\n--- Star Discrepancy D*_N ---")
    disc = run_discrepancy_test()
    print(f"  {'Method':<16} {'N=10':>10} {'N=100':>10} {'N=1000':>10}")
    print(f"  {'-'*46}")
    for mname in disc:
        d = disc[mname]["discrepancies"]
        print(f"  {mname:<16} {d[0]:10.6f} {d[3]:10.6f} {d[6]:10.6f}")

    # 2D tests
    print("\n--- 2D Integration (Circle Indicator, exact = {:.8f}) ---".format(EXACT_2D_CIRCLE))
    results_2d = run_2d_experiment()
    print(f"  {'Method':<16} {'N=25':>10} {'N=100':>10} {'N=1000':>10} {'Rate':>8}")
    print(f"  {'-'*54}")
    for mname in results_2d:
        data = results_2d[mname]
        errs = data["errors"]
        rate = fit_convergence_rate(data["Ns"], errs)
        print(f"  {mname:<16} {errs[0]:10.6f} {errs[2]:10.6f} {errs[5]:10.6f} {rate:8.2f}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.2f}s")

    # ─── Analysis ───
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)

    # Find best method per function
    for fname in results_1d:
        best_method = None
        best_err = float('inf')
        for mname in results_1d[fname]:
            err_1000 = results_1d[fname][mname]["errors"][-1]
            if err_1000 < best_err:
                best_err = err_1000
                best_method = mname
        rate_farey = fit_convergence_rate(
            results_1d[fname]["farey"]["Ns"],
            results_1d[fname]["farey"]["errors"])
        rate_halton = fit_convergence_rate(
            results_1d[fname]["halton"]["Ns"],
            results_1d[fname]["halton"]["errors"])
        farey_beats = results_1d[fname]["farey"]["errors"][-1] < results_1d[fname]["halton"]["errors"][-1]
        print(f"\n{fname}:")
        print(f"  Best at N=1000: {best_method} (err={best_err:.2e})")
        print(f"  Farey rate: {rate_farey:.2f}, Halton rate: {rate_halton:.2f}")
        print(f"  Farey beats Halton at N=1000? {'YES' if farey_beats else 'NO'}")

    # 2D summary
    print("\n2D circle indicator:")
    for mname in results_2d:
        err1k = results_2d[mname]["errors"][-1]
        rate = fit_convergence_rate(results_2d[mname]["Ns"], results_2d[mname]["errors"])
        print(f"  {mname:<16}: err@1000={err1k:.2e}, rate={rate:.2f}")

    # ─── Save JSON ───
    output = {
        "1d_integration": {},
        "1d_discrepancy": {},
        "2d_integration": {},
        "exact_values_1d": EXACT_1D,
        "exact_value_2d_circle": EXACT_2D_CIRCLE,
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_seconds": elapsed
        }
    }

    for fname in results_1d:
        output["1d_integration"][fname] = {}
        for mname in results_1d[fname]:
            d = results_1d[fname][mname]
            output["1d_integration"][fname][mname] = {
                "Ns": d["Ns"],
                "errors": [float(e) for e in d["errors"]],
                "convergence_rate": float(fit_convergence_rate(d["Ns"], d["errors"]))
            }

    for mname in disc:
        output["1d_discrepancy"][mname] = {
            "Ns": disc[mname]["Ns"],
            "discrepancies": [float(d) for d in disc[mname]["discrepancies"]]
        }

    for mname in results_2d:
        d = results_2d[mname]
        output["2d_integration"][mname] = {
            "Ns": d["Ns"],
            "errors": [float(e) for e in d["errors"]],
            "convergence_rate": float(fit_convergence_rate(d["Ns"], d["errors"]))
        }

    out_path = "/Users/saar/Desktop/Farey-Local/experiments/ray_tracing_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

if __name__ == "__main__":
    main()
