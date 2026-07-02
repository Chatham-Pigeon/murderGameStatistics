from helper_functions import sort
from SECRETS import *

class log:
    def __init__(self, raw_data: dict):
        self.gameRound = 0
        self.killerName = None
        self.victimName = None
        self.heldItem = None
        self.damageCause = None
        self.killerHealth = None
        self.victimArrows = None
        self.bodyFound = None
        self.gameTick = None
        self.killDistance = None
        self.fiendTimeLeft = None
        for key, value in raw_data.items():
            setattr(self, key, value)
rows = query(f"""
    SELECT k.*, g.*
    FROM kills k
    JOIN games g ON k.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID}""")

player_rounds = query(f"""
    SELECT pr.*
    FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID}""")
player_rounds_dict = {(r['gameRound'], r['name']): r for r in player_rounds}

kill_distance = {}
for i in rows:
    data = log(i)
    if data.killerName == "%killer":
        continue
    if not data.heldItem in ['stone_sword', 'wooden_sword']:
        continue
    key = (data.gameRound, data.killerName, data.victimName)
    if player_rounds_dict[(data.gameRound, data.killerName)]['timeAlive'] >= player_rounds_dict[(data.gameRound, data.victimName)]['timeAlive']:
        kill_distance[key] = data.killDistance

idx = 0
for key, distance in sort(kill_distance).items():
    idx += 1
    print(f"{idx}. ({key[0]}) {key[1]} kill {key[2]}: {distance}")
    if idx >= 250:
        break