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
class killLog:
    def __init__(self, victim, victim_role, death_cause, victim_arrow_count, killer, killer_role, killer_hand_item,killer_health, game_length_at_death):
        self.victim = victim
        self.victim_role = victim_role
        self.death_cause = death_cause
        self.victim_arrow_count = victim_arrow_count
        self.killer = killer
        self.killer_role = killer_role
        self.killer_hand_item = killer_hand_item
        self.killer_health = killer_health
        self.game_length_at_death = game_length_at_death
def parse_kill_message(message: str):
    message = message.split(" ")
    message.pop(0)
    message.pop(0)
    message.pop(0)
    game_id = message.pop(0).removesuffix(":")
    message = message[0].split(":")
    return killLog(message[0], message[1], message[2], message[3], message[4], message[5], message[6], message[7], message[8]), game_id

game_version = "1.0"
traitor_team = ['traitor', 'accomplice']
citizen_team = ['detective', 'innocent', 'doctor']
with open(f'../data/{game_version}.kills.txt', 'r') as file:
    recorded_games = []
    arrows_left_over = 0
    deaths = 0
    traitor_tks = 0
    inno_inno_tks = 0
    team_killers = {}
    arrow_count_left_over_count = {}
    death_causes = {}
    those_kinda_kills = 0
    most_killed_with_item = {}
    for line in file:
        deaths += 1
        kill, game_id = parse_kill_message(line)
        if not game_id in recorded_games:
            recorded_games.append(game_id)
        arrows_left_over += int(kill.victim_arrow_count)
        if int(kill.victim_arrow_count) not in arrow_count_left_over_count:
            arrow_count_left_over_count[int(kill.victim_arrow_count)] = 0
        arrow_count_left_over_count[int(kill.victim_arrow_count)] += 1
        if kill.death_cause not in death_causes:
            death_causes[kill.death_cause] = 0
        death_causes[kill.death_cause] += 1

        if kill.killer_hand_item not in most_killed_with_item:
            most_killed_with_item[kill.killer_hand_item] = 0
        most_killed_with_item[kill.killer_hand_item] += 1
        if kill.death_cause in ['projectile', "entity_attack"]:
            if kill.killer_role in traitor_team and kill.victim_role in traitor_team:
                traitor_tks += 1
                if kill.killer not in team_killers:
                    team_killers[kill.killer] = 0
                team_killers[kill.killer] += 1
            if kill.victim_role in citizen_team and kill.killer_role in citizen_team:
                inno_inno_tks += 1
                if kill.killer not in team_killers:
                    team_killers[kill.killer] = 0
                team_killers[kill.killer] += 1
        if kill.death_cause == "projectile" and not kill.killer_hand_item == "bow":
            those_kinda_kills += 1

print(f"avg arrows leftover per death {arrows_left_over / deaths}")
print(f" raw arrow leftover{arrows_left_over}")
print(f"arrows leftover dict {sort(arrow_count_left_over_count)}")
