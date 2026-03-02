from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages


class log:
    def __init__(self, raw_data: str):
        self.bowsShot = 0
        self.bowsLanded = 0
        self.timeAlive = 0
        self.role = None
        self.gameRound = None
        self.timestamp = None
        self.winTeam = None
        self.name = None
        self.alive = None
        self.won = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")


log_name = "player-stats"
time = "30d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r', encoding='utf-8') as f:
    time_alive = {}
    bow_accuracy = {}
    for line in f:
        stats = log(line)
        if stats.name == "KabanFriends":
            print(f"{stats.name} {stats.gameRound} ")
        if not stats.name in time_alive:
            time_alive[stats.name] = 0
        time_alive[stats.name] += stats.timeAlive
        if not stats.name in bow_accuracy:
            bow_accuracy[stats.name] = {"hit": 0, "shot": 0}
        bow_accuracy[stats.name]['shot'] += stats.bowsShot
        bow_accuracy[stats.name]['hit'] += stats.bowsLanded

time_alive = sort(time_alive)

idx = 0
for name, length in time_alive.items():
    if not name in ['nvct', 'Chatham_Pigeon', 'JJJT', 'Ace127', 'KabanFriends', 'Cactern', "Jeffree225", "pixlii", "Darqnt", "AutumnsBreeze"]:
        continue
    idx += 1
    minute, second = divmod(length / 20, 60)
    hour = ""
    h = ""
    if minute >= 60:
        hour, minute = divmod(minute, 60)
        hour = int(hour)
        h = "h"
    print(f"{idx}. {name}: {hour}{h}{int(minute)}m{int(round(second, 0))}s")
    if idx >= 100:
        pass

percent_accuracy = {}
for name, accuracy in bow_accuracy.items():
    if not accuracy['hit'] == 0 and accuracy['shot'] >= 25:
        percent_accuracy[name] = accuracy['hit'] / accuracy['shot'] * 100
    else:
        percent_accuracy[name] = 0
idx = 0
for name, rate in sort(percent_accuracy).items():
    idx += 1
    # print(f"{idx}. {name}: {rate}")

