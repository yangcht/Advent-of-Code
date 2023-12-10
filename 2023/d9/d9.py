import numpy as np
from scipy.interpolate import BarycentricInterpolator

with open('./d9_input.txt') as f:
    line = [lines.split() for lines in [lines.rstrip() for lines in f]]
    num_line = [[int(item) for item in sublist] for sublist in line]

#### Part 1
extrapolated_values = []

for i, line in enumerate(num_line):

    interpolator = BarycentricInterpolator(np.arange(len(line)), np.array(line))
    x_values = np.linspace(0, len(line), len(line))
    y_values = interpolator(x_values)
    extrapolated_values.append(y_values[-1])

print("Sum of extrapolated values:", round(sum(extrapolated_values)))


#### Part 2
extrapolated_values_reverse = []

for i, line in enumerate(num_line):
    interpolator = BarycentricInterpolator(np.arange(len(line)), np.array(line)[::-1])
    x_values = np.linspace(0, len(line), len(line))
    y_values = interpolator(x_values)
    extrapolated_values_reverse.append(y_values[-1])

print("Sum of extrapolated values:", round(sum(extrapolated_values_reverse)))