function r2(n::BigInt)
    s = string(n)
    h = div(length(s), 2)
    l = h > 0 ? parse(BigInt, s[1:h]) : BigInt(0)
    r = h < length(s) ? parse(BigInt, s[h+1:end]) : BigInt(0)
    return [l, r]
end

function r3(n::BigInt)
    return [n * BigInt(2024)]
end

const RULE_CACHE = Dict{BigInt, Vector{BigInt}}()

function rules(n::BigInt)
    if haskey(RULE_CACHE, n)
        return RULE_CACHE[n]
    end

    result = if n == 0
        [BigInt(1)]
    elseif iseven(length(string(n)))
        r2(n)
    else
        r3(n)
    end

    RULE_CACHE[n] = result
    return result
end

function read_input(fp::String)
    return split(readlines(fp) |> only, " ") .|> x -> parse(BigInt, x)
end

function main(num::Int)
    ini_states = read_input("./inputs/day11_1.txt")
    to_blink = num

    current_cnt = Dict{BigInt, BigInt}()
    for s in ini_states
        current_cnt[s] = get(current_cnt, s, BigInt(0)) + BigInt(1)
    end

    for _ in 1:to_blink
        next_cnts = Dict{BigInt, BigInt}()
        for (n, cnt) in current_cnt
            for nn in rules(n)
                next_cnts[nn] = get(next_cnts, nn, BigInt(0)) + cnt
            end
        end
        current_cnt = next_cnts
    end

    total = sum(values(current_cnt))
end

println("Q1: $(main(25))")
println("Q2: $(main(75))")
println("blink 10000 times: $(main(10000))")