import datetime
from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages

class roundData:
    # game_round, map_name, win_team, fiend_win, game_length, player_count, fiend_count
    # (1.0) **2025/11/3 01:07AM** 54653: The Trials:Citizens:false:854:4:0
    def __init__(self, input_string: str):
        if "#" in input_string:
            timestamp = input_string.split("#", 1)[0]
            input_string = input_string.split("#", 1)[1]
        else:
            timestamp = None
        data = input_string.split(":")
        data.pop(0)
        self.game_round = data.pop(0).split(" ")[1].removesuffix(":")
        self.map_name = data.pop(0).strip()
        self.win_team = data.pop(0)
        self.fiend_win = data.pop(0)
        self.game_length = data.pop(0)
        self.player_count = data.pop(0)
        self.fiend_count = data.pop(0).strip()
        self.timestamp = int(timestamp)
        if self.win_team == 'Traitors':
            self.win_team = 'traitor'
        if self.win_team == 'Citizens':
            self.win_team = "innocents"
        if self.map_name == "Forst_Mansion":
            self.map_name = "Forest_Mansion"



time_length = "allTime"
before_time = 1757415600
after_time = 1757415600 - 2592000
with (open(fr'C:\Users\jacta\PycharmProjects\PythonProject1\new_data\{time_length}.round-data.txt', 'r') as file):
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
    shortest_length = {}
    shortest_length_where = {}
    for i in file:
        count += 1
        round_info: roundData = roundData(i)
        if round_info.timestamp < after_time:
            continue
        if round_info.timestamp > before_time:
            continue
        if int(round_info.player_count) < 7:
            continue
        if int(round_info.player_count) not in shortest_length:
            shortest_length[int(round_info.player_count)] = int(round_info.game_length)
            shortest_length_where[int(round_info.player_count)] = round_info.game_round
        if shortest_length[int(round_info.player_count)] > int(round_info.game_length):
            shortest_length[int(round_info.player_count)] = int(round_info.game_length)
            shortest_length_where[int(round_info.player_count)] = round_info.game_round

        streak_win_team = round_info.win_team
        if round_info.fiend_win == 'true':
            streak_win_team = 'fiend'
        if streak_win_team == last_win_team:
            if int(round_info.player_count) >= 7:
                if streak_win_team == "traitor":
                    traitor_streak += 1
                if streak_win_team == "innocents":
                    innocent_streak += 1
                if streak_win_team == "fiend":
                    fiend_streak += 1
            else:
                if traitor_streak >= high_traitor_streak:
                    high_traitor_streak = traitor_streak + 1
                    trait_where = round_info.game_round
                if innocent_streak >= high_inno_streak:
                    high_inno_streak = innocent_streak + 1
                    inno_where = round_info.game_round
                if fiend_streak >= high_fiend_streak:
                    high_fiend_streak = fiend_streak + 1
                    fiend_where = round_info.game_round
                traitor_streak = 0
                innocent_streak = 0
                fiend_streak = 0
        else:
            if traitor_streak >= high_traitor_streak:
                high_traitor_streak = traitor_streak + 1
                trait_where = round_info.game_round
            if innocent_streak >= high_inno_streak:
                high_inno_streak = innocent_streak + 1
                inno_where = round_info.game_round
            if fiend_streak >= high_fiend_streak:
                high_fiend_streak = fiend_streak + 1
                fiend_where = round_info.game_round
            traitor_streak = 0
            innocent_streak = 0
            fiend_streak = 0

        last_win_team = streak_win_team
        inted_player_count = int(round_info.player_count)
        if inted_player_count not in game_length_per_count:
            game_length_per_count[int(round_info.player_count)] = [int(round_info.game_length)]
        else:
            game_length_per_count[int(round_info.player_count)].append(int(round_info.game_length))

        if inted_player_count not in player_count_count:
            player_count_count[int(round_info.player_count)] = 1
        else:
            player_count_count[int(round_info.player_count)] = player_count_count[int(round_info.player_count)] + 1

        if inted_player_count not in most_played_map_per_player_count:
            most_played_map_per_player_count[inted_player_count] = {f"{round_info.map_name}": 1}
        else:
            if round_info.map_name not in most_played_map_per_player_count[inted_player_count]:
                most_played_map_per_player_count[inted_player_count][round_info.map_name] = 1
            else:
                most_played_map_per_player_count[inted_player_count][round_info.map_name] += 1

        if inted_player_count not in win_team_per_player_count.keys():
            win_team_per_player_count[inted_player_count] = {"traitor": 0, "innocents": 0, "fiend": 0}
            if round_info.fiend_win == 'true':
                win_team_per_player_count[inted_player_count]['fiend'] = 1
            else:
                win_team_per_player_count[inted_player_count][round_info.win_team] = 1
        else:
            if round_info.fiend_win == 'true':
                win_team_per_player_count[inted_player_count]['fiend'] = win_team_per_player_count[inted_player_count]['fiend'] + 1
            else:
                win_team_per_player_count[inted_player_count][round_info.win_team] = win_team_per_player_count[inted_player_count][round_info.win_team] + 1

        avg_game_length = avg_game_length + int(round_info.game_length)
        total_rounds = total_rounds + 1
        if round_info.fiend_win == 'true':
            if 'fiend' not in avg_team_win_length:
                avg_team_win_length['fiend'] = int(round_info.game_length)
            else:
                avg_team_win_length['fiend'] = avg_team_win_length['fiend'] + int(round_info.game_length)
        else:
            if round_info.win_team not in avg_team_win_length:
                avg_team_win_length[round_info.win_team] = int(round_info.game_length)
            else:
                avg_team_win_length[round_info.win_team] = avg_team_win_length[round_info.win_team] + int(round_info.game_length)
        if round_info.fiend_win == 'false':
            win_dict[round_info.win_team] = win_dict[round_info.win_team] + 1
        else:
            fiend_role_wins[round_info.win_team] = fiend_role_wins[round_info.win_team] + 1
            win_dict['fiend'] = win_dict['fiend'] + 1

        if round_info.map_name not in map_count.keys():
            map_count[round_info.map_name] = 1
            map_role_wins[round_info.map_name] = {"traitor": 0, "innocents": 0, "fiend": 0}
            if round_info.fiend_win == 'true':
                map_role_wins[round_info.map_name]['fiend'] = 1
            else:
                map_role_wins[round_info.map_name][round_info.win_team] = 1
        else:
            map_count[round_info.map_name] = map_count[round_info.map_name] + 1
            if round_info.fiend_win == 'true':
                map_role_wins[round_info.map_name]['fiend'] = map_role_wins[round_info.map_name]['fiend'] + 1
            else:
                map_role_wins[round_info.map_name][round_info.win_team] = map_role_wins[round_info.map_name][round_info.win_team] + 1
        if round_info.map_name not in map_avg_length:
            map_avg_length[round_info.map_name] = int(round_info.game_length)
        else:
            map_avg_length[round_info.map_name] = map_avg_length[round_info.map_name] + int(round_info.game_length)




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
    print(f"short game length: {sort(shortest_length)}")
    print(f"short game length wher {shortest_length_where}")


