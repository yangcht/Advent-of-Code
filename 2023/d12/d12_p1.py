import numpy as np
import time

def read_input(file_path):
    spring_map = []
    spring_code = []
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split()
            spring_map.append(parts[0])
            spring_code.append([int(num) for num in parts[1].split(',')])
    return spring_map, spring_code

def generate_combinations(pattern, memo):
    if pattern in memo:
        return memo[pattern]

    if '?' not in pattern:
        memo[pattern] = [pattern]
        return memo[pattern]

    results = []
    question_mark_index = pattern.find('?')
    for symbol in ['#', '.']:
        new_pattern = pattern[:question_mark_index] + symbol + pattern[question_mark_index + 1:]
        results.extend(generate_combinations(new_pattern, memo))

    memo[pattern] = results
    return results

def count_hashes(sequence):
    counts = []
    count = 0
    for char in sequence:
        if char == '#':
            count += 1
        elif char == '.':
            if count > 0:
                counts.append(count)
                count = 0
    if count > 0:
        counts.append(count)
    return counts

def main():
    spring_map, spring_code = read_input('./d12_input.txt')
    memo = {}
    total_matching_counts = 0

    start_time = time.time()

    for row, code in zip(spring_map, spring_code):
        matching_counts = 0
        for combination in generate_combinations(row, memo):
            if count_hashes(combination) == code:
                matching_counts += 1
        total_matching_counts += matching_counts

    print(total_matching_counts)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
