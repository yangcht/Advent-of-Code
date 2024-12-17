import numpy as np
import matplotlib.pyplot as plt

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

def find_min_A(prog, initial_regs, program_output, start, end, step=1, visualize=False, visualize_step=1000):
    min_A = None
    As_digits = [[] for _ in range(16)] if visualize else None
    output_digits = [[] for _ in range(16)] if visualize else None

    for A in range(start, end, step):
        regs = [A, *initial_regs[1:]]
        output = run(prog, regs).split(',')
        if output == list(map(str, program_output)) and min_A is None:
            min_A = A
        if visualize and A % visualize_step == 0:
            for idx, digit in enumerate(output[:16]):
                As_digits[idx].append(A)
                output_digits[idx].append(int(digit))
        if A % 1_000_000 == 0 and A != 0:
            print(f"Checked up to A = {A}")
    if visualize:
        plot_pattern(As_digits, output_digits)
    return min_A

def plot_pattern(As_digits, output_digits):
    fig, axes = plt.subplots(4, 4, figsize=(20, 15), sharex=True)
    fig.suptitle('Initial A vs. Output Digits (1st to 16th)', fontsize=16)
    axes = axes.flatten()
    for i, ax in enumerate(axes[:16]):
        ax.scatter(As_digits[i], output_digits[i], s=10, alpha=0.6)
        ax.set_title(f'Digit {i+1}')
        ax.set_ylabel(f'Digit {i+1}')
        ax.grid(True)
        ax.set_ylim(-1, 9)
    for ax in axes[-4:]:
        ax.set_xlabel('Initial A Value')
    for j in range(16, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def main_p1(input_f):
    r, p = read_input(input_f)
    print(f"Q1: {run(p, r)}")

def main_p2(input_f):
    input_file = input_f
    initial_regs, prog = read_input(input_file)
    program_output = list(prog)
    RANGE_START = 90938893715360
    RANGE_END = 90938893815424
    RANGE_STEP = 1
    VISUALIZE_STEP = 1

    min_A = find_min_A(
        prog,
        initial_regs,
        program_output,
        start=RANGE_START,
        end=RANGE_END,
        step=RANGE_STEP,
        visualize=True,
        visualize_step=VISUALIZE_STEP
    )
    if min_A is not None:
        print(f"Q2 lowest {min_A}")

if __name__ == "__main__":
    f = './inputs/day17_1.txt'
    main_p1(f)
    # Part 2 was eye-balled from the figure for founding the first 8 digits of the 14 digits of A
    main_p2(f)