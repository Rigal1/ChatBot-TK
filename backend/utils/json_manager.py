import json

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        get_dict = json.load(f)
    return get_dict
