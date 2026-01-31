import SECRETS
from SECRETS import valid_feedback
from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.name = None
        self.map = None
        self.overall = None
        self.gameplay = None
        self.visuals = None
        self.gameRound = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")
log_name = "feedback"
time = "30d"
builders = {
    "Old Bunker": ["Sagittarixie"],
    "Haunted Hotel": ["StardustGemini"],
    "Subway Station": ["KabanFriends", "Powercyphe"],
    "Bowling Alley": ["endersaltz"],
    "Tropics": ["ninja70707"],
    "The Mall": ["Benneze"],
    "Mediterranean": ["ninja70707"],
    "Overgrown City": ["Och0"],
    "The Aquarium": ["Chatham_Pigeon"],
    "Walmar Street": ["Powercyphe"],
    "IKEAâ„¢": ["InfinityWorks"],
    "Behind The Waterfall": ["Powercyphe", "Legendarial"],
    "Office": ["The_Blue_Friend"],
    "Moon Base": ["Sagittarixie"],
    "Bunker 83": ["endersaltz", "ACraftingFish"],
    "Electrical Station": ["Sagittarixie", "The_Blue_Friend"],
    "The Commons": ["Sagittarixie"],
    "Emberwoods": ["Sagittarixie"],
    "Temple of KING Sr.": ["nvct"],
    "Impoverished Domicile": ["nvct"],
    "2Fort": ["redstonae"],
    "Fiend Casino": ["StardustGemini"],
    "Cliffside Mansion": ["Euws"],
    "Forest Mansion": ["Farbschaf"],
    "The Depths": ["nvct"],
    "The Mineshafts": ["TeamF"],
    "Cosmic Encounter": ["Diglett_go", "Killer77Kat"],
    "Oil Rig": ["nvct"],
    "The Brigade": ["nvct"],
    "The Trials": ["nvct"],
    "Abandoned Prison": ["JJJT", "Luxwind_"],
    "Highrise": ["Brxzillian"],
    "Seaside": ["Brxzillian"],
    "Japanese Estate": ["FigtheFruit"],
    "Glacial Grotto": ["Brxzillian"],
    "Overgrown Site": ["Brxzillian"],
    "Northorn Mansion": ["Brxzillian"],
    "Abandoned Factory": ["Farbschaf"],
    "Barclays Bank": ["TeamF"],
    "The Last Duel": ["nvct"]
}
votes = {'2Fort': 5.39, 'Abandoned Factory': 19.15, 'Abandoned Prison': 9.1, 'Barclays Bank': 8.92, 'Behind The Waterfall': 20.7, 'Bowling Alley': 9.92, 'Bunker 83': 9.77, 'Cliffside Mansion': 4.39, 'Cosmic Encounter': 10.09, 'Electrical Station': 7.66, 'Emberwoods': 12.51, 'Fiend Casino': 11.45, 'Forest Mansion': 11.06, 'Glacial Grotto': 11.73, 'Haunted Hotel': 6.24, 'Highrise': 26.16, 'IKEAâ„¢': 16.28, 'Impoverished Domicile': 9.4, 'Japanese Estate': 32.23, 'Mediterranean': 6.61, 'Moon Base': 9.63, 'Northorn Mansion': 8.6, 'Office': 6.47, 'Oil Rig': 19.85, 'Old Bunker': 9.68, 'Overgrown City': 6.13, 'Overgrown Site': 5.5, 'Seaside': 11.21, 'Subway Station': 5.39, 'Temple of KING Sr.': 7.16, 'The Aquarium': 11.61, 'The Brigade': 16.93, 'The Commons': 8.62, 'The Depths': 9.92, 'The Last Duel': 16.82, 'The Mall': 10.43, 'The Mineshafts': 14.96, 'The Trials': 20.5, 'Tropics': 12.99, 'Walmar Street': 24.33}
ratings = ['gameplay', 'visuals', 'overall']

with open(fr'../data/{time}.{log_name}-data.txt', 'r') as file:
    raters = {}
    map_feedback = {}
    for line in file:
        # loop variable initiations
        feedback = log(line)
        if not feedback.map in map_feedback:
            map_feedback[feedback.map] = {"visuals": [], "gameplay": [], "overall": [], "total": 0}
            raters[feedback.map] = []
        map_feedback[feedback.map]['total'] += 1

        # ensuring valid feedback
        if not valid_feedback(feedback):
            continue
        # if player did not rate all 3 choices, don't use feedback
        if feedback.visuals == 0 or feedback.gameplay == 0 or feedback.overall == 0:
            continue
        # if player built the map, do not use feedback
        if feedback.name in builders[feedback.map]:
            continue
        # ignore feedback from players who already rated (users most recent rating will be used)
        if feedback.name in raters[feedback.map]:
            continue

        # feedback is valid, continue with code
        raters[feedback.map].append(feedback.name)
        for rating in ratings:
            map_feedback[feedback.map][rating].append(getattr(feedback, rating))

total = 0
valid_total = 0
map_feedback_avgs = {}
#calculate averages
for map_name, feedbackDict in map_feedback.items():
    map_feedback_avgs[map_name] = {"visuals": 0, "gameplay": 0, "overall": 0}
    for rating in ratings:
        map_feedback_avgs[map_name][rating] = sum(feedbackDict[rating]) / len(feedbackDict[rating])
    total += feedbackDict['total']
    valid_total += len(map_feedback[map_name][rating])


# sort, calculate, display averages + other info map specfic
for rating in ratings:
    print(f"\n**Top 3 maps for {rating.capitalize()}**")
    idx = 0
    sort_key = rating
    map_feedback_avgs = sort_dict_by_nested_value(map_feedback_avgs, sort_key)
    for map_name, feedbackDict in map_feedback_avgs.items():
        idx += 1
        print(f"{idx}. {map_name}:")
        for rating in ratings:
            print(f"- {rating}: {round(feedbackDict[rating], 2)}")
        #print(f"- Total: {map_feedback[map_name]['total']}")
        #print(f"- Valid total: {len(map_feedback[map_name][rating])}")
        #print(f"- Valid percent: {round(len(map_feedback[map_name][rating]) / map_feedback[map_name]['total'] * 100, 2)}%")
        print(f"- Percent of the time map is selected when available: {votes[map_name]}%")
        if idx >= 3:
            pass
# overall avg + other ifo
print("Overall: ")
for rating in ratings:
    combined = 0
    for feedbackDict in map_feedback.values():
        combined += sum(feedbackDict[rating])
    print(f"- {rating}: {round(combined / valid_total, 2)}")
print(f"- Total: {total}")
print(f"- Valid total: {valid_total}")
print(f"- Valid percent: {round(valid_total / total * 100, 2)}%")








