import numpy as np

WALL, EMPTY, BOX, ROBOT = 0, 1, 2, 3
DIRS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

def parse_input(file):
    with open(file) as f:
        lines = f.read().strip().split("\n")
    return ([list(line) for line in lines if line.startswith('#')], 
            ''.join(line.strip() for line in lines if not line.startswith('#')))

def build_grid(layout):
    h, w = len(layout), max(len(row) for row in layout)
    grid = np.full((h, w), EMPTY, int)
    robot = next((i, row.index('@')) for i, row in enumerate(layout) if '@' in row)
    char_map = {'#': WALL, '.': EMPTY, 'O': BOX, '@': ROBOT}
    for i, row in enumerate(layout):
        for j, char in enumerate(row):
            grid[i, j] = char_map.get(char, EMPTY)
    return grid, robot

def move_robot(grid, robot, mv):
    dx, dy = DIRS.get(mv, (0, 0))
    rx, ry = robot
    nx, ny = rx + dx, ry + dy

    if not (0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]):
        return grid, robot
    if grid[nx, ny] == EMPTY:
        grid[rx, ry], grid[nx, ny] = EMPTY, ROBOT
        return grid, (nx, ny)
    if grid[nx, ny] == BOX:
        chain = [(nx, ny)]
        while 0 <= chain[-1][0] + dx < grid.shape[0] and 0 <= chain[-1][1] + dy < grid.shape[1] and grid[chain[-1][0] + dx, chain[-1][1] + dy] == BOX:
            chain.append((chain[-1][0] + dx, chain[-1][1] + dy))
        if 0 <= chain[-1][0] + dx < grid.shape[0] and 0 <= chain[-1][1] + dy < grid.shape[1] and grid[chain[-1][0] + dx, chain[-1][1] + dy] == EMPTY:
            for bx, by in reversed(chain):
                grid[bx + dx, by + dy], grid[bx, by] = BOX, EMPTY
            grid[rx, ry], grid[nx, ny] = EMPTY, ROBOT
            return grid, (nx, ny)
    return grid, robot

def gps_sum(grid):
    return sum(100 * x + y for x, y in np.argwhere(grid == BOX))

def print_map(grid):
    symbols = {WALL: '#', EMPTY: '.', BOX: 'O', ROBOT: '@'}
    print('\n'.join(''.join(symbols[c] for c in row) for row in grid), "\n")

def main():
    layout, moves = parse_input('./inputs/day15_1.txt')
    grid, robot = build_grid(layout)

    print("Initial Map:")
    print_map(grid)

    for mv in moves:
        grid, robot = move_robot(grid, robot, mv)

    print("Final Map:")
    print_map(grid)
    print(f"Q1 sum: {gps_sum(grid)}")

if __name__ == "__main__":
    main()
