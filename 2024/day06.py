import numpy as np

with open("./inputs/day06_1.txt") as f:
    grid = np.array([list(line) for line in f.read().splitlines()])

DIRS = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
ORDER = ["U", "R", "D", "L"]
rotate_right = lambda d: ORDER[(ORDER.index(d) + 1) % 4]

# PART 1: Calculate moves
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

print(f"Q1 sum: {simulate_1(grid)}")

# PART 2: Find loops
def simulate_2(grid):
    rows, cols = grid.shape
    x, y, dir = next(((r, c, "U") for r, row in enumerate(grid) for c, v in enumerate(row) if v == "^"), (None, None, None))
    memo = {}
    loop_pos = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == "." and (r, c) != (x, y):
                if check_loop(grid, x, y, dir, r, c, memo):
                    loop_pos.add((r, c))

    return len(loop_pos)

def check_loop(grid, x, y, dir, obs_x, obs_y, memo):
    rows, cols = grid.shape
    state = (x, y, dir, obs_x, obs_y)

    if state in memo:
        return memo[state]

    is_visited = set()
    while True:
        if (x, y, dir) in is_visited:
            memo[state] = True
            return True
        is_visited.add((x, y, dir))

        dx, dy = DIRS[dir]
        nx, ny = x + dx, y + dy

        if not (0 <= nx < rows and 0 <= ny < cols):
            memo[state] = False
            return False

        if (nx, ny) == (obs_x, obs_y) or grid[nx, ny] == "#":
            dir = rotate_right(dir)
        else:
            x, y = nx, ny

print(f"Q2 sum: {simulate_2(grid)}")