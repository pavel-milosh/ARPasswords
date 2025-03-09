import json
import os
import dataclasses

from aiogram.types import BotCommand


def _localization() -> dict[str, ...]:
    # TODO: Add different languages
    return json.load(open(os.path.join("localizations", "ru.json")))


empty: str = _localization()["empty"]


@dataclasses.dataclass
class AddPassword:
    initial: str
    enter_password: str
    info_: str


    def info(
            self,
            label: str,
            password: str,
            url: str | None,
            totp: str | None,
            backup_codes: list[str] | None,
    ) -> str:
        if url is None:
            url = empty
        if totp is None:
            totp = empty
        if backup_codes is None:
            backup_codes = empty
        else:
            backup_codes = json.dumps(backup_codes)
        return (self.info_.replace("[LABEL]", label)
                .replace("[PASSWORD]", password)
                .replace("[URL]", url)
                .replace("[TOTP]", totp)
                .replace("[BACKUP_CODES]", backup_codes))


@dataclasses.dataclass
class GeneratePassword:
    initial_: str
    generating: str
    delete: str


    def initial(self, password: str) -> str:
        return self.initial_.replace("[PASSWORD]", password)


@dataclasses.dataclass
class Key:
    initial: str
    incorrect: str
    deleting_: str
    done: str


    def deleting(self, key: str) -> str:
        return self.deleting_.replace("[KEY]", key)


# noinspection PyTypeChecker
commands: list[BotCommand] = [
    BotCommand(command=key, description=value)
    for key, value in _localization()["commands"].items()
]
generate_password: GeneratePassword = GeneratePassword(
    **_localization()["generate_password"]
)
key: Key = Key(**_localization()["key"])
add_password: AddPassword = AddPassword(**_localization()["add_password"])

def start(name: str) -> str:
    return _localization()["start"].replace("[NAME]", name)