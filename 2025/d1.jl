const DIAL      = 100
const START_POS = 50

function solve(path)
    pos, p1, p2 = START_POS, 0, 0

    for raw in eachline(path)
        line = strip(raw)
        isempty(line) && continue

        dir_char = line[1]
        steps    = parse(Int, line[2:end])

        dir = dir_char == 'R' ? 1 : -1

        first_zero = if dir_char == 'R'
            pos == 0 ? DIAL : DIAL - pos
        else
            pos == 0 ? DIAL : pos
        end

        if steps >= first_zero
            p2 += 1 + (steps - first_zero) ÷ DIAL
        end

        pos = mod(pos + dir * steps, DIAL)

        if pos == 0
            p1 += 1
        end
    end

    println("Part 1: $p1")
    println("Part 2: $p2")
end

# julia d1.jl ./input/d1.txt
input_file = ARGS[1]
solve(input_file)
