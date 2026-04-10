#!/usr/bin/env python3
"""
Three-Body Orbit Gap Verification via N-Body Integration
==========================================================

Verifies predicted periodic orbits from Stern-Brocot gap analysis by
running high-precision N-body integrations with scipy.

For each predicted orbit:
  - Integrate the planar three-body problem (equal masses)
  - Check if the trajectory returns to its initial conditions (periodicity)
  - Measure return error ||r(T) - r(0)||

Also verifies known orbits as controls to validate the integrator.

Author: Saar (with Claude)
Date: 2026-03-27
"""

import json
import os
import sys
import time
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")

# ═══════════════════════════════════════════════════════════════════
# 1. THREE-BODY EQUATIONS OF MOTION
# ═══════════════════════════════════════════════════════════════════

def threebody_eom(t, state, masses):
    """
    Equations of motion for the planar three-body problem.

    state = [x1, y1, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3]
    masses = [m1, m2, m3]

    Returns d(state)/dt.
    """
    G = 1.0  # Gravitational constant

    x1, y1 = state[0], state[1]
    x2, y2 = state[2], state[3]
    x3, y3 = state[4], state[5]
    vx1, vy1 = state[6], state[7]
    vx2, vy2 = state[8], state[9]
    vx3, vy3 = state[10], state[11]

    m1, m2, m3 = masses

    # Distances
    dx12, dy12 = x2 - x1, y2 - y1
    dx13, dy13 = x3 - x1, y3 - y1
    dx23, dy23 = x3 - x2, y3 - y2

    r12 = np.sqrt(dx12**2 + dy12**2)
    r13 = np.sqrt(dx13**2 + dy13**2)
    r23 = np.sqrt(dx23**2 + dy23**2)

    r12_3 = r12**3
    r13_3 = r13**3
    r23_3 = r23**3

    # Accelerations
    ax1 = G * m2 * dx12 / r12_3 + G * m3 * dx13 / r13_3
    ay1 = G * m2 * dy12 / r12_3 + G * m3 * dy13 / r13_3

    ax2 = -G * m1 * dx12 / r12_3 + G * m3 * dx23 / r23_3
    ay2 = -G * m1 * dy12 / r12_3 + G * m3 * dy23 / r23_3

    ax3 = -G * m1 * dx13 / r13_3 - G * m2 * dx23 / r23_3
    ay3 = -G * m1 * dy13 / r13_3 - G * m2 * dy23 / r23_3

    return [vx1, vy1, vx2, vy2, vx3, vy3,
            ax1, ay1, ax2, ay2, ax3, ay3]


def compute_energy(state, masses):
    """Compute total energy (kinetic + potential) for conservation check."""
    G = 1.0
    x1, y1 = state[0], state[1]
    x2, y2 = state[2], state[3]
    x3, y3 = state[4], state[5]
    vx1, vy1 = state[6], state[7]
    vx2, vy2 = state[8], state[9]
    vx3, vy3 = state[10], state[11]
    m1, m2, m3 = masses

    KE = 0.5 * (m1 * (vx1**2 + vy1**2) +
                m2 * (vx2**2 + vy2**2) +
                m3 * (vx3**2 + vy3**2))

    r12 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    r13 = np.sqrt((x3-x1)**2 + (y3-y1)**2)
    r23 = np.sqrt((x3-x2)**2 + (y3-y2)**2)

    PE = -G * (m1*m2/r12 + m1*m3/r13 + m2*m3/r23)

    return KE + PE


# ═══════════════════════════════════════════════════════════════════
# 2. INTEGRATION AND PERIODICITY CHECK
# ═══════════════════════════════════════════════════════════════════

def make_initial_state(v1, v2):
    """
    Construct initial state for equal-mass zero-angular-momentum three-body.

    Li & Liao catalog convention:
      r1 = (-1, 0), r2 = (1, 0), r3 = (0, 0)
      v1 = v2 = (v1, v2)
      v3 = -2*(v1, v2)

    This ensures zero total momentum: m*(v1+v2+v3) = m*(v + v - 2v) = 0.
    """
    # Positions
    x1, y1 = -1.0, 0.0
    x2, y2 = 1.0, 0.0
    x3, y3 = 0.0, 0.0

    # Velocities (Li & Liao convention)
    vx1, vy1 = v1, v2       # Body 1
    vx2, vy2 = v1, v2       # Body 2 (same as body 1)
    vx3, vy3 = -2*v1, -2*v2 # Body 3 (ensures zero momentum)

    return [x1, y1, x2, y2, x3, y3,
            vx1, vy1, vx2, vy2, vx3, vy3]


def integrate_orbit(v1, v2, T, masses=(1.0, 1.0, 1.0),
                    rtol=1e-12, atol=1e-12, max_step=0.01,
                    dense_output=True):
    """
    Integrate a three-body orbit and return results.

    Returns:
        sol: scipy ODE solution object
        return_error: ||r(T) - r(0)|| (position-space return distance)
        vel_error: ||v(T) - v(0)|| (velocity-space return distance)
        energy_drift: |E(T) - E(0)| / |E(0)|
    """
    state0 = make_initial_state(v1, v2)

    E0 = compute_energy(state0, masses)

    sol = solve_ivp(
        threebody_eom,
        [0, T],
        state0,
        method='DOP853',
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=dense_output,
        args=(masses,)
    )

    if not sol.success:
        return sol, float('inf'), float('inf'), float('inf')

    state_final = sol.y[:, -1]

    # Position return error (all 3 bodies)
    pos0 = np.array(state0[:6])
    posf = np.array(state_final[:6])
    return_error = np.linalg.norm(posf - pos0)

    # Velocity return error
    vel0 = np.array(state0[6:])
    velf = np.array(state_final[6:])
    vel_error = np.linalg.norm(velf - vel0)

    # Energy conservation check
    Ef = compute_energy(state_final, masses)
    energy_drift = abs(Ef - E0) / abs(E0) if E0 != 0 else abs(Ef - E0)

    return sol, return_error, vel_error, energy_drift


def check_permutation_return(sol, v1, v2, T):
    """
    Check if the orbit returns modulo body permutations.

    In the three-body problem, after time T bodies may have permuted.
    The full period is kT where k is the smallest integer such that
    bodies return to their original positions.

    We check all 6 permutations of (body1, body2, body3).
    """
    state0 = make_initial_state(v1, v2)
    state_f = sol.y[:, -1]

    pos0 = np.array(state0[:6]).reshape(3, 2)  # [[x1,y1],[x2,y2],[x3,y3]]
    posf = np.array(state_f[:6]).reshape(3, 2)

    vel0 = np.array(state0[6:]).reshape(3, 2)
    velf = np.array(state_f[6:]).reshape(3, 2)

    # All permutations of 3 bodies
    from itertools import permutations
    best_pos_err = float('inf')
    best_vel_err = float('inf')
    best_perm = None

    for perm in permutations([0, 1, 2]):
        posf_perm = posf[list(perm)]
        velf_perm = velf[list(perm)]
        pos_err = np.linalg.norm(posf_perm - pos0)
        vel_err = np.linalg.norm(velf_perm - vel0)
        total = pos_err + vel_err
        if total < best_pos_err + best_vel_err:
            best_pos_err = pos_err
            best_vel_err = vel_err
            best_perm = perm

    return best_pos_err, best_vel_err, best_perm


def classify_result(return_error, vel_error):
    """Classify orbit based on return error."""
    if return_error < 0.01 and vel_error < 0.01:
        return "LIKELY PERIODIC"
    elif return_error < 0.1:
        return "PROMISING"
    elif return_error < 1.0:
        return "MARGINAL"
    else:
        return "NOT PERIODIC"


# ═══════════════════════════════════════════════════════════════════
# 3. ORBIT PLOTTING
# ═══════════════════════════════════════════════════════════════════

def plot_orbit(sol, title, filename, v1, v2, T, return_error, classification):
    """Plot trajectory of all three bodies in x-y plane."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left panel: full orbit
    ax = axes[0]
    t_dense = np.linspace(0, T, 5000)
    states = sol.sol(t_dense)

    ax.plot(states[0], states[1], '-', color='#e74c3c', alpha=0.7, lw=0.8, label='Body 1')
    ax.plot(states[2], states[3], '-', color='#2ecc71', alpha=0.7, lw=0.8, label='Body 2')
    ax.plot(states[4], states[5], '-', color='#3498db', alpha=0.7, lw=0.8, label='Body 3')

    # Mark initial positions
    ax.plot(-1, 0, 'o', color='#e74c3c', ms=8, zorder=5)
    ax.plot(1, 0, 'o', color='#2ecc71', ms=8, zorder=5)
    ax.plot(0, 0, 'o', color='#3498db', ms=8, zorder=5)

    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'{title}\nv1={v1:.4f}, v2={v2:.4f}, T={T:.3f}')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Right panel: return distance over time
    ax2 = axes[1]
    n_check = 200
    t_check = np.linspace(T*0.01, T, n_check)
    errors = []
    state0 = make_initial_state(v1, v2)
    pos0 = np.array(state0[:6])

    for tc in t_check:
        sc = sol.sol(tc)
        err = np.linalg.norm(sc[:6] - pos0)
        errors.append(err)

    ax2.semilogy(t_check, errors, 'b-', lw=1)
    ax2.axhline(y=0.01, color='g', ls='--', alpha=0.5, label='Periodic threshold')
    ax2.axhline(y=0.1, color='orange', ls='--', alpha=0.5, label='Promising threshold')
    ax2.axhline(y=1.0, color='r', ls='--', alpha=0.5, label='Failure threshold')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('||r(t) - r(0)||')
    ax2.set_title(f'Return error = {return_error:.6f}\n{classification}')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


# ═══════════════════════════════════════════════════════════════════
# 4. MAIN VERIFICATION
# ═══════════════════════════════════════════════════════════════════

def load_data():
    """Load the full catalog data."""
    data_path = os.path.join(OUTPUT_DIR, "threebody_full_data.json")
    with open(data_path) as f:
        return json.load(f)


def get_known_controls(data):
    """
    Extract known orbits for control verification.

    We pick orbits with short words (simple, well-studied) that should
    have very small return errors with their catalog ICs.
    """
    results = data.get("results", [])

    controls = []
    # Target IDs: figure-eight (I.A-1), and a few other well-known short orbits
    target_ids = {"I.A-1", "I.A-2", "I.A-3", "I.B-1", "II.C-2"}

    for r in results:
        if r["id"] in target_ids and "v1" in r and "v2" in r and "T" in r:
            controls.append({
                "id": r["id"],
                "word": r["word"],
                "v1": r["v1"],
                "v2": r["v2"],
                "T": r["T"],
                "family": r["family"],
                "word_length": r.get("word_length", len(r["word"])),
            })

    return controls


def run_verification():
    """Main verification pipeline."""
    print("=" * 70)
    print("THREE-BODY ORBIT GAP VERIFICATION")
    print("=" * 70)

    data = load_data()
    gap_predictions = data.get("gap_predictions", [])

    print(f"\nLoaded {len(gap_predictions)} gap predictions")

    # ─── PHASE 1: Control orbits (known) ───
    print("\n" + "─" * 70)
    print("PHASE 1: CONTROL ORBITS (Known periodic orbits)")
    print("─" * 70)

    controls = get_known_controls(data)
    print(f"Found {len(controls)} control orbits: {[c['id'] for c in controls]}")

    control_results = []
    for ctrl in controls:
        print(f"\n  Integrating {ctrl['id']} (word: {ctrl['word'][:20]}{'...' if len(ctrl['word'])>20 else ''}, T={ctrl['T']:.4f})...")

        # Try T, 2T, 3T to handle body permutation periods
        best_result = None
        best_total_err = float('inf')
        best_sol = None
        best_mult = 1

        for mult in [1, 2, 3]:
            T_try = ctrl['T'] * mult
            t0 = time.time()
            max_step = min(0.01, ctrl['T'] / 500.0)

            sol, ret_err, vel_err, e_drift = integrate_orbit(
                ctrl['v1'], ctrl['v2'], T_try,
                max_step=max_step
            )
            elapsed = time.time() - t0

            # Also check permutation returns
            if sol.success:
                perm_pos, perm_vel, perm_idx = check_permutation_return(
                    sol, ctrl['v1'], ctrl['v2'], T_try
                )
                # Use the better of identity and permuted return
                eff_pos = min(ret_err, perm_pos)
                eff_vel = min(vel_err, perm_vel)
            else:
                eff_pos, eff_vel = ret_err, vel_err
                perm_pos, perm_vel, perm_idx = ret_err, vel_err, (0,1,2)

            total = eff_pos + eff_vel
            if total < best_total_err:
                best_total_err = total
                best_mult = mult
                best_sol = sol
                best_result = {
                    "id": ctrl['id'],
                    "word": ctrl['word'],
                    "v1": ctrl['v1'],
                    "v2": ctrl['v2'],
                    "T_catalog": ctrl['T'],
                    "T_used": T_try,
                    "T_multiplier": mult,
                    "return_error": eff_pos,
                    "velocity_error": eff_vel,
                    "return_error_identity": ret_err,
                    "return_error_perm": perm_pos,
                    "best_perm": list(perm_idx) if perm_idx else [0,1,2],
                    "energy_drift": e_drift,
                    "classification": classify_result(eff_pos, eff_vel),
                    "elapsed_s": elapsed,
                    "success": sol.success
                }

            print(f"    {mult}T={T_try:.4f}: pos_err={eff_pos:.2e} (id:{ret_err:.2e}, perm:{perm_pos:.2e}), "
                  f"vel_err={eff_vel:.2e}, E_drift={e_drift:.2e}")

        control_results.append(best_result)
        print(f"    BEST: {best_mult}T, {best_result['classification']}")

        # Plot with best multiplier
        if best_sol and best_sol.success and hasattr(best_sol, 'sol') and best_sol.sol is not None:
            plot_orbit(
                best_sol, f"Control: {ctrl['id']} ({ctrl['word'][:20]}...) [{best_mult}T]",
                os.path.join(OUTPUT_DIR, f"threebody_orbit_control_{ctrl['id'].replace('.','_')}.png"),
                ctrl['v1'], ctrl['v2'], ctrl['T'] * best_mult,
                best_result['return_error'], best_result['classification']
            )

    # ─── PHASE 2: Gap predictions ───
    print("\n" + "─" * 70)
    print("PHASE 2: GAP PREDICTIONS (Interpolated initial conditions)")
    print("─" * 70)

    gap_results = []
    for gap in gap_predictions:
        rank = gap['rank']
        v1 = gap['predicted_v1']
        v2 = gap['predicted_v2']
        T = gap['predicted_T']

        print(f"\n  Gap #{rank}: {gap['left_id']} <-> {gap['right_id']}")
        print(f"    v1={v1:.6f}, v2={v2:.6f}, T={T:.3f}")

        # Try T, 2T, 3T
        best_result = None
        best_total_err = float('inf')
        best_sol = None
        best_mult = 1

        for mult in [1, 2, 3]:
            T_try = T * mult
            t0 = time.time()
            max_step = min(0.05, T / 200.0)

            sol, ret_err, vel_err, e_drift = integrate_orbit(
                v1, v2, T_try, max_step=max_step
            )
            elapsed = time.time() - t0

            if sol.success:
                perm_pos, perm_vel, perm_idx = check_permutation_return(
                    sol, v1, v2, T_try
                )
                eff_pos = min(ret_err, perm_pos)
                eff_vel = min(vel_err, perm_vel)
            else:
                eff_pos, eff_vel = ret_err, vel_err
                perm_pos, perm_vel, perm_idx = ret_err, vel_err, (0,1,2)

            total = eff_pos + eff_vel
            if total < best_total_err:
                best_total_err = total
                best_mult = mult
                best_sol = sol
                best_result = {
                    "rank": rank,
                    "left_id": gap['left_id'],
                    "right_id": gap['right_id'],
                    "midpoint_fp": gap['midpoint_fp'],
                    "gap_size": gap['gap_size'],
                    "v1": v1,
                    "v2": v2,
                    "T_predicted": T,
                    "T_used": T_try,
                    "T_multiplier": mult,
                    "return_error": eff_pos,
                    "velocity_error": eff_vel,
                    "energy_drift": e_drift,
                    "classification": classify_result(eff_pos, eff_vel),
                    "elapsed_s": elapsed,
                    "success": sol.success
                }

            print(f"    {mult}T={T_try:.3f}: pos_err={eff_pos:.2e}, vel_err={eff_vel:.2e}, E_drift={e_drift:.2e}")

        gap_results.append(best_result)
        print(f"    BEST: {best_mult}T, {best_result['classification']}")

        # Plot
        if best_sol and best_sol.success and hasattr(best_sol, 'sol') and best_sol.sol is not None:
            plot_orbit(
                best_sol, f"Gap #{rank}: {gap['left_id']} <-> {gap['right_id']} [{best_mult}T]",
                os.path.join(OUTPUT_DIR, f"threebody_orbit_gap_{rank:02d}.png"),
                v1, v2, T * best_mult, best_result['return_error'],
                best_result['classification']
            )

    # ─── PHASE 3: Summary ───
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    # Control summary
    print("\nControl Orbits:")
    for r in control_results:
        sym = "OK" if "PERIODIC" in r['classification'] else "XX"
        mult_str = f"[{r.get('T_multiplier',1)}T]" if r.get('T_multiplier',1) > 1 else ""
        print(f"  [{sym}] {r['id']:10s}  ret_err={r['return_error']:.2e}  "
              f"vel_err={r['velocity_error']:.2e}  E_drift={r['energy_drift']:.2e}  "
              f"{r['classification']} {mult_str}")

    # Gap summary
    print("\nGap Predictions:")
    n_periodic = 0
    n_promising = 0
    n_failed = 0
    for r in gap_results:
        if r['classification'] == "LIKELY PERIODIC":
            sym = "**"
            n_periodic += 1
        elif r['classification'] == "PROMISING":
            sym = "* "
            n_promising += 1
        elif r['classification'] == "MARGINAL":
            sym = "? "
            n_promising += 1
        else:
            sym = "  "
            n_failed += 1
        print(f"  [{sym}] Gap #{r['rank']:2d}  ret_err={r['return_error']:.2e}  "
              f"vel_err={r['velocity_error']:.2e}  E_drift={r['energy_drift']:.2e}  "
              f"{r['classification']}")

    print(f"\n  Likely periodic: {n_periodic}/10")
    print(f"  Promising/Marginal: {n_promising}/10")
    print(f"  Not periodic: {n_failed}/10")

    # ─── Write report ───
    write_report(control_results, gap_results)

    return control_results, gap_results


def write_report(control_results, gap_results):
    """Write verification report as markdown."""
    report_path = os.path.join(OUTPUT_DIR, "THREEBODY_VERIFICATION.md")

    with open(report_path, 'w') as f:
        f.write("# Three-Body Gap Verification Results\n\n")
        f.write("**Date**: 2026-03-27\n")
        f.write("**Method**: N-body integration (scipy DOP853, rtol=atol=1e-12)\n")
        f.write("**Setup**: Equal masses m1=m2=m3=1, planar, zero angular momentum\n")
        f.write("**Initial positions**: r1=(-1,0), r2=(1,0), r3=(0,0)\n\n")

        f.write("## Classification Thresholds\n\n")
        f.write("| Category | Position Error | Velocity Error | Meaning |\n")
        f.write("|---|---|---|---|\n")
        f.write("| LIKELY PERIODIC | < 0.01 | < 0.01 | High confidence periodic orbit |\n")
        f.write("| PROMISING | < 0.1 | any | Worth refining with Newton's method |\n")
        f.write("| MARGINAL | < 1.0 | any | Possible but needs significant refinement |\n")
        f.write("| NOT PERIODIC | > 1.0 | any | Prediction failed at this precision |\n\n")

        # Controls
        f.write("---\n\n## Control Orbits (Known Periodic)\n\n")
        f.write("These validate our integrator. Known orbits should return with very small error.\n\n")
        f.write("| ID | Word | T_cat | T_used | Mult | Pos Error | Vel Error | E Drift | Status |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for r in control_results:
            word_short = r['word'][:15] + ('...' if len(r['word']) > 15 else '')
            T_cat = r.get('T_catalog', r.get('T', 0))
            T_used = r.get('T_used', T_cat)
            mult = r.get('T_multiplier', 1)
            f.write(f"| {r['id']} | {word_short} | {T_cat:.4f} | {T_used:.4f} | {mult}x | "
                    f"{r['return_error']:.2e} | {r['velocity_error']:.2e} | "
                    f"{r['energy_drift']:.2e} | {r['classification']} |\n")

        # Assess integrator
        ctrl_ok = sum(1 for r in control_results if r['return_error'] < 0.1)
        f.write(f"\n**Integrator validation**: {ctrl_ok}/{len(control_results)} controls returned within 0.1\n\n")

        # Gap predictions
        f.write("---\n\n## Gap Predictions (Interpolated Initial Conditions)\n\n")
        f.write("These are approximate ICs from linear interpolation between neighboring orbits.\n")
        f.write("Small errors would confirm new periodic orbits; large errors suggest the gap\n")
        f.write("contains no orbit at the interpolated point (refinement needed).\n\n")

        f.write("| Rank | Gap | v1 | v2 | T_pred | T_used | Mult | Pos Error | Vel Error | E Drift | Status |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
        for r in gap_results:
            gap_label = f"{r['left_id']} / {r['right_id']}"
            T_pred = r.get('T_predicted', r.get('T', 0))
            T_used = r.get('T_used', T_pred)
            mult = r.get('T_multiplier', 1)
            f.write(f"| {r['rank']} | {gap_label} | {r['v1']:.4f} | {r['v2']:.4f} | "
                    f"{T_pred:.1f} | {T_used:.1f} | {mult}x | "
                    f"{r['return_error']:.2e} | {r['velocity_error']:.2e} | "
                    f"{r['energy_drift']:.2e} | {r['classification']} |\n")

        # Summary stats
        n_periodic = sum(1 for r in gap_results if r['classification'] == "LIKELY PERIODIC")
        n_promising = sum(1 for r in gap_results if r['classification'] in ("PROMISING", "MARGINAL"))
        n_failed = sum(1 for r in gap_results if r['classification'] == "NOT PERIODIC")

        f.write(f"\n### Summary\n\n")
        f.write(f"- **Likely periodic**: {n_periodic}/10\n")
        f.write(f"- **Promising/Marginal**: {n_promising}/10\n")
        f.write(f"- **Not periodic**: {n_failed}/10\n\n")

        if n_periodic > 0:
            f.write("### Likely New Periodic Orbits\n\n")
            for r in gap_results:
                if r['classification'] == "LIKELY PERIODIC":
                    T_pred = r.get('T_predicted', r.get('T', 0))
                    f.write(f"- **Gap #{r['rank']}** ({r['left_id']} <-> {r['right_id']}): "
                            f"v1={r['v1']:.6f}, v2={r['v2']:.6f}, T={T_pred:.3f}, "
                            f"return_error={r['return_error']:.2e}\n")
            f.write("\n")

        if n_promising > 0:
            f.write("### Candidates for Refinement\n\n")
            for r in gap_results:
                if "PROMISING" in r['classification'] or "MARGINAL" in r['classification']:
                    T_pred = r.get('T_predicted', r.get('T', 0))
                    f.write(f"- **Gap #{r['rank']}** ({r['left_id']} <-> {r['right_id']}): "
                            f"v1={r['v1']:.6f}, v2={r['v2']:.6f}, T={T_pred:.3f}, "
                            f"return_error={r['return_error']:.2e}\n")
            f.write("\n")

        f.write("---\n\n## Interpretation\n\n")
        f.write("The gap predictions use *linear interpolation* of initial conditions between\n")
        f.write("neighboring known orbits in Stern-Brocot tree position. This is a zeroth-order\n")
        f.write("approximation; real orbit-finding would use:\n\n")
        f.write("1. The interpolated ICs as a **starting point** for Newton's method\n")
        f.write("2. A **shooting method** that minimizes ||r(T)-r(0)|| + ||v(T)-v(0)||\n")
        f.write("3. Period T as a free parameter (our T is also interpolated)\n\n")
        f.write("Even marginal results (error < 1.0) suggest there may be a nearby periodic\n")
        f.write("orbit that a proper numerical search would find.\n\n")

        f.write("## Orbit Plots\n\n")
        for r in control_results:
            fn = f"threebody_orbit_control_{r['id'].replace('.','_')}.png"
            f.write(f"### Control: {r['id']}\n")
            f.write(f"![{r['id']}]({fn})\n\n")

        for r in gap_results:
            fn = f"threebody_orbit_gap_{r['rank']:02d}.png"
            f.write(f"### Gap #{r['rank']}: {r['left_id']} <-> {r['right_id']}\n")
            f.write(f"![Gap {r['rank']}]({fn})\n\n")

    print(f"\nReport saved: {report_path}")


if __name__ == "__main__":
    control_results, gap_results = run_verification()
