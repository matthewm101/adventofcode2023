grid = []
with open("input.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            grid.append([c for c in line.strip()])

height = len(grid)
width = len(grid[0])

load = 0
for x in range(width):
    per_load = height
    for y in range(height):
        if grid[y][x] == 'O':
            load += per_load
            per_load -= 1
        elif grid[y][x] == '#':
            per_load = height - y - 1
print(f"The total load after rolling everything north is {load}.")

def rotate_north():
    for x in range(width):
        empty = 0
        for y in range(height):
            if grid[y][x] == 'O':
                grid[y][x] = '.'
                grid[empty][x] = 'O'
                empty += 1
            elif grid[y][x] == '#':
                empty = y+1
                
def rotate_south():
    for x in range(width):
        empty = height-1
        for y in range(height-1,-1,-1):
            if grid[y][x] == 'O':
                grid[y][x] = '.'
                grid[empty][x] = 'O'
                empty -= 1
            elif grid[y][x] == '#':
                empty = y-1
                
def rotate_west():
    for y in range(height):
        empty = 0
        for x in range(width):
            if grid[y][x] == 'O':
                grid[y][x] = '.'
                grid[y][empty] = 'O'
                empty += 1
            elif grid[y][x] == '#':
                empty = x+1

def rotate_east():
    for y in range(height):
        empty = width-1
        for x in range(width-1,-1,-1):
            if grid[y][x] == 'O':
                grid[y][x] = '.'
                grid[y][empty] = 'O'
                empty -= 1
            elif grid[y][x] == '#':
                empty = x-1

def gridstr():
    return "".join(["".join(r) for r in grid])

i = 0
memo = {}
while i < 1000000000:
    rotate_north()
    rotate_west()
    rotate_south()
    rotate_east()
    s = gridstr()
    if s in memo:
        delta = i+1-memo[s]
        i += (1000000000 - (i+1)) // delta * delta
    else:
        memo[s] = i+1
    i += 1

load = 0
for x in range(width):
    per_load = height
    for y in range(height):
        if grid[y][x] == 'O':
            load += per_load
        per_load -= 1
print(f"The total load after a billion cycles is {load}.")