import re
import numpy as np

def read_map(file):
    with open(file, 'r') as f:
        arr = np.array([list(line.rstrip('\n')) for line in f])
    return arr

def valid_pos(arr, r, c):
    return 0 <= r < arr.shape[0] and 0 <= c < arr.shape[1]

def find_antennas(arr):
    ants = {}
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            if arr[r, c].isalnum():
                freq = arr[r, c]
                ants.setdefault(freq, []).append((r, c))
    return ants

def generate_pairs(coords):
    sorted_coords = sorted(coords, key=lambda x: (x[0], x[1]))
    for i in range(len(sorted_coords)):
        for j in range(i + 1, len(sorted_coords)):
            yield sorted_coords[i], sorted_coords[j]

def find_antinodes(arr, antennas, limit_k=True):
    antinode_positions = set()
    for freq, coords in antennas.items():
        if len(coords) < 2:
            continue

        antinode_positions.update(coords)

        for (m, n), (i, j) in generate_pairs(coords):
            for r, c in coords:
                if (r, c) != (m, n) and (r, c) != (i, j):
                    if (r - m) * (j - n) == (i - m) * (c - n):
                        antinode_positions.add((r, c))
            k = 1
            while True:
                r1 = (k + 1) * i - k * m
                c1 = (k + 1) * j - k * n

                r2 = (k + 1) * m - k * i
                c2 = (k + 1) * n - k * j

                if not valid_pos(arr, r1, c1) and not valid_pos(arr, r2, c2):
                    break

                if valid_pos(arr, r1, c1):
                    antinode_positions.add((r1, c1))

                if valid_pos(arr, r2, c2):
                    antinode_positions.add((r2, c2))
                
                if limit_k:
                    break
                
                k += 1

    return antinode_positions

def main():
    arr = read_map('./inputs/day08_1.txt')
    antennas = find_antennas(arr)

    #PART 1: Find antinodes with distance * 1
    antinodes_1 = find_antinodes(arr, antennas, limit_k=True)
    print(f"Q1 sum: {len(antinodes_1)}")

    #PART 2: Find antinodes with distance * k
    antinodes_2 = find_antinodes(arr, antennas, limit_k=False)
    print(f"Q2 sum: {len(antinodes_2)}")


if __name__ == "__main__":
    main()
