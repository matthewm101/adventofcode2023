class Brick:
    def __init__(self, id, p1, p2) -> None:
        ps = sorted([p1,p2])
        self.id = id
        self.p1 = ps[0]
        self.p2 = ps[1]
        x1,y1,z1 = self.p1
        x2,y2,z2 = self.p2
        self.blocks = frozenset()
        self.deps = frozenset()
        if x1 != x2:
            self.blocks = frozenset((x,y1,z1) for x in range(x1,x2+1))
            self.deps = frozenset((x,y1,z1-1) for x in range(x1,x2+1))
        elif y1 != y2:
            self.blocks = frozenset((x1,y,z1) for y in range(y1,y2+1))
            self.deps = frozenset((x1,y,z1-1) for y in range(y1,y2+1))
        else:
            self.blocks = frozenset((x1,y1,z) for z in range(z1,z2+1))
            self.deps = frozenset([(x1,y1,z1-1)])
    
    def drop1(self):
        self.p1 = (self.p1[0],self.p1[1],self.p1[2] - 1)
        self.p2 = (self.p2[0],self.p2[1],self.p2[2] - 1)
        self.blocks = frozenset((b[0],b[1],b[2]-1) for b in self.blocks)
        self.deps = frozenset((d[0],d[1],d[2]-1) for d in self.deps)
        
    def settled(self,blocks):
        if self.on_floor(): return True
        return len(self.deps.intersection(blocks)) != 0
    
    def on_floor(self):
        return self.p1[2] == 0 or self.p2[2] == 0
        
bricks: list[Brick] = []
brick_map = {}
next_brick_id = 1
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0: continue
        splits = line.split("~")
        p1 = tuple([int(n) for n in splits[0].split(",")])
        p2 = tuple([int(n) for n in splits[1].split(",")])
        bricks.append(Brick(next_brick_id,p1,p2))
        brick_map[next_brick_id] = bricks[-1]
        next_brick_id += 1

# Making the blocks settle
settled_count = 0
while settled_count < len(bricks):
    settled_count = 0
    all_blocks = frozenset.union(*[b.blocks for b in bricks])
    for b in bricks:
        if b.settled(all_blocks):
            settled_count += 1
        else:
            b.drop1()
            while not b.settled(all_blocks):
                b.drop1()
                
dependencies = {i:set() for i in brick_map}
dependers = {i:set() for i in brick_map}
for top in bricks:
    top_id = top.id
    for bottom in bricks:
        bottom_id = bottom.id
        if len(bottom.blocks.intersection(top.deps)) > 0:
            dependencies[top_id].add(bottom_id)
            dependers[bottom_id].add(top_id)
            
vital_bricks = set()
for b_id in brick_map:
    if len(dependencies[b_id]) == 1:
        vital_bricks.add(list(dependencies[b_id])[0])

nonvital_bricks = frozenset(brick_map.keys()) - frozenset(vital_bricks)    
print(f"There are {len(nonvital_bricks)} bricks that can be safely deleted.")

reaction_counts = {}
for starter in vital_bricks:
    removed_set = set([starter])
    last_removed_set_size = 0
    while last_removed_set_size < len(removed_set):
        last_removed_set_size = len(removed_set)
        remaining_bricks = set(brick_map.keys()).difference(removed_set)
        for b in remaining_bricks:
            if len(dependencies[b]) > 0 and len(dependencies[b].difference(removed_set)) == 0:
                removed_set.add(b)
    reaction_counts[starter] = len(removed_set) - 1

reaction_count_sum = sum(c for c in reaction_counts.values())
print(f"The sum of the number of blocks that would fall from deleting each brick is {reaction_count_sum}.")