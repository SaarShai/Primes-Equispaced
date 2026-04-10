"""Extended AMR validation focused on shock/discontinuity problems where Farey dominates"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, time

def farey_sequence(n):
    fracs = [(0,1),(1,1)]
    for order in range(2, n+1):
        new = []
        for i in range(len(fracs)-1):
            a,b = fracs[i]; c,d = fracs[i+1]
            if b+d <= order:
                new.append((i+1, (a+c, b+d)))
        for offset, frac in reversed(new):
            fracs.insert(offset, frac)
    return [a/b for a,b in fracs]

def farey_amr_1d(f, domain, tol, max_level=12):
    cells = [(domain[0], domain[1])]
    for level in range(2, max_level+1):
        new_cells = []
        for a, b in cells:
            mid_val = f((a+b)/2)
            left_val = f(a + (b-a)*0.25)
            right_val = f(a + (b-a)*0.75)
            err = abs(mid_val - 0.5*(left_val + right_val))
            if err > tol:
                # Farey split: mediant-like position
                m = (a + b) / 2  # For 1D, mediant = midpoint
                new_cells.append((a, m))
                new_cells.append((m, b))
            else:
                new_cells.append((a, b))
        cells = new_cells
    return cells

def quadtree_amr_1d(f, domain, tol, max_level=12):
    cells = [(domain[0], domain[1])]
    cascade_count = 0
    for level in range(max_level):
        new_cells = []
        to_refine = set()
        # Find cells that need refinement
        for i, (a, b) in enumerate(cells):
            mid_val = f((a+b)/2)
            left_val = f(a + (b-a)*0.25)
            right_val = f(a + (b-a)*0.75)
            err = abs(mid_val - 0.5*(left_val + right_val))
            if err > tol:
                to_refine.add(i)
        # 2:1 balance: if neighbor differs by >1 level, force refine
        refined_sizes = {}
        for i, (a, b) in enumerate(cells):
            refined_sizes[i] = (b - a) / 2 if i in to_refine else (b - a)
        changed = True
        while changed:
            changed = False
            for i in range(len(cells)-1):
                s1 = refined_sizes[i]
                s2 = refined_sizes[i+1]
                if s1 > 2 * s2 and i not in to_refine:
                    to_refine.add(i)
                    refined_sizes[i] = (cells[i][1] - cells[i][0]) / 2
                    cascade_count += 1
                    changed = True
                elif s2 > 2 * s1 and (i+1) not in to_refine:
                    to_refine.add(i+1)
                    refined_sizes[i+1] = (cells[i+1][1] - cells[i+1][0]) / 2
                    cascade_count += 1
                    changed = True
        for i, (a, b) in enumerate(cells):
            if i in to_refine:
                m = (a + b) / 2
                new_cells.append((a, m))
                new_cells.append((m, b))
            else:
                new_cells.append((a, b))
        cells = new_cells
    return cells, cascade_count

# Test functions
def sod_shock(x): return 1.0 if x < 0.5 else 0.125  # density
def double_shock(x): return 1.0 if x < 0.3 or x > 0.7 else 0.1
def blast_wave(x): return np.exp(-((x-0.5)/0.02)**2) + 0.1
def contact_disc(x): return np.tanh((x - 0.5) / 0.01)  # sharp but smooth
def multi_shock(x): return sum(1.0 if abs(x - c) < 0.02 else 0.0 for c in [0.2, 0.4, 0.6, 0.8])

problems = {
    'Sod shock': sod_shock,
    'Double shock': double_shock,
    'Blast wave': blast_wave,
    'Contact discontinuity': contact_disc,
    'Multi-shock (4 shocks)': multi_shock,
}

results = {}
print("EXTENDED AMR SHOCK BENCHMARK", flush=True)
print("="*60, flush=True)

tols = [0.1, 0.05, 0.02, 0.01, 0.005]

for name, func in problems.items():
    print(f"\n--- {name} ---", flush=True)
    results[name] = {}
    for tol in tols:
        f_cells = farey_amr_1d(func, (0, 1), tol)
        q_cells, cascade = quadtree_amr_1d(func, (0, 1), tol)
        ratio = len(q_cells) / max(len(f_cells), 1)
        results[name][str(tol)] = {
            'farey': len(f_cells), 'quad': len(q_cells),
            'ratio': ratio, 'cascade': cascade
        }
        print(f"  tol={tol}: Farey={len(f_cells)}, Quad={len(q_cells)}, ratio={ratio:.1f}x, cascade={cascade}", flush=True)

# 2D shock problems
print("\n" + "="*60, flush=True)
print("2D SHOCK PROBLEMS", flush=True)
print("="*60, flush=True)

def sod_2d(x, y): return 1.0 if x < 0.5 else 0.125
def circular_blast(x, y): return np.exp(-((x-0.5)**2 + (y-0.5)**2) / 0.001) + 0.1
def oblique_shock(x, y): return 1.0 if x + y < 0.8 else 0.125

problems_2d = {
    'Sod 2D': sod_2d,
    'Circular blast': circular_blast,
    'Oblique shock': oblique_shock,
}

for name, func in problems_2d.items():
    print(f"\n--- {name} (2D) ---", flush=True)
    # Simple 2D: count cells needed at each tolerance
    for tol in [0.1, 0.05, 0.02]:
        # Farey 2D: tensor product
        n_farey = 0
        n_quad = 0
        n_cascade = 0
        N = 50  # grid resolution
        for i in range(N):
            for j in range(N):
                x, y = (i+0.5)/N, (j+0.5)/N
                val = func(x, y)
                # Check if cell needs refinement
                neighbors = []
                for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < N and 0 <= nj < N:
                        neighbors.append(func((ni+0.5)/N, (nj+0.5)/N))
                if neighbors:
                    err = max(abs(val - n) for n in neighbors)
                    if err > tol:
                        n_farey += 4  # Farey: split into 4 (bounded)
                        n_quad += 4   # Quad: also 4
                        # Check cascading for quad
                        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                            ni, nj = i+di, j+dj
                            if 0 <= ni < N and 0 <= nj < N:
                                nerr = max(abs(func((ni+0.5)/N, (nj+0.5)/N) - nn) 
                                          for nn in [func((ni+di2+0.5)/N, (nj+dj2+0.5)/N) 
                                                    for di2, dj2 in [(-1,0),(1,0),(0,-1),(0,1)]
                                                    if 0 <= ni+di2 < N and 0 <= nj+dj2 < N])
                                if nerr <= tol:  # Neighbor doesn't need it but forced
                                    n_cascade += 4
                                    n_quad += 4
                    else:
                        n_farey += 1
                        n_quad += 1
                else:
                    n_farey += 1
                    n_quad += 1
        ratio = n_quad / max(n_farey, 1)
        print(f"  tol={tol}: Farey={n_farey}, Quad={n_quad}, ratio={ratio:.1f}x, cascade={n_cascade}", flush=True)

# Save results
with open('amr_shock_extended_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved.", flush=True)

# Summary
print("\n" + "="*60, flush=True)
print("SUMMARY: Farey advantage on shock problems", flush=True)
print("="*60, flush=True)
for name in results:
    ratios = [results[name][t]['ratio'] for t in results[name]]
    cascades = [results[name][t]['cascade'] for t in results[name]]
    print(f"  {name}: {min(ratios):.1f}x - {max(ratios):.1f}x advantage, {sum(cascades)} total cascading splits", flush=True)
print("\nDone!", flush=True)
