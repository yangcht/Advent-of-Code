import itertools
import functools

NUM_LAYOUT = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
                 "0": (3, 1), "A": (3, 2)
}
DIR_LAYOUT = { "^": (0, 1), "A": (0, 2), 
               "<": (1, 0), "v": (1, 1), ">": (1, 2) }

def valid_path(moves, y, x, gap_y, gap_x):
    delta = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    for move in moves:
        if move == "A":
            continue
        y, x = y + delta[move][0], x + delta[move][1]
        if (y, x) == (gap_y, gap_x):
            return False
    return True

@functools.cache
def step_cost(py, px, ny, nx, depth, max_depth):
    dy, dx = ny - py, nx - px
    options = []
    for perm in itertools.permutations(range(4)):
        seq = []
        for p in perm:
            if p == 0 and dx > 0: seq.extend([">"] * abs(dx))
            if p == 1 and dy > 0: seq.extend(["v"] * abs(dy))
            if p == 2 and dx < 0: seq.extend(["<"] * abs(dx))
            if p == 3 and dy < 0: seq.extend(["^"] * abs(dy))
        seq.append("A")
        seq = "".join(seq)
        gap_y, gap_x = (0, 0) if depth >= 0 else (3, 0)
        if valid_path(seq, py, px, gap_y, gap_x):
            options.append(line_cost(seq, depth + 1, max_depth))
    if options:
        return min(options)
    return float("inf")

def line_cost(line, depth, max_depth):
    if depth == max_depth:
        return len(line)
    layout = DIR_LAYOUT if depth >= 0 else NUM_LAYOUT
    py, px = layout["A"]
    total_cost = 0
    for move in line:
        ny, nx = layout[move]
        total_cost += step_cost(py, px, ny, nx, depth, max_depth)
        py, px = ny, nx
    return total_cost

def compute_cost(data, max_depth):
    total = 0
    for line in data:
        total += line_cost(line, -1, max_depth) * int(line[:3])
    return total

with open("./inputs/day21_1.txt") as file:
    data = file.read().splitlines()

#Part 1 and Part 2
print(f'Q1: {compute_cost(data, 2)}')
print(f'Q2: {compute_cost(data, 25)}')

