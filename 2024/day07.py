import numpy as np
from itertools import product
from concurrent.futures import ProcessPoolExecutor

def eval_op(numbers, target_value, operators):
    for ops in product(operators, repeat=len(numbers) - 1):
        result = numbers[0]
        for i, op in enumerate(ops):
            result = op(result, numbers[i + 1])
        if result == target_value:
            return True
    return False

def ops_part1(args):
    target_value, numbers = args
    operations = [
        lambda x, y: x + y,
        lambda x, y: x * y
    ]
    return target_value if eval_op(numbers, target_value, operations) else 0

def ops_part2(args):
    target_value, numbers = args
    operations = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        lambda x, y: int(f"{x}{y}")
    ]
    return target_value if eval_op(numbers, target_value, operations) else 0

if __name__ == "__main__":
    input_file = "./inputs/day07_1.txt"
    calibration_data = []

    with open(input_file, "r") as f:
        for line in f:
            target, nums = line.strip().split(":")
            target_value = int(target)
            numbers = list(map(int, nums.split()))
            calibration_data.append((target_value, numbers))

    with ProcessPoolExecutor() as executor:
        part1_results = list(executor.map(ops_part1, calibration_data))
    print("Q1 sum:", np.sum(part1_results))

    with ProcessPoolExecutor() as executor:
        part2_results = list(executor.map(ops_part2, calibration_data))
    print("Q2 sum:", np.sum(part2_results))
