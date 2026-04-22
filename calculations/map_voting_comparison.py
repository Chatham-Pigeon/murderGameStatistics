from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
from collections import defaultdict
from itertools import combinations

class log:
    def __init__(self, raw_data: str):
        self.gameRound = None
        self.timestamp = None
        self.votingData = None
        self.playercount = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")

log_name = "map-voting"
time = "49d"

pair_shares = defaultdict(lambda: defaultdict(list))

with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    for line in file:
        vote = log(line)

        voting_dict = {}
        for part in vote.votingData.split(","):
            if '=' not in part:
                continue
            k, v = part.split("=", 1)
            if k == "Sinister Sancutary":
                k = "Sinister Sanctuary"
            if "IKEA" in k:
                k = "IKEA"
            if k in ("playercount", "random"):
                continue
            voting_dict[k] = int(v)

        if not voting_dict:
            continue

        percents = calculate_percentages(voting_dict, should_round=True)
        maps_in_round = list(voting_dict.keys())

        for map_a, map_b in combinations(maps_in_round, 2):
            pair = tuple(sorted([map_a, map_b]))
            total_ab = percents[map_a] + percents[map_b]
            if total_ab == 0:
                continue
            pair_shares[pair][map_a].append(round(percents[map_a] / total_ab * 100, 2))
            pair_shares[pair][map_b].append(round(percents[map_b] / total_ab * 100, 2))

map_wins = defaultdict(list)

for pair, shares in pair_shares.items():
    map_a, map_b = pair
    rounds = len(shares[map_a])
    avg_a = round(sum(shares[map_a]) / rounds, 2)
    avg_b = round(sum(shares[map_b]) / rounds, 2)
    if avg_a > avg_b:
        map_wins[map_a].append((map_b, avg_a, avg_b))
    else:
        map_wins[map_b].append((map_a, avg_b, avg_a))

for map_name, wins in sorted(map_wins.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"{map_name} ({len(wins)} wins):")
    for beaten, winner_pct, loser_pct in sorted(wins, key=lambda x: x[1], reverse=True):
        print(f"  - {beaten} ({winner_pct}% vs {loser_pct}%)")