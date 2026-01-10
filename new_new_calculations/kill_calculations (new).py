from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.killerName = None
        self.victimRole = None
        self.killerRole = None
        self.gameLength = None
        self.gameRound = None
        self.timestamp = None
        self.funcCall = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")
log_name = "kill"
time = "7d"
with open(fr'../new_data/{time}.{log_name}-data.txt', 'r') as file:
    killer_dict = {}
    for line in file:
        kill = log(line)
        if not kill.killerName in killer_dict:
            killer_dict[kill.killerName] = 0
        killer_dict[kill.killerName] += 1
print(killer_dict)





