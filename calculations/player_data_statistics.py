import ast
from datetime import datetime

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


def parse_message(content: str):
    player_data = {}
    content = content.replace("\n", "").strip()
    split_content = content.partition("{")
    meta_data = split_content[0].strip().split(" ")
    time_str = f"{meta_data[1].replace('*', '')} {meta_data[2].replace('*', '')}"
    time = datetime.strptime(time_str, "%Y/%m/%d %I:%M%p").timestamp()
    data_content = split_content[2].rstrip("}").strip()
    fields = [field.strip() for field in data_content.split(",")]
    for field in fields:
        if not field or ":" not in field:  # Skip empty or invalid fields
            continue
        key, value = [part.strip() for part in field.split(":", 1)]
        if key == "ignoreList" and value.startswith("[") and value.endswith("]"):
            try:
                parsed_list = ast.literal_eval(value)
                if isinstance(parsed_list, list):
                    player_data[key] = parsed_list
                else:
                    player_data[key] = value
            except (ValueError, SyntaxError):
                player_data[key] = value
        else:
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
                player_data[key] = value
            except ValueError:
                player_data[key] = value
    return player_data, time


wins_leaderboard = {}
game_version = "1.0"
cool_people = []
count = 0
role_wins = {"innocent": {}, "detective": {}, "doctor": {}, "fiend": {}, "traitor": {}, "accomplice": {}}
with open(f'../data/{game_version}.player_data.txt', 'r') as f:
    for line in f:
        count += 1
        print(count)
        data, time = parse_message(line)
        key: str
        for key, value in data.items():
            if key.startswith("roleWins."):
                key = key.replace("roleWins.", "")
                role_wins[key][data['name']] = value
        if "wins" in data:
            wins_leaderboard[data['name']] = data['wins']
        if "LSV" in data:
            if data['name'] not in cool_people:
                cool_people.append(data['name'])
        print(data)

print(f"all wins: {sort(wins_leaderboard)}")
for role, wins in role_wins.items():
    print(f"{role} wins: {sort(wins)}")
print(f"COOL PEOPLE {cool_people}")