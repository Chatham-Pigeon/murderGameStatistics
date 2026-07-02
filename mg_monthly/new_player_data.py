from helper_functions import sort, sort_dict_by_key, join_with_final
from SECRETS import *



class log:
    def __init__(self, raw_data: dict):
        self.gameRound = 0
        self.name = None
        self.role = None
        self.won = None
        self.totalDamageDealt = 0
        self.damageReceived = None
        self.healthHealed = None
        self.bowsShot = None
        self.bowsLanded = None
        self.meleeAttempts = None
        self.meleeSuccesses = None
        self.playersKilled = None
        self.timeAlive = None
        self.purchases = None
        self.gameRound = None
        self.map = None
        self.winner = None
        self.fiend = None
        self.length = None
        self.playercount = None
        self.timestamp = None
        self.gameType = None
        self.plotID = None
        self.winReason = None
        for key, value in raw_data.items():
            setattr(self, key, value)
# query data
rows = query(f"""
    SELECT pr.*, g.*
    FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID} AND g.timestamp >= {START_TIME}""")

game_rows = query(f"SELECT * FROM games WHERE plotID = {PLOT_ID} AND timestamp >= {START_TIME}")

# init const vars
rounds = {g['gameRound']: log(g) for g in game_rows}
AN_HOUR = 216000
with open('../secret_dir/all_players.txt', 'r') as file:
    existing_players = file.read().split("\n")

# init stat dicts
new_players = []
average_length = {"not_a_player": [5, 10, 12]}
current_player_length = {"not_a_layer": [12012, 12013, 12014, 12015,]}


rows = sorted(rows, key=lambda x: x['gameRound'])
for i in rows:
    stats = log(i)
    # differentiate between new & old players
    if not stats.name in existing_players:
        if not stats.name in new_players:
            new_players.append(stats.name)
    # init loop dicts
    if not stats.name in current_player_length:
        current_player_length[stats.name] = []
    if len(current_player_length[stats.name]) == 0:
        current_player_length[stats.name].append(stats.gameRound)
    else:
        # if been less than an hour (60*60) append that game round to list
        # when been MORE than an hour, append len of that list to their session length list, clear that  len
        if stats.timestamp - rounds[current_player_length[stats.name][-1]].timestamp > (60*60):
            # first session? make sure to init it
            if not stats.name in average_length:
                average_length[stats.name] = []
            average_length[stats.name].append(len(current_player_length[stats.name]))
            current_player_length[stats.name] = []
        else:
            current_player_length[stats.name].append(stats.gameRound)


# int(round(sum(x[1]) / len(x[1]), 0)))
# dict(sorted(average_length.items(), key=lambda x: len(x[1]))).items()
new_player_lengths = []
existing_player_lengths = []
for name, lengths in average_length.items():
    if name in new_players:
        new_player_lengths.extend(lengths)
    elif name in existing_players:
        existing_player_lengths.extend(lengths)
    else:
        print(name)
if len(new_player_lengths) > 0:
    print(f"New player avg: {sum(new_player_lengths) / len(new_player_lengths)}")
print(f"Existing player avg: {sum(existing_player_lengths) / len(existing_player_lengths)}")









