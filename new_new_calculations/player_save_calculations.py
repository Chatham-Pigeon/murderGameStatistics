from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.gameRound = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")
log_name = "player-save"
time = "7d"
coin_timer = 2400

with open(fr'../new_data/{time}.{log_name}-data.txt', 'r') as file:
    detective_kills_role = {}
    for line in file:
        save = log(line)




