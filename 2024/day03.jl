input_string = read("./inputs/day03_1.txt", String)

# PART 1: Parsing mul:
pattern_1 = r"mul\((\d{1,3}),\s*(\d{1,3})\)"

matches = eachmatch(pattern_1, input_string)

sum_1 = sum(parse(Int, m.captures[1]) * parse(Int, m.captures[2]) for m in matches)

println("Q1 sum: ", sum_1)

# PART 2: Parsing mul with do and don't switch
pattern_2 = r"(do\(\))|(don't\(\))|mul\((\d{1,3}),\s*(\d{1,3})\)"

global enabled = true
global sum_2 = 0

for match in eachmatch(pattern_2, input_string)
    if !isnothing(match.captures[1])
        global enabled = true
    elseif !isnothing(match.captures[2])
        global enabled = false
    elseif enabled && !isnothing(match.captures[3]) && !isnothing(match.captures[4])
        global sum_2
        sum_2 += parse(Int, match.captures[3]) * parse(Int, match.captures[4])
    end
end

println("Q2 sum: ", sum_2)