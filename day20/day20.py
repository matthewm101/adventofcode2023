graph = {}
reverse_graph = {}
module_types = {}
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0: continue
        splits = line.split(" -> ")
        typename = splits[0]
        name = typename
        if typename[0] == '&' or typename[0] == '%':
            name = typename[1:]
            module_types[name] = typename[0]
        graph[name] = splits[1].split(", ")

outputs = set()
for ns in graph.values():
    for n in ns:
        outputs.add(n)
for o in outputs:
    reverse_graph[o] = [m for m in graph if o in graph[m]]

flip_states = {m:False for m in module_types if module_types[m] == '%'}
conj_states = {m:{n:False for n in reverse_graph[m]} for m in module_types if module_types[m] == '&'}

low_pulses = 0
high_pulses = 0
for i in range(1000):
    low_pulses += 1 + len(graph["broadcaster"]) # Accounts for button push and low pulses sent from the broadcaster initially
    queue = [("broadcaster",False,n) for n in graph["broadcaster"]]
    while len(queue) > 0:
        new_queue = []
        for src, power, dst in queue:
            if dst not in module_types: continue
            if module_types[dst] == '%' and not power:
                flip_states[dst] = not flip_states[dst]
                for next_dst in graph[dst]:
                    new_queue.append((dst,flip_states[dst],next_dst))
                    # new_queue[next_dst] = (flip_states[dst],dst)
                if flip_states[dst]:
                    high_pulses += len(graph[dst])
                else:
                    low_pulses += len(graph[dst])
            if module_types[dst] == '&':
                conj_states[dst][src] = power
                result = not all(conj_states[dst].values())
                for next_dst in graph[dst]:
                    new_queue.append((dst,result,next_dst))
                    # new_queue[next_dst] = (result,dst)
                if result:
                    high_pulses += len(graph[dst])
                else:
                    low_pulses += len(graph[dst])
        queue = new_queue

print(f"{low_pulses} low and {high_pulses} high pulses were sent, multiplying to {low_pulses * high_pulses}.")

flip_states = {m:False for m in module_types if module_types[m] == '%'}
conj_states = {m:{n:False for n in reverse_graph[m]} for m in module_types if module_types[m] == '&'}


rx_parent = reverse_graph["rx"][0]
pushes_until_rx_parent_activates = {p:0 for p in reverse_graph[rx_parent]}
i = 0
while any(p[1] == 0 for p in pushes_until_rx_parent_activates.items()):
    i += 1
    low_pulses += 1 + len(graph["broadcaster"]) # Accounts for button push and low pulses sent from the broadcaster initially
    queue = [("broadcaster",False,n) for n in graph["broadcaster"]]
    while len(queue) > 0:
        new_queue = []
        for src, power, dst in queue:
            if dst not in module_types: continue
            if module_types[dst] == '%' and not power:
                flip_states[dst] = not flip_states[dst]
                for next_dst in graph[dst]:
                    new_queue.append((dst,flip_states[dst],next_dst))
            if module_types[dst] == '&':
                conj_states[dst][src] = power
                result = not all(conj_states[dst].values())
                for next_dst in graph[dst]:
                    new_queue.append((dst,result,next_dst))
        queue = new_queue
        if any((not s[1] and (s[2] == 'rx')) for s in queue):
            min_rx_pulses = i
        for src, power, dst in queue:
            if dst == rx_parent and power and pushes_until_rx_parent_activates[src] == 0:
                pushes_until_rx_parent_activates[src] = i
    
from math import lcm
min_rx_pulses = lcm(*pushes_until_rx_parent_activates.values())
print(f"The minimum number of pulses needed to make rx receive a low pulse is {min_rx_pulses}.")