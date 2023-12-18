import numpy as np
import matplotlib.pyplot as plt

def read_dig_plan(file_path):
    with open(file_path) as f:
        return [line.strip().split()[:2] + [line.strip().split()[2].strip('()')] for line in f]

def dig_map(dig_plan):
    directions = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
    position = (0, 0)
    return [(position := (position[0] + directions[d][0], position[1] + directions[d][1]), c, d) 
            for d, dist, c in dig_plan for _ in range(int(dist))]

def create_3d_grid(grid):
    min_x, max_x = min(x for (x, _), *_ in grid), max(x for (x, _), *_ in grid)
    min_y, max_y = min(y for (_, y), *_ in grid), max(y for (_, y), *_ in grid)
    grid_shape = (max_x - min_x + 1, max_y - min_y + 1)
    image_grid = np.full((*grid_shape, 3), '#ffffff', dtype=object)

    for i, ((x, y), color, direction) in enumerate(grid):
        next_direction = grid[i + 1][2] if i + 1 < len(grid) else ''
        image_grid[x - min_x, y - min_y, :] = [color, direction, next_direction]

    return image_grid

def fill_interior_3d(image_grid):
    filled_grid = np.copy(image_grid)
    rows, cols = filled_grid.shape[:2]

    for x in range(rows):
        fill = False
        for y in range(cols):
            color, current_dir, next_dir = filled_grid[x, y]
            if (current_dir, next_dir) in [('U', 'U'), ('R', 'U'), ('U', 'L'), ('L', 'U')]:
                fill = True
            elif (current_dir, next_dir) in [('D', 'D'), ('R', 'D'), ('D', 'L'), ('L', 'D')]:
                fill = False
            if fill and color == '#ffffff': 
                filled_grid[x, y, 0] = '#ffff00'

    return filled_grid

def plot_grid_3d(image_grid, save_path='d18_output.pdf', dpi=300):
    rows, cols = image_grid.shape[:2]
    rgb_grid = np.zeros((rows, cols, 3), dtype=np.uint8)

    for x in range(rows):
        for y in range(cols):
            color = image_grid[x, y, 0]
            if color:
                rgb_grid[x, y] = np.array([int(color[i:i+2], 16) for i in (1, 3, 5)])

    with plt.style.context('ggplot'):
        fig, ax = plt.subplots(figsize=(10, 10), dpi=dpi)
        ax.imshow(rgb_grid, aspect='auto')
        ax.axis('off')
        plt.savefig(save_path, format='pdf', bbox_inches='tight', dpi=dpi)
        plt.show()

def count_colored_pixels(image_grid):
    return np.count_nonzero(image_grid[:, :, 0] != '#ffffff')

#### Part 1
grid = dig_map(read_dig_plan('./d18_input.txt'))

image_3d_grid = create_3d_grid(grid)
filled_image_3d_grid = fill_interior_3d(image_3d_grid)
plot_grid_3d(filled_image_3d_grid)
total_colored_pixels = count_colored_pixels(filled_image_3d_grid)
print(f"Part 1 = {total_colored_pixels}")