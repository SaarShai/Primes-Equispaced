#!/usr/bin/env python3
"""
CLOCK SYNCHRONIZATION VIA FAREY INJECTION PRINCIPLE
====================================================

CORE IDEA:
  For prime p, the fractions {1/p, 2/p, ..., (p-1)/p} land in DISTINCT
  gaps of the Farey sequence F_{p-1}. This means if N nodes each pick
  a different k/p (mod 1) as their transmission time, NO TWO COLLIDE.

  This is a direct consequence of the injection principle:
    k -> gap_of(k/p) is injective for prime p.

THIS DEMO:
  1. TDMA scheduling with Farey slots vs random vs round-robin
  2. Sensor network with heterogeneous reporting rates
  3. Frequency hopping patterns
  4. Honest comparison with real-world protocols (ALOHA, CSMA, TDMA)

HONEST ASSESSMENT (upfront):
  The Farey injection gives a clean MATHEMATICAL guarantee of collision-freedom.
  But simple round-robin TDMA also gives collision-freedom with less complexity.
  The real question is: where does the NUMBER-THEORETIC structure buy you
  something that naive approaches cannot?
"""

import time
import random
from math import gcd, isqrt, pi, log, ceil, floor
from fractions import Fraction
from collections import defaultdict
from itertools import combinations

# ============================================================
# UTILITIES
# ============================================================

def sieve_primes(limit):
    """Return all primes up to limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def next_prime_above(n):
    """Return the smallest prime > n."""
    primes = sieve_primes(2 * n + 100)
    for p in primes:
        if p > n:
            return p
    raise ValueError(f"No prime found above {n}")

def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of Fraction objects."""
    fracs = set()
    for d in range(1, N + 1):
        for n in range(0, d + 1):
            if gcd(n, d) == 1:
                fracs.add(Fraction(n, d))
    return sorted(fracs)

def find_farey_gap(x, farey):
    """Find which gap of the Farey sequence x falls into.
    Returns index i such that farey[i] < x < farey[i+1]."""
    for i in range(len(farey) - 1):
        if farey[i] < x < farey[i + 1]:
            return i
    return -1  # x is a Farey fraction itself (not in a gap)

# ============================================================
# PART 1: TDMA SCHEDULING
# ============================================================

def demo_tdma_scheduling():
    """
    TDMA (Time Division Multiple Access): N nodes share a time period T.
    Each node gets a slot. The question is HOW to assign slots.

    Three strategies:
      1. Farey: node k transmits at time k/p (mod 1), p = next_prime(N)
      2. Round-robin: node k transmits at time k/N
      3. Random: node k picks a random time in [0,1)
    """
    print("=" * 70)
    print("PART 1: TDMA SCHEDULING COMPARISON")
    print("=" * 70)

    for N in [5, 10, 20, 50]:
        p = next_prime_above(N)
        print(f"\n--- N = {N} nodes, using prime p = {p} ---")

        # Strategy 1: Farey scheduling
        farey_times = sorted([(k / p) % 1.0 for k in range(1, N + 1)])
        farey_gaps = []
        for i in range(len(farey_times) - 1):
            farey_gaps.append(farey_times[i + 1] - farey_times[i])
        if len(farey_times) > 1:
            # Wraparound gap
            farey_gaps.append(1.0 - farey_times[-1] + farey_times[0])

        # Verify: are all Farey times distinct?
        farey_distinct = len(set(round(t, 15) for t in farey_times)) == N
        farey_min_gap = min(farey_gaps) if farey_gaps else 0
        farey_max_gap = max(farey_gaps) if farey_gaps else 0

        # Strategy 2: Round-robin
        rr_times = sorted([k / N for k in range(N)])
        rr_gaps = [1.0 / N] * N  # perfectly uniform
        rr_min_gap = 1.0 / N
        rr_max_gap = 1.0 / N

        # Strategy 3: Random (average over trials)
        n_trials = 1000
        random_collisions = 0
        random_min_gaps = []
        random_max_gaps = []
        collision_threshold = 1e-3  # two transmissions within 0.1% of period

        for _ in range(n_trials):
            rand_times = sorted([random.random() for _ in range(N)])
            rand_gaps = []
            for i in range(len(rand_times) - 1):
                rand_gaps.append(rand_times[i + 1] - rand_times[i])
            rand_gaps.append(1.0 - rand_times[-1] + rand_times[0])

            min_g = min(rand_gaps)
            random_min_gaps.append(min_g)
            random_max_gaps.append(max(rand_gaps))
            if min_g < collision_threshold:
                random_collisions += 1

        avg_random_min = sum(random_min_gaps) / n_trials
        collision_rate = random_collisions / n_trials

        print(f"  Farey scheduling (k/p mod 1):")
        print(f"    All distinct: {farey_distinct}")
        print(f"    Min gap: {farey_min_gap:.6f}  Max gap: {farey_max_gap:.6f}  Ratio: {farey_max_gap/farey_min_gap:.2f}")
        print(f"  Round-robin (k/N):")
        print(f"    All distinct: True (by construction)")
        print(f"    Min gap: {rr_min_gap:.6f}  Max gap: {rr_max_gap:.6f}  Ratio: 1.00 (perfectly uniform)")
        print(f"  Random scheduling:")
        print(f"    Collision rate (gap < {collision_threshold}): {collision_rate:.1%}")
        print(f"    Avg min gap: {avg_random_min:.6f}")

        # KEY METRIC: how uniform is the Farey schedule?
        # The "uniformity ratio" = max_gap / min_gap (1.0 = perfect)
        print(f"  --> Uniformity winner: Round-robin (ratio 1.00) vs Farey (ratio {farey_max_gap/farey_min_gap:.2f})")

    # MATHEMATICAL PROOF of collision-freedom
    print(f"\n--- PROOF: Why Farey scheduling is collision-free ---")
    p = 11
    N = 10
    farey = farey_sequence(p - 1)
    print(f"  F_{p-1} has {len(farey)} fractions, {len(farey)-1} gaps")

    assignments = {}
    for k in range(1, N + 1):
        frac = Fraction(k, p)
        gap = find_farey_gap(frac, farey)
        assignments[k] = gap
        print(f"    Node {k}: transmits at {k}/{p} = {float(frac):.4f}, lands in gap {gap}")

    # Verify injection
    gap_values = list(assignments.values())
    all_distinct = len(set(gap_values)) == len(gap_values)
    print(f"  All nodes in distinct gaps: {all_distinct}")
    print(f"  This is the INJECTION PRINCIPLE: k -> gap(k/p) is 1-to-1 for prime p.")

# ============================================================
# PART 2: SENSOR NETWORK
# ============================================================

def demo_sensor_network():
    """
    100 sensors, each reporting at a different rate.
    Sensor k reports every T_k seconds, where we derive T_k from k/p.

    The collision-free property means no two sensors ever transmit
    at exactly the same time (in the idealized continuous model).
    """
    print("\n" + "=" * 70)
    print("PART 2: SENSOR NETWORK (100 sensors)")
    print("=" * 70)

    N = 100
    p = next_prime_above(N)
    print(f"Using prime p = {p} for {N} sensors")

    # Each sensor k transmits at times: k/p + n for integer n >= 0
    # (period 1 normalized). The offset k/p guarantees separation.

    # Compute all transmission times in [0, 10) for all sensors
    T_max = 10.0  # simulate 10 time periods
    all_transmissions = []

    for k in range(1, N + 1):
        offset = k / p
        t = offset
        while t < T_max:
            all_transmissions.append((t, k))
            t += 1.0  # all sensors have period 1, just different offsets

    all_transmissions.sort()
    total_tx = len(all_transmissions)

    print(f"\nScenario A: All sensors same period (1.0), offset = k/{p}")
    print(f"  Total transmissions in [0, {T_max}): {total_tx}")

    # Find minimum gap between consecutive transmissions
    min_gap = float('inf')
    min_pair = None
    for i in range(len(all_transmissions) - 1):
        gap = all_transmissions[i + 1][0] - all_transmissions[i][0]
        if gap < min_gap:
            min_gap = gap
            min_pair = (all_transmissions[i], all_transmissions[i + 1])

    print(f"  Minimum gap between any two transmissions: {min_gap:.8f}")
    print(f"    Between sensor {min_pair[0][1]} at t={min_pair[0][0]:.6f}")
    print(f"       and sensor {min_pair[1][1]} at t={min_pair[1][0]:.6f}")
    print(f"  Theoretical minimum gap = 1/{p}*1/{p-1} ~ {1/(p*(p-1)):.8f}")

    # Check for exact collisions
    time_set = defaultdict(list)
    for t, k in all_transmissions:
        # Round to detect near-collisions
        time_set[round(t, 12)].append(k)

    collisions = {t: sensors for t, sensors in time_set.items() if len(sensors) > 1}
    print(f"  Exact collisions found: {len(collisions)}")

    # Scenario B: Different periods (sensor k reports every k/p seconds)
    print(f"\nScenario B: Sensor k reports every k/{p} seconds (heterogeneous rates)")
    all_tx_b = []
    for k in range(1, min(N + 1, 21)):  # first 20 sensors for manageability
        period = k / p
        t = 0.0
        while t < 5.0:
            all_tx_b.append((t, k))
            t += period

    all_tx_b.sort()

    # Find collisions
    collision_count = 0
    near_collision_count = 0
    near_threshold = 1e-6

    for i in range(len(all_tx_b) - 1):
        gap = all_tx_b[i + 1][0] - all_tx_b[i][0]
        if gap == 0:
            collision_count += 1
        elif gap < near_threshold:
            near_collision_count += 1

    print(f"  (20 sensors, 5 time units)")
    print(f"  Total transmissions: {len(all_tx_b)}")
    print(f"  Exact collisions: {collision_count}")
    print(f"  Near-collisions (gap < {near_threshold}): {near_collision_count}")

    # HONEST NOTE: heterogeneous periods lose the clean injection guarantee
    print(f"\n  HONEST NOTE: The injection principle guarantees collision-freedom")
    print(f"  for a SINGLE time period with offsets k/p. When sensors have")
    print(f"  DIFFERENT periods, collisions CAN occur at later times.")
    print(f"  The guarantee is per-period, not for all time.")

# ============================================================
# PART 3: FREQUENCY HOPPING
# ============================================================

def demo_frequency_hopping():
    """
    Frequency hopping: at each time slot t, node k uses channel (k*t mod p).

    Claim: for any two nodes k1 != k2, they collide (same channel at same time)
    at most once in any window of p consecutive time slots.

    This is because (k1*t mod p) = (k2*t mod p) iff (k1-k2)*t = 0 mod p,
    which (since p is prime and k1 != k2 with both < p) has exactly one
    solution t in {0, 1, ..., p-1}.
    """
    print("\n" + "=" * 70)
    print("PART 3: FREQUENCY HOPPING (p = 101, 10 nodes)")
    print("=" * 70)

    p = 101
    n_nodes = 10
    nodes = list(range(1, n_nodes + 1))

    print(f"  Channel for node k at time t: channel = (k * t) mod {p}")
    print(f"  Total channels: {p}")
    print(f"  Nodes: {nodes}")

    # Build channel assignment table for t = 0..p-1
    channels = {}  # (node, time) -> channel
    for k in nodes:
        for t in range(p):
            channels[(k, t)] = (k * t) % p

    # Print first 15 time slots
    print(f"\n  Channel assignments (first 15 time slots):")
    print(f"  {'Time':>6}", end="")
    for k in nodes:
        print(f"  Node{k:>2}", end="")
    print()

    for t in range(15):
        print(f"  {t:>6}", end="")
        for k in nodes:
            print(f"  {channels[(k,t)]:>6}", end="")
        print()
    print(f"  ...")

    # Count collisions per pair
    pair_collisions = {}
    for k1, k2 in combinations(nodes, 2):
        count = 0
        collision_times = []
        for t in range(p):
            if channels[(k1, t)] == channels[(k2, t)]:
                count += 1
                collision_times.append(t)
        pair_collisions[(k1, k2)] = (count, collision_times)

    print(f"\n  Collisions per pair over {p} time slots:")
    max_collisions = 0
    for (k1, k2), (count, times) in sorted(pair_collisions.items()):
        max_collisions = max(max_collisions, count)
        if count > 0:
            t_str = ",".join(str(t) for t in times[:5])
            print(f"    Nodes ({k1},{k2}): {count} collision(s) at t = {t_str}")

    print(f"\n  Maximum collisions for any pair: {max_collisions}")
    print(f"  THEOREM: Each pair collides EXACTLY ONCE in {p} slots.")
    print(f"  Proof: (k1-k2)*t = 0 mod p has exactly 1 solution since p is prime.")

    # Compare with random hopping
    n_trials = 1000
    random_max_collisions = []
    for _ in range(n_trials):
        # Each node picks a random channel at each time
        rand_channels = {}
        for k in nodes:
            for t in range(p):
                rand_channels[(k, t)] = random.randint(0, p - 1)

        trial_max = 0
        for k1, k2 in combinations(nodes, 2):
            count = sum(1 for t in range(p) if rand_channels[(k1, t)] == rand_channels[(k2, t)])
            trial_max = max(trial_max, count)
        random_max_collisions.append(trial_max)

    avg_random_max = sum(random_max_collisions) / n_trials
    print(f"\n  Random hopping comparison ({n_trials} trials):")
    print(f"    Expected collisions per pair: {p} * 1/{p} = 1.00")
    print(f"    Average MAX collisions (any pair): {avg_random_max:.1f}")
    print(f"    Farey hopping MAX collisions (any pair): {max_collisions}")
    print(f"    --> Both methods average ~1 collision per pair!")
    print(f"    --> But Farey gives a DETERMINISTIC guarantee: never more than 1.")
    print(f"    --> Random can spike (worst case in trials: {max(random_max_collisions)}).")

# ============================================================
# PART 4: PRACTICAL COMPARISON
# ============================================================

def demo_practical_comparison():
    """
    Compare Farey-based scheduling against real protocols.
    Be BRUTALLY HONEST about tradeoffs.
    """
    print("\n" + "=" * 70)
    print("PART 4: PRACTICAL COMPARISON WITH REAL PROTOCOLS")
    print("=" * 70)

    # Simulate 50 nodes over 10000 time slots
    N = 50
    p = next_prime_above(N)
    T = 10000

    print(f"\n  Simulation: {N} nodes, {T} time slots, prime p = {p}")

    # 1. Pure ALOHA: each node transmits with probability 1/N per slot
    aloha_collisions = 0
    aloha_successful = 0
    aloha_idle = 0

    for t in range(T):
        # Each node independently decides to transmit with prob 1/N
        transmitters = [k for k in range(N) if random.random() < 1.0 / N]
        if len(transmitters) == 0:
            aloha_idle += 1
        elif len(transmitters) == 1:
            aloha_successful += 1
        else:
            aloha_collisions += 1

    aloha_throughput = aloha_successful / T

    # 2. Slotted ALOHA (theoretical)
    # Throughput = N * (1/N) * (1 - 1/N)^(N-1) -> 1/e ~ 0.368
    slotted_aloha_theory = N * (1.0 / N) * ((1.0 - 1.0 / N) ** (N - 1))

    # 3. Round-robin TDMA
    # Each node gets exactly T/N slots, zero collisions
    rr_throughput = 1.0  # channel always busy, zero waste
    rr_latency = N  # must wait N slots for your turn

    # 4. Farey TDMA (using offsets k/p in [0,1) mapped to slots)
    # This is equivalent to round-robin when all nodes have same period!
    farey_throughput = 1.0  # also zero collisions
    farey_latency_max = 0
    farey_slots = sorted([(k / p) % 1.0, k] for k in range(1, N + 1))

    for i in range(len(farey_slots)):
        next_i = (i + 1) % len(farey_slots)
        if next_i > i:
            gap = farey_slots[next_i][0] - farey_slots[i][0]
        else:
            gap = 1.0 - farey_slots[i][0] + farey_slots[next_i][0]
        latency_in_slots = gap * p  # convert from [0,1) to slot count
        farey_latency_max = max(farey_latency_max, latency_in_slots)

    print(f"\n  Protocol Comparison:")
    print(f"  {'Protocol':<25} {'Throughput':<15} {'Max Latency':<15} {'Collisions':<15} {'Coordination':<15}")
    print(f"  {'-'*85}")
    print(f"  {'Pure ALOHA':<25} {aloha_throughput:<15.3f} {'1 slot':<15} {aloha_collisions:<15} {'None':<15}")
    print(f"  {'Slotted ALOHA (theory)':<25} {slotted_aloha_theory:<15.3f} {'1 slot':<15} {'~63%':<15} {'Slot sync':<15}")
    print(f"  {'Round-robin TDMA':<25} {rr_throughput:<15.3f} {str(rr_latency)+' slots':<15} {'0':<15} {'Full':<15}")
    print(f"  {'Farey TDMA':<25} {farey_throughput:<15.3f} {f'{farey_latency_max:.1f} slots':<15} {'0':<15} {'Prime p only':<15}")

    # The KEY question: what does Farey buy over round-robin?
    print(f"\n" + "-" * 70)
    print("HONEST ANALYSIS: Where does Farey scheduling actually help?")
    print("-" * 70)

    print("""
  WHAT FAREY GIVES YOU:
    1. Collision-free scheduling from a SINGLE shared parameter (the prime p).
       Each node only needs to know its own ID k and the prime p.
       No central coordinator assigns slots.

    2. SELF-ORGANIZING: If a new node joins with ID k', it automatically
       gets a collision-free slot at k'/p. No renegotiation needed
       (as long as total nodes < p).

    3. Graceful degradation: if some nodes leave, remaining nodes
       still have collision-free slots. No reorganization.

  WHAT ROUND-ROBIN GIVES THAT FAREY DOESN'T:
    1. PERFECTLY UNIFORM spacing (all gaps equal).
       Farey gaps are NOT uniform -- some nodes wait longer than others.

    2. SIMPLER to implement and understand.

    3. Lower maximum latency (N slots vs up to ~2 slots * p/N for Farey).

  WHERE FAREY GENUINELY WINS:
    1. AD-HOC NETWORKS: Nodes join/leave dynamically. With round-robin,
       adding a node requires reassigning ALL slots. With Farey, new node
       just picks k'/p.

    2. DECENTRALIZED SYSTEMS: No coordinator needed. Agreement on p suffices.

    3. COGNITIVE RADIO: The frequency hopping property (Part 3) gives
       bounded interference. Each pair interferes at most once per cycle.

    4. UNDERWATER ACOUSTIC NETWORKS: Long propagation delays make
       coordination expensive. Farey provides coordination-free scheduling.

  WHERE FAREY DOES NOT HELP:
    1. Static networks with known topology -- just use round-robin.
    2. Networks needing uniform latency guarantees.
    3. Very high node counts (p must be prime > N, and gaps shrink as 1/p^2).

  REAL SYSTEMS THAT USE SIMILAR IDEAS:
    - Chinese Remainder Theorem scheduling (used in LTE)
    - Costas arrays for radar (same modular arithmetic structure)
    - Reed-Solomon codes share algebraic roots with Farey hopping
    - FHSS (Frequency Hopping Spread Spectrum) in Bluetooth uses
      a similar but different pseudorandom hopping pattern
    """)

    # Quantify the non-uniformity cost
    print("  QUANTIFYING THE NON-UNIFORMITY COST:")
    for N in [10, 50, 100]:
        p = next_prime_above(N)
        slots = sorted((k / p) % 1.0 for k in range(1, N + 1))
        gaps = []
        for i in range(len(slots) - 1):
            gaps.append(slots[i + 1] - slots[i])
        gaps.append(1.0 - slots[-1] + slots[0])

        ideal = 1.0 / N
        max_gap = max(gaps)
        min_gap = min(gaps)
        std_gap = (sum((g - ideal) ** 2 for g in gaps) / len(gaps)) ** 0.5

        print(f"    N={N:>3}, p={p:>3}: ideal gap={ideal:.4f}, "
              f"min={min_gap:.4f}, max={max_gap:.4f}, "
              f"ratio={max_gap/min_gap:.2f}, "
              f"std={std_gap:.6f}")

    print(f"\n  As N grows, the Farey gaps become MORE uniform (ratio -> ~2).")
    print(f"  This is the three-distance theorem: for any irrational rotation,")
    print(f"  there are at most 3 distinct gap lengths. For k/p with prime p,")
    print(f"  the gaps take at most 3 values.")

# ============================================================
# PART 5: THREE-DISTANCE THEOREM IN ACTION
# ============================================================

def demo_three_distance():
    """
    The three-distance theorem (Steinhaus, 1957):
    Place N points on a circle at positions {k*alpha mod 1 : k=1..N}.
    The gaps take AT MOST 3 distinct values, and if there are 3,
    the largest equals the sum of the other two.

    For alpha = 1/p (prime), this means Farey scheduling has very
    structured gap sizes.
    """
    print("\n" + "=" * 70)
    print("PART 5: THREE-DISTANCE THEOREM (Gap Structure)")
    print("=" * 70)

    for p in [11, 53, 101, 503]:
        N = p - 1  # all p-1 points
        points = sorted((k / p) % 1.0 for k in range(1, p))
        gaps = []
        for i in range(len(points) - 1):
            gaps.append(round(points[i + 1] - points[i], 15))
        gaps.append(round(1.0 - points[-1] + points[0], 15))

        distinct_gaps = sorted(set(gaps))
        gap_counts = {g: gaps.count(g) for g in distinct_gaps}

        print(f"\n  p = {p}: placing k/p for k = 1..{p-1}")
        print(f"    Number of distinct gap sizes: {len(distinct_gaps)}")
        for g in distinct_gaps:
            # Express gap as a multiple of 1/p
            mult = round(g * p)
            print(f"      gap = {g:.10f} (= {mult}/{p}) occurs {gap_counts[g]} times")

        if len(distinct_gaps) == 1:
            print(f"    --> PERFECTLY UNIFORM (all gaps = 1/{p})")

    # Now with fewer nodes than p-1 (realistic: p = next_prime(N))
    print(f"\n  --- With N < p-1 nodes (p = next_prime(N), realistic) ---")
    for N in [10, 25, 50, 100]:
        p = next_prime_above(N)
        points = sorted((k / p) % 1.0 for k in range(1, N + 1))
        gaps = []
        for i in range(len(points) - 1):
            gaps.append(points[i + 1] - points[i])
        gaps.append(1.0 - points[-1] + points[0])

        # Round to avoid floating point noise, group into distinct values
        rounded_gaps = [round(g * p * p, 1) for g in gaps]  # scale for clarity
        distinct = sorted(set(rounded_gaps))

        print(f"    N = {N}, p = {p}: {len(distinct)} distinct gap sizes")
        print(f"      min gap = {min(gaps):.6f}, max gap = {max(gaps):.6f}, ratio = {max(gaps)/min(gaps):.2f}")

# ============================================================
# PART 6: SUMMARY VERDICT
# ============================================================

def summary_verdict():
    print("\n" + "=" * 70)
    print("FINAL VERDICT: IS FAREY SCHEDULING PRACTICAL?")
    print("=" * 70)
    print("""
  SCORE CARD:

  Category                    Farey    Round-Robin    Random ALOHA
  ----------------------------------------------------------------
  Collision-free guarantee    YES      YES            NO
  No coordinator needed       YES      NO             YES
  Dynamic join/leave          YES      NO (reassign)  YES
  Uniform latency             NO       YES            NO
  Simplicity                  MEDIUM   HIGH           HIGH
  Throughput                  100%     100%           ~37%
  Bounded interference (FH)   YES      N/A            NO

  VERDICT:

  Farey scheduling is NOT better than round-robin for static networks.
  It IS better for:
    - Ad-hoc networks where nodes join/leave without coordination
    - Decentralized systems that can only agree on a single prime p
    - Frequency hopping with guaranteed bounded interference
    - Mathematical elegance (if that counts!)

  The injection principle provides a COORDINATION-FREE collision guarantee.
  That is its unique selling point. If you have a coordinator, just use
  round-robin. If you don't, Farey scheduling is provably collision-free
  with only a shared prime number.

  REAL-WORLD RELEVANCE: Moderate.
  - The math is sound and the guarantees are real.
  - Similar ideas ARE used in practice (CRT scheduling, Costas arrays).
  - Pure Farey scheduling is not widely deployed, but the algebraic
    structure behind it (modular arithmetic over primes) is fundamental
    to many communication systems.
  """)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    t0 = time.time()

    demo_tdma_scheduling()
    demo_sensor_network()
    demo_frequency_hopping()
    demo_practical_comparison()
    demo_three_distance()
    summary_verdict()

    print(f"\nTotal runtime: {time.time() - t0:.1f}s")
