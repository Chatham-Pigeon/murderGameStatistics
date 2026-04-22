from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages, join_with_final


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
time = "48d"
moderators = ['JJJT', "Darqnt", "AutumnsBreeze", "Chatham_Pigeon", "nvct", "Ace127", "Jeffree225", "pixlii", "KabanFriends"]
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
moderator_teams = {}

max_streaks = {}  # {x: {'has': 0, 'without': 0}}
current_streaks = {}

for roundID, moderators_in_round in round_with_moderators.items():
    moderators_in_round = list(set(moderators_in_round))
    max_count = len(moderators_in_round)
    if not max_count in [0,]:
        if not tuple(moderators_in_round) in moderator_teams:
            moderator_teams[tuple(moderators_in_round)] = 0
        moderator_teams[tuple(moderators_in_round)] += 1
    if not max_count in rounds_with_moderators_count:
        rounds_with_moderators_count[max_count] = 0
    rounds_with_moderators_count[max_count] += 1

    for x in range(1, 6):
        if x not in max_streaks:
            max_streaks[x] = {'has': 0, 'without': 0}
            current_streaks[x] = {'has': 0, 'without': 0}
        if current_streaks[x]['has'] > max_streaks[x]['has']:
            max_streaks[x]['has'] = current_streaks[x]['has']
        if current_streaks[x]['without'] > max_streaks[x]['without']:
            max_streaks[x]['without'] = current_streaks[x]['without']
        if max_count >= x:
            current_streaks[x]['has'] += 1
            current_streaks[x]['without'] = 0
        else:
            current_streaks[x]['has'] = 0
            current_streaks[x]['without'] += 1

for x in current_streaks:
    if current_streaks[x]['has'] > max_streaks[x]['has']:
        max_streaks[x]['has'] = current_streaks[x]['has']
    if current_streaks[x]['without'] > max_streaks[x]['without']:
        max_streaks[x]['without'] = current_streaks[x]['without']



total_count = len(round_with_moderators)
print(f"Total Rounds: {total_count}\n")

print("Percent of rounds with atleast x moderators:")
rounds_with_moderators_count =  sort_dict_by_key(rounds_with_moderators_count, False)
for count, amount in rounds_with_moderators_count.items():
    if count == 0:
        continue
    print(f"{count}: {round(sum(list(rounds_with_moderators_count.values())[count:])/total_count*100,2)}% ({sum(list(rounds_with_moderators_count.values())[count:])})")

print("")
moderators_played_rounds_count = {}
for name, round_list in moderators_played_rounds.items():
    moderators_played_rounds_count[name] = len(round_list)
print("Moderator played rounds (percent of all games)")
for name, amount in sort(moderators_played_rounds_count).items():
    print(f"{name}: {amount} ({round(amount/total_count*100,2)}%)")

print("\nModerator group, amount of games played (percent of all games) \n")
for moderator_team, amount in sorted(moderator_teams.items(), key=lambda x: (len(x[0]), -x[1])):
    print(f"{join_with_final(list(moderator_team), ', ', ' & ')}: {amount} ({round(amount/total_count*100,2)}%)")
print("\nLongest streak with / without x moderators")
for x, streaks in max_streaks.items():
    print(f"{x}: with: {streaks['has']}, without: {streaks['without']}")