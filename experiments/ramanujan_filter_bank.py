#!/usr/bin/env python3
"""
Ramanujan Filter Bank: M(q)-Ordered vs Sequential Period Detection
=====================================================================
Tests whether ordering Ramanujan sum filters by |M(q)| descending
detects periods faster (fewer filters evaluated) than sequential ordering.

Key fix: Ramanujan sums are number-theoretic tools. c_q(n) responds to
integer periodicity, NOT sinusoidal periodicity. We use integer-periodic
test signals: x(n) = f(n mod P) + noise.

The Ramanujan periodicity transform:
  E(p) = (1/N) * sum_{q | p} |<x, c_q>|^2 / phi(q)

The detected period = argmax_p E(p).

Kill criterion:
  M(q)-ordering uses >=90% as many filters as sequential -> NO-GO
  M(q)-ordering uses <80% as many filters as sequential  -> GO (>20% savings)
"""

import numpy as np
import json
import time
from math import gcd

# ─── Number theory ──────────────────────────────────────────────────
def euler_phi(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def mertens_function(n_max):
    mu = [0] * (n_max + 1)
    mu[1] = 1
    is_prime = [True] * (n_max + 1)
    primes = []
    for i in range(2, n_max + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n_max:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (n_max + 1)
    for i in range(1, n_max + 1):
        M[i] = M[i - 1] + mu[i]
    return M, mu

def divisors_of(n):
    divs = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return sorted(divs)

# ─── Ramanujan sum (vectorized) ─────────────────────────────────────
def precompute_cq(Q, N):
    """Precompute c_q(n) for q=1..Q, n=0..N-1."""
    cq = {}
    ns = np.arange(N)
    for q in range(1, Q + 1):
        total = np.zeros(N)
        for a in range(1, q + 1):
            if gcd(a, q) == 1:
                total += np.cos(2 * np.pi * a * ns / q)
        cq[q] = total
    return cq

# ─── Signal generation ──────────────────────────────────────────────
def generate_periodic_signal(P, N, snr_db, rng):
    """
    Generate an integer-periodic signal: x(n) = pattern[n mod P] + noise.
    The pattern is a random vector of length P (fixed per period).
    """
    pattern = rng.randn(P)
    pattern = pattern / np.std(pattern)  # normalize
    signal = np.array([pattern[n % P] for n in range(N)])
    if snr_db == float('inf'):
        return signal
    sig_power = np.mean(signal ** 2)
    noise_power = sig_power / (10 ** (snr_db / 10))
    noise = rng.randn(N) * np.sqrt(noise_power)
    return signal + noise

# ─── Period detection via Ramanujan Periodicity Transform ────────────
def detect_period_rpt(x, cq, q_order, true_period, Q, N):
    """
    Evaluate filters in given order. After each new filter q, update
    period energies E(p) for all p that are multiples of q.
    Detect when argmax_p E(p) == true_period.

    E(p) = (1/N) * sum_{q | p, q evaluated} |<x, c_q>|^2 / phi(q)
    """
    period_energy = np.zeros(Q + 1)  # E(p) for p=0..Q

    # For speed, precompute which periods each q contributes to
    q_to_multiples = {}
    for q in range(1, Q + 1):
        q_to_multiples[q] = list(range(q, Q + 1, q))

    phi_cache = {q: euler_phi(q) for q in range(1, Q + 1)}

    for i, q in enumerate(q_order):
        inner = np.dot(x, cq[q])
        contribution = (inner ** 2) / (phi_cache[q] * N)
        for p in q_to_multiples[q]:
            period_energy[p] += contribution

        # Check argmax over candidate periods >= 2
        best = np.argmax(period_energy[2:]) + 2
        if best == true_period:
            return i + 1

    return len(q_order)

# ─── Direct filter detection ────────────────────────────────────────
def detect_direct(x, cq, q_order, true_period, N):
    """
    Simpler: the detected period is simply the q with highest
    |<x, c_q>|^2 / (phi(q) * N). No accumulation across divisors.
    """
    energies = {}
    phi_cache = {}
    for i, q in enumerate(q_order):
        if q not in phi_cache:
            phi_cache[q] = euler_phi(q)
        inner = np.dot(x, cq[q])
        energies[q] = (inner ** 2) / (phi_cache[q] * N)
        best = max(energies, key=energies.get)
        if best == true_period:
            return i + 1
    return len(q_order)

# ─── Main experiment ─────────────────────────────────────────────────
def run_experiment():
    print("=" * 72)
    print("Ramanujan Filter Bank: M(q)-Ordered vs Sequential Detection")
    print("Using integer-periodic signals (correct for Ramanujan sums)")
    print("=" * 72)

    Q = 120
    N = 500
    periods = [7, 13, 31, 97]
    snr_levels = [0, 5, 10, 20, float('inf')]
    n_random_trials = 50
    n_signal_trials = 30

    print(f"\nParameters: Q={Q}, N={N}, signal_trials={n_signal_trials}")
    print(f"Periods: {periods}")
    print(f"SNR levels: {[s if s != float('inf') else 'inf' for s in snr_levels]} dB")

    M, mu = mertens_function(Q)
    q_values = list(range(1, Q + 1))

    seq_order = list(q_values)
    mertens_order = sorted(q_values, key=lambda q: (-abs(M[q]), q))

    print(f"\nPosition of test periods in each ordering:")
    for P in periods:
        s_pos = seq_order.index(P) + 1
        m_pos = mertens_order.index(P) + 1
        print(f"  P={P:3d}: seq_pos={s_pos:3d}, mertens_pos={m_pos:3d}, M({P})={M[P]}")

    print(f"\nPrecomputing Ramanujan sums ({Q} x {N})...")
    t0 = time.time()
    cq = precompute_cq(Q, N)
    print(f"  Done in {time.time()-t0:.1f}s")

    # Verify detection works on clean signal first
    print("\n--- Sanity check: clean signal detection ---")
    for P in periods:
        rng = np.random.RandomState(42)
        x = generate_periodic_signal(P, N, float('inf'), rng)
        # Compute all energies
        energies = {}
        for q in range(2, Q+1):
            inner = np.dot(x, cq[q])
            energies[q] = (inner**2) / (euler_phi(q) * N)
        top5 = sorted(energies.items(), key=lambda kv: -kv[1])[:5]
        detected = top5[0][0]
        print(f"  P={P:3d}: detected={detected:3d} ({'OK' if detected==P else 'WRONG'}), "
              f"top5={[q for q,e in top5]}")

    results = {
        "parameters": {"Q": Q, "N": N, "periods": periods,
                        "snr_levels": [s if s != float('inf') else "inf" for s in snr_levels],
                        "n_random_trials": n_random_trials, "n_signal_trials": n_signal_trials},
        "mertens_order_top20": mertens_order[:20],
        "mertens_values_top20": [int(M[q]) for q in mertens_order[:20]],
        "period_positions": {},
        "test1_direct": [],
        "test2_rpt": [],
        "summary": {}
    }
    for P in periods:
        results["period_positions"][str(P)] = {
            "sequential": seq_order.index(P) + 1,
            "mertens": mertens_order.index(P) + 1,
            "M_value": int(M[P])
        }

    # ═══ TEST 1: Direct filter detection ═══
    print(f"\n{'='*72}")
    print("TEST 1: Direct detection (argmax_q E_q among evaluated filters)")
    print(f"{'='*72}")

    all_ms_1, all_rs_1 = [], []
    print(f"\n{'P':>4} {'SNR':>5} {'Seq':>6} {'M(q)':>6} {'Rand':>7} {'M/S':>6} {'R/S':>6} {'Verd':>7}")
    print("-" * 55)

    for P in periods:
        for snr_db in snr_levels:
            sc, mc, rc = [], [], []
            snr_label = f"{snr_db}dB" if snr_db != float('inf') else "clean"

            for trial in range(n_signal_trials):
                rng = np.random.RandomState(trial * 1000 + P)
                x = generate_periodic_signal(P, N, snr_db, rng)

                sc.append(detect_direct(x, cq, seq_order, P, N))
                mc.append(detect_direct(x, cq, mertens_order, P, N))

                tr = []
                for rt in range(n_random_trials):
                    ro = list(q_values)
                    np.random.RandomState(trial*10000+rt).shuffle(ro)
                    tr.append(detect_direct(x, cq, ro, P, N))
                rc.append(np.mean(tr))

            as_ = np.mean(sc); am = np.mean(mc); ar = np.mean(rc)
            rms = am/as_ if as_ > 0 else 999
            rrs = ar/as_ if as_ > 0 else 999
            all_ms_1.append(rms); all_rs_1.append(rrs)
            v = "GO" if rms < 0.80 else ("NO-GO" if rms >= 0.90 else "MARGIN")

            print(f"{P:>4} {snr_label:>5} {as_:>6.1f} {am:>6.1f} {ar:>7.1f} "
                  f"{rms:>5.2f}x {rrs:>5.2f}x {v:>7}")

            results["test1_direct"].append({
                "period": P, "snr_db": snr_db if snr_db != float('inf') else "inf",
                "avg_seq": round(float(as_),2), "avg_mertens": round(float(am),2),
                "avg_random": round(float(ar),2),
                "ratio_ms": round(float(rms),4), "ratio_rs": round(float(rrs),4),
                "verdict": v
            })

    ov1 = np.mean(all_ms_1)
    print(f"\nTest 1 mean M/S: {ov1:.4f} -> {'GO' if ov1<0.80 else ('NO-GO' if ov1>=0.90 else 'MARGINAL')}")

    # ═══ TEST 2: RPT (Ramanujan Periodicity Transform) ═══
    print(f"\n{'='*72}")
    print("TEST 2: RPT detection (E(p) accumulated from divisor filters)")
    print(f"{'='*72}")

    all_ms_2, all_rs_2 = [], []
    print(f"\n{'P':>4} {'SNR':>5} {'Seq':>6} {'M(q)':>6} {'Rand':>7} {'M/S':>6} {'R/S':>6} {'Verd':>7}")
    print("-" * 55)

    for P in periods:
        for snr_db in snr_levels:
            sc, mc, rc = [], [], []
            snr_label = f"{snr_db}dB" if snr_db != float('inf') else "clean"

            for trial in range(n_signal_trials):
                rng = np.random.RandomState(trial * 1000 + P)
                x = generate_periodic_signal(P, N, snr_db, rng)

                sc.append(detect_period_rpt(x, cq, seq_order, P, Q, N))
                mc.append(detect_period_rpt(x, cq, mertens_order, P, Q, N))

                tr = []
                for rt in range(n_random_trials):
                    ro = list(q_values)
                    np.random.RandomState(trial*10000+rt).shuffle(ro)
                    tr.append(detect_period_rpt(x, cq, ro, P, Q, N))
                rc.append(np.mean(tr))

            as_ = np.mean(sc); am = np.mean(mc); ar = np.mean(rc)
            rms = am/as_ if as_ > 0 else 999
            rrs = ar/as_ if as_ > 0 else 999
            all_ms_2.append(rms); all_rs_2.append(rrs)
            v = "GO" if rms < 0.80 else ("NO-GO" if rms >= 0.90 else "MARGIN")

            print(f"{P:>4} {snr_label:>5} {as_:>6.1f} {am:>6.1f} {ar:>7.1f} "
                  f"{rms:>5.2f}x {rrs:>5.2f}x {v:>7}")

            results["test2_rpt"].append({
                "period": P, "snr_db": snr_db if snr_db != float('inf') else "inf",
                "avg_seq": round(float(as_),2), "avg_mertens": round(float(am),2),
                "avg_random": round(float(ar),2),
                "ratio_ms": round(float(rms),4), "ratio_rs": round(float(rrs),4),
                "verdict": v
            })

    ov2 = np.mean(all_ms_2)
    print(f"\nTest 2 mean M/S: {ov2:.4f} -> {'GO' if ov2<0.80 else ('NO-GO' if ov2>=0.90 else 'MARGINAL')}")

    # ═══ FINAL SUMMARY ═══
    go_1 = sum(1 for r in all_ms_1 if r < 0.80)
    nogo_1 = sum(1 for r in all_ms_1 if r >= 0.90)
    go_2 = sum(1 for r in all_ms_2 if r < 0.80)
    nogo_2 = sum(1 for r in all_ms_2 if r >= 0.90)

    best = min(ov1, ov2)
    overall = "GO" if best < 0.80 else ("NO-GO" if best >= 0.90 else "MARGINAL")

    print(f"\n{'='*72}")
    print("FINAL SUMMARY")
    print(f"{'='*72}")
    print(f"Test 1 (direct):  M/S = {ov1:.4f}  GO={go_1}/{len(all_ms_1)}  NO-GO={nogo_1}/{len(all_ms_1)}")
    print(f"Test 2 (RPT):     M/S = {ov2:.4f}  GO={go_2}/{len(all_ms_2)}  NO-GO={nogo_2}/{len(all_ms_2)}")
    print(f"\nM(q) vs Random (Test 1): {ov1/np.mean(all_rs_1):.4f}x")
    print(f"M(q) vs Random (Test 2): {ov2/np.mean(all_rs_2):.4f}x")
    print(f"\nOVERALL VERDICT: {overall}")

    if overall == "NO-GO":
        print("\nDiagnosis: M(q)-ordering provides no meaningful speedup over")
        print("sequential ordering for Ramanujan filter bank period detection.")
        print("The position of a prime P in the M(q)-ordering is essentially")
        print("random with respect to detection utility.")
    elif overall == "GO":
        print("\nM(q)-ordering provides >20% savings in filters-to-detection!")
    else:
        print("\nResults are inconclusive (between 80-90% of sequential).")

    results["summary"] = {
        "test1_mean_ms": round(float(ov1), 4),
        "test1_mean_rs": round(float(np.mean(all_rs_1)), 4),
        "test1_go": go_1, "test1_nogo": nogo_1,
        "test2_mean_ms": round(float(ov2), 4),
        "test2_mean_rs": round(float(np.mean(all_rs_2)), 4),
        "test2_go": go_2, "test2_nogo": nogo_2,
        "overall_verdict": overall
    }

    outpath = "/Users/saar/Desktop/Farey-Local/experiments/ramanujan_filter_results.json"
    with open(outpath, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {outpath}")

if __name__ == "__main__":
    run_experiment()
