import numpy as np
import matplotlib.pyplot as plt
from heapq import heappush, heappop

def read_contraption(file_path):
    with open(file_path) as f:
        return np.array([[int(char) for char in line.strip()] for line in f])


def dijkstra_search(grid, start, end, min_step_before_turn, max_consecutive_steps):
    h, w = grid.shape
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = {}  
    queue = [(0, start, -1, 0, [start])]  

    while queue:
        loss, pos, d, dc, path = heappop(queue)
        if pos == end:
            return loss, path

        allowed_dirs = [_d for _d in range(4) if _d != d and (_d + 2) % 4 != d]

        for _d in allowed_dirs:
            for d_cont in range(min_step_before_turn, max_consecutive_steps + 1):
                _next_pos = (pos[0] + dirs[_d][0] * d_cont, pos[1] + dirs[_d][1] * d_cont)
                if 0 <= _next_pos[0] < h and 0 <= _next_pos[1] < w:
                    _next_loss = loss
                    _next_path = list(path)
                    valid_step = True
                    for i in range(d_cont):
                        step_pos = (pos[0] + dirs[_d][0] * i, pos[1] + dirs[_d][1] * i)
                        if 0 <= step_pos[0] < h and 0 <= step_pos[1] < w:
                            _next_loss += grid[step_pos]
                            _next_path.append(step_pos)
                        else:
                            valid_step = False
                            break

                    if valid_step and _next_loss < visited.get((_next_pos, _d), (float("inf"), []))[0]:
                        visited[(_next_pos, _d)] = (_next_loss, _next_path)
                        heappush(queue, (_next_loss, _next_pos, _d, d_cont, _next_path))

    return None, []  


def plot_path(grid, path):
    plt.figure(figsize=(15, 12)) 
    plt.imshow(grid, cmap='gist_earth', interpolation='nearest')
    plt.colorbar()
    if path:
        x, y = zip(*path)
        plt.plot(y, x, color="#96231b", linewidth=1, marker='o', markersize=3, 
                markerfacecolor='yellow', markeredgecolor='#96231b')

    plt.show()

traffic_map = read_contraption('./d17_input.txt')
start = (0, 0)
end = (len(traffic_map) - 1, len(traffic_map[0]) - 1)

#### Part 1
min_heat_loss, path = dijkstra_search(traffic_map, start, end, 1, 3)
print("Part 1 = ", min_heat_loss)
plot_path(traffic_map, path)

#### Part 2
min_heat_loss_2, path_2 = dijkstra_search(traffic_map, start, end, 4, 10)
print("Part 1 = ", min_heat_loss_2)
plot_path(traffic_map, path_2)