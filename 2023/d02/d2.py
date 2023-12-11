import re
import numpy as np


with open('./d2_input.txt') as f:
    lines = [lines.rstrip() for lines in f]

rows = []

for i, string in enumerate(lines):
    # Removing the initial part of the string up to the colon
    # Get the game number 
    game_number_match = re.search(r'Game (\d+):', string)
    game_number = int(game_number_match.group(1))
    modified_string = re.sub(r'Game \d+: ', '', string)
    parts = modified_string.split('; ')
    
    for part in parts:
        game_ind = game_number 

        # Finding all numbers and their associated colors
        matches = re.findall(r'(\d+) (red|blue|green)', part)
        red, blue, green = 0, 0, 0
        for value, color in matches:
            if color == 'red':
                red = int(value)
            elif color == 'blue':
                blue = int(value)
            elif color == 'green':
                green = int(value)

        # put them into a array
        rows.append([game_ind, red, green, blue])

table = np.array(rows)        

#### Part 1

mask = (table[:,1] > 12) | (table[:,2] > 13) | (table[:,3] > 14)
bad_table = table[mask]
bad_IDs = np.unique(bad_table[:,0])
IDs = np.unique(table[:,0])  
good_IDs = np.setdiff1d(IDs, bad_IDs)

print(sum(good_IDs))


#### Part 2

power_array = []
for value in IDs:
    rows = table[table[:,0] == value]
    power = np.max(rows[:,1]) * np.max(rows[:,2]) * np.max(rows[:,3])
    power_array.append(power)

power_array = np.array(power_array)
print(sum(power_array))