import numpy as np
import re

def parse(file):
    pattern = re.compile(r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)')
    with open(file, 'r') as f:
        matches = pattern.findall(f.read())
    data = np.array(matches, dtype=int)
    return data[:, :2], data[:, 2:]

def simulate(pos, vel, w, h, sec):
    return (pos + vel * sec) % [w, h]

def count_quads(pos, w, h):
    midx, midy = w // 2, h // 2
    x, y = pos[:, 0], pos[:, 1]
    return (
        np.sum((x < midx) & (y < midy) & (x != midx) & (y != midy)),
        np.sum((x > midx) & (y < midy) & (x != midx) & (y != midy)),
        np.sum((x < midx) & (y > midy) & (x != midx) & (y != midy)),
        np.sum((x > midx) & (y > midy) & (x != midx) & (y != midy)),
    )

def calc_entropy(pos, w, h):
    pos_down = pos // 2
    grid = np.zeros(((h + 1) // 2, (w + 1) // 2), dtype=int)
    np.add.at(grid, (pos_down[:, 1], pos_down[:, 0]), 1)
    counts = np.bincount(grid.flatten())
    counts = counts[counts > 0]
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs))

def find_pattern_sec(pos, vel, w, h, max_sec=10000):
    min_sec, min_ent, curr_pos = None, float('inf'), pos.copy()
    for sec in range(1, max_sec + 1):
        curr_pos = (curr_pos + vel) % [w, h]
        ent = calc_entropy(curr_pos, w, h)
        if ent < min_ent:
            min_sec, min_ent = sec, ent
    return min_sec

def main():
    pos, vel = parse('./inputs/day14_1.txt')
    w, h = 101, 103
    final_pos = simulate(pos, vel, w, h, 100)

    #PART 1: calculate the numbers in the quardrants
    print(f"Q1 safe factor: {np.prod(count_quads(final_pos, w, h))}")
    #PART 2: searching the patterns
    print(f"Q2 easter-egg second: {find_pattern_sec(pos, vel, w, h)}")

if __name__ == "__main__":
    main()
