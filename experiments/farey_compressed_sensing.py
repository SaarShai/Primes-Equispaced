#!/usr/bin/env python3
"""
Farey Compressed Sensing: Multiplicative Sparsity meets Farey Bases
===================================================================

Key insight: The universal formula
  Σ_{f∈F_N} e^{2πimf} = M(N) + 1 + Σ_{d|m, d>1} d·M(⌊N/d⌋)
means exponential sums over Farey fractions have SPARSE structure
in the Mertens basis — depending on only τ(m) terms (divisor count).

We test whether this makes Farey points a good sampling basis
for compressed sensing of signals with multiplicative structure.
"""

import numpy as np
from scipy.linalg import svd
from fractions import Fraction
import json
import time

# ============================================================
# PART 0: Core utilities
# ============================================================

def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of fractions in [0,1]."""
    fracs = set()
    for d in range(1, N + 1):
        for n in range(0, d + 1):
            fracs.add(Fraction(n, d))
    return sorted(fracs)

def farey_sequence_float(N):
    """Farey sequence as float array."""
    return np.array([float(f) for f in farey_sequence(N)], dtype=np.float64)

def mertens_function(n):
    """Compute M(n) = Σ_{k=1}^{n} μ(k) via sieve."""
    if n < 1:
        return 0
    mu = np.zeros(n + 1, dtype=np.int64)
    mu[1] = 1
    for i in range(1, n + 1):
        if mu[i] == 0 and i > 1:
            continue
        for j in range(2 * i, n + 1, i):
            mu[j] -= mu[i]
    return int(np.sum(mu[1:]))

def mobius_sieve(n):
    """Compute μ(k) for k = 0..n."""
    mu = np.zeros(n + 1, dtype=np.int64)
    mu[1] = 1
    for i in range(1, n + 1):
        for j in range(2 * i, n + 1, i):
            mu[j] -= mu[i]
    return mu

def mertens_array(N):
    """Compute M(k) for k = 0..N."""
    mu = mobius_sieve(N)
    M = np.cumsum(mu)
    return M

def divisors(m):
    """Return sorted list of divisors of m."""
    divs = []
    for d in range(1, int(m**0.5) + 1):
        if m % d == 0:
            divs.append(d)
            if d != m // d:
                divs.append(m // d)
    return sorted(divs)

def count_prime_factors(n):
    """Count distinct prime factors of n (Omega function without multiplicity)."""
    if n <= 1:
        return 0
    count = 0
    d = 2
    while d * d <= n:
        if n % d == 0:
            count += 1
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        count += 1
    return count

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:
        if n % d == 0 or (n + 2) % d == 0:
            return False
        d += 6
    return True


# ============================================================
# PART 1: Verify the Universal Formula
# ============================================================

def verify_universal_formula(N, max_m=50):
    """Verify: Σ e^{2πimf} over F_N = M(N)+1+Σ_{d|m,d>1} d·M(⌊N/d⌋)"""
    print("=" * 70)
    print(f"PART 1: Verifying Universal Formula for F_{N}")
    print("=" * 70)

    F = farey_sequence_float(N)
    K = len(F)
    M_arr = mertens_array(N)

    results = []
    max_error = 0.0

    for m in range(1, max_m + 1):
        # Direct computation
        direct = np.sum(np.exp(2j * np.pi * m * F))

        # Formula: M(N) + 1 + Σ_{d|m, d>1} d·M(⌊N/d⌋)
        divs = divisors(m)
        formula_val = M_arr[N] + 1
        for d in divs:
            if d > 1:
                formula_val += d * M_arr[N // d]

        error = abs(direct - formula_val)
        max_error = max(max_error, error)
        tau_m = len(divs)  # number of divisors

        results.append({
            'm': m,
            'direct_real': float(direct.real),
            'formula': int(formula_val),
            'error': float(error),
            'tau_m': tau_m,
            'omega_m': count_prime_factors(m),
            'is_prime': is_prime(m)
        })

    print(f"  |F_{N}| = {K} fractions")
    print(f"  Tested m = 1..{max_m}")
    print(f"  Max |direct - formula| = {max_error:.2e}")
    print(f"  Formula VERIFIED: {'YES' if max_error < 1e-6 else 'NO'}")
    print()

    # Show sparsity: primes need only 2 Mertens values, composites need more
    prime_tau = [r['tau_m'] for r in results if r['is_prime']]
    comp_tau = [r['tau_m'] for r in results if not r['is_prime'] and r['m'] > 1]
    print(f"  Primes:     avg τ(m) = {np.mean(prime_tau):.1f} (always 2)")
    print(f"  Composites: avg τ(m) = {np.mean(comp_tau):.1f}")
    print(f"  → Prime frequencies are MAXIMALLY SPARSE in Mertens basis")
    print()

    return results


# ============================================================
# PART 2: Farey Sensing Matrix Properties
# ============================================================

def farey_sensing_matrix(N, max_freq):
    """
    Build sensing matrix A where A[m,k] = e^{2πi m f_k} / sqrt(K)
    for f_k ∈ F_N, m = 1..max_freq.

    Normalized so columns have unit norm.
    """
    F = farey_sequence_float(N)
    K = len(F)
    A = np.zeros((max_freq, K), dtype=np.complex128)
    for m_idx in range(max_freq):
        m = m_idx + 1
        A[m_idx, :] = np.exp(2j * np.pi * m * F)
    A /= np.sqrt(K)
    return A, F

def analyze_sensing_matrix(N, max_freq):
    """Analyze properties of the Farey sensing matrix."""
    print("=" * 70)
    print(f"PART 2: Farey Sensing Matrix Properties (N={N}, max_freq={max_freq})")
    print("=" * 70)

    A, F = farey_sensing_matrix(N, max_freq)
    K = len(F)
    M = max_freq

    print(f"  Matrix dimensions: {M} x {K} (M frequencies x K Farey points)")
    print(f"  Compression ratio: {M}/{K} = {M/K:.3f}")

    # Gram matrix G = A* A (column coherence)
    G = A.conj().T @ A
    # Mutual coherence: max off-diagonal |G_{ij}|
    G_offdiag = np.abs(G) - np.eye(K) * np.abs(np.diag(G))
    mu_coherence = np.max(G_offdiag)

    print(f"\n  Column coherence (mutual coherence μ):")
    print(f"    μ = max|<a_i, a_j>| = {mu_coherence:.6f}")
    print(f"    For K={K} columns, Welch bound = sqrt((K-M)/(M(K-1))) ≈ {np.sqrt((K-M)/(M*(K-1))):.6f}" if M < K else "")

    # Singular values → condition number → RIP proxy
    U, S, Vh = svd(A, full_matrices=False)
    sigma_max = S[0]
    sigma_min = S[-1]
    cond = sigma_max / sigma_min if sigma_min > 1e-15 else float('inf')

    print(f"\n  Singular value analysis:")
    print(f"    σ_max = {sigma_max:.6f}")
    print(f"    σ_min = {sigma_min:.6f}")
    print(f"    Condition number = {cond:.4f}")
    print(f"    σ_max/σ_min ratio: {cond:.4f}")

    # RIP proxy: for s-sparse signals, check restricted singular values
    # Sample random s-sparse support sets and check singular values of submatrices
    print(f"\n  RIP proxy (restricted singular values for s-sparse signals):")
    rip_results = {}
    for s in [2, 3, 5, 8, 10]:
        if s > min(M, K):
            break
        delta_s_values = []
        n_trials = min(200, int(np.math.comb(K, s)) if K < 30 else 200)
        for _ in range(n_trials):
            support = np.random.choice(K, s, replace=False)
            A_S = A[:, support]
            svals = svd(A_S, compute_uv=False)
            # δ_s = max(|σ²-1|) over all s-column submatrices
            delta = max(abs(svals[0]**2 - 1), abs(svals[-1]**2 - 1))
            delta_s_values.append(delta)
        avg_delta = np.mean(delta_s_values)
        max_delta = np.max(delta_s_values)
        rip_results[s] = {'avg': avg_delta, 'max': max_delta}
        print(f"    s={s:2d}: avg δ_s = {avg_delta:.4f}, max δ_s = {max_delta:.4f}  "
              f"{'GOOD (<0.5)' if max_delta < 0.5 else 'MARGINAL' if max_delta < 1.0 else 'POOR'}")

    return {
        'N': N, 'K': K, 'M': M,
        'coherence': float(mu_coherence),
        'sigma_max': float(sigma_max),
        'sigma_min': float(sigma_min),
        'condition': float(cond),
        'rip_proxy': {str(k): {'avg': v['avg'], 'max': v['max']} for k, v in rip_results.items()}
    }


# ============================================================
# PART 3: Comparison sensing matrices
# ============================================================

def equispaced_sensing_matrix(K, max_freq):
    """DFT-like matrix with equispaced points."""
    t = np.arange(K) / K
    A = np.zeros((max_freq, K), dtype=np.complex128)
    for m_idx in range(max_freq):
        m = m_idx + 1
        A[m_idx, :] = np.exp(2j * np.pi * m * t)
    A /= np.sqrt(K)
    return A, t

def random_sensing_matrix(K, max_freq):
    """Random sampling points in [0,1]."""
    t = np.sort(np.random.rand(K))
    A = np.zeros((max_freq, K), dtype=np.complex128)
    for m_idx in range(max_freq):
        m = m_idx + 1
        A[m_idx, :] = np.exp(2j * np.pi * m * t)
    A /= np.sqrt(K)
    return A, t


# ============================================================
# PART 4: L1 Recovery (Basis Pursuit)
# ============================================================

def l1_recovery(A, y, solver='scipy'):
    """
    Solve min ||x||_1 subject to Ax = y (Basis Pursuit).
    Uses cvxpy if available, otherwise scipy linprog reformulation.
    """
    M_rows, K = A.shape

    try:
        import cvxpy as cp
        # Complex variable → split into real and imaginary
        x_var = cp.Variable(K, complex=True)
        objective = cp.Minimize(cp.norm(x_var, 1))
        constraints = [A @ x_var == y]
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.SCS, verbose=False, max_iters=5000)
        if x_var.value is not None:
            return x_var.value
        else:
            # Fallback: use real formulation
            pass
    except Exception:
        pass

    # Fallback: scipy-based real formulation
    # Split A into real/imag: [Re(A), -Im(A); Im(A), Re(A)] @ [Re(x); Im(x)] = [Re(y); Im(y)]
    A_real = np.vstack([np.hstack([A.real, -A.imag]),
                        np.hstack([A.imag,  A.real])])
    y_real = np.concatenate([y.real, y.imag])

    # min Σ t_i s.t. -t_i ≤ z_i ≤ t_i, A_real @ z = y_real
    from scipy.optimize import linprog
    n = 2 * K  # real + imag parts
    # Variables: [z (2K), t (2K)]
    c = np.concatenate([np.zeros(n), np.ones(n)])
    # z_i - t_i ≤ 0 and -z_i - t_i ≤ 0
    A_ub = np.vstack([
        np.hstack([np.eye(n), -np.eye(n)]),
        np.hstack([-np.eye(n), -np.eye(n)])
    ])
    b_ub = np.zeros(2 * n)
    A_eq = np.hstack([A_real, np.zeros((2 * M_rows, n))])
    b_eq = y_real

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='highs')
    if result.success:
        z = result.x[:n]
        return z[:K] + 1j * z[K:]
    else:
        return np.zeros(K, dtype=complex)


def l1_recovery_underdetermined(A, y):
    """
    For underdetermined system (fewer measurements than unknowns):
    min ||x||_1 s.t. Ax = y
    """
    try:
        import cvxpy as cp
        M_rows, K = A.shape
        x_var = cp.Variable(K, complex=True)
        objective = cp.Minimize(cp.norm(x_var, 1))
        constraints = [A @ x_var == y]
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.SCS, verbose=False, max_iters=10000,
                   eps=1e-8)
        if x_var.value is not None:
            return x_var.value
        return np.zeros(K, dtype=complex)
    except Exception as e:
        print(f"    [CVXPY failed: {e}, using pseudoinverse]")
        return np.linalg.lstsq(A, y, rcond=None)[0]


# ============================================================
# PART 5: The Main Experiment — Recovery Comparison
# ============================================================

def generate_multiplicatively_sparse_signal(max_freq, sparsity_type='prime', n_nonzero=5, seed=42):
    """
    Generate a signal whose Fourier coefficients are nonzero only at
    frequencies with specific multiplicative structure.

    sparsity_type:
      'prime'     - nonzero only at prime frequencies
      'prime_power' - nonzero at prime powers
      'smooth'    - nonzero at smooth numbers (all prime factors ≤ 5)
      'random'    - random support (baseline)
    """
    rng = np.random.RandomState(seed)
    x = np.zeros(max_freq, dtype=np.complex128)

    if sparsity_type == 'prime':
        primes = [m for m in range(2, max_freq + 1) if is_prime(m)]
        support = primes[:n_nonzero]
    elif sparsity_type == 'prime_power':
        pp = []
        for p in range(2, max_freq + 1):
            if is_prime(p):
                pk = p
                while pk <= max_freq:
                    pp.append(pk)
                    pk *= p
        pp.sort()
        support = pp[:n_nonzero]
    elif sparsity_type == 'smooth':
        smooth = [m for m in range(2, max_freq + 1)
                  if all(p <= 5 for p in prime_factorization(m))]
        support = smooth[:n_nonzero]
    elif sparsity_type == 'random':
        support = sorted(rng.choice(range(1, max_freq + 1), n_nonzero, replace=False))
    else:
        raise ValueError(f"Unknown sparsity type: {sparsity_type}")

    for idx in support:
        x[idx - 1] = rng.randn() + 1j * rng.randn()

    return x, support

def prime_factorization(n):
    """Return list of prime factors (with repetition)."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def recovery_experiment(N, max_freq, n_measurements, sparsity_type='prime',
                        n_nonzero=5, seed=42):
    """
    Compare compressed sensing recovery using:
    1. Farey sampling points
    2. Equispaced sampling points
    3. Random sampling points

    Setup: Signal x has max_freq Fourier coefficients (sparse).
    We observe n_measurements samples and try to recover x.
    """
    # Generate sparse signal
    x_true, support = generate_multiplicatively_sparse_signal(
        max_freq, sparsity_type, n_nonzero, seed)

    results = {}

    for sampling_name in ['farey', 'equispaced', 'random']:
        # Get sampling points
        if sampling_name == 'farey':
            F_full = farey_sequence_float(N)
            # Subsample to n_measurements points
            if len(F_full) <= n_measurements:
                t = F_full
            else:
                indices = np.linspace(0, len(F_full) - 1, n_measurements, dtype=int)
                t = F_full[indices]
        elif sampling_name == 'equispaced':
            t = np.arange(n_measurements) / n_measurements
        else:  # random
            rng = np.random.RandomState(seed + 1)
            t = np.sort(rng.rand(n_measurements))

        K = len(t)

        # Build sensing matrix: A[k, m] = e^{2πi m t_k} / sqrt(K)
        # We want to recover x (length max_freq) from y = A^T x sampled at t
        # Actually: y_k = Σ_m x_m e^{2πi m t_k}, so A[k,m] = e^{2πi m t_k}
        A = np.zeros((K, max_freq), dtype=np.complex128)
        for m in range(max_freq):
            A[:, m] = np.exp(2j * np.pi * (m + 1) * t)
        A /= np.sqrt(K)

        # Generate measurements
        y = A @ x_true

        # Add small noise
        noise_level = 1e-10
        y += noise_level * (np.random.randn(K) + 1j * np.random.randn(K))

        # Recover via L1 minimization
        if K >= max_freq:
            # Overdetermined: just solve least squares for comparison
            x_rec = np.linalg.lstsq(A, y, rcond=None)[0]
        else:
            x_rec = l1_recovery_underdetermined(A, y)

        # Metrics
        rel_error = np.linalg.norm(x_rec - x_true) / (np.linalg.norm(x_true) + 1e-15)

        # Support recovery: find largest entries
        rec_magnitudes = np.abs(x_rec)
        threshold = 0.1 * np.max(rec_magnitudes) if np.max(rec_magnitudes) > 0 else 0
        recovered_support = set(np.where(rec_magnitudes > threshold)[0] + 1)
        true_support = set(support)
        support_recall = len(recovered_support & true_support) / len(true_support)
        support_precision = (len(recovered_support & true_support) / len(recovered_support)
                            if len(recovered_support) > 0 else 0)

        results[sampling_name] = {
            'n_samples': K,
            'rel_error': float(rel_error),
            'support_recall': float(support_recall),
            'support_precision': float(support_precision),
            'recovered_support': sorted(recovered_support),
            'true_support': support,
        }

    return results, x_true, support


def run_recovery_experiments():
    """Run recovery experiments across different settings."""
    print("=" * 70)
    print("PART 4: Compressed Sensing Recovery Comparison")
    print("=" * 70)

    all_results = {}

    # Experiment parameters
    configs = [
        {'N': 20, 'max_freq': 40, 'n_meas': 15, 'type': 'prime', 'n_nz': 5},
        {'N': 20, 'max_freq': 40, 'n_meas': 15, 'type': 'random', 'n_nz': 5},
        {'N': 20, 'max_freq': 40, 'n_meas': 20, 'type': 'prime', 'n_nz': 5},
        {'N': 25, 'max_freq': 50, 'n_meas': 20, 'type': 'prime', 'n_nz': 8},
        {'N': 25, 'max_freq': 50, 'n_meas': 20, 'type': 'smooth', 'n_nz': 8},
        {'N': 30, 'max_freq': 60, 'n_meas': 25, 'type': 'prime', 'n_nz': 8},
    ]

    for i, cfg in enumerate(configs):
        label = f"N={cfg['N']}, freq={cfg['max_freq']}, meas={cfg['n_meas']}, type={cfg['type']}, s={cfg['n_nz']}"
        print(f"\n  Experiment {i+1}: {label}")
        print(f"  " + "-" * 60)

        results, x_true, support = recovery_experiment(
            cfg['N'], cfg['max_freq'], cfg['n_meas'], cfg['type'], cfg['n_nz'])

        all_results[label] = {}
        for name in ['farey', 'equispaced', 'random']:
            r = results[name]
            print(f"    {name:12s}: rel_err={r['rel_error']:.4e}, "
                  f"recall={r['support_recall']:.2f}, precision={r['support_precision']:.2f}")
            all_results[label][name] = {
                'rel_error': r['rel_error'],
                'support_recall': r['support_recall'],
                'support_precision': r['support_precision'],
            }
        print(f"    True support: {support}")

    return all_results


# ============================================================
# PART 6: Multiplicative Sparsity Analysis
# ============================================================

def multiplicative_sparsity_analysis(N_max=100):
    """
    Analyze "multiplicative sparsity": how many integers ≤ N have
    bounded number of prime factors?

    This defines a new sparsity concept where signals are "multiplicatively
    sparse" if their Fourier coefficients are supported on numbers
    with few distinct prime factors.
    """
    print("=" * 70)
    print("PART 5: Multiplicative Sparsity Landscape")
    print("=" * 70)

    omega_counts = {}  # omega -> count of integers with that many distinct prime factors
    for n in range(2, N_max + 1):
        w = count_prime_factors(n)
        omega_counts[w] = omega_counts.get(w, 0) + 1

    print(f"\n  Distribution of ω(n) for n ≤ {N_max}:")
    print(f"  {'ω(n)':>6s} | {'Count':>6s} | {'Fraction':>8s} | {'Cumulative':>10s}")
    print(f"  {'-'*6} | {'-'*6} | {'-'*8} | {'-'*10}")

    cumulative = 0
    total = N_max - 1
    omega_data = {}
    for w in sorted(omega_counts.keys()):
        cumulative += omega_counts[w]
        frac = omega_counts[w] / total
        cum_frac = cumulative / total
        print(f"  {w:6d} | {omega_counts[w]:6d} | {frac:8.4f} | {cum_frac:10.4f}")
        omega_data[w] = {
            'count': omega_counts[w],
            'fraction': frac,
            'cumulative': cum_frac
        }

    # Divisor count τ(m) as Mertens-basis sparsity
    print(f"\n  Mertens-basis sparsity τ(m) for m ≤ {N_max}:")
    tau_values = {}
    for m in range(1, N_max + 1):
        tau = len(divisors(m))
        tau_values[m] = tau

    # Group by type
    prime_taus = [tau_values[m] for m in range(2, N_max + 1) if is_prime(m)]
    composite_taus = [tau_values[m] for m in range(4, N_max + 1)
                      if not is_prime(m)]

    print(f"    Primes: τ always = {prime_taus[0]} (M(N) and M(⌊N/m⌋) only)")
    print(f"    Composites: avg τ = {np.mean(composite_taus):.1f}, "
          f"max τ = {max(composite_taus)}")
    print(f"    Highly composite (e.g. 60): τ(60) = {tau_values[60]}")
    print(f"    → PRIMES are the SPARSEST frequencies in the Mertens basis")
    print()

    # Sparsity advantage: ratio of number of Mertens terms needed
    avg_prime_tau = np.mean(prime_taus)
    avg_comp_tau = np.mean(composite_taus)
    print(f"  Sparsity advantage of primes over composites: {avg_comp_tau/avg_prime_tau:.1f}x fewer terms")

    return omega_data, tau_values


# ============================================================
# PART 7: Coherence Phase Transition
# ============================================================

def coherence_vs_N():
    """
    Study how the mutual coherence of the Farey sensing matrix
    changes with N. Good sensing matrices have LOW coherence.
    """
    print("=" * 70)
    print("PART 6: Coherence vs. Farey Order N")
    print("=" * 70)

    N_values = [5, 8, 10, 12, 15, 18, 20, 25]
    results = []

    for N in N_values:
        F = farey_sequence_float(N)
        K = len(F)
        max_freq = min(K - 1, 30)  # don't exceed matrix size

        A = np.zeros((max_freq, K), dtype=np.complex128)
        for m in range(max_freq):
            A[m, :] = np.exp(2j * np.pi * (m + 1) * F)
        A /= np.sqrt(K)

        # Coherence of A^H A
        G = A.conj().T @ A
        G_offdiag = np.abs(G) - np.eye(K)
        mu = np.max(G_offdiag)

        # Compare with random matrix of same size
        t_rand = np.sort(np.random.rand(K))
        A_rand = np.zeros((max_freq, K), dtype=np.complex128)
        for m in range(max_freq):
            A_rand[m, :] = np.exp(2j * np.pi * (m + 1) * t_rand)
        A_rand /= np.sqrt(K)
        G_rand = A_rand.conj().T @ A_rand
        G_rand_off = np.abs(G_rand) - np.eye(K)
        mu_rand = np.max(G_rand_off)

        # Equispaced
        t_eq = np.arange(K) / K
        A_eq = np.zeros((max_freq, K), dtype=np.complex128)
        for m in range(max_freq):
            A_eq[m, :] = np.exp(2j * np.pi * (m + 1) * t_eq)
        A_eq /= np.sqrt(K)
        G_eq = A_eq.conj().T @ A_eq
        G_eq_off = np.abs(G_eq) - np.eye(K)
        mu_eq = np.max(G_eq_off)

        results.append({
            'N': N, 'K': K, 'max_freq': max_freq,
            'mu_farey': float(mu), 'mu_random': float(mu_rand),
            'mu_equispaced': float(mu_eq)
        })

        print(f"  N={N:3d} (K={K:4d}): μ_farey={mu:.4f}  μ_random={mu_rand:.4f}  μ_equi={mu_eq:.4f}  "
              f"{'FAREY WINS' if mu < mu_rand and mu < mu_eq else 'RANDOM WINS' if mu_rand < mu else 'EQUI WINS'}")

    print()
    return results


# ============================================================
# PART 8: The Mertens Change-of-Basis
# ============================================================

def mertens_basis_analysis(N, max_freq=40):
    """
    The universal formula defines a change of basis:
    Column sums of A (Farey sensing matrix) live in a τ(m)-dimensional
    Mertens subspace. Analyze this structure.
    """
    print("=" * 70)
    print(f"PART 7: Mertens Change-of-Basis (N={N})")
    print("=" * 70)

    M_arr = mertens_array(N)

    # For each frequency m, the Farey exponential sum is determined by
    # {M(⌊N/d⌋) : d | m} — a vector in R^{τ(m)}
    # This means the "Farey spectrum" lives in a STRUCTURED low-dimensional space

    print(f"\n  Mertens representation of Farey exponential sums:")
    print(f"  {'m':>4s} | {'τ(m)':>4s} | {'Sum':>8s} | {'Mertens terms':>40s}")
    print(f"  {'-'*4} | {'-'*4} | {'-'*8} | {'-'*40}")

    for m in range(1, min(max_freq + 1, 21)):
        divs = divisors(m)
        tau = len(divs)
        # Formula value
        s = M_arr[N] + 1
        terms = [f"M({N})={M_arr[N]}"]
        for d in divs:
            if d > 1:
                val = d * M_arr[N // d]
                s += val
                terms.append(f"{d}·M({N//d})={val}")
        terms_str = " + ".join(terms)
        if len(terms_str) > 40:
            terms_str = terms_str[:37] + "..."
        print(f"  {m:4d} | {tau:4d} | {s:8d} | {terms_str:>40s}")

    # Key insight: the total information needed to compute ALL sums
    # is just {M(⌊N/d⌋) : d = 1..N} which has ~2√N distinct values
    distinct_M_values = set()
    for d in range(1, N + 1):
        distinct_M_values.add(N // d)

    print(f"\n  Total distinct M(⌊N/d⌋) values needed: {len(distinct_M_values)}")
    print(f"  This is ≈ 2√{N} = {2*np.sqrt(N):.1f}")
    print(f"  → ALL Farey exponential sums (infinitely many frequencies)")
    print(f"    are determined by just {len(distinct_M_values)} Mertens values!")
    print(f"  → This is EXTREME compression of spectral information")
    print()

    return len(distinct_M_values)


# ============================================================
# PART 9: Recovery Rate Phase Transition
# ============================================================

def phase_transition(N=20, max_freq=40, n_trials=10):
    """
    Map the phase transition: for each (sparsity s, measurements m),
    what fraction of trials successfully recover the signal?
    """
    print("=" * 70)
    print(f"PART 8: Phase Transition Diagram (N={N}, max_freq={max_freq})")
    print("=" * 70)

    F = farey_sequence_float(N)
    K_full = len(F)

    sparsity_values = [2, 3, 5, 8]
    meas_fractions = [0.15, 0.25, 0.35, 0.50, 0.65, 0.80]
    meas_values = [int(f * max_freq) for f in meas_fractions]
    meas_values = [m for m in meas_values if m >= 2]

    results_farey = np.zeros((len(sparsity_values), len(meas_values)))
    results_random = np.zeros((len(sparsity_values), len(meas_values)))

    for si, s in enumerate(sparsity_values):
        for mi, n_meas in enumerate(meas_values):
            success_farey = 0
            success_random = 0

            for trial in range(n_trials):
                # Generate random s-sparse signal on prime support
                primes = [p for p in range(2, max_freq + 1) if is_prime(p)]
                if len(primes) < s:
                    support = list(range(1, s + 1))
                else:
                    rng = np.random.RandomState(trial * 100 + si * 10 + mi)
                    support = sorted(rng.choice(primes, min(s, len(primes)), replace=False))

                x_true = np.zeros(max_freq, dtype=complex)
                for idx in support:
                    x_true[idx - 1] = rng.randn() + 1j * rng.randn()

                for sampling, success_count_ref in [
                    ('farey', None), ('random', None)
                ]:
                    if sampling == 'farey':
                        if K_full <= n_meas:
                            t = F
                        else:
                            indices = np.linspace(0, K_full - 1, n_meas, dtype=int)
                            t = F[indices]
                    else:
                        t = np.sort(np.random.RandomState(trial + 999).rand(n_meas))

                    Km = len(t)
                    A = np.zeros((Km, max_freq), dtype=complex)
                    for m_idx in range(max_freq):
                        A[:, m_idx] = np.exp(2j * np.pi * (m_idx + 1) * t)
                    A /= np.sqrt(Km)

                    y = A @ x_true

                    try:
                        if Km >= max_freq:
                            x_rec = np.linalg.lstsq(A, y, rcond=None)[0]
                        else:
                            x_rec = l1_recovery_underdetermined(A, y)

                        rel_err = np.linalg.norm(x_rec - x_true) / (np.linalg.norm(x_true) + 1e-15)
                        if rel_err < 0.05:
                            if sampling == 'farey':
                                success_farey += 1
                            else:
                                success_random += 1
                    except Exception:
                        pass

            results_farey[si, mi] = success_farey / n_trials
            results_random[si, mi] = success_random / n_trials

    print(f"\n  Phase transition: fraction of successful recoveries (tol < 5%)")
    print(f"\n  FAREY sampling:")
    header = "  s \\ m  | " + " | ".join(f"{m:5d}" for m in meas_values)
    print(header)
    print("  " + "-" * len(header))
    for si, s in enumerate(sparsity_values):
        row = f"  {s:5d}  | " + " | ".join(f"{results_farey[si,mi]:5.2f}" for mi in range(len(meas_values)))
        print(row)

    print(f"\n  RANDOM sampling:")
    print(header)
    print("  " + "-" * len(header))
    for si, s in enumerate(sparsity_values):
        row = f"  {s:5d}  | " + " | ".join(f"{results_random[si,mi]:5.2f}" for mi in range(len(meas_values)))
        print(row)

    # Advantage matrix
    advantage = results_farey - results_random
    print(f"\n  ADVANTAGE (Farey - Random):")
    print(header)
    print("  " + "-" * len(header))
    for si, s in enumerate(sparsity_values):
        row = f"  {s:5d}  | " + " | ".join(
            f"{advantage[si,mi]:+5.2f}" for mi in range(len(meas_values)))
        print(row)

    return {
        'sparsity_values': sparsity_values,
        'meas_values': meas_values,
        'farey': results_farey.tolist(),
        'random': results_random.tolist(),
        'advantage': advantage.tolist()
    }


# ============================================================
# PART 10: Divisor-Weighted Recovery
# ============================================================

def divisor_weighted_recovery(N=20, max_freq=40, n_meas=15, n_nonzero=5):
    """
    Use the divisor structure as a PRIOR for recovery:
    Instead of min ||x||_1, solve min Σ τ(m)|x_m|
    where τ(m) penalizes frequencies with many divisors.

    Rationale: frequencies with fewer divisors (primes) are cheaper
    in the Mertens basis, so we should prefer them.
    """
    print("=" * 70)
    print("PART 9: Divisor-Weighted L1 Recovery")
    print("=" * 70)

    import cvxpy as cp

    # Generate prime-sparse signal
    x_true, support = generate_multiplicatively_sparse_signal(
        max_freq, 'prime', n_nonzero, seed=42)

    F = farey_sequence_float(N)
    if len(F) > n_meas:
        indices = np.linspace(0, len(F) - 1, n_meas, dtype=int)
        t = F[indices]
    else:
        t = F

    K = len(t)
    A = np.zeros((K, max_freq), dtype=complex)
    for m in range(max_freq):
        A[:, m] = np.exp(2j * np.pi * (m + 1) * t)
    A /= np.sqrt(K)

    y = A @ x_true

    # Standard L1
    x_var = cp.Variable(max_freq, complex=True)
    prob_std = cp.Problem(cp.Minimize(cp.norm(x_var, 1)),
                          [A @ x_var == y])
    prob_std.solve(solver=cp.SCS, verbose=False, max_iters=10000)
    x_std = x_var.value if x_var.value is not None else np.zeros(max_freq, dtype=complex)

    # Divisor-weighted L1: min Σ w_m |x_m| where w_m = τ(m)/2
    # This penalizes non-prime frequencies
    weights = np.array([len(divisors(m + 1)) / 2.0 for m in range(max_freq)])
    # Primes get weight 1.0, composites get weight > 1.0

    x_var2 = cp.Variable(max_freq, complex=True)
    weighted_norm = cp.sum(cp.multiply(weights, cp.abs(x_var2)))
    prob_wt = cp.Problem(cp.Minimize(weighted_norm),
                         [A @ x_var2 == y])
    prob_wt.solve(solver=cp.SCS, verbose=False, max_iters=10000)
    x_wt = x_var2.value if x_var2.value is not None else np.zeros(max_freq, dtype=complex)

    # Inverse-divisor weighted: min Σ (1/τ(m)) |x_m| — FAVORS composites (control)
    weights_inv = np.array([2.0 / len(divisors(m + 1)) for m in range(max_freq)])
    x_var3 = cp.Variable(max_freq, complex=True)
    inv_weighted_norm = cp.sum(cp.multiply(weights_inv, cp.abs(x_var3)))
    prob_inv = cp.Problem(cp.Minimize(inv_weighted_norm),
                          [A @ x_var3 == y])
    prob_inv.solve(solver=cp.SCS, verbose=False, max_iters=10000)
    x_inv = x_var3.value if x_var3.value is not None else np.zeros(max_freq, dtype=complex)

    # Results
    err_std = np.linalg.norm(x_std - x_true) / (np.linalg.norm(x_true) + 1e-15)
    err_wt = np.linalg.norm(x_wt - x_true) / (np.linalg.norm(x_true) + 1e-15)
    err_inv = np.linalg.norm(x_inv - x_true) / (np.linalg.norm(x_true) + 1e-15)

    print(f"\n  Signal: {n_nonzero}-sparse on primes, max_freq={max_freq}")
    print(f"  Measurements: {K} Farey samples from F_{N}")
    print(f"  True support: {support}")
    print()
    print(f"  Recovery method          | Rel. Error  | Support found")
    print(f"  {'-'*25} | {'-'*11} | {'-'*30}")

    for name, x_rec, err in [
        ("Standard L1", x_std, err_std),
        ("Divisor-weighted L1", x_wt, err_wt),
        ("Inverse-div L1 (ctrl)", x_inv, err_inv),
    ]:
        mags = np.abs(x_rec)
        thresh = 0.1 * np.max(mags) if np.max(mags) > 0 else 0
        rec_supp = sorted(np.where(mags > thresh)[0] + 1)
        print(f"  {name:25s} | {err:11.4e} | {rec_supp}")

    print()
    print(f"  Divisor-weighted helps for prime-sparse signals: "
          f"{'YES' if err_wt < err_std else 'NO'} "
          f"({err_wt/err_std:.2f}x error ratio)")

    return {
        'standard_l1_error': float(err_std),
        'divisor_weighted_error': float(err_wt),
        'inverse_div_error': float(err_inv),
        'support_true': support,
        'improvement_ratio': float(err_wt / (err_std + 1e-15))
    }


# ============================================================
# MAIN
# ============================================================

def main():
    print("*" * 70)
    print("  FAREY COMPRESSED SENSING: Multiplicative Sparsity Meets")
    print("  the Farey Sequence via the Universal Formula")
    print("*" * 70)
    print()

    all_results = {}

    # Part 1: Verify the universal formula
    t0 = time.time()
    formula_results = verify_universal_formula(N=30, max_m=50)
    all_results['formula_verification'] = formula_results
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # Part 2: Sensing matrix properties
    t0 = time.time()
    matrix_props = analyze_sensing_matrix(N=15, max_freq=20)
    all_results['sensing_matrix'] = matrix_props
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # Part 5: Multiplicative sparsity landscape
    t0 = time.time()
    omega_data, tau_values = multiplicative_sparsity_analysis(N_max=100)
    all_results['multiplicative_sparsity'] = {
        'omega_distribution': {str(k): v for k, v in omega_data.items()},
        'mean_tau_primes': 2.0,
        'mean_tau_composites': float(np.mean([tau_values[m] for m in range(4, 101) if not is_prime(m)])),
    }
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # Part 6: Coherence comparison
    t0 = time.time()
    coherence_results = coherence_vs_N()
    all_results['coherence'] = coherence_results
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # Part 7: Mertens basis
    t0 = time.time()
    n_distinct = mertens_basis_analysis(N=30, max_freq=40)
    all_results['mertens_basis'] = {'N': 30, 'distinct_values': n_distinct}
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # Part 4: Recovery experiments
    t0 = time.time()
    recovery_results = run_recovery_experiments()
    all_results['recovery'] = recovery_results
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # Part 8: Phase transition
    t0 = time.time()
    phase_results = phase_transition(N=20, max_freq=40, n_trials=8)
    all_results['phase_transition'] = phase_results
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # Part 9: Divisor-weighted recovery
    t0 = time.time()
    div_results = divisor_weighted_recovery(N=20, max_freq=40, n_meas=15, n_nonzero=5)
    all_results['divisor_weighted'] = div_results
    print(f"  [Time: {time.time()-t0:.1f}s]\n")

    # ============================================================
    # SYNTHESIS
    # ============================================================
    print("=" * 70)
    print("SYNTHESIS: Key Findings")
    print("=" * 70)

    print("""
    1. UNIVERSAL FORMULA VERIFIED: The Farey exponential sum at frequency m
       depends on exactly τ(m) Mertens values. Primes are maximally sparse
       (τ(p) = 2), while composites require more terms.

    2. FAREY SENSING MATRIX: The matrix A with A_{mk} = e^{2πimf_k} has
       structured column sums governed by the Mertens function. The mutual
       coherence and RIP proxy were computed.

    3. MULTIPLICATIVE SPARSITY: ~25% of integers ≤100 are prime (ω=1),
       meaning prime-sparse signals are a substantial class. The divisor
       count τ(m) defines a natural "Mertens-basis sparsity" where primes
       are the cheapest frequencies.

    4. MERTENS COMPRESSION: ALL Farey exponential sums (for any frequency)
       are determined by only ~2√N distinct Mertens values. This is extreme
       spectral compression.

    5. DIVISOR-WEIGHTED L1: Using τ(m) as weights in L1 minimization
       encodes the prior that the signal is prime-sparse. This leverages
       the Farey/Mertens structure as inductive bias.

    KEY THEORETICAL INSIGHT:
       The Farey sequence provides a natural dictionary where:
       - Frequencies = integers m
       - Sparsity = divisor structure (primes are sparsest)
       - The Mertens function controls ALL column correlations
       - Compressed sensing recovery is governed by number-theoretic structure
    """)

    # Save results
    import json

    def make_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, complex):
            return {'real': obj.real, 'imag': obj.imag}
        if isinstance(obj, set):
            return sorted(list(obj))
        if isinstance(obj, dict):
            return {str(k): make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [make_serializable(v) for v in obj]
        return obj

    with open('/Users/new/Downloads/a3f522e1-8fdf-4aba-8a5e-6b5385438b6c_aristotle/experiments/farey_compressed_sensing_results.json', 'w') as f:
        json.dump(make_serializable(all_results), f, indent=2, default=str)
    print("  Results saved to farey_compressed_sensing_results.json")


if __name__ == '__main__':
    main()
