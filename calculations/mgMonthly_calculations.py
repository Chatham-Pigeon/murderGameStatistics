from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages, \
    formatted_win_rates


class log:
    def __init__(self, raw_data: str):
        self.length = None
        self.map = None
        self.fiend = None
        self.winner = None
        self.playercount = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")

log_name = "round"
time = "30d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    role_wins_proper = {"Traitors": 0, "Citizens": 0, "Fiends": 0}
    role_wins = {"Traitors": 0, "Citizens": 0}
    map_wins = {}
    role_wins_game_length = {"Traitors": [], "Citizens": [], "Fiends": []}
    role_wins_game_length_per_map = {"Highrise": {"Traitors": [], "Citizens": [], "Fiends": []}}
    for line in file:
        data = log(line)
        if int(data.playercount) < 7:
            continue
        role_wins[data.winner] += 1
        if not data.map in role_wins_game_length_per_map:
            role_wins_game_length_per_map[data.map] = {"Traitors": [], "Citizens": [], "Fiends": []}
        if data.fiend == 'false':
            role_wins_proper[data.winner] += 1
            role_wins_game_length[data.winner].append(data.length)
            role_wins_game_length_per_map[data.map][data.winner].append(data.length)
        else:
            role_wins_proper['Fiends'] += 1
            role_wins_game_length["Fiends"].append(data.length)
            role_wins_game_length_per_map[data.map]["Fiends"].append(data.length)

        if not data.map in map_wins:
            map_wins[data.map] = {"Traitors": 0, "Citizens": 0, "Fiends": 0}
        if data.fiend == 'false':
            map_wins[data.map][data.winner] += 1
        else:
            map_wins[data.map]['Fiends'] += 1



print(f"Overall win rates: {formatted_win_rates(role_wins_proper)}")
print(f"Winner when fiend overrides win condition: {formatted_win_rates(role_wins)}")
for map_name, wins in map_wins.items():
    map_wins[map_name] = calculate_percentages(wins, True)
target_role_win_percents = {"Traitors": 40, "Citizens": 40, "Fiends": 20}
euclidian_distance = {}

print(" ")
for map_name, wins in map_wins.items():
    role_differences_squared = {}
    for role, percent in wins.items():
        role_differences_squared[role] = (percent - target_role_win_percents[role]) ** 2
    euclidian_distance[map_name] = round(sum(role_differences_squared.values()) ** 0.5, 2)
avg_deviation = sum(euclidian_distance.values()) / len(euclidian_distance)
print(f"Maps ranked by their Euclidian Distance Deviation from a 40/40/20% win rate, lower is better. (avg is {avg_deviation}]")

euclidian_distance = sort(euclidian_distance, False)
idx = 0
for map_name, distance in euclidian_distance.items():
    idx += 1
    print(f"{idx}. {map_name}: {distance} ({formatted_win_rates(map_wins[map_name])})")
    if idx >= 10:
        continue
print("")
for role in target_role_win_percents.keys():
    print(f"Best Maps for {role}:")
    idx = 0
    for map_name, wins in sort_dict_by_nested_value(map_wins, role).items():
        idx += 1
        print(f"{idx}. {map_name}: {formatted_win_rates(wins)}")
        if idx >= 3:
            break
    print("")
role_wins_game_length_avg = {}
for role in target_role_win_percents.keys():
    role_wins_game_length_avg[role] = sum(role_wins_game_length[role]) / len(role_wins_game_length[role])
role_wins_game_length_avg_formatted = {}
for name, length in role_wins_game_length_avg.items():
    minutes, seconds = divmod(length / 20, 60)
    role_wins_game_length_avg_formatted[name] = f"{int(minutes)}m{int(round(seconds, 0))}s"
print(f"Average game length when role win: {", ".join(f"{role}: {time}" for role, time in role_wins_game_length_avg_formatted.items())}")
for map_name, role_lengths in role_wins_game_length_per_map.items():
    for role in target_role_win_percents.keys():
        role_wins_game_length_per_map[map_name][role] = sum(role_lengths[role]) / len(role_lengths[role])
role_wins_game_length_per_map_formatted = {}
for map_name in role_wins_game_length_per_map.keys():
    role_wins_game_length_per_map_formatted[map_name] = {"Traitors": "", "Citizens": "", "Fiends": ""}
    for role in target_role_win_percents.keys():
        minutes, seconds = divmod(role_wins_game_length_per_map[map_name][role] / 20, 60)
        role_wins_game_length_per_map_formatted[map_name][role] = f"{int(minutes)}m{int(round(seconds, 0))}s"

