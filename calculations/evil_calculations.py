def calculate_percentages(items):
    new_percentages = {}
    total = sum(value for value in items.values())
    for key, value in items.items():
        new_percentages[key] = round((value / total) * 100, 2)
    return new_percentages
def sort(items):
    return dict(sorted(items.items(), key=lambda x: x[1], reverse=True))
def parse_message(parsed_message: str):
    parse_alive = True
    if " (dead)" in parsed_message:
        parsed_message = parsed_message.replace(" (dead)", "")
        parse_alive = False
    parsed_message = parsed_message.split(" ")
    parse_data_version = parsed_message.pop(0).replace("(", "").replace(")", "")
    parsed_message.pop(0)
    parsed_message.pop(0)
    parse_name = parsed_message.pop(0).removesuffix(":")
    parsed_message = " ".join(parsed_message)
    return parse_data_version, parse_name, parsed_message.replace("\n", ""), parse_alive

game_version = "1.0"
common_words = {}
with (open(fr'C:\Users\jacta\PycharmProjects\PythonProject1\data\{game_version}.evil_data.txt', 'r', encoding='utf-8', errors='replace') as file):
    for i in file:
        data_version, name, message, dead = parse_message(i)
        for word in message.split(" "):
            if word not in common_words:
                common_words[word] = 0
            common_words[word] += 1
print(sort(common_words))