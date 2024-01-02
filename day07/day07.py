def hand_type_to_value(t) -> int:
    if t == [5] or t == [4] or t == [3] or t == [2] or t == [1] or t == []:
        return 13**5*6
    elif t == [1,4] or t == [1,3] or t == [1,2] or t == [1,1]:
        return 13**5*5
    elif t == [2,3] or t == [2,2]:
        return 13**5*4
    elif t == [1,1,3] or t == [1,1,2] or t == [1,1,1]:
        return 13**5*3
    elif t == [1,2,2]:
        return 13**5*2
    elif t == [1,1,1,2] or t == [1,1,1,1]:
        return 13**5
    return 0

def hand_to_int(hand: str) -> int:
    key = "23456789TJQKA"
    freqs = {}
    val = 0
    for c in hand:
        n = key.find(c)
        val = val * 13 + n
        if n in freqs:
            freqs[n] = freqs[n] + 1
        else:
            freqs[n] = 1
    hand_type = sorted(freqs.values())
    val += hand_type_to_value(hand_type)
    return val

def hand_to_int_with_jokers(hand: str) -> int:
    key = "J23456789TQKA"
    freqs = {}
    val = 0
    for c in hand:
        n = key.find(c)
        val = val * 13 + n
        if n > 0:
            if n in freqs:
                freqs[n] = freqs[n] + 1
            else:
                freqs[n] = 1
    hand_type = sorted(freqs.values())
    val += hand_type_to_value(hand_type)
    return val

hand_bids = []
joker_hand_bids = []
with open("input.txt") as f:
    for line in f:
        splits = line.strip().split(" ")
        hand_int = hand_to_int(splits[0])
        joker_hand_int = hand_to_int_with_jokers(splits[0])
        bid = int(splits[1])
        hand_bids.append((hand_int,bid))
        joker_hand_bids.append((joker_hand_int,bid))

hand_bids.sort()
winnings = 0
for i, h in enumerate(hand_bids, start=1):
    winnings += i * h[1]

print(f"The total winnings is {winnings}.")

joker_hand_bids.sort()
winnings = 0
for i, h in enumerate(joker_hand_bids, start=1):
    winnings += i * h[1]
    
print(f"The total winnings with jokers is {winnings}.")