class Card:
    def __init__(self, id, winners, numbers) -> None:
        self.id = id
        self.winners = set(winners)
        self.numbers = list(numbers)
        self.matches = len([n for n in self.numbers if n in self.winners])
        
    def score(self) -> int:
        if self.matches == 0: return 0
        else: return 2 ** (self.matches - 1)
        
    def successors(self, highest_id) -> list[int]:
        return list(range(self.id+1,min(highest_id+1,self.id+1+self.matches)))
        
        
def filter_empty(l) -> list[str]:
    return [n for n in l if n != ""]

cards = []
cards_dict = {}

with open("input.txt") as f:
    for line in f:
        id_and_values = line.replace("\n","").split(":")
        wins_and_nums = id_and_values[1].split("|")
        wins = filter_empty(wins_and_nums[0].split(" "))
        nums = filter_empty(wins_and_nums[1].split(" "))
        id = int(filter_empty(id_and_values[0].split(" "))[1])
        cards.append(Card(id,wins,nums))
        cards_dict[id] = cards[-1]

total_points = sum([c.score() for c in cards])
print(f"The total points across all cards is {total_points}.")

max_id = max([n.id for n in cards])
card_counts = {n.id:1 for n in cards}
for i in range(1, max_id+1):
    succs = cards_dict[i].successors(max_id)
    for succ in succs:
        card_counts[succ] += card_counts[i]
        
total_cards = sum(card_counts.values())
print(f"After duplicating all cards, there are {total_cards} in total.")