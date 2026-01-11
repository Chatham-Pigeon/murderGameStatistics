from math import floor
from math import ceil
from helper_functions import sort
def role_data(player_count):
    role_dictionary = {'traitor': max(1, floor(player_count / 4.5)), 'detective': max(1, floor(player_count / 8))}
    if player_count >= 6:
        role_dictionary['doctor'] = max(1, floor(player_count / 6))
    if player_count >= 5:
        role_dictionary['accomplice'] = max(1, ceil(player_count / 14))
    if player_count >= 7:
        role_dictionary['fiend'] = max(1, min(floor(player_count / 7), 3))
    role_count = 0
    for role, count in role_dictionary.items():
        role_count = role_count + count
    role_dictionary['innocent'] = player_count - role_count
    return role_dictionary

for i in range(3, 31):
    print(f"{i}.{sort(role_data(i))}")
