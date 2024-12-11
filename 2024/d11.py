import sys

def r0(n):
    return [1]

def rs(n):
    s = str(n)
    h = len(s) // 2
    l = int(s[:h])
    r = int(s[h:])
    return [l, r]

def rm(n):
    return [n * 2024]

def ar(n):
    if n == 0:
        return r0(n)
    d = len(str(n))
    if d % 2 == 0:
        return rs(n)
    return rm(n)

def ri(fp):
    with open(fp, 'r') as f:
        c = f.read()
    return list(map(int, c.strip().split()))

def main(num):
    fp = './d11.txt'
    is_ = ri(fp)

    tb = num
    memo = {}

    def cs(n, b):
        if b == 0:
            return 1
        k = (n, b)
        if k in memo:
            return memo[k]
        ns = ar(n)
        t = 0
        for nn in ns:
            t += cs(nn, b - 1)
        memo[k] = t
        return t

    ts = 0
    for s in is_:
        ts += cs(s, tb)

    print(f"{ts}")

if __name__ == "__main__":
    print("Q1:", end=" ")
    main(25)
    print("Q2:", end=" ")
    main(75)