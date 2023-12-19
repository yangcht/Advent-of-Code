import numpy as np
import itertools
import time
from multiprocessing import Pool

def process_row(np_pattern, spring_code_row, string_combinations):
    mask = np_pattern != '?'
    matching_rows_mask = np.all((string_combinations[:, mask] == np_pattern[mask]) | (np_pattern[mask] == '?'), axis=1)
    matching_rows = string_combinations[matching_rows_mask]

    matching_counts_per_row = 0
    for row in matching_rows:
        count = 0
        counts = []
        for char in row:
            if char == '#':
                count += 1
            elif char == '.' and count > 0:
                counts.append(count)
                count = 0 
        if count > 0:
            counts.append(count)        

        if counts == spring_code_row:
            matching_counts_per_row += 1           

    return matching_counts_per_row

def main():
    symbols = ['#', '.', "?"]
    spring_map = []
    spring_code = []

    with open('./d12_input.txt') as f:
        for line in f:
            parts = line.strip().split()
            spring_map.append([char for char in parts[0] if char in symbols])
            spring_code.append([int(num) for num in parts[1].split(',')])

    max_len = max([len(row) for row in spring_map])
    filled_spring_map = np.array([row + ['.'] * (max_len - len(row)) for row in spring_map])

    combinations = itertools.product(symbols[:2], repeat=max_len)
    string_combinations = np.array([[char for char in ''.join(comb)] for comb in combinations])

    start_time = time.time()

    with Pool() as pool:
        all_matching_counts = pool.starmap(process_row, [(row, code, string_combinations) for row, code in zip(filled_spring_map, spring_code)])

    print(sum(all_matching_counts))

    end_time = time.time() 
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == '__main__':
    main()
