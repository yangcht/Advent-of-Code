import math

def read_input(file_path):
    with open(file_path, 'r') as file:
        workflows, parts = file.read().split('\n\n')
    return [w.strip() for w in workflows.split('\n')], [p.strip() for p in parts.split('\n')]

def process_workflows(workflows, parts):
    workflow_dict = {wf.split('{')[0]: wf.split('{')[1].strip('}').split(',') for wf in workflows}
    
    def eval_condition(part, condition):
        key, value = condition.split('>') if '>' in condition else condition.split('<')
        return part.get(key, 0) > int(value) if '>' in condition else part.get(key, 0) < int(value)

    def exec_actions(part):
        current_workflow = 'in'
        while True:
            for action in workflow_dict[current_workflow]:
                if ':' in action:
                    condition, result = action.split(':')
                    if eval_condition(part, condition):
                        if result in 'AR': return result == 'A', part
                        current_workflow = result
                        break
                elif action in 'AR': return action == 'A', part
                else: current_workflow = action; break
            else: break
        return False, None

    total_sum = 0
    for part in parts:
        part_dict = {k: int(v) for k, v in (rating.split('=') for rating in part[1:-1].split(','))}
        accepted, accepted_part = exec_actions(part_dict)
        if accepted: total_sum += sum(accepted_part.values())

    return total_sum

def process_workflows_part_two(workflows):
    workflow_dict = {wf.split('{')[0]: wf.split('{')[1].strip('}').split(',') for wf in workflows}
    memo = {}

    def calculate_valid_combinations(workflow, ranges):
        if workflow in ['A', 'R']:
            return math.prod(u - l + 1 for l, u in ranges) if workflow == 'A' else 0

        if (workflow, tuple(ranges)) in memo:
            return memo[(workflow, tuple(ranges))]

        total_combinations = 0
        for action in workflow_dict[workflow]:
            if ':' in action: 
                condition, result = action.split(':')
                key = key_to_index[condition[0]]
                value = int(condition[2:])
                if condition[1] == '<':
                    new_ranges = ranges.copy()
                    new_ranges[key] = (ranges[key][0], min(ranges[key][1], value - 1))
                    total_combinations += calculate_valid_combinations(result, new_ranges)
                    ranges[key] = (max(ranges[key][0], value), ranges[key][1])
                else:
                    new_ranges = ranges.copy()
                    new_ranges[key] = (max(ranges[key][0], value + 1), ranges[key][1])
                    total_combinations += calculate_valid_combinations(result, new_ranges)
                    ranges[key] = (ranges[key][0], min(ranges[key][1], value))
            else:  
                total_combinations += calculate_valid_combinations(action, ranges)

        memo[(workflow, tuple(ranges))] = total_combinations
        return total_combinations

    key_to_index = {'x': 0, 'm': 1, 'a': 2, 's': 3}
    initial_ranges = [(1, 4000)] * 4  
    return calculate_valid_combinations('in', initial_ranges)

#### Part 1
workflows, parts = read_input('./d19_input.txt')
print("Part 1 =", process_workflows(workflows, parts))

#### Part 2
print("Part 2 =", process_workflows_part_two(workflows))