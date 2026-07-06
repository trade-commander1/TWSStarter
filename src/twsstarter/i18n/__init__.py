from __future__ import annotations
from twsstarter.i18n.strings import STRINGS, LANGUAGES

_lang: str = 'en'


def set_language(code: str) -> None:
    # LANGUAGES is the supported set (the languages TWS ships in); STRINGS may
    # still hold data for others, but only LANGUAGES entries are selectable.
    global _lang
    _lang = code if code in LANGUAGES else 'en'


def detect_language() -> str:
    try:
        from PyQt6.QtCore import QLocale
        prefix = QLocale.system().name().split('_')[0]
    except Exception:
        return 'en'
    return prefix if prefix in LANGUAGES else 'en'


def current() -> str:
    return _lang


def tr(key: str, **kwargs) -> str:
    text = STRINGS.get(_lang, {}).get(key) or STRINGS['en'].get(key, key)
    return text.format(**kwargs) if kwargs else text
