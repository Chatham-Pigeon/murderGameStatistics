from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages, \
    formatted_win_rates

builders = {
    "Old Bunker": ["Sagittarixie"],
    "Haunted Hotel": ["StardustGemini"],
    "Subway Station": ["KabanFriends", "Powercyphe"],
    "Bowling Alley": ["endersaltz"],
    "Tropics": ["ninja70707"],
    "The Mall": ["Benneze"],
    "Mediterranean": ["ninja70707"],
    "Overgrown City": ["Och0"],
    "The Aquarium": ["Chatham_Pigeon"],
    "Walmar Street": ["Powercyphe"],
    "IKEA": ["InfinityWorks"],
    "Behind The Waterfall": ["Powercyphe", "Legendarial"],
    "Office": ["The_Blue_Friend"],
    "Moon Base": ["Sagittarixie"],
    "Bunker 83": ["endersaltz", "ACraftingFish"],
    "Electrical Station": ["Sagittarixie", "The_Blue_Friend"],
    "The Commons": ["Sagittarixie"],
    "Emberwoods": ["Sagittarixie"],
    "Temple of KING Sr.": ["nvct"],
    "Impoverished Domicile": ["nvct"],
    "2Fort": ["redstonae"],
    "Fiend Casino": ["StardustGemini"],
    "Cliffside Mansion": ["Euws"],
    "Forest Mansion": ["Farbschaf"],
    "The Depths": ["nvct"],
    "The Mineshafts": ["TeamF"],
    "Cosmic Encounter": ["Diglett_go", "Killer77Kat"],
    "Oil Rig": ["nvct"],
    "The Brigade": ["nvct"],
    "The Trials": ["nvct"],
    "Abandoned Prison": ["JJJT", "Luxwind_"],
    "Highrise": ["Brxzillian"],
    "Seaside": ["Brxzillian"],
    "Japanese Estate": ["FigtheFruit"],
    "Glacial Grotto": ["Brxzillian"],
    "Overgrown Site": ["Brxzillian"],
    "Northorn Mansion": ["Brxzillian"],
    "Abandoned Factory": ["Farbschaf"],
    "Barclays Bank": ["TeamF"],
    "The Last Duel": ["nvct"],
    "Sinister Sanctuary": ["Jeffree225", "nammannam"],
    "Crimson Casino": ["Brxzillian"],
    "Deep Dark Lab": ["___SillyGoose__"],
    "Sculk Sanctum": ["RalseiDeltarune"],
    "Nastrond": ["nvct"]
}

class log:
    def __init__(self, raw_data: str):
        self.length = None
        self.map = None
        self.fiend = None
        self.winner = None
        self.playercount = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")

        if self.winner == "traitor":
            self.winner = "Traitors"
        if self.winner == "innocents":
            self.winner = "Citizens"
        if self.map == "Forst Mansion":
            self.map = "Forest Mansion"
        if self.map == "Barcleys Bank":
            self.map = "Barclays Bank"
        if self.map == "Sinister Sancutary":
            self.map = "Sinister Sanctuary"
        if "IKEA" in self.map:
            self.map = "IKEA"

log_name = "round"
time = "68d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    role_wins_proper = {"Traitors": 0, "Citizens": 0, "Fiends": 0}
    role_wins = {"Traitors": 0, "Citizens": 0}
    map_wins = {}
    role_wins_game_length = {"Traitors": [], "Citizens": [], "Fiends": []}
    role_wins_game_length_per_map = {"Highrise": {"Traitors": [], "Citizens": [], "Fiends": []}}
    amount_of_games = {}
    for line in file:
        data = log(line)
        if int(data.playercount) < 7:
            continue
        if not data.map in builders.keys():
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
        if data.map not in amount_of_games:
            amount_of_games[data.map] = 0
        amount_of_games[data.map] += 1



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
    print(f"{idx}. {map_name}: {distance} ({formatted_win_rates(map_wins[map_name])}) ({amount_of_games[map_name]} games)")
    if idx >= 10:
        pass
print("")
for role in target_role_win_percents.keys():
    print(f"Best Maps for {role}:")
    idx = 0
    for map_name, wins in sort_dict_by_nested_value(map_wins, role).items():
        idx += 1
        print(f"{idx}. {map_name}: {formatted_win_rates(wins)} ({amount_of_games[map_name]} games)")
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
print(f"map sum {sum(amount_of_games.values())}")
exit()
for map_name, role_lengths in role_wins_game_length_per_map.items():
    for role in target_role_win_percents.keys():
        role_wins_game_length_per_map[map_name][role] = sum(role_lengths[role]) / len(role_lengths[role])
role_wins_game_length_per_map_formatted = {}
for map_name in role_wins_game_length_per_map.keys():
    role_wins_game_length_per_map_formatted[map_name] = {"Traitors": "", "Citizens": "", "Fiends": ""}
    for role in target_role_win_percents.keys():
        minutes, seconds = divmod(role_wins_game_length_per_map[map_name][role] / 20, 60)
        role_wins_game_length_per_map_formatted[map_name][role] = f"{int(minutes)}m{int(round(seconds, 0))}s"

