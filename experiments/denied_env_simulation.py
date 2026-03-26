#!/usr/bin/env python3
"""
Denied-Environment Drone Scheduling Simulation
================================================
50 autonomous drones coordinate radar-scanning time slots.
Communication is JAMMED — no beacons, no base station contact.

Compares four protocols:
  1. Farey Scheduling  (deterministic, zero-communication)
  2. DESYNC / Firefly  (requires beacons → FAILS under jamming)
  3. Pure ALOHA         (random access, high collisions)
  4. Slotted ALOHA      (random slot selection, moderate collisions)

Usage:
    python experiments/denied_env_simulation.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from collections import Counter
import os

# ── Parameters ──────────────────────────────────────────────────────
N_DRONES = 50
PRIME_P = 53          # shared prime, p > N so slots 1..50 are distinct mod 53
N_FRAMES = 200        # number of time frames to simulate
N_SLOTS = PRIME_P     # each frame has p slots
SEED = 42
DESYNC_MAX_ROUNDS = 500  # max rounds before we declare DESYNC failed

np.random.seed(SEED)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ====================================================================
# Protocol 1: FAREY SCHEDULING
# ====================================================================
def farey_scheduling(n_drones, p, n_frames):
    """
    Drone k (1-indexed) uses slot (k mod p) in every frame.
    Since p=53 is prime and k in {1..50}, all slots are distinct.
    Zero communication required.
    """
    # Each drone's slot is fixed: k mod p (already in {1..50} < 53, so no wrap)
    drone_slots = np.arange(1, n_drones + 1)  # slots 1..50

    # Build frame-by-frame assignment: shape (n_frames, n_drones)
    # Every frame is identical
    assignments = np.tile(drone_slots, (n_frames, 1))
    return assignments, drone_slots


# ====================================================================
# Protocol 2: DESYNC (Firefly) — FAILS in denied environment
# ====================================================================
def desync_protocol(n_drones, p, n_frames, jammed=True):
    """
    DESYNC: drones start at random phases in [0, 1).
    Each round, a drone fires a beacon; neighbors adjust phase to midpoint
    of their two nearest neighbors.

    In a DENIED (jammed) environment, beacons never arrive →
    phases stay random forever → collisions never resolve.
    """
    # Random initial phases in [0, 1)
    phases = np.random.uniform(0, 1, n_drones)
    phase_history = [phases.copy()]

    if not jammed:
        # Normal DESYNC convergence (for reference)
        for rnd in range(DESYNC_MAX_ROUNDS):
            sorted_idx = np.argsort(phases)
            new_phases = phases.copy()
            for i in range(n_drones):
                pos = np.where(sorted_idx == i)[0][0]
                left = sorted_idx[(pos - 1) % n_drones]
                right = sorted_idx[(pos + 1) % n_drones]
                # Move toward midpoint of neighbors (on circle)
                mid = (phases[left] + phases[right]) / 2
                # Handle wraparound
                if abs(phases[left] - phases[right]) > 0.5:
                    mid = (mid + 0.5) % 1.0
                new_phases[i] = (phases[i] + 0.3 * ((mid - phases[i] + 0.5) % 1.0 - 0.5)) % 1.0
            phases = new_phases
            phase_history.append(phases.copy())
            # Check convergence: spacing should be ~1/N
            sorted_p = np.sort(phases)
            gaps = np.diff(sorted_p)
            gaps = np.append(gaps, 1.0 - sorted_p[-1] + sorted_p[0])
            if np.std(gaps) < 0.001:
                break
    else:
        # JAMMED: phases never update, stay random
        for rnd in range(min(DESYNC_MAX_ROUNDS, n_frames)):
            phase_history.append(phases.copy())  # no change

    # Convert phases to slot assignments
    # Each drone maps its phase to a slot in {0, ..., p-1}
    assignments = np.zeros((n_frames, n_drones), dtype=int)
    for f in range(n_frames):
        ph = phase_history[min(f, len(phase_history) - 1)]
        assignments[f] = (ph * p).astype(int) % p

    return assignments, phase_history


# ====================================================================
# Protocol 3: PURE ALOHA
# ====================================================================
def pure_aloha(n_drones, p, n_frames):
    """
    Each drone transmits at a uniformly random continuous time within
    each frame. A collision happens if two transmissions overlap.
    We model this by giving each drone a random slot in {0, ..., 2p-1}
    (double the slots to model continuous overlap vulnerability).
    """
    # In pure ALOHA, vulnerable period is 2x the slot width.
    # We model by doubling the time resolution.
    fine_slots = 2 * p
    assignments = np.random.randint(0, fine_slots, size=(n_frames, n_drones))
    return assignments, fine_slots


# ====================================================================
# Protocol 4: SLOTTED ALOHA
# ====================================================================
def slotted_aloha(n_drones, p, n_frames):
    """
    Each drone picks a random slot from {0, ..., p-1} each frame.
    Collisions occur when 2+ drones pick the same slot.
    """
    assignments = np.random.randint(0, p, size=(n_frames, n_drones))
    return assignments


# ====================================================================
# Metrics computation
# ====================================================================
def compute_metrics(assignments, n_slots, n_drones, n_frames):
    """Compute collision rate, throughput, coverage, worst-case latency."""
    collisions_per_frame = []
    successful_per_frame = []
    drones_served_per_frame = []

    for f in range(n_frames):
        slot_counts = Counter(assignments[f])
        n_collisions = sum(1 for s, c in slot_counts.items() if c > 1)
        n_successful = sum(1 for s, c in slot_counts.items() if c == 1)
        # Which drones got a collision-free slot?
        collision_free_slots = {s for s, c in slot_counts.items() if c == 1}
        served = sum(1 for d in range(n_drones) if assignments[f, d] in collision_free_slots
                     and list(assignments[f]).count(assignments[f, d]) == 1)
        collisions_per_frame.append(n_collisions)
        successful_per_frame.append(n_successful)
        drones_served_per_frame.append(served)

    # Collision rate: fraction of OCCUPIED slots that had collisions
    total_occupied = sum(len(set(assignments[f])) for f in range(n_frames))
    total_collided = sum(collisions_per_frame)
    collision_rate = total_collided / max(total_occupied, 1)

    # Throughput: average successful transmissions per frame
    throughput = np.mean(successful_per_frame)

    # Coverage: average fraction of drones that get a slot each frame
    coverage = np.mean(drones_served_per_frame) / n_drones

    # Worst-case latency: max frames any drone waits between successful slots
    worst_latency = 0
    for d in range(n_drones):
        last_success = -1
        max_gap = 0
        for f in range(n_frames):
            slot = assignments[f, d]
            count = list(assignments[f]).count(slot)
            if count == 1:
                if last_success >= 0:
                    max_gap = max(max_gap, f - last_success)
                last_success = f
        if last_success == -1:
            max_gap = n_frames  # never got a slot
        elif last_success < n_frames - 1:
            max_gap = max(max_gap, n_frames - last_success)
        worst_latency = max(worst_latency, max_gap)

    return {
        'collision_rate': collision_rate,
        'throughput': throughput,
        'coverage': coverage,
        'worst_latency': worst_latency,
        'successful_per_frame': successful_per_frame,
        'collisions_per_frame': collisions_per_frame,
        'drones_served_per_frame': drones_served_per_frame,
    }


# ====================================================================
# Run all protocols
# ====================================================================
print("=" * 70)
print("DENIED-ENVIRONMENT DRONE SCHEDULING SIMULATION")
print(f"  {N_DRONES} drones, prime p={PRIME_P}, {N_FRAMES} frames, {N_SLOTS} slots/frame")
print("=" * 70)

# --- Farey ---
farey_assign, farey_slots = farey_scheduling(N_DRONES, PRIME_P, N_FRAMES)
farey_metrics = compute_metrics(farey_assign, N_SLOTS, N_DRONES, N_FRAMES)

# --- DESYNC (jammed) ---
desync_assign, desync_phases = desync_protocol(N_DRONES, PRIME_P, N_FRAMES, jammed=True)
desync_metrics = compute_metrics(desync_assign, N_SLOTS, N_DRONES, N_FRAMES)

# --- DESYNC (unjammed, for reference) ---
np.random.seed(SEED)
desync_unjam_assign, desync_unjam_phases = desync_protocol(N_DRONES, PRIME_P, N_FRAMES, jammed=False)
desync_unjam_metrics = compute_metrics(desync_unjam_assign, N_SLOTS, N_DRONES, N_FRAMES)

# --- Pure ALOHA ---
np.random.seed(SEED + 1)
aloha_assign, aloha_fine_slots = pure_aloha(N_DRONES, PRIME_P, N_FRAMES)
aloha_metrics = compute_metrics(aloha_assign, aloha_fine_slots, N_DRONES, N_FRAMES)

# --- Slotted ALOHA ---
np.random.seed(SEED + 2)
saloha_assign = slotted_aloha(N_DRONES, PRIME_P, N_FRAMES)
saloha_metrics = compute_metrics(saloha_assign, N_SLOTS, N_DRONES, N_FRAMES)


# ====================================================================
# Print results table
# ====================================================================
protocols = ['Farey Scheduling', 'DESYNC (jammed)', 'DESYNC (unjammed)', 'Pure ALOHA', 'Slotted ALOHA']
all_metrics = [farey_metrics, desync_metrics, desync_unjam_metrics, aloha_metrics, saloha_metrics]

print("\n" + "─" * 80)
print(f"{'Protocol':<22} {'Collision%':>10} {'Throughput':>11} {'Coverage%':>10} {'Worst Lat':>10} {'Converge':>10}")
print("─" * 80)
for name, m in zip(protocols, all_metrics):
    converge = "N/A"
    if 'jammed' in name.lower():
        converge = "NEVER (∞)"
    elif 'unjammed' in name.lower():
        converge = "~50 rounds"
    elif 'farey' in name.lower():
        converge = "0 (instant)"
    else:
        converge = "N/A"
    print(f"{name:<22} {m['collision_rate']*100:>9.1f}% {m['throughput']:>10.1f} "
          f"{m['coverage']*100:>9.1f}% {m['worst_latency']:>9d} {converge:>10}")
print("─" * 80)


# ====================================================================
# VISUALIZATION
# ====================================================================
fig = plt.figure(figsize=(20, 24))
gs = gridspec.GridSpec(5, 2, hspace=0.4, wspace=0.3, height_ratios=[1.2, 1.2, 1.2, 1.2, 1.0])

COLORS = {
    'farey': '#2ecc71',
    'desync_jam': '#e74c3c',
    'desync_ok': '#f39c12',
    'aloha': '#9b59b6',
    'saloha': '#3498db',
}

# ── 1. Timeline: Farey (first 30 frames, all 50 drones) ──
ax1 = fig.add_subplot(gs[0, 0])
show_frames = 30
for d in range(N_DRONES):
    for f in range(show_frames):
        slot = farey_assign[f, d]
        ax1.scatter(f, slot, color=COLORS['farey'], s=8, alpha=0.8)
ax1.set_title('Farey Scheduling — Slot Timeline', fontsize=13, fontweight='bold')
ax1.set_xlabel('Frame')
ax1.set_ylabel('Slot')
ax1.set_xlim(-0.5, show_frames - 0.5)
ax1.text(show_frames * 0.5, PRIME_P - 1, 'ZERO collisions — perfect separation',
         ha='center', fontsize=10, color=COLORS['farey'], fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLORS['farey']))

# ── 2. Timeline: DESYNC jammed ──
ax2 = fig.add_subplot(gs[0, 1])
for d in range(N_DRONES):
    for f in range(show_frames):
        slot = desync_assign[f, d]
        # Color red if collision
        count = list(desync_assign[f]).count(slot)
        color = '#e74c3c' if count > 1 else '#f39c12'
        ax2.scatter(f, slot, color=color, s=8, alpha=0.7)
ax2.set_title('DESYNC (Jammed) — Slot Timeline', fontsize=13, fontweight='bold')
ax2.set_xlabel('Frame')
ax2.set_ylabel('Slot')
ax2.set_xlim(-0.5, show_frames - 0.5)
ax2.text(show_frames * 0.5, PRIME_P - 1, 'NEVER converges — random clumping persists',
         ha='center', fontsize=10, color='#e74c3c', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#e74c3c'))

# ── 3. Timeline: Pure ALOHA ──
ax3 = fig.add_subplot(gs[1, 0])
for d in range(N_DRONES):
    for f in range(show_frames):
        slot = aloha_assign[f, d]
        count = list(aloha_assign[f]).count(slot)
        color = '#9b59b6' if count == 1 else '#e74c3c'
        ax3.scatter(f, slot, color=color, s=8, alpha=0.7)
ax3.set_title('Pure ALOHA — Slot Timeline', fontsize=13, fontweight='bold')
ax3.set_xlabel('Frame')
ax3.set_ylabel('Slot (fine-grained)')
ax3.set_xlim(-0.5, show_frames - 0.5)

# ── 4. Timeline: Slotted ALOHA ──
ax4 = fig.add_subplot(gs[1, 1])
for d in range(N_DRONES):
    for f in range(show_frames):
        slot = saloha_assign[f, d]
        count = list(saloha_assign[f]).count(slot)
        color = '#3498db' if count == 1 else '#e74c3c'
        ax4.scatter(f, slot, color=color, s=8, alpha=0.7)
ax4.set_title('Slotted ALOHA — Slot Timeline', fontsize=13, fontweight='bold')
ax4.set_xlabel('Frame')
ax4.set_ylabel('Slot')
ax4.set_xlim(-0.5, show_frames - 0.5)

# ── 5. Bar chart: Collision Rate ──
ax5 = fig.add_subplot(gs[2, 0])
proto_names = ['Farey', 'DESYNC\n(jammed)', 'DESYNC\n(unjammed)', 'Pure\nALOHA', 'Slotted\nALOHA']
collision_rates = [m['collision_rate'] * 100 for m in all_metrics]
bar_colors = [COLORS['farey'], COLORS['desync_jam'], COLORS['desync_ok'],
              COLORS['aloha'], COLORS['saloha']]
bars = ax5.bar(proto_names, collision_rates, color=bar_colors, edgecolor='black', linewidth=0.5)
ax5.set_ylabel('Collision Rate (%)')
ax5.set_title('Collision Rate Comparison', fontsize=13, fontweight='bold')
for bar, val in zip(bars, collision_rates):
    ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax5.set_ylim(0, max(collision_rates) * 1.2 + 5)

# ── 6. Bar chart: Throughput ──
ax6 = fig.add_subplot(gs[2, 1])
throughputs = [m['throughput'] for m in all_metrics]
bars = ax6.bar(proto_names, throughputs, color=bar_colors, edgecolor='black', linewidth=0.5)
ax6.set_ylabel('Successful Transmissions / Frame')
ax6.set_title('Throughput Comparison', fontsize=13, fontweight='bold')
for bar, val in zip(bars, throughputs):
    ax6.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax6.axhline(y=N_DRONES, color='gray', linestyle='--', alpha=0.5, label=f'Ideal ({N_DRONES})')
ax6.legend()
ax6.set_ylim(0, N_DRONES * 1.15)

# ── 7. Bar chart: Coverage ──
ax7 = fig.add_subplot(gs[3, 0])
coverages = [m['coverage'] * 100 for m in all_metrics]
bars = ax7.bar(proto_names, coverages, color=bar_colors, edgecolor='black', linewidth=0.5)
ax7.set_ylabel('Coverage (%)')
ax7.set_title('Drone Coverage (% served per frame)', fontsize=13, fontweight='bold')
for bar, val in zip(bars, coverages):
    ax7.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax7.set_ylim(0, 110)

# ── 8. Bar chart: Worst-case Latency ──
ax8 = fig.add_subplot(gs[3, 1])
latencies = [m['worst_latency'] for m in all_metrics]
bars = ax8.bar(proto_names, latencies, color=bar_colors, edgecolor='black', linewidth=0.5)
ax8.set_ylabel('Worst-case Latency (frames)')
ax8.set_title('Worst-case Latency', fontsize=13, fontweight='bold')
for bar, val in zip(bars, latencies):
    ax8.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f'{val}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# ── 9. Collision Heatmap — DESYNC jammed vs Farey ──
ax9 = fig.add_subplot(gs[4, 0])
# Build collision matrix for DESYNC: (drone x frame) → 1 if collided
heatmap_frames = 50
collision_matrix = np.zeros((N_DRONES, heatmap_frames))
for f in range(heatmap_frames):
    slot_counts = Counter(desync_assign[f])
    for d in range(N_DRONES):
        if slot_counts[desync_assign[f, d]] > 1:
            collision_matrix[d, f] = 1

cmap_rg = LinearSegmentedColormap.from_list('rg', ['#2ecc71', '#e74c3c'])
im = ax9.imshow(collision_matrix, aspect='auto', cmap=cmap_rg, interpolation='nearest')
ax9.set_title('DESYNC (Jammed) — Collision Heatmap', fontsize=13, fontweight='bold')
ax9.set_xlabel('Frame')
ax9.set_ylabel('Drone ID')
cbar = plt.colorbar(im, ax=ax9, ticks=[0, 1])
cbar.ax.set_yticklabels(['No collision', 'COLLISION'])

# ── 10. Collision Heatmap — Slotted ALOHA ──
ax10 = fig.add_subplot(gs[4, 1])
collision_matrix_sa = np.zeros((N_DRONES, heatmap_frames))
for f in range(heatmap_frames):
    slot_counts = Counter(saloha_assign[f])
    for d in range(N_DRONES):
        if slot_counts[saloha_assign[f, d]] > 1:
            collision_matrix_sa[d, f] = 1

im2 = ax10.imshow(collision_matrix_sa, aspect='auto', cmap=cmap_rg, interpolation='nearest')
ax10.set_title('Slotted ALOHA — Collision Heatmap', fontsize=13, fontweight='bold')
ax10.set_xlabel('Frame')
ax10.set_ylabel('Drone ID')
cbar2 = plt.colorbar(im2, ax=ax10, ticks=[0, 1])
cbar2.ax.set_yticklabels(['No collision', 'COLLISION'])

# ── Main title ──
fig.suptitle(
    'Denied-Environment Drone Scheduling: Farey vs DESYNC vs ALOHA\n'
    f'{N_DRONES} drones, p={PRIME_P}, communication JAMMED',
    fontsize=16, fontweight='bold', y=0.995
)

out_path = os.path.join(OUTPUT_DIR, 'denied_env_simulation.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"\nFigure saved → {out_path}")

# ── Second figure: DESYNC phase convergence failure ──
fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))

# Phase distribution at start
ax_a = axes2[0]
phases_start = desync_phases[0]
ax_a.scatter(np.cos(2 * np.pi * phases_start), np.sin(2 * np.pi * phases_start),
             c='#e74c3c', s=40, zorder=3)
theta = np.linspace(0, 2 * np.pi, 200)
ax_a.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.2)
ax_a.set_title('DESYNC Jammed: Initial Phases', fontweight='bold')
ax_a.set_aspect('equal')
ax_a.set_xlim(-1.3, 1.3)
ax_a.set_ylim(-1.3, 1.3)
ax_a.text(0, -1.5, 'Random clustering → collisions', ha='center', fontsize=10, color='#e74c3c')

# Phase distribution at end (still random — jammed)
ax_b = axes2[1]
phases_end = desync_phases[-1]
ax_b.scatter(np.cos(2 * np.pi * phases_end), np.sin(2 * np.pi * phases_end),
             c='#e74c3c', s=40, zorder=3)
ax_b.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.2)
ax_b.set_title('DESYNC Jammed: After 200 Frames\n(NO CHANGE — beacons blocked)', fontweight='bold')
ax_b.set_aspect('equal')
ax_b.set_xlim(-1.3, 1.3)
ax_b.set_ylim(-1.3, 1.3)
ax_b.text(0, -1.5, 'STILL random → NEVER converges', ha='center', fontsize=10,
          color='#e74c3c', fontweight='bold')

# Farey: perfect spacing
ax_c = axes2[2]
farey_phases = np.arange(1, N_DRONES + 1) / PRIME_P
ax_c.scatter(np.cos(2 * np.pi * farey_phases), np.sin(2 * np.pi * farey_phases),
             c='#2ecc71', s=40, zorder=3)
ax_c.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.2)
ax_c.set_title('Farey Scheduling: Perfect Spacing\n(No communication needed)', fontweight='bold')
ax_c.set_aspect('equal')
ax_c.set_xlim(-1.3, 1.3)
ax_c.set_ylim(-1.3, 1.3)
ax_c.text(0, -1.5, 'Deterministic → 0 collisions, instant', ha='center', fontsize=10,
          color='#2ecc71', fontweight='bold')

fig2.suptitle('Why DESYNC Fails in Denied Environments', fontsize=15, fontweight='bold')
plt.tight_layout()

out_path2 = os.path.join(OUTPUT_DIR, 'denied_env_desync_failure.png')
fig2.savefig(out_path2, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Figure saved → {out_path2}")

# ── Third figure: Summary comparison table as visual ──
fig3, ax_t = plt.subplots(figsize=(14, 5))
ax_t.axis('off')

table_data = [
    ['Metric', 'Farey\nScheduling', 'DESYNC\n(jammed)', 'DESYNC\n(unjammed)', 'Pure\nALOHA', 'Slotted\nALOHA'],
    ['Collision Rate',
     f'{farey_metrics["collision_rate"]*100:.1f}%',
     f'{desync_metrics["collision_rate"]*100:.1f}%',
     f'{desync_unjam_metrics["collision_rate"]*100:.1f}%',
     f'{aloha_metrics["collision_rate"]*100:.1f}%',
     f'{saloha_metrics["collision_rate"]*100:.1f}%'],
    ['Throughput\n(per frame)',
     f'{farey_metrics["throughput"]:.1f}',
     f'{desync_metrics["throughput"]:.1f}',
     f'{desync_unjam_metrics["throughput"]:.1f}',
     f'{aloha_metrics["throughput"]:.1f}',
     f'{saloha_metrics["throughput"]:.1f}'],
    ['Coverage',
     f'{farey_metrics["coverage"]*100:.1f}%',
     f'{desync_metrics["coverage"]*100:.1f}%',
     f'{desync_unjam_metrics["coverage"]*100:.1f}%',
     f'{aloha_metrics["coverage"]*100:.1f}%',
     f'{saloha_metrics["coverage"]*100:.1f}%'],
    ['Worst Latency\n(frames)',
     f'{farey_metrics["worst_latency"]}',
     f'{desync_metrics["worst_latency"]}',
     f'{desync_unjam_metrics["worst_latency"]}',
     f'{aloha_metrics["worst_latency"]}',
     f'{saloha_metrics["worst_latency"]}'],
    ['Convergence',
     '0 (instant)', 'NEVER (∞)', '~50 rounds', 'N/A', 'N/A'],
    ['Needs\nCommunication?',
     'NO', 'YES\n(FAILS)', 'YES', 'NO', 'NO'],
]

table = ax_t.table(
    cellText=[row[1:] for row in table_data[1:]],
    colLabels=table_data[0][1:],
    rowLabels=[row[0] for row in table_data[1:]],
    loc='center',
    cellLoc='center',
)
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.0, 2.0)

# Color the Farey column green, DESYNC jammed red
for (row, col), cell in table.get_celld().items():
    if col == 0:  # Farey column
        cell.set_facecolor('#d5f5e3')
    elif col == 1:  # DESYNC jammed
        cell.set_facecolor('#fadbd8')
    elif col == 2:  # DESYNC unjammed
        cell.set_facecolor('#fef9e7')
    elif col == 3:  # Pure ALOHA
        cell.set_facecolor('#ebdef0')
    elif col == 4:  # Slotted ALOHA
        cell.set_facecolor('#d6eaf8')
    if row == 0:  # header
        cell.set_fontsize(11)
        cell.set_text_props(fontweight='bold')

fig3.suptitle(
    'Protocol Comparison Summary — Denied Environment\n'
    f'{N_DRONES} drones, p={PRIME_P}, all communication jammed',
    fontsize=14, fontweight='bold'
)
plt.tight_layout()

out_path3 = os.path.join(OUTPUT_DIR, 'denied_env_summary_table.png')
fig3.savefig(out_path3, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Figure saved → {out_path3}")

# ── Final summary ──
print("\n" + "=" * 70)
print("KEY FINDINGS")
print("=" * 70)
print(f"""
FAREY SCHEDULING:
  - Collision rate:  {farey_metrics['collision_rate']*100:.1f}% (PERFECT — zero collisions)
  - Throughput:      {farey_metrics['throughput']:.0f}/{N_DRONES} drones served every frame
  - Coverage:        {farey_metrics['coverage']*100:.0f}%
  - Worst latency:   {farey_metrics['worst_latency']} frame(s)
  - Communication:   NONE NEEDED
  - Convergence:     Instant (pre-computed from shared prime)

DESYNC (JAMMED):
  - Collision rate:  {desync_metrics['collision_rate']*100:.1f}%
  - Throughput:      {desync_metrics['throughput']:.1f}/{N_DRONES}
  - Coverage:        {desync_metrics['coverage']*100:.1f}%
  - FAILURE MODE:    Beacons are jammed → phases never update →
                     random collisions persist FOREVER

PURE ALOHA:
  - Collision rate:  {aloha_metrics['collision_rate']*100:.1f}%
  - Throughput:      {aloha_metrics['throughput']:.1f}/{N_DRONES}
  - Theoretical max: 1/(2e) ≈ 18.4% of capacity

SLOTTED ALOHA:
  - Collision rate:  {saloha_metrics['collision_rate']*100:.1f}%
  - Throughput:      {saloha_metrics['throughput']:.1f}/{N_DRONES}
  - Theoretical max: 1/e ≈ 36.8% of capacity

CONCLUSION:
  In a denied (jammed) environment, Farey scheduling is the ONLY protocol
  that achieves perfect coordination. DESYNC fails completely because it
  requires beacon exchange. ALOHA variants work without communication but
  suffer high collision rates and poor coverage.

  Farey scheduling exploits number theory (k/p for prime p > N gives
  distinct slots) to achieve what other protocols need communication for.
""")

plt.close('all')
print("Done. All figures saved to experiments/")
