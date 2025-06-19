# utils/file_manager.py

import json
import os

def load_json(filename: str, default: dict = {}) -> dict:
    path = f"data/{filename}"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=4)
        return default
    with open(path, "r") as f:
        return json.load(f)

def save_json(filename: str, data: dict):
    path = f"data/{filename}"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
