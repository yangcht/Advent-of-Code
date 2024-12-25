def parse(s):
    l, k = [], []
    for sch in s.split("\n\n"):
        r = sch.strip().split("\n")
        if r[0] == "#####":
            l.append([sum(1 for x in r if x[c] == "#") for c in range(len(r[0]))])
        elif r[-1] == "#####":
            k.append([sum(1 for x in reversed(r) if x[c] == "#") for c in range(len(r[0]))])
    return l, k

def count(l, k, h=7):
    return sum(1 for a in l for b in k if all(a[c] + b[c] <= h for c in range(len(a))))

def main():
    l, k = parse(open("./inpus/day25_1.txt").read())
    print(count(l, k))

if __name__ == "__main__":
    main()