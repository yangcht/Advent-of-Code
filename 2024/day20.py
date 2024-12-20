import sys
from collections import deque
from itertools import combinations


UDLR = [(-1,0),(1,0),(0,-1),(0,1)]

def read_map(filename):
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    return grid

def pos_finds(grid):
    start = end = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)
    return start, end

def path_find(grid, start, end):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False for c in range(cols)] for r in range(rows)]
    parent = [[None for c in range(cols)] for r in range(rows)]
    queue = deque()
    queue.append((start[0], start[1]))
    visited[start[1]][start[0]] = True

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[y][x]
            path.append(start)
            path.reverse()
            return path, len(path)

        for dx, dy in UDLR:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and grid[ny][nx] != '#':
                    visited[ny][nx] = True
                    parent[ny][nx] = (x, y)
                    queue.append((nx, ny))
    return [], float('inf')

def find_cheatable_walls(grid, path):
    walls = set()
    path_set = set(path)
    for idx in range(len(path)-1):
        x, y = path[idx]
        nx, ny = path[idx+1]
        if grid[ny][nx] == '#':
            walls.add((nx, ny))
        for dx, dy in UDLR:
            adj_x, adj_y = x + dx, y + dy
            if 0 <= adj_x < len(grid[0]) and 0 <= adj_y < len(grid):
                if grid[adj_y][adj_x] == '#' and (adj_x, adj_y) not in path_set:
                    walls.add((adj_x, adj_y))
    return walls

def cheating(grid, start, end, cheatable_walls):
    modified_grid = [list(row) for row in grid]
    for wall in cheatable_walls:
        x, y = wall
        modified_grid[y][x] = '.'

    mod_grid = [''.join(row) for row in modified_grid]
    path, time = path_find(mod_grid, start, end)

    return time

def main_p1(file_name, save_s):
    grid = read_map(file_name)
    start, end = pos_finds(grid)
    path, T = path_find(grid, start, end)
    print(f"Shortest path: {T} picoseconds")

    walls_on_path = find_cheatable_walls(grid, path)
    cheat_savings = []
    for wall in walls_on_path:
        T_cheat = cheating(grid, start, end, [wall])
        if T_cheat < float('inf'):
            S = T - T_cheat
            cheat_savings.append(((wall,), S))
    count = 0
    for cheats, saving in cheat_savings:
        if saving >= save_s:
            count +=1

    print(f"Q1: Total number of cheats that save {save_s} picoseconds is {count}")

if __name__ == "__main__":
    main_p1('./inputs/day20_1.txt', 100)