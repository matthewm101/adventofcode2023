rules = {} # Input: rule name. Output: array of rule steps. 
# Each rule step is a tuple: (cond,num,result). Cond is a letter in 'xmas' plus '<' or '>'. num is a number that goes with the cond. result is either 'A', 'D', or the name of another rule. The last rule will always succeed (x>0).
items = []

with open("input.txt") as f:
    for line in f:
        if len(line.strip()) == 0:
            break
        line = line.strip().replace("}","")
        splits = line.split("{")
        rule_name = splits[0]
        raw_rules = splits[1].split(",")
        rule_steps = []
        for step in raw_rules[:-1]:
            splits = step.split(":")
            cond = splits[0][:2]
            num = int(splits[0][2:])
            result = splits[1]
            rule_steps.append((cond,num,result))
        rule_steps.append(("x>",0,raw_rules[-1]))
        rules[rule_name] = rule_steps
    
    for line in f:
        line = line.strip().replace("{x=","").replace("m=","").replace("a=","").replace("s=","").replace("}","")
        items.append(tuple([int(x) for x in line.split(",")]))
            
def test(i):
    x = i[0]
    m = i[1]
    a = i[2]
    s = i[3]
    state = "in"
    while state != 'A' and state != 'R':
        rule = rules[state]
        for step in rule:
            match step[0]:
                case 'x>':
                    if x > step[1]: state = step[2]; break
                case 'x<':
                    if x < step[1]: state = step[2]; break
                case 'm>':
                    if m > step[1]: state = step[2]; break
                case 'm<':
                    if m < step[1]: state = step[2]; break
                case 'a>':
                    if a > step[1]: state = step[2]; break
                case 'a<':
                    if a < step[1]: state = step[2]; break
                case 's>':
                    if s > step[1]: state = step[2]; break
                case 's<':
                    if s < step[1]: state = step[2]; break
                case _:
                    raise "unreachable"
    return state == 'A'

accepted_items = [i for i in items if test(i)]
value_sum = sum([sum(i) for i in accepted_items])
print(f"The sum of the rating numbers of all accepted items is {value_sum}.")

def process_stated_range(r):
    state = r[0]
    lx = r[1]
    ux = r[2]
    lm = r[3]
    um = r[4]
    la = r[5]
    ua = r[6]
    ls = r[7]
    us = r[8]
    outputs = []
    rule = rules[state]
    for step in rule:
        match step[0]:
            case 'x>':
                if lx > step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif ux > step[1] and step[1] >= lx:
                    outputs.append((step[2],step[1]+1,ux,lm,um,la,ua,ls,us))
                    ux = step[1]
            case 'x<':
                if ux < step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif lx < step[1] and step[1] <= ux:
                    outputs.append((step[2],lx,step[1]-1,lm,um,la,ua,ls,us))
                    lx = step[1]
            case 'm>':
                if lm > step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif um > step[1] and step[1] >= lm:
                    outputs.append((step[2],lx,ux,step[1]+1,um,la,ua,ls,us))
                    um = step[1]
            case 'm<':
                if um < step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif lm < step[1] and step[1] <= um:
                    outputs.append((step[2],lx,ux,lm,step[1]-1,la,ua,ls,us))
                    lm = step[1]
            case 'a>':
                if la > step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif ua > step[1] and step[1] >= la:
                    outputs.append((step[2],lx,ux,lm,um,step[1]+1,ua,ls,us))
                    ua = step[1]
            case 'a<':
                if ua < step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif la < step[1] and step[1] <= ua:
                    outputs.append((step[2],lx,ux,lm,um,la,step[1]-1,ls,us))
                    la = step[1]
            case 's>':
                if ls > step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif us > step[1] and step[1] >= ls:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,step[1]+1,us))
                    us = step[1]
            case 's<':
                if us < step[1]:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,us)); return outputs
                elif ls < step[1] and step[1] <= us:
                    outputs.append((step[2],lx,ux,lm,um,la,ua,ls,step[1]-1))
                    ls = step[1]
            case _:
                raise "unreachable"
    raise "unreachable"

range_queue = [("in",1,4000,1,4000,1,4000,1,4000)]
accepted_ranges = []
while len(range_queue) > 0:
    new_range_queue = []
    for old_r in range_queue:
        for new_r in process_stated_range(old_r):
            if new_r[0] == 'A':
                accepted_ranges.append(new_r)
            elif new_r[0] != 'R':
                new_range_queue.append(new_r)
    range_queue = new_range_queue

def size_range(r):
    lx = r[1]
    ux = r[2]
    lm = r[3]
    um = r[4]
    la = r[5]
    ua = r[6]
    ls = r[7]
    us = r[8]
    return (ux-lx+1)*(um-lm+1)*(ua-la+1)*(us-ls+1)

total_combs = sum([size_range(r) for r in accepted_ranges])
print(f"There are {total_combs} unique ratings that are accepted by the workflows.")