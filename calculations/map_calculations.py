import datetime


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
game_version = "21.8"
#game_version = "1.0"
with (open(fr'C:\Users\jacta\PycharmProjects\PythonProject1\data\{game_version}.map_data.txt', 'r') as file):
    fiend_role_wins = {"traitor": 0, "innocents": 0}
    win_dict = {"traitor": 0, "innocents": 0, "fiend": 0}
    map_count = {}
    map_role_wins = {}
    total_rounds = 0
    avg_game_length = 0
    map_avg_length = {}
    avg_team_win_length = {}
    game_length_per_count = {}
    player_count_count = {}
    game_length_per_count_formatted = {}
    median_game_length_per_count = {}
    win_team_per_player_count = {}
    most_played_map_per_player_count = {}
    count = 0
    last_win_team = ""
    innocent_streak = 0
    traitor_streak = 0
    fiend_streak = 0
    high_inno_streak = 0
    high_traitor_streak = 0
    high_fiend_streak = 0
    inno_where = 0
    trait_where = 0
    fiend_where = 0
    for i in file:
        count += 1
        game_round, map_name, win_team, fiend_win, game_length, player_count, fiend_count = i.split(" ")
        if win_team == 'Traitors':
            win_team = 'traitor'
        if win_team == 'Citizens':
            win_team = "innocents"
        if map_name == "Forst_Mansion":
            map_name = "Forest_Mansion"
        streak_win_team = win_team
        if fiend_win == 'true':
            streak_win_team = 'fiend'
        if streak_win_team == last_win_team:
            if int(player_count) >= 7:
                if streak_win_team == "traitor":
                    traitor_streak += 1
                if streak_win_team == "innocents":
                    innocent_streak += 1
                if streak_win_team == "fiend":
                    fiend_streak += 1
            else:
                if traitor_streak >= high_traitor_streak:
                    high_traitor_streak = traitor_streak + 1
                    trait_where = game_round
                if innocent_streak >= high_inno_streak:
                    high_inno_streak = innocent_streak + 1
                    inno_where = game_round
                if fiend_streak >= high_fiend_streak:
                    high_fiend_streak = fiend_streak + 1
                    fiend_where = game_round
                traitor_streak = 0
                innocent_streak = 0
                fiend_streak = 0
        else:
            if traitor_streak >= high_traitor_streak:
                high_traitor_streak = traitor_streak + 1
                trait_where = game_round
            if innocent_streak >= high_inno_streak:
                high_inno_streak = innocent_streak + 1
                inno_where = game_round
            if fiend_streak >= high_fiend_streak:
                high_fiend_streak = fiend_streak + 1
                fiend_where = game_round
            traitor_streak = 0
            innocent_streak = 0
            fiend_streak = 0

        last_win_team = streak_win_team
        inted_player_count = int(player_count)
        if inted_player_count not in game_length_per_count:
            game_length_per_count[int(player_count)] = [int(game_length)]
        else:
            game_length_per_count[int(player_count)].append(int(game_length))

        if inted_player_count not in player_count_count:
            player_count_count[int(player_count)] = 1
        else:
            player_count_count[int(player_count)] = player_count_count[int(player_count)] + 1

        if inted_player_count not in most_played_map_per_player_count:
            most_played_map_per_player_count[inted_player_count] = {f"{map_name}": 1}
        else:
            if map_name not in most_played_map_per_player_count[inted_player_count]:
                most_played_map_per_player_count[inted_player_count][map_name] = 1
            else:
                most_played_map_per_player_count[inted_player_count][map_name] += 1

        if inted_player_count not in win_team_per_player_count.keys():
            win_team_per_player_count[inted_player_count] = {"traitor": 0, "innocents": 0, "fiend": 0}
            if fiend_win == 'true':
                win_team_per_player_count[inted_player_count]['fiend'] = 1
            else:
                win_team_per_player_count[inted_player_count][win_team] = 1
        else:
            if fiend_win == 'true':
                win_team_per_player_count[inted_player_count]['fiend'] = win_team_per_player_count[inted_player_count]['fiend'] + 1
            else:
                win_team_per_player_count[inted_player_count][win_team] = win_team_per_player_count[inted_player_count][win_team] + 1
        if int(player_count) < 7:
            continue
        avg_game_length = avg_game_length + int(game_length)
        total_rounds = total_rounds + 1
        if fiend_win == 'true':
            if 'fiend' not in avg_team_win_length:
                avg_team_win_length['fiend'] = int(game_length)
            else:
                avg_team_win_length['fiend'] = avg_team_win_length['fiend'] + int(game_length)
        else:
            if win_team not in avg_team_win_length:
                avg_team_win_length[win_team] = int(game_length)
            else:
                avg_team_win_length[win_team] = avg_team_win_length[win_team] + int(game_length)
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
        if map_name not in map_avg_length:
            map_avg_length[map_name] = int(game_length)
        else:
            map_avg_length[map_name] = map_avg_length[map_name] + int(game_length)



    for name, length in avg_team_win_length.items():
        length = (length / 20)
        minutes, seconds = divmod(length / win_dict[name], 60)
        avg_team_win_length[name] = f"{int(minutes)}m{int(round(seconds, 0))}s"

    for name, length in map_avg_length.items():
        length = (length / 20)
        minutes, seconds = divmod(length / map_count[name], 60)
        map_avg_length[name] = f"{int(minutes)}m{int(round(seconds, 0))}s"
    index = 0
    print("win team percent per player count")
    win_team_per_player_count_percentage = {}
    for count, wins in win_team_per_player_count.items():
        win_team_per_player_count_percentage[count] = calculate_percentages(wins, True)
    for count, wins in sort_dict_by_key(win_team_per_player_count_percentage).items():
        index += 1
        print(f"{index}. {count}: {wins}")
    index = 0
    print(f"avg win length when team: {avg_team_win_length}")
    print(f"total_rounds: {total_rounds}")
    print(f"avg game lengt by map: {map_avg_length}")
    print(f"win count{win_dict}")
    print(f"wins%: {calculate_percentages(win_dict)}")
    print(f"winner when fiend overrides win %, {calculate_percentages(fiend_role_wins)}")
    print(f"mapcount: {sort(map_count)}")
    print(f"mapcount%: {sort(calculate_percentages(map_count, True))}")
    minutes, remaining_seconds = divmod((avg_game_length/total_rounds)/20, 60)
    print(f"avg game length: {minutes}m{remaining_seconds}s")
    index = 0
    print("role win % by map:")
    map_role_wins_percentage = {}
    for name, wins in map_role_wins.items():
        map_role_wins_percentage[name] = calculate_percentages(wins, True)
    for name, wins in sort_dict_by_nested_value(map_role_wins_percentage, "fiend", True).items():
        index += 1
        print(f"{index}. {name}: {wins}")
    index = 0
    for count, lengths in game_length_per_count.items():
        if len(lengths) % 2 == 0:
            if len(lengths) < 2:
                continue
            middle_left = lengths[(len(lengths) // 2) - 1]
            middle_right = lengths[len(lengths) // 2]
            median = (middle_left + middle_right) / 2
        else:
            median = lengths[len(lengths) // 2]
        minutes, seconds = divmod(median / 20, 60)
        median_game_length_per_count[int(count)] = f"{int(minutes)}m{round(seconds, 2)}s"

    for count, lengths in game_length_per_count.items():
        count = int(count)
        game_length_per_count_formatted[count] = sum(lengths) / len(lengths) / 20
        minutes, remaining_seconds = divmod(game_length_per_count_formatted[count], 60)
        game_length_per_count_formatted[count] = f"{int(round(minutes, 2))}m{round(remaining_seconds, 2)}s"

    print(f"Game length per playercount: {sort_dict_by_key(game_length_per_count_formatted)}")
    print(f"player count count: {sort_dict_by_key(player_count_count)}")
    print(f"median player count per length: {sort_dict_by_key(median_game_length_per_count)}")
    print(f"most played map per player count:")
    for count, meowdict in sort_dict_by_key(most_played_map_per_player_count).items():
        print(f"{count}: {sort(calculate_percentages(meowdict, True))}")
    print(f"BIG INNO STREAK: {high_inno_streak}")
    print(f"BIG TRAITOR STREAK: {high_traitor_streak}")
    print(f"BIG FIEND STREAK: {high_fiend_streak}")

    print(f"trait where {trait_where} inno where: {inno_where} fiend where: {fiend_where}")


