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
    total_time = 0
    for line in file:
        data = log(line)
        total_time += int(data.length)
hours, minutes = divmod(total_time / 20 / 60, 60)
print(f"{int(hours)}h{int(minutes)}m")

