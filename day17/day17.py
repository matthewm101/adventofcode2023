import heapq

grid = []
with open("input.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            grid.append([int(c) for c in line.strip()])
width = len(grid[0])
height = len(grid)
valid_positions = set()
for x in range(width):
    for y in range(height):
        valid_positions.add((x,y))

print("Generating relaxed costs...")
hgrid = {p:999999999 for p in valid_positions}
hgrid[(width-1,height-1)] = 0
changed = True
while changed:
    changed = False
    for x in range(width-1,-1,-1):
        for y in range(height-1,-1,-1):
            for (dx,dy) in [(1,0),(-1,0),(0,1),(0,-1)]:
                new_x = x + dx
                new_y = y + dy
                if (new_x,new_y) in valid_positions:
                    cost = hgrid[(new_x,new_y)] + grid[new_y][new_x]
                    if cost < hgrid[(x,y)]:
                        changed = True
                        hgrid[(x,y)] = cost
print("Done.")
# print()
# for y in range(height):
#     for x in range(width):
#         print(hgrid[(x,y)],end=" ")
#     print()
# print()
                

        
# State format: (value,loss,x,y,dir+count,history)

def trans(s):
    cost = s[1]
    x = s[2]
    y = s[3]
    dir = s[4]
    new_states = set()
    for dx,dy,ddir in [(1,0,'>'),(-1,0,'<'),(0,1,'v'),(0,-1,'^')]:
        new_x = x + dx
        if new_x < 0 or new_x >= width: continue # Out of bounds
        new_y = y + dy
        if new_y < 0 or new_y >= height: continue # Out of bounds
        if ddir in dir and len(dir) == 3: continue # Too many movements in the same direction
        match ddir: # Illegal backwards movements
            case '>':
                if '<' in dir: continue
            case '<':
                if '>' in dir: continue
            case '^':
                if 'v' in dir: continue
            case 'v':
                if '^' in dir: continue
        
        new_dir = (dir + ddir) if (ddir in dir) else ddir
        new_cost = cost + grid[new_y][new_x]
        new_value = new_cost + hgrid[(new_x,new_y)]
        if (new_x,new_y,new_dir) not in seen:
            new_states.add((new_value, new_cost, new_x, new_y, new_dir))
            seen.add((new_x,new_y,new_dir))
    return new_states

start = (hgrid[(0,0)],0,0,0,"","")
seen = set()
heap = [start]
goal = None
# mindist = 100000
while len(heap) > 0:
    curr = heapq.heappop(heap)
    # dist = width + height - 2 - curr[2] - curr[3]
    # if dist < mindist:
    #     print(dist)
    #     mindist = dist
    if curr[2] == width-1 and curr[3] == height-1:
        goal = curr
        break
    nexts = trans(curr)
    for next in nexts:
        heapq.heappush(heap,next)

print(f"The regular crucible can reach the goal by losing only {goal[1]} heat.")

# State format: (value,loss,x,y,dir+count,history)

def ultra_trans(s):
    cost = s[1]
    x = s[2]
    y = s[3]
    dir = s[4]
    new_states = set()
    for dx,dy,ddir in [(1,0,'>'),(-1,0,'<'),(0,1,'v'),(0,-1,'^')]:
        if ddir in dir and len(dir) == 10: continue # Too many movements in the same direction
        if len(dir) > 0 and len(dir) < 4 and (ddir not in dir): continue # Not enough movements in the same direction
        match ddir: # Illegal backwards movements
            case '>':
                if '<' in dir: continue
            case '<':
                if '>' in dir: continue
            case '^':
                if 'v' in dir: continue
            case 'v':
                if '^' in dir: continue
        new_x = x + dx
        if new_x < 0 or new_x >= width: continue # Out of bounds
        new_y = y + dy
        if new_y < 0 or new_y >= height: continue # Out of bounds
        
        new_dir = (dir + ddir) if (ddir in dir) else ddir
        new_cost = cost + grid[new_y][new_x]
        new_value = new_cost + hgrid[(new_x,new_y)]
        if (new_x,new_y,new_dir) not in seen:
            new_states.add((new_value, new_cost, new_x, new_y, new_dir))
            seen.add((new_x,new_y,new_dir))
    return new_states

start = (hgrid[(0,0)],0,0,0,"")
seen = set()
heap = [start]
goal = None
# mindist = 100000
while len(heap) > 0:
    curr = heapq.heappop(heap)
    # dist = width + height - 2 - curr[2] - curr[3]
    # if dist < mindist:
    #     print(dist, curr)
    #     mindist = dist
    if curr[2] == width-1 and curr[3] == height-1 and len(curr[4]) >= 4:
        goal = curr
        break
    nexts = ultra_trans(curr)
    for next in nexts:
        heapq.heappush(heap,next)
print(f"The ultra crucible can reach the goal by losing only {goal[1]} heat.")