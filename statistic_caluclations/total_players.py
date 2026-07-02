from SECRETS import *


class log:
    def __init__(self, raw_data: dict):
        self.gameRound = 0
        self.name = None
        for key, value in raw_data.items():
            setattr(self, key, value)

with open(fr'all_players.txt', 'r', encoding='utf-8', errors='replace') as file:
    players = file.read().split("\n")

rows = query(f"""
    SELECT pr.*, g.*
    FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID}""")

for i in rows:
    stats = log(i)
    if not stats.name in players:
        players.append(stats.name)
print(players)
print(len(players))



