def parse_input(file_path):
    with open(file_path) as f:
        patterns_section, designs_section = f.read().split('\n\n', 1)
    patterns = [p.strip() for p in patterns_section.split(',') if p.strip()]
    designs = [d.strip() for d in designs_section.splitlines() if d.strip()]
    return patterns, designs

def count_combinations(design, patterns):
    dp = [0] * (len(design) + 1)
    dp[0] = 1
    for i in range(1, len(design) + 1):
        dp[i] = sum(dp[i - len(p)] for p in patterns if i >= len(p) and design[i - len(p):i] == p)
    return dp[-1]

def main(input_file):
    patterns, designs = parse_input(input_file)
    counts = [count_combinations(d, patterns) for d in designs]
    possible_designs = sum(1 for c in counts if c > 0)
    total_ways = sum(counts)
    print(f"Q1: Number of possible designs is {possible_designs}")
    print(f"Q2: Number of total designs is {total_ways}")

if __name__ == "__main__":
    main('./inputs/day19_1.txt')
