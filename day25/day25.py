graph = {}
connections = set()

def make_edge(a,b):
    return tuple(sorted([a,b]))

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0: continue
        left, right = tuple(line.split(": "))
        rights = right.split(" ")
        for r in rights:
            if left in graph:
                graph[left].add(r)
            else:
                graph[left] = set([r])
            if r in graph:
                graph[r].add(left)
            else:
                graph[r] = set([left])
            connections.add(make_edge(left,r))
vertices = list(graph.keys())
vertex_set = frozenset(vertices)

def bfs(start: str, end: str, edges: frozenset[tuple[str,str]]):
    # State format: current node, visited nodes, visited edges
    frontier = [(start,frozenset([start]),frozenset())]
    collective_seen = {start}
    while len(frontier) > 0:
        new_frontier = []
        for curr, seen_vertices, seen_edges in frontier:
            if curr == end: return seen_edges
            for next in graph[curr] - collective_seen:
                e = make_edge(curr,next)
                if e in edges:
                    new_frontier.append((next,seen_vertices.union({next}),seen_edges.union({e})))
                    collective_seen.add(next)
        frontier = new_frontier
    return None
                

def partition_search(start: str, seen: frozenset[str], edges: frozenset[tuple[str,str]]):
    for next in graph[start]:
        if next not in seen:
            e = make_edge(start,next)
            if e in edges:
                seen = seen | partition_search(next, seen | {next}, edges)
    return seen

def find_three_cut(start,end):
    first_path = bfs(start, end, connections)
    second_path = bfs(start, end, connections.difference(set(first_path)))
    third_path = bfs(start, end, connections.difference(set(first_path), set(second_path)))
    should_be_none = bfs(start, end, connections.difference(set(first_path), set(second_path), set(third_path)))
    if should_be_none is None:
        part_a = partition_search(start, frozenset({start}), connections.difference(set(first_path), set(second_path), set(third_path)))
        part_b = partition_search(end, frozenset({end}), connections.difference(set(first_path), set(second_path), set(third_path)))
        cut = []
        for a in part_a:
            for b in part_b:
                e = make_edge(a,b)
                if e in connections:
                     cut.append(e)
        if len(part_a) + len(part_b) == len(vertices) and len(cut) == 3:
            return cut, part_a, part_b
    return None, None, None

for i in range(len(vertices)-1):
    for j in range(i+1,len(vertices)):
        cut, part_a, part_b = find_three_cut(vertices[i], vertices[j])
        if cut is not None:
            print(f"The three wires to disconnect are {cut[0]}, {cut[1]}, and {cut[2]}.")
            print(f"This breaks the components into groups of {len(part_a)} and {len(part_b)}, multiplying to {len(part_a)*len(part_b)}.")
            exit(0)