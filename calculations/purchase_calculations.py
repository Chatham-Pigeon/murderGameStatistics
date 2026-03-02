from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.name = None
        self.role = None
        self.gameRound = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")
id_to_name = {
    "stone_sword": "Stone Sword",
    "detective_hat": "Detective Hat",
    "heal_potion": "Potion of Healing",
    "speed_potion": "Potion of Speed",
    "new_detective_sword": "Sword of Justice",
    "traitor_finder": "Detective Scanner",
    "sponge": "Sponge",
    "enchanted_bow": "Enchanted Bow",
    "healing_station": "Health Kit",
    "new_milk": "Splash Potion of Milk",
    "slow_giver": "Curse of Slowness",
    "new_traitor_sword": "Backstab Sword",
    "teleporter": "Teleporter",
    "new_grenade": "Grenade",
    "tnt": "TNT",
    "compass": "Compass",
    "torch": "Torch",
    "damage_station": "Damage Kit",
    "purchased_nothing": "Purchased Nothing"

}

log_name = "player-stats"
time = "30d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    counts = {}
    role_purchases = {}
    buyers = {"speed_potion": {"Chatham_Pigeon": 1}}
    for line in file:
        save = log(line)
        save.purchases = save.purchases.replace("[", "").replace("]", "").split(", ")
        if not save.role in counts:
            counts[save.role] = 0
        counts[save.role] += 1
        if not save.role in role_purchases:
            role_purchases[save.role] = {}
        for item in save.purchases:
            if item == '':
                item = "purchased_nothing"
            if not item in role_purchases[save.role]:
                role_purchases[save.role][item] = 0
            role_purchases[save.role][item] += 1
            if item not in buyers:
                buyers[item] = {}
            if not save.name in buyers[item]:
                buyers[item][save.name] = 0
            buyers[item][save.name] += 1



print("Role purchase Percents")
for role, purchases in role_purchases.items():
    role = str(role)
    print(f"{role.capitalize()}:")
    purchases = calculate_percentages(purchases, True)
    purchases = sort(purchases)
    for item, count in purchases.items():
        print(f"- {id_to_name[item]}: {count}%")

