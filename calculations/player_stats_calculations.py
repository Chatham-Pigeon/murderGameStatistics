from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.won = None
        self.alive = None
        self.name = None
        self.role = None
        self.gameRound = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")
log_name = "player-stats"
time = "30d"

with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    role_chances = {}
    for line in file:
        stats = log(line)
        if stats.won == 'true':
            if not stats.role in role_chances:
                role_chances[stats.role] = 0
            role_chances[stats.role] += 1
for role, chances in sort(calculate_percentages(role_chances)).items():
    print(f"{role}: {chances}%")