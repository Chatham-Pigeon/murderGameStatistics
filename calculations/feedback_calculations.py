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
time = "365d"
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
votes = {'2Fort': 5.21, 'Abandoned Factory': 21.51, 'Abandoned Prison': 7.25, 'Barclays Bank': 11.13, 'Behind The Waterfall': 21.3, 'Bowling Alley': 7.91, 'Bunker 83': 9.98, 'Cliffside Mansion': 5.5, 'Cosmic Encounter': 8.88, 'Electrical Station': 9.34, 'Emberwoods': 14.02, 'Fiend Casino': 9.49, 'Forest Mansion': 6.51, 'Glacial Grotto': 10.53, 'Haunted Hotel': 6.79, 'Highrise': 29.04, 'IKEAâ„¢': 12.36, 'Impoverished Domicile': 8.55, 'Japanese Estate': 33.59, 'Mediterranean': 8.35, 'Moon Base': 8.92, 'Northorn Mansion': 9.76, 'Office': 5.74, 'Oil Rig': 18.15, 'Old Bunker': 8.21, 'Overgrown City': 6.02, 'Overgrown Site': 7.21, 'Seaside': 13.07, 'Subway Station': 7.85, 'Temple of KING Sr.': 5.25, 'The Aquarium': 15.45, 'The Brigade': 17.86, 'The Commons': 10.19, 'The Depths': 10.39, 'The Last Duel': 12.75, 'The Mall': 12.04, 'The Mineshafts': 10.6, 'The Trials': 15.78, 'Tropics': 16.72, 'Walmar Street': 20.56}
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
            pass
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
            print(f"\- {rating}: {round(feedbackDict[rating], 2)}")
        print(f"- Total: {map_feedback[map_name]['total']}")
        print(f"- Valid total: {len(map_feedback[map_name][rating])}")
        print(f"- Valid percent: {round(len(map_feedback[map_name][rating]) / map_feedback[map_name]['total'] * 100, 2)}%")
        print(f"\- Percent of the time map is selected when available: {votes[map_name]}%")
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








