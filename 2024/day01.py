import numpy as np
from collections import Counter

a, b = np.loadtxt('./inputs/day01_1.txt', usecols=(0, 1), unpack=True)

### PART 1: Sum of Absolute Differences Between Sorted Lists
sum_distances = np.sum(np.abs(np.sort(a) - np.sort(b)))
print("Sum of distances:", sum_distances)

### PART 2: Sum of (Element * Number of Matches in Second List)

# Count the occurrences of each element in list b
count_b = Counter(b)

# For each element in a, get the count from b and multiply by the element
sum_similarity = np.sum(a * np.array([count_b[elem] for elem in a]))
print("Sum of similarity score:", sum_similarity)