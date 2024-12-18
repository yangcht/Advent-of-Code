from collections import deque

def read_input(file):
    with open(file) as f:
        return [tuple(map(int, line.strip().split(','))) for line in f]

def mem_grid(size, positions, limit=1024):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    for i, (x, y) in enumerate(positions[:limit]):
        grid[y][x] = '#'
    return grid

def shortest_path(grid, start, end):
    size = len(grid)
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    q = deque([(start[0], start[1], 0)])
    visited = {start}

    while q:
        x, y, steps = q.popleft()
        if (x, y) == end:
            return steps
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and grid[ny][nx] == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                q.append((nx, ny, steps + 1))
    return -1

def main():
    grid = mem_grid(71, read_input('./inputs/day18_1.txt'))
    print(f"Q1 Min steps is {shortest_path(grid, (0, 0), (70, 70))}")

if __name__ == "__main__":
    main()