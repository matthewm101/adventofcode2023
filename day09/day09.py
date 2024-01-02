rows = []
with open("input.txt") as f:
    for line in f:
        rows.append([int(n) for n in line.strip().split(" ")])

def extrapolate(l):
    if len([n for n in l if n != 0]) == 0:
        return 0
    return l[-1] + extrapolate([l[i+1] - l[i] for i in range(0,len(l)-1)])

extrapolations = [extrapolate(r) for r in rows]
extrapolated_sum = sum(extrapolations)

print(f"The sum of all the extrapolations is {extrapolated_sum}.")

def backwards_extrapolate(l):
    if len([n for n in l if n != 0]) == 0:
        return 0
    return l[0] - backwards_extrapolate([l[i+1] - l[i] for i in range(0,len(l)-1)])

extrapolations = [backwards_extrapolate(r) for r in rows]
extrapolated_sum = sum(extrapolations)

print(f"The sum of all backward extrapolations is {extrapolated_sum}.")