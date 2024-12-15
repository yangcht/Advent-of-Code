import re
import numpy as np
from scipy.fft import fft2, ifft2

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

def calc_orderness(pos, w, h):
    grid = np.zeros((h, w), dtype=float)
    np.add.at(grid, (pos[:, 1], pos[:, 0]), 1)
    fft_grid = fft2(grid)
    autocorr = ifft2(fft_grid * fft_grid.conjugate()).real
    autocorr = np.fft.fftshift(autocorr)
    autocorr /= autocorr.max()
    mx, my = autocorr.shape[0] // 2, autocorr.shape[1] // 2
    cp = autocorr[mx, my]
    autocorr[mx, my] = 0
    orderness = np.max(autocorr)
    autocorr[mx, my] = cp
    return -orderness

def find_pattern_sec(pos, vel, w, h, max_sec=10000):
    min_sec, min_ent = None, float('inf')
    curr_pos = pos.copy()
    for sec in range(1, max_sec + 1):
        curr_pos = (curr_pos + vel) % [w, h]
        ent = calc_orderness(curr_pos, w, h)
        if ent < min_ent:
            min_sec, min_ent = sec, ent
    return min_sec

def main():
    pos, vel = parse('./inputs/day14_1.txt')
    w, h = 101, 103
    
    # PART 1: After simulating for 100 steps, compute quadrant counts
    final_pos = simulate(pos, vel, w, h, 100)
    print(f"Q1 safe factor: {np.prod(count_quads(final_pos, w, h))}")

    # PART 2: Searching for the time step that yields maximum 'orderness'
    best_sec = find_pattern_sec(pos, vel, w, h)
    print(f"Q2 easter-egg second (max orderness): {best_sec}")

if __name__ == "__main__":
    main()