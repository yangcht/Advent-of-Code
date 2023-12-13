from functools import cache

def parse_input(data: str, n: int) -> list[tuple[str, tuple[int]]]:
    result = []
    for line in data.splitlines():
        springs, sizes = line.split()
        springs_expanded = ('?'.join([springs] * n)) 
        sizes_expanded = tuple(map(int, (','.join([sizes] * n)).split(',')))
        result.append((springs_expanded, sizes_expanded))
    return result

@cache
def find_solutions(springs: str, sizes: tuple[int], group_size: int = 0) -> int:
    if not springs:
        return int(not sizes and not group_size)

    num_solutions = 0
    symbol = ['.', '#'] if springs[0] == '?' else [springs[0]]
    for sym in symbol:
        if sym == '#':
            num_solutions += find_solutions(springs[1:], sizes, group_size + 1)
        elif group_size:
            if sizes and sizes[0] == group_size:
                num_solutions += find_solutions(springs[1:], sizes[1:])
        else:
            num_solutions += find_solutions(springs[1:], sizes)

    return num_solutions

def main(file_path: str, n: int) -> None:
    with open(file_path, 'r') as file:
        file_content = file.read()

    parsed_data = parse_input(file_content, n)
    total_arrangements = sum(find_solutions(springs + '.', sizes) for springs, sizes in parsed_data)
    print(total_arrangements)

#### Part 1
main('d12_input.txt', 1)

#### Part 2
main('d12_input.txt', 5)