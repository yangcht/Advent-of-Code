import numpy as np

def read_f(file_name):
    with open(file_name, 'r') as file:
        lines = [list(line.strip()) for line in file.readlines()]
    return np.array(lines)

def find_regions(matrix, char):
    visited = np.zeros_like(matrix, dtype=bool)
    rows, cols = matrix.shape
    regions = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and matrix[r, c] == char:
                stack, coords = [(r, c)], []
                while stack:
                    x, y = stack.pop()
                    if visited[x, y] or matrix[x, y] != char:
                        continue
                    visited[x, y] = True
                    coords.append((x, y))
                    stack.extend([
                        (nx, ny)
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if 0 <= (nx := x + dx) < rows and 0 <= (ny := y + dy) < cols
                    ])
                if coords:
                    regions.append(coords)
    return regions

def area_perimeter(region, matrix):
    area = len(region)
    perimeter = 0
    rows, cols = matrix.shape
    for x, y in region:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < rows and 0 <= ny < cols) or matrix[nx, ny] != matrix[x, y]:
                perimeter += 1
    return area, perimeter

def total_cost(matrix):
    unique_chars = np.unique(matrix)
    total_cost = 0

    for char in unique_chars:
        regions = find_regions(matrix, char)
        for region in regions:
            area, perimeter = area_perimeter(region, matrix)
            total_cost += area * perimeter
    return total_cost

def sides_count(reg, mat):
    rows, cols = mat.shape
    rs = set(reg)
    ue, de, le, re = [np.zeros((rows, cols), dtype=int) for _ in range(4)]

    for x, y in reg:
        ue[x, y] = 1 if x ==        0 or (x - 1, y) not in rs else 0
        de[x, y] = 1 if x == rows - 1 or (x + 1, y) not in rs else 0
        le[x, y] = 1 if y ==        0 or (x, y - 1) not in rs else 0
        re[x, y] = 1 if y == cols - 1 or (x, y + 1) not in rs else 0

    def h_count(mask):
        total = 0
        for row in mask:
            diff = np.diff(row, prepend=0)
            total += np.sum(diff == 1)
        return total

    def v_count(mask):
        total = 0
        for col in mask.T:
            diff = np.diff(col, prepend=0)
            total += np.sum(diff == 1)
        return total
    return h_count(ue) + h_count(de) + v_count(le) + v_count(re)

def total_cost_part_two(matrix):
    unique_chars = np.unique(matrix)
    total_cost = 0

    for char in unique_chars:
        regions = find_regions(matrix, char)
        for region in regions:
            area = len(region)
            sides = sides_count(region, matrix)
            total_cost += area * sides
    return total_cost

if __name__ == "__main__":
    matrix = read_f("./inputs/day12_1.txt")

    print(f"Q1 price: {total_cost(matrix)}")
    print(f"Q2 price: {total_cost_part_two(matrix)}")