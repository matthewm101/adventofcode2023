grid = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0: continue
        grid.append([c for c in line])

height = len(grid)
width = len(grid[0])
start_x = 0
start_y = 0
valid_positions = set()
for y in range(height):
    for x in range(width):
        if grid[y][x] == 'S':
            start_x = x
            start_y = y
            valid_positions.add((x,y))
        if grid[y][x] == '.':
            valid_positions.add((x,y))
valid_output_positions = set([(x,-1) for x in range(width)] + [(x,height) for x in range(width)] + [(-1,y) for y in range(height)] + [(width,y) for y in range(height)])
            
def step(p):
    output = set()
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        x = p[0] + dx
        y = p[1] + dy
        if (x,y) in valid_positions:
            output.add((x,y))
    return output

def modstep(p):
    output = set()
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        x = p[0] + dx
        y = p[1] + dy
        if (x%width,y%height) in valid_positions:
            output.add((x,y))
    return output

frontier = set([(start_x,start_y)])
for _ in range(64):
    new_frontier = set()
    for f in frontier:
        for o in step(f):
            new_frontier.add(o)
    frontier = new_frontier
            
print(f"There are {len(frontier)} plots accessible after exactly 64 steps.")

frontier = set([(start_x,start_y)])
f_0=f_1=f_2=0
for i in range(327):
    new_frontier = set()
    for f in frontier:
        for o in modstep(f):
            new_frontier.add(o)
    frontier = new_frontier
    if i == 64:
        f_0 = len(frontier)
    if i == 64 + 131:
        f_1 = len(frontier)
    if i == 64 + 2 * 131:
        f_2 = len(frontier)

x = (26501365 - 65) // 131
# f(0) = a(0)^2 + b(0) + c = c
# f(1) = a(1)^2 + b(1) + c = a + b + c
# f(2) = 4a + 2b + c
# Therefore c = f(0)
# Therefore a = (f_2 - 2f_1 + c) / 2
# Therefore b = f_1 - a - c
c = f_0 
a = int((f_2 - 2 * f_1 + c) / 2)
b = f_1 - a - c
y = a * x * x + b * x + c
print(f"There are {y} plots accessible after 26501365 steps on the infinite map.")
