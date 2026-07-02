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
        self.purchases: str = ""
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

rows = query(f"""
    SELECT pr.*, g.*
    FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID} AND g.timestamp >= {START_TIME}""")

role_purchases = {}
for i in rows:
    stats = log(i)
    if not stats.role in role_purchases:
        role_purchases[stats.role] = {}
    purchases = stats.purchases.split(" ")
    for item in purchases:
        if item == '':
            continue
        if not item in role_purchases[stats.role]:
            role_purchases[stats.role][item] = 0
        role_purchases[stats.role][item] +=1

for role, purchases in role_purchases.items():
    role: str = role
    print(f"- {role.capitalize()}")
    total = sum(purchases.values())
    for item, amt in purchases.items():
        print(f"{item}: {round(amt / total * 100,1)}%")






