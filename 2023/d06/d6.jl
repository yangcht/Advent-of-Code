# reading the input
lines = readlines("./d6_input.txt")
lines = rstrip.(lines)  # Julia uses broadcasting ('.') for element-wise operations

#### Part 1

time = parse.(Int64, split(split(lines[1], ':')[2]))
dist = parse.(Int64, split(split(lines[2], ':')[2]))

ways_to_win = Int[]

for (t, d) in zip(time, dist)
    time_arrays = 0:t
    results = [x for x in time_arrays if (t - x) * x > d]
    push!(ways_to_win, length(results))
end

println(prod(ways_to_win))

#### Part 2

time_new = parse(Int64, replace(split(lines[1], ':')[2], " " => ""))
dist_new = parse(Int64, replace(split(lines[2], ':')[2], " " => ""))

time_arrays = 0:time_new
results = [x for x in time_arrays if (time_new - x) * x > dist_new]

println(length(results))
