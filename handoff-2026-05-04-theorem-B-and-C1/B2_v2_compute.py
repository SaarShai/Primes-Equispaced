#!/usr/bin/env python3
"""B2 v2: pin α_ratio with today's tools.

Plan:
1. Compute integrals I_ON = ∫|M_W(iy)|²(1-sinc²(πy))dy and I_OFF = ∫(1-sinc²(πy))dy
   over a large window. Predicted ON/OFF ratio = 2.3147.
2. Fresh CUE MC at K=10³, with mollifier ON, scaled by Λ_K² = log²K.
   Compute c_∞_emp = E[|S|²]_ON / (log K)^p for p ∈ {0,1,2}.
3. Test α_ratio rational candidates: {1, 1/2, 1/3, 1/π, 2/π, 1/π², 1/(2π), 1/(2π²)}.
4. Cross-validate: compute c_∞_emp at K=300, K=1000, K=3000 — log-K stability test.

Today's tools applied:
- Orthogonal Plancherel mult = 1 (vs unitary 3): for Petersson AT-ZEROS this gives
  the factor (1+1)/(1+3) = 1/2 against ζ. But for BULK CUE Palm, R₂ is universal:
  α_ratio is the SAME constant in unitary and orthogonal cases. So α_ratio is
  determined PURELY by Snaith's CUE derivative ratio g(0).
- Snaith 2008 normalized 2nd-derivative moment: at θ=0 with a CUE pin,
  E[|Z'(θ_i)|²] = (N²/12)·(2π)²·... — computable.
- The N→∞ bulk limit converts |Z'(θ_i)|²/E[|Z'|²] → 1 a.s. for fixed CUE, so the
  ratio g(y) → 1 at bulk scaling away from y=0; at y→0 the singularity is killed
  by (1−sinc²(πy)) ~ (πy)²/3 vanishing.
- Therefore α_ratio = 1 (unconditionally, after correct normalization).
"""
import numpy as np
import time
from scipy.integrate import quad

# ----- 1. Theoretical integrals -----
def MW(y):
    w = 1j*y
    return (1 - np.exp(-1 - w))/(1 + w)

def MW_sq(y):
    return abs(MW(y))**2

def kernel_pair(y):
    # 1 - sinc²(πy); numpy sinc(x) = sin(πx)/(πx), so sinc(y) = sin(πy)/(πy).
    return 1.0 - np.sinc(y)**2

def integrand_ON(y):
    return MW_sq(y) * kernel_pair(y)

def integrand_OFF(y):
    return kernel_pair(y)

# OFF integral diverges — we need it cut off; in the MC the cutoff is N
# (number of eigenvalues). For theory, the OFF baseline is set to the
# continuous CUE pair density (1 - sinc²) integrated over compact support.
# But for the ratio, the natural finite-cutoff comparison is what the MC sees.

print("="*60)
print("Step 1: theoretical integrals")
print("="*60)
I_ON, _ = quad(integrand_ON, -50, 50, limit=200)
print(f"∫|M_W(iy)|²(1-sinc²(πy)) dy [|y|<50]  = {I_ON:.6f}")
# Cross-check tail
I_ON_100, _ = quad(integrand_ON, -100, 100, limit=400)
print(f"∫|M_W(iy)|²(1-sinc²(πy)) dy [|y|<100] = {I_ON_100:.6f}")

# Compute ∫|M_W|² alone (no kernel)
I_MW_only, _ = quad(MW_sq, -50, 50, limit=200)
print(f"∫|M_W(iy)|² dy [|y|<50] = {I_MW_only:.6f}")

# Compute ratio ON/MW_only — this measures how much (1-sinc²) cuts down |M_W|²
print(f"ratio ON/MW_only = {I_ON/I_MW_only:.6f}")

# The "predicted asymptotic ratio ON/OFF → 2.3147" from prior MC code:
# In the MC, OFF means mollifier = 1 (constant), and the sum is over N-1 angles.
# E[|Σ_{j≠i} e^{i log K · (θ_j - θ_i)}|²] in the bulk-scaling limit
# = ∫(1-sinc²(πy))dy_finite = N (with high-y cutoff)... need MC to see this.

# ----- 2. Fresh CUE MC at multiple K -----
print()
print("="*60)
print("Step 2: fresh CUE MC")
print("="*60)

def cue_eigenangles(N, rng):
    G = rng.standard_normal((N, N))
    H = rng.standard_normal((N, N))
    M = (G + 1j*H)/np.sqrt(2)
    Q, R = np.linalg.qr(M)
    d = np.diag(R)
    Q = Q * (d/np.abs(d))
    return np.sort(np.angle(np.linalg.eigvals(Q)))

def MW_array(y):
    w = 1j*y
    return (1 - np.exp(-1 - w))/(1 + w)

def compute_S(angles, idx, K, mollifier_on=True):
    diffs = angles - angles[idx]
    log_K = np.log(K)
    mask = np.arange(len(angles)) != idx
    d_raw = diffs[mask]
    # bulk scaling: y = N · d_raw / (2π)
    N_local = len(angles)
    y = N_local * d_raw / (2*np.pi)
    phase = np.exp(1j * log_K * d_raw)
    if mollifier_on:
        mw = MW_array(y)
    else:
        mw = np.ones_like(y, dtype=complex)
    return np.sum(phase * mw)

rng = np.random.default_rng(2026)

# Run at K = 300, 1000, 3000 with N = 100*log(K)/log(1000) scaling
results = []
for K in [300, 1000, 3000]:
    # Use N = 30*log(K) so N grows but is computationally cheap
    N = max(80, int(30*np.log(K)))
    n_samples = 300 if K <= 1000 else 200
    on_vals, off_vals = [], []
    t0 = time.time()
    for _ in range(n_samples):
        ang = cue_eigenangles(N, rng)
        i_idx = N//2
        on_vals.append(abs(compute_S(ang, i_idx, K, True))**2)
        off_vals.append(abs(compute_S(ang, i_idx, K, False))**2)
    on_m = np.mean(on_vals); off_m = np.mean(off_vals)
    on_se = np.std(on_vals)/np.sqrt(n_samples)
    off_se = np.std(off_vals)/np.sqrt(n_samples)
    ratio = on_m/off_m
    dt = time.time() - t0
    log_K_val = np.log(K)
    # c_∞_emp computed from ON branch under hypothesis E|S|² ~ c_∞ · log K
    # (we test multiple powers of log K)
    c_inf_p0 = on_m
    c_inf_p1 = on_m / log_K_val
    c_inf_p2 = on_m / log_K_val**2
    c_inf_pm1 = on_m * log_K_val
    line = (f"K={K:5d} N={N:4d} samples={n_samples:3d} "
            f"ON={on_m:7.3f}±{on_se:.3f} OFF={off_m:7.3f}±{off_se:.3f} "
            f"ratio={ratio:.4f} c_∞[p=0]={c_inf_p0:.3f} c_∞[p=1]={c_inf_p1:.3f} "
            f"c_∞[p=2]={c_inf_p2:.4f} dt={dt:.0f}s")
    print(line, flush=True)
    results.append({'K': K, 'N': N, 'on': on_m, 'on_se': on_se, 'off': off_m,
                    'off_se': off_se, 'ratio': ratio, 'log_K': log_K_val})

# ----- 3. Pin α_ratio -----
print()
print("="*60)
print("Step 3: α_ratio inference")
print("="*60)
print(f"Predicted: c_∞ = α_ratio · I_ON = α_ratio · {I_ON:.4f}")
print(f"If on_m → c_∞ asymptotically (no log K factor): α_ratio = on_m / {I_ON:.4f}")
print()
for r in results:
    alpha_p0 = r['on'] / I_ON
    alpha_p1 = r['on'] / (r['log_K'] * I_ON)
    alpha_pm1 = r['on'] * r['log_K'] / I_ON
    print(f"K={r['K']}: α_ratio (assuming p=0) = {alpha_p0:.4f}, "
          f"(p=1, divide by log K) = {alpha_p1:.4f}, "
          f"(p=-1, mult by log K) = {alpha_pm1:.4f}")

# Test rational candidates against the most-stable empirical value
print()
print("Rational candidates for α_ratio:")
candidates = {
    '1':    1.0,
    '1/2':  0.5,
    '1/3':  1/3,
    '2/π':  2/np.pi,
    '1/π':  1/np.pi,
    '1/π²': 1/np.pi**2,
    '1/(2π)': 1/(2*np.pi),
    '1/(2π²)': 1/(2*np.pi**2),
    '6/π²': 6/np.pi**2,
}
for name, val in candidates.items():
    print(f"  α = {name} = {val:.4f}")

# ----- 4. log-K stability check -----
print()
print("="*60)
print("Step 4: log-K stability")
print("="*60)
if len(results) >= 2:
    r1, r2 = results[0], results[-1]
    # If on_m grows linearly in log K, ratio of on_m / log K is stable
    rat_on_p0 = r2['on']/r1['on']
    rat_log = r2['log_K']/r1['log_K']
    print(f"on(K={r2['K']})/on(K={r1['K']}) = {rat_on_p0:.4f}")
    print(f"log(K={r2['K']})/log(K={r1['K']}) = {rat_log:.4f}")
    if abs(rat_on_p0 - 1.0) < 0.1:
        print("→ on_m is FLAT in log K (p=0): α_ratio = on_m / I_ON")
    elif abs(rat_on_p0 - rat_log) < 0.1:
        print("→ on_m grows ~ log K (p=1)")
    elif abs(rat_on_p0 - rat_log**2) < 0.2:
        print("→ on_m grows ~ log² K (p=2)")
    else:
        print(f"→ ambiguous power: rat_on={rat_on_p0:.3f}, rat_log={rat_log:.3f}, "
              f"rat_log²={rat_log**2:.3f}")
