import gettext


LANG: str = "ru"
TRANSLATIONS: dict[str, ...] = {}


def _get_translation(file: str) -> ...:
    if file not in TRANSLATIONS:
        TRANSLATIONS[file] = gettext.translation(file, "locales", languages=[LANG], fallback=True)
    return TRANSLATIONS[file]


def _(file: str, code: str | None = None) -> ...:
    translation: ... = _get_translation(file)
    if code is None:
        return translation
    return translation.gettext(code)