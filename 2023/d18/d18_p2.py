import re

def read_dig_plan(file_path):
    dir_dict = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    pattern = re.compile(r'\(#([0-9a-f]{5})([0-3])\)')
    with open(file_path, 'r') as file:
        return [(dir_dict[match.group(2)], int(match.group(1), 16)) for line in file if (match := pattern.search(line))]


def calculate_lagoon_area(dig_plan):
    x, y, area, perimeter = 0, 0, 0, 0
    vertices = [(x, y)]

    for direction, distance in dig_plan:
        x += distance if direction == 'R' else -distance if direction == 'L' else 0
        y += distance if direction == 'D' else -distance if direction == 'U' else 0
        vertices.append((x, y))
        perimeter += distance

    n = len(vertices) 
    for i in range(n):
        j = (i + 1) % n
        # Shoelace Formula
        area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]

    return abs(area) // 2 + perimeter // 2 + 1


dig_plan = read_dig_plan('d18_input.txt')
print(f"Part 2 = {calculate_lagoon_area(dig_plan)}")