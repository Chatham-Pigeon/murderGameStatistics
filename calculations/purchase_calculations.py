
def calculate_percentages(items):
    new_percentages = {}
    total = sum(value for value in items.values())
    for key, value in items.items():
        new_percentages[key] = round((value / total) * 100, 2)
    return new_percentages
def sort(items):
    return dict(sorted(items.items(), key=lambda x: [1], reverse=True))
# 45503
idx = 0
game_version = "1.0"
with (open(fr'C:\Users\jacta\PycharmProjects\PythonProject1\data\{game_version}.purchases.txt', 'r') as file):
    role_purchases = {}
    for i in file:
        idx = idx + 1
        role = i.strip().split(":").pop(0)
        bought_items = i.strip().split(":")[1].split(" ")
        if role not in role_purchases:
            role_purchases[role] = {}
        if bought_items == ['']:
            pass
        for item in bought_items:
            if item in role_purchases[role]:
                role_purchases[role][item] += 1
            else:
                role_purchases[role][item] = 1



for role, purchases in role_purchases.items():
    print(f"{role}: {dict(sorted(calculate_percentages(purchases).items(), key=lambda x: x[1], reverse=True))}")
