import json
from functools import lru_cache

@lru_cache
def load_config():
    with open("config/config.json", "r") as f:
        return json.load(f)
