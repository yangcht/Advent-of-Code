import numpy as np
from multiprocessing import Pool

with open("./inputs/day06_1.txt") as f:
    grid = np.array([list(line) for line in f.read().splitlines()])

DIRS = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
ORDER = ["U", "R", "D", "L"]
rotate_right = lambda d: ORDER[(ORDER.index(d) + 1) % 4]

def simulate_1(grid):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=int)
    x, y, dir = next(((r, c, "U") for r, row in enumerate(grid) for c, v in enumerate(row) if v == "^"), (None, None, None))
    visited[x, y] += 1
    steps = 0
    max_steps = 4 * rows * cols
    
    while steps < max_steps:
        steps += 1
        dx, dy = DIRS[dir]
        nx, ny = x + dx, y + dy
        
        if not (0 <= nx < rows and 0 <= ny < cols):
            break
        
        if grid[nx, ny] != "#":
            x, y = nx, ny
            visited[x, y] += 1
        else:
            dir = rotate_right(dir)
    
    return np.count_nonzero(visited)

def check_loop(grid, x, y, dir, obs_x, obs_y, dp_state):
    rows, cols = grid.shape
    state = (x, y, dir, obs_x, obs_y)
    if state in dp_state:
        return dp_state[state]

    visited = set()
    while True:
        if (x, y, dir) in visited:
            dp_state[state] = True
            return True
        visited.add((x, y, dir))
        
        dx, dy = DIRS[dir]
        nx, ny = x + dx, y + dy
        
        if not (0 <= nx < rows and 0 <= ny < cols):
            dp_state[state] = False
            return False
        if (nx, ny) == (obs_x, obs_y) or grid[nx, ny] == "#":
            dir = rotate_right(dir)
        else:
            x, y = nx, ny

def _check_loop_call(grid, x, y, dir, r, c):
    dp_state = {}
    return check_loop(grid, x, y, dir, r, c, dp_state)

def simulate_2(grid):
    rows, cols = grid.shape
    x, y, dir = next(((r, c, "U") for r, row in enumerate(grid) for c, v in enumerate(row) if v == "^"), (None, None, None))
    candidates = [(r, c) for r in range(rows) for c in range(cols) if grid[r, c] == "." and (r, c) != (x, y)]

    # Multiprocessing for loop checks
    with Pool() as pool:
        results = pool.starmap(_check_loop_call, [(grid, x, y, dir, r, c) for (r, c) in candidates])

    loop_pos = {pos for pos, found in zip(candidates, results) if found}
    return len(loop_pos)

if __name__ == "__main__":
    print(f"Q1 sum: {simulate_1(grid)}")
    print(f"Q2 sum: {simulate_2(grid)}")
