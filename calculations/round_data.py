from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages, formatted_win_rates


class log:
    def __init__(self, raw_data: str):
        self.gameRound = None
        self.timestamp = None
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
with open(fr'../data/{time}.{log_name}-data.txt', 'r', encoding='utf-8') as f:
    winrates_per_pc = {}
    longest_round = 0
    that_round = ""
    for line in f:
        data = log(line)
        if not data.playercount in winrates_per_pc:
            winrates_per_pc[data.playercount] = {"Citizens": 0, "Traitors": 0, "Fiends": 0}
        if data.fiend == 'false':
            winrates_per_pc[data.playercount][data.winner] += 1
        else:
            winrates_per_pc[data.playercount]["Fiends"] += 1
        if int(data.length) >= longest_round:
            longest_round = int(data.length)
            that_round = data.gameRound
target_role_win_percents = {"Traitors": 40, "Citizens": 40, "Fiends": 20}
euclidian_distance = {}

print(" ")
for map_name, wins in winrates_per_pc.items():
    role_differences_squared = {}
    for role, percent in calculate_percentages(wins).items():
        role_differences_squared[role] = (percent - target_role_win_percents[role]) ** 2
    euclidian_distance[map_name] = round(sum(role_differences_squared.values()) ** 0.5, 2)
avg_deviation = sum(euclidian_distance.values()) / len(euclidian_distance)

for count, rates in sort_dict_by_key(winrates_per_pc).items():
    print(f"{count}: {formatted_win_rates(sort(rates))} ({euclidian_distance[count]})")
print(f"f avggg deviation  {avg_deviation}")

win_most = {}
for count, rates in winrates_per_pc.items():
    rates = sort(rates)
    for team, percent in rates.items():
        if not team in win_most:
            win_most[team] = 0
        win_most[team] += 1
        break
print(win_most)
print(that_round)
print(longest_round)



