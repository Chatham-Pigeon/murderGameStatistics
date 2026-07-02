from helper_functions import sort_dict_by_nested_value, calculate_percentages, formatted_win_rates
from SECRETS import *
class log:
    def __init__(self, raw_data: dict):
        self.gameRound = None
        self.playercount = None
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



playercount_stats = {}
for i in rows:
    data = log(i)
    true_winner = data.winner
    if data.fiend == 1:
        true_winner = "Fiends"
    if not data.playercount in playercount_stats:
        playercount_stats[data.playercount] = {}
    if not true_winner in playercount_stats[data.playercount]:
        playercount_stats[data.playercount][true_winner] = 0
    playercount_stats[data.playercount][true_winner] += 1

win_target = {"Traitors": 40, "Citizens": 40, "Fiends": 20}
playercount_data = {}
for playercount_name, raw_stats in playercount_stats.items():
    stats = calculate_percentages(raw_stats, True)
    deviation_list = []
    playercount_data[playercount_name] = {}
    for team, wins in stats.items():
        remove_fiend = 0
        if not "Fiends" in stats:
            remove_fiend = 10
        deviation  = abs(wins - (win_target[team] + remove_fiend))
        deviation_list.append(deviation)
    playercount_data[playercount_name]['total'] = sum(raw_stats.values())
    playercount_data[playercount_name]['deviation'] = round(sum(deviation_list) / len(deviation_list), 2)
print("PLAYERCOUNT BALANCE DEVIATION")
idx = 0
for playercount_name, data in sort_dict_by_nested_value(playercount_data, 'deviation', False).items():
    deviation = data['deviation']
    total = data['total']
    if total < 30:
        continue
    idx += 1
    print(f"{idx}. {playercount_name}: {formatted_win_rates(calculate_percentages(playercount_stats[playercount_name], True))} ({deviation}) | {total} games")
print("\n\n")
idx = 0

playercount_data = sort_dict_by_nested_value(playercount_data, 'total', True)
for playercount_name, data in playercount_data.items():
    idx += 1
    print(f"{idx}. {playercount_name}: {data['total']}")


print(f"RANGE OF PLAYS: {list(playercount_data.values())[0]['total'] - list(playercount_data.values())[-1]['total']}")