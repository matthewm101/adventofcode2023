class Symbol:
    def __init__(self, x, y, char) -> None:
        self.x = x
        self.y = y
        self.char = char
        
    def debug(self) -> str:
        return f"({self.x},{self.y})='{self.char}'"
    
    def pos(self) -> tuple[int,int]:
        return (self.x,self.y)

class Number:
    def __init__(self, x, y, width, num) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.num = num
        
    def get_adjacents(self) -> set[tuple[int,int]]:
        adjacents: set[tuple[int,int]] = set([(self.x-1,self.y),(self.x+self.width,self.y)])
        for i in range(-1,self.width+1):
            adjacents.add((self.x+i,self.y-1))
            adjacents.add((self.x+i,self.y+1))
        return adjacents
    
    def check_is_part_number(self, symbol_locs: set[tuple[int,int]]) -> bool:
        inter = symbol_locs.intersection(self.get_adjacents())
        return len(inter) > 0
    
    def debug(self) -> str:
        return f"({self.x}+{self.width},{self.y})={self.num}"
    
    def get_adjacent_gears(self, symbols: list[Symbol]) -> list[Symbol]:
        adjs = self.get_adjacents()
        adj_gears = []
        for s in symbols:
            if s.char == '*' and (s.x,s.y) in adjs:
                adj_gears.append(s)
        return adj_gears

numbers = []
symbols = []

with open("input.txt") as f:
    for y,line in enumerate(f):
        line = line[:-1] # strip \n
        acc = None
        start_x = 0
        for x in range(len(line)):
            if line[x].isdigit():
                if acc is None:
                    acc = int(line[x])
                    start_x = x
                else:
                    acc = acc * 10 + int(line[x])
            elif acc is not None:
                numbers.append(Number(start_x, y, x - start_x, acc))
                acc = None
            if not line[x].isdigit() and not line[x] == '.':
                symbols.append(Symbol(x, y, line[x]))
        if acc is not None:
            numbers.append(Number(start_x, y, len(line) - start_x, acc))

symbol_positions = set([s.pos() for s in symbols])
# for n in numbers:
#     print(f"{n.debug()} {n.check_is_part_number(symbol_positions)}")
part_numbers = [n for n in numbers if n.check_is_part_number(symbol_positions)]
part_number_sum = sum([n.num for n in part_numbers])
print(f"The sum of all part numbers is {part_number_sum}.")

numbers_per_pos = {}
for n in part_numbers:
    gear_candidates = n.get_adjacent_gears(symbols)
    for g in gear_candidates:
        if (g.x,g.y) in numbers_per_pos.keys():
            numbers_per_pos[(g.x,g.y)].append(n)
        else:
            numbers_per_pos[(g.x,g.y)] = [n]

gear_ratio_sum = 0
for adj_nums in numbers_per_pos.values():
    if len(adj_nums) == 2:
        gear_ratio_sum += adj_nums[0].num * adj_nums[1].num

print(f"The sum of all gear ratios is {gear_ratio_sum}.")
# print([n.debug() for n in numbers])
# print([s.debug() for s in symbols])
