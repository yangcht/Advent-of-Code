using DelimitedFiles

#### Part 1

text = split(read("d5_input.txt", String), "\n\n")

seeds = parse.(Int64, split(split(text[1], ':')[2]))

maps = ["seed_to_soil_map", "soil_to_fertilizer_map", "fertilizer_to_water_map", 
        "water_to_light_map", "light_to_temperature_map", "temperature_to_humidity_map", 
        "humidity_to_location_map"]

data_for_maps = Dict()
final_map = Dict((key, nothing) for key in maps)

final_location = []
seed_transformation = []

for (i, seed) in enumerate(seeds) # Looping over each seed
    for (i, map_name) in enumerate(maps)
        rows = split(split(text[i+1], '\n', limit=2)[2], '\n')
        data_for_maps[map_name] = [parse.(Int, split(row)) for row in rows]
        # Looping over each map_data
        for maps_num in data_for_maps[map_name]
            if seed >= maps_num[2] && seed <= maps_num[2] + maps_num[3]
                seed = seed - maps_num[2] + maps_num[1]
                break
            end
        end
        push!(seed_transformation, seed)
    end
    push!(final_location, seed)
end

println(minimum(final_location))


#### Part 2

function read_file(filename)
    text = read(filename, String)
    blocks = split(text, "\n\n")

    seeds = parse.(Int64, split(split(blocks[1], ':')[2]))
    real_seeds, seeds_range = seeds[1:2:end], seeds[2:2:end]

    maps = [
        "seed_to_soil_map", "soil_to_fertilizer_map", "fertilizer_to_water_map",
        "water_to_light_map", "light_to_temperature_map", "temperature_to_humidity_map",
        "humidity_to_location_map"
    ]

    data_for_maps = Dict()
    for (i, map_name) in enumerate(maps)
        map_data = []
        for row in split(blocks[i+1], '\n')
            try
                push!(map_data, parse.(Int64, split(row)))
            catch e
                if isa(e, ArgumentError)
                    continue
                else
                    rethrow(e)
                end
            end
        end
        data_for_maps[map_name] = hcat(map_data...)'
    end

    return real_seeds, seeds_range, data_for_maps, maps
end

function transform_location(loc, maps, data_for_maps)
    for map_name in reverse(maps)
        for row in eachrow(data_for_maps[map_name])
            src, dest, length = row
            if src <= loc < src + length
                loc = loc - src + dest
                break
            end
        end
    end
    return loc
end

function find_smallest_location(real_seeds, seeds_range, data_for_maps, maps)
    j = 0
    while j < 10000000000 
        transformed_loc = transform_location(j, maps, data_for_maps)

        for (seed, length) in zip(real_seeds, seeds_range)
            if seed <= transformed_loc < seed + length
                return j  
            end
        end
        j += 1  
    end
    return -1  
end

# Read file and process
filename = "d5_input.txt"  # Replace with your actual file name

@time begin
    real_seeds, seeds_range, data_for_maps, maps = read_file(filename)
    smallest_loc = find_smallest_location(real_seeds, seeds_range, data_for_maps, maps)
    println(smallest_loc)
end