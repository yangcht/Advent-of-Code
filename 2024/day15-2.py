from collections import deque

def parse_input(file):
    with open(file) as f:
        lines = f.read().strip().split("\n")
    return [list(line) for line in lines if line.startswith('#')], ''.join(line.strip() for line in lines if not line.startswith('#'))

def expand_map(layout):
    return [[c for tile in row for c in {'#': '##', 'O': '[]', '.': '..', '@': '@.'}.get(tile, tile)] for row in layout]

def find_robot(layout):
    for y, row in enumerate(layout):
        if '@' in row:
            return row.index('@'), y

def valid_pos(layout, x, y):
    return 0 <= y < len(layout) and 0 <= x < len(layout[0]) and layout[y][x] != '#'

def push_block(layout, start, direction, vertical):
    dx, dy = direction
    queue, block, visited = deque([start]), [], set()

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited or not valid_pos(layout, x, y) or layout[y][x] not in ('[', ']'):
            continue
        visited.add((x, y))
        block.append((x, y))
        queue.extend([(x + (1 if layout[y][x] == '[' else -1), y), (x, y + dy)] if vertical else [(x + dx, y)])

    if any(not valid_pos(layout, bx + dx, by + dy) or layout[by + dy][bx + dx] == '#' for bx, by in block):
        return False

    for bx, by in reversed(block):
        nx, ny = bx + dx, by + dy
        layout[ny][nx], layout[by][bx] = layout[by][bx], '.'
    return True

def move_robot(layout, pos, move):
    x, y = pos
    dx, dy = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}[move]
    nx, ny = x + dx, y + dy

    if not valid_pos(layout, nx, ny):
        return pos
    if layout[ny][nx] in ('.', '@'):
        layout[y][x], layout[ny][nx] = '.', '@'
        return nx, ny
    if layout[ny][nx] in ('[', ']') and push_block(layout, (nx, ny), (dx, dy), dy != 0):
        layout[y][x], layout[ny][nx] = '.', '@'
        return nx, ny
    return pos

def gps_sum(layout):
    return sum(100 * y + x for y, row in enumerate(layout) for x, tile in enumerate(row) if tile == '[')

def print_map(layout):
    print("\n".join(map(''.join, layout)), "\n")

def main():
    layout, moves = parse_input('./inputs/day15_1.txt')
    layout = expand_map(layout)

    print("Initial Expanded Map:")
    print_map(layout)

    robot = find_robot(layout)
    for move in moves:
        robot = move_robot(layout, robot, move)

    print("Final Expanded Map:")
    print_map(layout)

    gps_total = gps_sum(layout)
    print(f"Q2 sum: {gps_total}")
    return gps_total

if __name__ == "__main__":
    main()
