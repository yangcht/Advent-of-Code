import numpy as np
from itertools import product

def eval_ops(numbers, test_val, operations):
    n = len(numbers)
    for operators in product(operations, repeat=n-1):
        result = numbers[0]
        for i, op in enumerate(operators):
            result = op(result, numbers[i + 1])
        if result == test_val:
            return True
    return False

with open("./inputs/day07_1.txt", 'r') as f:
    cal_eq = [
        (int(test_val.strip()), np.array(list(map(int, nums.split()))))
        for test_val, nums in (line.split(":") for line in f)
    ]

# PART 1: Count calibration results.
valid_test_vals = []
for test_val, numbers in cal_eq:
    if eval_ops(numbers, test_val, [lambda x, y: x + y, lambda x, y: x * y]):
        valid_test_vals.append(test_val)

print(f"Q1 sum: {np.sum(valid_test_vals)}")

# PART 2: Count new calibration results 
valid_test_vals_2 = []
for test_val, numbers in cal_eq:
    if eval_ops(numbers, test_val, [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: int(f"{x}{y}")]):
        valid_test_vals_2.append(test_val)

print(f"Q2 sum: {np.sum(valid_test_vals_2)}")