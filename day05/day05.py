def filter_invalid_ranges(l):
    return [r for r in l if r[0] <= r[1]]

def merge_ranges(l):
    l = sorted(l)
    i = 0
    while i < len(l) - 1:
        if l[i][1] > l[i+1][0]:
            l[i] = (l[i][0],max(l[i+1][1],l[i][1]))
            l.pop(i+1)
        else:
            i += 1
    return l

class RangeMap:
    def __init__(self, dst_start, src_start, length) -> None:
        self.new_start = dst_start
        self.new_end = dst_start + length - 1
        self.start = src_start
        self.length = length
        self.end = src_start + length - 1
        self.before_start = self.start - 1
        self.after_end = self.end + 1
        self.offset = dst_start - src_start
    
    def calc_map(self, x):
        offset = x - self.start
        if 0 <= offset < self.length:
            return self.new_start + offset
        return None
    
    def calc_map_range(self, rng): # rng is a tuple: (inclusive start, inclusive end)
        # returns a tuple with two lists:
        # a list of all mapped ranges (will either have 0 or 1 entries)
        # a list of all unmapped ranges (will either have 0, 1, or 2 entries)
        start = rng[0]
        end = rng[1]
        if start > self.end or end < self.start:
            return ([],[rng])
        to_be_mapped_start = max(start,self.start)
        to_be_mapped_end = min(end,self.end)
        mapped_ranges = [(to_be_mapped_start + self.offset, to_be_mapped_end + self.offset)]
        unmapped_ranges = [(start,self.before_start),(self.after_end,end)]
        result = (filter_invalid_ranges(mapped_ranges),filter_invalid_ranges(unmapped_ranges))
        return result
    
    def __str__(self):
        return f"{self.src_start}+{self.length}->{self.dst_start}"
    

lines = []
with open("input.txt") as f:
    lines = [l.replace("\n","") for l in f if l != "\n"]
seeds = [int(s) for s in lines[0].split(": ")[1].split(" ")]

i = 2
seed_to_soil = []
while lines[i] != "soil-to-fertilizer map:":
    splits = [int(n) for n in lines[i].split(" ")]
    seed_to_soil.append(RangeMap(splits[0], splits[1], splits[2]))
    i += 1

i += 1
soil_to_fert = []
while lines[i] != "fertilizer-to-water map:":
    splits = [int(n) for n in lines[i].split(" ")]
    soil_to_fert.append(RangeMap(splits[0], splits[1], splits[2]))
    i += 1
    
i += 1
fert_to_water = []
while lines[i] != "water-to-light map:":
    splits = [int(n) for n in lines[i].split(" ")]
    fert_to_water.append(RangeMap(splits[0], splits[1], splits[2]))
    i += 1
    
i += 1
water_to_light = []
while lines[i] != "light-to-temperature map:":
    splits = [int(n) for n in lines[i].split(" ")]
    water_to_light.append(RangeMap(splits[0], splits[1], splits[2]))
    i += 1
    
i += 1
light_to_temp = []
while lines[i] != "temperature-to-humidity map:":
    splits = [int(n) for n in lines[i].split(" ")]
    light_to_temp.append(RangeMap(splits[0], splits[1], splits[2]))
    i += 1
    
i += 1
temp_to_humid = []
while lines[i] != "humidity-to-location map:":
    splits = [int(n) for n in lines[i].split(" ")]
    temp_to_humid.append(RangeMap(splits[0], splits[1], splits[2]))
    i += 1
    
i += 1
humid_to_loc = []
while i < len(lines):
    splits = [int(n) for n in lines[i].split(" ")]
    humid_to_loc.append(RangeMap(splits[0], splits[1], splits[2]))
    i += 1
    
def use_rangemaps(inputs, rangemaps):
    outputs = []
    for i in inputs:
        output = i
        for m in rangemaps:
            res = m.calc_map(i)
            if res is not None:
                output = res
                break
        outputs.append(output)
    return outputs

soils = use_rangemaps(seeds,seed_to_soil)
ferts = use_rangemaps(soils,soil_to_fert)
waters = use_rangemaps(ferts,fert_to_water)
lights = use_rangemaps(waters,water_to_light)
temps = use_rangemaps(lights,light_to_temp)
humids = use_rangemaps(temps,temp_to_humid)
locs: list[int] = use_rangemaps(humids,humid_to_loc)

lowest_loc = sorted(locs)[0]
print(f"The lowest location number from any of the initial seeds is {lowest_loc}.")

def use_rangemaps_ranges(inputs, rangemaps):
    outputs = []
    curr_inputs = inputs
    for m in rangemaps:
        next_inputs = []
        for i in curr_inputs:
            (new_output, more_input) = m.calc_map_range(i)
            for o in new_output:
                outputs.append(o)
            for mi in more_input:
                next_inputs.append(mi)
        curr_inputs = next_inputs
    for i in curr_inputs:
        outputs.append(i)
    return outputs

seed_ranges = [(seeds[i],seeds[i]+seeds[i+1]-1) for i in range(0,len(seeds),2)]
soil_ranges = merge_ranges(use_rangemaps_ranges(seed_ranges,seed_to_soil))
fert_ranges = merge_ranges(use_rangemaps_ranges(soil_ranges,soil_to_fert))
water_ranges = merge_ranges(use_rangemaps_ranges(fert_ranges,fert_to_water))
light_ranges = merge_ranges(use_rangemaps_ranges(water_ranges,water_to_light))
temp_ranges = merge_ranges(use_rangemaps_ranges(light_ranges,light_to_temp))
humid_ranges = merge_ranges(use_rangemaps_ranges(temp_ranges,temp_to_humid))
loc_ranges = merge_ranges(use_rangemaps_ranges(humid_ranges,humid_to_loc))
lowest_loc = min([n[0] for n in loc_ranges])
print(f"The lowest location number from any of the initial seed ranges is {lowest_loc}.")