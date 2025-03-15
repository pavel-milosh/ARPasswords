import json


def _() -> dict[str, str | list[str]]:
    return json.load(open("config.json"))
