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
log_name = "player-stats"
time = "30d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    counts = {}
    role_purchases = {}
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
                continue
            if not item in role_purchases[save.role]:
                role_purchases[save.role][item] = 0
            role_purchases[save.role][item] += 1
        if not save.purchases[0] == '':
            print(save.purchases)
for role, purchases in role_purchases.items():
    print(f"{role}:")
    purchases = calculate_percentages(purchases, True)
    purchases = sort(purchases)
    for item, count in purchases.items():
        print(f"- {item}: {count}")
