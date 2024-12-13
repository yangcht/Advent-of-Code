import numpy as np
from scipy.optimize import linprog

def parse_data(lines):
    def extract_vals(line, sep):
        return tuple(int(part.split(sep)[1]) for part in line.strip().split(':')[1].split(','))
    return extract_vals(lines[0], '+'), extract_vals(lines[1], '+'), extract_vals(lines[2], '=')

def min_cost(a, b, prize, part):
    ax, ay = a
    bx, by = b
    px, py = (prize[0] + 10**13, prize[1] + 10**13) if part == 2 else prize

    res = linprog([3, 1], A_eq=[[ax, bx], [ay, by]], b_eq=[px, py])
    if not res.success:
        return None

    A, B = map(round, res.x)
    if ax * A + bx * B == px and ay * A + by * B == py:
        return 3 * A + B, (A, B)
    return None

def main(part):
    with open('./inputs/day13_1.txt') as f:
        lines = [line.strip() for line in f if line.strip()]

    machines = [lines[i:i+3] for i in range(0, len(lines), 3)]
    total_cost, solutions = 0, []

    for idx, mach in enumerate(machines, 1):
        if (res := min_cost(*parse_data(mach), part=part)):
            cost, (A, B) = res
            total_cost += cost
            solutions.append((idx, A, B, cost))

    print(f"Q{part} min tokens: {total_cost}")

if __name__ == "__main__":
    main(1)
    main(2)