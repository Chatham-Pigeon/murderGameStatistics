


def calculate_percentages(items, should_round: bool = False):
    new_percentages = {}
    total = sum(value for value in items.values())
    if total == 0:
        for key in items:
            new_percentages[key] = 0
        return new_percentages
    for key, value in items.items():
        new_percentages[key] = (value / total) * 100
        if should_round:
            new_percentages[key] = round(new_percentages[key], 2)

    return new_percentages
def sort(items, reverse = True):
    return dict(sorted(items.items(), key=lambda x: x[1], reverse=reverse))
def sort_dict_by_key(meow, reverse = True):
    return dict(sorted(meow.items(), reverse=reverse))
def sort_dict_by_nested_value(items, key, reverse=True):
    return dict(sorted(items.items(), key=lambda x: x[1].get(key, 0), reverse=reverse))
def formatted_win_rates(items):
    return ", ".join(f"{role}: {percent}%" for role, percent in calculate_percentages(items, True).items())

def join_with_final(lst, sep=", ", final=" and "):
    if len(lst) <= 1:
        return "".join(lst)
    return sep.join(lst[:-1]) + final + lst[-1]
