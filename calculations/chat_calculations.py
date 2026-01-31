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
    yappers = {}
    words = {}
    people = []
    for line in file:
        chat = log(line)
        if not chat.name in yappers:
            yappers[chat.name] = 0
        yappers[chat.name] += 1
        chat.message = str(chat.message)
        split_chat = chat.message.split(" ")
        for word in split_chat:
            if not word in words:
                words[word] = 0
            words[word] += 1
        if chat.name not in people:
            people.append(chat.name)
    yapped_about = {}
with open(fr'../data/{time}.{log_name}-data.txt', 'r', encoding='utf-8', errors='replace') as file:
    for line2 in file:
        chat = log(line2)
        chat.message = str(chat.message)
        split_chat = chat.message.split(" ")
        for word in split_chat:
            if word in people:
                if word not in yapped_about:
                    yapped_about[word] = 0
                yapped_about[word] += 1
#print(f"Biggest yappers: {sort(yappers)}")
#print(f"Most popular words {sort(words)}")
print(sort(yapped_about))
print(f"People talking: {len(people)}")
