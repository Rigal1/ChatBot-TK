import os

def load_env_file(path):
    with open(path, "r") as f:
        env = f.read().split("\n")
    return env

def load_env(path):
    if not os.path.exists(path):
        return {}
    env_file = load_env_file(path)
    env = {}
    for line in env_file:
        if line == "":
            continue
        key, value = line.split(":")
        env[key] = value
    return env
        
