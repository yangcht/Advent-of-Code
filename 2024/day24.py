import re

with open('./inputs/day24_1.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

sections = []
current = []
for line in lines:
    if line == '':
        if current:
            sections.append(current)
            current = []
    else:
        current.append(line)
if current:
    sections.append(current)

initial = sections[0]
gates = sections[1]

wires = {}
for line in initial:
    wire, val = line.split(':')
    wires[wire.strip()] = int(val.strip())

parsed_gates = []
gate_pattern = re.compile(r'^(\w+)\s+(AND|OR|XOR)\s+(\w+)\s*->\s*(\w+)$')
for gate in gates:
    m = gate_pattern.match(gate)
    if m:
        parsed_gates.append(m.groups())

remaining = parsed_gates.copy()
while remaining:
    progress = False
    to_remove = []
    for gate in remaining:
        in1, op, in2, out = gate
        if in1 in wires and in2 in wires:
            if op == 'AND':
                wires[out] = wires[in1] & wires[in2]
            elif op == 'OR':
                wires[out] = wires[in1] | wires[in2]
            elif op == 'XOR':
                wires[out] = wires[in1] ^ wires[in2]
            to_remove.append(gate)
            progress = True
    for gate in to_remove:
        remaining.remove(gate)
    if not progress:
        break

z_wires = {k: v for k, v in wires.items() if k.startswith('z')}
sorted_z = sorted(z_wires.items(), key=lambda x: int(re.match(r'z(\d+)', x[0]).group(1)))
binary = ''.join(str(val) for _, val in sorted_z[::-1])

print(f"Q1: {int(binary, 2)}")
