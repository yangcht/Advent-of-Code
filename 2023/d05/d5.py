import numpy as np

#### Part 1

with open('d5_input.txt', 'r') as file:
    text = file.read().split('\n\n')

seeds = np.array(list(map(int, text[0].split(':')[1].split())), dtype=np.int64)

maps = ["seed_to_soil_map", "soil_to_fertilizer_map", "fertilizer_to_water_map", 
        "water_to_light_map", "light_to_temperature_map", "temperature_to_humidity_map", 
        "humidity_to_location_map"]

data_for_maps = {}
final_map = {key: None for key in maps}

final_location = []
seed_transformation = []

for i, seed in enumerate(seeds): # looping over each seed
    for i, map_name in enumerate(maps, 1):
        data_for_maps[map_name] = [list(map(int, row.split())) for row in text[i].split('\n', 1)[1].split('\n')]
            # looping over each map_data
        for j in range(len(data_for_maps[map_name])):
            maps_num = data_for_maps[map_name][j] # maps_num[1] = src , maps_num[0] = destination
            if (seed >= maps_num[1]) and (seed <= maps_num[1] + maps_num[2]):
                seed = seed - maps_num[1] + maps_num[0]    
                break
            else:
                pass    
        seed_transformation.append(seed)

    final_location.append(seed)

print(min(final_location))              


#### Part 2

def read_file(filename):
    with open(filename, 'r') as file:
        text = file.read().split('\n\n')

    seeds = np.array(text[0].split(':')[1].split(), dtype=np.int64)
    real_seeds, seeds_range = seeds[::2], seeds[1::2]

    maps = [
        "seed_to_soil_map", "soil_to_fertilizer_map", "fertilizer_to_water_map",
        "water_to_light_map", "light_to_temperature_map", "temperature_to_humidity_map",
        "humidity_to_location_map"
    ]

    data_for_maps = {}
    for i, map_name in enumerate(maps):
        map_data = []
        for row in text[i+1].split('\n'):
            try:
                map_data.append(list(map(int, row.split())))
            except ValueError:
                continue
        data_for_maps[map_name] = np.array(map_data, dtype=np.int64)

    return real_seeds, seeds_range, data_for_maps, maps

def transform_location(loc, maps, data_for_maps):
    for map_name in reversed(maps):
        for src, dest, length in data_for_maps[map_name]:
            if src <= loc < src + length:
                loc = loc - src + dest
                break
    return loc

def find_smallest_location(real_seeds, seeds_range, data_for_maps, maps):
    j = 0
    while j < 10000000000:  # A large number, you might want to adjust this based on your data
        transformed_loc = transform_location(j, maps, data_for_maps)
        
        for seed, length in zip(real_seeds, seeds_range):
            if seed <= transformed_loc < seed + length:
                return j  # Return immediately once a match is found
            else:
                pass 
        j += 1  # Increment the location to check
        #print(j)
    return -1  # Indicates no location found within the range

# Read file and process
filename = 'd5_input.txt'  # Replace with your actual file name

real_seeds, seeds_range, data_for_maps, maps = read_file(filename)
smallest_loc = find_smallest_location(real_seeds, seeds_range, data_for_maps, maps)
print(smallest_loc)