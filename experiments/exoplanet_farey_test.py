#!/usr/bin/env python3
"""
Exoplanet Resonance Chain Analysis: Testing Farey Ordering in Multi-Planet Systems
==================================================================================

Downloads confirmed exoplanet data from the NASA Exoplanet Archive TAP API,
computes consecutive period ratios in multi-planet systems, and tests whether
these ratios follow Farey sequence ordering more closely than random.

Tests:
  1. Farey approximation: Are real ratios closer to Farey fractions than random?
  2. Mediant ordering: Do consecutive triples satisfy the mediant property?
  3. Farey level clustering: Do systems cluster at low Farey levels?
  4. Stern-Brocot depth distribution: Are real ratios shallower than random?

Author: Saar / Claude analysis
Date: 2026-03-27
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import csv
import io
import math
import numpy as np
from collections import defaultdict
from fractions import Fraction
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────
# 1. Farey / Stern-Brocot utilities
# ─────────────────────────────────────────────────────────────────────

def farey_sequence(n):
    """Generate Farey sequence F_n as list of Fraction objects."""
    fracs = set()
    for q in range(1, n + 1):
        for p in range(0, q + 1):
            fracs.add(Fraction(p, q))
    return sorted(fracs)


def farey_sequence_range(n, lo=1.0, hi=3.0):
    """Generate Farey-like fractions p/q with 1 <= q <= n and lo <= p/q <= hi."""
    fracs = set()
    for q in range(1, n + 1):
        p_lo = max(1, int(math.ceil(lo * q)))
        p_hi = int(math.floor(hi * q))
        for p in range(p_lo, p_hi + 1):
            fracs.add(Fraction(p, q))
    return sorted(fracs)


def nearest_farey(x, n, lo=1.0, hi=3.0):
    """Find the Farey fraction p/q (q <= n) closest to x in [lo, hi].
    Returns (Fraction, error)."""
    best_frac = Fraction(1, 1)
    best_err = abs(x - 1.0)
    for q in range(1, n + 1):
        p_lo = max(1, int(math.ceil(lo * q)))
        p_hi = int(math.floor(hi * q))
        for p in range(p_lo, p_hi + 1):
            frac = Fraction(p, q)
            err = abs(x - float(frac))
            if err < best_err:
                best_err = err
                best_frac = frac
    return best_frac, best_err


def stern_brocot_depth(x, max_depth=30):
    """Find the depth of x (as a Fraction) in the Stern-Brocot tree.
    For irrational x (given as float), find the depth of the best rational
    approximation found by descending the tree."""
    if isinstance(x, float):
        # Convert to fraction with bounded denominator
        frac = Fraction(x).limit_denominator(1000)
    else:
        frac = x

    # Descend the Stern-Brocot tree
    lo_p, lo_q = 0, 1  # 0/1
    hi_p, hi_q = 1, 0  # 1/0 = infinity
    depth = 0

    for _ in range(max_depth):
        med_p = lo_p + hi_p
        med_q = lo_q + hi_q
        med = Fraction(med_p, med_q)
        if med == frac:
            return depth + 1
        elif frac < med:
            hi_p, hi_q = med_p, med_q
        else:
            lo_p, lo_q = med_p, med_q
        depth += 1

    return depth


def stern_brocot_depth_real(x, max_depth=50):
    """Stern-Brocot depth for a real number > 0.
    Uses the standard SB tree descent: depth = number of steps to reach
    the best rational approximation with bounded denominator.
    We limit denominator to 100 to get a meaningful depth."""
    frac = Fraction(x).limit_denominator(100)
    # Descend the SB tree from 0/1 ... 1/0
    lo_p, lo_q = 0, 1
    hi_p, hi_q = 1, 0  # represents infinity
    depth = 0
    for _ in range(max_depth):
        med_p = lo_p + hi_p
        med_q = lo_q + hi_q
        if med_q > 200:  # bail if denominators grow too large
            break
        med = Fraction(med_p, med_q)
        if med == frac:
            return depth + 1
        elif frac < med:
            hi_p, hi_q = med_p, med_q
        else:
            lo_p, lo_q = med_p, med_q
        depth += 1
    return depth


def mediant(a, b):
    """Compute mediant of two fractions a = p1/q1, b = p2/q2."""
    return Fraction(a.numerator + b.numerator, a.denominator + b.denominator)


# ─────────────────────────────────────────────────────────────────────
# 2. Data download from NASA Exoplanet Archive
# ─────────────────────────────────────────────────────────────────────

def download_exoplanet_data():
    """Download multi-planet system data from NASA Exoplanet Archive TAP API."""
    query = (
        "SELECT pl_name,hostname,pl_orbper,sy_pnum "
        "FROM ps "
        "WHERE sy_pnum>=3 AND pl_orbper IS NOT NULL AND default_flag=1"
    )
    url = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
        + urllib.parse.urlencode({"query": query, "format": "csv"})
    )

    print(f"Downloading from NASA Exoplanet Archive...")
    print(f"URL: {url[:120]}...")

    # Try cached file first
    cache_path = os.path.join(OUT_DIR, "exoplanet_data_cache.csv")
    if os.path.exists(cache_path):
        print(f"  Using cached data: {cache_path}")
        with open(cache_path) as f:
            data = f.read()
        if data.startswith("pl_name"):
            reader = csv.DictReader(io.StringIO(data))
            rows = list(reader)
            print(f"  Loaded {len(rows)} planet entries from cache.")
            return rows
        else:
            print("  Cache file invalid, downloading fresh...")

    req = urllib.request.Request(url, headers={"User-Agent": "Python/ExoplanetFareyAnalysis"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read().decode("utf-8")
        # Cache for next time
        with open(cache_path, "w") as f:
            f.write(data)
    except Exception as e:
        print(f"Download failed: {e}")
        print("Using cached/fallback data for known resonant systems.")
        return None

    # Parse CSV
    reader = csv.DictReader(io.StringIO(data))
    rows = list(reader)
    print(f"Downloaded {len(rows)} planet entries.")
    return rows


def parse_systems(rows):
    """Group planets by host star, sort by orbital period."""
    systems = defaultdict(list)
    for row in rows:
        try:
            period = float(row["pl_orbper"])
            name = row["pl_name"].strip()
            host = row["hostname"].strip()
            nplanets = int(row["sy_pnum"])
            systems[host].append({
                "name": name,
                "period": period,
                "nplanets": nplanets,
            })
        except (ValueError, KeyError):
            continue

    # Sort each system by period and keep only systems with 3+ measured periods
    result = {}
    for host, planets in systems.items():
        planets.sort(key=lambda p: p["period"])
        if len(planets) >= 3:
            result[host] = planets

    return result


def get_fallback_systems():
    """Hardcoded known resonant chain systems as fallback."""
    systems = {
        "TRAPPIST-1": [
            {"name": "TRAPPIST-1 b", "period": 1.51087081, "nplanets": 7},
            {"name": "TRAPPIST-1 c", "period": 2.4218233, "nplanets": 7},
            {"name": "TRAPPIST-1 d", "period": 4.049610, "nplanets": 7},
            {"name": "TRAPPIST-1 e", "period": 6.099615, "nplanets": 7},
            {"name": "TRAPPIST-1 f", "period": 9.206690, "nplanets": 7},
            {"name": "TRAPPIST-1 g", "period": 12.35294, "nplanets": 7},
            {"name": "TRAPPIST-1 h", "period": 18.767, "nplanets": 7},
        ],
        "HD 110067": [
            {"name": "HD 110067 b", "period": 9.11367, "nplanets": 6},
            {"name": "HD 110067 c", "period": 13.67354, "nplanets": 6},
            {"name": "HD 110067 d", "period": 20.51903, "nplanets": 6},
            {"name": "HD 110067 e", "period": 30.79312, "nplanets": 6},
            {"name": "HD 110067 f", "period": 41.05862, "nplanets": 6},
            {"name": "HD 110067 g", "period": 54.76989, "nplanets": 6},
        ],
        "Kepler-223": [
            {"name": "Kepler-223 b", "period": 7.3845, "nplanets": 4},
            {"name": "Kepler-223 c", "period": 9.8456, "nplanets": 4},
            {"name": "Kepler-223 d", "period": 14.7887, "nplanets": 4},
            {"name": "Kepler-223 e", "period": 19.7257, "nplanets": 4},
        ],
        "TOI-178": [
            {"name": "TOI-178 b", "period": 1.9146, "nplanets": 6},
            {"name": "TOI-178 c", "period": 3.2385, "nplanets": 6},
            {"name": "TOI-178 d", "period": 6.5578, "nplanets": 6},
            {"name": "TOI-178 e", "period": 9.9619, "nplanets": 6},
            {"name": "TOI-178 f", "period": 15.2318, "nplanets": 6},
            {"name": "TOI-178 g", "period": 20.7075, "nplanets": 6},
        ],
        "Kepler-80": [
            {"name": "Kepler-80 f", "period": 0.9868, "nplanets": 6},
            {"name": "Kepler-80 d", "period": 3.0722, "nplanets": 6},
            {"name": "Kepler-80 e", "period": 4.6453, "nplanets": 6},
            {"name": "Kepler-80 b", "period": 7.0525, "nplanets": 6},
            {"name": "Kepler-80 c", "period": 9.5236, "nplanets": 6},
            {"name": "Kepler-80 g", "period": 14.6456, "nplanets": 6},
        ],
    }
    return systems


# ─────────────────────────────────────────────────────────────────────
# 3. Compute period ratios and Farey approximations
# ─────────────────────────────────────────────────────────────────────

def compute_ratios(systems, farey_order=12):
    """For each system, compute consecutive period ratios and their
    nearest Farey approximation."""
    all_ratios = []
    system_results = {}

    for host, planets in systems.items():
        periods = [p["period"] for p in planets]
        names = [p["name"] for p in planets]
        ratios = []
        for i in range(len(periods) - 1):
            r = periods[i + 1] / periods[i]
            frac, err = nearest_farey(r, farey_order, lo=1.0, hi=3.5)
            sb_depth = stern_brocot_depth_real(r)
            ratios.append({
                "pair": f"{names[i]} / {names[i+1]}",
                "ratio": r,
                "nearest_farey": frac,
                "farey_error": err,
                "farey_denom": frac.denominator,
                "sb_depth": sb_depth,
            })
            all_ratios.append({
                "host": host,
                "ratio": r,
                "nearest_farey": frac,
                "farey_error": err,
                "farey_denom": frac.denominator,
                "sb_depth": sb_depth,
            })
        system_results[host] = {
            "planets": planets,
            "ratios": ratios,
            "farey_level": max(r["farey_denom"] for r in ratios) if ratios else 0,
        }

    return system_results, all_ratios


# ─────────────────────────────────────────────────────────────────────
# 4. Statistical tests
# ─────────────────────────────────────────────────────────────────────

def generate_random_ratios(n, lo=1.0, hi=2.5, seed=42):
    """Generate n random period ratios uniformly in [lo, hi]."""
    rng = np.random.default_rng(seed)
    return rng.uniform(lo, hi, n)


def test1_farey_proximity(real_ratios, farey_order=12, n_random=10000):
    """TEST 1: Are real period ratios closer to Farey fractions than random?"""
    print("\n" + "=" * 70)
    print("TEST 1: Farey Proximity")
    print("=" * 70)

    real_errors = np.array([r["farey_error"] for r in real_ratios])

    # Generate random ratios in similar range
    real_vals = np.array([r["ratio"] for r in real_ratios])
    lo, hi = real_vals.min() * 0.95, real_vals.max() * 1.05

    random_ratios = generate_random_ratios(n_random, lo=max(1.0, lo), hi=min(3.5, hi))
    random_errors = []
    for x in random_ratios:
        _, err = nearest_farey(x, farey_order, lo=1.0, hi=3.5)
        random_errors.append(err)
    random_errors = np.array(random_errors)

    # Two-sample KS test
    ks_stat, ks_pval = stats.ks_2samp(real_errors, random_errors)

    # Mann-Whitney U test (one-sided: real < random)
    mw_stat, mw_pval = stats.mannwhitneyu(real_errors, random_errors, alternative="less")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((real_errors.std()**2 + random_errors.std()**2) / 2)
    cohens_d = (random_errors.mean() - real_errors.mean()) / pooled_std if pooled_std > 0 else 0

    print(f"  Real ratios: n={len(real_errors)}, mean error={real_errors.mean():.6f}, "
          f"median={np.median(real_errors):.6f}")
    print(f"  Random ratios: n={len(random_errors)}, mean error={random_errors.mean():.6f}, "
          f"median={np.median(random_errors):.6f}")
    print(f"  KS test: D={ks_stat:.4f}, p={ks_pval:.2e}")
    print(f"  Mann-Whitney U (one-sided): U={mw_stat:.0f}, p={mw_pval:.2e}")
    print(f"  Cohen's d (effect size): {cohens_d:.3f}")

    return {
        "real_errors": real_errors,
        "random_errors": random_errors,
        "ks_stat": ks_stat,
        "ks_pval": ks_pval,
        "mw_stat": mw_stat,
        "mw_pval": mw_pval,
        "cohens_d": cohens_d,
    }


def test2_mediant_ordering(system_results):
    """TEST 2: Do consecutive period ratios satisfy the mediant property?
    For each triple of consecutive planets, check if the middle ratio is
    approximately the mediant of the outer two ratios."""
    print("\n" + "=" * 70)
    print("TEST 2: Mediant Ordering")
    print("=" * 70)

    mediant_errors = []
    mediant_details = []
    total_triples = 0

    for host, sysdata in system_results.items():
        ratios = sysdata["ratios"]
        if len(ratios) < 2:
            continue
        for i in range(len(ratios) - 1):
            r1 = ratios[i]["nearest_farey"]
            r2 = ratios[i + 1]["nearest_farey"]
            # Actual middle ratio from the original data
            actual_r1 = ratios[i]["ratio"]
            actual_r2 = ratios[i + 1]["ratio"]

            # The mediant of the two Farey fractions
            med = mediant(r1, r2)
            # In the Farey context, mediant is the "in-between" fraction
            # Check if there's an intermediate ratio that matches
            # For triples (a,b,c), check if b ~ mediant(a,c)
            med_val = float(med)
            # The "middle" value to compare against
            # Actually for a triple of period ratios r1, r2, the mediant
            # gives a prediction for what a missing intermediate ratio would be
            mediant_err = abs(actual_r2 - med_val)
            mediant_errors.append(mediant_err)
            mediant_details.append({
                "host": host,
                "r1": str(r1),
                "r2": str(r2),
                "mediant": str(med),
                "actual_r2": actual_r2,
                "mediant_val": med_val,
                "error": mediant_err,
            })
            total_triples += 1

    # Compare with random: for random pairs of Farey fractions, what's the
    # mediant error to a random third ratio?
    rng = np.random.default_rng(123)
    random_mediant_errors = []
    farey_fracs = farey_sequence_range(12, 1.0, 3.0)
    farey_floats = [float(f) for f in farey_fracs]

    for _ in range(5000):
        idx1, idx2 = sorted(rng.choice(len(farey_fracs), 2, replace=False))
        f1, f2 = farey_fracs[idx1], farey_fracs[idx2]
        med = mediant(f1, f2)
        rand_ratio = rng.uniform(1.0, 2.5)
        random_mediant_errors.append(abs(rand_ratio - float(med)))

    mediant_errors = np.array(mediant_errors)
    random_mediant_errors = np.array(random_mediant_errors)

    if len(mediant_errors) > 0:
        ks_stat, ks_pval = stats.ks_2samp(mediant_errors, random_mediant_errors)
        print(f"  Total consecutive pairs tested: {total_triples}")
        print(f"  Mean mediant error (real): {mediant_errors.mean():.4f}")
        print(f"  Mean mediant error (random): {random_mediant_errors.mean():.4f}")
        print(f"  KS test: D={ks_stat:.4f}, p={ks_pval:.2e}")
    else:
        ks_stat, ks_pval = 0, 1
        print("  No triples available for testing.")

    return {
        "mediant_errors": mediant_errors,
        "random_mediant_errors": random_mediant_errors,
        "details": mediant_details,
        "ks_stat": ks_stat,
        "ks_pval": ks_pval,
    }


def test3_farey_level(system_results, n_random_sys=5000):
    """TEST 3: Do systems cluster at low Farey levels?
    Farey level = minimum N such that F_N contains all nearest-Farey ratios."""
    print("\n" + "=" * 70)
    print("TEST 3: Farey Level Clustering")
    print("=" * 70)

    real_levels = []
    for host, sysdata in system_results.items():
        if sysdata["farey_level"] > 0:
            real_levels.append(sysdata["farey_level"])

    # Simulate random systems
    rng = np.random.default_rng(456)
    random_levels = []
    for _ in range(n_random_sys):
        n_planets = rng.integers(3, 8)
        rand_ratios = sorted(rng.uniform(1.05, 2.5, n_planets - 1))
        max_denom = 0
        for r in rand_ratios:
            frac, _ = nearest_farey(r, 12, lo=1.0, hi=3.5)
            max_denom = max(max_denom, frac.denominator)
        random_levels.append(max_denom)

    real_levels = np.array(real_levels)
    random_levels = np.array(random_levels)

    ks_stat, ks_pval = stats.ks_2samp(real_levels, random_levels)
    mw_stat, mw_pval = stats.mannwhitneyu(real_levels, random_levels, alternative="less")

    print(f"  Real systems: n={len(real_levels)}, mean level={real_levels.mean():.2f}, "
          f"median={np.median(real_levels):.0f}")
    print(f"  Random systems: n={len(random_levels)}, mean level={random_levels.mean():.2f}, "
          f"median={np.median(random_levels):.0f}")
    print(f"  KS test: D={ks_stat:.4f}, p={ks_pval:.2e}")
    print(f"  Mann-Whitney U (one-sided): U={mw_stat:.0f}, p={mw_pval:.2e}")

    return {
        "real_levels": real_levels,
        "random_levels": random_levels,
        "ks_stat": ks_stat,
        "ks_pval": ks_pval,
        "mw_stat": mw_stat,
        "mw_pval": mw_pval,
    }


def test4_sb_depth(real_ratios, n_random=10000):
    """TEST 4: Are real ratios shallower in the Stern-Brocot tree?"""
    print("\n" + "=" * 70)
    print("TEST 4: Stern-Brocot Depth Distribution")
    print("=" * 70)

    real_depths = np.array([r["sb_depth"] for r in real_ratios])

    real_vals = np.array([r["ratio"] for r in real_ratios])
    lo, hi = max(1.0, real_vals.min() * 0.95), min(3.5, real_vals.max() * 1.05)

    rng = np.random.default_rng(789)
    random_ratios = rng.uniform(lo, hi, n_random)
    random_depths = np.array([stern_brocot_depth_real(x) for x in random_ratios])

    ks_stat, ks_pval = stats.ks_2samp(real_depths, random_depths)
    mw_stat, mw_pval = stats.mannwhitneyu(real_depths, random_depths, alternative="less")

    pooled_std = np.sqrt((real_depths.std()**2 + random_depths.std()**2) / 2)
    cohens_d = (random_depths.mean() - real_depths.mean()) / pooled_std if pooled_std > 0 else 0

    print(f"  Real ratios: n={len(real_depths)}, mean depth={real_depths.mean():.2f}, "
          f"median={np.median(real_depths):.0f}")
    print(f"  Random ratios: n={len(random_depths)}, mean depth={random_depths.mean():.2f}, "
          f"median={np.median(random_depths):.0f}")
    print(f"  KS test: D={ks_stat:.4f}, p={ks_pval:.2e}")
    print(f"  Mann-Whitney U (one-sided): U={mw_stat:.0f}, p={mw_pval:.2e}")
    print(f"  Cohen's d: {cohens_d:.3f}")

    return {
        "real_depths": real_depths,
        "random_depths": random_depths,
        "ks_stat": ks_stat,
        "ks_pval": ks_pval,
        "mw_stat": mw_stat,
        "mw_pval": mw_pval,
        "cohens_d": cohens_d,
    }


# ─────────────────────────────────────────────────────────────────────
# 5. Focused resonant chain analysis
# ─────────────────────────────────────────────────────────────────────

KNOWN_RESONANT = [
    "TRAPPIST-1", "HD 110067", "Kepler-223", "TOI-178", "Kepler-80",
    "Kepler-60", "Kepler-90", "GJ 876", "HR 8799",
]


def analyze_resonant_chains(system_results, all_ratios):
    """Detailed analysis of known resonant chain systems."""
    print("\n" + "=" * 70)
    print("RESONANT CHAIN ANALYSIS")
    print("=" * 70)

    resonant_ratios = []
    non_resonant_ratios = []

    for r in all_ratios:
        if r["host"] in KNOWN_RESONANT:
            resonant_ratios.append(r)
        else:
            non_resonant_ratios.append(r)

    # Print details for known systems
    for host in KNOWN_RESONANT:
        if host in system_results:
            sys = system_results[host]
            print(f"\n  {host} ({len(sys['planets'])} planets, Farey level {sys['farey_level']}):")
            for r in sys["ratios"]:
                print(f"    {r['pair']:40s}  ratio={r['ratio']:.6f}  "
                      f"nearest={r['nearest_farey']}  err={r['farey_error']:.6f}  "
                      f"SB-depth={r['sb_depth']}")

    # Compare resonant vs non-resonant
    if resonant_ratios and non_resonant_ratios:
        res_errors = np.array([r["farey_error"] for r in resonant_ratios])
        nonres_errors = np.array([r["farey_error"] for r in non_resonant_ratios])
        mw_stat, mw_pval = stats.mannwhitneyu(res_errors, nonres_errors, alternative="less")
        print(f"\n  Resonant vs non-resonant Farey errors:")
        print(f"    Resonant: n={len(res_errors)}, mean={res_errors.mean():.6f}")
        print(f"    Non-resonant: n={len(nonres_errors)}, mean={nonres_errors.mean():.6f}")
        print(f"    Mann-Whitney U (one-sided): p={mw_pval:.2e}")

    return resonant_ratios, non_resonant_ratios


def test5_resonant_permutation(system_results, n_perm=10000):
    """TEST 5: Permutation test for known resonant chains.
    For each known resonant system, compute mean Farey error of its ratios.
    Then compare against the distribution of mean errors from random subsets
    of the same size drawn from all systems."""
    print("\n" + "=" * 70)
    print("TEST 5: Resonant Chain Permutation Test")
    print("=" * 70)

    # Collect Farey errors from known resonant systems (ratios <= 3.5 only)
    resonant_errors = []
    for host in KNOWN_RESONANT:
        if host in system_results:
            for r in system_results[host]["ratios"]:
                if r["ratio"] <= 3.5:
                    resonant_errors.append(r["farey_error"])

    if not resonant_errors:
        print("  No resonant chain data available.")
        return {}

    resonant_errors = np.array(resonant_errors)
    observed_mean = resonant_errors.mean()
    n_res = len(resonant_errors)

    # Collect all errors from all systems (ratios <= 3.5)
    all_errors = []
    for host, sysdata in system_results.items():
        for r in sysdata["ratios"]:
            if r["ratio"] <= 3.5:
                all_errors.append(r["farey_error"])
    all_errors = np.array(all_errors)

    # Permutation test
    rng = np.random.default_rng(999)
    perm_means = []
    for _ in range(n_perm):
        sample = rng.choice(all_errors, size=n_res, replace=False)
        perm_means.append(sample.mean())
    perm_means = np.array(perm_means)

    p_value = np.mean(perm_means <= observed_mean)

    # Also compute SB depth comparison
    resonant_depths = []
    for host in KNOWN_RESONANT:
        if host in system_results:
            for r in system_results[host]["ratios"]:
                if r["ratio"] <= 3.5:
                    resonant_depths.append(r["sb_depth"])
    resonant_depths = np.array(resonant_depths)

    all_depths = []
    for host, sysdata in system_results.items():
        for r in sysdata["ratios"]:
            if r["ratio"] <= 3.5:
                all_depths.append(r["sb_depth"])
    all_depths = np.array(all_depths)

    depth_perm_means = []
    for _ in range(n_perm):
        sample = rng.choice(all_depths, size=len(resonant_depths), replace=False)
        depth_perm_means.append(sample.mean())
    depth_perm_means = np.array(depth_perm_means)
    depth_p = np.mean(depth_perm_means <= resonant_depths.mean())

    print(f"  Resonant chain ratios: n={n_res}")
    print(f"  Mean Farey error (resonant): {observed_mean:.6f}")
    print(f"  Mean Farey error (all): {all_errors.mean():.6f}")
    print(f"  Permutation p-value (error): {p_value:.4f}")
    print(f"  Mean SB depth (resonant): {resonant_depths.mean():.2f}")
    print(f"  Mean SB depth (all): {all_depths.mean():.2f}")
    print(f"  Permutation p-value (depth): {depth_p:.4f}")

    return {
        "n_resonant": n_res,
        "observed_mean_error": float(observed_mean),
        "perm_p_error": float(p_value),
        "observed_mean_depth": float(resonant_depths.mean()),
        "perm_p_depth": float(depth_p),
        "perm_means": perm_means,
    }


# ─────────────────────────────────────────────────────────────────────
# 6. Visualization
# ─────────────────────────────────────────────────────────────────────

def plot_test1(t1_results):
    """Plot Farey approximation error distributions."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    ax = axes[0]
    ax.hist(t1_results["random_errors"], bins=50, alpha=0.5, label="Random", density=True, color="gray")
    ax.hist(t1_results["real_errors"], bins=30, alpha=0.7, label="Real systems", density=True, color="steelblue")
    ax.set_xlabel("Distance to nearest Farey fraction (F_12)")
    ax.set_ylabel("Density")
    ax.set_title("TEST 1: Farey Proximity")
    ax.legend()
    ax.text(0.98, 0.95,
            f"KS p = {t1_results['ks_pval']:.2e}\n"
            f"MW p = {t1_results['mw_pval']:.2e}\n"
            f"Cohen's d = {t1_results['cohens_d']:.2f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, bbox=dict(boxstyle="round", fc="wheat", alpha=0.5))

    # ECDF
    ax = axes[1]
    real_sorted = np.sort(t1_results["real_errors"])
    rand_sorted = np.sort(t1_results["random_errors"])
    ax.plot(real_sorted, np.linspace(0, 1, len(real_sorted)), label="Real systems", color="steelblue", lw=2)
    ax.plot(rand_sorted, np.linspace(0, 1, len(rand_sorted)), label="Random", color="gray", lw=1.5, alpha=0.7)
    ax.set_xlabel("Distance to nearest Farey fraction")
    ax.set_ylabel("Cumulative fraction")
    ax.set_title("ECDF: Real vs Random")
    ax.legend()

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "exoplanet_test1_farey_proximity.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved: {path}")


def plot_test3(t3_results):
    """Plot Farey level distributions."""
    fig, ax = plt.subplots(figsize=(8, 5))

    bins = np.arange(0.5, 13.5, 1)
    ax.hist(t3_results["random_levels"], bins=bins, alpha=0.5, label="Random systems",
            density=True, color="gray")
    ax.hist(t3_results["real_levels"], bins=bins, alpha=0.7, label="Real systems",
            density=True, color="darkorange")
    ax.set_xlabel("Farey level N (max denominator of nearest fractions)")
    ax.set_ylabel("Density")
    ax.set_title("TEST 3: Farey Level of Multi-Planet Systems")
    ax.legend()
    ax.text(0.98, 0.95,
            f"KS p = {t3_results['ks_pval']:.2e}\n"
            f"MW p = {t3_results['mw_pval']:.2e}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, bbox=dict(boxstyle="round", fc="wheat", alpha=0.5))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "exoplanet_test3_farey_level.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved: {path}")


def plot_test4(t4_results):
    """Plot Stern-Brocot depth distributions."""
    fig, ax = plt.subplots(figsize=(8, 5))

    max_d = max(t4_results["real_depths"].max(), 30)
    bins = np.arange(-0.5, max_d + 1.5, 1)
    ax.hist(t4_results["random_depths"], bins=bins, alpha=0.5, label="Random",
            density=True, color="gray")
    ax.hist(t4_results["real_depths"], bins=bins, alpha=0.7, label="Real systems",
            density=True, color="forestgreen")
    ax.set_xlabel("Stern-Brocot tree depth (sum of CF coefficients)")
    ax.set_ylabel("Density")
    ax.set_title("TEST 4: Stern-Brocot Depth Distribution")
    ax.legend()
    ax.set_xlim(0, 40)
    ax.text(0.98, 0.95,
            f"KS p = {t4_results['ks_pval']:.2e}\n"
            f"MW p = {t4_results['mw_pval']:.2e}\n"
            f"Cohen's d = {t4_results['cohens_d']:.2f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, bbox=dict(boxstyle="round", fc="wheat", alpha=0.5))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "exoplanet_test4_sb_depth.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved: {path}")


def plot_resonant_chains(system_results):
    """Plot period ratios for known resonant chains on a Farey number line."""
    targets = [h for h in KNOWN_RESONANT if h in system_results]
    if not targets:
        return

    fig, ax = plt.subplots(figsize=(14, 6))

    # Draw Farey fractions as vertical lines
    farey_fracs = farey_sequence_range(8, 1.0, 2.6)
    for f in farey_fracs:
        fv = float(f)
        if 1.0 <= fv <= 2.6:
            ax.axvline(fv, color="lightblue", alpha=0.3, lw=0.5)
            if f.denominator <= 5:
                ax.axvline(fv, color="lightblue", alpha=0.6, lw=1)
                ax.text(fv, len(targets) + 0.3, f"{f.numerator}/{f.denominator}",
                        ha="center", va="bottom", fontsize=7, color="steelblue")

    colors = plt.cm.Set1(np.linspace(0, 1, len(targets)))
    for i, host in enumerate(targets):
        sys = system_results[host]
        for j, r in enumerate(sys["ratios"]):
            ax.plot(r["ratio"], i, "o", color=colors[i], markersize=8)
            ax.plot(float(r["nearest_farey"]), i, "x", color=colors[i],
                    markersize=6, alpha=0.5)
            # Draw line from actual to nearest Farey
            ax.plot([r["ratio"], float(r["nearest_farey"])], [i, i],
                    "-", color=colors[i], alpha=0.3, lw=1)

    ax.set_yticks(range(len(targets)))
    ax.set_yticklabels(targets)
    ax.set_xlabel("Period ratio P_{i+1} / P_i")
    ax.set_title("Resonant Chain Period Ratios vs Farey Fractions")
    ax.set_xlim(1.0, 2.6)
    ax.legend(["Farey fractions (F_8)", "Actual ratio (o)", "Nearest Farey (x)"],
              loc="upper right", fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "exoplanet_resonant_chains.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved: {path}")


def plot_ratio_scatter(all_ratios, system_results):
    """Scatter plot: ratio vs Farey error, colored by whether system is resonant."""
    fig, ax = plt.subplots(figsize=(10, 6))

    resonant_x, resonant_y = [], []
    other_x, other_y = [], []

    for r in all_ratios:
        if r["host"] in KNOWN_RESONANT:
            resonant_x.append(r["ratio"])
            resonant_y.append(r["farey_error"])
        else:
            other_x.append(r["ratio"])
            other_y.append(r["farey_error"])

    ax.scatter(other_x, other_y, alpha=0.3, s=15, color="gray", label="Other systems")
    ax.scatter(resonant_x, resonant_y, alpha=0.8, s=40, color="red",
               edgecolors="black", lw=0.5, label="Known resonant chains", zorder=5)

    # Mark key Farey fractions on x-axis
    key_fracs = [Fraction(3, 2), Fraction(4, 3), Fraction(5, 3),
                 Fraction(5, 4), Fraction(2, 1), Fraction(8, 5), Fraction(7, 5)]
    for f in key_fracs:
        fv = float(f)
        ax.axvline(fv, color="blue", alpha=0.15, lw=1)
        ax.text(fv, ax.get_ylim()[1] * 0.95 if ax.get_ylim()[1] > 0 else 0.04,
                f"{f.numerator}/{f.denominator}", ha="center", fontsize=7, color="blue")

    ax.set_xlabel("Period ratio")
    ax.set_ylabel("Distance to nearest Farey fraction (F_12)")
    ax.set_title("All Multi-Planet Systems: Ratio vs Farey Approximation Error")
    ax.legend()
    ax.set_yscale("log")

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "exoplanet_ratio_scatter.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved: {path}")


# ─────────────────────────────────────────────────────────────────────
# 7. Main
# ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("EXOPLANET RESONANCE CHAIN - FAREY ORDERING ANALYSIS")
    print("=" * 70)

    # Download data
    rows = download_exoplanet_data()
    if rows:
        systems = parse_systems(rows)
        print(f"Parsed {len(systems)} multi-planet systems (3+ measured periods).")
    else:
        systems = {}

    # Merge in fallback data for known resonant systems
    fallback = get_fallback_systems()
    for host, planets in fallback.items():
        if host not in systems:
            systems[host] = planets
            print(f"  Added fallback: {host}")

    if not systems:
        print("ERROR: No data available.")
        sys.exit(1)

    print(f"\nTotal systems: {len(systems)}")

    # Compute ratios
    FAREY_ORDER = 12
    system_results, all_ratios = compute_ratios(systems, farey_order=FAREY_ORDER)
    print(f"Total period ratios computed: {len(all_ratios)}")

    # Summary stats
    ratios_array = np.array([r["ratio"] for r in all_ratios])
    print(f"Ratio range: [{ratios_array.min():.4f}, {ratios_array.max():.4f}]")
    print(f"Mean ratio: {ratios_array.mean():.4f}")

    # Filter to ratios in [1.0, 3.5] -- beyond that, pairs are too widely spaced
    # to be in any reasonable mean-motion resonance
    RATIO_MAX = 3.5
    all_ratios_full = all_ratios
    all_ratios = [r for r in all_ratios if r["ratio"] <= RATIO_MAX]
    print(f"Ratios in [1, {RATIO_MAX}]: {len(all_ratios)} / {len(all_ratios_full)}")

    # Run tests
    t1 = test1_farey_proximity(all_ratios, farey_order=FAREY_ORDER)
    t2 = test2_mediant_ordering(system_results)
    t3 = test3_farey_level(system_results)
    t4 = test4_sb_depth(all_ratios)

    # Resonant chain analysis
    res_ratios, nonres_ratios = analyze_resonant_chains(system_results, all_ratios)
    t5 = test5_resonant_permutation(system_results)

    # Plots
    print("\n" + "=" * 70)
    print("GENERATING FIGURES")
    print("=" * 70)
    plot_test1(t1)
    plot_test3(t3)
    plot_test4(t4)
    plot_resonant_chains(system_results)
    plot_ratio_scatter(all_ratios, system_results)

    # ── Summary ─────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    results = {
        "n_systems": len(systems),
        "n_ratios": len(all_ratios),
        "farey_order": FAREY_ORDER,
        "test1_ks_pval": float(t1["ks_pval"]),
        "test1_mw_pval": float(t1["mw_pval"]),
        "test1_cohens_d": float(t1["cohens_d"]),
        "test2_ks_pval": float(t2["ks_pval"]),
        "test3_ks_pval": float(t3["ks_pval"]),
        "test3_mw_pval": float(t3["mw_pval"]),
        "test4_ks_pval": float(t4["ks_pval"]),
        "test4_mw_pval": float(t4["mw_pval"]),
        "test4_cohens_d": float(t4["cohens_d"]),
        "mean_real_farey_error": float(t1["real_errors"].mean()),
        "mean_random_farey_error": float(t1["random_errors"].mean()),
        "mean_real_sb_depth": float(t4["real_depths"].mean()),
        "mean_random_sb_depth": float(t4["random_depths"].mean()),
        "test5_perm_p_error": float(t5.get("perm_p_error", 1.0)),
        "test5_perm_p_depth": float(t5.get("perm_p_depth", 1.0)),
        "test5_n_resonant": int(t5.get("n_resonant", 0)),
    }

    # Save JSON
    json_path = os.path.join(OUT_DIR, "exoplanet_results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results JSON: {json_path}")

    # Print summary table
    print(f"\n  {'Test':<40s} {'p-value':>12s} {'Effect':>10s}")
    print(f"  {'-'*62}")
    d1 = f"d={t1['cohens_d']:.2f}"
    d4 = f"d={t4['cohens_d']:.2f}"
    print(f"  {'T1: Farey proximity (KS)':<40s} {t1['ks_pval']:>12.2e} {d1:>10s}")
    print(f"  {'T1: Farey proximity (MW)':<40s} {t1['mw_pval']:>12.2e}")
    print(f"  {'T2: Mediant ordering (KS)':<40s} {t2['ks_pval']:>12.2e}")
    print(f"  {'T3: Farey level clustering (KS)':<40s} {t3['ks_pval']:>12.2e}")
    print(f"  {'T3: Farey level clustering (MW)':<40s} {t3['mw_pval']:>12.2e}")
    print(f"  {'T4: SB depth (KS)':<40s} {t4['ks_pval']:>12.2e} {d4:>10s}")
    print(f"  {'T4: SB depth (MW)':<40s} {t4['mw_pval']:>12.2e}")
    t5_pe = f"{t5.get('perm_p_error', 1.0):.4f}"
    t5_pd = f"{t5.get('perm_p_depth', 1.0):.4f}"
    print(f"  {'T5: Resonant perm (Farey error)':<40s} {t5_pe:>12s}")
    print(f"  {'T5: Resonant perm (SB depth)':<40s} {t5_pd:>12s}")

    # Generate markdown report
    generate_report(results, t1, t2, t3, t4, t5, system_results, all_ratios,
                    res_ratios, nonres_ratios)

    print("\nDone.")


def generate_report(results, t1, t2, t3, t4, t5, system_results, all_ratios,
                    res_ratios, nonres_ratios):
    """Generate EXOPLANET_RESULTS.md"""

    # Resonant chain table
    chain_lines = []
    for host in KNOWN_RESONANT:
        if host in system_results:
            sys = system_results[host]
            for r in sys["ratios"]:
                chain_lines.append(
                    f"| {host} | {r['ratio']:.6f} | {r['nearest_farey']} | "
                    f"{r['farey_error']:.6f} | {r['sb_depth']} |"
                )

    chain_table = "\n".join(chain_lines) if chain_lines else "| (no data) | | | | |"

    # Interpretation
    sig_threshold = 0.05
    t1_sig = results["test1_mw_pval"] < sig_threshold
    t3_sig = results["test3_mw_pval"] < sig_threshold
    t4_sig = results["test4_mw_pval"] < sig_threshold

    interpretation_lines = []
    if t1_sig:
        interpretation_lines.append(
            f"- TEST 1 SIGNIFICANT (p={results['test1_mw_pval']:.2e}): "
            f"Real period ratios are closer to Farey fractions than random, "
            f"with effect size d={results['test1_cohens_d']:.2f}."
        )
    else:
        interpretation_lines.append(
            f"- TEST 1 NOT SIGNIFICANT (p={results['test1_mw_pval']:.2e}): "
            f"No strong evidence that all multi-planet ratios prefer Farey fractions."
        )

    if t3_sig:
        interpretation_lines.append(
            f"- TEST 3 SIGNIFICANT (p={results['test3_mw_pval']:.2e}): "
            f"Real systems cluster at lower Farey levels than random."
        )
    else:
        interpretation_lines.append(
            f"- TEST 3 NOT SIGNIFICANT (p={results['test3_mw_pval']:.2e}): "
            f"No evidence of Farey-level clustering beyond random."
        )

    if t4_sig:
        interpretation_lines.append(
            f"- TEST 4 SIGNIFICANT (p={results['test4_mw_pval']:.2e}): "
            f"Real ratios sit shallower in the Stern-Brocot tree (d={results['test4_cohens_d']:.2f})."
        )
    else:
        interpretation_lines.append(
            f"- TEST 4 NOT SIGNIFICANT (p={results['test4_mw_pval']:.2e}): "
            f"No strong evidence of shallow SB-tree preference."
        )

    t5_sig = results["test5_perm_p_error"] < sig_threshold
    if t5_sig:
        interpretation_lines.append(
            f"- TEST 5 SIGNIFICANT (p={results['test5_perm_p_error']:.4f}): "
            f"Known resonant chains have lower Farey errors than random subsets of equal size."
        )
    else:
        interpretation_lines.append(
            f"- TEST 5 NOT SIGNIFICANT (p={results['test5_perm_p_error']:.4f}): "
            f"Known resonant chains do not stand out from the general population in Farey error."
        )

    interpretation = "\n".join(interpretation_lines)

    report = f"""# Exoplanet Resonance Chains and Farey Ordering

## Overview

Analysis of {results['n_systems']} multi-planet systems (3+ planets with measured
orbital periods) from the NASA Exoplanet Archive. We test whether consecutive
period ratios P_{{i+1}}/P_i follow Farey sequence ordering.

Total period ratios analyzed: {results['n_ratios']}
Farey order used: F_{{{results['farey_order']}}}

## Test Results

| Test | Statistic | p-value | Effect Size |
|------|-----------|---------|-------------|
| T1: Farey proximity (KS) | KS | {results['test1_ks_pval']:.2e} | d={results['test1_cohens_d']:.2f} |
| T1: Farey proximity (MW, one-sided) | MW-U | {results['test1_mw_pval']:.2e} | |
| T2: Mediant ordering (KS) | KS | {results['test2_ks_pval']:.2e} | |
| T3: Farey level clustering (KS) | KS | {results['test3_ks_pval']:.2e} | |
| T3: Farey level clustering (MW) | MW-U | {results['test3_mw_pval']:.2e} | |
| T4: SB depth (KS) | KS | {results['test4_ks_pval']:.2e} | d={results['test4_cohens_d']:.2f} |
| T4: SB depth (MW, one-sided) | MW-U | {results['test4_mw_pval']:.2e} | |
| T5: Resonant chain perm (error) | Perm | {results['test5_perm_p_error']:.4f} | n={results['test5_n_resonant']} |
| T5: Resonant chain perm (depth) | Perm | {results['test5_perm_p_depth']:.4f} | |

### Key Numbers

- Mean Farey error (real): {results['mean_real_farey_error']:.6f}
- Mean Farey error (random): {results['mean_random_farey_error']:.6f}
- Mean SB depth (real): {results['mean_real_sb_depth']:.2f}
- Mean SB depth (random): {results['mean_random_sb_depth']:.2f}

## Interpretation

{interpretation}

## Known Resonant Chain Details

| System | Ratio | Nearest Farey | Error | SB Depth |
|--------|-------|---------------|-------|----------|
{chain_table}

## Figures

- `exoplanet_test1_farey_proximity.png` - Farey error distributions
- `exoplanet_test3_farey_level.png` - Farey level clustering
- `exoplanet_test4_sb_depth.png` - Stern-Brocot depth distributions
- `exoplanet_resonant_chains.png` - Resonant chain ratios vs Farey fractions
- `exoplanet_ratio_scatter.png` - All ratios scatter plot

## Methodology

1. Downloaded all confirmed planets in systems with 3+ planets from NASA Exoplanet Archive
2. Computed consecutive period ratios (sorted by period within each system)
3. For each ratio, found the nearest fraction p/q with q <= {results['farey_order']}
4. Compared real distributions against random uniform ratios in the same range
5. Used two-sample KS tests and one-sided Mann-Whitney U tests
6. Effect sizes reported as Cohen's d where applicable

## Notes

- The Farey order N={results['farey_order']} was chosen to capture common MMR ratios
  (3:2, 4:3, 5:3, 5:4, 2:1, 8:5) while avoiding overfitting with too many fractions
- Stern-Brocot depth computed as sum of continued fraction coefficients
- Random baseline uses uniform distribution in the observed ratio range
- Known resonant systems represent a small fraction of all multi-planet systems;
  the signal may be diluted in the full population
"""

    path = os.path.join(OUT_DIR, "EXOPLANET_RESULTS.md")
    with open(path, "w") as f:
        f.write(report)
    print(f"  Report: {path}")


if __name__ == "__main__":
    main()
