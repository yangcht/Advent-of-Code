import numpy as np

# reading the input
with open('./d6_input.txt') as f:  
    lines = [lines.rstrip() for lines in f]

#### Part 1

time = np.array(lines[0].split(':')[1].split(), dtype=np.int64)
dist = np.array(lines[1].split(':')[1].split(), dtype=np.int64)

ways_to_win = []

for time, dist in zip(time, dist):
    time_arrays = np.arange(0, time+1)
    results = [x for x in time_arrays if (time - x) * x > dist]
    ways_to_win.append(len(results))

print(np.prod(ways_to_win))


#### Part 2

time = np.array(int(lines[0].split(':')[1].replace(" ","")), dtype=np.int64)
dist = np.array(int(lines[1].split(':')[1].replace(" ","")), dtype=np.int64)

time_arrays = np.arange(0, time+1)
results = [x for x in time_arrays if (time - x) * x > dist]

print(len(results))
