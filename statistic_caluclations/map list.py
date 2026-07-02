from SECRETS import *
class log:
    def __init__(self, raw_data: dict):
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
        if "IKEA" in self.map:
            self.map = "IKEA"

rows = query(f"SELECT * FROM games WHERE plotID = {PLOT_ID}")


maps = []
for i in rows:
    data = log(i)
    if not data.map in maps:
        maps.append(data.map)
print(", ".join(maps))
print(len(maps))