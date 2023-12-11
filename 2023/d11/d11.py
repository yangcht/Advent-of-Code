import numpy as np

with open('./d11_input.txt') as f:
    sky_map = np.array([list(line.strip()) for line in f])

empty_row = np.where(~np.any(sky_map == '#', axis=1))[0]       
empty_col = np.where(~np.any(sky_map == '#', axis=0))[0] 
y_gal, x_gal = np.argwhere(sky_map == '#').T

shortest_path = []
expansion_factor = []

for i, x_value in enumerate(x_gal):
    for j in range(i + 1, len(x_gal)):
        distance = abs(x_gal[i] - x_gal[j]) + abs(y_gal[i] - y_gal[j])
        expanding_row = 0
        expanding_col = 0
        for row in empty_row:
            if row in range(min(y_gal[i], y_gal[j]), max(y_gal[i], y_gal[j]) + 1):
                expanding_row = expanding_row + 1
        for col in empty_col:
            if col in range(min(x_gal[i], x_gal[j]), max(x_gal[i], x_gal[j]) + 1):
                expanding_col = expanding_col + 1

        expansion_factor.append(expanding_row + expanding_col)
        shortest_path.append(distance)

shortest_path = np.array(shortest_path)
expansion_factor = np.array(expansion_factor)

#### Part 1
factor = 2
print(sum(shortest_path + (factor-1) * (expansion_factor)))

#### Part 2
factor = 1000000
print(sum(shortest_path + (factor-1) * (expansion_factor)))