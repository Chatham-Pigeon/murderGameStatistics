from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages, \
    formatted_win_rates


class log:
    def __init__(self, raw_data: str):
        self.length = None
        self.map = None
        self.fiend = None
        self.winner = None
        self.playercount = None
        self.gameRound = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")

log_name = "round"
time = "2w"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    rounds = []
    duplicated_rounds = []
    for line in file:
        data = log(line)
        if not data.gameRound in rounds:
            rounds.append(data.gameRound)
        else:
            if not data.gameRound in duplicated_rounds:
                duplicated_rounds.append(data.gameRound)
                print(data.gameRound)


