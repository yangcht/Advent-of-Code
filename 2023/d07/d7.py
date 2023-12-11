import numpy as np

#### Part 1

conversion_dict = {'A': 'F', 'K': 'E', 'Q': 'D', 'J': 'C', 'T': 'B'}

def check_type(s):

    s_s = ''.join(sorted(s))

    if len(set(s_s)) == 1:
        return '7'  # Five of a kind
    elif len(set(s_s)) == 2:
        if s_s[0] == s_s[1] == s_s[2] == s_s[3] or s_s[1] == s_s[2] == s_s[3] == s_s[4]:
            return '6'  # Four of a kind
        else:
            return '5'  # Full house
    elif len(set(s_s)) == 3:
        if s_s[0] == s_s[1] == s_s[2] or s_s[1] == s_s[2] == s_s[3] or s_s[2] == s_s[3] == s_s[4]:
            return '4'  # Three of a kind
        else:
            return '3'  # Two pair 
    elif len(set(s_s)) == 4:
        return '2'  # One pair
    else:
        return '1'  # High card    

# reading the input
with open('./d7_input.txt') as f:  
    lines = [lines.rstrip().split() for lines in f]    

new_cards_and_points = []

for line in lines:
    points = check_type(line[0])
    new_cards_and_points.append([points + ''.join(conversion_dict.get(c, c) for c in line[0]), line[1]])

# using lexicographical sorting
sorted_list = sorted(new_cards_and_points, key=lambda x: x[0]) 

sorted_score = [int(sublist[1]) for sublist in sorted_list]
winning_number = [i for i in range(1, len(sorted_list) + 1)]
print(sum(np.multiply(sorted_score, winning_number)))


#### Part 2

conversion_dict = {'A': 'F', 'K': 'E', 'Q': 'D', 'T': 'B', 'J': '0'}

def check_type_with_J(s):
    # now need to consider additional situation when there is a 0(J)
    s_s = ''.join(sorted(s))

    if len(set(s_s)) == 1:
        return '7'  # Five of a kind
    elif len(set(s_s)) == 2:
        if s_s[0] == s_s[1] == s_s[2] == s_s[3] or s_s[1] == s_s[2] == s_s[3] == s_s[4]:
            if any(element == 'J' for element in s_s):
                return '7'  # Four of a kind with 0 -> Five of a kind
            else:
                return '6'  # Four of a kind
        else:
            if any(element == 'J' for element in s_s):
                return '7'  # Full house with 0 -> Five of a kind
            else:
                return '5'  # Full house
    elif len(set(s_s)) == 3:
        if (s_s[0] == s_s[1] == s_s[2]) or (s_s[1] == s_s[2] == s_s[3]) or (s_s[2] == s_s[3] == s_s[4]):
            if any(element == 'J' for element in s_s):
                return '6' # Three of a kind with 0 -> Four of a kind
            else:
                return '4'  # Three of a kind with two 0
        else:
            if sum(element == 'J' for element in s_s) == 2:
                return '6' # Two pair with two 0 --> Four of a kind
            if sum(element == 'J' for element in s_s) == 1:
                return '5' # Two pair with a single 0 --> Full house
            else:
                return '3'  # Two pair 
    elif len(set(s_s)) == 4:
        if any(element == 'J' for element in s_s):
            return '4' # One pair with 0 --> Three of a kind
        else:
            return '2'  # One pair
    elif len(set(s_s)) == 5:
        if any(element == 'J' for element in s_s):
            return '2'  # High card with 0 --> One pair
        else:
            return '1'  # High card    
    else:
        print("Error")    


# reading the input
with open('./d7_input.txt') as f:  
    lines = [lines.rstrip().split() for lines in f]    

new_cards_and_points = []

for line in lines:
    points = check_type_with_J(line[0])
    new_cards_and_points.append([points + ''.join(conversion_dict.get(c, c) for c in line[0]), line[1]])

# using lexicographical sorting
sorted_list = sorted(new_cards_and_points, key=lambda x: x[0]) 

sorted_score = [int(sublist[1]) for sublist in sorted_list]
winning_number = [i for i in range(1, len(sorted_list) + 1)]
print(sum(np.multiply(sorted_score, winning_number)))