#!/usr/bin/env python3
"""
Fast orbit search v3: Uses event-based termination for close encounters,
focuses on neighbor perturbations with short periods, and uses DOP853.
"""

import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import time
import sys

# Load data
with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_exact_data.json') as f:
    exact_data = json.load(f)

results = exact_data['results']
orbits_by_id = {r['id']: r for r in results}

# Target: row=6-15, col=1.30-1.35 (most interesting empty cell)
# Neighbors (representatives)
neighbor_ids = ['I.A-2', 'I.B-17', 'I.B-2', 'I.B-3', 'I.A-3', 'II.C-190', 'II.C-192']
neighbor_orbits = [orbits_by_id[oid] for oid in neighbor_ids]

print("="*60)
print("ORBIT SEARCH v3 - Target cell: 6-15 | 1.30-1.35")
print("="*60)

# =============================================================================
# THREE-BODY with close-encounter detection
# =============================================================================
MIN_DIST = 0.001  # If two bodies get this close, abort

def threebody_rhs(t, state):
    x1, y1, x2, y2, x3, y3 = state[:6]
    vx1, vy1, vx2, vy2, vx3, vy3 = state[6:]

    dx12, dy12 = x2 - x1, y2 - y1
    dx13, dy13 = x3 - x1, y3 - y1
    dx23, dy23 = x3 - x2, y3 - y2

    r12_sq = dx12**2 + dy12**2
    r13_sq = dx13**2 + dy13**2
    r23_sq = dx23**2 + dy23**2

    # Close encounter check
    if r12_sq < MIN_DIST**2 or r13_sq < MIN_DIST**2 or r23_sq < MIN_DIST**2:
        return [0]*12  # Will be caught by event

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


def close_encounter(t, state):
    x1, y1, x2, y2, x3, y3 = state[:6]
    r12 = (x2-x1)**2 + (y2-y1)**2
    r13 = (x3-x1)**2 + (y3-y1)**2
    r23 = (x3-x2)**2 + (y3-y2)**2
    return min(r12, r13, r23) - MIN_DIST**2

close_encounter.terminal = True
close_encounter.direction = -1


def escape_event(t, state):
    """Detect if system is escaping (body >10 from origin)."""
    x1, y1, x2, y2, x3, y3 = state[:6]
    r_max = max(x1**2+y1**2, x2**2+y2**2, x3**2+y3**2)
    return 100 - r_max  # Negative when r_max > 10

escape_event.terminal = True
escape_event.direction = -1


def make_ic(vx, vy):
    return np.array([-1.0, 0.0, 1.0, 0.0, 0.0, 0.0, vx, vy, vx, vy, -2*vx, -2*vy])


def return_error(vx, vy, T, rtol=1e-10, atol=1e-10):
    if T < 2 or T > 100:
        return 1e10
    y0 = make_ic(vx, vy)
    try:
        sol = solve_ivp(threebody_rhs, [0, T], y0, method='DOP853',
                       rtol=rtol, atol=atol,
                       events=[close_encounter, escape_event],
                       max_step=T/20)
        if sol.status != 0:  # Terminated by event
            return 1e10
        if sol.t[-1] < T * 0.99:  # Didn't reach final time
            return 1e10
        yf = sol.y[:, -1]
        diff = yf - y0
        return np.sqrt(np.sum(diff**2))
    except Exception:
        return 1e10


def objective(params, rtol=1e-8, atol=1e-8):
    vx, vy, T = params
    return return_error(vx, vy, T, rtol, atol)


# =============================================================================
# Verify known orbits work
# =============================================================================
print("\n--- Verifying known orbits ---")
for o in neighbor_orbits[:3]:
    t0 = time.time()
    err = return_error(o['v1'], o['v2'], o['T'])
    dt = time.time() - t0
    print(f"  {o['id']}: error={err:.3e}, time={dt:.2f}s")
    sys.stdout.flush()

# =============================================================================
# STRATEGY: Focus on SHORT-period orbits near known neighbors
# The target cell needs word_length ~10-20 (based on neighbors)
# and T in the range 8-25
# Focus on the 3 closest neighbors: I.A-2 (T=6.2), I.B-2 (T=13.9), I.B-3 (T=10.5)
# =============================================================================
print("\n--- Phase 1: Systematic perturbation of short-period neighbors ---")
sys.stdout.flush()

# The short-period neighbors most likely to interpolate into the empty cell
focus_orbits = [
    orbits_by_id['I.A-2'],   # T=6.2, wl=8,  cell (2-5, 1.30-1.35)  - above
    orbits_by_id['I.B-2'],   # T=13.9, wl=14, cell (6-15, 1.25-1.30) - left
    orbits_by_id['I.B-3'],   # T=10.5, wl=16, cell (6-15, 1.35-1.45) - right
    orbits_by_id['II.C-190'],# T=15.3, wl=18, cell (16-30, 1.25-1.30) - below-left
]

best_error = 1e10
best_params = None
n_eval = 0
t_start = time.time()

# First, systematic grid around each focus orbit
for o in focus_orbits:
    vx0, vy0, T0 = o['v1'], o['v2'], o['T']
    # Try T multipliers (looking for harmonics)
    for T_mult in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]:
        T = T0 * T_mult
        if T < 5 or T > 60: continue
        err = return_error(vx0, vy0, T, rtol=1e-8, atol=1e-8)
        n_eval += 1
        if err < best_error:
            best_error = err
            best_params = [vx0, vy0, T]
            if err < 1.0:
                print(f"  Good: err={err:.4e} from {o['id']} T*{T_mult:.2f}, T={T:.3f}")
                sys.stdout.flush()

print(f"  Grid search: {n_eval} evals in {time.time()-t_start:.1f}s, best={best_error:.4e}")
sys.stdout.flush()

# Perturbation search
np.random.seed(42)
for o in focus_orbits:
    vx0, vy0, T0 = o['v1'], o['v2'], o['T']
    for scale in [0.005, 0.01, 0.02, 0.05, 0.1]:
        for _ in range(40):
            dvx = np.random.normal(0, scale)
            dvy = np.random.normal(0, scale)
            # Try both the original T and nearby T values
            for T in [T0, T0*1.1, T0*0.9, T0*1.5, T0*2.0]:
                dT = np.random.normal(0, max(0.5, T*scale*0.3))
                vx, vy = vx0 + dvx, vy0 + dvy
                T_try = T + dT
                if T_try < 5 or T_try > 60: continue
                err = return_error(vx, vy, T_try, rtol=1e-8, atol=1e-8)
                n_eval += 1
                if err < best_error:
                    best_error = err
                    best_params = [vx, vy, T_try]
                    if err < 1.0:
                        print(f"  Found: err={err:.4e} near {o['id']}, "
                              f"vx={vx:.8f}, vy={vy:.8f}, T={T_try:.4f}")
                        sys.stdout.flush()
            if n_eval % 100 == 0:
                elapsed = time.time() - t_start
                print(f"  ... {n_eval} evals, {elapsed:.0f}s, best={best_error:.4e}")
                sys.stdout.flush()

# Also try interpolation between pairs of orbits
print("\n--- Phase 1b: Interpolation between orbit pairs ---")
sys.stdout.flush()
for i, o1 in enumerate(focus_orbits):
    for j, o2 in enumerate(focus_orbits):
        if i >= j: continue
        for alpha in [0.25, 0.5, 0.75]:
            vx = (1-alpha)*o1['v1'] + alpha*o2['v1']
            vy = (1-alpha)*o1['v2'] + alpha*o2['v2']
            T = (1-alpha)*o1['T'] + alpha*o2['T']
            err = return_error(vx, vy, T, rtol=1e-8, atol=1e-8)
            n_eval += 1
            if err < best_error:
                best_error = err
                best_params = [vx, vy, T]
                print(f"  Interp {o1['id']}-{o2['id']} a={alpha}: err={err:.4e}")
                sys.stdout.flush()
            # Also perturb the interpolation
            for _ in range(10):
                dvx = np.random.normal(0, 0.02)
                dvy = np.random.normal(0, 0.02)
                dT = np.random.normal(0, 1.0)
                err = return_error(vx+dvx, vy+dvy, T+dT, rtol=1e-8, atol=1e-8)
                n_eval += 1
                if err < best_error:
                    best_error = err
                    best_params = [vx+dvx, vy+dvy, T+dT]
                    if err < 1.0:
                        print(f"  Interp+perturb: err={err:.4e}")
                        sys.stdout.flush()

elapsed = time.time() - t_start
print(f"\nPhase 1 complete: {n_eval} evals in {elapsed:.0f}s, best={best_error:.4e}")
sys.stdout.flush()

# =============================================================================
# Phase 2: Local optimization of best candidates
# =============================================================================
if best_error < 5.0 and best_params is not None:
    print(f"\n--- Phase 2: Nelder-Mead refinement ---")
    sys.stdout.flush()

    res = minimize(lambda p: return_error(p[0], p[1], p[2], 1e-10, 1e-10),
                  best_params, method='Nelder-Mead',
                  options={'maxiter': 2000, 'xatol': 1e-12, 'fatol': 1e-14})
    if res.fun < best_error:
        best_error = res.fun
        best_params = list(res.x)
        print(f"  Nelder-Mead: error={res.fun:.6e}")

    # Powell
    res2 = minimize(lambda p: return_error(p[0], p[1], p[2], 1e-10, 1e-10),
                   best_params, method='Powell',
                   options={'maxiter': 5000, 'ftol': 1e-15})
    if res2.fun < best_error:
        best_error = res2.fun
        best_params = list(res2.x)
        print(f"  Powell: error={res2.fun:.6e}")

    print(f"  Refined best: error={best_error:.6e}")
    print(f"  Params: vx={best_params[0]:.12f}, vy={best_params[1]:.12f}, T={best_params[2]:.8f}")
    sys.stdout.flush()

# =============================================================================
# Phase 3: If near a known orbit, it might just be that orbit at a different T
# Try ultra-fine refinement with high tolerance
# =============================================================================
if best_error < 0.1 and best_params is not None:
    print(f"\n--- Phase 3: Ultra-fine refinement ---")
    sys.stdout.flush()

    res3 = minimize(lambda p: return_error(p[0], p[1], p[2], 1e-12, 1e-12),
                   best_params, method='Nelder-Mead',
                   options={'maxiter': 5000, 'xatol': 1e-14, 'fatol': 1e-16})
    if res3.fun < best_error:
        best_error = res3.fun
        best_params = list(res3.x)
        print(f"  Ultra-fine NM: error={res3.fun:.6e}")
    sys.stdout.flush()

# =============================================================================
# RESULT
# =============================================================================
print(f"\n{'='*60}")
print(f"FINAL RESULT")
print(f"{'='*60}")
print(f"Best error: {best_error:.6e}")
if best_params is not None:
    print(f"vx = {best_params[0]:.14f}")
    print(f"vy = {best_params[1]:.14f}")
    print(f"T  = {best_params[2]:.10f}")

status = 'found' if best_error < 0.01 else ('near-miss' if best_error < 0.1 else 'not_found')
print(f"Status: {status}")

orbit_data = {
    'vx': float(best_params[0]) if best_params is not None else None,
    'vy': float(best_params[1]) if best_params is not None else None,
    'T': float(best_params[2]) if best_params is not None else None,
    'return_error': float(best_error),
    'target_cell': {'row': '6-15', 'col': '1.30-1.35'},
    'status': status,
    'n_evaluations': n_eval,
    'total_time_s': time.time() - t_start,
}

with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_new_orbit.json', 'w') as f:
    json.dump(orbit_data, f, indent=2)
print(f"\nSaved to threebody_new_orbit.json")
