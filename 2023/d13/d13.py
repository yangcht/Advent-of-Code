import numpy as np

def read_array_from_file(file_path):
    with open(file_path, 'r') as f:
        array_str = f.read().strip().split('\n\n')
    arrays = [np.array([list(row) for row in arr.split('\n')]) for arr in array_str]
    return [np.where(arr == '#', 1, 0) for arr in arrays]

ashes_and_rocks = read_array_from_file('./d13_input.txt')

def find_mirror(array):
    for i in range(1, array.shape[0]):
        if i <= array.shape[0] // 2:
            if np.array_equal(array[:i, :], array[i:2*i, :][::-1]): # for the first half
                return i
        else:
            if np.array_equal(array[i:, :], array[2*i-array.shape[0]:i, :][::-1]): # for the second half
                return i
    return None

def find_mirror_smudge(array):
    for i in range(1, array.shape[0]):
        if i <= array.shape[0] // 2:
            diff = array[:i, :] - array[i:2*i, :][::-1]
            if np.count_nonzero(diff) == 1: 
                return i
        else:
            diff = array[i:, :] - array[2*i-array.shape[0]:i, :][::-1]
            if np.count_nonzero(diff) == 1:  
                return i

    return None

def process_arrays(arrays, find_mirror_function):
    summary = 0
    for array in arrays:
        horizontal_result = find_mirror_function(array)
        if horizontal_result is not None:
            summary += 100 * horizontal_result

        vertical_result = find_mirror_function(array.T)
        if vertical_result is not None:
            summary += vertical_result

    return summary
    

#### Part 1
print("part 1: ", process_arrays(ashes_and_rocks, find_mirror))

#### Part 2
print("part 1: ", process_arrays(ashes_and_rocks, find_mirror_smudge))