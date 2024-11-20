import json


def load_paifu(file):
    with open(file) as f:
        json_data = json.load(f)
    return json_data


def get_game_info(json_data):
    game_info = {"max_kyoku_num": 0, "player_names": {}, "gameid": None}
    for entry in json_data:
        if entry["cmd"] == "gamestart":
            game_info["gameid"] = entry["args"][0][3:]
        elif entry["cmd"] == "player":
            game_info["player_names"][entry["args"][0]] = entry["args"][1]
        elif entry["cmd"] == "kyokustart":
            game_info["max_kyoku_num"] += 1
    return game_info


def extract_one_kyoku(json_data, kyoku_num):
    def count_kyoku(json_data):
        count = 0
        for entry in json_data:
            if entry["cmd"] == "kyokustart":
                count += 1
        return count

    max_kyoku_num = count_kyoku(json_data)
    if kyoku_num < 0:
        raise ValueError(f"kyoku_num: {kyoku_num} must be larger than 0.")
    elif max_kyoku_num <= kyoku_num:
        raise ValueError(f"kyoku_num: {kyoku_num} is too large.")

    kyoku_num += 1
    kyoku = []
    for entry in json_data:
        if entry["cmd"] == "kyokustart":
            kyoku_num -= 1
            if kyoku_num == 0:
                kyoku.append(entry)
        elif kyoku_num == 0:
            kyoku.append(entry)
            if entry["cmd"] == "kyokuend":
                break
    return kyoku
