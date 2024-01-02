original_positions = []
original_xs = set()
original_ys = set()

with open("input.txt") as f:
    for y,line in enumerate(f):
        line = line.strip()
        for x,c in enumerate(line):
            if c == '#':
                original_positions.append((x,y))
                original_xs.add(x)
                original_ys.add(y)



def compute_expansion(amount):
    x_booster = []
    y_booster = []
    for x in range(max(original_xs)+1):
        if len([p for p in original_positions if p[0] == x]) == 0:
            if len(x_booster) > 0:
                x_booster.append(x_booster[-1] + amount)
            else:
                x_booster.append(amount)
        else:
            if len(x_booster) > 0:
                x_booster.append(x_booster[-1])
            else:
                x_booster.append(0)
    for y in range(max(original_ys)+1):
        if len([p for p in original_positions if p[1] == y]) == 0:
            if len(y_booster) > 0:
                y_booster.append(y_booster[-1] + amount)
            else:
                y_booster.append(amount)
        else:
            if len(y_booster) > 0:
                y_booster.append(y_booster[-1])
            else:
                y_booster.append(0)
    new_positions = []
    for x,y in original_positions:
        xx = x + x_booster[x]
        yy = y + y_booster[y]
        new_positions.append((xx,yy))
    return new_positions

new_positions = compute_expansion(1)
total_pairwise_distance = 0
for i in range(len(new_positions)-1):
    for j in range(i+1,len(new_positions)):
        total_pairwise_distance += abs(new_positions[i][0] - new_positions[j][0]) + abs(new_positions[i][1] - new_positions[j][1])
print(f"The total distance between all pairs of galaxies after empty rows/columns are doubled is {total_pairwise_distance}.")

new_positions = compute_expansion(999999)
total_pairwise_distance = 0
for i in range(len(new_positions)-1):
    for j in range(i+1,len(new_positions)):
        total_pairwise_distance += abs(new_positions[i][0] - new_positions[j][0]) + abs(new_positions[i][1] - new_positions[j][1])
print(f"The total distance between all pairs of galaxies after empty rows/columns are 1000000x'd is {total_pairwise_distance}.")