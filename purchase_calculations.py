def calculate_percentages(items):
    new_percentages = {}
    total = sum(value for value in items.values())
    for key, value in items.items():
        new_percentages[key] = (value / total) * 100
    return new_percentages
def sort(items):
    return dict(sorted(items.items(), key=lambda x: x[1], reverse=True))

with (open('purchases.txt', 'r') as file):
    item_count = {}
    for i in file:
        role = i.strip().split(":").pop(0)
        bought_items = i.strip().split(":")[1].split(" ")
        if role in ['detective']:
            if len(bought_items) >= 2:
                item = bought_items[1]
                if item in ['']:
                    continue
                if item in item_count:
                    item_count[item] = item_count[item] + 1
                else:
                    item_count[item] = 1

item_count = dict(sorted(item_count.items(), key=lambda x: x[1], reverse=True))
print(item_count)
percentages = dict(sorted(calculate_percentages(item_count).items(), key=lambda x: x[1], reverse=True))
print(percentages)

