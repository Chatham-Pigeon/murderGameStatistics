from helper_functions import sort_dict_by_nested_value, calculate_percentages, formatted_win_rates
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

rows = query(f"SELECT * FROM games WHERE plotID = {PLOT_ID} AND timestamp >= {START_TIME} AND playercount >= 7")



map_stats = {}
for i in rows:
    data = log(i)
    if not data.map in MAP_DICT:
        continue
    true_winner = data.winner
    if data.fiend == 1:
        true_winner = "Fiends"
    if not data.map in map_stats:
        map_stats[data.map] = {"Traitors": 0, "Citizens": 0, "Fiends": 0}
    map_stats[data.map][true_winner] += 1

win_target = {"Traitors": 40, "Citizens": 40, "Fiends": 20}
map_data = {}
for map_name, raw_stats in map_stats.items():
    stats = calculate_percentages(raw_stats, True)
    deviation_list = []
    map_data[map_name] = {}
    for team, wins in stats.items():
        deviation  = abs(wins - win_target[team])
        deviation_list.append(deviation)
    map_data[map_name]['total'] = sum(raw_stats.values())
    map_data[map_name]['deviation'] = round(sum(deviation_list) / len(deviation_list), 2)
print("MAP BALANCE DEVIATION")
idx = 0
for map_name, data in sort_dict_by_nested_value(map_data, 'deviation', False).items():
    idx += 1
    deviation = data['deviation']
    total = data['total']
    print(f"{idx}. {map_name}: {formatted_win_rates(calculate_percentages(map_stats[map_name], True))} ({deviation}) | {total} games")
print("\n\n")
idx = 0

map_data = sort_dict_by_nested_value(map_data, 'total', True)
for map_name, data in map_data.items():
    idx += 1
    print(f"{idx}. {map_name}: {data['total']}")


print(f"RANGE OF PLAYS: {list(map_data.values())[0]['total'] - list(map_data.values())[-1]['total']}")