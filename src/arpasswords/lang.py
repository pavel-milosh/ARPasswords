import asyncio
import gettext
import os
from typing import Any


TRANSLATIONS: dict[str, Any] = {}


def _get_translation(file: str) -> Any:
    folder: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")
    lang: str = "en" if file == "main_logger" else "ru"
    if file not in TRANSLATIONS:
        TRANSLATIONS[file] = gettext.translation(file, folder, languages=[lang], fallback=True)
    return TRANSLATIONS[file]


def _text(file: str, code: str | None = None) -> Any:
    translation: Any = _get_translation(file)
    if code is None:
        return translation
    return translation.gettext(code)


async def _(file: str, code: str | None = None) -> Any:
    return await asyncio.to_thread(_text, file, code)
