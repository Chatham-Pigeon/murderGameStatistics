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

game_version = "1.0"
total_games_played = 0
with open(f'../old_data/{game_version}.statistics.txt', 'r') as f:
    #initalizing variables
    health_healed = {}
    games_played = {}
    bows_shot = {}
    bows_hit = {}
    # combining all the old_data
    for data in f:
        if game_version == "0.0":
            data = f"(0.0) {data}"
        stats = parse_message(data)
        total_games_played += 1
        if stats['name'] not in games_played:
            games_played[stats['name']] = 0
        games_played[stats['name']] += 1

        if 'healthHealed' in stats:
            if stats['name'] not in health_healed:
                health_healed[stats['name']] = 0
            health_healed[stats['name']] += stats['healthHealed']

        if stats['name'] not in bows_shot:
            bows_hit[stats['name']] = 0
            bows_shot[stats['name']] = 0
        if 'bowsShot' in stats:
            bows_shot[stats['name']] += stats['bowsShot']
        if 'bowsLanded' in stats:
            bows_hit[stats['name']] += stats['bowsLanded']
bow_rate = {}
for name, value in bows_hit.items():
        if not bows_shot[name] == 0 or not bows_hit[name] == 0:
            bow_rate[name] = bows_hit[name] / bows_shot[name] * 100
idx = 0
for name, value in sort(bow_rate).items():
    if games_played[name] >= 50:
        idx += 1
        if idx > 25:
            break
        print(f"{idx}. {name}: {value}")


