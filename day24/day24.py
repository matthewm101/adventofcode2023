class Stone:
    def __init__(self,p,v) -> None:
        self.p0 = p
        self.v0 = v

from fractions import Fraction

def check_intersection_xy(stone1: Stone, stone2: Stone):
    x1, x2 = stone1.p0[0], stone2.p0[0]
    y1, y2 = stone1.p0[1], stone2.p0[1]
    vx1, vx2 = stone1.v0[0], stone2.v0[0]
    vy1, vy2 = stone1.v0[1], stone2.v0[1]
    
    numerator = ((y1 - y2) * vx2) + ((x2 - x1) * vy2)
    denominator = (vy2 * vx1) - (vy1 * vx2)
    if denominator == 0: return False
    t1 = Fraction(numerator, denominator)
    x_int = x1 + vx1 * t1
    y_int = y1 + vy1 * t1
    t2 = (x_int - x2) / vx2
    upper = 400000000000000
    lower = 200000000000000
    return t1 > 0 and t2 > 0 and x_int >= lower and x_int <= upper and y_int >= lower and y_int <= upper

stones = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0: continue
        p, v = tuple(line.split(" @ "))
        p = [int(pp) for pp in p.split(", ")]
        v = [int(vv) for vv in v.split(", ")]
        stones.append(Stone(p,v))

intersections = 0
for i in range(len(stones)-1):
    for j in range(i+1,len(stones)):
        if check_intersection_xy(stones[i],stones[j]):
            intersections += 1
            
print(f"There are {intersections} x-y intersections in the test area.")

print(f"Solving the second part, please wait...")
import z3 as solver # whoops, kinda want z3 as a variable name
xp, yp, zp, vxp, vyp, vzp = solver.Ints('xp yp zp vxp vyp vzp')
t1, t2, t3 = solver.Ints('t1 t2 t3')
x1, y1, z1, x2, y2, z2, x3, y3, z3 = solver.Ints('x1 y1 z1 x2 y2 z2 x3 y3 z3')
vx1, vy1, vz1, vx2, vy2, vz2, vx3, vy3, vz3 = solver.Ints('vx1 vy1 vz1 vx2 vy2 vz2 vx3 vy3 vz3')
s = solver.Solver()

ranked_stones = [(sum([abs(v) for v in s.v0]), n) for n,s in enumerate(stones)]
ranked_stones.sort()
easy_stones = [stones[n] for _, n in ranked_stones[:3]]

s.add(
    xp + vxp * t1 == x1 + vx1 * t1,
    yp + vyp * t1 == y1 + vy1 * t1,
    zp + vzp * t1 == z1 + vz1 * t1,
    xp + vxp * t2 == x2 + vx2 * t2,
    yp + vyp * t2 == y2 + vy2 * t2,
    zp + vzp * t2 == z2 + vz2 * t2,
    xp + vxp * t3 == x3 + vx3 * t3,
    yp + vyp * t3 == y3 + vy3 * t3,
    zp + vzp * t3 == z3 + vz3 * t3,
    t1 > 0, t2 > 0, t3 > 0,
    x1 == easy_stones[0].p0[0], x2 == easy_stones[1].p0[0], x3 == easy_stones[2].p0[0],
    y1 == easy_stones[0].p0[1], y2 == easy_stones[1].p0[1], y3 == easy_stones[2].p0[1],
    z1 == easy_stones[0].p0[2], z2 == easy_stones[1].p0[2], z3 == easy_stones[2].p0[2],
    vx1 == easy_stones[0].v0[0], vx2 == easy_stones[1].v0[0], vx3 == easy_stones[2].v0[0],
    vy1 == easy_stones[0].v0[1], vy2 == easy_stones[1].v0[1], vy3 == easy_stones[2].v0[1],
    vz1 == easy_stones[0].v0[2], vz2 == easy_stones[1].v0[2], vz3 == easy_stones[2].v0[2]
)

assert s.check() == solver.sat
m = s.model()
x, y, z, vx, vy, vz = m.evaluate(xp), m.evaluate(yp), m.evaluate(zp), m.evaluate(vxp), m.evaluate(vyp), m.evaluate(vzp)
print(f"To hit all the hailstones, the rock must start at ({x},{y},{z}) with a velocity of ({vx},{vy},{vz}).")
print(f"The sum of all the starting position dimensions is {(x.as_long()+y.as_long()+z.as_long())}.")
