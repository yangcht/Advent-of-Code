import numpy as np

# reading the input
with open('./d3_input.txt') as f:  
    lines = [lines.rstrip() for lines in f]
    line = [list(line) for line in lines]

engine_array = np.array(line)

#### Part 1

# transform the string arrary in to a integer array
# . = 99 and symbol = -99
def convert_to_int(char):
    if char.isdigit():  
        return int(char)
    elif char == '.':  
        return -11
    else:  
        return -99  
    
vectorized_convert = np.vectorize(convert_to_int)   
integer_array = vectorized_convert(engine_array)   

rows, cols = integer_array.shape 

for i in range(rows):
    end = None
    combined_number = 0
    multiplier = 1
    counter = 0 

    for j in range(cols - 1, -1, -1):
        if integer_array[i,j] >= 0:
            if end is None:
                end = j
            combined_number += integer_array[i, j] * multiplier
            multiplier *= 10
            counter += 1
            integer_array[i, j:end+1] = combined_number
        else:
            combined_number = 0
            multiplier = 1
            end = None
            counter = 0 

rows, cols = integer_array.shape
has_target_neighbor = np.full((rows, cols), False)

for i in range(rows):
    for j in range(cols):
        if integer_array[i, j] == -99:
            has_target_neighbor[i, j] = False
        elif integer_array[i, j] == -11:
            has_target_neighbor[i, j] = False      
        else:
            check_number = 0
            for r in range(max(i - 1, 0), min(i + 2, rows)):
                for c in range(max(j - 1, 0), min(j + 2, cols)):
                    if integer_array[r, c] == -99:
                        has_target_neighbor[i, j] = True

filtered_array = integer_array[has_target_neighbor]

 

clean_array = []
for i, num in enumerate(filtered_array):
    if filtered_array[i] != filtered_array[i - 1]:
        clean_array.append(filtered_array[i])

clean_array = np.array(clean_array)

print(sum(clean_array))


#### Part 2

# transform the string arrary in to a integer array
# . = 99 and symbol = -99, * = -24
def convert_to_int(char):
    if char.isdigit():  
        return int(char)
    elif char == '.':  
        return -11
    elif char == '*':
        return -24
    else:  
        return -99  
    
vectorized_convert = np.vectorize(convert_to_int)   
integer_array = vectorized_convert(engine_array)   

rows, cols = integer_array.shape 

for i in range(rows):
    end = None
    combined_number = 0
    multiplier = 1
    counter = 0 

    for j in range(cols - 1, -1, -1):
        if integer_array[i,j] >= 0:
            if end is None:
                end = j
            combined_number += integer_array[i, j] * multiplier
            multiplier *= 10
            counter += 1
            integer_array[i, j:end+1] = combined_number
        else:
            combined_number = 0
            multiplier = 1
            end = None
            counter = 0 

# print(integer_array)

rows, cols = integer_array.shape
has_target_neighbor = np.full((rows, cols), False)

gear_sum = 0
final_gears = []

for i in range(rows):
    for j in range(cols):
        if integer_array[i, j] == -24:
            check_number = 0
            gear_box = []
            for r in range(max(i - 1, 0), min(i + 2, rows)):
                for c in range(max(j - 1, 0), min(j + 2, cols)):
                    if (integer_array[r, c] != -99) & (integer_array[r, c] != -11) & (integer_array[r, c] != -24):
                        #print(integer_array[r, c])
                        gear_box.append(integer_array[r, c])
            unique_gear_box = np.unique(gear_box)
            if len(unique_gear_box) == 2:
                final_gears.append(unique_gear_box)
                gear_power = np.prod(unique_gear_box)
                #print(unique_gear_box)
                gear_sum += gear_power
                #print(gear_power)


print(gear_sum)