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

rows = query(f"""
    SELECT pr.*, g.*
    FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID} AND g.timestamp >= {START_TIME}""")

players = []
alive_lengths = []
for i in rows:
    stats = log(i)
    # team wins calcs
    true_winner = stats.winner
    if stats.fiend == 1:
        true_winner = "Fiends"
    players.append(stats.name)
    alive_lengths.append(stats.timeAlive)


players = list(set(players))
print(f"- Unique players: {len(players)}")
time_hours, time_minutes = divmod(sum(alive_lengths) / 20 / 60, 60)
print(f"- Combined playtime total: {int(time_hours)}h{int(round(time_minutes, 0))}m")
time_hours, time_minutes = divmod(sum(alive_lengths) / len(players) / 20 / 60, 60)
print(f"- Average playtimetime per player {int(time_hours)}h{int(round(time_minutes, 0))}m")





