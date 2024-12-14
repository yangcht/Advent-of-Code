import numpy as np
from numba import njit

with open("./inputs/day06_1.txt") as f:
    grid = np.array([list(line) for line in f.read().splitlines()])

DIRS = np.array([(-1, 0), (0, 1), (1, 0), (0, -1)]) 

@njit
def find_start(grid):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == "^":
                return r, c
    return -1, -1

@njit
def simulate_1(grid):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=np.int32)
    x, y = find_start(grid)
    dir_index = 0

    steps = 0
    max_steps = 4 * rows * cols

    while steps < max_steps:
        steps += 1
        dx, dy = DIRS[dir_index]
        nx, ny = x + dx, y + dy

        if not (0 <= nx < rows and 0 <= ny < cols):
            break

        if grid[nx, ny] != "#":
            x, y = nx, ny
            visited[x, y] += 1
        else:
            dir_index = (dir_index + 1) % 4

    return np.count_nonzero(visited)

@njit
def check_loop(grid, x, y, dir_index, obs_x, obs_y):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols, 4), dtype=np.bool_)
    while True:
        if visited[x, y, dir_index]:
            return True
        visited[x, y, dir_index] = True

        dx, dy = DIRS[dir_index]
        nx, ny = x + dx, y + dy

        if not (0 <= nx < rows and 0 <= ny < cols):
            return False

        if (nx, ny) == (obs_x, obs_y) or grid[nx, ny] == "#":
            dir_index = (dir_index + 1) % 4
        else:
            x, y = nx, ny

@njit(parallel=True)
def simulate_2(grid):
    rows, cols = grid.shape
    x, y = find_start(grid)
    dir_index = 0
    candidates = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == "." and (r, c) != (x, y):
                candidates.append((r, c))

    candidates = np.array(candidates, dtype=np.int32)
    results = np.zeros(len(candidates), dtype=np.bool_)

    for i in range(len(candidates)):
        r, c = candidates[i]
        results[i] = check_loop(grid, x, y, dir_index, r, c)

    return np.sum(results)

if __name__ == "__main__":
    print(f"Q1 sum: {simulate_1(grid)}")
    print(f"Q2 sum: {simulate_2(grid)}")