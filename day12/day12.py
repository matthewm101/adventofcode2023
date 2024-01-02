all_cells = []
all_sections = []
with open("input.txt") as f:
    for line in f:
        splits = line.strip().split(" ")
        row = []
        for c in splits[0]:
            row.append(c)
        all_cells.append(tuple(row))
        splits = splits[1].split(",")
        all_sections.append(tuple([int(n) for n in splits]))

memo = {} # this magically makes this thing run a bajillion times faster
def solve(cells,sections):
    if len(sections) == 0:
        if '#' in cells:
            return 0 # Contradiction found, fail immediately
        return 1 # Everything else is a . or ?, and the only valid solution is to make everything .
    if len(cells) < sum(sections) + len(sections) - 1:
        return 0 # Not enough space left to fit everything
    solutions = 0
    if len(cells) == sections[0] and '.' not in cells:
        return 1 # One section left, and everything can be filled: only valid solution is to make everything #
    if (cells,sections) in memo:
        return memo[(cells,sections)]
    if '.' not in cells[0:sections[0]] and '#' != cells[sections[0]]:
        solutions += solve(cells[sections[0]+1:],sections[1:])
    if '#' != cells[0]:
        solutions += solve(cells[1:],sections)
    memo[(cells,sections)] = solutions
    return solutions

count_sum = sum([solve(all_cells[i], all_sections[i]) for i in range(len(all_cells))])
print(f"The sum of all the possible solutions for each folded spring is {count_sum}.")

all_unfolded_cells = [((c + tuple(['?'])) * 5)[:-1] for c in all_cells]
all_unfolded_sections = [s * 5 for s in all_sections]
count_sum = 0
for i in range(len(all_unfolded_cells)):
    count_sum += solve(all_unfolded_cells[i], all_unfolded_sections[i])
print(f"The sum of all the possible solutions for each unfolded spring is {count_sum}.")