from helper_functions import sort_dict_by_nested_value, calculate_percentages, builders
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


win_reasons = {}
game_lengths = {"The Aquarium": {"Fiends": [], "Traitors": [], "Citizens": []}}
for i in rows:
    data = log(i)
    if not data.map in builders:
        continue

    # track win reasons
    if not data.map in win_reasons:
        win_reasons[data.map] = {"kill": 0, "time": 0}
    win_reasons[data.map][data.winReason] += 1

    # track game lengths per team
    if not data.map in game_lengths:
        game_lengths[data.map] = {"Fiends": [], "Traitors": [], "Citizens": []}
    if data.fiend == 1:
        game_lengths[data.map]["Fiends"].append(data.length)
    else:
        game_lengths[data.map][data.winner].append(data.length)

win_reasons = sort_dict_by_nested_value(win_reasons, 'time')
print("WIN REASONS AS %")
idx = 0
for map_name, reasons in win_reasons.items():
    idx += 1
    print(f" {idx} - {map_name}")
    for reason, percent  in calculate_percentages(reasons, True).items():
        print(f"{reason}: {percent}%")

calculated_game_lengths = {"The Aquarium": {"Fiends": 0, "Traitors": 0, "Citizens": 0}}
for map_name, team_lengths in game_lengths.items():
    calculated_game_lengths[map_name] = {}
    for team, lengths in team_lengths.items():
        calculated_game_lengths[map_name][team] = int(round(sum(lengths) / len(lengths) / 20, 0))
    calculated_game_lengths[map_name]["average"] = int(round(sum(calculated_game_lengths[map_name].values()) / len(calculated_game_lengths[map_name]), 0))

print("\n\nAVG GAME LENGTH")
for map_name, team_lengths in sort_dict_by_nested_value(calculated_game_lengths, "average").items():
    print(f"{idx} - {map_name}")
    for team, length in team_lengths.items():
        minutes, seconds = divmod(length, 60)
        length = f"{int(minutes)}m{int(round(seconds, 0))}s"
        print(f"{team}: {length}")