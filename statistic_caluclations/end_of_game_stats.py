from helper_functions import sort_dict_by_nested_value
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

current_round = 0
total_players = 0
alive_players = 0
round_alive_dict = {}
for i in rows:
    stats = log(i)
    if not stats.gameRound == current_round:
        round_alive_dict[stats.gameRound] = {"total_players": total_players, "alive_players": alive_players}
        alive_players = 0
        total_players = 0
        current_round = stats.gameRound
    alive_players += stats.won
    total_players += 1
print(sort_dict_by_nested_value(round_alive_dict, "total_players"))
print(len(round_alive_dict))
total = 0
for game_round, data in round_alive_dict.items():
    total += data['alive_players']
print(total)
print(total / len(round_alive_dict))









