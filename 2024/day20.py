from itertools import product
import heapq

def read_map(filename):
    return [list(line.strip()) for line in open(filename)]

def find_st_ed(grid):
    st = ed = None
    free_pos = {(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell in ".SE"}
    for x, y in free_pos:
        if grid[y][x] == "S": st = (x, y)
        if grid[y][x] == "E": ed = (x, y)
    return st, ed, free_pos

def dijkstra(st, free_pos):
    to_visit = [(0, st)]
    visited = {st: 0}
    while to_visit:
        score, (cx, cy) = heapq.heappop(to_visit)
        if visited.get((cx, cy), float('inf')) < score: continue
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            np = (cx + dx, cy + dy)
            if np in free_pos and (np not in visited or visited[np] > score + 1):
                visited[np] = score + 1
                heapq.heappush(to_visit, (score + 1, np))
    return visited

def get_cheats(dist, cheat_steps):
    return sum(
        1 for p in dist for dx, dy in product(range(-cheat_steps, cheat_steps + 1), repeat=2)
        if (dx or dy) and abs(dx) + abs(dy) <= cheat_steps and
           (np := (p[0] + dx, p[1] + dy)) in dist and
           dist[p] - dist[np] - (abs(dx) + abs(dy)) >= 100
    )

def run_cheats(file, cheat_allowance):
    grid = read_map(file)
    start, _, free_space = find_st_ed(grid)
    return get_cheats(dijkstra(start, free_space), cheat_allowance)

if __name__ == "__main__":
    file = "./inputs/day20_1.txt"
    print(f"Q1: The possible cheats are {run_cheats(file, 2)}")
    print(f"Q2: The possible chates are {run_cheats(file, 20)}")