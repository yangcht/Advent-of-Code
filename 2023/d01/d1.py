import numpy as np
import re
 
#### part 1

with open('./d1_input.txt') as f:
    lines = [lines.rstrip() for lines in f]

numbers_sum = 0
numbers_num = 0
num_list = []

for i, string in enumerate(lines):
    numbers_string = ''.join([char for char in string if char.isdigit()])
    numbers_num = int(str(numbers_string[0])) * 10 + int(str(numbers_string[-1]))
    numbers_sum = numbers_sum + numbers_num    
    num_list.append(numbers_num)
    # print(numbers_num)

print(numbers_sum)

#### part 2

with open('./d1_input.txt') as f:
    lines = [lines.rstrip() for lines in f]

patch = {"oonee": "one", "ttwoo": "two", "tthreee": "three", "ffourr": "four", 
"ffivee": "five", "ssixx": "six", "ssevenn": "seven", "eeightt": "eight", "nninee": "nine"}

for key, word in patch.items():
    lines = [line.replace(word, key) for line in lines] 

l_digits = {"1": "one", "2": "two", "3": "three", "4": "four", 
"5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
# Create a pattern that includes both keys and values

for key, word in l_digits.items():
    lines = [line.replace(word, key) for line in lines] 


numbers_sum_2 = 0
numbers_num_2 = 0

num_list_2 = []

for i, string in enumerate(lines):
    numbers_n_2 = ''.join([char for char in string if char.isdigit()])
    numbers_num_2 = int(str(numbers_n_2[0])) * 10 + int(str(numbers_n_2[-1]))
    numbers_sum_2 = numbers_sum_2 + numbers_num_2    
    num_list_2.append(numbers_num_2)

    # print(numbers_num)

print(numbers_sum_2)
