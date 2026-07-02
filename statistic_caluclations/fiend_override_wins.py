from SECRETS import *
from helper_functions import calculate_percentages


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
wins = {"Traitors": 0, "Citizens": 0}
for i in rows:
    data = log(i)
    if data.fiend == 1:
        wins[data.winner] += 1
print(calculate_percentages(wins))
