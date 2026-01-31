from collections import defaultdict


class log:
    def __init__(self, raw_data: str):
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
    for line in f:
        stats = log(line)




