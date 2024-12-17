import numpy as np

def read_input(fn):
    regs = [0, 0, 0]
    prog = []
    with open(fn) as f:
        for line in f:
            l = line.strip()
            if l.startswith('Register A:'):
                regs[0] = int(l.split(':')[1])
            elif l.startswith('Register B:'):
                regs[1] = int(l.split(':')[1])
            elif l.startswith('Register C:'):
                regs[2] = int(l.split(':')[1])
            elif l.startswith('Program:'):
                prog = np.array(list(map(int, l.split(':')[1].split(','))))
    return regs, prog

def get_val(op, regs):
    return op if op <= 3 else regs[0] if op == 4 else regs[1] if op == 5 else regs[2]

def run(progs, regs):
    ip, out = 0, []
    while ip < len(progs):
        opc, opd = progs[ip], progs[ip+1] if ip+1 < len(progs) else 0
        if opc == 0:
            regs[0] //= 2**get_val(opd, regs)
        elif opc == 1:
            regs[1] ^= opd
        elif opc == 2:
            regs[1] = get_val(opd, regs) % 8
        elif opc == 3:
            ip = opd if regs[0] else ip + 2
            continue
        elif opc == 4:
            regs[1] ^= regs[2]
        elif opc == 5:
            out.append(str(get_val(opd, regs) % 8))
        elif opc == 6:
            regs[1] = regs[0] // 2**get_val(opd, regs)
        elif opc == 7:
            regs[2] = regs[0] // 2**get_val(opd, regs)
        ip += 2
    return ','.join(out)

def main():
    r, p = read_input('./inputs/day17_1.txt')
    print(run(p, r))

if __name__ == "__main__":
    main()