from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.spawnType_natural = None
        self.spawnType_death = None
        self.points = None
        self.name = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            key = key.replace(".", "_")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")

log_name = "april-fools"
time = "30d"
total_spawned_natural = 37417
total_spawned_death = 29532
with open(fr'../data/{time}.{log_name}.txt', 'r') as file:
    total_natural_collected = 0
    players_points = {}
    for line in file:
        data = log(line)
        total_natural_collected += data.spawnType_natural
        players_points[data.name] = data.points


print(total_natural_collected)
print(sort(players_points,))
players_points = sort(players_points, False)
idx = 152
for player, points in players_points.items():
    idx -= 1
    print(f"{idx}. {player}: {points}")


