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
time = "3y"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    lengths = []
    for line in file:
        data = log(line)
        if data.winner == "traitor":
            data.winner = "Traitors"
        if data.winner == "innocents":
            data.winner = "Citizens"
        if data.map == "Forst Mansion":
            data.map = "Forest Mansion"
        if data.map == "Barcleys Bank":
            data.map = "Barclays Bank"
        if int(data.playercount) <= 2:
            continue
        if data.fiend == "true":
            lengths.append(data.length)
average = sum(lengths) / len(lengths)
minutes, seconds = divmod(average / 20, 60)
print(f"{int(minutes)}m{int(round(seconds, 0))}s")



