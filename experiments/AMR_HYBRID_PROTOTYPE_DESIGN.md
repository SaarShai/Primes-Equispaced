### Design: Hybrid AMR with Farey Transitions

This design proposes a hybrid Adaptive Mesh Refinement (AMR) strategy for OpenFOAM (or a generic finite volume solver). It combines the robust structure of Quadtree/Box refinement (QT) with the precision of Farey-based rational alignment, using a specialized "Transition" mechanism to handle non-conformities without cascading refinement.

#### 1. Design Philosophy & Strategy
The core conflict in standard AMR is the "Staircase Effect." If a shock lies at a non-dyadic rational coordinate (e.g., $x=1/3$ or $x=0.3$), a standard QT grid (which refines by powers of 2, i.e., $1/2, 1/4, 1/8$) cannot align exactly with the shock without cascading refinement to a very fine level, unnecessarily refining large areas of the domain.

**The Solution:**
1.  **Farey Split:** Cells containing shocks are refined using a "Farey Mediant" approach. This creates sub-cells aligned to the shock coordinate (rational alignment) rather than a strict power-of-2 grid.
2.  **Transition Elements:** Because the Farey split produces edges of arbitrary rational lengths (e.g., $1/3$) and standard QT neighbors have dyadic lengths (e.g., $1/2$), a direct geometric match is impossible.
    *   *Standard AMR (Cascade):* Refine the neighbor recursively until lengths match (expensive).
    *   *Proposed Design (Zero Cascading):* We do **not** cascade. Instead, we introduce a **Transition Element** (or Patch) at the interface. This element bridges the rational gap, ensuring the mesh remains conforming (no hanging nodes left unaddressed) while preserving the local resolution of the shock.

#### 2. Key Components

*   **`QT_Cell`**: Standard refinement. Splits $[0,1] \to [0, 0.5], [0.5, 1]$. Vertices are dyadic rationals ($k/2^n$).
*   **`Farey_Cell`**: Refined using mediant insertion. If a shock is at $x$, the split aligns a vertex to $x$.
*   **`Transition_Element`**: A specialized geometry or patch connecting a `Farey_Cell` face (length $L_{farey}$) to a `QT_Cell` face (length $L_{qt}$). In a standard hexahedral context, this is often a T-junction or a set of generalized polyhedra, but here we model it logically as a bridging patch.

#### 3. Python Design Implementation

The following Python class design simulates the topology and logic of this hybrid grid.

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple
import random

@dataclass
class Node:
    x: float
    y: float
    id: int

class AMR_Cell:
    """Base class for cells."""
    def __init__(self, id: int, level: int, coords: Tuple[float, float, float, float]):
        self.id = id
        self.level = level
        self.coords = coords # (x0, y0, x1, y1)
        self.is_shock = False
        self.type = "QT"
        self.children: List['AMR_Cell'] = []

    def split(self, cell_type: str):
        """Generate children based on split type."""
        pass

    def __repr__(self):
        return f"Cell({self.id}, L{self.level}, {self.type})"

class FareyCell(AMR_Cell):
    """
    A cell refined using Farey Mediant logic.
    This creates a split aligned to a specific rational shock location.
    """
    def __init__(self, id: int, level: int, coords: Tuple[float, float, float, float], shock_loc: float):
        super().__init__(id, level, coords)
        self.type = "Farey"
        self.is_shock = True
        self.shock_loc = shock_loc # The precise location of the shock within this cell

    def split(self) -> List['FareyCell']:
        """
        Farey Split:
        Splits the cell such that one edge aligns with shock_loc.
        Standard QT splits at 0.5. Farey splits at shock_loc (e.g., 0.3).
        Creates sub-cells with non-power-of-2 dimensions.
        """
        x0, y0, x1, y1 = self.coords
        
        # Define split line at shock_loc
        # In 1D (x-axis for simplicity), we split at shock_loc
        mid_x = shock_loc
        
        # Create sub-cells (Left and Right for 1D, or similar logic for 2D)
        # 1D logic for simulation purposes
        left_child = FareyCell(self.id*2, self.level+1, (x0, y0, mid_x, y1), mid_x)
        right_child = FareyCell(self.id*2+1, self.level+1, (mid_x, y0, x1, y1), mid_x)
        
        return [left_child, right_child]

class TransitionElement:
    """
    A specialized element used to bridge Farey/QT boundaries without cascading.
    This represents the 'Zero Cascading' approach.
    Instead of refining the neighbor, we insert a bridge.
    """
    def __init__(self, id: int, farey_face: float, qt_face: float):
        self.id = id
        self.farey_face_length = farey_face
        self.qt_face_length = qt_face
        self.type = "Transition"
        
        # Log savings
        self.cost_reduction = 0
        self._calculate_impact()

    def _calculate_impact(self):
        """
        Simulates the cost savings of using a Transition Element vs Cascading.
        Cascading would force the QT neighbor to split until its edge matches the Farey edge.
        """
        # If we cascaded, we might need to split the QT neighbor multiple times.
        # Transition elements act as a "patch" (e.g. T-junction or 2 quads).
        # The logic implies we avoid the cascade depth.
        self.cost_reduction = 1.0 # Represents avoiding the cascade cost
        print(f"Transition Element {self.id}: Bridged gap {self.farey_face_length} vs {self.qt_face_length}")

class HybridAMRManager:
    def __init__(self, mesh_size: int = 100):
        self.mesh_size = mesh_size
        self.cells: Dict[int, AMR_Cell] = {}
        self.transition_elements: List[TransitionElement] = []

    def identify_shocks(self):
        """Simulate shock detection."""
        # Randomly place a shock
        shock_x = 0.33 # A rational number that isn't dyadic (1/3)
        # Mark a cell at this location
        cell_id = 1
        self.cells[cell_id] = FareyCell(cell_id, 0, (0.0, 0.0, 1.0, 1.0), shock_x)

    def apply_farey_split(self, cell: FareyCell):
        """Applies the Farey Split logic."""
        children = cell.split()
        # In a real implementation, we'd update topology here.
        # For simulation, we track that a split occurred.
        pass

    def resolve_boundary_non_conformity(self, farey_cell: FareyCell, qt_neighbor: AMR_Cell):
        """
        The Core Logic: Zero Cascading.
        Checks boundary lengths. If mismatch (Farey vs QT):
        1. Standard approach: Cascade QT neighbor (Expensive).
        2. This design: Use Transition Element (Cheaper/Faster).
        """
        
        # Calculate lengths
        # Farey split at 0.33 creates edges ~0.33 and ~0.67 (relative to cell width)
        farey_edge_len = 0.33 
        qt_edge_len = 0.5 # Standard QT level match
        
        # Check 2:1 rule or Conformance
        if abs(farey_edge_len - qt_edge_len) > 0.01:
            print(f"Non-conformity detected: Farey({farey_edge_len}) != QT({qt_edge_len})")
            
            # Option A: Cascade (Commented out per "Zero Cascading" design)
            # self.cascade_refinement(qt_neighbor) 
            
            # Option B: Use Transition Element (Active Design)
            trans_id = len(self.transition_elements)
            trans = TransitionElement(trans_id, farey_edge_len, qt_edge_len)
            self.transition_elements.append(trans)
            print(f"Zero Cascading Applied: Used Transition Element ID {trans_id} to bridge gap.")
            
        return len(self.transition_elements)

    def run_simulation(self):
        self.identify_shocks()
        
        # Get the Farey Cell
        farey_cell = list(self.cells.values())[0]
        
        # Simulate a neighbor
        qt_neighbor = AMR_Cell(id=101, level=0, coords=(0.0, 0.0, 1.0, 1.0))
        
        print("\n--- AMR Topology Resolution ---")
        self.apply_farey_split(farey_cell)
        
        # Resolve the interface
        count = self.resolve_boundary_non_conformity(farey_cell, qt_neighbor)
        
        print(f"\nTotal Transition Elements Generated: {count}")

# Run the design
if __name__ == "__main__":
    manager = HybridAMRManager()
    manager.run_simulation()
```

### Explanation of "Zero Cascading" Savings

The Python simulation above illustrates the **Transition Element** logic. Here is the breakdown of why this design saves computational resources compared to a standard AMR cascade:

1.  **The Problem (The Staircase Effect):**
    *   A shock is located at $x = 1/3$.
    *   A standard QT grid cell spans $x \in [0, 1]$.
    *   To resolve the shock, a QT grid must refine the cell until a node exists at or near $1/3$. Since $1/3$ is not a dyadic rational (i.e., not $k/2^n$), the QT grid must refine to a specific depth (Level 10 or 11) just to approximate $1/3$ closely enough for the solver.
    *   Once refined to that depth, *all* neighbors along that face must also be refined to maintain the 2:1 conformity rule. This cascades the refinement deep into the domain, creating thousands of extra elements near the shock.

2.  **The Farey Solution:**
    *   A `FareyCell` splits exactly at $x = 1/3$. It is locally conforming and perfectly aligned with the physics of the shock.
    *   However, its face now has a length corresponding to $1/3$ (of the parent width).

3.  **The Transition Element (Zero Cascading):**
    *   The standard neighbor (`QT_Cell`) has a face length of $1/2$ (at that level).
    *   **Standard Cascade:** To fix the $1/3$ vs $1/2$ mismatch, the neighbor must split until its face aligns with the $1/3$ requirement (requiring very deep recursion).
    *   **Our Design:** We use a **Transition Element**. This acts as a "T-junction" or a specialized patch. It takes the coarse QT face and maps it to the fine Farey face without forcing the QT neighbor to subdivide recursively.

**Performance Impact:**
*   **Cascade:** Depth $N$ -> Cost $\propto 4^N$ (exponential growth in mesh size).
*   **Transition:** Depth $N$ -> Cost $\propto 1$ (constant overhead for the patch).
*   The result is a mesh that resolves the shock with high precision (due to Farey splitting) without generating the massive block of cells usually required to satisfy the 2:1 conformity rule on the neighbor.
