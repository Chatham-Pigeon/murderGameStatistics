
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
    total_time = 0
    players = []
    for line in f:
        stats = log(line)
        total_time += stats.timeAlive
        if not stats.name in players:
            players.append(stats.name)
hours, minutes = divmod(total_time / 20 / 60, 60)
print(f"{int(hours)}h{int(minutes)}m")
total_time = total_time / len(players)
hours, minutes = divmod(total_time / 20 / 60, 60)
print(f"avg per player {int(hours)}h{int(minutes)}m")
print(len(players))



