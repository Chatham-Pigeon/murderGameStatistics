from helper_functions import sort, sort_dict_by_nested_value
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
        for key, value in raw_data.items():
            setattr(self, key, value)

rows = query(f"""
    SELECT pr.* FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID}""")
rounds = 0
wins = 0
role_player_wins = {"total": {}}
for i in rows:
    stats = log(i)
    rounds += 1
    wins += stats.won
    if not stats.role in role_player_wins:
        role_player_wins[stats.role] = {}
    if not stats.name in role_player_wins[stats.role]:
        role_player_wins[stats.role][stats.name] = {"rounds": 0, "wins": 0}
    if not stats.name in role_player_wins["total"]:
        role_player_wins["total"][stats.name] = {"rounds": 0, "wins": 0}
    role_player_wins[stats.role][stats.name]['rounds'] += 1
    role_player_wins[stats.role][stats.name]['wins'] += stats.won
    role_player_wins["total"][stats.name]['rounds'] += 1
    role_player_wins["total"][stats.name]['wins'] += stats.won

win_percentages = {}
for role, players in role_player_wins.items():
    win_percentages[role] = {}
    for player, data in players.items():
        if data['rounds'] >= 50 and data['wins'] >= 1:
            win_percentages[role][player] = data['wins'] / data['rounds'] * 100
for role, players in win_percentages.items():
    print(f"- {role}")
    idx = 0
    for player, data in sort(players).items():
        idx += 1
        if idx > 10:
            break
        print(f"{idx}. {player}: {round(data, 2)}%")
idx = 0
print("Total round leaderboard")
for player, data in sort_dict_by_nested_value(role_player_wins['total'], "rounds").items():
    if data['rounds'] < 50:
        continue
    idx += 1
    if idx > 10:
        break
    print(f"{idx}. {player}: {data}")


print(rounds)
print(wins)
print(f"Percent: {round(wins / rounds  * 100, 2)}")

