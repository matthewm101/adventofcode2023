
class Game:
    def __init__(self, id, rounds):
        self.id = id
        self.rounds = rounds
    
    def is_possible(self, max_reds, max_greens, max_blues) -> bool:
        for round in self.rounds:
            if round[0] > max_reds or round[1] > max_greens or round[2] > max_blues:
                return False
        return True
    
    def fewest_cubes_power(self) -> int:
        fewest_red = 0
        fewest_green = 0
        fewest_blue = 0
        for round in self.rounds:
            fewest_red = max(fewest_red, round[0])
            fewest_green = max(fewest_green, round[1])
            fewest_blue = max(fewest_blue, round[2])
        return fewest_red * fewest_green * fewest_blue

possible_sum = 0
power_sum = 0

with open("input.txt") as f:
    for line in f:
        line = line.replace(" ","").replace("Game","").replace("blue","B").replace("green","G").replace("red","R").replace("\n","")
        game_and_rounds = line.split(":") # Split 0: the game number, split 1: the rest
        raw_rounds = game_and_rounds[1].split(";")
        rounds = []
        for raw_round in raw_rounds:
            colors = raw_round.split(",")
            red = 0
            green = 0
            blue = 0
            for color in colors:
                if color[-1] == 'R':
                    red = int(color[:-1])
                elif color[-1] == 'G':
                    green = int(color[:-1])
                elif color[-1] == 'B':
                    blue = int(color[:-1])
            rounds.append((red,green,blue))
        game = Game(int(game_and_rounds[0]), rounds)
        if game.is_possible(12,13,14):
            possible_sum += game.id
        power_sum += game.fewest_cubes_power()
            
print(f"The sum of the IDs of all possible games is {possible_sum}.")
print(f"The sum of all powers is {power_sum}.")