import numpy as np

def read_contraption(file_path):
    with open(file_path) as f:
        return np.array([[char for char in line.strip()] for line in f])

def update_direction(direction, tile):
    direction_map = {('→', '/'): '↑', ('↓', '/'): '←', ('←', '/'): '↓', ('↑', '/'): '→',
                    ('→', '\\'): '↓', ('↑', '\\'): '←', ('←', '\\'): '↑', ('↓', '\\'): '→'}
    return direction_map.get((direction, tile), direction)

def trace_beam(x, y, direction, energized, contraption):
    arrow_map = {'→': (0, 1), '←': (0, -1), '↑': (-1, 0), '↓': (1, 0)}
    valid_mirrors = {('|', '←'), ('|', '→'), ('-', '↑'), ('-', '↓')}

    while 0 <= x < len(contraption) and 0 <= y < len(contraption[0]):
        tile = contraption[x, y]

        if tile in '/\\':
            direction = update_direction(direction, tile)
        elif tile in '-|' and (x, y) in energized:
            return energized

        energized.add((x, y))

        if (tile, direction) in valid_mirrors:
            new_directions = {'|': [('↑', -1, 0), ('↓', 1, 0)], '-': [('←', 0, -1), ('→', 0, 1)]}[tile]
            for new_direction, dx, dy in new_directions:
                trace_beam(x + dx, y + dy, new_direction, energized, contraption)
            return energized

        dx, dy = arrow_map[direction]
        x, y = x + dx, y + dy

    return energized

def find_optimal_start(contraption):
    rows, cols = contraption.shape
    max_energized = 0

    # Top and bottom rows
    for y in range(cols):
        max_energized = max(max_energized, len(trace_beam(0, y, '↓', set(), contraption)))
        max_energized = max(max_energized, len(trace_beam(rows - 1, y, '↑', set(), contraption)))

    # Leftmost and rightmost columns
    for x in range(rows):
        max_energized = max(max_energized, len(trace_beam(x, 0, '→', set(), contraption)))
        max_energized = max(max_energized, len(trace_beam(x, cols - 1, '←', set(), contraption)))

    return max_energized

file_path = 'd16_input.txt'
contraption = read_contraption(file_path)
if contraption is not None:
    energized = set()
    trace_beam(0, 0, '→', energized, contraption)
    print(f"Part 1 = {len(energized)}")

    optimal_energized = find_optimal_start(contraption)
    print(f"Part 2 = {optimal_energized}")
else:
    print("Fail")