instructions = ""
lefts = {}
rights = {}

with open("input.txt") as f:
    instructions = f.readline().strip()
    f.readline()
    for l in f:
        if len(l) > 0:
            lefts[l[0:3]] = l[7:10]
            rights[l[0:3]] = l[12:15]

A_positions = [p for p in lefts.keys() if p[2] == 'A']
Z_positions = [p for p in lefts.keys() if p[2] == 'Z']
A_memo = {} # maps pos to (pos, steps taken)
Z_memo = {} # maps pos to steps taken. Note: while unspecified in the problem, it turns out that leaving a Z will always cause the next Z to be the same Z.
# Meaning, there is no need to keep track of which Z is encountered next, since it will always be the same Z.
# It also turns out that the cycle does not change after going from a Z position to itself, so I excluded the cycle from the key and just assume it is the same cycle obtained by going from A to Z.
for a_starting_pos in A_positions:
    pos = a_starting_pos
    cycle = 0
    steps_taken = 0
    while pos[2] != 'Z':
        if instructions[cycle] == "L":
            pos = lefts[pos]
        else:
            pos = rights[pos]
        cycle = (cycle + 1) % len(instructions)
        steps_taken += 1
    
    z_starting_pos = pos
    initial_steps_taken = steps_taken
    A_memo[a_starting_pos] = (z_starting_pos,steps_taken)
    
    force_loop = True
    while pos[2] != 'Z' or force_loop:
        force_loop = False
        if instructions[cycle] == "L":
            pos = lefts[pos]
        else:
            pos = rights[pos]
        cycle = (cycle + 1) % len(instructions)
        steps_taken += 1
    Z_memo[z_starting_pos] = steps_taken - initial_steps_taken


print(f"{A_memo['AAA'][1]} steps are required to go from AAA to ZZZ.")

Z_positions = [A_memo[p][0] for p in A_positions]
initial_steps = [A_memo[p][1] for p in A_positions]
initial_cycles = [s % len(instructions) for s in initial_steps]
cycle_wraparound_times = [] # For each i, represents the steps needed to go from the corresponding initial position and cycle to the exact same position and cycle.
# Big realization: there aren't any intermediate cycles! Meaning, the path taken from a node to itself when starting on a specific cycle will always end on that cycle. 
# Consequently, all steps taken to go from a node to itself is a multiple of the number of instructions.
for i, z_pos in enumerate(Z_positions):
    cycle_wraparound_times.append(Z_memo[z_pos])
    assert cycle_wraparound_times[-1] % len(instructions) == 0 # this proves that each transition from a state to itself preserves the cycle index

# Last big realization: the initial steps needed to get from any A to Z is exactly the same to get from Z to itself. So the answer is just the LCM of all the steps. Nice.
from math import lcm
repeat = lcm(*cycle_wraparound_times)

print(f"{repeat} steps are required for starters from all xxA positions to end up at xxZ positions.")
