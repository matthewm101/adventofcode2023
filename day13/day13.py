grids = []
with open("input.txt") as f:
    current_grid = []
    for line in f:
        line = line.strip()
        if len(line) > 0:
            current_grid.append([c for c in line])
        else:
            grids.append(current_grid)
            current_grid = []
    if current_grid != []:
        grids.append(current_grid)

def find_reflection(grid):
    height = len(grid)
    width = len(grid[0])
    for x in range(1,width):
        i = 0
        success = True
        while 0 <= x-i-1 and x+i < width:
            if len([y for y in range(height) if grid[y][x-1-i] != grid[y][x+i]]) > 0:
                success = False
                break
            i += 1
        if success:
            return x
    for y in range(1,height):
        i = 0
        success = True
        while 0 <= y-i-1 and y+i < height:
            if len([x for x in range(width) if grid[y-1-i][x] != grid[y+i][x]]) > 0:
                success = False
                break
            i += 1
        if success:
            return y * 100
    return 0

reflection_sum = 0
for g in grids:
    reflection_sum += find_reflection(g)
print(f"The sum of all reflections is {reflection_sum}.")

def find_almost_reflection(grid):
    height = len(grid)
    width = len(grid[0])
    for x in range(1,width):
        i = 0
        mistakes = 0
        while 0 <= x-i-1 and x+i < width:
            mistakes += len([y for y in range(height) if grid[y][x-1-i] != grid[y][x+i]])
            i += 1
        if mistakes == 1:
            return x
    for y in range(1,height):
        i = 0
        mistakes = 0
        while 0 <= y-i-1 and y+i < height:
            mistakes += len([x for x in range(width) if grid[y-1-i][x] != grid[y+i][x]])
            i += 1
        if mistakes == 1:
            return y * 100
    return 0

reflection_sum = 0
for g in grids:
    reflection_sum += find_almost_reflection(g)
print(f"The sum of all almost-reflections is {reflection_sum}.")