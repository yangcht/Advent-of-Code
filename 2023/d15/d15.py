import numpy as np

def read_array_from_file(file_path):
    return np.genfromtxt(file_path, delimiter=',', dtype=str)


def read_label_operation_lens(file_path):
    with open(file_path, 'r') as f:
        steps = f.read().strip().split(',')

    return np.array([[step.split(op)[0], op, step.split(op)[1] if op in step else ''] 
            for step in steps 
            for op in ['=', '-'] if op in step])


def HASH_algorithm(a):
    num = 0
    for i, char in enumerate(a):
        num = ((num + ord(char)) * 17) % 256
    return num


def HASH_MAP(label, operation, focal_length, boxes):
    box_num = HASH_algorithm(label)
    if operation == '=':
        focal_length = int(focal_length)
        lens = (label, focal_length)
        boxes[box_num] = [lens if l[0] == label else l for l in boxes[box_num]]
        if all(l[0] != label for l in boxes[box_num]):
            boxes[box_num].append(lens)
    elif operation == '-':
        boxes[box_num] = [l for l in boxes[box_num] if l[0] != label]


#### Part 1
input_list = read_array_from_file('./d15_input.txt')
vectorized_hash = np.vectorize(HASH_algorithm)
part1_result = vectorized_hash(input_list)
print("Part 1 = ", sum(part1_result))


#### Part 2
LoL = read_label_operation_lens('./d15_input.txt')
uniqe_labels = np.array([np.unique(LoL[:,0])]) 
boxes = {i: [] for i in range(256)}

for label, operation, focal_length in LoL:
    HASH_MAP(label, operation, focal_length, boxes)

total_focusing_power = sum((box_index + 1) * (slot_index + 1) * int(focal_length) 
                            for box_index, lenses in boxes.items() 
                            for slot_index, (_, focal_length) in enumerate(lenses))

print("Part 2 = ", total_focusing_power)