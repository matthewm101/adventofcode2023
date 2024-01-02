def asciihash(s):
    v = 0
    for c in s:
        v = (v + ord(c)) * 17 % 256
    return v

steps = []
with open("input.txt") as f:
    steps = f.readline().strip().split(",")
    
hashes = [asciihash(s) for s in steps]
hash_sum = sum(hashes)
print(f"The sum of all hashes is {hash_sum}.")

hashmap = [[] for i in range(256)]
for step in steps:
    if '-' in step:
        name = step[:-1]
        h = asciihash(name)
        for item in hashmap[h]:
            if item[0] == name:
                hashmap[h].remove(item)
                break
    else:
        splits = step.split("=")
        name = splits[0]
        fl = int(splits[1])
        h = asciihash(name)
        for i in range(len(hashmap[h])):
            if hashmap[h][i][0] == name:
                hashmap[h][i] = (name,fl)
                break
        else:
            hashmap[h].append((name,fl))

total_power = 0
for boxno, box in enumerate(hashmap):
    for slotno, item in enumerate(box):
        total_power += (boxno + 1) * (slotno + 1) * item[1]

print(f"The total focusing power is {total_power}.")