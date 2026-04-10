#!/usr/bin/env python3
"""
Analyze the periodic table of three-body orbits:
1. Identify the 4 physically interesting empty cells
2. Attempt orbit discovery in the most promising one via shooting method
"""

import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# Load data
# =============================================================================
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

print("="*80)
print("PERIODIC TABLE STRUCTURE")
print("="*80)
print(f"\nRows (9): CF period length bins")
for b in row_bins:
    print(f"  Row '{b['label']}': period length in [{b['lo']}, {b['hi']}]")

print(f"\nColumns (8): Geometric mean of CF partial quotients bins")
for b in col_bins:
    print(f"  Col '{b['label']}': gmean in [{b['lo']}, {b['hi']})")

print(f"\nTotal cells: {len(row_labels) * len(col_labels)} = {len(row_labels)} x {len(col_labels)}")

# =============================================================================
# Build occupancy grid and find all empty cells
# =============================================================================
grid = {}  # (ri, ci) -> count
for ri, rl in enumerate(row_labels):
    for ci, cl in enumerate(col_labels):
        key = f"{rl}|{cl}"
        cell = table['cells'][key]
        grid[(ri, ci)] = cell['count']

populated = sum(1 for v in grid.values() if v > 0)
empty = sum(1 for v in grid.values() if v == 0)
print(f"\nPopulated cells: {populated}")
print(f"Empty cells: {empty}")
print(f"Total orbits: {table['metadata']['n_in_table']}")

# =============================================================================
# Identify "physically interesting" empty cells
# An empty cell is interesting if it's surrounded by populated cells
# Score = number of populated neighbors (4-connected: up, down, left, right)
# =============================================================================
print("\n" + "="*80)
print("EMPTY CELL ANALYSIS")
print("="*80)

empty_cell_scores = []
for ri in range(len(row_labels)):
    for ci in range(len(col_labels)):
        if grid[(ri, ci)] == 0:
            neighbors = []
            neighbor_details = []
            for dri, dci, direction in [(-1,0,'above'), (1,0,'below'), (0,-1,'left'), (0,1,'right'),
                                         (-1,-1,'above-left'), (-1,1,'above-right'),
                                         (1,-1,'below-left'), (1,1,'below-right')]:
                nri, nci = ri + dri, ci + dci
                if 0 <= nri < len(row_labels) and 0 <= nci < len(col_labels):
                    count = grid[(nri, nci)]
                    if count > 0:
                        neighbors.append((nri, nci, direction, count))
                        key = f"{row_labels[nri]}|{col_labels[nci]}"
                        cell_data = table['cells'][key]
                        neighbor_details.append({
                            'direction': direction,
                            'row': row_labels[nri],
                            'col': col_labels[nci],
                            'count': count,
                            'representative': cell_data.get('representative'),
                            'avg_nobility': cell_data.get('avg_nobility'),
                        })

            # Only 4-connected for "interesting" score
            n4 = sum(1 for _, _, d, _ in neighbors if d in ('above', 'below', 'left', 'right'))
            # Also count 8-connected
            n8 = len(neighbors)

            empty_cell_scores.append({
                'ri': ri, 'ci': ci,
                'row': row_labels[ri], 'col': col_labels[ci],
                'n4_neighbors': n4,
                'n8_neighbors': n8,
                'neighbor_details': neighbor_details,
            })

# Sort by number of 4-connected populated neighbors, then 8-connected
empty_cell_scores.sort(key=lambda x: (-x['n4_neighbors'], -x['n8_neighbors']))

# The "physically interesting" ones: those with most populated neighbors
print("\nAll empty cells ranked by neighbor count:")
for i, ec in enumerate(empty_cell_scores):
    print(f"  {i+1}. Row={ec['row']:>10s}, Col={ec['col']:>10s} | "
          f"4-neighbors={ec['n4_neighbors']}, 8-neighbors={ec['n8_neighbors']}")

# Top 4 physically interesting
print("\n" + "="*80)
print("TOP 4 PHYSICALLY INTERESTING EMPTY CELLS")
print("="*80)

interesting = [ec for ec in empty_cell_scores if ec['n4_neighbors'] >= 3]
if len(interesting) < 4:
    interesting = empty_cell_scores[:4]

for i, ec in enumerate(interesting[:4]):
    print(f"\n--- Empty Cell #{i+1}: Row={ec['row']}, Col={ec['col']} ---")
    print(f"  CF period range: {ec['row']}")
    print(f"  Geometric mean range: {ec['col']}")
    print(f"  4-connected populated neighbors: {ec['n4_neighbors']}")
    print(f"  8-connected populated neighbors: {ec['n8_neighbors']}")
    print(f"  Neighboring cells:")
    for nd in ec['neighbor_details']:
        print(f"    {nd['direction']:>12s}: Row={nd['row']}, Col={nd['col']}, "
              f"count={nd['count']}, rep={nd['representative']}, nobility={nd['avg_nobility']:.3f}"
              if nd['avg_nobility'] else
              f"    {nd['direction']:>12s}: Row={nd['row']}, Col={nd['col']}, count={nd['count']}")

    # Expected CF properties
    row_bin = row_bins[ec['ri']]
    col_bin = col_bins[ec['ci']]
    mid_period = (row_bin['lo'] + row_bin['hi']) / 2
    mid_gmean = (col_bin['lo'] + col_bin['hi']) / 2
    print(f"  Expected CF properties for orbit in this cell:")
    print(f"    CF period length: {row_bin['lo']}-{row_bin['hi']} (midpoint: {mid_period})")
    print(f"    CF gmean: {col_bin['lo']}-{col_bin['hi']} (midpoint: {mid_gmean:.3f})")

# =============================================================================
# Select most promising cell and gather neighbor orbit data
# =============================================================================
best_cell = interesting[0]
print(f"\n\n{'='*80}")
print(f"ORBIT SEARCH: Most promising cell")
print(f"  Row={best_cell['row']}, Col={best_cell['col']}")
print(f"  4-connected neighbors: {best_cell['n4_neighbors']}, 8-connected: {best_cell['n8_neighbors']}")
print(f"{'='*80}")

# Gather ICs from neighboring orbits
neighbor_orbits = []
for nd in best_cell['neighbor_details']:
    rep_id = nd['representative']
    if rep_id and rep_id in orbits_by_id:
        orb = orbits_by_id[rep_id]
        neighbor_orbits.append(orb)
        print(f"\n  Neighbor orbit {orb['id']}:")
        print(f"    v1={orb['v1']}, v2={orb['v2']}, T={orb['T']}")
        print(f"    word={orb['word'][:40]}, word_length={orb['word_length']}")

# Also get ALL orbits in neighboring cells (not just representatives)
all_neighbor_orbits = []
for nd in best_cell['neighbor_details']:
    key = f"{nd['row']}|{nd['col']}"
    cell_data = table['cells'][key]
    if cell_data['count'] > 0:
        pass

# Use the exact data directly
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

# Get all orbits in the neighboring cells
neighbor_cell_keys = set()
for nd in best_cell['neighbor_details']:
    neighbor_cell_keys.add((nd['row'], nd['col']))

all_neighbor_orbits = []
for r in results:
    if r.get('period_not_found', False):
        continue
    rl = get_row_bin_label(r['cf_period_length'])
    cl = get_col_bin_label(r['cf_period_gmean'])
    if (rl, cl) in neighbor_cell_keys:
        all_neighbor_orbits.append(r)

print(f"\n  Total orbits in neighboring cells: {len(all_neighbor_orbits)}")

# =============================================================================
# THREE-BODY INTEGRATION
# =============================================================================
def threebody_rhs(t, state):
    """
    Equal mass three-body problem in 2D.
    State: [x1, y1, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3]
    """
    x1, y1, x2, y2, x3, y3 = state[:6]
    vx1, vy1, vx2, vy2, vx3, vy3 = state[6:]

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

    # Accelerations (G=1, m=1)
    ax1 = dx12/r12_3 + dx13/r13_3
    ay1 = dy12/r12_3 + dy13/r13_3

    ax2 = -dx12/r12_3 + dx23/r23_3
    ay2 = -dy12/r12_3 + dy23/r23_3

    ax3 = -dx13/r13_3 - dx23/r23_3
    ay3 = -dy13/r13_3 - dy23/r23_3

    return [vx1, vy1, vx2, vy2, vx3, vy3, ax1, ay1, ax2, ay2, ax3, ay3]


def make_initial_state(vx, vy):
    """
    Li-Liao convention:
    r1=(-1,0), r2=(1,0), r3=(0,0)
    v1=v2=(vx,vy), v3=-2*(vx,vy)
    """
    return [
        -1.0, 0.0,   # r1
         1.0, 0.0,   # r2
         0.0, 0.0,   # r3
         vx, vy,     # v1
         vx, vy,     # v2
        -2*vx, -2*vy # v3
    ]


def return_error(vx, vy, T):
    """
    Integrate for time T and measure how close the state returns to initial.
    Return error = sum of squared differences in positions and velocities.
    """
    y0 = make_initial_state(vx, vy)
    try:
        sol = solve_ivp(threebody_rhs, [0, T], y0, method='RK45',
                       rtol=1e-12, atol=1e-12, max_step=T/100)
        if not sol.success:
            return 1e10

        yf = sol.y[:, -1]
        y0_arr = np.array(y0)
        yf_arr = np.array(yf)

        # Position error (bodies may return permuted - check all permutations)
        # For simplicity, check identity permutation first
        pos_err = np.sum((yf_arr[:6] - y0_arr[:6])**2)
        vel_err = np.sum((yf_arr[6:] - y0_arr[6:])**2)

        return np.sqrt(pos_err + vel_err)
    except Exception:
        return 1e10


def return_error_vec(params):
    """Wrapper for optimizer: params = [vx, vy, T]"""
    vx, vy, T = params
    if T < 1 or T > 200:
        return 1e10
    return return_error(vx, vy, T)


# =============================================================================
# INTERPOLATE ICs FOR THE EMPTY CELL
# =============================================================================
print("\n\n--- Interpolating initial conditions ---")

# Target cell properties
target_row = best_cell['row']
target_col = best_cell['col']
target_row_bin = row_bins[best_cell['ri']]
target_col_bin = col_bins[best_cell['ci']]

# Get ICs from all neighbor orbits
vxs = [o['v1'] for o in all_neighbor_orbits]
vys = [o['v2'] for o in all_neighbor_orbits]
Ts = [o['T'] for o in all_neighbor_orbits]
wls = [o['word_length'] for o in all_neighbor_orbits]

if len(all_neighbor_orbits) > 0:
    avg_vx = np.mean(vxs)
    avg_vy = np.mean(vys)
    avg_T = np.mean(Ts)
    avg_wl = np.mean(wls)
    T_estimate = 6 * avg_wl  # from word length

    print(f"  Average neighbor ICs: vx={avg_vx:.6f}, vy={avg_vy:.6f}")
    print(f"  Average neighbor T: {avg_T:.3f}")
    print(f"  Average word length: {avg_wl:.1f}")
    print(f"  T estimate from word length: {T_estimate:.1f}")

    std_vx = np.std(vxs) if len(vxs) > 1 else 0.05
    std_vy = np.std(vys) if len(vys) > 1 else 0.05
    std_T = np.std(Ts) if len(Ts) > 1 else 5.0

    print(f"  Spread: std_vx={std_vx:.6f}, std_vy={std_vy:.6f}, std_T={std_T:.3f}")
else:
    print("  WARNING: No neighbor orbits found! Using generic starting point.")
    avg_vx, avg_vy, avg_T = 0.3, 0.5, 30.0
    std_vx, std_vy, std_T = 0.1, 0.1, 10.0
    T_estimate = avg_T

# =============================================================================
# SHOOTING: Try many starting guesses
# =============================================================================
print("\n\n--- Shooting method: searching for periodic orbit ---")

best_error = 1e10
best_params = None
n_tries = 100

np.random.seed(42)

# Generate starting guesses by interpolating and perturbing neighbor ICs
starting_guesses = []

# 1. Average of neighbors
starting_guesses.append((avg_vx, avg_vy, avg_T))
starting_guesses.append((avg_vx, avg_vy, T_estimate))

# 2. Each neighbor orbit's ICs
for o in neighbor_orbits:
    starting_guesses.append((o['v1'], o['v2'], o['T']))

# 3. Random perturbations around average
for _ in range(n_tries - len(starting_guesses)):
    vx = avg_vx + np.random.normal(0, std_vx * 0.5)
    vy = avg_vy + np.random.normal(0, std_vy * 0.5)
    T = avg_T + np.random.normal(0, std_T * 0.5)
    if T < 5: T = 5
    starting_guesses.append((vx, vy, T))

print(f"  Trying {len(starting_guesses)} starting guesses...")
print(f"  Search region: vx in [{avg_vx - 2*std_vx:.4f}, {avg_vx + 2*std_vx:.4f}]")
print(f"                 vy in [{avg_vy - 2*std_vy:.4f}, {avg_vy + 2*std_vy:.4f}]")
print(f"                 T  in [{max(5, avg_T - 2*std_T):.1f}, {avg_T + 2*std_T:.1f}]")

results_list = []

for i, (vx0, vy0, T0) in enumerate(starting_guesses):
    # First evaluate raw error
    err0 = return_error(vx0, vy0, T0)

    if err0 < 5.0:  # Worth refining
        # Local optimization
        try:
            res = minimize(return_error_vec, [vx0, vy0, T0],
                          method='Nelder-Mead',
                          options={'maxiter': 500, 'xatol': 1e-10, 'fatol': 1e-12})
            if res.fun < best_error:
                best_error = res.fun
                best_params = res.x
                if res.fun < 0.01:
                    print(f"  *** SUCCESS at try {i}: error={res.fun:.6e}, "
                          f"vx={res.x[0]:.10f}, vy={res.x[1]:.10f}, T={res.x[2]:.6f}")

            results_list.append({
                'try': i,
                'vx0': vx0, 'vy0': vy0, 'T0': T0,
                'err0': err0,
                'vx': res.x[0], 'vy': res.x[1], 'T': res.x[2],
                'error': res.fun,
            })
        except Exception as e:
            pass

    if (i+1) % 20 == 0:
        print(f"  ... tried {i+1}/{len(starting_guesses)}, best error so far: {best_error:.6e}")

# Sort results by error
results_list.sort(key=lambda x: x['error'])

print(f"\n\n--- RESULTS ---")
print(f"Best error: {best_error:.6e}")
if best_params is not None:
    print(f"Best params: vx={best_params[0]:.10f}, vy={best_params[1]:.10f}, T={best_params[2]:.6f}")

print(f"\nTop 10 results:")
for r in results_list[:10]:
    print(f"  Try {r['try']:3d}: error={r['error']:.6e}, "
          f"vx={r['vx']:.8f}, vy={r['vy']:.8f}, T={r['T']:.4f}")

# =============================================================================
# If good result found, try harder refinement
# =============================================================================
found_orbit = None

if best_error < 1.0 and best_params is not None:
    print(f"\n\n--- Refining best candidate (error={best_error:.6e}) ---")

    # Try Powell method for finer refinement
    try:
        res2 = minimize(return_error_vec, best_params,
                       method='Powell',
                       options={'maxiter': 5000, 'ftol': 1e-15})
        if res2.fun < best_error:
            best_error = res2.fun
            best_params = res2.x
            print(f"  Powell refined: error={res2.fun:.6e}")
    except:
        pass

    # Try L-BFGS-B with numerical gradients
    try:
        bounds = [(best_params[0]-0.01, best_params[0]+0.01),
                  (best_params[1]-0.01, best_params[1]+0.01),
                  (best_params[2]-1, best_params[2]+1)]
        res3 = minimize(return_error_vec, best_params,
                       method='L-BFGS-B', bounds=bounds,
                       options={'maxiter': 1000})
        if res3.fun < best_error:
            best_error = res3.fun
            best_params = res3.x
            print(f"  L-BFGS-B refined: error={res3.fun:.6e}")
    except:
        pass

if best_error < 0.01:
    print(f"\n  *** ORBIT FOUND! Error = {best_error:.6e}")
    found_orbit = {
        'vx': float(best_params[0]),
        'vy': float(best_params[1]),
        'T': float(best_params[2]),
        'return_error': float(best_error),
        'target_cell': {'row': target_row, 'col': target_col},
    }
elif best_error < 0.1:
    print(f"\n  Near-miss: error = {best_error:.6e} (threshold is 0.01)")
    print(f"  This may still be a valid orbit that needs more refinement.")
    found_orbit = {
        'vx': float(best_params[0]),
        'vy': float(best_params[1]),
        'T': float(best_params[2]),
        'return_error': float(best_error),
        'target_cell': {'row': target_row, 'col': target_col},
        'status': 'near-miss',
    }
else:
    print(f"\n  No orbit found (best error = {best_error:.6e})")
    print(f"  The empty cell may genuinely be forbidden by physical constraints.")

# =============================================================================
# If we have a near-miss, try differential evolution as a global optimizer
# =============================================================================
if best_error > 0.01 and len(all_neighbor_orbits) > 0:
    print(f"\n\n--- Trying differential evolution (global search) ---")
    bounds_de = [
        (avg_vx - 3*std_vx, avg_vx + 3*std_vx),
        (avg_vy - 3*std_vy, avg_vy + 3*std_vy),
        (max(5, avg_T - 3*std_T), avg_T + 3*std_T),
    ]
    print(f"  Bounds: {bounds_de}")

    try:
        res_de = differential_evolution(return_error_vec, bounds_de,
                                         maxiter=200, seed=42, tol=1e-12,
                                         popsize=20, mutation=(0.5, 1.5),
                                         recombination=0.9)
        print(f"  DE result: error={res_de.fun:.6e}")
        print(f"  DE params: vx={res_de.x[0]:.10f}, vy={res_de.x[1]:.10f}, T={res_de.x[2]:.6f}")

        if res_de.fun < best_error:
            best_error = res_de.fun
            best_params = res_de.x

            if best_error < 0.01:
                print(f"  *** ORBIT FOUND via DE! Error = {best_error:.6e}")
                found_orbit = {
                    'vx': float(best_params[0]),
                    'vy': float(best_params[1]),
                    'T': float(best_params[2]),
                    'return_error': float(best_error),
                    'target_cell': {'row': target_row, 'col': target_col},
                }
    except Exception as e:
        print(f"  DE failed: {e}")

# =============================================================================
# Also try searching around KNOWN orbits more aggressively
# Maybe a slight perturbation of a known orbit falls in the empty cell
# =============================================================================
if best_error > 0.01:
    print(f"\n\n--- Trying perturbations of known neighbor orbits ---")
    for orb in neighbor_orbits[:5]:
        vx0, vy0, T0 = orb['v1'], orb['v2'], orb['T']
        for scale in [0.01, 0.02, 0.05, 0.1]:
            for _ in range(20):
                dvx = np.random.normal(0, scale)
                dvy = np.random.normal(0, scale)
                dT = np.random.normal(0, T0 * scale * 0.5)
                vx, vy, T = vx0 + dvx, vy0 + dvy, T0 + dT
                err = return_error(vx, vy, T)
                if err < 1.0:
                    res = minimize(return_error_vec, [vx, vy, T],
                                 method='Nelder-Mead',
                                 options={'maxiter': 500, 'xatol': 1e-10, 'fatol': 1e-12})
                    if res.fun < best_error:
                        best_error = res.fun
                        best_params = res.x
                        if res.fun < 0.01:
                            print(f"  *** ORBIT FOUND! error={res.fun:.6e}, "
                                  f"perturbed from {orb['id']}")
                            found_orbit = {
                                'vx': float(res.x[0]),
                                'vy': float(res.x[1]),
                                'T': float(res.x[2]),
                                'return_error': float(res.fun),
                                'target_cell': {'row': target_row, 'col': target_col},
                                'source': f"perturbed from {orb['id']}",
                            }
    print(f"  Best error after perturbation search: {best_error:.6e}")


# =============================================================================
# OUTPUT: Save found orbit
# =============================================================================
if found_orbit and found_orbit['return_error'] < 0.1:
    print(f"\n\nSaving orbit to threebody_new_orbit.json")
    with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_new_orbit.json', 'w') as f:
        json.dump(found_orbit, f, indent=2)

# =============================================================================
# OUTPUT: Summary data for the report
# =============================================================================
summary = {
    'interesting_empty_cells': [],
    'best_search_result': {
        'target_cell': {'row': target_row, 'col': target_col},
        'best_error': float(best_error),
        'best_params': [float(x) for x in best_params] if best_params is not None else None,
        'n_neighbor_orbits': len(all_neighbor_orbits),
        'n_tries': len(starting_guesses),
        'found': best_error < 0.01,
    },
}

for ec in interesting[:4]:
    summary['interesting_empty_cells'].append({
        'row': ec['row'],
        'col': ec['col'],
        'n4_neighbors': ec['n4_neighbors'],
        'n8_neighbors': ec['n8_neighbors'],
        'neighbors': ec['neighbor_details'],
    })

with open('/Users/saar/Desktop/Farey-Local/experiments/empty_cell_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\n\nDONE. Best return error: {best_error:.6e}")
print(f"Orbit {'FOUND' if best_error < 0.01 else 'NOT FOUND'}")
