# PART 1: Checking for each line the "safe" reports
# PART 2: Checking for each line the "safe" reports after applying dampener
function is_safe(r)
    diffs = [b - a for (a, b) in zip(r[1:end-1], r[2:end])]
    return ((all(diffs .> 0) || all(diffs .< 0)) && all(1 .<= abs.(diffs) .<= 3))
end

function dampener_counts(reports)
    safe_status = [is_safe(r) for r in reports]
    safe_count = count(safe_status)
    total_count = safe_count + count(
        (!safe_status[i] && length(reports[i]) >= 3) &&
        any(j -> is_safe(reports[i][[1:j-1; j+1:end]]), 1:length(reports[i]))
        for i in 1:length(reports)
    )
    return safe_count, total_count
end

function main()
    reports = [parse.(Int, split(strip(line))) for line in eachline("./inputs/day02_1.txt")]
    q1, q2 = dampener_counts(reports)
    println("Q1 safe count: $q1")
    println("Q2 safe count: $q2")
end

main()