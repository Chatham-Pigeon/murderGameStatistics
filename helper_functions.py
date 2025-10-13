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
