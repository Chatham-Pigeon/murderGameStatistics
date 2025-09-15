def calculate_percentages(items, should_round: bool = False):
    new_percentages = {}
    total = sum(value for value in items.values())
    for key, value in items.items():
        new_percentages[key] = (value / total) * 100
        if should_round is True:
            new_percentages[key] = round(new_percentages[key], 2)
    return new_percentages
def sort(items):
    return dict(sorted(items.items(), key=lambda x: x[1], reverse=True))
def sort_dict_by_key(meow):
    return dict(sorted(meow.items(), reverse=True))
def sort_dict_by_nested_value(items, key, reverse=True):
    return dict(sorted(items.items(), key=lambda x: x[1].get(key, 0), reverse=reverse))

def parse_voting_message(message: str):
    # (1.0) 2025/9/15 06:13PM plot: The Mineshafts,0:Mediterranean,0:Oil Rig,3:The Aquarium,1:The Depths,0:random:0#7
    data_split = message.split(":")
    # remove the time & plot metadata, save the data version at the start but remove brackets
    data_version = data_split.pop(0).split(" ").pop(0).replace("(", "").replace(")", "")
    # delete the 13PM plot that is split because of the : in the time
    data_split.pop(0)
    # last index includes playercount & votes for random
    last_index = data_split.pop(-1).split("#")
    # get playercount
    player_count = last_index[1]
    # move the votes for "random" actually into the "random" list value
    data_split[-1] = f"{data_split[-1]},{last_index[0]}"
    voting_data = {}
    for i in data_split:
        pass
        i = i.strip()
        map_name, vote_count = i.split(",")
        voting_data[map_name] = int(vote_count)
    return voting_data, int(player_count)
game_version = "1.0"
with (open(fr'C:\Users\jacta\PycharmProjects\PythonProject1\data\{game_version}.voting_data.txt', 'r') as file):
    total_votes = {}
    total_vote_count = 0
    rounds = 0
    total_vote_percent = 0
    for i in file:
        rounds += 1
        voting_dict, player_count = parse_voting_message(i)
        total_round_votes = 0
        for name, count in voting_dict.items():
            total_vote_count += count
            total_round_votes += count
            if name not in total_votes:
                total_votes[name] = 0
            total_votes[name] += count
        total_vote_percent += total_round_votes / player_count * 100
        print(total_vote_percent)
print(sort(total_votes))
print(f"TOTAL VOTE COUNT: {total_vote_count}")
print(f"vote % {total_vote_percent / rounds}")

