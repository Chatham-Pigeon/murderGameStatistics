from helper_functions import calculate_percentages
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


amount_of_games = []
winners = {"Traitors": 0, "Citizens": 0, "Fiend": 0}
for i in rows:
    data = log(i)
    if int(data.playercount) > 6:
        if data.fiend == 1:
            winners['Fiend'] += 1
        else:
            winners[data.winner] += 1
        amount_of_games.append(data.gameRound)
print(calculate_percentages(winners, True))
print(len(amount_of_games))



