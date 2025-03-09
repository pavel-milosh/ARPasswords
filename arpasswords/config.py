import json
import dataclasses


@dataclasses.dataclass
class TelegramConfig:
    token: str


def _config() -> dict[str, ...]:
    return json.load(open("config.json"))


def telegram() -> TelegramConfig:
    return TelegramConfig(**_config()["telegram"])
