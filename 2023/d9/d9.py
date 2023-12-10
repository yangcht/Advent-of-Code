import numpy as np
from scipy.interpolate import BarycentricInterpolator

with open('./d9_input.txt') as f:
    line = [lines.split() for lines in [lines.rstrip() for lines in f]]
    num_line = [[int(item) for item in sublist] for sublist in line]

def extrapolate_and_sum(num_list, reverse=False):
    sum_extrapolated_values = 0

    for line in num_list:
        if reverse:
            line = line[::-1]
        interpolator = BarycentricInterpolator(np.arange(len(line)), np.array(line))
        x_values = np.linspace(0, len(line), len(line))
        y_values = interpolator(x_values)
        sum_extrapolated_values += y_values[-1]

    return round(sum_extrapolated_values)

#### Part 1
print(extrapolate_and_sum(num_line))

#### Part 2
print(extrapolate_and_sum(num_line, reverse=True))
