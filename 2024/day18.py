from collections import deque

def read_input(file):
    with open(file) as f:
        return [tuple(map(int, line.strip().split(','))) for line in f]

def mem_grid(size):
    return [['.' for m in range(size)] for n in range(size)]

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

def find_blocking_byte(grid, positions, start, end):
    for i, (x, y) in enumerate(positions):
        grid[y][x] = '#'
        if shortest_path(grid, start, end) == -1:
            return x, y
    return None

def main():
    positions = read_input('./inputs/day18_1.txt')
    grid = mem_grid(71)

    # PART 1: Path sarch after 1024 bytes
    for i, (x, y) in enumerate(positions[:1024]):
        grid[y][x] = '#'
    print(f"Q1 Min steps is {shortest_path(grid, (0, 0), (70, 70))}")

    # PART 2: First blocking byte
    grid = mem_grid(71)
    blocking_byte = find_blocking_byte(grid, positions, (0, 0), (70, 70))
    print(f"Q2 First blocking byte is {blocking_byte[0]},{blocking_byte[1]}")

if __name__ == "__main__":
    main()