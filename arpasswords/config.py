import json


def _() -> dict[str, str]:
    return json.load(open("config.json"))
