from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.wins = None
        self.name = None
        self.opt = None
        self.LSV = None
        self.ignoreList = None
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
time = "30d"
roles = ['innocent', 'detective', 'doctor', 'traitor', 'accomplice', 'fiend']
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    wins = {}
    role_wins = {}
    players = []
    for line in file:
        save = log(line)
        wins_innocent = 0
        wins_detective = 0
        wins_doctor = 0
        wins_traitor = 0
        wins_fiend = 0
        wins_accomplice = 0
        for role in roles:
            try:
                exec(f"wins_{role} = getattr(save, 'roleWins.{role}')")
            except AttributeError as e:
                pass
        if save.wins is None:
            save.wins = 0
        wins[save.name] = save.wins
        if not save.name in players:
            players.append(save.name)
wins = sort(wins)
idx = 0
for name, wins in wins.items():
    idx += 1
    print(f"{idx}. {name}: {wins}")
    if idx >= 100:
        break
print(len(players))





