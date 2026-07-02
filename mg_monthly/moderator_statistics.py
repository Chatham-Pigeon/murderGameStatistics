from helper_functions import sort, sort_dict_by_key, join_with_final
from SECRETS import *

class log:
    def __init__(self, raw_data: dict):
        self.gameRound = 0
        self.name = None
        self.role = None
        self.won = None
        self.totalDamageDealt = 0
        self.damageReceived = None
        self.healthHealed = None
        self.bowsShot = None
        self.bowsLanded = None
        self.meleeAttempts = None
        self.meleeSuccesses = None
        self.playersKilled = None
        self.timeAlive = None
        self.purchases = None
        self.gameRound = None
        self.map = None
        self.winner = None
        self.fiend = None
        self.length = None
        self.playercount = None
        self.timestamp = None
        self.gameType = None
        self.plotID = None
        self.winReason = None
        for key, value in raw_data.items():
            setattr(self, key, value)
MODERATORS = ["JJJT", "Chatham_Pigeon", "nvct", "pixlii", "Darqnt", "Jeffree225", "AutumnsBreeze", "Ace127"]
rows = query(f"""
    SELECT pr.*, g.*
    FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID} AND g.timestamp >= {START_TIME}""")

rounds_with_moderators = {}
moderator_round_count = {mod: 0 for mod in MODERATORS}
for i in rows:
    stats = log(i)
    # team wins calcs
    true_winner = stats.winner
    if stats.fiend == 1:
        true_winner = "Fiends"
    if not stats.gameRound in rounds_with_moderators:
        rounds_with_moderators[stats.gameRound] = []
    if stats.name in MODERATORS:
        rounds_with_moderators[stats.gameRound].append(stats.name)
        if not stats.name in moderator_round_count:
            moderator_round_count[stats.name] = 0
        moderator_round_count[stats.name] += 1



moderator_count = {c: 0 for c in range(1, 31)}
has_moderator_streak = {c: 0 for c in range(1, 31)}
highest_moderator_streak =  {c: 0 for c in range(1, 31)}
no_moderator_streak = {c: 0 for c in range(1, 31)}
lowest_moderator_streak =  {c: 0 for c in range(1, 31)}

moderator_groups = {}
for rounds, moderators in sort_dict_by_key(rounds_with_moderators).items():
    # Moderator grouping
    if not tuple(moderators) in moderator_groups:
        moderator_groups[tuple(moderators)] = 0
    moderator_groups[tuple(moderators)] += 1

    for count, amt in moderator_count.items():

        # With/Without moderator streak resetting
        if no_moderator_streak[count] > lowest_moderator_streak[count]:
            lowest_moderator_streak[count] = no_moderator_streak[count]
        if has_moderator_streak[count] > highest_moderator_streak[count]:
            highest_moderator_streak[count] = has_moderator_streak[count]

        # With/Without moderator streak incrementing, + moderators per round counting
        if len(moderators) >= count:
            moderator_count[count] += 1
            has_moderator_streak[count] += 1
            no_moderator_streak[count] = 0

        else:
            no_moderator_streak[count] += 1
            has_moderator_streak[count] = 0




print(f"Total rounds: {len(rounds_with_moderators)}\n")

print("Rounds with atleast x moderators: (% of total rounds)")
for count, amt in moderator_count.items():
    print(f"{count}: {amt} ({round(amt / len(rounds_with_moderators) * 100, 2)}%)")
    if amt == 0:
        break
print("")
print("Moderator Round Count (% of total rounds)")
idx = 0
for moderator, count in sort(moderator_round_count).items():
    idx += 1
    print(f"{idx}. {moderator}: {count} ({round(count / len(rounds_with_moderators) * 100, 2)}%)")
print("")
print("Longest streak with/without at least x moderators")
for count, streak in highest_moderator_streak.items():
    print(f"{count}: {streak} / {lowest_moderator_streak[count]}")
    if streak == 0:
        break
print("")
# print("Moderator Groups (% of total rounds)")
with open(fr'player_groups.txt', 'a', encoding='utf-8', errors='replace') as file:
    for group, count in sorted(moderator_groups.items(), key=lambda x: (len(x[0]), -x[1])):
        file.write(f"{join_with_final(group, ", ", " & ")}: {count} ({round(count / len(rounds_with_moderators) * 100, 2)}%)")

