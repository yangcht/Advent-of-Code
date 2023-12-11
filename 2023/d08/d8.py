import numpy as np
import re
import math
from functools import reduce

def navigate_nodes(starting_node, clean_maps, num_instruction, ending):
    # Initialize the variables
    stop_loop = False
    nodes_list = []
    next_node = starting_node

    # Main loop
    while not stop_loop:
        for left_right in num_instruction:
            nodes_list.append(next_node)
            next_node = clean_maps[clean_maps[:, 0] == next_node][0, left_right]
            if ending == 'Z':
                if next_node[-1] == ending:
                    stop_loop = True
                    nodes_list.append(next_node)
                    break
            elif ending == 'ZZZ':    
                if next_node == 'ZZZ':
                    stop_loop = True
                    nodes_list.append(next_node)
                    break
    # Return the total steps and the list of nodes
    return nodes_list

with open('./d8_input.txt') as f:
    lines = [lines.rstrip() for lines in f]
    
    # convert LR to 1 and 2  
    instruction = lines[0] 
    num_instruction = np.array([1 if char == 'L' else 2 for char in instruction]) 
    #print(num_instruction)
    num_instruction_for_loop = np.tile(num_instruction, 100000)

    # convert the map into a n*3 string array
    pattern = r'[=(),]'
    maps = [re.split(pattern, line) for line in lines[2:]]
    clean_maps = np.array([[element.strip() for element in sublist if element.strip()] for sublist in maps])


#### Part 1

# using the while loop to control the nested iteration 
# initial condtions
path = navigate_nodes('AAA', clean_maps, num_instruction, 'ZZZ')
print(len(path)-1)

#### Part 2

# using the while loop to control the nested iteration 
# initial condtions
stop_loop = False
starting_node = clean_maps[np.vectorize(lambda s: s.endswith('A'))(clean_maps[:, 0])][:,0]
node_cycle = starting_node
end_node = starting_node

all_nodes = [[] for _ in range(len(starting_node))]
second_cycle_node = [[] for _ in range(len(starting_node))]

# calculating the cycle of each starting node:
for i, node in enumerate(starting_node):
    # cycle from **A to **Z
    next_node = navigate_nodes(node, clean_maps, num_instruction_for_loop, 'Z')
    all_nodes[i].append(next_node) 
    end_node[i] = next_node[-1]

# calculating the cycle of each starting node:
for j, node in enumerate(end_node):
    # cycle from **Z to **Z
    second_cycle_node[j].append(navigate_nodes(node, clean_maps, num_instruction_for_loop, 'Z')) 

A_Z_cycle = np.array([len(inner_list) for outer_list in all_nodes for inner_list in outer_list])
Z_Z_cycle = np.array([len(inner_list) for outer_list in second_cycle_node for inner_list in outer_list])

for i in range(len(A_Z_cycle)):
    print('A-Z cycle length:', A_Z_cycle[i] - 1, '|', 'Z-Z cycle length:', Z_Z_cycle[i] - 1)

if A_Z_cycle[0] == Z_Z_cycle[0]:    
    final_cycles = (A_Z_cycle - 1)
else:
    print("something interesting")

# calculate the least common multiple (LCM) of the cycles
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def lcm_of_array(array):
    return reduce(lcm, array)

print(lcm_of_array(final_cycles))