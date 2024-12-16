from bisect import insort
import numpy as np
from copy import deepcopy
from collections import deque

def parse_maze(file_path):
    with open(file_path, 'r') as file:
        maze = [list(line.strip()) for line in file]
    start, end = [(x, y)
                  for y, row in enumerate(maze)
                  for x, cell in enumerate(row)
                  if cell in "SE"]
    return maze, start, end

def get_neighbors(x, y, direction, maze):
    DIR = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    dx, dy = DIR[direction]
    if 0 <= y + dy < len(maze) and 0 <= x + dx < len(maze[0]) and maze[y + dy][x + dx] != '#':
        yield x + dx, y + dy, direction, 1
    for turn_cost, turn_dir in [(1000, 1), (1000, -1)]:
        yield x, y, (direction + turn_dir) % 4, turn_cost

def find_lowest_score(file_path):
    maze, (start_x, start_y), (end_x, end_y) = parse_maze(file_path)
    queue, visited = [(0, start_x, start_y, d) for d in range(4)], np.zeros((len(maze), len(maze[0]), 4), dtype=bool)
    queue.sort()

    while queue:
        cost, x, y, direction = queue.pop(0)
        if visited[y, x, direction]:
            continue
        visited[y, x, direction] = True
        if (x, y) == (end_x, end_y):
            return cost
        for next_x, next_y, next_dir, move_cost in get_neighbors(x, y, direction, maze):
            if not visited[next_y, next_x, next_dir]:
                insort(queue, (cost + move_cost, next_x, next_y, next_dir))
    return -1

def find_all_shortest_paths(file_path):
    maze, (start_x, start_y), (end_x, end_y) = parse_maze(file_path)
    min_cost = find_lowest_score(file_path)
    queue = deque()

    for direction in range(4):
        queue.append((start_x, start_y, direction, 0, [(start_x, start_y)]))

    all_paths = []
    visited = {}
    while queue:
        x, y, direction, cost, path = queue.popleft()
        if cost > min_cost:
            continue
        if (x, y) == (end_x, end_y) and cost == min_cost:
            all_paths.append(path)
            continue
        for next_x, next_y, next_dir, move_cost in get_neighbors(x, y, direction, maze):
            new_cost = cost + move_cost
            if new_cost > min_cost:
                continue
            state = (next_x, next_y, next_dir)
            if state in visited:
                if new_cost > visited[state]:
                    continue
            visited[state] = new_cost
            new_path = path + [(next_x, next_y)]
            queue.append((next_x, next_y, next_dir, new_cost, new_path))

    return all_paths

def calculate_tiles(file_path):
    shortest_paths = find_all_shortest_paths(file_path)
    maze, _, _ = parse_maze(file_path)
    unique_matrix = np.zeros((len(maze), len(maze[0])), dtype=int)
    for path in shortest_paths:
        x_coords, y_coords = zip(*path)
        unique_matrix[y_coords, x_coords] = 1
    return len(shortest_paths), unique_matrix.sum()

if __name__ == "__main__":

    score = find_lowest_score("./inputs/day16_1.txt")
    print(f"Q1 lowest score: {score}")

    num_path, total_tiles = calculate_tiles("./inputs/day16_1.txt")
    print(f"Q2: {total_tiles} unique tiles from {num_path} shortest paths")
