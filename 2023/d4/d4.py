# reading the input

numbers = []

with open('./d4_input.txt') as f: 
    for lines in f:
        line = lines.rstrip() 
        _, numbers_line = line.split(":")
        winning_numbers, my_numbers = numbers_line.split("|")
        winning_num = [int(num) for num in winning_numbers.split()]
        my_num = [int(num) for num in my_numbers.split()]
        numbers.append([winning_num, my_num])

#### Part 1

points_per_card = []
my_winning_numbers = []
matching_card_numbers = []

for m in range(len(numbers)):
    power_of_two = 0
    points = 0
    for i in range(len(numbers[0][1])): # looping over my numbers
        for j in range(len(numbers[m][0])):
            if numbers[m][1][i] == numbers[m][0][j]:
                switch_to_points = 1
                power_of_two += 1
                my_winning_numbers.append(numbers[m][1][i])
                points = switch_to_points * 2**(power_of_two-1) 
                switch_to_points = 0
    matching_card_numbers.append(power_of_two)            
    #print(points)            
    points_per_card.append(points)

print(sum(points_per_card))    


#### Part 2

card_numbers = [1] * len(matching_card_numbers)

for n, matching_number in enumerate(matching_card_numbers):
    #print(n, matching_number, card_numbers)
    for i in range(matching_number):
        card_numbers[n+i+1] = card_numbers[n+i+1] + card_numbers[n]
        
print(sum(card_numbers))