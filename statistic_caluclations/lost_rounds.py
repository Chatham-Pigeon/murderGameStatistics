from SECRETS import *


class log:
    def __init__(self, raw_data: dict):
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
        if "IKEA" in self.map:
            self.map = "IKEA"


start_time = "1780272000"
rows = query(f"SELECT * FROM games WHERE plotID = {PLOT_ID} AND timestamp >= {start_time}")
logs = [log(i) for i in rows]
logs_dict = {f"{log(i).gameRound}": log(i) for i in rows}

# --- Round stats ---
round_nums = [data.gameRound for data in logs]

total_rounds = len(round_nums)
lowest_round = min(round_nums)
highest_round = max(round_nums)

full_range = set(range(lowest_round, highest_round + 1))
existing_rounds = set(round_nums)
missing_rounds = sorted(full_range - existing_rounds)

expected_count = len(full_range)
missing_count = len(missing_rounds)
existing_count = len(existing_rounds)

missing_pct = (missing_count / expected_count) * 100
existing_pct = (existing_count / expected_count) * 100



# --- All missing sequences longer than 1 ---
sequences = []
current_seq = []

for r in missing_rounds:
    if not current_seq or r == current_seq[-1] + 1:
        current_seq.append(r)
    else:
        if len(current_seq) >= 1:
            sequences.append(current_seq)
        current_seq = [r]

if len(current_seq) >= 1:
    sequences.append(current_seq)

sequences.sort(key=lambda s: len(s), reverse=True)

print("Missing sequences (>1):")
for seq in sequences:
    print(f"  {seq[0]}–{seq[-1]} ({len(seq)} rounds)")


print(f"Total rounds:   {total_rounds}")
print(f"Lowest round:   {lowest_round}")
print(f"Highest round:  {highest_round}")
print(f"Missing rounds: {missing_count} ({missing_pct:.1f}%) — {missing_rounds}")
print(f"Existing rounds: {existing_count} ({existing_pct:.1f}%)")


recent_missing_round = missing_rounds[-1] + 1
round_after_recent_missing = logs_dict[f"{recent_missing_round}"]
print(f"timestamp of round after latest missing: {round_after_recent_missing.timestamp}")
print(f"latest mssing round: {recent_missing_round}")
