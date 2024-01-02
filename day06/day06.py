times = []
dists = []
with open("input.txt") as f:
    times = [int(n) for n in f.readline().replace("Time:","").strip().split(" ") if len(n) > 0]
    dists = [int(n) for n in f.readline().replace("Distance:","").strip().split(" ") if len(n) > 0]
records = [0 for n in times]

for i in range(len(times)):
    for charging_time in range(0,times[i]+1):
        distance = charging_time * (times[i] - charging_time)
        if distance > dists[i]:
            records[i] = records[i] + 1

product = 1
for r in records: product *= r
print(f"The product of all potential records of each race is {product}.")

big_time = 0
big_dist = 0
big_records = 0
with open("input.txt") as f:
    big_time = int(f.readline().replace("Time:","").strip().replace(" ",""))
    big_dist = int(f.readline().replace("Distance:","").strip().replace(" ",""))

print(f"Inefficiently calculating all possible records ({big_time} iterations)...")
for charging_time in range(0,big_time+1):
    distance = charging_time * (big_time - charging_time)
    if distance > big_dist:
        big_records += 1
print(f"The number of possible records for the big race is {big_records}.")