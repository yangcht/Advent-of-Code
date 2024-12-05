with open("./inputs/day05_1.txt", "r") as file:
    content = file.read().strip()

rule_part, page_part = content.split("\n\n")

rules = [list(map(int, line.split('|'))) for line in rule_part.splitlines()]
pages = [list(map(int, line.split(','))) for line in page_part.splitlines()]

# PART I: Find pages that follows the rules:
def check_rules_for_page(page, rules):
    for rule in rules:

        match = [page.index(r) for r in rule if r in page]

        if not ((len(match) == 2 and match[1] > match[0]) or len(match) <= 1):
            return False

    return True 

middle_page = [
    page[len(page) // 2]
    for page in pages
    if check_rules_for_page(page, rules)
]

# PART II: Reorder pages according to the rules:
ordered_page = []

def order_page_by_rules(page, rules):
    violate_rule = True
    while violate_rule:
        violate_rule = False
        for rule in rules:
            match = [page.index(r) for r in rule if r in page]
            if len(match) == 2 and match[1] < match[0]:
                page[match[0]], page[match[1]] = page[match[1]], page[match[0]]
                violate_rule = True

    return page

middle_ordered_page = [
    order_page_by_rules(page[:], rules)[len(page) // 2]
    for page in pages
    if not check_rules_for_page(page, rules)
]

print(f'Q1 sum: {sum(middle_page)}')
print(f'Q2 sum: {sum(middle_ordered_page)}')
