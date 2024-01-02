grid = []
with open("input.txt") as f:
    for line in f:
        grid.append([c for c in line.strip()])
height = len(grid)
width = len(grid[0])
valid_locations = set()
for x in range(width):
    for y in range(height):
        valid_locations.add((x,y))

def run_test(initial_input):
    inputs = initial_input # Maps locations to the direction of an input
    update_queue = list(inputs.keys())
    while len(update_queue) > 0:
        new_update_queue = set()
        def update(x,y,d):
            if (x,y) in inputs:
                if d not in inputs[(x,y)]:
                    inputs[(x,y)].add(d)
                    new_update_queue.add((x,y))
            elif (x,y) in valid_locations:
                inputs[(x,y)] = set([d])
                new_update_queue.add((x,y))
        for pos in update_queue:
            x = pos[0]
            y = pos[1]
            match grid[y][x]:
                case '.':
                    if '>' in inputs[pos]:
                        update(x+1,y,'>')
                    if '<' in inputs[pos]:
                        update(x-1,y,'<')
                    if '^' in inputs[pos]:
                        update(x,y-1,'^')
                    if 'v' in inputs[pos]:
                        update(x,y+1,'v')
                case '/':
                    if '>' in inputs[pos]:
                        update(x,y-1,'^')
                    if '<' in inputs[pos]:
                        update(x,y+1,'v')
                    if '^' in inputs[pos]:
                        update(x+1,y,'>')
                    if 'v' in inputs[pos]:
                        update(x-1,y,'<')
                case '\\':
                    if '>' in inputs[pos]:
                        update(x,y+1,'v')
                    if '<' in inputs[pos]:
                        update(x,y-1,'^')
                    if '^' in inputs[pos]:
                        update(x-1,y,'<')
                    if 'v' in inputs[pos]:
                        update(x+1,y,'>')
                case '-':
                    if '>' in inputs[pos]:
                        update(x+1,y,'>')
                    if '<' in inputs[pos]:
                        update(x-1,y,'<')
                    if '^' in inputs[pos] or 'v' in inputs[pos]:
                        update(x+1,y,'>')
                        update(x-1,y,'<')
                case '|':
                    if '^' in inputs[pos]:
                        update(x,y-1,'^')
                    if 'v' in inputs[pos]:
                        update(x,y+1,'v')
                    if '<' in inputs[pos] or '>' in inputs[pos]:
                        update(x,y-1,'^')
                        update(x,y+1,'v')
        update_queue = new_update_queue
    return len(inputs)

top_left_rightward_tiles = run_test({(0,0):set(">")})

print(f"When the light starts rightward at the top-left, there are {top_left_rightward_tiles} energized tiles.")

best = 0
for x in range(width):
    best = max(best, run_test({(x,0):set("v")}), run_test({(x,height-1):set("^")}))
for y in range(height):
    best = max(best, run_test({(0,y):set(">")}), run_test({(width-1,y):set("<")}))
print(f"The best possible initial configuration energizes {best} tiles.")