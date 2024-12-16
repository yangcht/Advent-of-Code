from bisect import insort
import numpy as np

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
    queue, visited = [(0, start_x, start_y, 0)], np.zeros((len(maze), len(maze[0]), 4), dtype=bool)

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

if __name__ == "__main__":

    score = find_lowest_score("./inputs/day16_1.txt")
    print(f"Q1 lowest score: {score}")
