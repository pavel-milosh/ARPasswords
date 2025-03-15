import asyncio
import gettext
from typing import Any


LANG: str = "ru"
TRANSLATIONS: dict[str, Any] = {}


def _get_translation(file: str) -> Any:
    if file not in TRANSLATIONS:
        TRANSLATIONS[file] = gettext.translation(file, "locales", languages=[LANG], fallback=True)
    return TRANSLATIONS[file]


def _c_(file: str, code: str | None = None) -> Any:
    translation: Any = _get_translation(file)
    if code is None:
        return translation
    return translation.gettext(code)


async def _(file: str, code: str | None = None) -> Any:
    return await asyncio.to_thread(_c_, file, code)
