#!/usr/bin/env python3
"""
Fast orbit search for the most promising empty cell in the periodic table.
Uses coarse integration for screening, fine integration only for refinement.
"""

import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, differential_evolution
import time
import warnings
warnings.filterwarnings('ignore')

# Load data
with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_periodic_table.json') as f:
    table = json.load(f)

with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_exact_data.json') as f:
    exact_data = json.load(f)

results = exact_data['results']
orbits_by_id = {r['id']: r for r in results}

row_bins = table['metadata']['row_bins']
col_bins = table['metadata']['col_bins']
row_labels = [b['label'] for b in row_bins]
col_labels = [b['label'] for b in col_bins]

# Target cell: row=6-15, col=1.30-1.35 (most promising, 4 cardinal neighbors)
target_row = '6-15'
target_col = '1.30-1.35'

# Neighbor orbits
neighbor_ids = ['I.A-2', 'I.B-17', 'I.B-2', 'I.B-3', 'I.A-3', 'II.C-190', 'II.C-192']
neighbor_orbits = [orbits_by_id[oid] for oid in neighbor_ids if oid in orbits_by_id]

print("Target cell: row=6-15, col=1.30-1.35")
print(f"Neighbors: {len(neighbor_orbits)} orbits")
for o in neighbor_orbits:
    print(f"  {o['id']:12s}: v1={o['v1']:.10f}, v2={o['v2']:.10f}, T={o['T']:.6f}, wl={o['word_length']}")

# Also get ALL orbits in neighboring cells
def get_row_bin_label(period_length):
    for b in row_bins:
        if b['lo'] <= period_length <= b['hi']:
            return b['label']
    return None

def get_col_bin_label(gmean):
    for b in col_bins:
        if b['lo'] <= gmean < b['hi']:
            return b['label']
    if gmean >= col_bins[-1]['hi']:
        return col_bins[-1]['label']
    return None

neighbor_cell_keys = {
    ('2-5', '1.30-1.35'), ('16-30', '1.30-1.35'),
    ('6-15', '1.25-1.30'), ('6-15', '1.35-1.45'),
    ('2-5', '1.35-1.45'), ('16-30', '1.25-1.30'), ('16-30', '1.35-1.45'),
}

all_neighbor_orbits = []
for r in results:
    if r.get('period_not_found', False):
        continue
    rl = get_row_bin_label(r['cf_period_length'])
    cl = get_col_bin_label(r['cf_period_gmean'])
    if (rl, cl) in neighbor_cell_keys:
        all_neighbor_orbits.append(r)

print(f"Total orbits in neighboring cells: {len(all_neighbor_orbits)}")

# =============================================================================
# THREE-BODY INTEGRATOR
# =============================================================================
def threebody_rhs(t, state):
    x1, y1, x2, y2, x3, y3 = state[:6]
    vx1, vy1, vx2, vy2, vx3, vy3 = state[6:]

    dx12, dy12 = x2 - x1, y2 - y1
    dx13, dy13 = x3 - x1, y3 - y1
    dx23, dy23 = x3 - x2, y3 - y2

    r12_sq = dx12**2 + dy12**2
    r13_sq = dx13**2 + dy13**2
    r23_sq = dx23**2 + dy23**2

    r12_3 = r12_sq**1.5
    r13_3 = r13_sq**1.5
    r23_3 = r23_sq**1.5

    ax1 = dx12/r12_3 + dx13/r13_3
    ay1 = dy12/r12_3 + dy13/r13_3
    ax2 = -dx12/r12_3 + dx23/r23_3
    ay2 = -dy12/r12_3 + dy23/r23_3
    ax3 = -dx13/r13_3 - dx23/r23_3
    ay3 = -dy13/r13_3 - dy23/r23_3

    return [vx1, vy1, vx2, vy2, vx3, vy3, ax1, ay1, ax2, ay2, ax3, ay3]


def make_ic(vx, vy):
    return [-1.0, 0.0, 1.0, 0.0, 0.0, 0.0, vx, vy, vx, vy, -2*vx, -2*vy]


def return_error(vx, vy, T, rtol=1e-10, atol=1e-10):
    """Integrate and measure return error."""
    y0 = make_ic(vx, vy)
    try:
        sol = solve_ivp(threebody_rhs, [0, T], y0, method='DOP853',
                       rtol=rtol, atol=atol)
        if not sol.success:
            return 1e10
        yf = sol.y[:, -1]
        diff = np.array(yf) - np.array(y0)
        return np.sqrt(np.sum(diff**2))
    except Exception:
        return 1e10


def objective_coarse(params):
    vx, vy, T = params
    if T < 3 or T > 100:
        return 1e10
    return return_error(vx, vy, T, rtol=1e-8, atol=1e-8)


def objective_fine(params):
    vx, vy, T = params
    if T < 3 or T > 100:
        return 1e10
    return return_error(vx, vy, T, rtol=1e-12, atol=1e-12)


# =============================================================================
# VERIFY: Can we reproduce known orbits?
# =============================================================================
print("\n--- Verifying known orbits ---")
for o in neighbor_orbits[:3]:
    err = return_error(o['v1'], o['v2'], o['T'], rtol=1e-12, atol=1e-12)
    print(f"  {o['id']}: return_error = {err:.6e}")

# =============================================================================
# PHASE 1: Coarse screening with many starting points
# =============================================================================
print("\n--- Phase 1: Coarse screening ---")
t0 = time.time()

vxs = [o['v1'] for o in all_neighbor_orbits]
vys = [o['v2'] for o in all_neighbor_orbits]
Ts = [o['T'] for o in all_neighbor_orbits]

avg_vx, avg_vy, avg_T = np.mean(vxs), np.mean(vys), np.mean(Ts)
std_vx = max(np.std(vxs), 0.02)
std_vy = max(np.std(vys), 0.02)
std_T = max(np.std(Ts), 2.0)

print(f"  Center: vx={avg_vx:.6f}, vy={avg_vy:.6f}, T={avg_T:.3f}")
print(f"  Spread: std_vx={std_vx:.6f}, std_vy={std_vy:.6f}, std_T={std_T:.3f}")

np.random.seed(42)
candidates = []

# Try each neighbor orbit directly
for o in all_neighbor_orbits:
    err = objective_coarse([o['v1'], o['v2'], o['T']])
    if err < 5.0:
        candidates.append((err, o['v1'], o['v2'], o['T'], f"direct:{o['id']}"))

# Try perturbations around each neighbor
n_per_orbit = 30
for o in all_neighbor_orbits:
    for _ in range(n_per_orbit):
        dvx = np.random.normal(0, 0.03)
        dvy = np.random.normal(0, 0.03)
        dT = np.random.normal(0, 2.0)
        vx, vy, T = o['v1'] + dvx, o['v2'] + dvy, o['T'] + dT
        if T < 3: continue
        err = objective_coarse([vx, vy, T])
        if err < 5.0:
            candidates.append((err, vx, vy, T, f"perturb:{o['id']}"))

# Random in the interpolation region
for _ in range(200):
    vx = avg_vx + np.random.normal(0, std_vx * 0.7)
    vy = avg_vy + np.random.normal(0, std_vy * 0.7)
    T = avg_T + np.random.normal(0, std_T * 0.7)
    if T < 3: continue
    err = objective_coarse([vx, vy, T])
    if err < 5.0:
        candidates.append((err, vx, vy, T, "random"))

# Try a grid of T values with neighbor ICs
for o in neighbor_orbits:
    for T_mult in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]:
        T = o['T'] * T_mult
        if T < 3 or T > 100: continue
        err = objective_coarse([o['v1'], o['v2'], T])
        if err < 5.0:
            candidates.append((err, o['v1'], o['v2'], T, f"Tmult:{o['id']}x{T_mult}"))

candidates.sort()
t1 = time.time()
print(f"  Phase 1 done in {t1-t0:.1f}s, {len(candidates)} candidates with err < 5")
if candidates:
    print(f"  Best coarse error: {candidates[0][0]:.6e}")
    for c in candidates[:10]:
        print(f"    err={c[0]:.4e}, vx={c[1]:.8f}, vy={c[2]:.8f}, T={c[3]:.4f}, src={c[4]}")

# =============================================================================
# PHASE 2: Refine best candidates with Nelder-Mead
# =============================================================================
print("\n--- Phase 2: Local refinement ---")
best_error = 1e10
best_params = None

# Take top 30 candidates
for i, (err0, vx, vy, T, src) in enumerate(candidates[:30]):
    try:
        res = minimize(objective_coarse, [vx, vy, T],
                      method='Nelder-Mead',
                      options={'maxiter': 1000, 'xatol': 1e-10, 'fatol': 1e-14})
        if res.fun < best_error:
            best_error = res.fun
            best_params = res.x
            print(f"  #{i}: error={res.fun:.6e} (from {src}), "
                  f"vx={res.x[0]:.10f}, vy={res.x[1]:.10f}, T={res.x[2]:.6f}")
            if res.fun < 0.01:
                print(f"  *** FOUND at coarse level!")
    except:
        pass

t2 = time.time()
print(f"  Phase 2 done in {t2-t1:.1f}s, best error: {best_error:.6e}")

# =============================================================================
# PHASE 3: Fine refinement of the best result
# =============================================================================
if best_error < 1.0 and best_params is not None:
    print("\n--- Phase 3: Fine refinement ---")

    # Refine with high-precision integration
    try:
        res = minimize(objective_fine, best_params,
                      method='Nelder-Mead',
                      options={'maxiter': 2000, 'xatol': 1e-12, 'fatol': 1e-15})
        if res.fun < best_error:
            best_error = res.fun
            best_params = res.x
            print(f"  Nelder-Mead fine: error={res.fun:.6e}")
    except:
        pass

    try:
        res = minimize(objective_fine, best_params,
                      method='Powell',
                      options={'maxiter': 5000, 'ftol': 1e-15})
        if res.fun < best_error:
            best_error = res.fun
            best_params = res.x
            print(f"  Powell fine: error={res.fun:.6e}")
    except:
        pass

    t3 = time.time()
    print(f"  Phase 3 done in {t3-t2:.1f}s, best error: {best_error:.6e}")

# =============================================================================
# PHASE 4: If not found yet, try differential evolution
# =============================================================================
if best_error > 0.01:
    print("\n--- Phase 4: Differential Evolution ---")

    # Try around each known orbit with small bounds
    for o in neighbor_orbits[:4]:
        bounds_de = [
            (o['v1'] - 0.1, o['v1'] + 0.1),
            (o['v2'] - 0.1, o['v2'] + 0.1),
            (max(3, o['T'] - 10), o['T'] + 10),
        ]
        try:
            res_de = differential_evolution(objective_coarse, bounds_de,
                                           maxiter=100, seed=42, tol=1e-10,
                                           popsize=15, workers=1)
            if res_de.fun < best_error:
                best_error = res_de.fun
                best_params = res_de.x
                print(f"  DE near {o['id']}: error={res_de.fun:.6e}")
                if res_de.fun < 0.01:
                    print(f"  *** FOUND via DE!")
                    break
        except Exception as e:
            pass

    # Wider search
    if best_error > 0.01:
        bounds_wide = [
            (0.0, 0.7),
            (0.0, 0.6),
            (5, 60),
        ]
        try:
            res_de = differential_evolution(objective_coarse, bounds_wide,
                                           maxiter=200, seed=123, tol=1e-10,
                                           popsize=20, workers=1)
            if res_de.fun < best_error:
                best_error = res_de.fun
                best_params = res_de.x
                print(f"  Wide DE: error={res_de.fun:.6e}")
        except Exception as e:
            print(f"  Wide DE failed: {e}")

    t4 = time.time()
    print(f"  Phase 4 done in {t4 - (t3 if 't3' in dir() else t2):.1f}s")

# =============================================================================
# FINAL RESULT
# =============================================================================
print(f"\n{'='*60}")
print(f"FINAL RESULT")
print(f"{'='*60}")
print(f"Best return error: {best_error:.6e}")
if best_params is not None:
    print(f"Best params: vx={best_params[0]:.12f}, vy={best_params[1]:.12f}, T={best_params[2]:.8f}")

if best_error < 0.01:
    print("\n*** ORBIT FOUND! ***")
    orbit_data = {
        'vx': float(best_params[0]),
        'vy': float(best_params[1]),
        'T': float(best_params[2]),
        'return_error': float(best_error),
        'target_cell': {'row': target_row, 'col': target_col},
        'status': 'found',
    }
    with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_new_orbit.json', 'w') as f:
        json.dump(orbit_data, f, indent=2)
    print("Saved to threebody_new_orbit.json")
elif best_error < 0.1:
    print(f"\nNear-miss (error {best_error:.6e} vs threshold 0.01)")
    orbit_data = {
        'vx': float(best_params[0]),
        'vy': float(best_params[1]),
        'T': float(best_params[2]),
        'return_error': float(best_error),
        'target_cell': {'row': target_row, 'col': target_col},
        'status': 'near-miss',
    }
    with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_new_orbit.json', 'w') as f:
        json.dump(orbit_data, f, indent=2)
    print("Saved near-miss to threebody_new_orbit.json")
else:
    print(f"\nNo orbit found. Best error: {best_error:.6e}")
    orbit_data = {
        'best_error': float(best_error),
        'best_params': [float(x) for x in best_params] if best_params is not None else None,
        'target_cell': {'row': target_row, 'col': target_col},
        'status': 'not_found',
    }
    with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_new_orbit.json', 'w') as f:
        json.dump(orbit_data, f, indent=2)
    print("Saved search results to threebody_new_orbit.json")
