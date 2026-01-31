from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
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
time = "30d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    map_shares = {}  # map → sum of % when available
    map_counts = {}  # map → times it was available (one of 5)
    map_selected = {}  # map → times it was actually selected (non-ambiguous)

    for line in file:
        map_shares = {}  # sum of % when available
        map_counts = {}  # times available
        map_selected = {}  # times actually selected (non-ambiguous)

        for line in file:
            vote = log(line)
            voting_dict = {}

            for part in vote.votingData.split(","):
                if '=' not in part:
                    continue
                k, v = part.split("=", 1)
                if k in ("playercount", "random"):
                    continue
                try:
                    voting_dict[k] = int(v)
                except:
                    pass

            if not voting_dict:
                continue

            total_votes_this_round = sum(voting_dict.values())
            percents = calculate_percentages(voting_dict, should_round=True)

            # Record availability & vote share
            for m, p in percents.items():
                if m not in map_shares:
                    map_shares[m] = 0.0
                    map_counts[m] = 0
                    map_selected[m] = 0

                map_shares[m] += p
                map_counts[m] += 1

            # Only count selection if unambiguous (one clear winner)
            if total_votes_this_round > 0:
                max_votes = max(voting_dict.values())
                winners = [m for m, cnt in voting_dict.items() if cnt == max_votes]
                if len(winners) == 1:
                    winner = winners[0]
                    map_selected[winner] += 1

        # Build the three dictionaries
        average_vote_shares = {}
        selection_rates = {}
        appearance_counts = {}

        for m in sorted(map_counts.keys()):
            appearances = map_counts[m]
            if appearances == 0:
                continue

            avg_share = round(map_shares[m] / appearances, 2)
            selected_count = map_selected.get(m, 0)
            select_rate = round((selected_count / appearances) * 100, 2) if appearances > 0 else 0.0

            average_vote_shares[m] = avg_share
            selection_rates[m] = select_rate
            appearance_counts[m] = appearances

        # Print them separately
        print("Average vote share (%) when available:")
        print(average_vote_shares)
        print("\nSelection rate (%) when available (non-ambiguous rounds only):")
        print(selection_rates)
        print("\nAppearance counts:")
        print(appearance_counts)

