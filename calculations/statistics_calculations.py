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

with open('data/statistics.txt', 'r') as f:
    win_team_count = 0
    total = 0
    alive_count = 0
    dead_count = 0
    top_kills = 0
    top_killers = []
    all_players = []
    total_kills = 0
    for i in f:
        stats = parse_message(i)
        total += 1
        if 'winTeam' in stats.keys():
            win_team_count += 1
        if stats['alive'] == 'true':
            alive_count += 1
        else:
            dead_count += 1
        if 'playersKilled' in stats:
            total_kills += stats['playersKilled']
            if stats['playersKilled'] > top_kills:
                top_kills = stats['playersKilled']
                top_killers.clear()
                top_killers.append(stats['name'])
            if stats['playersKilled'] == top_kills:
                top_killers.append(stats['name'])
    print(alive_count)
    print(dead_count)
    print(total)
    print(win_team_count)
    print(f"top kills: {top_kills}")
    print(f"top killers: {top_killers}")
    print(f"total kills: {total_kills}")
    print(f"avg kils: {total_kills / total}")


