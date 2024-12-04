import numpy as np

# PART 1: counting the incidents of XMAS in the char matrix
def count_xmas(grid):
    target = "XMAS"
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def valid(r, c, dr, dc):
        return all(
            0 <= r + k * dr < grid.shape[0] and
            0 <= c + k * dc < grid.shape[1] and
            grid[r + k * dr, c + k * dc] == target[k]
            for k in range(len(target))
        )

    return sum(
        valid(r, c, dr, dc)
        for r, c in np.ndindex(grid.shape)
        if grid[r, c] == target[0]
        for dr, dc in directions
    )

# PART 2: counting the incidents of the corss MAS
def count_x_mas(grid):

    grid = np.array([list(row) for row in grid])

    center_A = grid[1:-1, 1:-1] == 'A'

    tl = grid[:-2, :-2]
    tr = grid[:-2, 2:]
    bl = grid[2:, :-2]
    br = grid[2:, 2:]

    filter1 = (tl == 'M') & (tr == 'M') & (bl == 'S') & (br == 'S')
    filter2 = (tl == 'M') & (tr == 'S') & (bl == 'M') & (br == 'S')
    filter3 = (tl == 'S') & (tr == 'M') & (bl == 'S') & (br == 'M')
    filter4 = (tl == 'S') & (tr == 'S') & (bl == 'M') & (br == 'M')

    total_x_mas = np.sum(center_A & (filter1 | filter2 | filter3 | filter4))

    return total_x_mas

if __name__ == "__main__":
    matrix = np.genfromtxt("./inputs/day04_1.txt", dtype=str, delimiter="\n")
    grid = np.array([list(row) for row in matrix])
    print(f"Q1 counts: {count_xmas(grid)}")
    print(f"Q2 counts: {count_x_mas(grid)}")