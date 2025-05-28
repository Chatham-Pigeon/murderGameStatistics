item_count = {}
percentages = {}

def calculate_percentages(bought_items):
    total = sum(value for value in bought_items.values())
    for key, value in bought_items.items():
        percentages[key] = (value / total) * 100
    return percentages

with (open('purchases.txt', 'r') as file):
    none = 0
    two = 0
    one = 0
    for i in file:
        i = i.strip()
        split_i = i.split(":")
        role = split_i.pop(0)
        bought_items = split_i[0].split(" ")
        if role in ['traitor']:
            if len(bought_items) == 0:
                none = none + 1
            elif len(bought_items) == 2:
                one = one + 1
            else:
                two = two + 1
                item = bought_items[0]
                if item in ['']:
                    continue
                if item in item_count:
                    item_count[f'{item}'] = item_count[f'{item}'] + 1
                else:
                    item_count[f'{item}'] = 1
            percentages = calculate_percentages(item_count)
item_count = dict(sorted(item_count.items(), key=lambda x: x[1], reverse=True))
print(item_count)
percentages = dict(sorted(percentages.items(), key=lambda x: x[1], reverse=True))
print(percentages)
print(f"{none} {one} {two}")
