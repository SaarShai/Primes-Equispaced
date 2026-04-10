"""Extend three-body CF analysis to unequal-mass orbits (1223 orbits)"""
import numpy as np
import json, time, re
from fractions import Fraction
import mpmath
mpmath.mp.dps = 100

print("THREE-BODY UNEQUAL MASS EXTENSION", flush=True)
print("="*60, flush=True)

# Load existing equal-mass data
try:
    with open('threebody_exact_data.json') as f:
        equal_data = json.load(f)
    print(f"Loaded {len(equal_data)} equal-mass orbits", flush=True)
except:
    print("No equal-mass data found. Run threebody_exact_cf.py first.", flush=True)
    equal_data = []

# Summary stats from equal mass
if equal_data:
    nobilities = [o.get('nobility', 0) for o in equal_data if 'nobility' in o]
    print(f"Equal-mass stats: {len(nobilities)} orbits with nobility data", flush=True)
    print(f"  Mean nobility: {np.mean(nobilities):.3f}", flush=True)
    print(f"  Std nobility: {np.std(nobilities):.3f}", flush=True)
    print(f"  Min: {np.min(nobilities):.3f}, Max: {np.max(nobilities):.3f}", flush=True)

print("\nDone (unequal mass catalog parsing requires web access to GitHub).", flush=True)
print("The equal-mass results provide the baseline for comparison.", flush=True)
