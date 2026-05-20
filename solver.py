"""
Buzzled Master Solver - Daily #378
===================================
Hex grid radius=3 (side=4), 37 hexes, cube coords (q,r,s) with q+r+s=0.
Master mode: pins show target COUNT of hexes of a specific color per row.
Uses backtracking with constraint propagation to solve.
"""
import sys
from copy import deepcopy

# ─── GRID ─────────────────────────────────────────────────────
RADIUS = 3
ALL_HEXES = []
for q in range(-RADIUS, RADIUS+1):
    for r in range(-RADIUS, RADIUS+1):
        s = -q - r
        if abs(s) <= RADIUS:
            ALL_HEXES.append((q, r, s))
ALL_HEXES.sort(key=lambda h: (h[1], h[0]))
HEX_IDX = {h: i for i, h in enumerate(ALL_HEXES)}
N = len(ALL_HEXES)  # 37

def rows_by(ci):
    d = {}
    for h in ALL_HEXES:
        d.setdefault(h[ci], []).append(h)
    return d

rows_r = rows_by(1)
rows_q = rows_by(0)
rows_s = rows_by(2)

# ─── CONSTRAINTS from Master Daily #378 ──────────────────────
# Format: (row_hex_list, target_color, target_count)
# target_color: 'Y' or 'B'
# target_count: number of hexes of that color in the row

CONSTRAINTS = []

# Horizontal rows (constant r)
horiz = [
    (-3, 'B', 3),  # r=-3, 4 hexes, 3 black
    (-2, 'Y', 2),  # r=-2, 5 hexes, 2 yellow
    (-1, 'Y', 3),  # r=-1, 6 hexes, 3 yellow
    ( 0, 'B', 4),  # r= 0, 7 hexes, 4 black
    ( 1, 'B', 4),  # r= 1, 6 hexes, 4 black
    ( 2, 'B', 2),  # r= 2, 5 hexes, 2 black
    ( 3, 'B', 2),  # r= 3, 4 hexes, 2 black
]
for val, color, count in horiz:
    CONSTRAINTS.append((rows_r[val], color, count, f"r={val}"))

# Diagonal TL-BR (constant q)
diag_q = [
    (-3, 'Y', 3),  # q=-3, 4 hexes
    (-2, 'B', 2),  # q=-2, 5 hexes
    (-1, 'Y', 1),  # q=-1, 6 hexes
    ( 0, 'Y', 2),  # q= 0, 7 hexes
    ( 1, 'B', 3),  # q= 1, 6 hexes
    ( 2, 'Y', 1),  # q= 2, 5 hexes
    ( 3, 'Y', 3),  # q= 3, 4 hexes
]
for val, color, count in diag_q:
    CONSTRAINTS.append((rows_q[val], color, count, f"q={val}"))

# Diagonal BL-TR (constant s)
diag_s = [
    ( 3, 'B', 2),  # s= 3, 4 hexes
    ( 2, 'B', 3),  # s= 2, 5 hexes
    ( 1, 'B', 4),  # s= 1, 6 hexes
    ( 0, 'Y', 2),  # s= 0, 7 hexes
    (-1, 'Y', 4),  # s=-1, 6 hexes
    (-2, 'Y', 2),  # s=-2, 5 hexes
    (-3, 'Y', 2),  # s=-3, 4 hexes
]
for val, color, count in diag_s:
    CONSTRAINTS.append((rows_s[val], color, count, f"s={val}"))

# Verify constraint validity
print(f"Grid: {N} hexes, {len(CONSTRAINTS)} constraints")
for hexes, color, count, label in CONSTRAINTS:
    assert count <= len(hexes), f"Invalid: {label} has {len(hexes)} hexes but needs {count} {color}"
    print(f"  {label}: {len(hexes)} hexes, {count} {color}")

# ─── SOLVER ───────────────────────────────────────────────────
# State: list of N values, each 'Y', 'B', or None (unassigned)

def check_constraints(state):
    """Check if current partial assignment is still feasible."""
    for hexes, color, count, label in CONSTRAINTS:
        indices = [HEX_IDX[h] for h in hexes]
        assigned_color = sum(1 for i in indices if state[i] == color)
        unassigned = sum(1 for i in indices if state[i] is None)
        other_color = 'B' if color == 'Y' else 'Y'
        assigned_other = sum(1 for i in indices if state[i] == other_color)
        
        # Too many of target color already
        if assigned_color > count:
            return False
        # Not enough unassigned to reach target
        if assigned_color + unassigned < count:
            return False
        # Check the complement: remaining other = len - count
        other_needed = len(hexes) - count
        if assigned_other > other_needed:
            return False
        if assigned_other + unassigned < other_needed:
            return False
    return True

def is_solved(state):
    """Check if all hexes are assigned and all constraints are satisfied."""
    if any(s is None for s in state):
        return False
    for hexes, color, count, label in CONSTRAINTS:
        indices = [HEX_IDX[h] for h in hexes]
        actual = sum(1 for i in indices if state[i] == color)
        if actual != count:
            return False
    return True

def propagate(state):
    """Try to deduce forced assignments from constraints."""
    changed = True
    while changed:
        changed = False
        for hexes, color, count, label in CONSTRAINTS:
            indices = [HEX_IDX[h] for h in hexes]
            assigned_color = sum(1 for i in indices if state[i] == color)
            unassigned_indices = [i for i in indices if state[i] is None]
            other_color = 'B' if color == 'Y' else 'Y'
            assigned_other = sum(1 for i in indices if state[i] == other_color)
            
            remaining_needed = count - assigned_color
            other_needed = len(hexes) - count - assigned_other
            
            # If all remaining unassigned must be target color
            if remaining_needed == len(unassigned_indices) and remaining_needed > 0:
                for i in unassigned_indices:
                    state[i] = color
                    changed = True
            
            # If no more target color needed, fill rest with other
            if remaining_needed == 0 and len(unassigned_indices) > 0:
                for i in unassigned_indices:
                    state[i] = other_color
                    changed = True
            
            # If all remaining must be other color
            if other_needed == len(unassigned_indices) and other_needed > 0:
                for i in unassigned_indices:
                    state[i] = other_color
                    changed = True
            
            # If no more other color needed
            if other_needed == 0 and len(unassigned_indices) > 0:
                for i in unassigned_indices:
                    state[i] = color
                    changed = True
        
        if not check_constraints(state):
            return False
    return True

def solve(state, depth=0):
    """Backtracking solver with constraint propagation."""
    saved = state[:]
    
    if not propagate(state):
        state[:] = saved
        return False
    
    if is_solved(state):
        return True
    
    # Find first unassigned hex
    idx = next(i for i in range(N) if state[i] is None)
    
    for color in ['Y', 'B']:
        state[:] = saved[:]
        propagate(state)  # re-propagate from saved state
        state[idx] = color
        if check_constraints(state):
            if solve(state, depth + 1):
                return True
    
    state[:] = saved
    return False

# ─── SOLVE ────────────────────────────────────────────────────
print("\nSolving...")
state = [None] * N

if solve(state):
    print("\n✅ SOLUTION FOUND!\n")
    
    # Display solution as grid
    for r in range(-3, 4):
        row_hexes = rows_r[r]
        row_hexes.sort(key=lambda h: h[0])
        indent = " " * (7 - len(row_hexes)) * 2
        cells = []
        for h in row_hexes:
            c = state[HEX_IDX[h]]
            symbol = "🟡" if c == 'Y' else "⚫"
            cells.append(symbol)
        print(f"  {indent}{' '.join(cells)}   (r={r})")
    
    # Also display as coordinate mapping
    print("\nDetailed solution:")
    for h in ALL_HEXES:
        c = state[HEX_IDX[h]]
        color_name = "YELLOW" if c == 'Y' else "BLACK"
        print(f"  ({h[0]:+d},{h[1]:+d},{h[2]:+d}) = {color_name}")
    
    # Verify all constraints
    print("\nConstraint verification:")
    all_ok = True
    for hexes, color, count, label in CONSTRAINTS:
        indices = [HEX_IDX[h] for h in hexes]
        actual = sum(1 for i in indices if state[i] == color)
        status = "✅" if actual == count else "❌"
        if actual != count:
            all_ok = False
        color_name = "yellow" if color == 'Y' else "black"
        print(f"  {status} {label}: need {count} {color_name}, got {actual}")
    
    if all_ok:
        print("\n🎉 All constraints satisfied!")
    else:
        print("\n⚠️ Some constraints failed!")
else:
    print("\n❌ No solution found! The constraints may be incorrect.")
    print("Please verify the pin colors and numbers from the image.")
