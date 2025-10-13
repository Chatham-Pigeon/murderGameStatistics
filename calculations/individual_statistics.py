import datetime

def sort(items):
    return dict(sorted(items.items(), key=lambda x: x[1], reverse=True))
def sort_dict_by_key(meow):
    return dict(sorted(meow.items(), reverse=True))

def sort_dict_by_nested_value(items, key, reverse=True):
    return dict(sorted(items.items(), key=lambda x: x[1].get(key, 0), reverse=reverse))
def calculate_percentages(items, should_round: bool = False):
    new_percentages = {}
    total = sum(value for value in items.values())
    for key, value in items.items():
        new_percentages[key] = (value / total) * 100
        if should_round is True:
            new_percentages[key] = round(new_percentages[key], 2)
    return new_percentages

def parse_message(content):
    statistics = {}
    content: str = content.replace("\n", "")
    content = content.partition("{")[2].replace("}", "")
    content: list = content.split(",")
    for j in content:
        j = j.strip().split(":")
        value = j[1].strip()
        try:
            value = float(value)
        except ValueError:
            value = f"{value}"
        statistics[f"{j[0]}"] = value
    return statistics
all_stats = []
game_version = "1.0"
games_played = 0
player = input("Player: ")
with open(f'../data/{game_version}.statistics.txt', 'r') as f:
    #initalizing variables
    health_healed = 0
    wins = 0
    losses = 0
    total_time_alive = 0
    kills = 0
    highest_kill_count = 0
    bow_shots = 0
    bow_hits = 0
    played_maps = {}
    melee_hits = 0
    melee_attempts = 0
    role_win_data = {"innocent": {"wins": 0, "losses": 0}, "detective": {"wins": 0, "losses": 0}, "traitor": {"wins": 0, "losses": 0}, "accomplice": {"wins": 0, "losses": 0}, "fiend": {"wins": 0, "losses": 0}, "doctor": {"wins": 0, "losses": 0}}    # combining all the data
    for data in f:
        if game_version == "0.0":
            data = f"(0.0) {data}"
        stats = parse_message(data)
        if not stats['name'] == player:
            continue
        games_played += 1
        if 'healthHealed' in stats:
            health_healed += stats['healthHealed']

        if stats['map'] not in played_maps:
            played_maps[stats['map']] = 1
        else:
            played_maps[stats['map']] += 1

        if stats['alive'] == "true":
            wins += 1
            role_win_data[stats['role']]['wins'] += 1
        else:
            losses += 1
            role_win_data[stats['role']]['losses'] += 1
        if 'timeAlive' in stats:
            total_time_alive += stats['timeAlive']

        if "playersKilled" in stats:
            kills += stats['playersKilled']
            if stats['playersKilled'] > highest_kill_count:
                highest_kill_count = stats['playersKilled']

        if 'bowsShot' in stats:
            bow_shots += stats['bowsShot']
        if 'bowsLanded' in stats:
            bow_hits += stats['bowsLanded']
        if 'meleeSucesses' in stats:
            melee_hits += stats['meleeSucesses']
            melee_attempts += stats['meleeAttempts']


# calculating information from data
highest_count = 0
most_played_maps = []
for map_name, count in played_maps.items():
    # current map played count is same as highest seen,, therefore played even amount
    if count == highest_count:
        most_played_maps.append(map_name)
    # seen count higher than new count,,, new highest map found
    if count > highest_count:
        most_played_maps.clear()
        most_played_maps.append(map_name)
        highest_count = count
# since its only 1 map dont display it as a list
if len(most_played_maps) == 1:
    most_played_maps = most_played_maps[0]
# ['healthHealed', 'map', 'name', 'role', 'alive', 'damageReceived', 'totalDamageDealt', 'bowsShot', 'bowsLanded', 'timeAlive', 'playersKilled', 'meleeAttempts']
# displaying data
print(f"Total Health Healed: {health_healed}")
print(f"Average Health healed: {health_healed / games_played}")
print(f"Most played map {most_played_maps}")
print(f"Least played map: {"NOTHING I CBF!!"}")
print(f"Total Wins: {wins}")
print(f"Total Losses: {losses}")
print(f"Win Loss Ratio: {wins / losses}")
print(f"Win percentage: {wins / (wins + losses) * 100}")
print(f"Total Time spent alive {round(total_time_alive / 20 / 60 / 60, 2)}h")
print(f"Average time spent alive {round(total_time_alive / games_played / 20 / 60, 2)}m")
print(f"Total kills {kills}")
print(f"Kill/Death ratio: {kills / losses}")
print(f"Highest kill count in a round {highest_kill_count}")
print(f"Games played: {games_played}")
print(f"Bow Shots {bow_shots}")
print(f"Bow Hits {bow_hits}")
print(f"Bow Percent {bow_hits / bow_shots * 100}")
print(f"bow Rate {bow_hits / bow_shots}")
print(f"melee attempts: {melee_attempts}")
print(f"melee successes: {melee_hits}")
print(f"melee percent {melee_hits / melee_attempts * 100}")
for role, role_data in role_win_data.items():
    print(f"{role} WIN PERCENT: {calculate_percentages(role_data, True)}")