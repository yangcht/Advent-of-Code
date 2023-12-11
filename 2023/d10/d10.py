import numpy as np

with open('./d10_input.txt') as f:
    maze = [[char for char in lines.strip()] for lines in f]
    maze = np.array(maze)

# Just for the visualization    
symbol_map = {'J': '┘', 'L': '└', 'F': '┌', '7': '┐'}
for key, value in symbol_map.items():
    maze[maze == key] = value
            
def show_map(line):           
    for sublist in line:
        print(''.join(sublist))     

viz_maze = np.copy(maze)
direction_maze = np.zeros(maze.shape)
        
# Define movable symbols and their possible directions
movable_symbols = {
    '┘': [(0, -1), (-1, 0)],  # Left or Up
    '└': [(0, 1), (-1, 0)], # Right or Up
    '┌': [(0, 1), (1, 0)],# Right or Down
    '┐': [(0, -1), (1, 0)], # Left or Down
    '|': [(-1, 0), (1, 0)], # Up or Down
    '-': [(0, -1), (0, 1)], # Left or Right
}

highlight = {'┘': '╝', '└': '╚', '┌': '╔', '┐':'╗', '|': '║', '-': '═', 'S': '█'}

pos = np.where(maze == 'S')
current_pos = (pos[0][0], pos[1][0])  

# Starting from S, searching for the start that have to meet the condition
searching = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left and Right

for way in searching:
    next_pos = (current_pos[0] + way[0], current_pos[1] + way[1])
    diff = np.array(current_pos) - np.array(next_pos)
    if maze[next_pos] in movable_symbols and tuple(diff) in movable_symbols[maze[next_pos]]:
        viz_maze[next_pos] = highlight[maze[next_pos]]
        if way[0]!= 0:
            direction_maze[current_pos] = way[0]
        else:
            direction_maze[current_pos] = - diff[0]
        break

found_end = False
n = 0
while found_end == False:
    if tuple(diff) in movable_symbols[maze[next_pos]]:
        next_directions = [d for d in movable_symbols[maze[next_pos]] if tuple(diff) != d]
        if next_directions:
            dx, dy = next_directions[0]
            current_pos = next_pos
            if dx != 0:
                direction_maze[next_pos] = dx  
            else:
                direction_maze[next_pos] = - diff[0]
            next_pos = (next_pos[0] + dx, next_pos[1] + dy)

    diff = np.array(current_pos) - np.array(next_pos)    
    if maze[next_pos] == 'S':
        found_end = True

    viz_maze[next_pos] = highlight[maze[next_pos]]
    n = n + 1        

print(round(n/2))    
show_map(viz_maze)   

#### Part 2

walls = ['╝', '╚', '╔', '╗', '║', '═', '█']

highlighted_array = np.zeros(direction_maze.shape)

highlight = False

for i, row in enumerate(highlighted_array):
    for j, item in enumerate(row):
        if direction_maze[i][j] != 0:
            rotating_direction = int(direction_maze[i][j])
            
for i, row in enumerate(highlighted_array):
    for j, item in enumerate(row):
        if highlight:
            highlighted_array[i][j] = 1

        if direction_maze[i][j] == - rotating_direction:
            highlight = True 
        if direction_maze[i][j] == rotating_direction:
            highlight = False

for i, row in enumerate(highlighted_array):
    for j, item in enumerate(row):
        if viz_maze[i][j] in walls:
            highlighted_array[i][j] = 0

print(round(np.sum(highlighted_array)))    