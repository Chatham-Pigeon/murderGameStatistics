from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages, \
    formatted_win_rates
import matplotlib.pyplot as plt

class log:
    def __init__(self, raw_data: str):
        self.length = None
        self.map = None
        self.fiend = None
        self.winner = None
        self.playercount = None
        self.gameRound = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")

log_name = "round"
time = "68d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    total_time = 0
    rounds = []
    games_in_hour = {}
    players_in_hour = {}
    for line in file:
        data = log(line)
        timestamp = int(data.timestamp)
        hour = (timestamp // 3600) % 24
        if not hour in games_in_hour:
            games_in_hour[hour] = 0
            players_in_hour[hour] = 0
        players_in_hour[hour] += int(data.playercount)
        games_in_hour[hour] += 1
for hour, amt in sort_dict_by_key(games_in_hour).items():
    print(f"<t:{hour * 3600}:t>: {amt} ({hour})")
graph = plt.barh(games_in_hour.keys(), games_in_hour.values())
plt.show()
avg = {}
for hour, amt in sort_dict_by_key(players_in_hour).items():
    print(f"<t:{hour * 3600}:t>: {int(round(amt / games_in_hour[hour], 0))} ({hour})")
    avg[hour] = int(round(amt / games_in_hour[hour], 0))
graph = plt.barh(avg.keys(), avg.values())
plt.show()