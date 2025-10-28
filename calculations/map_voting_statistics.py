def calculate_percentages(items, should_round: bool = False):
    new_percentages = {}
    total = sum(value for value in items.values())
    for key, value in items.items():
        try:
            new_percentages[key] = (value / total) * 100
        except ZeroDivisionError as e:
            new_percentages[key] = 0
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
game_version = "2weeks"
with (open(fr'C:\Users\jacta\PycharmProjects\PythonProject1\data\{game_version}.voting_data.txt', 'r') as file):
    total_votes = {}
    total_vote_count = 0
    rounds = 0
    total_vote_percent = 0
    avg_vote_percent_per_map = {}
    map_seen_count = {}
    maps = []
    for i in file:
        rounds += 1
        voting_dict, player_count = parse_voting_message(i)
        total_round_votes = 0
        voting_dict_percent = calculate_percentages(voting_dict, False)
        for name, count in voting_dict.items():
            if name not in maps:
                maps.append(name)
            total_vote_count += count
            total_round_votes += count
            if name not in total_votes:
                total_votes[name] = 0
            if name not in map_seen_count:
                map_seen_count[name] = 0
            map_seen_count[name] += 1
            if name not in avg_vote_percent_per_map:
                avg_vote_percent_per_map[name] = 0
            avg_vote_percent_per_map[name] += voting_dict_percent[name]
            total_votes[name] += count
        total_vote_percent += total_round_votes / player_count * 100
#


print(sort(total_votes))
print(f"TOTAL VOTE COUNT: {total_vote_count}")
print(f"vote % {total_vote_percent / rounds}")
print("avg % of vote share when available to vote")
idx = 0
for name, percent in sort(avg_vote_percent_per_map).items():
    idx += 1
    print(f"{idx}. {name}: {percent / map_seen_count[name]}")
print(", ".join(maps))
