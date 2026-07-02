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

player = input("Input the player: ")

teams = {"fiend": "Fiends", "traitor": "Traitors", "accomplice": "Traitors", "innocent": "Citizens", "detective": "Citizens", "doctor": "Citizens"}

rows = query(f"""
    SELECT pr.*, g.*
    FROM player_rounds pr
    JOIN games g ON pr.gameRound = g.gameRound
    WHERE g.plotID = {PLOT_ID} AND pr.name = '{player}'""")
role_team_wins = {"total": {'rounds': 0, 'wins': 0}}
role_personal_wins = {"total": {'rounds': 0, 'wins': 0}}

for i in rows:
    stats = log(i)

    # team wins calcs
    true_winner = stats.winner
    if stats.fiend == 1:
        true_winner = "Fiends"
    if not stats.role in role_team_wins:
        role_team_wins[stats.role] = {'rounds': 0, 'wins': 0}
    role_team_wins[stats.role]['rounds'] += 1
    role_team_wins["total"]['rounds'] += 1
    if teams[stats.role] == true_winner:
        role_team_wins["total"]['wins'] += 1
        role_team_wins[stats.role]['wins'] += 1

    # personal win calcs

    if not stats.role in role_personal_wins:
        role_personal_wins[stats.role] = {"rounds": 0, "wins": 0}
    role_personal_wins[stats.role]['rounds'] += 1
    role_personal_wins["total"]['rounds'] += 1
    if stats.won == 1:
        role_personal_wins[stats.role]['wins'] += 1
        role_personal_wins["total"]['wins'] += 1




print("- Team win Percent")
for role, stats in role_team_wins.items():
    print(f"{role}: {round(stats['wins'] / stats['rounds'] * 100, 2)}% ({stats['rounds']})")

print(f"\n- Personal win Percent")
for role, stats in role_personal_wins.items():
    print(f"{role}: {round(stats['wins'] / stats['rounds'] * 100, 2)}% ({stats['rounds']})")

print(f"\ntotal rounds: {role_team_wins['total']['rounds']}")

print(f"\n- % of team wins alive")
for role, stats in role_personal_wins.items():
    print(f"{role}: {round((round(role_personal_wins[role]['wins'] / role_personal_wins[role]['rounds'] * 100, 2)) /  (round(role_team_wins[role]['wins'] / role_team_wins[role]['rounds'] * 100, 2)) * 100, 2)}%")




