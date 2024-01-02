grid = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0: continue
        grid.append([c for c in line])

height = len(grid)
width = len(grid[0])

important_spots = set()
starting_point = (0,0)
ending_point = (0,0)
for x in range(width):
    if grid[0][x] == '.':
        starting_point = (x,0)
        important_spots.add(starting_point)
    if grid[height-1][x] == '.':
        ending_point = (x,height-1)
        important_spots.add(ending_point)
for y in range(1,height-1):
    for x in range(1,width-1):
        if grid[y][x] != '#' and len([True for p in [(1,0),(-1,0),(0,1),(0,-1)] if grid[y+p[1]][x+p[0]] != '#']) > 2:
            important_spots.add((x,y))
    
# The following structure maps (start,end) tuples to the length needed; the entry will not be present if it is impossible
edges = {}
neighbors = {p:set() for p in important_spots}
def update_edge(start,end,length):
    k = (start,end)
    if k in edges:
        edges[k] = max(length,edges[k])
        neighbors[start].add(end)
    else:
        edges[k] = length
        neighbors[start].add(end)

for start in important_spots:
    for end in important_spots:
        if start == end: continue
        frontier = set([start])
        seen = set([start])
        steps = 0
        while len(frontier) > 0:
            steps += 1
            new_frontier = set()
            for p in frontier:
                x,y = p
                nexts = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                if grid[y][x] == '>': nexts = [(x+1,y)]
                elif grid[y][x] == '<': nexts = [(x-1,y)]
                elif grid[y][x] == 'v': nexts = [(x,y+1)]
                elif grid[y][x] == '^': nexts = [(x,y-1)]
                for next_p in nexts:
                    next_x, next_y = next_p
                    if next_p == end:
                        update_edge(start,end,steps)
                    elif (0 <= next_x < width) and (0 <= next_y < height) and grid[next_y][next_x] != '#' and next_p not in important_spots and next_p not in seen:
                        new_frontier.add(next_p)
            frontier = new_frontier
            seen.update(frontier)

frontier = [(starting_point,0,frozenset([starting_point]))]
longest_length = 0
while len(frontier) > 0:
    new_frontier = []
    for curr_p, length, seen in frontier:
        if curr_p == ending_point:
            longest_length = max(length,longest_length)
            continue
        for next_p in neighbors[curr_p].difference(seen):
            new_frontier.append((next_p, length + edges[(curr_p,next_p)], seen.union(frozenset([next_p]))))
    frontier = new_frontier
    
print(f"The longest path with slippery slopes is {longest_length} steps long.")

for start in important_spots:
    for end in important_spots:
        if start == end: continue
        if (start,end) in edges and (end,start) not in edges:
            edges[(end,start)] = edges[(start,end)]
            neighbors[end].add(start)

# Python keeps killing my attempts at doing a BFS, so it's time for a DFS

def search(current_p: tuple[int,int], length: int, seen: frozenset[tuple[int,int]]):
    if current_p == ending_point:
        return length
    return max([search(next_p, length + edges[(current_p,next_p)], seen | frozenset([next_p])) for next_p in neighbors[current_p].difference(seen)] + [0])

longest_length = search(starting_point, 0, frozenset([starting_point]))

print(f"The longest path without slippery slopes is {longest_length} steps long.")