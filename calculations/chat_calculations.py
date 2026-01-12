from helper_functions import sort, sort_dict_by_nested_value, sort_dict_by_key, calculate_percentages
class log:
    def __init__(self, raw_data: str):
        self.state = None
        self.message = None
        self.name = None
        self.gameRound = None
        self.timestamp = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")

log_name = "chat"
time = "30d"
with open(fr'../data/{time}.{log_name}-data.txt', 'r', encoding='utf-8', errors='replace') as file:
    for line in file:
        chat = log(line)
        with open('file', 'a', encoding='utf-8', errors='replace') as file2:
            file2.write(f"({chat.state}) {chat.name}: {chat.message}\n")
print("done")
