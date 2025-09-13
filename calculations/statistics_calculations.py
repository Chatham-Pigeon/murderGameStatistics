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
with open(f'../data/{game_version}.statistics.txt', 'r') as f:
    win_team_count = 0
    total = 0
    alive_count = 0
    dead_count = 0
    top_kills = 0
    top_killers = []
    all_players = []
    index_of_that = []
    total_kills = 0
    total_has_kills = 0
    player_won_count = 0
    player_lost_count = 0
    total_shots = 0
    total_hits = 0
    games_played = 0
    players_win_rate = {}
    players_win_rate_percent = {}
    time_played = {}
    players_bow_rate = {}
    players_bow_rate_percent = {}
    players_kills_rate = {}
    players_kills_rate_percent = {}
    players_healed_amt = {}
    count = 0
    for i in f:
        count += 1
        if game_version == "0.0":
            i = f"(0.0) {i}"
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
            if stats['playersKilled'] == top_kills:
                top_killers.append(stats['name'])
                index_of_that.append(count)
            if stats['playersKilled'] > top_kills:
                top_kills = stats['playersKilled']
                top_killers.clear()
                index_of_that.clear()
                top_killers.append(stats['name'])
                index_of_that.append(count)

            total_has_kills += 1
        if not stats['name'] in players_win_rate:
            players_win_rate[stats['name']] = {'games': 0, 'won': 0, "lost": 0}
        if not stats['name'] in time_played:
            time_played[stats['name']] = 0
        if not stats['name'] in players_bow_rate:
            players_bow_rate[stats['name']] = {"shot": 0, "hit": 0}
        if not stats['name'] in players_kills_rate:
            players_kills_rate[stats['name']] = {"kills": 0, "deaths": 0}
        if not stats['name'] in players_healed_amt:
            players_healed_amt[stats['name']] = 0


        if 'bowsShot' in stats:
            total_shots += 1
            players_bow_rate[stats['name']]['shot'] += 1
        if 'bowsLanded' in stats:
            total_hits += 1
            players_bow_rate[stats['name']]['hit'] += 1
        if stats["alive"] == 'true':
            player_won_count += 1
            players_win_rate[stats['name']]['won'] += 1
        else:
            player_lost_count += 1
            players_win_rate[stats['name']]['lost'] += 1
            players_kills_rate[stats['name']]['deaths']  += 1
        if 'timeAlive' in stats:
            time_played[stats['name']] += int(stats['timeAlive'])
        players_win_rate[stats['name']]['games'] += 1
        if 'playersKilled' in stats:
            players_kills_rate[stats['name']]['kills']  += stats['playersKilled']
        if 'totalDamageDealt' in stats:
            players_healed_amt[stats['name']] += stats['totalDamageDealt']


    print(alive_count)
    print(dead_count)
    print(total)
    print(win_team_count)
    print(f"top kills: {top_kills}")
    print(f"top killers: {top_killers}")
    print(f"index of that {index_of_that}")
    print(f"total kills: {total_kills}")
    print(f"avg kils: {total_kills / total}")
    print(f"avg kills where atleast 1 {total_kills / total_has_kills}")
    print(f"player win count: {player_won_count}")
    print(f"player lost count {player_lost_count}")
    print(f"win percent {player_won_count / (player_lost_count + player_won_count) * 100}")
    print(f"bows hit {total_shots / (total_shots + total_hits) * 100}")
    print(f"raw {total_hits} {total_shots}")
    print(f"games played {games_played}")
    index = 0
    for name, data in sort_dict_by_nested_value(players_win_rate, 'won').items():
        index += 1
        if index > 11:
            break
        print(f"!!! {index}. {name}: {data['won']}")
        total_games = data.pop('games')
        if total_games >= 15:
            players_win_rate_percent[name] = calculate_percentages(data, True)
    print("player win rate percent")
    index = 0
    for name, data in sort_dict_by_nested_value(players_win_rate_percent, 'won').items():
        index += 1
        print(f"{index}. {name}: {data}")
    print("player bow rate %")
    index = 0
    for name, data in players_bow_rate.items():
        index += 1
        if data['hit'] > 0 and data['shot'] > 0:
            players_bow_rate_percent[name] = data['shot'] / (data['shot'] + data['hit']) * 100
    index = 0
    for name, data in sort(players_bow_rate_percent).items():
        index += 1
        if index > 11:
            break
        print(f"{index}. {name}: {data}")
    print("TIME PLAYED!!")
    index = 0
    for name, time in sort(time_played).items():
        index += 1
        if index > 26:
            break
        print(f"{index}. {name}: {float(time / 20 / 60 / 60)}")
    print("KILLS/DEATHS!!")
    index = 0
    for name, data in players_kills_rate.items():
        index += 1
        if data['kills'] > 10 and data['deaths'] > 10:
            players_kills_rate_percent[name] = round(data['kills'] / data['deaths'], 2)
    index = 0
    for name, data in sort(players_kills_rate_percent).items():
        index += 1
        if index > 11:
            break
        print(f"{index}. {name}: {data} ({int(players_kills_rate[name]['kills'])}/{int(players_kills_rate[name]['deaths'])})")
    index = 0
    for name, amt in sort(players_healed_amt).items():
        index += 1
        if index > 26:
            break
        print(f"{index}. {name}")






