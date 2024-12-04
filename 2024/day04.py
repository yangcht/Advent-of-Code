import numpy as np

# PART 1: counting the incidents of XMAS in the char matrix
def count_xmas(grid):
    target = "XMAS"
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    t_len = len(target)

    def valid(r, c, dr, dc):
        return all(
            0 <= r + k * dr < grid.shape[0] and
            0 <= c + k * dc < grid.shape[1] and
            grid[r + k * dr, c + k * dc] == target[k]
            for k in range(t_len)
        )

    return sum(
        valid(r, c, dr, dc)
        for r, c in np.ndindex(grid.shape)
        if grid[r, c] == target[0]
        for dr, dc in directions
    )

if __name__ == "__main__":
    matrix = np.genfromtxt("./inputs/day04_1.txt", dtype=str, delimiter="\n")
    grid = np.array([list(row) for row in matrix])
    nr_xmas = count_xmas(grid)
    print(f"Q1 counts: {nr_xmas}")