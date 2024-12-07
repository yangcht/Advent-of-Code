#!/bin/bash

print_header() {
    echo "+-----------------+-----------------+-----------------+-----------------+-----------------------+-----------------+-----------------+"
    printf "| %-15s | %-15s | %-15s | %-15s | %-21s | %-15s | %-15s |\n" "File Name" "Mean Time (s)" "Std Dev (s)" "Min Time (s)" "CPU-f-Norm T (µs/MHz)" "Part 1" "Part 2"
    echo "+-----------------+-----------------+-----------------+-----------------+-----------------------+-----------------+-----------------+"
}

print_row() {
    printf "| %-15s | %-15s | %-15s | %-15s | %-21s | %-15s | %-15s |\n" "$1" "$2" "$3" "$4" "$5" "$6" "$7"
}

filter_warnings() {
    echo "$1" | grep -v "Intel MKL WARNING"
}

run_benchmark() {
    local cmd="$1"
    hyperfine --warmup 2 --export-json temp.json "$cmd" > /dev/null 2>&1
    mean=$(jq '.results[0].mean' temp.json | xargs printf "%.5f")
    stddev=$(jq '.results[0].stddev' temp.json | xargs printf "%.5f")
    mintime=$(jq '.results[0].min' temp.json | xargs printf "%.5f")
    echo "$mean" "$stddev" "$mintime"
}

normalize_by_cpu_freq() {
    local mean_time="$1"
    local cpu_freq=3.2
    if [[ -z "$cpu_freq" || "$cpu_freq" == "0" ]]; then
        exit 1
    fi
    normalized_time=$(echo "$mean_time / $cpu_freq * 1000" | bc -l)
    printf "%.5f" "$normalized_time"
}

print_header

for script in $(ls | grep -E "\.py$|\.jl$" | sort); do
    if [[ $script == *.py ]]; then
        read mean stddev mintime < <(run_benchmark "python $script")
        output=$(python "$script" 2>/dev/null)
    elif [[ $script == *.jl ]]; then
        read mean stddev mintime < <(run_benchmark "julia $script")
        output=$(julia "$script" 2>/dev/null)
    fi

    cpu_norm_time=$(normalize_by_cpu_freq "$mean")

    output=$(filter_warnings "$output")
    part1=$(echo "$output" | sed -n '1p' | awk -F':' '{print $2}' | xargs)
    part2=$(echo "$output" | sed -n '2p' | awk -F':' '{print $2}' | xargs)
    part1=${part1:-"N/A"}
    part2=${part2:-"N/A"}

    print_row "$script" "$mean" "$stddev" "$mintime" "$cpu_norm_time" "$part1" "$part2"
done

echo "+-----------------+-----------------+-----------------+-----------------+-----------------------+-----------------+-----------------+"

rm -f temp.json