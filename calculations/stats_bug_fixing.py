
class log:
    def __init__(self, raw_data: str):
        self.bowsShot = 0
        self.bowsLanded = 0
        self.timeAlive = 0
        self.role = None
        self.gameRound = None
        self.timestamp = None
        self.winTeam = None
        self.name = None
        self.alive = None
        self.won = None
        raw_data = raw_data.removesuffix("\n").split(";")
        for i in raw_data:
            key, value = i.split(":")
            if value.isdigit():
                setattr(self, key, int(value))
            else:
                setattr(self, key, f"{value}")


log_name = "player-stats"
time = "2w"
bugged_rounds = [85655,
85654,
85650,
85649,
85639,
85636,
85629,
85626,
85619,
85612,
85610,
85609,
85587,
85577,
85571,
85563,
85558,
85555,
85554,
85538,
85531,
85526,
85512,
85467,
85462,
85458,
85449,
85448,
85446,
85445,
85443,
85434,
85433,
85425,
85420,
85415,
85400,
85393,
85388,
85386]
player_to_uuid = {
    "LFabio_3": "ade4abd5-d190-4ac9-b66d-02631d43194e",
    "soundsofsci": "1757386b-094d-44fd-8c57-dcac904942e3",
    "MacroSwitcheado": "a7cd458a-2a6f-4563-a591-f7dfa81186fb",
    "Nickiskools": "709fe766-d495-472c-ac29-e6a51d6d6821",
    "x40cc": "d6af7704-a07c-444e-bac9-4466dfea1e1e",
    "Killer77Kat": "4ef6aa12-91c3-45b4-a252-7a3ede2e5dc7",
    "SoulessCat": "262b0c40-7b10-4fc9-bf23-cd8a51c5cffd",
    "Mlgrd": "ff8da0b1-d837-44f1-8a54-d8ca6f6b90fc",
    "ThatOneSkyGuy": "ff2bdeb0-3cdb-4a5b-a5f5-b87fbd0254c1",
    "Peaceify": "a75a0112-ba3b-4a9c-bce6-18c2b0c67555",
    "ayoshh": "5900fbdd-f404-48f9-9114-6d73baa64e48",
    "Darqnt": "b0adbf04-2eb7-401d-8ee6-1a2d5428925a",
    "Traif": "77248471-c3b2-4467-bb31-e8ca9ceae08c",
    "JJJT": "dbf4cd1c-051b-483a-b0b4-3288edfc9f3e",
    "pl4yr": "17e305e8-a0ce-4e3b-85dc-8f46dff39e14",
    "Emayeah": "5d2fb96d-5236-4f2e-b5e2-9eea6414d6d4",
    "ghostlykiss": "156934d9-7547-49e2-86d5-598e244eac24",
    "AKAN5": "93a4b4a2-0f67-4fbb-af73-231d2ed50fbd",
    "DiamondGamer4Ev": "5532d637-ac81-452a-893e-a4c8d5d040ba",
    "Agentfennec": "a4a2dabb-9076-4db1-a731-940c77b832b9",
    "FGHydro": "3ba86ce3-2f9a-461c-a02d-cdce05b7c946",
    "WrongTeacher822": "4da3465f-eb96-4df9-946c-e13540369223",
    "This_isabadname": "3f9592b5-b4bd-47ad-bb57-364098db3216",
    "nvct": "790eea8f-5865-49a2-a027-3ecdbc35befc",
    "iceaxe789": "3bc0d39c-06ac-41e3-b569-6a97da748178",
    "MindTrixxx": "794f9f2f-a28c-4a20-bd0b-cb858ad0250a",
    "glostone": "e03bc95e-6e73-44b8-a3c5-494fd10d9407",
    "Chatham_Pigeon": "8ce80d82-9aad-46c8-9754-0ba0165583d6",
    "Petrowo": "03781219-ef50-40c5-b610-a6918e4c5f1c",
    "splat_deluxe": "24b699ac-fd40-4c10-9cf8-64cbd41e2c97",
}
with open(fr'../data/{time}.{log_name}-data.txt', 'r', encoding='utf-8') as f:
    seen_bugged_rounds = []
    players_bugged = {}
    for line in f:
        stats = log(line)
        if int(stats.gameRound) in bugged_rounds:
            if not int(stats.gameRound) in seen_bugged_rounds:
                if stats.role == "fiend":
                    if not stats.name in players_bugged:
                        players_bugged[stats.name] = 0
                    players_bugged[stats.name] += 3
                    seen_bugged_rounds.append(int(stats.gameRound))
result = ""
for player, extra_wins in players_bugged.items():
    result = result + f"{player_to_uuid[player]}:{extra_wins},"
print(result)
print(len(result))

