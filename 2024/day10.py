import numpy as np
from collections import deque

DIR = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def read_f(f):
    with open(f, 'r') as f:
        data = [list(map(int, line.strip())) for line in f if line.strip()]
    return np.array(data)

def get_pos(data, n):
    return np.argwhere(data == n)

def bfs(m, s, e, dr):
    q, seen = deque([s]), {s}
    while q:
        x, y = q.popleft()
        if (x, y) not in e:
            for dx, dy in dr:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m.shape[0] and 0 <= ny < m.shape[1] and (nx, ny) not in seen and m[nx, ny] == m[x, y] + 1:
                    q.append((nx, ny))
                    seen.add((nx, ny))
    return len(seen & e)

def score_sum(m):
    s = get_pos(m, 0)
    e = set(map(tuple, get_pos(m, 9)))
    t = 0
    for st in s:
        t += bfs(m, tuple(st), e, DIR)
    return t

def rating_sum(m):
    p = (m == 9).astype(np.int64)
    for h in range(8, -1, -1):
        for x, y in zip(*np.where(m == h)):
            p[x, y] = sum(
                p[nx, ny]
                for dx, dy in DIR
                if 0 <= (nx := x + dx) < m.shape[0] and
                   0 <= (ny := y + dy) < m.shape[1] and
                   m[nx, ny] == h + 1
            )
    return p[m == 0].sum()

if __name__ == "__main__":
    hike_map = read_f('./inputs/day10_1.txt')

    #PART 1: Score of unique 0 -> unique 9
    print(f"Q1 sum: {score_sum(hike_map)}")
    #PART 2: Rating of unique 0->9
    print(f"Q2 sum: {rating_sum(hike_map)}")
