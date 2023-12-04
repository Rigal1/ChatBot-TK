from backend.utils import json_manager

def save_parameter(data, path):
    json_manager.save_json(data, path)

def load_parameter(path):
    return json_manager.load_json(path)
        