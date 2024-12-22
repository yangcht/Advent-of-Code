import numpy as np

def evolve(secret):
    secret ^= (secret * 64)
    secret %= 16777216
    secret ^= (secret // 32)
    secret %= 16777216
    secret ^= (secret * 2048)
    secret %= 16777216
    return secret

def sum_2k_secrets(buyers, steps=2000):
    total = 0
    for buyer in buyers:
        secret = buyer
        for _ in range(steps):
            secret = evolve(secret)
        total += secret
    return total

def find_max_bananas(buyers, steps=2000):
    base3, base2, base1 = 19**3, 19**2, 19
    sequence_totals = [0] * (19**4)
    for buyer in buyers:
        secret = buyer
        prev_price = secret % 10
        changes = [-9, -9, -9, -9]
        seen_sequences = set()
        for _ in range(steps):
            secret = evolve(secret)
            current_price = secret % 10
            change = current_price - prev_price
            changes = changes[1:] + [change]
            if changes[0] != -9:
                idx = (changes[0] + 9) * base3 + (changes[1] + 9) * base2 + (changes[2] + 9) * base1 + (changes[3] + 9)
                if idx not in seen_sequences:
                    sequence_totals[idx] += current_price
                    seen_sequences.add(idx)
            prev_price = current_price
    return max(sequence_totals) if sequence_totals else 0

def main():
    with open('./inputs/day22_1.txt') as file:
        initial_secrets = [int(line) for line in file if line.strip()]
    q1_sum = sum_2k_secrets(initial_secrets)
    q2_max = find_max_bananas(initial_secrets)
    print(f"Q1: the sum is {q1_sum}")
    print(f"Q2: the most banana I can get is {q2_max}")

if __name__ == "__main__":
    main()