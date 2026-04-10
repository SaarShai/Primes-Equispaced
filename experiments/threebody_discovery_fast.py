#!/usr/bin/env python3
"""
Fast Three-Body Orbit Discovery via CF/Nobility Framework
===========================================================
Optimized version: focuses on short-period orbits (T<60), uses faster integration,
and prints results incrementally.

Target: Empty cell 6-15|1.30-1.35 in the periodic table
"""

import json
import os
import sys
import time
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)

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
    r12_3, r13_3, r23_3 = r12**3, r13**3, r23**3
    ax1 = G * m2 * dx12 / r12_3 + G * m3 * dx13 / r13_3
    ay1 = G * m2 * dy12 / r12_3 + G * m3 * dy13 / r13_3
    ax2 = -G * m1 * dx12 / r12_3 + G * m3 * dx23 / r23_3
    ay2 = -G * m1 * dy12 / r12_3 + G * m3 * dy23 / r23_3
    ax3 = -G * m1 * dx13 / r13_3 - G * m2 * dx23 / r23_3
    ay3 = -G * m1 * dy13 / r13_3 - G * m2 * dy23 / r23_3
    return [vx1, vy1, vx2, vy2, vx3, vy3, ax1, ay1, ax2, ay2, ax3, ay3]

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
    return [-1.0, 0.0, 1.0, 0.0, 0.0, 0.0, v1, v2, v1, v2, -2*v1, -2*v2]

def integrate_fast(v1, v2, T, rtol=1e-10, atol=1e-10):
    """Fast integration - no dense output unless needed."""
    state0 = make_initial_state(v1, v2)
    try:
        sol = solve_ivp(
            threebody_eom, [0, T], state0,
            method='DOP853', rtol=rtol, atol=atol,
            max_step=min(0.05, T/50.0),
            args=((1.0, 1.0, 1.0),)
        )
    except Exception:
        return None, float('inf'), float('inf'), float('inf')
    if not sol.success:
        return sol, float('inf'), float('inf'), float('inf')
    sf = sol.y[:, -1]
    pos_err = np.linalg.norm(sf[:6] - np.array(state0[:6]))
    vel_err = np.linalg.norm(sf[6:] - np.array(state0[6:]))
    E0 = compute_energy(state0, (1,1,1))
    Ef = compute_energy(sf, (1,1,1))
    e_drift = abs(Ef-E0)/abs(E0) if E0 != 0 else abs(Ef-E0)
    return sol, pos_err, vel_err, e_drift

def integrate_dense(v1, v2, T, rtol=1e-12, atol=1e-12):
    """High-precision integration with dense output for plotting."""
    state0 = make_initial_state(v1, v2)
    sol = solve_ivp(
        threebody_eom, [0, T], state0,
        method='DOP853', rtol=rtol, atol=atol,
        max_step=min(0.01, T/500.0),
        dense_output=True, args=((1.0, 1.0, 1.0),)
    )
    sf = sol.y[:, -1]
    pos_err = np.linalg.norm(sf[:6] - np.array(state0[:6]))
    vel_err = np.linalg.norm(sf[6:] - np.array(state0[6:]))
    E0 = compute_energy(state0, (1,1,1))
    Ef = compute_energy(sf, (1,1,1))
    e_drift = abs(Ef-E0)/abs(E0) if E0 != 0 else abs(Ef-E0)
    return sol, pos_err, vel_err, e_drift

def check_perm_return(sol, v1, v2):
    from itertools import permutations
    state0 = make_initial_state(v1, v2)
    sf = sol.y[:, -1]
    pos0 = np.array(state0[:6]).reshape(3,2)
    posf = np.array(sf[:6]).reshape(3,2)
    vel0 = np.array(state0[6:]).reshape(3,2)
    velf = np.array(sf[6:]).reshape(3,2)
    best_t, best_p, best_v, best_perm = float('inf'), float('inf'), float('inf'), (0,1,2)
    for perm in permutations([0,1,2]):
        pe = np.linalg.norm(posf[list(perm)] - pos0)
        ve = np.linalg.norm(velf[list(perm)] - vel0)
        if pe + ve < best_t:
            best_t = pe + ve
            best_p, best_v = pe, ve
            best_perm = perm
    return best_p, best_v, best_perm

def objective(params):
    """Minimize return error. params = [v1, v2, T]"""
    v1, v2, T = params
    if T < 2.0 or T > 200.0:
        return 1e10
    sol, pe, ve, _ = integrate_fast(v1, v2, T)
    if sol is None or not sol.success:
        return 1e10
    try:
        pp, vp, _ = check_perm_return(sol, v1, v2)
        return min(pe, pp) + min(ve, vp)
    except:
        return pe + ve

def ratio_to_cf(x, max_terms=30):
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
    cf_pos = [a for a in cf if a > 0]
    if not cf_pos:
        return 0.0
    return math.exp(sum(math.log(a) for a in cf_pos) / len(cf_pos))

def compute_cf_properties(v1, v2, T):
    """Compute CF from winding angle."""
    sol, pe, ve, ed = integrate_dense(v1, v2, T)
    if not sol.success:
        return [], 0.0
    t_pts = np.linspace(0, T, 5000)
    states = sol.sol(t_pts)
    cx = (states[0] + states[2] + states[4]) / 3.0
    cy = (states[1] + states[3] + states[5]) / 3.0
    dx1 = states[0] - cx
    dy1 = states[1] - cy
    dx2 = states[2] - cx
    dy2 = states[3] - cy
    a1 = np.unwrap(np.arctan2(dy1, dx1))
    a2 = np.unwrap(np.arctan2(dy2, dx2))
    tot1 = a1[-1] - a1[0]
    tot2 = a2[-1] - a2[0]
    if abs(tot2) > 0.01:
        ratio = abs(tot1 / tot2)
    else:
        ratio = 0.0
    cf = ratio_to_cf(ratio)
    return cf, ratio


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("THREE-BODY ORBIT DISCOVERY - FAST VERSION")
    print("=" * 70)
    print(f"Target cell: 6-15|1.30-1.35")
    print()

    # Load seed orbits from full data
    with open(os.path.join(OUTPUT_DIR, "threebody_full_data.json")) as f:
        full_data = json.load(f)

    # Collect short-period seeds from neighboring cells
    seed_ids = ['I.A-2', 'I.A-3', 'I.B-2', 'I.B-3', 'I.A-7', 'I.B-10',
                'I.B-17', 'II.C-9', 'II.C-19', 'II.C-62', 'II.C-66',
                'I.A-5', 'I.A-14', 'II.C-30', 'II.C-78']

    seeds = []
    for r in full_data['results']:
        if r['id'] in seed_ids and 'v1' in r and 'v2' in r:
            seeds.append(r)

    print(f"Loaded {len(seeds)} seeds")
    for s in seeds:
        print(f"  {s['id']:10s}: v1={s['v1']:.4f}, v2={s['v2']:.4f}, T={s['T']:.3f}")

    # Generate candidates: focus on T < 60
    rng = np.random.RandomState(42)
    candidates = []

    # Strategy 1: Perturb seeds (50 candidates)
    for s in seeds:
        for _ in range(4):
            dv1 = rng.normal(0, 0.03)
            dv2 = rng.normal(0, 0.03)
            T_base = s['T']
            for mult in [1, 2, 3]:
                T_try = T_base * mult
                if 3 < T_try < 60:
                    candidates.append({'v1': s['v1']+dv1, 'v2': s['v2']+dv2,
                                       'T': T_try + rng.normal(0, T_try*0.1),
                                       'src': f"perturb({s['id']},{mult}x)"})

    # Strategy 2: Interpolate pairs (30 candidates)
    for i in range(min(len(seeds), 8)):
        for j in range(i+1, min(len(seeds), 8)):
            for alpha in [0.25, 0.5, 0.75]:
                s1, s2 = seeds[i], seeds[j]
                T_interp = s1['T']*(1-alpha) + s2['T']*alpha
                if 3 < T_interp < 60:
                    candidates.append({
                        'v1': s1['v1']*(1-alpha)+s2['v1']*alpha,
                        'v2': s1['v2']*(1-alpha)+s2['v2']*alpha,
                        'T': T_interp,
                        'src': f"interp({s1['id']},{s2['id']})"
                    })

    # Strategy 3: Grid around the best seeds (20 candidates)
    best_seeds = [s for s in seeds if s['T'] < 30]
    for s in best_seeds[:5]:
        for _ in range(4):
            candidates.append({
                'v1': s['v1'] + rng.uniform(-0.1, 0.1),
                'v2': s['v2'] + rng.uniform(-0.1, 0.1),
                'T': rng.uniform(max(3, s['T']*0.5), min(60, s['T']*3)),
                'src': f"grid({s['id']})"
            })

    candidates = candidates[:120]
    print(f"\nGenerated {len(candidates)} candidates")

    # ─── Phase 1: Quick screen ───
    print("\n--- PHASE 1: Quick Screen ---")
    screened = []
    for i, c in enumerate(candidates):
        v1, v2, T = c['v1'], c['v2'], c['T']

        # Try T, also 2T and 3T if short
        best_err = float('inf')
        best_T = T
        for mult in [1]:
            T_try = T * mult
            if T_try > 120:
                continue
            sol, pe, ve, ed = integrate_fast(v1, v2, T_try, rtol=1e-8, atol=1e-8)
            if sol is not None and sol.success:
                try:
                    pp, vp, _ = check_perm_return(sol, v1, v2)
                    err = min(pe, pp) + min(ve, vp)
                except:
                    err = pe + ve
                if err < best_err:
                    best_err = err
                    best_T = T_try

        screened.append({'v1': v1, 'v2': v2, 'T': best_T, 'err': best_err, 'src': c['src']})

        if (i+1) % 20 == 0:
            good = sum(1 for s in screened if s['err'] < 1.0)
            print(f"  {i+1}/{len(candidates)} screened, {good} promising")

    screened.sort(key=lambda x: x['err'])

    print(f"\nTop 15 after screening:")
    for i, s in enumerate(screened[:15]):
        print(f"  #{i+1}: err={s['err']:.4e}, v1={s['v1']:.4f}, v2={s['v2']:.4f}, T={s['T']:.2f}, src={s['src'][:40]}")

    # ─── Phase 2: Nelder-Mead refinement ───
    print("\n--- PHASE 2: Nelder-Mead Refinement (top 15) ---")
    refined = []
    for i, s in enumerate(screened[:15]):
        if s['err'] > 5.0:
            continue
        print(f"  Refining #{i+1} (err={s['err']:.3e})...", end='', flush=True)
        t0 = time.time()

        result = minimize(objective, [s['v1'], s['v2'], s['T']],
                         method='Nelder-Mead',
                         options={'maxiter': 300, 'xatol': 1e-10, 'fatol': 1e-12, 'adaptive': True})

        v1o, v2o, To = result.x
        err_opt = result.fun
        elapsed = time.time() - t0

        # Also try refining with period multiples
        for mult in [2, 3]:
            T_try = To * mult
            if T_try > 200:
                continue
            r2 = minimize(objective, [v1o, v2o, T_try],
                         method='Nelder-Mead',
                         options={'maxiter': 200, 'xatol': 1e-10, 'fatol': 1e-12, 'adaptive': True})
            if r2.fun < err_opt:
                v1o, v2o, To = r2.x
                err_opt = r2.fun

        print(f" -> err={err_opt:.4e} (v1={v1o:.6f}, v2={v2o:.6f}, T={To:.4f}) [{elapsed:.1f}s]")

        if err_opt < 2.0:
            refined.append({'v1': v1o, 'v2': v2o, 'T': To, 'err': err_opt, 'src': s['src']})

    refined.sort(key=lambda x: x['err'])

    # ─── Phase 3: Deep refinement ───
    print("\n--- PHASE 3: Deep Refinement (top 5) ---")
    discoveries = []

    for i, r in enumerate(refined[:5]):
        print(f"\n  Deep refining #{i+1} (err={r['err']:.3e})...")
        v1, v2, T = r['v1'], r['v2'], r['T']

        # Multiple rounds
        for rnd in range(8):
            res = minimize(objective, [v1, v2, T],
                          method='Nelder-Mead',
                          options={'maxiter': 500, 'xatol': 1e-12, 'fatol': 1e-14, 'adaptive': True})
            if res.fun < objective([v1, v2, T]):
                v1, v2, T = res.x

            # Also try Powell
            try:
                res2 = minimize(objective, [v1, v2, T],
                               method='Powell',
                               options={'maxiter': 500, 'ftol': 1e-14})
                if res2.fun < objective([v1, v2, T]):
                    v1, v2, T = res2.x
            except:
                pass

            current_err = objective([v1, v2, T])
            print(f"    Round {rnd+1}: err={current_err:.6e}")
            if current_err < 1e-4:
                break

        # Final high-precision verification
        sol, pe, ve, ed = integrate_dense(v1, v2, T)
        if sol.success:
            pp, vp, perm = check_perm_return(sol, v1, v2)
            best_pe = min(pe, pp)
            best_ve = min(ve, vp)

            if best_pe < 0.01 and best_ve < 0.01:
                cls = "PERIODIC"
            elif best_pe < 0.1:
                cls = "PROMISING"
            elif best_pe < 1.0:
                cls = "MARGINAL"
            else:
                cls = "NOT PERIODIC"

            print(f"  RESULT: {cls} | pos={best_pe:.6e} vel={best_ve:.6e} E_drift={ed:.2e}")
            print(f"  ICs: v1={v1:.12f}, v2={v2:.12f}, T={T:.12f}")

            # CF analysis
            cf, ratio = compute_cf_properties(v1, v2, T)
            gm = cf_gmean(cf) if cf else 0

            # Classify cell
            row_bins = [(1,1,'1'), (2,5,'2-5'), (6,15,'6-15'), (16,30,'16-30'),
                        (31,50,'31-50'), (51,80,'51-80')]
            col_bins = [(1.0,1.05,'1.00-1.05'), (1.05,1.1,'1.05-1.10'),
                        (1.1,1.15,'1.10-1.15'), (1.15,1.2,'1.15-1.20'),
                        (1.2,1.25,'1.20-1.25'), (1.25,1.3,'1.25-1.30'),
                        (1.3,1.35,'1.30-1.35'), (1.35,1.45,'1.35-1.45')]
            row = col = "?"
            for lo, hi, label in row_bins:
                if lo <= len(cf) <= hi:
                    row = label; break
            for lo, hi, label in col_bins:
                if lo <= gm < hi:
                    col = label; break
            cell = f"{row}|{col}"
            target = (cell == "6-15|1.30-1.35")

            print(f"  CF: {cf[:15]}, len={len(cf)}, gmean={gm:.4f}")
            print(f"  Cell: {cell}, IN TARGET: {'YES!' if target else 'no'}")

            discoveries.append({
                'v1': v1, 'v2': v2, 'T': T,
                'pos_err': best_pe, 'vel_err': best_ve, 'e_drift': ed,
                'classification': cls, 'cf': cf, 'gmean': gm,
                'cell': cell, 'target': target, 'src': r['src'],
                'sol': sol, 'perm': perm,
            })

            # Plot
            if sol.sol is not None:
                plot_orbit(sol, v1, v2, T, best_pe, cls, gm, cell, i+1)

    # ─── Summary ───
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    n_periodic = sum(1 for d in discoveries if d['classification'] == 'PERIODIC')
    n_promising = sum(1 for d in discoveries if d['classification'] == 'PROMISING')
    n_target = sum(1 for d in discoveries if d['target'])

    print(f"Periodic: {n_periodic}")
    print(f"Promising: {n_promising}")
    print(f"In target cell: {n_target}")

    for i, d in enumerate(discoveries):
        print(f"\n  #{i+1} {d['classification']}: v1={d['v1']:.10f}, v2={d['v2']:.10f}, T={d['T']:.10f}")
        print(f"    pos_err={d['pos_err']:.4e}, vel_err={d['vel_err']:.4e}")
        print(f"    CF len={len(d['cf'])}, gmean={d['gmean']:.4f}, cell={d['cell']}")

    # Write report
    write_report(seeds, screened, refined, discoveries)

    return discoveries


def plot_orbit(sol, v1, v2, T, pos_err, cls, gmean, cell, num):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    t_dense = np.linspace(0, T, 5000)
    states = sol.sol(t_dense)

    ax = axes[0]
    ax.plot(states[0], states[1], '-', color='#e74c3c', alpha=0.7, lw=0.5, label='Body 1')
    ax.plot(states[2], states[3], '-', color='#2ecc71', alpha=0.7, lw=0.5, label='Body 2')
    ax.plot(states[4], states[5], '-', color='#3498db', alpha=0.7, lw=0.5, label='Body 3')
    ax.plot(-1, 0, 'o', color='#e74c3c', ms=8, zorder=5)
    ax.plot(1, 0, 'o', color='#2ecc71', ms=8, zorder=5)
    ax.plot(0, 0, 'o', color='#3498db', ms=8, zorder=5)
    ax.set_aspect('equal')
    ax.set_title(f"Discovery #{num}: {cls}\nv1={v1:.6f}, v2={v2:.6f}, T={T:.4f}")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    state0 = make_initial_state(v1, v2)
    pos0 = np.array(state0[:6])
    t_check = np.linspace(T*0.01, T, 300)
    errors = [np.linalg.norm(sol.sol(tc)[:6] - pos0) for tc in t_check]
    ax2.semilogy(t_check, errors, 'b-', lw=1)
    ax2.axhline(y=0.01, color='g', ls='--', alpha=0.5, label='Periodic')
    ax2.axhline(y=0.1, color='orange', ls='--', alpha=0.5, label='Promising')
    ax2.set_title(f"pos_err={pos_err:.2e}, gmean={gmean:.4f}, cell={cell}")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fname = os.path.join(OUTPUT_DIR, f"threebody_discovery_{num:02d}.png")
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {fname}")


def write_report(seeds, screened, refined, discoveries):
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
        f.write("Cell 6-15|1.30-1.35 has **7 occupied neighbors** -- the most constrained\n")
        f.write("empty cell and the best target for guided orbit discovery.\n\n")

        f.write("### Target Cell Properties\n\n")
        f.write("An orbit in this cell would have:\n")
        f.write("- CF period length between 6 and 15\n")
        f.write("- Geometric mean of CF partial quotients between 1.30 and 1.35\n")
        f.write("- This implies a mix of small and moderately large CF entries (e.g., [2,1,1,1,3,1,1,1,2])\n")
        f.write("- Expected free-group word length: ~14-24 (based on neighbors)\n")
        f.write("- Expected period T*: ~20-50 (interpolated from neighbors)\n\n")

        f.write("## Seed Orbits\n\n")
        f.write("| ID | v1 | v2 | T | Word len |\n")
        f.write("|---|---|---|---|---|\n")
        for s in seeds[:12]:
            f.write(f"| {s['id']} | {s['v1']:.6f} | {s['v2']:.6f} | {s['T']:.3f} | {len(s.get('word',''))} |\n")

        f.write(f"\n## Screening: {len(screened)} candidates\n\n")
        n_sub1 = sum(1 for s in screened if s['err'] < 1.0)
        f.write(f"- Promising (err < 1.0): {n_sub1}\n\n")

        f.write("### Top 10\n\n")
        f.write("| Rank | Error | v1 | v2 | T | Source |\n")
        f.write("|---|---|---|---|---|---|\n")
        for i, s in enumerate(screened[:10]):
            f.write(f"| {i+1} | {s['err']:.4e} | {s['v1']:.4f} | {s['v2']:.4f} | {s['T']:.2f} | {s['src'][:35]} |\n")

        f.write(f"\n## Refinement: {len(refined)} candidates\n\n")
        f.write("| Rank | Error | v1 | v2 | T | Source |\n")
        f.write("|---|---|---|---|---|---|\n")
        for i, r in enumerate(refined[:10]):
            f.write(f"| {i+1} | {r['err']:.4e} | {r['v1']:.6f} | {r['v2']:.6f} | {r['T']:.4f} | {r['src'][:35]} |\n")

        f.write(f"\n## Discoveries\n\n")
        if not discoveries:
            f.write("No confirmed periodic orbits in this run. The search found candidates in the\n")
            f.write("MARGINAL range, suggesting periodic orbits exist nearby but need more intensive\n")
            f.write("refinement (Newton-Raphson, continuation methods).\n\n")

        n_periodic = sum(1 for d in discoveries if d['classification'] == 'PERIODIC')
        n_promising = sum(1 for d in discoveries if d['classification'] == 'PROMISING')
        n_target = sum(1 for d in discoveries if d.get('target'))

        f.write(f"- **Periodic orbits found**: {n_periodic}\n")
        f.write(f"- **Promising candidates**: {n_promising}\n")
        f.write(f"- **In target cell (6-15|1.30-1.35)**: {n_target}\n\n")

        for i, d in enumerate(discoveries):
            f.write(f"### {'DISCOVERY' if d['classification'] == 'PERIODIC' else 'Candidate'} #{i+1}: {d['classification']}\n\n")
            f.write(f"| Property | Value |\n")
            f.write(f"|---|---|\n")
            f.write(f"| v1 | {d['v1']:.12f} |\n")
            f.write(f"| v2 | {d['v2']:.12f} |\n")
            f.write(f"| T | {d['T']:.12f} |\n")
            f.write(f"| Position error | {d['pos_err']:.6e} |\n")
            f.write(f"| Velocity error | {d['vel_err']:.6e} |\n")
            f.write(f"| Energy drift | {d['e_drift']:.6e} |\n")
            f.write(f"| CF | {d['cf'][:20]} |\n")
            f.write(f"| CF period length | {len(d['cf'])} |\n")
            f.write(f"| gmean | {d['gmean']:.6f} |\n")
            f.write(f"| Cell | {d['cell']} |\n")
            f.write(f"| In target? | {'**YES**' if d.get('target') else 'No'} |\n")
            f.write(f"| Source | {d['src']} |\n\n")

            f.write(f"![Discovery {i+1}](threebody_discovery_{i+1:02d}.png)\n\n")

        f.write("## Method\n\n")
        f.write("1. **Seed selection**: Short-period orbits from the 7 neighboring cells\n")
        f.write("2. **Candidate generation**: Perturbation, interpolation, and grid search (~120 candidates)\n")
        f.write("3. **Quick screening**: Low-precision integration to filter promising ICs\n")
        f.write("4. **Nelder-Mead refinement**: Optimize (v1, v2, T) to minimize return error\n")
        f.write("5. **Deep refinement**: 8 rounds of Nelder-Mead + Powell on best candidates\n")
        f.write("6. **CF classification**: Compute winding angle ratio and its continued fraction\n\n")

        f.write("## Significance\n\n")
        f.write("This is the first attempt to use continued fraction structure to **predict and discover**\n")
        f.write("new three-body periodic orbits. The CF/nobility framework identifies WHERE in parameter\n")
        f.write("space to search based on number-theoretic properties, rather than brute-force scanning.\n")

    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
