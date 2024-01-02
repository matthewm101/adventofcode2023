grid = []
with open("input.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            grid.append(list(line.strip()))

height = len(grid)
width = len(grid[0])
def at(x,y):
    if 0 <= x < width:
        if 0 <= y < height:
            return grid[y][x]
    return '.'

start_y = None
start_x = None
for y in range(height):
    for x in range(width):
        if at(x,y) == 'S':
            start_y = y
            start_x = x
            
if at(start_x,start_y-1) in "7|F":
    if at(start_x-1,start_y) in "L-F":
        grid[start_y][start_x] = 'J'
    elif at(start_x,start_y+1) in "J|L":
        grid[start_y][start_x] = '|'
    else:
        grid[start_y][start_x] = 'L'
elif at(start_x-1,start_y) in "L-F":
    if at(start_x,start_y+1) in "J|L":
        grid[start_y][start_x] = '7'
    else:
        grid[start_y][start_x] = '-'
else:
    grid[start_y][start_x] = 'F'    
            
def links(x,y):
    result = []
    def test(xx,yy,answers):
        if at(xx,yy) in answers: result.append((xx,yy))
    match at(x,y):
        case '|': test(x,y+1,"J|L"); test(x,y-1,"7|F")
        case '-': test(x-1,y,"L-F"); test(x+1,y,"J-7")
        case 'J': test(x-1,y,"L-F"); test(x,y-1,"7|F")
        case 'L': test(x+1,y,"J-7"); test(x,y-1,"7|F")
        case '7': test(x-1,y,"L-F"); test(x,y+1,"J|L")
        case 'F': test(x+1,y,"J-7"); test(x,y+1,"J|L")
    return result

fill = {(start_x,start_y):0}
frontier = [(start_x,start_y)]
while len(frontier) > 1 or len(fill) == 1:
    new_frontier = []
    for f in frontier:
        ls = links(*f)
        for l in ls:
            if l not in fill:
                fill[l] = fill[f] + 1
                new_frontier.append(l)
    frontier = new_frontier
end = frontier[0]
print(f"The end is at {end}, which is {fill[end]} steps away.")

def to_supergrid_tile(c):
    match c:
        case '|': return [[False, True, False],[False, True, False],[False, True, False]]
        case 'J': return [[False, True, False],[True, True, False],[False, False, False]]
        case 'L': return [[False, True, False],[False, True, True],[False, False, False]]
        case '-': return [[False, False, False],[True, True, True],[False, False, False]]
        case '7': return [[False, False, False],[True, True, False],[False, True, False]]
        case 'F': return [[False, False, False],[False, True, True],[False, True, False]]
        case '.': return [[False, False, False],[False, False, False],[False, False, False]]
    print(c)

supergrid = [[False for x in range(3 * width)] for y in range(3 * height)]
for x,y in fill.keys():
    tile = to_supergrid_tile(at(x,y))
    for xx in range(3):
        for yy in range(3):
            supergrid[y * 3 + yy][x * 3 + xx] = tile[yy][xx]
def superget(x,y):
    if 0 <= x < 3*width:
        if 0 <= y < 3*height:
            return supergrid[y][x]
    return True
                
flood_fill_starts = []
match grid[start_y][start_x]:
    case '|': flood_fill_starts = [(3*start_x-1,3*start_y),(3*start_x+1,3*start_y)]
    case 'J': flood_fill_starts = [(3*start_x-1,3*start_y-1),(3*start_x+1,3*start_y+1)]
    case 'L': flood_fill_starts = [(3*start_x+1,3*start_y-1),(3*start_x-1,3*start_y+1)]
    case '-': flood_fill_starts = [(3*start_x,3*start_y-1),(3*start_x,3*start_y+1)]
    case '7': flood_fill_starts = [(3*start_x-1,3*start_y+1),(3*start_x+1,3*start_y-1)]
    case 'F': flood_fill_starts = [(3*start_x+1,3*start_y+1),(3*start_x-1,3*start_y-1)]

round_x_enclosed_tiles = [set([]),set([])]
round_x_okay = [True,True]

for r in range(2): # do two rounds: one will cover all the enclosed tiles, one will cover all the outside tiles, but we don't know which
    frontier = set([flood_fill_starts[r]])
    seen = set(frontier)
    while len(frontier) > 0:
        new_frontier = set([])
        for x,y in frontier:
            for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if (xx,yy) not in seen and not superget(xx,yy):
                    seen.add((xx,yy))
                    new_frontier.add((xx,yy))
                    true_x = xx // 3
                    true_y = yy // 3
                    if (true_x,true_y) not in fill.keys():
                        round_x_enclosed_tiles[r].add((true_x,true_y))
        frontier = new_frontier
    if len([p for p in seen if p[0] == 0 or p[0] == width*3-1 or p[1] == 0 or p[1] == height*3-1]) > 0:
        round_x_okay[r] = False

n_enclosed_tiles = len(round_x_enclosed_tiles[0]) if round_x_okay[0] else len(round_x_enclosed_tiles[1])
print(f"There are {n_enclosed_tiles} tiles enclosed in the loop.")