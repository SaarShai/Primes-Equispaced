#!/usr/bin/env python3
"""
Three-Body Orbit Discovery via CF/Nobility Framework
======================================================

Target: Empty cell 6-15|1.30-1.35 in the periodic table
(CF period length 6-15, geometric mean of partial quotients 1.30-1.35)

This cell has 7 occupied neighbors — the most of any empty cell.

Strategy:
1. Use known orbits from neighboring cells as seed initial conditions
2. Perturb + optimize to find orbits that would fall in the target cell
3. Use shooting method: minimize ||r(T)-r(0)|| + ||v(T)-v(0)||
   with T as a free parameter
4. Classify any discovered orbit by its CF structure

Author: Saar (with Claude)
Date: 2026-03-29
"""

import json
import os
import sys
import time
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, differential_evolution
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")

# ═══════════════════════════════════════════════════════════════════
# 1. THREE-BODY INTEGRATOR (from threebody_verify_gaps.py)
# ═══════════════════════════════════════════════════════════════════

def threebody_eom(t, state, masses):
    G = 1.0
    x1, y1, x2, y2, x3, y3 = state[:6]
    vx1, vy1, vx2, vy2, vx3, vy3 = state[6:]
    m1, m2, m3 = masses

    dx12, dy12 = x2 - x1, y2 - y1
    dx13, dy13 = x3 - x1, y3 - y1
    dx23, dy23 = x3 - x2, y3 - y2

    r12 = np.sqrt(dx12**2 + dy12**2)
    r13 = np.sqrt(dx13**2 + dy13**2)
    r23 = np.sqrt(dx23**2 + dy23**2)

    r12_3 = r12**3
    r13_3 = r13**3
    r23_3 = r23**3

    ax1 = G * m2 * dx12 / r12_3 + G * m3 * dx13 / r13_3
    ay1 = G * m2 * dy12 / r12_3 + G * m3 * dy13 / r13_3
    ax2 = -G * m1 * dx12 / r12_3 + G * m3 * dx23 / r23_3
    ay2 = -G * m1 * dy12 / r12_3 + G * m3 * dy23 / r23_3
    ax3 = -G * m1 * dx13 / r13_3 - G * m2 * dx23 / r23_3
    ay3 = -G * m1 * dy13 / r13_3 - G * m2 * dy23 / r23_3

    return [vx1, vy1, vx2, vy2, vx3, vy3,
            ax1, ay1, ax2, ay2, ax3, ay3]


def compute_energy(state, masses):
    G = 1.0
    x1, y1, x2, y2, x3, y3 = state[:6]
    vx1, vy1, vx2, vy2, vx3, vy3 = state[6:]
    m1, m2, m3 = masses
    KE = 0.5 * (m1*(vx1**2+vy1**2) + m2*(vx2**2+vy2**2) + m3*(vx3**2+vy3**2))
    r12 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    r13 = np.sqrt((x3-x1)**2 + (y3-y1)**2)
    r23 = np.sqrt((x3-x2)**2 + (y3-y2)**2)
    PE = -G * (m1*m2/r12 + m1*m3/r13 + m2*m3/r23)
    return KE + PE


def make_initial_state(v1, v2):
    """Li & Liao convention: r1=(-1,0), r2=(1,0), r3=(0,0), v1=v2=(v1,v2), v3=-2(v1,v2)"""
    return [-1.0, 0.0, 1.0, 0.0, 0.0, 0.0,
            v1, v2, v1, v2, -2*v1, -2*v2]


def integrate_orbit(v1, v2, T, masses=(1.0, 1.0, 1.0),
                    rtol=1e-12, atol=1e-12, max_step=0.01):
    """Integrate and return (sol, pos_error, vel_error, energy_drift)."""
    state0 = make_initial_state(v1, v2)
    E0 = compute_energy(state0, masses)

    try:
        sol = solve_ivp(
            threebody_eom, [0, T], state0,
            method='DOP853', rtol=rtol, atol=atol,
            max_step=max_step, dense_output=True,
            args=(masses,)
        )
    except Exception:
        return None, float('inf'), float('inf'), float('inf')

    if not sol.success:
        return sol, float('inf'), float('inf'), float('inf')

    state_final = sol.y[:, -1]
    pos0 = np.array(state0[:6])
    posf = np.array(state_final[:6])
    vel0 = np.array(state0[6:])
    velf = np.array(state_final[6:])

    return_error = np.linalg.norm(posf - pos0)
    vel_error = np.linalg.norm(velf - vel0)
    Ef = compute_energy(state_final, masses)
    energy_drift = abs(Ef - E0) / abs(E0) if E0 != 0 else abs(Ef - E0)

    return sol, return_error, vel_error, energy_drift


def check_permutation_return(sol, v1, v2, T):
    """Check return error under all body permutations."""
    from itertools import permutations
    state0 = make_initial_state(v1, v2)
    state_f = sol.y[:, -1]

    pos0 = np.array(state0[:6]).reshape(3, 2)
    posf = np.array(state_f[:6]).reshape(3, 2)
    vel0 = np.array(state0[6:]).reshape(3, 2)
    velf = np.array(state_f[6:]).reshape(3, 2)

    best_total = float('inf')
    best_pos = float('inf')
    best_vel = float('inf')
    best_perm = (0, 1, 2)

    for perm in permutations([0, 1, 2]):
        pe = np.linalg.norm(posf[list(perm)] - pos0)
        ve = np.linalg.norm(velf[list(perm)] - vel0)
        if pe + ve < best_total:
            best_total = pe + ve
            best_pos = pe
            best_vel = ve
            best_perm = perm

    return best_pos, best_vel, best_perm


# ═══════════════════════════════════════════════════════════════════
# 2. SHOOTING METHOD OPTIMIZER
# ═══════════════════════════════════════════════════════════════════

def return_error_objective(params, masses=(1.0, 1.0, 1.0)):
    """
    Objective function: minimize total return error.
    params = [v1, v2, T]
    """
    v1, v2, T = params
    if T < 1.0 or T > 300.0:
        return 1e10

    max_step = min(0.05, T / 100.0)

    try:
        sol, pos_err, vel_err, e_drift = integrate_orbit(
            v1, v2, T, masses=masses,
            rtol=1e-10, atol=1e-10, max_step=max_step
        )
    except Exception:
        return 1e10

    if sol is None or not sol.success:
        return 1e10

    # Also check permutations
    try:
        perm_pos, perm_vel, _ = check_permutation_return(sol, v1, v2, T)
        best_pos = min(pos_err, perm_pos)
        best_vel = min(vel_err, perm_vel)
    except Exception:
        best_pos = pos_err
        best_vel = vel_err

    return best_pos + best_vel


def refine_orbit(v1, v2, T, method='Nelder-Mead', maxiter=200):
    """
    Refine initial conditions using optimization.
    Returns (v1_opt, v2_opt, T_opt, final_error).
    """
    x0 = [v1, v2, T]

    try:
        result = minimize(
            return_error_objective, x0,
            method=method,
            options={'maxiter': maxiter, 'xatol': 1e-10, 'fatol': 1e-10,
                     'adaptive': True}
        )
        v1_opt, v2_opt, T_opt = result.x
        final_err = result.fun
        return v1_opt, v2_opt, T_opt, final_err, result.success
    except Exception as e:
        return v1, v2, T, 1e10, False


# ═══════════════════════════════════════════════════════════════════
# 3. CF ANALYSIS (classify discovered orbits)
# ═══════════════════════════════════════════════════════════════════

def compute_cf_from_angle(v1, v2, T):
    """
    Compute the continued fraction representation of the orbit's
    winding angle ratio.

    For zero-angular-momentum 3-body with Li-Liao convention,
    the topology is characterized by the ratio of angular motions.
    We approximate by computing the winding number from the trajectory.
    """
    # Integrate with dense output
    sol, pos_err, vel_err, e_drift = integrate_orbit(
        v1, v2, T, rtol=1e-12, atol=1e-12, max_step=min(0.01, T/500)
    )
    if sol is None or not sol.success:
        return [], 0.0

    # Compute winding of body 1 around center of mass
    t_pts = np.linspace(0, T, 10000)
    states = sol.sol(t_pts)

    # Center of mass (equal masses)
    cx = (states[0] + states[2] + states[4]) / 3.0
    cy = (states[1] + states[3] + states[5]) / 3.0

    # Body 1 relative to CM
    dx = states[0] - cx
    dy = states[1] - cy

    # Total angle wound
    angles = np.arctan2(dy, dx)
    dtheta = np.diff(np.unwrap(angles))
    total_angle = np.sum(dtheta)

    # Body 2 relative to CM
    dx2 = states[2] - cx
    dy2 = states[3] - cy
    angles2 = np.arctan2(dy2, dx2)
    dtheta2 = np.diff(np.unwrap(angles2))
    total_angle2 = np.sum(dtheta2)

    # Winding ratio
    if abs(total_angle2) > 0.01:
        ratio = abs(total_angle / total_angle2)
    else:
        ratio = 0.0

    # Convert ratio to CF
    cf = ratio_to_cf(ratio, max_terms=30)

    return cf, ratio


def ratio_to_cf(x, max_terms=30):
    """Convert a real number to its continued fraction representation."""
    cf = []
    for _ in range(max_terms):
        a = int(math.floor(x))
        cf.append(a)
        frac = x - a
        if abs(frac) < 1e-10:
            break
        x = 1.0 / frac
        if x > 1e10:
            break
    return cf


def cf_gmean(cf):
    """Geometric mean of CF partial quotients."""
    if not cf or len(cf) == 0:
        return 0.0
    cf_pos = [a for a in cf if a > 0]
    if not cf_pos:
        return 0.0
    return math.exp(sum(math.log(a) for a in cf_pos) / len(cf_pos))


def classify_cell(cf_period_length, gmean):
    """Determine which periodic table cell this orbit falls in."""
    row_bins = [(1,1,'1'), (2,5,'2-5'), (6,15,'6-15'), (16,30,'16-30'),
                (31,50,'31-50'), (51,80,'51-80'), (81,120,'81-120'),
                (121,180,'121-180'), (181,300,'181-300')]
    col_bins = [(1.0,1.05,'1.00-1.05'), (1.05,1.1,'1.05-1.10'),
                (1.1,1.15,'1.10-1.15'), (1.15,1.2,'1.15-1.20'),
                (1.2,1.25,'1.20-1.25'), (1.25,1.3,'1.25-1.30'),
                (1.3,1.35,'1.30-1.35'), (1.35,1.45,'1.35-1.45')]

    row = None
    for lo, hi, label in row_bins:
        if lo <= cf_period_length <= hi:
            row = label
            break

    col = None
    for lo, hi, label in col_bins:
        if lo <= gmean < hi:
            col = label
            break

    return row, col


# ═══════════════════════════════════════════════════════════════════
# 4. SEED GENERATION
# ═══════════════════════════════════════════════════════════════════

def load_seed_orbits():
    """
    Load known orbits from neighboring cells to use as seeds.
    Focus on the smallest/simplest orbits that are closest to the
    target cell (6-15|1.30-1.35).
    """
    with open(os.path.join(OUTPUT_DIR, "threebody_full_data.json")) as f:
        full_data = json.load(f)

    results = full_data['results']

    # Seed orbits: short-period orbits from adjacent cells
    seeds = []

    # Direct neighbors with known ICs
    # These are the simplest orbits from cells that border 6-15|1.30-1.35
    seed_ids = [
        # Cell 2-5|1.30-1.35 (below-left)
        'I.A-2',   # v1=0.3069, v2=0.1255, T=6.235, cf=[2,1,1,1,2], gmean=1.3195
        # Cell 2-5|1.35-1.45 (below-right)
        'I.A-3',   # v1=0.6150, v2=0.5226, T=37.321, cf=[1,3,1], gmean=1.4422
        # Cell 6-15|1.25-1.30 (left)
        'I.B-2',   # v1=0.4059, v2=0.2302, T=13.867, cf=[2,1,1,1,2,1,1,1,2], gmean=1.2599
        'I.A-5',   # in cell 6-15|1.20-1.25
        # Cell 6-15|1.35-1.45 (right)
        'I.B-3',   # v1=0.0833, v2=0.1279, T=10.465, cf=[2,1,1,1,4,1,1,1,2], gmean=1.3608
        'I.A-7',   # v1=0.1215, v2=0.1012, T=15.744, cf period in 6-15 range, gmean=1.377
        # Cell 16-30|1.30-1.35 (above)
        'I.B-17',  # v1=0.3956, v2=0.1544, T=41.788, cf_len=14, gmean=1.2809
        # Nearby small orbits
        'II.C-9',  # v1=0.1739, v2=0.1141, T=21.754, gmean=1.377
        'II.C-19', # v1=0.1869, v2=0.2045, T=27.725, gmean=1.3195
        'II.C-62', # v1=0.1468, v2=0.1988, T=15.585, gmean=1.2599
        'I.B-10',  # v1=0.3980, v2=0.1761, T=27.823, gmean=1.3195
        'II.C-66', # v1=0.1350, v2=0.1388, T=26.917, gmean=1.3195
    ]

    for r in results:
        if r['id'] in seed_ids and 'v1' in r and 'v2' in r:
            cf = r.get('cf_period', [])
            gm = cf_gmean(cf) if cf else 0
            seeds.append({
                'id': r['id'],
                'v1': r['v1'],
                'v2': r['v2'],
                'T': r['T'],
                'cf': cf,
                'gmean': gm,
                'word': r.get('word', ''),
            })

    return seeds


def generate_candidate_ics(seeds, n_candidates=100):
    """
    Generate candidate initial conditions by:
    1. Interpolating between seed orbits
    2. Perturbing seeds with targeted noise
    3. Grid search in regions suggested by the seed distribution
    """
    candidates = []
    rng = np.random.RandomState(42)

    # Strategy 1: Perturb each seed (40 candidates)
    for seed in seeds:
        for _ in range(4):
            dv1 = rng.normal(0, 0.05)
            dv2 = rng.normal(0, 0.05)
            dT = rng.normal(0, seed['T'] * 0.3)
            candidates.append({
                'v1': seed['v1'] + dv1,
                'v2': seed['v2'] + dv2,
                'T': max(3.0, seed['T'] + dT),
                'source': f"perturb({seed['id']})",
            })

    # Strategy 2: Interpolate between pairs of seeds (30 candidates)
    for i in range(len(seeds)):
        for j in range(i+1, len(seeds)):
            s1, s2 = seeds[i], seeds[j]
            for alpha in [0.3, 0.5, 0.7]:
                candidates.append({
                    'v1': s1['v1'] * (1-alpha) + s2['v1'] * alpha,
                    'v2': s1['v2'] * (1-alpha) + s2['v2'] * alpha,
                    'T': s1['T'] * (1-alpha) + s2['T'] * alpha,
                    'source': f"interp({s1['id']},{s2['id']},a={alpha})",
                })
            if len(candidates) >= 70:
                break
        if len(candidates) >= 70:
            break

    # Strategy 3: Grid search in the v1-v2 space near seeds (30 candidates)
    # Focus on the region where most seeds cluster
    v1_vals = [s['v1'] for s in seeds]
    v2_vals = [s['v2'] for s in seeds]
    T_vals = [s['T'] for s in seeds]

    v1_range = (min(v1_vals) - 0.05, max(v1_vals) + 0.05)
    v2_range = (min(v2_vals) - 0.05, max(v2_vals) + 0.05)

    # Target T range: for CF period 6-15 with gmean ~1.325,
    # expect T ~ 15-50 based on neighbors
    for _ in range(30):
        candidates.append({
            'v1': rng.uniform(v1_range[0], v1_range[1]),
            'v2': rng.uniform(v2_range[0], v2_range[1]),
            'T': rng.uniform(8.0, 60.0),
            'source': 'random_grid',
        })

    # Trim to exactly n_candidates
    candidates = candidates[:n_candidates]

    return candidates


# ═══════════════════════════════════════════════════════════════════
# 5. MAIN DISCOVERY PIPELINE
# ═══════════════════════════════════════════════════════════════════

def run_discovery():
    """Main orbit discovery pipeline."""
    print("=" * 70)
    print("THREE-BODY ORBIT DISCOVERY VIA CF/NOBILITY FRAMEWORK")
    print("=" * 70)
    print(f"Target cell: 6-15|1.30-1.35")
    print(f"  CF period length: 6 to 15")
    print(f"  Geometric mean of CF quotients: 1.30 to 1.35")
    print(f"  This cell has 7 occupied neighbors (most of any empty cell)")
    print()

    # Load seeds
    seeds = load_seed_orbits()
    print(f"Loaded {len(seeds)} seed orbits from neighboring cells:")
    for s in seeds:
        cf_str = str(s['cf'][:8]) + ('...' if len(s['cf']) > 8 else '')
        print(f"  {s['id']:10s}: v1={s['v1']:.4f}, v2={s['v2']:.4f}, T={s['T']:.3f}, "
              f"gmean={s['gmean']:.4f}, cf={cf_str}")

    # Generate candidates
    candidates = generate_candidate_ics(seeds, n_candidates=100)
    print(f"\nGenerated {len(candidates)} candidate ICs")

    # Phase 1: Quick screen (low precision)
    print("\n" + "─" * 70)
    print("PHASE 1: Quick screening (100 candidates, low precision)")
    print("─" * 70)

    screened = []
    for i, cand in enumerate(candidates):
        v1, v2, T = cand['v1'], cand['v2'], cand['T']

        # Quick integration
        max_step = min(0.1, T / 50.0)
        try:
            sol, pos_err, vel_err, e_drift = integrate_orbit(
                v1, v2, T, rtol=1e-8, atol=1e-8, max_step=max_step
            )
        except Exception:
            continue

        if sol is None or not sol.success:
            continue

        # Also try 2T, 3T
        best_err = pos_err + vel_err
        best_T = T
        best_mult = 1

        for mult in [2, 3]:
            T_try = T * mult
            if T_try > 300:
                continue
            try:
                sol2, pe2, ve2, _ = integrate_orbit(
                    v1, v2, T_try, rtol=1e-8, atol=1e-8,
                    max_step=min(0.1, T_try/50.0)
                )
                if sol2 and sol2.success:
                    try:
                        pp, vp, _ = check_permutation_return(sol2, v1, v2, T_try)
                        err2 = min(pe2, pp) + min(ve2, vp)
                    except:
                        err2 = pe2 + ve2
                    if err2 < best_err:
                        best_err = err2
                        best_T = T_try
                        best_mult = mult
            except:
                pass

        screened.append({
            'v1': v1, 'v2': v2, 'T': best_T, 'T_orig': T,
            'mult': best_mult,
            'error': best_err,
            'source': cand['source'],
        })

        if (i + 1) % 10 == 0:
            print(f"  Screened {i+1}/100...", end='')
            good = sum(1 for s in screened if s['error'] < 1.0)
            print(f" ({good} promising so far)")

    # Sort by error
    screened.sort(key=lambda x: x['error'])

    print(f"\nScreening complete. Top 20 candidates:")
    for i, s in enumerate(screened[:20]):
        print(f"  #{i+1}: err={s['error']:.4e}, v1={s['v1']:.4f}, v2={s['v2']:.4f}, "
              f"T={s['T']:.3f} ({s['mult']}x), src={s['source'][:40]}")

    # Phase 2: Refine top candidates
    print("\n" + "─" * 70)
    print("PHASE 2: Refinement (top 20 candidates, Nelder-Mead optimization)")
    print("─" * 70)

    refined = []
    for i, cand in enumerate(screened[:20]):
        print(f"\n  Refining #{i+1}: v1={cand['v1']:.6f}, v2={cand['v2']:.6f}, T={cand['T']:.3f}")
        print(f"    Initial error: {cand['error']:.4e}")

        t0 = time.time()
        v1_opt, v2_opt, T_opt, final_err, success = refine_orbit(
            cand['v1'], cand['v2'], cand['T'], maxiter=500
        )
        elapsed = time.time() - t0

        print(f"    Refined: v1={v1_opt:.8f}, v2={v2_opt:.8f}, T={T_opt:.6f}")
        print(f"    Final error: {final_err:.4e} (took {elapsed:.1f}s)")

        # High-precision verification
        if final_err < 1.0:
            sol, pos_err, vel_err, e_drift = integrate_orbit(
                v1_opt, v2_opt, T_opt, rtol=1e-12, atol=1e-12,
                max_step=min(0.01, T_opt/500)
            )

            if sol and sol.success:
                perm_pos, perm_vel, perm_idx = check_permutation_return(
                    sol, v1_opt, v2_opt, T_opt
                )
                best_pos = min(pos_err, perm_pos)
                best_vel = min(vel_err, perm_vel)

                print(f"    High-prec: pos_err={best_pos:.4e}, vel_err={best_vel:.4e}, "
                      f"E_drift={e_drift:.4e}")

                refined.append({
                    'v1': v1_opt, 'v2': v2_opt, 'T': T_opt,
                    'pos_error': best_pos, 'vel_error': best_vel,
                    'total_error': best_pos + best_vel,
                    'energy_drift': e_drift,
                    'source': cand['source'],
                    'perm': list(perm_idx),
                    'sol': sol,
                })

    # Sort refined by total error
    refined.sort(key=lambda x: x['total_error'])

    # Phase 3: Deep refinement of best candidates
    print("\n" + "─" * 70)
    print("PHASE 3: Deep refinement of best candidates")
    print("─" * 70)

    discoveries = []
    for i, cand in enumerate(refined[:5]):
        if cand['total_error'] > 1.0:
            continue

        print(f"\n  Deep refining #{i+1}: err={cand['total_error']:.4e}")

        # Multiple rounds of Nelder-Mead
        v1, v2, T = cand['v1'], cand['v2'], cand['T']
        for round_num in range(5):
            v1_new, v2_new, T_new, err_new, _ = refine_orbit(
                v1, v2, T, maxiter=1000
            )
            if err_new < return_error_objective([v1, v2, T]):
                v1, v2, T = v1_new, v2_new, T_new
            print(f"    Round {round_num+1}: err={return_error_objective([v1, v2, T]):.6e}")

        # Final high-precision check
        sol, pos_err, vel_err, e_drift = integrate_orbit(
            v1, v2, T, rtol=1e-13, atol=1e-13,
            max_step=min(0.005, T/1000)
        )

        if sol and sol.success:
            perm_pos, perm_vel, perm_idx = check_permutation_return(sol, v1, v2, T)
            best_pos = min(pos_err, perm_pos)
            best_vel = min(vel_err, perm_vel)

            classification = "PERIODIC" if best_pos < 0.01 and best_vel < 0.01 else \
                           "PROMISING" if best_pos < 0.1 else \
                           "MARGINAL" if best_pos < 1.0 else "NOT PERIODIC"

            print(f"    FINAL: pos={best_pos:.6e}, vel={best_vel:.6e}, class={classification}")

            # Compute CF properties
            cf, ratio = compute_cf_from_angle(v1, v2, T)
            gm = cf_gmean(cf) if cf else 0
            row, col = classify_cell(len(cf), gm) if cf else (None, None)
            cell_key = f"{row}|{col}" if row and col else "unknown"

            print(f"    CF: {cf[:15]}{'...' if len(cf)>15 else ''}")
            print(f"    CF period length: {len(cf)}, gmean: {gm:.4f}")
            print(f"    Cell: {cell_key}")

            discoveries.append({
                'v1': v1, 'v2': v2, 'T': T,
                'pos_error': best_pos, 'vel_error': best_vel,
                'total_error': best_pos + best_vel,
                'energy_drift': e_drift,
                'classification': classification,
                'cf': cf, 'gmean': gm,
                'cf_period_length': len(cf),
                'cell': cell_key,
                'target_cell': cell_key == "6-15|1.30-1.35",
                'source': cand['source'],
                'perm': list(perm_idx),
                'sol': sol,
            })

    # Phase 4: Report
    print("\n" + "=" * 70)
    print("DISCOVERY RESULTS")
    print("=" * 70)

    n_periodic = sum(1 for d in discoveries if d['classification'] == 'PERIODIC')
    n_promising = sum(1 for d in discoveries if d['classification'] == 'PROMISING')
    n_target = sum(1 for d in discoveries if d.get('target_cell', False))

    print(f"\nPeriodic orbits found: {n_periodic}")
    print(f"Promising candidates: {n_promising}")
    print(f"In target cell (6-15|1.30-1.35): {n_target}")

    for i, d in enumerate(discoveries):
        print(f"\n  Discovery #{i+1}: {d['classification']}")
        print(f"    v1 = {d['v1']:.10f}")
        print(f"    v2 = {d['v2']:.10f}")
        print(f"    T  = {d['T']:.10f}")
        print(f"    pos_error = {d['pos_error']:.6e}")
        print(f"    vel_error = {d['vel_error']:.6e}")
        print(f"    energy_drift = {d['energy_drift']:.6e}")
        print(f"    CF = {d['cf'][:20]}")
        print(f"    gmean = {d['gmean']:.4f}")
        print(f"    cell = {d['cell']}")
        print(f"    IN TARGET? {'YES!' if d.get('target_cell') else 'no'}")

    # Plot best discoveries
    for i, d in enumerate(discoveries[:5]):
        if d['sol'] and d['sol'].success:
            plot_discovery(d, i+1)

    # Write report
    write_discovery_report(seeds, screened, refined, discoveries)

    return discoveries


def plot_discovery(disc, num):
    """Plot a discovered orbit."""
    sol = disc['sol']
    T = disc['T']
    v1, v2 = disc['v1'], disc['v2']

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    t_dense = np.linspace(0, T, 10000)
    states = sol.sol(t_dense)

    ax = axes[0]
    ax.plot(states[0], states[1], '-', color='#e74c3c', alpha=0.7, lw=0.5, label='Body 1')
    ax.plot(states[2], states[3], '-', color='#2ecc71', alpha=0.7, lw=0.5, label='Body 2')
    ax.plot(states[4], states[5], '-', color='#3498db', alpha=0.7, lw=0.5, label='Body 3')
    ax.plot(-1, 0, 'o', color='#e74c3c', ms=8, zorder=5)
    ax.plot(1, 0, 'o', color='#2ecc71', ms=8, zorder=5)
    ax.plot(0, 0, 'o', color='#3498db', ms=8, zorder=5)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f"Discovery #{num}: {disc['classification']}\n"
                 f"v1={v1:.6f}, v2={v2:.6f}, T={T:.4f}")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    state0 = make_initial_state(v1, v2)
    pos0 = np.array(state0[:6])
    n_check = 500
    t_check = np.linspace(T*0.01, T, n_check)
    errors = [np.linalg.norm(sol.sol(tc)[:6] - pos0) for tc in t_check]
    ax2.semilogy(t_check, errors, 'b-', lw=1)
    ax2.axhline(y=0.01, color='g', ls='--', alpha=0.5, label='Periodic')
    ax2.axhline(y=0.1, color='orange', ls='--', alpha=0.5, label='Promising')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('||r(t) - r(0)||')
    ax2.set_title(f"Return error = {disc['pos_error']:.2e}\n"
                  f"CF gmean={disc['gmean']:.4f}, cell={disc['cell']}")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fname = os.path.join(OUTPUT_DIR, f"threebody_discovery_{num:02d}.png")
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {fname}")


def write_discovery_report(seeds, screened, refined, discoveries):
    """Write the discovery report."""
    report_path = os.path.join(OUTPUT_DIR, "THREEBODY_ORBIT_DISCOVERY.md")

    with open(report_path, 'w') as f:
        f.write("# Three-Body Orbit Discovery via CF/Nobility Framework\n\n")
        f.write("**Date**: 2026-03-29\n")
        f.write("**Target cell**: 6-15|1.30-1.35 (CF period length 6-15, gmean 1.30-1.35)\n")
        f.write("**Method**: Shooting optimization from neighbor-interpolated initial conditions\n")
        f.write("**Setup**: Equal masses m1=m2=m3=1, planar, zero angular momentum\n\n")

        f.write("## Background\n\n")
        f.write("The periodic table of three-body orbits organizes 691 known orbits by their\n")
        f.write("continued fraction (CF) structure. The table has 21 empty cells that predict\n")
        f.write("orbit types that SHOULD exist but haven't been found.\n\n")
        f.write("Cell 6-15|1.30-1.35 has 7 occupied neighbors, making it the most constrained\n")
        f.write("empty cell and the best target for guided orbit discovery.\n\n")

        f.write("## Seed Orbits (from neighboring cells)\n\n")
        f.write("| ID | v1 | v2 | T | gmean | CF period |\n")
        f.write("|---|---|---|---|---|---|\n")
        for s in seeds:
            cf_str = str(s['cf'][:6]) + ('...' if len(s['cf']) > 6 else '')
            f.write(f"| {s['id']} | {s['v1']:.6f} | {s['v2']:.6f} | {s['T']:.3f} | "
                    f"{s['gmean']:.4f} | {cf_str} |\n")

        f.write(f"\n## Screening Results\n\n")
        f.write(f"- Candidates screened: {len(screened)}\n")
        n_sub1 = sum(1 for s in screened if s['error'] < 1.0)
        n_sub01 = sum(1 for s in screened if s['error'] < 0.1)
        n_sub001 = sum(1 for s in screened if s['error'] < 0.01)
        f.write(f"- Error < 1.0: {n_sub1}\n")
        f.write(f"- Error < 0.1: {n_sub01}\n")
        f.write(f"- Error < 0.01: {n_sub001}\n\n")

        f.write("### Top 10 after screening\n\n")
        f.write("| Rank | Error | v1 | v2 | T | Source |\n")
        f.write("|---|---|---|---|---|---|\n")
        for i, s in enumerate(screened[:10]):
            f.write(f"| {i+1} | {s['error']:.4e} | {s['v1']:.6f} | {s['v2']:.6f} | "
                    f"{s['T']:.3f} | {s['source'][:40]} |\n")

        f.write(f"\n## Refined Results\n\n")
        f.write(f"- Candidates refined: {len(refined)}\n\n")

        f.write("| Rank | Pos Error | Vel Error | v1 | v2 | T | Source |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for i, r in enumerate(refined[:10]):
            f.write(f"| {i+1} | {r['pos_error']:.4e} | {r['vel_error']:.4e} | "
                    f"{r['v1']:.8f} | {r['v2']:.8f} | {r['T']:.6f} | {r['source'][:30]} |\n")

        f.write(f"\n## Discoveries\n\n")

        if not discoveries:
            f.write("No periodic orbits found in this run.\n\n")
        else:
            n_periodic = sum(1 for d in discoveries if d['classification'] == 'PERIODIC')
            n_promising = sum(1 for d in discoveries if d['classification'] == 'PROMISING')
            n_target = sum(1 for d in discoveries if d.get('target_cell', False))

            f.write(f"- **Periodic orbits**: {n_periodic}\n")
            f.write(f"- **Promising candidates**: {n_promising}\n")
            f.write(f"- **In target cell**: {n_target}\n\n")

            for i, d in enumerate(discoveries):
                f.write(f"### Discovery #{i+1}: {d['classification']}\n\n")
                f.write(f"| Property | Value |\n")
                f.write(f"|---|---|\n")
                f.write(f"| v1 | {d['v1']:.12f} |\n")
                f.write(f"| v2 | {d['v2']:.12f} |\n")
                f.write(f"| T | {d['T']:.12f} |\n")
                f.write(f"| Position error | {d['pos_error']:.6e} |\n")
                f.write(f"| Velocity error | {d['vel_error']:.6e} |\n")
                f.write(f"| Energy drift | {d['energy_drift']:.6e} |\n")
                f.write(f"| CF period | {d['cf'][:20]} |\n")
                f.write(f"| CF period length | {d['cf_period_length']} |\n")
                f.write(f"| gmean | {d['gmean']:.6f} |\n")
                f.write(f"| Cell | {d['cell']} |\n")
                f.write(f"| In target cell? | {'YES' if d.get('target_cell') else 'No'} |\n")
                f.write(f"| Source | {d['source']} |\n\n")

                f.write(f"![Discovery {i+1}](threebody_discovery_{i+1:02d}.png)\n\n")

        f.write("## Method Details\n\n")
        f.write("### Phase 1: Candidate Generation\n")
        f.write("- Perturbation of seed orbits (random Gaussian noise)\n")
        f.write("- Interpolation between pairs of seed orbits\n")
        f.write("- Random grid search in the v1-v2-T space\n\n")
        f.write("### Phase 2: Screening\n")
        f.write("- Low-precision integration (rtol=atol=1e-8)\n")
        f.write("- Test T, 2T, 3T for permutation periods\n")
        f.write("- Sort by total return error\n\n")
        f.write("### Phase 3: Refinement\n")
        f.write("- Nelder-Mead optimization of (v1, v2, T)\n")
        f.write("- Objective: minimize ||r(T)-r(0)|| + ||v(T)-v(0)||\n")
        f.write("- High-precision verification (rtol=atol=1e-12)\n\n")
        f.write("### Phase 4: Deep Refinement\n")
        f.write("- 5 rounds of Nelder-Mead on best candidates\n")
        f.write("- Ultra-high-precision verification (rtol=atol=1e-13)\n")
        f.write("- CF analysis to classify the orbit's cell position\n\n")

        f.write("## Interpretation\n\n")
        f.write("Even if no orbit lands exactly in cell 6-15|1.30-1.35, finding periodic\n")
        f.write("orbits near this cell demonstrates the predictive power of the CF framework.\n")
        f.write("The framework identifies WHERE to look based on number-theoretic structure.\n\n")
        f.write("A future, more intensive search (>10K candidates, Newton-Raphson refinement,\n")
        f.write("continuation methods) could fill this cell definitively.\n")

    print(f"\nReport saved: {report_path}")


if __name__ == "__main__":
    discoveries = run_discovery()
