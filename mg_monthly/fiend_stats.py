from SECRETS import *


class game_log:
    def __init__(self, raw_data: dict):
        self.gameRound = 0
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

class player_log:
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
        for key, value in raw_data.items():
            setattr(self, key, value)

class kill_log:
    def __init__(self, raw_data: dict):
        self.gameRound = 0
        self.killerName = None
        self.victimName = None
        self.heldItem = None
        self.damageCause = None
        self.killerHealth = None
        self.victimArrows = None
        self.bodyFound = None
        self.gameTick = None
        self.killDistance = None
        self.fiendTimeLeft = None
        for key, value in raw_data.items():
            setattr(self, key, value)
FIEND_TIME_TICKS = 70 * 20
FIEND_GRACE_PERIOD = 30 * 20
def get_fiend_task(tick: int):
    if tick < FIEND_TIME_TICKS + FIEND_GRACE_PERIOD:
        return 1
    return 1 + (tick - FIEND_GRACE_PERIOD) // FIEND_TIME_TICKS

def get_fiend_count(playercount: int):
    return min(playercount // 7, 3)
game_rows = query(f"""
    SELECT *
    FROM games
    WHERE plotID = {PLOT_ID} AND timestamp >= {START_TIME}""")

player_rows = query(f"""
    SELECT *
    FROM player_rounds
    WHERE gameRound IN (
        SELECT gameRound FROM games
        WHERE plotID = {PLOT_ID} AND timestamp >= {START_TIME})
""")

game_players = {0: {}}
for player in player_rows:
    if not player['gameRound'] in game_players:
        game_players[player['gameRound']] = {}
    game_players[player['gameRound']][player['name']] = player

kill_rows = query(f"""
    SELECT *
    FROM kills
    WHERE gameRound IN (
        SELECT gameRound FROM games
        WHERE plotID = {PLOT_ID} AND timestamp >= {START_TIME})
""")
game_kills = {0: []}
for kill in kill_rows:
    if not kill['gameRound'] in game_kills:
        game_kills[kill['gameRound']] = []
    game_kills[kill['gameRound']].append(kill)




for i in game_rows:
    data = game_log(i)
    true_winner = data.winner
    if data.fiend == 1:
        true_winner = "Fiends"
    dead_fiends = 0
    fiend_dead_time = 0
    FIEND_BEHAVIOURS = {0: {"fail": 0, "kill": 0, "won": 0, "dead": 0}}
    for kill in game_kills[data.gameRound]:
        kill = kill_log(kill)
        if kill.killerName == "%killer":
            continue
        # FIEND TEAM DIE CHECK
        if game_players[data.gameRound][kill.victimName]['role'] == 'fiend':
            if fiend_dead_time >= kill.gameTick:
                fiend_dead_time = kill.gameTick
            dead_fiends += 1
            if dead_fiends == get_fiend_count(data.playercount):
                kill_task = get_fiend_task(kill.gameTick)
                FIEND_BEHAVIOURS[kill_task]['dead'] = True

        if not game_players[data.gameRound][kill.killerName]['role'] == 'fiend':
            continue
        # WIN

        # SUCCESS





