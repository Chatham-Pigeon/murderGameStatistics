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
rows = query(f"SELECT * FROM games WHERE plotID = {PLOT_ID} AND timestamp >= {START_TIME}")


# Tracking
game_list = []
game_lengths = {"Traitors": [], "Citizens": [], "Fiends": []}
for i in rows:
    data = log(i)
    game_list.append(data.gameRound)
    true_winner = data.winner
    if data.fiend == 1:
        true_winner = "Fiends"
    game_lengths[true_winner].append(data.length)

# Calculations / Printing
total_time = 0
print("- Game lengths per win team")
for team, data in game_lengths.items():
    average = sum(data) / len(data)
    total_time += sum(data)
    to_seconds = average / 20
    time_minute, time_seconds = divmod(to_seconds, 60)
    print(f"{team}: {int(time_minute)}m{int(round(time_seconds, 0))}s")
total_time = total_time / 20

print(f"- Game Count = {len(game_list)}")
time_hours, time_minutes = divmod(total_time / 60, 60)
print(f"- Game length total: {int(time_hours)}h{int(round(time_minutes, 0))}m")




