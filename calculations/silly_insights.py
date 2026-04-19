from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages


class log:
    def __init__(self, raw_data: str):
        self.bowsShot = 0
        self.bowsLanded = 0
        self.timeAlive = 0
        self.role = None
        self.gameRound = None
        self.timestamp = None
        self.winTeam = None
        self.name = None
        self.alive = None
        self.won = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")


log_name = "player-stats"
time = "30d"
moderators = ['JJJT', "Darqnt", "AutumnsBreeze", "Chatham_Pigeon", "nvct", "Ace127", "Jeffree225", "pixlii"]
with open(fr'../data/{time}.{log_name}-data.txt', 'r', encoding='utf-8') as f:
    round_with_moderators = {   }
    for line in f:
        stats = log(line)
        if not stats.gameRound in round_with_moderators:
            round_with_moderators[stats.gameRound] = []
        if stats.name in moderators:
            round_with_moderators[stats.gameRound].append(stats.name)
print(len(round_with_moderators))
rounds_with_moderators_count = {}
for roundID, moderators_in_round in round_with_moderators.items():
    moderators_in_round = list(set(moderators_in_round))
    for idx in range(0,8):
        if len(moderators_in_round) >= idx:
            max_count = idx
            if max_count >= 5:
                print(f"{roundID}: {moderators_in_round}")
    if not max_count in rounds_with_moderators_count:
        rounds_with_moderators_count[max_count] = 0
    rounds_with_moderators_count[max_count] += 1

for count, amount in rounds_with_moderators_count.items():
    print(f"Rounds with {count} moderators: {amount}")

