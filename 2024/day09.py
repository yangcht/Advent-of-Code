import os
import numpy as np

def parse_map(s):
    arr = np.array(list(s), dtype=int)
    f = arr[::2]
    fr = np.append(arr[1::2], 0) if len(arr) % 2 else arr[1::2]
    
    c = np.cumsum(f + fr)
    total = c[-1] if c.size > 0 else 0
    
    dsk = np.full(total, -1, dtype=int)
    
    fi = np.where(f > 0)[0]
    fs = np.insert(c[:-1], 0, 0)[fi]
    
    for id, start, length in zip(fi, fs, f[fi]):
        dsk[start:start + length] = id
    frs = list(zip(fi, fs, f[fi]))
    
    return dsk, frs

def chk_sum(dsk):
    mask = dsk != -1
    idx = np.nonzero(mask)[0]
    ids = dsk[mask]
    return np.dot(idx, ids)

def first_occ(dsk, val):
    idxs = np.flatnonzero(dsk == val)
    return idxs[0] if idxs.size > 0 else None

def last_occ(dsk):
    idxs = np.flatnonzero(dsk != -1)
    return idxs[-1] if idxs.size > 0 else None

def contig(dsk, start, length, id):
    return np.all(dsk[start:start + length] == id)

def find_space(dsk, length):
    free = (dsk == -1).astype(int)
    conv = np.convolve(free, np.ones(length, dtype=int), mode='valid')
    pos = np.where(conv == length)[0]
    return pos[0] if pos.size > 0 else None

def move_blk(dsk, frm, to, length):
    dsk[to:to + length] = dsk[frm:frm + length]
    dsk[frm:frm + length] = -1

def compact(dsk, frs, mode):
    if mode == 'Q1':
        while True:
            dot = first_occ(dsk, -1)
            if dot is None:
                break

            last_p = last_occ(dsk)
            if last_p is None or last_p < dot:
                break

            fid = dsk[last_p]
            dsk[dot] = fid
            dsk[last_p] = -1

    elif mode == 'Q2':
        sorted_f = sorted(frs, key=lambda x: x[0], reverse=True)

        for fid, start, length in sorted_f:
            if contig(dsk, start, length, fid):
                pos = find_space(dsk, length)
                if pos is not None and pos < start:
                    move_blk(dsk, start, pos, length)

def read_file(fp):
    with open(fp, 'r') as f:
        return f.read().strip()

def main():
    inp = read_file("./inputs/day09_1.txt")

    # Part 1
    d1, fr1 = parse_map(inp)
    compact(d1, fr1, 'Q1')
    cs1 = chk_sum(d1)
    print(f"Q1 Checksum: {cs1}")

    # Part 2
    d2, fr2 = parse_map(inp)
    compact(d2, fr2, 'Q2')
    cs2 = chk_sum(d2)
    print(f"Q2 Checksum: {cs2}")

if __name__ == "__main__":
    main()
