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


teams = {"Citizens": 0, "Traitors": 0, "Fiends": 0}
for i in rows:
    data = log(i)
    if data.playercount < 7:
        continue
    true_winner = data.winner
    if data.fiend == 1:
        true_winner = "Fiends"
    teams[true_winner] += 1
print(calculate_percentages(teams))
