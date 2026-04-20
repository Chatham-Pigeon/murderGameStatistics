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
    round_with_moderators = {}
    moderators_played_rounds = {}
    for line in f:
        stats = log(line)
        if not stats.gameRound in round_with_moderators:
            round_with_moderators[stats.gameRound] = []
        if stats.name in moderators:
            if stats.gameRound in list(round_with_moderators.keys()):
                round_with_moderators[stats.gameRound].append(stats.name)
            if not stats.name in moderators_played_rounds:
                moderators_played_rounds[stats.name] = []
            moderators_played_rounds[stats.name].append(stats.gameRound)


rounds_with_moderators_count = {}
for roundID, moderators_in_round in round_with_moderators.items():
    moderators_in_round = list(set(moderators_in_round))
    for idx in range(0,8):
        if len(moderators_in_round) >= idx:
            max_count = idx
    if not max_count in rounds_with_moderators_count:
        rounds_with_moderators_count[max_count] = 0
    rounds_with_moderators_count[max_count] += 1

total_count = len(round_with_moderators)
print(f"Total Rounds: {total_count}\n")

rounds_with_moderators_count =  sort_dict_by_key(rounds_with_moderators_count, False)
for count, amount in rounds_with_moderators_count.items():
    if count == 0:
        continue
    print(f"Percent of rounds with atleast {count} moderators: {round(sum(list(rounds_with_moderators_count.values())[count:])/total_count*100,2)}% ({sum(list(rounds_with_moderators_count.values())[count:])})")

print("")
moderators_played_rounds_count = {}
for name, round_list in moderators_played_rounds.items():
    moderators_played_rounds_count[name] = len(round_list)

for name, amount in sort(moderators_played_rounds_count).items():
    print(f"{name} played {amount} rounds ({round(amount/total_count*100,2)}% of all rounds)")
