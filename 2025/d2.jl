#!/usr/bin/env julia

function parse_ranges(line::String)
    range_parts = split(line, ",")
    return [parse.(Int, split(r, "-")) for r in range_parts if !isempty(r)]
end

function invalid_id_part1(n::Int)
    s = string(n)
    len = length(s)
    return len % 2 == 0 && s[1:len ÷ 2] == s[len ÷ 2 + 1:end]
end

function invalid_id_part2(n::Int)
    s = string(n)
    len = length(s)
    for k in 1:len ÷ 2
        if len % k == 0 && all(s[i:i+k-1] == s[1:k] for i in 1:k:len)
            return true
        end
    end
    return false
end

function invalid_id_counter(file::String)
    line = open(readline, file)
    raw_ranges = parse_ranges(line)
    total1 = 0
    total2 = 0

    for (a, b) in raw_ranges
        for n in a:b
            total1 += invalid_id_part1(n) ? n : 0
            total2 += invalid_id_part2(n) ? n : 0
        end
    end

    println("Part 1: $total1")
    println("Part 2: $total2")
end

function main()
    filename = ARGS[1]
    invalid_id_counter(filename)
end

# julia d2.jl ./input/d2.txt
main()