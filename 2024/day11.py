def r1(n):
    return [1]

def r2(n):
    s = str(n)
    h = len(s) // 2
    l = int(s[:h]) if h > 0 else 0
    r = int(s[h:]) if h < len(s) else 0
    return [l, r]

def r3(n):
    return [n * 2024]

rule_cache = {}
def rules(n):
    if n in rule_cache:
        return rule_cache[n]
    if n == 0:
        result = r1(n)
    elif len(str(n)) % 2 == 0:
        result = r2(n)
    else:
        result = r3(n)
    rule_cache[n] = result
    return result

def read_input(fp):
    with open(fp, 'r') as f:
        return list(map(int, f.read().strip().split()))

def main(num):
    ini_states = read_input('./inputs/day11_1.txt')
    to_blink = num

    current_cnt = {}
    for s in ini_states:
        current_cnt[s] = current_cnt.get(s, 0) + 1

    for step in range(1, to_blink + 1):
        next_cnts = {}
        for n, cnt in current_cnt.items():
            for nn in rules(n):
                next_cnts[nn] = next_cnts.get(nn, 0) + cnt
        current_cnt = next_cnts

    total = sum(current_cnt.values())
    print(f"{total}")

if __name__ == "__main__":
    print("Q1:", end=" ")
    main(25)
    print("Q2:", end=" ")
    main(75)
    print("blink 10000 times:", end=" ")
    main(10000)
