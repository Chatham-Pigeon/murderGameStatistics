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

with (open('map_data.txt', 'r') as file):
    fiend_role_wins = {"traitor": 0, "innocents": 0}
    win_dict = {"traitor": 0, "innocents": 0, "fiend": 0}
    map_count = {}
    map_role_wins = {}
    for i in file:
        game_round, map_name, win_team, fiend_win, game_length, player_count, fiend_count = i.split(" ")
        if int(player_count) < 7:
            continue

        if fiend_win == 'false':
            win_dict[win_team] = win_dict[win_team] + 1
        else:
            fiend_role_wins[win_team] = fiend_role_wins[win_team] + 1
            win_dict['fiend'] = win_dict['fiend'] + 1

        if map_name not in map_count.keys():
            map_count[map_name] = 1
            map_role_wins[map_name] = {"traitor": 0, "innocents": 0, "fiend": 0}
            if fiend_win == 'true':
                map_role_wins[map_name]['fiend'] = 1
            else:
                map_role_wins[map_name][win_team] = 1
        else:
            map_count[map_name] = map_count[map_name] + 1
            if fiend_win == 'true':
                map_role_wins[map_name]['fiend'] = map_role_wins[map_name]['fiend'] + 1
            else:
                map_role_wins[map_name][win_team] = map_role_wins[map_name][win_team] + 1

    print(win_dict)
    print(f"wins: {calculate_percentages(win_dict)}")
    print(f"role when fiend win, {calculate_percentages(fiend_role_wins)}")
    print(f"mapcount: {sort(map_count)}")
    print(f"mapcount%: {sort(calculate_percentages(map_count))}")
    for name, wins in map_role_wins.items():
        print(f"{name}: {sort(calculate_percentages(wins, True))}")

