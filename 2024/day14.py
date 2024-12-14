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
    valid = pos[(pos[:,0] != midx) & (pos[:,1] != midy)]
    q1 = np.sum((valid[:,0] < midx) & (valid[:,1] < midy))
    q2 = np.sum((valid[:,0] > midx) & (valid[:,1] < midy))
    q3 = np.sum((valid[:,0] < midx) & (valid[:,1] > midy))
    q4 = np.sum((valid[:,0] > midx) & (valid[:,1] > midy))
    return q1, q2, q3, q4

def safety_factor(quads):
    return np.prod(quads)

def create_grid(pos, w, h):
    grid = np.zeros((h, w), dtype=int)
    np.add.at(grid, (pos[:,1], pos[:,0]), 1)
    return grid

def calc_entropy(grid):
    counts = np.bincount(grid.flatten())
    probs = counts[counts > 0] / counts.sum()
    return -np.sum(probs * np.log2(probs))

def find_pattern_sec(pos, vel, w, h, max_sec=10000):
    min_sec, min_ent = None, float('inf')
    for sec in range(1, max_sec + 1):
        curr_pos = simulate(pos, vel, w, h, sec)
        ent = calc_entropy(create_grid(curr_pos, w, h))
        if ent < min_ent:
            min_ent, min_sec = ent, sec
    return min_sec

def main():
    pos, vel = parse('./inputs/day14_1.txt')
    w, h = 101, 103
    final_pos = simulate(pos, vel, w, h, 100)
    quads = count_quads(final_pos, w, h)
    print(f"Q1 safe factor: {safety_factor(quads)}")
    print(f"Q2 easter-egg second: {find_pattern_sec(pos, vel, w, h)}")

if __name__ == "__main__":
    main()