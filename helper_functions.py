import re
import config


def get_last_message(channel_id: int):
    with open(r"C:\Users\jacta\PycharmProjects\PythonProject1\lastseen.txt", 'r') as file:
        for line in file:
            line = line.split(":")
            if int(line[0]) == channel_id:
                return int(line[1])
    return 0

def set_last_message(channel_id: int, message_id: int):
    saved_last_seen = {}
    with open(r"C:\Users\jacta\PycharmProjects\PythonProject1\lastseen.txt", 'r') as file:
        for line in file:
            line = line.split(":")
            saved_last_seen[int(line[0])] = int(line[1])
    saved_last_seen[int(channel_id)] = message_id
    print(f"LAST SEEN ALL B4 SAVED {saved_last_seen}")
    file2: file
    with open(fr'C:\Users\jacta\PycharmProjects\PythonProject1\lastseen.txt', 'w') as file2:
        for new_channel_id, new_message_id in saved_last_seen.items():
            file2.writelines(f'{new_channel_id}:{new_message_id}\n')
def check_char(checkchar: str, time):
    #3d12h32m
    length = []
    # long ass string,,,, convert time (list) to concated string,,
    # partition that (get all content from before the time character was seen)
    # reverse the list so we track upwards TOWARDS the time
    idx = 0
    for char2 in "".join(reversed("".join(time).partition(checkchar)[0])):
        # if the character seen is numeric, add it to the list of numbers
        idx = idx + 1
        if char2.isnumeric():
            length.append(char2)
        else:
            break
    try:
        return int("".join(reversed(length)))
    except:
        return 0
def parsetime(time: str):
    #3d12h32m
    seconds_time = 0
    time: str = re.sub(r'(\d+[a-zA-Z])[a-zA-Z]+', r'\1', time) # ai generated regex :(
    time: list = list(time)
    idx = 0
    for char in time:
        if char in config.times.keys():
            length = check_char(char, time)
            seconds_time = seconds_time + (length * config.times[char])
        idx = idx + 1
    return seconds_time