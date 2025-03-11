import json


def _() -> dict[str, ...]:
    return json.load(open("config.json"))
